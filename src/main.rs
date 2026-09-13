use arrow_array::{Array, Float64Array, UInt64Array};
use icebug_algorithms::*;
use icebug_core::{Edge, ExecutionContext, NodeId, from_edges};
use std::{fs, io::Write, time::Instant};
fn main() -> Result<(), Box<dyn std::error::Error>> {
    let a: Vec<String> = std::env::args().collect();
    if !(5..=6).contains(&a.len()) {
        return Err(
            "usage: BENCH INPUT.txt|IPC_DIR ALGORITHM OUTPUT.bin SOURCE [NEW_IPC_DIR]".into(),
        );
    }
    let ctx = ExecutionContext::default();
    let g = if std::path::Path::new(&a[1]).is_dir() {
        let dir = std::path::Path::new(&a[1]);
        let tables = grustcat::ArrowGraph::read_ipc(
            fs::File::open(dir.join("nodes.arrow"))?,
            fs::File::open(dir.join("edges.arrow"))?,
        )?;
        grustcat::icebug_from_arrow(&tables, Some("weight"), &ctx)?
    } else {
        let input = fs::read_to_string(&a[1])?;
        let mut t = input.split_whitespace();
        let n: usize = t.next().ok_or("missing n")?.parse()?;
        let m: usize = t.next().ok_or("missing m")?.parse()?;
        let mut edges = Vec::with_capacity(m);
        for _ in 0..m {
            edges.push(Edge {
                source: t.next().ok_or("source")?.parse()?,
                target: t.next().ok_or("target")?.parse()?,
                weight: t.next().ok_or("weight")?.parse()?,
            });
        }
        from_edges(n, true, true, &edges)?
    };
    let g = g.prepare_incoming(&ctx)?;
    let n = g.node_count();
    if let Some(dir) = a.get(5) {
        fs::create_dir(dir)?;
        let dir = std::path::Path::new(dir);
        grustcat::arrow_from_icebug(&g)?.write_ipc(
            fs::File::create(dir.join("nodes.arrow"))?,
            fs::File::create(dir.join("edges.arrow"))?,
        )?;
    }
    let source = NodeId(a[4].parse()?);
    let mut reachable = 0u64;
    let mut path_entries = 0u64;
    let mut node_sum = 0u64;
    let mut cost_sum = 0.;
    let mut consume = |nodes: &[u64], costs: &[f64]| {
        reachable += 1;
        path_entries += nodes.len() as u64;
        node_sum += std::hint::black_box(nodes).iter().sum::<u64>();
        cost_sum += std::hint::black_box(costs).iter().sum::<f64>();
    };
    let start = Instant::now();
    let mut iterations = 0;
    let batch = match a[2].as_str() {
        "bfs" => bfs(&g, source, &ctx)?,
        "dijkstra-full" => dijkstra_paths(&g, source, &ctx, &mut consume)?,
        "dijkstra" => dijkstra(&g, source, &ctx)?,
        "wcc" => weakly_connected_components(&g, &ctx)?,
        "scc" => strongly_connected_components(&g, &ctx)?,
        "pagerank" => {
            let r = pagerank(&g, &PageRankOptions::default(), &ctx)?;
            iterations = r.iterations;
            if !r.converged {
                return Err("PageRank failed to converge".into());
            }
            r.scores
        }
        _ => return Err("unknown algorithm".into()),
    };
    let ms = start.elapsed().as_secs_f64() * 1000.;
    let col = batch.column(1);
    let values: Vec<f64> = if let Some(v) = col.as_any().downcast_ref::<Float64Array>() {
        (0..n)
            .map(|i| if v.is_null(i) { -1. } else { v.value(i) })
            .collect()
    } else {
        let v = col
            .as_any()
            .downcast_ref::<UInt64Array>()
            .ok_or("bad type")?;
        (0..n).map(|i| v.value(i) as f64).collect()
    };
    let mut f = fs::File::create(&a[3])?;
    for x in values {
        f.write_all(&x.to_le_bytes())?;
    }
    println!(
        "{{\"ms\":{ms},\"iterations\":{iterations},\"reachable\":{reachable},\"path_entries\":{path_entries},\"node_sum\":{node_sum},\"cost_sum\":{cost_sum}}}"
    );
    Ok(())
}
