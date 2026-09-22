#!/usr/bin/env python3
"""Generate the simple-rust-algo-bench blog post from the B6 evidence bundle.

Usage: b6_post.py EVIDENCE_DIR TEMPLATE OUTPUT [--check]

Reads EVIDENCE_DIR/timed/*.json, EVIDENCE_DIR/parity/*.json,
EVIDENCE_DIR/campaign.jsonl, EVIDENCE_DIR/campaign.log, EVIDENCE_DIR/sources.json
and EVIDENCE_DIR/control/, plus the B5 bundle beside it (EVIDENCE_DIR/../b5-quegee)
for every "B5 said" figure, and writes OUTPUT with every {{PLACEHOLDER}} in
TEMPLATE replaced. Every number in the post is computed here from those files;
none is typed in. A B5 cell is only ever shown as B5's own ratio beside B6's,
never mixed into a B6 ratio. With --check, OUTPUT must already equal what would
be written.

The selections are b6_report.py's, so the post and the results document are
two renderings of one set of files. Rows keep a fixed order - fixture, then
run, then the order the run listed its participants - and nothing is sorted
by time, because a table sorted by time is a ranking. A median of integers
that falls on .5 is printed as .5 rather than rounded.
"""
import collections, json, pathlib, re, statistics, sys

E = pathlib.Path(sys.argv[1])
TEMPLATE = pathlib.Path(sys.argv[2])
OUT = pathlib.Path(sys.argv[3])
CHECK = '--check' in sys.argv[4:]
B5 = E.parent/'b5-quegee'
# The repository commit the bundle and the results document are linked at.
# A reference for the reader, not a measurement.
SOURCE_COMMIT = 'faab6c806a4a408e91af4c7022064890240f806a'

RUNS = ['one-thread', 'full-width', 'pinned-one-thread', 'pinned-full-width',
        'large-one-thread', 'large-full-width', 'xlarge-one-thread', 'xlarge-full-width']
PROTOCOL = ('one-thread', 'full-width')
FAMILIES = ('hub', 'uniform')
LARGE_RUNS = ('large-one-thread', 'large-full-width', 'xlarge-one-thread', 'xlarge-full-width')

def load(root):
    data = {r: json.loads((root/'timed'/f'{r}.json').read_text()) for r in RUNS}
    idx = {r: {(c['fixture'].removesuffix('.edges'), c['algorithm'], c['participant'], c['call']): c
               for c in d['cells']} for r, d in data.items()}
    return data, idx
data, idx = load(E)
data5, idx5 = load(B5)
sources = json.loads((E/'sources.json').read_text())
sources5 = json.loads((B5/'sources.json').read_text())
NEXT, NEXT5 = sources['grust_next']['commit'][:7], sources5['grust_next']['commit'][:7]
assert sources['grust']['commit'] == sources5['grust']['commit'], 'B5 and B6 timed different v0.22.0 builds'

def ms(c): return '—' if c is None else f"{c['total_ms']:.2f} ± {c['total_mad']:.2f}"
def flt(c): return '—' if c is None or c['minflt'] is None else f"{c['minflt']:.0f}"
def cell(run, fx, alg, p, call=None): return idx[run].get((fx, alg, p, call))
def cell5(run, fx, alg, p, call=None): return idx5[run].get((fx, alg, p, call))
def pct(r): return f"{100 * (r - 1):+.1f}%"
def count(x): return f"{x:.0f}" if float(x).is_integer() else f"{x:.1f}"
def signed_count(x): return count(x) if x < 0 else '+' + count(x)
def plural(n, one, many): return f"{n} {one if n == 1 else many}"
def grouped(n): return f"{n:,}"
def fixtures(run, families=None):
    names = sorted({k[0] for k in idx[run]})
    return [f for f in names if families is None or f.split('-')[0] in families]
