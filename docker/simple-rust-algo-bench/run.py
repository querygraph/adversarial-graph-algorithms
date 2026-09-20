#!/usr/bin/env python3
"""B3's timed run: counterbalanced, parity-gated, and honest about absence.

Parity runs first and a mismatched cell is never timed. Variant order alternates
between repeats so a monotone drift affects both halves of every pair. Steal is
read across the whole run and printed above the tables, per AGENTS.md. Tables
are as wide as the participants that have the kernel, and each says who is
absent and that the reason is no such kernel rather than a slow one.
"""
import argparse, json, pathlib, statistics, subprocess, sys, time

ALGORITHMS = ['pagerank', 'wcc', 'bfs', 'triangles']

def steal_ticks():
    with open('/proc/stat') as handle:
        fields = handle.readline().split()
    return int(fields[8])

def receipt(binary):
    out = subprocess.run([str(binary), '--receipt'], capture_output=True, text=True, timeout=120)
    out.check_returncode()
    return json.loads(out.stdout)

def sample(binary, fixture, algorithm, tolerance):
    out = subprocess.run([str(binary), '--fixture', str(fixture), '--algorithm', algorithm,
                          '--tolerance', repr(tolerance)], capture_output=True, text=True, timeout=3600)
    out.check_returncode()
    return json.loads(out.stdout)

def spread(values):
    middle = statistics.median(values)
    return middle, statistics.median([abs(value - middle) for value in values])

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--directory', type=pathlib.Path, default=pathlib.Path('/opt/bench'))
    p.add_argument('--fixtures', type=pathlib.Path, required=True)
    p.add_argument('--participants', nargs='+',
                   default=['library', 'icebug', 'icecat', 'grustcat', 'grust'])
    p.add_argument('--tolerance', type=float, default=1e-8)
    p.add_argument('--warmups', type=int, default=1)
    p.add_argument('--repeats', type=int, default=5)
    p.add_argument('--parity', type=pathlib.Path, required=True,
                   help='parity.json from parity.py; a cell that did not agree is not timed')
    p.add_argument('--output', type=pathlib.Path, required=True)
    a = p.parse_args()

    verdicts = {(row['fixture'], row['participant'], row['algorithm']): row['verdict']
                for row in json.loads(a.parity.read_text())}
    declared = {name: receipt(a.directory/name) for name in a.participants}

    before, started = steal_ticks(), time.time()
    samples = []
    for fixture in sorted(a.fixtures.glob('*.edges')):
        for algorithm in ALGORITHMS:
            present = [name for name in a.participants
                       if algorithm in declared[name]['algorithms']
                       and verdicts.get((fixture.name, name, algorithm)) == 'agrees']
            if not present: continue
            for repeat in range(a.warmups + a.repeats):
                # ABBA: a monotone drift moves the first and last variant in
                # opposite directions across the pair, so the comparison absorbs it.
                order = present if repeat % 2 == 0 else list(reversed(present))
                for name in order:
                    found = sample(a.directory/name, fixture, algorithm, a.tolerance)
                    found.update(repeat=repeat, warmup=repeat < a.warmups)
                    samples.append(found)
    after = steal_ticks()

    kept = [s for s in samples if not s['warmup']]
    cells = {}
    for s in kept:
        cells.setdefault((s['fixture'], s['algorithm'], s['participant']), []).append(s)
    report = dict(
        steal_ticks_over_run=after - before, seconds=round(time.time() - started, 1),
        tolerance=a.tolerance, warmups=a.warmups, repeats=a.repeats,
        participants={name: declared[name] for name in a.participants},
        cells=[])
    for (fixture, algorithm, participant), rows in sorted(cells.items()):
        kernel, kernel_spread = spread([r['kernel_ms'] for r in rows])
        iterations = rows[0].get('iterations')
        report['cells'].append(dict(
            fixture=fixture, algorithm=algorithm, participant=participant,
            iterations=iterations,
            total_ms=kernel, total_mad=kernel_spread,
            per_iteration_ms=(kernel / iterations) if iterations else None,
            build_ms=spread([r['build_ms'] for r in rows])[0],
            parse_ms=spread([r['parse_ms'] for r in rows])[0],
            absent=[name for name in a.participants
                    if algorithm not in declared[name]['algorithms']]))
    a.output.write_text(json.dumps(report, indent=1)+'\n')
    print(f"steal over the run: {after - before} ticks")
    print(f"{len(kept)} timed samples in {report['seconds']}s -> {a.output}")
    for cell in report['cells']:
        per = f"{cell['per_iteration_ms']:.6f}" if cell['per_iteration_ms'] else '-'
        print(f"{cell['fixture']:<18} {cell['algorithm']:<10} {cell['participant']:<9} "
              f"iters {str(cell['iterations'] or '-'):>4}  total {cell['total_ms']:9.4f} "
              f"± {cell['total_mad']:.4f}  per-iteration {per}")

if __name__ == '__main__': sys.exit(main())
