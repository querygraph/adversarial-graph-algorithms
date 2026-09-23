#!/usr/bin/env python3
"""Generate the simple-rust-algo-bench blog post from four evidence bundles.

Usage: b9_post.py EVIDENCE_DIR TEMPLATE OUTPUT [TEMPLATE OUTPUT ...] [--check]

EVIDENCE_DIR is the B9 bundle. B7's, B6's and B5's bundles are read beside it,
from EVIDENCE_DIR/../b7-quegee, ../b6-quegee and ../b5-quegee. Every
{{PLACEHOLDER}} in every TEMPLATE is replaced with a value computed here from
those files; none is typed in. All the templates share one set of values, so a
figure that appears in the post and in the related-work note is one
computation, and a value the evidence supplies that no template uses is an
error. With --check, each OUTPUT must already equal what would be written.

This is `b6_post.py` carried forward. Its B5-and-B6 selections are kept
unchanged, so the post and the results document stay two renderings of one set
of files, and the campaigns the kernel stack added are computed by the same
rules `b7_report.py` uses for the results document's B7 and B9 sections.

Two rules the script enforces rather than states:

- **No absolute crosses a campaign.** A B9 millisecond is never divided by a
  B7, B6 or B5 millisecond. Where two campaigns appear in one sentence, each
  contributes a ratio formed inside its own bundle, and `ASSERT_NO_CROSS`
  below is the only place a cell of one campaign meets a cell of another: the
  unchanged-code table, whose purpose is to say how far the host moved.
- **Where counts differ, per sweep is the comparison.** The participants stop
  at three different iteration counts, so a total is the time to tolerance
  under that participant's own stopping rule and a per-iteration figure is the
  cost of one sweep. Every distance drawn between participants is drawn on the
  per-iteration column, with the sum of the two cells' MAD/median as its
  margin; a distance smaller than its margin is inside dispersion.

Rows keep a fixed order - fixture, then run, then the order the run listed its
participants - and nothing is sorted by time, because a table sorted by time is
a ranking.
"""
import collections, json, pathlib, re, statistics, sys

E = pathlib.Path(sys.argv[1])
CHECK = '--check' in sys.argv[2:]
B7, B6, B5 = E.parent/'b7-quegee', E.parent/'b6-quegee', E.parent/'b5-quegee'
# The repository commit the bundles and the results document are linked at.
# A reference for the reader, not a measurement.
SOURCE_COMMIT = 'a62e68c1977afe4a6a1eb52af6ed75208ad075c8'

RUNS6 = ['one-thread', 'full-width', 'pinned-one-thread', 'pinned-full-width',
         'large-one-thread', 'large-full-width', 'xlarge-one-thread', 'xlarge-full-width']
RUNS9 = ['one-thread', 'full-width', 'large-one-thread', 'large-full-width',
         'xlarge-one-thread', 'xlarge-full-width']
PROTOCOL = ('one-thread', 'full-width')
FAMILIES = ('hub', 'uniform')
LARGE_RUNS = ('large-one-thread', 'large-full-width', 'xlarge-one-thread', 'xlarge-full-width')
F32 = '+f32'

# ---------------------------------------------------------------------------
# loading
# ---------------------------------------------------------------------------

def load(root, runs, prefix=''):
    data = {r: json.loads((root/'timed'/f'{prefix}{r}.json').read_text()) for r in runs}
    idx = {r: {(c['fixture'].removesuffix('.edges'), c['algorithm'], c['participant'], c['call']): c
               for c in d['cells']} for r, d in data.items()}
    return data, idx

data, idx = load(B6, RUNS6)
data5, idx5 = load(B5, RUNS6[:2] + RUNS6[4:])
data7, idx7 = load(B7, RUNS9, 'b7-')
data9, idx9 = load(E, RUNS9, 'b9-')
sources = json.loads((B6/'sources.json').read_text())
sources5 = json.loads((B5/'sources.json').read_text())
sources7 = json.loads((B7/'sources.json').read_text())
sources9 = json.loads((E/'sources.json').read_text())
image9 = json.loads((E/'receipts'/'image.json').read_text())
audit9 = json.loads((E/'receipts'/'audit.json').read_text())
manifest9 = json.loads((E/'fixtures-manifest.json').read_text())
NEXT, NEXT5 = sources['grust_next']['commit'][:7], sources5['grust_next']['commit'][:7]
NEXT7, NEXT9 = sources7['grust_next']['commit'][:7], sources9['grust_next']['commit'][:7]
for s in (sources5, sources7, sources9):
    assert s['grust']['commit'] == sources['grust']['commit'], 'the campaigns timed different v0.22.0 builds'
for tree in sources9.values():
    assert tree['uncommitted'] == '', 'a B9 tree was built dirty'
assert manifest9['identical_to_b6'] is True, 'B9 did not time B6\'s fixtures'
assert len({b['sha256'] for b in audit9}) == len(audit9) == 6, 'six distinct binaries'

# ---------------------------------------------------------------------------
# formatting
# ---------------------------------------------------------------------------

def ms(c): return '—' if c is None else f"{c['total_ms']:.2f} ± {c['total_mad']:.2f}"
def flt(c): return '—' if c is None or c['minflt'] is None else f"{c['minflt']:.0f}"
def pct(r): return f"{100 * (r - 1):+.1f}%"
def count(x): return f"{x:.0f}" if float(x).is_integer() else f"{x:.1f}"
def signed_count(x): return count(x) if x < 0 else '+' + count(x)
def plural(n, one, many): return f"{n} {one if n == 1 else many}"
def grouped(n): return f"{n:,}"
def span(values, digits=3): return f"{min(values):.{digits}f} to {max(values):.{digits}f}"

def cell(run, fx, alg, p, call=None): return idx[run].get((fx, alg, p, call))
def cell5(run, fx, alg, p, call=None): return idx5[run].get((fx, alg, p, call))
def cell7(run, fx, p, call=None): return idx7[run].get((fx, 'pagerank', p, call))
def cell9(run, fx, p, call=None): return idx9[run].get((fx, 'pagerank', p, call))

