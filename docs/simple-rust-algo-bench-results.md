# simple-rust-algo-bench: correctness first, timings pending

Status: **B1, B2 and B3 complete; the timed tables are not yet in this
repository.** Recorded 2026-09-21. This document holds what has been established
— that the participants compute the same functions — and states what has not.

**B3 carries two corrections, stated below under "A correction to B3": its
Grust PageRank times include a transpose no other participant's kernel time
does, and its claim of bit-identical PageRank across implementations does not
hold. B4, a rerun that measures the first, the Grust kernel change since
v0.22.0 and the cost of Grust's accounting, ran on 2026-09-21; its results are
under "B4: results".**

**B4 in turn carries a correction of its own, stated under "B5: what B4 got
wrong": it built the transpose inside the build timer for WCC and BFS, two
kernels that never read it, which left the allocator in a state their v0.22.0
column was not measured in and moved their first-call rows. B5, a rerun of the
whole campaign with that corrected, with minor page faults recorded beside
every call and against Grust `ca68900`, ran on 2026-09-22; its results are
under "B5: results". B4's tables stand as published, with B5's beside them —
and B4's WCC and BFS first-call rows, and its "the cause is unexplained"
paragraph, should be read with B5's correction.**
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
profile's.** B4 measured it: on `uniform-65536` at one thread the transpose is 8.77 ms of `grust-next`'s `build_ms`, against a first-call gap to `grustcat` of 28.20 ms on v0.22.0 in the same run, 31% of it. The corrected rows are under
"B4: results", beside B3's rather than in place of them. BFS, WCC and triangles
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

## B4: the rerun's protocol

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

## B4: results

