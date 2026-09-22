#!/usr/bin/env python3
"""Generate the simple-rust-algo-bench blog post from the B5 evidence bundle.

Usage: b5_post.py EVIDENCE_DIR TEMPLATE OUTPUT [--check]

Reads EVIDENCE_DIR/timed/*.json, EVIDENCE_DIR/parity/*.json,
EVIDENCE_DIR/campaign.jsonl and EVIDENCE_DIR/sources.json, plus the two
protocol-size runs of ../b4-quegee for the drift and "the previous rerun said"
figures, and writes OUTPUT with every {{PLACEHOLDER}} in TEMPLATE replaced.
Every number in the post is computed here from those files; none is typed in.
With --check, OUTPUT must already equal what would be written.

The selections are b5_report.py's, so the post and the results document are
two renderings of one set of files. Rows keep a fixed order - fixture, then
run, then the order the run listed its participants - and nothing is sorted
by time, because a table sorted by time is a ranking. A median of integers
that falls on .5 is printed as .5 rather than rounded.
"""
import collections, json, pathlib, statistics, sys

E = pathlib.Path(sys.argv[1])
TEMPLATE = pathlib.Path(sys.argv[2])
OUT = pathlib.Path(sys.argv[3])
CHECK = '--check' in sys.argv[4:]
# The repository commit the bundle and the results document are linked at.
# A reference for the reader, not a measurement.
SOURCE_COMMIT = '633ff36305e1d6b201d04570a48f400e678dc70b'

RUNS = ['one-thread', 'full-width', 'pinned-one-thread', 'pinned-full-width',
        'large-one-thread', 'large-full-width', 'xlarge-one-thread', 'xlarge-full-width']
data = {r: json.loads((E/'timed'/f'{r}.json').read_text()) for r in RUNS}
idx = {r: {(c['fixture'].removesuffix('.edges'), c['algorithm'], c['participant'], c['call']): c
           for c in d['cells']} for r, d in data.items()}
b4 = {}
for run in ('one-thread', 'full-width'):
    for c in json.loads((E.parent/'b4-quegee'/'timed'/f'{run}.json').read_text())['cells']:
        b4[(run, c['fixture'].removesuffix('.edges'), c['algorithm'], c['participant'], c['call'])] = c

PROTOCOL = ('one-thread', 'full-width')
FAMILIES = ('hub', 'uniform')

def ms(c): return '—' if c is None else f"{c['total_ms']:.2f} ± {c['total_mad']:.2f}"
def flt(c): return '—' if c is None or c['minflt'] is None else f"{c['minflt']:.0f}"
def cell(run, fx, alg, p, call=None): return idx[run].get((fx, alg, p, call))
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

one = data['one-thread']
sizes = sorted({int(k[0].split('-')[1]) for r in idx for k in idx[r]})
protocol_size = max(s for s in sizes if s <= 65536)

# --- parity ----------------------------------------------------------------
parity = {p.stem.removeprefix('parity-'): json.loads(p.read_text()) for p in sorted((E/'parity').glob('parity-*.json'))}
counts = {}
for name in ('fixtures-unset', 'fixtures-1', 'fixtures-16'):
    counts[name] = collections.Counter(r['verdict'] for r in parity[name])
assert len({tuple(sorted(c.items())) for c in counts.values()}) == 1, 'protocol sets disagree'
pc = counts['fixtures-1']
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

# --- the kernel change ----------------------------------------------------------
rows, ratios = [], []
for run in [r for r in RUNS if not r.startswith('pinned')]:
    for fx in fixtures(run, FAMILIES):
        for suffix, old, new in grust_pairs(run):
            o, n = cell(run, fx, 'pagerank', old, 'second'), cell(run, fx, 'pagerank', new, 'second')
            if not (o and n): continue
            ratios.append(n['total_ms'] / o['total_ms'])
            rows.append(f"| `{fx}` | {run} | {kernel_name('pagerank', suffix)} | {ms(o)} | {ms(n)} | {ratios[-1]:.3f} |")
kernel = '\n'.join(rows)

# --- every cell that got worse ---------------------------------------------------
worse, compared = [], 0
for run in [r for r in RUNS if not r.startswith('pinned')]:
    for (fx, alg, participant, call), o in sorted(idx[run].items()):
        for suffix, old, new in grust_pairs(run):
            if participant != old: continue
            n = cell(run, fx, alg, new, call)
            if n is None: continue
            compared += 1
            ratio = n['total_ms'] / o['total_ms']
            if ratio > 1: worse.append((ratio, fx, alg, run, kernel_name(alg, suffix), call, o, n))
