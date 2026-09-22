#!/usr/bin/env python3
"""Fill the B5 placeholders in the results document from the evidence bundle.

Usage: b5_report.py EVIDENCE_DIR RESULTS_DOC

Reads EVIDENCE_DIR/timed/*.json, EVIDENCE_DIR/parity/*.json,
EVIDENCE_DIR/campaign.jsonl and EVIDENCE_DIR/sources.json, and rewrites
RESULTS_DOC with every PENDING-B5-* placeholder replaced. Every number in the
B5 section is computed here from those files; none is typed in. Rows keep a
fixed order - fixture, then run, then the order the run listed its participants
- and nothing is sorted by time, because a table sorted by time is a ranking.
"""
import collections, json, pathlib, statistics, sys

E = pathlib.Path(sys.argv[1])
DOC = pathlib.Path(sys.argv[2])
RUNS = ['one-thread', 'full-width', 'pinned-one-thread', 'pinned-full-width',
        'large-one-thread', 'large-full-width', 'xlarge-one-thread', 'xlarge-full-width']
data = {r: json.loads((E/'timed'/f'{r}.json').read_text()) for r in RUNS
        if (E/'timed'/f'{r}.json').exists()}
idx = {r: {(c['fixture'].removesuffix('.edges'), c['algorithm'], c['participant'], c['call']): c
           for c in d['cells']} for r, d in data.items()}
# B4's protocol-size runs, for the two open items and the drift table. Never
# mixed into a B5 table: a B4 cell is only ever compared as B4's own figure.
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
def fixtures(run, families=None):
    names = sorted({k[0] for k in idx[run]})
    return [f for f in names if families is None or f.split('-')[0] in families]

# Each run's Grust variants: at one thread both kernels are timed under their
# own concurrency suffix, at full width one is.
def suffixes(run):
    return ['#1', '#unset'] if 'one-thread' in run else ['']
def kernel_name(alg, suffix):
    if alg != 'pagerank': return 'concurrency ' + ('1' if suffix == '#1' else 'unset' if suffix == '#unset' else 'as the run')
    return 'pull' if suffix != '#unset' else 'push'

# --- the allocator artifact, corrected ------------------------------------
# WCC and BFS never read in-arcs. B4 built the transpose for them anyway; the
# +eager rows here are that behaviour, beside the corrected rows and v0.22.0.
rows = []
for run in [r for r in PROTOCOL if r in idx]:
    for fx in fixtures(run):
        for alg in ('wcc', 'bfs'):
            for suffix in suffixes(run):
                old = cell(run, fx, alg, f'grust{suffix}', 'first')
                new = cell(run, fx, alg, f'grust-next@counted{suffix}', 'first')
                eager = cell(run, fx, alg, f'grust-next@counted+eager{suffix}', 'first')
                if not (old and new and eager): continue
                rows.append(f"| `{fx}` | {alg} | {run} | {kernel_name(alg, suffix)} | {ms(old)} | {flt(old)} | "
                            f"{ms(new)} | {flt(new)} | {ms(eager)} | {flt(eager)} | "
                            f"{pct(new['total_ms'] / old['total_ms'])} | {pct(eager['total_ms'] / new['total_ms'])} |")
alloc = '\n'.join(rows)

pairs = [(cell(run, fx, alg, f'grust{s}', 'first'), cell(run, fx, alg, f'grust-next@counted{s}', 'first'),
          cell(run, fx, alg, f'grust-next@counted+eager{s}', 'first'))
         for run in [r for r in PROTOCOL if r in idx] for fx in fixtures(run)
         for alg in ('wcc', 'bfs') for s in suffixes(run)]
pairs = [p for p in pairs if all(p) and all(c['minflt'] is not None for c in p)]
alloc_summary = (
    f"Across the {len(pairs)} WCC and BFS first-call cells at the protocol sizes, the corrected "
    f"`grust-next` takes a median of {statistics.median(n['minflt'] - o['minflt'] for o, n, _ in pairs):+.0f} "
    f"minor page faults against v0.22.0 and the `+eager` row a median of "
    f"{statistics.median(e['minflt'] - n['minflt'] for _, n, e in pairs):+.0f} against the corrected one; "
    f"`+eager` is slower than the corrected row in {sum(e['total_ms'] > n['total_ms'] for _, n, e in pairs)} of "
    f"{len(pairs)} of them, by a median of "
    f"{pct(statistics.median(e['total_ms'] / n['total_ms'] for _, n, e in pairs))}.")

