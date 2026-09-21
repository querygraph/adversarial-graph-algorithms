//! The `icecat` participant: the Rust rewrite of the NetworKit-derived kernels,
//! Arrow 59.3 buffers throughout. Its crates are named `icebug-*` for
//! compatibility; the lineage is Icebug (C++) then Icecat (this).
//!
//! It has no triangle kernel, so it runs PageRank, WCC and BFS only.

use std::time::Instant;

use arrow_array::{Array, Float64Array, UInt64Array};
use icebug_algorithms::{PageRankOptions, Personalization, bfs, pagerank, weakly_connected_components};
use icebug_core::{ExecutionContext, builder::Edge, builder::from_edges, graph::NodeId};

const PARTICIPANT: &str = "icecat";

fn read(path: &str) -> (usize, Vec<(u64, u64)>) {
    let text = std::fs::read_to_string(path).expect("fixture");
    let mut lines = text.lines();
    let mut header = lines.next().expect("header").split_whitespace();
    let nodes: usize = header.next().expect("nodes").parse().expect("nodes");
    let declared: usize = header.next().expect("edges").parse().expect("edges");
    let edges: Vec<(u64, u64)> = lines
        .filter(|line| !line.trim().is_empty())
        .map(|line| {
            let mut parts = line.split_whitespace();
            (parts.next().expect("source").parse().expect("source"),
             parts.next().expect("target").parse().expect("target"))
        })
        .collect();
    assert_eq!(edges.len(), declared, "fixture header disagrees with its body");
    (nodes, edges)
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.iter().any(|a| a == "--receipt") {
        println!(
            "{{\"participant\":\"{PARTICIPANT}\",\"version\":\"{}\",\"commit\":\"{}\",\
              \"precision\":\"f64\",\"algorithms\":[\"pagerank\",\"wcc\",\"bfs\"],\
              \"parallel\":\"sequential; the parallel feature is not enabled\",\"width_capable\":false}}",
            env!("CARGO_PKG_VERSION"), option_env!("BENCH_COMMIT").unwrap_or("unknown"));
        return;
    }
    let fixture = args.iter().position(|a| a == "--fixture").map(|i| args[i + 1].clone()).expect("--fixture");
    let algorithm = args.iter().position(|a| a == "--algorithm").map(|i| args[i + 1].clone()).expect("--algorithm");
    let max_iterations: usize = args.iter().position(|a| a == "--max-iterations")
        .map(|i| args[i + 1].parse().expect("--max-iterations")).unwrap_or(100);
    let tolerance: f64 = args.iter().position(|a| a == "--tolerance")
        .map(|i| args[i + 1].parse().expect("--tolerance")).unwrap_or(1e-10);

    let started = Instant::now();
    let (nodes, edges) = read(&fixture);
    let parse_ms = started.elapsed().as_secs_f64() * 1e3;

    // Generous: this participant's context is a memory ceiling, and a ceiling
    // that could fire would make the column a measurement of a limit.
    let context = ExecutionContext::new(usize::MAX);

    let started = Instant::now();
    let graph = from_edges(nodes, true, false,
        &edges.iter().map(|&(source, target)| Edge { source, target, weight: 1.0 }).collect::<Vec<_>>())
        .expect("graph");
    let build_ms = started.elapsed().as_secs_f64() * 1e3;

    // This participant's PageRank pulls, so it needs the reverse index. Other
    // participants build theirs inside the kernel or not at all, so the cost is
    // timed and reported on its own rather than hidden in either phase.
    let started = Instant::now();
    let graph = if algorithm == "pagerank" { graph.prepare_incoming(&context).expect("incoming") } else { graph };
    let incoming_ms = started.elapsed().as_secs_f64() * 1e3;

    let started = Instant::now();
    let (summary, materialise) = match algorithm.as_str() {
        "pagerank" => {
            let result = pagerank(&graph, &PageRankOptions {
                damping: 0.85, tolerance, max_iterations, personalization: Personalization::Uniform,
            }, &context).expect("pagerank");
            let kernel_ms = started.elapsed().as_secs_f64() * 1e3;
            let started = Instant::now();
            let column = result.scores.column(1).as_any().downcast_ref::<Float64Array>().expect("f64 scores");
            let scores: Vec<f64> = (0..column.len()).map(|i| column.value(i)).collect();
            let sum: f64 = scores.iter().sum();
            let (argmax, max) = scores.iter().enumerate()
                .fold((0usize, f64::MIN), |(bi, bv), (i, v)| if *v > bv { (i, *v) } else { (bi, bv) });
            (format!("\"kernel_ms\":{kernel_ms},\"iterations\":{},\"residual\":{},\"converged\":{},\
                      \"sum\":{sum},\"max\":{max},\"argmax\":{argmax}",
                     result.iterations, result.residual, result.converged),
             started.elapsed().as_secs_f64() * 1e3)
        }
        "wcc" => {
            let batch = weakly_connected_components(&graph, &context).expect("wcc");
            let kernel_ms = started.elapsed().as_secs_f64() * 1e3;
            let started = Instant::now();
            let column = batch.column(1).as_any().downcast_ref::<UInt64Array>().expect("u64 labels");
            let labels: Vec<u64> = (0..column.len()).map(|i| column.value(i)).collect();
            let distinct: std::collections::HashSet<_> = labels.iter().collect();
            (format!("\"kernel_ms\":{kernel_ms},\"count\":{},\"probe_label\":{}", distinct.len(), labels[0]),
             started.elapsed().as_secs_f64() * 1e3)
        }
        "bfs" => {
            let batch = bfs(&graph, NodeId(0), &context).expect("bfs");
            let kernel_ms = started.elapsed().as_secs_f64() * 1e3;
            let started = Instant::now();
            let column = batch.column(1);
            let distances: Vec<i64> = (0..column.len()).map(|i| {
                if column.is_null(i) { -1 } else {
                    column.as_any().downcast_ref::<UInt64Array>().map(|a| a.value(i) as i64)
                        .or_else(|| column.as_any().downcast_ref::<Float64Array>().map(|a| a.value(i) as i64))
                        .expect("distance column")
                }
            }).collect();
            let reached = distances.iter().filter(|d| **d >= 0).count();
            let total: i64 = distances.iter().filter(|d| **d > 0).sum();
            (format!("\"kernel_ms\":{kernel_ms},\"reached\":{reached},\"distance_sum\":{total}"),
             started.elapsed().as_secs_f64() * 1e3)
        }
        other => panic!("unknown or absent algorithm {other}"),
    };
    println!("{{\"participant\":\"{PARTICIPANT}\",\"algorithm\":\"{algorithm}\",\"fixture\":\"{fixture}\",\
               \"nodes\":{nodes},\"edges\":{},\"parse_ms\":{parse_ms},\"build_ms\":{build_ms},\"prepare_incoming_ms\":{incoming_ms},{summary},\
               \"materialise_ms\":{materialise},\"peak_bytes\":{}}}",
             edges.len(), context.peak_bytes());
}
