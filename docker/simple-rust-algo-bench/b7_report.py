#!/usr/bin/env python3
"""The PageRank-precision campaigns' tables, estimate and results section,
all computed from evidence files. B7 first; `--campaign b8` and `--campaign b9`
run the same plan on later commits of the kernel stack.

    b7_report.py tables BUNDLE_DIR        Markdown for every timed run
    b7_report.py estimate B6_BUNDLE_DIR   expected duration from B6's walls
    b7_report.py section BUNDLE_DIR       the results document's results section
    b7_report.py --campaign b8 section BUNDLE_DIR   the same for B8, with B7 beside it
    b7_report.py --campaign b9 section BUNDLE_DIR   the same for B9
    b7_report.py --campaign b8 hosts --timed QUEGEE_DIR EIGEN_DIR LAKECAT_DIR   the shape on other hosts

`regenerate-check.sh` beside this file regenerates every campaign's tables.md
and results section and `cmp`s them against what is committed; run it before
committing anything that touches a bundle, this generator or the results
document.

A campaign in BUNDLED_PREVIOUS gets three further subsections, each computed
from its own bundle and the named one: `grust-next@unchecked+f32` against
`neo4j-graph` one sweep at a time, what work accounting costs per sweep in each
campaign, and the unchanged-code table that says why no absolute of one
campaign is set beside an absolute of another. Every ratio in them is formed
from two cells of one campaign; no cell of one is ever divided by a cell of
another.

`tables` reads BUNDLE_DIR/timed/<campaign>-*.json (or the files given with
--timed) and BUNDLE_DIR/parity/parity-<campaign>-*.json, and prints, per run and fixture, one
row per cell with the iteration count beside the total and the per-iteration
time, then one table per fixture with every participant's iteration count side
by side across the runs, so a reader sees at once whether the `+f32` rows
stopped at the count `neo4j-graph` stopped at. Where two counts differ, the
text under the table says that the per-iteration figure is the comparable one
and the total is not. Rows keep the order the run listed its participants and
nothing is sorted by time.

`estimate` is the basis of the campaign's length. For every B7 cell it takes
the B6 sample walls of the same participant on the same fixture at the same
kernel, and for a `+f32` row the f64 row of the same variant, since B6 has no
f32 Grust rows; that assumption is printed with the figure. The per-run
overhead outside the samples - process start, the ABBA bookkeeping - is B6's
own ratio of run seconds to summed walls. Three totals are printed: the plan
as written, the plan with v0.22.0's push loop added back, and the plan with no
v0.22.0 row at all, so the choice among them can be read off rather than taken
on trust.
"""
import argparse, collections, json, os, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import campaign

F32 = '+f32'
CAMPAIGN = 'b7'   # set from --campaign; the prefix of every output file
PREVIOUS = {'b7': 'b6', 'b8': 'b7', 'b9': 'b8'}
# The nearest campaign that has a bundle, for readings formed as a ratio inside
# each campaign separately. B8 ran on quegee and was never bundled, so B9's
# nearest bundled campaign is B7; nothing here divides a cell of one campaign by
# a cell of another, and the entry exists so that the document says which bundle
# a printed figure came out of.
BUNDLED_PREVIOUS = {'b9': 'b7'}
COMPARED = ['neo4j-graph', 'grust-next@unchecked+f32', 'grust-next@counted+f32', 'grust-next@unchecked', 'grust-next@counted']

def fmt(value, digits=3):
    return '-' if value is None else f'{value:.{digits}f}'

def kernel(participant, run):
    """Which PageRank kernel a Grust row ran: the `#` suffix says, else the run's width."""
    if base(participant).split('@')[0].split('+')[0] not in ('grust', 'grust-next'): return ''
    if participant.endswith('#unset'): return 'push'
    return 'pull'

def base(participant):
    return participant.split('#')[0]

def load_timed(paths):
    """The run files, in the plan's order, never in the file system's."""
    order = list(campaign.PLANS['b7']['runs'])
    reports = []
    for path in paths:
        report = json.loads(pathlib.Path(path).read_text())
        report['_file'] = pathlib.Path(path).name
        reports.append(report)
    def rank(report):
        name = report['label'].split('-', 1)[1] if report['label'].startswith('b') else report['label']
        return order.index(name) if name in order else len(order)
    return sorted(reports, key=rank)

def cell_rows(report):
    order = list(report['participants'])
    return sorted(report['cells'], key=lambda c: (c['fixture'], order.index(c['participant']), c['call'] or ''))

def tables(a):
    paths = a.timed or sorted((a.bundle/'timed').glob(f'{CAMPAIGN}-*.json'))
    if not paths: raise SystemExit(f'no {CAMPAIGN.upper()} timed runs under {a.bundle}/timed')
    reports = load_timed(paths)
    print(f'# {CAMPAIGN.upper()} tables\n')
    print('Every PageRank cell, with its iteration count beside its total and its per-iteration time. '
          'The precision column is what the participant declared in its receipt. '
          'Two cells whose iteration counts differ did not do the same work, and their totals are not '
          'compared; their per-iteration times are. A row marked UNUSABLE is printed with its numbers and '
          'enters no comparison.\n')
    for report in reports:
        pinned = report.get('glibc_tunables')
        print(f"## `{report['_file']}`: {report['label']}\n")
        print(f"workers {report['workers']}, concurrency {report['concurrency']}, "
              f"allocator {'pinned: ' + pinned if pinned else 'glibc default, not pinned'}, "
              f"{report['warmups']} warmup + {report['repeats']} repeats, "
              f"steal over the run {report['steal_ticks_over_run']} ticks, {report['seconds']} s, "
              f"unusable at MAD/median >= {report['unusable_dispersion']}\n")
        if report['skipped']:
            print('Not timed (no agreeing parity row):', ', '.join(
                f"`{s['participant']}` {s['fixture'].removesuffix('.edges')}" for s in report['skipped']), '\n')
        print('| fixture | participant | precision | accounting | kernel | call | iters | converged | residual | '
              'total ms | MAD | MAD/median | per iter ms | build ms | incoming ms | minflt | steal | usable |')
        print('| --- | --- | --- | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: '
              '| ---: | --- |')
        for c in cell_rows(report):
            residual, converged = c.get('residual'), c.get('converged')
            print(f"| {c['fixture'].removesuffix('.edges')} | `{c['participant']}` | {c.get('precision') or ''} | "
                  f"{c['accounting'] or ''} | {kernel(c['participant'], report['label'])} | {c['call'] or ''} | "
                  f"{c['iterations'] or '-'} | {'' if converged is None else ('yes' if converged else '**NO**')} | "
                  f"{'-' if residual is None else f'{residual:.3g}'} | "
                  f"{fmt(c['total_ms'])} | {fmt(c['total_mad'])} | {fmt(c['dispersion'])} | "
                  f"{fmt(c['per_iteration_ms'], 4)} | {fmt(c['build_ms'], 2)} | {fmt(c['incoming_ms'], 2)} | "
                  f"{fmt(c.get('minflt'), 0)} | {c['steal_ticks']} | {'**UNUSABLE**' if c['unusable'] else 'yes'} |")
        print()
    side_by_side(reports)
    parity_summary(a)