One host, quegee, 2026-09-21. Grust `2182cdb` (v0.22.0) as `grust`, Grust
`4d8e5db` (`main`, the merge of PR #30) as `grust-next`, Icecat `57b443ec`,
this harness at `9d58001`, image `simple-rust-algo-bench:rerun-4d8e5db` built on
the host from clean trees. One warmup, five repeats, counterbalanced, parity
gated at every concurrency. **Every cell of every run, with its steal, its
dispersion and its usability, is in
`simple-rust-algo-bench-evidence/b4-quegee/tables.md`**, generated from the run
files by `tables.py`; the tables below select from it and add nothing to it.
Times are milliseconds, median ± MAD. Steal is ticks over that cell's group of
samples.

**Host conditions.** A resident agent session on the host, pid 1496, used up to
63% of a CPU in bursts through the afternoon, and parity runs that overlapped it
are marked shared in `campaign.jsonl`; its last sighting there is in the run
that started at 20:22:49Z. The operator paused it at or before 20:26Z and then
killed it; that is the operator's account, and what the campaign itself records
is that the process was absent before every timed run, from 20:59:30Z on. The
host was checked idle before and after every run and sampled once a second
during it.
- `one-thread`: clean, started 2026-09-21T20:59:32+0000, 235.7 s, 1 steal ticks over the run, 0 sightings.
- `full-width`: clean, started 2026-09-21T21:03:29+0000, 114.9 s, 0 steal ticks over the run, 0 sightings.
- `large-one-thread`: clean, started 2026-09-21T21:05:26+0000, 2507.0 s, 10 steal ticks over the run, 0 sightings.
- `large-full-width`: clean, started 2026-09-21T21:47:16+0000, 909.4 s, 4 steal ticks over the run, 0 sightings.
- `xlarge-one-thread`: DISCARDED: host shared during the run, started 2026-09-21T22:02:27+0000, 5368.7 s, 21 steal ticks over the run, 2 sightings.
- `xlarge-one-thread`: clean, started 2026-09-21T23:33:03+0000, 5120.8 s, 20 steal ticks over the run, 0 sightings.
- `xlarge-full-width`: clean, started 2026-09-22T00:58:26+0000, 1772.0 s, 8 steal ticks over the run, 0 sightings.

The first `xlarge-one-thread` was discarded, and the cause was ours: in its
first 35 seconds the agent running the campaign started a `docker run` of the
audit script and a `sha256sum` of the xlarge fixtures, to collect provenance for
this document. The watcher saw both and the run was discarded as the protocol
requires; its file is kept under `discarded/` and none of its numbers appears
here. `xlarge-one-thread` was then run again, and `xlarge-full-width` — which the
campaign had not reached — run for the first time, on an idle host with nothing
else started on it.

**None of the 1080 cells reached the 0.25 MAD/median threshold**; the largest dispersion was 0.170, `grust-next@work-uncounted#unset` bfs uniform-65536 first in one-thread.

**Parity at `4d8e5db`**, every fixture set at concurrency unset, 1 and 16, before any timing. `grust-next` is bit-identical to v0.22.0 in every PageRank row, which is the gate that licenses the kernel comparison below; the only mismatches are the `neo4j-graph` dangling-mass rows B3 already reported.

| file | agree | absent | mismatch | error | bits-identical to v0.22.0 | mismatched rows |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `fixtures-1` | 220 | 32 | 4 | 0 | 24 of 24 | neo4j-graph layered-16384, neo4j-graph layered-65536, neo4j-graph path-16384, neo4j-graph path-65536 |
| `fixtures-16` | 220 | 32 | 4 | 0 | 24 of 24 | neo4j-graph layered-16384, neo4j-graph layered-65536, neo4j-graph path-16384, neo4j-graph path-65536 |
| `fixtures-large-1` | 16 | 0 | 0 | 0 | 6 of 6 | — |
| `fixtures-large-16` | 16 | 0 | 0 | 0 | 6 of 6 | — |
| `fixtures-large-unset` | 16 | 0 | 0 | 0 | 6 of 6 | — |
| `fixtures-unset` | 220 | 32 | 4 | 0 | 24 of 24 | neo4j-graph layered-16384, neo4j-graph layered-65536, neo4j-graph path-16384, neo4j-graph path-65536 |
| `fixtures-xlarge-1` | 16 | 0 | 0 | 0 | 6 of 6 | — |
| `fixtures-xlarge-16` | 16 | 0 | 0 | 0 | 6 of 6 | — |
| `fixtures-xlarge-unset` | 16 | 0 | 0 | 0 | 6 of 6 | — |

3 parity invocations exited 1. `parity.py` exits 1 whenever any row mismatches, and the protocol fixture set always contains the four known `neo4j-graph` rows; the PageRank-only large sets contain none and exit 0. The driver records a parity verdict from its file, not its exit code. 3 parity invocations are marked shared, every sighting in them the resident session above. Parity verdicts are computed results and do not depend on host load, so these were not rerun; the files above are the output of the last invocation of each set and configuration, including the shared ones. Every parity and timed invocation used the same image, built once before parity began.

**Absolute times moved between B3 and B4 on unchanged code.** `grust` at v0.22.0 on `uniform-65536`, one thread, first call: 65.71 ms in B3, 59.44 ± 3.00 in B4; `icecat` 33.76 then 30.24 ± 0.19. The binaries were rebuilt from the same
sources, stamped with different commits. So a B4 cell is compared only with
other cells of the same B4 run, never with a B3 cell.

### The transpose correction

One thread, pull kernel (concurrency 1), PageRank. "First" is a fresh
projection's first kernel call, which is what B3 timed; on v0.22.0 it includes
building the transpose. "Second" repeats the call on the same projection with
the transpose cached — and on warm caches, which is not the condition of any
other participant's timed call: triangles on `uniform-65536` at full width, which builds nothing lazily, takes 33.28 ms on v0.22.0's first call and 27.08 on its second, 19% less. So v0.22.0's second call is not
the corrected number. The corrected number is `grust-next`'s first call, whose
transpose is built inside `build_ms` as grustcat's is; the transpose column is
its share of that build. That column contains the kernel change as well; the
next table separates the two.

| fixture | `grust` v0.22.0 first | `grust` v0.22.0 second | `grust-next` counted first | transpose, in `build_ms` | `grustcat` | steal |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `hub-65536` | 65.11 ± 0.37 | 55.68 ± 4.07 | 36.90 ± 0.07 | 8.52 | 34.01 ± 0.34 | 0 |
| `uniform-65536` | 59.44 ± 3.00 | 49.38 ± 4.14 | 35.02 ± 0.10 | 8.77 | 31.24 ± 0.35 | 1 |
| `hub-2097152` | 6388.56 ± 29.42 | 5625.49 ± 67.26 | 3460.55 ± 110.02 | 723.86 | 3112.82 ± 12.53 | 5 |
| `uniform-2097152` | 6661.30 ± 59.64 | 5957.46 ± 26.04 | 3696.77 ± 24.86 | 708.88 | 3512.28 ± 41.73 | 5 |
| `hub-4194304` | 14198.59 ± 88.39 | 12486.68 ± 74.79 | 8180.58 ± 42.20 | 1552.63 | 7014.94 ± 55.22 | 11 |
| `uniform-4194304` | 13314.92 ± 61.02 | 11981.43 ± 23.08 | 7268.50 ± 229.66 | 1365.16 | 7052.95 ± 62.84 | 9 |

### The kernel change, v0.22.0 against `4d8e5db`

Same mode (counted), same concurrency, and second call against second call, so
the transpose is cached on both sides. Both builds return the same scores bit
for bit, which parity checked on every fixture at every concurrency.

| fixture | run | kernel | v0.22.0 | `4d8e5db` | ratio | steal |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `hub-16384` | one-thread | pull | 9.50 ± 0.01 | 8.82 ± 0.02 | 0.928 | 0 |
| `hub-16384` | one-thread | push | 50.64 ± 0.02 | 22.85 ± 0.11 | 0.451 | 0 |
| `hub-65536` | one-thread | pull | 55.68 ± 4.07 | 36.55 ± 0.18 | 0.656 | 0 |
| `hub-65536` | one-thread | push | 207.57 ± 2.73 | 94.26 ± 0.60 | 0.454 | 0 |
| `uniform-16384` | one-thread | pull | 9.12 ± 0.01 | 8.30 ± 0.01 | 0.910 | 0 |
| `uniform-16384` | one-thread | push | 47.91 ± 0.01 | 21.13 ± 0.02 | 0.441 | 0 |
| `uniform-65536` | one-thread | pull | 49.38 ± 4.14 | 34.05 ± 0.06 | 0.689 | 1 |
| `uniform-65536` | one-thread | push | 195.33 ± 0.76 | 88.79 ± 0.91 | 0.455 | 1 |
| `hub-16384` | full-width | pull | 3.49 ± 0.07 | 3.63 ± 0.11 | 1.040 | 0 |
| `hub-65536` | full-width | pull | 8.65 ± 0.22 | 7.70 ± 0.11 | 0.890 | 0 |
| `uniform-16384` | full-width | pull | 3.28 ± 0.10 | 3.46 ± 0.03 | 1.056 | 0 |
| `uniform-65536` | full-width | pull | 8.33 ± 0.08 | 7.24 ± 0.15 | 0.870 | 0 |
| `hub-2097152` | large-one-thread | pull | 5625.49 ± 67.26 | 3564.08 ± 88.06 | 0.634 | 5 |
| `hub-2097152` | large-one-thread | push | 16114.66 ± 40.17 | 7141.83 ± 235.42 | 0.443 | 5 |
| `uniform-2097152` | large-one-thread | pull | 5957.46 ± 26.04 | 3592.64 ± 35.02 | 0.603 | 5 |
| `uniform-2097152` | large-one-thread | push | 16646.03 ± 302.70 | 7030.66 ± 38.47 | 0.422 | 5 |
| `hub-2097152` | large-full-width | pull | 562.12 ± 8.64 | 271.02 ± 17.65 | 0.482 | 2 |
| `uniform-2097152` | large-full-width | pull | 640.06 ± 14.20 | 277.59 ± 13.38 | 0.434 | 2 |
| `hub-4194304` | xlarge-one-thread | pull | 12486.68 ± 74.79 | 8040.04 ± 88.57 | 0.644 | 11 |
| `hub-4194304` | xlarge-one-thread | push | 34026.71 ± 75.39 | 15106.92 ± 140.47 | 0.444 | 11 |
| `uniform-4194304` | xlarge-one-thread | pull | 11981.43 ± 23.08 | 7227.70 ± 115.88 | 0.603 | 9 |
| `uniform-4194304` | xlarge-one-thread | push | 26102.82 ± 517.15 | 13142.20 ± 105.13 | 0.503 | 9 |
| `hub-4194304` | xlarge-full-width | pull | 1362.08 ± 1.53 | 731.33 ± 16.30 | 0.537 | 4 |
| `uniform-4194304` | xlarge-full-width | pull | 1458.50 ± 2.96 | 761.34 ± 8.27 | 0.522 | 4 |

**It got worse elsewhere.** On `4d8e5db`, counted WCC is slower than v0.22.0 on the first call in 24 of 24 one-thread and full-width cells (+0.3% to +18.9%; median +15.9% at one thread), and on the second call in 11 of 24; counted BFS is slower than v0.22.0 on the first call in 20 of 24 one-thread and full-width cells (-4.5% to +11.4%; median +7.6% at one thread), and on the second call in 8 of 24. The largest PageRank change the wrong way, second call against second call, is +11.1%. At one thread the uncounted modes' medians for the same WCC and BFS cells are -23.0% to -47.6% against v0.22.0. Every such cell is in `tables.md`. **The
cause is unexplained.** A penalty that fades on the second call is consistent
with state left by the build — `grust-next` now builds the transpose just
before the first call — and with other one-off costs; the control that would
separate them is `grust-next` without `prepare_incoming`, which this run did
not include.

### What the accounting guarantee costs

`grust-next`, first call, by mode. `counted` is the default and what v0.22.0
always does; `unchecked` performs neither work accounting nor cancellation
checks, and `neo4j-graph` performs neither either, though Grust still admits memory in every
mode. `neo4j-graph` is `f32` and stops on its own rule (26 to 34 iterations
where the others run 16 or 17), so its column is a total for a different
number of iterations, not a kernel comparison.

| fixture | run | kernel | counted | work-uncounted | unchecked | `neo4j-graph` | steal |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `hub-65536` | one-thread | pagerank, pull | 36.90 ± 0.07 | 34.15 ± 0.22 | 32.43 ± 0.38 | 40.03 ± 0.40 | 0 |
| `hub-65536` | one-thread | pagerank, push | 96.04 ± 0.97 | 61.09 ± 0.51 | 58.18 ± 0.51 | 40.03 ± 0.40 | 0 |
| `hub-65536` | one-thread | wcc, concurrency 1 | 7.31 ± 0.03 | 4.93 ± 0.07 | 4.62 ± 0.04 | 3.84 ± 0.01 | 0 |
| `hub-65536` | one-thread | wcc, concurrency unset | 19.78 ± 0.06 | 10.15 ± 0.04 | 9.52 ± 0.13 | 3.84 ± 0.01 | 0 |
| `hub-65536` | one-thread | triangles, concurrency 1 | 77.02 ± 1.57 | 77.26 ± 0.61 | 75.89 ± 0.71 | 42.31 ± 0.74 | 0 |
| `hub-65536` | one-thread | triangles, concurrency unset | 79.47 ± 0.31 | 76.28 ± 0.76 | 76.82 ± 1.03 | 42.31 ± 0.74 | 0 |
| `uniform-65536` | one-thread | pagerank, pull | 35.02 ± 0.10 | 32.53 ± 0.08 | 30.89 ± 0.16 | 48.49 ± 0.20 | 1 |
| `uniform-65536` | one-thread | pagerank, push | 88.77 ± 0.66 | 57.11 ± 0.44 | 53.63 ± 0.39 | 48.49 ± 0.20 | 1 |
| `uniform-65536` | one-thread | wcc, concurrency 1 | 10.70 ± 0.10 | 8.74 ± 0.02 | 8.44 ± 0.02 | 3.86 ± 0.01 | 0 |
| `uniform-65536` | one-thread | wcc, concurrency unset | 20.23 ± 0.09 | 11.13 ± 0.08 | 10.58 ± 0.13 | 3.86 ± 0.01 | 0 |
| `uniform-65536` | one-thread | triangles, concurrency 1 | 80.43 ± 0.61 | 80.84 ± 0.95 | 81.73 ± 0.38 | 46.94 ± 1.05 | 0 |
| `uniform-65536` | one-thread | triangles, concurrency unset | 83.23 ± 1.01 | 81.66 ± 1.92 | 81.05 ± 0.31 | 46.94 ± 1.05 | 0 |
| `hub-65536` | full-width | pagerank, pull | 9.06 ± 0.11 | 6.97 ± 0.22 | 6.52 ± 0.05 | 15.42 ± 0.73 | 0 |
| `hub-65536` | full-width | wcc | 2.84 ± 0.07 | 2.36 ± 0.05 | 2.31 ± 0.13 | 3.10 ± 0.23 | 0 |
| `hub-65536` | full-width | triangles | 31.37 ± 0.18 | 30.70 ± 0.15 | 30.94 ± 0.34 | 3.79 ± 0.02 | 0 |
| `uniform-65536` | full-width | pagerank, pull | 8.95 ± 0.16 | 6.47 ± 0.14 | 6.50 ± 0.06 | 17.19 ± 0.36 | 0 |
| `uniform-65536` | full-width | wcc | 3.21 ± 0.05 | 2.60 ± 0.17 | 2.74 ± 0.03 | 3.18 ± 0.18 | 0 |
| `uniform-65536` | full-width | triangles | 32.98 ± 0.15 | 32.20 ± 0.24 | 32.10 ± 0.12 | 4.09 ± 0.08 | 0 |
| `hub-2097152` | large-one-thread | pagerank, pull | 3460.55 ± 110.02 | 3514.41 ± 35.93 | 3186.54 ± 21.14 | 2585.38 ± 139.56 | 5 |
| `hub-2097152` | large-one-thread | pagerank, push | 6980.05 ± 561.78 | 5839.02 ± 239.40 | 5862.38 ± 75.51 | 2585.38 ± 139.56 | 5 |
| `uniform-2097152` | large-one-thread | pagerank, pull | 3696.77 ± 24.86 | 3581.36 ± 134.98 | 3363.09 ± 63.65 | 2553.54 ± 75.83 | 5 |
| `uniform-2097152` | large-one-thread | pagerank, push | 7015.63 ± 49.71 | 5733.41 ± 3.37 | 5596.27 ± 20.63 | 2553.54 ± 75.83 | 5 |
| `hub-2097152` | large-full-width | pagerank, pull | 264.98 ± 8.93 | 244.46 ± 3.46 | 241.99 ± 6.30 | 272.61 ± 2.04 | 2 |
| `uniform-2097152` | large-full-width | pagerank, pull | 267.94 ± 6.19 | 261.48 ± 12.04 | 268.63 ± 8.12 | 283.89 ± 1.33 | 2 |
| `hub-4194304` | xlarge-one-thread | pagerank, pull | 8180.58 ± 42.20 | 7677.63 ± 18.04 | 7494.93 ± 36.38 | 6158.30 ± 164.91 | 11 |
| `hub-4194304` | xlarge-one-thread | pagerank, push | 15152.10 ± 70.99 | 12675.26 ± 63.88 | 12707.47 ± 12.41 | 6158.30 ± 164.91 | 11 |
| `uniform-4194304` | xlarge-one-thread | pagerank, pull | 7268.50 ± 229.66 | 7031.98 ± 142.72 | 6828.03 ± 232.25 | 5328.15 ± 153.34 | 9 |
| `uniform-4194304` | xlarge-one-thread | pagerank, push | 12873.93 ± 345.52 | 10783.82 ± 317.82 | 10736.38 ± 588.46 | 5328.15 ± 153.34 | 9 |
| `hub-4194304` | xlarge-full-width | pagerank, pull | 730.85 ± 3.55 | 698.17 ± 18.59 | 695.38 ± 15.32 | 342.47 ± 39.57 | 4 |
| `uniform-4194304` | xlarge-full-width | pagerank, pull | 757.06 ± 6.56 | 733.26 ± 11.33 | 723.81 ± 13.01 | 620.22 ± 22.72 | 4 |

Counting also costs in the build: `grust-next`'s `build_ms` for PageRank on `hub-65536` at one thread is 127.68 ms counted, 71.95 work-uncounted and 69.54 unchecked, because building the projection and its transpose charges work too.

### PageRank precision, restated for the sizes above L3

At 2,097,152 nodes an `f64` score array is 16.8 MB and `neo4j-graph`'s `f32`
one 8.4 MB, against quegee's 24.8 MB L3: either fits alone, and neither fits
beside the rest of a working set whose edge arrays alone exceed 100 MB. At
4,194,304 the `f64` array is 33.6 MB and does not fit on its own; the `f32` one
is 16.8 MB and does. At that size single precision can buy cache residency on
the one randomly indexed array, not only bandwidth. This is arithmetic from
array sizes and the host's L3, not a measurement of cache behaviour.

## B5: what B4 got wrong, and the protocol that corrects it

An attribution run outside this harness, on the measuring host, found two
things behind B4's WCC and BFS rows. Its evidence is on that host in
`~/src/perfattr/clean/R1-R8` with its driver `drive.py`; it is not this
repository's evidence and nothing below is taken from it as a number. What B5
does is correct the harness for both and measure again.

- **An allocator artifact, and it was ours.** B4's Grust participant called
  `prepare_incoming()` inside the build timer for every algorithm, to make its
  build column the same work as grustcat's constructor. WCC and BFS never read
  the incoming adjacency — checked in the kernels, not inferred — so for those
  two the harness built and freed a transpose nothing would read, immediately
  before the call it was timing. Freeing a large mapped chunk raises glibc's
  own mmap threshold, so the next call's large allocations came from a
  different place: the attribution measured about 112 to 128 extra minor page
  faults on the first call, and pinning the threshold removed the difference.
  B4's `grust-next` first calls were therefore slower, and its second calls
  faster, than the code alone accounts for.
- **A real regression, since fixed.** `WorkMeter::charge` had been pushed out
  of line in 16 kernels at `4d8e5db`, which is what B4 timed. It is inlined
  again on Grust `ca68900`, the commit B5 times, which also adds child contexts
  and `with_execution`.

The harness changes, each with the reason it is not the other choice:

- **The transpose is built in the build timer only for the kernel that reads
  it.** `--prepare-incoming needed` is the default: PageRank's pull kernel, and
  nothing else in this matrix. B4's behaviour stays available as the `+eager`
  variant, `--prepare-incoming always`, and is timed as its own labelled row at
  the protocol sizes, so the correction is shown rather than asserted. Matching
  grustcat's constructor was the wrong thing to match: a build column that does
  work no kernel will read is not the same measurement as a build column that
  does work the kernel needs.
- **Minor page faults beside every first-call time.** Every participant now
  reads `getrusage(RUSAGE_SELF).ru_minflt` on both sides of the call it times,
  outside the timer, and reports it; `tables.md` carries it for every cell. A
  time that moved while the counter did not is not this effect.
- **The allocator is pinned for every participant in a run, or for none.**
  Pinning `GLIBC_TUNABLES=glibc.malloc.mmap_threshold=131072` for the Grust
  participants alone would compare two allocators, which is the same kind of
  error as B4's. Whether to pin at all is decided by measurement, not by
  assumption: `pinned-one-thread` and `pinned-full-width` repeat the two
  protocol-size runs with the threshold pinned for the whole container, every
  participant included, and are published as their own labelled table.

**The rule for that decision, fixed before the runs.** The published tables are
the default-allocator runs, because glibc's default is the allocator every
participant's users have and none of these projects sets a tunable; the pinned
runs are published beside them as a labelled probe of what the threshold is
worth to each participant. That stands unless the corrected harness leaves the
two Grust builds in different allocator states on the same cell — which the
page-fault counter now shows directly — in which case the first-call rows would
be the pinned ones and every size would be rerun pinned. The line is a median
difference of 25 minor page faults over the WCC and BFS first-call cells at the
protocol sizes, a fifth of the 112 to 128 the attribution measured for the
artifact itself. Which of those happened is stated under "B5: results", with
the counter it was decided on, by the script that reads the evidence.

One host preparation is new and applies to every run equally: the page cache is
dropped before the campaign starts. A parity invocation at 2,097,152 nodes was
discarded here because `kswapd` and `kcompactd` woke during it, which is the
kernel reclaiming memory for the run rather than a second workload — but the
idle rule does not distinguish those, and weakening the rule to let a run pass
is not a thing to do to a rule. The cause is removed instead, before anything
is timed, and the campaign keeps the rule it was written with.

Everything else is B4's protocol unchanged: parity before timing and a
mismatched cell never timed, the bits gate against v0.22.0, counterbalanced
order, one warmup and five repeats, thread width set for every participant by
name, the 0.25 MAD/median dispersion rule, steal reported per cell, the
accounting modes as separate rows, the `neo4j-graph` naming, and the protocol,
large and xlarge sizes.

## B5: results

One host, quegee, 2026-09-22. Grust `2182cdb` (v0.22.0) as `grust`, Grust `ca68900` as `grust-next`, Icecat `57b443ec`, this harness at `9ec8548`, image `simple-rust-algo-bench:b5-ca68900`, built on the host from clean trees. One warmup, five repeats,
counterbalanced, parity gated at every concurrency. **Every cell of every run,
with its steal, its dispersion, its minor page faults and its usability, is in
`simple-rust-algo-bench-evidence/b5-quegee/tables.md`**, generated from the run
files by `tables.py`; the tables below select from it and add nothing to it.
Times are milliseconds, median ± MAD; page faults are the median of the same
samples, read outside the timers. Steal is ticks over that cell's group.

**Host conditions.** 1 resident agent session was seen by name across the campaign (2382171 codex resume 01a0ad61-0419-7110-9e8c-c25058935bc0). 0 sightings were recorded over 8 timed invocations, and a run with a sighting is discarded rather than published. The host was checked idle before and after every run and sampled once a second during it.

- `one-thread`: clean, started 2026-09-22T07:32:22+0000, 236.8 s, 1 steal ticks over the run, 0 sightings, 1 resident agent session.
- `full-width`: clean, started 2026-09-22T07:36:21+0000, 104.5 s, 0 steal ticks over the run, 0 sightings, 1 resident agent session.
- `pinned-one-thread`: clean, started 2026-09-22T07:38:08+0000, 139.4 s, 1 steal ticks over the run, 0 sightings, 1 resident agent session.
- `pinned-full-width`: clean, started 2026-09-22T07:40:29+0000, 76.2 s, 0 steal ticks over the run, 0 sightings, 1 resident agent session.
- `large-one-thread`: clean, started 2026-09-22T07:41:47+0000, 1674.2 s, 7 steal ticks over the run, 0 sightings, 1 resident agent session.
- `large-full-width`: clean, started 2026-09-22T08:09:44+0000, 711.1 s, 3 steal ticks over the run, 0 sightings, 1 resident agent session.
- `xlarge-one-thread`: clean, started 2026-09-22T08:21:37+0000, 4300.3 s, 129 steal ticks over the run, 0 sightings, 1 resident agent session.
- `xlarge-full-width`: clean, started 2026-09-22T09:33:19+0000, 1551.3 s, 7 steal ticks over the run, 0 sightings, 1 resident agent session.

**1 of 1840 cells reached the 0.25 MAD/median threshold** and enter no table: `grust-next@counted` pagerank path-65536 first in pinned-full-width, 48.21 ± 12.26.

**Parity at the commit under test**, every fixture set at concurrency unset, 1
and 16, before any timing. `grust-next` must return v0.22.0's PageRank vector
bit for bit or it is a mismatch and is never timed.

| file | agree | absent | mismatch | error | bits-identical to v0.22.0 | mismatched rows |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `fixtures-1` | 252 | 32 | 4 | 0 | 24 of 24 | neo4j-graph layered-16384, neo4j-graph layered-65536, neo4j-graph path-16384, neo4j-graph path-65536 |
| `fixtures-16` | 252 | 32 | 4 | 0 | 24 of 24 | neo4j-graph layered-16384, neo4j-graph layered-65536, neo4j-graph path-16384, neo4j-graph path-65536 |
| `fixtures-large-1` | 18 | 0 | 0 | 0 | 6 of 6 | — |
| `fixtures-large-16` | 18 | 0 | 0 | 0 | 6 of 6 | — |
| `fixtures-large-unset` | 18 | 0 | 0 | 0 | 6 of 6 | — |
| `fixtures-unset` | 252 | 32 | 4 | 0 | 24 of 24 | neo4j-graph layered-16384, neo4j-graph layered-65536, neo4j-graph path-16384, neo4j-graph path-65536 |
| `fixtures-xlarge-1` | 18 | 0 | 0 | 0 | 6 of 6 | — |
| `fixtures-xlarge-16` | 18 | 0 | 0 | 0 | 6 of 6 | — |
| `fixtures-xlarge-unset` | 18 | 0 | 0 | 0 | 6 of 6 | — |

3 parity invocations exited 1: `parity.py` exits 1 whenever any row mismatches, and the protocol fixture set always contains the four known `neo4j-graph` dangling-mass rows; the PageRank-only large sets contain none and exit 0. The driver takes its verdict from the file, not the exit code. 2 parity invocations are marked shared.

The `--bits-identical` gate names v0.22.0 and the three accounting modes. The `+eager` variant differs from `grust-next@counted` only in where the transpose is built, so its rows are compared with v0.22.0's in the same parity files after the fact: its PageRank digest and iteration count equal v0.22.0's in 36 of 36 rows.

### The allocator artifact, corrected

WCC and BFS read no in-arcs. B4 built the transpose for them anyway, inside the
build timer and immediately before the call it timed; `+eager` is that
behaviour, kept as its own row. The page-fault columns are the quantity the
artifact moved, so the correction can be read off the counter beside the time.

| fixture | algorithm | run | kernel | `grust` v0.22.0 | faults | `grust-next` | faults | `grust-next` `+eager` | faults | next/v0.22.0 | eager/next |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `hub-16384` | wcc | one-thread | concurrency 1 | 1.54 ± 0.01 | 33 | 1.48 ± 0.01 | 32 | 1.48 ± 0.00 | 32 | -3.9% | -0.2% |
| `hub-16384` | wcc | one-thread | concurrency unset | 4.14 ± 0.00 | 33 | 4.09 ± 0.00 | 32 | 4.09 ± 0.00 | 32 | -1.2% | +0.0% |
| `hub-16384` | bfs | one-thread | concurrency 1 | 1.52 ± 0.01 | 36 | 1.53 ± 0.00 | 32 | 1.54 ± 0.01 | 32 | +0.9% | +1.0% |
| `hub-16384` | bfs | one-thread | concurrency unset | 1.51 ± 0.01 | 36 | 1.55 ± 0.00 | 36 | 1.59 ± 0.01 | 64 | +2.6% | +2.4% |
| `hub-65536` | wcc | one-thread | concurrency 1 | 6.66 ± 0.01 | 128 | 6.46 ± 0.04 | 128 | 6.54 ± 0.03 | 128 | -3.0% | +1.3% |
| `hub-65536` | wcc | one-thread | concurrency unset | 16.88 ± 0.01 | 128 | 16.67 ± 0.01 | 128 | 16.68 ± 0.03 | 128 | -1.3% | +0.1% |
| `hub-65536` | bfs | one-thread | concurrency 1 | 5.90 ± 0.02 | 146 | 6.25 ± 0.07 | 130 | 6.07 ± 0.00 | 194 | +6.0% | -2.9% |
| `hub-65536` | bfs | one-thread | concurrency unset | 6.97 ± 0.13 | 144 | 7.40 ± 0.06 | 144 | 7.17 ± 0.05 | 256 | +6.1% | -3.0% |
| `layered-16384` | wcc | one-thread | concurrency 1 | 0.62 ± 0.01 | 32 | 0.69 ± 0.01 | 32 | 0.67 ± 0.01 | 32 | +10.1% | -2.8% |
| `layered-16384` | wcc | one-thread | concurrency unset | 1.43 ± 0.01 | 32 | 1.41 ± 0.00 | 32 | 1.42 ± 0.02 | 32 | -1.3% | +0.8% |
| `layered-16384` | bfs | one-thread | concurrency 1 | 0.45 ± 0.01 | 30 | 0.44 ± 0.01 | 26 | 0.44 ± 0.00 | 26 | -0.8% | -1.3% |
| `layered-16384` | bfs | one-thread | concurrency unset | 0.45 ± 0.00 | 30 | 0.44 ± 0.00 | 30 | 0.49 ± 0.01 | 58 | -3.9% | +13.2% |
| `layered-65536` | wcc | one-thread | concurrency 1 | 2.50 ± 0.01 | 128 | 2.78 ± 0.00 | 128 | 2.76 ± 0.02 | 128 | +11.0% | -0.5% |
| `layered-65536` | wcc | one-thread | concurrency unset | 5.74 ± 0.01 | 128 | 5.72 ± 0.00 | 128 | 5.72 ± 0.00 | 128 | -0.5% | +0.1% |
| `layered-65536` | bfs | one-thread | concurrency 1 | 1.83 ± 0.01 | 119 | 1.79 ± 0.01 | 103 | 1.78 ± 0.01 | 103 | -2.1% | -0.8% |
| `layered-65536` | bfs | one-thread | concurrency unset | 1.84 ± 0.02 | 119 | 1.82 ± 0.01 | 119 | 2.04 ± 0.00 | 231 | -1.0% | +11.8% |
| `path-16384` | wcc | one-thread | concurrency 1 | 0.43 ± 0.01 | 32 | 0.45 ± 0.01 | 32 | 0.44 ± 0.01 | 32 | +4.2% | -1.8% |
| `path-16384` | wcc | one-thread | concurrency unset | 0.99 ± 0.01 | 32 | 0.97 ± 0.00 | 32 | 0.98 ± 0.00 | 32 | -2.7% | +2.0% |
| `path-16384` | bfs | one-thread | concurrency 1 | 0.42 ± 0.00 | 36 | 0.38 ± 0.00 | 32 | 0.38 ± 0.00 | 32 | -9.2% | -1.4% |
| `path-16384` | bfs | one-thread | concurrency unset | 0.41 ± 0.01 | 37 | 0.38 ± 0.00 | 36 | 0.46 ± 0.00 | 64 | -6.4% | +20.0% |
| `path-65536` | wcc | one-thread | concurrency 1 | 1.77 ± 0.00 | 128 | 1.79 ± 0.01 | 128 | 1.81 ± 0.02 | 128 | +0.9% | +1.2% |
| `path-65536` | wcc | one-thread | concurrency unset | 3.98 ± 0.01 | 128 | 3.96 ± 0.01 | 128 | 3.97 ± 0.01 | 128 | -0.6% | +0.2% |
| `path-65536` | bfs | one-thread | concurrency 1 | 1.68 ± 0.01 | 144 | 1.58 ± 0.03 | 128 | 1.57 ± 0.00 | 128 | -5.8% | -0.5% |
| `path-65536` | bfs | one-thread | concurrency unset | 1.68 ± 0.01 | 144 | 1.64 ± 0.01 | 144 | 1.84 ± 0.01 | 256 | -2.5% | +12.5% |
| `uniform-16384` | wcc | one-thread | concurrency 1 | 2.04 ± 0.00 | 32 | 2.32 ± 0.01 | 32 | 2.32 ± 0.01 | 32 | +13.6% | +0.1% |
| `uniform-16384` | wcc | one-thread | concurrency unset | 4.15 ± 0.00 | 32 | 4.09 ± 0.00 | 32 | 4.10 ± 0.00 | 32 | -1.2% | +0.0% |
| `uniform-16384` | bfs | one-thread | concurrency 1 | 1.58 ± 0.01 | 36 | 1.59 ± 0.01 | 32 | 1.60 ± 0.03 | 32 | +1.0% | +0.2% |
| `uniform-16384` | bfs | one-thread | concurrency unset | 1.57 ± 0.01 | 36 | 1.62 ± 0.00 | 36 | 1.65 ± 0.03 | 64 | +2.8% | +2.3% |
| `uniform-65536` | wcc | one-thread | concurrency 1 | 8.88 ± 0.05 | 128 | 9.81 ± 0.03 | 128 | 9.91 ± 0.06 | 128 | +10.5% | +1.0% |
| `uniform-65536` | wcc | one-thread | concurrency unset | 17.08 ± 0.05 | 128 | 16.96 ± 0.03 | 128 | 17.04 ± 0.02 | 128 | -0.7% | +0.5% |
| `uniform-65536` | bfs | one-thread | concurrency 1 | 6.39 ± 0.05 | 210 | 6.63 ± 0.04 | 134 | 6.22 ± 0.05 | 198 | +3.8% | -6.2% |
| `uniform-65536` | bfs | one-thread | concurrency unset | 7.06 ± 0.11 | 144 | 7.54 ± 0.04 | 144 | 7.32 ± 0.09 | 256 | +6.7% | -2.9% |
| `hub-16384` | wcc | full-width | concurrency as the run | 1.20 ± 0.04 | 141 | 0.49 ± 0.01 | 4 | 0.45 ± 0.01 | 2 | -59.4% | -7.5% |
| `hub-16384` | bfs | full-width | concurrency as the run | 1.52 ± 0.00 | 36 | 1.54 ± 0.01 | 0 | 1.47 ± 0.01 | 0 | +1.4% | -4.7% |
| `hub-65536` | wcc | full-width | concurrency as the run | 2.38 ± 0.03 | 239 | 1.48 ± 0.05 | 6 | 1.50 ± 0.05 | 3 | -38.0% | +1.5% |
| `hub-65536` | bfs | full-width | concurrency as the run | 4.07 ± 0.08 | 390 | 3.17 ± 0.01 | 131 | 3.01 ± 0.02 | 119 | -22.0% | -5.1% |
| `layered-16384` | wcc | full-width | concurrency as the run | 0.98 ± 0.02 | 140 | 0.38 ± 0.02 | 35 | 0.31 ± 0.00 | 34 | -61.3% | -17.9% |
| `layered-16384` | bfs | full-width | concurrency as the run | 0.45 ± 0.00 | 30 | 0.46 ± 0.00 | 26 | 0.45 ± 0.00 | 26 | +0.3% | -1.0% |
| `layered-65536` | wcc | full-width | concurrency as the run | 1.51 ± 0.01 | 239 | 0.89 ± 0.01 | 133 | 0.86 ± 0.01 | 132 | -40.8% | -3.3% |
| `layered-65536` | bfs | full-width | concurrency as the run | 1.84 ± 0.01 | 119 | 1.85 ± 0.03 | 103 | 1.84 ± 0.04 | 102 | +0.6% | -0.6% |
| `path-16384` | wcc | full-width | concurrency as the run | 0.93 ± 0.07 | 137 | 0.47 ± 0.02 | 35 | 0.41 ± 0.02 | 35 | -49.4% | -12.8% |
| `path-16384` | bfs | full-width | concurrency as the run | 0.42 ± 0.00 | 36 | 0.41 ± 0.00 | 32 | 0.40 ± 0.01 | 32 | -2.4% | -1.5% |
| `path-65536` | wcc | full-width | concurrency as the run | 1.43 ± 0.01 | 238 | 1.04 ± 0.04 | 133 | 1.23 ± 0.03 | 133 | -26.8% | +17.7% |
| `path-65536` | bfs | full-width | concurrency as the run | 1.69 ± 0.01 | 144 | 1.63 ± 0.02 | 128 | 1.62 ± 0.02 | 128 | -3.4% | -0.3% |
| `uniform-16384` | wcc | full-width | concurrency as the run | 1.32 ± 0.03 | 142 | 0.57 ± 0.01 | 3 | 0.51 ± 0.03 | 3 | -56.4% | -11.1% |
| `uniform-16384` | bfs | full-width | concurrency as the run | 1.56 ± 0.00 | 36 | 1.71 ± 0.02 | 0 | 1.53 ± 0.01 | 0 | +9.4% | -10.2% |
| `uniform-65536` | wcc | full-width | concurrency as the run | 2.71 ± 0.16 | 241 | 1.80 ± 0.06 | 4 | 1.65 ± 0.04 | 4 | -33.7% | -8.2% |
| `uniform-65536` | bfs | full-width | concurrency as the run | 4.20 ± 0.04 | 367 | 3.27 ± 0.08 | 118 | 3.16 ± 0.01 | 123 | -22.2% | -3.4% |

Across the 48 WCC and BFS first-call cells at the protocol sizes, the corrected `grust-next` takes a median of -2 minor page faults against v0.22.0 and the `+eager` row a median of +0 against the corrected one; `+eager` is slower than the corrected row in 22 of 48 of them, by a median of -0.4%.

### The allocator pinned, for every participant

`GLIBC_TUNABLES=glibc.malloc.mmap_threshold=131072` set for the whole
container, so every participant in the run has it. First call, at the protocol
size, against the same cell of the same run unpinned.

| fixture | algorithm | run | participant | default allocator | faults | pinned | faults | pinned/default |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `hub-65536` | pagerank | one-thread | `neo4j-graph` | 35.93 ± 0.14 | 70 | 36.03 ± 0.13 | 137 | +0.3% |
| `hub-65536` | pagerank | one-thread | `icebug` | 42.13 ± 0.80 | 400 | 43.07 ± 0.80 | 400 | +2.2% |
| `hub-65536` | pagerank | one-thread | `icecat` | 34.12 ± 0.01 | 607 | 34.66 ± 0.05 | 902 | +1.6% |
| `hub-65536` | pagerank | one-thread | `grustcat` | 30.23 ± 0.03 | 0 | 30.56 ± 0.09 | 387 | +1.1% |
| `hub-65536` | pagerank | one-thread | `grust#1` | 52.59 ± 0.21 | 1024 | 53.30 ± 0.05 | 647 | +1.4% |
| `hub-65536` | pagerank | one-thread | `grust#unset` | 203.55 ± 0.34 | 512 | 204.43 ± 0.20 | 645 | +0.4% |
| `hub-65536` | pagerank | one-thread | `grust-next@counted#1` | 34.02 ± 0.13 | 384 | 34.52 ± 0.33 | 516 | +1.5% |
| `hub-65536` | pagerank | one-thread | `grust-next@counted#unset` | 95.14 ± 0.47 | 512 | 95.38 ± 0.69 | 645 | +0.3% |
| `hub-65536` | wcc | one-thread | `neo4j-graph` | 3.75 ± 0.01 | 32 | 4.48 ± 0.01 | 393 | +19.4% |
| `hub-65536` | wcc | one-thread | `icebug` | 11.25 ± 0.41 | 239 | 11.36 ± 0.06 | 240 | +1.0% |
| `hub-65536` | wcc | one-thread | `icecat` | 3.48 ± 0.22 | 127 | 3.73 ± 0.01 | 258 | +7.1% |
| `hub-65536` | wcc | one-thread | `grustcat` | 2.44 ± 0.01 | 0 | 2.46 ± 0.02 | 0 | +0.8% |
| `hub-65536` | wcc | one-thread | `grust#1` | 6.66 ± 0.01 | 128 | 6.84 ± 0.02 | 258 | +2.6% |
| `hub-65536` | wcc | one-thread | `grust#unset` | 16.88 ± 0.01 | 128 | 17.10 ± 0.01 | 258 | +1.3% |
| `hub-65536` | wcc | one-thread | `grust-next@counted#1` | 6.46 ± 0.04 | 128 | 6.72 ± 0.01 | 258 | +4.1% |
| `hub-65536` | wcc | one-thread | `grust-next@counted#unset` | 16.67 ± 0.01 | 128 | 16.97 ± 0.00 | 258 | +1.8% |
| `hub-65536` | bfs | one-thread | `icebug` | 8.41 ± 0.23 | 216 | 8.45 ± 0.07 | 216 | +0.5% |
| `hub-65536` | bfs | one-thread | `icecat` | 4.37 ± 0.01 | 385 | 4.50 ± 0.03 | 388 | +3.0% |
| `hub-65536` | bfs | one-thread | `grustcat` | 4.06 ± 0.13 | 1 | 4.61 ± 0.20 | 129 | +13.7% |
| `hub-65536` | bfs | one-thread | `grust#1` | 5.90 ± 0.02 | 146 | 6.28 ± 0.08 | 420 | +6.5% |
| `hub-65536` | bfs | one-thread | `grust#unset` | 6.97 ± 0.13 | 144 | 6.99 ± 0.06 | 274 | +0.2% |
| `hub-65536` | bfs | one-thread | `grust-next@counted#1` | 6.25 ± 0.07 | 130 | 6.59 ± 0.04 | 435 | +5.5% |
| `hub-65536` | bfs | one-thread | `grust-next@counted#unset` | 7.40 ± 0.06 | 144 | 7.27 ± 0.08 | 258 | -1.6% |
| `hub-65536` | triangles | one-thread | `neo4j-graph` | 35.34 ± 0.15 | 4 | 35.09 ± 0.16 | 4 | -0.7% |
| `hub-65536` | triangles | one-thread | `grust#1` | 74.25 ± 0.24 | 1665 | 73.73 ± 0.71 | 1290 | -0.7% |
| `hub-65536` | triangles | one-thread | `grust#unset` | 73.80 ± 0.18 | 1665 | 73.37 ± 0.15 | 1290 | -0.6% |
| `hub-65536` | triangles | one-thread | `grust-next@counted#1` | 72.51 ± 0.02 | 1666 | 71.71 ± 0.34 | 1290 | -1.1% |
| `hub-65536` | triangles | one-thread | `grust-next@counted#unset` | 72.29 ± 0.06 | 1666 | 71.81 ± 0.27 | 1290 | -0.7% |
| `uniform-65536` | pagerank | one-thread | `neo4j-graph` | 44.24 ± 0.08 | 71 | 43.99 ± 0.03 | 138 | -0.6% |
| `uniform-65536` | pagerank | one-thread | `icebug` | 39.50 ± 0.78 | 398 | 38.97 ± 0.24 | 398 | -1.3% |
| `uniform-65536` | pagerank | one-thread | `icecat` | 32.69 ± 0.02 | 607 | 32.83 ± 0.06 | 902 | +0.4% |
| `uniform-65536` | pagerank | one-thread | `grustcat` | 29.27 ± 0.12 | 0 | 28.85 ± 0.10 | 0 | -1.4% |
| `uniform-65536` | pagerank | one-thread | `grust#1` | 51.51 ± 0.43 | 1025 | 50.34 ± 0.13 | 647 | -2.3% |
| `uniform-65536` | pagerank | one-thread | `grust#unset` | 192.34 ± 0.36 | 512 | 192.56 ± 0.26 | 645 | +0.1% |
| `uniform-65536` | pagerank | one-thread | `grust-next@counted#1` | 32.48 ± 0.20 | 384 | 32.18 ± 0.39 | 516 | -0.9% |
| `uniform-65536` | pagerank | one-thread | `grust-next@counted#unset` | 88.77 ± 0.68 | 512 | 89.06 ± 0.28 | 645 | +0.3% |
| `uniform-65536` | wcc | one-thread | `neo4j-graph` | 3.75 ± 0.00 | 32 | 4.49 ± 0.02 | 393 | +19.7% |
| `uniform-65536` | wcc | one-thread | `icebug` | 12.83 ± 0.08 | 244 | 12.81 ± 0.26 | 243 | -0.1% |
| `uniform-65536` | wcc | one-thread | `icecat` | 4.02 ± 0.07 | 35 | 4.34 ± 0.01 | 259 | +7.9% |
| `uniform-65536` | wcc | one-thread | `grustcat` | 3.05 ± 0.04 | 0 | 3.06 ± 0.01 | 0 | +0.5% |
| `uniform-65536` | wcc | one-thread | `grust#1` | 8.88 ± 0.05 | 128 | 8.87 ± 0.02 | 258 | -0.0% |
| `uniform-65536` | wcc | one-thread | `grust#unset` | 17.08 ± 0.05 | 128 | 17.29 ± 0.06 | 258 | +1.3% |
| `uniform-65536` | wcc | one-thread | `grust-next@counted#1` | 9.81 ± 0.03 | 128 | 10.03 ± 0.04 | 258 | +2.3% |
| `uniform-65536` | wcc | one-thread | `grust-next@counted#unset` | 16.96 ± 0.03 | 128 | 17.33 ± 0.04 | 258 | +2.2% |
| `uniform-65536` | bfs | one-thread | `icebug` | 8.43 ± 0.14 | 216 | 8.34 ± 0.11 | 217 | -1.1% |
| `uniform-65536` | bfs | one-thread | `icecat` | 3.93 ± 0.04 | 180 | 4.20 ± 0.03 | 386 | +6.8% |
| `uniform-65536` | bfs | one-thread | `grustcat` | 4.36 ± 0.12 | 0 | 4.43 ± 0.04 | 0 | +1.7% |
| `uniform-65536` | bfs | one-thread | `grust#1` | 6.39 ± 0.05 | 210 | 6.40 ± 0.06 | 428 | +0.2% |
| `uniform-65536` | bfs | one-thread | `grust#unset` | 7.06 ± 0.11 | 144 | 6.93 ± 0.03 | 273 | -1.9% |
| `uniform-65536` | bfs | one-thread | `grust-next@counted#1` | 6.63 ± 0.04 | 134 | 6.71 ± 0.05 | 420 | +1.3% |
| `uniform-65536` | bfs | one-thread | `grust-next@counted#unset` | 7.54 ± 0.04 | 144 | 7.17 ± 0.03 | 257 | -4.9% |
| `uniform-65536` | triangles | one-thread | `neo4j-graph` | 39.47 ± 0.14 | 4 | 39.25 ± 0.06 | 4 | -0.5% |
| `uniform-65536` | triangles | one-thread | `grust#1` | 80.93 ± 0.52 | 1668 | 78.90 ± 0.04 | 780 | -2.5% |
| `uniform-65536` | triangles | one-thread | `grust#unset` | 81.49 ± 0.35 | 1668 | 78.91 ± 0.02 | 780 | -3.2% |
| `uniform-65536` | triangles | one-thread | `grust-next@counted#1` | 78.55 ± 1.00 | 1157 | 77.41 ± 0.12 | 780 | -1.5% |
| `uniform-65536` | triangles | one-thread | `grust-next@counted#unset` | 78.43 ± 0.03 | 1157 | 77.30 ± 0.06 | 780 | -1.4% |
| `hub-65536` | pagerank | full-width | `neo4j-graph` | 15.03 ± 0.04 | 94 | 15.21 ± 0.04 | 170 | +1.2% |
| `hub-65536` | pagerank | full-width | `icebug` | 7.45 ± 0.04 | 502 | 7.45 ± 0.04 | 487 | -0.0% |
| `hub-65536` | pagerank | full-width | `icecat` | 34.07 ± 0.07 | 608 | 34.60 ± 0.01 | 901 | +1.5% |
| `hub-65536` | pagerank | full-width | `grustcat` | 30.28 ± 0.22 | 0 | 30.53 ± 0.08 | 387 | +0.8% |
| `hub-65536` | pagerank | full-width | `grust` | 17.79 ± 0.26 | 1133 | 16.97 ± 0.12 | 771 | -4.6% |
| `hub-65536` | pagerank | full-width | `grust-next@counted` | 7.22 ± 0.04 | 13 | 8.30 ± 0.12 | 533 | +15.0% |
| `hub-65536` | wcc | full-width | `neo4j-graph` | 3.18 ± 0.05 | 226 | 3.37 ± 0.09 | 415 | +6.2% |
| `hub-65536` | wcc | full-width | `icebug` | 11.21 ± 0.09 | 239 | 11.04 ± 0.22 | 239 | -1.5% |
| `hub-65536` | wcc | full-width | `icecat` | 3.71 ± 0.02 | 256 | 3.74 ± 0.01 | 259 | +0.7% |
| `hub-65536` | wcc | full-width | `grustcat` | 2.46 ± 0.01 | 0 | 2.44 ± 0.00 | 0 | -0.8% |
| `hub-65536` | wcc | full-width | `grust` | 2.38 ± 0.03 | 239 | 2.66 ± 0.05 | 368 | +11.3% |
| `hub-65536` | wcc | full-width | `grust-next@counted` | 1.48 ± 0.05 | 6 | 2.12 ± 0.03 | 261 | +43.8% |
| `hub-65536` | bfs | full-width | `icebug` | 8.41 ± 0.05 | 216 | 8.38 ± 0.06 | 216 | -0.4% |
| `hub-65536` | bfs | full-width | `icecat` | 3.79 ± 0.03 | 109 | 4.39 ± 0.10 | 388 | +15.8% |
| `hub-65536` | bfs | full-width | `grustcat` | 3.98 ± 0.08 | 0 | 4.62 ± 0.04 | 129 | +16.0% |
| `hub-65536` | bfs | full-width | `grust` | 4.07 ± 0.08 | 390 | 4.73 ± 0.08 | 598 | +16.3% |
| `hub-65536` | bfs | full-width | `grust-next@counted` | 3.17 ± 0.01 | 131 | 3.82 ± 0.06 | 414 | +20.5% |
| `hub-65536` | triangles | full-width | `neo4j-graph` | 3.50 ± 0.05 | 52 | 3.56 ± 0.05 | 52 | +1.6% |
| `hub-65536` | triangles | full-width | `grust` | 31.16 ± 0.11 | 1768 | 30.92 ± 0.18 | 1393 | -0.8% |
| `hub-65536` | triangles | full-width | `grust-next@counted` | 28.78 ± 0.09 | 1026 | 29.61 ± 0.06 | 1290 | +2.9% |
| `uniform-65536` | pagerank | full-width | `neo4j-graph` | 16.30 ± 0.28 | 94 | 16.09 ± 0.10 | 173 | -1.3% |
| `uniform-65536` | pagerank | full-width | `icebug` | 7.37 ± 0.06 | 488 | 7.14 ± 0.12 | 489 | -3.2% |
| `uniform-65536` | pagerank | full-width | `icecat` | 32.72 ± 0.05 | 606 | 32.90 ± 0.11 | 902 | +0.6% |
| `uniform-65536` | pagerank | full-width | `grustcat` | 29.50 ± 0.10 | 0 | 29.02 ± 0.06 | 0 | -1.6% |
| `uniform-65536` | pagerank | full-width | `grust` | 17.41 ± 0.34 | 1134 | 16.80 ± 0.19 | 771 | -3.5% |
| `uniform-65536` | pagerank | full-width | `grust-next@counted` | 7.01 ± 0.16 | 12 | 7.85 ± 0.12 | 531 | +12.1% |
| `uniform-65536` | wcc | full-width | `neo4j-graph` | 3.08 ± 0.13 | 228 | 3.88 ± 0.06 | 413 | +26.1% |
| `uniform-65536` | wcc | full-width | `icebug` | 13.06 ± 0.11 | 244 | 12.82 ± 0.07 | 243 | -1.8% |
| `uniform-65536` | wcc | full-width | `icecat` | 3.96 ± 0.01 | 3 | 4.35 ± 0.01 | 258 | +9.9% |
| `uniform-65536` | wcc | full-width | `grustcat` | 3.08 ± 0.02 | 0 | 3.07 ± 0.01 | 0 | -0.3% |
| `uniform-65536` | wcc | full-width | `grust` | 2.71 ± 0.16 | 241 | 2.96 ± 0.08 | 370 | +9.3% |
| `uniform-65536` | wcc | full-width | `grust-next@counted` | 1.80 ± 0.06 | 4 | 2.37 ± 0.08 | 262 | +31.8% |
| `uniform-65536` | bfs | full-width | `icebug` | 8.58 ± 0.26 | 216 | 8.58 ± 0.05 | 216 | +0.1% |
| `uniform-65536` | bfs | full-width | `icecat` | 4.03 ± 0.30 | 253 | 4.26 ± 0.02 | 386 | +5.7% |
| `uniform-65536` | bfs | full-width | `grustcat` | 4.35 ± 0.08 | 0 | 4.38 ± 0.05 | 0 | +0.6% |
| `uniform-65536` | bfs | full-width | `grust` | 4.20 ± 0.04 | 367 | 4.75 ± 0.07 | 556 | +13.0% |
| `uniform-65536` | bfs | full-width | `grust-next@counted` | 3.27 ± 0.08 | 118 | 4.03 ± 0.04 | 453 | +23.1% |
| `uniform-65536` | triangles | full-width | `neo4j-graph` | 3.99 ± 0.04 | 51 | 3.77 ± 0.03 | 55 | -5.6% |
| `uniform-65536` | triangles | full-width | `grust` | 32.54 ± 0.32 | 1770 | 31.27 ± 0.05 | 882 | -3.9% |
| `uniform-65536` | triangles | full-width | `grust-next@counted` | 29.06 ± 0.08 | 517 | 29.74 ± 0.09 | 780 | +2.4% |

Median change under pinning, per participant: `grust` +0.1% over 24 cells; `grust-next` +2.0% over 24 cells; `grustcat` +0.7% over 12 cells; `icebug` -0.2% over 12 cells; `icecat` +4.4% over 12 cells; `neo4j-graph` +0.7% over 12 cells.

**The decision, by the rule fixed before the runs.** Over the same 48 WCC and BFS first-call cells, the median difference in minor page faults between v0.22.0 and the corrected `grust-next` is 2, against the 25 that the rule set as the line and the 112 to 128 the attribution measured for the artifact itself. The two builds are therefore in the same allocator state on the same cell, and the published tables are the default-allocator runs: glibc's default is what every participant's users have, and none of these projects sets a tunable. The pinned runs above stay as a labelled probe, and they also show that the threshold is not a Grust-specific effect — it moves participants that contain no Grust at all.

### The transpose, on the build side

One thread, pull kernel (concurrency 1), PageRank — the one kernel here that
reads in-arcs, and so the one whose build column contains them. "First" is a
fresh projection's first kernel call; on v0.22.0 it includes building the
transpose. "Second" repeats it with the transpose cached and on warm caches,
which is not the condition of any other participant's timed call.

| fixture | `grust` v0.22.0 first | `grust` v0.22.0 second | `grust-next` counted first | transpose, in `build_ms` | `grustcat` | steal |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `hub-65536` | 52.59 ± 0.21 | 44.00 ± 0.17 | 34.02 ± 0.13 | 6.41 | 30.23 ± 0.03 | 0 |
| `uniform-65536` | 51.51 ± 0.43 | 42.87 ± 0.33 | 32.48 ± 0.20 | 6.36 | 29.27 ± 0.12 | 0 |
| `hub-2097152` | 4987.08 ± 70.65 | 4398.60 ± 71.31 | 2170.69 ± 43.13 | 552.73 | 1946.08 ± 46.23 | 3 |
| `uniform-2097152` | 5186.50 ± 59.96 | 4575.57 ± 48.02 | 2207.80 ± 62.26 | 529.75 | 2399.05 ± 35.57 | 4 |
| `hub-4194304` | 12663.28 ± 36.71 | 11300.51 ± 50.55 | 6941.34 ± 23.40 | 1184.65 | 6040.22 ± 40.65 | 121 |
| `uniform-4194304` | 13286.45 ± 45.87 | 11878.26 ± 54.01 | 7030.83 ± 59.57 | 1173.68 | 7113.24 ± 94.56 | 8 |

### The kernel change, v0.22.0 against the commit under test

Same mode (counted), same concurrency, second call against second call, so the
transpose is cached on both sides. Both builds return the same scores bit for
bit, which parity checked on every fixture at every concurrency.

| fixture | run | kernel | v0.22.0 | `ca68900` | ratio | steal |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `hub-16384` | one-thread | pull | 9.60 ± 0.01 | 7.98 ± 0.00 | 0.831 | 0 |
| `hub-16384` | one-thread | push | 50.40 ± 0.01 | 23.16 ± 0.04 | 0.460 | 0 |
| `hub-65536` | one-thread | pull | 44.00 ± 0.17 | 33.20 ± 0.10 | 0.755 | 0 |
| `hub-65536` | one-thread | push | 202.19 ± 0.14 | 95.60 ± 0.56 | 0.473 | 0 |
| `uniform-16384` | one-thread | pull | 9.20 ± 0.00 | 7.54 ± 0.02 | 0.819 | 0 |
| `uniform-16384` | one-thread | push | 47.73 ± 0.01 | 21.50 ± 0.01 | 0.450 | 0 |
| `uniform-65536` | one-thread | pull | 42.87 ± 0.33 | 31.61 ± 0.25 | 0.737 | 0 |
| `uniform-65536` | one-thread | push | 191.54 ± 0.13 | 88.63 ± 0.72 | 0.463 | 0 |
| `hub-16384` | full-width | pull | 3.46 ± 0.02 | 3.29 ± 0.01 | 0.951 | 0 |
| `hub-65536` | full-width | pull | 8.71 ± 0.14 | 7.10 ± 0.06 | 0.816 | 0 |
| `uniform-16384` | full-width | pull | 3.30 ± 0.07 | 3.39 ± 0.25 | 1.027 | 0 |
| `uniform-65536` | full-width | pull | 8.16 ± 0.07 | 6.68 ± 0.10 | 0.819 | 0 |
| `hub-2097152` | large-one-thread | pull | 4398.60 ± 71.31 | 1935.33 ± 23.39 | 0.440 | 3 |
| `hub-2097152` | large-one-thread | push | 7772.38 ± 75.86 | 4115.77 ± 46.30 | 0.530 | 3 |
| `uniform-2097152` | large-one-thread | pull | 4575.57 ± 48.02 | 2010.09 ± 52.55 | 0.439 | 4 |
| `uniform-2097152` | large-one-thread | push | 7545.63 ± 82.12 | 4300.81 ± 153.48 | 0.570 | 4 |
| `hub-2097152` | large-full-width | pull | 502.37 ± 9.55 | 233.44 ± 1.37 | 0.465 | 1 |
| `uniform-2097152` | large-full-width | pull | 548.05 ± 17.24 | 253.45 ± 9.76 | 0.462 | 2 |
| `hub-4194304` | xlarge-one-thread | pull | 11300.51 ± 50.55 | 6969.36 ± 27.73 | 0.617 | 121 |
| `hub-4194304` | xlarge-one-thread | push | 26010.01 ± 279.41 | 12936.74 ± 26.41 | 0.497 | 121 |
| `uniform-4194304` | xlarge-one-thread | pull | 11878.26 ± 54.01 | 7036.39 ± 65.96 | 0.592 | 8 |
| `uniform-4194304` | xlarge-one-thread | push | 24393.09 ± 778.50 | 12394.91 ± 269.46 | 0.508 | 8 |
| `hub-4194304` | xlarge-full-width | pull | 1347.79 ± 3.82 | 710.51 ± 15.55 | 0.527 | 4 |
| `uniform-4194304` | xlarge-full-width | pull | 1446.17 ± 3.87 | 750.56 ± 21.85 | 0.519 | 3 |

### Every cell that got worse

Counted `grust-next` against v0.22.0, same fixture, algorithm, kernel and call.
70 of the 216 counted cells with a v0.22.0 counterpart are slower on `ca68900`, by +0.0% to +117.4%.

| fixture | algorithm | run | kernel | call | v0.22.0 | faults | `ca68900` | faults | change | steal |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `hub-16384` | bfs | full-width | concurrency as the run | first | 1.52 ± 0.00 | 36 | 1.54 ± 0.01 | 0 | +1.4% | 0 |
| `hub-16384` | bfs | full-width | concurrency as the run | second | 1.47 ± 0.01 | 0 | 1.47 ± 0.01 | 0 | +0.3% | 0 |
| `hub-16384` | triangles | full-width | concurrency as the run | second | 6.19 ± 0.03 | 2 | 7.05 ± 0.02 | 512 | +13.9% | 0 |
| `hub-65536` | triangles | full-width | concurrency as the run | second | 25.06 ± 0.04 | 1 | 26.36 ± 0.15 | 1025 | +5.2% | 0 |
| `layered-16384` | bfs | full-width | concurrency as the run | first | 0.45 ± 0.00 | 30 | 0.46 ± 0.00 | 26 | +0.3% | 0 |
| `layered-16384` | pagerank | full-width | pull | second | 13.37 ± 0.18 | 0 | 14.14 ± 0.19 | 0 | +5.8% | 0 |
| `layered-16384` | triangles | full-width | concurrency as the run | second | 1.66 ± 0.01 | 1 | 2.14 ± 0.03 | 318 | +29.2% | 0 |
| `layered-16384` | wcc | full-width | concurrency as the run | second | 0.33 ± 0.00 | 32 | 0.34 ± 0.01 | 30 | +2.0% | 0 |
| `layered-65536` | bfs | full-width | concurrency as the run | first | 1.84 ± 0.01 | 119 | 1.85 ± 0.03 | 103 | +0.6% | 0 |
| `layered-65536` | triangles | full-width | concurrency as the run | second | 6.41 ± 0.02 | 2 | 7.07 ± 0.08 | 508 | +10.2% | 0 |
| `layered-65536` | wcc | full-width | concurrency as the run | second | 0.84 ± 0.01 | 129 | 0.84 ± 0.02 | 125 | +0.8% | 0 |
| `path-16384` | pagerank | full-width | pull | first | 10.44 ± 0.17 | 262 | 15.45 ± 0.69 | 108 | +47.9% | 0 |
| `path-16384` | pagerank | full-width | pull | second | 8.65 ± 0.12 | 0 | 16.14 ± 0.36 | 64 | +86.6% | 0 |
| `path-16384` | triangles | full-width | concurrency as the run | second | 0.94 ± 0.01 | 1 | 1.44 ± 0.01 | 256 | +53.6% | 0 |
| `path-16384` | wcc | full-width | concurrency as the run | second | 0.29 ± 0.01 | 33 | 0.41 ± 0.03 | 17 | +40.0% | 0 |
| `path-65536` | pagerank | full-width | pull | first | 16.31 ± 0.02 | 754 | 26.27 ± 2.31 | 401 | +61.1% | 0 |
| `path-65536` | pagerank | full-width | pull | second | 12.24 ± 0.22 | 2 | 26.62 ± 0.47 | 355 | +117.4% | 0 |
| `path-65536` | triangles | full-width | concurrency as the run | second | 3.53 ± 0.03 | 1 | 5.80 ± 0.06 | 1120 | +64.2% | 0 |
| `path-65536` | wcc | full-width | concurrency as the run | second | 0.76 ± 0.00 | 133 | 0.81 ± 0.08 | 66 | +6.7% | 0 |
| `uniform-16384` | bfs | full-width | concurrency as the run | first | 1.56 ± 0.00 | 36 | 1.71 ± 0.02 | 0 | +9.4% | 0 |
| `uniform-16384` | bfs | full-width | concurrency as the run | second | 1.47 ± 0.00 | 0 | 1.51 ± 0.03 | 0 | +2.5% | 0 |
| `uniform-16384` | pagerank | full-width | pull | second | 3.30 ± 0.07 | 1 | 3.39 ± 0.25 | 0 | +2.7% | 0 |
| `uniform-16384` | triangles | full-width | concurrency as the run | second | 6.42 ± 0.03 | 1 | 7.27 ± 0.01 | 512 | +13.3% | 0 |
| `uniform-65536` | triangles | full-width | concurrency as the run | second | 26.15 ± 0.08 | 1 | 27.61 ± 0.16 | 1026 | +5.6% | 0 |
| `hub-16384` | bfs | one-thread | concurrency 1 | first | 1.52 ± 0.01 | 36 | 1.53 ± 0.00 | 32 | +0.9% | 0 |
| `hub-16384` | bfs | one-thread | concurrency unset | first | 1.51 ± 0.01 | 36 | 1.55 ± 0.00 | 36 | +2.6% | 0 |
| `hub-16384` | bfs | one-thread | concurrency 1 | second | 1.46 ± 0.03 | 0 | 1.46 ± 0.00 | 0 | +0.0% | 0 |
| `hub-16384` | bfs | one-thread | concurrency unset | second | 1.44 ± 0.01 | 0 | 1.44 ± 0.00 | 0 | +0.2% | 0 |
| `hub-16384` | triangles | one-thread | concurrency 1 | second | 15.58 ± 0.03 | 32 | 16.19 ± 0.05 | 511 | +3.9% | 0 |
| `hub-16384` | triangles | one-thread | concurrency unset | second | 15.56 ± 0.06 | 32 | 16.16 ± 0.08 | 543 | +3.8% | 0 |
| `hub-65536` | bfs | one-thread | concurrency 1 | first | 5.90 ± 0.02 | 146 | 6.25 ± 0.07 | 130 | +6.0% | 0 |
| `hub-65536` | bfs | one-thread | concurrency unset | first | 6.97 ± 0.13 | 144 | 7.40 ± 0.06 | 144 | +6.1% | 0 |
| `hub-65536` | bfs | one-thread | concurrency 1 | second | 5.29 ± 0.01 | 0 | 5.47 ± 0.06 | 0 | +3.4% | 0 |
| `hub-65536` | bfs | one-thread | concurrency unset | second | 6.26 ± 0.00 | 0 | 6.39 ± 0.01 | 0 | +2.1% | 0 |
| `hub-65536` | triangles | one-thread | concurrency 1 | second | 68.50 ± 0.39 | 128 | 70.27 ± 0.06 | 1535 | +2.6% | 0 |
| `hub-65536` | triangles | one-thread | concurrency unset | second | 68.51 ± 0.09 | 128 | 69.14 ± 0.73 | 1152 | +0.9% | 0 |
| `layered-16384` | pagerank | one-thread | pull | first | 30.17 ± 0.05 | 192 | 30.82 ± 0.07 | 96 | +2.2% | 0 |
| `layered-16384` | pagerank | one-thread | pull | second | 29.34 ± 0.08 | 0 | 30.53 ± 0.01 | 0 | +4.1% | 0 |
| `layered-16384` | triangles | one-thread | concurrency 1 | second | 2.18 ± 0.01 | 32 | 2.54 ± 0.01 | 350 | +16.3% | 0 |
| `layered-16384` | triangles | one-thread | concurrency unset | second | 2.19 ± 0.03 | 32 | 2.27 ± 0.01 | 159 | +3.9% | 0 |
| `layered-16384` | wcc | one-thread | concurrency 1 | first | 0.62 ± 0.01 | 32 | 0.69 ± 0.01 | 32 | +10.1% | 0 |
| `layered-65536` | pagerank | one-thread | pull | first | 108.55 ± 0.05 | 766 | 111.19 ± 0.09 | 384 | +2.4% | 0 |
| `layered-65536` | pagerank | one-thread | pull | second | 104.83 ± 0.08 | 0 | 110.15 ± 0.12 | 0 | +5.1% | 0 |
| `layered-65536` | triangles | one-thread | concurrency 1 | second | 8.79 ± 0.01 | 128 | 10.44 ± 0.04 | 1497 | +18.8% | 1 |
| `layered-65536` | triangles | one-thread | concurrency unset | second | 8.78 ± 0.00 | 128 | 9.18 ± 0.01 | 635 | +4.5% | 1 |
| `layered-65536` | wcc | one-thread | concurrency 1 | first | 2.50 ± 0.01 | 128 | 2.78 ± 0.00 | 128 | +11.0% | 0 |
| `path-16384` | triangles | one-thread | concurrency 1 | first | 1.52 ± 0.10 | 256 | 1.56 ± 0.05 | 256 | +2.7% | 0 |
| `path-16384` | triangles | one-thread | concurrency 1 | second | 1.08 ± 0.04 | 32 | 1.39 ± 0.02 | 256 | +28.2% | 0 |
| `path-16384` | wcc | one-thread | concurrency 1 | first | 0.43 ± 0.01 | 32 | 0.45 ± 0.01 | 32 | +4.2% | 0 |
| `path-16384` | wcc | one-thread | concurrency unset | second | 0.99 ± 0.02 | 30 | 1.00 ± 0.01 | 48 | +1.0% | 0 |
| `path-65536` | pagerank | one-thread | pull | second | 51.00 ± 0.10 | 0 | 51.76 ± 0.11 | 352 | +1.5% | 0 |
| `path-65536` | triangles | one-thread | concurrency 1 | first | 6.14 ± 0.03 | 1024 | 6.18 ± 0.02 | 1024 | +0.6% | 0 |
| `path-65536` | triangles | one-thread | concurrency unset | first | 6.18 ± 0.03 | 1024 | 6.21 ± 0.06 | 1024 | +0.6% | 0 |
| `path-65536` | triangles | one-thread | concurrency 1 | second | 4.32 ± 0.01 | 128 | 5.79 ± 0.03 | 1120 | +34.0% | 0 |
| `path-65536` | wcc | one-thread | concurrency 1 | first | 1.77 ± 0.00 | 128 | 1.79 ± 0.01 | 128 | +0.9% | 0 |
| `path-65536` | wcc | one-thread | concurrency unset | second | 3.97 ± 0.00 | 126 | 4.07 ± 0.01 | 192 | +2.4% | 0 |
| `uniform-16384` | bfs | one-thread | concurrency 1 | first | 1.58 ± 0.01 | 36 | 1.59 ± 0.01 | 32 | +1.0% | 0 |
| `uniform-16384` | bfs | one-thread | concurrency unset | first | 1.57 ± 0.01 | 36 | 1.62 ± 0.00 | 36 | +2.8% | 0 |
| `uniform-16384` | triangles | one-thread | concurrency 1 | second | 16.97 ± 0.04 | 32 | 17.66 ± 0.02 | 512 | +4.1% | 0 |
| `uniform-16384` | triangles | one-thread | concurrency unset | second | 17.02 ± 0.01 | 32 | 17.68 ± 0.03 | 544 | +3.9% | 0 |
| `uniform-16384` | wcc | one-thread | concurrency 1 | first | 2.04 ± 0.00 | 32 | 2.32 ± 0.01 | 32 | +13.6% | 0 |
| `uniform-16384` | wcc | one-thread | concurrency 1 | second | 2.26 ± 0.02 | 31 | 2.27 ± 0.01 | 15 | +0.5% | 0 |
| `uniform-65536` | bfs | one-thread | concurrency 1 | first | 6.39 ± 0.05 | 210 | 6.63 ± 0.04 | 134 | +3.8% | 0 |
| `uniform-65536` | bfs | one-thread | concurrency unset | first | 7.06 ± 0.11 | 144 | 7.54 ± 0.04 | 144 | +6.7% | 0 |
| `uniform-65536` | bfs | one-thread | concurrency 1 | second | 5.52 ± 0.01 | 0 | 5.60 ± 0.01 | 0 | +1.5% | 0 |
| `uniform-65536` | bfs | one-thread | concurrency unset | second | 6.37 ± 0.06 | 0 | 6.46 ± 0.02 | 0 | +1.4% | 0 |
| `uniform-65536` | triangles | one-thread | concurrency 1 | second | 75.73 ± 0.50 | 128 | 77.53 ± 0.31 | 1537 | +2.4% | 0 |
| `uniform-65536` | triangles | one-thread | concurrency unset | second | 76.01 ± 0.05 | 128 | 76.06 ± 0.36 | 1154 | +0.1% | 0 |
| `uniform-65536` | wcc | one-thread | concurrency 1 | first | 8.88 ± 0.05 | 128 | 9.81 ± 0.03 | 128 | +10.5% | 0 |
| `uniform-65536` | wcc | one-thread | concurrency 1 | second | 9.25 ± 0.02 | 128 | 9.61 ± 0.05 | 64 | +4.0% | 0 |

The largest of them: `path-65536` pagerank full-width pull second +117.4%; `path-16384` pagerank full-width pull second +86.6%; `path-65536` triangles full-width concurrency as the run second +64.2%; `path-65536` pagerank full-width pull first +61.1%; `path-16384` triangles full-width concurrency as the run second +53.6%.

Three shapes account for most of that list, and only one of them has a cause
here.

- **PageRank on the `path` family, and at full width above all.**
  5 of them are PageRank on the `path` family, +1.5% to +117.4%: `path-16384` full-width first 10.44 to 15.45 ms; `path-16384` full-width second 8.65 to 16.14 ms; `path-65536` full-width first 16.31 to 26.27 ms; `path-65536` full-width second 12.24 to 26.62 ms; `path-65536` one-thread second 51.00 to 51.76 ms. `path` is a chain, where the pull kernel's work per node is
  one arc and a parallel split has nothing to amortise; it is not a family this
  document publishes PageRank on,
  because `path` has a dangling node and `neo4j-graph` computes a different
  function there. It is timed, it got much worse, and **the cause is not
  established here.** A kernel that is faster on every `hub` and `uniform` cell
  at the same width and twice as slow on a chain is a finding about the shape
  of the graph, not a rounding.
- **The triangles second call.** 22 are the triangles second call, +0.1% to +64.2%, and every one of them takes more minor page faults than v0.22.0 did: a median of 32 faults on v0.22.0 against 544 on `ca68900`. v0.22.0's second triangle call allocates almost nothing and the later commit's allocates again, which is a change in what the second call does rather than in how fast it does it.
- **WCC's first call at concurrency 1.** WCC on the pull-side concurrency 1 first call is slower on 6 of 8 fixtures at one thread, -3.9% to +13.6%, with the page-fault counts equal on 7 of 8. Where the faults
  are equal it is not the allocator; the same cells at concurrency unset are
  not slower, and at full width the same kernel is far faster than v0.22.0.
  **Unexplained.**

Everything else in the table is within a few per cent, and the second-call
rows of PageRank — the comparison the kernel change is about — move the other
way by factors, not percentages.

### The two items the attribution left open

**Counted BFS on the first call.** B4 had it 8 to 11% slower than v0.22.0 on
`uniform` and `hub`. The last column is what the same cell said in B4.

| fixture | run | kernel | v0.22.0 | faults | `ca68900` | faults | change | B4 said |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `hub-16384` | one-thread | concurrency 1 | 1.52 ± 0.01 | 36 | 1.53 ± 0.00 | 32 | +0.9% | -1.1% |
| `hub-16384` | one-thread | concurrency unset | 1.51 ± 0.01 | 36 | 1.55 ± 0.00 | 36 | +2.6% | +0.6% |
| `hub-65536` | one-thread | concurrency 1 | 5.90 ± 0.02 | 146 | 6.25 ± 0.07 | 130 | +6.0% | +6.8% |
| `hub-65536` | one-thread | concurrency unset | 6.97 ± 0.13 | 144 | 7.40 ± 0.06 | 144 | +6.1% | +5.7% |
| `uniform-16384` | one-thread | concurrency 1 | 1.58 ± 0.01 | 36 | 1.59 ± 0.01 | 32 | +1.0% | -4.0% |
| `uniform-16384` | one-thread | concurrency unset | 1.57 ± 0.01 | 36 | 1.62 ± 0.00 | 36 | +2.8% | +0.8% |
| `uniform-65536` | one-thread | concurrency 1 | 6.39 ± 0.05 | 210 | 6.63 ± 0.04 | 134 | +3.8% | -0.4% |
| `uniform-65536` | one-thread | concurrency unset | 7.06 ± 0.11 | 144 | 7.54 ± 0.04 | 144 | +6.7% | +11.4% |
| `hub-16384` | full-width | concurrency as the run | 1.52 ± 0.00 | 36 | 1.54 ± 0.01 | 0 | +1.4% | +0.7% |
| `hub-65536` | full-width | concurrency as the run | 4.07 ± 0.08 | 390 | 3.17 ± 0.01 | 131 | -22.0% | -4.5% |
| `uniform-16384` | full-width | concurrency as the run | 1.56 ± 0.00 | 36 | 1.71 ± 0.02 | 0 | +9.4% | +0.5% |
| `uniform-65536` | full-width | concurrency as the run | 4.20 ± 0.04 | 367 | 3.27 ± 0.08 | 118 | -22.2% | +4.9% |

At one-thread, 8 of 8 `hub` and `uniform` first-call cells are slower than v0.22.0, +0.9% to +6.7%, where B4's same cells ran -4.0% to +11.4%. At full-width, 2 of 4 `hub` and `uniform` first-call cells are slower than v0.22.0, -22.2% to +9.4%, where B4's same cells ran -4.5% to +4.9%. So at one thread it persists, over a narrower range than B4's rows, and at full width the same kernel is faster than v0.22.0 on the larger fixture of each family and slower on the smaller. The page-fault counts beside each row are within a few of each other, so what is left is not the allocator effect. **What it is not** is now stated rather than assumed: it
is not the transpose, which this run does not build for BFS, and it is not the
allocator state, which the counter beside each row shows to be the same. What
it is remains unexplained.

**PageRank on `layered-16384` at sixteen threads.** The full-width run is the
sixteen-thread one, and its `layered-16384` rows are: first call -2.7%; second call +5.8%. The second call is still slower and the first is not, which is the same shape B4 reported and is unexplained.

| fixture | run | kernel | call | v0.22.0 | `ca68900` | change | steal |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| `layered-16384` | one-thread | pull | first | 30.17 ± 0.05 | 30.82 ± 0.07 | +2.2% | 0 |
| `layered-16384` | one-thread | pull | second | 29.34 ± 0.08 | 30.53 ± 0.01 | +4.1% | 0 |
| `layered-16384` | one-thread | push | first | 115.40 ± 0.06 | 88.78 ± 0.12 | -23.1% | 0 |
| `layered-16384` | one-thread | push | second | 115.15 ± 0.00 | 88.49 ± 0.10 | -23.2% | 0 |
| `layered-65536` | one-thread | pull | first | 108.55 ± 0.05 | 111.19 ± 0.09 | +2.4% | 0 |
| `layered-65536` | one-thread | pull | second | 104.83 ± 0.08 | 110.15 ± 0.12 | +5.1% | 0 |
| `layered-65536` | one-thread | push | first | 414.37 ± 0.65 | 318.68 ± 0.09 | -23.1% | 0 |
| `layered-65536` | one-thread | push | second | 412.83 ± 0.09 | 317.91 ± 0.15 | -23.0% | 0 |
| `layered-16384` | full-width | pull | first | 15.13 ± 0.14 | 14.72 ± 0.15 | -2.7% | 0 |
| `layered-16384` | full-width | pull | second | 13.37 ± 0.18 | 14.14 ± 0.19 | +5.8% | 0 |
| `layered-65536` | full-width | pull | first | 25.49 ± 0.11 | 21.11 ± 0.15 | -17.2% | 0 |
| `layered-65536` | full-width | pull | second | 21.09 ± 0.09 | 20.07 ± 0.21 | -4.8% | 0 |

### What the accounting guarantee costs

`grust-next`, first call, by mode, beside `neo4j-graph`, which performs no
accounting and is `f32` on its own stopping rule.

| fixture | run | kernel | counted | work-uncounted | unchecked | `neo4j-graph` | steal |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `hub-65536` | one-thread | pagerank, pull | 34.02 ± 0.13 | 31.92 ± 0.12 | 31.14 ± 0.26 | 35.93 ± 0.14 | 0 |
| `hub-65536` | one-thread | pagerank, push | 95.14 ± 0.47 | 58.50 ± 0.10 | 56.15 ± 0.25 | 35.93 ± 0.14 | 0 |
| `hub-65536` | one-thread | wcc, concurrency 1 | 6.46 ± 0.04 | 4.28 ± 0.02 | 3.84 ± 0.05 | 3.75 ± 0.01 | 0 |
| `hub-65536` | one-thread | wcc, concurrency unset | 16.67 ± 0.01 | 7.10 ± 0.05 | 6.03 ± 0.01 | 3.75 ± 0.01 | 0 |
| `hub-65536` | one-thread | triangles, concurrency 1 | 72.51 ± 0.02 | 71.64 ± 0.11 | 71.10 ± 0.33 | 35.34 ± 0.15 | 0 |
| `hub-65536` | one-thread | triangles, concurrency unset | 72.29 ± 0.06 | 71.36 ± 0.04 | 70.87 ± 0.11 | 35.34 ± 0.15 | 0 |
| `uniform-65536` | one-thread | pagerank, pull | 32.48 ± 0.20 | 30.66 ± 0.18 | 29.58 ± 0.11 | 44.24 ± 0.08 | 0 |
| `uniform-65536` | one-thread | pagerank, push | 88.77 ± 0.68 | 55.19 ± 0.25 | 53.94 ± 0.24 | 44.24 ± 0.08 | 0 |
| `uniform-65536` | one-thread | wcc, concurrency 1 | 9.81 ± 0.03 | 8.49 ± 0.01 | 7.88 ± 0.05 | 3.75 ± 0.00 | 0 |
| `uniform-65536` | one-thread | wcc, concurrency unset | 16.96 ± 0.03 | 8.06 ± 0.04 | 6.85 ± 0.11 | 3.75 ± 0.00 | 0 |
| `uniform-65536` | one-thread | triangles, concurrency 1 | 78.55 ± 1.00 | 77.72 ± 0.06 | 77.84 ± 0.20 | 39.47 ± 0.14 | 0 |
| `uniform-65536` | one-thread | triangles, concurrency unset | 78.43 ± 0.03 | 78.37 ± 0.22 | 77.15 ± 0.09 | 39.47 ± 0.14 | 0 |
| `hub-65536` | full-width | pagerank, pull | 7.22 ± 0.04 | 4.70 ± 0.01 | 4.69 ± 0.02 | 15.03 ± 0.04 | 0 |
| `hub-65536` | full-width | wcc, concurrency as the run | 1.48 ± 0.05 | 1.24 ± 0.02 | 1.30 ± 0.09 | 3.18 ± 0.05 | 0 |
| `hub-65536` | full-width | triangles, concurrency as the run | 28.78 ± 0.09 | 28.14 ± 0.68 | 27.39 ± 0.30 | 3.50 ± 0.05 | 0 |
| `uniform-65536` | full-width | pagerank, pull | 7.01 ± 0.16 | 4.48 ± 0.05 | 4.51 ± 0.04 | 16.30 ± 0.28 | 0 |
| `uniform-65536` | full-width | wcc, concurrency as the run | 1.80 ± 0.06 | 1.52 ± 0.09 | 1.54 ± 0.05 | 3.08 ± 0.13 | 0 |
| `uniform-65536` | full-width | triangles, concurrency as the run | 29.06 ± 0.08 | 28.25 ± 0.06 | 27.90 ± 0.02 | 3.99 ± 0.04 | 0 |
| `hub-2097152` | large-one-thread | pagerank, pull | 2170.69 ± 43.13 | 2013.59 ± 101.38 | 1935.46 ± 322.66 | 2091.59 ± 5.88 | 3 |
| `hub-2097152` | large-one-thread | pagerank, push | 4025.06 ± 132.51 | 3436.31 ± 43.29 | 2917.49 ± 44.54 | 2091.59 ± 5.88 | 3 |
| `uniform-2097152` | large-one-thread | pagerank, pull | 2207.80 ± 62.26 | 1791.58 ± 24.65 | 1968.11 ± 30.86 | 2162.61 ± 19.69 | 4 |
| `uniform-2097152` | large-one-thread | pagerank, push | 4023.10 ± 11.14 | 3184.51 ± 89.67 | 3133.06 ± 182.93 | 2162.61 ± 19.69 | 4 |
| `hub-2097152` | large-full-width | pagerank, pull | 274.75 ± 15.17 | 219.87 ± 5.69 | 209.83 ± 0.64 | 260.04 ± 1.68 | 1 |
| `uniform-2097152` | large-full-width | pagerank, pull | 248.59 ± 6.98 | 228.12 ± 3.92 | 226.02 ± 1.64 | 262.94 ± 2.50 | 2 |
| `hub-4194304` | xlarge-one-thread | pagerank, pull | 6941.34 ± 23.40 | 6696.58 ± 21.59 | 6493.19 ± 37.52 | 4610.20 ± 513.82 | 121 |
| `hub-4194304` | xlarge-one-thread | pagerank, push | 13050.81 ± 144.21 | 10628.13 ± 52.99 | 10623.61 ± 256.95 | 4610.20 ± 513.82 | 121 |
| `uniform-4194304` | xlarge-one-thread | pagerank, pull | 7030.83 ± 59.57 | 6737.94 ± 17.02 | 6604.33 ± 13.99 | 5387.87 ± 359.63 | 8 |
| `uniform-4194304` | xlarge-one-thread | pagerank, push | 12327.00 ± 48.97 | 10187.56 ± 121.81 | 10020.11 ± 338.23 | 5387.87 ± 359.63 | 8 |
| `hub-4194304` | xlarge-full-width | pagerank, pull | 734.54 ± 19.96 | 714.56 ± 8.58 | 685.88 ± 10.29 | 388.19 ± 36.49 | 4 |
| `uniform-4194304` | xlarge-full-width | pagerank, pull | 747.76 ± 13.22 | 735.39 ± 11.02 | 720.94 ± 15.14 | 578.25 ± 1.81 | 3 |

Counting also costs in the build: `grust-next`'s `build_ms` for PageRank on `hub-65536` at one thread is 47.07 ms counted, 38.00 work-uncounted and 37.56 unchecked, because building the projection and its transpose charges work too.

### B4 against B5 on unchanged code

The participants that did not change between the two runs, one thread, first
call. A B5 cell is compared only with other cells of the same B5 run; this
table is the size of the drift between campaigns, not a correction to either.

| fixture | algorithm | participant | B4 | B5 | change |
| --- | --- | --- | ---: | ---: | ---: |
| `hub-65536` | pagerank | `grust#1` | 65.11 ± 0.37 | 52.59 ± 0.21 | -19.2% |
| `hub-65536` | wcc | `grust#1` | 7.17 ± 0.09 | 6.66 ± 0.01 | -7.1% |
| `uniform-65536` | pagerank | `grust#1` | 59.44 ± 3.00 | 51.51 ± 0.43 | -13.3% |
| `uniform-65536` | wcc | `grust#1` | 9.45 ± 0.02 | 8.88 ± 0.05 | -6.1% |
| `hub-65536` | pagerank | `grust#unset` | 206.77 ± 0.88 | 203.55 ± 0.34 | -1.6% |
| `hub-65536` | wcc | `grust#unset` | 17.28 ± 0.10 | 16.88 ± 0.01 | -2.3% |
| `uniform-65536` | pagerank | `grust#unset` | 196.00 ± 0.71 | 192.34 ± 0.36 | -1.9% |
| `uniform-65536` | wcc | `grust#unset` | 17.42 ± 0.03 | 17.08 ± 0.05 | -1.9% |
| `hub-65536` | pagerank | `icecat` | 31.74 ± 0.09 | 34.12 ± 0.01 | +7.5% |
| `hub-65536` | wcc | `icecat` | 3.80 ± 0.00 | 3.48 ± 0.22 | -8.4% |
| `uniform-65536` | pagerank | `icecat` | 30.24 ± 0.19 | 32.69 ± 0.02 | +8.1% |
| `uniform-65536` | wcc | `icecat` | 4.51 ± 0.01 | 4.02 ± 0.07 | -10.7% |
| `hub-65536` | pagerank | `grustcat` | 34.01 ± 0.34 | 30.23 ± 0.03 | -11.1% |
| `hub-65536` | wcc | `grustcat` | 2.41 ± 0.01 | 2.44 ± 0.01 | +1.3% |
| `uniform-65536` | pagerank | `grustcat` | 31.24 ± 0.35 | 29.27 ± 0.12 | -6.3% |
| `uniform-65536` | wcc | `grustcat` | 3.01 ± 0.03 | 3.05 ± 0.04 | +1.0% |
| `hub-65536` | pagerank | `neo4j-graph` | 40.03 ± 0.40 | 35.93 ± 0.14 | -10.2% |
| `hub-65536` | wcc | `neo4j-graph` | 3.84 ± 0.01 | 3.75 ± 0.01 | -2.3% |
| `uniform-65536` | pagerank | `neo4j-graph` | 48.49 ± 0.20 | 44.24 ± 0.08 | -8.8% |
| `uniform-65536` | wcc | `neo4j-graph` | 3.86 ± 0.01 | 3.75 ± 0.00 | -2.9% |
| `hub-65536` | pagerank | `icebug` | 76.06 ± 1.27 | 42.13 ± 0.80 | -44.6% |
| `hub-65536` | wcc | `icebug` | 22.33 ± 0.59 | 11.25 ± 0.41 | -49.6% |
| `uniform-65536` | pagerank | `icebug` | 69.77 ± 0.57 | 39.50 ± 0.78 | -43.4% |
| `uniform-65536` | wcc | `icebug` | 24.76 ± 1.29 | 12.83 ± 0.08 | -48.2% |

The same binaries' sources, on the same fixtures and the same host, move -49.6% to +8.1% between the two campaigns, and the largest of those is a participant containing no Grust at all. Both campaigns were built from clean trees on that host and ran on an idle one; B5 additionally dropped the page cache before starting, which B4 did not. **The drift is unexplained**, and it is the reason a cell is only ever compared with other cells of its own run.

## B6: one commit, the same protocol

B5 timed Grust `ca68900` and left two things unexplained: PageRank on the
`path` family at full width, up to 2.2 times v0.22.0, and WCC's first call at
one worker, 10 to 14% slower. An attribution on the measuring host, outside
this harness, found the cause of the first and part of the second, and one
commit fixed it. B6 measures that commit under B5's protocol, unchanged, so
that the two campaigns differ in one thing.

- **What changed: one commit.** Grust `55a200f`, "Pad each work meter's
  balance to a whole cache line", merged to `main` as `87fc462`. Between
  `ca68900` and `87fc462`, the only files changed outside `docs/` and the
  changelog are that commit's three: `crates/grust-procedures/src/resources.rs`,
  `resources/accounting.rs` and the new `resources/balance.rs`. The other
  commits in the range are a design proposal under `docs/`.
- **The cause it fixed, as the commit states it.** A `WorkMeter` spends its
  admitted block from one shared `AtomicUsize`, exchanged once per visited
  entry by the worker that owns the meter. As a bare `Arc<AtomicUsize>` that
  word was a 32-byte heap chunk, and glibc's tcache handed it out beside
  whatever the same size class had just freed — since the projection build
  went parallel, the pool's own bookkeeping, which other cores keep writing.
  Every such write took the cache line from the worker, and its next
  `lock cmpxchg` had to fetch it back; the commit's attribution put more than
  half of PageRank's pull-arc loop on that exchange at sixteen workers on a
  path, and disabling tcache with the same code recovered it. The balance is
  now the word followed by 56 bytes of padding, `repr(C)`, one whole line and
  not over-aligned, so two balances never share a line and the balance leaves
  the 32-byte class. What is counted, when a budget refuses, and every
  accounting mode are unchanged; the commit says results and work counts are
  bit for bit the same, and B6's parity gate checks that here rather than
  taking the commit's word.
- **What the commit's own measurement left open.** Its message records that
  the one-worker WCC residue responded to the balance's chunk size class and
  not to its line — a shape padded on both sides recovered PageRank equally
  and left one-worker WCC at the unpadded head's +11%, while every other chunk
  size tried brought it within 1 to 2% — and calls that mechanism unexplained.
  B6 measures it under the campaign's protocol below. It does not explain it.

**Nothing else changed.** The harness is at `633ff36`, which differs from
B5's `9ec8548` by `b5_report.py` alone, a file the image copies and nothing in
it runs; `campaign.py plan` printed the same bytes from both checkouts on the
host before the build, and `plan.json` in the bundle is that output. The
twelve fixtures were SHA-256-checked against B5's manifest before the build,
and the manifest in the bundle records the check. The image was built as B5's
was: on quegee, under a 20 GB memory cap with four jobs, from clean trees, and
the audit, image receipt and manifest were taken before parity and never
during a run. `icebug`, whose receipt carries only Icecat's commit, is the
same binary byte for byte as in B5's audit; the Rust participants carry the
harness commit in theirs and so differ from B5's by that stamp. The page cache
was dropped after parity and before the first timed run, as in B5. Parity
came first, every fixture set at concurrency unset, 1 and 16, with the bits
gate of `grust-next` against v0.22.0, and a variant that disagrees is never
timed.

## B6: results

One host, quegee, 2026-09-22. Grust `2182cdb` (v0.22.0) as `grust`, Grust `87fc462` as `grust-next`, Icecat `57b443ec`, this harness at `633ff36`, image `simple-rust-algo-bench:b6-87fc462`, built on the host from clean trees. The 12 fixtures are SHA-256-identical to B5's: `identical_to_b5` is true in the manifest. One warmup, five repeats,
counterbalanced, parity gated at every concurrency. **Every cell of every run,
with its steal, its dispersion, its minor page faults and its usability, is in
`simple-rust-algo-bench-evidence/b6-quegee/tables.md`**, generated from the run
files by `tables.py`; the tables below select from it and add nothing to it.
Times are milliseconds, median ± MAD; page faults are the median of the same
samples, read outside the timers. Steal is ticks over that cell's group. Where
a table shows a B5 column, it is B5's own ratio for the same cell, computed
from B5's bundle; no B5 time is ever divided by a B6 time.

**Host conditions.** 1 resident agent session was seen by name across the campaign (2382171 codex resume 01a0ad61-0419-7110-9e8c-c25058935bc0). 0 sightings were recorded over 8 timed invocations, and a run with a sighting is discarded rather than published. The host was checked idle before and after every run and sampled once a second during it. The timed campaign ran from 2026-09-22T15:10:29Z to 2026-09-22T18:07:22Z, 8 runs, in the order listed.

- `one-thread`: clean, started 2026-09-22T15:10:31+0000, 260.1 s, 1 steal ticks over the run, 0 sightings, 1 resident agent session.
- `full-width`: clean, started 2026-09-22T15:14:53+0000, 116.7 s, 0 steal ticks over the run, 0 sightings, 1 resident agent session.
- `pinned-one-thread`: clean, started 2026-09-22T15:16:52+0000, 156.2 s, 1 steal ticks over the run, 0 sightings, 1 resident agent session.
- `pinned-full-width`: clean, started 2026-09-22T15:19:30+0000, 86.4 s, 0 steal ticks over the run, 0 sightings, 1 resident agent session.
- `large-one-thread`: clean, started 2026-09-22T15:20:59+0000, 2334.2 s, 10 steal ticks over the run, 0 sightings, 1 resident agent session.
- `large-full-width`: clean, started 2026-09-22T15:59:55+0000, 815.1 s, 3 steal ticks over the run, 0 sightings, 1 resident agent session.
- `xlarge-one-thread`: clean, started 2026-09-22T16:13:32+0000, 5131.5 s, 21 steal ticks over the run, 0 sightings, 1 resident agent session.
- `xlarge-full-width`: clean, started 2026-09-22T17:39:06+0000, 1696.0 s, 7 steal ticks over the run, 0 sightings, 1 resident agent session.

**None of the 1840 cells reached the 0.25 MAD/median threshold**; the largest dispersion was 0.137, `grust-next@unchecked` wcc hub-16384 second in full-width.

**Parity at the commit under test**, every fixture set at concurrency unset, 1
and 16, before any timing. `grust-next` must return v0.22.0's PageRank vector
bit for bit or it is a mismatch and is never timed.

| file | agree | absent | mismatch | error | bits-identical to v0.22.0 | mismatched rows |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `fixtures-1` | 252 | 32 | 4 | 0 | 24 of 24 | neo4j-graph layered-16384, neo4j-graph layered-65536, neo4j-graph path-16384, neo4j-graph path-65536 |
| `fixtures-16` | 252 | 32 | 4 | 0 | 24 of 24 | neo4j-graph layered-16384, neo4j-graph layered-65536, neo4j-graph path-16384, neo4j-graph path-65536 |
| `fixtures-large-1` | 18 | 0 | 0 | 0 | 6 of 6 | — |
| `fixtures-large-16` | 18 | 0 | 0 | 0 | 6 of 6 | — |
| `fixtures-large-unset` | 18 | 0 | 0 | 0 | 6 of 6 | — |
| `fixtures-unset` | 252 | 32 | 4 | 0 | 24 of 24 | neo4j-graph layered-16384, neo4j-graph layered-65536, neo4j-graph path-16384, neo4j-graph path-65536 |
| `fixtures-xlarge-1` | 18 | 0 | 0 | 0 | 6 of 6 | — |
| `fixtures-xlarge-16` | 18 | 0 | 0 | 0 | 6 of 6 | — |
| `fixtures-xlarge-unset` | 18 | 0 | 0 | 0 | 6 of 6 | — |

3 parity invocations exited 1, the protocol set's known `neo4j-graph` dangling-mass rows as in B5; the driver takes its verdict from the file, not the exit code. 0 parity invocations are marked shared and 0 were not started; every fixture set has a clean invocation at every concurrency, and the files are the output of the last invocation of each.

The `--bits-identical` gate names v0.22.0 and the three accounting modes. The `+eager` variant's PageRank digest and iteration count equal v0.22.0's in 36 of 36 rows.

**The allocator state, re-decided on B6's own counter**, by B5's rule.
Across the 48 WCC and BFS first-call cells at the protocol sizes, `grust-next` takes a median of -2 minor page faults against v0.22.0, and the median absolute difference is 2, against the 25 that B5's rule set as the line. The two builds are in the same allocator state on the same cell, and the published tables are the default-allocator runs, as in B5; the pinned runs stay as a labelled probe in `tables.md`. Median change under pinning, per participant, first
call at the protocol size against the same cell unpinned: `grust` +0.5% over 24 cells; `grust-next` +2.3% over 24 cells; `grustcat` +0.5% over 12 cells; `icebug` -1.5% over 12 cells; `icecat` +0.6% over 12 cells; `neo4j-graph` +0.6% over 12 cells.

### The transpose, on the build side

One thread, pull kernel (concurrency 1), PageRank — the one kernel here that
reads in-arcs, and so the one whose build column contains them. "First" is a
fresh projection's first kernel call; on v0.22.0 it includes building the
transpose. "Second" repeats it with the transpose cached and on warm caches,
which is not the condition of any other participant's timed call.

| fixture | `grust` v0.22.0 first | `grust` v0.22.0 second | `grust-next` counted first | transpose, in `build_ms` | `grustcat` | steal |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `hub-65536` | 68.11 ± 2.53 | 57.38 ± 1.85 | 35.21 ± 0.23 | 7.32 | 32.59 ± 0.38 | 0 |
| `uniform-65536` | 60.82 ± 3.60 | 48.70 ± 3.01 | 32.86 ± 0.37 | 7.13 | 30.88 ± 0.28 | 0 |
| `hub-2097152` | 6581.11 ± 71.46 | 5802.03 ± 38.39 | 3859.96 ± 2.75 | 686.14 | 3310.95 ± 24.32 | 5 |
| `uniform-2097152` | 6999.18 ± 112.79 | 6164.16 ± 55.86 | 3821.94 ± 99.41 | 636.85 | 3836.22 ± 12.17 | 5 |
| `hub-4194304` | 14778.23 ± 100.50 | 13074.01 ± 130.01 | 8695.93 ± 24.39 | 1482.25 | 7349.00 ± 45.76 | 11 |
| `uniform-4194304` | 15671.38 ± 112.88 | 14150.99 ± 74.58 | 9001.38 ± 40.23 | 1469.27 | 8617.93 ± 93.54 | 10 |

### The kernel change, v0.22.0 against `87fc462`

Same mode (counted), same concurrency, second call against second call, so the
transpose is cached on both sides. Both builds return the same scores bit for
bit, which parity checked on every fixture at every concurrency. The last
ratio is what B5 measured for the same cell on `ca68900`.

| fixture | run | kernel | v0.22.0 | `87fc462` | ratio | B5 ratio, `ca68900` | steal |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `hub-16384` | one-thread | pull | 9.60 ± 0.01 | 7.97 ± 0.00 | 0.831 | 0.831 | 0 |
| `hub-16384` | one-thread | push | 50.58 ± 0.03 | 23.18 ± 0.05 | 0.458 | 0.460 | 0 |
| `hub-65536` | one-thread | pull | 57.38 ± 1.85 | 34.59 ± 0.04 | 0.603 | 0.755 | 0 |
| `hub-65536` | one-thread | push | 204.56 ± 0.32 | 95.01 ± 0.20 | 0.464 | 0.473 | 0 |
| `uniform-16384` | one-thread | pull | 9.23 ± 0.02 | 7.54 ± 0.01 | 0.817 | 0.819 | 0 |
| `uniform-16384` | one-thread | push | 48.53 ± 0.74 | 21.66 ± 0.11 | 0.446 | 0.450 | 0 |
| `uniform-65536` | one-thread | pull | 48.70 ± 3.01 | 31.90 ± 0.35 | 0.655 | 0.737 | 0 |
| `uniform-65536` | one-thread | push | 194.23 ± 0.50 | 88.52 ± 0.50 | 0.456 | 0.463 | 0 |
| `hub-16384` | full-width | pull | 3.42 ± 0.03 | 3.44 ± 0.03 | 1.004 | 0.951 | 0 |
| `hub-65536` | full-width | pull | 8.90 ± 0.19 | 7.58 ± 0.24 | 0.851 | 0.816 | 0 |
| `uniform-16384` | full-width | pull | 3.30 ± 0.05 | 3.33 ± 0.13 | 1.009 | 1.027 | 0 |
| `uniform-65536` | full-width | pull | 8.40 ± 0.08 | 6.77 ± 0.14 | 0.806 | 0.819 | 0 |
| `hub-2097152` | large-one-thread | pull | 5802.03 ± 38.39 | 3812.73 ± 101.14 | 0.657 | 0.440 | 5 |
| `hub-2097152` | large-one-thread | push | 17246.72 ± 220.63 | 7378.80 ± 66.93 | 0.428 | 0.530 | 5 |
| `uniform-2097152` | large-one-thread | pull | 6164.16 ± 55.86 | 3797.86 ± 144.29 | 0.616 | 0.439 | 5 |
| `uniform-2097152` | large-one-thread | push | 17070.93 ± 105.84 | 7023.50 ± 278.99 | 0.411 | 0.570 | 5 |
| `hub-2097152` | large-full-width | pull | 584.95 ± 5.36 | 263.12 ± 22.10 | 0.450 | 0.465 | 2 |
| `uniform-2097152` | large-full-width | pull | 614.92 ± 11.23 | 274.66 ± 18.41 | 0.447 | 0.462 | 1 |
| `hub-4194304` | xlarge-one-thread | pull | 13074.01 ± 130.01 | 8709.38 ± 18.38 | 0.666 | 0.617 | 11 |
| `hub-4194304` | xlarge-one-thread | push | 35862.50 ± 212.07 | 15597.02 ± 106.25 | 0.435 | 0.497 | 11 |
| `uniform-4194304` | xlarge-one-thread | pull | 14150.99 ± 74.58 | 8987.69 ± 46.44 | 0.635 | 0.592 | 10 |
| `uniform-4194304` | xlarge-one-thread | push | 35547.34 ± 61.75 | 15050.22 ± 172.93 | 0.423 | 0.508 | 10 |
| `hub-4194304` | xlarge-full-width | pull | 1455.25 ± 24.86 | 815.82 ± 16.57 | 0.561 | 0.527 | 3 |
| `uniform-4194304` | xlarge-full-width | pull | 1630.55 ± 1.23 | 880.33 ± 12.05 | 0.540 | 0.519 | 4 |

### PageRank on the `path` family, the cell the commit was written for

Pull kernel, both calls, both protocol runs. `path` is a chain with a dangling
node and is not a family this document publishes PageRank on, because
`neo4j-graph` computes a different function there; it is timed, and in B5 it
was where the regression was largest.

| fixture | run | call | v0.22.0 | faults | `87fc462` | faults | change | B5 said | steal |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `path-16384` | one-thread | first | 15.51 ± 0.03 | 160 | 14.76 ± 0.02 | 96 | -4.8% | -4.3% | 0 |
| `path-16384` | one-thread | second | 14.71 ± 0.02 | 0 | 14.65 ± 0.01 | 64 | -0.4% | -0.0% | 0 |
| `path-65536` | one-thread | first | 54.48 ± 0.00 | 640 | 52.84 ± 0.44 | 384 | -3.0% | -3.7% | 0 |
| `path-65536` | one-thread | second | 51.14 ± 0.12 | 0 | 52.04 ± 0.07 | 352 | +1.8% | +1.5% | 0 |
| `path-16384` | full-width | first | 10.60 ± 0.08 | 261 | 9.91 ± 0.19 | 108 | -6.5% | +47.9% | 0 |
| `path-16384` | full-width | second | 8.86 ± 0.13 | 0 | 9.68 ± 0.05 | 64 | +9.3% | +86.6% | 0 |
| `path-65536` | full-width | first | 16.72 ± 0.24 | 755 | 12.72 ± 0.05 | 407 | -23.9% | +61.1% | 0 |
| `path-65536` | full-width | second | 12.24 ± 0.16 | 2 | 12.29 ± 0.14 | 353 | +0.4% | +117.4% | 0 |

### Every cell that got worse

Counted `grust-next` against v0.22.0, same fixture, algorithm, kernel and call.
68 of the 216 counted cells with a v0.22.0 counterpart are slower on `87fc462`, by +0.3% to +52.7%; 50 of those are slower by more than the dispersion of the two cells. The standing column applies one rule to every cell: the
margin is the two cells' relative MADs added together; a ratio inside it is
"within dispersion", outside it the cell is "still slower".

| fixture | algorithm | run | kernel | call | v0.22.0 | faults | `87fc462` | faults | change | standing | steal |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| `hub-16384` | bfs | full-width | concurrency as the run | first | 1.57 ± 0.03 | 36 | 1.58 ± 0.04 | 0 | +0.7% | within dispersion | 0 |
| `hub-16384` | bfs | full-width | concurrency as the run | second | 1.45 ± 0.01 | 0 | 1.48 ± 0.01 | 0 | +2.3% | still slower | 0 |
| `hub-16384` | pagerank | full-width | pull | second | 3.42 ± 0.03 | 0 | 3.44 ± 0.03 | 0 | +0.4% | within dispersion | 0 |
| `hub-16384` | triangles | full-width | concurrency as the run | second | 6.28 ± 0.01 | 1 | 7.23 ± 0.05 | 512 | +15.2% | still slower | 0 |
| `hub-65536` | triangles | full-width | concurrency as the run | second | 25.66 ± 0.04 | 1 | 28.00 ± 0.56 | 1025 | +9.1% | still slower | 0 |
| `layered-16384` | pagerank | full-width | pull | second | 13.83 ± 0.32 | 0 | 14.42 ± 0.17 | 0 | +4.3% | still slower | 0 |
| `layered-16384` | triangles | full-width | concurrency as the run | second | 1.70 ± 0.01 | 1 | 2.17 ± 0.05 | 318 | +27.4% | still slower | 0 |
| `layered-16384` | wcc | full-width | concurrency as the run | second | 0.34 ± 0.01 | 30 | 0.36 ± 0.01 | 30 | +6.2% | within dispersion | 0 |
| `layered-65536` | triangles | full-width | concurrency as the run | second | 6.56 ± 0.01 | 1 | 7.29 ± 0.00 | 508 | +11.1% | still slower | 0 |
| `path-16384` | pagerank | full-width | pull | second | 8.86 ± 0.13 | 0 | 9.68 ± 0.05 | 64 | +9.3% | still slower | 0 |
| `path-16384` | triangles | full-width | concurrency as the run | second | 0.97 ± 0.02 | 2 | 1.39 ± 0.01 | 256 | +42.5% | still slower | 0 |
| `path-65536` | pagerank | full-width | pull | second | 12.24 ± 0.16 | 2 | 12.29 ± 0.14 | 353 | +0.4% | within dispersion | 0 |
| `path-65536` | triangles | full-width | concurrency as the run | second | 3.63 ± 0.04 | 1 | 5.54 ± 0.08 | 1120 | +52.7% | still slower | 0 |
| `uniform-16384` | bfs | full-width | concurrency as the run | first | 1.68 ± 0.04 | 36 | 1.84 ± 0.05 | 0 | +9.8% | still slower | 0 |
| `uniform-16384` | bfs | full-width | concurrency as the run | second | 1.47 ± 0.00 | 0 | 1.50 ± 0.01 | 0 | +2.3% | still slower | 0 |
| `uniform-16384` | pagerank | full-width | pull | second | 3.30 ± 0.05 | 1 | 3.33 ± 0.13 | 0 | +0.9% | within dispersion | 0 |
| `uniform-16384` | triangles | full-width | concurrency as the run | second | 6.49 ± 0.02 | 1 | 7.37 ± 0.05 | 512 | +13.6% | still slower | 0 |
| `uniform-65536` | triangles | full-width | concurrency as the run | second | 26.56 ± 0.07 | 1 | 28.66 ± 0.49 | 1026 | +7.9% | still slower | 0 |
| `hub-16384` | bfs | one-thread | concurrency 1 | first | 1.56 ± 0.00 | 36 | 1.59 ± 0.02 | 32 | +1.6% | still slower | 0 |
| `hub-16384` | bfs | one-thread | concurrency unset | first | 1.58 ± 0.02 | 36 | 1.60 ± 0.02 | 36 | +1.3% | within dispersion | 0 |
| `hub-16384` | bfs | one-thread | concurrency 1 | second | 1.44 ± 0.00 | 0 | 1.46 ± 0.00 | 0 | +1.6% | still slower | 0 |
| `hub-16384` | bfs | one-thread | concurrency unset | second | 1.44 ± 0.00 | 0 | 1.47 ± 0.00 | 0 | +2.2% | still slower | 0 |
| `hub-16384` | triangles | one-thread | concurrency 1 | second | 15.73 ± 0.03 | 32 | 16.44 ± 0.06 | 511 | +4.5% | still slower | 0 |
| `hub-16384` | triangles | one-thread | concurrency unset | second | 15.69 ± 0.02 | 32 | 16.33 ± 0.07 | 543 | +4.1% | still slower | 0 |
| `hub-65536` | bfs | one-thread | concurrency unset | first | 9.60 ± 0.25 | 144 | 10.64 ± 0.58 | 144 | +10.8% | still slower | 0 |
| `hub-65536` | bfs | one-thread | concurrency 1 | second | 5.90 ± 0.11 | 0 | 6.20 ± 0.19 | 0 | +5.0% | within dispersion | 0 |
| `hub-65536` | bfs | one-thread | concurrency unset | second | 7.37 ± 0.26 | 0 | 8.08 ± 0.77 | 0 | +9.7% | within dispersion | 0 |
| `hub-65536` | triangles | one-thread | concurrency unset | second | 76.04 ± 0.80 | 128 | 76.58 ± 1.94 | 641 | +0.7% | within dispersion | 0 |
| `layered-16384` | pagerank | one-thread | pull | first | 30.23 ± 0.01 | 192 | 30.86 ± 0.03 | 96 | +2.1% | still slower | 0 |
| `layered-16384` | pagerank | one-thread | pull | second | 29.35 ± 0.01 | 0 | 30.65 ± 0.01 | 0 | +4.4% | still slower | 0 |
| `layered-16384` | triangles | one-thread | concurrency 1 | second | 2.21 ± 0.01 | 32 | 2.59 ± 0.00 | 350 | +17.0% | still slower | 0 |
| `layered-16384` | triangles | one-thread | concurrency unset | second | 2.22 ± 0.00 | 32 | 2.32 ± 0.01 | 159 | +4.4% | still slower | 0 |
| `layered-16384` | wcc | one-thread | concurrency 1 | first | 0.63 ± 0.00 | 32 | 0.69 ± 0.00 | 32 | +9.5% | still slower | 0 |
| `layered-16384` | wcc | one-thread | concurrency 1 | second | 0.65 ± 0.00 | 27 | 0.65 ± 0.01 | 15 | +0.4% | within dispersion | 0 |
| `layered-65536` | bfs | one-thread | concurrency unset | first | 1.87 ± 0.00 | 119 | 1.88 ± 0.03 | 119 | +0.5% | within dispersion | 0 |
| `layered-65536` | bfs | one-thread | concurrency unset | second | 1.59 ± 0.00 | 0 | 1.59 ± 0.01 | 0 | +0.4% | within dispersion | 0 |
| `layered-65536` | pagerank | one-thread | pull | first | 108.93 ± 0.15 | 766 | 112.30 ± 0.20 | 384 | +3.1% | still slower | 0 |
| `layered-65536` | pagerank | one-thread | pull | second | 105.20 ± 0.09 | 0 | 110.90 ± 0.14 | 0 | +5.4% | still slower | 0 |
| `layered-65536` | triangles | one-thread | concurrency 1 | second | 8.98 ± 0.05 | 128 | 11.02 ± 0.31 | 1497 | +22.7% | still slower | 0 |
| `layered-65536` | triangles | one-thread | concurrency unset | second | 8.96 ± 0.02 | 128 | 10.26 ± 0.14 | 635 | +14.5% | still slower | 0 |
| `layered-65536` | wcc | one-thread | concurrency 1 | first | 2.56 ± 0.01 | 128 | 2.81 ± 0.01 | 128 | +9.7% | still slower | 0 |
| `path-16384` | triangles | one-thread | concurrency 1 | first | 1.54 ± 0.01 | 256 | 1.58 ± 0.01 | 256 | +2.2% | still slower | 0 |
| `path-16384` | triangles | one-thread | concurrency unset | first | 1.56 ± 0.01 | 256 | 1.58 ± 0.01 | 256 | +1.0% | within dispersion | 0 |
| `path-16384` | triangles | one-thread | concurrency 1 | second | 1.09 ± 0.00 | 32 | 1.42 ± 0.01 | 256 | +30.3% | still slower | 0 |
| `path-16384` | wcc | one-thread | concurrency 1 | first | 0.45 ± 0.00 | 32 | 0.45 ± 0.00 | 32 | +0.5% | within dispersion | 0 |
| `path-65536` | pagerank | one-thread | pull | second | 51.14 ± 0.12 | 0 | 52.04 ± 0.07 | 352 | +1.8% | still slower | 0 |
| `path-65536` | triangles | one-thread | concurrency 1 | first | 6.23 ± 0.07 | 1024 | 6.34 ± 0.03 | 1024 | +1.8% | still slower | 0 |
| `path-65536` | triangles | one-thread | concurrency unset | first | 6.24 ± 0.03 | 1025 | 6.30 ± 0.02 | 1024 | +1.0% | still slower | 0 |
| `path-65536` | triangles | one-thread | concurrency 1 | second | 4.39 ± 0.01 | 128 | 6.10 ± 0.09 | 1120 | +39.2% | still slower | 0 |
| `path-65536` | wcc | one-thread | concurrency 1 | first | 1.80 ± 0.00 | 128 | 1.83 ± 0.01 | 128 | +1.9% | still slower | 0 |
| `uniform-16384` | bfs | one-thread | concurrency 1 | first | 1.63 ± 0.02 | 36 | 1.66 ± 0.03 | 32 | +1.8% | within dispersion | 0 |
| `uniform-16384` | bfs | one-thread | concurrency unset | first | 1.67 ± 0.04 | 36 | 1.75 ± 0.05 | 36 | +5.0% | still slower | 0 |
| `uniform-16384` | bfs | one-thread | concurrency 1 | second | 1.46 ± 0.00 | 0 | 1.49 ± 0.02 | 0 | +1.8% | still slower | 0 |
| `uniform-16384` | bfs | one-thread | concurrency unset | second | 1.47 ± 0.00 | 0 | 1.49 ± 0.00 | 0 | +1.5% | still slower | 0 |
| `uniform-16384` | triangles | one-thread | concurrency 1 | second | 17.19 ± 0.05 | 32 | 17.82 ± 0.13 | 512 | +3.7% | still slower | 1 |
| `uniform-16384` | triangles | one-thread | concurrency unset | second | 17.17 ± 0.02 | 32 | 17.82 ± 0.04 | 544 | +3.8% | still slower | 1 |
| `uniform-16384` | wcc | one-thread | concurrency 1 | first | 2.07 ± 0.01 | 32 | 2.35 ± 0.01 | 32 | +13.7% | still slower | 0 |
| `uniform-16384` | wcc | one-thread | concurrency unset | first | 4.17 ± 0.01 | 32 | 4.27 ± 0.01 | 32 | +2.2% | still slower | 0 |
| `uniform-16384` | wcc | one-thread | concurrency 1 | second | 2.29 ± 0.00 | 31 | 2.30 ± 0.00 | 16 | +0.7% | still slower | 0 |
| `uniform-16384` | wcc | one-thread | concurrency unset | second | 4.17 ± 0.02 | 31 | 4.18 ± 0.00 | 0 | +0.3% | within dispersion | 0 |
| `uniform-65536` | bfs | one-thread | concurrency unset | first | 9.72 ± 0.30 | 144 | 10.32 ± 0.19 | 144 | +6.1% | still slower | 0 |
| `uniform-65536` | bfs | one-thread | concurrency 1 | second | 6.63 ± 0.19 | 0 | 7.18 ± 0.27 | 0 | +8.2% | still slower | 0 |
| `uniform-65536` | bfs | one-thread | concurrency unset | second | 7.59 ± 0.48 | 0 | 8.05 ± 0.42 | 0 | +6.2% | within dispersion | 0 |
| `uniform-65536` | triangles | one-thread | concurrency 1 | first | 87.25 ± 0.46 | 1668 | 87.90 ± 0.24 | 1157 | +0.7% | within dispersion | 0 |
| `uniform-65536` | triangles | one-thread | concurrency 1 | second | 82.22 ± 0.98 | 128 | 86.47 ± 1.25 | 1537 | +5.2% | still slower | 0 |
| `uniform-65536` | triangles | one-thread | concurrency unset | second | 79.80 ± 0.24 | 128 | 83.88 ± 0.64 | 1154 | +5.1% | still slower | 0 |
| `uniform-65536` | wcc | one-thread | concurrency 1 | first | 9.36 ± 0.05 | 128 | 10.39 ± 0.02 | 128 | +11.0% | still slower | 0 |
| `uniform-65536` | wcc | one-thread | concurrency 1 | second | 9.83 ± 0.07 | 128 | 10.25 ± 0.09 | 64 | +4.3% | still slower | 0 |

The largest of them: `path-65536` triangles full-width concurrency as the run second +52.7%; `path-16384` triangles full-width concurrency as the run second +42.5%; `path-65536` triangles one-thread concurrency 1 second +39.2%; `path-16384` triangles one-thread concurrency 1 second +30.3%; `layered-16384` triangles full-width concurrency as the run second +27.4%.

- **The triangles second call.** 21 of them are the triangles second call, +0.7% to +52.7%, with a median of 32 minor page faults on v0.22.0 against 543 on `87fc462`: the same shape as B5, where the second call allocates again on the later commit and v0.22.0's does not. The padding commit does not touch it and it is not expected to.

### B5's slower cells, on the padded commit

B5 found 70 of its 216 counted cells slower than v0.22.0 on `ca68900`. On `87fc462`, the same cells stand: **5 faster than v0.22.0, 18 within dispersion of it, 47 still slower**. The standing is decided by one rule for every cell: the B6 ratio against a margin of the two cells' relative MADs added together; inside the margin the two are level, outside it one is faster.

| fixture | algorithm | run | kernel | call | B5 change | v0.22.0 | faults | `87fc462` | faults | B6 change | standing | steal |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| `hub-16384` | bfs | full-width | concurrency as the run | first | +1.4% | 1.57 ± 0.03 | 36 | 1.58 ± 0.04 | 0 | +0.7% | within dispersion | 0 |
| `hub-16384` | bfs | full-width | concurrency as the run | second | +0.3% | 1.45 ± 0.01 | 0 | 1.48 ± 0.01 | 0 | +2.3% | still slower | 0 |
| `hub-16384` | triangles | full-width | concurrency as the run | second | +13.9% | 6.28 ± 0.01 | 1 | 7.23 ± 0.05 | 512 | +15.2% | still slower | 0 |
| `hub-65536` | triangles | full-width | concurrency as the run | second | +5.2% | 25.66 ± 0.04 | 1 | 28.00 ± 0.56 | 1025 | +9.1% | still slower | 0 |
| `layered-16384` | bfs | full-width | concurrency as the run | first | +0.3% | 0.46 ± 0.01 | 30 | 0.46 ± 0.00 | 26 | -0.0% | within dispersion | 0 |
| `layered-16384` | pagerank | full-width | pull | second | +5.8% | 13.83 ± 0.32 | 0 | 14.42 ± 0.17 | 0 | +4.3% | still slower | 0 |
| `layered-16384` | triangles | full-width | concurrency as the run | second | +29.2% | 1.70 ± 0.01 | 1 | 2.17 ± 0.05 | 318 | +27.4% | still slower | 0 |
| `layered-16384` | wcc | full-width | concurrency as the run | second | +2.0% | 0.34 ± 0.01 | 30 | 0.36 ± 0.01 | 30 | +6.2% | within dispersion | 0 |
| `layered-65536` | bfs | full-width | concurrency as the run | first | +0.6% | 1.89 ± 0.01 | 119 | 1.88 ± 0.00 | 103 | -0.4% | within dispersion | 0 |
| `layered-65536` | triangles | full-width | concurrency as the run | second | +10.2% | 6.56 ± 0.01 | 1 | 7.29 ± 0.00 | 508 | +11.1% | still slower | 0 |
| `layered-65536` | wcc | full-width | concurrency as the run | second | +0.8% | 0.88 ± 0.03 | 125 | 0.86 ± 0.01 | 123 | -2.2% | within dispersion | 0 |
| `path-16384` | pagerank | full-width | pull | first | +47.9% | 10.60 ± 0.08 | 261 | 9.91 ± 0.19 | 108 | -6.5% | faster than v0.22.0 | 0 |
| `path-16384` | pagerank | full-width | pull | second | +86.6% | 8.86 ± 0.13 | 0 | 9.68 ± 0.05 | 64 | +9.3% | still slower | 0 |
| `path-16384` | triangles | full-width | concurrency as the run | second | +53.6% | 0.97 ± 0.02 | 2 | 1.39 ± 0.01 | 256 | +42.5% | still slower | 0 |
| `path-16384` | wcc | full-width | concurrency as the run | second | +40.0% | 0.30 ± 0.00 | 33 | 0.30 ± 0.02 | 17 | -0.2% | within dispersion | 0 |
| `path-65536` | pagerank | full-width | pull | first | +61.1% | 16.72 ± 0.24 | 755 | 12.72 ± 0.05 | 407 | -23.9% | faster than v0.22.0 | 0 |
| `path-65536` | pagerank | full-width | pull | second | +117.4% | 12.24 ± 0.16 | 2 | 12.29 ± 0.14 | 353 | +0.4% | within dispersion | 0 |
| `path-65536` | triangles | full-width | concurrency as the run | second | +64.2% | 3.63 ± 0.04 | 1 | 5.54 ± 0.08 | 1120 | +52.7% | still slower | 0 |
| `path-65536` | wcc | full-width | concurrency as the run | second | +6.7% | 0.78 ± 0.01 | 132 | 0.67 ± 0.02 | 68 | -14.2% | faster than v0.22.0 | 0 |
| `uniform-16384` | bfs | full-width | concurrency as the run | first | +9.4% | 1.68 ± 0.04 | 36 | 1.84 ± 0.05 | 0 | +9.8% | still slower | 0 |
| `uniform-16384` | bfs | full-width | concurrency as the run | second | +2.5% | 1.47 ± 0.00 | 0 | 1.50 ± 0.01 | 0 | +2.3% | still slower | 0 |
| `uniform-16384` | pagerank | full-width | pull | second | +2.7% | 3.30 ± 0.05 | 1 | 3.33 ± 0.13 | 0 | +0.9% | within dispersion | 0 |
| `uniform-16384` | triangles | full-width | concurrency as the run | second | +13.3% | 6.49 ± 0.02 | 1 | 7.37 ± 0.05 | 512 | +13.6% | still slower | 0 |
| `uniform-65536` | triangles | full-width | concurrency as the run | second | +5.6% | 26.56 ± 0.07 | 1 | 28.66 ± 0.49 | 1026 | +7.9% | still slower | 0 |
| `hub-16384` | bfs | one-thread | concurrency 1 | first | +0.9% | 1.56 ± 0.00 | 36 | 1.59 ± 0.02 | 32 | +1.6% | still slower | 0 |
| `hub-16384` | bfs | one-thread | concurrency unset | first | +2.6% | 1.58 ± 0.02 | 36 | 1.60 ± 0.02 | 36 | +1.3% | within dispersion | 0 |
| `hub-16384` | bfs | one-thread | concurrency 1 | second | +0.0% | 1.44 ± 0.00 | 0 | 1.46 ± 0.00 | 0 | +1.6% | still slower | 0 |
| `hub-16384` | bfs | one-thread | concurrency unset | second | +0.2% | 1.44 ± 0.00 | 0 | 1.47 ± 0.00 | 0 | +2.2% | still slower | 0 |
| `hub-16384` | triangles | one-thread | concurrency 1 | second | +3.9% | 15.73 ± 0.03 | 32 | 16.44 ± 0.06 | 511 | +4.5% | still slower | 0 |
| `hub-16384` | triangles | one-thread | concurrency unset | second | +3.8% | 15.69 ± 0.02 | 32 | 16.33 ± 0.07 | 543 | +4.1% | still slower | 0 |
| `hub-65536` | bfs | one-thread | concurrency 1 | first | +6.0% | 7.73 ± 0.14 | 146 | 7.58 ± 0.39 | 130 | -2.0% | within dispersion | 0 |
| `hub-65536` | bfs | one-thread | concurrency unset | first | +6.1% | 9.60 ± 0.25 | 144 | 10.64 ± 0.58 | 144 | +10.8% | still slower | 0 |
| `hub-65536` | bfs | one-thread | concurrency 1 | second | +3.4% | 5.90 ± 0.11 | 0 | 6.20 ± 0.19 | 0 | +5.0% | within dispersion | 0 |
| `hub-65536` | bfs | one-thread | concurrency unset | second | +2.1% | 7.37 ± 0.26 | 0 | 8.08 ± 0.77 | 0 | +9.7% | within dispersion | 0 |
| `hub-65536` | triangles | one-thread | concurrency 1 | second | +2.6% | 77.93 ± 1.04 | 128 | 75.83 ± 1.42 | 1535 | -2.7% | within dispersion | 0 |
| `hub-65536` | triangles | one-thread | concurrency unset | second | +0.9% | 76.04 ± 0.80 | 128 | 76.58 ± 1.94 | 641 | +0.7% | within dispersion | 0 |
| `layered-16384` | pagerank | one-thread | pull | first | +2.2% | 30.23 ± 0.01 | 192 | 30.86 ± 0.03 | 96 | +2.1% | still slower | 0 |
| `layered-16384` | pagerank | one-thread | pull | second | +4.1% | 29.35 ± 0.01 | 0 | 30.65 ± 0.01 | 0 | +4.4% | still slower | 0 |
| `layered-16384` | triangles | one-thread | concurrency 1 | second | +16.3% | 2.21 ± 0.01 | 32 | 2.59 ± 0.00 | 350 | +17.0% | still slower | 0 |
| `layered-16384` | triangles | one-thread | concurrency unset | second | +3.9% | 2.22 ± 0.00 | 32 | 2.32 ± 0.01 | 159 | +4.4% | still slower | 0 |
| `layered-16384` | wcc | one-thread | concurrency 1 | first | +10.1% | 0.63 ± 0.00 | 32 | 0.69 ± 0.00 | 32 | +9.5% | still slower | 0 |
| `layered-65536` | pagerank | one-thread | pull | first | +2.4% | 108.93 ± 0.15 | 766 | 112.30 ± 0.20 | 384 | +3.1% | still slower | 0 |
| `layered-65536` | pagerank | one-thread | pull | second | +5.1% | 105.20 ± 0.09 | 0 | 110.90 ± 0.14 | 0 | +5.4% | still slower | 0 |
| `layered-65536` | triangles | one-thread | concurrency 1 | second | +18.8% | 8.98 ± 0.05 | 128 | 11.02 ± 0.31 | 1497 | +22.7% | still slower | 0 |
| `layered-65536` | triangles | one-thread | concurrency unset | second | +4.5% | 8.96 ± 0.02 | 128 | 10.26 ± 0.14 | 635 | +14.5% | still slower | 0 |
| `layered-65536` | wcc | one-thread | concurrency 1 | first | +11.0% | 2.56 ± 0.01 | 128 | 2.81 ± 0.01 | 128 | +9.7% | still slower | 0 |
| `path-16384` | triangles | one-thread | concurrency 1 | first | +2.7% | 1.54 ± 0.01 | 256 | 1.58 ± 0.01 | 256 | +2.2% | still slower | 0 |
| `path-16384` | triangles | one-thread | concurrency 1 | second | +28.2% | 1.09 ± 0.00 | 32 | 1.42 ± 0.01 | 256 | +30.3% | still slower | 0 |
| `path-16384` | wcc | one-thread | concurrency 1 | first | +4.2% | 0.45 ± 0.00 | 32 | 0.45 ± 0.00 | 32 | +0.5% | within dispersion | 0 |
| `path-16384` | wcc | one-thread | concurrency unset | second | +1.0% | 1.00 ± 0.01 | 31 | 0.95 ± 0.00 | 16 | -5.5% | faster than v0.22.0 | 0 |
| `path-65536` | pagerank | one-thread | pull | second | +1.5% | 51.14 ± 0.12 | 0 | 52.04 ± 0.07 | 352 | +1.8% | still slower | 0 |
| `path-65536` | triangles | one-thread | concurrency 1 | first | +0.6% | 6.23 ± 0.07 | 1024 | 6.34 ± 0.03 | 1024 | +1.8% | still slower | 0 |
| `path-65536` | triangles | one-thread | concurrency unset | first | +0.6% | 6.24 ± 0.03 | 1025 | 6.30 ± 0.02 | 1024 | +1.0% | still slower | 0 |
| `path-65536` | triangles | one-thread | concurrency 1 | second | +34.0% | 4.39 ± 0.01 | 128 | 6.10 ± 0.09 | 1120 | +39.2% | still slower | 0 |
| `path-65536` | wcc | one-thread | concurrency 1 | first | +0.9% | 1.80 ± 0.00 | 128 | 1.83 ± 0.01 | 128 | +1.9% | still slower | 0 |
| `path-65536` | wcc | one-thread | concurrency unset | second | +2.4% | 4.03 ± 0.02 | 126 | 3.88 ± 0.02 | 64 | -3.8% | faster than v0.22.0 | 0 |
| `uniform-16384` | bfs | one-thread | concurrency 1 | first | +1.0% | 1.63 ± 0.02 | 36 | 1.66 ± 0.03 | 32 | +1.8% | within dispersion | 0 |
| `uniform-16384` | bfs | one-thread | concurrency unset | first | +2.8% | 1.67 ± 0.04 | 36 | 1.75 ± 0.05 | 36 | +5.0% | still slower | 0 |
| `uniform-16384` | triangles | one-thread | concurrency 1 | second | +4.1% | 17.19 ± 0.05 | 32 | 17.82 ± 0.13 | 512 | +3.7% | still slower | 1 |
| `uniform-16384` | triangles | one-thread | concurrency unset | second | +3.9% | 17.17 ± 0.02 | 32 | 17.82 ± 0.04 | 544 | +3.8% | still slower | 1 |
| `uniform-16384` | wcc | one-thread | concurrency 1 | first | +13.6% | 2.07 ± 0.01 | 32 | 2.35 ± 0.01 | 32 | +13.7% | still slower | 0 |
| `uniform-16384` | wcc | one-thread | concurrency 1 | second | +0.5% | 2.29 ± 0.00 | 31 | 2.30 ± 0.00 | 16 | +0.7% | still slower | 0 |
| `uniform-65536` | bfs | one-thread | concurrency 1 | first | +3.8% | 8.60 ± 0.17 | 209 | 8.28 ± 0.55 | 134 | -3.8% | within dispersion | 0 |
| `uniform-65536` | bfs | one-thread | concurrency unset | first | +6.7% | 9.72 ± 0.30 | 144 | 10.32 ± 0.19 | 144 | +6.1% | still slower | 0 |
| `uniform-65536` | bfs | one-thread | concurrency 1 | second | +1.5% | 6.63 ± 0.19 | 0 | 7.18 ± 0.27 | 0 | +8.2% | still slower | 0 |
| `uniform-65536` | bfs | one-thread | concurrency unset | second | +1.4% | 7.59 ± 0.48 | 0 | 8.05 ± 0.42 | 0 | +6.2% | within dispersion | 0 |
| `uniform-65536` | triangles | one-thread | concurrency 1 | second | +2.4% | 82.22 ± 0.98 | 128 | 86.47 ± 1.25 | 1537 | +5.2% | still slower | 0 |
| `uniform-65536` | triangles | one-thread | concurrency unset | second | +0.1% | 79.80 ± 0.24 | 128 | 83.88 ± 0.64 | 1154 | +5.1% | still slower | 0 |
| `uniform-65536` | wcc | one-thread | concurrency 1 | first | +10.5% | 9.36 ± 0.05 | 128 | 10.39 ± 0.02 | 128 | +11.0% | still slower | 0 |
| `uniform-65536` | wcc | one-thread | concurrency 1 | second | +4.0% | 9.83 ± 0.07 | 128 | 10.25 ± 0.09 | 64 | +4.3% | still slower | 0 |

Of the still-slower cells, by shape: triangles second call 20; bfs second call 5; BFS first call 5; WCC first call at concurrency 1 5; pagerank second call 3; triangles first call 3; PageRank on `path` 2; pagerank first call 2; wcc second call 2.

### The one-worker WCC residue

WCC's first call, concurrency 1 at one thread and as the run at full width,
with B5's ratio beside B6's. The commit's own measurement found this residue
responds to the chunk size class of the balance and not to its cache line, and
did not find why; this campaign measures it under the protocol and does not
explain it either.

| fixture | run | kernel | v0.22.0 | faults | `87fc462` | faults | change | B5 said | standing | steal |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| `hub-16384` | one-thread | concurrency 1 | 1.56 ± 0.01 | 32 | 1.50 ± 0.00 | 32 | -3.7% | -3.9% | faster than v0.22.0 | 0 |
| `hub-65536` | one-thread | concurrency 1 | 7.12 ± 0.01 | 128 | 6.99 ± 0.07 | 128 | -1.8% | -3.0% | faster than v0.22.0 | 0 |
| `layered-16384` | one-thread | concurrency 1 | 0.63 ± 0.00 | 32 | 0.69 ± 0.00 | 32 | +9.5% | +10.1% | still slower | 0 |
| `layered-65536` | one-thread | concurrency 1 | 2.56 ± 0.01 | 128 | 2.81 ± 0.01 | 128 | +9.7% | +11.0% | still slower | 0 |
| `path-16384` | one-thread | concurrency 1 | 0.45 ± 0.00 | 32 | 0.45 ± 0.00 | 32 | +0.5% | +4.2% | within dispersion | 0 |
| `path-65536` | one-thread | concurrency 1 | 1.80 ± 0.00 | 128 | 1.83 ± 0.01 | 128 | +1.9% | +0.9% | still slower | 0 |
| `uniform-16384` | one-thread | concurrency 1 | 2.07 ± 0.01 | 32 | 2.35 ± 0.01 | 32 | +13.7% | +13.6% | still slower | 0 |
| `uniform-65536` | one-thread | concurrency 1 | 9.36 ± 0.05 | 128 | 10.39 ± 0.02 | 128 | +11.0% | +10.5% | still slower | 0 |
| `hub-16384` | full-width | concurrency as the run | 1.31 ± 0.02 | 142 | 0.49 ± 0.03 | 3 | -62.8% | -59.4% | faster than v0.22.0 | 0 |
| `hub-65536` | full-width | concurrency as the run | 2.53 ± 0.01 | 241 | 1.62 ± 0.05 | 3 | -35.8% | -38.0% | faster than v0.22.0 | 0 |
| `layered-16384` | full-width | concurrency as the run | 1.06 ± 0.01 | 140 | 0.38 ± 0.00 | 35 | -64.6% | -61.3% | faster than v0.22.0 | 0 |
| `layered-65536` | full-width | concurrency as the run | 1.60 ± 0.02 | 241 | 0.90 ± 0.01 | 132 | -43.8% | -40.8% | faster than v0.22.0 | 0 |
| `path-16384` | full-width | concurrency as the run | 1.00 ± 0.01 | 137 | 0.31 ± 0.01 | 35 | -68.9% | -49.4% | faster than v0.22.0 | 0 |
| `path-65536` | full-width | concurrency as the run | 1.52 ± 0.00 | 241 | 0.82 ± 0.01 | 132 | -45.9% | -26.8% | faster than v0.22.0 | 0 |
| `uniform-16384` | full-width | concurrency as the run | 1.51 ± 0.04 | 140 | 0.60 ± 0.01 | 4 | -60.1% | -56.4% | faster than v0.22.0 | 0 |
| `uniform-65536` | full-width | concurrency as the run | 2.68 ± 0.06 | 241 | 1.91 ± 0.11 | 6 | -28.7% | -33.7% | faster than v0.22.0 | 0 |

At one thread, concurrency 1, WCC's first call on `87fc462` is slower than v0.22.0 on 6 of 8 fixtures, -3.7% to +13.7%; 5 of those are beyond the dispersion margin, and the page-fault counts are equal on 8 of 8. **Unexplained.**

### The two items B5 left open

**Counted BFS on the first call.** The last two columns are what the same
cell said in B5 and where it stands now.

| fixture | run | kernel | v0.22.0 | faults | `87fc462` | faults | change | B5 said | standing |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `hub-16384` | one-thread | concurrency 1 | 1.56 ± 0.00 | 36 | 1.59 ± 0.02 | 32 | +1.6% | +0.9% | still slower |
| `hub-16384` | one-thread | concurrency unset | 1.58 ± 0.02 | 36 | 1.60 ± 0.02 | 36 | +1.3% | +2.6% | within dispersion |
| `hub-65536` | one-thread | concurrency 1 | 7.73 ± 0.14 | 146 | 7.58 ± 0.39 | 130 | -2.0% | +6.0% | within dispersion |
| `hub-65536` | one-thread | concurrency unset | 9.60 ± 0.25 | 144 | 10.64 ± 0.58 | 144 | +10.8% | +6.1% | still slower |
| `uniform-16384` | one-thread | concurrency 1 | 1.63 ± 0.02 | 36 | 1.66 ± 0.03 | 32 | +1.8% | +1.0% | within dispersion |
| `uniform-16384` | one-thread | concurrency unset | 1.67 ± 0.04 | 36 | 1.75 ± 0.05 | 36 | +5.0% | +2.8% | still slower |
| `uniform-65536` | one-thread | concurrency 1 | 8.60 ± 0.17 | 209 | 8.28 ± 0.55 | 134 | -3.8% | +3.8% | within dispersion |
| `uniform-65536` | one-thread | concurrency unset | 9.72 ± 0.30 | 144 | 10.32 ± 0.19 | 144 | +6.1% | +6.7% | still slower |
| `hub-16384` | full-width | concurrency as the run | 1.57 ± 0.03 | 36 | 1.58 ± 0.04 | 0 | +0.7% | +1.4% | within dispersion |
| `hub-65536` | full-width | concurrency as the run | 4.30 ± 0.23 | 396 | 3.33 ± 0.03 | 118 | -22.6% | -22.0% | faster than v0.22.0 |
| `uniform-16384` | full-width | concurrency as the run | 1.68 ± 0.04 | 36 | 1.84 ± 0.05 | 0 | +9.8% | +9.4% | still slower |
| `uniform-65536` | full-width | concurrency as the run | 4.43 ± 0.13 | 315 | 3.42 ± 0.04 | 116 | -22.9% | -22.2% | faster than v0.22.0 |

At one-thread, 6 of 8 `hub` and `uniform` first-call cells are slower than v0.22.0, -3.8% to +10.8%, 4 of them beyond dispersion. At full-width, 2 of 4 `hub` and `uniform` first-call cells are slower than v0.22.0, -22.9% to +9.8%, 1 of them beyond dispersion.

**PageRank on `layered-16384` at sixteen threads.** The full-width run's
`layered-16384` rows are: first call -5.8%, faster than v0.22.0; second call +4.3%, still slower.

| fixture | run | kernel | call | v0.22.0 | `87fc462` | change | B5 said | standing | steal |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- | ---: |
| `layered-16384` | one-thread | pull | first | 30.23 ± 0.01 | 30.86 ± 0.03 | +2.1% | +2.2% | still slower | 0 |
| `layered-16384` | one-thread | pull | second | 29.35 ± 0.01 | 30.65 ± 0.01 | +4.4% | +4.1% | still slower | 0 |
| `layered-16384` | one-thread | push | first | 115.73 ± 0.05 | 89.61 ± 0.13 | -22.6% | -23.1% | faster than v0.22.0 | 0 |
| `layered-16384` | one-thread | push | second | 115.94 ± 0.50 | 88.68 ± 0.09 | -23.5% | -23.2% | faster than v0.22.0 | 0 |
| `layered-65536` | one-thread | pull | first | 108.93 ± 0.15 | 112.30 ± 0.20 | +3.1% | +2.4% | still slower | 0 |
| `layered-65536` | one-thread | pull | second | 105.20 ± 0.09 | 110.90 ± 0.14 | +5.4% | +5.1% | still slower | 0 |
| `layered-65536` | one-thread | push | first | 415.65 ± 0.73 | 319.23 ± 0.44 | -23.2% | -23.1% | faster than v0.22.0 | 0 |
| `layered-65536` | one-thread | push | second | 414.62 ± 0.05 | 318.24 ± 0.19 | -23.2% | -23.0% | faster than v0.22.0 | 0 |
| `layered-16384` | full-width | pull | first | 15.66 ± 0.05 | 14.75 ± 0.14 | -5.8% | -2.7% | faster than v0.22.0 | 0 |
| `layered-16384` | full-width | pull | second | 13.83 ± 0.32 | 14.42 ± 0.17 | +4.3% | +5.8% | still slower | 0 |
| `layered-65536` | full-width | pull | first | 25.84 ± 0.11 | 21.06 ± 0.10 | -18.5% | -17.2% | faster than v0.22.0 | 0 |
| `layered-65536` | full-width | pull | second | 21.55 ± 0.33 | 20.46 ± 0.56 | -5.0% | -4.8% | faster than v0.22.0 | 0 |

### What the accounting guarantee costs

`grust-next`, first call, by mode, beside `neo4j-graph`, which performs no
accounting and is `f32` on its own stopping rule.

| fixture | run | kernel | counted | work-uncounted | unchecked | `neo4j-graph` | steal |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `hub-65536` | one-thread | pagerank, pull | 35.21 ± 0.23 | 33.14 ± 0.10 | 32.41 ± 0.27 | 37.65 ± 0.13 | 0 |
| `hub-65536` | one-thread | pagerank, push | 96.40 ± 0.39 | 58.94 ± 0.16 | 57.39 ± 1.06 | 37.65 ± 0.13 | 0 |
| `hub-65536` | one-thread | wcc, concurrency 1 | 6.99 ± 0.07 | 5.03 ± 0.04 | 4.64 ± 0.03 | 3.82 ± 0.01 | 0 |
| `hub-65536` | one-thread | wcc, concurrency unset | 17.00 ± 0.00 | 7.96 ± 0.07 | 6.83 ± 0.09 | 3.82 ± 0.01 | 0 |
| `hub-65536` | one-thread | triangles, concurrency 1 | 78.08 ± 2.25 | 78.75 ± 2.61 | 78.22 ± 1.21 | 38.74 ± 1.00 | 0 |
| `hub-65536` | one-thread | triangles, concurrency unset | 78.80 ± 1.26 | 77.60 ± 0.17 | 78.14 ± 0.86 | 38.74 ± 1.00 | 0 |
| `uniform-65536` | one-thread | pagerank, pull | 32.86 ± 0.37 | 31.06 ± 0.43 | 30.12 ± 0.22 | 45.66 ± 0.31 | 0 |
| `uniform-65536` | one-thread | pagerank, push | 89.76 ± 0.35 | 55.68 ± 1.20 | 54.70 ± 0.52 | 45.66 ± 0.31 | 0 |
| `uniform-65536` | one-thread | wcc, concurrency 1 | 10.39 ± 0.02 | 9.10 ± 0.06 | 8.53 ± 0.04 | 3.81 ± 0.01 | 0 |
| `uniform-65536` | one-thread | wcc, concurrency unset | 17.39 ± 0.02 | 8.81 ± 0.14 | 7.59 ± 0.19 | 3.81 ± 0.01 | 0 |
| `uniform-65536` | one-thread | triangles, concurrency 1 | 87.90 ± 0.24 | 84.51 ± 0.39 | 81.81 ± 2.10 | 43.22 ± 0.85 | 0 |
| `uniform-65536` | one-thread | triangles, concurrency unset | 84.66 ± 0.68 | 85.12 ± 0.84 | 82.98 ± 1.28 | 43.22 ± 0.85 | 0 |
| `hub-65536` | full-width | pagerank, pull | 7.27 ± 0.14 | 5.02 ± 0.11 | 4.87 ± 0.10 | 15.18 ± 0.90 | 0 |
| `hub-65536` | full-width | wcc, concurrency as the run | 1.62 ± 0.05 | 1.33 ± 0.02 | 1.31 ± 0.15 | 3.12 ± 0.04 | 0 |
| `hub-65536` | full-width | triangles, concurrency as the run | 29.38 ± 0.17 | 28.21 ± 0.22 | 28.03 ± 0.20 | 3.65 ± 0.03 | 0 |
| `uniform-65536` | full-width | pagerank, pull | 7.02 ± 0.09 | 4.58 ± 0.02 | 4.52 ± 0.10 | 16.42 ± 0.12 | 0 |
| `uniform-65536` | full-width | wcc, concurrency as the run | 1.91 ± 0.11 | 1.54 ± 0.11 | 1.72 ± 0.05 | 3.61 ± 0.17 | 0 |
| `uniform-65536` | full-width | triangles, concurrency as the run | 28.92 ± 0.12 | 28.13 ± 0.24 | 28.28 ± 0.06 | 4.06 ± 0.12 | 0 |
| `hub-2097152` | large-one-thread | pagerank, pull | 3859.96 ± 2.75 | 3658.76 ± 72.12 | 3522.52 ± 66.73 | 2799.31 ± 14.78 | 5 |
| `hub-2097152` | large-one-thread | pagerank, push | 7310.90 ± 133.02 | 5932.34 ± 97.08 | 5925.81 ± 42.85 | 2799.31 ± 14.78 | 5 |
| `uniform-2097152` | large-one-thread | pagerank, pull | 3821.94 ± 99.41 | 3781.66 ± 156.43 | 3610.51 ± 272.06 | 2743.32 ± 60.24 | 5 |
| `uniform-2097152` | large-one-thread | pagerank, push | 6961.88 ± 126.42 | 5649.18 ± 291.57 | 5656.10 ± 147.64 | 2743.32 ± 60.24 | 5 |
| `hub-2097152` | large-full-width | pagerank, pull | 278.46 ± 2.12 | 256.36 ± 16.47 | 240.62 ± 1.85 | 277.25 ± 1.97 | 2 |
| `uniform-2097152` | large-full-width | pagerank, pull | 275.17 ± 3.47 | 258.63 ± 15.61 | 250.92 ± 5.43 | 284.00 ± 3.72 | 1 |
| `hub-4194304` | xlarge-one-thread | pagerank, pull | 8695.93 ± 24.39 | 8472.43 ± 101.71 | 8058.38 ± 69.09 | 6991.53 ± 176.59 | 11 |
| `hub-4194304` | xlarge-one-thread | pagerank, push | 15647.71 ± 133.88 | 13012.93 ± 35.06 | 12983.58 ± 130.98 | 6991.53 ± 176.59 | 11 |
| `uniform-4194304` | xlarge-one-thread | pagerank, pull | 9001.38 ± 40.23 | 8836.78 ± 54.05 | 8452.58 ± 44.06 | 9137.71 ± 260.54 | 10 |
| `uniform-4194304` | xlarge-one-thread | pagerank, push | 15124.71 ± 144.47 | 12422.13 ± 13.69 | 12418.80 ± 121.39 | 9137.71 ± 260.54 | 10 |
| `hub-4194304` | xlarge-full-width | pagerank, pull | 792.73 ± 38.46 | 772.11 ± 41.04 | 749.20 ± 27.73 | 416.49 ± 0.58 | 3 |
| `uniform-4194304` | xlarge-full-width | pagerank, pull | 871.10 ± 9.45 | 877.40 ± 3.12 | 857.59 ± 15.76 | 651.10 ± 26.70 | 4 |

Counting also costs in the build: `grust-next`'s `build_ms` for PageRank on `hub-65536` at one thread is 51.66 ms counted, 44.95 work-uncounted and 45.35 unchecked.

### B5 against B6 on unchanged code

The participants that did not change between the two campaigns, one thread,
first call, on the same host on the same day. A B6 cell is compared only with
other cells of the same B6 run; this table is the size of the drift between
campaigns, not a correction to either.

| fixture | algorithm | participant | B5 | B6 | change |
| --- | --- | --- | ---: | ---: | ---: |
| `hub-65536` | pagerank | `grust#1` | 52.59 ± 0.21 | 68.11 ± 2.53 | +29.5% |
| `hub-65536` | wcc | `grust#1` | 6.66 ± 0.01 | 7.12 ± 0.01 | +6.9% |
| `uniform-65536` | pagerank | `grust#1` | 51.51 ± 0.43 | 60.82 ± 3.60 | +18.1% |
| `uniform-65536` | wcc | `grust#1` | 8.88 ± 0.05 | 9.36 ± 0.05 | +5.5% |
| `hub-65536` | pagerank | `grust#unset` | 203.55 ± 0.34 | 205.29 ± 0.31 | +0.9% |
| `hub-65536` | wcc | `grust#unset` | 16.88 ± 0.01 | 17.19 ± 0.01 | +1.8% |
| `uniform-65536` | pagerank | `grust#unset` | 192.34 ± 0.36 | 194.71 ± 0.52 | +1.2% |
| `uniform-65536` | wcc | `grust#unset` | 17.08 ± 0.05 | 17.44 ± 0.03 | +2.1% |
| `hub-65536` | pagerank | `icecat` | 34.12 ± 0.01 | 35.02 ± 0.04 | +2.6% |
| `hub-65536` | wcc | `icecat` | 3.48 ± 0.22 | 3.30 ± 0.01 | -5.2% |
| `uniform-65536` | pagerank | `icecat` | 32.69 ± 0.02 | 33.54 ± 0.61 | +2.6% |
| `uniform-65536` | wcc | `icecat` | 4.02 ± 0.07 | 4.45 ± 0.07 | +10.7% |
| `hub-65536` | pagerank | `grustcat` | 30.23 ± 0.03 | 32.59 ± 0.38 | +7.8% |
| `hub-65536` | wcc | `grustcat` | 2.44 ± 0.01 | 2.52 ± 0.03 | +3.1% |
| `uniform-65536` | pagerank | `grustcat` | 29.27 ± 0.12 | 30.88 ± 0.28 | +5.5% |
| `uniform-65536` | wcc | `grustcat` | 3.05 ± 0.04 | 3.11 ± 0.00 | +2.1% |
| `hub-65536` | pagerank | `neo4j-graph` | 35.93 ± 0.14 | 37.65 ± 0.13 | +4.8% |
| `hub-65536` | wcc | `neo4j-graph` | 3.75 ± 0.01 | 3.82 ± 0.01 | +1.7% |
| `uniform-65536` | pagerank | `neo4j-graph` | 44.24 ± 0.08 | 45.66 ± 0.31 | +3.2% |
| `uniform-65536` | wcc | `neo4j-graph` | 3.75 ± 0.00 | 3.81 ± 0.01 | +1.7% |
| `hub-65536` | pagerank | `icebug` | 42.13 ± 0.80 | 73.66 ± 4.05 | +74.8% |
| `hub-65536` | wcc | `icebug` | 11.25 ± 0.41 | 21.58 ± 0.39 | +91.9% |
| `uniform-65536` | pagerank | `icebug` | 39.50 ± 0.78 | 63.38 ± 5.24 | +60.5% |
| `uniform-65536` | wcc | `icebug` | 12.83 ± 0.08 | 25.98 ± 0.20 | +102.6% |

The same binaries' sources, on the same fixtures and the same host, move -5.2% to +102.6% between B5 and B6, a median of +4.0%; by participant, `grust#1` +5.5% to +29.5%; `grust#unset` +0.9% to +2.1%; `icecat` -5.2% to +10.7%; `grustcat` +2.1% to +7.8%; `neo4j-graph` +1.7% to +4.8%; `icebug` +60.5% to +102.6%. B4 to B5 moved -49.6% to +8.1%, and the participant that moved most then, `icebug`, is the one that moves most now, the other way. Both campaigns were built from clean trees on the host, dropped the page cache before timing and ran on an idle host on the same day. A cell is still only ever compared with other cells of its own run; the B5 columns in the tables above are B5's own ratios, not B5 times against B6 times.

**Above L3, every participant.** PageRank at 2,097,152 and 4,194,304 nodes,
first call, every participant of each run, B5 beside B6. This is the drift
the kernel-change table's large and xlarge rows sit on.

| fixture | run | participant | B5 | B6 | change | steal B5 | steal B6 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `hub-2097152` | large-one-thread | `neo4j-graph` | 2091.59 ± 5.88 | 2799.31 ± 14.78 | +33.8% | 3 | 5 |
| `hub-2097152` | large-one-thread | `icebug` | 4305.74 ± 358.39 | 5183.16 ± 63.78 | +20.4% | 3 | 5 |
| `hub-2097152` | large-one-thread | `icecat` | 1713.81 ± 21.95 | 3050.72 ± 95.92 | +78.0% | 3 | 5 |
| `hub-2097152` | large-one-thread | `grustcat` | 1946.08 ± 46.23 | 3310.95 ± 24.32 | +70.1% | 3 | 5 |
| `hub-2097152` | large-one-thread | `grust#1` | 4987.08 ± 70.65 | 6581.11 ± 71.46 | +32.0% | 3 | 5 |
| `hub-2097152` | large-one-thread | `grust#unset` | 7810.23 ± 196.88 | 17228.60 ± 33.90 | +120.6% | 3 | 5 |
| `hub-2097152` | large-one-thread | `grust-next@counted#1` | 2170.69 ± 43.13 | 3859.96 ± 2.75 | +77.8% | 3 | 5 |
| `hub-2097152` | large-one-thread | `grust-next@work-uncounted#1` | 2013.59 ± 101.38 | 3658.76 ± 72.12 | +81.7% | 3 | 5 |
| `hub-2097152` | large-one-thread | `grust-next@unchecked#1` | 1935.46 ± 322.66 | 3522.52 ± 66.73 | +82.0% | 3 | 5 |
| `hub-2097152` | large-one-thread | `grust-next@counted#unset` | 4025.06 ± 132.51 | 7310.90 ± 133.02 | +81.6% | 3 | 5 |
| `hub-2097152` | large-one-thread | `grust-next@work-uncounted#unset` | 3436.31 ± 43.29 | 5932.34 ± 97.08 | +72.6% | 3 | 5 |
| `hub-2097152` | large-one-thread | `grust-next@unchecked#unset` | 2917.49 ± 44.54 | 5925.81 ± 42.85 | +103.1% | 3 | 5 |
| `uniform-2097152` | large-one-thread | `neo4j-graph` | 2162.61 ± 19.69 | 2743.32 ± 60.24 | +26.9% | 4 | 5 |
| `uniform-2097152` | large-one-thread | `icebug` | 4140.89 ± 40.40 | 5312.45 ± 138.11 | +28.3% | 4 | 5 |
| `uniform-2097152` | large-one-thread | `icecat` | 2063.81 ± 324.69 | 3081.58 ± 62.09 | +49.3% | 4 | 5 |
| `uniform-2097152` | large-one-thread | `grustcat` | 2399.05 ± 35.57 | 3836.22 ± 12.17 | +59.9% | 4 | 5 |
| `uniform-2097152` | large-one-thread | `grust#1` | 5186.50 ± 59.96 | 6999.18 ± 112.79 | +35.0% | 4 | 5 |
| `uniform-2097152` | large-one-thread | `grust#unset` | 7639.66 ± 159.36 | 17040.90 ± 206.43 | +123.1% | 4 | 5 |
| `uniform-2097152` | large-one-thread | `grust-next@counted#1` | 2207.80 ± 62.26 | 3821.94 ± 99.41 | +73.1% | 4 | 5 |
| `uniform-2097152` | large-one-thread | `grust-next@work-uncounted#1` | 1791.58 ± 24.65 | 3781.66 ± 156.43 | +111.1% | 4 | 5 |
| `uniform-2097152` | large-one-thread | `grust-next@unchecked#1` | 1968.11 ± 30.86 | 3610.51 ± 272.06 | +83.5% | 4 | 5 |
| `uniform-2097152` | large-one-thread | `grust-next@counted#unset` | 4023.10 ± 11.14 | 6961.88 ± 126.42 | +73.0% | 4 | 5 |
| `uniform-2097152` | large-one-thread | `grust-next@work-uncounted#unset` | 3184.51 ± 89.67 | 5649.18 ± 291.57 | +77.4% | 4 | 5 |
| `uniform-2097152` | large-one-thread | `grust-next@unchecked#unset` | 3133.06 ± 182.93 | 5656.10 ± 147.64 | +80.5% | 4 | 5 |
| `hub-2097152` | large-full-width | `neo4j-graph` | 260.04 ± 1.68 | 277.25 ± 1.97 | +6.6% | 1 | 2 |
| `hub-2097152` | large-full-width | `icebug` | 455.57 ± 6.23 | 518.72 ± 7.09 | +13.9% | 1 | 2 |
| `hub-2097152` | large-full-width | `icecat` | 1713.89 ± 3.47 | 3147.45 ± 26.40 | +83.6% | 1 | 2 |
| `hub-2097152` | large-full-width | `grustcat` | 2161.98 ± 199.82 | 3292.03 ± 63.31 | +52.3% | 1 | 2 |
| `hub-2097152` | large-full-width | `grust` | 1084.33 ± 7.68 | 1385.34 ± 22.93 | +27.8% | 1 | 2 |
| `hub-2097152` | large-full-width | `grust-next@counted` | 274.75 ± 15.17 | 278.46 ± 2.12 | +1.3% | 1 | 2 |
| `hub-2097152` | large-full-width | `grust-next@work-uncounted` | 219.87 ± 5.69 | 256.36 ± 16.47 | +16.6% | 1 | 2 |
| `hub-2097152` | large-full-width | `grust-next@unchecked` | 209.83 ± 0.64 | 240.62 ± 1.85 | +14.7% | 1 | 2 |
| `uniform-2097152` | large-full-width | `neo4j-graph` | 262.94 ± 2.50 | 284.00 ± 3.72 | +8.0% | 2 | 1 |
| `uniform-2097152` | large-full-width | `icebug` | 483.90 ± 8.91 | 555.11 ± 28.87 | +14.7% | 2 | 1 |
| `uniform-2097152` | large-full-width | `icecat` | 2005.72 ± 109.56 | 3121.82 ± 32.92 | +55.6% | 2 | 1 |
| `uniform-2097152` | large-full-width | `grustcat` | 2640.27 ± 28.74 | 3850.63 ± 43.42 | +45.8% | 2 | 1 |
| `uniform-2097152` | large-full-width | `grust` | 1131.94 ± 8.18 | 1375.91 ± 31.94 | +21.6% | 2 | 1 |
| `uniform-2097152` | large-full-width | `grust-next@counted` | 248.59 ± 6.98 | 275.17 ± 3.47 | +10.7% | 2 | 1 |
| `uniform-2097152` | large-full-width | `grust-next@work-uncounted` | 228.12 ± 3.92 | 258.63 ± 15.61 | +13.4% | 2 | 1 |
| `uniform-2097152` | large-full-width | `grust-next@unchecked` | 226.02 ± 1.64 | 250.92 ± 5.43 | +11.0% | 2 | 1 |
| `hub-4194304` | xlarge-one-thread | `neo4j-graph` | 4610.20 ± 513.82 | 6991.53 ± 176.59 | +51.7% | 121 | 11 |
| `hub-4194304` | xlarge-one-thread | `icebug` | 9735.12 ± 74.54 | 11825.67 ± 206.46 | +21.5% | 121 | 11 |
| `hub-4194304` | xlarge-one-thread | `icecat` | 5627.61 ± 16.79 | 7064.36 ± 28.88 | +25.5% | 121 | 11 |
| `hub-4194304` | xlarge-one-thread | `grustcat` | 6040.22 ± 40.65 | 7349.00 ± 45.76 | +21.7% | 121 | 11 |
| `hub-4194304` | xlarge-one-thread | `grust#1` | 12663.28 ± 36.71 | 14778.23 ± 100.50 | +16.7% | 121 | 11 |
| `hub-4194304` | xlarge-one-thread | `grust#unset` | 26184.63 ± 328.74 | 35911.29 ± 191.93 | +37.1% | 121 | 11 |
| `hub-4194304` | xlarge-one-thread | `grust-next@counted#1` | 6941.34 ± 23.40 | 8695.93 ± 24.39 | +25.3% | 121 | 11 |
| `hub-4194304` | xlarge-one-thread | `grust-next@work-uncounted#1` | 6696.58 ± 21.59 | 8472.43 ± 101.71 | +26.5% | 121 | 11 |
| `hub-4194304` | xlarge-one-thread | `grust-next@unchecked#1` | 6493.19 ± 37.52 | 8058.38 ± 69.09 | +24.1% | 121 | 11 |
| `hub-4194304` | xlarge-one-thread | `grust-next@counted#unset` | 13050.81 ± 144.21 | 15647.71 ± 133.88 | +19.9% | 121 | 11 |
| `hub-4194304` | xlarge-one-thread | `grust-next@work-uncounted#unset` | 10628.13 ± 52.99 | 13012.93 ± 35.06 | +22.4% | 121 | 11 |
| `hub-4194304` | xlarge-one-thread | `grust-next@unchecked#unset` | 10623.61 ± 256.95 | 12983.58 ± 130.98 | +22.2% | 121 | 11 |
| `uniform-4194304` | xlarge-one-thread | `neo4j-graph` | 5387.87 ± 359.63 | 9137.71 ± 260.54 | +69.6% | 8 | 10 |
| `uniform-4194304` | xlarge-one-thread | `icebug` | 9144.45 ± 104.25 | 11464.33 ± 235.68 | +25.4% | 8 | 10 |
| `uniform-4194304` | xlarge-one-thread | `icecat` | 5853.91 ± 22.44 | 7517.19 ± 19.79 | +28.4% | 8 | 10 |
| `uniform-4194304` | xlarge-one-thread | `grustcat` | 7113.24 ± 94.56 | 8617.93 ± 93.54 | +21.2% | 8 | 10 |
| `uniform-4194304` | xlarge-one-thread | `grust#1` | 13286.45 ± 45.87 | 15671.38 ± 112.88 | +18.0% | 8 | 10 |
| `uniform-4194304` | xlarge-one-thread | `grust#unset` | 24235.23 ± 476.78 | 35726.69 ± 89.21 | +47.4% | 8 | 10 |
| `uniform-4194304` | xlarge-one-thread | `grust-next@counted#1` | 7030.83 ± 59.57 | 9001.38 ± 40.23 | +28.0% | 8 | 10 |
| `uniform-4194304` | xlarge-one-thread | `grust-next@work-uncounted#1` | 6737.94 ± 17.02 | 8836.78 ± 54.05 | +31.1% | 8 | 10 |
| `uniform-4194304` | xlarge-one-thread | `grust-next@unchecked#1` | 6604.33 ± 13.99 | 8452.58 ± 44.06 | +28.0% | 8 | 10 |
| `uniform-4194304` | xlarge-one-thread | `grust-next@counted#unset` | 12327.00 ± 48.97 | 15124.71 ± 144.47 | +22.7% | 8 | 10 |
| `uniform-4194304` | xlarge-one-thread | `grust-next@work-uncounted#unset` | 10187.56 ± 121.81 | 12422.13 ± 13.69 | +21.9% | 8 | 10 |
| `uniform-4194304` | xlarge-one-thread | `grust-next@unchecked#unset` | 10020.11 ± 338.23 | 12418.80 ± 121.39 | +23.9% | 8 | 10 |
| `hub-4194304` | xlarge-full-width | `neo4j-graph` | 388.19 ± 36.49 | 416.49 ± 0.58 | +7.3% | 4 | 3 |
| `hub-4194304` | xlarge-full-width | `icebug` | 1089.02 ± 2.76 | 1192.34 ± 5.14 | +9.5% | 4 | 3 |
| `hub-4194304` | xlarge-full-width | `icecat` | 5549.37 ± 15.72 | 6956.02 ± 125.06 | +25.3% | 4 | 3 |
| `hub-4194304` | xlarge-full-width | `grustcat` | 5934.81 ± 32.05 | 7494.99 ± 66.69 | +26.3% | 4 | 3 |
| `hub-4194304` | xlarge-full-width | `grust` | 2780.12 ± 7.49 | 3136.15 ± 52.84 | +12.8% | 4 | 3 |
| `hub-4194304` | xlarge-full-width | `grust-next@counted` | 734.54 ± 19.96 | 792.73 ± 38.46 | +7.9% | 4 | 3 |
| `hub-4194304` | xlarge-full-width | `grust-next@work-uncounted` | 714.56 ± 8.58 | 772.11 ± 41.04 | +8.1% | 4 | 3 |
| `hub-4194304` | xlarge-full-width | `grust-next@unchecked` | 685.88 ± 10.29 | 749.20 ± 27.73 | +9.2% | 4 | 3 |
| `uniform-4194304` | xlarge-full-width | `neo4j-graph` | 578.25 ± 1.81 | 651.10 ± 26.70 | +12.6% | 3 | 4 |
| `uniform-4194304` | xlarge-full-width | `icebug` | 1041.13 ± 8.76 | 1186.87 ± 12.17 | +14.0% | 3 | 4 |
| `uniform-4194304` | xlarge-full-width | `icecat` | 5928.57 ± 73.21 | 7546.97 ± 59.78 | +27.3% | 3 | 4 |
| `uniform-4194304` | xlarge-full-width | `grustcat` | 7109.01 ± 114.64 | 8827.12 ± 59.57 | +24.2% | 3 | 4 |
| `uniform-4194304` | xlarge-full-width | `grust` | 2833.46 ± 22.82 | 3272.92 ± 23.78 | +15.5% | 3 | 4 |
| `uniform-4194304` | xlarge-full-width | `grust-next@counted` | 747.76 ± 13.22 | 871.10 ± 9.45 | +16.5% | 3 | 4 |
| `uniform-4194304` | xlarge-full-width | `grust-next@work-uncounted` | 735.39 ± 11.02 | 877.40 ± 3.12 | +19.3% | 3 | 4 |
| `uniform-4194304` | xlarge-full-width | `grust-next@unchecked` | 720.94 ± 15.14 | 857.59 ± 15.76 | +19.0% | 3 | 4 |

Every participant is slower above L3 in B6 than in B5: large-one-thread +20.4% to +123.1% over 24 cells; large-full-width +1.3% to +83.6% over 16 cells; xlarge-one-thread +16.7% to +69.6% over 24 cells; xlarge-full-width +7.3% to +27.3% over 16 cells. The participants that contain no Grust move with the ones that do, the page-fault counts are the same to within a few, and steal over those four runs is at most 21 ticks in 5132 s, so it is not the code under test and not a second workload. **The cause is not established here.** It is the reason the large and xlarge rows of the kernel-change table above are read as ratios within B6 and not against B5's ratios for the same cells, which were taken on a faster host state.

**A control, after the campaign.** The shortest large run, `large-full-width`,
repeated once after the last campaign run under the same driver with its own
tag (`control/` in the bundle), idle-checked and watched like any run. It is
not a campaign run and corrects nothing; it says whether the slower host state
was still there afterwards. PageRank, first call, every participant.

| fixture | participant | B5 | B6 campaign | control | control/B6 | control/B5 | steal |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `hub-2097152` | `neo4j-graph` | 260.04 ± 1.68 | 277.25 ± 1.97 | 275.66 ± 1.12 | -0.6% | +6.0% | 2 |
| `hub-2097152` | `icebug` | 455.57 ± 6.23 | 518.72 ± 7.09 | 530.39 ± 10.80 | +2.3% | +16.4% | 2 |
| `hub-2097152` | `icecat` | 1713.89 ± 3.47 | 3147.45 ± 26.40 | 3101.10 ± 81.86 | -1.5% | +80.9% | 2 |
| `hub-2097152` | `grustcat` | 2161.98 ± 199.82 | 3292.03 ± 63.31 | 3303.96 ± 64.00 | +0.4% | +52.8% | 2 |
| `hub-2097152` | `grust` | 1084.33 ± 7.68 | 1385.34 ± 22.93 | 1396.68 ± 12.95 | +0.8% | +28.8% | 2 |
| `hub-2097152` | `grust-next@counted` | 274.75 ± 15.17 | 278.46 ± 2.12 | 286.18 ± 7.79 | +2.8% | +4.2% | 2 |
| `hub-2097152` | `grust-next@work-uncounted` | 219.87 ± 5.69 | 256.36 ± 16.47 | 297.97 ± 12.62 | +16.2% | +35.5% | 2 |
| `hub-2097152` | `grust-next@unchecked` | 209.83 ± 0.64 | 240.62 ± 1.85 | 260.88 ± 6.00 | +8.4% | +24.3% | 2 |
| `uniform-2097152` | `neo4j-graph` | 262.94 ± 2.50 | 284.00 ± 3.72 | 277.19 ± 2.63 | -2.4% | +5.4% | 2 |
| `uniform-2097152` | `icebug` | 483.90 ± 8.91 | 555.11 ± 28.87 | 541.24 ± 18.44 | -2.5% | +11.8% | 2 |
| `uniform-2097152` | `icecat` | 2005.72 ± 109.56 | 3121.82 ± 32.92 | 3096.83 ± 70.85 | -0.8% | +54.4% | 2 |
| `uniform-2097152` | `grustcat` | 2640.27 ± 28.74 | 3850.63 ± 43.42 | 3825.67 ± 31.15 | -0.6% | +44.9% | 2 |
| `uniform-2097152` | `grust` | 1131.94 ± 8.18 | 1375.91 ± 31.94 | 1390.53 ± 15.81 | +1.1% | +22.8% | 2 |
| `uniform-2097152` | `grust-next@counted` | 248.59 ± 6.98 | 275.17 ± 3.47 | 268.47 ± 5.41 | -2.4% | +8.0% | 2 |
| `uniform-2097152` | `grust-next@work-uncounted` | 228.12 ± 3.92 | 258.63 ± 15.61 | 256.74 ± 4.83 | -0.7% | +12.5% | 2 |
| `uniform-2097152` | `grust-next@unchecked` | 226.02 ± 1.64 | 250.92 ± 5.43 | 251.34 ± 6.27 | +0.2% | +11.2% | 2 |

Attempt 1: `DISCARDED: host shared during the run`, started 2026-09-22T18:14:09+0000, 816.1 s, 3 steal ticks, 8 sightings (du -sh /home/admin/src). Attempt 2: `clean`, started 2026-09-22T18:29:36+0000, 812.6 s, 4 steal ticks, 0 sightings. A discarded attempt is kept in the bundle, renamed, and enters no table; the rows above are the clean one. Against the campaign's own `large-full-width` cells it is -2.5% to +16.2%, a median of -0.2%; against B5's, +4.2% to +80.9%, a median of +19.6%. So the host was still in the slower state after the campaign ended; the state is not a transient of one run.

## B7: PageRank at f32, the same protocol

Every PageRank table since B3 has carried one sentence under it: `neo4j-graph`
accumulates and returns f32, every other participant f64. B6's tables show
what that sentence hides. Under the same tolerance, 1e-8, Grust's f64 kernel
stopped at 16 or 17 iterations on every hub and uniform fixture at every size,
and `neo4j-graph` stopped between 20 and 36; so a `neo4j-graph` total and a
Grust total were never the same number of sweeps over the arcs, and a ratio
of them was a ratio of two stopping rules as much as of two kernels. B7 adds
the row that was missing: Grust's PageRank with f32 scores, beside its f64
one and beside `neo4j-graph`, with the iteration count printed in every table
beside the total, so that a reader can see where each stopped and compare
what is comparable.

- **What changed in Grust: one commit.** `ead3568`, "PageRank with f32
  scores", on top of B6's `87fc462`. The kernel is made generic over a sealed
  `Score` trait that f64 and f32 implement; `pagerank` keeps its signature and
  its f64 results, `pagerank_f32` returns `PageRank<f32>`, and the procedure
  layer takes `precision: 'f64' | 'f32'`. Every score, per-arc share,
  dangling mass and teleport share is formed and accumulated in the score
  type; the L1 residual is summed in f64 from the score differences at either
  precision, which is what `neo4j-graph` does for its f32 kernel, and the
  stop stays residual <= tolerance. The commit states that the f64 kernel's
  bits, work charges and refusal units are unchanged and that the f32 kernel
  charges the same work and is bit-identical at one, two, three and sixteen
  workers; B7's parity checks the first on every fixture at every
  concurrency against v0.22.0 and the second between the f32 build's counted
  and unchecked rows, rather than taking the commit's word. The commit's own
  tests record where f32 stops and where it cannot: on a dangling-free
  120,000-node graph both precisions stop at the same iteration at 1e-8; with
  half the nodes dangling f32 needs about twice the iterations at every
  tolerance of 1e-6 and below; and on a four-node graph whose largest scores
  are near 0.45, where an f32 ulp exceeds 1e-8, f32 never meets 1e-8, ending
  after the iteration cap with `converged` false.
- **What changed in the harness.** `fdf85a9` against B6's `633ff36`. The
  Grust participant source gains `--precision {f64,f32}`, default f64, behind
  a cargo feature that is on for `grust-next` and off for the v0.22.0 build,
  which refuses the flag non-zero rather than running f64 under an f32 label;
  any algorithm but PageRank refuses it the same way. A variant tag `+f32`
  passes it, and the receipt taken with the variant's flags declares `f32`, so
  parity holds the row to the rule `neo4j-graph` is held to, a relative 1e-6
  on the sum and the maximum floored at the stopping tolerance, and to nothing
  looser. The bits gate takes one group per base, the f64 builds against
  v0.22.0 and the f32 builds against their own counted row, since an f32
  vector is never bit-identical to an f64 one. A PageRank row that reports
  `converged: false` gets its own verdict, `not converged`, with the residual
  it stalled at, and is never timed; the tolerance is never loosened to make
  it converge. Every cell records its iteration count, its residual and
  whether it converged, and every table prints the count beside the total.
  `campaign.py` takes `--plan b7`; the B6 plan and its outputs are unchanged
  under the default.
- **What did not change.** The eight hub and uniform fixtures are the same
  bytes B5 and B6 timed, SHA-256-checked against B6's manifest before the
  build. The image was built on quegee under a 20 GB memory cap with four
  jobs; the two Grust trees were staged by `git archive` of the named commits
  rather than from working trees, so no checkout state reached them, and
  `sources.json` says so. The audit found six distinct binaries, and the
  audit, image receipt and manifest were taken before parity and never during
  a run. Parity came first, every fixture set at concurrency unset, 1 and 16;
  the page cache was dropped after parity and before the first timed run; one
  warmup and five repeats, counterbalanced; idle-checked before and after
  every run and sampled once a second during it; steal per cell and per run;
  a run with a sighting discarded; a cell at or above 0.25 MAD/median
  unusable. The work directory is B6's, so the reference cache was reused and
  every B7 output carries a `b7-` prefix beside B6's.
- **What is narrower than B6.** PageRank alone, on the two dangling-free
  families, because that is where the count differs and where `neo4j-graph`
  agrees with the reference; no pinned runs, since the allocator was B5's
  question and B6 re-decided it on the counter; no `+eager` row. v0.22.0 is
  present as the anchor at the pull kernel and at full width, and its push
  loop is not: at 4,194,304 nodes that row is 83 seconds a sample, the most
  expensive cell of B6's matrix, and nothing in B7 is compared with it. The
  estimate that decided this is `b7_report.py estimate` over B6's bundle, and
  the campaign's timed runs took 102 minutes against its 106.

## B7: results

One host, quegee, 2026-09-22. Grust `2182cdb` (v0.22.0) as `grust`, Grust `ead3568` as `grust-next`, Icecat `57b443ec`, this harness at `fdf85a9`, image `simple-rust-algo-bench:b7-ead3568`, built on the host from commits staged by `git archive`. The 8 fixtures are SHA-256-identical to B6's: `identical_to_b6` is true in the manifest. One warmup, five repeats, counterbalanced, parity gated at every concurrency. **Every cell of every run, with its iteration count, its residual, its steal, its dispersion and its usability, is in `simple-rust-algo-bench-evidence/b7-quegee/tables.md`**, generated from the run files by `b7_report.py tables`; the tables below select from it and add nothing to it. Times are milliseconds, median ± MAD, of the kernel call alone; per-iteration is that median divided by the iteration count the participant reported. Steal is ticks over that cell's group.

**Host conditions.** 1 resident agent session was seen by name across the campaign (2382171 codex resume 01a0ad61-0419-7110-9e8c-c25058935bc0). 0 sightings were recorded over 6 timed invocations, and a run with a sighting is discarded rather than published. The host was checked idle before and after every run and sampled once a second during it. The timed campaign ran from 2026-09-22T22:21:33+0000 to 2026-09-23T00:03:41+0000, 6 runs, in the order listed.

- `one-thread`: clean, started 2026-09-22T22:21:33+0000, 34.3 s, 0 steal ticks over the run, 0 sightings, 1 resident agent session.
- `full-width`: clean, started 2026-09-22T22:22:10+0000, 13.3 s, 0 steal ticks over the run, 0 sightings, 1 resident agent session.
- `large-one-thread`: clean, started 2026-09-22T22:22:25+0000, 1514.5 s, 6 steal ticks over the run, 0 sightings, 1 resident agent session.
- `large-full-width`: clean, started 2026-09-22T22:47:42+0000, 329.5 s, 2 steal ticks over the run, 0 sightings, 1 resident agent session.
- `xlarge-one-thread`: clean, started 2026-09-22T22:53:13+0000, 3560.6 s, 14 steal ticks over the run, 0 sightings, 1 resident agent session.
- `xlarge-full-width`: clean, started 2026-09-22T23:52:36+0000, 665.3 s, 3 steal ticks over the run, 0 sightings, 1 resident agent session.

**0 of the 240 cells reached the 0.25 MAD/median threshold**; the largest dispersion was 0.108, `grust-next@unchecked` uniform-2097152 first in b7-large-full-width.

**Parity at the commit under test**, hub and uniform at every size, PageRank, at concurrency unset, 1 and 16, before any timing. The f64 builds must return v0.22.0's vector bit for bit; the `+f32` builds must return their counted row's. A row that reports `converged: false` is `not converged`, its own verdict, and is never timed.

| file | agrees | mismatch | error | not converged | f64 bits-identical to v0.22.0 | `+f32` unchecked identical to counted | rows not agreeing |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `fixtures-1` | 24 | 0 | 0 | 0 | 8 of 8 | 4 of 4 | — |
| `fixtures-16` | 24 | 0 | 0 | 0 | 8 of 8 | 4 of 4 | — |
| `fixtures-large-1` | 12 | 0 | 0 | 0 | 4 of 4 | 2 of 2 | — |
| `fixtures-large-16` | 12 | 0 | 0 | 0 | 4 of 4 | 2 of 2 | — |
| `fixtures-large-unset` | 12 | 0 | 0 | 0 | 4 of 4 | 2 of 2 | — |
| `fixtures-unset` | 24 | 0 | 0 | 0 | 8 of 8 | 4 of 4 | — |
| `fixtures-xlarge-1` | 12 | 0 | 0 | 0 | 4 of 4 | 2 of 2 | — |
| `fixtures-xlarge-16` | 12 | 0 | 0 | 0 | 4 of 4 | 2 of 2 | — |
| `fixtures-xlarge-unset` | 12 | 0 | 0 | 0 | 4 of 4 | 2 of 2 | — |

0 parity invocations exited non-zero; 0 are marked other than clean (none).

**Where each participant stopped.** The iteration count every participant reported, per fixture and run. `neo4j-graph` sums its f32 residual in f64 and stops at residual < tolerance; Grust at either precision sums its residual in f64 and stops at residual <= tolerance; every row here ran at tolerance 1e-8 and a cap of 100 iterations. A Grust row reports the same count on both calls, so one is shown.

| fixture | run | `neo4j-graph` | `grust-next@counted+f32#1` | `grust-next@counted+f32#unset` | `grust-next@unchecked+f32#1` | `grust-next@unchecked+f32#unset` | `grust-next@counted+f32` | `grust-next@unchecked+f32` | `grust#1` | `grust-next@counted#1` | `grust-next@counted#unset` | `grust-next@unchecked#1` | `grust-next@unchecked#unset` | `grust` | `grust-next@counted` | `grust-next@unchecked` |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `hub-16384` | one-thread | 36 | 20 | 21 | 20 | 21 | — | — | 17 | 17 | 17 | 17 | 17 | — | — | — |
| `hub-65536` | one-thread | 28 | 20 | 21 | 20 | 21 | — | — | 17 | 17 | 17 | 17 | 17 | — | — | — |
| `uniform-16384` | one-thread | 28 | 19 | 19 | 19 | 19 | — | — | 16 | 16 | 16 | 16 | 16 | — | — | — |
| `uniform-65536` | one-thread | 34 | 19 | 20 | 19 | 20 | — | — | 16 | 16 | 16 | 16 | 16 | — | — | — |
| `hub-16384` | full-width | 36 | — | — | — | — | 20 | 20 | — | — | — | — | — | 17 | 17 | 17 |
| `hub-65536` | full-width | 33 | — | — | — | — | 20 | 20 | — | — | — | — | — | 17 | 17 | 17 |
| `uniform-16384` | full-width | 28 | — | — | — | — | 19 | 19 | — | — | — | — | — | 16 | 16 | 16 |
| `uniform-65536` | full-width | 34 | — | — | — | — | 19 | 19 | — | — | — | — | — | 16 | 16 | 16 |
| `hub-2097152` | large-one-thread | 26 | 20 | 21 | 20 | 21 | — | — | 16 | 16 | 16 | 16 | 16 | — | — | — |
| `uniform-2097152` | large-one-thread | 26 | 19 | 20 | 19 | 20 | — | — | 16 | 16 | 16 | 16 | 16 | — | — | — |
| `hub-2097152` | large-full-width | 28 | — | — | — | — | 20 | 20 | — | — | — | — | — | 16 | 16 | 16 |
| `uniform-2097152` | large-full-width | 27 | — | — | — | — | 19 | 19 | — | — | — | — | — | 16 | 16 | 16 |
| `hub-4194304` | xlarge-one-thread | 23 | 20 | 21 | 20 | 21 | — | — | 16 | 16 | 16 | 16 | 16 | — | — | — |
| `uniform-4194304` | xlarge-one-thread | 29 | 19 | 20 | 19 | 20 | — | — | 16 | 16 | 16 | 16 | 16 | — | — | — |
| `hub-4194304` | xlarge-full-width | 19 | — | — | — | — | 20 | 20 | — | — | — | — | — | 16 | 16 | 16 |
| `uniform-4194304` | xlarge-full-width | 29 | — | — | — | — | 19 | 19 | — | — | — | — | — | 16 | 16 | 16 |

Of 48 `+f32` cells, 0 stopped at the count `neo4j-graph` stopped at on the same fixture in the same run and 48 did not. Where the counts differ the two totals are not the same number of sweeps over the arcs; the per-iteration figure is the one that compares them, and it is a comparison of one sweep's cost, not of the time to an answer at this tolerance, which is the total.

### `neo4j-graph` beside Grust at f32, and Grust at f64 beside both

Total and per-iteration time of the kernel call, with the count. For `grust-next` the second call is shown, which has the transpose cached and runs on warm caches, and the first call in `tables.md`; `neo4j-graph` times one call on a fresh build. `counted` charges work to a shared meter and observes cancellation; `unchecked` does neither and is the like-for-like row against `neo4j-graph`, which performs no accounting. Nothing in this table is a ratio; a reader who forms one takes the boundary with it.

**one-thread** (workers 1), cells as total ms ± MAD / per-iteration ms / iterations:

| fixture | kernel | `neo4j-graph` f32 | `grust-next@unchecked+f32` | `grust-next@counted+f32` | `grust-next@unchecked` f64 | `grust-next@counted` f64 | `grust` v0.22.0 f64 | steal |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `hub-16384` | pull | 13.26 ± 0.03 / 0.368 / 36 | 9.05 ± 0.01 / 0.453 / 20 | 9.26 ± 0.01 / 0.463 / 20 | 7.55 ± 0.01 / 0.444 / 17 | 7.89 ± 0.01 / 0.464 / 17 | 9.66 ± 0.02 / 0.568 / 17 | 0 |
| `hub-16384` | push | — (push is sequential by construction; neo4j-graph has no such kernel) | 16.32 ± 0.02 / 0.777 / 21 | 27.90 ± 0.04 / 1.329 / 21 | 13.47 ± 0.03 / 0.792 / 17 | 23.25 ± 0.05 / 1.368 / 17 | — | 0 |
| `hub-65536` | pull | 36.61 ± 0.28 / 1.307 / 28 | 36.67 ± 0.06 / 1.834 / 20 | 37.90 ± 0.02 / 1.895 / 20 | 31.58 ± 0.14 / 1.858 / 17 | 33.41 ± 0.44 / 1.966 / 17 | 50.67 ± 1.32 / 2.981 / 17 | 0 |
| `hub-65536` | push | — (push is sequential by construction; neo4j-graph has no such kernel) | 65.42 ± 0.02 / 3.115 / 21 | 112.06 ± 0.58 / 5.336 / 21 | 57.93 ± 0.74 / 3.408 / 17 | 95.08 ± 0.35 / 5.593 / 17 | — | 0 |
| `uniform-16384` | pull | 10.51 ± 0.03 / 0.375 / 28 | 8.58 ± 0.01 / 0.451 / 19 | 8.81 ± 0.00 / 0.464 / 19 | 7.12 ± 0.01 / 0.445 / 16 | 7.49 ± 0.01 / 0.468 / 16 | 9.24 ± 0.01 / 0.578 / 16 | 0 |
| `uniform-16384` | push | — (push is sequential by construction; neo4j-graph has no such kernel) | 14.70 ± 0.01 / 0.774 / 19 | 25.10 ± 0.03 / 1.321 / 19 | 12.68 ± 0.01 / 0.793 / 16 | 21.54 ± 0.02 / 1.346 / 16 | — | 0 |
| `uniform-65536` | pull | 45.11 ± 0.16 / 1.327 / 34 | 34.88 ± 0.09 / 1.836 / 19 | 36.13 ± 0.08 / 1.902 / 19 | 29.63 ± 0.15 / 1.852 / 16 | 31.98 ± 0.34 / 1.999 / 16 | 46.25 ± 0.34 / 2.890 / 16 | 0 |
| `uniform-65536` | push | — (push is sequential by construction; neo4j-graph has no such kernel) | 62.13 ± 0.22 / 3.107 / 20 | 106.23 ± 0.25 / 5.312 / 20 | 55.45 ± 2.12 / 3.466 / 16 | 89.70 ± 0.53 / 5.606 / 16 | — | 0 |

**full-width** (workers 16), cells as total ms ± MAD / per-iteration ms / iterations:

| fixture | kernel | `neo4j-graph` f32 | `grust-next@unchecked+f32` | `grust-next@counted+f32` | `grust-next@unchecked` f64 | `grust-next@counted` f64 | `grust` v0.22.0 f64 | steal |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `hub-16384` | pull | 13.53 ± 0.09 / 0.376 / 36 | 3.29 ± 0.04 / 0.164 / 20 | 3.91 ± 0.07 / 0.195 / 20 | 2.82 ± 0.04 / 0.166 / 17 | 3.41 ± 0.13 / 0.200 / 17 | 3.51 ± 0.05 / 0.207 / 17 | 0 |
| `hub-65536` | pull | 15.22 ± 0.17 / 0.461 / 33 | 5.02 ± 0.08 / 0.251 / 20 | 7.71 ± 0.06 / 0.385 / 20 | 4.65 ± 0.09 / 0.273 / 17 | 7.23 ± 0.27 / 0.425 / 17 | 8.62 ± 0.08 / 0.507 / 17 | 0 |
| `uniform-16384` | pull | 10.77 ± 0.06 / 0.385 / 28 | 3.10 ± 0.01 / 0.163 / 19 | 3.84 ± 0.14 / 0.202 / 19 | 2.65 ± 0.07 / 0.166 / 16 | 3.26 ± 0.16 / 0.204 / 16 | 3.35 ± 0.06 / 0.209 / 16 | 0 |
| `uniform-65536` | pull | 16.22 ± 0.09 / 0.477 / 34 | 4.74 ± 0.01 / 0.250 / 19 | 7.36 ± 0.01 / 0.387 / 19 | 4.35 ± 0.11 / 0.272 / 16 | 6.69 ± 0.10 / 0.418 / 16 | 8.36 ± 0.25 / 0.522 / 16 | 0 |

**large-one-thread** (workers 1), cells as total ms ± MAD / per-iteration ms / iterations:

| fixture | kernel | `neo4j-graph` f32 | `grust-next@unchecked+f32` | `grust-next@counted+f32` | `grust-next@unchecked` f64 | `grust-next@counted` f64 | `grust` v0.22.0 f64 | steal |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `hub-2097152` | pull | 2559.78 ± 166.85 / 98.453 / 26 | 2392.00 ± 109.60 / 119.600 / 20 | 2846.56 ± 152.30 / 142.328 / 20 | 3240.03 ± 49.12 / 202.502 / 16 | 3674.28 ± 195.60 / 229.643 / 16 | 5502.70 ± 59.61 / 343.919 / 16 | 3 |
| `hub-2097152` | push | — (push is sequential by construction; neo4j-graph has no such kernel) | 4135.77 ± 38.31 / 196.941 / 21 | 5857.05 ± 92.95 / 278.907 / 21 | 5715.69 ± 63.27 / 357.231 / 16 | 6930.57 ± 40.09 / 433.161 / 16 | — | 3 |
| `uniform-2097152` | pull | 2378.46 ± 11.42 / 91.479 / 26 | 2175.48 ± 43.25 / 114.499 / 19 | 2414.53 ± 16.06 / 127.080 / 19 | 3185.56 ± 203.04 / 199.098 / 16 | 3421.73 ± 43.31 / 213.858 / 16 | 5826.54 ± 39.65 / 364.159 / 16 | 3 |
| `uniform-2097152` | push | — (push is sequential by construction; neo4j-graph has no such kernel) | 3703.31 ± 84.24 / 185.165 / 20 | 5466.82 ± 179.99 / 273.341 / 20 | 5485.69 ± 60.69 / 342.856 / 16 | 6517.60 ± 90.64 / 407.350 / 16 | — | 3 |

**large-full-width** (workers 16), cells as total ms ± MAD / per-iteration ms / iterations:

| fixture | kernel | `neo4j-graph` f32 | `grust-next@unchecked+f32` | `grust-next@counted+f32` | `grust-next@unchecked` f64 | `grust-next@counted` f64 | `grust` v0.22.0 f64 | steal |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `hub-2097152` | pull | 270.98 ± 3.42 / 9.678 / 28 | 232.81 ± 1.44 / 11.640 / 20 | 252.41 ± 2.24 / 12.621 / 20 | 211.99 ± 0.53 / 13.250 / 16 | 246.47 ± 4.91 / 15.405 / 16 | 496.69 ± 3.21 / 31.043 / 16 | 1 |
| `uniform-2097152` | pull | 274.85 ± 4.51 / 10.180 / 27 | 240.31 ± 2.40 / 12.648 / 19 | 256.15 ± 0.62 / 13.481 / 19 | 260.61 ± 11.69 / 16.288 / 16 | 270.47 ± 21.41 / 16.904 / 16 | 600.75 ± 8.96 / 37.547 / 16 | 1 |

**xlarge-one-thread** (workers 1), cells as total ms ± MAD / per-iteration ms / iterations:

| fixture | kernel | `neo4j-graph` f32 | `grust-next@unchecked+f32` | `grust-next@counted+f32` | `grust-next@unchecked` f64 | `grust-next@counted` f64 | `grust` v0.22.0 f64 | steal |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `hub-4194304` | pull | 6292.37 ± 217.86 / 273.581 / 23 | 7600.20 ± 89.06 / 380.010 / 20 | 8275.85 ± 259.97 / 413.793 / 20 | 7802.65 ± 97.01 / 487.666 / 16 | 8257.34 ± 125.18 / 516.084 / 16 | 12614.11 ± 170.82 / 788.382 / 16 | 7 |
| `hub-4194304` | push | — (push is sequential by construction; neo4j-graph has no such kernel) | 13808.21 ± 317.20 / 657.534 / 21 | 16554.15 ± 617.35 / 788.293 / 21 | 12868.34 ± 85.01 / 804.271 / 16 | 15247.29 ± 31.81 / 952.956 / 16 | — | 7 |
| `uniform-4194304` | pull | 7717.04 ± 48.57 / 266.105 / 29 | 7410.01 ± 211.73 / 390.001 / 19 | 7612.90 ± 50.97 / 400.679 / 19 | 7905.37 ± 28.25 / 494.086 / 16 | 8418.24 ± 63.59 / 526.140 / 16 | 13365.33 ± 74.47 / 835.333 / 16 | 7 |
| `uniform-4194304` | push | — (push is sequential by construction; neo4j-graph has no such kernel) | 12140.00 ± 143.59 / 607.000 / 20 | 15328.09 ± 715.85 / 766.405 / 20 | 12264.49 ± 133.20 / 766.531 / 16 | 14839.20 ± 147.88 / 927.450 / 16 | — | 7 |

**xlarge-full-width** (workers 16), cells as total ms ± MAD / per-iteration ms / iterations:

| fixture | kernel | `neo4j-graph` f32 | `grust-next@unchecked+f32` | `grust-next@counted+f32` | `grust-next@unchecked` f64 | `grust-next@counted` f64 | `grust` v0.22.0 f64 | steal |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `hub-4194304` | pull | 406.32 ± 4.20 / 21.385 / 19 | 565.32 ± 8.24 / 28.266 / 20 | 623.24 ± 42.75 / 31.162 / 20 | 766.65 ± 3.65 / 47.916 / 16 | 798.97 ± 9.99 / 49.935 / 16 | 1424.91 ± 10.84 / 89.057 / 16 | 1 |
| `uniform-4194304` | pull | 622.34 ± 11.31 / 21.460 / 29 | 534.08 ± 50.27 / 28.109 / 19 | 568.30 ± 7.83 / 29.911 / 19 | 788.05 ± 17.47 / 49.253 / 16 | 859.26 ± 7.47 / 53.704 / 16 | 1559.55 ± 9.31 / 97.472 / 16 | 2 |

**Unchanged code against B6.** `grust` (v0.22.0) and `neo4j-graph` are the same binaries' sources as in B6, differing at most by the harness commit stamped into them, on the same fixtures, under the same protocol. Their B7 total against their B6 total on the same cell, as the median and the range of the ratio, is a reading of the host, not of any code:

| participant | cells | median B7/B6 | smallest | largest |
| --- | ---: | ---: | --- | --- |
| `grust` | 32 | 0.962 | 0.829 (hub-2097152 large-full-width first) | 1.027 (hub-16384 full-width second) |
| `neo4j-graph` | 16 | 0.977 | 0.845 (uniform-4194304 xlarge-one-thread) | 1.005 (uniform-16384 full-width) |


### The boundary, restated for f32

- **Three counts, not two.** On every fixture in every run, `neo4j-graph`,
  Grust at f32 and Grust at f64 stopped at three different iteration counts.
  The f32 rows stopped 3 to 4 iterations after the f64 rows and well before
  `neo4j-graph`; the residuals at which they stopped are in `tables.md`, the
  f32 rows between 8.0e-9 and 9.5e-9 and the f64 rows between 3.2e-9 at the
  protocol sizes and 9.96e-9 above L3, all below the tolerance, so every row
  stopped by the rule and not by the cap. Where the
  counts differ, a total is the time to this tolerance under that
  participant's rule and the per-iteration figure is the cost of one sweep;
  the tables above give both, and neither is a ratio.
- **`neo4j-graph`'s count is a property of its run.** Its residual is a f64
  sum accumulated across worker threads, so its order depends on the width,
  and its count moved with the run: 28 at one thread and 33 at sixteen on
  `hub-65536`, 23 and 19 on `hub-4194304`. Grust's residual is formed in fixed
  chunks and its count did not move with the width at either precision, which
  is what the bits gate checked. A count for `neo4j-graph` therefore belongs
  to a run, and the side-by-side table keeps it there.
- **What f32 cannot do.** An f32 kernel cannot meet a tolerance below one ulp
  of a moving score except at an exact fixed point, and Grust's commit records
  a graph where it never meets 1e-8. No B7 row stalled: every f32 cell
  converged under the cap of 100 on these fixtures, whose largest scores are
  far below 0.45. On a dangling-heavy graph the same commit's tests record
  f32 needing about twice the iterations at tolerances of 1e-6 and below; B7's
  two families have no dangling nodes and this document does not measure that
  regime. A campaign on `path` or `layered` must expect it and restate this
  paragraph rather than inherit it.
- **The scores are different numbers.** Every f32 vector agrees with the f64
  reference to between 2.6e-13 and 9.7e-11 absolute per score, and no score is
  bit-identical to the reference's; the f64 rows are bit-identical to
  v0.22.0's on every fixture. A reader comparing a `+f32` row with an f64 row
  is comparing two answers, not two timings of one.

## What is not here

- **Not portable.** Every timing here is from one host — quegee, 16 vCPU on 8
  physical cores, 24.8 MB L3, not burstable — and is a fact about that machine
  as much as about the code. Numbers produced on a burstable box during this
  work were for shape only and none is quoted here.
- **No ranking.** The B4 and B5 tables put `neo4j-graph` beside Grust's
  accounting modes so a reader can compare like for like, and B5's pinned probe
  puts every participant beside itself; this document does not reduce them to
  an order, and `neo4j-graph` computes in `f32` to its own stopping rule.
- **No cause for what is left of the WCC and BFS first-call slowdown**, only
  its shape, and now the knowledge that it is not the allocator: B5 records the
  page faults of every call, and they are equal where the times are not.
- **No cause here for PageRank's collapse on the `path` family at full
  width** as B5 measured it. The cause was found outside this harness and is
  stated by Grust `55a200f`, which B6 times; what this document holds is the
  before and the after, not the attribution.
- **No cause for the one-worker WCC residue**, which the padding commit's own
  measurement tied to the balance's chunk size class and did not explain, and
  which B6 measures under the protocol without explaining either.
- **No cause for the drift between campaigns on unchanged code**, which was
  large for two participants between B4 and B5 and is why no cell of one
  campaign is compared with a cell of another; B6 reports its own drift
  against B5 in the same form.
- **No f32 result outside the dangling-free families.** B7 times Grust's f32
  PageRank on `hub` and `uniform` alone; where f32 needs twice the iterations,
  or cannot meet the tolerance at all, is stated from Grust's own tests and
  is not measured here.
- **A dated result.** B3 describes v0.22.0, B4 describes `4d8e5db`, B5
  describes `ca68900`, B6 describes `87fc462` and B7 describes `ead3568`; a
  column measured later describes that code.
