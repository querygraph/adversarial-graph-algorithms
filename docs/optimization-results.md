# Current-source benchmark optimization

Qualification is in progress. This report separates the completed initial build/allocator experiment from the latest Arrow/DataFusion qualification; results from different source pins are not pooled.

## Execution and comparison boundaries

- Historical participants are built from the unchanged published snapshot.
- Current Grust direct executes native graph kernels. Ordinary Cypher includes parsing, policy checks, projection and row consumption; full paths also have a separately timed distance-verification query.
- Arrow includes explicit row-to-Arrow conversion and Arrow projection, followed by native Grust kernels and Arrow result consumption. DataFusion additionally executes complete node/edge scan plans before the same native kernels. Preparation is reported separately and in end-to-end time.
- Turso main supplies a durable database and verified snapshot for Grust kernels. These columns do not claim Turso-native SQL graph algorithms. Database loading is not compared with GDS projection as equivalent ingestion.
- Every requested full path is constructed and its node and cumulative-cost arrays consumed. No large-case shortcuts are enabled.
- Two CPUs and 4 GiB per service, one algorithm worker, fixed graph hashes, portable release targets and pinned dependency locks. Neo4j uses the published heap/page-cache configuration. Whole-container memory peak is not per-participant RSS.

## Initial allocator and release-profile experiment

Grust `c8ec3104e203177f2035252c90fc9fdfdfe71b39`, Turso main `9a082e5bc33705e3593fac19046506e18a382921`, Rust 1.97.1. Four current participants, four families, full-path Dijkstra and PageRank, 4096 nodes, three build variants. One warmup and five measured samples per cell, alternating forward/reverse build order. All 576 outcomes passed; historical binary hashes match across variants.

Direct Grust end-to-end milliseconds, median ± MAD (five measured samples):

| Graph | Algorithm | System/default | Mimalloc/default | System/thin LTO |
|---|---|---:|---:|---:|
| path | dijkstra-full | 240.239 ± 1.026 | 260.794 ± 0.408 | 249.519 ± 1.276 |
| path | pagerank | 37.616 ± 2.455 | 36.745 ± 0.161 | 34.388 ± 0.194 |
| hub | dijkstra-full | 12.831 ± 0.410 | 11.612 ± 0.231 | 12.145 ± 0.371 |
| hub | pagerank | 52.443 ± 0.064 | 50.338 ± 0.163 | 51.333 ± 0.342 |
| layered | dijkstra-full | 21.167 ± 0.502 | 18.231 ± 0.103 | 19.719 ± 0.515 |
| layered | pagerank | 70.675 ± 0.331 | 62.501 ± 1.067 | 69.267 ± 0.273 |
| uniform | dijkstra-full | 47.371 ± 0.180 | 34.001 ± 0.235 | 44.720 ± 0.235 |
| uniform | pagerank | 64.844 ± 0.551 | 52.576 ± 1.461 | 64.590 ± 0.183 |

Mimalloc improves several loading-heavy end-to-end cases but regresses the full-path chain by about 8.6%. Kernel-only changes can have a different sign: this is not evidence of a universal algorithm speedup. Thin LTO is mixed and remains optional. Mimalloc is the user-requested process-wide default; the system allocator remains an explicit control.

The initial Neo4j-inclusive qualification passed all 60 family/size/algorithm cases at 128 and 1024 nodes with one warmup and five measured repetitions. This is separate from the latest-source qualification below.

## Latest-source qualification

Grust `3a739544c3d9e6581bdac7563d8cc3a66cdcf828` from the optimized `turso-mvcc-concurrency` branch; Turso main remains pinned as above. Arrow 59.3.0 and DataFusion 55.1.0. Six current executables use an actual Rust global mimalloc allocator by default; `--allocator system` builds the control.

The mimalloc release image passed 216 current-participant correctness checks and 45 historical Cypher/Arrow checks. A DataFusion runtime smoke test with `MIMALLOC_SHOW_STATS=1` emitted allocator statistics, confirming active allocations rather than just a configuration label.

### Neo4j-inclusive qualification at this pin

The full matrix passed on host `grust` between 17:20:40 and 17:24:54 UTC on
2026-09-17: six families x five algorithms at 128 and 1024 nodes, full paths
enabled, one warmup and five measured repetitions, all 60 cases reported
`pass`. Ten participant columns are present in every case: the historical C++,
Rust, Grustcat and Grustcat Cypher participants, upstream Grust direct and
Cypher, both Turso snapshot columns, Arrow and DataFusion. Every current
participant sample carries the runtime allocator label `mimalloc`, so the
allocator is an observed property of the measured processes rather than a build
flag. An earlier attempt at the same matrix was terminated externally partway
through (exit 137, no kernel out-of-memory event); its partial evidence is
retained separately and is not pooled with this run.

### Allocator policy

Mimalloc is the standing default for every current participant. The initial
experiment above measured it as a broad improvement with one clear exception,
the full-path chain, where it cost about 8.6% end-to-end at the previous source
pin. That exception predates the Arrow and DataFusion routing, so its sign at
the current pin is not established. A matched system-allocator control at this
exact pin, differing only in the six global allocator declarations and the build
receipt, is measured separately; `--allocator system` remains the explicit
control build. Any regression it shows will be reported rather than dropped.

### Source lineage

The Grust pin is code-identical to the strain benchmark's pin
`a04ebd7578c7ab87d29d31575e12db1193b1e9b1`: every commit between them changes
only `docs/book/chapters/turso-under-strain.md`. The two benchmarks therefore
exercise the same Grust implementation, while their measurements remain
separate and unpooled.

Remaining qualification: the 4096 Neo4j-inclusive run, the matched
latest-source allocator control, independent durable group-commit measurements,
profiling, and large full-path completion/resource tests. No final performance
claim is made for these unfinished runs.

## Reproduction and evidence

See [the runner documentation](../docker/README.md#current-grust-and-turso-main) for exact source pins, locked builds, allocator selection and group-commit settings. Raw results currently reside under `.measurements/latest-qualification-neo4j` (this pin's passing matrix), `.measurements/qualification`, `.measurements/optimization`, and `.measurements/variants`; the final evidence bundle will retain every outcome and build receipt.