worse.sort(key=lambda w: (w[3], w[1], w[2], w[5]))
worst = sorted(worse, key=lambda w: -w[0])[:5]
path_pr = sorted([w for w in worse if w[2] == 'pagerank' and w[1].startswith('path')], key=lambda w: (w[1], w[3], w[5]))
tri = [w for w in worse if w[2] == 'triangles' and w[5] == 'second' and w[6]['minflt'] is not None and w[7]['minflt'] is not None]
wcc1 = [(n['total_ms'] / o['total_ms'], o, n) for run in PROTOCOL for fx in fixtures(run)
        for o, n in [(cell(run, fx, 'wcc', 'grust#1', 'first'), cell(run, fx, 'wcc', 'grust-next@counted#1', 'first'))] if o and n]

# --- BFS first call, against what B4 said ------------------------------------------
def bfs(run):
    out = []
    for fx in fixtures(run, FAMILIES):
        for s in suffixes(run):
            o, n = cell(run, fx, 'bfs', f'grust{s}', 'first'), cell(run, fx, 'bfs', f'grust-next@counted{s}', 'first')
            b, bo = b4.get((run, fx, 'bfs', f'grust-next@counted{s}', 'first')), b4.get((run, fx, 'bfs', f'grust{s}', 'first'))
            out.append((n['total_ms'] / o['total_ms'], b['total_ms'] / bo['total_ms']))
    return out
bfs_one, bfs_full = bfs('one-thread'), bfs('full-width')

# --- accounting modes at the protocol sizes ----------------------------------------
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

# --- triangles at width, layered, lineage, drift ------------------------------------
u = f'uniform-{protocol_size}'
tri_neo_one, tri_grust_one = cell('one-thread', u, 'triangles', 'neo4j-graph'), cell('one-thread', u, 'triangles', 'grust-next@counted#1', 'first')
tri_neo_full, tri_grust_full = cell('full-width', u, 'triangles', 'neo4j-graph'), cell('full-width', u, 'triangles', 'grust-next@counted', 'first')
tri_grust_full_unchecked = cell('full-width', u, 'triangles', 'grust-next@unchecked', 'first')
layered16 = [(call, cell('full-width', 'layered-16384', 'pagerank', 'grust', call),
              cell('full-width', 'layered-16384', 'pagerank', 'grust-next@counted', call)) for call in ('first', 'second')]
l16 = {call: n['total_ms'] / o['total_ms'] for call, o, n in layered16}
layered_shape = ('The second call is still slower and the first is not, which is the same shape the previous rerun reported.'
                 if l16['second'] > 1 and l16['first'] <= 1 else 'A call is still slower.' if max(l16.values()) > 1
                 else 'Neither call is slower on this host and this commit.')

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

drift = []
for p, call in (('grust#1', 'first'), ('grust#unset', 'first'), ('icecat', None), ('grustcat', None), ('neo4j-graph', None), ('icebug', None)):
    for fx in (f'hub-{protocol_size}', u):
        for alg in ('pagerank', 'wcc'):
            a, b = cell('one-thread', fx, alg, p, call), b4.get(('one-thread', fx, alg, p, call))
            if a and b: drift.append((a['total_ms'] / b['total_ms'], p))
drift_largest = max(drift, key=lambda d: abs(d[0] - 1))[1]

# --- host record ---------------------------------------------------------------------
records = [json.loads(line) for line in (E/'campaign.jsonl').read_text().splitlines()]
timed = [r for r in records if 'run' in r]
assert all(r['status'] == 'clean' and not r['sightings'] for r in timed)
sessions = sorted({s for r in records for s in r.get('resident_sessions', [])})
everything = [(r, c) for r, d in data.items() for c in d['cells']]
unusable = [(r, c) for r, c in everything if c['unusable']]
largest = max(timed, key=lambda r: r['steal_ticks'])
sources = json.loads((E/'sources.json').read_text())