def side_by_side(reports):
    """Iteration counts across runs, one column per participant, one row per fixture and run."""
    print('## Iteration counts side by side\n')
    print('Each cell is the iteration count the participant reported for that fixture in that run (a Grust '
          'row reports the same count on both calls, so one is shown). `neo4j-graph` first, then the `+f32` '
          'rows, which are the rows that could stop where it stops, then the f64 rows. Where a count differs '
          'from `neo4j-graph`\'s in the same row, the two totals were not the same number of sweeps over the '
          'arcs, and only the per-iteration column of the table above compares them.\n')
    columns = []
    for report in reports:
        for c in report['cells']:
            if c['participant'] not in columns: columns.append(c['participant'])
    seen = list(columns)
    columns.sort(key=lambda p: (not p.startswith('neo4j-graph'), F32 not in p, seen.index(p)))
    print('| fixture | run | ' + ' | '.join(f'`{p}`' for p in columns) + ' |')
    print('| --- | --- | ' + ' | '.join('---:' for _ in columns) + ' |')
    findings = []
    for report in reports:
        by = collections.defaultdict(dict)
        for c in report['cells']:
            by[c['fixture']].setdefault(c['participant'], c['iterations'])
        for fixture in sorted(by):
            counts = by[fixture]
            print(f"| {fixture.removesuffix('.edges')} | {report['label']} | "
                  + ' | '.join(str(counts.get(p, '-')) if counts.get(p) is not None else '-' for p in columns) + ' |')
            anchor = counts.get('neo4j-graph')
            for p, n in counts.items():
                if F32 in p and anchor is not None and n is not None:
                    findings.append((fixture, report['label'], p, n, anchor))
    print()
    same = [f for f in findings if f[3] == f[4]]
    differ = [f for f in findings if f[3] != f[4]]
    if findings:
        print(f'Of {len(findings)} `+f32` cells, {len(same)} stopped at the same count as `neo4j-graph` on the '
              f'same fixture in the same run and {len(differ)} did not.', end=' ')
        if differ:
            print('For those, the totals are not comparable and the per-iteration times are:')
            print()
            for fixture, label, p, n, anchor in differ:
                print(f"- {fixture.removesuffix('.edges')}, {label}: `{p}` stopped at {n}, `neo4j-graph` at {anchor}.")
        else:
            print('Their totals are comparable as wholes.')
        print()

def parity_summary(a):
    paths = sorted((a.bundle/'parity').glob(f'parity-{CAMPAIGN}-*.json')) if a.bundle else []
    if not paths: return
    print('## Parity\n')
    print(f'Every row parity produced for the participants {CAMPAIGN.upper()} times, PageRank only. `vector` is how many of '
          'the n scores were bit-identical to the reference\'s f64 scores and the largest distance, in f64 '
          'ulps and in absolute terms; for an f32 row, widened to f64, the ulp figure is meaningless and the '
          'absolute one is the distance. It is recorded and not gated, as it is for every row. '
          '`bits` is the bit gate: f64 builds against v0.22.0, `+f32` builds against their counted row.\n')
    print('| file | fixture | participant | concurrency | verdict | iters | residual | vector | bits | detail |')
    print('| --- | --- | --- | --- | --- | ---: | ---: | --- | --- | --- |')
    for path in paths:
        for r in json.loads(path.read_text()):
            if r['algorithm'] != 'pagerank': continue
            v = r.get('vector_against_reference')
            vector = f"{v['identical']}/{v['of']}, max {v['max_ulps']} f64 ulps, {v['max_abs']:.3g} abs" if v else ''
            b = r.get('bits_identical_to')
            bits = f"{'same as' if b['identical'] else 'DIFFERS from'} `{b['participant']}`" if b else ''
            residual = r.get('residual')
            print(f"| {path.name} | {r['fixture'].removesuffix('.edges')} | `{r['participant']}` | "
                  f"{'unset' if r['concurrency'] is None else r['concurrency']} | {r['verdict']} | "
                  f"{r.get('iterations') or '-'} | {'-' if residual is None else f'{residual:.3g}'} | "
                  f"{vector} | {bits} | {r.get('detail', '')} |")
    print()

def walls(report):
    """Mean wall per sample for every (fixture, variant) PageRank cell of a B6 run, and the run's overhead."""
    per = collections.defaultdict(list)
    for s in report['samples']:
        if s['algorithm'] != 'pagerank': continue
        per[(os.path.basename(s['fixture']), s['variant'])].append(
            s['parse_ms'] + s['build_ms'] + s['kernel_ms'] + s.get('kernel_second_ms', 0) + s.get('materialise_ms', 0))
    total = sum(sum(v) for v in per.values())
    group = sum(g['seconds'] for g in report['groups'] if g['algorithm'] == 'pagerank')
    return {k: sum(v) / len(v) / 1e3 for k, v in per.items()}, (group / (total / 1e3) if total else 1.0)

