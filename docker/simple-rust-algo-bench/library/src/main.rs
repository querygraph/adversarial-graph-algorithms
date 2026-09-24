//! The `neo4j-labs/graph` participant.
//!
//! Reads the shared fixture, builds the library's own CSR through its builder
//! API, and calls its kernels through `graph::prelude`. Parse, build, kernel and
//! materialisation are timed apart because a project that builds a faster
//! structure and a project that runs a faster kernel are different findings.

use std::time::Instant;

use graph::prelude::*;

const PARTICIPANT: &str = "library";

fn receipt() {
    // Versions come from the build rather than from a literal, so a dependency
    // bump cannot leave the receipt describing the previous binary.
    println!(
        "{{\"participant\":\"{PARTICIPANT}\",\"version\":\"{}\",\"commit\":\"{}\",\
          \"library\":\"graph {} / graph_builder {}\",\"precision\":\"f32\",\
          \"algorithms\":[\"pagerank\",\"wcc\",\"triangles\"],\"parallel\":\"rayon, library default\",\"width_capable\":true}}",
        env!("CARGO_PKG_VERSION"),
        option_env!("BENCH_COMMIT").unwrap_or("unknown"),
        env!("GRAPH_VERSION"),
        env!("GRAPH_BUILDER_VERSION"),
    );
}

fn read(path: &str) -> (usize, Vec<(usize, usize)>) {
    let text = std::fs::read_to_string(path).expect("fixture");
    let mut lines = text.lines();
    let mut header = lines.next().expect("header").split_whitespace();
    let nodes: usize = header.next().expect("nodes").parse().expect("nodes");
    let declared: usize = header.next().expect("edges").parse().expect("edges");
    let edges: Vec<(usize, usize)> = lines
        .filter(|line| !line.trim().is_empty())
        .map(|line| {
            let mut parts = line.split_whitespace();
            (
                parts.next().expect("source").parse().expect("source"),
                parts.next().expect("target").parse().expect("target"),
            )
        })
        .collect();
    assert_eq!(edges.len(), declared, "fixture header disagrees with its body");
    (nodes, edges)
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.iter().any(|a| a == "--receipt") {
        return receipt();
    }
    let fixture = args.iter().position(|a| a == "--fixture").map(|i| args[i + 1].clone()).expect("--fixture");
    let algorithm = args.iter().position(|a| a == "--algorithm").map(|i| args[i + 1].clone()).expect("--algorithm");
    let iterations: usize = args.iter().position(|a| a == "--max-iterations")
        .map(|i| args[i + 1].parse().expect("--max-iterations")).unwrap_or(100);
    let tolerance: f64 = args.iter().position(|a| a == "--tolerance")
        .map(|i| args[i + 1].parse().expect("--tolerance")).unwrap_or(1e-10);

    let started = Instant::now();
    let (nodes, edges) = read(&fixture);
    let parse_ms = started.elapsed().as_secs_f64() * 1e3;

    let started = Instant::now();
    let directed: DirectedCsrGraph<usize> = GraphBuilder::new()
        .csr_layout(CsrLayout::Sorted)
        .edges(edges.iter().copied())
        .build();
    let build_ms = started.elapsed().as_secs_f64() * 1e3;

    let started = Instant::now();
    let (summary, materialise) = match algorithm.as_str() {
        "pagerank" => {
            let config = PageRankConfig::new(iterations, tolerance, PageRankConfig::DEFAULT_DAMPING_FACTOR);
            let (scores, ran, error) = page_rank(&directed, config);
            let kernel_ms = started.elapsed().as_secs_f64() * 1e3;
            let started = Instant::now();
            let sum: f64 = scores.iter().map(|s| *s as f64).sum();
            let (argmax, max) = scores.iter().enumerate()
                .fold((0usize, f32::MIN), |(bi, bv), (i, v)| if *v > bv { (i, *v) } else { (bi, bv) });
            (format!("\"kernel_ms\":{kernel_ms},\"iterations\":{ran},\"error\":{error},\
                      \"sum\":{sum},\"max\":{max},\"argmax\":{argmax}"),
             started.elapsed().as_secs_f64() * 1e3)
        }
        "wcc" => {
            let components = wcc_afforest_dss(&directed, WccConfig::default());
            let kernel_ms = started.elapsed().as_secs_f64() * 1e3;
            let started = Instant::now();
            let labels: Vec<usize> = (0..nodes).map(|node| components.component(node)).collect();
            let distinct: std::collections::HashSet<_> = labels.iter().collect();
            (format!("\"kernel_ms\":{kernel_ms},\"count\":{},\"probe_label\":{}", distinct.len(), labels[0]),
             started.elapsed().as_secs_f64() * 1e3)
        }
        "triangles" => {
            let undirected: UndirectedCsrGraph<usize> = GraphBuilder::new()
                .csr_layout(CsrLayout::Deduplicated)
                .edges(edges.iter().copied())
                .build();
            let started = Instant::now();
            let total = global_triangle_count(&undirected);
            (format!("\"kernel_ms\":{},\"triangles\":{total}", started.elapsed().as_secs_f64() * 1e3), 0.0)
        }
        other => panic!("unknown algorithm {other}"),
    };
    println!("{{\"participant\":\"{PARTICIPANT}\",\"algorithm\":\"{algorithm}\",\"fixture\":\"{fixture}\",\
               \"nodes\":{nodes},\"edges\":{},\"parse_ms\":{parse_ms},\"build_ms\":{build_ms},\
               {summary},\"materialise_ms\":{materialise}}}", edges.len());
}
