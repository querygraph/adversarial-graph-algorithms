use arrow_array::{Array, Float64Array, UInt64Array};
use grustcat::{GrustGraph, grust};
use icebug_core::ExecutionContext;
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
        GrustGraph::from_arrow(&tables, Some("weight"))?
    } else {
        let input = fs::read_to_string(&a[1])?;
        let mut t = input.split_whitespace();
        let n: usize = t.next().ok_or("missing n")?.parse()?;
        let m: usize = t.next().ok_or("missing m")?.parse()?;
        let nodes = (0..n)
            .map(|i| grust::Node {
                id: i.to_string().into(),
                label: "Node".into(),
                props: grust::Props::new(),
            })
            .collect();
        let mut edges = Vec::with_capacity(m);
        for _ in 0..m {
            let u = t.next().ok_or("source")?;
            let v = t.next().ok_or("target")?;
            let w: f64 = t.next().ok_or("weight")?.parse()?;
            edges.push(grust::Edge::new(
                "EDGE",
                u,
                v,
                grust::Props::from([("weight".into(), grust::Value::Float(w))]),
            ));
        }
        if t.next().is_some() {
            return Err("trailing graph input".into());
        }
        GrustGraph::new(grust::Graph::new(nodes, edges), Some("weight"))?
    };
    let n = g.node_count();
    if let Some(dir) = a.get(5) {
        fs::create_dir(dir)?;
        let dir = std::path::Path::new(dir);
        g.to_arrow()?.write_ipc(
            fs::File::create(dir.join("nodes.arrow"))?,
            fs::File::create(dir.join("edges.arrow"))?,
        )?;
    }
    let source: usize = a[4].parse()?;
    let text = match a[2].as_str() {
        "bfs" => "CALL grustcat.bfs($source) YIELD node_id, distance RETURN node_id, distance",
        "dijkstra" => {
            "CALL grustcat.dijkstra($source) YIELD node_id, distance RETURN node_id, distance"
        }
        "wcc" => "CALL grustcat.wcc() YIELD node_id, component_id RETURN node_id, component_id",
        "scc" => "CALL grustcat.scc() YIELD node_id, component_id RETURN node_id, component_id",
        "pagerank" => "CALL grustcat.pagerank() YIELD node_id, score RETURN node_id, score",
        "dijkstra-full" => {
            "CALL grustcat.fullPaths($source) YIELD nodeIds, costs UNWIND range(0,size(nodeIds)-1) AS i RETURN count(*) AS path_entries, sum(nodeIds[i]) AS node_sum, sum(costs[i]) AS cost_sum"
        }
        _ => return Err("unknown algorithm".into()),
    };
    let params = grustcat_cypher::CypherParameters::from([(
        "source".into(),
        grust::Value::Int(i64::try_from(source)?),
    )]);
    let start = Instant::now();
    let result = grustcat_cypher::query(&g, text, &params, &ctx)?;
    let ms = start.elapsed().as_secs_f64() * 1000.;
    let iterations = result.iterations;
    let reachable = result.reachable;
    let (path_entries, node_sum, cost_sum) = if result.distances.is_some() {
        (
            result
                .rows
                .column(0)
                .as_any()
                .downcast_ref::<UInt64Array>()
                .ok_or("bad count")?
                .value(0),
            result
                .rows
                .column(1)
                .as_any()
                .downcast_ref::<UInt64Array>()
                .ok_or("bad sum")?
                .value(0),
            result
                .rows
                .column(2)
                .as_any()
                .downcast_ref::<Float64Array>()
                .ok_or("bad sum")?
                .value(0),
        )
    } else {
        (0, 0, 0.)
    };
    let batch = result.distances.unwrap_or(result.rows);
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
        "{{\"query\":{text:?},\"execution_class\":\"grust-parser-arrow-backend\",\"ms\":{ms},\"iterations\":{iterations},\"reachable\":{reachable},\"path_entries\":{path_entries},\"node_sum\":{node_sum},\"cost_sum\":{cost_sum}}}"
    );
    Ok(())
}