def estimate(a):
    plan = campaign.PLANS['b7']
    samples = 1 + 5   # one warmup and five repeats, as B6 and B7
    print(f'B7 duration estimate from {a.bundle}\n')
    print('Basis: for each B7 cell, B6\'s mean wall per sample (parse + build + both calls + materialise) of the '
          'same participant on the same fixture at the same kernel, times six samples; a `+f32` row is taken at '
          'its f64 row\'s wall, because B6 has no f32 Grust row - so an f32 kernel that is faster per sweep and '
          'stops at more sweeps could land on either side of this. Each run is scaled by B6\'s own ratio of run '
          'seconds to summed walls for that run, which is the harness overhead the samples do not contain.\n')
    print('| run | participants | B6 overhead | as planned | + `grust#unset` | no v0.22.0 row |')
    print('| --- | ---: | ---: | ---: | ---: | ---: |')
    totals = collections.Counter()
    for run, spec in plan['runs'].items():
        report = json.loads((a.bundle/'timed'/f'{run}.json').read_text())
        wall, overhead = walls(report)
        fixtures = sorted({f for f, _ in wall if f.split('-')[0] in spec['families']})
        def seconds(participants):
            total = 0.0
            for fixture in fixtures:
                for p in participants:
                    proxy = p.replace(F32, '')
                    if (fixture, proxy) not in wall:
                        raise SystemExit(f'{run}: B6 has no {proxy} on {fixture} to stand in for {p}')
                    total += wall[(fixture, proxy)] * samples
            return total * overhead
        planned = seconds(spec['participants'])
        with_push = seconds(spec['participants'] + (['grust#unset'] if 'one-thread' in run else []))
        without = seconds([p for p in spec['participants'] if base(p) != 'grust'])
        totals.update(planned=planned, with_push=with_push, without=without)
        print(f"| {run} | {len(spec['participants'])} | {overhead:.3f} | {planned / 60:.1f} min | "
              f"{with_push / 60:.1f} min | {without / 60:.1f} min |")
    print(f"| **timed total** | | | **{totals['planned'] / 60:.0f} min** | **{totals['with_push'] / 60:.0f} min** | "
          f"**{totals['without'] / 60:.0f} min** |")
    print()
    parity = [json.loads(line) for line in (a.bundle/'campaign.jsonl').read_text().splitlines()]
    parity_seconds = sum(r.get('seconds') or 0 for r in parity if r.get('name', '').startswith('parity-'))
    b6_participants = len(campaign.PARITY_PARTICIPANTS)
    b7_participants = len(plan['parity_participants'])
    print(f"Parity, as a bound: B6's nine parity invocations took {parity_seconds / 60:.0f} min for "
          f"{b6_participants} participants and four algorithms, including the Python reference for each; "
          f"B7 runs {b7_participants} participants and PageRank alone, so at most about "
          f"{parity_seconds / 60 * b7_participants / b6_participants:.0f} min, less where the reference cache "
          "from the same work directory is reused.")

def parity_rows(bundle):
    for path in sorted((bundle/'parity').glob(f'parity-{CAMPAIGN}-*.json')):
        yield path, [r for r in json.loads(path.read_text()) if r['algorithm'] == 'pagerank']

