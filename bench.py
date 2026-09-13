"""Deterministic paired algorithm comparison; complete vector validation before timing reports."""

import argparse, array, hashlib, json, math, os, platform, random, statistics, subprocess, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def generate(family, n):
    rng = random.Random(20260913)
    edges = set()
    if family == "path":
        edges.update((u, u + 1) for u in range(n - 1))
    elif family == "hub":
        edges.update((0, u) for u in range(1, n))
        edges.update((u, 0) for u in range(1, n) if u % 11)
    elif family == "clusters":
        edges.update(
            (u, (u // 64) * 64 + (u + 1) % 64) for u in range(n) if u % 64 < 60
        )
        edges.update(
            (u, (u // 64) * 64 + (u + 7) % 60) for u in range(n) if u % 64 < 60
        )
    elif family == "layered":
        edges.update((u, u + v) for u in range(n) for v in (1, 17, 127) if u + v < n)
    elif family == "uniform":
        edges.update((rng.randrange(n), rng.randrange(n)) for _ in range(8 * n))
    elif family == "rmat":
        scale = n.bit_length() - 1
        for _ in range(8 * n):
            u = v = 0
            for b in range(scale - 1, -1, -1):
                r = rng.random()
                if r >= 0.76:
                    u |= 1 << b
                if 0.57 <= r < 0.76 or r >= 0.95:
                    v |= 1 << b
            edges.add((u, v))
    return sorted((u, v, 1 + (u * 17 + v * 13) % 31) for u, v in edges if u != v)


def execute(exe, graph, alg, source, output):
    env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1")
    start = time.monotonic()
    p = subprocess.run(
        [str(exe), str(graph), alg, str(output), str(source)],
        capture_output=True,
        text=True,
        env=env,
        timeout=None if alg == "dijkstra-full" else 180,
        check=True,
    )
    metrics = json.loads(p.stdout)
    metrics["process_seconds"] = time.monotonic() - start
    values = array.array("d")
    values.frombytes(output.read_bytes())
    return metrics, values


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--rust-executable", type=Path, default=ROOT / "rust-bench")
    p.add_argument("--sizes", type=int, nargs="+", default=[16384, 65536])
    p.add_argument("--repeats", type=int, default=5)
    p.add_argument("--label", default="baseline")
    p.add_argument(
        "--families",
        nargs="+",
        default=["path", "hub", "clusters", "layered", "uniform", "rmat"],
    )
    p.add_argument(
        "--algorithms", nargs="+", default=["bfs", "dijkstra", "wcc", "scc", "pagerank"]
    )
    a = p.parse_args()
    (ROOT / "data").mkdir(exist_ok=True)
    results = []
    executables = {"cpp": ROOT / "legacy", "rust": a.rust_executable.resolve()}
    binary_sha256 = {
        name: hashlib.sha256(exe.read_bytes()).hexdigest()
        for name, exe in executables.items()
    }
    for n in a.sizes:
        if n < 128 or n & (n - 1):
            raise ValueError("sizes must be powers of two >=128")
        for family in a.families:
            graph = ROOT / "data" / f"{family}-{n}.txt"
            edges = generate(family, n)
            graph.write_text(
                f"{n} {len(edges)}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in edges)
            )
            digest = hashlib.sha256(graph.read_bytes()).hexdigest()
            for alg in a.algorithms:
                timings = {"cpp": [], "rust": []}
                errors = []
                iterations = {}
                for repeat in range(a.repeats + 1):
                    values = {}
                    for name in ["cpp", "rust"] if repeat % 2 == 0 else ["rust", "cpp"]:
                        m, v = execute(
                            executables[name],
                            graph,
                            alg,
                            0,
                            ROOT / "results" / f"{name}.bin",
                        )
                        values[name] = v
                        if repeat:
                            timings[name].append(m["ms"])
                        iterations[name] = m["iterations"]
                    if len(values["cpp"]) != n or len(values["rust"]) != n:
                        raise AssertionError("wrong result length")
                    error = max(
                        abs(x - y) for x, y in zip(values["cpp"], values["rust"])
                    )
                    errors.append(error)
                    if alg == "pagerank":
                        assert error <= 1e-9, (family, alg, error)
                        for v in values.values():
                            assert abs(sum(v) - 1) < 1e-9 and all(
                                math.isfinite(x) and x >= 0 for x in v
                            )
                        assert iterations["cpp"] == iterations["rust"], iterations
                    else:
                        assert error == 0, (family, alg, error)
                row = dict(
                    family=family,
                    n=n,
                    edges=len(edges),
                    algorithm=alg,
                    source=0,
                    sha256=digest,
                    timings_ms=timings,
                    max_abs_error=max(errors),
                    iterations=iterations,
                )
                row["ratio"] = statistics.median(timings["rust"]) / statistics.median(
                    timings["cpp"]
                )
                results.append(row)
                print(
                    f"{family:10} {n:7} {alg:9} cpp={statistics.median(timings['cpp']):9.3f} rust={statistics.median(timings['rust']):9.3f} ratio={row['ratio']:.2f}",
                    flush=True,
                )
                (ROOT / "results" / f"{a.label}.json").write_text(
                    json.dumps(
                        dict(
                            executable_paths={k: str(v) for k,v in executables.items()},
                            binary_sha256=binary_sha256,
                            platform=platform.platform(),
                            date=time.strftime("%Y-%m-%d"),
                            repeats=a.repeats,
                            warmups=1,
                            results=results,
                        ),
                        indent=2,
                    )
                )


if __name__ == "__main__":
    main()
