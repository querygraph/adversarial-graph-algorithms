# Grust performance review and experiment plan

Reviewed 2026-09-18. This pass is review and planning only, at the user's
request while Fable samples. No source changes, builds, tests, profiling, or
new benchmark runs were performed. No speedup below is newly measured.

The objective is less execution, allocation, and preparation overhead while
preserving results, resource admission, and disclosed timing boundaries.

## Baseline and existing findings

The local `.upstream-grust` checkout is clean at
`3a739544c3d9e6581bdac7563d8cc3a66cdcf828`. It is **not** the latest experimental
implementation. Fable's active run uses
`.measurements/sampled-4096/context/grust-upstream`; its `resources.rs` contains
atomic work accounting and deadline sampling. Treat the staged source hashes
and eventual run receipts as authoritative, not the older checkout alone.
Do not modify that context or draw conclusions from incomplete result files.

[The existing report](optimization-results.md) records:

- Atomic work admission (`23de753`) already replaced per-charge mutex locking.
  It reports 1,224 passing paired samples and substantial direct-kernel gains.
  Replacing the mutex is completed prior work, not a new proposal here.
- A deadline-sampling probe reduced the 4096 full-path Cypher query from
  21,721 ms to 2,574 ms. This is a probe, not completed qualification of the
  active participant. The report attributes the unusually expensive clock
  reads to this host's Xen clocksource.
- Allocator and LTO experiments are already available. Their effects are mixed;
  neither warrants a universal speedup claim or another first-priority sweep.

The source findings below are structural observations. Their remaining runtime
importance must be profiled after deadline sampling; old hotspot percentages
cannot predict the new distribution. Paths are relative to the Grust source root
unless a benchmark-repository path is explicitly given.

## Prioritized changes

| Priority | Candidate | Main affected surfaces | First evidence to collect |
|---|---|---|---|
| 1 | Skip sampling bookkeeping when no deadline exists | Direct, Arrow, DataFusion, snapshot kernels | Paired no-deadline kernel timings and instruction counts |
| 2 | Charge bounded contiguous loops in chunks | All kernels and projection | Meter share after sampling; exact budget boundary tests |
| 3 | Produce actual multirow scalar procedure batches | Cypher BFS, distances, WCC, SCC, PageRank | Batches, allocations, and query time per output row |
| 4 | Transfer or borrow procedure values instead of deep copying | Cypher paths and other large values | Allocated bytes and copy stacks per path entry |
| 5 | Avoid temporary UNWIND arrays; simplify numeric aggregation | General Cypher array consumers | Allocation and scalar-dispatch profiles |
| 6 | Avoid duplicate internal projection validation | All preparation paths | Separate map-building, validation, and CSR timings |
| 7 | Precompute PageRank transition probabilities | Iterative weighted PageRank | Iteration time, setup time, and additional memory |
| 8 | Improve path-buffer layout and heap operations | Direct and adapted shortest paths | Post-meter reconstruction and heap profiles |
| 9 | Reuse Arrow schemas and amortize short-path batch metadata | Arrow and DataFusion results | Metadata allocations versus copied payload bytes |

### 1. No-deadline fast path in sampled resource accounting

In the active staged `crates/grust-procedures/src/resources.rs`,
`check_state(Sampled)` performs `charges_since_deadline_read.fetch_add(1)`
before testing whether `limits.deadline` is `Some`. Thus deadline-free direct
calls still perform a sampling-counter atomic in addition to work admission.

After checking cancellation, return immediately if there is no deadline.
Only executions with deadlines need the sampling counter. This preserves exact
work admission and cancellation checks and is the smallest first experiment.
Compare against Fable's sampled version, not the old mutex implementation.

Also clarify sampling units: the current implementation counts **charge calls**,
not the `units` argument. One call can admit a whole chunk. A 1024-call interval
does not imply a 1024-work-unit or fixed wall-time response bound. Keep exact
checkpoints at explicit boundaries, and measure deadline overshoot for long
adjacency rows and large output conversions before changing either interval.

### 2. Fewer shared atomic operations in bounded loops

`grust-algorithms/src/{traversal,pagerank,shortest}.rs` and
`projection/adjacency.rs` repeatedly charge one unit inside tight loops.
Atomics remove locks but still serialize each update to shared state.

Start with fixed, contiguous operations: array copies, initialization,
normalization, and adjacency slices whose length is known. Pre-admit a bounded
chunk and process it with periodic exact checkpoints. Existing buffer filling
and path reversal already demonstrate chunked work; extend carefully.

Do not silently change near-limit behavior by rejecting a whole chunk where
the old code would admit a prefix. Retain the scalar path near budget exhaustion
or design an explicit partial-grant mechanism. Preserve error ordering and
accounting for an early consumer stop. Dynamic heap and predecessor loops are
later candidates, not grounds for unchecked post-hoc charging.