def section(a):
    """The B7 results section: every figure computed from the bundle, none typed."""
    reports = load_timed(sorted((a.bundle/'timed').glob(f'{CAMPAIGN}-*.json')))
    # PageRank is the campaign; any other algorithm's cell has no count to show.
    for rep in reports: rep['cells'] = [c for c in rep['cells'] if c['algorithm'] == 'pagerank']
    # `campaign.jsonl` in a bundle, `campaign-<name>.jsonl` in the work directory it came from.
    record = next(p for p in (a.bundle/'campaign.jsonl', a.bundle/f'campaign-{CAMPAIGN}.jsonl') if p.exists())
    log = [json.loads(l) for l in record.read_text().splitlines()]
    sources = json.loads((a.bundle/'sources.json').read_text())
    manifest = json.loads((a.bundle/'fixtures-manifest.json').read_text())
    image = json.loads((a.bundle/'receipts'/'image.json').read_text())
    timed_log = [r for r in log if 'run' in r]
    parity_log = [r for r in log if 'run' not in r]
    residents = sorted({s for r in log for s in r.get('resident_sessions', [])})
    print(f'## {CAMPAIGN.upper()}: results\n')
    print(f"One host, quegee, {timed_log[0]['before']['at'][:10] if timed_log else '—'}. "
          f"Grust `{sources['grust']['commit'][:7]}` (v0.22.0) as `grust`, Grust `{sources['grust_next']['commit'][:7]}` "
          f"as `grust-next`, Icecat `{sources['icecat']['commit'][:8]}`, this harness at `{sources['bench']['commit'][:7]}`, "
          f"image `{image['tag']}`, built on the host from commits staged by `git archive`. The "
          f"{len(manifest['fixtures'])} fixtures are SHA-256-identical to B6's: `identical_to_b6` is "
          f"{str(manifest['identical_to_b6']).lower()} in the manifest. One warmup, five repeats, counterbalanced, parity "
          "gated at every concurrency. **Every cell of every run, with its iteration count, its residual, its steal, "
          f"its dispersion and its usability, is in `simple-rust-algo-bench-evidence/{CAMPAIGN}-quegee/tables.md`**, generated "
          "from the run files by `b7_report.py tables`; the tables below select from it and add nothing to it. Times "
          "are milliseconds, median ± MAD, of the kernel call alone; per-iteration is that median divided by the "
          "iteration count the participant reported. Steal is ticks over that cell's group.\n")
    sightings = sum(len(r.get('sightings', [])) for r in timed_log)
    print(f"**Host conditions.** {len(residents)} resident agent session{'' if len(residents) == 1 else 's'} "
          f"{'was' if len(residents) == 1 else 'were'} seen by name across the campaign ({'; '.join(residents) or 'none'}). "
          f"{sightings} sightings were recorded over {len(timed_log)} timed invocations, and a run with a sighting is "
          "discarded rather than published. The host was checked idle before and after every run and sampled once a "
          f"second during it. The timed campaign ran from {timed_log[0]['before']['at'] if timed_log else '—'} to "
          f"{timed_log[-1]['after']['at'] if timed_log and 'after' in timed_log[-1] else '—'}, {len(timed_log)} runs, "
          "in the order listed.\n")
    for r in timed_log:
        print(f"- `{r['run']}`: {r['status']}, started {r['before']['at']}, {r.get('seconds')} s, "
              f"{r.get('steal_ticks')} steal ticks over the run, {len(r.get('sightings', []))} sightings, "
              f"{len(r.get('resident_sessions', []))} resident agent session{'' if len(r.get('resident_sessions', [])) == 1 else 's'}.")
    print()
    cells = [c for rep in reports for c in rep['cells']]
    unusable = [c for c in cells if c['unusable']]
    worst = max(cells, key=lambda c: c['dispersion'] or 0) if cells else None
    if worst:
        print(f"**{len(unusable)} of the {len(cells)} cells reached the {reports[0]['unusable_dispersion']} MAD/median "
              f"threshold**; the largest dispersion was {worst['dispersion']:.3f}, `{worst['participant']}` "
              f"{worst['fixture'].removesuffix('.edges')}{' ' + worst['call'] if worst['call'] else ''} in "
              f"{worst['participant'] and next(rep['label'] for rep in reports if worst in rep['cells'])}."
              + (' Unusable cells are printed and marked in `tables.md` and enter no table here.' if unusable else '') + '\n')
    skipped = [(rep['label'], s) for rep in reports for s in rep['skipped']]
    if skipped:
        print('Not timed, having no agreeing parity row: ' + ', '.join(f"`{s['participant']}` {s['fixture'].removesuffix('.edges')} in {label}" for label, s in skipped) + '.\n')
    print('**Parity at the commit under test**, hub and uniform at every size, PageRank, at concurrency unset, 1 and 16, '
          'before any timing. The f64 builds must return v0.22.0\'s vector bit for bit; the `+f32` builds must return '
          'their counted row\'s. A row that reports `converged: false` is `not converged`, its own verdict, and is never '
          'timed.\n')
    print('| file | agrees | mismatch | error | not converged | f64 bits-identical to v0.22.0 | `+f32` unchecked identical to counted | rows not agreeing |')
    print('| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |')
    for path, rows in parity_rows(a.bundle):
        count = collections.Counter(r['verdict'] for r in rows)
        f64 = [r for r in rows if 'bits_identical_to' in r and F32 not in r['participant']]
        f32 = [r for r in rows if 'bits_identical_to' in r and F32 in r['participant']]
        odd = [f"`{r['participant']}` {r['fixture'].removesuffix('.edges')}" for r in rows if r['verdict'] != 'agrees']
        print(f"| `{path.name.removeprefix(f'parity-{CAMPAIGN}-').removesuffix('.json')}` | {count['agrees']} | {count['MISMATCH']} | "
              f"{count['error']} | {count['not converged']} | "
              f"{sum(r['bits_identical_to']['identical'] for r in f64)} of {len(f64)} | "
              f"{sum(r['bits_identical_to']['identical'] for r in f32)} of {len(f32)} | {', '.join(odd) or '—'} |")
    print()
    exits = collections.Counter((r['status'], r.get('exit')) for r in parity_log)
    print(f"{sum(1 for r in parity_log if r.get('exit'))} parity invocations exited non-zero; "
          f"{sum(1 for r in parity_log if r['status'] != 'clean')} are marked other than clean "
          f"({', '.join(f'{r['name']}: {r['status']}' for r in parity_log if r['status'] != 'clean') or 'none'}).\n")
    print('**Where each participant stopped.** The iteration count every participant reported, per fixture and run. '
          '`neo4j-graph` sums its f32 residual in f64 and stops at residual < tolerance; Grust at either precision '
          'sums its residual in f64 and stops at residual <= tolerance; every row here ran at tolerance 1e-8 and a '
          'cap of 100 iterations. A Grust row reports the same count on both calls, so one is shown.\n')
    columns = []
    for rep in reports:
        for c in rep['cells']:
            if c['participant'] not in columns: columns.append(c['participant'])
    seen = list(columns)
    columns.sort(key=lambda p: (not p.startswith('neo4j-graph'), F32 not in p, seen.index(p)))
    print('| fixture | run | ' + ' | '.join(f'`{p}`' for p in columns) + ' |')
    print('| --- | --- | ' + ' | '.join('---:' for _ in columns) + ' |')
    findings = []
    for rep in reports:
        by = collections.defaultdict(dict)
        for c in rep['cells']: by[c['fixture']].setdefault(c['participant'], c['iterations'])
        for fixture in sorted(by):
            counts = by[fixture]
            print(f"| `{fixture.removesuffix('.edges')}` | {rep['label'].removeprefix(f'{CAMPAIGN}-')} | "
                  + ' | '.join(str(counts[p]) if counts.get(p) is not None else '—' for p in columns) + ' |')
            for p, n in counts.items():
                if F32 in p and counts.get('neo4j-graph') is not None and n is not None:
                    findings.append((n == counts['neo4j-graph'], n, counts['neo4j-graph']))
    print()
    same = sum(1 for f in findings if f[0])
    print(f"Of {len(findings)} `+f32` cells, {same} stopped at the count `neo4j-graph` stopped at on the same fixture in "
          f"the same run and {len(findings) - same} did not. "
          + ("Where the counts differ the two totals are not the same number of sweeps over the arcs; the per-iteration "
             "figure is the one that compares them, and it is a comparison of one sweep's cost, not of the time to an "
             "answer at this tolerance, which is the total." if len(findings) - same else
             "Their totals are comparable as wholes.") + '\n')
    print('### `neo4j-graph` beside Grust at f32, and Grust at f64 beside both\n')
    print('Total and per-iteration time of the kernel call, with the count. For `grust-next` the second call is shown, '
          'which has the transpose cached and runs on warm caches, and the first call in `tables.md`; `neo4j-graph` '
          'times one call on a fresh build. `counted` charges work to a shared meter and observes cancellation; '
          '`unchecked` does neither and is the like-for-like row against `neo4j-graph`, which performs no accounting. '
          'Nothing in this table is a ratio; a reader who forms one takes the boundary with it.\n')
    def show(c):
        if not c or c['per_iteration_ms'] is None: return '—'
        return f"{c['total_ms']:.2f} ± {c['total_mad']:.2f} / {c['per_iteration_ms']:.3f} / {c['iterations']}"
    for rep in reports:
        idx = {(c['fixture'], c['participant'], c['call']): c for c in rep['cells']}
        suffixes = ['#1', '#unset'] if 'one-thread' in rep['label'] else ['']
        print(f"**{rep['label'].removeprefix(f'{CAMPAIGN}-')}** (workers {rep['workers']}), cells as total ms ± MAD / per-iteration ms / iterations:\n")
        print('| fixture | kernel | `neo4j-graph` f32 | `grust-next@unchecked+f32` | `grust-next@counted+f32` | `grust-next@unchecked` f64 | `grust-next@counted` f64 | `grust` v0.22.0 f64 | steal |')
        print('| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |')
        for fixture in sorted({c['fixture'] for c in rep['cells']}):
            for s in suffixes:
                n = idx.get((fixture, 'neo4j-graph', None))
                row = [idx.get((fixture, f'grust-next@unchecked+f32{s}', 'second')), idx.get((fixture, f'grust-next@counted+f32{s}', 'second')),
                       idx.get((fixture, f'grust-next@unchecked{s}', 'second')), idx.get((fixture, f'grust-next@counted{s}', 'second')),
                       idx.get((fixture, f'grust{s}', 'second'))]
                if not any(row): continue
                steal = next((c['steal_ticks'] for c in row if c), '—')
                print(f"| `{fixture.removesuffix('.edges')}` | {'push' if s == '#unset' else 'pull'} | {show(n) if s != '#unset' else '— (push is sequential by construction; neo4j-graph has no such kernel)'} | "
                      + ' | '.join(show(c) for c in row) + f" | {steal} |")
        print()
    if PREVIOUS[CAMPAIGN] != 'b6': beside_previous(a, reports)
    unchanged_against_previous(a, reports)
    if CAMPAIGN in BUNDLED_PREVIOUS:
        like_for_like(reports)
        accounting_cost(a, reports)
        host_between_campaigns(a, reports)


