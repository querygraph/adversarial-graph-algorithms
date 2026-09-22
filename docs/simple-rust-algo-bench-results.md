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

One host, quegee, 2026-09-22. PENDING-B5-PROVENANCE One warmup, five repeats,
counterbalanced, parity gated at every concurrency. **Every cell of every run,
with its steal, its dispersion, its minor page faults and its usability, is in
`simple-rust-algo-bench-evidence/b5-quegee/tables.md`**, generated from the run
files by `tables.py`; the tables below select from it and add nothing to it.
Times are milliseconds, median ± MAD; page faults are the median of the same
samples, read outside the timers. Steal is ticks over that cell's group.

**Host conditions.** PENDING-B5-RESIDENT

PENDING-B5-HOSTRUNS

PENDING-B5-UNUSABLE

**Parity at the commit under test**, every fixture set at concurrency unset, 1
and 16, before any timing. `grust-next` must return v0.22.0's PageRank vector
bit for bit or it is a mismatch and is never timed.

PENDING-B5-PARITY

### The allocator artifact, corrected

WCC and BFS read no in-arcs. B4 built the transpose for them anyway, inside the
build timer and immediately before the call it timed; `+eager` is that
behaviour, kept as its own row. The page-fault columns are the quantity the
artifact moved, so the correction can be read off the counter beside the time.

| fixture | algorithm | run | kernel | `grust` v0.22.0 | faults | `grust-next` | faults | `grust-next` `+eager` | faults | next/v0.22.0 | eager/next |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
PENDING-B5-ALLOC

PENDING-B5-ALLOCSUM

### The allocator pinned, for every participant

`GLIBC_TUNABLES=glibc.malloc.mmap_threshold=131072` set for the whole
container, so every participant in the run has it. First call, at the protocol
size, against the same cell of the same run unpinned.

| fixture | algorithm | run | participant | default allocator | faults | pinned | faults | pinned/default |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
PENDING-B5-PINNED

Median change under pinning, per participant: PENDING-B5-PINVERDICT

PENDING-B5-PINDECISION

### The transpose, on the build side

One thread, pull kernel (concurrency 1), PageRank — the one kernel here that
reads in-arcs, and so the one whose build column contains them. "First" is a
fresh projection's first kernel call; on v0.22.0 it includes building the
transpose. "Second" repeats it with the transpose cached and on warm caches,
which is not the condition of any other participant's timed call.

| fixture | `grust` v0.22.0 first | `grust` v0.22.0 second | `grust-next` counted first | transpose, in `build_ms` | `grustcat` | steal |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
PENDING-B5-TRANSPOSE

### The kernel change, v0.22.0 against the commit under test

Same mode (counted), same concurrency, second call against second call, so the
transpose is cached on both sides. Both builds return the same scores bit for
bit, which parity checked on every fixture at every concurrency.

| fixture | run | kernel | v0.22.0 | `ca68900` | ratio | steal |
| --- | --- | --- | ---: | ---: | ---: | ---: |
PENDING-B5-KERNEL

### Every cell that got worse

Counted `grust-next` against v0.22.0, same fixture, algorithm, kernel and call.
PENDING-B5-WORSESUM

| fixture | algorithm | run | kernel | call | v0.22.0 | faults | `ca68900` | faults | change | steal |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
PENDING-B5-WORSE

### The two items the attribution left open

**Counted BFS on the first call.** B4 had it 8 to 11% slower than v0.22.0 on
`uniform` and `hub`. The last column is what the same cell said in B4.

| fixture | run | kernel | v0.22.0 | faults | `ca68900` | faults | change | B4 said |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
PENDING-B5-BFSOPEN

**PageRank on `layered-16384` at sixteen threads.**

| fixture | run | kernel | call | v0.22.0 | `ca68900` | change | steal |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
PENDING-B5-LAYEREDOPEN

### What the accounting guarantee costs

`grust-next`, first call, by mode, beside `neo4j-graph`, which performs no
accounting and is `f32` on its own stopping rule.

| fixture | run | kernel | counted | work-uncounted | unchecked | `neo4j-graph` | steal |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
PENDING-B5-ACCT

PENDING-B5-BUILD

### B4 against B5 on unchanged code

The participants that did not change between the two runs, one thread, first
call. A B5 cell is compared only with other cells of the same B5 run; this
table is the size of the drift between campaigns, not a correction to either.

| fixture | algorithm | participant | B4 | B5 | change |
| --- | --- | --- | ---: | ---: | ---: |
PENDING-B5-DRIFT

## What is not here

- **Not portable.** Every timing here is from one host — quegee, 16 vCPU on 8
  physical cores, 24.8 MB L3, not burstable — and is a fact about that machine
  as much as about the code. Numbers produced on a burstable box during this
  work were for shape only and none is quoted here.
- **No ranking.** The B4 tables put `neo4j-graph` beside Grust's accounting
  modes so a reader can compare like for like; this document does not reduce
  them to an order, and `neo4j-graph` computes in `f32` to its own stopping
  rule.
- **No cause for the WCC and BFS first-call slowdown**, only its shape.
- **A dated result.** B3 describes v0.22.0 and B4 describes `4d8e5db`; a column
  measured later describes that code.
