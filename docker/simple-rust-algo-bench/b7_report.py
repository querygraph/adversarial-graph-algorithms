#!/usr/bin/env python3
"""B7's tables, and its duration estimate, both computed from evidence files.

    b7_report.py tables BUNDLE_DIR        Markdown for every B7 timed run
    b7_report.py estimate B6_BUNDLE_DIR   expected B7 duration from B6's walls

`tables` reads BUNDLE_DIR/timed/b7-*.json (or the files given with --timed)
and BUNDLE_DIR/parity/parity-b7-*.json, and prints, per run and fixture, one
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
    reports = []
    for path in paths:
        report = json.loads(pathlib.Path(path).read_text())
        report['_file'] = pathlib.Path(path).name
        reports.append(report)
    return reports

def cell_rows(report):
    order = list(report['participants'])
    return sorted(report['cells'], key=lambda c: (c['fixture'], order.index(c['participant']), c['call'] or ''))

def tables(a):
    paths = a.timed or sorted((a.bundle/'timed').glob('b7-*.json'))
    if not paths: raise SystemExit(f'no B7 timed runs under {a.bundle}/timed')
    reports = load_timed(paths)
    print('# B7 tables\n')
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
    paths = sorted((a.bundle/'parity').glob('parity-b7-*.json')) if a.bundle else []
    if not paths: return
    print('## Parity\n')
    print('Every row parity produced for the participants B7 times, PageRank only. `vector` is how many of '
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

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('command', choices=['tables', 'estimate'])
    p.add_argument('bundle', type=pathlib.Path, nargs='?')
    p.add_argument('--timed', type=pathlib.Path, nargs='+', help='tables: these run files instead of the bundle\'s')
    a = p.parse_args()
    if a.bundle is None and not a.timed: raise SystemExit('give a bundle directory or --timed files')
    tables(a) if a.command == 'tables' else estimate(a)

if __name__ == '__main__': main()
