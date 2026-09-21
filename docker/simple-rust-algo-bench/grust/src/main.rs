//! The `grust` participant: Grust's own kernels over `GraphProjection`, direct,
//! with no procedure layer, no Cypher and no storage backend.
//!
//! The budget is deliberately unbounded here. Charging is part of what these
//! kernels do and stays on, but a limit that could fire would make the column a
//! measurement of a policy rather than of a kernel; the resources it did charge
//! are reported beside the result instead.

use std::time::Instant;

use grust_algorithms::{
    ExecutionContext, ExecutionLimits, GraphProjection, Orientation, ProjectionEdge,
    SnapshotIdentity, PageRankOptions, TriangleOptions, pagerank, triangles,
    weakly_connected_components,
};

const PARTICIPANT: &str = "grust";

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
              \"precision\":\"f64\",\"algorithms\":[\"pagerank\",\"wcc\",\"triangles\"],\
              \"parallel\":\"sequential unless with_concurrency is requested\",\"width_capable\":true}}",
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

    // Two distinct things could be called "sequential": concurrency unset, where
    // PageRank takes the push loop kept as the parallel path's oracle, and
    // concurrency 1, where it takes the pull kernel on one thread. They are
    // different algorithms, so the flag is explicit and the receipt records which.
    let concurrency: Option<usize> = args.iter().position(|a| a == "--concurrency")
        .map(|i| args[i + 1].parse().expect("--concurrency"));
    let mut context = ExecutionContext::new(ExecutionLimits {
        memory_bytes: usize::MAX,
        work_units: usize::MAX,
        batch_rows: 1 << 16,
        deadline: None,
    })
    .expect("execution context");
    if let Some(workers) = concurrency {
        context = context.with_concurrency(workers).expect("concurrency");
    }

    let started = Instant::now();
    let orientation = if algorithm == "triangles" { Orientation::Undirected } else { Orientation::Outgoing };
    let projection = GraphProjection::from_topology(
        SnapshotIdentity::new("fixture".into(), "r1".into(), "reader".into()).expect("identity"),
        (0..nodes).map(|node| format!("{node}").into()).collect(),
        edges.iter().enumerate()
            .map(|(ordinal, &(source, target))| ProjectionEdge { source, target, ordinal, id: None })
            .collect(),
        None,
        orientation,
        &context,
    )
    .expect("projection");
    let build_ms = started.elapsed().as_secs_f64() * 1e3;

    let started = Instant::now();
    let (summary, materialise) = match algorithm.as_str() {
        "pagerank" => {
            let result = pagerank(&projection, PageRankOptions {
                damping: 0.85, tolerance, max_iterations, personalization: None,
            }).expect("pagerank");
            let kernel_ms = started.elapsed().as_secs_f64() * 1e3;
            let started = Instant::now();
            let scores = result.values();
            let sum: f64 = scores.iter().sum();
            let (argmax, max) = scores.iter().enumerate()
                .fold((0usize, f64::MIN), |(bi, bv), (i, v)| if *v > bv { (i, *v) } else { (bi, bv) });
            (format!("\"kernel_ms\":{kernel_ms},\"iterations\":{},\"sum\":{sum},\"max\":{max},\"argmax\":{argmax}",
                     result.iterations()),
             started.elapsed().as_secs_f64() * 1e3)
        }
        "wcc" => {
            let result = weakly_connected_components(&projection).expect("wcc");
            let kernel_ms = started.elapsed().as_secs_f64() * 1e3;
            let started = Instant::now();
            let labels = result.values();
            let distinct: std::collections::HashSet<_> = labels.iter().collect();
            (format!("\"kernel_ms\":{kernel_ms},\"count\":{},\"probe_label\":{}", distinct.len(), labels[0]),
             started.elapsed().as_secs_f64() * 1e3)
        }
        "triangles" => {
            let result = triangles(&projection, TriangleOptions { max_degree: None }).expect("triangles");
            let kernel_ms = started.elapsed().as_secs_f64() * 1e3;
            (format!("\"kernel_ms\":{kernel_ms},\"triangles\":{}", result.triangle_count()), 0.0)
        }
        other => panic!("unknown algorithm {other}"),
    };
    let usage = context.usage().expect("usage");
    println!("{{\"participant\":\"{PARTICIPANT}\",\"algorithm\":\"{algorithm}\",\"fixture\":\"{fixture}\",\
               \"nodes\":{nodes},\"edges\":{},\"parse_ms\":{parse_ms},\"build_ms\":{build_ms},{summary},\
               \"materialise_ms\":{materialise},\"work_units\":{},\"peak_bytes\":{},\"concurrency\":{}}}",
             edges.len(), usage.work_units, usage.peak_bytes,
             concurrency.map(|w| w.to_string()).unwrap_or_else(|| "null".into()));
}
