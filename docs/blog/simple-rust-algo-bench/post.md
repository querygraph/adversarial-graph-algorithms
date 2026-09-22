# Same function first: an in-memory kernel benchmark with `neo4j-labs/graph` as a participant

Grust gives Rust applications one property-graph API across memory, embedded databases, SQL systems and remote graph services, and since Mysid it registers thirty-three graph algorithms over a projection of any of them. The note at the end of this repository's [related-work document](https://github.com/querygraph/adversarial-graph-algorithms/blob/633ff36305e1d6b201d04570a48f400e678dc70b/docs/related-work.md) compared those kernels with the best-known Rust graph algorithm library, [`neo4j-labs/graph`](https://github.com/neo4j-labs/graph), and ended by saying the comparison was unmeasured: the way to settle it was to add the library as a participant, under the same disclosed boundaries as every other column, and until then the note was a description of scope rather than a result.

That participant now exists. This post is about what adding it established, what it did not, the two measurement artifacts it found in our own timer, the regression it caught, and the cells where the current Grust commit is slower than the release before it. The benchmark is `simple-rust-algo-bench`, the results document is [`simple-rust-algo-bench-results.md`](https://github.com/querygraph/adversarial-graph-algorithms/blob/633ff36305e1d6b201d04570a48f400e678dc70b/docs/simple-rust-algo-bench-results.md), the evidence bundle is [`b5-quegee`](https://github.com/querygraph/adversarial-graph-algorithms/tree/633ff36305e1d6b201d04570a48f400e678dc70b/docs/simple-rust-algo-bench-evidence/b5-quegee), and every number below is computed from that bundle by a script rather than copied from a table. The same files render the [kernels page on adversari.al](https://adversari.al/graph/kernels).

## One execution class, and nothing smuggled into a number

The benchmark measures one thing: an in-memory graph built once from the same input, with kernels called directly through each project's own Rust API. No Cypher in any row, because a query layer parses, plans, admits and converts, and timing it against a library call measures the layer rather than the kernel. No database, no snapshot. And no feature difference absorbed into a shared cell: where Grust runs a kernel under a cooperative budget and the library runs it without one, that difference is a separate, labelled measurement, not an unexplained slowdown.

Five participants build in one image and are five distinct binaries. `neo4j-graph` is the `neo4j-labs/graph` library, graph 0.3.2 / graph_builder 0.4.2, through its builder and `graph::prelude`; an earlier run keyed it `library`, renamed because Grust is a library too. `icebug` is the Arrow update of NetworKit, in C++. `icecat` is the Rust rewrite of those kernels. `grustcat` is Grust's model projected to packed Arrow adjacency. `grust` is Grust's own kernels over `GraphProjection`, the general kernel over a backend-neutral graph. The lineage is NetworKit → Icebug → Icecat → Grustcat, and a column that skipped the middle could not tell a rewrite's cost from a design's. The crate names do not follow the lineage: Icecat's Rust crates are named `icebug-*` for compatibility, which an earlier draft of the design labelled backwards.

Four kernels, only what the participants share: PageRank, weakly connected components, breadth-first distances from one source, and triangle counting. Tables are as wide as the participants that have the kernel, each naming who is absent and that the reason is no such kernel rather than a slow one. Two of the five, `icecat` and `grustcat`, cannot use a second thread at all, so the full-width run is not a five-column parallel table and no width ratio is drawn against them.

## Parity, and what it did and did not establish

Every participant is checked against a reference written independently in Python, PageRank iterated to the stated tolerance, components by union-find, BFS by queue, triangles by ordered enumeration, before anything is timed. A cell that did not agree is never timed. At the commit under test, the protocol fixture set at each of three concurrencies shows 252 agreements, 32 absences and 4 mismatches, and the mismatches are all one difference: `neo4j-graph`'s PageRank does not redistribute dangling mass, so on a graph with a node that has no outgoing edge it computes a different function. NetworKit defaults to the same and offers an option this harness sets; Grust's kernels always redistribute. That is a choice, not a defect, and the consequence is that PageRank is compared only on the two dangling-free families, `hub` and `uniform`.

`neo4j-graph` also accumulates and returns `f32` where every other participant is `f64`. That is stated under every PageRank table as a boundary rather than a rounding footnote: its score array is half the bytes. At 65,536 nodes every participant's working set fits in the measuring host's L3, so single precision buys bandwidth on one array and no cache residency; at 4,194,304 nodes an `f64` score array no longer fits that L3 on its own and the `f32` one does, which is arithmetic from array sizes rather than a measurement of cache behaviour.

**What parity did not establish is bit identity across implementations.** The first run of this benchmark said the reference, `grust`, `icecat` and `grustcat` return the same `f64` bit pattern for PageRank. It had never compared bits: it held the maximum and the sum to the stopping tolerance and stored no scores. When the rerun compared whole vectors, Grust's push kernel matched the reference on 65,467 of 65,536 scores of `uniform-65536` within 2 ulps and on 3,230 of `hub-65536` within 7; the pull kernel matched 29,430 of `uniform-65536` within 4. The sentence was withdrawn. What holds is weaker and sufficient: every `f64` participant agrees with the reference far inside the stopping tolerance with the same iteration count, so they compute the same function to the precision that tolerance defines, which is what licenses comparing their speeds. Bit identity holds where it is now stated, between Grust builds: the commit under test returns v0.22.0's PageRank vector bit for bit, every score by digest and the iteration count, on 108 of 108 rows across three accounting modes and every fixture at every concurrency, and that gate is what licenses the kernel comparison below. A kernel that changed a score computes a different function.

## The first artifact: the transpose was on the wrong side of the timer

Grust's pull PageRank kernel needs the incoming adjacency, and at v0.22.0 a projection builds it lazily inside the first kernel call that asks for it. The first timed run made exactly one call at a concurrency that selects the pull kernel, so every Grust PageRank time in it contained a one-off transpose. `grustcat`, `neo4j-graph` and NetworKit build their reverse adjacency in their constructors, inside the build timer, and `icecat` builds it between the two timers and reports it apart. The same work sat on opposite sides of the boundary, and the run's headline per-iteration figure divided that build across the iterations. It was found by profiling outside the harness and then measured inside it.

The later commit has `prepare_incoming()`; the `grust-next` participant calls it inside the build timer and reports its share as `incoming_ms`. v0.22.0 has no such method, so every Grust build runs the kernel twice on one projection and reports both calls. The second call runs on warm caches, which is not the condition of any other participant's timed call, so it is labelled rather than presented as the corrected number. One thread, pull kernel, milliseconds, median ± MAD:

| fixture | `grust` v0.22.0 first | v0.22.0 second | `grust-next` first | transpose, in `build_ms` | `grustcat` |
| --- | ---: | ---: | ---: | ---: | ---: |
| `hub-65536` | 52.59 ± 0.21 | 44.00 ± 0.17 | 34.02 ± 0.13 | 6.41 | 30.23 ± 0.03 |
| `uniform-65536` | 51.51 ± 0.43 | 42.87 ± 0.33 | 32.48 ± 0.20 | 6.36 | 29.27 ± 0.12 |
| `hub-2097152` | 4987.08 ± 70.65 | 4398.60 ± 71.31 | 2170.69 ± 43.13 | 552.73 | 1946.08 ± 46.23 |
| `uniform-2097152` | 5186.50 ± 59.96 | 4575.57 ± 48.02 | 2207.80 ± 62.26 | 529.75 | 2399.05 ± 35.57 |
| `hub-4194304` | 12663.28 ± 36.71 | 11300.51 ± 50.55 | 6941.34 ± 23.40 | 1184.65 | 6040.22 ± 40.65 |
| `uniform-4194304` | 13286.45 ± 45.87 | 11878.26 ± 54.01 | 7030.83 ± 59.57 | 1173.68 | 7113.24 ± 94.56 |

BFS, WCC and triangles read no incoming adjacency and were never affected.

## The second artifact: the allocator state, and it was ours too

The rerun that measured the transpose built it inside the build timer for every algorithm, to make Grust's build column the same work as `grustcat`'s constructor. WCC and BFS never read the incoming adjacency, so for those two the harness built and freed a transpose nothing would read, immediately before the call it was timing. Freeing a large mapped chunk raises glibc's own mmap threshold, so the next call's large allocations came from a different place than the v0.22.0 column's. That rerun's `grust-next` first calls were slower, and its second calls faster, than the code alone accounts for, and its "the cause is unexplained" paragraph was about this.

The correction has three parts, each with the reason it is not the other choice. The transpose is now built in the build timer only for the kernel that reads it; the previous behaviour is kept as a `+eager` variant and timed as its own labelled row, so the correction is shown rather than asserted. Matching a constructor was the wrong thing to match: a build column that does work no kernel will read is not the same measurement as one that does work the kernel needs. Every participant now reads its minor page faults on both sides of the call it times, outside the timer, so a time that moved while the counter did not is not this effect. And whether to pin the allocator at all was decided by measurement rather than assumption: pinning `GLIBC_TUNABLES=glibc.malloc.mmap_threshold` for the Grust participants alone would compare two allocators, the same kind of error again, so two runs repeat the protocol sizes with the threshold pinned for the whole container, every participant included.

Over the 48 WCC and BFS first-call cells at the protocol sizes, the corrected `grust-next` takes a median of -2.5 minor page faults against v0.22.0, and the `+eager` row a median of +0 against the corrected one; where `+eager` moves the counter at all, 11 cells, it takes 5 to 112 more faults, which is the artifact measured inside the harness. The rule for the pinning decision was fixed before the runs: the published tables stay on the default allocator, because glibc's default is what every participant's users have and none of these projects sets a tunable, unless the median difference in first-call faults between the two Grust builds exceeded 25. It is 2.5. The pinned runs stay as a labelled probe, and the probe shows the threshold is not a Grust-specific effect: median change under pinning, per participant, `grust` +0.1% over 24 cells; `grust-next` +2.0% over 24 cells; `grustcat` +0.7% over 12 cells; `icebug` -0.2% over 12 cells; `icecat` +4.4% over 12 cells; `neo4j-graph` +0.7% over 12 cells.

## The regression, which was real

Between v0.22.0 and the commit the rerun timed, `WorkMeter::charge` had been pushed out of line in sixteen kernels. That is the call every kernel makes once per unit of graph work, so every counted row of that rerun was measured with it out of line. It is inlined again at `ca68900`, the commit this campaign times, which also adds child contexts and `with_execution`. The rerun's counted WCC and BFS rows therefore carried both the allocator state and the outlined charge, and what remains after both are corrected is stated rather than inferred. Counted BFS on the first call is what the attribution had left open; at one thread, 8 of 8 `hub` and `uniform` first-call cells are still slower than v0.22.0, +0.9% to +6.7%, where the previous rerun's same cells ran -4.0% to +11.4%; at full width, 2 of 4, -22.2% to +9.4%. The page-fault counts beside each row are within a few of each other, so what is left is not the allocator, and it is not the transpose, which this run does not build for BFS. What it is remains unexplained.

The PageRank kernel change itself, second call against second call so the transpose is cached on both sides, with both builds returning the same bits:

| fixture | run | kernel | v0.22.0 | `ca68900` | ratio |
| --- | --- | --- | ---: | ---: | ---: |
| `hub-16384` | one-thread | pull | 9.60 ± 0.01 | 7.98 ± 0.00 | 0.831 |
| `hub-16384` | one-thread | push | 50.40 ± 0.01 | 23.16 ± 0.04 | 0.460 |
| `hub-65536` | one-thread | pull | 44.00 ± 0.17 | 33.20 ± 0.10 | 0.755 |
| `hub-65536` | one-thread | push | 202.19 ± 0.14 | 95.60 ± 0.56 | 0.473 |
| `uniform-16384` | one-thread | pull | 9.20 ± 0.00 | 7.54 ± 0.02 | 0.819 |
| `uniform-16384` | one-thread | push | 47.73 ± 0.01 | 21.50 ± 0.01 | 0.450 |
| `uniform-65536` | one-thread | pull | 42.87 ± 0.33 | 31.61 ± 0.25 | 0.737 |
| `uniform-65536` | one-thread | push | 191.54 ± 0.13 | 88.63 ± 0.72 | 0.463 |
| `hub-16384` | full-width | pull | 3.46 ± 0.02 | 3.29 ± 0.01 | 0.951 |
| `hub-65536` | full-width | pull | 8.71 ± 0.14 | 7.10 ± 0.06 | 0.816 |
| `uniform-16384` | full-width | pull | 3.30 ± 0.07 | 3.39 ± 0.25 | 1.027 |
| `uniform-65536` | full-width | pull | 8.16 ± 0.07 | 6.68 ± 0.10 | 0.819 |
| `hub-2097152` | large-one-thread | pull | 4398.60 ± 71.31 | 1935.33 ± 23.39 | 0.440 |
| `hub-2097152` | large-one-thread | push | 7772.38 ± 75.86 | 4115.77 ± 46.30 | 0.530 |
| `uniform-2097152` | large-one-thread | pull | 4575.57 ± 48.02 | 2010.09 ± 52.55 | 0.439 |
| `uniform-2097152` | large-one-thread | push | 7545.63 ± 82.12 | 4300.81 ± 153.48 | 0.570 |
| `hub-2097152` | large-full-width | pull | 502.37 ± 9.55 | 233.44 ± 1.37 | 0.465 |
| `uniform-2097152` | large-full-width | pull | 548.05 ± 17.24 | 253.45 ± 9.76 | 0.462 |
| `hub-4194304` | xlarge-one-thread | pull | 11300.51 ± 50.55 | 6969.36 ± 27.73 | 0.617 |
| `hub-4194304` | xlarge-one-thread | push | 26010.01 ± 279.41 | 12936.74 ± 26.41 | 0.497 |
| `uniform-4194304` | xlarge-one-thread | pull | 11878.26 ± 54.01 | 7036.39 ± 65.96 | 0.592 |
| `uniform-4194304` | xlarge-one-thread | push | 24393.09 ± 778.50 | 12394.91 ± 269.46 | 0.508 |
| `hub-4194304` | xlarge-full-width | pull | 1347.79 ± 3.82 | 710.51 ± 15.55 | 0.527 |
| `uniform-4194304` | xlarge-full-width | pull | 1446.17 ± 3.87 | 750.56 ± 21.85 | 0.519 |

The ratio is below 1 in 23 of 24 cells, between 0.439 and 1.027. The later commit hoists each source's share out of the pull kernel's arc loop and charges the push loop's arcs in blocks instead of one atomic per arc; the large and extra-large sizes are where the hoist changes which arrays are indexed at random beyond the L3, and they are in the table because a change measured only where everything fits in cache is a change measured where it matters least.

## What the accounting modes cost, and buy

Every `grust-next` row names its mode. `counted` is the default and what v0.22.0 always does: work is charged to a shared counter and cancellation is observed, so an untrusted or shared caller can be given an algorithm without being given the machine, and an exhausted budget stops a kernel where it stands. `work-uncounted` charges nothing and still observes cancellation. `unchecked` does neither and cannot be stopped once started. Memory admission is performed in every mode. `neo4j-graph` performs no accounting, so `unchecked` is its like-for-like row and the distance to `counted` is what the guarantee costs; its column is `f32` on its own stopping rule, a total for a different number of iterations, not a kernel comparison. First call, protocol size, milliseconds:

| fixture | run | kernel | counted | work-uncounted | unchecked | `neo4j-graph` |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `hub-65536` | one-thread | pagerank, pull | 34.02 ± 0.13 | 31.92 ± 0.12 | 31.14 ± 0.26 | 35.93 ± 0.14 |
| `hub-65536` | one-thread | pagerank, push | 95.14 ± 0.47 | 58.50 ± 0.10 | 56.15 ± 0.25 | 35.93 ± 0.14 |
| `hub-65536` | one-thread | wcc, concurrency 1 | 6.46 ± 0.04 | 4.28 ± 0.02 | 3.84 ± 0.05 | 3.75 ± 0.01 |
| `hub-65536` | one-thread | wcc, concurrency unset | 16.67 ± 0.01 | 7.10 ± 0.05 | 6.03 ± 0.01 | 3.75 ± 0.01 |
| `hub-65536` | one-thread | triangles, concurrency 1 | 72.51 ± 0.02 | 71.64 ± 0.11 | 71.10 ± 0.33 | 35.34 ± 0.15 |
| `hub-65536` | one-thread | triangles, concurrency unset | 72.29 ± 0.06 | 71.36 ± 0.04 | 70.87 ± 0.11 | 35.34 ± 0.15 |
| `uniform-65536` | one-thread | pagerank, pull | 32.48 ± 0.20 | 30.66 ± 0.18 | 29.58 ± 0.11 | 44.24 ± 0.08 |
| `uniform-65536` | one-thread | pagerank, push | 88.77 ± 0.68 | 55.19 ± 0.25 | 53.94 ± 0.24 | 44.24 ± 0.08 |
| `uniform-65536` | one-thread | wcc, concurrency 1 | 9.81 ± 0.03 | 8.49 ± 0.01 | 7.88 ± 0.05 | 3.75 ± 0.00 |
| `uniform-65536` | one-thread | wcc, concurrency unset | 16.96 ± 0.03 | 8.06 ± 0.04 | 6.85 ± 0.11 | 3.75 ± 0.00 |
| `uniform-65536` | one-thread | triangles, concurrency 1 | 78.55 ± 1.00 | 77.72 ± 0.06 | 77.84 ± 0.20 | 39.47 ± 0.14 |
| `uniform-65536` | one-thread | triangles, concurrency unset | 78.43 ± 0.03 | 78.37 ± 0.22 | 77.15 ± 0.09 | 39.47 ± 0.14 |
| `hub-65536` | full-width | pagerank, pull | 7.22 ± 0.04 | 4.70 ± 0.01 | 4.69 ± 0.02 | 15.03 ± 0.04 |
| `hub-65536` | full-width | wcc, concurrency as the run | 1.48 ± 0.05 | 1.24 ± 0.02 | 1.30 ± 0.09 | 3.18 ± 0.05 |
| `hub-65536` | full-width | triangles, concurrency as the run | 28.78 ± 0.09 | 28.14 ± 0.68 | 27.39 ± 0.30 | 3.50 ± 0.05 |
| `uniform-65536` | full-width | pagerank, pull | 7.01 ± 0.16 | 4.48 ± 0.05 | 4.51 ± 0.04 | 16.30 ± 0.28 |
| `uniform-65536` | full-width | wcc, concurrency as the run | 1.80 ± 0.06 | 1.52 ± 0.09 | 1.54 ± 0.05 | 3.08 ± 0.13 |
| `uniform-65536` | full-width | triangles, concurrency as the run | 29.06 ± 0.08 | 28.25 ± 0.06 | 27.90 ± 0.02 | 3.99 ± 0.04 |

Over those 18 cells `counted` takes +0.9% to +176.5% against `unchecked`, the largest on wcc, concurrency unset, `hub-65536` at one-thread. Counting also costs in the build: `grust-next`'s `build_ms` for PageRank on `hub-65536` at one thread is 47.07 ms counted, 38.00 work-uncounted and 37.56 unchecked, because building the projection and its transpose charges work too. The push kernel's block charging is part of the kernel change above; the table says how much of the distance to `unchecked` remains in each mode.

## The results, with the ones against this side first

**Every cell that got worse.** Counted `grust-next` against v0.22.0, same fixture, kernel, concurrency and call, over every run: 70 of the 216 counted cells with a v0.22.0 counterpart are slower on `ca68900`, by +0.0% to +117.4%. The largest: `path-65536` pagerank full-width pull second +117.4%; `path-16384` pagerank full-width pull second +86.6%; `path-65536` triangles full-width concurrency as the run second +64.2%; `path-65536` pagerank full-width pull first +61.1%; `path-16384` triangles full-width concurrency as the run second +53.6%. Three shapes account for most of that list, and only one of them has a cause.

- **PageRank on the `path` family, above all at full width.** 5 of them, +1.5% to +117.4%: `path-16384` full-width first 10.44 to 15.45 ms; `path-16384` full-width second 8.65 to 16.14 ms; `path-65536` full-width first 16.31 to 26.27 ms; `path-65536` full-width second 12.24 to 26.62 ms; `path-65536` one-thread second 51.00 to 51.76 ms. `path` is a chain, where the pull kernel's work per node is one arc and a parallel split has nothing to amortise. It is not a family PageRank is compared on, because it has a dangling node and `neo4j-graph` computes a different function there; it was timed, it got much worse, and the cause is not established. A kernel that is faster on every `hub` and `uniform` cell at the same width and twice as slow on a chain is a finding about the shape of the graph, not a rounding. **Unexplained.**
- **The triangles second call.** 22 of them, +0.1% to +64.2%, and every one of them takes more minor page faults than v0.22.0 did: a median of 32 on v0.22.0 against 543.5 on `ca68900`. v0.22.0's second triangle call allocates almost nothing and the later commit's allocates again. That is a change in what the second call does rather than in how fast it does it, and it is the one shape with a cause.
- **WCC's first call at concurrency 1.** Slower on 6 of 8 fixtures at one thread, -3.9% to +13.6%, with the page-fault counts equal on 7 of 8. Where the faults are equal it is not the allocator; the same cells at concurrency unset are not slower, and at full width the same kernel is far faster than v0.22.0. **Unexplained.**

**Triangle counting at width.** On `uniform-65536` at one thread, `neo4j-graph` counts triangles in 39.47 ± 0.14 ms and Grust's counted kernel at concurrency 1 in 78.55 ± 1.00; at 16 workers, 3.99 ± 0.04 against 29.06 ± 0.08. The gap widens with width, and the accounting rows show it is not the guarantee: `unchecked` at full width is 27.90 ± 0.02. Where it lives is not established here.

**PageRank on `layered-16384` at sixteen threads.** First call -2.7%, second call +5.8%. The second call is still slower and the first is not, which is the same shape the previous rerun reported. **Unexplained.**

**The lineage, at equal width.** PageRank at 65,536 nodes, one thread, first call, per iteration in milliseconds, because the participants stop on different rules and only per-iteration compares kernels. This is the one configuration in which the comparison is valid:

| participant | precision | `hub` / iter | iters | `uniform` / iter | iters | boundary |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `neo4j-graph` | f32 | 1.283 | 28 | 1.301 | 34 | no accounting; its own stopping rule |
| `icebug` | f64 | 3.511 | 12 | 3.590 | 11 | NetworKit, `DISTRIBUTE_SINKS` set |
| `icecat` | f64 | 2.007 | 17 | 2.043 | 16 | sequential by construction |
| `grustcat` | f64 | 1.778 | 17 | 1.829 | 16 | sequential by construction; tolerance fixed in the crate |
| `grust#1` | f64 | 3.093 | 17 | 3.219 | 16 | v0.22.0, pull: the transpose is built inside this call |
| `grust-next@counted#1` | f64 | 2.001 | 17 | 2.030 | 16 | counted, pull: the transpose is in `build_ms` |

The general kernel over the backend-neutral projection, with the transpose on the same side as everyone else's and the work meter charging, runs at +11.0% per iteration against the specialised Arrow kernel that descends from it on `uniform`, where the first run, with the transpose inside Grust's timer alone, had reported a wider gap. That sentence is about a boundary correction and a kernel change together; the tables above separate them.

**Drift between campaigns on unchanged code.** The participants that did not change between the previous rerun and this one, on the same fixtures and the same host, move -49.6% to +8.1% between the two campaigns, and the largest of those is `icebug`, a participant containing no Grust at all. Both campaigns were built from clean trees and ran on an idle host; this one additionally dropped the page cache before starting. **Unexplained**, and the reason a cell is only ever compared with other cells of its own run.

## The host, and the record

One host, quegee, 16 vCPU on 8 physical cores, 24.8 MB L3, not burstable. 8 timed runs, all clean, none discarded, none rerun; 1,840 cells, of which 1 reached the dispersion rule of 0.25 MAD/median and enters no table (`grust-next@counted` pagerank `path-65536` first in pinned-full-width, 48.21 ± 12.26). Steal is recorded per cell; the largest over a run was 129 ticks across `xlarge-one-thread`'s 4300 seconds. 1 resident agent session was seen by name across the campaign, asleep, and it is in every snapshot of the record rather than reconstructed afterwards. Two parity invocations are marked shared because the kernel's own `kswapd` and `kcompactd` woke to reclaim memory for the run; the idle rule does not distinguish that from a second workload, and it was not weakened to let a run pass. The cause was removed instead, by dropping the page cache before the timed campaign began.

## What is not here

**Not a ranking.** The accounting table puts `neo4j-graph` beside Grust's modes so a reader can compare like for like, and the pinned probe puts every participant beside itself; nothing reduces them to an order, and `neo4j-graph` computes in `f32` to its own stopping rule.

**Not portable.** Every timing is a fact about one host on one day as much as about the code. Numbers produced on burstable hosts during this work were for shape only and none is quoted.

**No cause** for what is left of the WCC and BFS first-call slowdown, for PageRank's collapse on the `path` family at full width, for the `layered-16384` second call, or for the drift between campaigns on unchanged code. Only their shapes, and for the first the knowledge that it is not the allocator.

**A dated result.** v0.22.0 and `ca68900` are what was timed. A column measured later describes that code, and the related-work note's remark about a moving target still applies to it.

The harness is `docker/simple-rust-algo-bench/` in the repository, a separate image from the full-path harness. `b5_report.py` regenerates the results document's B5 section from the bundle byte for byte, `b5_post.py` generates this post from the same files, and the site's renderer fails its build on an unlisted evidence file, an unrendered placeholder, or a value no placeholder uses.