# The pre-registered rule: the published tables stay on the default allocator
# unless the corrected harness still leaves the two Grust builds in different
# allocator states on the same cell. The attribution measured the artifact at
# about 112 to 128 extra minor faults on a first call, so a residual difference
# of a fifth of that is the line, and the number it is judged on is printed.
RESIDUAL_FAULTS = 25
residual = statistics.median(abs(n['minflt'] - o['minflt']) for o, n, _ in pairs)

# --- the allocator pinned, for every participant ---------------------------
rows, moved = [], []
for base, pinned in (('one-thread', 'pinned-one-thread'), ('full-width', 'pinned-full-width')):
    if pinned not in idx: continue
    order = list(data[pinned]['participants'])
    for fx in fixtures(pinned, FAMILIES):
        if not fx.endswith('65536'): continue
        for alg in ('pagerank', 'wcc', 'bfs', 'triangles'):
            for participant in order:
                free, pin = cell(base, fx, alg, participant, None), cell(pinned, fx, alg, participant, None)
                if free is None or pin is None:
                    free = free or cell(base, fx, alg, participant, 'first')
                    pin = pin or cell(pinned, fx, alg, participant, 'first')
                if not (free and pin): continue
                ratio = pin['total_ms'] / free['total_ms']
                moved.append((ratio, participant, alg, fx, base))
                rows.append(f"| `{fx}` | {alg} | {base} | `{participant}` | {ms(free)} | {flt(free)} | "
                            f"{ms(pin)} | {flt(pin)} | {pct(ratio)} |")
pinned_table = '\n'.join(rows)
by_participant = collections.defaultdict(list)
for ratio, participant, *_ in moved: by_participant[participant.split('@')[0].split('#')[0]].append(ratio)
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

# --- the kernel change: v0.22.0 against the commit under test ---------------
def grust_pairs(run):
    """(suffix, v0.22.0 key, grust-next counted key) for the kernels this run timed."""
    return [(s, f'grust{s}', f'grust-next@counted{s}') for s in suffixes(run)]

rows = []
for run in [r for r in RUNS if r in idx and not r.startswith('pinned')]:
    for fx in fixtures(run, FAMILIES):
        for suffix, old, new in grust_pairs(run):
            o, n = cell(run, fx, 'pagerank', old, 'second'), cell(run, fx, 'pagerank', new, 'second')
            if not (o and n): continue
            rows.append(f"| `{fx}` | {run} | {kernel_name('pagerank', suffix)} | {ms(o)} | {ms(n)} | "
                        f"{n['total_ms'] / o['total_ms']:.3f} | "
                        f"{n['steal_ticks']} |")
kernel = '\n'.join(rows)

# --- every cell that got worse ---------------------------------------------
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
    f"{o['steal_ticks']} |" for ratio, fx, alg, run, kn, call, o, n in worse)
worse_summary = (f"{len(worse)} of the {compared} counted cells with a v0.22.0 counterpart are slower on "
                 f"`ca68900`, by {pct(min(w[0] for w in worse))} to {pct(max(w[0] for w in worse))}." if worse
                 else f"None of the {compared} counted cells with a v0.22.0 counterpart is slower on `ca68900`.")

# --- the two open items ------------------------------------------------------
rows = []
for run in [r for r in PROTOCOL if r in idx]:
    for fx in fixtures(run, FAMILIES):
        for suffix in suffixes(run):
            o = cell(run, fx, 'bfs', f'grust{suffix}', 'first')
            n = cell(run, fx, 'bfs', f'grust-next@counted{suffix}', 'first')
            b = b4.get((run, fx, 'bfs', f'grust-next@counted{suffix}', 'first'))
            bo = b4.get((run, fx, 'bfs', f'grust{suffix}', 'first'))
            if not (o and n): continue
            was = pct(b['total_ms'] / bo['total_ms']) if b and bo else '—'
            rows.append(f"| `{fx}` | {run} | {kernel_name('bfs', suffix)} | {ms(o)} | {flt(o)} | {ms(n)} | "
                        f"{flt(n)} | {pct(n['total_ms'] / o['total_ms'])} | {was} |")
bfs_open = '\n'.join(rows)

