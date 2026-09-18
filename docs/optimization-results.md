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

### Large full-path completion

Both large chains completed with every participant, one sample and no warmup, as
completion and resource demonstrations rather than performance rankings. The
16384 chain builds 134,225,920 entries in each path array and the 65536 chain
2,147,516,416; every node and cumulative-cost entry is constructed and consumed,
with no large-case shortcut enabled. The 65536 run took three and a half hours
of wall time and passed. Milliseconds:

| Participant | 16384 | 65536 |
|---|---:|---:|
| cpp | 1,088 | 30,454 |
| rust | 674 | 10,921 |
| grustcat | 667 | 10,888 |
| grustcat_cypher | 664 | 10,785 |
| grust_upstream_direct | 4,138 | 66,477 |
| turso_direct | 4,045 | 65,000 |
| grust_arrow | 14,718 | 241,622 |
| grust_datafusion | 15,646 | 245,380 |
| grust_upstream_cypher | 361,935 | 5,808,625 |
| turso_cypher | 362,102 | 5,817,678 |
| GDS | 22,803 | 387,426 |

Ordinary Cypher at 65536 takes about 1.6 hours per participant, which is why a
single sample is the whole measurement. These columns are not equal work: the
historical adapters report kernel and Arrow result construction, upstream direct
adds result conversion and resource accounting, Arrow and DataFusion add
conversion and projection, and Cypher adds parsing, policy validation and row
consumption with distance verification timed separately.

## Lock-free work accounting

Profiling `grust_upstream_direct` on the 16384 chain with `perf` attributed
72.8% of kernel self time to `ExecutionContext::charge_work`, against 14.8% for
visiting paths and 6.6% for advancing path buffers. The meter took a mutex on
every call and kernels call it once per visited entry and per reconstructed path
step, about 134 million times in that case. Grust commit `23de753` on
`work/algorithms-performance` holds `work_units` and `cancelled` as atomics and
admits each charge through a compare-exchange that recomputes admission against
the value it replaces, so budgets are still enforced exactly, granularity is
still per unit, and cancellation is still published before wakers are collected.

The patched source passed its Rust tests and the Neo4j-inclusive 4096 matrix,
then ran against the matched baseline in one container, alternating order, one
warmup and five measured samples per cell. Both variants carry the Turso
ordering fix, so the pair differs only in the work meter. All 1,224 paired
samples passed. Kernel and query milliseconds, median +/- MAD:

