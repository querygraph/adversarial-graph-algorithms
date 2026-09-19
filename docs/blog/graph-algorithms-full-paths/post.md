# Graph algorithms, full paths, and the work a benchmark must count

![Graph Algorithm Benchmark cover: a rocket marked Rust flies out of a ringed planet's debris field, past rocks marked JVM, legacy, GC pauses, warmup and heavy runtime, toward a sunrise over Earth.](../../../cover/graph-algorithm-benchmark.PNG)

The [graph-algorithm benchmark on adversari.al](https://adversari.al/graph/algorithms)
compares implementations on identical generated graphs. Its most revealing
experiment is a chain of 65,536 nodes, where every implementation computes
shortest paths and constructs and consumes the full node sequence and
cumulative-cost sequence for every reachable destination. Neo4j is allowed to
finish.

The important change came before any timing. We had to agree on what the result
contained. Everything after that — three rounds of optimization, two regressions,
and one correctness bug — followed from having an output contract explicit enough
to argue about.

## A distance is not a path

A shortest-distance query returns one number for each destination. A full-path
query also returns the intermediate nodes and the cost accumulated along that
route. Those are different output contracts, even when both operations are called
Dijkstra.

A chain makes the difference concrete. The path to the source contains one node.
The path to the next contains two, then three. Across all destinations, each
array contains `n(n + 1) / 2` entries. At 65,536 nodes that is **2,147,516,416
entries in the node-ID array and the same number in the cumulative-cost array**,
for each engine.

Nothing is summed in closed form, no graph family is special-cased, and paths are
reconstructed one at a time into reused buffers rather than retained together.
The mode removes both the native process deadline and the Neo4j transaction
deadline.

## Columns are execution classes, not engines

The first published run had five columns. **Icebug** is the Apache Arrow update
of the C++ NetworKit codebase. **Icecat** is the Rust rewrite. **Grustcat** is the
Grust-compatible implementation with an Arrow projection. **Grustcat Cypher**
adds a parser and semantic analyzer over a focused typed Arrow backend. The fifth
is **Neo4j Community with official GDS** and its unmodified single-source
Dijkstra procedure.

That run, one sample per cell with no warmup, in Linux ARM64 Docker on an Apple
M1 Max, in seconds:

| Variant | 16,384-node chain | 65,536-node chain |
|---|---:|---:|
| Icebug | 1.102 | 22.233 |
| Icecat | 1.053 | 16.648 |
| Grustcat | 1.032 | 16.710 |
| Grustcat Cypher | 1.028 | 16.727 |
| Neo4j GDS | 11.889 | 194.113 |

Every number later in this post comes from a different machine — an 8-vCPU Xeon
in EC2 — and none of them belong in that table. Graph loading and projection sit
outside the reported timers. Native timings include the algorithms,
reconstruction and aggregation; Neo4j's is server query time including Cypher
aggregation.

**The gap in that lineup is the one that mattered.** Grustcat Cypher is a typed
Arrow adapter — a Cypher-shaped front end over a fast path, and the repository
always said so. It is not the general query executor. So the benchmark had never
measured what an ordinary Cypher query costs.

## Six more columns, and a ninety-fold question

Pointing the same protocol at current upstream sources added six: native
execution on current kernels, **the general Cypher executor**, an Arrow-native
path, DataFusion scan-plan preparation, and Grust algorithms over a verified
snapshot from a durable Turso database. Eleven columns, all with deliberately
unequal and disclosed boundaries.

Ordinary Cypher came in at roughly ninety times direct execution — nearly ninety
minutes for one full-path query at 65,536 nodes.

The obvious suspect was the query shape. The benchmark's Grust column expands one
row per path entry with `UNWIND`; Neo4j's GDS query folds each path in place with
`reduce`. At 65,536 nodes that is 2.1 billion interpreter rows against 65,536.

It was not the query. Removing the row expansion entirely — asking only for
`count(*)` and `sum(size(nodeIds))` — saved about 4%: 20,804 ms against 21,721.
And the fold shape could not be written at all, because Grust's Cypher had no
`reduce` to write it with.

`perf` put about 83% of the time in `__vdso_clock_gettime` and its syscall path.
The bounded read policy requires a finite deadline, this participant disclosed a
24-hour ceiling, and the execution context checked that deadline on **every
charge against the work budget** — once per path entry, roughly 8.4 million times
at 4,096 nodes. Direct execution sets no deadline, skips the clock, and finished
the same work in 197 ms.

Two things turned that from an engine result into a policy result. The host's
clocksource is `xen`, not `tsc`, so every read goes through a paravirtual clock
instead of a register. And GDS samples its own termination check: the shipped
`gds.jar` carries `RUN_CHECK_NODE_COUNT = 10000` and `INTERVAL_MS = 10000`, so
its algorithms consult a cached flag every ten thousand nodes and that flag
re-reads the clock every ten seconds. Grust checked every unit. What looked like
an executor deficit was one engine sampling and the other not.

Grust now samples too, every 1024 charges — an order of magnitude tighter than
the engine it is measured against. Cancellation is never sampled, budget limits
still fail exactly at their limit, and an explicit checkpoint still reads the
clock every time.

## The meter cost more than the work it guarded

Profiling the native path found the same shape of problem underneath.
**72.8% of kernel self time in full-path Dijkstra was `charge_work`** — the
cooperative budget meter — against 14.8% for visiting paths. Kernels charge per
visited entry, and the meter took a mutex on every call: about 134 million lock
acquisitions in a single-threaded kernel.

Making the counter and cancellation flag atomics, with admission recomputed
through a compare-exchange so budgets are still enforced exactly, improved
full-path Dijkstra by up to 29.4% on direct execution — except on hub graphs,
where it was flat — and PageRank by 22.5 to 29.1% across families.

Then the same problem once more, one layer down. A streaming `CALL` was
deep-copying every yielded value into each row, so a path list was cloned once
per path, and work was still charged per entry even after charging became cheap.
Borrowing the yielded lists and admitting work per path — or per 1024 steps —
took direct execution on the 16,384-node chain from 3,190 ms to 1,298 ms and
ordinary Cypher from 36,913 ms to 20,255 ms. At 4,096 nodes with five measured
samples, direct improved 58.7% and ordinary Cypher 45.2%.

The meter was never one problem. It was the same problem in three places.

On the 65,536-node chain, the full run fell from **3 hours 32 minutes to 35
minutes**, with ordinary Cypher going from 5,808,625 ms to 594,419 ms. Throughout,
the four frozen historical binaries are byte-identical across every run and moved
by at most 1.4%. That control is what makes the rest attributable to the code
rather than to the machine.

## The Rust rewrite beats the C++ it came from, and not for the reason you'd guess

The Rust implementation finishes the 65,536-node chain in 10,888 ms against the
NetworKit-derived C++ at 30,454 — 2.8x. At 4,096 nodes it is 1.55x. **The gap
widens with the work**, and that is the whole clue: a language or codegen
advantage is a constant factor, and this one grows.

`perf` over both, same chain, same limits. The C++ run spends 36.2% in
`SSSP::getPath`, 20.1% in the caller's loop, **15.2% in `do_user_addr_fault`** —
kernel page-fault handling — and another 10.7% between libc and kernel memory
locking. The Rust run spends 66.7% in its Dijkstra and 33.2% in consumption, with
no allocator or kernel frame above 2%. About a quarter of the C++ time is the
allocator and the kernel. None of the Rust time is.

The cause is in the data structures. NetworKit stores predecessors as
`std::vector<std::vector<node>>`, one heap block per node, so reconstruction
chases pointers across n separate allocations — the price of supporting multiple
shortest paths. `getPath` then builds a fresh vector per target with `push_back`
and no `reserve`, growing and reallocating as it goes, then reverses it, and the
caller allocates a second vector for the costs. On a chain the paths sum to
`n(n+1)/2` entries, so at 65,536 that is 2.1 billion entries through 131,072
allocations whose sizes grow linearly with the target. That churn is what the
page faults are.

The Rust side keeps a flat parent array and two reconstruction buffers allocated
once and cleared per target. After the first few paths it never allocates again.

So this is not a verdict on the languages, and it would be dishonest to sell it
as one. `getPath` returns by value, which *cannot* reuse a caller's buffer: the
cost is forced by the shape of the interface, and the same C++ with an
out-parameter or a visitor would close most of it. The interesting finding is
that the most expensive thing in a mature C++ graph library, on this workload,
was an API decision.

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
number was affected, because every published run used bulk loading. What caught
it was the benchmark's own per-sample comparison against a C++ reference.

## What did not work

`reduce` now exists in Grust's Cypher. It returns aggregates identical to the
`UNWIND` form, and it is slower: 4.6 to 4.9 times on the pin where it landed, and
about 6.1 times on current code, where the row-expansion path improved faster
than the fold did. The benchmark keeps the row-expansion shape.

The reason it stays slower is the same problem one axis over. Work accounting is
now lock-free, but each folded element still evaluates through the general scoped
evaluator, and every variable reference clones a value and charges its bytes
through a memory account that takes the state mutex. Two references per element
means two lock round-trips plus a string allocation, and the per-entry string is
inherent to path node identifiers being a string type. Closing the gap needs
either byte accounting without the mutex — exactly what work accounting already
got — or a compiled fold. Neither is in this release, which is why the shape
stays as it is.

That comparison has shifted in an interesting way. When the clock reads dominated,
removing the row expansion was worth about 4% and the query shape was irrelevant.
On current code the same measurement is 1,533 ms against 718 ms without the
expansion — the shape is now worth about half the query. The fold is still the
slower way to write it, but the prize for making it fast is no longer rounding
error.

A first attempt at deadline sampling regressed every path that sets no deadline
by 13 to 46%, because the sampling counter ticked whether or not a deadline
existed. It reached `main` before the paired measurement that would have caught
it. The fix returns before both the counter and the clock when there is no
deadline, and a re-measurement put every affected cell back within dispersion.

An audit of this post's own numbers against the retained samples found three
ranges stated more favourably than they measured, and corrected them.

Both kinds of failure are here because a benchmark that publishes only the
changes that worked is not measuring, it is advertising.

## Evidence beyond one chain

The historical variants pass 30 small cases: six graph families across BFS,
Dijkstra, weak and strong components, and PageRank. The runtime image passes 45
kernel and Arrow interchange checks; the current-source images add 216. Every
matrix run for this work — 60 cases at 128 and 1,024 nodes, 30 at 4,096, on each
source pin — passed, as did 2,016 paired samples across four sweeps.

Those checks keep algorithm-specific distinctions visible. BFS compares
reachability and level order because native and GDS result shapes differ.
Component partitions are canonicalized. PageRank uses the same weighted model but
different convergence rules, checked within recorded tolerances. There is no
combined score that hides the differences.

The large chain has unique shortest paths, so every distance, the path-entry
count, the node-ID sum and the cumulative-cost sum are independently calculated
and compared. Matching aggregates on a tied graph would not, by itself, prove
every interior node correct.

## What these numbers are not

Not a ranking of engines: the columns are execution classes with unequal,
disclosed boundaries. Not portable — the clock findings are shaped by one host's
`xen` clocksource, and a TSC host would show a smaller penalty for the same code.
The 16,384 and 65,536 results are single samples establishing completion, not
stable rankings. Results from four source pins are kept in four separate sets and
never pooled, and the M1 Max table above is not comparable with any of them.

## Reproducing it

```sh
git clone https://github.com/querygraph/adversarial-graph-algorithms
cd adversarial-graph-algorithms

# the published September measurement, from the checksum-verified snapshot
./docker/run.sh --frozen --output /tmp/frozen -- --full-path --algorithms dijkstra \
  --families path --sizes 16384 65536 --warmups 0 --repeats 1 --label reproduced

# current sources: Grust and Turso at their pinned commits, with Arrow,
# DataFusion and the mimalloc allocator
./docker/run.sh --output /tmp/current -- --full-path --sizes 128 1024 \
  --warmups 1 --repeats 5 --label current
```

The repository carries a checksum-verified snapshot of the measured source, so
the frozen run needs no sibling checkouts; official Neo4j and GDS archives are
downloaded and checksum-verified separately. The samples behind every table are
committed under `publication/evidence/`, with checksums, so the distributional
claims — the cells, the medians, the dispersions — are recomputable without
rerunning anything.

The [Graph tab](https://adversari.al/graph) indexes this alongside the
[graph-query benchmark](https://adversari.al/graph/queries) and the
[strain ledger](https://adversari.al/graph/strain). Their datasets, protocols and
execution classes are not pooled into one leaderboard. The
[Adversarial Cognition book](https://firstpair.org/read/adversarial-cognition/)
carries the longer discussion of testable boundaries. Here the boundary is the
output itself: what must exist, what must be consumed, and what the clock
includes.