def fixtures(run, families=None, which=idx):
    names = sorted({k[0] for k in which[run]})
    return [f for f in names if families is None or f.split('-')[0] in families]
def suffixes(run): return ['#1', '#unset'] if 'one-thread' in run else ['']
def pull_suffix(run): return '#1' if 'one-thread' in run else ''
def kernel_name(alg, suffix):
    if alg != 'pagerank': return 'concurrency ' + ('1' if suffix == '#1' else 'unset' if suffix == '#unset' else 'as the run')
    return 'pull' if suffix != '#unset' else 'push'
def grust_pairs(run): return [(s, f'grust{s}', f'grust-next@counted{s}') for s in suffixes(run)]
def ratio(o, n): return n['total_ms'] / o['total_ms']

# A cell's standing against v0.22.0, with the dispersion of both sides as the
# margin: the sum of the two relative MADs. Inside it the two are level;
# outside it one is faster. The rule is b6_report.py's, one rule for every cell.
def standing(o, n):
    r = ratio(o, n)
    margin = o['total_mad'] / o['total_ms'] + n['total_mad'] / n['total_ms']
    if r > 1 + margin: return 'still slower'
    if r < 1 - margin: return 'faster than v0.22.0'
    return 'within dispersion'

# A per-sweep distance and its margin, b7_report.py's rule: per-iteration ms
# over per-iteration ms on the same cell of the same run, with the sum of the
# two cells' MAD/median. Both cells are always from one campaign.
def sweep(a, b):
    if not a or not b or a['per_iteration_ms'] is None or b['per_iteration_ms'] is None: return None
    return (a['per_iteration_ms'] / b['per_iteration_ms'], (a['dispersion'] or 0) + (b['dispersion'] or 0))
def outside(r): return abs(r[0] - 1) > r[1]
def pm(r): return f"{r[0]:.3f} ± {r[1]:.3f}"
def by_pct(r): return f"{abs(100 * (r[0] - 1)):.1f}% ± {100 * r[1]:.1f}"

one = data['one-thread']
sizes = sorted({int(k[0].split('-')[1]) for r in idx for k in idx[r]})
protocol_size = max(s for s in sizes if s <= 65536)
large_sizes = [s for s in sizes if s > protocol_size]

# ---------------------------------------------------------------------------
# B6: parity, and the bits
# ---------------------------------------------------------------------------
parity = {p.stem.removeprefix('parity-'): json.loads(p.read_text()) for p in sorted((B6/'parity').glob('parity-*.json'))}
counts = {name: collections.Counter(r['verdict'] for r in parity[name])
          for name in ('fixtures-unset', 'fixtures-1', 'fixtures-16')}
assert len({tuple(sorted(c.items())) for c in counts.values()}) == 1, 'protocol sets disagree'
pc = counts['fixtures-1']
assert pc['error'] == 0
bits = [r['bits_identical_to']['identical'] for rows in parity.values() for r in rows if 'bits_identical_to' in r]
def ref(file, fx):
    r = next(x for x in parity[file] if x['participant'] == 'grust' and x['algorithm'] == 'pagerank' and x['fixture'] == fx + '.edges')
    return r['vector_against_reference']
ref_push_u = ref('fixtures-unset', f'uniform-{protocol_size}')
ref_push_h = ref('fixtures-unset', f'hub-{protocol_size}')
ref_pull_u = ref('fixtures-1', f'uniform-{protocol_size}')
parity_records6 = [json.loads(l) for l in (B6/'campaign.jsonl').read_text().splitlines() if 'run' not in json.loads(l)]

# ---------------------------------------------------------------------------
# B6: the transpose, on the build side
# ---------------------------------------------------------------------------
rows = []
for run in ('one-thread', 'large-one-thread', 'xlarge-one-thread'):
    for fx in fixtures(run, FAMILIES):
        if run == 'one-thread' and not fx.endswith(str(protocol_size)): continue
        o1, o2 = cell(run, fx, 'pagerank', 'grust#1', 'first'), cell(run, fx, 'pagerank', 'grust#1', 'second')
        n1, gc = cell(run, fx, 'pagerank', 'grust-next@counted#1', 'first'), cell(run, fx, 'pagerank', 'grustcat')
        rows.append(f"| `{fx}` | {ms(o1)} | {ms(o2)} | {ms(n1)} | {n1['incoming_ms']:.2f} | {ms(gc)} |")
transpose = '\n'.join(rows)

# ---------------------------------------------------------------------------
# B6: the allocator, corrected and re-decided on the counter
# ---------------------------------------------------------------------------
pairs = [(cell(run, fx, alg, f'grust{s}', 'first'), cell(run, fx, alg, f'grust-next@counted{s}', 'first'),
          cell(run, fx, alg, f'grust-next@counted+eager{s}', 'first'))
         for run in PROTOCOL for fx in fixtures(run) for alg in ('wcc', 'bfs') for s in suffixes(run)]
pairs = [p for p in pairs if all(p) and all(c['minflt'] is not None for c in p)]
RESIDUAL_FAULTS = 25  # the pre-registered line, from the results document's B5 protocol
residual = statistics.median(abs(n['minflt'] - o['minflt']) for o, n, _ in pairs)
eager_moved = [e['minflt'] - n['minflt'] for _, n, e in pairs if e['minflt'] > n['minflt']]
moved = collections.defaultdict(list)
for base, pinned in (('one-thread', 'pinned-one-thread'), ('full-width', 'pinned-full-width')):
    for fx in fixtures(pinned, FAMILIES):
        if not fx.endswith(str(protocol_size)): continue
        for alg in ('pagerank', 'wcc', 'bfs', 'triangles'):
            for participant in data[pinned]['participants']:
                free, pin = cell(base, fx, alg, participant), cell(pinned, fx, alg, participant)
                if free is None or pin is None:
                    free = free or cell(base, fx, alg, participant, 'first')
                    pin = pin or cell(pinned, fx, alg, participant, 'first')
                if not (free and pin): continue
                moved[participant.split('@')[0].split('#')[0]].append(pin['total_ms'] / free['total_ms'])
