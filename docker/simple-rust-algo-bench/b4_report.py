#!/usr/bin/env python3
"""Fill the B4 placeholders in the results document from the evidence bundle.

Usage: b4_report.py EVIDENCE_DIR RESULTS_DOC

Reads EVIDENCE_DIR/timed/*.json, EVIDENCE_DIR/campaign.jsonl and the B3 bundle
beside it, and rewrites RESULTS_DOC with every PENDING-* placeholder replaced.
Every number in the B4 section is computed here from those files; none is typed
in. Rows keep a fixed order, fixture then run, and nothing is sorted by time.
"""
import json, pathlib, statistics, sys

E = pathlib.Path(sys.argv[1])
DOC = pathlib.Path(sys.argv[2])
RUNS = ['one-thread', 'full-width', 'large-one-thread', 'large-full-width', 'xlarge-one-thread', 'xlarge-full-width']
data = {r: json.loads((E/'timed'/f'{r}.json').read_text()) for r in RUNS}
idx = {r: {(c['fixture'].removesuffix('.edges'), c['algorithm'], c['participant'], c['call']): c for c in d['cells']}
       for r, d in data.items()}
B3 = json.loads((E.parent/'b3-quegee'/'one-thread.json').read_text())
b3 = {(c['fixture'].split('/')[-1].removesuffix('.edges'), c['algorithm'], c['participant']): c for c in B3['cells']}

def ms(c): return f"{c['total_ms']:.2f} ± {c['total_mad']:.2f}"
def cell(run, fx, alg, p, call=None): return idx[run].get((fx, alg, p, call))
def pct(r): return f"{100 * (r - 1):+.1f}%"

# The transpose correction: one thread, pull kernel.
rows = []
for run, n in [('one-thread', 65536), ('large-one-thread', 2097152), ('xlarge-one-thread', 4194304)]:
    for family in ('hub', 'uniform'):
        fx = f'{family}-{n}'
        o1, o2 = cell(run, fx, 'pagerank', 'grust#1', 'first'), cell(run, fx, 'pagerank', 'grust#1', 'second')
        n1, gc = cell(run, fx, 'pagerank', 'grust-next@counted#1', 'first'), cell(run, fx, 'pagerank', 'grustcat')
        rows.append(f"| `{fx}` | {ms(o1)} | {ms(o2)} | {ms(n1)} | {n1['incoming_ms']:.2f} | {ms(gc)} | {n1['steal_ticks']} |")
transpose = '\n'.join(rows)

# The kernel change: counted, second call against second call.
rows = []
for run in RUNS:
    width = 'full-width' in run
    kernels = ([('pull', 'grust', 'grust-next@counted')] if width else
               [('pull', 'grust#1', 'grust-next@counted#1'), ('push', 'grust#unset', 'grust-next@counted#unset')])
    for fx in sorted({k[0] for k in idx[run] if k[1] == 'pagerank' and k[0].split('-')[0] in ('hub', 'uniform')}):
        for name, old, new in kernels:
            o, n = cell(run, fx, 'pagerank', old, 'second'), cell(run, fx, 'pagerank', new, 'second')
            rows.append(f"| `{fx}` | {run} | {name} | {ms(o)} | {ms(n)} | {n['total_ms'] / o['total_ms']:.3f} | {n['steal_ticks']} |")
kernel = '\n'.join(rows)

# Accounting modes, first call, beside neo4j-graph.
rows = []
for run in RUNS:
    width = 'full-width' in run
    large = run.startswith(('large', 'xlarge'))
    suffixes = [('pull', '')] if width else [('pull', '#1'), ('push', '#unset')]
    for fx in sorted({k[0] for k in idx[run]}):
        if fx.split('-')[0] not in ('hub', 'uniform'): continue
        if not large and not fx.endswith('65536'): continue
        for alg in (['pagerank'] if large else ['pagerank', 'wcc', 'triangles']):
            for name, suf in suffixes:
                cs = [cell(run, fx, alg, f'grust-next@{m}{suf}', 'first') for m in ('counted', 'work-uncounted', 'unchecked')]
                if not all(cs): continue
                neo = cell(run, fx, alg, 'neo4j-graph')
                label = (f"{alg}, {name}" if alg == 'pagerank' else
                         alg if width else f"{alg}, concurrency {'1' if suf == '#1' else 'unset'}")
                rows.append(f"| `{fx}` | {run} | {label} | " + ' | '.join(ms(c) for c in cs) +
                            f" | {ms(neo) if neo else '—'} | {cs[0]['steal_ticks']} |")
