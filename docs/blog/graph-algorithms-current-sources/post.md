# What the benchmark found when we pointed it at current code

![Prometheus breaks the chains of a graph, scattering sparks between its nodes.](../../../cover/prometheus-breaks-graphs-headboard.png)

The [graph-algorithm benchmark](https://adversari.al/graph/algorithms) published in
September compared five execution variants on identical graphs and let a
65,536-node chain run to completion, with every implementation constructing and
consuming 2,147,516,416 path entries. That measurement is frozen and unchanged.

This is what happened when the same protocol was pointed at current upstream
sources instead of the snapshot, and given six new columns to fill.

## Adding the column that was missing

The published benchmark's Cypher column, Grustcat Cypher, is a typed Arrow
adapter — a Cypher-shaped front end over a fast path. It was never the general
query executor, and the repository said so. So the benchmark never measured what
an ordinary Cypher query actually costs.

The new columns include that executor, plus native execution on current kernels,
an Arrow-native path, DataFusion scan-plan preparation, and Grust algorithms
running over a verified snapshot from a durable Turso database. Eleven columns
now, all with disclosed and deliberately unequal boundaries: direct execution
times the kernel with projection separate; ordinary Cypher adds parsing, policy
validation, projection and row consumption; the Turso columns are not
Turso-native SQL graph algorithms.

The first full run put ordinary Cypher at roughly ninety times direct execution,
and nearly ninety minutes for a single full-path query at 65,536 nodes. That
number turned out to be mostly about clocks.

## Ninety times slower, and almost none of it was the query

The obvious suspect was the query shape. The Grust column expands one row per
path entry with `UNWIND`; Neo4j's GDS query folds each path in place with
`reduce`. At 65,536 nodes that is 2.1 billion interpreter rows against 65,536.

It was not the query. Removing the row expansion entirely — asking only for
`count(*)` and `sum(size(nodeIds))` — saved about 4%: 20,804 ms against 21,721.
And the fold shape could not be written at all, because Grust's Cypher had no
`reduce` to write it with.

`perf` put about 83% of the time in `__vdso_clock_gettime` and its syscall path.
The bounded read policy requires a finite deadline, this participant disclosed a
24-hour ceiling, and the execution context checked that deadline on every charge
against the work budget — once per path entry, roughly 8.4 million times at 4096
nodes. Direct execution sets no deadline, skips the clock, and finished the same
work in 197 ms.

Two things turned that from an engine result into a policy result. The host's
clocksource is `xen`, not `tsc`, so every read goes through a paravirtual clock
instead of a register. And GDS samples its own termination check: the shipped
`gds.jar` carries `RUN_CHECK_NODE_COUNT = 10000` and `INTERVAL_MS = 10000`, so
its algorithms consult a flag every ten thousand nodes and that flag re-reads the
clock every ten seconds. Grust checked every unit. What looked like an executor
deficit was one engine sampling and the other not.

Grust now samples too, every 1024 charges — an order of magnitude tighter than
the engine it is measured against. Cancellation is never sampled, budget limits
still fail exactly at their limit, and an explicit `checkpoint` still reads the
clock every time.

## The meter cost more than the work

Profiling the native path found the same shape of problem one layer down.
**72.8% of kernel self time in full-path Dijkstra was `charge_work`** — the
cooperative budget meter — against 14.8% for actually visiting paths. Kernels
charge per visited entry, and the meter took a mutex on every call: about 134
million lock acquisitions in a single-threaded kernel.

Replacing that with atomics, with admission recomputed through a compare-exchange
so budgets are still enforced exactly, improved full-path Dijkstra by 14 to 29%
on direct execution and PageRank by 23 to 29% across graph families.

Together, on the 65,536-node chain: a run that took **3 hours 32 minutes** now
takes **35 minutes**. Ordinary Cypher went from 5,808,625 ms to 594,419 ms.
Direct execution went from 66,477 ms to 51,869 ms.

Throughout, the four historical binaries are byte-identical across every run and
moved by at most 1.4%. That control is what makes the rest attributable to the
code rather than to the machine.

## The benchmark found a correctness bug, and it was not in an algorithm

A durable-loading experiment failed all 36 of its samples. Neither group commit
nor the journal mode was responsible: results were associated with nodes by
position in the snapshot rather than by node identifier. Bulk loading inserts in
input order, so position and identifier coincided and the defect was invisible.
Four concurrent writers scrambled insertion order, and every distance landed on
the wrong node.

The returned values were an exact permutation of the reference — identical
multisets, wrong positions. Snapshot verification could not catch it, by
construction: it compares sorted records, because database scan order is
legitimately arbitrary, which makes it blind to a permutation. No published
number was affected, because every published run used bulk loading. The check
that caught it was the benchmark's own per-sample comparison against a C++
reference.

## What did not work

`reduce` now exists in Grust's Cypher. It returns aggregates identical to the
`UNWIND` form, and it is 4.6 to 4.9 times slower at three different sizes — a
constant factor, not a scaling one. The benchmark keeps the row-expansion shape.
Expressing the query the way GDS expresses it currently costs more than the rows
it removes.

A first attempt at deadline sampling regressed every path that sets no deadline
by 13 to 46%, because the sampling counter ticked whether or not a deadline
existed. It reached `main` before the paired measurement that caught it. The fix
returns before both the counter and the clock when there is no deadline, and a
re-measurement put every affected cell back within dispersion.

Both are in the report, because a benchmark that only publishes the changes that
worked is not measuring, it is advertising.

## What these numbers are not

They are not a ranking of engines: the columns are execution classes with
unequal, disclosed boundaries. They are not portable — the clock findings are
shaped by one host's `xen` clocksource, and a TSC host would show a smaller
penalty for the same code. The 16,384 and 65,536 results are single samples that
establish completion, not stable rankings. Results from three source pins are
kept in three separate sets and never pooled.

The [full report](https://github.com/querygraph/adversarial-graph-algorithms/blob/main/docs/optimization-results.md)
carries the boundaries, the dispersions, the regressions and the raw evidence.
`./docker/run.sh` now measures current sources by default; `--frozen` reproduces
the published September measurement exactly as it was.
