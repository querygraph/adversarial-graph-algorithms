# simple-rust-algo-bench: correctness first, timings pending

Status: **B1, B2 and B3 complete; the timed tables are not yet in this
repository.** Recorded 2026-09-21. This document holds what has been established
— that the participants compute the same functions — and states what has not.

**B3 carries two corrections, stated below under "A correction to B3": its
Grust PageRank times include a transpose no other participant's kernel time
does, and its claim of bit-identical PageRank across implementations does not
hold. A rerun that measures the first is prepared and has not been timed.**
Nothing between here and the correction has been changed except one name: the
participant B3 keyed `library` is keyed `neo4j-graph` here and in the evidence,
because Grust is a library too. The B3 tables stand as published, with the
corrections beside them.

B3 ran on the dedicated host on 2026-09-21 with **0 steal ticks over each run**,
against Grust `2182cdb` (v0.22.0), Icecat `57b443ec` and this harness at
`8fd8223`. Its evidence bundle is in this repository at
`simple-rust-algo-bench-evidence/b3-quegee/`, and every number below was
recomputed from those files rather than transcribed.

## What has been established

Five participants build in one image, are five distinct binaries, and were
checked against an independent reference at four sizes before anything was
timed.

| participant | what runs | language | parallel |
| --- | --- | --- | --- |
| `neo4j-graph` | `neo4j-labs/graph` via its builder and `graph::prelude` | Rust | rayon, unconditional |
| `icebug` | the Arrow update of NetworKit, its own headers | C++ | OpenMP, NetworKit defaults |
| `icecat` | the Rust rewrite of those kernels, Arrow 59.3 | Rust | sequential; parallel feature off |
| `grustcat` | Grust's model projected to packed Arrow adjacency | Rust | sequential |
| `grust` | Grust's kernels over `GraphProjection`, direct | Rust | sequential unless requested |

The crate names do not follow the lineage: Icecat's Rust crates are named
`icebug-*` for compatibility. The lineage is NetworKit → Icebug (C++) → Icecat
(Rust) → Grustcat.

## Parity, before any timing

80 checks per size — five participants, four algorithms, four graph families.
Identical at every size:

| size | agrees | absent | mismatch |
| ---: | ---: | ---: | ---: |
| 1,024 | 58 | 20 | 2 |
| 4,096 | 58 | 20 | 2 |
| 16,384 | 58 | 20 | 2 |
| 65,536 | 58 | 20 | 2 |

And at 16,384 for each kernel the timed run may select:

| configuration | agrees | absent | mismatch |
| --- | ---: | ---: | ---: |
| concurrency unset (push) | 58 | 20 | 2 |
| concurrency 1 (pull, one thread) | 58 | 20 | 2 |
| concurrency 2 (pull) | 58 | 20 | 2 |

Per participant, at every size: `icebug`, `icecat`, `grustcat` and `grust` agree
on 12 of 12 checks for the algorithms they implement; `neo4j-graph` agrees on 10 of
12 and mismatches on 2.

**The strongest single result is that the reference, `grust`, `icecat` and
`grustcat` return the same `f64` bit pattern for PageRank after the same 16
iterations.** Four implementations, one written independently in Python, compute
the same function rather than four nearby ones. That is what licenses comparing
their speeds at all.

The reference is in `docker/simple-rust-algo-bench/reference.py`: PageRank
iterated to the stated tolerance, components by union-find, BFS by queue,
triangles by ordered enumeration. It is borrowed from no participant, because a
participant that agrees with another participant has demonstrated nothing. Raw
results are in `simple-rust-algo-bench-evidence/parity-*.json`.

### The two mismatches, which are one difference

`neo4j-graph`'s PageRank does not redistribute dangling mass: it divides by
out-degree with no sink handling, so a node with no outgoing edge takes its share
out of the distribution. The deficit tracks the dangling fraction rather than
sitting at a fixed offset, which is what a leak does:

| fixture | dangling nodes | share | `neo4j-graph` score sum |
| --- | ---: | ---: | ---: |
| `layered-1024` | 64 | 6.25% | 0.672 |
| `layered-4096` | 64 | 1.56% | 0.911 |
| `layered-16384` | 64 | 0.39% | 0.978 |
| `layered-65536` | 64 | 0.10% | 0.994 |
| `path-1024` | 1 | 0.098% | 0.994 |
| `path-65536` | 1 | 0.0015% | 0.99991 |

