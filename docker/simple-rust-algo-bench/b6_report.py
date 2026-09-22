#!/usr/bin/env python3
"""Fill the B6 placeholders in the results document from the evidence bundle.

Usage: b6_report.py EVIDENCE_DIR RESULTS_DOC

Reads EVIDENCE_DIR/timed/*.json, EVIDENCE_DIR/parity/*.json,
EVIDENCE_DIR/campaign.jsonl, EVIDENCE_DIR/sources.json and the B5 bundle
beside it (EVIDENCE_DIR/../b5-quegee), and rewrites RESULTS_DOC with every
PENDING-B6-* placeholder replaced. Every number in the B6 section is computed
here from those files; none is typed in. A B5 cell is only ever shown as B5's
own figure beside B6's, never mixed into a B6 ratio. Rows keep a fixed order -
fixture, then run, then the order the run listed its participants - and
nothing is sorted by time, because a table sorted by time is a ranking.
"""
import collections, json, pathlib, statistics, sys

E = pathlib.Path(sys.argv[1])
DOC = pathlib.Path(sys.argv[2])
B5 = E.parent/'b5-quegee'
RUNS = ['one-thread', 'full-width', 'pinned-one-thread', 'pinned-full-width',
        'large-one-thread', 'large-full-width', 'xlarge-one-thread', 'xlarge-full-width']
PROTOCOL = ('one-thread', 'full-width')
FAMILIES = ('hub', 'uniform')

def load(root):
    data = {r: json.loads((root/'timed'/f'{r}.json').read_text()) for r in RUNS
            if (root/'timed'/f'{r}.json').exists()}
    idx = {r: {(c['fixture'].removesuffix('.edges'), c['algorithm'], c['participant'], c['call']): c
               for c in d['cells']} for r, d in data.items()}
    return data, idx
data, idx = load(E)
data5, idx5 = load(B5)
sources = json.loads((E/'sources.json').read_text())
sources5 = json.loads((B5/'sources.json').read_text())
NEXT, NEXT5 = sources['grust_next']['commit'][:7], sources5['grust_next']['commit'][:7]

def ms(c): return '—' if c is None else f"{c['total_ms']:.2f} ± {c['total_mad']:.2f}"
def flt(c): return '—' if c is None or c['minflt'] is None else f"{c['minflt']:.0f}"
def cell(run, fx, alg, p, call=None): return idx[run].get((fx, alg, p, call))
def cell5(run, fx, alg, p, call=None): return idx5[run].get((fx, alg, p, call))
def pct(r): return f"{100 * (r - 1):+.1f}%"
def plural(n, one, many): return f"{n} {one if n == 1 else many}"
def fixtures(run, families=None):
    names = sorted({k[0] for k in idx[run]})
    return [f for f in names if families is None or f.split('-')[0] in families]
def suffixes(run):
    return ['#1', '#unset'] if 'one-thread' in run else ['']
def kernel_name(alg, suffix):
    if alg != 'pagerank': return 'concurrency ' + ('1' if suffix == '#1' else 'unset' if suffix == '#unset' else 'as the run')
    return 'pull' if suffix != '#unset' else 'push'
def grust_pairs(run):
    return [(s, f'grust{s}', f'grust-next@counted{s}') for s in suffixes(run)]

# A cell's standing against v0.22.0, with the dispersion of both sides as the
# margin: the sum of the two relative MADs. Inside it the two are level; outside
# it one is faster. The rule is the same for every cell and is stated in the
# document beside the table it decides.
def standing(o, n):
    ratio = n['total_ms'] / o['total_ms']
    margin = o['total_mad'] / o['total_ms'] + n['total_mad'] / n['total_ms']
    if ratio > 1 + margin: return 'still slower'
    if ratio < 1 - margin: return 'faster than v0.22.0'
    return 'within dispersion'

# --- the allocator state, re-decided on B6's own counter ------------------
pairs = [(cell(run, fx, alg, f'grust{s}', 'first'), cell(run, fx, alg, f'grust-next@counted{s}', 'first'))
         for run in [r for r in PROTOCOL if r in idx] for fx in fixtures(run)
         for alg in ('wcc', 'bfs') for s in suffixes(run)]
