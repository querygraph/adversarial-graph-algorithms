#!/usr/bin/env python3
"""B2: every participant against the same independent reference, before timing.

A mismatch is reported as a mismatch and never as a time. Tolerances are per
participant, at the precision that participant can express, because an f32
kernel cannot be held to an f64 number. Nothing here is a measurement of speed:
durations printed by the participants are ignored.

Two checks were added for the rerun, both recorded per PageRank row:

- **Every score against the reference, bit for bit**, for a participant that can
  write its scores (`scores_out` in its receipt). B3 published that four
  implementations return "the same f64 bit pattern"; what its parity compared
  was the maximum, the sum and the argmax. This records how many of the n
  scores are bit-identical to the reference's and the largest difference, so a
  claim about the vector rests on the vector. It is recorded, not gated: the
  reference forms each share as `d*s/deg` and Grust as `d*s*(1/deg)`, which may
  round differently in the last place while agreeing to far inside tolerance.
- **`--bits-identical BASE CANDIDATE...`**: every candidate's PageRank vector
  must have the same digest and iteration count as BASE's on every fixture.
  This is the gate that licenses comparing two builds' times: a kernel change
  that altered a score is a different function, not a faster one. A candidate
  that differs is a MISMATCH, and a mismatched cell is never timed.
"""
import argparse, hashlib, json, pathlib, pickle, struct, subprocess, sys, tempfile

import reference as ref
import variants

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

def digest(values):
    """FNV-1a over each value's little-endian IEEE-754 bits; the participant's own."""
    hash_ = 0xcbf29ce484222325
    for value in values:
        for byte in struct.pack('<d', value):
            hash_ = ((hash_ ^ byte) * 0x100000001b3) & 0xffffffffffffffff
    return f'{hash_:016x}'

def bits(value):
    return struct.unpack('<q', struct.pack('<d', value))[0]

def against_reference(found, expected):
    """How many scores are bit-identical to the reference's, and how far the rest are."""
    identical = sum(1 for a, b in zip(found, expected) if bits(a) == bits(b))
    return dict(identical=identical, of=len(expected),
                max_abs=max(abs(a - b) for a, b in zip(found, expected)),
                max_ulps=max(abs(bits(a) - bits(b)) for a, b in zip(found, expected)))

def receipt(binary, extra=()):
    """The variant's declaration, or the reason it refused to make one.

    A build asked for a mode it does not have exits non-zero here; that is a
    finding about the variant, recorded as an error on every row, not a crash.
    """
    out = subprocess.run([str(binary), '--receipt', *extra], capture_output=True, text=True, timeout=120)
    if out.returncode: return dict(refused=out.stderr.strip()[-300:])
    return json.loads(out.stdout)

def run(binary, fixture, algorithm, tolerance, concurrency=None, extra=(), scores_out=None):
    command = [str(binary), '--fixture', str(fixture), '--algorithm', algorithm,
               '--tolerance', repr(tolerance), *extra]
    # Concurrency selects a kernel, not a thread count: unset takes Grust's push
    # loop and 1 takes the pull kernel on one thread. Parity must therefore gate
    # the configuration that will be timed, not a neighbouring one.
    if concurrency is not None: command += ['--concurrency', str(concurrency)]
    if scores_out is not None: command += ['--scores-out', str(scores_out)]
    out = subprocess.run(command, capture_output=True, text=True, timeout=3600)
    if out.returncode: return None, out.stderr.strip()[-300:]
    return json.loads(out.stdout), None

def cached(cache, fixture, tolerance, name, compute):
    """The reference's result for this fixture's bytes, computed once.

    At 4,194,304 nodes the Python reference takes minutes per algorithm, and
    parity runs once per concurrency. The key is the fixture's SHA-256 and the
    tolerance, so a changed fixture or tolerance cannot reuse a stale answer.
    """
    if cache is None: return compute()
    digest_ = hashlib.sha256(fixture.read_bytes()).hexdigest()
    path = cache/f'{digest_}-{tolerance!r}-{name}.pickle'
    if path.exists(): return pickle.loads(path.read_bytes())
    value = compute()
    cache.mkdir(parents=True, exist_ok=True)
    path.write_bytes(pickle.dumps(value))
    return value