pin_verdict = '; '.join(f"`{p}` {pct(statistics.median(rs))} over {len(rs)} cells" for p, rs in sorted(moved.items())) + '.'
assert residual <= RESIDUAL_FAULTS, 'the template states the default-allocator branch of the rule; the evidence took the other'

# ---------------------------------------------------------------------------
# B6: the regression the padding commit was written against
# ---------------------------------------------------------------------------
path5 = []
for run in PROTOCOL:
    s = '#1' if run == 'one-thread' else ''
    for fx in [f for f in fixtures(run) if f.startswith('path')]:
        for call in ('first', 'second'):
            path5.append((ratio(cell5(run, fx, 'pagerank', f'grust{s}', call),
                                cell5(run, fx, 'pagerank', f'grust-next@counted{s}', call)), run, fx, call))
b5_path_worst = max(path5)
wcc5 = [ratio(cell5('one-thread', fx, 'wcc', 'grust#1', 'first'), cell5('one-thread', fx, 'wcc', 'grust-next@counted#1', 'first'))
        for fx in fixtures('one-thread')]
path_cells = []
for run in PROTOCOL:
    s = '#1' if run == 'one-thread' else ''
    for fx in [f for f in fixtures(run) if f.startswith('path')]:
        for call in ('first', 'second'):
            o, n = cell(run, fx, 'pagerank', f'grust{s}', call), cell(run, fx, 'pagerank', f'grust-next@counted{s}', call)
            o5, n5 = cell5(run, fx, 'pagerank', f'grust{s}', call), cell5(run, fx, 'pagerank', f'grust-next@counted{s}', call)
            path_cells.append((run, fx, call, ratio(o, n), ratio(o5, n5), standing(o, n)))
path_worst = next(c for c in path_cells if (c[0], c[1], c[2]) == (b5_path_worst[1], b5_path_worst[2], b5_path_worst[3]))
path_full = [c for c in path_cells if c[0] == 'full-width']
path_one = [c for c in path_cells if c[0] == 'one-thread']

# B6's PageRank kernel change against v0.22.0, second call on both sides
kernel_ratios = []
for run in [r for r in RUNS6 if not r.startswith('pinned')]:
    for fx in fixtures(run, FAMILIES):
        for suffix, old, new in grust_pairs(run):
            o, n = cell(run, fx, 'pagerank', old, 'second'), cell(run, fx, 'pagerank', new, 'second')
            if not (o and n): continue
            kernel_ratios.append(ratio(o, n))

# ---------------------------------------------------------------------------
# B6: every cell that got worse, and B5's slower cells on the padded commit
# ---------------------------------------------------------------------------
worse, compared = [], 0
for run in [r for r in RUNS6 if not r.startswith('pinned')]:
    for (fx, alg, participant, call), o in sorted(idx[run].items()):
        for suffix, old, new in grust_pairs(run):
            if participant != old: continue
            n = cell(run, fx, alg, new, call)
            if n is None: continue
            compared += 1
            if ratio(o, n) > 1: worse.append((ratio(o, n), fx, alg, run, kernel_name(alg, suffix), call, o, n))
worse.sort(key=lambda w: (w[3], w[1], w[2], w[5]))
worst = sorted(worse, key=lambda w: -w[0])[:5]
beyond = [w for w in worse if standing(w[6], w[7]) == 'still slower']
tri = [w for w in worse if w[2] == 'triangles' and w[5] == 'second' and w[6]['minflt'] is not None and w[7]['minflt'] is not None]
wcc1 = [(ratio(o, n), o, n) for fx in fixtures('one-thread')
        for o, n in [(cell('one-thread', fx, 'wcc', 'grust#1', 'first'), cell('one-thread', fx, 'wcc', 'grust-next@counted#1', 'first'))]]
worse5 = []
for run in [r for r in RUNS6 if not r.startswith('pinned')]:
    for (fx, alg, participant, call), o in sorted(idx5[run].items()):
        for suffix, old, new in grust_pairs(run):
            if participant != old: continue
            n = cell5(run, fx, alg, new, call)
            if n is None: continue
            if ratio(o, n) > 1: worse5.append((fx, alg, run, kernel_name(alg, suffix), suffix, call))
verdicts, still = collections.Counter(), []
for fx, alg, run, kn, suffix, call in worse5:
    o, n = cell(run, fx, alg, f'grust{suffix}', call), cell(run, fx, alg, f'grust-next@counted{suffix}', call)
    assert o and n, f'{run} {fx} {alg} {call}: timed in B5 and not in B6'
    verdicts[standing(o, n)] += 1
    if standing(o, n) == 'still slower': still.append((fx, alg, kn, call))
ALG = {'pagerank': 'PageRank', 'wcc': 'WCC', 'bfs': 'BFS', 'triangles': 'triangles'}
by_shape = collections.Counter(
    'PageRank on `path`' if alg == 'pagerank' and fx.startswith('path') else
    'the triangles second call' if alg == 'triangles' and call == 'second' else
    'the WCC first call at concurrency 1' if alg == 'wcc' and call == 'first' and kn == 'concurrency 1' else
    'the BFS first call' if alg == 'bfs' and call == 'first' else
    f'the {ALG[alg]} {call} call' for fx, alg, kn, call in still)
still_by_shape = '; '.join(f"{shape} {n}" for shape, n in by_shape.most_common())

def bfs(run):
    out = []
    for fx in fixtures(run, FAMILIES):
        for s in suffixes(run):
            o, n = cell(run, fx, 'bfs', f'grust{s}', 'first'), cell(run, fx, 'bfs', f'grust-next@counted{s}', 'first')
            out.append((ratio(o, n), standing(o, n)))
    return out
bfs_one, bfs_full = bfs('one-thread'), bfs('full-width')