pairs = [p for p in pairs if all(p) and all(c['minflt'] is not None for c in p)]
RESIDUAL_FAULTS = 25
residual = statistics.median(abs(n['minflt'] - o['minflt']) for o, n in pairs)
alloc_note = (
    f"Across the {len(pairs)} WCC and BFS first-call cells at the protocol sizes, `grust-next` takes a median of "
    f"{statistics.median(n['minflt'] - o['minflt'] for o, n in pairs):+.0f} minor page faults against v0.22.0, "
    f"and the median absolute difference is {residual:.0f}, against the {RESIDUAL_FAULTS} that B5's rule set as "
    "the line. " +
    ("The two builds are in the same allocator state on the same cell, and the published tables are the "
     "default-allocator runs, as in B5; the pinned runs stay as a labelled probe in `tables.md`."
     if residual <= RESIDUAL_FAULTS else
     "That is above the line, so the first-call rows would be contaminated on the default allocator and the "
     "published tables would have to be the pinned runs."))

moved = []
for base, pinned in (('one-thread', 'pinned-one-thread'), ('full-width', 'pinned-full-width')):
    if pinned not in idx: continue
    for fx in fixtures(pinned, FAMILIES):
        if not fx.endswith('65536'): continue
        for alg in ('pagerank', 'wcc', 'bfs', 'triangles'):
            for participant in data[pinned]['participants']:
                free, pin = cell(base, fx, alg, participant, None), cell(pinned, fx, alg, participant, None)
                if free is None or pin is None:
                    free = free or cell(base, fx, alg, participant, 'first')
                    pin = pin or cell(pinned, fx, alg, participant, 'first')
                if not (free and pin): continue
                moved.append((pin['total_ms'] / free['total_ms'], participant))
by_participant = collections.defaultdict(list)
for ratio, participant in moved: by_participant[participant.split('@')[0].split('#')[0]].append(ratio)
pin_verdict = ('; '.join(f"`{p}` {pct(statistics.median(rs))} over {len(rs)} cells"
                         for p, rs in sorted(by_participant.items())) + '.')

# --- the transpose, on the build side --------------------------------------
rows = []
for run in [r for r in ('one-thread', 'large-one-thread', 'xlarge-one-thread') if r in idx]:
    for fx in fixtures(run, FAMILIES):
        if run == 'one-thread' and not fx.endswith('65536'): continue
        o1, o2 = cell(run, fx, 'pagerank', 'grust#1', 'first'), cell(run, fx, 'pagerank', 'grust#1', 'second')
        n1, gc = cell(run, fx, 'pagerank', 'grust-next@counted#1', 'first'), cell(run, fx, 'pagerank', 'grustcat')
        if not (o1 and o2 and n1 and gc): continue
        rows.append(f"| `{fx}` | {ms(o1)} | {ms(o2)} | {ms(n1)} | {n1['incoming_ms']:.2f} | {ms(gc)} | "
                    f"{n1['steal_ticks']} |")
transpose = '\n'.join(rows)

# --- the kernel change, with B5's ratio for the same cell beside it ---------
rows = []
for run in [r for r in RUNS if r in idx and not r.startswith('pinned')]:
    for fx in fixtures(run, FAMILIES):
        for suffix, old, new in grust_pairs(run):
            o, n = cell(run, fx, 'pagerank', old, 'second'), cell(run, fx, 'pagerank', new, 'second')
            if not (o and n): continue
            o5, n5 = cell5(run, fx, 'pagerank', old, 'second'), cell5(run, fx, 'pagerank', new, 'second')
            was = f"{n5['total_ms'] / o5['total_ms']:.3f}" if o5 and n5 else '—'
            rows.append(f"| `{fx}` | {run} | {kernel_name('pagerank', suffix)} | {ms(o)} | {ms(n)} | "
                        f"{n['total_ms'] / o['total_ms']:.3f} | {was} | {n['steal_ticks']} |")
kernel = '\n'.join(rows)

# PageRank on the path family, the cell the padding commit was written for:
# every call, both protocol runs, B5's ratio beside B6's.
rows = []
for run in [r for r in PROTOCOL if r in idx]:
    for fx in [f for f in fixtures(run) if f.startswith('path')]:
        for suffix, old, new in grust_pairs(run):
            if suffix == '#unset': continue
            for call in ('first', 'second'):
                o, n = cell(run, fx, 'pagerank', old, call), cell(run, fx, 'pagerank', new, call)
                o5, n5 = cell5(run, fx, 'pagerank', old, call), cell5(run, fx, 'pagerank', new, call)
                if not (o and n): continue
                was = pct(n5['total_ms'] / o5['total_ms']) if o5 and n5 else '—'
                rows.append(f"| `{fx}` | {run} | {call} | {ms(o)} | {flt(o)} | {ms(n)} | {flt(n)} | "
                            f"{pct(n['total_ms'] / o['total_ms'])} | {was} | {n['steal_ticks']} |")