| Graph | Algorithm | Participant | Baseline | Patched | Change |
|---|---|---|---:|---:|---:|
| hub | dijkstra-full | arrow | 39.85 +/- 0.04 | 38.55 +/- 0.20 | -3.3% |
| hub | dijkstra-full | datafusion | 40.31 +/- 0.60 | 39.29 +/- 0.10 | -2.5% |
| hub | dijkstra-full | upstream cypher | 514.58 +/- 3.77 | 510.45 +/- 3.04 | -0.8% |
| hub | dijkstra-full | upstream direct | 2.09 +/- 0.06 | 2.03 +/- 0.36 | -2.9% |
| hub | dijkstra-full | turso-cypher | 512.32 +/- 0.54 | 507.25 +/- 3.94 | -1.0% |
| hub | dijkstra-full | turso-direct | 1.64 +/- 0.01 | 1.66 +/- 0.16 | +1.1% |
| hub | pagerank | arrow | 41.55 +/- 0.25 | 29.92 +/- 0.39 | -28.0% |
| hub | pagerank | datafusion | 41.53 +/- 0.47 | 29.89 +/- 0.52 | -28.0% |
| hub | pagerank | upstream cypher | 1757.41 +/- 16.23 | 1747.38 +/- 4.44 | -0.6% |
| hub | pagerank | upstream direct | 41.04 +/- 0.79 | 29.13 +/- 0.09 | -29.0% |
| hub | pagerank | turso-cypher | 1753.34 +/- 7.28 | 1738.44 +/- 8.37 | -0.8% |
| hub | pagerank | turso-direct | 41.46 +/- 0.81 | 29.59 +/- 0.58 | -28.6% |
| layered | dijkstra-full | arrow | 52.94 +/- 0.24 | 49.61 +/- 0.15 | -6.3% |
| layered | dijkstra-full | datafusion | 51.81 +/- 0.17 | 49.65 +/- 0.06 | -4.2% |
| layered | dijkstra-full | upstream cypher | 971.85 +/- 13.01 | 963.73 +/- 6.49 | -0.8% |
| layered | dijkstra-full | upstream direct | 4.85 +/- 0.17 | 3.49 +/- 0.05 | -27.9% |
| layered | dijkstra-full | turso-cypher | 961.28 +/- 1.18 | 955.44 +/- 2.36 | -0.6% |
| layered | dijkstra-full | turso-direct | 5.27 +/- 0.04 | 4.32 +/- 0.05 | -18.1% |
| layered | pagerank | arrow | 54.88 +/- 0.74 | 39.22 +/- 0.07 | -28.5% |
| layered | pagerank | datafusion | 50.12 +/- 0.45 | 38.60 +/- 0.24 | -23.0% |
| layered | pagerank | upstream cypher | 2267.99 +/- 22.41 | 2252.42 +/- 1.03 | -0.7% |
| layered | pagerank | upstream direct | 50.01 +/- 0.77 | 38.78 +/- 0.63 | -22.5% |
| layered | pagerank | turso-cypher | 2273.01 +/- 10.92 | 2265.48 +/- 13.25 | -0.3% |
| layered | pagerank | turso-direct | 53.82 +/- 0.94 | 38.17 +/- 0.34 | -29.1% |
| path | dijkstra-full | arrow | 942.49 +/- 13.56 | 738.28 +/- 8.31 | -21.7% |
| path | dijkstra-full | datafusion | 957.55 +/- 28.89 | 724.55 +/- 10.56 | -24.3% |
| path | dijkstra-full | upstream cypher | 22603.46 +/- 42.00 | 22204.15 +/- 16.82 | -1.8% |
| path | dijkstra-full | upstream direct | 242.31 +/- 0.50 | 196.70 +/- 1.18 | -18.8% |
| path | dijkstra-full | turso-cypher | 22635.17 +/- 80.02 | 22257.26 +/- 15.19 | -1.7% |
| path | dijkstra-full | turso-direct | 243.76 +/- 2.04 | 193.19 +/- 1.61 | -20.7% |
| path | pagerank | arrow | 31.98 +/- 0.08 | 22.83 +/- 0.02 | -28.6% |
| path | pagerank | datafusion | 29.18 +/- 0.20 | 22.38 +/- 0.40 | -23.3% |
| path | pagerank | upstream cypher | 1323.53 +/- 8.87 | 1314.65 +/- 10.59 | -0.7% |
| path | pagerank | upstream direct | 30.71 +/- 0.93 | 22.47 +/- 0.03 | -26.8% |
| path | pagerank | turso-cypher | 1337.72 +/- 1.74 | 1315.16 +/- 1.62 | -1.7% |
| path | pagerank | turso-direct | 31.32 +/- 2.73 | 22.47 +/- 0.12 | -28.3% |
| uniform | dijkstra-full | arrow | 44.31 +/- 0.39 | 42.36 +/- 0.10 | -4.4% |
| uniform | dijkstra-full | datafusion | 45.25 +/- 0.89 | 43.50 +/- 0.07 | -3.9% |
| uniform | dijkstra-full | upstream cypher | 1557.83 +/- 6.79 | 1571.25 +/- 6.81 | +0.9% |
| uniform | dijkstra-full | upstream direct | 3.66 +/- 0.04 | 2.59 +/- 0.15 | -29.4% |
| uniform | dijkstra-full | turso-cypher | 1585.40 +/- 7.40 | 1563.36 +/- 3.19 | -1.4% |
| uniform | dijkstra-full | turso-direct | 3.65 +/- 0.31 | 3.13 +/- 0.40 | -14.3% |
| uniform | pagerank | arrow | 23.41 +/- 0.20 | 16.72 +/- 0.26 | -28.6% |
| uniform | pagerank | datafusion | 23.42 +/- 0.13 | 16.68 +/- 0.35 | -28.8% |
| uniform | pagerank | upstream cypher | 2208.48 +/- 1.61 | 2177.80 +/- 4.82 | -1.4% |
| uniform | pagerank | upstream direct | 23.04 +/- 0.25 | 16.35 +/- 0.05 | -29.1% |
| uniform | pagerank | turso-cypher | 2194.01 +/- 0.55 | 2213.91 +/- 9.97 | +0.9% |
| uniform | pagerank | turso-direct | 21.55 +/- 0.11 | 16.43 +/- 0.02 | -23.8% |