def suffixes(run): return ['#1', '#unset'] if 'one-thread' in run else ['']
def kernel_name(alg, suffix):
    if alg != 'pagerank': return 'concurrency ' + ('1' if suffix == '#1' else 'unset' if suffix == '#unset' else 'as the run')
    return 'pull' if suffix != '#unset' else 'push'
def grust_pairs(run): return [(s, f'grust{s}', f'grust-next@counted{s}') for s in suffixes(run)]
def ratio(o, n): return n['total_ms'] / o['total_ms']

# A cell's standing against v0.22.0, with the dispersion of both sides as the
# margin: the sum of the two relative MADs. Inside it the two are level; outside
# it one is faster. The rule is b6_report.py's and is the same for every cell.
def standing(o, n):
    r = ratio(o, n)
    margin = o['total_mad'] / o['total_ms'] + n['total_mad'] / n['total_ms']
    if r > 1 + margin: return 'still slower'
    if r < 1 - margin: return 'faster than v0.22.0'
    return 'within dispersion'

one = data['one-thread']
sizes = sorted({int(k[0].split('-')[1]) for r in idx for k in idx[r]})
protocol_size = max(s for s in sizes if s <= 65536)
large_sizes = [s for s in sizes if s > protocol_size]

# --- parity ----------------------------------------------------------------
parity = {p.stem.removeprefix('parity-'): json.loads(p.read_text()) for p in sorted((E/'parity').glob('parity-*.json'))}
counts = {}
for name in ('fixtures-unset', 'fixtures-1', 'fixtures-16'):
    counts[name] = collections.Counter(r['verdict'] for r in parity[name])
assert len({tuple(sorted(c.items())) for c in counts.values()}) == 1, 'protocol sets disagree'
pc = counts['fixtures-1']
assert pc['error'] == 0
bits = [r['bits_identical_to']['identical'] for rows in parity.values() for r in rows if 'bits_identical_to' in r]
def ref(file, fx):
    r = next(x for x in parity[file] if x['participant'] == 'grust' and x['algorithm'] == 'pagerank' and x['fixture'] == fx + '.edges')
    return r['vector_against_reference']
ref_push_u, ref_push_h, ref_pull_u = ref('fixtures-unset', f'uniform-{protocol_size}'), ref('fixtures-unset', f'hub-{protocol_size}'), ref('fixtures-1', f'uniform-{protocol_size}')

# --- the transpose, on the build side ----------------------------------------
rows = []
for run in ('one-thread', 'large-one-thread', 'xlarge-one-thread'):
    for fx in fixtures(run, FAMILIES):
        if run == 'one-thread' and not fx.endswith(str(protocol_size)): continue
        o1, o2 = cell(run, fx, 'pagerank', 'grust#1', 'first'), cell(run, fx, 'pagerank', 'grust#1', 'second')
        n1, gc = cell(run, fx, 'pagerank', 'grust-next@counted#1', 'first'), cell(run, fx, 'pagerank', 'grustcat')
        rows.append(f"| `{fx}` | {ms(o1)} | {ms(o2)} | {ms(n1)} | {n1['incoming_ms']:.2f} | {ms(gc)} |")
transpose = '\n'.join(rows)

# --- the allocator ------------------------------------------------------------
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

# --- what B5 left open, in B5's own figures ------------------------------------------
path5 = []
for run in PROTOCOL:
    s = '#1' if run == 'one-thread' else ''
    for fx in [f for f in fixtures(run) if f.startswith('path')]:
        for call in ('first', 'second'):
            path5.append((ratio(cell5(run, fx, 'pagerank', f'grust{s}', call), cell5(run, fx, 'pagerank', f'grust-next@counted{s}', call)), run, fx, call))
b5_path_worst = max(path5)
wcc5 = [ratio(cell5('one-thread', fx, 'wcc', 'grust#1', 'first'), cell5('one-thread', fx, 'wcc', 'grust-next@counted#1', 'first'))
        for fx in fixtures('one-thread')]

