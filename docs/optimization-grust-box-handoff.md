# Algorithms benchmark optimization handoff

Prepared 2026-09-17. Continue on host `grust`; the strain benchmark is running
on the originating host (`quegee`). Do not build or measure there during that run.

## Objective and current status

Update this algorithms benchmark to exercise current upstream Grust and optimize
its integration and implementation using measured bottlenecks. Preserve equivalent
requested work, correctness checks, resource limits, and all participant outcomes.
Report observed performance, including regressions; no ranking is an acceptance gate.

The user explicitly confirmed **this algorithms benchmark**, rather than the
separate graph-query/strain benchmark. Turso is not currently a participant here.
Group commit accelerates database write workloads; there are no commits inside
these algorithm timers. Do not add a group-commit switch to claim a kernel gain.
Allocator changes may affect input construction, projection, and query execution;
measure those phases separately.

No optimization has been implemented or measured in this session. No benchmark
container has been started. Local review copied three upstream helper files:

- `docker/stage_upstream.py`, copied from upstream `stage_companion.py`.
- `check_upstream.py`, copied from the upstream algorithm benchmark directory.
- `participant_audit.py`, copied from the same directory.

These are unfinished copies, not included in the handoff commit. The root-level
copies are ignored by this repository's allowlist `.gitignore`. The staging copy
still calculates paths as if it lived in Grust and must not be run as-is.
Recreate the helpers from the pinned upstream checkout when implementing the
integration, and fix path ownership and `.gitignore` deliberately.

## Source and host inventory

| Item | Observed revision or state |
| --- | --- |
| Benchmark before this handoff | `78135797b2f4094ff04d0b816b2404404a49a12a` |
| Current clean Grust on quegee | `c8ec3104e203177f2035252c90fc9fdfdfe71b39` |
| Existing clean Grust on grust box | `29fd384c253d044e00b608b1338712b4e3265987` |
| grust box capacity at inspection | Load average 0.00; about 30 GiB available RAM; about 500 GiB free disk; no Docker containers |
| Icecat sibling on quegee | Absent; historical sources available through this benchmark's frozen snapshot |

Capacity is a point-in-time observation: check again before running. An interactive
Claude process was present on grust; do not terminate or interfere with other work.
SSH alias `grust` works from quegee. Cargo and Docker are installed there; toolchain
and dependency availability have not been qualified. Source archives were prepared
under `/tmp` on quegee, but **not transferred**. Fetch Git commits instead.

## Obtain isolated working copies on grust

Fetch this handoff branch into a new benchmark checkout, avoiding changes to any
existing checkout. The branch name is `work/algorithms-optimization-handoff`.

```sh
cd ~/src
git clone --branch work/algorithms-optimization-handoff \
  git@github.com:querygraph/adversarial-graph-algorithms.git
git -C ~/src/grust fetch origin
git -C ~/src/grust worktree add -b work/algorithms-performance \
  ~/src/grust-algorithms-opt c8ec3104e203177f2035252c90fc9fdfdfe71b39
```

If the pinned Grust commit is not available after fetching, locate its remote
branch or transfer it explicitly; do not silently substitute the older local tree.
Read Grust's `AGENTS.md` and applicable instructions before making changes.
Current Grust instructions cover benchmark neutrality and release/book obligations
for substantial crate changes. Keep source edits in the isolated worktree.

## Findings that should guide implementation

1. `docker/run.sh` always calls `docker/prepare.py` in frozen-snapshot mode.
   Merely updating `~/src/grust`, or manually staging local sources then invoking
   `run.sh`, does not measure the new implementation.
2. Historical Grustcat and Grustcat Cypher are Icecat adapters. They must stay
   separately attributed from upstream Grust algorithms and ordinary Cypher.
3. Upstream already supplies `benchmarks/algorithms/stage_companion.py`,
   `check_upstream.py`, and `participant_audit.py`. The staging helper verifies
   the frozen context, preserves historical participants, and adds
   `grust_upstream_direct` and `grust_upstream_cypher` in a separate build stage.
   Start by reproducing that supported integration, rather than rewriting it.
4. The upstream binaries are examples of `grust-algorithm-procedures`:
   `grust-upstream-direct` and `grust-upstream-cypher`. Their shared implementation
   lives at `crates/grust-algorithm-procedures/examples/protocol/mod.rs`.
   They disclose loading, preparation, execution, verification, serialization,
   and end-to-end timings where available, plus provider identity.
5. Direct execution builds a projection before the kernel timer. Ordinary Cypher
   includes parsing, policy validation, projection, and consumption. Full-path
   Cypher performs a separate distance-verification query outside its main timer.
   Preserve these boundaries; their ratio is not pure dispatch overhead.
6. Upstream `crates/grust-algorithms/src/shortest.rs` reconstructs paths with reused
   node, cost, and edge buffers, charging work at each predecessor step and during
   reversal. Inspect the cost of resource accounting, reconstruction, and
   ordinary Cypher aggregation with a profiler before deciding what to change.
   These are hypotheses, not established bottlenecks.
7. The root Cargo manifest has no tuned release profile or allocator selection.
   Current Grust's lockfile contains mimalloc 0.1.52, but that does not activate
   it in these binaries. Record the actual global allocator in build receipts.

## Execution plan

### 1. Establish a current-source baseline

