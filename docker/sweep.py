#!/usr/bin/env python3
"""Within one limited container, alternate pinned binaries and retain every sample."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import statistics
import sys
import traceback

sys.path.insert(0, '/opt/benchmark')
import bench
import participant_audit

PARTICIPANTS = ['grust-upstream-direct', 'grust-upstream-cypher', 'turso-direct', 'turso-cypher', 'grust-arrow', 'grust-datafusion']


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--variants', nargs='+', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--sizes', nargs='+', type=int, default=[4096])
    p.add_argument('--families', nargs='+', choices=['path', 'hub', 'clusters', 'layered', 'uniform', 'rmat'], default=['path', 'hub', 'layered', 'uniform'])
    p.add_argument('--algorithms', nargs='+', choices=['bfs', 'dijkstra', 'dijkstra-full', 'wcc', 'scc', 'pagerank'], default=['dijkstra-full', 'pagerank'])
    p.add_argument('--participants', nargs='+', choices=PARTICIPANTS, default=PARTICIPANTS)
    p.add_argument('--warmups', type=int, default=1)
    p.add_argument('--repeats', type=int, default=5)
    p.add_argument('--group-commit', action='store_true', help='Alternate MVCC off/engine/client statement loading')
    a = p.parse_args()
    if a.repeats < 1 or a.warmups < 0 or any(n < 128 or n & (n-1) for n in a.sizes): p.error('invalid sample count or graph size')
    if a.group_commit and any(not name.startswith('turso-') for name in a.participants):
        p.error('--group-commit requires --participants turso-direct and/or turso-cypher')
    a.output.mkdir(parents=True, exist_ok=False)
    os.environ.update(BENCH_RESULTS_DIR=str(a.output), BENCH_AUDIT_LABEL='sweep')
    execute = participant_audit.capture(bench.execute)
    metadata = dict(argv=sys.argv, platform=platform.platform(), environment={k:v for k,v in os.environ.items() if k.startswith('BENCH_')}, variants={})
    for path in ['/sys/fs/cgroup/cpu.max', '/sys/fs/cgroup/memory.max', '/proc/cpuinfo', '/proc/loadavg', '/proc/stat']:
        metadata[path] = Path(path).read_text()
    for variant in a.variants:
        metadata['variants'][str(variant)] = dict(receipt=json.loads((variant/'build-receipt.json').read_text()),
            binaries={name:hashlib.sha256((variant/name).read_bytes()).hexdigest() for name in a.participants})
    (a.output/'metadata.json').write_text(json.dumps(metadata, indent=2)+'\n')
    configurations = [(v, 'default') for v in a.variants]
    if a.group_commit:
        configurations = [(v, group) for v in a.variants for group in ['off', 'engine', 'client']]
    failures = 0
    rows = []
    with (a.output/'samples.jsonl').open('x') as samples:
        for n in a.sizes:
            for family in a.families:
                edges = bench.generate(family, n)
                graph = a.output/f'{family}-{n}.txt'
                graph.write_text(f'{n} {len(edges)}\n'+''.join(f'{u} {v} {w}\n' for u,v,w in edges))
                for algorithm in a.algorithms:
                    reference_metrics, expected = execute(Path('/opt/benchmark/legacy'), graph, algorithm, 0, a.output/'reference.bin')
                    case = dict(family=family, n=n, algorithm=algorithm, graph_sha256=hashlib.sha256(graph.read_bytes()).hexdigest(), samples=[])
                    for repeat in range(a.warmups+a.repeats):
                        order = configurations if repeat % 2 == 0 else list(reversed(configurations))
                        for variant, group in order:
                            for participant in a.participants:
                                row = dict(variant=variant.name, group_commit=group, participant=participant, repeat=repeat,
                                           warmup=repeat < a.warmups, family=family, n=n, algorithm=algorithm)
                                if a.group_commit:
                                    os.environ.update(BENCH_TURSO_JOURNAL='mvcc', BENCH_TURSO_LOAD='statements', BENCH_TURSO_WRITERS='4', BENCH_TURSO_GROUP_COMMIT=group)
                                try:
                                    metrics, values = execute(variant/participant, graph, algorithm, 0, a.output/'actual.bin')
                                    row['metrics'] = metrics
                                    assert metrics['provider'] == 'grust.algorithms'
                                    assert metrics['participant'] == participant.replace('-', '_')
                                    assert metrics['allocator'] == metadata['variants'][str(variant)]['receipt']['allocator']
                                    if a.group_commit:
                                        backend = metrics['backend_details']
                                        for field, wanted in dict(journal='mvcc', synchronous='FULL', group_commit=group,
                                                                  load_mode='statements', writers=4, snapshot_verified=True).items():
                                            assert backend[field] == wanted, (field, backend[field], wanted)
                                    assert len(values) == n and all(math.isfinite(x) for x in values)
                                    if algorithm == 'pagerank':
                                        assert max(abs(x-y) for x,y in zip(values,expected)) <= 1e-9
                                        assert abs(sum(values)-1) <= 1e-8
                                    else: assert values == expected
                                    if algorithm == 'dijkstra-full' and family == 'path':
                                        for key in ['reachable', 'path_entries', 'node_sum', 'cost_sum']:
                                            assert metrics[key] == reference_metrics[key], key
                                    row['status'] = 'pass'
                                except Exception as error:
                                    row.update(status='mismatch' if isinstance(error, AssertionError) else 'error', error=traceback.format_exc())
                                    failures += 1
                                samples.write(json.dumps(row)+'\n'); samples.flush()
                                case['samples'].append(row)
                    rows.append(case)
                    (a.output/'results.json').write_text(json.dumps(dict(metadata=metadata, failures=failures, results=rows), indent=2)+'\n')
                    print(f'{family} {n} {algorithm}: {len(case["samples"])} samples, {failures} failures', flush=True)
    terminal = dict(status='pass' if not failures else 'failed', failures=failures)
    for name in ['/proc/loadavg', '/proc/stat', '/sys/fs/cgroup/memory.peak']:
        if Path(name).exists(): terminal[name] = Path(name).read_text()
    terminal['memory_boundary'] = 'whole sweep container, including file cache; not per-participant RSS'
    (a.output/'status.json').write_text(json.dumps(terminal, indent=2)+'\n')
    return bool(failures)


if __name__ == '__main__': raise SystemExit(main())