# --- PageRank on the path family, the cell the commit was written for ------------------
rows, path_cells = [], []
for run in PROTOCOL:
    s = '#1' if run == 'one-thread' else ''
    for fx in [f for f in fixtures(run) if f.startswith('path')]:
        for call in ('first', 'second'):
            o, n = cell(run, fx, 'pagerank', f'grust{s}', call), cell(run, fx, 'pagerank', f'grust-next@counted{s}', call)
            o5, n5 = cell5(run, fx, 'pagerank', f'grust{s}', call), cell5(run, fx, 'pagerank', f'grust-next@counted{s}', call)
            path_cells.append((run, fx, call, ratio(o, n), ratio(o5, n5), standing(o, n)))
            rows.append(f"| `{fx}` | {run} | {call} | {ms(o)} | {flt(o)} | {ms(n)} | {flt(n)} | {pct(ratio(o, n))} | {pct(ratio(o5, n5))} |")
path_rows = '\n'.join(rows)
path_worst = next(c for c in path_cells if (c[0], c[1], c[2]) == (b5_path_worst[1], b5_path_worst[2], b5_path_worst[3]))
path_full = [c for c in path_cells if c[0] == 'full-width']
path_one = [c for c in path_cells if c[0] == 'one-thread']

# --- the kernel change, with B5's ratio beside it -------------------------------------
rows, ratios = [], []
for run in [r for r in RUNS if not r.startswith('pinned')]:
    for fx in fixtures(run, FAMILIES):
        for suffix, old, new in grust_pairs(run):
            o, n = cell(run, fx, 'pagerank', old, 'second'), cell(run, fx, 'pagerank', new, 'second')
            if not (o and n): continue
            o5, n5 = cell5(run, fx, 'pagerank', old, 'second'), cell5(run, fx, 'pagerank', new, 'second')
            ratios.append(ratio(o, n))
            rows.append(f"| `{fx}` | {run} | {kernel_name('pagerank', suffix)} | {ms(o)} | {ms(n)} | {ratios[-1]:.3f} | {ratio(o5, n5):.3f} |")
kernel = '\n'.join(rows)

# --- every cell that got worse, on B6 ---------------------------------------------------
worse, compared = [], 0
for run in [r for r in RUNS if not r.startswith('pinned')]:
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

# --- B5's slower cells, on the padded commit ----------------------------------------------
worse5, compared5 = [], 0
for run in [r for r in RUNS if not r.startswith('pinned')]:
    for (fx, alg, participant, call), o in sorted(idx5[run].items()):
        for suffix, old, new in grust_pairs(run):
            if participant != old: continue
            n = cell5(run, fx, alg, new, call)
            if n is None: continue
            compared5 += 1
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

# --- BFS first call, with B5's ratio for the same cell ------------------------------------
def bfs(run):
    out = []
    for fx in fixtures(run, FAMILIES):
        for s in suffixes(run):
            o, n = cell(run, fx, 'bfs', f'grust{s}', 'first'), cell(run, fx, 'bfs', f'grust-next@counted{s}', 'first')
            o5, n5 = cell5(run, fx, 'bfs', f'grust{s}', 'first'), cell5(run, fx, 'bfs', f'grust-next@counted{s}', 'first')
            out.append((ratio(o, n), ratio(o5, n5), standing(o, n)))
    return out
bfs_one, bfs_full = bfs('one-thread'), bfs('full-width')

# --- accounting modes at the protocol sizes ----------------------------------------------
rows, c_over_u = [], []
for run in PROTOCOL:
    for fx in fixtures(run, FAMILIES):
        if not fx.endswith(str(protocol_size)): continue
        for alg in ('pagerank', 'wcc', 'triangles'):
            for suffix in suffixes(run):
                cs = [cell(run, fx, alg, f'grust-next@{m}{suffix}', 'first') for m in ('counted', 'work-uncounted', 'unchecked')]
                if not all(cs): continue
                neo = cell(run, fx, alg, 'neo4j-graph')
                c_over_u.append((cs[0]['total_ms'] / cs[2]['total_ms'], f"{alg}, {kernel_name(alg, suffix)}, `{fx}` at {run}"))
                rows.append(f"| `{fx}` | {run} | {alg}, {kernel_name(alg, suffix)} | " + ' | '.join(ms(c) for c in cs) + f" | {ms(neo)} |")