def suffixes_for(name):
    """The kernel suffixes a run carries: one-thread runs time the push loop too."""
    return ['#1', '#unset'] if 'one-thread' in name else ['']

def pull_suffix(name):
    return '#1' if 'one-thread' in name else ''

def bundled_previous_cells(a, reports):
    """The nearest bundled campaign's PageRank cells, keyed as this campaign's."""
    previous = BUNDLED_PREVIOUS[CAMPAIGN]
    root = a.bundle.parent/f'{previous}-quegee'
    found = {}
    for rep in reports:
        name = rep['label'].removeprefix(f'{CAMPAIGN}-')
        path = root/'timed'/f'{previous}-{name}.json'
        if path.exists():
            found[name] = {(c['fixture'], c['participant'], c['call']): c
                           for c in json.loads(path.read_text())['cells'] if c['algorithm'] == 'pagerank'}
    return found

def plural(n, one, many):
    return f'{n} {one if n == 1 else many}'

def ratio(cell, other):
    """cell's per-sweep cost over other's, with the sum of the two MAD/medians as its margin."""
    if not cell or not other or cell['per_iteration_ms'] is None or other['per_iteration_ms'] is None: return None
    return (cell['per_iteration_ms'] / other['per_iteration_ms'],
            (cell['dispersion'] or 0) + (other['dispersion'] or 0))

def like_for_like(reports):
    """`grust-next@unchecked+f32` against `neo4j-graph`, one sweep against one sweep.

    Both rows carry f32 scores and neither performs accounting, so this is the
    pair the campaign calls like for like. The figure is per-iteration ms over
    per-iteration ms on the same cell of the same run; it is not a total, the
    two rows stop at different counts, and its margin is the sum of the two
    cells' MAD/median.
    """
    print(f'### One sweep of `grust-next@unchecked+f32` against one sweep of `neo4j-graph`\n')
    print('Per cell, both participants\' per-iteration ms and iteration count, and the first over the second, with '
          'the sum of the two cells\' MAD/median as its margin. Both rows carry f32 scores and neither charges work '
          'to a meter, which is why they are put together; they stop at different counts, so this compares the cost '
          'of one sweep and not the time to an answer, and the totals are in the tables above. A figure whose '
          'distance from 1 is smaller than its margin is inside dispersion and is not a difference.\n')
    print('| fixture | run | `grust-next@unchecked+f32` per-iter / iters | `neo4j-graph` per-iter / iters | ratio ± | outside its margin |')
    print('| --- | --- | ---: | ---: | ---: | --- |')
    rows = []
    for rep in reports:
        name = rep['label'].removeprefix(f'{CAMPAIGN}-')
        idx = {(c['fixture'], c['participant'], c['call']): c for c in rep['cells']}
        s = pull_suffix(name)
        for fixture in sorted({c['fixture'] for c in rep['cells']}):
            n = idx.get((fixture, 'neo4j-graph', None))
            g = idx.get((fixture, f'grust-next@unchecked+f32{s}', 'second'))
            r = ratio(g, n)
            if r is None: continue
            outside = abs(r[0] - 1) > r[1]
            rows.append((fixture, name, r, outside))
            print(f"| `{fixture.removesuffix('.edges')}` | {name} | {g['per_iteration_ms']:.3f} / {g['iterations']} | "
                  f"{n['per_iteration_ms']:.3f} / {n['iterations']} | {r[0]:.3f} ± {r[1]:.3f} | {'yes' if outside else 'no'} |")
    print()
    below = [r for r in rows if r[2][0] <= 1]
    above = [r for r in rows if r[2][0] > 1]
    above_margin = [r for r in above if r[3]]
    inside = [r for r in above if not r[3]]
    def named(rs): return ', '.join(f"`{f.removesuffix('.edges')}` {n} ({r[0]:.3f} ± {r[1]:.3f})" for f, n, r, _ in rs)
    print(f"Of the {len(rows)} cells, {len(below)} put Grust's sweep at or below `neo4j-graph`'s and "
          f"{plural(len(above), 'is', 'are')} above it. Of those {len(above)}, "
          f"{plural(len(inside), 'is', 'are')} above by less than its margin and inside dispersion"
          + (f" ({named(inside)})" if inside else '') + f", and {plural(len(above_margin), 'is', 'are')} "
          "above by more than the margin on that cell"
          + (f": {named(above_margin)}" if above_margin else '') + ". "
          "Every one of these figures is formed inside this campaign from two cells of the same run.\n")

