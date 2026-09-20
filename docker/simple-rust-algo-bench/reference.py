#!/usr/bin/env python3
"""The parity reference: slow, obvious, and borrowed from no participant.

A participant that agrees with another participant has demonstrated nothing; the
reference therefore implements each algorithm independently, in the most direct
form, and is never timed. Semantics follow the main harness: PageRank teleports
and redistributes dangling mass, components are weak, BFS distances are hop
counts, triangles are counted once each on the undirected view.
"""
import argparse, json, pathlib
from collections import deque

def read(path):
    with path.open() as handle:
        nodes, count = (int(part) for part in handle.readline().split())
        edges = [tuple(int(part) for part in line.split()) for line in handle if line.strip()]
    assert len(edges) == count, f'{path}: header says {count} edges, file has {len(edges)}'
    return nodes, edges

def pagerank(nodes, edges, damping=0.85, tolerance=1e-8, max_iterations=100):
    out = [[] for _ in range(nodes)]
    degree = [0]*nodes
    for source, target in edges:
        out[source].append(target)
        degree[source] += 1
    scores = [1.0/nodes]*nodes
    for iteration in range(1, max_iterations+1):
        dangling = sum(scores[node] for node in range(nodes) if degree[node] == 0)
        nxt = [(1.0-damping)/nodes + damping*dangling/nodes]*nodes
        for source in range(nodes):
            if not degree[source]: continue
            share = damping*scores[source]/degree[source]
            for target in out[source]: nxt[target] += share
        delta = sum(abs(a-b) for a, b in zip(nxt, scores))
        scores = nxt
        if delta < tolerance: break
    return scores, iteration

def components(nodes, edges):
    parent = list(range(nodes))
    def find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node
    for source, target in edges:
        a, b = find(source), find(target)
        if a != b: parent[max(a, b)] = min(a, b)
    labels = [find(node) for node in range(nodes)]
    return labels, len(set(labels))

def bfs(nodes, edges, source=0):
    out = [[] for _ in range(nodes)]
    for a, b in edges: out[a].append(b)
    distance = [-1]*nodes
    distance[source] = 0
    queue = deque([source])
    while queue:
        node = queue.popleft()
        for other in out[node]:
            if distance[other] < 0:
                distance[other] = distance[node]+1
                queue.append(other)
    reached = sum(1 for d in distance if d >= 0)
    return distance, reached, sum(d for d in distance if d > 0)

def triangles(nodes, edges):
    # Undirected view; each triangle counted once, by ordering its vertices.
    neighbours = [set() for _ in range(nodes)]
    for a, b in edges:
        if a != b:
            neighbours[a].add(b)
            neighbours[b].add(a)
    total = 0
    for a in range(nodes):
        higher = [b for b in neighbours[a] if b > a]
        for b in higher:
            total += sum(1 for c in higher if c > b and c in neighbours[b])
    return total

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('fixture', type=pathlib.Path)
    p.add_argument('--source', type=int, default=0)
    p.add_argument('--probe', type=int, default=0, help='node whose component label is reported')
    p.add_argument('--tolerance', type=float, default=1e-8,
                   help='L1 stopping tolerance; 1e-8 is the only value grustcat can express')
    p.add_argument('--max-iterations', type=int, default=100)
    a = p.parse_args()
    nodes, edges = read(a.fixture)
    scores, iterations = pagerank(nodes, edges, tolerance=a.tolerance, max_iterations=a.max_iterations)
    labels, count = components(nodes, edges)
    distance, reached, total = bfs(nodes, edges, a.source)
    print(json.dumps(dict(
        fixture=a.fixture.name, nodes=nodes, edges=len(edges),
        pagerank=dict(iterations=iterations, sum=sum(scores), max=max(scores),
                      argmax=scores.index(max(scores)), scores=scores),
        wcc=dict(count=count, probe=a.probe, probe_label=labels[a.probe], labels=labels),
        bfs=dict(source=a.source, reached=reached, distance_sum=total, distances=distance),
        triangles=triangles(nodes, edges)), indent=1))

if __name__ == '__main__': main()