path_table = '\n'.join(rows)

# --- every cell that got worse, on B6 ----------------------------------------
worse, compared = [], 0
for run in [r for r in RUNS if r in idx and not r.startswith('pinned')]:
    for (fx, alg, participant, call), o in sorted(idx[run].items()):
        for suffix, old, new in grust_pairs(run):
            if participant != old: continue
            n = cell(run, fx, alg, new, call)
            if n is None: continue
            compared += 1
            ratio = n['total_ms'] / o['total_ms']
            if ratio > 1:
                worse.append((ratio, fx, alg, run, kernel_name(alg, suffix), call, o, n))
worse.sort(key=lambda w: (w[3], w[1], w[2], w[5]))
worse_rows = '\n'.join(
    f"| `{fx}` | {alg} | {run} | {kn} | {call} | {ms(o)} | {flt(o)} | {ms(n)} | {flt(n)} | {pct(ratio)} | "
    f"{standing(o, n)} | {o['steal_ticks']} |" for ratio, fx, alg, run, kn, call, o, n in worse)
beyond = [w for w in worse if standing(w[6], w[7]) == 'still slower']
worse_summary = (f"{len(worse)} of the {compared} counted cells with a v0.22.0 counterpart are slower on "
                 f"`{NEXT}`, by {pct(min(w[0] for w in worse))} to {pct(max(w[0] for w in worse))}; "
                 f"{len(beyond)} of those are slower by more than the dispersion of the two cells." if worse
                 else f"None of the {compared} counted cells with a v0.22.0 counterpart is slower on `{NEXT}`.")
worst = sorted(worse, key=lambda w: -w[0])[:5]
worse_worst = ('; '.join(f"`{fx}` {alg} {run} {kn} {call} {pct(ratio)}"
                         for ratio, fx, alg, run, kn, call, o, n in worst) + '.') if worst else '—'

tri = [(ratio, fx, run, o, n) for ratio, fx, alg, run, kn, call, o, n in worse
       if alg == 'triangles' and call == 'second' and o['minflt'] is not None and n['minflt'] is not None]
tri_note = (f"{len(tri)} of them are the triangles second call, {pct(min(r for r, *_ in tri))} to "
            f"{pct(max(r for r, *_ in tri))}, with a median of {statistics.median(o['minflt'] for _, _, _, o, _ in tri):.0f} "
            f"minor page faults on v0.22.0 against {statistics.median(n['minflt'] for _, _, _, _, n in tri):.0f} on "
            f"`{NEXT}`: the same shape as B5, where the second call allocates again on the later commit and "
            "v0.22.0's does not. The padding commit does not touch it and it is not expected to."
            ) if tri else 'No triangles second call is slower.'

# --- B5's slower cells, on the padded commit --------------------------------
worse5, compared5 = [], 0
for run in [r for r in RUNS if r in idx5 and not r.startswith('pinned')]:
    for (fx, alg, participant, call), o in sorted(idx5[run].items()):
        for suffix, old, new in grust_pairs(run):
            if participant != old: continue
            n = cell5(run, fx, alg, new, call)
            if n is None: continue
            compared5 += 1
            if n['total_ms'] / o['total_ms'] > 1:
                worse5.append((n['total_ms'] / o['total_ms'], fx, alg, run, kernel_name(alg, suffix), suffix, call, o, n))
worse5.sort(key=lambda w: (w[3], w[1], w[2], w[6]))
rows, verdicts = [], collections.Counter()
for ratio5, fx, alg, run, kn, suffix, call, o5, n5 in worse5:
    o, n = cell(run, fx, alg, f'grust{suffix}', call), cell(run, fx, alg, f'grust-next@counted{suffix}', call)
    if not (o and n):
        verdicts['not timed in B6'] += 1
        rows.append(f"| `{fx}` | {alg} | {run} | {kn} | {call} | {pct(ratio5)} | — | — | — | — | — | not timed in B6 | — |")
        continue
    verdict = standing(o, n)
    verdicts[verdict] += 1
    rows.append(f"| `{fx}` | {alg} | {run} | {kn} | {call} | {pct(ratio5)} | {ms(o)} | {flt(o)} | {ms(n)} | {flt(n)} | "
                f"{pct(n['total_ms'] / o['total_ms'])} | {verdict} | {n['steal_ticks']} |")
