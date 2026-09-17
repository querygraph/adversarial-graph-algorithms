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

### Allocator policy, measured at this pin

Mimalloc is the standing default for every current participant, and the matched
control measures that choice rather than assuming it. Both builds come from the
same commit, lockfile, Arrow and DataFusion versions and release profile; the
staged sources differ only in the build receipt and the six global allocator
declarations, and the two binary sets were exported from their own validated
images. One container, network disabled, two CPUs and 4 GiB, 4096 nodes, four
families, full-path Dijkstra and PageRank, six participants, one warmup and five
measured samples per cell with forward/reverse variant order alternating between
repeats. All 576 outcomes passed and every result was validated against the C++
reference.

End-to-end milliseconds, median ± MAD over five measured samples:

| Graph | Algorithm | Participant | System | Mimalloc | Change |
|---|---|---|---:|---:|---:|
| hub | dijkstra-full | arrow | 59.322 ± 0.797 | 51.312 ± 0.311 | -13.5% |
| hub | dijkstra-full | datafusion | 63.565 ± 0.296 | 55.298 ± 0.157 | -13.0% |
| hub | dijkstra-full | upstream cypher | 1064.609 ± 3.806 | 1079.307 ± 8.556 | +1.4% |
| hub | dijkstra-full | upstream direct | 13.842 ± 0.113 | 12.442 ± 0.206 | -10.1% |
| hub | dijkstra-full | turso-cypher | 1243.994 ± 1.208 | 1216.520 ± 5.502 | -2.2% |
| hub | dijkstra-full | turso-direct | 172.527 ± 2.100 | 161.962 ± 0.816 | -6.1% |
| hub | pagerank | arrow | 54.107 ± 1.105 | 54.285 ± 3.103 | +0.3% |
| hub | pagerank | datafusion | 57.379 ± 0.389 | 57.067 ± 0.962 | -0.5% |
| hub | pagerank | upstream cypher | 1768.976 ± 3.649 | 1772.839 ± 12.428 | +0.2% |
| hub | pagerank | upstream direct | 53.536 ± 0.152 | 48.257 ± 0.616 | -9.9% |
| hub | pagerank | turso-cypher | 1940.979 ± 1.847 | 1937.247 ± 2.835 | -0.2% |
| hub | pagerank | turso-direct | 216.561 ± 1.659 | 198.938 ± 0.649 | -8.1% |
| layered | dijkstra-full | arrow | 78.226 ± 1.140 | 70.719 ± 0.361 | -9.6% |
| layered | dijkstra-full | datafusion | 83.414 ± 1.246 | 73.908 ± 0.088 | -11.4% |
| layered | dijkstra-full | upstream cypher | 1704.635 ± 6.306 | 1698.790 ± 15.025 | -0.3% |
| layered | dijkstra-full | upstream direct | 22.863 ± 0.350 | 19.303 ± 0.712 | -15.6% |
| layered | dijkstra-full | turso-cypher | 1932.621 ± 10.790 | 1881.284 ± 12.554 | -2.7% |
| layered | dijkstra-full | turso-direct | 229.823 ± 1.796 | 209.588 ± 0.592 | -8.8% |
| layered | pagerank | arrow | 73.135 ± 0.423 | 68.620 ± 1.385 | -6.2% |
| layered | pagerank | datafusion | 80.513 ± 0.584 | 72.293 ± 1.011 | -10.2% |
| layered | pagerank | upstream cypher | 2299.987 ± 8.662 | 2279.929 ± 4.905 | -0.9% |
| layered | pagerank | upstream direct | 72.633 ± 1.608 | 70.488 ± 5.729 | -3.0% |
| layered | pagerank | turso-cypher | 2505.016 ± 14.245 | 2492.272 ± 15.026 | -0.5% |
| layered | pagerank | turso-direct | 279.794 ± 1.569 | 256.615 ± 1.736 | -8.3% |
| path | dijkstra-full | arrow | 997.234 ± 0.878 | 940.904 ± 2.012 | -5.6% |
| path | dijkstra-full | datafusion | 946.715 ± 3.510 | 997.948 ± 2.934 | +5.4% |
| path | dijkstra-full | upstream cypher | 23409.530 ± 8.233 | 23045.083 ± 43.239 | -1.6% |
| path | dijkstra-full | upstream direct | 252.695 ± 12.022 | 249.282 ± 1.492 | -1.4% |
| path | dijkstra-full | turso-cypher | 23766.257 ± 47.946 | 23090.628 ± 22.119 | -2.8% |
| path | dijkstra-full | turso-direct | 366.720 ± 10.557 | 358.046 ± 2.166 | -2.4% |
| path | pagerank | arrow | 38.212 ± 1.055 | 39.358 ± 0.758 | +3.0% |
| path | pagerank | datafusion | 43.294 ± 0.416 | 43.579 ± 0.819 | +0.7% |
| path | pagerank | upstream cypher | 1328.727 ± 10.596 | 1332.674 ± 9.538 | +0.3% |
| path | pagerank | upstream direct | 38.682 ± 0.920 | 37.708 ± 0.678 | -2.5% |
| path | pagerank | turso-cypher | 1454.881 ± 7.456 | 1452.111 ± 13.503 | -0.2% |
| path | pagerank | turso-direct | 150.733 ± 1.589 | 147.719 ± 0.423 | -2.0% |
| uniform | dijkstra-full | arrow | 106.218 ± 0.930 | 86.221 ± 0.599 | -18.8% |
| uniform | dijkstra-full | datafusion | 108.711 ± 0.094 | 90.821 ± 1.233 | -16.5% |
| uniform | dijkstra-full | upstream cypher | 3167.063 ± 1.025 | 3117.894 ± 22.795 | -1.6% |
| uniform | dijkstra-full | upstream direct | 51.614 ± 0.451 | 37.290 ± 0.438 | -27.8% |
| uniform | dijkstra-full | turso-cypher | 3633.011 ± 29.743 | 3569.619 ± 7.368 | -1.7% |
| uniform | dijkstra-full | turso-direct | 521.335 ± 1.245 | 462.919 ± 2.892 | -11.2% |
| uniform | pagerank | arrow | 80.166 ± 0.623 | 65.202 ± 0.347 | -18.7% |
| uniform | pagerank | datafusion | 82.765 ± 1.724 | 68.209 ± 1.958 | -17.6% |
| uniform | pagerank | upstream cypher | 2254.800 ± 6.573 | 2238.654 ± 17.802 | -0.7% |
| uniform | pagerank | upstream direct | 69.067 ± 1.136 | 55.154 ± 0.964 | -20.1% |
| uniform | pagerank | turso-cypher | 2726.222 ± 10.405 | 2655.668 ± 2.571 | -2.6% |
| uniform | pagerank | turso-direct | 538.826 ± 0.792 | 478.331 ± 2.648 | -11.2% |

