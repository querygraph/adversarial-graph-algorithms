//! Database preparation only; algorithms remain the pinned upstream implementation.
use grust_core::{Graph, GraphStore, GraphAdminStore};
use grust_turso::{TursoConfig, TursoGraphStore, TursoJournalMode, TursoSynchronous};
use serde_json::{Value, json};
use std::{error::Error, time::Instant};

type Result<T> = std::result::Result<T, Box<dyn Error>>;

pub fn prepare(graph: Graph) -> Result<(Graph, Value)> {
    let runtime = tokio::runtime::Builder::new_multi_thread().worker_threads(2).enable_all().build()?;
    runtime.block_on(async move {
        let directory = tempfile::tempdir()?;
        let journal = std::env::var("BENCH_TURSO_JOURNAL").unwrap_or("wal".into());
        let group = std::env::var("BENCH_TURSO_GROUP_COMMIT").unwrap_or("engine".into());
        let load = std::env::var("BENCH_TURSO_LOAD").unwrap_or("bulk".into());
        let writers: usize = std::env::var("BENCH_TURSO_WRITERS").unwrap_or("4".into()).parse()?;
        if !(1..=32).contains(&writers) { return Err("writers must be in 1..=32".into()); }
        let journal_mode = match journal.as_str() {
            "wal" => TursoJournalMode::Wal, "mvcc" => TursoJournalMode::Mvcc,
            _ => return Err("journal must be wal or mvcc".into()),
        };
        if group == "client" && (journal != "mvcc" || load != "statements") {
            return Err("client group commit requires mvcc and statements load".into());
        }
        let started = Instant::now();
        let mut store = TursoGraphStore::connect(TursoConfig {
            path: directory.path().join("graph.db").to_string_lossy().into_owned(),
            journal_mode, ..Default::default()
        }).await?;
        store.bootstrap().await?;
        store.set_synchronous(TursoSynchronous::Full).await?;
        if journal == "mvcc" { store.set_mvcc_group_commit(group == "engine").await?; }
        match group.as_str() {
            "off" => {},
            "client" => store = store.with_group_commit().await?,
            "engine" => {},
            _ => return Err("group commit must be off, client, or engine".into()),
        }
        let setup_ms = started.elapsed().as_secs_f64() * 1000.;
        let started = Instant::now();
        match load.as_str() {
            "bulk" => { store.put_graph(&graph).await?; },
            "statements" => {
                // Separate node/edge phases ensure all endpoints exist before edge writes.
                for node_phase in [true, false] {
                    let mut tasks = tokio::task::JoinSet::new();
                    for writer in 0..writers {
                        let handle = store.connect_shared().await?;
                        handle.set_synchronous(TursoSynchronous::Full).await?;
                        let nodes: Vec<_> = graph.nodes.iter().skip(writer).step_by(writers).cloned().collect();
                        let edges: Vec<_> = graph.edges.iter().skip(writer).step_by(writers).cloned().collect();
                        tasks.spawn(async move {
                            if node_phase { for node in nodes { handle.put_node(&node).await?; } }
                            else { for edge in edges { handle.put_edge(&edge).await?; } }
                            Ok::<(), grust_core::GrustError>(())
                        });
                    }
                    while let Some(result) = tasks.join_next().await { result??; }
                }
            },
            _ => return Err("load must be bulk or statements".into()),
        }
        let database_load_ms = started.elapsed().as_secs_f64() * 1000.;
        let started = Instant::now();
        let snapshot = store.read_graph().await?;
        let snapshot_ms = started.elapsed().as_secs_f64() * 1000.;
        let started = Instant::now();
        // Compare full records independent of database scan order, outside query timers.
        let canonical = |g: &Graph| -> Result<(Vec<String>, Vec<String>)> {
            let mut nodes = g.nodes.iter().map(serde_json::to_string).collect::<std::result::Result<Vec<_>, _>>()?;
            let mut edges = g.edges.iter().map(serde_json::to_string).collect::<std::result::Result<Vec<_>, _>>()?;
            nodes.sort(); edges.sort(); Ok((nodes, edges))
        };
        if canonical(&graph)? != canonical(&snapshot)? { return Err("Turso snapshot differs from input".into()); }
        let snapshot_verification_ms = started.elapsed().as_secs_f64() * 1000.;
        Ok((snapshot, json!({"backend": "grust-turso", "storage": "temporary file", "journal": journal,
            "synchronous": "FULL", "group_commit": if journal == "wal" { "not_applicable" } else { &group }, "load_mode": load,
            "writers": if load == "bulk" { 1 } else { writers }, "runtime_threads": 2,
            "setup_ms": setup_ms, "database_load_ms": database_load_ms,
            "snapshot_ms": snapshot_ms, "snapshot_verification_ms": snapshot_verification_ms,
            "snapshot_verified": true})))
    })
}
