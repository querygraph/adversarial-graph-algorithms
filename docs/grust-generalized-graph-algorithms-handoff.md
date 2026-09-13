# Generalized graph algorithms in Grust: implementation handoff

**Prepared:** 2026-09-13. **Audience:** an implementation agent on another machine.
**Task:** add a general, backend-neutral graph analytics capability to Grust,
including direct Rust APIs, Arrow input/output, and extensible Cypher procedures.
This document is an implementation specification, not a claim that the work is done.

## 1. Assignment and completion boundary

Build an extensible analytics subsystem, not another switch containing five
procedure names and not a second parser for a benchmark query. An independent
provider must be able to register an algorithm without editing the Cypher parser,
semantic analyzer, or executor. The same algorithm implementation must be callable
from Rust and through the ordinary Grust query API.

“Full capability” has two dimensions: a complete extension/execution architecture
and a growing algorithm catalog. Deliver the architecture and the mandatory
initial catalog below, then expand the catalog through that architecture. Do not
claim parity with every Neo4j GDS algorithm or arbitrary Cypher on the strength of
five kernels. Maintain an explicit implemented/unsupported matrix for algorithms,
options, execution modes, graph representations, and backends.

The mandatory initial catalog is BFS, Dijkstra distances, one shortest full path
per reachable destination, weakly connected components, strongly connected
components, and PageRank. Generalized admission, signatures, graph selection,
resource accounting, streaming consumption, Arrow results, and registration by
an external provider are equally required. Five procedures alone are incomplete.

The separate QueryGraph/Pinax demonstration now puts catalog/lakehouse discovery
in Part I and graph workflows in an optional Part II. Do not expand that demo's
main workflow or edit its book/site as part of this Grust task. Metadata discovery
is not a reason to execute analytics. MCP exposure can later wrap the same registry;
it must not create another algorithm implementation or authorization bypass.

## 2. Terminology and source ownership

| Name | Meaning in this work |
| --- | --- |
| Icebug | Original C++ NetworKit fork with Arrow graph support |
| Icecat | First Rust/Arrow rewrite; its internal crates still use `icebug-*` names |
| Grustcat | Experimental Grust-compatible Rust analytics adapter in Icecat |
| Grustcat Cypher | Grust parser/analyzer plus a narrow, separate typed Arrow backend |
| Grust | Target upstream property-graph library and backend/query ecosystem |
| Neo4j GDS | Official implementation used as an independent benchmark participant |

Do not rename the target subsystem to Icecat or add dependencies from Grust into
Icecat/Grustcat. Port or extract reusable kernels into Grust-owned crates, retaining
licenses and notices. Grustcat should ultimately become a compatibility adapter
and benchmark client of Grust analytics rather than a second owner of the kernels.

### Committed source references

The current work is committed and pushed; clone Git repositories directly. No new
source archive is needed for this handoff.