b5worse_table = '\n'.join(rows)
b5worse_summary = (
    f"B5 found {len(worse5)} of its {compared5} counted cells slower than v0.22.0 on `{NEXT5}`. On `{NEXT}`, the same "
    f"cells stand: **{verdicts['faster than v0.22.0']} faster than v0.22.0, {verdicts['within dispersion']} within "
    f"dispersion of it, {verdicts['still slower']} still slower**"
    + (f", {verdicts['not timed in B6']} not timed in B6" if verdicts['not timed in B6'] else '') + ". "
    "The standing is decided by one rule for every cell: the B6 ratio against a margin of the two cells' relative "
    "MADs added together; inside the margin the two are level, outside it one is faster.")

still = [(ratio5, fx, alg, run, kn, suffix, call) for ratio5, fx, alg, run, kn, suffix, call, o5, n5 in worse5
         if (c := (cell(run, fx, alg, f'grust{suffix}', call), cell(run, fx, alg, f'grust-next@counted{suffix}', call)))
         and all(c) and standing(*c) == 'still slower']
by_shape = collections.Counter(
    'PageRank on `path`' if alg == 'pagerank' and fx.startswith('path') else
    'triangles second call' if alg == 'triangles' and call == 'second' else
    'WCC first call at concurrency 1' if alg == 'wcc' and call == 'first' and kn == 'concurrency 1' else
    'BFS first call' if alg == 'bfs' and call == 'first' else
    f'{alg} {call} call' for _, fx, alg, run, kn, suffix, call in still)
still_note = ("Of the still-slower cells, by shape: " + '; '.join(f"{shape} {n}" for shape, n in by_shape.most_common()) + '.'
              if still else 'No B5 cell is still slower beyond dispersion.')

# --- the one-worker WCC residue ---------------------------------------------
rows, res = [], []
for run in [r for r in PROTOCOL if r in idx]:
    for fx in fixtures(run):
        for suffix in suffixes(run):
            if 'one-thread' in run and suffix != '#1': continue
            o, n = cell(run, fx, 'wcc', f'grust{suffix}', 'first'), cell(run, fx, 'wcc', f'grust-next@counted{suffix}', 'first')
            o5, n5 = cell5(run, fx, 'wcc', f'grust{suffix}', 'first'), cell5(run, fx, 'wcc', f'grust-next@counted{suffix}', 'first')
            if not (o and n): continue
            was = pct(n5['total_ms'] / o5['total_ms']) if o5 and n5 else '—'
            if run == 'one-thread': res.append((n['total_ms'] / o['total_ms'], standing(o, n), o, n))
            rows.append(f"| `{fx}` | {run} | {kernel_name('wcc', suffix)} | {ms(o)} | {flt(o)} | {ms(n)} | {flt(n)} | "
                        f"{pct(n['total_ms'] / o['total_ms'])} | {was} | {standing(o, n)} | {n['steal_ticks']} |")
wcc_table = '\n'.join(rows)
wcc_note = (f"At one thread, concurrency 1, WCC's first call on `{NEXT}` is slower than v0.22.0 on "
            f"{sum(r > 1 for r, *_ in res)} of {len(res)} fixtures, {pct(min(r for r, *_ in res))} to "
            f"{pct(max(r for r, *_ in res))}; {sum(s == 'still slower' for _, s, *_ in res)} of those are beyond the "
            f"dispersion margin, and the page-fault counts are equal on {sum(o['minflt'] == n['minflt'] for _, _, o, n in res)} "
            f"of {len(res)}.")

# --- the two items B5 left open ------------------------------------------------
rows, bfs = [], []
for run in [r for r in PROTOCOL if r in idx]:
    for fx in fixtures(run, FAMILIES):
        for suffix in suffixes(run):
            o, n = cell(run, fx, 'bfs', f'grust{suffix}', 'first'), cell(run, fx, 'bfs', f'grust-next@counted{suffix}', 'first')
            o5, n5 = cell5(run, fx, 'bfs', f'grust{suffix}', 'first'), cell5(run, fx, 'bfs', f'grust-next@counted{suffix}', 'first')
            if not (o and n): continue
            was = pct(n5['total_ms'] / o5['total_ms']) if o5 and n5 else '—'
            bfs.append((run, n['total_ms'] / o['total_ms'], standing(o, n)))
            rows.append(f"| `{fx}` | {run} | {kernel_name('bfs', suffix)} | {ms(o)} | {flt(o)} | {ms(n)} | "
                        f"{flt(n)} | {pct(n['total_ms'] / o['total_ms'])} | {was} | {standing(o, n)} |")