A local work allowance is a larger alternative: distinguish globally reserved
credits from consumed work, refund unused credits on drop, and preserve shared
admission under concurrency. Do not introduce it until profiling justifies the
extra protocol and its effect on `usage()` is specified and tested.

### 3. Bounded scalar batches

`grust-algorithm-procedures/src/output.rs::AlgorithmCursor::next_batch`
returns exactly one scalar row, despite the context having `batch_rows`.
Each row incurs an outer allocation, reservation ownership, cursor dispatch,
and downstream batch validation. This affects all scalar algorithm results.

Fill up to the admitted row limit using one batch reservation and outer vector.
Use a byte cap as well as a row cap for long IDs. Start with scalar results;
keep paths separately bounded because a single path can already be large.
Measure sizes 1, 32, 256, and 1024 to select a useful default rather than
assuming the largest batch wins. Report the extra production caused by early
LIMIT, while keeping cleanup and error visibility intact.

### 4. Procedure-to-Cypher ownership transfer

`output.rs::path_batch` converts dense path rows to owned string ID arrays,
copies costs, and constructs edge ordinals. Then
`grust-cypher/src/read/streaming.rs` iterates `batch.rows()` and calls
`clone_value` on yielded fields. Large path arrays therefore undergo another
owned copy at the binding boundary. Array fusion already avoids cloning the
entire row for **every expanded element**; that is not missing functionality.

Investigate consuming a batch into owned rows, or a borrowed binding overlay
valid while the batch reservation remains alive. An ownership-transfer API must
carry memory reservations with moved values; dropping the cursor must not
release charges for retained arrays. Handle duplicate YIELD aliases and
correlated input bindings explicitly. Apply this generically to procedures.

A later typed batch interface could expose dense ID indices plus an immutable
ID dictionary to compatible consumers, reducing per-entry string allocation.
That is an architectural extension with schema/lifetime implications. Preserve
external string IDs and materialize the public representation when required;
never substitute numeric row indices for user IDs.

### 5. Streaming UNWIND and numeric aggregation

`grust-cypher/src/read/streaming_fusion.rs::try_unwind` compiles expression
inputs once per incoming row, but then calls `eval` on the UNWIND expression.
The fused path consumes an owned typed array, including an evaluated `range`.

Borrow variable/parameter arrays, and iterate admitted integer ranges directly
without constructing an index vector. Keep every requested array access and
aggregate operation. Preserve range endpoints, negative steps, overflow,
null behavior, expression errors, and equivalent work admission.

`read/streaming_aggregate.rs` implements each SUM update through
`sum_return_values(&[sum.clone(), value])`. A dedicated numeric accumulator
can avoid repeated generic dispatch and the two-value scan. Preserve checked
integer addition, the precise point of float promotion, null omission, and
iteration order. Measure before attempting SIMD or reassociation, which can
alter floating-point results. General compiled input slots can later avoid
rebuilding small boxed expression trees for each incoming row.

### 6. Projection construction without redundant checks

`grust-algorithms/src/graph_input.rs::from_graph` builds an ID map, validates
IDs/endpoints, validates extracted weights, and assigns ordinals by enumeration.
`projection.rs::from_buffers` then builds the retained ID map, checks weights
again, and allocates a HashSet to validate ordinal uniqueness.

Introduce a private validated-input builder that carries the already established
invariants and transfers reusable lookup state where practical. Ordinals
produced by enumeration do not require a second hash set. The public arbitrary
topology/Arrow entrypoints must retain full validation. Keep validation of
unselected nodes and missing endpoints: filtering must not hide invalid input.

Projection caching already exists in procedure `preparation.rs`; do not propose
it as new. Cross-query reuse is a separate design because `GraphProjection`
retains an `ExecutionContext`. A reusable immutable topology would need separate
storage ownership and per-query resource admission, snapshot/principal isolation,
and cache eviction. Report cold and reused preparation as distinct classes.

### 7. PageRank transition preparation

`grust-algorithms/src/pagerank.rs` computes each edge probability as
`(weight / row_maximum) / row_total` during every iteration. The row scaling is
intentional: it avoids overflow even for multiple `f64::MAX` weights.

Experiment with an admitted probability buffer computed once using the same
two divisions and reused across iterations. Retain accumulation order and
dangling semantics. Compare setup cost plus execution, not iterations alone;
the extra roughly eight bytes per arc can outweigh the gain for short runs.
Keep a low-memory path and test extreme weights, tiny positive weights,
personalization, isolates, and non-convergence. Do not replace the scaled formula
with an unguarded reciprocal product that changes underflow/overflow behavior.