rows = []
for run in [r for r in PROTOCOL if r in idx]:
    for fx in [f for f in fixtures(run) if f.startswith('layered')]:
        for suffix in suffixes(run):
            for call in ('first', 'second'):
                o = cell(run, fx, 'pagerank', f'grust{suffix}', call)
                n = cell(run, fx, 'pagerank', f'grust-next@counted{suffix}', call)
                if not (o and n): continue
                rows.append(f"| `{fx}` | {run} | {kernel_name('pagerank', suffix)} | {call} | {ms(o)} | {ms(n)} | "
                            f"{pct(n['total_ms'] / o['total_ms'])} | {o['steal_ticks']} |")
layered_open = '\n'.join(rows)

# --- accounting modes, first call, beside neo4j-graph -----------------------
rows = []
for run in [r for r in RUNS if r in idx and not r.startswith('pinned')]:
    large = run.startswith(('large', 'xlarge'))
    for fx in fixtures(run, FAMILIES):
        if not large and not fx.endswith('65536'): continue
        for alg in (['pagerank'] if large else ['pagerank', 'wcc', 'triangles']):
            for suffix in suffixes(run):
                cs = [cell(run, fx, alg, f'grust-next@{m}{suffix}', 'first')
                      for m in ('counted', 'work-uncounted', 'unchecked')]
                if not all(cs): continue
                neo = cell(run, fx, alg, 'neo4j-graph')
                rows.append(f"| `{fx}` | {run} | {alg}, {kernel_name(alg, suffix)} | " +
                            ' | '.join(ms(c) for c in cs) + f" | {ms(neo)} | {cs[0]['steal_ticks']} |")
acct = '\n'.join(rows)

o = idx['one-thread']
bh = lambda m: o[('hub-65536', 'pagerank', f'grust-next@{m}#1', 'first')]['build_ms']
build = (f"Counting also costs in the build: `grust-next`'s `build_ms` for PageRank on `hub-65536` at one thread "
         f"is {bh('counted'):.2f} ms counted, {bh('work-uncounted'):.2f} work-uncounted and {bh('unchecked'):.2f} "
         "unchecked, because building the projection and its transpose charges work too.")

# --- host record, dispersion, parity, drift ---------------------------------
lines = []
for line in (E/'campaign.jsonl').read_text().splitlines():
    r = json.loads(line)
    if 'run' not in r: continue
    lines.append(f"- `{r['run']}`: {r['status']}, started {r['before']['at']}, {r['seconds']} s, "
                 f"{r['steal_ticks']} steal ticks over the run, {len(r['sightings'])} sightings, "
                 f"{len(r.get('resident_sessions', []))} resident agent sessions.")
host = '\n'.join(lines)

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
# The bits gate names v0.22.0 and the three accounting modes; the `+eager`
# variant differs from counted only in where the transpose is built, and its
# digests are checked here from the same parity files rather than assumed.
eager_same, eager_rows = 0, 0
for name in sorted((E/'parity').glob('parity-*.json')):
    prows = json.loads(name.read_text())
    base = {r['fixture']: r for r in prows if r['participant'] == 'grust' and r['algorithm'] == 'pagerank'}
    for r in prows:
        if r['participant'] != 'grust-next@counted+eager' or r['algorithm'] != 'pagerank': continue
        other = base.get(r['fixture'])
        if other is None or 'found' not in r: continue
        eager_rows += 1
        eager_same += (r['found']['scores_digest'] == other['found']['scores_digest']
                       and r['iterations'] == other['iterations'])

records = [json.loads(line) for line in (E/'campaign.jsonl').read_text().splitlines()]
shared = [r for r in records if 'run' not in r and r['status'].startswith('DISCARDED')]
exit1 = [r for r in records if 'run' not in r and r.get('exit') == 1]
parity = ("| file | agree | absent | mismatch | error | bits-identical to v0.22.0 | mismatched rows |\n"
          "| --- | ---: | ---: | ---: | ---: | ---: | --- |\n" + '\n'.join(psum) + "\n\n"
          f"{len(exit1)} parity invocations exited 1: `parity.py` exits 1 whenever any row mismatches, and the "
          "protocol fixture set always contains the four known `neo4j-graph` dangling-mass rows; the "
          "PageRank-only large sets contain none and exit 0. The driver takes its verdict from the file, not "
          f"the exit code. {len(shared)} parity invocations are marked shared.\n\n"
          f"The `--bits-identical` gate names v0.22.0 and the three accounting modes. The `+eager` variant "
          f"differs from `grust-next@counted` only in where the transpose is built, so its rows are compared "
          f"with v0.22.0's in the same parity files after the fact: its PageRank digest and iteration count "
          f"equal v0.22.0's in {eager_same} of {eager_rows} rows.")