def accounting_cost(a, reports):
    """`counted` against `unchecked`: what charging work to a shared meter costs per sweep."""
    previous = bundled_previous_cells(a, reports)
    old = BUNDLED_PREVIOUS[CAMPAIGN].upper()
    print(f'### What work accounting costs per sweep, here and in {old}\n')
    print("`counted` charges work to a shared meter and observes cancellation; `unchecked` does neither and runs the "
          "same kernel otherwise. Their per-iteration ms over each other on the same cell of the same run is what the "
          f"meter costs, with the sum of the two cells' MAD/median as its margin. The {old} column is formed the same "
          f"way inside {old}'s own bundle: no {CAMPAIGN.upper()} cell is divided by a {old} cell, and the two columns "
          f"are each campaign's own reading. {PREVIOUS[CAMPAIGN].upper()} ran on this host between them and was never "
          "bundled, so it is not a column here.\n")
    print(f'| fixture | run | kernel | precision | {old} counted/unchecked ± | {CAMPAIGN.upper()} counted/unchecked ± |')
    print('| --- | --- | --- | --- | ---: | ---: |')
    pull_rows, push_rows = [], []
    for rep in reports:
        name = rep['label'].removeprefix(f'{CAMPAIGN}-')
        new = {(c['fixture'], c['participant'], c['call']): c for c in rep['cells']}
        old_cells = previous.get(name, {})
        for fixture in sorted({c['fixture'] for c in rep['cells']}):
            for s in suffixes_for(name):
                for tag, p in (('f32', F32), ('f64', '')):
                    def pair(cells):
                        return ratio(cells.get((fixture, f'grust-next@counted{p}{s}', 'second')),
                                     cells.get((fixture, f'grust-next@unchecked{p}{s}', 'second')))
                    o, n = pair(old_cells), pair(new)
                    if n is None and o is None: continue
                    def show(r): return '—' if r is None else f'{r[0]:.3f} ± {r[1]:.3f}'
                    kern = 'push' if s == '#unset' else 'pull'
                    if n: (push_rows if kern == 'push' else pull_rows).append((fixture, name, tag, o, n))
                    print(f"| `{fixture.removesuffix('.edges')}` | {name} | {kern} | {tag} | {show(o)} | {show(n)} |")
    print()
    if not pull_rows: return
    def span(rs, i):
        vals = [r[i][0] for r in rs if r[i]]
        return (min(vals), max(vals)) if vals else None
    def named(rs, i): return ', '.join(f"`{f.removesuffix('.edges')}` {n} {t} ({r[i][0]:.3f} ± {r[i][1]:.3f})"
                                       for r in rs for f, n, t in [(r[0], r[1], r[2])])
    outside_new = [r for r in pull_rows if abs(r[4][0] - 1) > r[4][1]]
    outside_old = [r for r in pull_rows if r[3] and abs(r[3][0] - 1) > r[3][1]]
    lo, hi = span(pull_rows, 4)
    olo, ohi = span(pull_rows, 3)
    print(f"Over the {len(pull_rows)} pull-kernel cells the meter's cost in {CAMPAIGN.upper()} runs from {lo:.3f} to "
          f"{hi:.3f}, and {plural(len(outside_new), 'cell differs', 'cells differ')} from 1 by more than the margin on that cell"
          + (': ' + named(outside_new, 4) if outside_new else '') + '. '
          + (f"On the same cells in {old} it ran from {olo:.3f} to {ohi:.3f}, with "
             f"{plural(len(outside_old), 'cell', 'cells')} outside their margins. " if olo is not None else ''))
    for size, label in (('2097152', '2,097,152'), ('4194304', '4,194,304')):
        big = [r for r in pull_rows if size in r[0]]
        if not big: continue
        blo, bhi = span(big, 4)
        obl, out = span(big, 3), [r for r in big if abs(r[4][0] - 1) > r[4][1]]
        print(f"At {label} nodes the {len(big)} pull cells read {blo:.3f} to {bhi:.3f} in {CAMPAIGN.upper()}"
              + (f" against {obl[0]:.3f} to {obl[1]:.3f} in {old}" if obl else '')
              + (f", every one inside its own margin." if not out else
                 f", of which {plural(len(out), 'is', 'are')} outside the margin on that cell: " + named(out, 4) + '.')
              + ' ' + ', '.join(f"{'Below' if r[4][0] < 1 else 'Above'} 1 is the meter costing "
                                f"{'less' if r[4][0] < 1 else 'more'} than no meter" for r in out[:1]) + ('.' if out else ''))
    if push_rows:
        plo, phi = span(push_rows, 4)
        polo, pohi = span(push_rows, 3)
        worse = [r for r in push_rows if r[3] and r[4][0] - r[3][0] > r[4][1] + r[3][1]]
        print(f"The push kernel is not in that state. Over its {len(push_rows)} cells the meter costs {plo:.3f} to "
              f"{phi:.3f} in {CAMPAIGN.upper()}"
              + (f" against {polo:.3f} to {pohi:.3f} in {old}" if polo is not None else '')
              + (f", and on {plural(len(worse), 'cell', 'cells')} the {CAMPAIGN.upper()} figure exceeds the {old} "
                 f"figure by more than both margins together: " + ', '.join(
                     f"`{r[0].removesuffix('.edges')}` {r[1]} {r[2]} ({r[3][0]:.3f} to {r[4][0]:.3f})" for r in worse)
                 if worse else '') + '.')
    print()