# ---------------------------------------------------------------------------
# B6: what the accounting modes cost at the protocol sizes
# ---------------------------------------------------------------------------
c_over_u = []
for run in PROTOCOL:
    for fx in fixtures(run, FAMILIES):
        if not fx.endswith(str(protocol_size)): continue
        for alg in ('pagerank', 'wcc', 'triangles'):
            for suffix in suffixes(run):
                cs = [cell(run, fx, alg, f'grust-next@{m}{suffix}', 'first') for m in ('counted', 'work-uncounted', 'unchecked')]
                if not all(cs): continue
                c_over_u.append((cs[0]['total_ms'] / cs[2]['total_ms'], f"{alg}, {kernel_name(alg, suffix)}, `{fx}` at {run}"))

# ---------------------------------------------------------------------------
# B6: the host, and the drift against B5 on unchanged code
# ---------------------------------------------------------------------------
drift = []
for p, call in (('grust#1', 'first'), ('grust#unset', 'first'), ('icecat', None), ('grustcat', None), ('neo4j-graph', None), ('icebug', None)):
    for fx in (f'hub-{protocol_size}', f'uniform-{protocol_size}'):
        for alg in ('pagerank', 'wcc'):
            a, b = cell('one-thread', fx, alg, p, call), cell5('one-thread', fx, alg, p, call)
            drift.append((a['total_ms'] / b['total_ms'], p))
drift_largest = max(drift, key=lambda d: abs(d[0] - 1))[1]
large, large_no_grust = collections.defaultdict(list), []
for run in LARGE_RUNS:
    for fx in fixtures(run, FAMILIES):
        for participant in data[run]['participants']:
            call = 'first' if participant.startswith('grust') and not participant.startswith('grustcat') else None
            a, b = cell(run, fx, 'pagerank', participant, call), cell5(run, fx, 'pagerank', participant, call)
            large[run].append(a['total_ms'] / b['total_ms'])
            if participant in ('icebug', 'icecat', 'grustcat', 'neo4j-graph'): large_no_grust.append(large[run][-1])
large_all = [r for rs in large.values() for r in rs]
assert min(large_all) > 1, 'the template says every participant is slower above L3; the evidence disagrees'
cdata = json.loads((B6/'control'/'large-full-width-control.json').read_text())
cidx = {(c['fixture'].removesuffix('.edges'), c['algorithm'], c['participant'], c['call']): c for c in cdata['cells']}
attempts = [json.loads(line) for line in (B6/'control'/'campaign-control.jsonl').read_text().splitlines()]
assert len(attempts) == 2 and attempts[0]['status'].startswith('DISCARDED') and attempts[1]['status'] == 'clean'
cr5, cr6 = [], []
for fx in fixtures('large-full-width', FAMILIES):
    for participant in data['large-full-width']['participants']:
        call = 'first' if participant.startswith('grust') and not participant.startswith('grustcat') else None
        c, a, b = cidx[(fx, 'pagerank', participant, call)], cell('large-full-width', fx, 'pagerank', participant, call), cell5('large-full-width', fx, 'pagerank', participant, call)
        cr6.append(c['total_ms'] / a['total_ms']); cr5.append(c['total_ms'] / b['total_ms'])
assert statistics.median(cr5) > 1.1 and abs(statistics.median(cr6) - 1) < 0.1, 'the template says the slower state outlived the campaign'
thp = {}
for line in (B6/'control'/'vmstat-thp.txt').read_text().splitlines():
    if line.startswith('== '): side = line[3:]
    elif 'thp_fault_fallback' in line: thp[side] = int(re.search(r'thp_fault_fallback (\d+)', line).group(1))
assert len(thp) == 4 and len(set(thp.values())) == 1, 'the template says the THP fallback counter did not move'

# ---------------------------------------------------------------------------
# B7: the three stopping counts, and what f32 is not
# ---------------------------------------------------------------------------
def counts_of(which, runs, campaign):
    out = collections.defaultdict(list)
    for run in runs:
        for fx in fixtures(run, FAMILIES, which):
            for p, n in ((k[2], c['iterations']) for k, c in which[run].items() if k[0] == fx):
                if n is None: continue
                if p.startswith('neo4j-graph'): out['neo'].append(n)
                elif F32 in p: out['f32'].append(n)
                elif p.startswith('grust-next'): out['f64'].append(n)
    return out
counts7, counts9 = counts_of(idx7, RUNS9, 'b7'), counts_of(idx9, RUNS9, 'b9')
for c in (counts7, counts9):
    assert min(c['f32']) > max(c['f64']), 'the template says the f32 rows stop after the f64 rows'

# One count per participant per fixture and run, as the results document's
# side-by-side table counts them: a Grust row reports the same count on both
# calls, so the two calls are one cell here.
f32_same = 0
f32_cells = 0
for run in RUNS9:
    for fx in fixtures(run, FAMILIES, idx9):
        n = cell9(run, fx, 'neo4j-graph')
        seen = {}
        for (f, _, p, call), c in idx9[run].items():
            if f != fx or F32 not in p: continue
            seen.setdefault(p, c['iterations'])
        for p, n_iters in seen.items():
            if n is None or n_iters is None: continue
            f32_cells += 1
            f32_same += n_iters == n['iterations']

# How far the f32 answers are from the f64 reference, from B7's parity rows.
abs7 = [r['vector_against_reference']['max_abs'] for path in sorted((B7/'parity').glob('parity-b7-*.json'))
        for r in json.loads(path.read_text())
        if r['algorithm'] == 'pagerank' and F32 in r['participant'] and r.get('vector_against_reference')]
identical7 = [r['vector_against_reference']['identical'] for path in sorted((B7/'parity').glob('parity-b7-*.json'))
              for r in json.loads(path.read_text())
              if r['algorithm'] == 'pagerank' and F32 in r['participant'] and r.get('vector_against_reference')]
assert abs7 and max(identical7) == 0, 'the template says no f32 score is bit-identical to the reference'