### 8. Reconstruction and heap layout

`shortest.rs` reconstructs each predecessor chain backwards into three vectors,
then reverses nodes, costs, and edges separately. Consider a reusable suffix
buffer filled backwards, returning a forward slice without reversal. It still
constructs every requested node, cost, and edge. Evaluate initialization cost,
extra retained length, and memory admission against the current capacity-only
scratch. Do not trade away short-path performance to improve only long chains.

The indexed binary heap maintains inverse positions on every swap. A hole-based
sift or a small higher-arity heap may reduce stores on graphs with substantial
frontiers. Preserve stable cost/node tie ordering, bounded O(V) storage, and
zero-weight behavior. Chains alone cannot evaluate heap changes.

### 9. Arrow output ownership and batch metadata

A further review of the sampled context confirms that
`grust-algorithms/src/arrow_output.rs::ArrowResultCursor` **already batches
scalar rows** using `batch_rows`. Candidate 3 applies to the scalar procedure
adapter, not this Arrow cursor.

Arrow full paths still create six builders and a RecordBatch per destination.
`finish` constructs a batch with `try_from_iter`, attaches reservation ownership
to each array, and constructs another batch with the resulting columns.
Investigate retaining the invariant schema per cursor and constructing the final
batch directly after ownership attachment. Measure schema/metadata allocations
separately: this is more likely to matter for many short paths than for one
large array. Do not assume ownership attachment copies physical buffers; inspect
`retain_array_owner` before attributing a payload-copy cost to it.

A separate experiment can pack several short full paths into a byte-bounded
LargeList batch. Long paths still require individually bounded output. Preserve
row order, original edge ordinals, Utf8 child-offset limits, and reservations
that survive raw array exports and slices. Scratch buffers cannot be reused
while an emitted batch still owns their data; use ownership transfer or an
explicit return-to-pool mechanism rather than mutating shared Arrow storage.

The benchmark's `docker/arrow_adapter.rs` parses returned string node IDs when
consuming output. Account for that cost separately from the library's Arrow
conversion. Replacing external IDs with row indices only in this participant
would change the interface being measured. Likewise, DataFusion currently
collects node and edge scan results before projection; streaming ingestion is
a distinct preparation experiment requiring endpoint-resolution and retained
memory accounting, not a kernel improvement.

## Experiment sequence after Fable finishes

1. Freeze Fable's final source hashes, image digest, allocator, toolchain,
   lockfile, sample outcomes, and resource policy. Reconcile the source checkout
   with that exact implementation in an isolated location.
2. Profile this baseline by phase: loading, projection, kernel, procedure
   conversion, Cypher binding/aggregation, verification, and serialization.
   Use separate diagnostic runs for counters/allocation instrumentation so they
   do not contaminate measured samples. Include no-deadline and finite-deadline
   contexts and retain this host's clocksource in the receipt.
3. Implement candidate 1 independently, then select between 2 and 3–5 using
   the new profiles. Change one factor per pair. Run relevant resource and
   semantic tests before timing. No implementation work is authorized for
   this review-only pass.
4. Run all six families and five algorithms at 128/1024 for correctness; use
   representative 4096/16384 workloads for repeated timings. Include
   distance-only Dijkstra as well as full paths. Use the existing two-CPU,
   four-GiB envelope, fixed seeds/hashes, one algorithm worker, warmups, and at
   least five measured repetitions with alternating baseline/candidate order.
5. Report every sample, median/MAD, phase times, peak accounted memory, and
   per-process RSS where available. Keep regressions and failures visible.
   Repeat noisy cells before accepting a change; then measure combinations
   of independently accepted changes. Do not add individual speedup ratios.
6. Only after small tests pass, run large full-path completion cases. These
   establish completion and resource behavior, not stable rankings from a
   single sample. Preserve the full-path work and current timer boundaries.

Required regression coverage: exhausted and overflowing work budgets;
concurrent charges; cancellation during a high-degree row and long path;
deadline expiry and final-boundary checks; partial batches and early LIMIT;
retained output after cursor drop; arbitrary IDs and duplicate aliases;
invalid endpoints/weights/ordinals; tied paths and zero-cost cycles;
null/overflow/mixed numeric aggregate semantics; and independent provider
behavior through the generic procedure interface.

Acceptance means a reproducible improvement attributable to a concrete change,
with correctness and resource contracts intact and tradeoffs disclosed. No
claim that every workload improves is required. Library changes belong in Grust;
the benchmark retains neutral participants and results. Before any later release,
follow that checkout's AGENTS.md changelog, verification, book, and named-release
requirements. This document neither implements nor releases those changes.
