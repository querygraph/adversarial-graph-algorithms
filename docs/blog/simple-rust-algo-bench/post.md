# What one PageRank sweep costs: five implementations on one host

![A water strider standing on the surface of a pond, its feet dimpling the water into a lattice of linked nodes, while a turtle crosses a chain of lily pads beside it.](assets/water-strider-turtle.png)

## What this measures

One function, timed the same way four times. Five participants build in one image as five distinct binaries — the last campaign's audit found 6 of them, each with its own receipt and SHA-256 — and each runs the same kernel over the same fixtures on one dedicated host: PageRank in every campaign, and WCC, BFS and triangle counting in the wider ones. `neo4j-graph` is the [`neo4j-labs/graph`](https://github.com/neo4j-labs/graph) Rust library, graph 0.3.2 / graph_builder 0.4.2, through its builder and `graph::prelude`; it accumulates and returns `f32`, stops by its own rule, and performs no work accounting. `icebug` is the Arrow update of NetworKit, in C++. `icecat` is the Rust rewrite of those kernels. `grustcat` is those kernels over Grust's model, projected to packed Arrow adjacency. `grust` is Grust's own kernels over a `GraphProjection`, the general kernel over a backend-neutral graph.

Every cell is checked against a reference written independently in Python — PageRank iterated to the stated tolerance, components by union-find, BFS by queue, triangles by ordered enumeration — before it is timed, and **a cell that did not agree is never timed.** Over the four campaigns Grust's PageRank kernel was changed seven times and timed again after every change: against that reference, against the release Grust shipped before this work, and beside the library in the same image. Each of those commits asserted the same thing about itself — that the scores it returned were bit for bit what they had been, at both precisions and at every worker count — and each campaign checked that assertion on the measuring host before it timed anything.

