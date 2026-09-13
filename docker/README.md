# Graph algorithm Docker benchmark

Builds Icebug (C++/Arrow), Icecat (Rust/Arrow), Grustcat (Grust + Arrow), Grustcat Cypher (Grust parser + Arrow query backend), and official Neo4j GDS from the sibling checkouts. Run from `~/src/adversarial-graph-algorithms` with Docker Compose v2 and Python 3 available. Expected source directories are `../icecat` and `../grust`; `python3 docker/prepare.py --icecat PATH --grust PATH` also supports other layouts when invoking Compose directly.

```sh
# Build and test all five algorithms on six small graph families.
./docker/run.sh --full-path --sizes 128 --warmups 1 --repeats 1 --label docker-smoke

# Full paths, including the previously timed-out Neo4j case; no deadline.
./docker/run.sh --full-path --algorithms dijkstra --families path \
  --sizes 16384 65536 --warmups 0 --repeats 1 --label docker-full-path-proof

# Repeated full benchmark. Long paths can take a substantial time in GDS.
./docker/run.sh
```

Results, generated graphs, Markdown reports, source hashes, compiler/package versions, and container resource limits remain in `docker-results/`. Override with `BENCH_OUTPUT=/absolute/path`. The script removes its dedicated Compose services on exit; it does not remove results. No database ports are published. Neo4j authentication is disabled only inside the isolated benchmark network. The server has a 2 GiB Java heap, 512 MiB page cache, and a 4 GiB container memory limit. Both services have a two-CPU quota; algorithm concurrency is one. JVM background threads may use the second CPU. Docker Desktop measurements include its Linux VM and must not be mixed with native macOS measurements.

The images compile Linux binaries for the host Docker architecture, without forcing x86 emulation or native-CPU tuning. Rust is 1.97.1; C++ Arrow is pinned to Debian's available 24.0.0-1 package, independently of Rust Arrow 59.3.0. Neo4j Community 2026.08.0 and GDS 2026.08.1 are the official release archives, verified against `neo4j/downloads.json`. Base image tags and transitive OS packages are not immutable; package receipts and source checksums document each build. No enterprise algorithms or third-party Neo4j substitutes are used.

## Full-path contract

`--full-path` changes Dijkstra only. Each engine computes weighted single-source shortest paths and materializes source-first node IDs and cumulative-cost arrays for every reachable target, including the source. Each array element is consumed in count/sum aggregates. Unreachable targets have no path. Any shortest path is acceptable when ties exist. Peak output buffering is one path per native engine; GDS streams paths through server-side Cypher aggregation. Path output size is quadratic on a chain: 65,536 nodes produce 2,147,516,416 entries in each of the two arrays.

Icecat and Grustcat retain one predecessor on a strict distance improvement and reuse path buffers. Icebug uses its official Dijkstra predecessor storage and `getPath`, which may retain more equal-cost predecessor information internally. GDS uses unmodified `gds.allShortestPaths.dijkstra.stream`; Cypher consumes `nodeIds` and `costs` before returning compact summaries. These are equivalent requested outputs, with each engine's own implementation and allocation strategy. Native timers include Dijkstra, predecessor tracking, path construction, and aggregation; Rust additionally builds the Arrow distance result. GDS's timer is server query time, including Cypher overhead. The report also records client wall time. Loading, CSR construction, and GDS projection are measured separately or excluded; this is not a graph-ingestion benchmark.

All distance vectors must match exactly. Small GDS fixtures additionally validate every path edge and cumulative cost; Rust tests cover ties, zero-cost cycles, and isolates. The large chain has a unique path to every target: independent formulas check exact reachable count, path-entry count, node-ID sum, and cumulative-cost sum for all four. General tied graphs need not have matching path lengths or checksums. Aggregates are diagnostics, not collision-resistant proofs of every interior node on large general graphs.

The [Neo4j Python driver API](https://neo4j.com/docs/api/python-driver/current/api.html) specifies zero as an unlimited transaction timeout. Full-path native processes have no timeout; GDS transactions explicitly use `timeout=0` (unlimited), including validation. There is no special large-chain cutoff. `--warmups 0 --repeats 1` is a completion/correctness demonstration, not a stable performance estimate. Without `--full-path`, the historical distance-only native comparison remains available and retains its bounded large Neo4j probe; those Dijkstra results are explicitly not equivalent work.

BFS validates reachability/level order (GDS's traversal output differs from native distances). WCC/SCC compare canonical partitions. PageRank uses the same weighted uniform model but different native/GDS convergence rules, recorded in the report. Full-path equivalence does not claim to remove these other algorithm-specific differences.

For manual iteration after staging:

```sh
docker compose build
docker compose up -d --wait neo4j
docker compose run --rm --user "$(id -u):$(id -g)" benchmark \
  --full-path --algorithms dijkstra --families path --sizes 65536 \
  --warmups 0 --repeats 1 --label manual-full-path
docker compose down
```


## Grustcat Cypher variant

Docker now includes a fifth column, `grustcat-cypher`. It uses the Grust Cypher parser and semantic analyzer with the focused Arrow physical backend documented in [the crate README](../../icecat/rust/crates/grustcat-cypher/README.md). It does not use Grust's materializing reference executor or modify Grust's general procedure dispatcher. The accepted procedure namespace is `grustcat.*`, not `gds.*`. For full paths it compiles `CALL … YIELD … UNWIND range(…) … RETURN count(*), sum(…), sum(…)` into streaming aggregation over actual path arrays. Query text is recorded in raw results. Both it and Neo4j consume equivalent arrays, while their query syntax and machinery differ.

Compilation (parsing, semantic checks and planning) is inside the new column's timer, followed by algorithm execution, aggregation and Arrow result construction. Source parameter setup and input projection are outside the timer. Direct Grustcat remains a separate column. Native runs can opt into the new column with `neo4j/compare.py --include-grustcat --include-grustcat-cypher`; Docker includes both automatically.

`check_cypher.py` validates the three Rust variants across all graph families and all algorithm modes, and cross-reads Arrow IPC from each writer. The final runtime image executes these checks during its build. Its receipt is `/opt/benchmark/cypher-validation.json`.