# ---------------------------------------------------------------------------
# B9: parity, and the bits gate the five commits asserted
# ---------------------------------------------------------------------------
parity9 = {path.stem.removeprefix('parity-b9-'): [r for r in json.loads(path.read_text()) if r['algorithm'] == 'pagerank']
           for path in sorted((E/'parity').glob('parity-b9-*.json'))}
rows9 = [r for rows in parity9.values() for r in rows]
verdict9 = collections.Counter(r['verdict'] for r in rows9)
bits9_f64 = [r for r in rows9 if 'bits_identical_to' in r and F32 not in r['participant']]
bits9_f32 = [r for r in rows9 if 'bits_identical_to' in r and F32 in r['participant']]
assert all(r['bits_identical_to']['identical'] for r in bits9_f64 + bits9_f32), 'a B9 bits row is not identical'
assert verdict9['MISMATCH'] == verdict9['error'] == verdict9['not converged'] == 0
log9 = [json.loads(l) for l in (E/'campaign.jsonl').read_text().splitlines()]
timed9 = [r for r in log9 if 'run' in r]
parity_log9 = [r for r in log9 if 'run' not in r]
residents9 = sorted({s for r in log9 for s in r.get('resident_sessions', [])})
assert all(r['status'] == 'clean' and not r['sightings'] for r in log9), 'a B9 invocation was not clean'
cells9 = [c for r in RUNS9 for c in data9[r]['cells']]
unusable9 = [c for c in cells9 if c['unusable']]
worst9 = max(cells9, key=lambda c: c['dispersion'])
worst9_run = next(r for r in RUNS9 if worst9 in data9[r]['cells'])

# ---------------------------------------------------------------------------
# B9: one sweep of grust-next@unchecked+f32 against one sweep of neo4j-graph
# ---------------------------------------------------------------------------
lfl_rows, lfl = [], []
for run in RUNS9:
    s = pull_suffix(run)
    for fx in fixtures(run, FAMILIES, idx9):
        n = cell9(run, fx, 'neo4j-graph')
        g = cell9(run, fx, f'grust-next@unchecked+f32{s}', 'second')
        r = sweep(g, n)
        if r is None: continue
        lfl.append((fx, run, r))
        lfl_rows.append(f"| `{fx}` | {run} | {g['per_iteration_ms']:.3f} / {g['iterations']} | "
                        f"{n['per_iteration_ms']:.3f} / {n['iterations']} | {pm(r)} | {'yes' if outside(r) else 'no'} |")
lfl_below = [x for x in lfl if x[2][0] <= 1]
lfl_above = [x for x in lfl if x[2][0] > 1]
lfl_inside = [x for x in lfl_above if not outside(x[2])]
lfl_outside = sorted([x for x in lfl_above if outside(x[2])], key=lambda x: -x[2][0])
assert all(x[1] == 'one-thread' for x in lfl_outside), 'the template says every cell above its margin is at one thread'
def named(xs): return ', '.join(f"`{fx}` {run} ({pm(r)})" for fx, run, r in xs)
def named_pct(xs): return ', '.join(f"`{fx}` by {by_pct(r)}" for fx, run, r in xs)

# ---------------------------------------------------------------------------
# B9 and B7: what work accounting costs per sweep, each formed inside its own bundle
# ---------------------------------------------------------------------------
meter_rows, pull_meter, push_meter = [], [], []
for run in RUNS9:
    for fx in fixtures(run, FAMILIES, idx9):
        for s in suffixes(run):
            for tag, p in (('f32', F32), ('f64', '')):
                def pair(get):
                    return sweep(get(run, fx, f'grust-next@counted{p}{s}', 'second'),
                                 get(run, fx, f'grust-next@unchecked{p}{s}', 'second'))
                o, n = pair(cell7), pair(cell9)
                if n is None: continue
                kern = 'push' if s == '#unset' else 'pull'
                (push_meter if kern == 'push' else pull_meter).append((fx, run, tag, o, n))
                meter_rows.append(f"| `{fx}` | {run} | {kern} | {tag} | {'—' if o is None else pm(o)} | {pm(n)} |")
def meter_span(rs, i, size=None):
    vals = [r[i][0] for r in rs if r[i] and (size is None or size in r[0])]
    return span(vals)
pull_outside9 = [r for r in pull_meter if outside(r[4])]
pull_outside7 = [r for r in pull_meter if r[3] and outside(r[3])]
push_worse = [r for r in push_meter if r[3] and r[4][0] - r[3][0] > r[4][1] + r[3][1]]
big_meter = {str(s): [r for r in pull_meter if str(s) in r[0]] for s in large_sizes}
protocol_full = [r for r in pull_meter if r[1] == 'full-width' and str(protocol_size) in r[0]]

# ---------------------------------------------------------------------------
# B9 against B7 on unchanged code: the only place two campaigns' cells meet
# ---------------------------------------------------------------------------
ASSERT_NO_CROSS = 'the unchanged-code table'
unchanged = []
for run in RUNS9:
    for (fx, alg, p, call), c in sorted(idx9[run].items()):
        if p.split('#')[0].split('+')[0] not in ('grust', 'neo4j-graph'): continue
        o = cell7(run, fx, p, call)
        if not o or o['per_iteration_ms'] is None or c['per_iteration_ms'] is None: continue
        if o['unusable'] or c['unusable']: continue
        unchanged.append((c['per_iteration_ms'] / o['per_iteration_ms'], p, fx, run, call, o, c))
unchanged_lo, unchanged_hi = min(unchanged), max(unchanged)
neo_2m = sorted([u for u in unchanged if u[1] == 'neo4j-graph' and str(large_sizes[0]) in u[2] and u[3] == 'large-one-thread'],
                key=lambda u: u[2])
assert neo_2m, 'the template names the reference participant\'s own 2M one-thread sweep'
neo_2m_text = ', '.join(f"`{u[2]}` at B7's {u[5]['per_iteration_ms']:.0f} ms against B9's {u[6]['per_iteration_ms']:.0f} ms" for u in neo_2m)

