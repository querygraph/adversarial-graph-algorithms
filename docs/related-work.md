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
them is a measured performance claim. No participant in this benchmark has been
measured against `neo4j-labs/graph`.

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

## What is not established

Nothing above is a performance comparison, and none is offered here. The two
projects have not been measured against each other, their execution envelopes
differ, and parallel execution is currently being added to the kernels on this
side, so any speed statement written today would describe a moving target.

The way to settle it is to add the library as a participant: it has a clean
builder API, it computes several of the same algorithms, and a column for it
would replace argument with evidence, under the same disclosed boundaries as
every other column. Until that exists, this note should be read as a description
of scope, not as a result.
