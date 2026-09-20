#!/usr/bin/env python3
"""Generate the fixture graphs every participant reads, byte-identically.

One file per graph, ASCII, `source target` per line with zero-based ids, sorted
by source then target, preceded by a header line `nodes edges`. Every
participant parses the same bytes: a fixture built per participant would measure
the generator.
"""
import argparse, pathlib, random

def path_graph(n):
    return [(i, i+1) for i in range(n-1)]

def hub_graph(n, rng, spokes=8):
    # A few hubs of very high degree, the rest attached to one of them.
    hubs = max(1, n // 1024)
    edges = {(h, (h+1) % hubs) for h in range(hubs)} if hubs > 1 else set()
    for node in range(hubs, n):
        edges.add((rng.randrange(hubs), node))
        for _ in range(spokes - 1):
            other = rng.randrange(n)
            if other != node: edges.add((node, other))
    return sorted(edges)

def layered_graph(n, rng, width=64):
    edges = set()
    layers = [list(range(start, min(start+width, n))) for start in range(0, n, width)]
    for lower, upper in zip(layers, layers[1:]):
        for node in lower:
            for _ in range(2):
                edges.add((node, rng.choice(upper)))
    return sorted(edges)

def uniform_graph(n, rng, degree=8):
    edges = set()
    for node in range(n):
        for _ in range(degree):
            other = rng.randrange(n)
            if other != node: edges.add((node, other))
    return sorted(edges)

FAMILIES = {'path': lambda n, rng: path_graph(n), 'hub': hub_graph,
            'layered': layered_graph, 'uniform': uniform_graph}

def write(path, nodes, edges):
    with path.open('w') as out:
        out.write(f'{nodes} {len(edges)}\n')
        for source, target in edges: out.write(f'{source} {target}\n')

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=pathlib.Path, required=True)
    p.add_argument('--sizes', type=int, nargs='+', default=[4096])
    p.add_argument('--families', nargs='+', default=sorted(FAMILIES))
    p.add_argument('--seed', type=int, default=20260920)
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    for family in a.families:
        for size in a.sizes:
            # Seeded per fixture so a size added later does not move the others.
            rng = random.Random(f'{a.seed}-{family}-{size}')
            edges = FAMILIES[family](size, rng)
            target = a.output/f'{family}-{size}.edges'
            write(target, size, edges)
            print(f'{target} {size} nodes {len(edges)} edges')

if __name__ == '__main__': main()