This is a choice, not a defect, and the framing matters: **NetworKit defaults to
no sink handling too** and offers `DISTRIBUTE_SINKS` as an option, which this
harness sets. Grust's kernels always redistribute. So the accurate statement is
that two of these projects expose a choice the third does not, and on a graph
with dangling nodes they compute different functions.

Consequently **PageRank is published only on the dangling-free families**, `hub`
and `uniform`. The rows above are the reason, kept here rather than dropped.

### PageRank precision is a boundary, not a rounding footnote

**`neo4j-graph` accumulates and returns `f32`; every other participant is `f64`.**
Its score array is half the bytes, so half the memory traffic on the one array
PageRank touches randomly per arc. It is stated under every PageRank table.

**How much that is worth is size-dependent, and at these sizes it is small.** At
65,536 nodes the `f64` score array is 512 KB and the `f32` one 256 KB, against a
whole PageRank working set of a few megabytes — inside the L3 of either
measuring host, and about 1% of the 24.8 MB L3 of the one that publishes. So
single precision buys bandwidth on one array here and no cache residency at all.
The arrays cross that L3 somewhere in the hundreds of thousands of nodes at this
density; a run above that size must restate this sentence rather than inherit
it, because there halving an array that no longer fits is a different kind of
advantage. Cache residency is a property of the measuring host, like steal, and
is stated with the host rather than as a fact about the code.

Its consequences are measured rather than inferred, on `hub-16384`, which has no
dangling node:

