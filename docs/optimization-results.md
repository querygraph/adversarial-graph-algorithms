# The algorithms benchmark on current sources

This report covers the current-source extension of the published graph-algorithm
benchmark: what it measures, what it found, what it changed upstream, and what
its numbers do not mean. The published 2026-09-13 full-path measurement is a
separate, unchanged experiment, reproducible with `./docker/run.sh --frozen`.

Every number here was measured on host `grust`, an 8-vCPU Xeon E5-2686 v4
instance, in Docker with two CPUs and 4 GiB per service and algorithm
concurrency one. Nothing is pooled across hosts or across source pins.

## What is measured

Eleven columns run over identical generated directed weighted graphs, in six
families, for five algorithms, with full paths constructed and consumed when
requested.

Four historical participants come from the frozen published snapshot: the C++
NetworKit update, the Rust rewrite, Grustcat, and Grustcat Cypher. Official
Neo4j GDS is the fifth published column. Six current participants build from
pinned upstream sources:

| Column | Execution class |
|---|---|
| `grust_upstream_direct` | current kernels through the native API |
| `grust_upstream_cypher` | the general Cypher executor: parse, policy validation, projection, row consumption |
| `grust_arrow` | row-to-Arrow conversion, native Arrow projection, Arrow result consumption |
| `grust_datafusion` | complete DataFusion node/edge scan plans, then the same native kernels |
| `turso_direct`, `turso_cypher` | Grust kernels over a verified snapshot from a durable Turso database |

These are execution classes, not engines. The columns do not do equal work, and
this report never presents them as if they did. Direct execution times the kernel
and result conversion with projection separate. Ordinary Cypher additionally
parses, validates against a read policy, projects and consumes rows, and runs
full-path distance verification in its own timer. Arrow and DataFusion add
conversion and preparation. The Turso columns run Grust kernels over a
materialized snapshot and are not Turso-native SQL graph algorithms; their
database loading is not comparable to a GDS projection as ingestion.

Method: one warmup and five measured samples per cell unless stated, alternating
forward and reverse variant order inside a single limited container, median and
median absolute deviation reported, **every sample validated against the C++
reference**, every failure retained rather than discarded, and a process audit,
build receipt, image digest and source hash kept for each run.

## Three source pins

Results belong to the pin that produced them and are never pooled.

| Pin | Contents |
|---|---|
| `3a73954` | current-source baseline: Arrow/DataFusion routing, Turso facade |
| `b5e92bd` | adds lock-free work accounting and the sampled deadline check |
| `37fdf9c` | adds the Cypher reference-executor work and list binding forms |

## Correctness

Every matrix passed on every pin it was run on: 60 cases at 128 and 1024 nodes
and 30 cases at 4096, six families by five algorithms, GDS included, full paths
enabled. The release images pass 216 current-participant checks and 45 historical
Cypher/Arrow interchange checks. The paired sweeps contributed a further 576,
576, 288 and 576 validated samples with no failures.

### A correctness defect the performance work found

The first durable group-commit run failed all 36 of its samples. The cause was
neither group commit nor the journal mode: results were associated with nodes by
position in the snapshot graph rather than by node identifier. Bulk loading and
single-writer loading both insert in input order, so position and identifier
coincided and the defect stayed invisible; four interleaved writers scrambled
insertion order, and every distance was attached to the wrong node. The returned
values were an exact permutation of the reference — identical multisets, wrong
positions. Snapshot verification could not catch it by construction, because it
compares sorted records: database scan order is legitimately arbitrary, so the
check is blind to a permutation.

The adapter now permutes the verified snapshot back into input order before
execution, reported as a separate `snapshot_ordering_ms` phase outside every
algorithm timer and costing under a millisecond at these sizes. No published
measurement was affected: every qualification and sweep used bulk loading, whose
exact agreement with the reference holds under both journal modes.

## Findings

### The allocator is a measured default, not an assumption

Mimalloc is the standing default for all six current participants and is an
actual Rust global allocator, observable as a runtime label on every sample. A
matched control at the same pin, differing only in the build receipt and six
global allocator declarations, ran both binary sets in one container at 4096
nodes: **mimalloc is faster in 41 of 48 cells**, by as much as 27.8% on sparse
random graphs, with the largest gains in direct execution and in the Arrow and
DataFusion preparation paths.

Three cells are slower and are reported rather than dropped, led by DataFusion on
the full-path chain at +5.4%, outside both dispersions and therefore real. An
8.6% chain regression measured at the previous pin did **not** reproduce here;
that cell is now 1.4% faster, within run-to-run spread.

### Cooperative accounting cost more than the work it guarded

