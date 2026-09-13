"""Run unmodified official GDS procedures over identical synthetic edge files."""

import argparse
import hashlib
import json
import logging
import math
import os
import platform
from pathlib import Path
import statistics
import sys
import time
from neo4j import GraphDatabase, Query
from neo4j.exceptions import Neo4jError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import bench

logging.getLogger("neo4j.notifications").setLevel(logging.ERROR)


def canonical(rows, n):
    labels = [None] * n
    minima = {}
    for r in rows:
        u, label = r["nodeId"], r["componentId"]
        labels[u] = label
        minima[label] = min(minima.get(label, n), u)
    return [minima[x] for x in labels]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sizes", nargs="+", type=int, default=[16384, 65536])
    parser.add_argument(
        "--families",
        nargs="+",
        default=["path", "hub", "clusters", "layered", "uniform", "rmat"],
    )
    parser.add_argument("--warmups", type=int, default=10)
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--label", default="neo4j-official")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--include-grustcat", action="store_true")
    parser.add_argument("--include-grustcat-cypher", action="store_true")
    parser.add_argument("--uri", default=os.environ.get("NEO4J_URI", "bolt://127.0.0.1:17687"))
    parser.add_argument("--algorithms", nargs="+", choices=["bfs", "dijkstra", "wcc", "scc", "pagerank"], default=["bfs", "dijkstra", "wcc", "scc", "pagerank"])
    parser.add_argument("--full-path", action="store_true", help="Equivalent full-path Dijkstra output, with no transaction or process timeout")
    args = parser.parse_args()
    if (
        args.repeats < 1
        or args.warmups < 0
        or any(n < 128 or n & (n - 1) for n in args.sizes)
    ):
        parser.error(
            "positive repeats, nonnegative warmups, and power-of-two sizes >=128 required"
        )
    if not args.label or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in args.label):
        parser.error("label must contain only letters, digits, hyphens and underscores")
    result_dir = Path(os.environ.get("BENCH_RESULTS_DIR", ROOT / "results"))
    data_dir = Path(os.environ.get("BENCH_DATA_DIR", ROOT / "data"))
    result_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    output = result_dir / f"{args.label}.json"
    native_executables = {"cpp": "legacy", "rust": "rust-bench"}
    if args.include_grustcat:
        native_executables["grustcat"] = "grustcat"
    if args.include_grustcat_cypher:
        native_executables["grustcat_cypher"] = "grustcat-cypher"
    results = []
    prior_metadata = None
    if args.resume and output.exists():
        prior_metadata = json.loads(output.read_text())["metadata"]
        results = [
            r
            for r in json.loads(output.read_text())["results"]
            if r["algorithm"] != "pagerank"
            or r["configuration"].get("tolerance") == 1e-10
        ]
    completed = {(r["family"], r["n"], r["algorithm"]) for r in results}
    with GraphDatabase.driver(args.uri, auth=None) as driver:
        with driver.session(database="neo4j") as session:

            def query(text, **params):
                return session.run(Query(text, timeout=0 if args.full_path else 180), **params).data()

            metadata = {
                "gds": query("RETURN gds.version() AS version")[0]["version"],
                "database": query(
                    "CALL dbms.components() YIELD versions,edition RETURN versions,edition"
                ),
                "warmups": args.warmups,
                "repeats": args.repeats,
                "concurrency": 1,
                "dijkstra_mode": "full-path" if args.full_path else "distance-only-native",
                "java": (ROOT / "neo4j/java-version.txt").read_text().strip()
                if (ROOT / "neo4j/java-version.txt").exists() else "OpenJDK 21.0.12 ARM64 (local setup)",
                "runner_platform": platform.platform(),
                "native_engines": {"cpp": "Icebug", "rust": "Icecat", "grustcat": "Grustcat", "grustcat_cypher": "Grustcat Cypher"},
                "heap": os.environ.get("BENCH_NEO4J_HEAP", "4G"),
                "user_log_level": "WARN",
                "server_log_level": "WARN",
                "page_cache": os.environ.get("BENCH_NEO4J_PAGE_CACHE", "1G"),
                "jar_sha256": hashlib.sha256(
                    (ROOT / "neo4j/gds.jar").read_bytes()
                ).hexdigest(),
                "native_binary_sha256": {
                    x: hashlib.sha256((ROOT / x).read_bytes()).hexdigest()
                    for x in native_executables.values()
                },
            }
            if prior_metadata is not None:
                for key in [
                    "gds",
                    "jar_sha256",
                    "native_binary_sha256",
                    "concurrency", "dijkstra_mode",
                    "warmups",
                    "repeats",
                    "user_log_level",
                    "server_log_level", "java", "heap", "page_cache", "runner_platform",
                ]:
                    if prior_metadata.get(key) != metadata.get(key):
                        raise RuntimeError(
                            f"resume metadata mismatch for {key}; use a new label"
                        )
            for n in args.sizes:
                for family in args.families:
                    if all(
                        (family, n, alg) in completed
                        for alg in args.algorithms
                    ):
                        continue
                    path = data_dir / f"{family}-{n}.txt"
                    if not path.exists():
                        edges = bench.generate(family, n)
                        path.write_text(
                            f"{n} {len(edges)}\n"
                            + "".join(f"{u} {v} {w}\n" for u, v, w in edges)
                        )
                    with path.open() as f:
                        nn, m = map(int, next(f).split())
                        edges = [list(map(int, line.split())) for line in f]
                    assert nn == n and len(edges) == m
                    name = f"agbench_{family}_{n}"
                    query("CALL gds.graph.drop($name,false)", name=name)
                    projection = query(
                        "CALL gds.graph.project.cypher($name, 'UNWIND range(0, $n - 1) AS id RETURN id', \"UNWIND $edges AS e RETURN e[0] AS source,e[1] AS target,toFloat(e[2]) AS weight,'EDGE' AS type\", {parameters:{n:$n,edges:$edges},readConcurrency:1}) YIELD nodeCount,relationshipCount,projectMillis RETURN *",
                        name=name,
                        n=n,
                        edges=edges,
                    )[0]
                    assert (
                        projection["nodeCount"] == n
                        and projection["relationshipCount"] == m
                    )
                    print("projected", family, n, m, flush=True)
                    del edges
                    try:
                        for alg in args.algorithms:
                            if (family, n, alg) in completed:
                                continue
                            native = {x: [] for x in native_executables}
                            expected = None
                            native_iterations = {}
                            native_queries = {}
                            path_summaries = {x: [] for x in native_executables}
                            for repeat in range(args.repeats + args.warmups):
                                values = {}
                                engines = list(native_executables.items())
                                offset = repeat % len(engines)
                                for backend, exe in engines[offset:] + engines[:offset]:
                                    metrics, v = bench.execute(
                                        ROOT / exe,
                                        path,
                                        "dijkstra-full" if args.full_path and alg == "dijkstra" else alg,
                                        0,
                                        result_dir / f"neo4j-{backend}.bin",
                                    )
                                    if repeat >= args.warmups:
                                        native[backend].append(metrics["ms"])
                                    if args.full_path and alg == "dijkstra":
                                        path_summaries[backend].append({k: metrics[k] for k in ["reachable", "path_entries", "node_sum", "cost_sum"]})
                                    if "query" in metrics:
                                        native_queries[backend] = metrics["query"]
                                    values[backend] = v
                                    native_iterations[backend] = metrics["iterations"]
                                for backend, actual in values.items():
                                    assert len(actual) == n and all(math.isfinite(x) for x in actual)
                                    if alg == "pagerank":
                                        assert max(abs(x-y) for x,y in zip(values["cpp"],actual)) <= 1e-9
                                        assert abs(sum(actual)-1.) <= 1e-8
                                        assert native_iterations[backend] == native_iterations["cpp"]
                                    else:
                                        assert values["cpp"] == actual
                                expected = values["rust"]
                            config = {
                                "concurrency": 1,
                                "logProgress": False,
                                "relationshipTypes": ["EDGE"],
                            }
                            if alg in ["bfs", "dijkstra"]:
                                config["sourceNode"] = 0
                            if alg in ["dijkstra", "pagerank"]:
                                config["relationshipWeightProperty"] = "weight"
                            if alg == "pagerank":
                                config.update(
                                    dampingFactor=0.85,
                                    tolerance=1e-10,
                                    maxIterations=1000,
                                )
                            proc = {
                                "bfs": "gds.bfs.stats",
                                "dijkstra": "gds.allShortestPaths.dijkstra.stream",
                                "wcc": "gds.wcc.stats",
                                "scc": "gds.scc.stats",
                                "pagerank": "gds.pageRank.stats",
                            }[alg]
                            if not args.full_path and alg == "dijkstra" and family == "path" and n >= 65536:
                                start = time.perf_counter()
                                try:
                                    session.run(
                                        Query(
                                            f"CALL {proc}($name,$config) YIELD totalCost RETURN count(*) AS reachable,sum(totalCost) AS distance_sum",
                                            timeout=30,
                                        ),
                                        name=name,
                                        config=config,
                                    ).consume()
                                    status = "completed_bounded_probe"
                                except Neo4jError as error:
                                    if (
                                        "Terminated" not in error.code
                                        and "TimedOut" not in error.code
                                    ):
                                        raise
                                    status = "transaction_timeout"
                                row = {
                                    "family": family,
                                    "n": n,
                                    "edges": m,
                                    "algorithm": alg,
                                    "graph_sha256": hashlib.sha256(
                                        path.read_bytes()
                                    ).hexdigest(),
                                    "configuration": config,
                                    "procedure": proc,
                                    "native_ms": native,
                                    "status": status,
                                    "deadline_seconds": 30,
                                    "probe_wall_seconds": time.perf_counter() - start,
                                    "samples": [],
                                    "validation": {"gds_full_output_validated": False},
                                    "timing_kind": "bounded_server_query",
                                }
                                results.append(row)
                                output.write_text(
                                    json.dumps(
                                        {"metadata": metadata, "results": results},
                                        indent=2,
                                    )
                                )
                                print(
                                    f"{family} {n} {alg}: {status} after {row['probe_wall_seconds']:.1f}s",
                                    flush=True,
                                )
                                continue
                            full_query = (
                                f"CALL {proc}($name,$config) YIELD targetNode,totalCost,nodeIds,costs "
                                "RETURN count(*) AS reachable,sum(totalCost) AS distance_sum,"
                                "sum(size(nodeIds)) AS path_entries,"
                                "sum(reduce(s=0,x IN nodeIds | s+x)) AS node_sum,"
                                "sum(reduce(s=0.0,x IN costs | s+x)) AS cost_sum,"
                                "collect([targetNode,totalCost]) AS distances"
                            )
                            samples = []
                            warmups = []
                            case_warmups = (
                                min(args.warmups, 2)
                                if alg == "dijkstra" and family == "path"
                                else args.warmups
                            )
                            for repeat in range(case_warmups + args.repeats):
                                start = time.perf_counter()
                                if alg == "dijkstra":
                                    result = session.run(
                                        Query(
                                            full_query if args.full_path else f"CALL {proc}($name,$config) YIELD totalCost RETURN count(*) AS reachable,sum(totalCost) AS distance_sum",
                                            timeout=0 if args.full_path else 180,
                                        ),
                                        name=name,
                                        config=config,
                                    )
                                    metrics = result.data()[0]
                                    summary = result.consume()
                                    if args.full_path:
                                        actual = [-1.] * n
                                        for target, cost in metrics.pop("distances"):
                                            actual[int(target)] = cost
                                        assert actual == list(expected)
                                        assert metrics["reachable"] == sum(x >= 0 for x in expected)
                                        if family == "path":
                                            wanted = {
                                                "reachable": n,
                                                "path_entries": n * (n + 1) // 2,
                                                "node_sum": sum(u * (n-u) for u in range(n)),
                                                "cost_sum": sum(d * (n-u) for u,d in enumerate(expected)),
                                            }
                                            for candidate in [metrics] + [v for values in path_summaries.values() for v in values]:
                                                assert all(candidate[k] == v for k,v in wanted.items()), (candidate, wanted)
                                    metrics["server_query_ms"] = (
                                        summary.result_available_after or 0
                                    ) + (summary.result_consumed_after or 0)
                                else:
                                    metrics = query(
                                        f"CALL {proc}($name,$config)",
                                        name=name,
                                        config=config,
                                    )[0]
                                metrics["client_wall_ms"] = (
                                    time.perf_counter() - start
                                ) * 1000
                                (warmups if repeat < case_warmups else samples).append(
                                    metrics
                                )
                            validation = {}
                            if alg == "bfs":
                                ids = query(
                                    "CALL gds.bfs.stream($name,$config) YIELD nodeIds RETURN nodeIds",
                                    name=name,
                                    config=config,
                                )[0]["nodeIds"]
                                reachable = {
                                    u for u, v in enumerate(expected) if v >= 0
                                }
                                assert (
                                    len(ids) == len(set(ids)) and set(ids) == reachable
                                )
                                assert all(
                                    expected[a] <= expected[b]
                                    for a, b in zip(ids, ids[1:])
                                )
                                validation = {
                                    "reachable_nodes": len(ids),
                                    "reachability_and_level_order_match": True,
                                }
                            elif alg == "dijkstra" and args.full_path:
                                validation = {"all_distances_match": True,
                                    "path_aggregates_match_unique_path_oracle": family == "path"}
                                # Validate every node and cumulative cost on small fixtures.
                                # Large unique paths use independently calculated exact aggregates.
                                if n <= 1024:
                                    edge_weights = {}
                                    with path.open() as f:
                                        next(f)
                                        for line in f:
                                            u,v,w = map(int,line.split())
                                            edge_weights[u,v] = w
                                    seen = set()
                                    for row in session.run(Query(
                                        f"CALL {proc}($name,$config) YIELD targetNode,totalCost,nodeIds,costs RETURN *", timeout=0), name=name, config=config):
                                        target, nodes, costs = row["targetNode"], row["nodeIds"], row["costs"]
                                        assert target not in seen
                                        seen.add(target)
                                        assert nodes[0] == 0 and nodes[-1] == target
                                        assert len(nodes) == len(costs) and costs[0] == 0 and costs[-1] == expected[target]
                                        for u,v,a,b in zip(nodes,nodes[1:],costs,costs[1:]):
                                            assert a + edge_weights[u,v] == b
                                    assert seen == {u for u,d in enumerate(expected) if d >= 0}
                                    validation["every_gds_path_edge_and_cost_validated"] = True
                            elif alg == "dijkstra":
                                rows = query(
                                    f"CALL {proc}($name,$config) YIELD targetNode,totalCost RETURN targetNode,totalCost",
                                    name=name,
                                    config=config,
                                )
                                actual = [-1.0] * n
                                for r in rows:
                                    actual[r["targetNode"]] = r["totalCost"]
                                assert actual == list(expected)
                                validation = {"all_distances_match": True}
                            elif alg in ["wcc", "scc"]:
                                rows = query(
                                    f"CALL gds.{alg}.stream($name,$config) YIELD nodeId,componentId RETURN nodeId,componentId",
                                    name=name,
                                    config=config,
                                )
                                assert canonical(rows, n) == list(expected)
                                validation = {"canonical_partition_matches": True}
                            else:
                                rows = query(
                                    "CALL gds.pageRank.stream($name,$config) YIELD nodeId,score RETURN nodeId,score",
                                    name=name,
                                    config=config,
                                )
                                actual = [0.0] * n
                                for r in rows:
                                    actual[r["nodeId"]] = r["score"]
                                mass = sum(actual)
                                actual = [v / mass for v in actual]
                                error = max(
                                    abs(x - y) for x, y in zip(actual, expected)
                                )
                                l1 = sum(abs(x - y) for x, y in zip(actual, expected))
                                assert all(math.isfinite(v) and v >= 0 for v in actual)
                                assert error <= 1e-8 and l1 <= 1e-7, (
                                    family,
                                    n,
                                    error,
                                    l1,
                                )
                                assert all(s["didConverge"] for s in samples)
                                validation = {
                                    "raw_gds_score_sum": mass,
                                    "normalization": "divide by raw sum",
                                    "max_absolute_error": error,
                                    "l1_error": l1,
                                }
                            row = {
                                "family": family,
                                "n": n,
                                "edges": m,
                                "algorithm": alg,
                                "graph_sha256": hashlib.sha256(
                                    path.read_bytes()
                                ).hexdigest(),
                                "projection": projection,
                                "configuration": config,
                                "procedure": proc,
                                "timing_kind": "server_query"
                                if alg == "dijkstra"
                                else "reported_compute",
                                "native_ms": native,
                                "native_iterations": native_iterations,
                                "native_queries": native_queries,
                                "native_path_summaries": path_summaries if args.full_path and alg == "dijkstra" else {},
                                "warmups": warmups,
                                "samples": samples,
                                "validation": validation,
                            }
                            results.append(row)
                            output.write_text(
                                json.dumps(
                                    {"metadata": metadata, "results": results}, indent=2
                                )
                            )
                            print(
                                f"{family:9} {n:7} {alg:9} GDS={statistics.median(s.get('computeMillis', s.get('server_query_ms')) for s in samples):7.1f} ms Rust={statistics.median(native['rust']):8.3f} C++={statistics.median(native['cpp']):8.3f}",
                                flush=True,
                            )
                    finally:
                        query("CALL gds.graph.drop($name,false)", name=name)


if __name__ == "__main__":
    main()
