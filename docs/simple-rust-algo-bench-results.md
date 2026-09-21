# simple-rust-algo-bench: correctness first, timings pending

Status: **B1 and B2 complete; B3 not run.** Recorded 2026-09-21. This document
holds what has been established — that the participants compute the same
functions — and states what has not. No timing appears here, and none will
until it comes from the dedicated host.

## What has been established

Five participants build in one image, are five distinct binaries, and were
checked against an independent reference at four sizes before anything was
timed.

| participant | what runs | language | parallel |
| --- | --- | --- | --- |
| `library` | `neo4j-labs/graph` via its builder and `graph::prelude` | Rust | rayon, unconditional |
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
on 12 of 12 checks for the algorithms they implement; `library` agrees on 10 of
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

`library`'s PageRank does not redistribute dangling mass: it divides by
out-degree with no sink handling, so a node with no outgoing edge takes its share
out of the distribution. The deficit tracks the dangling fraction rather than
sitting at a fixed offset, which is what a leak does:

| fixture | dangling nodes | share | `library` score sum |
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

**The library accumulates and returns `f32`; every other participant is `f64`.**
Its score array is half the bytes, so half the memory traffic on the one array
PageRank touches randomly per arc — which is a difference in the resource this
kernel is bound by, not only in the digits it reports. It is stated under every
PageRank table.

Its consequences are measured rather than inferred, on `hub-16384`, which has no
dangling node:

| tolerance | `library` iterations | `library` score sum | `grust` iterations | `grust` score sum |
| --- | ---: | ---: | ---: | ---: |
| 1e-4 (the library's own default) | 8 | 0.9997947451 | 8 | 1.000000000000 |
| 1e-8 (the protocol tolerance) | 36 | 0.9999999668 | 17 | 1.000000000000 |

Three things follow. **The `f64` kernels preserve mass exactly at every
iteration** and the `f32` one does not: it is 2.1e-4 short after eight iterations
and still 3.3e-8 short at its converged answer. **At the same loose tolerance both
take eight iterations**, so the iteration gap at 1e-8 is about how each measures
its own residual rather than about one converging faster. And **the library does
reach 1e-8**, with a residual of 9.3e-9 — it needs about twice the iterations to
get there.

A row at the library's own `1E-4` is therefore worth publishing beside the
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
  library takes 41 iterations where the others take 16, on its own stopping rule.
- **Concurrency is explicit, because it selects a kernel.** With concurrency
  unset Grust's PageRank takes the push loop that the parallel path is tested
  against; with concurrency 1 it takes the pull kernel on one thread. The two
  return different scores in the last digit, so they are distinguishable in the
  evidence and not only in a timing. Parity therefore gates the configuration
  that is timed: push, pull at one thread and pull at two all have their own
  parity runs.
- **Thread width is set for every participant by name.** The three projects read
  it from three places — Grust from `with_concurrency`, the library from
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
- Variant order alternates between repeats; steal is read across the run and
  printed above the tables.

## What is not here

- **No timings.** B3 runs on the dedicated host, after the release sweep. Every
  number produced on a burstable box during this work was for shape only and none
  of it is quoted.
- **No comparison against `neo4j-labs/graph` on speed.** Nothing in this document
  says which is faster, because nothing has been measured that could.
- **No claim about parallel execution.** Whether the Grust participants run
  parallel in the timed run is undecided at the time of writing.
- **A dated result.** Parallel execution is being added to the kernels on this
  side as this is written; a column measured then describes that code.