acct = '\n'.join(rows)
bh = lambda m: cell('one-thread', f'hub-{protocol_size}', 'pagerank', f'grust-next@{m}#1', 'first')['build_ms']

# --- triangles at width, layered, lineage ------------------------------------------------
u = f'uniform-{protocol_size}'
tri_neo_one, tri_grust_one = cell('one-thread', u, 'triangles', 'neo4j-graph'), cell('one-thread', u, 'triangles', 'grust-next@counted#1', 'first')
tri_neo_full, tri_grust_full = cell('full-width', u, 'triangles', 'neo4j-graph'), cell('full-width', u, 'triangles', 'grust-next@counted', 'first')
tri_grust_full_unchecked = cell('full-width', u, 'triangles', 'grust-next@unchecked', 'first')
l16 = {}
for call in ('first', 'second'):
    o, n = cell('full-width', 'layered-16384', 'pagerank', 'grust', call), cell('full-width', 'layered-16384', 'pagerank', 'grust-next@counted', call)
    o5, n5 = cell5('full-width', 'layered-16384', 'pagerank', 'grust', call), cell5('full-width', 'layered-16384', 'pagerank', 'grust-next@counted', call)
    l16[call] = (ratio(o, n), standing(o, n), ratio(o5, n5))

LINEAGE = [('neo4j-graph', None, 'no accounting; its own stopping rule'),
           ('icebug', None, 'NetworKit, `DISTRIBUTE_SINKS` set'),
           ('icecat', None, 'sequential by construction'),
           ('grustcat', None, 'sequential by construction; tolerance fixed in the crate'),
           ('grust#1', 'first', 'v0.22.0, pull: the transpose is built inside this call'),
           ('grust-next@counted#1', 'first', 'counted, pull: the transpose is in `build_ms`')]
rows = []
for p, call, note in LINEAGE:
    h, uu = cell('one-thread', f'hub-{protocol_size}', 'pagerank', p, call), cell('one-thread', u, 'pagerank', p, call)
    rows.append(f"| `{p}` | {h['precision']} | {h['per_iteration_ms']:.3f} | {h['iterations']} | {uu['per_iteration_ms']:.3f} | {uu['iterations']} | {note} |")
lineage = '\n'.join(rows)
lineage_gap = pct(cell('one-thread', u, 'pagerank', 'grust-next@counted#1', 'first')['per_iteration_ms'] /
                  cell('one-thread', u, 'pagerank', 'grustcat')['per_iteration_ms'])

# --- B5 against B6 on unchanged code, at the protocol size and above L3 ------------------------
drift = []
for p, call in (('grust#1', 'first'), ('grust#unset', 'first'), ('icecat', None), ('grustcat', None), ('neo4j-graph', None), ('icebug', None)):
    for fx in (f'hub-{protocol_size}', u):
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