# ---------------------------------------------------------------------------
# B9: what v0.22.0's own kernel did over the stack, inside B9
# ---------------------------------------------------------------------------
anchor_rows, anchor = [], []
for run in RUNS9:
    s = pull_suffix(run)
    for fx in fixtures(run, FAMILIES, idx9):
        o = cell9(run, fx, f'grust{s}', 'second')
        n = cell9(run, fx, f'grust-next@counted{s}', 'second')
        r = sweep(n, o)
        if r is None: continue
        anchor.append((fx, run, r))
        anchor_rows.append(f"| `{fx}` | {run} | {o['per_iteration_ms']:.3f} / {o['iterations']} | "
                           f"{n['per_iteration_ms']:.3f} / {n['iterations']} | {pm(r)} |")
assert all(a[2][0] < 1 for a in anchor), 'the template says every B9 counted sweep is below v0.22.0\'s in B9'

values = {
    'SOURCE_COMMIT': SOURCE_COMMIT,
    'NEO4J_LIBRARY': one['participants']['neo4j-graph']['library'],
    'GRUST_B5': NEXT5, 'GRUST_B6': NEXT, 'GRUST_B7': NEXT7, 'GRUST_B9': NEXT9,
    'BENCH_B6': sources['bench']['commit'][:7], 'BENCH_B5': sources5['bench']['commit'][:7],
    'BENCH_B9': sources9['bench']['commit'][:7], 'IMAGE_B9': image9['tag'],
    'GRUST_OLD': sources['grust']['commit'][:7],
    'PROTOCOL_SIZE': grouped(protocol_size), 'PROTOCOL_SIZE_RAW': str(protocol_size),
    'LARGE_SIZE': grouped(large_sizes[0]), 'XLARGE_SIZE': grouped(large_sizes[1]),
    'WIDTH': str(data['full-width']['workers']),
    # B6 parity and bits
    'PARITY_AGREE': str(pc['agrees']), 'PARITY_ABSENT': str(pc['absent']), 'PARITY_MISMATCH': str(pc['MISMATCH']),
    'PARITY_INVOCATIONS': str(len(parity_records6)), 'PARITY_EXIT1': str(sum(1 for r in parity_records6 if r['exit'] == 1)),
    'REF_OF': grouped(ref_push_u['of']),
    'REF_PUSH_UNIFORM': grouped(ref_push_u['identical']), 'REF_PUSH_UNIFORM_ULPS': str(ref_push_u['max_ulps']),
    'REF_PUSH_HUB': grouped(ref_push_h['identical']), 'REF_PUSH_HUB_ULPS': str(ref_push_h['max_ulps']),
    'REF_PULL_UNIFORM': grouped(ref_pull_u['identical']), 'REF_PULL_UNIFORM_ULPS': str(ref_pull_u['max_ulps']),
    'BITS_SAME': str(sum(bits)), 'BITS_ROWS': str(len(bits)),
    # B6 artifacts
    'TRANSPOSE_ROWS': transpose,
    'ALLOC_PAIRS': str(len(pairs)),
    'ALLOC_NEXT_FAULTS': signed_count(statistics.median(n['minflt'] - o['minflt'] for o, n, _ in pairs)),
    'ALLOC_EAGER_FAULTS': signed_count(statistics.median(e['minflt'] - n['minflt'] for _, n, e in pairs)),
    'ALLOC_EAGER_MOVED': str(len(eager_moved)),
    'ALLOC_EAGER_EXTRA_MIN': str(min(eager_moved)), 'ALLOC_EAGER_EXTRA_MAX': str(max(eager_moved)),
    'ALLOC_LINE': str(RESIDUAL_FAULTS), 'ALLOC_RESIDUAL': count(residual),
    'PIN_VERDICT': pin_verdict,
    # B6 regression and kernel change
    'B5_PATH_WORST': pct(b5_path_worst[0]), 'B5_PATH_WORST_CELL': f"`{b5_path_worst[2]}` {b5_path_worst[1]} {b5_path_worst[3]} call",
    'B5_WCC_SLOWER': str(sum(r > 1 for r in wcc5)), 'B5_WCC_OF': str(len(wcc5)), 'B5_WCC_MAX': pct(max(wcc5)),
    'PATH_WORST_B6': pct(path_worst[3]), 'PATH_WORST_STANDING': path_worst[5],
    'PATH_FULL_B5_MIN': pct(min(c[4] for c in path_full)), 'PATH_FULL_B5_MAX': pct(max(c[4] for c in path_full)),
    'PATH_FULL_B6_MIN': pct(min(c[3] for c in path_full)), 'PATH_FULL_B6_MAX': pct(max(c[3] for c in path_full)),
    'PATH_FULL_SLOWER': str(sum(c[5] == 'still slower' for c in path_full)), 'PATH_FULL_OF': str(len(path_full)),
    'PATH_ONE_B6_MIN': pct(min(c[3] for c in path_one)), 'PATH_ONE_B6_MAX': pct(max(c[3] for c in path_one)),
    'KERNEL_FASTER': str(sum(r < 1 for r in kernel_ratios)), 'KERNEL_TOTAL': str(len(kernel_ratios)),
    'KERNEL_MIN': f"{min(kernel_ratios):.3f}", 'KERNEL_MAX': f"{max(kernel_ratios):.3f}",
    # B6 accounting
    'ACCT_PROTOCOL_CELLS': str(len(c_over_u)),
    'ACCT_MIN': pct(min(r for r, _ in c_over_u)), 'ACCT_MAX': pct(max(r for r, _ in c_over_u)),
    'ACCT_MAX_CELL': max(c_over_u)[1],
    # B6 cells that got worse
    'WORSE_COUNT': str(len(worse)), 'WORSE_TOTAL': str(compared), 'WORSE_BEYOND': str(len(beyond)),
    'WORSE_MIN': pct(min(w[0] for w in worse)), 'WORSE_MAX': pct(max(w[0] for w in worse)),
    'WORSE_WORST': '; '.join(f"`{fx}` {alg} {run} {kn} {call} {pct(r)}" for r, fx, alg, run, kn, call, _, _ in worst) + '.',
    'B5_STAND_FASTER': str(verdicts['faster than v0.22.0']), 'B5_STAND_WITHIN': str(verdicts['within dispersion']),
    'B5_STAND_SLOWER': str(verdicts['still slower']), 'STILL_BY_SHAPE': still_by_shape,
    'TRI_COUNT': str(len(tri)), 'TRI_MIN': pct(min(w[0] for w in tri)), 'TRI_MAX': pct(max(w[0] for w in tri)),
    'TRI_FAULTS_OLD': count(statistics.median(w[6]['minflt'] for w in tri)),
    'TRI_FAULTS_NEW': count(statistics.median(w[7]['minflt'] for w in tri)),
    'WCC_SLOWER': str(sum(r > 1 for r, _, _ in wcc1)), 'WCC_OF': str(len(wcc1)),
    'WCC_MIN': pct(min(r for r, _, _ in wcc1)), 'WCC_MAX': pct(max(r for r, _, _ in wcc1)),
    'WCC_BEYOND': str(sum(standing(o, n) == 'still slower' for _, o, n in wcc1)),
    'WCC_FAULTS_EQUAL': str(sum(o['minflt'] == n['minflt'] for _, o, n in wcc1)),
    'BFS_ONE_SLOWER': str(sum(r > 1 for r, _ in bfs_one)), 'BFS_ONE_OF': str(len(bfs_one)),
    'BFS_ONE_MIN': pct(min(r for r, _ in bfs_one)), 'BFS_ONE_MAX': pct(max(r for r, _ in bfs_one)),
    'BFS_ONE_BEYOND': str(sum(s == 'still slower' for _, s in bfs_one)),
    'BFS_FULL_SLOWER': str(sum(r > 1 for r, _ in bfs_full)), 'BFS_FULL_OF': str(len(bfs_full)),
    'BFS_FULL_MIN': pct(min(r for r, _ in bfs_full)), 'BFS_FULL_MAX': pct(max(r for r, _ in bfs_full)),
    'BFS_FULL_BEYOND': str(sum(s == 'still slower' for _, s in bfs_full)),
    # B6 drift and control
    'DRIFT_MIN': pct(min(d for d, _ in drift)), 'DRIFT_MAX': pct(max(d for d, _ in drift)),
    'DRIFT_MEDIAN': pct(statistics.median(d for d, _ in drift)), 'DRIFT_LARGEST': drift_largest,
    'LARGE_MIN': pct(min(large_all)), 'LARGE_MAX': pct(max(large_all)),
    'LARGE_NO_GRUST_MIN': pct(min(large_no_grust)), 'LARGE_NO_GRUST_MAX': pct(max(large_no_grust)),
    'CONTROL_B6_MEDIAN': pct(statistics.median(cr6)), 'CONTROL_B5_MEDIAN': pct(statistics.median(cr5)),
    # B7: the three counts
    'B7_NEO_MIN': str(min(counts7['neo'])), 'B7_NEO_MAX': str(max(counts7['neo'])),
    'B7_F32_MIN': str(min(counts7['f32'])), 'B7_F32_MAX': str(max(counts7['f32'])),
    'B7_F64_MIN': str(min(counts7['f64'])), 'B7_F64_MAX': str(max(counts7['f64'])),
    'B7_F32_ABS_MIN': f"{min(abs7):.1e}", 'B7_F32_ABS_MAX': f"{max(abs7):.1e}",
    'B7_F32_IDENTICAL': str(max(identical7)),
    # B9: the counts, the parity, the record
    'B9_NEO_MIN': str(min(counts9['neo'])), 'B9_NEO_MAX': str(max(counts9['neo'])),
    'B9_F32_MIN': str(min(counts9['f32'])), 'B9_F32_MAX': str(max(counts9['f32'])),
    'B9_F64_MIN': str(min(counts9['f64'])), 'B9_F64_MAX': str(max(counts9['f64'])),
    'B9_F32_SAME': str(f32_same), 'B9_F32_CELLS': str(f32_cells),
    'B9_PARITY_ROWS': str(len(rows9)), 'B9_PARITY_AGREE': str(verdict9['agrees']),
    'B9_PARITY_MISMATCH': str(verdict9['MISMATCH']), 'B9_PARITY_UNCONVERGED': str(verdict9['not converged']),
    'B9_BITS_F64': f"{sum(r['bits_identical_to']['identical'] for r in bits9_f64)} of {len(bits9_f64)}",
    'B9_BITS_F32': f"{sum(r['bits_identical_to']['identical'] for r in bits9_f32)} of {len(bits9_f32)}",
    'B9_PARITY_INVOCATIONS': str(len(parity_log9)),
    'B9_CAMPAIGN_START': timed9[0]['before']['at'], 'B9_CAMPAIGN_END': timed9[-1]['after']['at'],
    'B9_TIMED_RUNS': str(len(timed9)), 'B9_CELLS': grouped(len(cells9)), 'B9_UNUSABLE': str(len(unusable9)),
    'B9_DISPERSION_RULE': str(data9['one-thread']['unusable_dispersion']),
    'B9_WORST_DISPERSION': f"{worst9['dispersion']:.3f}",
    'B9_WORST_CELL': f"`{worst9['participant']}` {worst9['fixture'].removesuffix('.edges')} in {worst9_run}",
    'B9_STEAL_MAX': str(max(r['steal_ticks'] for r in timed9)),
    'B9_RESIDENTS': plural(len(residents9), 'resident agent session was', 'resident agent sessions were'),
    'B9_FIXTURES': str(len(manifest9['fixtures'])), 'B9_BINARIES': str(len(audit9)),
    # B9: like for like
    'LFL_ROWS': '\n'.join(lfl_rows),
    'LFL_TOTAL': str(len(lfl)), 'LFL_BELOW': str(len(lfl_below)),
    'LFL_INSIDE': str(len(lfl_inside)), 'LFL_INSIDE_CELLS': named(lfl_inside) or 'none',
    'LFL_OUTSIDE': str(len(lfl_outside)), 'LFL_OUTSIDE_CELLS': named(lfl_outside) or 'none',
    'LFL_OUTSIDE_PCT': named_pct(lfl_outside) or 'none',
    'LFL_FULL_MIN': f"{min(x[2][0] for x in lfl if 'full-width' in x[1]):.3f}",
    'LFL_FULL_MAX': f"{max(x[2][0] for x in lfl if 'full-width' in x[1]):.3f}",
    # B9: against v0.22.0, inside B9
    'ANCHOR_ROWS': '\n'.join(anchor_rows),
    'ANCHOR_MIN': f"{min(a[2][0] for a in anchor):.3f}", 'ANCHOR_MAX': f"{max(a[2][0] for a in anchor):.3f}",
    'ANCHOR_CELLS': str(len(anchor)),
    # B9 and B7: the meter
    'METER_ROWS': '\n'.join(meter_rows),
    'METER_PULL_CELLS': str(len(pull_meter)),
    'METER_PULL_B9': meter_span(pull_meter, 4), 'METER_PULL_B7': meter_span(pull_meter, 3),
    'METER_PULL_OUTSIDE_B9': str(len(pull_outside9)), 'METER_PULL_OUTSIDE_B7': str(len(pull_outside7)),
    'METER_LARGE_B9': meter_span(big_meter[str(large_sizes[0])], 4), 'METER_LARGE_B7': meter_span(big_meter[str(large_sizes[0])], 3),
    'METER_LARGE_CELLS': str(len(big_meter[str(large_sizes[0])])),
    'METER_XLARGE_B9': meter_span(big_meter[str(large_sizes[1])], 4), 'METER_XLARGE_B7': meter_span(big_meter[str(large_sizes[1])], 3),
    'METER_XLARGE_CELLS': str(len(big_meter[str(large_sizes[1])])),
    'METER_PROTOCOL_FULL_B9': meter_span(protocol_full, 4), 'METER_PROTOCOL_FULL_B7': meter_span(protocol_full, 3),
    'METER_PUSH_CELLS': str(len(push_meter)),
    'METER_PUSH_B9': meter_span(push_meter, 4), 'METER_PUSH_B7': meter_span(push_meter, 3),
    'METER_PUSH_WORSE': str(len(push_worse)),
    # B9 against B7 on unchanged code
    'UNCHANGED_CELLS': str(len(unchanged)),
    'UNCHANGED_MEDIAN': f"{statistics.median(u[0] for u in unchanged):.3f}",
    'UNCHANGED_MIN': f"{unchanged_lo[0]:.3f}", 'UNCHANGED_MAX': f"{unchanged_hi[0]:.3f}",
    'UNCHANGED_MIN_CELL': f"`{unchanged_lo[1]}` {unchanged_lo[2]} {unchanged_lo[3]}",
    'UNCHANGED_MAX_CELL': f"`{unchanged_hi[1]}` {unchanged_hi[2]} {unchanged_hi[3]}",
    'UNCHANGED_NEO_2M': neo_2m_text,
    'ASSERT_NO_CROSS': ASSERT_NO_CROSS,
}