The benchmark is `simple-rust-algo-bench`; the results document is [`simple-rust-algo-bench-results.md`](https://github.com/querygraph/adversarial-graph-algorithms/blob/a62e68c1977afe4a6a1eb52af6ed75208ad075c8/docs/simple-rust-algo-bench-results.md), the evidence bundles are [`b5-quegee`](https://github.com/querygraph/adversarial-graph-algorithms/tree/a62e68c1977afe4a6a1eb52af6ed75208ad075c8/docs/simple-rust-algo-bench-evidence/b5-quegee), [`b6-quegee`](https://github.com/querygraph/adversarial-graph-algorithms/tree/a62e68c1977afe4a6a1eb52af6ed75208ad075c8/docs/simple-rust-algo-bench-evidence/b6-quegee), [`b7-quegee`](https://github.com/querygraph/adversarial-graph-algorithms/tree/a62e68c1977afe4a6a1eb52af6ed75208ad075c8/docs/simple-rust-algo-bench-evidence/b7-quegee) and [`b9-quegee`](https://github.com/querygraph/adversarial-graph-algorithms/tree/a62e68c1977afe4a6a1eb52af6ed75208ad075c8/docs/simple-rust-algo-bench-evidence/b9-quegee), and every number in this post is computed from those bundles by a script rather than copied from a table. The same files render the [kernels page on adversari.al](https://adversari.al/graph/kernels).

## How it came out

**Per sweep, on the one pair of rows that carries the same precision under the same stopping rule with neither charging work to a meter** — `grust-next@unchecked+f32` beside `neo4j-graph`, both formed inside the last campaign's own bundle — of the 16 cells, 12 put Grust's sweep at or below the reference participant's. Inside dispersion, above by less than the margin on the cell, 1 of the 16: `hub-16384` one-thread (1.000 ± 0.003). **The remaining 3 are above by more than the margin on that cell, and all of them are at one thread on the protocol-size fixtures: `uniform-65536` by 14.7% ± 0.5, `hub-65536` by 10.8% ± 0.2, `uniform-16384` by 0.4% ± 0.2.** Nothing in this campaign explains those three, and none of the commits in the stack was aimed at them.

**Against the release Grust shipped before this work**, on the counted default rather than the unchecked row and read inside the last campaign, the same kernel's sweep is 0.296 to 0.813 of v0.22.0's over 16 cells, with both sides returning the same bits. That is the reading that spans the whole stack, because it is Grust against Grust inside one campaign.

**Work accounting used to cost and now mostly does not.** Over the 32 pull-kernel cells the meter's cost per sweep runs 0.952 to 1.075 in B9 where the campaign before it read 1.023 to 1.557. Above L3 it is within noise of no meter at all: 0.952 to 1.031 at 2,097,152 nodes and 0.955 to 1.026 at 4,194,304, against B7's 1.038 to 1.190 and 1.027 to 1.102. At the protocol size and full width it is reduced and not gone: 1.056 to 1.075 where B7 read 1.537 to 1.557.

**One result moved the wrong way.** On the push kernel the meter costs 1.285 to 1.846 in B9 against 1.185 to 1.727 in B7 over its 16 cells, and on 14 of them the B9 figure exceeds the B7 figure by more than both margins together. **Why it moved is not established here, and this post does not attribute it.**

Every figure above is a distance with its margin rather than a verdict, and every one of them is formed inside a single campaign. The next section says why a figure here can take no other form; the tables come after it.

## How to read a number

**Per sweep, because the rows stop at different counts.** The three PageRank rows that appear side by side stop at three different iteration counts under the same tolerance: `neo4j-graph` between 14 and 36 sweeps, Grust at `f32` at 19 to 21, Grust at `f64` at 16 to 17. Two rows that did not take the same number of sweeps over the arcs did not do the same work, so **their totals are not comparable and their per-sweep times are.** A total is the time to reach the tolerance under that participant's own stopping rule, which is the number a reader who wants an answer should take; a per-iteration figure is the cost of one sweep and nothing else. Every distance drawn below is drawn on the per-sweep column, with the sum of the two cells' MAD over median as its margin, and a distance smaller than its margin is inside dispersion and is not a difference.

**No absolute crosses a campaign.** The host was restarted between the last two campaigns, and the participants whose code did not change moved anyway: over 48 cells of unchanged code the median B9-over-B7 per-sweep ratio is 0.942. A millisecond in one campaign is not a millisecond in the next, so every comparison here is either between two cells of one campaign, or between a ratio formed inside one campaign and a ratio formed inside another. The method section prints the size of that drift, and the one place where a cell of one campaign meets a cell of another.

## The details

### One sweep against one sweep

Both rows carry `f32` scores and neither charges work to a meter, which is why they are put together; they stop at different counts, so this is the cost of one sweep and not the time to an answer. The margin on each cell is the sum of the two cells' MAD over median, and every figure is formed inside B9 from two cells of the same run.

| fixture | run | `grust-next@unchecked+f32` per-iter / iters | `neo4j-graph` per-iter / iters | ratio ± | outside its margin |
| --- | --- | ---: | ---: | ---: | --- |
| `hub-16384` | one-thread | 0.363 / 20 | 0.363 / 36 | 1.000 ± 0.003 | no |
| `hub-65536` | one-thread | 1.427 / 20 | 1.288 / 28 | 1.108 ± 0.002 | yes |
| `uniform-16384` | one-thread | 0.372 / 19 | 0.370 / 28 | 1.004 ± 0.002 | yes |
| `uniform-65536` | one-thread | 1.493 / 19 | 1.301 / 34 | 1.147 ± 0.005 | yes |
| `hub-16384` | full-width | 0.161 / 20 | 0.366 / 36 | 0.438 ± 0.013 | yes |
| `hub-65536` | full-width | 0.159 / 20 | 0.555 / 26 | 0.287 ± 0.039 | yes |
| `uniform-16384` | full-width | 0.162 / 19 | 0.372 / 28 | 0.436 ± 0.013 | yes |
| `uniform-65536` | full-width | 0.161 / 19 | 0.479 / 34 | 0.336 ± 0.045 | yes |
| `hub-2097152` | large-one-thread | 68.511 / 20 | 80.063 / 26 | 0.856 ± 0.018 | yes |
| `uniform-2097152` | large-one-thread | 73.087 / 19 | 82.874 / 26 | 0.882 ± 0.010 | yes |
| `hub-2097152` | large-full-width | 7.796 / 20 | 9.270 / 28 | 0.841 ± 0.023 | yes |
| `uniform-2097152` | large-full-width | 8.026 / 19 | 9.575 / 28 | 0.838 ± 0.008 | yes |
| `hub-4194304` | xlarge-one-thread | 162.299 / 20 | 176.128 / 23 | 0.921 ± 0.041 | yes |
| `uniform-4194304` | xlarge-one-thread | 200.294 / 19 | 251.760 / 29 | 0.796 ± 0.007 | yes |
| `hub-4194304` | xlarge-full-width | 16.919 / 20 | 24.505 / 14 | 0.690 ± 0.158 | yes |
| `uniform-4194304` | xlarge-full-width | 18.365 / 19 | 20.130 / 29 | 0.912 ± 0.076 | yes |

The two cells at 65,536 nodes are the largest distances in the table and they are not small: a sequential sweep of a graph that fits in this host's L3 costs Grust about an eighth more there than it costs the reference participant. At full width the same column runs 0.287 to 0.912, and those are different cells, not the same cells read differently.

### Against the release before it

Inside B9, on the counted default, second call against second call so the transpose is cached on both sides:

| fixture | run | `grust` v0.22.0 per-iter / iters | `grust-next@counted` per-iter / iters | ratio ± |
| --- | --- | ---: | ---: | ---: |
| `hub-16384` | one-thread | 0.567 / 17 | 0.349 / 17 | 0.615 ± 0.003 |
| `hub-65536` | one-thread | 2.595 / 17 | 1.412 / 17 | 0.544 ± 0.012 |
| `uniform-16384` | one-thread | 0.578 / 16 | 0.351 / 16 | 0.608 ± 0.003 |
| `uniform-65536` | one-thread | 2.708 / 16 | 1.421 / 16 | 0.525 ± 0.015 |
| `hub-16384` | full-width | 0.202 / 17 | 0.164 / 17 | 0.813 ± 0.029 |
| `hub-65536` | full-width | 0.502 / 17 | 0.183 / 17 | 0.365 ± 0.008 |
| `uniform-16384` | full-width | 0.208 / 16 | 0.163 / 16 | 0.783 ± 0.039 |
| `uniform-65536` | full-width | 0.511 / 16 | 0.184 / 16 | 0.361 ± 0.013 |
| `hub-2097152` | large-one-thread | 262.648 / 16 | 77.638 / 16 | 0.296 ± 0.020 |
| `uniform-2097152` | large-one-thread | 273.899 / 16 | 91.337 / 16 | 0.333 ± 0.128 |
| `hub-2097152` | large-full-width | 31.719 / 16 | 10.216 / 16 | 0.322 ± 0.051 |
| `uniform-2097152` | large-full-width | 33.790 / 16 | 10.194 / 16 | 0.302 ± 0.023 |
| `hub-4194304` | xlarge-one-thread | 654.481 / 16 | 273.106 / 16 | 0.417 ± 0.004 |
| `uniform-4194304` | xlarge-one-thread | 698.234 / 16 | 286.087 / 16 | 0.410 ± 0.017 |
| `hub-4194304` | xlarge-full-width | 82.646 / 16 | 31.984 / 16 | 0.387 ± 0.011 |
| `uniform-4194304` | xlarge-full-width | 89.167 / 16 | 33.720 / 16 | 0.378 ± 0.027 |

Both sides of that table return the same bits. That is the result this work was for.

### What work accounting costs, and what it buys

`counted` is Grust's default and what v0.22.0 always does: work is charged to a shared meter and cancellation is observed, so an untrusted or shared caller can be given an algorithm without being given the machine, and an exhausted budget stops a kernel where it stands. `unchecked` does neither and cannot be stopped once started; it is the like-for-like row against a library that performs no accounting, and the distance to `counted` is what the guarantee costs. Memory admission is performed in every mode.

Per sweep, on the same cell of the same run, with each campaign's column formed inside its own bundle:

| fixture | run | kernel | precision | B7 counted/unchecked ± | B9 counted/unchecked ± |
| --- | --- | --- | --- | ---: | ---: |
| `hub-16384` | one-thread | pull | f32 | 1.023 ± 0.002 | 0.998 ± 0.002 |
| `hub-16384` | one-thread | pull | f64 | 1.045 ± 0.002 | 1.002 ± 0.003 |
| `hub-16384` | one-thread | push | f32 | 1.710 ± 0.002 | 1.785 ± 0.003 |
| `hub-16384` | one-thread | push | f64 | 1.727 ± 0.005 | 1.787 ± 0.004 |
| `hub-65536` | one-thread | pull | f32 | 1.034 ± 0.002 | 1.000 ± 0.004 |
| `hub-65536` | one-thread | pull | f64 | 1.058 ± 0.018 | 1.003 ± 0.005 |
| `hub-65536` | one-thread | push | f32 | 1.713 ± 0.005 | 1.792 ± 0.002 |
| `hub-65536` | one-thread | push | f64 | 1.641 ± 0.016 | 1.771 ± 0.018 |
| `uniform-16384` | one-thread | pull | f32 | 1.027 ± 0.001 | 0.999 ± 0.003 |
| `uniform-16384` | one-thread | pull | f64 | 1.051 ± 0.003 | 1.001 ± 0.003 |
| `uniform-16384` | one-thread | push | f32 | 1.707 ± 0.002 | 1.837 ± 0.002 |
| `uniform-16384` | one-thread | push | f64 | 1.699 ± 0.002 | 1.836 ± 0.009 |
| `uniform-65536` | one-thread | pull | f32 | 1.036 ± 0.005 | 1.000 ± 0.005 |
| `uniform-65536` | one-thread | pull | f64 | 1.079 ± 0.016 | 1.002 ± 0.004 |
| `uniform-65536` | one-thread | push | f32 | 1.710 ± 0.006 | 1.846 ± 0.002 |
| `uniform-65536` | one-thread | push | f64 | 1.618 ± 0.044 | 1.796 ± 0.005 |
| `hub-16384` | full-width | pull | f32 | 1.189 ± 0.030 | 1.019 ± 0.014 |
| `hub-16384` | full-width | pull | f64 | 1.210 ± 0.054 | 1.025 ± 0.020 |
| `hub-65536` | full-width | pull | f32 | 1.537 ± 0.024 | 1.069 ± 0.009 |
| `hub-65536` | full-width | pull | f64 | 1.557 ± 0.056 | 1.056 ± 0.032 |
| `uniform-16384` | full-width | pull | f32 | 1.238 ± 0.038 | 1.033 ± 0.014 |
| `uniform-16384` | full-width | pull | f64 | 1.229 ± 0.076 | 1.007 ± 0.027 |
| `uniform-65536` | full-width | pull | f32 | 1.552 ± 0.004 | 1.073 ± 0.036 |
| `uniform-65536` | full-width | pull | f64 | 1.537 ± 0.042 | 1.075 ± 0.020 |
| `hub-2097152` | large-one-thread | pull | f32 | 1.190 ± 0.099 | 1.023 ± 0.025 |
| `hub-2097152` | large-one-thread | pull | f64 | 1.134 ± 0.068 | 0.952 ± 0.072 |
| `hub-2097152` | large-one-thread | push | f32 | 1.416 ± 0.025 | 1.536 ± 0.018 |
| `hub-2097152` | large-one-thread | push | f64 | 1.213 ± 0.017 | 1.422 ± 0.100 |
| `uniform-2097152` | large-one-thread | pull | f32 | 1.110 ± 0.027 | 0.969 ± 0.007 |
| `uniform-2097152` | large-one-thread | pull | f64 | 1.074 ± 0.076 | 0.972 ± 0.162 |
| `uniform-2097152` | large-one-thread | push | f32 | 1.476 ± 0.056 | 1.537 ± 0.020 |
| `uniform-2097152` | large-one-thread | push | f64 | 1.188 ± 0.025 | 1.479 ± 0.183 |
| `hub-2097152` | large-full-width | pull | f32 | 1.084 ± 0.015 | 0.978 ± 0.023 |
| `hub-2097152` | large-full-width | pull | f64 | 1.163 ± 0.022 | 0.971 ± 0.051 |
| `uniform-2097152` | large-full-width | pull | f32 | 1.066 ± 0.012 | 1.031 ± 0.037 |
| `uniform-2097152` | large-full-width | pull | f64 | 1.038 ± 0.124 | 1.000 ± 0.022 |
| `hub-4194304` | xlarge-one-thread | pull | f32 | 1.089 ± 0.043 | 1.026 ± 0.053 |
| `hub-4194304` | xlarge-one-thread | pull | f64 | 1.058 ± 0.028 | 1.002 ± 0.009 |
| `hub-4194304` | xlarge-one-thread | push | f32 | 1.199 ± 0.060 | 1.460 ± 0.045 |
| `hub-4194304` | xlarge-one-thread | push | f64 | 1.185 ± 0.009 | 1.287 ± 0.025 |
| `uniform-4194304` | xlarge-one-thread | pull | f32 | 1.027 ± 0.035 | 0.955 ± 0.084 |
| `uniform-4194304` | xlarge-one-thread | pull | f64 | 1.065 ± 0.011 | 1.006 ± 0.019 |
| `uniform-4194304` | xlarge-one-thread | push | f32 | 1.263 ± 0.059 | 1.296 ± 0.084 |
| `uniform-4194304` | xlarge-one-thread | push | f64 | 1.210 ± 0.021 | 1.285 ± 0.007 |
| `hub-4194304` | xlarge-full-width | pull | f32 | 1.102 ± 0.083 | 1.025 ± 0.021 |
| `hub-4194304` | xlarge-full-width | pull | f64 | 1.042 ± 0.017 | 0.956 ± 0.058 |
| `uniform-4194304` | xlarge-full-width | pull | f32 | 1.064 ± 0.108 | 1.021 ± 0.071 |
| `uniform-4194304` | xlarge-full-width | pull | f64 | 1.090 ± 0.031 | 0.985 ± 0.029 |

Of the 32 pull-kernel cells, 10 are outside their own margins in B9 where 28 were in B7; the 8 cells at 2,097,152 nodes and the 8 at 4,194,304 have one cell each outside its own margin, and in opposite directions. That is what charging a reduction block rather than a node was for. The push kernel is the exception summarised above: the block change is in the pull kernel's reduction and the push loop still charges per node, which is a candidate and not an attribution. A failure that fits a plausible story is the most dangerous kind, because the story ends the search; the control that would separate the candidates has not been run.

B6 is where the cost of the guarantee was largest. Over 18 first-call cells at the protocol size `counted` took -0.2% to +148.8% against `unchecked`, the largest on wcc, concurrency unset, `hub-65536` at one-thread.

### What changed in the kernel, campaign by campaign

**B5** timed Grust `ca68900`, which put `WorkMeter::charge` back in line in sixteen kernels after it had been pushed out of line; the history section below is what that campaign found and did not explain.

**B6** timed `87fc462`, which pads the work meter's shared balance to a whole cache line, under B5's protocol with nothing else changed. On the PageRank kernel itself, second call against second call so the transpose is cached on both sides and both builds returning the same bits, the ratio to v0.22.0 is below 1 in 22 of 24 cells, between 0.411 and 1.009. What is counted, when a budget refuses, and every accounting mode are unchanged, and B6's parity gate checked that rather than taking the commit's word.

**B7** added the row that made a per-sweep comparison legitimate. Every PageRank table since the first campaign carried one sentence under it: `neo4j-graph` accumulates and returns `f32`, every other participant `f64`. Under the same tolerance Grust's `f64` kernel stopped at 16 or 17 iterations on every hub and uniform fixture at every size, and `neo4j-graph` stopped between 19 and 36; a total of one against a total of the other was a ratio of two stopping rules as much as of two kernels, and a per-sweep figure across two precisions was a comparison of two arithmetics. Grust `ead3568` makes the kernel generic over a sealed `Score` trait that `f64` and `f32` implement: `pagerank` keeps its signature and its `f64` results, `pagerank_f32` returns `PageRank<f32>`, and the procedure layer takes a precision. Every score, per-arc share, dangling mass and teleport share is formed and accumulated in the score type; the L1 residual is summed in `f64` from the score differences at either precision, which is what `neo4j-graph` does for its own `f32` kernel, and the stop stays residual at or below tolerance. The participant gains `--precision {f64,f32}` behind a cargo feature that is off for the v0.22.0 build, which refuses the flag rather than running `f64` under an `f32` label, and a row that reports `converged: false` gets its own verdict and is never timed — the tolerance is never loosened to make a row converge.

What that bought is a pair of rows that carry the same precision under the same stopping rule with neither charging work to a meter. What it did not buy is a shared iteration count. In B7 the `f32` rows stopped at 19 to 21 sweeps, after the `f64` rows and well before `neo4j-graph`, and the same three-way split holds in B9: of 48 `+f32` cells, 0 stopped where `neo4j-graph` stopped. So the per-sweep column is the comparison and the totals are not, and both are printed.

**B9** runs B7's plan, unchanged in every part, at Grust `4a9e7f5`, the head of the kernel branch stack. Over the commit B7 timed the stack adds four-byte CSR targets, work charged one reduction block at a time rather than one node, PageRank's inner loop written without the ArticleRank term, four-byte CSR row offsets, and the non-finite test moved from the node to the block. Every one of those commits asserts bit-identical scores at both precisions and at every width, and the parity below is that claim checked on this host before anything was timed. The harness is at `cea69ee`, the image is `simple-rust-algo-bench:b9-4a9e7f5`, built on the host from commits staged by `git archive`, and the 8 fixtures are SHA-256-identical to B6's.

## Method and equivalence

### One execution class, and nothing smuggled into a number

The benchmark measures one thing: an in-memory graph built once from the same input, with kernels called directly through each project's own Rust API. No Cypher in any row, because a query layer parses, plans, admits and converts, and timing it against a library call measures the layer rather than the kernel. No database, no snapshot. And no feature difference absorbed into a shared cell: where Grust runs a kernel under a cooperative budget and the library runs it without one, that difference is a separate, labelled measurement, not an unexplained slowdown.

The lineage is NetworKit → Icebug → Icecat → Grustcat, and a column that skipped the middle could not tell a rewrite's cost from a design's. Two of the five participants, `icecat` and `grustcat`, cannot use a second thread at all, so the 16-worker runs are not a five-column parallel table and no width ratio is drawn against them. **`neo4j-graph` accumulates and returns `f32`, to its own stopping rule, and performs no work accounting.** That sentence belongs under every table its column appears in, and it is why the campaigns built the rows that make a comparison legitimate rather than drawing one across the difference.

### Parity, and what it did and did not establish

At B6's commit the protocol fixture set at each of three concurrencies shows 252 agreements, 32 absences and 4 mismatches, and the mismatches are all one difference: `neo4j-graph`'s PageRank does not redistribute dangling mass, so on a graph with a node that has no outgoing edge it computes a different function. NetworKit defaults to the same and offers an option this harness sets; Grust's kernels always redistribute. That is a choice, not a defect, and the consequence is that PageRank is compared only on the two dangling-free families, `hub` and `uniform`. All 9 parity invocations ran once, in order, on an idle host; 3 of them exited 1, the parity script's exit on any mismatching row, and the driver takes its verdict from the file rather than the exit code.

**What parity did not establish is bit identity across implementations.** The first run of this benchmark said the reference, `grust`, `icecat` and `grustcat` return the same `f64` bit pattern for PageRank. It had never compared bits: it held the maximum and the sum to the stopping tolerance and stored no scores. When the rerun compared whole vectors, Grust's push kernel matched the reference on 65,467 of 65,536 scores of `uniform-65536` within 2 ulps and on 3,230 of `hub-65536` within 7; the pull kernel matched 29,430 of `uniform-65536` within 4. The sentence was withdrawn. What holds is weaker and sufficient: every `f64` participant agrees with the reference far inside the stopping tolerance with the same iteration count, so they compute the same function to the precision that tolerance defines, which is what licenses comparing their speeds.

Bit identity holds where it is now stated, between Grust builds, and it is gated rather than asserted. In B6 the commit under test returned v0.22.0's PageRank vector bit for bit on 108 of 108 rows across three accounting modes and every fixture at every concurrency. In B9, after five further commits to the kernel stack, 144 of 144 PageRank parity rows agree, 0 mismatch and 0 fail to converge; the `f64` rows are bit-identical to v0.22.0's vector on 48 of 48 rows and the `+f32` unchecked rows to their own counted rows on 24 of 24. A kernel that changed a score would compute a different function, and the gate is what stands between "faster" and "faster at something else".

The `f32` rows are also a different answer, not a different timing of one. Every `f32` vector agrees with the `f64` reference to between 2.6e-13 and 9.7e-11 absolute per score, and 0 scores are bit-identical to it. An `f32` kernel cannot meet a tolerance below one ulp of a moving score except at an exact fixed point; on these dangling-free families every `f32` cell converged under the cap, and on a dangling-heavy graph the same commit's own tests record `f32` needing about twice the iterations at tolerances of 1e-6 and below. That regime is not measured here and a campaign that enters it must restate this paragraph rather than inherit it.

### Dispersion, drift, and the one crossing

A cell's dispersion is its MAD over its median, and a cell at or above 0.25 is unusable and is not published. A distance between two cells carries the sum of their dispersions as its margin, and a distance smaller than its margin is not a difference.

Drift between campaigns is measured rather than assumed. Over 48 cells of unchanged code the median B9-over-B7 per-sweep ratio is 0.942, with individual cells from 0.644 (`neo4j-graph` hub-4194304 xlarge-one-thread) to 1.203 (`neo4j-graph` hub-65536 full-width); the reference participant's own one-thread sweep above L3 reads `hub-2097152` at B7's 98 ms against B9's 80 ms, `uniform-2097152` at B7's 91 ms against B9's 83 ms, on code that did not change. The one place a cell of one campaign meets a cell of another is the unchanged-code table, and nowhere else; that table exists to show the size of what the rule is avoiding.

### The host, and the record

B9's timed campaign ran from 2026-09-23T15:31:00+0000 to 2026-09-23T16:49:49+0000: 6 runs, all clean, none discarded, none rerun, 9 parity invocations before any of them, and the page cache dropped after parity and before the first timed run. 240 cells, 0 of them at or above the threshold that makes a cell unusable; the largest dispersion was 0.144, `neo4j-graph` hub-4194304 in xlarge-full-width. Steal was at most 10 ticks over a run, a run with a sighting is discarded rather than published, and 0 resident agent sessions were seen by name across the campaign. The record also says what it lost: the host script that writes the image receipt and the fixture manifest has a previous campaign's prefix hard-coded, so running it for B9 overwrote the previous campaign's receipt, which was read back from the image still on the host. That is in the bundle's own README rather than repaired quietly.

The harness is `docker/simple-rust-algo-bench/` in the repository. `b7_report.py --campaign b9` regenerates the results document's B9 section and the bundle's `tables.md` byte for byte from the bundle, `regenerate-check.sh` is the gate that every commit runs, `b9_post.py` generates this post from the same files, and the site's renderer fails its build on an unlisted evidence file, an unrendered placeholder, or a value no placeholder uses.

## History, and what went wrong

*Optional reading. The results above do not depend on this section; it is the record of how the apparatus was wrong and how it was found out, kept because a benchmark whose mistakes are not on the page is asking to be taken on trust.*

### The first artifact: the transpose was on the wrong side of the timer

Grust's pull PageRank kernel needs the incoming adjacency, and at v0.22.0 a projection builds it lazily inside the first kernel call that asks for it. The first timed run made exactly one call at a concurrency that selects the pull kernel, so every Grust PageRank time in it contained a one-off transpose. `grustcat`, `neo4j-graph` and NetworKit build their reverse adjacency in their constructors, inside the build timer, and `icecat` builds it between the two timers and reports it apart. The same work sat on opposite sides of the boundary, and the run's headline per-iteration figure divided that build across the iterations. It was found by profiling outside the harness and then measured inside it.

The later commit has `prepare_incoming()`; the `grust-next` participant calls it inside the build timer and reports its share as `incoming_ms`. v0.22.0 has no such method, so every Grust build runs the kernel twice on one projection and reports both calls. The second call runs on warm caches, which is not the condition of any other participant's timed call, so it is labelled rather than presented as the corrected number. One thread, pull kernel, milliseconds, median ± MAD, from B6's bundle:

| fixture | `grust` v0.22.0 first | v0.22.0 second | `grust-next` first | transpose, in `build_ms` | `grustcat` |
| --- | ---: | ---: | ---: | ---: | ---: |
| `hub-65536` | 68.11 ± 2.53 | 57.38 ± 1.85 | 35.21 ± 0.23 | 7.32 | 32.59 ± 0.38 |
| `uniform-65536` | 60.82 ± 3.60 | 48.70 ± 3.01 | 32.86 ± 0.37 | 7.13 | 30.88 ± 0.28 |
| `hub-2097152` | 6581.11 ± 71.46 | 5802.03 ± 38.39 | 3859.96 ± 2.75 | 686.14 | 3310.95 ± 24.32 |
| `uniform-2097152` | 6999.18 ± 112.79 | 6164.16 ± 55.86 | 3821.94 ± 99.41 | 636.85 | 3836.22 ± 12.17 |
| `hub-4194304` | 14778.23 ± 100.50 | 13074.01 ± 130.01 | 8695.93 ± 24.39 | 1482.25 | 7349.00 ± 45.76 |
| `uniform-4194304` | 15671.38 ± 112.88 | 14150.99 ± 74.58 | 9001.38 ± 40.23 | 1469.27 | 8617.93 ± 93.54 |

BFS, WCC and triangles read no incoming adjacency and were never affected.

### The second artifact: the allocator state, and it was ours too

The rerun that measured the transpose built it inside the build timer for every algorithm, to make Grust's build column the same work as `grustcat`'s constructor. WCC and BFS never read the incoming adjacency, so for those two the harness built and freed a transpose nothing would read, immediately before the call it was timing. Freeing a large mapped chunk raises glibc's own mmap threshold, so the next call's large allocations came from a different place than the v0.22.0 column's. That rerun's `grust-next` first calls were slower, and its second calls faster, than the code alone accounts for.

The correction has three parts, each with the reason it is not the other choice. The transpose is now built in the build timer only for the kernel that reads it; the previous behaviour is kept as a `+eager` variant and timed as its own labelled row, so the correction is shown rather than asserted. Matching a constructor was the wrong thing to match: a build column that does work no kernel will read is not the same measurement as one that does work the kernel needs. Every participant now reads its minor page faults on both sides of the call it times, outside the timer, so a time that moved while the counter did not is not this effect. And whether to pin the allocator at all was decided by measurement: pinning `GLIBC_TUNABLES` for the Grust participants alone would compare two allocators, the same kind of error again, so two runs repeat the protocol sizes with the threshold pinned for the whole container, every participant included.

Over the 48 WCC and BFS first-call cells at the protocol sizes, the corrected `grust-next` takes a median of -2 minor page faults against v0.22.0, and the `+eager` row a median of +0 against the corrected one; where `+eager` moves the counter at all, 14 cells, it takes 1 to 112 more faults, which is the artifact measured inside the harness. The rule for the pinning decision was fixed before the runs: the published tables stay on the default allocator unless the median difference in first-call faults between the two Grust builds exceeded 25. Re-decided on the campaign's own counter, it is 2. The pinned runs stay as a labelled probe, and the probe shows the threshold is not a Grust-specific effect: median change under pinning, per participant, `grust` +0.5% over 24 cells; `grust-next` +2.3% over 24 cells; `grustcat` +0.5% over 12 cells; `icebug` -1.5% over 12 cells; `icecat` +0.6% over 12 cells; `neo4j-graph` +0.6% over 12 cells.

### The regression, its cause, and what one commit was worth

Between v0.22.0 and the commit the rerun timed, `WorkMeter::charge` had been pushed out of line in sixteen kernels. That is the call every kernel makes once per unit of graph work, so every counted row of that rerun was measured with it out of line. It was inlined again at `ca68900`, the commit B5 timed under the corrected harness. B5's tables left two things unexplained after the allocator and the transpose were ruled out by the page-fault counter beside each row: PageRank on the `path` family at full width, where the `path-65536` full-width second call ran +117.4% over v0.22.0, and WCC's first call at one worker, slower on 6 of 8 fixtures by up to +13.6%.

An attribution on the measuring host, outside the harness, found the first was false sharing. Each work meter spends its admitted block from one shared `AtomicUsize`; as a bare `Arc<AtomicUsize>` that word was a 32-byte heap chunk, and glibc's tcache handed it out beside whatever the same size class had just freed, which since the projection build went parallel was the pool's own bookkeeping, written by other cores. Every such write took the cache line from the worker, and its next exchange had to fetch it back. Grust `87fc462` pads the balance to a whole cache line.

B6 times `87fc462` under B5's protocol with nothing else changed: the harness at `633ff36` differs from B5's `9ec8548` by the report script alone, the fixtures are SHA-256-identical, the runs ran in B5's order. On the cell the commit was written for, `path-65536` full-width second call — +117.4% in B5 — the figure is +0.4% on the padded commit, within dispersion. The four full-width `path` cells that B5 had at +47.9% to +117.4% are -23.9% to +9.3% here, with 1 of 4 still slower beyond the dispersion of the two cells; the one-thread cells are -4.8% to +1.8%. The regression is closed at the cell where it was largest.

### The campaign that died with its host

Between B5 and B6 the host itself moved. Every participant's PageRank above L3 was slower in B6 than in B5, including the four that contain no Grust at all, and a control run after B6 found the slower state had outlived the campaign rather than following any run in it; the cheapest candidate, transparent hugepage starvation, was checked on the kernel's own counter and ruled out. That is why B6 reads its large sizes within itself, why the host was restarted before the last two campaigns, and why no absolute in this post crosses a campaign. The figures are in the last item of the next section, which is where the unexplained results are kept.

## What is still slower, and what is unexplained

- **Like-for-like at one thread on the protocol sizes, 3 cells.** `uniform-65536` one-thread (1.147 ± 0.005), `hub-65536` one-thread (1.108 ± 0.002), `uniform-16384` one-thread (1.004 ± 0.002), each above its own margin. Unexplained, and stated as plainly as the cells that improved.
- **The push kernel's meter cost**, worse in B9 than in B7 on 14 of 16 cells. **Unexplained.**
- **WCC's first call at one worker.** In B6, slower than v0.22.0 on 6 of 8 fixtures at one thread, -3.7% to +13.7%, 5 of them beyond the dispersion margin, with the page-fault counts equal on 8 of 8. Where the faults are equal it is not the allocator; the padding commit's own measurement found this residue responds to the chunk size class of the balance and not to its cache line, and did not find why. **Unexplained.** WCC is not in the last two campaigns' matrix, so B9 says nothing about it either way.
- **Counted BFS on the first call.** At one thread, 6 of 8 `hub` and `uniform` first-call cells slower than v0.22.0, -3.8% to +10.8%, 4 beyond dispersion; at full width, 2 of 4, -22.9% to +9.8%, 1 beyond. The page-fault counts beside each row are within a few of each other, so it is not the allocator, and it is not the transpose, which BFS does not build. **Unexplained.**
- **The triangles second call.** 21 of B6's slower cells, +0.7% to +52.7%, taking a median of 543 minor page faults against v0.22.0's 32. v0.22.0's second triangle call allocates almost nothing and the later commit's allocates again: a change in what the second call does rather than in how fast it does it. This is the one shape on the list with a cause.
- **The host above L3.** Between B5 and B6 every participant's PageRank at 2,097,152 and 4,194,304 nodes was slower, by +1.3% to +123.1%, and the four participants that contain no Grust moved with the ones that do, +6.6% to +83.6%. A control after B6 repeated the shortest large run and stood -0.2% from the campaign's own cells and +19.6% from B5's, so the slower state outlived the campaign; the cheapest candidate, transparent hugepage starvation, was checked and the kernel's `thp_fault_fallback` counter did not move. At the protocol size the unchanged participants moved -5.2% to +102.6% between those campaigns, a median of +4.0%, and the largest of those is `icebug`, a participant containing no Grust at all. Between B7 and B9 the same reading is the one in the method section above. **The cause is not established**, and it is why no absolute here crosses a campaign.

For completeness on B6's own side: 68 of its 216 counted cells with a v0.22.0 counterpart were slower on the padded commit, by +0.3% to +52.7%, 50 of them beyond the dispersion of the two cells; the largest were `path-65536` triangles full-width concurrency as the run second +52.7%; `path-16384` triangles full-width concurrency as the run second +42.5%; `path-65536` triangles one-thread concurrency 1 second +39.2%; `path-16384` triangles one-thread concurrency 1 second +30.3%; `layered-16384` triangles full-width concurrency as the run second +27.4%. Of the cells B5 had found slower, on the padded commit 5 are faster than v0.22.0, 18 are within dispersion of it and 47 are still slower, by shape: the triangles second call 20; the BFS first call 5; the BFS second call 5; the WCC first call at concurrency 1 5; the PageRank second call 3; the triangles first call 3; the PageRank first call 2; PageRank on `path` 2; the WCC second call 2.

## What a reader should take from this

The kernel got faster per sweep across the stack, and it did so without giving up anything the gates check. That is the claim worth making, and it is narrower and more useful than a ranking:

- **Determinism is a product property, not an overhead.** Seven changes to a hot kernel, each asserting bit-identical scores at both precisions and every worker count, and a parity gate that refuses to time a build whose vector moved. The value of that is not visible in a timing column; it is visible the first time an answer has to be reproduced. Every comparison in this post rests on it, because a kernel that changed a score would be a different function timed under the same name.
- **Admission control is a product property too, and now it is nearly free where it used to cost.** Charging a reduction block rather than a node took the meter's cost above L3 to within noise of no meter, on the kernel the change was in. On the push loop the same campaign records it getting worse, with no cause established — which is the honest shape of a result, and the reason the two kernels are reported separately rather than averaged into one number.
- **Exact answers first.** Parity comes before timing, a cell that did not agree is never timed, a row that did not converge is never timed, and the tolerance is never loosened to make one converge.
- **The cells that are still behind the participant beside them stay on the page.** 3 of them, at one thread on the graphs that fit in L3, by figures this campaign can measure and cannot explain. They are on this page for the same reason the improvements are.

## What is not here

**Not a ranking.** The tables put `neo4j-graph` beside Grust's accounting modes so a reader can compare like for like; nothing reduces them to an order, and `neo4j-graph` computes in `f32` to its own stopping rule and performs no work accounting.

**Not portable.** Every timing is a fact about one host — quegee, 16 vCPU on 8 physical cores, 24.8 MB L3, not burstable — on one day, as much as about the code. Numbers produced on burstable hosts during this work were for shape only and none is quoted.

**No absolute across campaigns**, for the reason stated above and shown in the unchanged-code table.

**No `f32` result outside the dangling-free families**, and no measurement of the regime where `f32` needs twice the iterations or cannot meet the tolerance at all; that is stated from Grust's own tests.

**A dated result.** v0.22.0 (`2182cdb`), `ca68900`, `87fc462`, `ead3568` and `4a9e7f5` are what was timed, and a column measured later describes that code.
