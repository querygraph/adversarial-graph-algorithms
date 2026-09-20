# Adversarial graph algorithms

Five execution variants over identical generated directed weighted graphs: Icebug (C++/Arrow NetworKit update), Icecat (Rust/Arrow rewrite), Grustcat (Grust/Arrow), Grustcat Cypher (Grust parser and typed Arrow backend), and official Neo4j GDS.

Published benchmark: **https://adversari.al/graph/algorithms**. The [graph index](https://adversari.al/graph) also links the separate graph-query and strain benchmarks.

## Reproduce the published full-path run

```sh
git clone https://github.com/querygraph/adversarial-graph-algorithms
cd adversarial-graph-algorithms
./docker/run.sh --frozen --full-path --algorithms dijkstra --families path \
  --sizes 16384 65536 --warmups 0 --repeats 1 --label reproduced-full-path
```

`--frozen` selects the published measured snapshot. Without it, `run.sh` measures
current upstream Grust and Turso with Arrow, DataFusion and mimalloc; see below.

Requires Docker Compose v2 and Python 3.12+ (safe tar extraction). `docker/prepare.py` defaults to the checksum-verified measured source snapshot in `publication/`; no sibling repositories are required. Official Neo4j/GDS archives are downloaded and checksum-verified separately. For local development, `python3 docker/prepare.py --local` stages `../icecat` and `../grust`; then invoke Compose directly. The snapshot includes the exact staged build inputs, while transitive OS packages/base-image tags are not immutable. Separate dependency licenses are under `publication/licenses/`; bundled sources retain their own notices.

The 65,536-node chain produces 2,147,516,416 entries in each path array per engine. Neo4j has no transaction deadline in full-path mode. One measured run and no warmup demonstrate completion and correctness; they do not establish stable performance rankings. GDS includes server-side Cypher overhead. Grustcat Cypher includes parsing, semantic analysis, planning, typed Arrow execution and aggregation; it is not the general Grust reference executor.

[Protocol and resource limits](docker/README.md) · [raw evidence and checksums](publication/evidence/) · [source snapshot receipt](publication/source.json).

All five variants also passed 30 small cases (six families × five algorithms); the runtime image passes 45 kernel/Arrow interchange checks. BFS and PageRank have documented cross-engine output/convergence differences. Graph loading and projection are outside kernel/query timers. No published query-suite result is pooled with these measurements.

## Grust implementation handoff

[Generalized graph algorithms in Grust](docs/grust-generalized-graph-algorithms-handoff.md) describes the proposed upstream architecture, Arrow and Cypher contracts, phased acceptance gates, and benchmark validation. It includes committed source references and clone commands for an implementation agent on another machine.

## Current sources are the default

`./docker/run.sh` with no source flags measures current upstream Grust and Turso:
the historical four participants plus upstream direct and Cypher, both Turso
snapshot columns, Arrow and DataFusion, built with the mimalloc global allocator.
Checkouts come from `docker/upstream-pins.json`; a missing checkout is cloned at
its pinned commit, and a checkout sitting at any other commit is refused rather
than silently measured. Pass `--upstream-grust` or `--turso` to measure a
different source on purpose, which is recorded as unpinned in the run receipt.

The [current Grust/Turso workflow](docker/README.md#current-grust-and-turso-main)
adds upstream direct/Cypher execution, Arrow/DataFusion preparation, and
Turso-backed snapshot participants, with process-wide mimalloc by default and
explicit allocator and release-profile controls. Turso main is pinned by
commit for each experiment. The historical reproduction command above continues
to use the published frozen sources. Group commit is measured in a separate
concurrent-write preparation workload, outside algorithm timers.

[Related work](docs/related-work.md) places these participants against the
best-known Rust graph algorithm library and states what has not been measured.

[The current-source report](docs/optimization-results.md) carries the measured
results, boundaries, regressions and evidence, kept separate from the historical
publication. The [write-up](docs/blog/graph-algorithms-full-paths/post.md) covers the output
contract and what measuring it on current sources found.