Prepare the historical context with `python3 docker/prepare.py`. Verify the
published source and official Neo4j/GDS archive checksums. Then run the upstream
staging helper from the isolated Grust worktree, with a new output directory:

```sh
python3 ~/src/grust-algorithms-opt/benchmarks/algorithms/stage_companion.py \
  --frozen-context ~/src/adversarial-graph-algorithms/.docker-context \
  --output /tmp/algorithms-current-baseline
docker build --target benchmark -t algorithms-current-baseline:local \
  /tmp/algorithms-current-baseline
```

Follow upstream `benchmarks/algorithms/README.md` for the dedicated Neo4j service,
network, and benchmark container command. Use two CPUs and 4 GiB per service,
algorithm concurrency one, and the historical Neo4j heap/page-cache settings.
Do not run independent measurement jobs concurrently. Retain image validation
receipts, including the 72 upstream checks against the historical C++ participant.

Run the six families and five algorithms at 128 and 1024 nodes, with full-path
Dijkstra enabled. Confirm all vectors, partitions, PageRank checks, and path
aggregates before starting performance experiments. Keep reference binary/source
identities fixed across optimization trials.

### 2. Make upstream participation a supported repository workflow

Add an explicit upstream-source option to the preparation/runner workflow, with
an isolated context and image identity. The historical reproduction command must
continue using the frozen snapshot. Provide one documented command that stages,
builds, validates, and runs current Grust without being overwritten by `run.sh`.

Reuse the upstream provider assertions, raw process audit, and report columns.
Record upstream source commit plus dirty diff/source hashes, compiler, allocator,
release profile, architecture, image digest, dataset hashes, and resource limits.
Avoid a misleading `crate_version` if introducing a separate driver package.
Preserve failures even if validation or report generation aborts. Refuse result
label collisions or use unique run directories so retries cannot overwrite evidence.

Test both preparation modes and the handoff between staging, Compose, and runner.
Assert a requested upstream run actually invokes `grust.algorithms`, not Grustcat.

### 3. Measure build and allocator changes independently

Compare current release defaults against thin LTO and fewer codegen units, then
system allocator against an explicitly selected mimalloc global allocator.
Use build-time allocator selection unless a runtime mechanism is truly implemented;
do not expose a `--mimalloc` argument that merely changes a label.

Hold source, data, limits, workload, and compiler constant for each comparison.
Include end-to-end and loading/projection effects, not only kernel milliseconds.
Portable build flags should remain the default. If testing native CPU tuning,
record the target features and qualify results as host-specific.

### 4. Profile and optimize measured hot paths

Profile representative paths, high-degree hubs, layered graphs, and sparse random
graphs. Investigate allocation count, property/ID conversion, projection copies,
resource-accounting overhead, buffer reversal, query row materialization, and
aggregation. Prioritize changes that improve multiple graph families.

Library-level changes belong in Grust, not duplicated benchmark kernels. Preserve
bounded memory, cancellation/deadline responsiveness, exact work-budget behavior,
and cursor cleanup on failure. Batching accounting requires explicit tests for
exhausted budgets, early visitor termination, cancellation, and partial batches.
Do not assume unlimited-budget benchmark settings justify removing safety checks.

Full paths must still be constructed and every requested node/cost consumed.
No closed-form sums, omitted arrays, graph-family special cases, or changed timer
boundaries may substitute for the requested work. Reuse projections or prepared
plans only in explicitly separate execution classes that disclose their setup cost.

### 5. Qualify final changes on grust

Run affected Rust tests and the complete small Docker correctness suite. Include
ties, zero-cost cycles, disconnected nodes, parallel edges, arbitrary IDs, invalid
weights, resource exhaustion, cancellation, and cursor early drop as appropriate.

Measure baseline and optimized binaries on this same host using warmups and at
least five measured samples for practical-sized cases. Alternate run order, retain
every sample, and report median and dispersion. Use 128/1024 for validation and
larger representative sizes for profiling and stable timing.

Run weighted 16384- and 65536-node full paths as completion/resource tests after
smaller cases pass. The large chain has 2,147,516,416 entries in each path array.
A single large-case sample establishes completion, not stable performance ranking.
Historical native full-path/GDS queries have no timeout; upstream Cypher discloses
a 24-hour policy ceiling. Preserve and report these distinctions.

Keep kernel/query, projection, serialization, verification, process wall, and peak
memory measurements separately labeled. Do not present whole-container peak RSS
as a per-participant measurement. Do not pool timings from quegee and grust.

## Deliverables and completion criteria

- A supported, tested current-Grust runner alongside historical reproduction.
- Measured allocator/build choices and any justified upstream optimizations.
- Exact correctness for admitted workloads, with all failures retained distinctly.
- Reproducible baseline/optimized receipts and a report stating phase boundaries,
  dispersion, regressions, and limitations; no predetermined winner.
- Focused commits and documentation in the appropriate repositories, following
  applicable Grust release instructions if library changes trigger them.

Suggested continuation prompt: “Read docs/optimization-grust-box-handoff.md and
complete the algorithms optimization on this host. Start with the pinned current
Grust baseline and existing upstream participant integration. Preserve historical
participants and full-path work, profile before modifying kernels, and retain
correctness and repeated timing evidence. Avoid the strain benchmark on quegee.”