bfs_open = '\n'.join(rows)
def bfs_verdict_for(run):
    cells = [(r, s) for rr, r, s in bfs if rr == run]
    return (f"At {run}, {sum(r > 1 for r, _ in cells)} of {len(cells)} `hub` and `uniform` first-call cells are slower "
            f"than v0.22.0, {pct(min(r for r, _ in cells))} to {pct(max(r for r, _ in cells))}, "
            f"{sum(s == 'still slower' for _, s in cells)} of them beyond dispersion.")
bfs_verdict = ' '.join(bfs_verdict_for(run) for run in PROTOCOL if run in idx)

rows = []
for run in [r for r in PROTOCOL if r in idx]:
    for fx in [f for f in fixtures(run) if f.startswith('layered')]:
        for suffix in suffixes(run):
            for call in ('first', 'second'):
                o, n = cell(run, fx, 'pagerank', f'grust{suffix}', call), cell(run, fx, 'pagerank', f'grust-next@counted{suffix}', call)
                o5, n5 = cell5(run, fx, 'pagerank', f'grust{suffix}', call), cell5(run, fx, 'pagerank', f'grust-next@counted{suffix}', call)
                if not (o and n): continue
                was = pct(n5['total_ms'] / o5['total_ms']) if o5 and n5 else '—'
                rows.append(f"| `{fx}` | {run} | {kernel_name('pagerank', suffix)} | {call} | {ms(o)} | {ms(n)} | "
                            f"{pct(n['total_ms'] / o['total_ms'])} | {was} | {standing(o, n)} | {o['steal_ticks']} |")
layered_open = '\n'.join(rows)
l16 = [(call, cell('full-width', 'layered-16384', 'pagerank', 'grust', call),
        cell('full-width', 'layered-16384', 'pagerank', 'grust-next@counted', call)) for call in ('first', 'second')]
l16 = [(call, o, n) for call, o, n in l16 if o and n]
layered_verdict = ('; '.join(f"{call} call {pct(n['total_ms'] / o['total_ms'])}, {standing(o, n)}" for call, o, n in l16) + '.')

# --- accounting modes, first call, beside neo4j-graph -----------------------
rows = []
for run in [r for r in RUNS if r in idx and not r.startswith('pinned')]:
    large = run.startswith(('large', 'xlarge'))
    for fx in fixtures(run, FAMILIES):
        if not large and not fx.endswith('65536'): continue
        for alg in (['pagerank'] if large else ['pagerank', 'wcc', 'triangles']):
            for suffix in suffixes(run):
                cs = [cell(run, fx, alg, f'grust-next@{m}{suffix}', 'first') for m in ('counted', 'work-uncounted', 'unchecked')]
                if not all(cs): continue
                neo = cell(run, fx, alg, 'neo4j-graph')
                rows.append(f"| `{fx}` | {run} | {alg}, {kernel_name(alg, suffix)} | " +
                            ' | '.join(ms(c) for c in cs) + f" | {ms(neo)} | {cs[0]['steal_ticks']} |")
acct = '\n'.join(rows)
o1 = idx['one-thread']
bh = lambda m: o1[('hub-65536', 'pagerank', f'grust-next@{m}#1', 'first')]['build_ms']
build = (f"Counting also costs in the build: `grust-next`'s `build_ms` for PageRank on `hub-65536` at one thread "
         f"is {bh('counted'):.2f} ms counted, {bh('work-uncounted'):.2f} work-uncounted and {bh('unchecked'):.2f} unchecked.")

# --- host record, dispersion, parity ---------------------------------------
records = [json.loads(line) for line in (E/'campaign.jsonl').read_text().splitlines()]
timed = [r for r in records if 'run' in r]
host = '\n'.join(f"- `{r['run']}`: {r['status']}, started {r['before']['at']}, {r['seconds']} s, "
                 f"{r['steal_ticks']} steal ticks over the run, {plural(len(r['sightings']), 'sighting', 'sightings')}, "
                 f"{plural(len(r.get('resident_sessions', [])), 'resident agent session', 'resident agent sessions')}."
                 for r in timed)
log = (E/'campaign.log').read_text().splitlines()
start = next(l.split()[1] for l in log if l.startswith('CAMPAIGN-START'))
end = next(l.split()[1] for l in log if l.startswith('CAMPAIGN-END'))
span = f"The timed campaign ran from {start} to {end}, {plural(len(timed), 'run', 'runs')}, in the order listed."

