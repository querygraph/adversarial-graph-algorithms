<!-- b9_post: wrap 76 -->
# Related work: Rust graph algorithm libraries

Parallel graph algorithms in Rust are established work, and this benchmark does
not claim otherwise. This note records how the participants here relate to the
best-known Rust library in the space, so that the comparison is about what each
project does rather than about which name is newer.

## neo4j-labs/graph

[`neo4j-labs/graph`](https://github.com/neo4j-labs/graph) describes itself as
"a library for high-performant graph algorithms." It is actively maintained —
not archived, most recent commit 2026-06-10 — and organised as five crates:
`builder`, `algos`, `app`, `mate` (Python bindings) and `server`.

Its algorithm crate depends on `ahash`, `atomic_float`, `graph_builder`,
`nanorand`, `num-format` and `rayon`. Graphs are constructed by the builder from
file input into an in-memory compressed representation, and algorithms run in
parallel over it. `graph_server` is an Apache Arrow Flight server: clients create
and manage graphs in memory, run algorithms and stream results back through a
Flight client such as pyarrow.

That is a mature, parallel, Arrow-connected Rust graph algorithm library, and it
predates this work by years.

## Where the projects differ

The differences below are scope differences, not quality judgements, and none of
them is a measured performance claim. The measurements that do exist are the
in-memory kernel benchmark's, described at the end of this note; they are
boundaried rows, not a verdict on any difference below.

**A query language over the algorithms.** The participants here include a
general Cypher executor: algorithms are reached through
`CALL grust.algorithms.* YIELD …` with parsing, semantic analysis, policy
validation, projection and row consumption inside the measured boundary. In
`neo4j-labs/graph`, algorithms are called from Rust, Python or Flight actions;
the single occurrence of Cypher in that repository is GDL, a Cypher-flavoured
graph literal used to construct graphs in `builder/src/input/gdl.rs`, not a query
language implementation.

**Where Arrow sits in the stack.** Both projects use Arrow, at different layers.
`graph_server` uses Arrow Flight as the transport that carries results to
clients. The participants here use Arrow inside execution: a row graph is
converted to Arrow input, projected through a native Arrow API, and algorithm
results are consumed as Arrow batches, with a separate column in which DataFusion
executes complete node and edge scan plans before the same native kernels run.
Conversion, preparation and projection are timed apart from the kernels.

**Where the graph comes from.** `neo4j-labs/graph` builds its own in-memory
representation from file input. The participants here run over a backend-neutral
property-graph API, and one pair of columns executes the same kernels over a
snapshot read back from a durable Turso database and verified against the input
before execution. Database loading, snapshot capture and verification are
reported as separate phases and are not presented as equivalent to any other
project's ingestion.

**What the algorithms are accountable to.** Execution here runs under a
cooperative budget: kernels charge work once per visited entry and per
reconstructed path step, memory is admitted before it is allocated, and
cancellation and an optional deadline are observed during execution, with an
exhausted budget failing exactly at its limit. That machinery is why an
untrusted or shared caller can be given an algorithm without being given the
machine. `neo4j-labs/graph` has no equivalent layer — its algorithm crate
depends on `ahash`, `atomic_float`, `graph_builder`, `nanorand`, `num-format`
and `rayon`, and a repository search returns no matches for budget or deadline —
which is the ordinary and reasonable choice for a library whose caller owns the
process.

**What the algorithm is required to return.** Most algorithm libraries, including
that one, return one value per node: a rank, a component identifier, a distance.
The workload that distinguishes this benchmark asks for full paths — the node
sequence and the cumulative-cost sequence for every reachable destination, all
constructed and consumed. On a 65,536-node chain that is 2,147,516,416 entries in
each array, and it exercises reconstruction and result conversion at a scale that
per-node outputs never reach.

## What has been measured since, and what has not

An earlier version of this note ended by saying the two projects had not been
measured against each other, and that the way to settle it was to add the
library as a participant under the same disclosed boundaries as every other
column. That participant now exists, keyed `neo4j-graph`, in
[`simple-rust-algo-bench`](simple-rust-algo-bench-results.md): one execution
class, an in-memory graph built once from the same input with kernels called
through each project's own Rust API, beside Icebug, Icecat, Grustcat and
Grust's general kernel, on one dedicated host. What that established:

- **Same function first.** Every participant is checked against an independent
  reference before anything is timed, and a cell that did not agree is never
  timed. `neo4j-graph`'s PageRank does not redistribute dangling mass, which is
  a choice rather than a defect, NetworKit's default too, and it means PageRank
  is compared only on the dangling-free families. It accumulates and returns
  `f32` where every other participant is `f64`, stated under every PageRank
  table as a boundary. The claim that the `f64` participants are bit-identical
  to one another was made, checked, and withdrawn; what holds is agreement far
  inside the stopping tolerance with the same iteration count.
- **The accountability difference is a separate measurement, as this note
  asked.** Grust's cooperative budget is timed as its own labelled rows,
  `counted`, `work-uncounted` and `unchecked`, with `unchecked` the
  like-for-like row for a library that performs no accounting and the distance
  to `counted` what the guarantee costs. Nothing about it is absorbed into a
  shared cell.
- **Two measurement artifacts were in this side's timer, and were corrected in
  the open.** Grust's first run timed its PageRank transpose inside the kernel
  while every other participant built its reverse adjacency in the build timer;
  the rerun that corrected it then built the transpose for kernels that never
  read it, leaving the allocator in a state the baseline was not measured in.
  Both are stated as corrections in the results document, with the earlier
  tables left standing beside the corrected ones, and the third campaign records
  minor page faults beside every call so that neither has to be taken on trust.
- **Every cell where the current Grust commit is slower than the release before
  it is listed**, with the unexplained ones marked unexplained.
- **A regression the third campaign found was attributed outside the harness,
  fixed by one commit, and the commit was timed under the same protocol with
  nothing else changed.** The fourth campaign puts B5's figure for each cell
  beside its own and lists which of B5's slower cells are faster, level, or
  still slower on the padded commit; it also records that the host was slower
  above L3 for every participant, including the ones that contain no Grust,
  and reads its large sizes within itself for that reason.
- **The precision boundary was removed rather than argued around.** The fifth
  campaign adds a Grust PageRank that accumulates in `f32`, so that Grust and
  `neo4j-graph` compute at the same precision under the same stopping rule with
  neither row charging work to a meter, and that pair is what a per-sweep
  comparison is drawn on. The three rows still stop at three different counts —
  `neo4j-graph` between {{B9_NEO_MIN}} and {{B9_NEO_MAX}} sweeps, Grust at `f32`
  at {{B9_F32_MIN}} to {{B9_F32_MAX}}, Grust at `f64` at {{B9_F64_MIN}} to
  {{B9_F64_MAX}} — so totals are not comparable across participants and
  per-sweep times are. `neo4j-graph` accumulates in `f32` to its own stopping
  rule and performs no work accounting, wherever its column appears.
- **The comparison this note once called unmeasured is measured, and this is
  what it says.** Per sweep, on the like-for-like pair, inside the sixth
  campaign's own bundle: of {{LFL_TOTAL}} cells, {{LFL_BELOW}} put Grust's sweep
  at or below `neo4j-graph`'s, {{LFL_INSIDE}} is above by less than the margin
  on that cell, and {{LFL_OUTSIDE}} are above by more — all at one thread on the
  graphs that fit in the host's L3, the largest being {{LFL_OUTSIDE_PCT}}. No
  cause for those three is established. Over the same campaign the kernel's
  counted sweep is {{ANCHOR_MIN}} to {{ANCHOR_MAX}} of the release before it on
  {{ANCHOR_CELLS}} cells, with both sides returning the same bits.
- **Work accounting moved in both directions, and both are reported.** On the
  pull kernel the meter's cost per sweep is {{METER_LARGE_B9}} at
  {{LARGE_SIZE}} nodes and {{METER_XLARGE_B9}} at {{XLARGE_SIZE}}, where the
  campaign before it read {{METER_LARGE_B7}} and {{METER_XLARGE_B7}}; on the
  push kernel it is {{METER_PUSH_B9}} against {{METER_PUSH_B7}}, worse on
  {{METER_PUSH_WORSE}} of {{METER_PUSH_CELLS}} cells by more than both margins
  together, with no cause established. Each column is a ratio formed inside its
  own campaign; no cell of one campaign is divided by a cell of another.

The results document, its evidence bundles at
[`simple-rust-algo-bench-evidence/b5-quegee/`](simple-rust-algo-bench-evidence/b5-quegee/),
[`b6-quegee/`](simple-rust-algo-bench-evidence/b6-quegee/),
[`b7-quegee/`](simple-rust-algo-bench-evidence/b7-quegee/)
and [`b9-quegee/`](simple-rust-algo-bench-evidence/b9-quegee/),
and the [post that explains the campaigns](blog/simple-rust-algo-bench/post.md)
hold the numbers and the boundaries they carry; this note does not repeat the
tables, and it offers no ranking. The same bundles render the
[kernels page on adversari.al](https://adversari.al/graph/kernels), where every
figure is rendered from a hash-verified file rather than typed.

What is still not settled: the cause of the three like-for-like cells above
their margin, all at one thread at or below {{PROTOCOL_SIZE}} nodes; the cause
of the push kernel's meter cost rising between the last two campaigns; the
cause of the remaining first-call slowdown in counted WCC and BFS, which the
page-fault counter shows is not the allocator and which the padding commit's
own measurement tied to the balance's chunk size class without explaining; and
the drift between campaigns on unchanged participants, which reaches a median
per-sweep ratio of {{UNCHANGED_MEDIAN}} over {{UNCHANGED_CELLS}} cells between
the last two, and is why a cell is only ever compared with other cells of its
own campaign. And the remark about a moving target still applies: the timed
columns describe v0.22.0 (`{{GRUST_OLD}}`) and the commits `{{GRUST_B5}}`,
`{{GRUST_B6}}`, `{{GRUST_B7}}` and `{{GRUST_B9}}` on one host, and a column
measured later describes that code.
