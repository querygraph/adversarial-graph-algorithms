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

# Grust's kernels fall back to sequential below a published threshold; the
# library parallelises unconditionally. Below a floor `workers_above` returns
# None whatever concurrency was requested, so a small-size row would compare a
# parallel library against a Grust kernel that declined to parallelise -- and it
# would flatter us, which is the direction that is easiest not to notice. The
# units and floors are read from grust-algorithms/src/parallel.rs; each row
# records whether the Grust-family kernels were eligible at its size.
FLOORS = {
    'pagerank': (lambda nodes, edges: (nodes + edges) * 2, 1 << 14),
    'wcc': (lambda nodes, edges: nodes + edges * 2, 1 << 14),
    'bfs': (lambda nodes, edges: nodes + edges, 1 << 18),
}
GRUST_FAMILY = {'grust', 'grustcat', 'icecat'}

def eligibility(algorithm, nodes, edges):
    if algorithm not in FLOORS: return None
    units, floor = FLOORS[algorithm][0](nodes, edges), FLOORS[algorithm][1]
    return dict(units=units, floor=floor, parallel_eligible=units >= floor)

def steal_ticks():
    with open('/proc/stat') as handle:
        fields = handle.readline().split()
    return int(fields[8])

def receipt(binary):
    out = subprocess.run([str(binary), '--receipt'], capture_output=True, text=True, timeout=120)
    out.check_returncode()
    return json.loads(out.stdout)

def worker_env(workers):
    """Give every participant the same width, explicitly.

    The three projects take their thread count from three different places:
    Grust from `with_concurrency`, the library from `available_parallelism` for
    PageRank and triangles and from rayon for WCC, NetworKit from OpenMP. Left
    alone under a CPU quota they disagree - OpenMP reads the affinity mask and
    would oversubscribe a quota the others respect - so each is set by name and
    the value is recorded in every cell.
    """
    import os
    if workers is None: return None
    return dict(os.environ, OMP_NUM_THREADS=str(workers), RAYON_NUM_THREADS=str(workers),
                OPENBLAS_NUM_THREADS=str(workers))

def sample(binary, fixture, algorithm, tolerance, concurrency=None, workers=None):
    command = [str(binary), '--fixture', str(fixture), '--algorithm', algorithm,
               '--tolerance', repr(tolerance)]
    if concurrency is not None: command += ['--concurrency', str(concurrency)]
    out = subprocess.run(command, capture_output=True, text=True, timeout=3600,
                         env=worker_env(workers))
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
    p.add_argument('--concurrency', type=int,
                   help='passed to participants that accept it; unset and 1 are different kernels')
    p.add_argument('--workers', type=int,
                   help='thread width given to every participant by name: OMP_NUM_THREADS for '
                        'NetworKit, RAYON_NUM_THREADS for the library WCC, --concurrency for Grust. '
                        'Set it to the cgroup CPU count; left unset the three disagree.')
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
                    found = sample(a.directory/name, fixture, algorithm, a.tolerance, a.concurrency, a.workers)
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
        workers=a.workers, concurrency=a.concurrency,
        # Table rules, emitted with the data so a report cannot quietly drop them.
        notes=dict(
            width=('At full width, only participants declaring width_capable can use a second '
                   'thread. The others are shown with their times, labelled sequential by '
                   'construction, and no width-to-width ratio is drawn against them.'),
            lineage=('The lineage comparison - icebug to icecat to grustcat to grust - is valid '
                     'only at equal width, so it belongs to the one-thread run. At full width a '
                     'difference between them is a statement about threads, not about a rewrite.'),
            across=('Cells from runs at different widths are not divided by one another. A '
                    'scaling factor is its own table with its own heading.'),
            precision=('PageRank precision differs by participant: the library accumulates and '
                       'returns f32, every other participant f64. The score array is half the '
                       'bytes, so it is half the memory traffic on the one array PageRank touches '
                       'randomly per arc. State it under every PageRank table; it is a boundary, '
                       'not a rounding footnote. WCC and triangle counts carry no such difference '
                       '- component labels are indices and the triangle count is u64. '
                       'Size-dependent: at 65,536 nodes every working set fits in the measuring '
                       'host L3 with room to spare, so f32 buys bandwidth on one array and no '
                       'cache residency at all. The arrays cross a 24.8 MB L3 somewhere in the '
                       'hundreds of thousands of nodes at this density, and a run above that '
                       'must restate this sentence rather than inherit it.')),
        participants={name: declared[name] for name in a.participants},
        cells=[])
    for (fixture, algorithm, participant), rows in sorted(cells.items()):
        kernel, kernel_spread = spread([r['kernel_ms'] for r in rows])
        iterations = rows[0].get('iterations')
        report['cells'].append(dict(
            fixture=fixture, algorithm=algorithm, participant=participant,
            iterations=iterations,
            # An f32 kernel's residual can sit at its arithmetic floor rather
            # than below the tolerance it was asked for, which the iteration
            # count alone does not show.
            residual=rows[0].get('residual', rows[0].get('error')),
            precision=declared[participant].get('precision'),
            total_ms=kernel, total_mad=kernel_spread,
            per_iteration_ms=(kernel / iterations) if iterations else None,
            build_ms=spread([r['build_ms'] for r in rows])[0],
            grust_family_floor=(eligibility(algorithm, rows[0]['nodes'], rows[0]['edges'])
                                if participant in GRUST_FAMILY else None),
            # Declared by the participant, not inferred here: two of the five
            # cannot use a second thread whatever --workers says, so a
            # width-to-width ratio against them is not a statement about width.
            width_capable=declared[participant].get('width_capable'),
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