# --- host record ---------------------------------------------------------------------------
records = [json.loads(line) for line in (E/'campaign.jsonl').read_text().splitlines()]
timed = [r for r in records if 'run' in r]
parity_records = [r for r in records if 'run' not in r]
assert all(r['status'] == 'clean' and not r['sightings'] for r in timed)
assert all(r['status'] == 'clean' and not r['sightings'] for r in parity_records)
exit1 = [r for r in parity_records if r['exit'] == 1]
sessions = sorted({s for r in records for s in r.get('resident_sessions', [])})
everything = [(r, c) for r, d in data.items() for c in d['cells']]
unusable = [(r, c) for r, c in everything if c['unusable']]
largest = max(timed, key=lambda r: r['steal_ticks'])
large_records = [r for r in timed if r['run'] in LARGE_RUNS]
log = (E/'campaign.log').read_text().splitlines()
start = next(l.split()[1] for l in log if l.startswith('CAMPAIGN-START'))
end = next(l.split()[1] for l in log if l.startswith('CAMPAIGN-END'))
if unusable:
    unusable_text = (f"of which {len(unusable)} reached the dispersion rule of {one['unusable_dispersion']} MAD/median and enters no table ("
                     + '; '.join(f"`{c['participant']}` {c['algorithm']} `{c['fixture'].removesuffix('.edges')}` {c['call'] or ''} in {r}, {ms(c)}" for r, c in unusable) + ')')
else:
    r, c = max(everything, key=lambda rc: rc[1]['dispersion'])
    unusable_text = (f"none of which reached the dispersion rule of {one['unusable_dispersion']} MAD/median; the largest dispersion was "
                     f"{c['dispersion']:.3f}, `{c['participant']}` {c['algorithm']} `{c['fixture'].removesuffix('.edges')}` {c['call'] or ''} in {r}")

# --- the control after the campaign ---------------------------------------------------------
cdata = json.loads((E/'control'/'large-full-width-control.json').read_text())
cidx = {(c['fixture'].removesuffix('.edges'), c['algorithm'], c['participant'], c['call']): c for c in cdata['cells']}
attempts = [json.loads(line) for line in (E/'control'/'campaign-control.jsonl').read_text().splitlines()]
assert len(attempts) == 2 and attempts[0]['status'].startswith('DISCARDED') and attempts[1]['status'] == 'clean'
hungry = sorted({h.split(' ', 2)[2] for s in attempts[0]['sightings'] for h in s['hungry']})
assert len(hungry) == 1, 'the template names one process in the discarded attempt'
hungry_pct = [int(h.split(' ', 2)[1].rstrip('%')) for s in attempts[0]['sightings'] for h in s['hungry']]
cr5, cr6 = [], []
for fx in fixtures('large-full-width', FAMILIES):
    for participant in data['large-full-width']['participants']:
        call = 'first' if participant.startswith('grust') and not participant.startswith('grustcat') else None
        c, a, b = cidx[(fx, 'pagerank', participant, call)], cell('large-full-width', fx, 'pagerank', participant, call), cell5('large-full-width', fx, 'pagerank', participant, call)
        cr6.append(c['total_ms'] / a['total_ms']); cr5.append(c['total_ms'] / b['total_ms'])
assert statistics.median(cr5) > 1.1 and abs(statistics.median(cr6) - 1) < 0.1, 'the template says the slower state outlived the campaign'
thp = {}
for line in (E/'control'/'vmstat-thp.txt').read_text().splitlines():
    if line.startswith('== '): side = line[3:]
    elif 'thp_fault_fallback' in line: thp[side] = int(re.search(r'thp_fault_fallback (\d+)', line).group(1))
assert len(thp) == 4 and len(set(thp.values())) == 1, 'the template says the THP fallback counter did not move'