def host_between_campaigns(a, reports):
    """Why no absolute number here is put beside one from another campaign."""
    previous = bundled_previous_cells(a, reports)
    if not previous: return
    old = BUNDLED_PREVIOUS[CAMPAIGN].upper()
    print(f'### Why no {CAMPAIGN.upper()} time is compared with a {old} or {PREVIOUS[CAMPAIGN].upper()} time\n')
    print(f"`neo4j-graph` and `grust` (v0.22.0) are the same sources in {old} and in {CAMPAIGN.upper()}, on fixtures "
          "with the same SHA-256, under the same protocol. The host was restarted between the campaigns. Their "
          "per-sweep figures moved anyway, by cell and in both directions, so a difference between a "
          f"{CAMPAIGN.upper()} number and a {old} number is not readable as a difference in code and none is formed "
          "outside this table, which exists to say so:\n")
    print(f'| fixture | run | participant | call | {old} per-iter | {CAMPAIGN.upper()} per-iter | {CAMPAIGN.upper()}/{old} |')
    print('| --- | --- | --- | --- | ---: | ---: | ---: |')
    seen = []
    for rep in reports:
        name = rep['label'].removeprefix(f'{CAMPAIGN}-')
        old_cells = previous.get(name)
        if old_cells is None: continue
        for c in cell_rows(rep):
            if base(c['participant']).split('+')[0] not in ('grust', 'neo4j-graph'): continue
            o = old_cells.get((c['fixture'], c['participant'], c['call']))
            if not o or o['per_iteration_ms'] is None or c['per_iteration_ms'] is None: continue
            if o['unusable'] or c['unusable']: continue
            r = c['per_iteration_ms'] / o['per_iteration_ms']
            seen.append((r, c['participant'], c['fixture'], name, c['call']))
            print(f"| `{c['fixture'].removesuffix('.edges')}` | {name} | `{c['participant']}` | {c['call'] or '—'} | "
                  f"{o['per_iteration_ms']:.3f} | {c['per_iteration_ms']:.3f} | {r:.3f} |")
    print()
    if not seen: return
    import statistics
    lo, hi = min(seen), max(seen)
    n2m = [s for s in seen if s[1] == 'neo4j-graph' and '2097152' in s[2] and 'one-thread' in s[3]]
    print(f"{len(seen)} cells of unchanged code, median {CAMPAIGN.upper()}/{old} {statistics.median(s[0] for s in seen):.3f}, "
          f"from {lo[0]:.3f} (`{lo[1]}` {lo[2].removesuffix('.edges')} {lo[3]}{' ' + lo[4] if lo[4] else ''}) to "
          f"{hi[0]:.3f} (`{hi[1]}` {hi[2].removesuffix('.edges')} {hi[3]}{' ' + hi[4] if hi[4] else ''}). ", end='')
    if n2m:
        for r, _, fixture, name, _ in sorted(n2m, key=lambda s: s[2]):
            pass
        parts = ', '.join(f"{fixture.removesuffix('.edges')} {old} "
                          f"{previous[name][(fixture, 'neo4j-graph', None)]['per_iteration_ms']:.0f} ms against "
                          f"{CAMPAIGN.upper()} {previous[name][(fixture, 'neo4j-graph', None)]['per_iteration_ms'] * r:.0f} ms"
                          for r, _, fixture, name, _ in sorted(n2m, key=lambda s: s[2]))
        print(f"The reference participant's own one-thread sweep at 2,097,152 nodes is among the cells that moved: {parts}.", end='')
    print(f" Every comparison this section makes is therefore between two cells of {CAMPAIGN.upper()}.")

def previous_cells(a, reports):
    """The previous campaign's PageRank cells, keyed as this campaign's, run by run."""
    previous = PREVIOUS[CAMPAIGN]
    root = a.bundle.parent/f'{previous}-quegee'
    found = {}
    for rep in reports:
        name = rep['label'].removeprefix(f'{CAMPAIGN}-')
        path = root/'timed'/(f'{name}.json' if previous == 'b6' else f'{previous}-{name}.json')
        if path.exists():
            found[name] = {(c['fixture'], c['participant'], c['call']): c
                           for c in json.loads(path.read_text())['cells'] if c['algorithm'] == 'pagerank'}
    return found

def beside_previous(a, reports):
    """Each compared participant's per-sweep distance to neo4j-graph, in the previous campaign and in this one.

    A distance is a ratio formed inside one campaign, per-iteration ms of the
    participant over per-iteration ms of neo4j-graph on the same cell, so the
    two columns are each campaign's own figure and no cell of one is divided by
    a cell of the other. Its margin is the sum of the two cells' relative MADs;
    a change between campaigns smaller than both margins is inside dispersion.
    """
    previous = previous_cells(a, reports)
    if not previous: return
    old_name = PREVIOUS[CAMPAIGN].upper()
    print(f'### {old_name} beside {CAMPAIGN.upper()}, per sweep\n')
    print(f'For every cell, the per-iteration time and iteration count of each participant in {old_name} and in '
          f'{CAMPAIGN.upper()}, and its distance to `neo4j-graph` in each: per-iteration ms over `neo4j-graph`\'s '
          'per-iteration ms on the same cell of the same campaign, with the sum of the two cells\' MAD/median as its '
          f'margin. The {old_name} figures are {old_name}\'s own, from its bundle; nothing here divides a '
          f'{CAMPAIGN.upper()} cell by a {old_name} cell. For Grust the second call is shown. A change in distance '
          'smaller than both margins is within dispersion and is not a change.\n')
    print(f'| fixture | run | kernel | participant | {old_name} per-iter / iters | {old_name} distance ± | '
          f'{CAMPAIGN.upper()} per-iter / iters | {CAMPAIGN.upper()} distance ± |')
    print('| --- | --- | --- | --- | ---: | ---: | ---: | ---: |')
    def distance(cell, anchor):
        if not cell or not anchor or cell['per_iteration_ms'] is None or anchor['per_iteration_ms'] is None: return None
        return (cell['per_iteration_ms'] / anchor['per_iteration_ms'],
                (cell['dispersion'] or 0) + (anchor['dispersion'] or 0))
    for rep in reports:
        name = rep['label'].removeprefix(f'{CAMPAIGN}-')
        old = previous.get(name)
        if old is None: continue
        new = {(c['fixture'], c['participant'], c['call']): c for c in rep['cells']}
        suffixes = ['#1', '#unset'] if 'one-thread' in name else ['']
        for fixture in sorted({c['fixture'] for c in rep['cells']}):
            for s in suffixes:
                kernel = 'push' if s == '#unset' else 'pull'
                anchors = (old.get((fixture, 'neo4j-graph', None)), new.get((fixture, 'neo4j-graph', None)))
                for p in COMPARED:
                    key = p if p == 'neo4j-graph' else f'{p}{s}'
                    call = None if p == 'neo4j-graph' else 'second'
                    if p == 'neo4j-graph' and s == '#unset': continue
                    o, n = old.get((fixture, key, call)), new.get((fixture, key, call))
                    if not (o or n): continue
                    def per(c): return '—' if not c or c['per_iteration_ms'] is None else f"{c['per_iteration_ms']:.3f} / {c['iterations']}"
                    def dist(d): return '—' if d is None else f"{d[0]:.3f} ± {d[1]:.3f}"
                    print(f"| `{fixture.removesuffix('.edges')}` | {name} | {kernel} | `{key}` | {per(o)} | "
                          f"{dist(distance(o, anchors[0]))} | {per(n)} | {dist(distance(n, anchors[1]))} |")
        print()