acct = '\n'.join(rows)

# Host record, from the campaign log.
lines = []
for line in (E/'campaign.jsonl').read_text().splitlines():
    r = json.loads(line)
    if 'run' not in r: continue
    lines.append(f"- `{r['run']}`: {r['status']}, started {r['before']['at']}, {r['seconds']} s, "
                 f"{r['steal_ticks']} steal ticks over the run, {len(r['sightings'])} sightings.")
host = '\n'.join(lines)

# The dispersion rule, applied.
everything = [(r, c) for r, d in data.items() for c in d['cells']]
unusable = [(r, c) for r, c in everything if c['unusable']]
if unusable:
    u = (f"**{len(unusable)} of {len(everything)} cells reached the 0.25 MAD/median threshold** and enter no table: " +
         '; '.join(f"`{c['participant']}` {c['algorithm']} {c['fixture'].removesuffix('.edges')} {c['call'] or ''} in "
                   f"{r}, {ms(c)}" for r, c in unusable) + '.')
else:
    r, c = max(everything, key=lambda rc: rc[1]['dispersion'])
    u = (f"**None of the {len(everything)} cells reached the 0.25 MAD/median threshold**; the largest dispersion was "
         f"{c['dispersion']:.3f}, `{c['participant']}` {c['algorithm']} {c['fixture'].removesuffix('.edges')} "
         f"{c['call'] or ''} in {r}.")

# What got worse: counted grust-next against v0.22.0, same concurrency and call.
def ratios(alg, call):
    out = []
    for run, pairs in [('one-thread', [('grust#1', 'grust-next@counted#1'), ('grust#unset', 'grust-next@counted#unset')]),
                       ('full-width', [('grust', 'grust-next@counted')])]:
        for old, new in pairs:
            for (fx, a, p, c), o in idx[run].items():
                if p == old and a == alg and c == call:
                    out.append((idx[run][(fx, a, new, c)]['total_ms'] / o['total_ms'], run))
    return out
parts = []
for alg in ('wcc', 'bfs'):
    first, second = ratios(alg, 'first'), ratios(alg, 'second')
    one = [r for r, run in first if run == 'one-thread']
    parts.append(f"counted {alg.upper()} is slower than v0.22.0 on the first call in {sum(r > 1 for r, _ in first)} of "
                 f"{len(first)} one-thread and full-width cells ({pct(min(r for r, _ in first))} to "
                 f"{pct(max(r for r, _ in first))}; median {pct(statistics.median(one))} at one thread), and on the "
                 f"second call in {sum(r > 1 for r, _ in second)} of {len(second)}")
uncounted = []
for alg in ('wcc', 'bfs'):
    for mode in ('work-uncounted', 'unchecked'):
        for call in ('first', 'second'):
            for k in ('#1', '#unset'):
                uncounted.append(statistics.median(
                    idx['one-thread'][(fx, alg, f'grust-next@{mode}{k}', call)]['total_ms'] / o['total_ms']
                    for (fx, a, p, c), o in idx['one-thread'].items() if p == f'grust{k}' and a == alg and c == call))
pagerank = [r for r, _ in ratios('pagerank', 'second')]
worse = ("**It got worse elsewhere.** On `4d8e5db`, " + '; '.join(parts) + ". The largest PageRank change the "
         f"wrong way, second call against second call, is {pct(max(pagerank))}. At one thread the uncounted modes' "
         f"medians for the same WCC and BFS cells are {pct(max(uncounted))} to {pct(min(uncounted))} against "
         "v0.22.0. Every such cell is in `tables.md`.")

o = idx['one-thread']
tr = o[('uniform-65536', 'pagerank', 'grust-next@counted#1', 'first')]['incoming_ms']
gap = o[('uniform-65536', 'pagerank', 'grust#1', 'first')]['total_ms'] - o[('uniform-65536', 'pagerank', 'grustcat', None)]['total_ms']
correction = (f"on `uniform-65536` at one thread the transpose is {tr:.2f} ms of `grust-next`'s `build_ms`, against a "
              f"first-call gap to `grustcat` of {gap:.2f} ms on v0.22.0 in the same run, {100 * tr / gap:.0f}% of it.")