| Repository | Branch and pinned source commit |
| --- | --- |
| [querygraph/grust](https://github.com/querygraph/grust/tree/work/arrow-interchange) | `work/arrow-interchange` — `62b8b0fa2b12ec84ee02b5296969efeaf0367a58` |
| [querygraph/icecat](https://github.com/querygraph/icecat/tree/feat/rust-rewrite) | `feat/rust-rewrite` — `3cbc07a510c0bf1803f83a10776d40d0e6f556ba` |
| [querygraph/adversarial-graph-algorithms](https://github.com/querygraph/adversarial-graph-algorithms) | Historical measured protocol/evidence: `1dafd6254762c690bd72f46511fb4f4e5b78f9ca`; this handoff follows that commit |

Grust's Arrow branch is based on `65b5416243a39a01014b2bf3f48737f29786162f`.
At publication, `origin/main` had 21 newer commits. Reconcile the Arrow commit with
current upstream before implementing the generalized subsystem; do not overwrite
newer work. The source is available on a branch, not a new crates.io release.
Icecat is published through the QueryGraph fork because the current GitHub account
could not push to `Ladybug-Memory/icebug`. Preserve source licenses and notices.

### Obtain and verify the reference implementation

Use sibling directories: the experimental crates' Cargo path dependencies expect
`icecat/` and `grust/` to share a parent.

```sh
mkdir grust-algorithms-work
cd grust-algorithms-work
git clone --branch work/arrow-interchange https://github.com/querygraph/grust.git grust
git clone --branch feat/rust-rewrite https://github.com/querygraph/icecat.git icecat
git clone https://github.com/querygraph/adversarial-graph-algorithms.git algorithms
git -C grust checkout --detach 62b8b0fa2b12ec84ee02b5296969efeaf0367a58
git -C icecat checkout --detach 3cbc07a510c0bf1803f83a10776d40d0e6f556ba
cargo test --locked --manifest-path grust/Cargo.toml -p grust-arrow
cargo test --locked --manifest-path icecat/rust/Cargo.toml
cargo test --locked --manifest-path icecat/rust/crates/grustcat/Cargo.toml
cargo test --locked --manifest-path icecat/rust/crates/grustcat-cypher/Cargo.toml
# After reference checks, create your implementation branch from current Grust main
# and reconcile the Arrow commit with it. Keep the pinned references available.
```

The existing published benchmark retains its original measured inputs and receipts
under `publication/`; those establish historical provenance. They are not the
source-delivery mechanism for this task. Use the committed checkouts above for
implementation and local-development benchmarks.

### Validation when committing this handoff

The pinned checkouts passed the Icecat core/algorithms/IPC tests, optional
DataFusion integration, parallel algorithm tests, Grustcat parity tests, Grustcat
Cypher tests, and Grust Arrow/facade tests. Duplicate Python test-name checking
also passed. The DataFusion test emitted a macOS linker unwind-size warning but
completed successfully. These focused checks are not a fresh full C++/Python or
Grust backend matrix, nor a rerun of the published Docker measurements.

### Files to inspect first

Paths in this table are relative to the corresponding repository.

| Source | Why it matters |
| --- | --- |
| Grust `AGENTS.md`, `PUBLISH.md`, `FIRSTPAIR.md`, `RELEASES.md` | Engineering, neutrality, release, and book contracts |
| `crates/grust-core/src/lib.rs` | `Graph`, `GraphIndex`, identities, values, backend contracts |
| `crates/grust-core/src/typed_graph_index.rs` | Existing indexing abstractions; avoid redundant projection APIs |
| `crates/grust-arrow/src/lib.rs`, `README.md` | Unreleased interchange contract and explicit limitations |
| `crates/grust-cypher/src/read.rs` | `procedure_signature`, `procedure_rows`, CALL/YIELD execution |
| `crates/grust-cypher/src/semantics.rs` | Semantic scope and validation |
| `crates/grust-cypher/src/read_policy.rs`, `read_budget.rs` | Procedure admission and existing query budgets |
| `crates/grust-cypher/src/pushdown.rs` | Catalog/TVF pushdown, correlation, backend execution classes |
| `crates/grust-cypher/src/session.rs`, planner and named-graph tests | Query context and graph selection |
| Icecat `rust/crates/grustcat/src/{lib,adjacency,interchange}.rs` | Kernels, packed adjacency, Arrow adapters |
| Icecat `rust/crates/grustcat-cypher/src/{lib,plan}.rs`, `tests/queries.rs` | Narrow backend and semantic-oracle tests |
| Icecat `rust/crates/icebug-core/src/execution.rs` | Existing context semantics; not a budget-enforcement proof |
| Icecat `rust/crates/icebug-algorithms/` | Independent Rust kernels and tests |
| Benchmark `docker/`, `neo4j/compare.py`, `check_arrow.py`, `check_cypher.py` | Protocol, official GDS calls, correctness checks |

Re-find symbols at current HEAD; line numbers and module organization may change.

## 3. What already works, and what does not

Grustcat projects a validated Grust graph into packed outgoing/incoming adjacency
once. Targets and weights are contiguous Arrow buffers; kernels do not traverse
property maps in their inner loops. The projection costs O(V+E) copying/allocation.
The two orientations occupy approximately `16*(V+1) + 32*E` bytes, before the
retained Grust model, ID maps, scratch, and allocator overhead. Preserve the locality
benefit without assuming every algorithm needs both orientations or weights.

The current Arrow interchange represents node IDs and labels as strings, directed
edge endpoints and optional edge IDs, and scalar properties as typed columns.
`present.<key>` distinguishes absent properties from explicit null values in
`property.<key>`. It preserves isolates, loops, parallel edges, row order, and edge
IDs. It rejects mixed non-null property types and complex values rather than
silently stringifying them. Grust supports parallel edges; Icecat's simple-graph
builder rejects them. Do not adopt the latter restriction silently upstream.

Current IPC support accepts one RecordBatch in each of two Arrow **file-format**
inputs. It has no multi-batch/stream-format support, mmap, spill, or hard untrusted
input allocation bound. Arrow-to-Grust conversion materializes values. Direct
Arrow input/output is implemented; zero-copy graph construction is not.

Current Grust CALL execution uses a closed signature match and a closed execution
match, returning `Vec<Vec<Value>>`. Arguments are evaluated per incoming row;
YIELD supports projections/aliases and filtering. CALL and UNWIND materialize and
clone intermediate bindings. The reference engine now also has substantial
budgeted/indexed/pushdown machinery: extend it rather than bypassing its checks.
`ReadQueryPolicy::allow_catalog_procedures` currently gates CALL generally, while
pushdown knows particular catalog and TVF forms. Both need deliberate integration.

Grustcat Cypher validates an entire AST against a limited subset and maps it to
kernels or fused path aggregates. It rejects unsupported syntax. It does **not**
modify the general dispatcher, use its read-policy admission, provide arbitrary
Cypher execution, or enforce a hard budget for all allocations. Its timing is not
the timing of the general Grust executor. Preserve it as historical evidence and
a migration oracle; do not present it as the completed architecture.

## 4. Target architecture and dependency direction

Choose final module names after reviewing upstream. A reasonable proposed split is:

- `grust-core`: graph identity/snapshot capabilities and minimal shared types.
- `grust-algorithms`: typed projections, reusable algorithm kernels, parameters,
  results, cancellation and accounting integration; no Cypher dependency.
- `grust-procedures`: reusable signatures, registry, invocation/cursor contracts,
  depending only on foundational types. A focused existing module is acceptable
  if a new crate would add no useful boundary.
- `grust-cypher`: parse/validate/plan CALL using registry metadata; execute through
  provider interfaces. Never depend on Grustcat or Icecat.
- `grust-algorithm-procedures`: adapters registering algorithm implementations;
  depends on algorithms and procedure contracts, not on parser internals.
- `grust-arrow`: interchange and optional Arrow adapters at a dependency layer
  that does not create a cycle. Arrow-specific result adapters may warrant their
  own module/crate if both the executor and providers need them.
- Facade `grust-graph`: feature-gated assembly and convenient public entrypoints.

Require a dependency diagram and minimal feature matrix before adding crates.
Use one authoritative algorithm implementation for direct calls and procedures.
Keep external registration feasible without exposing executor internals. A
statically linked Rust registration API is sufficient initially; shared-library
plugin loading is not a prerequisite.

### Immutable graph/projection capability

An invocation receives a validated graph snapshot/projection handle, never an
unchecked graph name interpreted differently by each provider. Record graph and
snapshot identities, external-to-dense ID mapping, node/edge selection, orientation,
weight property and missing-weight policy, parallel-edge policy, and preparation
cost. Selected nodes with no selected edges remain isolates.

Expose efficient typed adjacency views for the kernel's needs. Build reverse
adjacency lazily or explicitly when requested. A snapshot handle owns or pins the
necessary buffers; eviction cannot invalidate an active cursor. Cache keys include
snapshot, projection parameters, relevant authorization scope, and representation
version. Do not reuse a projection across different tenants or stale snapshots.
If a backend cannot provide a stable snapshot, disclose/reject that execution mode.

Preserve external string identities at the API boundary. Dense integer indices
are internal unless a result explicitly declares them and carries its ID mapping.
Do not reinterpret `NodeId` as an Arrow row offset. Edge identity matters for
multigraph paths: node sequences alone cannot identify which parallel edge was used.

Support an Arrow-native construction path without converting every property into
`Value` and back. Topology validation, ID indexing, and CSR construction still may
copy. State precisely which buffers are shared and which are allocated.

### One registry for signatures and implementations

Each immutable procedure definition declares its canonical name/aliases/version,
argument types, nullability, defaults, named option schema, output names/types,
read/write mode, determinism, correlation behavior, graph requirements, streaming
behavior, and resource controls. Reject duplicate registrations and aliases.

The same definition drives static argument/YIELD checking, dynamic parameter
validation, introspection, execution, and backend capability negotiation. Reject
unknown configuration keys instead of silently using defaults. A prepared plan
pins the registry generation/signature version; replacing providers must not alter
an already prepared plan's schema or meaning.

Retain `db.labels`, `db.relationshipTypes`, `db.propertyKeys`, `tvf.range`, and
`tvf.keys` as built-in providers with compatibility tests. Preserve current name
normalization and YIELD behavior unless a documented compatibility change is made.
A read-only algorithm permission must not silently broaden the catalog-procedure
flag. Admission must account for provider mode, graph scope, projection access,
and backend support before work begins.

A useful contract sketch—not an existing or mandatory Rust signature—is:

```text
ProcedureDefinition { name, arguments, options, output_schema, mode, capabilities }
ProcedureRegistry.resolve(name) -> pinned definition + provider
Provider.open(validated arguments, invocation context) -> Result<Cursor>
Cursor.next_batch() -> Result<Option<schema-checked owned batch>>
InvocationContext { graph capability, query budget, cancellation, deadline,
                    concurrency, execution identity, metrics }
```

Use typed errors for unknown procedure/option, invalid arguments, unsupported
representation/backend/mode, denied access, stale graph/plan, budget exceeded,
cancelled, numerical failure, and provider failure. Do not turn unsupported work
into empty successful results. Translate these errors at transport boundaries.

### Backend execution is explicit

Provide at least two integration proofs: a local immutable graph and another
adapter/snapshot source supported by Grust. Each backend declares whether a
procedure runs natively, through an explicitly selected local projection, or is
unsupported. No automatic download/fallback to the whole graph, no change of
named graph, and no reuse of another backend's timer as its own result.

If native execution is supported, its signature/output/semantics must match the
registered contract. Preserve the existing pushdown classification and tests.
Introspection and EXPLAIN should identify provider, graph snapshot, execution
class, projection preparation, and streaming/blocking boundaries.

## 5. Streaming and resource contracts are mandatory

A cursor alone does not solve memory growth. CALL, YIELD, projection, filtering,
UNWIND, and ungrouped aggregation must consume incrementally. Correlated CALL
still invokes once per incoming binding under current semantics; cache projection
preparation separately from algorithm results. Do not hoist a correlated call
because it happens to return the same answer on a fixture.

Owned Arrow RecordBatches are a useful fast path; bounded scalar batches can keep
reference compatibility. Define schema consistency, null semantics, batch ownership,
retention, and accounting. Arrow buffers may outlive the cursor through shared
ownership: dropping a cursor must not release budget charges for retained buffers.
Consumers impose backpressure; cap prefetch and concurrent invocations.

Global aggregates maintain incremental states. Grouped aggregates, DISTINCT,
sorting, joins, and collecting functions need budgeted materialization, an explicit
spill implementation, or a documented resource-limit/unsupported outcome. Never
silently truncate. `LIMIT` after an aggregate does not bound the aggregate input.
An early LIMIT may stop output consumption; it does not guarantee a global kernel
can avoid its preparation/computation. Describe both costs honestly.

Charge projection buffers, ID maps, queues/heaps/stacks, iterative vectors,
predecessors, result arrays, queued batches, correlation state, and downstream
operator allocations. Reconcile these with existing Grust budgets; do not add an
unrelated counter that excludes half the execution. Reserve before allocating and
use fallible allocations where practical. Poll cancellation in long adjacency rows,
heap/iteration loops, path reconstruction, and result production. Parallel workers
share a query budget and thread cap. Errors/drop/cancellation release owned resources.
Partial output must remain visibly failed, never a complete result or partial commit.

Full-path output emits source-first node IDs and cumulative costs for each reachable
target, including the source. Reuse one path buffer or produce bounded owned path
batches. Borrowed visitor slices are valid only during the callback; Arrow results
need retained ownership. Checked offsets are mandatory: 32-bit List offsets can
overflow even when individual paths fit. Use bounded batches and/or LargeList;
64-bit offsets alone do not make total output fit in memory. A single oversized
path also needs an explicit allocation-limit outcome or documented chunk protocol.

Fuse typed UNWIND/index/aggregate operations over real path arrays where semantics
permit it. Do not substitute a chain formula, count-only traversal, or distance
vector for requested full paths. Validate the general plan against the reference
executor on small cases, including nulls, aliases, duplicates, correlation and errors.
DataFusion is suitable for Arrow expressions/aggregation or as an optional execution
adapter; it is not a substitute for adjacency kernels or a second Cypher semantics
engine. Keep its dependency optional unless a measured design review supports more.

## 6. Algorithm contracts and staged catalog

Before implementing a kernel, specify direction, weights, defaults, output schema,
ID domain, order guarantees, null/unreachable behavior, determinism, numeric types,
limits, and the exact result being computed. Validate once at projection or invocation
boundaries; do not guess graph semantics in inner loops.

| Initial algorithm | Required decisions and checks |
| --- | --- |
| BFS | Hop distances/reachability, source validation, isolates and orientation; predecessor/path output is a distinct option |
| Dijkstra | Finite nonnegative weights, explicit missing/null-weight policy, zero-cost cycles, overflow and unreachable nulls |
| Full shortest paths | One selected shortest path per reachable target; ties allowed by documented rule; not enumeration of all equal-cost paths |
| WCC | Directed input treated by weak connectivity; include isolates; canonicalize labels for comparison |
| SCC | Directed reachability components; iterative traversal for deep graphs; avoid recursion overflow |
| PageRank | Damping, max iterations, tolerance/norm, personalization, dangling mass, edge weights, normalization and non-convergence status |

Reject invalid sources, NaN/infinite weights, invalid damping/tolerance, and output
integer overflow explicitly. A weighted path's cumulative costs start at zero and
end at its distance. For multigraphs, retain edge identity or define how the path
result disambiguates edges. A predecessor representation must not create cycles on
zero-weight ties. Specify whether duplicate edges contribute separately to degree,
PageRank and path choices; coalescing requires an explicit reducer.

Broader catalog roadmap, using the same registry/projection/cursor contracts:

| Family | Candidate additions and special obligations |
| --- | --- |
| Traversal and reachability | DFS, multi-source BFS, bounded reachability, topological order with cycle reporting |
| Paths and distances | A*, Bellman–Ford with negative-cycle reporting, DAG paths, all-pairs and k-shortest paths with output/work limits |
| Centrality | Degree, closeness/harmonic, exact and sampled betweenness, eigenvector/HITS; normalization and directed/disconnected semantics |
| Structure | Triangle counts, clustering coefficient, k-core, articulation points/bridges, bipartiteness; multigraph semantics |
| Communities | Label propagation, Louvain/Leiden; seeded randomness, weighted/directed assumptions, convergence and quality objective |
| Trees and flow | Minimum spanning forest, max-flow/min-cut; disconnected input, capacities and direction contracts |
| Similarity and prediction | Jaccard/overlap and neighborhood scores; candidate generation and pair-count budgets |
| Embeddings and ML | Separate opt-in family with model/artifact lifecycle, seeds, training provenance and resource requirements |

These are proposed scope families, not assertions of current Grust or GDS coverage.
At phase zero, turn them into a tracked coverage matrix with priorities, owner,
reference oracle, and deferred status. Prefer complete, composable vertical slices
to empty procedure registrations or misleading compatibility aliases.

Names such as `grust.algorithms.pagerank` are proposed. Preserve existing application
APIs through adapters where feasible; `grustcat.*` remains historical. Use a GDS
namespace only for deliberately tested compatibility, not approximate resemblance.
Start with read/stream and stats/estimate modes. Mutate/write modes require a later
explicit transaction/capability design: algorithms compute against a pinned snapshot,
write-back validates that snapshot and commits atomically, and cancellation never
leaves partially written scores. Do not implement mutation as a hidden side effect.

## 7. Evidence inherited from this work

Published protocol: [adversari.al/graph/algorithms](https://adversari.al/graph/algorithms).
The independent query-suite and strain pages are separate experiments. Do not pool
their results or apply their timing corrections to these algorithm measurements.

The five-way Docker completion run used Linux ARM64 on an Apple M1 Max host.
Both containers had a two-CPU quota and 4 GiB memory limit; algorithm concurrency
was one. Neo4j Community 2026.08.0/GDS 2026.08.1 used a 2 GiB heap and 512 MiB page
cache. Full-path transactions and native processes had no deadline. The official
GDS procedure was `gds.allShortestPaths.dijkstra.stream`, aggregated server-side.

| Chain nodes | Icebug s | Icecat s | Grustcat s | Grustcat Cypher s | GDS server s |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 16,384 | 1.102 | 1.053 | 1.032 | 1.028 | 11.889 |
| 65,536 | 22.233 | 16.648 | 16.710 | 16.727 | 194.113 |

There was **one measured sample and zero warmups** per large case. These numbers
show completed equivalent requested output and correctness, not stable rankings
or a portable performance guarantee. The 65,536-node chain contributes
2,147,516,416 entries to **each** path array per engine. Distances and independent
chain aggregate formulas were checked. Checksums on arbitrary tied graphs do not
prove every interior path element; use full structural checks on small cases.

Timers differ explicitly: native timers cover algorithm, path construction and
consumption; Rust also constructs Arrow distances; Grustcat Cypher includes parse,
analyze and plan; GDS reports server query time and separately records client wall
time. Loading/projection are outside those timers. Future runs must additionally
measure end-to-end loading and projection, not hide their cost in a kernel metric.

All five variants passed 30 small cases (six families times five algorithms), and
the image passed 45 kernel/Arrow interchange checks. BFS output shape and PageRank
convergence criteria differ across engines and are checked under stated comparison
rules. Historical distance-only native versus full-path GDS timings are not equivalent
work. Keep their timeout/error evidence, but do not reuse them as parity measurements.

Raw files under `publication/evidence/` include `docker-cypher-full-path.json`, its
`-environment.json`, `docker-cypher-smoke.json`, image validation, and SHA-256 receipts.
The full unrounded numbers, query text, options, and source hashes are authoritative.

## 8. Reproduction and comparison workflow

First reproduce the frozen baseline without editing it:

```sh
cd algorithms
./docker/run.sh --full-path --sizes 128 --warmups 1 --repeats 1 --label baseline-smoke
./docker/run.sh --full-path --algorithms dijkstra --families path \
  --sizes 16384 65536 --warmups 0 --repeats 1 --label baseline-completion
```

Docker Compose v2 and Python 3.12+ are required. Use a dedicated machine/resource
envelope and retain results. Long-path runs can be expensive. Read the protocol;
do not silently add a deadline and report its absence as a correctness failure.
For statistical measurements, use repeated optimized runs, calibrated warmups,
reported dispersion, fixed seeds and multiple graph families. Do not mix native
macOS, Docker ARM64, native x86-64, or emulated runs into one speed ratio.

**Important:** `docker/run.sh` always prepares the frozen snapshot by default.
It will overwrite a manually staged local context. To test new upstream code:

```sh
python3 docker/prepare.py --local --icecat /absolute/grust-algorithms-work/icecat \
  --grust /absolute/grust-algorithms-work/grust
# Adapt benchmark Cargo dependencies/binaries and Dockerfile for the NEW provider first.
# Then use Compose directly, so run.sh does not replace the changed sources.
docker compose build
mkdir -p docker-results
docker compose up -d --wait neo4j
docker compose run --rm --user "$(id -u):$(id -g)" benchmark \
  --full-path --sizes 128 --warmups 1 --repeats 3 --label upstream-smoke
docker compose down
```

The existing harness still invokes the old Grustcat kernels. Merely staging new
Grust does **not** benchmark new generalized algorithms. Add separately named
participants for direct upstream algorithms, generalized CALL, and any backend-native
execution. Record which provider was invoked; add a test/counter that fails if a
new column accidentally delegates to the old benchmark implementation. Preserve
all original participants and official GDS calls as independent references.

Compare correctness before timing. Report kernel, projection, full query including
compilation, prepared-query execution, transport/serialization, end-to-end wall time,
and peak memory separately. Account for retained model/projection/batch memory.
Use small, medium and large paths, hubs, clusters, layered, uniform and R-MAT graphs,
plus isolates, duplicate edges, ties and disconnected components. Seeds and generator
versions belong in receipts. Keep pass, mismatch, unsupported, unavailable, timeout,
error and not-applicable as distinct outcomes.

Engineering targets are internal properties: no per-edge property-map lookup in
hot kernels, projection reused across calls, no per-path-entry binding clone in
fused consumption, resource use bounded by the declared working set, and measured
low dispatch overhead relative to the **same direct Grust kernel**. Choose numeric
thresholds from repeatable measurements on the target machine before optimization.
Do not optimize a protocol or document to favor a named benchmark participant.

## 9. Delivery phases and acceptance gates

1. **Inventory and decisions.** Reconcile current Grust with the frozen Arrow work;
   record existing public APIs, feature/dependency design, schemas, ID policy, budget
   ownership, backend capability matrix, and prioritized algorithm matrix. Run current
   tests first and preserve unrelated changes. No implementation milestone is complete
   merely because this design is written.
2. **General registration.** Migrate catalog/TVF built-ins, introduce registry-backed
   validation and admission, and add a tiny external provider integration test. Prove
   unknown names/options/YIELD fields fail before invocation; preserve correlated
   invocation counts, aliases, filtering, graph scope and pushdown compatibility.
3. **Projection and direct kernels.** Integrate Arrow support and the six initial
   algorithm operations; expose direct typed Rust calls and canonical results. Test
   IDs, weights, multigraphs, numerical edge cases, conversion fidelity and cancellation.
4. **Streaming execution.** Integrate bounded provider results through CALL and its
   consumers. Prove early drop cleanup, mid-stream failure, retained-batch accounting,
   cancellation and budget failure. Test batches of 1, small irregular sizes, and large
   sizes; answers and errors must remain semantically consistent.
5. **General algorithm procedures.** Register the initial catalog with typed options,
   introspection and EXPLAIN. Exercise them through the ordinary public query entrypoint
   and a second backend capability path. New providers require no executor edits.
6. **Full-path and performance qualification.** Validate generic/fused execution against
   the reference interpreter, then run the large chain under a declared memory envelope.
   Demonstrate every requested path element is consumed without billions of row objects.
   Add current upstream participants to the neutral Docker harness and retain all evidence.
7. **Broader catalog and release.** Expand the prioritized families through the same
   contracts. Update public docs/examples, compatibility matrix, changelog, Grust book,
   and release artifacts. Follow the target checkout's release instructions; report which
   algorithms/modes/backends remain unsupported rather than calling the catalog universal.

Required regression cases include empty graphs, invalid/duplicate IDs, missing endpoints,
self-loops, parallel edges, isolates, deep chains, high-degree hubs, zero weights,
negative/nonfinite weights, tied paths, invalid options, null parameters, arithmetic
overflow, non-convergence, graph mutation while a snapshot is pinned, named-graph and
principal isolation, concurrent queries, consumer retention, provider exceptions,
cancellation during preparation/computation/consumption, and allocation-limit failures.
For each algorithm use an independent oracle or mathematical invariant on small graphs.
Test Arrow absent versus null, integer precision, schema/type errors, chunk boundaries,
and failure writing the second IPC sink. Make unsupported IO modes explicit until added.

Run the relevant workspace CI and feature combinations. Typical starting commands
(verify package/feature names at current HEAD) are:

```sh
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
cargo test --workspace --doc
cargo build --release --locked
# Before release, as required by Grust's AGENTS.md:
cargo package --workspace --allow-dirty
```

Do not suppress unrelated failures; record baseline failures and distinguish checks
requiring external backends. Keep tests in focused modules and avoid enlarging already
oversized executor files. Honor current AGENTS.md neutrality, named-release, dependency
order, crates.io verification, and book rules. The authoring of this handoff does not
itself publish or implement anything; the implementing agent follows its actual session
scope and the repository's release contract. Do not infer instructions to send messages
or publish unrelated sites from this document.

## 10. Required final handoff from the implementing agent

Deliver a source commit/PR with an architecture summary, runnable direct Rust and
ordinary Cypher examples, algorithm/backend/option coverage matrix, migration notes,
Arrow schema and ID contracts, budget/cancellation semantics, and retained test and
benchmark receipts with exact source/container identities. State where results are
materialized or copied and which operations can spill. Include the external-provider
example that proves extensibility and the full-path streaming evidence.

Explicitly distinguish: implemented versus proposed; available in source versus released;
reference versus optimized versus backend-native execution; and completed correctness
checks versus statistical performance evidence. List remaining work with concrete
acceptance criteria. Do not stop at the benchmark-specific dispatcher or leave a second
hard-coded signature table behind the public registry.