def unchanged_against_previous(a, reports):
    """v0.22.0 and neo4j-graph did not change between campaigns; their cells say what the host did."""
    previous = previous_cells(a, reports)
    if not previous: return
    old_name = PREVIOUS[CAMPAIGN].upper()
    import statistics
    pairs = collections.defaultdict(list)
    for rep in reports:
        name = rep['label'].removeprefix(f'{CAMPAIGN}-')
        old = previous.get(name)
        if old is None: continue
        for c in rep['cells']:
            if c['participant'].split('#')[0] not in ('grust', 'neo4j-graph'): continue
            o = old.get((c['fixture'], c['participant'], c['call']))
            if o and not o['unusable'] and not c['unusable']:
                pairs[c['participant'].split('#')[0]].append((c['total_ms'] / o['total_ms'], c['fixture'], name, c['call']))
    if not pairs: return
    print(f'**Unchanged code against {old_name}.** `grust` (v0.22.0) and `neo4j-graph` are the same binaries\' sources as in '
          f'{old_name}, differing at most by the harness commit stamped into them, on the same fixtures, under the same '
          f'protocol. Their {CAMPAIGN.upper()} total against their {old_name} total on the same cell, as the median and the '
          'range of the ratio, is a reading of the host, not of any code:\n')
    print(f'| participant | cells | median {CAMPAIGN.upper()}/{old_name} | smallest | largest |')
    print('| --- | ---: | ---: | --- | --- |')
    for name, rs in sorted(pairs.items()):
        lo, hi = min(rs), max(rs)
        print(f"| `{name}` | {len(rs)} | {statistics.median(r[0] for r in rs):.3f} | "
              f"{lo[0]:.3f} ({lo[1].removesuffix('.edges')} {lo[2]}{' ' + lo[3] if lo[3] else ''}) | "
              f"{hi[0]:.3f} ({hi[1].removesuffix('.edges')} {hi[2]}{' ' + hi[3] if hi[3] else ''}) |")
    print()

def hosts(a):
    """The per-sweep distance of the f32 unchecked row to neo4j-graph on every host given, cell by cell.

    Every host but the first is a burstable, shared box: its figure is a ratio
    formed inside one run on that box, printed with that run's steal, and is
    never an absolute time. The first bundle is the measuring host's.
    """
    bundles = [pathlib.Path(b) for b in a.timed] if a.timed else [a.bundle]
    names = [b.name for b in bundles]
    print(f'### The shape on other hosts\n')
    print('Per cell, the per-iteration time of `grust-next@unchecked+f32` (second call) over the per-iteration time of '
          '`neo4j-graph` on the same cell of the same run on the same host, with the sum of the two cells\' MAD/median as '
          'its margin, and the run\'s steal ticks and width. The first column is the measuring host. Every other host '
          'is a burstable instance shared with other work: its steal is read per run and printed, its figure is a '
          'ratio on a shared box and nothing from it is an absolute time or is compared with another host\'s time. '
          'On a host narrower than 16 CPUs the full-width run is the host\'s width and is labelled so.\n')
    print('| fixture | run | ' + ' | '.join(f'`{n}` ratio ± (width, steal)' for n in names) + ' |')
    print('| --- | --- | ' + ' | '.join('---:' for _ in names) + ' |')
    rows = collections.OrderedDict()
    for i, b in enumerate(bundles):
        reports = load_timed(sorted((b/'timed').glob(f'{CAMPAIGN}-*.json')))
        record = next((p for p in (b/'campaign.jsonl', b/f'campaign-{CAMPAIGN}.jsonl') if p.exists()), None)
        steal = {}
        if record:
            for l in record.read_text().splitlines():
                r = json.loads(l)
                if 'run' in r: steal[r['run']] = r.get('steal_ticks')
        for rep in reports:
            name = rep['label'].removeprefix(f'{CAMPAIGN}-')
            idx = {(c['fixture'], c['participant'], c['call']): c for c in rep['cells']}
            for fixture in sorted({c['fixture'] for c in rep['cells']}):
                s = '#1' if 'one-thread' in name else ''
                n, f = idx.get((fixture, 'neo4j-graph', None)), idx.get((fixture, f'grust-next@unchecked+f32{s}', 'second'))
                cell = '—'
                if n and f and n['per_iteration_ms'] and f['per_iteration_ms']:
                    cell = (f"{f['per_iteration_ms'] / n['per_iteration_ms']:.3f} ± "
                            f"{(f['dispersion'] or 0) + (n['dispersion'] or 0):.3f} ({rep['workers']}, {steal.get(name, '?')})")
                rows.setdefault((fixture, name), ['—'] * len(bundles))[i] = cell
    for (fixture, name), cells in rows.items():
        print(f"| `{fixture.removesuffix('.edges')}` | {name} | " + ' | '.join(cells) + ' |')
    print()

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--campaign', choices=list(PREVIOUS), default='b7',
                   help='which campaign\'s files: the prefix of every output')
    p.add_argument('command', choices=['tables', 'estimate', 'section', 'hosts'])
    p.add_argument('bundle', type=pathlib.Path, nargs='?')
    p.add_argument('--timed', type=pathlib.Path, nargs='+',
                   help='tables: these run files instead of the bundle\'s; hosts: the bundle directories, measuring host first')
    a = p.parse_args()
    global CAMPAIGN
    CAMPAIGN = a.campaign
    if a.bundle is None and not a.timed: raise SystemExit('give a bundle directory or --timed files')
    dict(tables=tables, estimate=estimate, section=section, hosts=hosts)[a.command](a)

if __name__ == '__main__': main()
