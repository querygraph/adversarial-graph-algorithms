#!/usr/bin/env python3
"""B2: every participant against the same independent reference, before timing.

A mismatch is reported as a mismatch and never as a time. Tolerances are per
participant, at the precision that participant can express, because an f32
kernel cannot be held to an f64 number. Nothing here is a measurement of speed:
durations printed by the participants are ignored.
"""
import argparse, json, pathlib, subprocess, sys

import reference as ref

ALGORITHMS = ['pagerank', 'wcc', 'bfs', 'triangles']
# f32 carries about seven significant digits; f64 comparisons are held far
# tighter but not to equality, since summation order legitimately differs.
RELATIVE = {'f32': 1e-6, 'f64': 1e-12}

def score_agrees(found, expected, relative, stopping):
    """PageRank scores are only defined to the iteration's own stopping point.

    Two implementations that both stop at L1 <= t can legitimately differ by
    about t per node, whatever their float width, so holding them to a
    precision-derived tolerance tests the stopping rule and not the answer.
    """
    return abs(found - expected) <= max(stopping, abs(expected) * relative)

def receipt(binary):
    out = subprocess.run([str(binary), '--receipt'], capture_output=True, text=True, timeout=120)
    out.check_returncode()
    return json.loads(out.stdout)

def run(binary, fixture, algorithm, tolerance, concurrency=None):
    command = [str(binary), '--fixture', str(fixture), '--algorithm', algorithm,
               '--tolerance', repr(tolerance)]
    # Concurrency selects a kernel, not a thread count: unset takes Grust's push
    # loop and 1 takes the pull kernel on one thread. Parity must therefore gate
    # the configuration that will be timed, not a neighbouring one.
    if concurrency is not None: command += ['--concurrency', str(concurrency)]
    out = subprocess.run(command, capture_output=True, text=True, timeout=1800)
    if out.returncode: return None, out.stderr.strip()[:200]
    return json.loads(out.stdout), None

def close(found, expected, relative):
    if expected == 0: return abs(found) <= relative
    return abs(found - expected) / abs(expected) <= relative

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--directory', type=pathlib.Path, default=pathlib.Path('/opt/bench'))
    p.add_argument('--fixtures', type=pathlib.Path, required=True)
    p.add_argument('--participants', nargs='+',
                   default=['library', 'icebug', 'icecat', 'grustcat', 'grust'])
    p.add_argument('--tolerance', type=float, default=1e-8,
                   help='the only value grustcat can express, so the only one all five share')
    p.add_argument('--concurrency', type=int,
                   help='passed to participants that accept it; unset and 1 are different kernels')
    p.add_argument('--output', type=pathlib.Path)
    a = p.parse_args()

    rows, mismatches = [], 0
    for fixture in sorted(a.fixtures.glob('*.edges')):
        nodes, edges = ref.read(fixture)
        scores, iterations = ref.pagerank(nodes, edges, tolerance=a.tolerance)
        ordered = sorted(scores, reverse=True)
        separation = ordered[0] - ordered[1] if len(ordered) > 1 else float('inf')
        labels, components = ref.components(nodes, edges)
        distances, reached, distance_sum = ref.bfs(nodes, edges, 0)
        triangles = ref.triangles(nodes, edges)
        expected = {
            'pagerank': dict(max=max(scores), argmax=scores.index(max(scores)), sum=sum(scores)),
            'wcc': dict(count=components, probe_label=labels[0]),
            'bfs': dict(reached=reached, distance_sum=distance_sum),
            'triangles': dict(triangles=triangles),
        }
        for name in a.participants:
            binary = a.directory/name
            declared = receipt(binary)
            relative = RELATIVE[declared.get('precision', 'f64')]
            for algorithm in ALGORITHMS:
                if algorithm not in declared['algorithms']:
                    rows.append(dict(fixture=fixture.name, participant=name, algorithm=algorithm,
                                     verdict='absent', detail='no such kernel in this project'))
                    continue
                found, error = run(binary, fixture, algorithm, a.tolerance, a.concurrency)
                if error is not None:
                    rows.append(dict(fixture=fixture.name, participant=name, algorithm=algorithm,
                                     verdict='error', detail=error))
                    mismatches += 1
                    continue
                differences, notes = [], []
                for field, value in expected[algorithm].items():
                    if field not in found: continue
                    if algorithm == 'pagerank' and field == 'argmax':
                        # On a near-uniform graph the top scores are separated by
                        # less than the stopping tolerance, so which node is the
                        # maximum is not determined by the computation. Comparing
                        # it there tests a tie-break, not an answer.
                        if separation <= a.tolerance:
                            # Not a comparison: the computation does not determine
                            # which node is the maximum, so a disagreement here is
                            # a tie-break and agreement is luck. Recorded, not scored.
                            if found[field] != value:
                                notes.append(f'argmax undetermined at tolerance {a.tolerance:g}: '
                                             f'top two reference scores differ by {separation:.3g}')
                            continue
                        ok = found[field] == value
                    elif algorithm == 'pagerank' and field in ('max', 'sum'):
                        ok = score_agrees(found[field], value, relative, a.tolerance)
                    else:
                        ok = close(found[field], value, relative) if isinstance(value, float) else found[field] == value
                    if not ok: differences.append(f'{field}: {found[field]!r} against {value!r}')
                verdict = 'agrees' if not differences else 'MISMATCH'
                mismatches += bool(differences)
                rows.append(dict(fixture=fixture.name, participant=name, algorithm=algorithm,
                                 verdict=verdict, detail='; '.join(differences + notes),
                                 notes=notes, iterations=found.get('iterations')))
    width = max(len(r['participant']) for r in rows)
    for row in rows:
        print(f"{row['fixture']:<18} {row['participant']:<{width}} {row['algorithm']:<10} "
              f"{row['verdict']:<8} {row.get('detail','')}")
    print(f"\n{len(rows)} checks, {mismatches} mismatches")
    if a.output: a.output.write_text(json.dumps(rows, indent=1)+'\n')
    return 1 if mismatches else 0

if __name__ == '__main__': sys.exit(main())
