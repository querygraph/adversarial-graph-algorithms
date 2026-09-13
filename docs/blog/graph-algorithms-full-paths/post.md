# Graph algorithms, full paths, and the work a benchmark must count

![Prometheus breaks the chains of a graph, scattering sparks between its nodes.](../../../cover/prometheus-breaks-graphs-headboard.png)

The new [graph-algorithm benchmark on adversari.al](https://adversari.al/graph/algorithms) compares five execution variants on identical graphs: Icebug, Icecat, Grustcat, Grustcat Cypher, and official Neo4j Graph Data Science. Its most revealing experiment is a chain of 65,536 nodes. Every implementation computes shortest paths and constructs and consumes the full node sequence and cumulative-cost sequence for every reachable destination. Neo4j is allowed to finish. All five complete, and their distances and independent path aggregates agree.

The important change came before the timing. We had to agree on what the result contained.

## A distance is not a path

A shortest-distance query can return one number for each destination. A full-path query also returns the intermediate nodes and the cost accumulated along that route. Those are different output contracts, even when both operations are called Dijkstra.

A chain makes the difference concrete. The path to the source contains one node. The path to the next node contains two, then three, and so on. Across all destinations, each array contains `n(n + 1) / 2` entries. At 65,536 nodes, that is **2,147,516,416 entries in the node-ID array and the same number in the cumulative-cost array**, for each engine.

An earlier comparison timed distance-only native results against Neo4j’s full-path procedure and bounded the large Neo4j case with a transaction timeout. We retain that [historical evidence](https://adversari.al/evidence/graph-algorithms/2026-09-13/neo4j-official.json) as a separate experiment. It is not the basis of the new full-path table.

The new mode includes predecessor tracking, reconstruction, and consumption of the path arrays. It does not retain every path simultaneously. Native code processes one path at a time; Neo4j streams its procedure output into server-side Cypher aggregation. The full-path mode removes both the native process deadline and the Neo4j transaction deadline.

## Five columns, explicit boundaries

**Icebug** is the original Apache Arrow update of the C++ NetworKit codebase. **Icecat** is the first Rust rewrite. **Grustcat** is the Grust-compatible implementation, with an Arrow projection of the graph. **Grustcat Cypher** adds Grust’s parser and semantic analyzer, followed by a focused typed Arrow execution backend. The final column runs **Neo4j Community 2026.08.0 with official GDS 2026.08.1** and its unmodified single-source Dijkstra procedure.

The completed Docker run produced these times in seconds:

| Variant | 16,384-node chain | 65,536-node chain |
|---|---:|---:|
| Icebug | 1.102 | 22.233 |
| Icecat | 1.053 | 16.648 |
| Grustcat | 1.032 | 16.710 |
| Grustcat Cypher | 1.028 | 16.727 |
| Neo4j GDS | 11.889 | 194.113 |

These are **one-sample completion measurements with no warmup**, taken in Linux ARM64 Docker containers on an Apple M1 Max host. They do not establish stable rankings or isolate the cost of a programming language. Each service has a two-CPU quota and a 4 GiB memory limit; algorithm concurrency is one. Neo4j has a 2 GiB heap and 512 MiB page cache.

Graph loading and projection are outside the reported timers. Native timings include the algorithms, reconstruction, and aggregation; Rust also constructs an Arrow distance result. Grustcat Cypher includes parsing, semantic checks, and planning. Neo4j’s number is server query time, including Cypher aggregation; its client wall time is retained in the raw results. Allocation strategies and internal work remain engine-specific. The requested path output is equivalent, but the execution machinery is not identical.

The [raw results](https://adversari.al/evidence/graph-algorithms/2026-09-13/docker-cypher-full-path.json) include samples, query text, configurations, validation, and binary hashes. The accompanying [environment receipt](https://adversari.al/evidence/graph-algorithms/2026-09-13/docker-cypher-full-path-environment.json) records source hashes, compiler and package versions, and container limits.

## Cypher can preserve the output contract

The Grustcat Cypher variant admits a deliberately small query subset. For full paths, its query has this shape:

```cypher
CALL grustcat.fullPaths($source) YIELD nodeIds, costs
UNWIND range(0, size(nodeIds)-1) AS i
RETURN count(*) AS path_entries,
       sum(nodeIds[i]) AS node_sum,
       sum(costs[i]) AS cost_sum
```

Grust parses and semantically analyzes the query. The backend then validates the whole syntax tree and compiles the admitted operations. It fuses the expansion and aggregates over actual path arrays, avoiding billions of intermediate row objects. Unsupported query forms fail explicitly.

This is not Grust’s general, materializing reference executor, and it does not implement Neo4j’s procedure namespace. We compare its aggregate semantics with the real Grust reference executor on small fixtures. A general graph-algorithm dispatcher would require an extensible procedure registry and bounded batch execution through the surrounding Cypher pipeline. Adding a streaming procedure is insufficient if the next operator collects all its rows.

## Evidence beyond one chain

The five variants also pass 30 small cases: six graph families across BFS, Dijkstra, weak and strong components, and PageRank. The Docker runtime image passes 45 kernel and Arrow interchange checks. The graph families include paths, hubs, clusters, layered graphs, uniform graphs, and R-MAT graphs.

Those checks keep algorithm-specific distinctions visible. BFS compares reachability and level order because the native and GDS result shapes differ. Component partitions are canonicalized. PageRank uses the same weighted uniform model but different convergence rules; normalized scores are checked within recorded tolerances. There is no combined score that hides those differences.

Small Neo4j paths are validated edge by edge. The large chain has unique shortest paths, so we independently calculate and compare every distance, the path-entry count, the node-ID sum, and the cumulative-cost sum. Matching aggregates on an arbitrary tied graph would not, by itself, prove that every interior node was correct.

## A graph index with room for separate experiments

The [Graph tab](https://adversari.al/graph) now opens an index. The extensive [graph-query benchmark](https://adversari.al/graph/queries) is a sibling of the new algorithm benchmark, with its upstream provenance, historical cohorts, and timing corrections preserved. The [strain ledger](https://adversari.al/graph/strain) remains another distinct experiment. Their datasets, protocols, and execution classes are not pooled into one leaderboard.

The [benchmark repository](https://github.com/querygraph/adversarial-graph-algorithms) includes a checksum-verified snapshot of the measured source. Docker can build it without local sibling checkouts. Official Neo4j and GDS archives are downloaded separately and checksum-verified; base-image tags and transitive OS packages are not immutable, so the receipts remain part of the experiment.

```sh
git clone https://github.com/querygraph/adversarial-graph-algorithms
cd adversarial-graph-algorithms
./docker/run.sh --full-path --algorithms dijkstra --families path \
  --sizes 16384 65536 --warmups 0 --repeats 1 --label reproduced-full-path
```

The [Adversarial Cognition book](https://firstpair.org/read/adversarial-cognition/) adds this graph experiment to its discussion of testable boundaries. Here the boundary is the output itself: what must exist, what must be consumed, and what the clock includes. Once that contract is explicit, a completed run becomes evidence a reader can inspect and reproduce.