sources = json.loads((E/'sources.json').read_text())
image = json.loads((E/'receipts'/'image.json').read_text()) if (E/'receipts'/'image.json').exists() else {}
provenance = (f"Grust `{sources['grust']['commit'][:7]}` (v0.22.0) as `grust`, Grust "
              f"`{sources['grust_next']['commit'][:7]}` as `grust-next`, Icecat "
              f"`{sources['icecat']['commit'][:8]}`, this harness at `{sources['bench']['commit'][:7]}`, image "
              f"`{image.get('tag', 'simple-rust-algo-bench:b5')}`, built on the host from clean trees.")

def b5_b4(fx, alg, participant, call, run='one-thread'):
    return idx[run].get((fx, alg, participant, call)), b4.get((run, fx, alg, participant, call))
drift_rows = []
for participant, call in (('grust#1', 'first'), ('grust#unset', 'first'), ('icecat', 'first'),
                          ('grustcat', 'first'), ('neo4j-graph', 'first'), ('icebug', 'first')):
    for fx in ('hub-65536', 'uniform-65536'):
        for alg in ('pagerank', 'wcc'):
            a, b = b5_b4(fx, alg, participant, call if participant.startswith('grust#') else None)
            if not (a and b): continue
            drift_rows.append(f"| `{fx}` | {alg} | `{participant}` | {ms(b)} | {ms(a)} | "
                              f"{pct(a['total_ms'] / b['total_ms'])} |")
drift = '\n'.join(drift_rows)

decision = (
    f"**The decision, by the rule fixed before the runs.** Over the same {len(pairs)} WCC and BFS first-call "
    f"cells, the median difference in minor page faults between v0.22.0 and the corrected `grust-next` is "
    f"{residual:.0f}, against the {RESIDUAL_FAULTS} that the rule set as the line and the 112 to 128 the "
    f"attribution measured for the artifact itself. " +
    (f"The two builds are therefore in the same allocator state on the same cell, and the published tables are "
     f"the default-allocator runs: glibc's default is what every participant's users have, and none of these "
     f"projects sets a tunable. The pinned runs above stay as a labelled probe, and they also show that the "
     f"threshold is not a Grust-specific effect — it moves participants that contain no Grust at all."
     if residual <= RESIDUAL_FAULTS else
     f"That is above the line, so the first-call rows would be contaminated on the default allocator, and the "
     f"published tables are the pinned runs; the campaign was rerun pinned at every size."))

# Agent sessions, recorded rather than reconstructed.
sessions = sorted({session for r in records for session in r.get('resident_sessions', [])})
timed = [r for r in records if 'run' in r]
resident = (f"{len(sessions)} resident agent sessions were seen by name across the campaign"
            + (f" ({'; '.join(sessions)})" if sessions else "")
            + f". {sum(len(r['sightings']) for r in timed)} sightings were recorded over "
            f"{len(timed)} timed invocations, and a run with a sighting is discarded rather than published. "
            f"The host was checked idle before and after every run and sampled once a second during it.")

s = DOC.read_text()
for key, value in [('PENDING-B5-PROVENANCE', provenance), ('PENDING-B5-HOSTRUNS', host),
                   ('PENDING-B5-UNUSABLE', u), ('PENDING-B5-PARITY', parity),
                   ('PENDING-B5-ALLOC', alloc), ('PENDING-B5-ALLOCNOTE', alloc_summary),
                   ('PENDING-B5-PINNED', pinned_table), ('PENDING-B5-PINVERDICT', pin_verdict),
                   ('PENDING-B5-TRANSPOSE', transpose), ('PENDING-B5-KERNEL', kernel),
                   ('PENDING-B5-WORSENOTE', worse_summary), ('PENDING-B5-WORSE', worse_rows),
                   ('PENDING-B5-BFSOPEN', bfs_open), ('PENDING-B5-LAYEREDOPEN', layered_open),
                   ('PENDING-B5-PINDECISION', decision), ('PENDING-B5-RESIDENT', resident),
                   ('PENDING-B5-ACCT', acct), ('PENDING-B5-BUILD', build), ('PENDING-B5-DRIFT', drift)]:
    assert s.count(key) == 1, key
    s = s.replace(key, value)
DOC.write_text(s)