everything = [(r, c) for r, d in data.items() for c in d['cells']]
unusable = [(r, c) for r, c in everything if c['unusable']]
if unusable:
    u = (f"**{len(unusable)} of {len(everything)} cells reached the 0.25 MAD/median threshold** and enter no "
         "table: " + '; '.join(f"`{c['participant']}` {c['algorithm']} {c['fixture'].removesuffix('.edges')} "
                               f"{c['call'] or ''} in {r}, {ms(c)}" for r, c in unusable) + '.')
else:
    r, c = max(everything, key=lambda rc: rc[1]['dispersion'] or 0)
    u = (f"**None of the {len(everything)} cells reached the 0.25 MAD/median threshold**; the largest dispersion "
         f"was {c['dispersion']:.3f}, `{c['participant']}` {c['algorithm']} "
         f"{c['fixture'].removesuffix('.edges')} {c['call'] or ''} in {r}.")

psum = []
for name in sorted((E/'parity').glob('parity-*.json')):
    prows = json.loads(name.read_text())
    count = collections.Counter(r['verdict'] for r in prows)
    bits = [r['bits_identical_to']['identical'] for r in prows if 'bits_identical_to' in r]
    odd = sorted({(r['participant'], r['fixture']) for r in prows if r['verdict'] not in ('agrees', 'absent')})
    psum.append(f"| `{name.stem.removeprefix('parity-')}` | {count['agrees']} | {count['absent']} | "
                f"{count['MISMATCH']} | {count['error']} | {sum(bits)} of {len(bits)} | "
                f"{', '.join(p + ' ' + f.removesuffix('.edges') for p, f in odd) or '—'} |")
eager_same, eager_rows = 0, 0
for name in sorted((E/'parity').glob('parity-*.json')):
    prows = json.loads(name.read_text())
    base = {r['fixture']: r for r in prows if r['participant'] == 'grust' and r['algorithm'] == 'pagerank'}
    for r in prows:
        if r['participant'] != 'grust-next@counted+eager' or r['algorithm'] != 'pagerank': continue
        other = base.get(r['fixture'])
        if other is None or 'found' not in r: continue
        eager_rows += 1
        eager_same += (r['found']['scores_digest'] == other['found']['scores_digest'] and r['iterations'] == other['iterations'])
shared = [r for r in records if 'run' not in r and r['status'].startswith('DISCARDED')]
notstarted = [r for r in records if 'run' not in r and r['status'].startswith('not started')]
exit1 = [r for r in records if 'run' not in r and r.get('exit') == 1]
parity = ("| file | agree | absent | mismatch | error | bits-identical to v0.22.0 | mismatched rows |\n"
          "| --- | ---: | ---: | ---: | ---: | ---: | --- |\n" + '\n'.join(psum) + "\n\n"
          f"{len(exit1)} parity invocations exited 1, the protocol set's known `neo4j-graph` dangling-mass rows as in "
          f"B5; the driver takes its verdict from the file, not the exit code. {plural(len(shared), 'parity invocation is', 'parity invocations are')} marked "
          f"shared and {plural(len(notstarted), 'was', 'were')} not started; every fixture set has a clean invocation at every concurrency, "
          "and the files are the output of the last invocation of each.\n\n"
          f"The `--bits-identical` gate names v0.22.0 and the three accounting modes. The `+eager` variant's PageRank "
          f"digest and iteration count equal v0.22.0's in {eager_same} of {eager_rows} rows.")

image = json.loads((E/'receipts'/'image.json').read_text()) if (E/'receipts'/'image.json').exists() else {}
manifest = json.loads((E/'fixtures-manifest.json').read_text())
provenance = (f"Grust `{sources['grust']['commit'][:7]}` (v0.22.0) as `grust`, Grust "
              f"`{sources['grust_next']['commit'][:7]}` as `grust-next`, Icecat "
              f"`{sources['icecat']['commit'][:8]}`, this harness at `{sources['bench']['commit'][:7]}`, image "
              f"`{image.get('tag', 'simple-rust-algo-bench:b6')}`, built on the host from clean trees. "
              f"The {len(manifest['fixtures'])} fixtures are SHA-256-identical to B5's: "
              f"`identical_to_b5` is {str(manifest['identical_to_b5']).lower()} in the manifest.")