Mimalloc is faster in 41 of the 48 cells and slower in 7.
The largest gains are on the sparse random family, where direct execution
improves 27.8% on full-path Dijkstra and 20.1% on PageRank, and on the Arrow and
DataFusion preparation paths, which improve 16-19% there. Ordinary Cypher moves
little in either direction, as expected: parsing, policy checks and row
consumption dominate its time.

The regression that motivated this control did not reproduce. At the previous
pin, mimalloc cost the full-path chain about 8.6% end-to-end; at this pin the
same cell is 252.695 ± 12.022 ms against 249.282 ± 1.492 ms, a 1.4% improvement
within run-to-run spread. The remaining slower cells are small and specific:
DataFusion on the full-path chain at +5.4% (946.715 ± 3.510 against 997.948 ±
2.934, outside both dispersions and therefore real), Arrow PageRank on the chain
at +3.0%, and three cells at or below 1.4% that are inside their dispersion.
Mimalloc is therefore the default on measured grounds, with the DataFusion chain
cell disclosed as a genuine regression rather than dropped. `--allocator system`
remains the explicit control build.

### Source lineage

The Grust pin is code-identical to the strain benchmark's pin
`a04ebd7578c7ab87d29d31575e12db1193b1e9b1`: every commit between them changes
only `docs/book/chapters/turso-under-strain.md`. The two benchmarks therefore
exercise the same Grust implementation, while their measurements remain
separate and unpooled.