values = {
    'SOURCE_COMMIT': SOURCE_COMMIT,
    'NEO4J_LIBRARY': one['participants']['neo4j-graph']['library'],
    'GRUST_NEW': NEXT, 'GRUST_B5': NEXT5, 'BENCH': sources['bench']['commit'][:7], 'BENCH_B5': sources5['bench']['commit'][:7],
    'PROTOCOL_SIZE': grouped(protocol_size), 'PROTOCOL_SIZE_RAW': str(protocol_size),
    'LARGE_SIZE': grouped(large_sizes[0]), 'XLARGE_SIZE': grouped(max(sizes)),
    'WIDTH': str(data['full-width']['workers']),
    'PARITY_AGREE': str(pc['agrees']), 'PARITY_ABSENT': str(pc['absent']), 'PARITY_MISMATCH': str(pc['MISMATCH']),
    'PARITY_INVOCATIONS': str(len(parity_records)), 'PARITY_EXIT1': str(len(exit1)),
    'REF_OF': grouped(ref_push_u['of']),
    'REF_PUSH_UNIFORM': grouped(ref_push_u['identical']), 'REF_PUSH_UNIFORM_ULPS': str(ref_push_u['max_ulps']),
    'REF_PUSH_HUB': grouped(ref_push_h['identical']), 'REF_PUSH_HUB_ULPS': str(ref_push_h['max_ulps']),
    'REF_PULL_UNIFORM': grouped(ref_pull_u['identical']), 'REF_PULL_UNIFORM_ULPS': str(ref_pull_u['max_ulps']),
    'BITS_SAME': str(sum(bits)), 'BITS_ROWS': str(len(bits)),
    'TRANSPOSE_ROWS': transpose,
    'ALLOC_PAIRS': str(len(pairs)),
    'ALLOC_NEXT_FAULTS': signed_count(statistics.median(n['minflt'] - o['minflt'] for o, n, _ in pairs)),
    'ALLOC_EAGER_FAULTS': signed_count(statistics.median(e['minflt'] - n['minflt'] for _, n, e in pairs)),
    'ALLOC_EAGER_MOVED': str(len(eager_moved)),
    'ALLOC_EAGER_EXTRA_MIN': str(min(eager_moved)), 'ALLOC_EAGER_EXTRA_MAX': str(max(eager_moved)),
    'ALLOC_LINE': str(RESIDUAL_FAULTS), 'ALLOC_RESIDUAL': count(residual),
    'PIN_VERDICT': pin_verdict,
    'B5_PATH_WORST': pct(b5_path_worst[0]), 'B5_PATH_WORST_CELL': f"`{b5_path_worst[2]}` {b5_path_worst[1]} {b5_path_worst[3]} call",
    'B5_WCC_SLOWER': str(sum(r > 1 for r in wcc5)), 'B5_WCC_OF': str(len(wcc5)), 'B5_WCC_MAX': pct(max(wcc5)),
    'PATH_ROWS': path_rows,
    'PATH_WORST_B6': pct(path_worst[3]), 'PATH_WORST_STANDING': path_worst[5],
    'PATH_FULL_B5_MIN': pct(min(c[4] for c in path_full)), 'PATH_FULL_B5_MAX': pct(max(c[4] for c in path_full)),
    'PATH_FULL_B6_MIN': pct(min(c[3] for c in path_full)), 'PATH_FULL_B6_MAX': pct(max(c[3] for c in path_full)),
    'PATH_FULL_SLOWER': str(sum(c[5] == 'still slower' for c in path_full)), 'PATH_FULL_OF': str(len(path_full)),
    'PATH_FULL_STILL_CELLS': '; '.join(f"`{fx}` {call} call {pct(r6)} against B5's {pct(r5)}"
                                       for run, fx, call, r6, r5, s in path_full if s == 'still slower') or 'none',
    'PATH_ONE_B6_MIN': pct(min(c[3] for c in path_one)), 'PATH_ONE_B6_MAX': pct(max(c[3] for c in path_one)),
    'PATH_ONE_B5_MIN': pct(min(c[4] for c in path_one)), 'PATH_ONE_B5_MAX': pct(max(c[4] for c in path_one)),
    'KERNEL_ROWS': kernel, 'KERNEL_FASTER': str(sum(r < 1 for r in ratios)), 'KERNEL_TOTAL': str(len(ratios)),
    'KERNEL_MIN': f"{min(ratios):.3f}", 'KERNEL_MAX': f"{max(ratios):.3f}",
    'ACCT_ROWS': acct, 'ACCT_PROTOCOL_CELLS': str(len(c_over_u)),
    'ACCT_MIN': pct(min(r for r, _ in c_over_u)), 'ACCT_MAX': pct(max(r for r, _ in c_over_u)),
    'ACCT_MAX_CELL': max(c_over_u)[1],
    'BUILD_COUNTED': f"{bh('counted'):.2f}", 'BUILD_WORK_UNCOUNTED': f"{bh('work-uncounted'):.2f}", 'BUILD_UNCHECKED': f"{bh('unchecked'):.2f}",
    'WORSE_COUNT': str(len(worse)), 'WORSE_TOTAL': str(compared), 'WORSE_BEYOND': str(len(beyond)),
    'WORSE_MIN': pct(min(w[0] for w in worse)), 'WORSE_MAX': pct(max(w[0] for w in worse)),
    'WORSE_WORST': '; '.join(f"`{fx}` {alg} {run} {kn} {call} {pct(r)}" for r, fx, alg, run, kn, call, _, _ in worst) + '.',
    'B5_WORSE_COUNT': str(len(worse5)), 'B5_WORSE_TOTAL': str(compared5),
    'B5_STAND_FASTER': str(verdicts['faster than v0.22.0']), 'B5_STAND_WITHIN': str(verdicts['within dispersion']),
    'B5_STAND_SLOWER': str(verdicts['still slower']), 'STILL_BY_SHAPE': still_by_shape,
    'TRI_COUNT': str(len(tri)), 'TRI_MIN': pct(min(w[0] for w in tri)), 'TRI_MAX': pct(max(w[0] for w in tri)),
    'TRI_ALL_MORE_FAULTS': 'every one of them takes' if all(w[7]['minflt'] > w[6]['minflt'] for w in tri)
                           else f"{sum(w[7]['minflt'] > w[6]['minflt'] for w in tri)} of them take",
    'TRI_FAULTS_OLD': count(statistics.median(w[6]['minflt'] for w in tri)), 'TRI_FAULTS_NEW': count(statistics.median(w[7]['minflt'] for w in tri)),
    'WCC_SLOWER': str(sum(r > 1 for r, _, _ in wcc1)), 'WCC_OF': str(len(wcc1)),
    'WCC_MIN': pct(min(r for r, _, _ in wcc1)), 'WCC_MAX': pct(max(r for r, _, _ in wcc1)),
    'WCC_BEYOND': str(sum(standing(o, n) == 'still slower' for _, o, n in wcc1)),
    'WCC_FAULTS_EQUAL': str(sum(o['minflt'] == n['minflt'] for _, o, n in wcc1)),
    'BFS_ONE_SLOWER': str(sum(r > 1 for r, _, _ in bfs_one)), 'BFS_ONE_OF': str(len(bfs_one)),
    'BFS_ONE_MIN': pct(min(r for r, _, _ in bfs_one)), 'BFS_ONE_MAX': pct(max(r for r, _, _ in bfs_one)),
    'BFS_ONE_BEYOND': str(sum(s == 'still slower' for _, _, s in bfs_one)),
    'BFS_ONE_B5MIN': pct(min(b for _, b, _ in bfs_one)), 'BFS_ONE_B5MAX': pct(max(b for _, b, _ in bfs_one)),
    'BFS_FULL_SLOWER': str(sum(r > 1 for r, _, _ in bfs_full)), 'BFS_FULL_OF': str(len(bfs_full)),
    'BFS_FULL_MIN': pct(min(r for r, _, _ in bfs_full)), 'BFS_FULL_MAX': pct(max(r for r, _, _ in bfs_full)),
    'BFS_FULL_BEYOND': str(sum(s == 'still slower' for _, _, s in bfs_full)),
    'BFS_FULL_B5MIN': pct(min(b for _, b, _ in bfs_full)), 'BFS_FULL_B5MAX': pct(max(b for _, b, _ in bfs_full)),
    'TRI_NEO_ONE': ms(tri_neo_one), 'TRI_GRUST_ONE': ms(tri_grust_one),
    'TRI_NEO_FULL': ms(tri_neo_full), 'TRI_GRUST_FULL': ms(tri_grust_full), 'TRI_GRUST_FULL_UNCHECKED': ms(tri_grust_full_unchecked),
    'LAYERED16_FIRST': pct(l16['first'][0]), 'LAYERED16_FIRST_STANDING': l16['first'][1], 'LAYERED16_FIRST_B5': pct(l16['first'][2]),
    'LAYERED16_SECOND': pct(l16['second'][0]), 'LAYERED16_SECOND_STANDING': l16['second'][1], 'LAYERED16_SECOND_B5': pct(l16['second'][2]),
    'LINEAGE_ROWS': lineage, 'LINEAGE_GAP': lineage_gap,
    'DRIFT_MIN': pct(min(d for d, _ in drift)), 'DRIFT_MAX': pct(max(d for d, _ in drift)),
    'DRIFT_MEDIAN': pct(statistics.median(d for d, _ in drift)), 'DRIFT_LARGEST': drift_largest,
    'LARGE_MIN': pct(min(large_all)), 'LARGE_MAX': pct(max(large_all)),
    'LARGE_RUN_RANGES': '; '.join(f"{run} {pct(min(rs))} to {pct(max(rs))} over {len(rs)} cells" for run, rs in large.items()),
    'LARGE_NO_GRUST_MIN': pct(min(large_no_grust)), 'LARGE_NO_GRUST_MAX': pct(max(large_no_grust)),
    'LARGE_STEAL_MAX': str(max(r['steal_ticks'] for r in large_records)), 'LARGE_SECONDS_MAX': f"{max(r['seconds'] for r in large_records):.0f}",
    'CONTROL_HUNGRY': hungry[0], 'CONTROL_HUNGRY_MIN': str(min(hungry_pct)), 'CONTROL_HUNGRY_MAX': str(max(hungry_pct)),
    'CONTROL_SIGHTINGS': str(len(attempts[0]['sightings'])), 'CONTROL_STEAL': str(attempts[1]['steal_ticks']), 'CONTROL_SECONDS': f"{attempts[1]['seconds']:.1f}",
    'CONTROL_B6_MIN': pct(min(cr6)), 'CONTROL_B6_MAX': pct(max(cr6)), 'CONTROL_B6_MEDIAN': pct(statistics.median(cr6)),
    'CONTROL_B5_MIN': pct(min(cr5)), 'CONTROL_B5_MAX': pct(max(cr5)), 'CONTROL_B5_MEDIAN': pct(statistics.median(cr5)),
    'CAMPAIGN_START': start, 'CAMPAIGN_END': end,
    'TIMED_RUNS': str(len(timed)), 'TOTAL_CELLS': grouped(len(everything)), 'UNUSABLE_TEXT': unusable_text,
    'LARGEST_STEAL_TICKS': str(largest['steal_ticks']), 'LARGEST_STEAL_RUN': largest['run'], 'LARGEST_STEAL_SECONDS': f"{largest['seconds']:.0f}",
    'RESIDENT_SESSIONS': plural(len(sessions), 'resident agent session was', 'resident agent sessions were'),
}

text = TEMPLATE.read_text()
used = set()
def fill(m):
    key = m.group(1)
    assert key in values, f'template asks for {key}, which the evidence does not supply'
    used.add(key)
    return values[key]
out = re.sub(r'\{\{(\w+)\}\}', fill, text)
unused = set(values) - used
assert not unused, f'values never used: {sorted(unused)}'
assert '{{' not in out
if CHECK:
    assert OUT.read_text() == out, f'{OUT} is stale: regenerate it with b6_post.py'
    print(f'{OUT}: up to date, {len(values)} values from {E}')
else:
    OUT.write_text(out)
    print(f'{OUT}: written, {len(values)} values from {E}')
