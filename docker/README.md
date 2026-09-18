# Graph algorithm Docker benchmark

By default, builds Icebug (C++/Arrow), Icecat (Rust/Arrow), Grustcat (Grust + Arrow), Grustcat Cypher (Grust parser + Arrow query backend), and official Neo4j GDS from the checksum-verified published snapshot. Requires Docker Compose v2 and Python 3.12+. Sibling checkouts are only needed for explicit development mode: `python3 docker/prepare.py --local --icecat PATH --grust PATH`. The current-source workflow below stages upstream Grust and Turso separately.

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

## Current Grust and Turso main

The current-source workflow preserves the frozen historical participants and adds
`grust_upstream_direct`, `grust_upstream_cypher`, `turso_direct`, `turso_cypher`,
`grust_arrow`, and `grust_datafusion`.
Turso runs Grust kernels over a verified snapshot from a temporary file-backed
Turso database; it is not a Turso-native SQL graph-algorithm implementation.
Loading and snapshot capture have separate timers. The GDS projection consumes
edge parameters without equivalent durable ingestion, so database-load timings
are not a Turso-versus-Neo4j ingestion comparison.

`./docker/run.sh` runs this workflow by default; the commands below pin sources
explicitly, which is what a separate experiment needs. `--frozen` selects the
historical published snapshot instead.

```sh
# Resolve main once, then keep this checkout fixed throughout the experiment.
git clone https://github.com/querygraph/grust.git /tmp/algorithms-grust
git -C /tmp/algorithms-grust checkout 3a739544c3d9e6581bdac7563d8cc3a66cdcf828
git clone https://github.com/tursodatabase/turso.git /tmp/algorithms-turso
git -C /tmp/algorithms-turso checkout 9a082e5bc33705e3593fac19046506e18a382921
./docker/run.sh --upstream-grust /tmp/algorithms-grust \
  --turso /tmp/algorithms-turso --mimalloc --profile default \
  --lockfile docker/upstream-Cargo.lock --output /tmp/algorithms-mimalloc \
  -- --full-path --sizes 128 1024 --warmups 1 --repeats 5 --label qualification
```

The output directory must be new. The runner prepares isolated frozen/current
contexts, builds both services, runs image correctness checks, records image and
compiler identities, and runs the suite with the same two-CPU/four-GiB limits.
Build and runtime logs, per-file hashes, exact dependency lockfile, image validation,
raw process outcomes, terminal status, and reports remain in that directory even
if the run fails. Each Compose project has a unique name. Source directories
are copied without editing the original checkouts. The supplied lockfile targets
the two commits above; omit `--lockfile` to resolve a new source combination,
then reuse the resulting `upstream-Cargo.lock` for every trial. Resolution is not
silently repeated when a lockfile is supplied.

`--mimalloc` (also `--allocator mimalloc`) is the default and installs an actual
global allocator for the whole process in all current participant binaries.
Use `--allocator system` for the explicit baseline control. Historical binaries stay fixed. `--profile thin` enables
thin LTO and one codegen unit for the current participants; default preserves
Cargo's release defaults. Both use portable CPU targets. Compare allocator and
profile changes independently with fixed source and lockfile, alternating trial
order, warmups, at least five measured samples, and median/dispersion. Inspect
loading/projection/end-to-end phases as well as query/kernel timings.

Turso defaults to WAL, bulk loading, and `synchronous=FULL`. For a separate
concurrent-write preparation experiment, set:

```sh
export BENCH_TURSO_JOURNAL=mvcc BENCH_TURSO_LOAD=statements
export BENCH_TURSO_WRITERS=4
export BENCH_TURSO_GROUP_COMMIT=engine # or off, or client
```

`engine` explicitly enables Turso engine grouping and leaves Grust client
grouping off. `off` disables both; `client` disables engine grouping and enables
Grust's client committer. These settings apply only to MVCC; WAL records grouping
as not applicable. Client grouping requires the statements workload. Each trial
loads exactly the same nodes and edges, with all nodes committed before edge
writes, and checks the full recovered snapshot before algorithm execution.
Runtime has two worker threads and algorithm concurrency remains one. Statement
loading includes connection setup, task scheduling, and input batching. It is a
disclosed preparation workload, not the strain benchmark's hot-node workload.
No group-commit change can be credited as an algorithm-kernel optimization.

Workflow checks: `python3 -m unittest discover -s docker -v`.
Set `BENCH_TEST_CONTEXT=/path/to/staged/context` to also check actual staging.

For paired measurements after building the three variants, export the binaries
and receipts with `python3 docker/export_variant.py IMAGE OUTPUT`. Stop other
measurement jobs and the idle Neo4j service, then run a single container:

```sh
docker run --rm --cpus 2 --memory 4g --network none \
  --user "$(id -u):$(id -g)" \
  -v /absolute/results:/work -v /absolute/variants:/variants:ro \
  -v "$PWD/docker":/scripts:ro --entrypoint python3 IMAGE \
  /scripts/sweep.py \
  --variants /variants/system-default /variants/mimalloc-default /variants/system-thin \
  --output /work/optimization --sizes 4096 --warmups 1 --repeats 5
python3 docker/report_sweep.py /absolute/results/optimization/results.json
```

The sweep alternates forward/reverse variant order, validates every result against
C++, keeps warmups and measurements separately, and retains all failures while
continuing the other samples. Use `--group-commit --participants turso-direct
--variants /variants/system-default --families hub --algorithms dijkstra
--sizes 128 1024` for the separate engine/off/client durable-loading experiment.
Each sweep output directory must be new. Whole-container memory peak is explicitly
labeled and is not a per-participant RSS measurement.

The current optimized Grust pin is from `turso-mvcc-concurrency`, which is newer
than `main` and contains the Arrow/DataFusion routing work and Turso allocator
facade feature. Arrow 59.3.0 and DataFusion 55.1.0 are locked. `grust_arrow`
converts the row graph into Arrow input, uses the native Arrow projection API,
and consumes native Arrow algorithm results. `grust_datafusion` executes complete
node/edge DataFusion scan plans first and then uses the same Arrow/native path.
Conversion, DataFusion preparation and projection are timed independently.
Neither column claims that DataFusion executes algorithm CALLs or provides
independent BFS/Dijkstra/PageRank kernels. Every full path's node and cost arrays
are materialized and consumed. DataFusion has one target partition, a 256 MiB
working pool, and spilling disabled; caller-owned Arrow inputs remain outside
that logical pool and inside the container limit.