At 16384, where each path array holds sixteen times the entries:

| Graph | Algorithm | Participant | Baseline | Patched | Change |
|---|---|---|---:|---:|---:|
| path | dijkstra-full | arrow | 15274.34 +/- 131.95 | 11372.30 +/- 105.86 | -25.5% |
| path | dijkstra-full | datafusion | 15383.43 +/- 78.78 | 11601.42 +/- 85.75 | -24.6% |
| path | dijkstra-full | upstream direct | 3985.76 +/- 64.73 | 3188.18 +/- 9.37 | -20.0% |
| uniform | dijkstra-full | arrow | 220.57 +/- 1.88 | 213.16 +/- 1.24 | -3.4% |
| uniform | dijkstra-full | datafusion | 184.55 +/- 0.71 | 177.87 +/- 4.28 | -3.6% |
| uniform | dijkstra-full | upstream direct | 16.30 +/- 0.19 | 12.73 +/- 0.04 | -21.9% |

Full-path Dijkstra improves 14 to 29% on direct execution and about 25% on the
Arrow and DataFusion paths at 16384. PageRank improves 23 to 29% almost
everywhere, since it charges once per node per iteration. Ordinary Cypher moves
between -1.8% and +0.9%, as expected where parsing, policy checks and row
consumption dominate.

The measured gain is smaller than the profile might suggest. A 72.8% share of
kernel self time is not 72.8% of removable wall time: the atomic still costs,
and the work around it is real. 3 of 54 cells are
slower, all at or below 1.1% and at or near their dispersion, and are reported
rather than dropped. These numbers belong to their own source pin and are not
pooled with the baseline cells above.

## Why ordinary Cypher is slow here, and how much of it is this host

Ordinary Cypher's full-path numbers are roughly ninety times direct execution at
4096 and 1.6 hours at 65536. A probe over the same chain, same policy and same
procedure isolates the cause, and it is not the one the query text suggests.

| Query shape at 4096 | Kernel/query ms |
|---|---:|
| `UNWIND` one row per path entry, as the participant runs it | 21,721 |
| No `UNWIND` at all: `RETURN count(*), sum(size(nodeIds))` | 20,804 |
| `UNWIND` with no list indexing: `RETURN count(i)` | 20,716 |
| GDS's fold shape: `sum(reduce(s = 0, x IN nodeIds | s + x))` | rejected |

Removing the row expansion entirely saves about 4%. The fold-in-row shape GDS
uses is not expressible: Grust's Cypher has no `reduce`, and the parser rejects
it. So the row-per-entry formulation is not a harness choice that inflates the
number; it is the only formulation available, and it is not where the time goes.

`perf` attributes about 83% of the remaining time to `__vdso_clock_gettime`,
`do_syscall_64` and `pvclock_clocksource_read`. The cause is the deadline check:
the bounded read policy requires a finite deadline, this participant discloses a
24-hour ceiling, and `ExecutionContext::check_state` therefore reads the clock on
every charge, once per path entry, about 8.4 million times at 4096. Direct
execution passes no deadline, skips the clock entirely, and runs in 197 ms.

**This host reads the clock the slow way.** Its clocksource is `xen`, not `tsc`,
so each read goes through the paravirtual clock rather than a register read. The
penalty is therefore partly a property of this machine: the same code on a
TSC host would pay roughly an order of magnitude less per read. Every ordinary
Cypher number in this report carries that caveat, and none of them should be
read as a portable measurement of the executor.

Sampling the deadline every 1024 charges instead of reading the clock per unit,
as an experiment on this same probe, returns identical aggregates and runs the
participant's query in 2,574 ms rather than 21,721 ms, an 8.4x improvement. That
change trades deadline granularity for clock reads and is not committed; it is
recorded here as measured headroom, not as a result.

Remaining qualification: none outstanding for this pin. Any further source
change starts a new pinned set. The deadline-sampling headroom above is an open
proposal, not a measured participant.

## Reproduction and evidence

See [the runner documentation](../docker/README.md#current-grust-and-turso-main) for exact source pins, locked builds, allocator selection and group-commit settings. Raw results currently reside under `.measurements/latest-qualification-neo4j` (this pin's passing matrix), `.measurements/qualification`, `.measurements/optimization`, and `.measurements/variants`; the final evidence bundle will retain every outcome and build receipt.
