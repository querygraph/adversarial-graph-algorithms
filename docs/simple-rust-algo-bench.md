# simple-rust-algo-bench: an in-memory column for `neo4j-labs/graph`, icecat and grustcat

Status: **scheduled, not yet run.** Recorded 2026-09-20. Called
`simple-rust-algo-bench`: simple because it is one execution class and three
algorithms, and named for what it measures rather than for who it compares. This answers the open
item at the end of [`related-work.md`](related-work.md), which says the way to
settle a comparison with `neo4j-labs/graph` is to add it as a participant under
the same disclosed boundaries as every other column, and that until that exists
the note is a description of scope rather than a result.

## What this measures, and what it deliberately does not

One execution class only: **an in-memory graph, built once from the same input,
with algorithm kernels called directly through each project's own Rust API.**

- **No Cypher.** Not in any published row. A query layer parses, plans, admits
  and converts; a library call does none of those. Timing one against the other
  measures the layer, not the kernel, and the row would be unreadable as
  evidence.
- **No database.** No Turso, no Neo4j, no snapshot capture. Those columns exist
  in the main harness and stay there.
- **No feature difference smuggled into a number.** Where this side runs a
  kernel under a cooperative budget — work charged per visited entry, memory
  admitted before allocation, cancellation and deadline observed — and the
  library runs it without one, that difference is **reported as a separate
  measurement**, not absorbed into a shared cell. `related-work.md` already
  describes the accountability gap; this benchmark must not convert it into an
  unexplained slowdown.

Cypher and Turso variants **may be run for our own information** and are useful
for exactly one thing: knowing what our own layers cost. They are recorded in a
separate table, labelled as a different execution class, and are not comparable
with any library column.

## Participants

| Column | What runs | Language |
| --- | --- | --- |
| `library` | `neo4j-labs/graph` via its builder API and `graph::prelude` algorithms | Rust |
| `icebug` | the Arrow update of NetworKit, the C++ kernels already in this harness | C++ |
| `icecat` | the Rust rewrite of those kernels, Arrow 59.3 buffers throughout | Rust |
| `grustcat` | Grust's model projected to packed Arrow adjacency | Rust |
| `grust` | Grust's own kernels over `GraphProjection`, direct, no procedures | Rust |

`icebug` and `icecat` are both in the set because the lineage is
**NetworKit → Icebug (Arrow, C++) → Icecat (the Rust rewrite) → Grustcat**, per
`rust/README.md` in that repository, and a column that skips the middle cannot
tell a rewrite's cost from a design's. Note the crate names do not follow the
lineage: Icecat's Rust crates are still called `icebug-*`, and its Python import
is `icebug_rust`, kept for compatibility. A column labelled from a crate name
would label this backwards — as an earlier draft of this document did.

Three of the five are Arrow-first — Icebug, Icecat and Grustcat — so the
C++-to-Rust cell and the Rust-to-Rust cells are not confounded by a change of
memory layout at the same time.

## Algorithms

Only what every participant implements, so no cell is empty and no column is
flattered by its absence:

- **PageRank** — damping 0.85, L1 tolerance 1e-8, iteration cap stated per run,
  and **the iteration count reported beside the time**, because a kernel that
  converges in fewer iterations is not faster per iteration.
- **Weakly connected components** — component count and the label of a fixed
  probe node reported, so a wrong answer cannot look fast.
- **Breadth-first distances from one source** — reached count and distance sum
  reported.

Deliberately excluded for now: full paths, which only this side computes and
which `related-work.md` already names as the workload that distinguishes the
main benchmark; and anything one project has and another does not.

## What is timed apart

Per participant, per sample: **input parse**, **graph build**, **kernel**, and
**result materialisation**. The kernel column is the only one any two
participants are compared on. A project that builds a faster structure and a
project that runs a faster kernel are different findings and must not be summed.

## Protocol

- Same input files, same node and edge counts, same orientation, same weights.
- Every participant's answer validated against the same reference before any
  timing is kept; a mismatched sample is reported as a mismatch and never as a
  time.
- Warmups and repeats stated per run; median and full spread reported, never a
  single figure. Variant order counterbalanced within a run.
- **Timings published only from quegee** (c5n, dedicated, 0.00045% lifetime
  steal). grust and eigen are t2-class and burstable: they build and verify, and
  any number from them is labelled shared-host and is a ratio at best.
- The host's steal figure printed above every table, per `AGENTS.md`.

## Where it runs

A **separate Docker image** under `docker/simple-rust-algo-bench/`, not the main harness
image. The main image carries a JVM, Neo4j, GDS, a C++ NetworKit build and
Turso; none of that belongs in an in-memory library comparison, and keeping it
out means the image builds in minutes and the participants cannot accidentally
share a runtime.

## Order of work

1. Image builds all five participants and prints each one's version, commit and
   binary digest. On eigen, which is idle and mine.
2. Correctness parity: every participant agrees with the reference on all three
   algorithms across the fixture sizes, before anything is timed.
3. Timed run on quegee, **after Q5**, which is on the release critical path.
4. Report, with the accountability difference stated as a separate measurement
   and the Cypher and Turso figures in their own table if they were run.

## What this cannot settle

Parallel execution is being added to the kernels on this side as this is
written. A column measured today describes today's code, and the note in
`related-work.md` about a moving target still applies. The run is dated and its
commits recorded so a later run can be compared with it rather than replacing it.