| tolerance | `neo4j-graph` iterations | `neo4j-graph` score sum | `grust` iterations | `grust` score sum |
| --- | ---: | ---: | ---: | ---: |
| 1e-4 (`neo4j-graph`'s own default) | 8 | 0.9997947451 | 8 | 1.000000000000 |
| 1e-8 (the protocol tolerance) | 36 | 0.9999999668 | 17 | 1.000000000000 |

Three things follow. **The `f64` kernels preserve mass exactly at every
iteration** and the `f32` one does not: it is 2.1e-4 short after eight iterations
and still 3.3e-8 short at its converged answer. **At the same loose tolerance both
take eight iterations**, so the iteration gap at 1e-8 is about how each measures
its own residual rather than about one converging faster. And **`neo4j-graph` does
reach 1e-8**, with a residual of 9.3e-9 — it needs about twice the iterations to
get there.

A row at `neo4j-graph`'s own `1E-4` is therefore worth publishing beside the
protocol row: it is where its author put the default, it costs one more sample,
and at that tolerance its answer is 2e-4 short of a distribution on a graph with
nothing dangling.

**WCC and triangles carry no such difference.** `global_triangle_count` returns
`u64` and contains no floating point at all; component labels are index types,
and the only `f32` in the WCC path is a sampling percentage inside a heuristic
that chooses which component to skip, not a value that reaches a label.

### Two things the parity checker gets right only because they were wrong first

- **Score agreement is held to the run's stopping tolerance, not to float
  precision.** Two implementations that both stop at L1 ≤ t can differ by about t
  per node whatever their float width. Holding `f64` participants to 1e-12
  reported four NetworKit mismatches that were agreements within the tolerance
  both sides were asked for.
- **Argmax is not compared where the top two scores are separated by less than
  the tolerance.** On a chain that separation is exactly zero: every interior node
  has the same rank, so which one is the maximum is a tie-break rather than a
  result. It is recorded as a note.

## The protocol, fixed before the timings exist

- **Tolerance 1e-8**, because `grustcat`'s PageRank parameters are fixed in the
  crate and it is the only value that participant can express. Not because it is
  a good number.
- **Sizes 16,384 and 65,536.** Grust's kernels fall back to sequential below
  published floors — `1 << 14` units for PageRank and WCC, `1 << 18` for BFS —
  and 16,384 nodes at about eight edges per node is the smallest size clearing
  all three. Below a floor a row would compare a parallel library against a
  kernel that declined to parallelise, which flatters this side.
- **Every timed cell records its units, its floor and whether the floor was
  cleared**, so a row below a floor labels itself.
- **Tables are as wide as the participants that have the kernel**: five columns
  for PageRank and WCC, four for BFS, three for triangles, each naming who is
  absent and that the reason is no such kernel rather than a slow one.
- **`iterations`, `total` and `per iteration` are all published.** Per-iteration
  compares the kernels; total is what a user of that project waits for. The
  `neo4j-graph` takes 41 iterations where the others take 16, on its own stopping rule.
- **Concurrency is explicit, because it selects a kernel.** With concurrency
  unset Grust's PageRank takes the push loop that the parallel path is tested
  against; with concurrency 1 it takes the pull kernel on one thread. The two
  return different scores in the last digit, so they are distinguishable in the
  evidence and not only in a timing. Parity therefore gates the configuration
  that is timed: push, pull at one thread and pull at two all have their own
  parity runs.
- **Thread width is set for every participant by name.** The three projects read
  it from three places — Grust from `with_concurrency`, `neo4j-graph` from
  `available_parallelism` for PageRank and triangles and from rayon for WCC,
  NetworKit from OpenMP — and under a CPU quota they disagree, because OpenMP
  reads the affinity mask rather than the quota. Left alone, NetworKit would run
  the host's CPU count inside a two-CPU quota the others respect. The width is
  set in each place and recorded in every cell.
- **Two of the five cannot use a second thread at all.** `icecat` and `grustcat`
  are sequential by construction, so the full-width run is not a five-column
  parallel table and cannot become one. They appear in it with their times,
  labelled sequential by construction, because dropping them would hide that a
  participant exists — but no width-to-width ratio is drawn against them.
- **The lineage comparison belongs to the one-thread run.** Icebug to Icecat to
  Grustcat to Grust is the most informative comparison in the design and it is
  valid only at equal width. At full width, "Grust is faster than Grustcat" would
  be a statement about threads wearing the clothes of a statement about a
  rewrite.
- **Cells from runs at different widths are never divided by one another.** A
  scaling factor is its own table with its own heading, not an arithmetic a
  reader is invited to perform across two tables whose thread counts differ.
- Parity gates timing: a cell that did not agree is never timed.
- **A cell whose median absolute deviation is at least 0.25 of its median is
  unusable** and enters no table; it is reported as unusable, with its numbers,
  beside the table it would have been in. Adopted for the rerun and applied to
  every cell by `run.py` (`--unusable-dispersion 0.25`), rather than judged by
  eye per cell as B3's one such cell was.
- Variant order alternates between repeats; steal is read across the run and
  printed above the tables.


## The timed run

One host, quegee: 16 vCPU on 8 physical cores, 24.8 MB L3, not burstable.
**0 steal ticks over each run.** Tolerance 1e-8, one warmup, five repeats,
counterbalanced order, parity-gated. Evidence in
`simple-rust-algo-bench-evidence/b3-quegee/`.

### Two results against this side, stated first because they are ours

**Our general kernel is 2.1x slower per iteration than the specialised one that
descends from it.** At one thread on `uniform-65536`, `grustcat` runs PageRank at
1.981 ms per iteration and `grust` at 4.107. Same machine, same width, same
function to the same tolerance, both `f64`, both 16 iterations — so it is a cost
of the general projection rather than of the language or the measurement.

**`neo4j-graph`'s triangle counting scales far better than ours.** On
`uniform-65536` it is 47.65 ms against our 86.80 at one thread, a factor of 1.8;
at full width it is 4.11 against 30.17, a factor of **7.3**. The sequential gap
is modest and the parallel gap is not, which places the difference in how each
parallelises rather than in the kernel.

A third, not against us but against an assumption: **`icebug`, the C++ original,
is the slowest sequential PageRank here and the best parallel one** — 6.3 ms per
iteration at one thread, and 7.8x at width where we reach 3.4x.

### PageRank at 65,536, one thread

Totals and per-iteration, because the participants stop on different rules and
only the second compares kernels.

| participant | hub total | hub /iter | uniform total | uniform /iter | iters | precision |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `neo4j-graph` | 39.23 | 1.401 | 48.47 | 1.425 | 28 / 34 | **f32** |
| `icebug` (C++) | 73.50 | 6.125 | 69.68 | 6.335 | 12 / 11 | f64 |
| `icecat` (Rust) | 35.57 | 2.092 | 33.76 | 2.110 | 17 / 16 | f64 |
| `grustcat` | 32.18 | 1.893 | 31.70 | 1.981 | 17 / 16 | f64 |
| `grust` | 66.08 | 3.887 | 65.71 | 4.107 | 17 / 16 | f64 |

**`neo4j-graph` computes in single precision and the others in double.** Its score
array is half the bytes. At this size that buys bandwidth on one array and no
cache residency: every participant's working set is inside this host's 24.8 MB
L3. The arrays cross that L3 in the hundreds of thousands of nodes at this
density, and a larger run must restate this rather than inherit it.

The lineage, per iteration at equal width: C++ `icebug` 6.13 → Rust `icecat`
2.09 → `grustcat` 1.89 → `grust` 3.89. **This is the only configuration in which
that comparison is valid**, because two participants cannot use a second thread.

### Full width, `--cpus 16 --workers 16`

`icecat` and `grustcat` are sequential by construction. Their times are shown
where they appear but **no width ratio is drawn against them**, and they barely
move, which is the honest confirmation of the label rather than a result.

| cell | one thread | full width | ratio |
| --- | ---: | ---: | ---: |
| `icebug` pagerank uniform-65536 | 69.68 | 8.96 | **7.78x** |
| `grust` pagerank uniform-65536 | 65.71 | 19.20 | 3.42x |
| `neo4j-graph` pagerank uniform-65536 | 48.47 | 17.03 | 2.85x |
| `neo4j-graph` triangles uniform-65536 | 47.65 | 4.11 | **11.59x** |
| `grust` triangles uniform-65536 | 86.80 | 30.17 | 2.88x |
| `grust` bfs hub-65536 | 7.86 | 4.30 | 1.83x |
| `grust` bfs hub-16384 | 1.63 | 1.66 | 0.98x |

**That last row is not a scaling failure.** BFS at 16,384 computes 147,313 units
against a floor of 262,144, so Grust's kernel declines to parallelise and no
second thread is used; the cell records `parallel_eligible: false`. At 65,536 it
clears the floor and moves. A run at 16,384 alone would have published a row that
looked like a defect and was a threshold.

### One cell not published

`icebug` PageRank on `hub-16384` at full width read 54.09 ± 51.01 ms — a spread
the size of its median, plausibly OpenMP spinning on a graph too small to
amortise it. A median with a MAD its own size is not a measurement, so it is
recorded as unusable and enters no table.

## A correction to B3

**Grust's PageRank rows above include building the transpose; no other
participant's kernel time does.** Grust's pull kernel needs the incoming
adjacency, and at v0.22.0 a projection builds it lazily, inside the first
kernel call that asks for it. B3 made exactly one call, and both timed runs set
a concurrency, which selects the pull kernel, so `kernel_ms` for every `grust`
PageRank row in both timed tables contains a one-off transpose. `grustcat`,
`neo4j-graph` and NetworKit build their reverse adjacency in their
constructors, inside `build_ms` (checked in each source: grustcat's
constructor, `graph_builder`'s `DirectedCsrGraph::csr_inc`, NetworKit's
`GraphW::addEdge` filling `inEdges`); `icecat` builds it between the two timers
and reports it apart. The same work therefore sat on opposite sides of the
timing boundary, against us.

What that affects: the one-thread PageRank table, the lineage sentence under it,
the headline "2.1x slower per iteration" (per-iteration divides the one-off
build across 16 or 17 iterations, so it inflates that column too), and the
`grust` PageRank rows of the full-width table. A profile outside this harness
attributed 25–29% of the published 2.1x gap to it; **that figure is the
profile's and has not been measured here.** The rerun measures it, on both
the release and the later commit, and the corrected numbers will be stated
here beside the published ones, not in place of them. BFS, WCC and triangles
are unaffected: none of them reads the incoming adjacency.

### A second correction: "the same `f64` bit pattern" does not hold

"What has been established" says the reference, `grust`, `icecat` and
`grustcat` return the same `f64` bit pattern for PageRank after 16 iterations.
B3's parity never compared bits: it held `max` and `sum` to the stopping
tolerance and stored no scores. The rerun's parity compares them, on the
measuring host, with evidence in
`simple-rust-algo-bench-evidence/b4-prep-44aa421/`. On `uniform-65536`, the
fixture the sentence is about, all four take 16 iterations, and:

| participant | maximum score | same bits as the reference |
| --- | --- | --- |
| reference | `4.285462911850025e-05` | — |
| `grust`, push (concurrency unset) | `4.285462911850025e-05` | yes |
| `grust`, pull (concurrency 1) | `4.285462911850024e-05` | no, 1 ulp |
| `icecat` | `4.285462911850024e-05` | no, 1 ulp |
| `grustcat` | `4.285462911850024e-05` | no, 1 ulp |

Over whole vectors, Grust's push kernel is bit-identical to the reference on
every `path` and `layered` fixture, and on 65,467 of 65,536 scores of
`uniform-65536` (the rest within 2 ulps); on `hub-65536` 3,230 of 65,536 (within
7 ulps). The pull kernel matches 29,430 of 65,536 on `uniform-65536`, within 4
ulps. The two formulations differ where the rounding would be expected to: the
reference forms each share as `d·s/deg` and Grust's push loop as
`d·s·(1/deg)`; that this explains every differing bit is plausible and
unverified.

**The sentence is withdrawn as written.** What holds is that every `f64`
participant agrees with the reference far inside the stopping tolerance, with
the same iteration count, so they compute the same function to the precision
that tolerance defines — which is what licenses comparing their speeds. Bit
identity is a stronger property and holds where it is stated: between Grust
builds. `grust-next` returns v0.22.0's vector bit for bit on 24 of 24
PageRank checks at each of the three concurrency configurations.

## The rerun, prepared and not yet timed

Everything in "The protocol" above still holds: tolerance 1e-8, sizes 16,384
and 65,536, thread width set per participant by name, counterbalanced order,
one warmup and five repeats, parity before timing. The rerun adds three
measurements, each as its own labelled rows and never folded into one number.

- **The transpose, on the build side.** Grust at the commit under test has
  `GraphProjection::prepare_incoming()`; the `grust-next` participant calls it
  inside the build timer, as grustcat's constructor does, and reports its share
  of `build_ms` as `incoming_ms`. v0.22.0 has no such method, so every Grust
  build runs the kernel twice on one projection and reports both: `call: first`
  is what B3 published, `call: second` has the transpose cached. The second
  call also runs on warm caches, which is not the same condition as grustcat's
  first call after its constructor; it is labelled rather than presented as the
  corrected number. The two calls must return identical results or the
  participant exits non-zero and the cell is never timed.
- **The kernel change.** `grust` is v0.22.0 (`2182cdb`), as published;
  `grust-next` is the later commit, built from the same participant source with
  a feature that selects the API it added. Its PageRank hoists each source's
  share out of the pull kernel's arc loop and charges the push loop's arcs in
  blocks instead of one atomic per arc. Both kernels are timed: pull
  (`#1`, what B3 timed) and push (`#unset`, where the charging changed).
- **Accounting modes.** `grust-next` takes `--accounting counted`,
  `work-uncounted` or `unchecked`, and every output line names the mode.
  `counted` is the default, is what v0.22.0 always does, and stays a row.
  `neo4j-graph` performs no accounting, so `unchecked` is its like-for-like row
  and the distance to `counted` is what the guarantee costs. v0.22.0 accepts
  only `counted` and refuses the others rather than running counted under
  another name.

Gates and discipline added for it:

- **Bits gate the comparison.** A `grust-next` PageRank vector must equal
  v0.22.0's bit for bit — every score, compared by digest, and the iteration
  count — at the same concurrency on every fixture, or it is a mismatch and is
  never timed. A kernel that changed a score computes a different function.
- **Every score is also compared with the reference**, and the count of
  bit-identical scores is recorded.
- **Host idle before, during and after every run**: no cargo, rustc, perf,
  other benchmark or other container, checked on the host outside the image and
  sampled once a second through the run. A shared run is kept, renamed
  discarded, and not published; nothing retries on its own.
- **Steal is reported with every cell**, not only per run.
- **The unusable-cell rule is now stated in "The protocol" above**: MAD at
  least 0.25 of the median. B3 made that call by eye for one cell at 94%.
- **A size above L3.** The hoist changes which arrays the pull kernel indexes
  at random, and at 65,536 every one of them fits in this host's L3, so it was
  never measured where that matters. By arithmetic, not measurement: one `f64`
  per node is 16.8 MB at 2,097,152 nodes and 33.6 MB at 4,194,304, against a
  24.8 MB L3; v0.22.0's pull loop indexes two such arrays per arc, `scores` and
  `offsets`, and the later commit's one, `shares`. Those runs will restate the
  precision paragraph for their size rather than inherit it, as that paragraph
  requires.

## What is not here

- **Not portable.** Every timing below is from one host — quegee, 16 vCPU on 8
  physical cores, 24.8 MB L3, not burstable, 0 steal ticks per run — and is a
  fact about that machine as much as about the code. Numbers produced on a
  burstable box during this work were for shape only and none is quoted here.
- **No comparison against `neo4j-labs/graph` on speed.** Nothing in this document
  says which is faster, because nothing has been measured that could.
- **No claim about parallel execution.** Whether the Grust participants run
  parallel in the timed run is undecided at the time of writing.
- **A dated result.** Parallel execution is being added to the kernels on this
  side as this is written; a column measured then describes that code.