def close(found, expected, relative):
    if expected == 0: return abs(found) <= relative
    return abs(found - expected) / abs(expected) <= relative

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--directory', type=pathlib.Path, default=pathlib.Path('/opt/bench'))
    p.add_argument('--fixtures', type=pathlib.Path, required=True)
    p.add_argument('--participants', nargs='+',
                   default=['neo4j-graph', 'icebug', 'icecat', 'grustcat', 'grust'],
                   help='participant names, optionally with @accounting-mode; see variants.py')
    p.add_argument('--algorithms', nargs='+', default=ALGORITHMS)
    p.add_argument('--tolerance', type=float, default=1e-8,
                   help='the only value grustcat can express, so the only one all five share')
    p.add_argument('--concurrency', type=int,
                   help='passed to participants that accept it; unset and 1 are different kernels')
    p.add_argument('--bits-identical', nargs='+', metavar='KEY',
                   help='BASE then CANDIDATES: each candidate PageRank vector must equal BASE bit for bit')
    p.add_argument('--reference-cache', type=pathlib.Path,
                   help='directory keeping the reference result per fixture SHA-256 and tolerance')
    p.add_argument('--output', type=pathlib.Path)
    a = p.parse_args()

    specs = [variants.parse(name) for name in a.participants]
    if any('#' in spec['key'] for spec in specs):
        raise SystemExit('parity runs one concurrency at a time: pass --concurrency, not #N')
    receipts = {spec['key']: receipt(a.directory/spec['binary'], spec['args']) for spec in specs}
    scratch = pathlib.Path(tempfile.mkdtemp(prefix='parity-scores-'))

    rows, mismatches = [], 0
    for fixture in sorted(a.fixtures.glob('*.edges')):
        loaded = []
        def graph():
            if not loaded: loaded.append(ref.read(fixture))
            return loaded[0]
        memo = lambda name, compute: cached(a.reference_cache, fixture, a.tolerance, name, compute)
        scores, iterations = memo('pagerank', lambda: ref.pagerank(*graph(), tolerance=a.tolerance))
        ordered = sorted(scores, reverse=True)
        separation = ordered[0] - ordered[1] if len(ordered) > 1 else float('inf')
        # The reference computes only what this run checks: at the large size the
        # triangle enumeration alone is minutes of Python. Labels are reduced to
        # what is compared before caching, so the cache is not a copy of the graph.
        components, probe = (memo('wcc', lambda: (lambda r: (r[1], r[0][0]))(ref.components(*graph())))
                             if 'wcc' in a.algorithms else (None, None))
        labels = [probe]
        _, reached, distance_sum = ((None,) + memo('bfs', lambda: ref.bfs(*graph(), 0)[1:])
                                    if 'bfs' in a.algorithms else (None, None, None))
        triangles = memo('triangles', lambda: ref.triangles(*graph())) if 'triangles' in a.algorithms else None
        expected = {
            'pagerank': dict(max=max(scores), argmax=scores.index(max(scores)), sum=sum(scores)),
            'wcc': dict(count=components, probe_label=labels[0]),
            'bfs': dict(reached=reached, distance_sum=distance_sum),
            'triangles': dict(triangles=triangles),
        }
        reference_digest = digest(scores)
        for spec in specs:
            name, binary, declared = spec['key'], a.directory/spec['binary'], receipts[spec['key']]
            relative = RELATIVE[declared.get('precision', 'f64')]
            for algorithm in a.algorithms:
                row = dict(fixture=fixture.name, participant=name, algorithm=algorithm,
                           concurrency=a.concurrency, accounting=declared.get('accounting'))
                if 'refused' in declared:
                    rows.append(dict(row, verdict='error', detail=declared['refused']))
                    mismatches += 1
                    continue
                if algorithm not in declared['algorithms']:
                    rows.append(dict(row, verdict='absent', detail='no such kernel in this project'))
                    continue
                dump = (scratch/f'{fixture.stem}-{name}.scores'
                        if algorithm == 'pagerank' and declared.get('scores_out') else None)
                found, error = run(binary, fixture, algorithm, a.tolerance, a.concurrency,
                                   spec['args'], dump)
                if error is not None:
                    rows.append(dict(row, verdict='error', detail=error))
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
                if algorithm == 'pagerank':
                    row.update(found={k: found.get(k) for k in ('sum', 'max', 'argmax', 'scores_digest')},
                               reference=dict(iterations=iterations, sum=sum(scores), max=max(scores),
                                              scores_digest=reference_digest),
                               max_bits_equal_reference=bits(found['max']) == bits(max(scores)))
                    if dump is not None:
                        if not dump.exists():
                            differences.append('declared scores_out and wrote no scores')
                        else:
                            found_scores = [struct.unpack('>d', bytes.fromhex(line))[0]
                                            for line in dump.read_text().split()]
                            if digest(found_scores) != found.get('scores_digest'):
                                differences.append('written scores do not match the printed digest')
                            row['vector_against_reference'] = against_reference(found_scores, scores)
                            dump.unlink()
                row.update(verdict='agrees' if not differences else 'MISMATCH',
                           detail='; '.join(differences + notes), notes=notes,
                           iterations=found.get('iterations'))
                mismatches += bool(differences)
                rows.append(row)

    if a.bits_identical:
        base, *candidates = a.bits_identical
        for row in rows:
            if row['algorithm'] != 'pagerank' or row['participant'] not in candidates: continue
            if row['verdict'] != 'agrees': continue
            base_row = next((r for r in rows if r['fixture'] == row['fixture']
                             and r['participant'] == base and r['algorithm'] == 'pagerank'), None)
            if base_row is None or base_row['verdict'] != 'agrees':
                row.update(verdict='MISMATCH', detail=f'{base} has no agreeing PageRank row to compare bits with')
                mismatches += 1
                continue
            same = (row['found']['scores_digest'] == base_row['found']['scores_digest']
                    and row['iterations'] == base_row['iterations'])
            row['bits_identical_to'] = dict(participant=base, identical=same)
            if not same:
                row.update(verdict='MISMATCH',
                           detail=f"scores differ from {base}: digest {row['found']['scores_digest']} "
                                  f"against {base_row['found']['scores_digest']}, iterations "
                                  f"{row['iterations']} against {base_row['iterations']}")
                mismatches += 1

    width = max(len(r['participant']) for r in rows)
    for row in rows:
        extra = ''
        if 'vector_against_reference' in row:
            v = row['vector_against_reference']
            extra = f"  vector-bits-equal-reference={v['identical']}/{v['of']} max_ulps={v['max_ulps']}"
        if 'max_bits_equal_reference' in row:
            extra += f"  max-bits-equal-reference={row['max_bits_equal_reference']}"
        if 'bits_identical_to' in row:
            extra += f"  same-bits-as-{row['bits_identical_to']['participant']}={row['bits_identical_to']['identical']}"
        print(f"{row['fixture']:<20} {row['participant']:<{width}} {row['algorithm']:<10} "
              f"{row['verdict']:<8} {row.get('detail','')}{extra}")
    print(f"\n{len(rows)} checks, {mismatches} mismatches")
    if a.output: a.output.write_text(json.dumps(rows, indent=1)+'\n')
    return 1 if mismatches else 0

if __name__ == '__main__': sys.exit(main())
