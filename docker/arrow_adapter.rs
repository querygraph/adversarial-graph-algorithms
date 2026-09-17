//! Explicit Arrow preparation/result consumption, optionally through DataFusion.
//! These are Grust kernels, not DataFusion implementations of graph algorithms.
use super::{Output, Result, MEMORY_BYTES};
use arrow_array::{Array, Float64Array, LargeListArray, StringArray};
use grust_algorithms::*;
use grust_arrow::ArrowGraph;
use grust_core::Graph;
use grust_datafusion::{DataFusionEngine, ExecutionOptions, SpillPolicy};
use std::{num::NonZeroUsize, time::Instant};

pub(super) fn run(input: &Graph, algorithm: &str, source: &str, datafusion: bool) -> Result<Output> {
    let preparation = Instant::now();
    let start = Instant::now();
    let arrow = ArrowGraph::from_graph(input)?;
    let conversion_ms = start.elapsed().as_secs_f64() * 1000.;
    let start = Instant::now();
    let (nodes, edges, plans) = if datafusion {
        let runtime = tokio::runtime::Builder::new_current_thread().enable_all().build()?;
        runtime.block_on(async move {
            let engine = DataFusionEngine::new(ExecutionOptions {
                working_memory_bytes: NonZeroUsize::new(MEMORY_BYTES).unwrap(),
                target_partitions: NonZeroUsize::new(1).unwrap(),
                batch_rows: NonZeroUsize::new(1024).unwrap(),
                spill: SpillPolicy::Disabled,
            })?;
            let (nodes, edges) = arrow.into_tables();
            engine.register_table("nodes", nodes)?;
            engine.register_table("edges", edges)?;
            // The graph is already selected. Consume all structural and property
            // columns through real DataFusion plans; no filtered graph is substituted.
            let nodes = engine.dataframe("SELECT * FROM nodes").await?;
            let edges = engine.dataframe("SELECT * FROM edges").await?;
            let plans = serde_json::json!({
                "nodes": nodes.logical_plan().display_indent().to_string(),
                "edges": edges.logical_plan().display_indent().to_string(),
            });
            Ok::<_, Box<dyn std::error::Error>>((nodes.collect().await?, edges.collect().await?, plans))
        })?
    } else {
        (vec![arrow.nodes().clone()], vec![arrow.edges().clone()], serde_json::Value::Null)
    };
    let dataframe_ms = start.elapsed().as_secs_f64() * 1000.;
    let context = ExecutionContext::new(ExecutionLimits {
        memory_bytes: MEMORY_BYTES, work_units: usize::MAX, batch_rows: 1024, deadline: None,
    })?;
    let start = Instant::now();
    let graph = GraphProjection::from_arrow_batches(
        SnapshotIdentity::new("benchmark".into(), "input-arrow".into(), "benchmark-reader".into())?,
        &nodes, &edges,
        ProjectionOptions { weight: WeightSelection::Property { key: "weight", missing: MissingWeight::Reject }, ..Default::default() },
        &context,
    )?;
    let projection_ms = start.elapsed().as_secs_f64() * 1000.;
    let mut output = Output {
        preparation_ms: Some(preparation.elapsed().as_secs_f64() * 1000.),
        arrow_details: Some(serde_json::json!({"conversion_ms": conversion_ms,
            "datafusion_preparation_ms": if datafusion { Some(dataframe_ms) } else { None },
            "projection_ms": projection_ms, "datafusion_plans": plans,
            "input_node_batches": nodes.len(), "input_edge_batches": edges.len(),
            "result_format": "Arrow 59 record batches", "target_partitions": 1,
            "datafusion_memory_bytes": if datafusion { Some(MEMORY_BYTES) } else { None },
            "input_admission": "caller-owned; covered by container limit", "spill": "disabled"})),
        ..Default::default()
    };
    let start = Instant::now();
    output.values = vec![-1.; input.nodes.len()];
    let mut cursor = match algorithm {
        "bfs" => bfs(&graph, source)?.into_arrow_results(),
        "dijkstra" => dijkstra(&graph, source)?.into_arrow_results(),
        "dijkstra-full" => shortest_paths(&graph, source)?.into_arrow_results()?,
        "wcc" => weakly_connected_components(&graph)?.into_arrow_results(),
        "scc" => strongly_connected_components(&graph)?.into_arrow_results(),
        "pagerank" => {
            let rank = pagerank(&graph, PageRankOptions::default())?;
            if !rank.converged() { return Err("PageRank did not converge".into()); }
            output.iterations = rank.iterations();
            rank.into_arrow_results()
        },
        _ => return Err("unsupported Arrow algorithm".into()),
    };
    while let Some(admitted) = cursor.next_batch()? {
        let batch = admitted.record_batch();
        if algorithm == "dijkstra-full" {
            let targets = batch.column_by_name("targetNodeId").unwrap().as_any().downcast_ref::<StringArray>().unwrap();
            let totals = batch.column_by_name("totalCost").unwrap().as_any().downcast_ref::<Float64Array>().unwrap();
            let ids = batch.column_by_name("nodeIds").unwrap().as_any().downcast_ref::<LargeListArray>().unwrap();
            let costs = batch.column_by_name("costs").unwrap().as_any().downcast_ref::<LargeListArray>().unwrap();
            for row in 0..batch.num_rows() {
                output.values[targets.value(row).parse::<usize>()?] = totals.value(row);
                output.reachable += 1;
                let ids = ids.value(row);
                let ids = ids.as_any().downcast_ref::<StringArray>().unwrap();
                let costs = costs.value(row);
                let costs = costs.as_any().downcast_ref::<Float64Array>().unwrap();
                if ids.len() != costs.len() { return Err("path arrays have unequal length".into()); }
                context.charge_work(ids.len().saturating_add(costs.len()))?;
                for i in 0..ids.len() {
                    output.path_entries += 1;
                    output.node_sum += ids.value(i).parse::<u64>()?;
                    output.cost_sum += costs.value(i);
                }
            }
        } else {
            let ids = batch.column_by_name("nodeId").unwrap().as_any().downcast_ref::<StringArray>().unwrap();
            let values = batch.column(1);
            context.charge_work(batch.num_rows())?;
            for row in 0..batch.num_rows() {
                let value = if values.is_null(row) { -1. }
                else if let Some(values) = values.as_any().downcast_ref::<Float64Array>() { values.value(row) }
                else { values.as_any().downcast_ref::<StringArray>().ok_or("unexpected Arrow value type")?.value(row).parse::<usize>()? as f64 };
                output.values[ids.value(row).parse::<usize>()?] = value;
            }
        }
    }
    output.execution_ms = start.elapsed().as_secs_f64() * 1000.;
    Ok(output)
}