Profiling `grust_upstream_direct` on the 16384-node chain with `perf` attributed
**72.8% of kernel self time to `ExecutionContext::charge_work`**, against 14.8%
for visiting paths and 6.6% for advancing path buffers. Kernels charge one work
unit per visited entry and per reconstructed path step, and the meter took a
mutex on every call: about 134 million lock acquisitions for that one case, in a
single-threaded kernel.

Grust now holds the work counter and the cancellation flag as atomics, admitting
each charge through a compare-exchange that recomputes admission against the
value it replaces, so budgets are still enforced exactly and granularity is still
per unit. Measured against a matched baseline differing only in that change,
full-path Dijkstra improved by up to 29.4% on direct execution — except on the
hub family, where it was flat at -2.9% and +1.1% — and about 25% on the Arrow
and DataFusion paths at 16384; PageRank improved between 22.5% and 29.1% across
every family, since it charges once per node per iteration.

The gain is smaller than the profile share suggests. A 72.8% share of self time
is not 72.8% of removable wall time: the atomic still costs, and the work around
it is real.

### Ordinary Cypher was mostly reading the clock

Ordinary Cypher's full-path query was about ninety times direct execution. The
query text was not the reason. On the same graph and policy, removing the row
expansion entirely — `RETURN count(*), sum(size(nodeIds))` instead of one
`UNWIND` row per path entry — saved about 4%: 20,804 ms against 21,721 ms.

`perf` attributed about 83% of the remainder to `__vdso_clock_gettime`,
`do_syscall_64` and `pvclock_clocksource_read`. The bounded read policy requires
a finite deadline, this participant discloses a 24-hour ceiling, and the state
check therefore read the clock on **every charge** — roughly 8.4 million times at
4096. Direct execution passes no deadline, skips the clock, and ran in 197 ms.

Two things make that a policy difference rather than an engine difference. First,
**this host's clocksource is `xen`, not `tsc`**, so each read goes through the
paravirtual clock rather than a register read, and the penalty is partly a
property of this machine. Second, **GDS samples its own termination check**:
`TerminationFlag.RUN_CHECK_NODE_COUNT = 10000` and
`TerminationFlagImpl.INTERVAL_MS = 10000` in the shipped `gds.jar`, so algorithms
consult the flag every 10,000 nodes and the flag re-reads the clock every ten
seconds. Grust checked every unit. The resulting time difference was a
checking-policy difference that an earlier draft of this report presented as
executor performance.

Grust now samples the deadline every 1024 charges. An interval sweep shows the
win is complete by 256 and flat thereafter, so the interval stays tight and
remains an order of magnitude stricter than the engine it is compared against.
Cancellation is never sampled, budget limits still fail exactly at their limit,
memory admission keeps an exact check, and `checkpoint` reads the clock every
time, so an explicit poll stays precise.

**A regression in the first implementation, recorded because it reached `main`.**
The sampling counter ticked on every charge whether or not a deadline existed, so
the deadline-free kernels — every direct, Arrow and DataFusion path — paid an
atomic read-modify-write they had never paid before: full-path Dijkstra on the
chain 27.8% slower, PageRank on sparse random graphs 40.6% slower, while Cypher
improved by up to 89.9%. An execution without a deadline now returns before both
the counter and the clock. A paired re-measurement put every affected cell back
within dispersion, between −2.5% and +2.0%, with the Cypher gain intact at
−89.8%.

### The reference executor, and what it did not reach

The `37fdf9c` pin adds sampled deadlines in read admission and per-row memory
charges, compact candidate rows, aggregates folded as they are evaluated, shared
relationships and path elements instead of deep copies, and nodes bound by
reference. Ordinary Cypher at 4096 improves between 88.6% and 98.1% across every
graph family — clusters Dijkstra from 340.75 ± 0.83 ms to 8.47 ± 0.30, rmat from
1121.98 ± 6.49 to 36.33 ± 0.05, uniform PageRank from 1483.02 ± 2.71 to 61.82 ±
0.55. Direct, Arrow and DataFusion are unchanged, which is correct: the work is
in the Cypher executor.

Full-path Dijkstra on the chain was the exception. It did not improve, and the
penalty grew with the work: +2.0% at 4096, +9.8% at 16384, +11.0% at 65536,
while direct and Arrow stayed flat in the same runs. That case is dominated by
materializing one heap-allocated string per path entry — `nodeIds` is declared
`ValueType::Strings`, and the profile showed `Vec<String>::clone` and `cfree` in
the residual — rather than by the per-row overhead that work removed.

### The chain case, once it was charged per path