### Neo4j-inclusive qualification at 4096

The same matrix passed at 4096 nodes with the mimalloc build: 30 cases, six
families by five algorithms, full paths, one warmup and five measured
repetitions, GDS included. Medians for full-path Dijkstra on the chain, the
benchmark's signature workload, in milliseconds:

| Participant | Median, ms |
|---|---:|
| cpp | 65.318 |
| rust | 41.989 |
| grustcat | 39.488 |
| grustcat_cypher | 41.394 |
| grust_upstream_direct | 255.174 |
| turso_direct | 242.016 |
| grust_arrow | 969.051 |
| grust_datafusion | 985.547 |
| grust_upstream_cypher | 22704.301 |
| turso_cypher | 22698.615 |

These columns are not equal work. The historical adapters report kernel and
Arrow result construction; upstream direct adds result conversion and resource
accounting; Arrow and DataFusion add conversion, preparation and projection;
ordinary Cypher adds parsing, policy validation, projection and row consumption,
with full-path distance verification timed separately. The gap between upstream
direct and the historical adapter is larger than those boundaries alone would
suggest and is the profiling target, not an accepted cost.

### Durable group commit

Group commit is a property of concurrent durable loading, not of the algorithm
kernels, and is measured as its own preparation workload: MVCC journal,
`synchronous=FULL`, statements loading, four writers, the hub family, one warmup
and five measured samples per cell, with nodes fully committed before any edge
write and the recovered snapshot verified before execution. All 36 outcomes
passed. Database load time, median +/- MAD in milliseconds:

| Nodes | Off | Engine | Client |
|---:|---:|---:|---:|
| 128 | 1261.627 +/- 16.491 | 590.089 +/- 7.176 | 670.386 +/- 26.608 |
| 1024 | 9962.163 +/- 84.301 | 4232.310 +/- 38.286 | 5274.666 +/- 145.228 |

Engine grouping roughly halves durable load time, by 53% at 128 nodes and 58% at
1024; Grust's client committer recovers most but not all of that, 47% at both
sizes. The algorithm timers are unmoved across all three settings, at about 0.03
ms for 128 nodes and 0.3 ms for 1024, which is the expected result: no group
commit setting may be credited as a kernel optimization. Snapshot ordering costs
0.05 to 0.63 ms and sits outside every algorithm timer.

WAL declines this workload outright. With four concurrent writers it fails on
node insertion with `database is locked`, which is why the experiment is
specified for MVCC only.

### A correctness defect found by this experiment

The first group-commit run failed all 36 samples. The cause was not group commit
and not the journal mode: results were associated with nodes by position in the
snapshot graph rather than by node identifier. Bulk loading and single-writer
loading both insert in input order, so position and identifier coincided and the
defect stayed invisible; four interleaved writers scrambled insertion order, and
`read_graph` returned verified records in that order, so every distance was
attached to the wrong node. The returned values were an exact permutation of the
reference, with identical multisets and wrong positions. Snapshot verification
could not catch it, by construction: it compares sorted records because database
scan order is legitimately arbitrary.

The adapter now permutes the verified snapshot back into input node order before
execution, reported as the separate `snapshot_ordering_ms` phase above. No
measurement published here was affected, because every qualification and sweep
used bulk loading, whose exact agreement with the C++ reference is confirmed
under both journal modes and is re-confirmed by every passing cell in this
report. The defect was reachable only through the statements path, which this
experiment exercised for the first time.

Remaining qualification: profiling of the full-path reconstruction path and
large full-path completion/resource tests. No final performance claim is made
for these unfinished runs.

## Reproduction and evidence

See [the runner documentation](../docker/README.md#current-grust-and-turso-main) for exact source pins, locked builds, allocator selection and group-commit settings. Raw results currently reside under `.measurements/latest-qualification-neo4j` (this pin's passing matrix), `.measurements/qualification`, `.measurements/optimization`, and `.measurements/variants`; the final evidence bundle will retain every outcome and build receipt.