used = set()
# A template whose first line is `<!-- b9_post: wrap N -->` is a hand-wrapped
# document: the directive is stripped, and every paragraph a value was
# substituted into is re-wrapped to N columns so that a figure's width does not
# leave a ragged line in a file people also edit by hand. Paragraphs with no
# placeholder are left exactly as they are, so the diff shows only what the
# evidence changed. Tables, headings and fenced blocks are never re-wrapped.
WRAP = re.compile(r'^<!-- b9_post: wrap (\d+) -->\n')

def rewrap(block, width):
    if block.startswith(('|', '#', '    ', '```')) or '\n|' in block: return block
    import textwrap
    if block.lstrip().startswith('- '):
        items, current = [], []
        for line in block.split('\n'):
            if line.startswith('- ') and current:
                items.append(current); current = []
            current.append(line.strip())
        items.append(current)
        return '\n'.join(textwrap.fill(' '.join(' '.join(item).split()), width, subsequent_indent='  ',
                                       break_on_hyphens=False, break_long_words=False)
                         for item in items)
    return textwrap.fill(' '.join(block.split()), width, break_on_hyphens=False, break_long_words=False)

def render(template, out_path):
    def fill(m):
        key = m.group(1)
        assert key in values, f'{template}: asks for {key}, which the evidence does not supply'
        used.add(key)
        return values[key]
    text = template.read_text()
    wrap = WRAP.match(text)
    if wrap:
        text = text[wrap.end():]
        width = int(wrap.group(1))
        blocks = []
        for block in text.split('\n\n'):
            filled = re.sub(r'\{\{(\w+)\}\}', fill, block)
            blocks.append(rewrap(filled, width) if filled != block else block)
        out = '\n\n'.join(blocks)
    else:
        out = re.sub(r'\{\{(\w+)\}\}', fill, text)
    assert '{{' not in out, f'{template}: placeholder left unrendered'
    assert r'A\*' not in out, f'{template}: Ghost renders the escape literally; write A* as a code span'
    if CHECK:
        assert out_path.read_text() == out, f'{out_path} is stale: regenerate it with b9_post.py'
    else:
        out_path.write_text(out)
    return out_path

# Every template named on the command line shares one set of values, so a
# number that appears in the post and in the note is the same computation, and
# every value the evidence supplies is used by one of them.
targets = [pathlib.Path(p) for p in sys.argv[2:] if p != '--check']
assert len(targets) % 2 == 0 and targets, 'give TEMPLATE OUTPUT pairs'
written = [render(t, o) for t, o in zip(targets[0::2], targets[1::2])]
unused = set(values) - used
assert not unused, f'values never used: {sorted(unused)}'
print(f"{', '.join(str(p) for p in written)}: {'up to date' if CHECK else 'written'}, "
      f'{len(values)} values from {E} with {B7.name}, {B6.name} and {B5.name} beside it')