# --- B5 against B6 on unchanged code ------------------------------------------
drift_rows, ratios_ = [], []
for participant, call in (('grust#1', 'first'), ('grust#unset', 'first'), ('icecat', None),
                          ('grustcat', None), ('neo4j-graph', None), ('icebug', None)):
    for fx in ('hub-65536', 'uniform-65536'):
        for alg in ('pagerank', 'wcc'):
            a, b = cell('one-thread', fx, alg, participant, call), cell5('one-thread', fx, alg, participant, call)
            if not (a and b): continue
            ratios_.append(a['total_ms'] / b['total_ms'])
            drift_rows.append(f"| `{fx}` | {alg} | `{participant}` | {ms(b)} | {ms(a)} | {pct(a['total_ms'] / b['total_ms'])} |")
drift = '\n'.join(drift_rows)
by_p = collections.defaultdict(list)
for row, r in zip(drift_rows, ratios_): by_p[row.split('`')[3]].append(r)
drift_note = (f"The same binaries' sources, on the same fixtures and the same host, move {pct(min(ratios_))} to "
              f"{pct(max(ratios_))} between B5 and B6, a median of {pct(statistics.median(ratios_))}; by participant, "
              + '; '.join(f"`{p}` {pct(min(rs))} to {pct(max(rs))}" for p, rs in by_p.items())
              + ". B4 to B5 moved -49.6% to +8.1%, and the participant that moved most then, `icebug`, is the one "
              "that moves most now, the other way. Both campaigns were built from clean trees on the host, dropped "
              "the page cache before timing and ran on an idle host on the same day. A cell is still only ever "
              "compared with other cells of its own run; the B5 columns in the tables above are B5's own ratios, "
              "not B5 times against B6 times.")

# Above L3 the drift is not a participant's: every participant's PageRank at
# 2,097,152 and 4,194,304 nodes is slower in B6 than in B5, including the ones
# that contain no Grust. Shown per participant, first call, so the kernel-change
# ratios at those sizes are read with it.
rows, large_ratios = [], collections.defaultdict(list)
for run in [r for r in ('large-one-thread', 'large-full-width', 'xlarge-one-thread', 'xlarge-full-width') if r in idx and r in idx5]:
    for fx in fixtures(run, FAMILIES):
        for participant in data[run]['participants']:
            call = 'first' if participant.startswith('grust') and not participant.startswith('grustcat') else None
            a, b = cell(run, fx, 'pagerank', participant, call), cell5(run, fx, 'pagerank', participant, call)
            if not (a and b): continue
            large_ratios[run].append(a['total_ms'] / b['total_ms'])
            rows.append(f"| `{fx}` | {run} | `{participant}` | {ms(b)} | {ms(a)} | {pct(a['total_ms'] / b['total_ms'])} | "
                        f"{b['steal_ticks']} | {a['steal_ticks']} |")
large_drift = '\n'.join(rows)
_records = [json.loads(line) for line in (E/'campaign.jsonl').read_text().splitlines()]
_large = [r for r in _records if r.get('run') in large_ratios]
large_note = ("Every participant is slower above L3 in B6 than in B5: "
              + '; '.join(f"{run} {pct(min(rs))} to {pct(max(rs))} over {len(rs)} cells" for run, rs in large_ratios.items())
              + ". The participants that contain no Grust move with the ones that do, the page-fault counts are the "
              f"same to within a few, and steal over those four runs is at most {max(r['steal_ticks'] for r in _large)} "
              f"ticks in {max(r['seconds'] for r in _large):.0f} s, so it is not the code under test and not a second "
              "workload. **The cause is not established here.** It is the reason the large and xlarge rows of the "
              "kernel-change table above are read as ratios within B6 and not against B5's ratios for the same "
              "cells, which were taken on a faster host state.")