Reporting that cell produced the next change (Tadpole 0.21.0, `9573aac`), which
stopped deep-copying every yielded value into each row and began admitting work
per path, or per 1024 steps, instead of per entry. It removed both the
regression and much of the original cost. At 4096 nodes with five measured
samples on the chain: direct execution 196.07 ± 1.67 to **80.92 ± 0.15 ms**
(−58.7%), ordinary Cypher 2301.51 ± 10.60 to **1260.51 ± 1.63 ms** (−45.2%),
Arrow 737.34 ± 6.06 to 605.82 ± 6.72 ms (−17.8%). On the 16384 chain: Cypher
36,913 to 20,255 ms, direct 3,190 to 1,298 ms, Arrow 11,612 to 9,397 ms, with
the frozen C++ participant moving 0.4% in the same runs.

Direct execution improving by 58.7% is the per-entry charge the first profile
found, now charged per path: worth roughly a further 2.4x on this case beyond
what removing the mutex achieved. The 65536 case has not been re-run at this
pin, and this pin's dependency resolution differs from the earlier ones, so its
lockfile is recorded with the run rather than reused.

### List binding forms

`reduce` now parses and returns aggregates identical to the `UNWIND` form, so the
feature is correct. It is also slower, by a constant factor rather than a scaling
one: 4.7x at 1024 nodes, 4.6x at 2048, 4.9x at 4096, with both shapes scaling
linearly in entries. The benchmark keeps the `UNWIND` shape. Until the fold path
reuses whatever makes the aggregate path fast, expressing the GDS-shaped query
costs more than the row expansion it removes.

## Full-path completion at scale

The chain at 16384 builds 134,225,920 entries in each path array; at 65536 it
builds 2,147,516,416. Every entry is constructed and consumed, with no large-case
shortcut and no transaction deadline for the native participants. These are
single samples with no warmup: they establish completion and resource behaviour,
not ranking.

Milliseconds at 65536, by pin:

| Participant | `3a73954` | `b5e92bd` | `37fdf9c` |
|---|---:|---:|---:|
| grustcat | 10,888 | 10,873 | 10,855 |
| rust | 10,921 | 10,947 | 10,883 |
| cpp | 30,454 | 30,716 | 30,721 |
| turso_direct | 65,000 | 52,213 | 51,661 |
| grust_upstream_direct | 66,477 | 52,142 | 51,869 |
| grust_datafusion | 245,380 | 183,576 | 184,981 |
| grust_arrow | 241,622 | 184,957 | 184,291 |
| GDS | 387,426 | 383,461 | 383,461 |
| turso_cypher | 5,817,678 | 527,756 | 599,910 |
| grust_upstream_cypher | 5,808,625 | 535,450 | 594,419 |

The whole run fell from **3 h 32 m to 35 m** of wall time. The historical
binaries are byte-identical across all three runs and moved by at most 1.4%,
which is what makes the current-participant changes attributable to the code
rather than to the machine.

Ordinary Cypher went from about fifteen times GDS to about 1.55 times it on this
case. Those are still not equal work — GDS's projection is built before its timer
starts and Grust's Cypher timer includes projection — but the gap that looked
like an executor deficit was mostly deadline-checking policy.

## What these numbers are not

- Not a ranking of engines. The columns are execution classes with disclosed and
  unequal boundaries.
- Not portable. The deadline and clock findings are shaped by a `xen`
  clocksource; a TSC host would show a smaller penalty for the same code.
- Not stable at 16384 and 65536. Those are single samples.
- Not pooled. Three source pins, three result sets, kept separate.
- Not per-participant memory. Container peaks are whole-container figures,
  including file cache, and are labelled as such.
- Not a query-suite result. No result from the separate graph-query or strain
  benchmarks is combined with these.

## Reproduction

`./docker/run.sh` measures current sources by default, cloning the pinned
checkouts recorded in `docker/upstream-pins.json` and refusing a checkout that
sits at any other commit. `--frozen` reproduces the published snapshot
measurement. `docker/README.md` documents allocator selection, group-commit
settings, the paired sweep, and the exact commands behind every table above. Raw
evidence, receipts and retained failures live under `.measurements/`.

## Durable loading, measured separately

Group commit is a property of concurrent durable loading, not of the algorithm
kernels, and is measured as its own preparation workload: MVCC journal,
`synchronous=FULL`, statements loading, four writers, nodes fully committed
before any edge write, and the recovered snapshot verified before execution. All
36 outcomes passed. Database load time, median ± MAD in milliseconds:

| Nodes | Off | Engine | Client |
|---:|---:|---:|---:|
| 128 | 1261.627 ± 16.491 | 590.089 ± 7.176 | 670.386 ± 26.608 |
| 1024 | 9962.163 ± 84.301 | 4232.310 ± 38.286 | 5274.666 ± 145.228 |

Engine grouping roughly halves durable load time; Grust's client committer
recovers most but not all of that. The algorithm timers are unmoved across all
three settings, which is the expected result: no group-commit setting may be
credited as a kernel optimization. WAL declines this workload outright, failing
on node insertion with `database is locked` at four writers, which is why the
experiment is specified for MVCC only.