values = {
    'SOURCE_COMMIT': SOURCE_COMMIT,
    'NEO4J_LIBRARY': one['participants']['neo4j-graph']['library'],
    'GRUST_NEW': sources['grust_next']['commit'][:7],
    'PROTOCOL_SIZE': grouped(protocol_size), 'PROTOCOL_SIZE_RAW': str(protocol_size), 'XLARGE_SIZE': grouped(max(sizes)),
    'WIDTH': str(data['full-width']['workers']),
    'PARITY_AGREE': str(pc['agrees']), 'PARITY_ABSENT': str(pc['absent']), 'PARITY_MISMATCH': str(pc['MISMATCH']),
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
    'BFS_ONE_SLOWER': str(sum(r > 1 for r, _ in bfs_one)), 'BFS_ONE_OF': str(len(bfs_one)),
    'BFS_ONE_MIN': pct(min(r for r, _ in bfs_one)), 'BFS_ONE_MAX': pct(max(r for r, _ in bfs_one)),
    'BFS_ONE_B4MIN': pct(min(b for _, b in bfs_one)), 'BFS_ONE_B4MAX': pct(max(b for _, b in bfs_one)),
    'BFS_FULL_SLOWER': str(sum(r > 1 for r, _ in bfs_full)), 'BFS_FULL_OF': str(len(bfs_full)),
    'BFS_FULL_MIN': pct(min(r for r, _ in bfs_full)), 'BFS_FULL_MAX': pct(max(r for r, _ in bfs_full)),
    'KERNEL_ROWS': kernel, 'KERNEL_FASTER': str(sum(r < 1 for r in ratios)), 'KERNEL_TOTAL': str(len(ratios)),
    'KERNEL_MIN': f"{min(ratios):.3f}", 'KERNEL_MAX': f"{max(ratios):.3f}",
    'ACCT_ROWS': acct, 'ACCT_PROTOCOL_CELLS': str(len(c_over_u)),
    'ACCT_MIN': pct(min(r for r, _ in c_over_u)), 'ACCT_MAX': pct(max(r for r, _ in c_over_u)),
    'ACCT_MAX_CELL': max(c_over_u)[1],
    'BUILD_COUNTED': f"{bh('counted'):.2f}", 'BUILD_WORK_UNCOUNTED': f"{bh('work-uncounted'):.2f}", 'BUILD_UNCHECKED': f"{bh('unchecked'):.2f}",
    'WORSE_COUNT': str(len(worse)), 'WORSE_TOTAL': str(compared),
    'WORSE_MIN': pct(min(w[0] for w in worse)), 'WORSE_MAX': pct(max(w[0] for w in worse)),
    'WORSE_WORST': '; '.join(f"`{fx}` {alg} {run} {kn} {call} {pct(r)}" for r, fx, alg, run, kn, call, _, _ in worst) + '.',
    'PATH_PR_COUNT': str(len(path_pr)), 'PATH_PR_MIN': pct(min(w[0] for w in path_pr)), 'PATH_PR_MAX': pct(max(w[0] for w in path_pr)),
    'PATH_PR_CELLS': '; '.join(f"`{fx}` {run} {call} {o['total_ms']:.2f} to {n['total_ms']:.2f} ms" for _, fx, _, run, _, call, o, n in path_pr) + '.',
    'TRI_COUNT': str(len(tri)), 'TRI_MIN': pct(min(w[0] for w in tri)), 'TRI_MAX': pct(max(w[0] for w in tri)),
    'TRI_ALL_MORE_FAULTS': 'every one of them takes' if all(w[7]['minflt'] > w[6]['minflt'] for w in tri)
                           else f"{sum(w[7]['minflt'] > w[6]['minflt'] for w in tri)} of them take",
    'TRI_FAULTS_OLD': count(statistics.median(w[6]['minflt'] for w in tri)), 'TRI_FAULTS_NEW': count(statistics.median(w[7]['minflt'] for w in tri)),
    'WCC_SLOWER': str(sum(r > 1 for r, _, _ in wcc1)), 'WCC_OF': str(len(wcc1)),
    'WCC_MIN': pct(min(r for r, _, _ in wcc1)), 'WCC_MAX': pct(max(r for r, _, _ in wcc1)),
    'WCC_FAULTS_EQUAL': str(sum(o['minflt'] == n['minflt'] for _, o, n in wcc1)),
    'TRI_NEO_ONE': ms(tri_neo_one), 'TRI_GRUST_ONE': ms(tri_grust_one),
    'TRI_NEO_FULL': ms(tri_neo_full), 'TRI_GRUST_FULL': ms(tri_grust_full), 'TRI_GRUST_FULL_UNCHECKED': ms(tri_grust_full_unchecked),
    'LAYERED16_FIRST': pct(l16['first']), 'LAYERED16_SECOND': pct(l16['second']), 'LAYERED16_SHAPE': layered_shape,
    'LINEAGE_ROWS': lineage, 'LINEAGE_GAP': lineage_gap,
    'DRIFT_MIN': pct(min(d for d, _ in drift)), 'DRIFT_MAX': pct(max(d for d, _ in drift)), 'DRIFT_LARGEST': drift_largest,
    'TIMED_RUNS': str(len(timed)), 'TOTAL_CELLS': grouped(len(everything)),
    'UNUSABLE_COUNT': str(len(unusable)), 'DISPERSION_RULE': str(one['unusable_dispersion']),
    'UNUSABLE_CELLS': '; '.join(f"`{c['participant']}` {c['algorithm']} `{c['fixture'].removesuffix('.edges')}` {c['call'] or ''} in {r}, {ms(c)}" for r, c in unusable),
    'LARGEST_STEAL_TICKS': str(largest['steal_ticks']), 'LARGEST_STEAL_RUN': largest['run'], 'LARGEST_STEAL_SECONDS': f"{largest['seconds']:.0f}",
    'RESIDENT_SESSIONS': plural(len(sessions), 'resident agent session was', 'resident agent sessions were'),
}

text = TEMPLATE.read_text()
used = set()
import re
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
    assert OUT.read_text() == out, f'{OUT} is stale: regenerate it with b5_post.py'
    print(f'{OUT}: up to date, {len(values)} values from {E}')
else:
    OUT.write_text(out)
    print(f'{OUT}: written, {len(values)} values from {E}')