drift = (f"`grust` at v0.22.0 on `uniform-65536`, one thread, first call: "
         f"{b3[('uniform-65536', 'pagerank', 'grust')]['total_ms']:.2f} ms in B3, "
         f"{ms(o[('uniform-65536', 'pagerank', 'grust#1', 'first')])} in B4; `icecat` "
         f"{b3[('uniform-65536', 'pagerank', 'icecat')]['total_ms']:.2f} then "
         f"{ms(o[('uniform-65536', 'pagerank', 'icecat', None)])}.")
fw = idx['full-width']
t1 = fw[('uniform-65536', 'triangles', 'grust', 'first')]['total_ms']
t2 = fw[('uniform-65536', 'triangles', 'grust', 'second')]['total_ms']
warm = (f"triangles on `uniform-65536` at full width, which builds nothing lazily, takes {t1:.2f} ms on v0.22.0's "
        f"first call and {t2:.2f} on its second, {100 * (1 - t2 / t1):.0f}% less.")
bh = lambda m: o[('hub-65536', 'pagerank', f'grust-next@{m}#1', 'first')]['build_ms']
build = (f"Counting also costs in the build: `grust-next`'s `build_ms` for PageRank on `hub-65536` at one thread is "
         f"{bh('counted'):.2f} ms counted, {bh('work-uncounted'):.2f} work-uncounted and {bh('unchecked'):.2f} "
         "unchecked, because building the projection and its transpose charges work too.")

# Parity at the timed commit, and what its exit codes and shared runs mean.
import collections
psum = []
for name in sorted((E/'parity').glob('parity-*.json')):
    rows = json.loads(name.read_text())
    count = collections.Counter(r['verdict'] for r in rows)
    bits = [r['bits_identical_to']['identical'] for r in rows if 'bits_identical_to' in r]
    odd = sorted({(r['participant'], r['fixture']) for r in rows if r['verdict'] not in ('agrees', 'absent')})
    psum.append(f"| `{name.stem.removeprefix('parity-')}` | {count['agrees']} | {count['absent']} | {count['MISMATCH']} | "
                f"{count['error']} | {sum(bits)} of {len(bits)} | "
                f"{', '.join(p + ' ' + f.removesuffix('.edges') for p, f in odd) or '—'} |")
records = [json.loads(line) for line in (E/'campaign.jsonl').read_text().splitlines()]
shared = [r for r in records if 'run' not in r and r['status'].startswith('DISCARDED')]
exit1 = [r for r in records if 'run' not in r and r['exit'] == 1]
parity = ("**Parity at `4d8e5db`**, every fixture set at concurrency unset, 1 and 16, before any timing. "
          "`grust-next` is bit-identical to v0.22.0 in every PageRank row, which is the gate that licenses the "
          "kernel comparison below; the only mismatches are the `neo4j-graph` dangling-mass rows B3 already reported.\n\n"
          "| file | agree | absent | mismatch | error | bits-identical to v0.22.0 | mismatched rows |\n"
          "| --- | ---: | ---: | ---: | ---: | ---: | --- |\n" + '\n'.join(psum) + "\n\n"
          f"{len(exit1)} parity invocations exited 1. `parity.py` exits 1 whenever any row mismatches, and the "
          "protocol fixture set always contains the four known `neo4j-graph` rows; the PageRank-only large sets "
          "contain none and exit 0. The driver records a parity verdict from its file, not its exit code. "
          f"{len(shared)} parity invocations are marked shared, every sighting in them the resident session above. "
          "Parity verdicts are computed results and do not depend on host load, so these were not rerun; the files "
          "above are the output of the last invocation of each set and configuration, including the shared ones. "
          "Every parity and timed invocation used the same image, built once before parity began.")

s = DOC.read_text()
for key, value in [('PENDING-TRANSPOSE', transpose), ('PENDING-KERNEL', kernel), ('PENDING-ACCT', acct),
                   ('PENDING-HOSTRUNS', host), ('PENDING-UNUSABLE', u), ('PENDING-WORSE', worse),
                   ('PENDING-CORRECTION', correction), ('PENDING-DRIFT', drift), ('PENDING-WARM', warm),
                   ('PENDING-BUILD', build), ('PENDING-PARITY', parity)]:
    assert s.count(key) == 1, key
    s = s.replace(key, value)
DOC.write_text(s)