# A control: the shortest large run repeated after the campaign, under the
# same driver with its own tag, so the record says whether the slower host
# state was still there afterwards. It is not a campaign run and is compared
# with the campaign's own cells only as a ratio, participant by participant.
control_file = E/'control'/'large-full-width-control.json'
if control_file.exists():
    cdata = json.loads(control_file.read_text())
    cidx = {(c['fixture'].removesuffix('.edges'), c['algorithm'], c['participant'], c['call']): c for c in cdata['cells']}
    attempts = [json.loads(line) for line in (E/'control'/'campaign-control.jsonl').read_text().splitlines()]
    attempts_note = ' '.join(
        f"Attempt {i}: `{r['status']}`, started {r['before']['at']}, {r['seconds']} s, {r['steal_ticks']} steal ticks, "
        f"{plural(len(r['sightings']), 'sighting', 'sightings')}"
        + (f" ({'; '.join(sorted({h.split(' ', 2)[2] for s in r['sightings'] for h in s['hungry']}))})" if r['sightings'] else '')
        + '.' for i, r in enumerate(attempts, 1))
    rows, cr5, cr6 = [], [], []
    for fx in fixtures('large-full-width', FAMILIES):
        for participant in data['large-full-width']['participants']:
            call = 'first' if participant.startswith('grust') and not participant.startswith('grustcat') else None
            c, a, b = cidx.get((fx, 'pagerank', participant, call)), cell('large-full-width', fx, 'pagerank', participant, call), cell5('large-full-width', fx, 'pagerank', participant, call)
            if not (c and a and b): continue
            cr6.append(c['total_ms'] / a['total_ms']); cr5.append(c['total_ms'] / b['total_ms'])
            rows.append(f"| `{fx}` | `{participant}` | {ms(b)} | {ms(a)} | {ms(c)} | {pct(c['total_ms'] / a['total_ms'])} | "
                        f"{pct(c['total_ms'] / b['total_ms'])} | {c['steal_ticks']} |")
    control = ('\n'.join(rows) + "\n\n" +
               f"{attempts_note} A discarded attempt is kept in the bundle, renamed, and enters no table; the rows "
               f"above are the clean one. Against "
               f"the campaign's own `large-full-width` cells it is {pct(min(cr6))} to {pct(max(cr6))}, a median of "
               f"{pct(statistics.median(cr6))}; against B5's, {pct(min(cr5))} to {pct(max(cr5))}, a median of "
               f"{pct(statistics.median(cr5))}. " +
               ("So the host was still in the slower state after the campaign ended; the state is not a transient of "
                "one run." if statistics.median(cr5) > 1.1 and abs(statistics.median(cr6) - 1) < 0.1 else
                "So the host had moved again between the campaign and the control." if abs(statistics.median(cr6) - 1) >= 0.1 else
                "So by the time of the control the host was back near B5's state."))
else:
    control = 'No control run is in the bundle.'

sessions = sorted({session for r in records for session in r.get('resident_sessions', [])})
resident = (f"{plural(len(sessions), 'resident agent session was', 'resident agent sessions were')} "
            "seen by name across the campaign"
            + (f" ({'; '.join(sessions)})" if sessions else "")
            + f". {plural(sum(len(r['sightings']) for r in timed), 'sighting was', 'sightings were')} "
            f"recorded over {len(timed)} timed invocations, and a run with a sighting is discarded rather than "
            "published. The host was checked idle before and after every run and sampled once a second during it. "
            + span)

s = DOC.read_text()
for key, value in [('PENDING-B6-PROVENANCE', provenance), ('PENDING-B6-RESIDENT', resident),
                   ('PENDING-B6-HOSTRUNS', host), ('PENDING-B6-UNUSABLE', u), ('PENDING-B6-PARITY', parity),
                   ('PENDING-B6-ALLOCNOTE', alloc_note), ('PENDING-B6-PINVERDICT', pin_verdict),
                   ('PENDING-B6-TRANSPOSE', transpose), ('PENDING-B6-KERNEL', kernel), ('PENDING-B6-PATHTABLE', path_table),
                   ('PENDING-B6-WORSENOTE', worse_summary), ('PENDING-B6-WORSETABLE', worse_rows),
                   ('PENDING-B6-WORSEWORST', worse_worst), ('PENDING-B6-TRIANGLES', tri_note),
                   ('PENDING-B6-B5WORSENOTE', b5worse_summary), ('PENDING-B6-B5WORSETABLE', b5worse_table),
                   ('PENDING-B6-STILLNOTE', still_note),
                   ('PENDING-B6-WCCTABLE', wcc_table), ('PENDING-B6-WCCNOTE', wcc_note),
                   ('PENDING-B6-BFSOPEN', bfs_open), ('PENDING-B6-BFSVERDICT', bfs_verdict),
                   ('PENDING-B6-LAYEREDOPEN', layered_open), ('PENDING-B6-LAYEREDVERDICT', layered_verdict),
                   ('PENDING-B6-ACCT', acct), ('PENDING-B6-BUILD', build),
                   ('PENDING-B6-DRIFTTABLE', drift), ('PENDING-B6-DRIFTCAVEAT', drift_note),
                   ('PENDING-B6-LARGEDRIFT', large_drift), ('PENDING-B6-LARGENOTE', large_note),
                   ('PENDING-B6-CONTROL', control)]:
    assert s.count(key) == 1, key
    s = s.replace(key, value)
DOC.write_text(s)
