# Same function first: an in-memory kernel benchmark with `neo4j-labs/graph` as a participant

Grust gives Rust applications one property-graph API across memory, embedded databases, SQL systems and remote graph services, and since Mysid it registers thirty-three graph algorithms over a projection of any of them. The note at the end of this repository's [related-work document](https://github.com/querygraph/adversarial-graph-algorithms/blob/faab6c806a4a408e91af4c7022064890240f806a/docs/related-work.md) compared those kernels with the best-known Rust graph algorithm library, [`neo4j-labs/graph`](https://github.com/neo4j-labs/graph), and ended by saying the comparison was unmeasured: the way to settle it was to add the library as a participant, under the same disclosed boundaries as every other column, and until then the note was a description of scope rather than a result.

That participant now exists. This post is about what adding it established, what it did not, the two measurement artifacts it found in our own timer, the regression it caught, the one commit written against that regression and what timing it under an unchanged protocol did and did not close, and the cells where the current Grust commit is slower than the release before it. The benchmark is `simple-rust-algo-bench`, the results document is [`simple-rust-algo-bench-results.md`](https://github.com/querygraph/adversarial-graph-algorithms/blob/faab6c806a4a408e91af4c7022064890240f806a/docs/simple-rust-algo-bench-results.md), the evidence bundles are [`b5-quegee`](https://github.com/querygraph/adversarial-graph-algorithms/tree/faab6c806a4a408e91af4c7022064890240f806a/docs/simple-rust-algo-bench-evidence/b5-quegee) and [`b6-quegee`](https://github.com/querygraph/adversarial-graph-algorithms/tree/faab6c806a4a408e91af4c7022064890240f806a/docs/simple-rust-algo-bench-evidence/b6-quegee), and every number below is computed from those bundles by a script rather than copied from a table. Where a B5 figure appears beside a B6 one it is B5's own ratio from B5's bundle; no B5 time is ever divided by a B6 time. The same files render the [kernels page on adversari.al](https://adversari.al/graph/kernels).

## One execution class, and nothing smuggled into a number

The benchmark measures one thing: an in-memory graph built once from the same input, with kernels called directly through each project's own Rust API. No Cypher in any row, because a query layer parses, plans, admits and converts, and timing it against a library call measures the layer rather than the kernel. No database, no snapshot. And no feature difference absorbed into a shared cell: where Grust runs a kernel under a cooperative budget and the library runs it without one, that difference is a separate, labelled measurement, not an unexplained slowdown.

Five participants build in one image and are five distinct binaries. `neo4j-graph` is the `neo4j-labs/graph` library, graph 0.3.2 / graph_builder 0.4.2, through its builder and `graph::prelude`; an earlier run keyed it `library`, renamed because Grust is a library too. `icebug` is the Arrow update of NetworKit, in C++. `icecat` is the Rust rewrite of those kernels. `grustcat` is Grust's model projected to packed Arrow adjacency. `grust` is Grust's own kernels over `GraphProjection`, the general kernel over a backend-neutral graph. The lineage is NetworKit → Icebug → Icecat → Grustcat, and a column that skipped the middle could not tell a rewrite's cost from a design's. The crate names do not follow the lineage: Icecat's Rust crates are named `icebug-*` for compatibility, which an earlier draft of the design labelled backwards.

Four kernels, only what the participants share: PageRank, weakly connected components, breadth-first distances from one source, and triangle counting. Tables are as wide as the participants that have the kernel, each naming who is absent and that the reason is no such kernel rather than a slow one. Two of the five, `icecat` and `grustcat`, cannot use a second thread at all, so the full-width run is not a five-column parallel table and no width ratio is drawn against them.

## Parity, and what it did and did not establish

Every participant is checked against a reference written independently in Python, PageRank iterated to the stated tolerance, components by union-find, BFS by queue, triangles by ordered enumeration, before anything is timed. A cell that did not agree is never timed. At the commit under test, the protocol fixture set at each of three concurrencies shows 252 agreements, 32 absences and 4 mismatches, and the mismatches are all one difference: `neo4j-graph`'s PageRank does not redistribute dangling mass, so on a graph with a node that has no outgoing edge it computes a different function. NetworKit defaults to the same and offers an option this harness sets; Grust's kernels always redistribute. That is a choice, not a defect, and the consequence is that PageRank is compared only on the two dangling-free families, `hub` and `uniform`. All 9 parity invocations ran once, in order, on an idle host; 3 of them exited 1, the parity script's exit on any mismatching row, here the four `neo4j-graph` rows above, and the driver takes its verdict from the file rather than the exit code.

`neo4j-graph` also accumulates and returns `f32` where every other participant is `f64`. That is stated under every PageRank table as a boundary rather than a rounding footnote: its score array is half the bytes. At 65,536 nodes every participant's working set fits in the measuring host's L3, so single precision buys bandwidth on one array and no cache residency; at 4,194,304 nodes an `f64` score array no longer fits that L3 on its own and the `f32` one does, which is arithmetic from array sizes rather than a measurement of cache behaviour.

**What parity did not establish is bit identity across implementations.** The first run of this benchmark said the reference, `grust`, `icecat` and `grustcat` return the same `f64` bit pattern for PageRank. It had never compared bits: it held the maximum and the sum to the stopping tolerance and stored no scores. When the rerun compared whole vectors, Grust's push kernel matched the reference on 65,467 of 65,536 scores of `uniform-65536` within 2 ulps and on 3,230 of `hub-65536` within 7; the pull kernel matched 29,430 of `uniform-65536` within 4. The sentence was withdrawn. What holds is weaker and sufficient: every `f64` participant agrees with the reference far inside the stopping tolerance with the same iteration count, so they compute the same function to the precision that tolerance defines, which is what licenses comparing their speeds. Bit identity holds where it is now stated, between Grust builds: the commit under test returns v0.22.0's PageRank vector bit for bit, every score by digest and the iteration count, on 108 of 108 rows across three accounting modes and every fixture at every concurrency, and that gate is what licenses the kernel comparison below. A kernel that changed a score computes a different function.

## The first artifact: the transpose was on the wrong side of the timer

Grust's pull PageRank kernel needs the incoming adjacency, and at v0.22.0 a projection builds it lazily inside the first kernel call that asks for it. The first timed run made exactly one call at a concurrency that selects the pull kernel, so every Grust PageRank time in it contained a one-off transpose. `grustcat`, `neo4j-graph` and NetworKit build their reverse adjacency in their constructors, inside the build timer, and `icecat` builds it between the two timers and reports it apart. The same work sat on opposite sides of the boundary, and the run's headline per-iteration figure divided that build across the iterations. It was found by profiling outside the harness and then measured inside it.

The later commit has `prepare_incoming()`; the `grust-next` participant calls it inside the build timer and reports its share as `incoming_ms`. v0.22.0 has no such method, so every Grust build runs the kernel twice on one projection and reports both calls. The second call runs on warm caches, which is not the condition of any other participant's timed call, so it is labelled rather than presented as the corrected number. One thread, pull kernel, milliseconds, median ± MAD:

| fixture | `grust` v0.22.0 first | v0.22.0 second | `grust-next` first | transpose, in `build_ms` | `grustcat` |
| --- | ---: | ---: | ---: | ---: | ---: |
| `hub-65536` | 68.11 ± 2.53 | 57.38 ± 1.85 | 35.21 ± 0.23 | 7.32 | 32.59 ± 0.38 |
| `uniform-65536` | 60.82 ± 3.60 | 48.70 ± 3.01 | 32.86 ± 0.37 | 7.13 | 30.88 ± 0.28 |
| `hub-2097152` | 6581.11 ± 71.46 | 5802.03 ± 38.39 | 3859.96 ± 2.75 | 686.14 | 3310.95 ± 24.32 |
| `uniform-2097152` | 6999.18 ± 112.79 | 6164.16 ± 55.86 | 3821.94 ± 99.41 | 636.85 | 3836.22 ± 12.17 |
| `hub-4194304` | 14778.23 ± 100.50 | 13074.01 ± 130.01 | 8695.93 ± 24.39 | 1482.25 | 7349.00 ± 45.76 |
| `uniform-4194304` | 15671.38 ± 112.88 | 14150.99 ± 74.58 | 9001.38 ± 40.23 | 1469.27 | 8617.93 ± 93.54 |

BFS, WCC and triangles read no incoming adjacency and were never affected.

## The second artifact: the allocator state, and it was ours too

The rerun that measured the transpose built it inside the build timer for every algorithm, to make Grust's build column the same work as `grustcat`'s constructor. WCC and BFS never read the incoming adjacency, so for those two the harness built and freed a transpose nothing would read, immediately before the call it was timing. Freeing a large mapped chunk raises glibc's own mmap threshold, so the next call's large allocations came from a different place than the v0.22.0 column's. That rerun's `grust-next` first calls were slower, and its second calls faster, than the code alone accounts for, and its "the cause is unexplained" paragraph was about this.

The correction has three parts, each with the reason it is not the other choice. The transpose is now built in the build timer only for the kernel that reads it; the previous behaviour is kept as a `+eager` variant and timed as its own labelled row, so the correction is shown rather than asserted. Matching a constructor was the wrong thing to match: a build column that does work no kernel will read is not the same measurement as one that does work the kernel needs. Every participant now reads its minor page faults on both sides of the call it times, outside the timer, so a time that moved while the counter did not is not this effect. And whether to pin the allocator at all was decided by measurement rather than assumption: pinning `GLIBC_TUNABLES=glibc.malloc.mmap_threshold` for the Grust participants alone would compare two allocators, the same kind of error again, so two runs repeat the protocol sizes with the threshold pinned for the whole container, every participant included.

Over the 48 WCC and BFS first-call cells at the protocol sizes, the corrected `grust-next` takes a median of -2 minor page faults against v0.22.0, and the `+eager` row a median of +0 against the corrected one; where `+eager` moves the counter at all, 14 cells, it takes 1 to 112 more faults, which is the artifact measured inside the harness. The rule for the pinning decision was fixed before the runs: the published tables stay on the default allocator, because glibc's default is what every participant's users have and none of these projects sets a tunable, unless the median difference in first-call faults between the two Grust builds exceeded 25. Re-decided on this campaign's own counter, it is 2. The pinned runs stay as a labelled probe, and the probe shows the threshold is not a Grust-specific effect: median change under pinning, per participant, `grust` +0.5% over 24 cells; `grust-next` +2.3% over 24 cells; `grustcat` +0.5% over 12 cells; `icebug` -1.5% over 12 cells; `icecat` +0.6% over 12 cells; `neo4j-graph` +0.6% over 12 cells.

## The regression, which was real, and the commit written against it

Between v0.22.0 and the commit the rerun timed, `WorkMeter::charge` had been pushed out of line in sixteen kernels. That is the call every kernel makes once per unit of graph work, so every counted row of that rerun was measured with it out of line. It was inlined again at `ca68900`, the commit the third campaign, B5, timed under the corrected harness. B5's tables left two things unexplained after the allocator and the transpose were ruled out by the page-fault counter beside each row: PageRank on the `path` family at full width, where the `path-65536` full-width second call ran +117.4% over v0.22.0, and WCC's first call at one worker, slower on 6 of 8 fixtures by up to +13.6%.

An attribution on the measuring host, outside the harness, found the first was false sharing. Each work meter spends its admitted block from one shared `AtomicUsize`; as a bare `Arc<AtomicUsize>` that word was a 32-byte heap chunk, and glibc's tcache handed it out beside whatever the same size class had just freed, which since the projection build went parallel was the pool's own bookkeeping, written by other cores. Every such write took the cache line from the worker, and its next exchange had to fetch it back. Grust `55a200f` pads the balance to a whole cache line, so two balances never share a line and the balance leaves the 32-byte class, and was merged to `main` as `87fc462`. What is counted, when a budget refuses, and every accounting mode are unchanged, and the parity gate above checks that rather than taking the commit's word. The commit's own measurement also said what it did not explain: the one-worker WCC residue responded to the balance's chunk size class and not to its line.

The fourth campaign, B6, times `87fc462` under B5's protocol with nothing else changed. The harness at `633ff36` differs from B5's `9ec8548` by the report script alone, a file the image copies and nothing in it runs; the twelve fixtures are SHA-256-identical to B5's; the image was built the same way on the same host from clean trees; parity came first at every concurrency; the page cache was dropped before the first timed run; the eight runs ran in B5's order. The two campaigns differ in one commit.

**The cell the commit was written for.** PageRank on `path`, pull kernel, both calls, both protocol runs, with B5's change for the same cell beside B6's. `path` is a chain with a dangling node and not a family PageRank is compared on, because `neo4j-graph` computes a different function there; it was timed, and in B5 it was where the regression was largest.

| fixture | run | call | v0.22.0 | faults | `87fc462` | faults | change | B5 said |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `path-16384` | one-thread | first | 15.51 ± 0.03 | 160 | 14.76 ± 0.02 | 96 | -4.8% | -4.3% |
| `path-16384` | one-thread | second | 14.71 ± 0.02 | 0 | 14.65 ± 0.01 | 64 | -0.4% | -0.0% |
| `path-65536` | one-thread | first | 54.48 ± 0.00 | 640 | 52.84 ± 0.44 | 384 | -3.0% | -3.7% |
| `path-65536` | one-thread | second | 51.14 ± 0.12 | 0 | 52.04 ± 0.07 | 352 | +1.8% | +1.5% |
| `path-16384` | full-width | first | 10.60 ± 0.08 | 261 | 9.91 ± 0.19 | 108 | -6.5% | +47.9% |
| `path-16384` | full-width | second | 8.86 ± 0.13 | 0 | 9.68 ± 0.05 | 64 | +9.3% | +86.6% |
| `path-65536` | full-width | first | 16.72 ± 0.24 | 755 | 12.72 ± 0.05 | 407 | -23.9% | +61.1% |
| `path-65536` | full-width | second | 12.24 ± 0.16 | 2 | 12.29 ± 0.14 | 353 | +0.4% | +117.4% |

The `path-65536` full-width second call, +117.4% in B5, is +0.4% on `87fc462`, within dispersion. The four full-width cells that B5 had at +47.9% to +117.4% are -23.9% to +9.3% here, 1 of 4 still slower beyond the dispersion of the two cells: `path-16384` second call +9.3% against B5's +86.6%. The one-thread cells are -4.8% to +1.8% against B5's -4.3% to +1.5%. The regression is closed at the cell where it was largest. Its cause was found outside this harness and is stated by the commit; what the campaign holds is the before and the after.

The PageRank kernel change itself, second call against second call so the transpose is cached on both sides, with both builds returning the same bits, and B5's ratio for the same cell beside B6's:

| fixture | run | kernel | v0.22.0 | `87fc462` | ratio | B5 ratio, `ca68900` |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `hub-16384` | one-thread | pull | 9.60 ± 0.01 | 7.97 ± 0.00 | 0.831 | 0.831 |
| `hub-16384` | one-thread | push | 50.58 ± 0.03 | 23.18 ± 0.05 | 0.458 | 0.460 |
| `hub-65536` | one-thread | pull | 57.38 ± 1.85 | 34.59 ± 0.04 | 0.603 | 0.755 |
| `hub-65536` | one-thread | push | 204.56 ± 0.32 | 95.01 ± 0.20 | 0.464 | 0.473 |
| `uniform-16384` | one-thread | pull | 9.23 ± 0.02 | 7.54 ± 0.01 | 0.817 | 0.819 |
| `uniform-16384` | one-thread | push | 48.53 ± 0.74 | 21.66 ± 0.11 | 0.446 | 0.450 |
| `uniform-65536` | one-thread | pull | 48.70 ± 3.01 | 31.90 ± 0.35 | 0.655 | 0.737 |
| `uniform-65536` | one-thread | push | 194.23 ± 0.50 | 88.52 ± 0.50 | 0.456 | 0.463 |
| `hub-16384` | full-width | pull | 3.42 ± 0.03 | 3.44 ± 0.03 | 1.004 | 0.951 |
| `hub-65536` | full-width | pull | 8.90 ± 0.19 | 7.58 ± 0.24 | 0.851 | 0.816 |
| `uniform-16384` | full-width | pull | 3.30 ± 0.05 | 3.33 ± 0.13 | 1.009 | 1.027 |
| `uniform-65536` | full-width | pull | 8.40 ± 0.08 | 6.77 ± 0.14 | 0.806 | 0.819 |
| `hub-2097152` | large-one-thread | pull | 5802.03 ± 38.39 | 3812.73 ± 101.14 | 0.657 | 0.440 |
| `hub-2097152` | large-one-thread | push | 17246.72 ± 220.63 | 7378.80 ± 66.93 | 0.428 | 0.530 |
| `uniform-2097152` | large-one-thread | pull | 6164.16 ± 55.86 | 3797.86 ± 144.29 | 0.616 | 0.439 |
| `uniform-2097152` | large-one-thread | push | 17070.93 ± 105.84 | 7023.50 ± 278.99 | 0.411 | 0.570 |
| `hub-2097152` | large-full-width | pull | 584.95 ± 5.36 | 263.12 ± 22.10 | 0.450 | 0.465 |
| `uniform-2097152` | large-full-width | pull | 614.92 ± 11.23 | 274.66 ± 18.41 | 0.447 | 0.462 |
| `hub-4194304` | xlarge-one-thread | pull | 13074.01 ± 130.01 | 8709.38 ± 18.38 | 0.666 | 0.617 |
| `hub-4194304` | xlarge-one-thread | push | 35862.50 ± 212.07 | 15597.02 ± 106.25 | 0.435 | 0.497 |
| `uniform-4194304` | xlarge-one-thread | pull | 14150.99 ± 74.58 | 8987.69 ± 46.44 | 0.635 | 0.592 |
| `uniform-4194304` | xlarge-one-thread | push | 35547.34 ± 61.75 | 15050.22 ± 172.93 | 0.423 | 0.508 |
| `hub-4194304` | xlarge-full-width | pull | 1455.25 ± 24.86 | 815.82 ± 16.57 | 0.561 | 0.527 |
| `uniform-4194304` | xlarge-full-width | pull | 1630.55 ± 1.23 | 880.33 ± 12.05 | 0.540 | 0.519 |

The ratio is below 1 in 22 of 24 cells, between 0.411 and 1.009. The later commit hoists each source's share out of the pull kernel's arc loop and charges the push loop's arcs in blocks instead of one atomic per arc; the large and extra-large sizes are where the hoist changes which arrays are indexed at random beyond the L3, and they are in the table because a change measured only where everything fits in cache is a change measured where it matters least. The large and extra-large rows are read as ratios within B6 only, for a reason under the drift heading below: the host ran every participant slower above L3 in B6 than in B5, and a B5 ratio at those sizes was taken on a different host state.

## What the accounting modes cost, and buy

Every `grust-next` row names its mode. `counted` is the default and what v0.22.0 always does: work is charged to a shared counter and cancellation is observed, so an untrusted or shared caller can be given an algorithm without being given the machine, and an exhausted budget stops a kernel where it stands. `work-uncounted` charges nothing and still observes cancellation. `unchecked` does neither and cannot be stopped once started. Memory admission is performed in every mode. `neo4j-graph` performs no accounting, so `unchecked` is its like-for-like row and the distance to `counted` is what the guarantee costs; its column is `f32` on its own stopping rule, a total for a different number of iterations, not a kernel comparison. First call, protocol size, milliseconds:

| fixture | run | kernel | counted | work-uncounted | unchecked | `neo4j-graph` |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `hub-65536` | one-thread | pagerank, pull | 35.21 ± 0.23 | 33.14 ± 0.10 | 32.41 ± 0.27 | 37.65 ± 0.13 |
| `hub-65536` | one-thread | pagerank, push | 96.40 ± 0.39 | 58.94 ± 0.16 | 57.39 ± 1.06 | 37.65 ± 0.13 |
| `hub-65536` | one-thread | wcc, concurrency 1 | 6.99 ± 0.07 | 5.03 ± 0.04 | 4.64 ± 0.03 | 3.82 ± 0.01 |
| `hub-65536` | one-thread | wcc, concurrency unset | 17.00 ± 0.00 | 7.96 ± 0.07 | 6.83 ± 0.09 | 3.82 ± 0.01 |
| `hub-65536` | one-thread | triangles, concurrency 1 | 78.08 ± 2.25 | 78.75 ± 2.61 | 78.22 ± 1.21 | 38.74 ± 1.00 |
| `hub-65536` | one-thread | triangles, concurrency unset | 78.80 ± 1.26 | 77.60 ± 0.17 | 78.14 ± 0.86 | 38.74 ± 1.00 |
| `uniform-65536` | one-thread | pagerank, pull | 32.86 ± 0.37 | 31.06 ± 0.43 | 30.12 ± 0.22 | 45.66 ± 0.31 |
| `uniform-65536` | one-thread | pagerank, push | 89.76 ± 0.35 | 55.68 ± 1.20 | 54.70 ± 0.52 | 45.66 ± 0.31 |
| `uniform-65536` | one-thread | wcc, concurrency 1 | 10.39 ± 0.02 | 9.10 ± 0.06 | 8.53 ± 0.04 | 3.81 ± 0.01 |
| `uniform-65536` | one-thread | wcc, concurrency unset | 17.39 ± 0.02 | 8.81 ± 0.14 | 7.59 ± 0.19 | 3.81 ± 0.01 |
| `uniform-65536` | one-thread | triangles, concurrency 1 | 87.90 ± 0.24 | 84.51 ± 0.39 | 81.81 ± 2.10 | 43.22 ± 0.85 |
| `uniform-65536` | one-thread | triangles, concurrency unset | 84.66 ± 0.68 | 85.12 ± 0.84 | 82.98 ± 1.28 | 43.22 ± 0.85 |
| `hub-65536` | full-width | pagerank, pull | 7.27 ± 0.14 | 5.02 ± 0.11 | 4.87 ± 0.10 | 15.18 ± 0.90 |
| `hub-65536` | full-width | wcc, concurrency as the run | 1.62 ± 0.05 | 1.33 ± 0.02 | 1.31 ± 0.15 | 3.12 ± 0.04 |
| `hub-65536` | full-width | triangles, concurrency as the run | 29.38 ± 0.17 | 28.21 ± 0.22 | 28.03 ± 0.20 | 3.65 ± 0.03 |
| `uniform-65536` | full-width | pagerank, pull | 7.02 ± 0.09 | 4.58 ± 0.02 | 4.52 ± 0.10 | 16.42 ± 0.12 |
| `uniform-65536` | full-width | wcc, concurrency as the run | 1.91 ± 0.11 | 1.54 ± 0.11 | 1.72 ± 0.05 | 3.61 ± 0.17 |
| `uniform-65536` | full-width | triangles, concurrency as the run | 28.92 ± 0.12 | 28.13 ± 0.24 | 28.28 ± 0.06 | 4.06 ± 0.12 |

Over those 18 cells `counted` takes -0.2% to +148.8% against `unchecked`, the largest on wcc, concurrency unset, `hub-65536` at one-thread. Counting also costs in the build: `grust-next`'s `build_ms` for PageRank on `hub-65536` at one thread is 51.66 ms counted, 44.95 work-uncounted and 45.35 unchecked, because building the projection and its transpose charges work too. The push kernel's block charging is part of the kernel change above; the table says how much of the distance to `unchecked` remains in each mode.

## The results, with the ones against this side first

**Every cell that got worse.** Counted `grust-next` against v0.22.0, same fixture, kernel, concurrency and call, over every run: 68 of the 216 counted cells with a v0.22.0 counterpart are slower on `87fc462`, by +0.3% to +52.7%, and 50 of those are slower by more than the dispersion of the two cells, where the margin is the two cells' relative MADs added together. The largest: `path-65536` triangles full-width concurrency as the run second +52.7%; `path-16384` triangles full-width concurrency as the run second +42.5%; `path-65536` triangles one-thread concurrency 1 second +39.2%; `path-16384` triangles one-thread concurrency 1 second +30.3%; `layered-16384` triangles full-width concurrency as the run second +27.4%.

**B5's slower cells, on the padded commit.** B5 found 70 of its 216 counted cells slower than v0.22.0 on `ca68900`. On `87fc462` the same cells stand, by that one rule for every cell: 5 faster than v0.22.0, 18 within dispersion of it, 47 still slower. Of the still-slower cells, by shape: the triangles second call 20; the BFS first call 5; the BFS second call 5; the WCC first call at concurrency 1 5; the PageRank second call 3; the triangles first call 3; the PageRank first call 2; PageRank on `path` 2; the WCC second call 2. Three shapes account for most of that list, and only one of them has a cause.

- **The triangles second call.** 21 of this campaign's slower cells, +0.7% to +52.7%, and every one of them takes more minor page faults than v0.22.0 did: a median of 32 on v0.22.0 against 543 on `87fc462`. v0.22.0's second triangle call allocates almost nothing and the later commit's allocates again. That is a change in what the second call does rather than in how fast it does it, the same shape B5 found, and it is the one shape with a cause. The padding commit does not touch it and was not expected to.
- **WCC's first call at concurrency 1.** Slower on 6 of 8 fixtures at one thread, -3.7% to +13.7%, 5 of them beyond the dispersion margin, with the page-fault counts equal on 8 of 8. Where the faults are equal it is not the allocator; the padding commit's own measurement found this residue responds to the chunk size class of the balance and not to its cache line, and did not find why. The same cells at concurrency unset are not slower, and at full width the same kernel is far faster than v0.22.0. **Unexplained.**
- **Counted BFS on the first call.** At one thread, 6 of 8 `hub` and `uniform` first-call cells are slower than v0.22.0, -3.8% to +10.8%, 4 of them beyond dispersion, where B5's same cells ran +0.9% to +6.7%; at full width, 2 of 4, -22.9% to +9.8%, 1 beyond, where B5 ran -22.2% to +9.4%. The page-fault counts beside each row are within a few of each other, so what is left is not the allocator, and it is not the transpose, which this run does not build for BFS. **Unexplained.**

**Triangle counting at width.** On `uniform-65536` at one thread, `neo4j-graph` counts triangles in 43.22 ± 0.85 ms and Grust's counted kernel at concurrency 1 in 87.90 ± 0.24; at 16 workers, 4.06 ± 0.12 against 28.92 ± 0.12. The gap widens with width, and the accounting rows show it is not the guarantee: `unchecked` at full width is 28.28 ± 0.06. Where it lives is not established here.

**PageRank on `layered-16384` at sixteen threads.** First call -5.8%, faster than v0.22.0, where B5 said -2.7%; second call +4.3%, still slower, where B5 said +5.8%. **Unexplained.**

**The lineage, at equal width.** PageRank at 65,536 nodes, one thread, first call, per iteration in milliseconds, because the participants stop on different rules and only per-iteration compares kernels. This is the one configuration in which the comparison is valid:

| participant | precision | `hub` / iter | iters | `uniform` / iter | iters | boundary |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `neo4j-graph` | f32 | 1.345 | 28 | 1.343 | 34 | no accounting; its own stopping rule |
| `icebug` | f64 | 6.138 | 12 | 5.762 | 11 | NetworKit, `DISTRIBUTE_SINKS` set |
| `icecat` | f64 | 2.060 | 17 | 2.096 | 16 | sequential by construction |
| `grustcat` | f64 | 1.917 | 17 | 1.930 | 16 | sequential by construction; tolerance fixed in the crate |
| `grust#1` | f64 | 4.007 | 17 | 3.801 | 16 | v0.22.0, pull: the transpose is built inside this call |
| `grust-next@counted#1` | f64 | 2.071 | 17 | 2.054 | 16 | counted, pull: the transpose is in `build_ms` |

The general kernel over the backend-neutral projection, with the transpose on the same side as everyone else's and the work meter charging, runs at +6.4% per iteration against the specialised Arrow kernel that descends from it on `uniform`, where the first run, with the transpose inside Grust's timer alone, had reported a wider gap. That sentence is about a boundary correction and a kernel change together; the tables above separate them.

**Drift between campaigns on unchanged code, and a host that was slower above L3.** At the protocol size, the participants that did not change between B5 and B6, on the same fixtures and the same host, move -5.2% to +102.6% between the two campaigns, a median of +4.0%, and the largest of those is `icebug`, a participant containing no Grust at all. Above L3 the drift is not a participant's: every participant's PageRank at 2,097,152 and 4,194,304 nodes is slower in B6 than in B5, by +1.3% to +123.1% (large-one-thread +20.4% to +123.1% over 24 cells; large-full-width +1.3% to +83.6% over 16 cells; xlarge-one-thread +16.7% to +69.6% over 24 cells; xlarge-full-width +7.3% to +27.3% over 16 cells), and the four participants that contain no Grust move with the ones that do, +6.6% to +83.6%. The page-fault counts are the same to within a few, steal over those four runs is at most 21 ticks in 5132 seconds, and the watcher saw nothing, so it is not the code under test and not a second workload. A control after the campaign repeated the shortest large run, `large-full-width`, under the same driver with its own tag. Its first attempt was discarded by the rule: a `du -sh /home/admin/src` not started by the driver used 10 to 25% of a CPU during the run, 8 sightings, and the attempt is kept in the bundle, renamed, entering no table. The second attempt was clean, 4 steal ticks over 812.6 seconds, and stands -2.5% to +16.2% from the campaign's own cells, a median of -0.2%, and +4.2% to +80.9% from B5's, a median of +19.6%: the slower state outlived the campaign and is not a transient of one run. The cheapest candidate, transparent hugepage starvation, was checked beside the control, and the kernel's `thp_fault_fallback` counter did not move across it. **The cause is not established.** It is why the large and extra-large kernel-change rows are read within B6 only, and why a cell is only ever compared with other cells of its own run.

## The host, and the record

One host, quegee, 16 vCPU on 8 physical cores, 24.8 MB L3, not burstable. The timed campaign ran from 2026-09-22T15:10:29Z to 2026-09-22T18:07:22Z: 8 timed runs, all clean, none discarded, none rerun; 1,840 cells, none of which reached the dispersion rule of 0.25 MAD/median; the largest dispersion was 0.137, `grust-next@unchecked` wcc `hub-16384` second in full-width. Steal is recorded per cell; the largest over a run was 21 ticks across `xlarge-one-thread`'s 5132 seconds. 1 resident agent session was seen by name across the campaign, asleep, and it is in every snapshot of the record rather than reconstructed afterwards. Unlike B5, no parity invocation was marked shared and none was refused a start; the page cache was dropped after parity and before the first timed run, as in B5, so the reclaim that the idle rule had refused to distinguish from a second workload did not recur.

## What is not here

**Not a ranking.** The accounting table puts `neo4j-graph` beside Grust's modes so a reader can compare like for like, and the pinned probe puts every participant beside itself; nothing reduces them to an order, and `neo4j-graph` computes in `f32` to its own stopping rule.

**Not portable.** Every timing is a fact about one host on one day as much as about the code, and this campaign's own record shows the host in a slower state above L3 than the campaign before it. Numbers produced on burstable hosts during this work were for shape only and none is quoted.

**No cause** for what is left of the WCC and BFS first-call slowdown, for the `layered-16384` second call, or for the drift between campaigns on unchanged code and the slower host state above L3. Only their shapes; for the first, the knowledge that it is not the allocator, and for the one-worker WCC residue the padding commit's own finding that it follows the balance's chunk size class rather than its cache line. For the `path` family at full width the cause was found outside the harness and is stated by the commit; this campaign holds the before and the after.

**A dated result.** v0.22.0 and `87fc462` are what was timed. A column measured later describes that code, and the related-work note's remark about a moving target still applies to it.

The harness is `docker/simple-rust-algo-bench/` in the repository, a separate image from the full-path harness. `b6_report.py` regenerates the results document's B6 section from the bundle byte for byte, `b6_post.py` generates this post from the same files, and the site's renderer fails its build on an unlisted evidence file, an unrendered placeholder, or a value no placeholder uses.
