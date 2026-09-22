#!/usr/bin/env python3
"""The timed run: counterbalanced, parity-gated, and honest about absence.

Parity runs first and a mismatched cell is never timed. Variant order alternates
between repeats so a monotone drift affects both halves of every pair. Steal is
read across the whole run and across every cell, per AGENTS.md. Tables are as
wide as the participants that have the kernel, and each says who is absent and
that the reason is no such kernel rather than a slow one.

A participant name may carry `@mode` (Grust's accounting), `+tag` (how it runs;
`+f32` alone changes what it computes, and its receipt says so) and
`#N`/`#unset` (its concurrency, which selects a kernel); see variants.py. A participant that reports `kernel_second_ms`
produces two rows per cell, `call: first` and `call: second`, and they are
never folded into one number: the first is what a single call costs on a fresh
projection, the second what it costs once anything the first call built and
cached is already there.

Every cell records the minor page faults taken across the call it times, read
outside the timer by the participant itself. B4's WCC and BFS first-call rows
moved with that counter and not with any kernel: a transpose built and freed
for a kernel that never reads it left glibc's allocator in a different state.
The counter is beside every first-call time here so that such an effect is
visible in the evidence rather than in a later attribution.
"""
import argparse, json, os, pathlib, statistics, subprocess, sys, time

import variants

ALGORITHMS = ['pagerank', 'wcc', 'bfs', 'triangles']

# Grust's kernels fall back to sequential below a published threshold; the
# neo4j-graph participant parallelises unconditionally. Below a floor
# `workers_above` returns None whatever concurrency was requested, so a
# small-size row would compare a parallel library against a Grust kernel that
# declined to parallelise -- and it would flatter us, which is the direction that
# is easiest not to notice. The units and floors are read from
# grust-algorithms/src/parallel.rs; each row records whether the Grust-family
# kernels were eligible at its size.
FLOORS = {
    'pagerank': (lambda nodes, edges: (nodes + edges) * 2, 1 << 14),
    'wcc': (lambda nodes, edges: nodes + edges * 2, 1 << 14),
    'bfs': (lambda nodes, edges: nodes + edges, 1 << 18),
}
GRUST_FAMILY = {'grust', 'grust-next', 'grustcat', 'icecat'}

def eligibility(algorithm, nodes, edges):
    if algorithm not in FLOORS: return None
    units, floor = FLOORS[algorithm][0](nodes, edges), FLOORS[algorithm][1]
    return dict(units=units, floor=floor, parallel_eligible=units >= floor)

def steal_ticks():
    with open('/proc/stat') as handle:
        fields = handle.readline().split()
    return int(fields[8])

def receipt(binary, extra=()):
    out = subprocess.run([str(binary), '--receipt', *extra], capture_output=True, text=True, timeout=120)
    out.check_returncode()
    return json.loads(out.stdout)

def worker_env(workers):
    """Give every participant the same width, explicitly.

    The three projects take their thread count from three different places:
    Grust from `with_concurrency`, neo4j-graph from `available_parallelism` for
    PageRank and triangles and from rayon for WCC, NetworKit from OpenMP. Left
    alone under a CPU quota they disagree - OpenMP reads the affinity mask and
    would oversubscribe a quota the others respect - so each is set by name and
    the value is recorded in every cell.
    """
    if workers is None: return None
    return dict(os.environ, OMP_NUM_THREADS=str(workers), RAYON_NUM_THREADS=str(workers),
                OPENBLAS_NUM_THREADS=str(workers))

def sample(binary, fixture, algorithm, tolerance, concurrency=None, workers=None, extra=()):
    command = [str(binary), '--fixture', str(fixture), '--algorithm', algorithm,
               '--tolerance', repr(tolerance), *extra]
    if concurrency is not None: command += ['--concurrency', str(concurrency)]
    out = subprocess.run(command, capture_output=True, text=True, timeout=3600,
                         env=worker_env(workers))
    out.check_returncode()
    return json.loads(out.stdout)

def spread(values):
    middle = statistics.median(values)
    return middle, statistics.median([abs(value - middle) for value in values])

# Where each participant reports the minor page faults of a phase. The Grust
# participants time two calls and report one counter per call; the others time
# one call and report `minflt_kernel`. A participant that reports none gives
# None here rather than a zero, which would claim it took no fault.
FAULTS = dict(first=('minflt_first', 'minflt_kernel'), second=('minflt_second',),
              build=('minflt_build',))

def faults(rows, phase):
    for field in FAULTS[phase]:
        values = [row[field] for row in rows if row.get(field) is not None]
        if values: return spread(values)[0]
    return None

def transpose(spec, algorithm, rows, incoming):
    """Which timer a reverse index was built under, where it is known.

    B3's finding was that this differed by participant and was not recorded.
    B5 asks it of every algorithm, not only PageRank, because B4's answer for
    WCC and BFS - built inside build_ms, for a kernel that never reads it - is
    the artifact this run corrects. grust-next builds it with prepare_incoming
    inside build_ms where a kernel reads it; icecat builds it between the two
    timers and prints it apart; grust at v0.22.0 builds it inside the first
    pull-kernel call, so inside that call's kernel_ms. grustcat, neo4j-graph
    and NetworKit build theirs in their constructors, inside build_ms, and
    print no figure for it.
    """
    if incoming:
        built = 'inside build_ms'
        if rows[0].get('prepare_incoming') == 'always' and not rows[0].get('reads_incoming'):
            built += ', for a kernel that does not read it: B4 behaviour, kept as its own row'
        return dict(where=built, ms=spread(incoming)[0])
    apart = [r['prepare_incoming_ms'] for r in rows if 'prepare_incoming_ms' in r]
    if apart:
        return dict(where='timed apart: in neither build_ms nor kernel_ms', ms=spread(apart)[0])
    if rows[0].get('prepare_incoming') is not None:
        # A Grust participant that reported its policy and built nothing.
        if rows[0].get('reads_incoming'):
            return dict(where='inside kernel_ms of the first call', ms=None)
        return dict(where='not built: this kernel does not read in-arcs', ms=None)
    if algorithm != 'pagerank': return None
    return dict(where='inside build_ms, in the constructor; not reported apart', ms=None)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--directory', type=pathlib.Path, default=pathlib.Path('/opt/bench'))
    p.add_argument('--fixtures', type=pathlib.Path, required=True)
    p.add_argument('--participants', nargs='+',
                   default=['neo4j-graph', 'icebug', 'icecat', 'grustcat', 'grust'],
                   help='participant names, optionally with @accounting-mode and #concurrency')
    p.add_argument('--algorithms', nargs='+', default=ALGORITHMS)
    p.add_argument('--tolerance', type=float, default=1e-8)
    p.add_argument('--warmups', type=int, default=1)
    p.add_argument('--repeats', type=int, default=5)
    p.add_argument('--parity', type=pathlib.Path, nargs='+', required=True,
                   help='parity JSON from parity.py, one per concurrency the variants use; a cell '
                        'whose variant did not agree at its own concurrency is not timed')
    p.add_argument('--concurrency', type=int,
                   help='passed to participants that accept it, unless a variant fixes its own; '
                        'unset and 1 are different kernels')
    p.add_argument('--workers', type=int,
                   help='thread width given to every participant by name: OMP_NUM_THREADS for '
                        'NetworKit, RAYON_NUM_THREADS for neo4j-graph WCC, --concurrency for Grust. '
                        'Set it to the cgroup CPU count; left unset the three disagree.')
    p.add_argument('--unusable-dispersion', type=float, default=0.25,
                   help='a cell whose MAD is at least this fraction of its median is marked unusable')
    p.add_argument('--families', nargs='+', metavar='FAMILY',
                   help='only fixtures named FAMILY-<size>.edges; default every fixture in the directory')
    p.add_argument('--label', default='', help='free text recorded in the report, e.g. the run name')
    p.add_argument('--output', type=pathlib.Path, required=True)
    a = p.parse_args()

    specs = [variants.parse(name, a.concurrency) for name in a.participants]
    verdicts = {}
    for path in a.parity:
        for row in json.loads(path.read_text()):
            if 'concurrency' not in row:
                raise SystemExit(f'{path}: parity rows carry no concurrency; rerun parity.py')
            verdicts[(row['fixture'], row['participant'], row['algorithm'], row['concurrency'])] = row['verdict']
    declared = {spec['key']: receipt(a.directory/spec['binary'], spec['args']) for spec in specs}

    def agreed(fixture, spec, algorithm):
        return verdicts.get((fixture.name, spec['parity_key'], algorithm, spec['concurrency'])) == 'agrees'

    fixtures = [f for f in sorted(a.fixtures.glob('*.edges'))
                if a.families is None or f.name.split('-')[0] in a.families]
    if not fixtures:
        raise SystemExit(f'no fixtures in {a.fixtures} for families {a.families}')
    before, started = steal_ticks(), time.time()
    samples, groups, skipped = [], {}, []
    for fixture in fixtures:
        for algorithm in a.algorithms:
            present = [spec for spec in specs if algorithm in declared[spec['key']]['algorithms']]
            for spec in present:
                if not agreed(fixture, spec, algorithm):
                    skipped.append(dict(fixture=fixture.name, algorithm=algorithm, participant=spec['key'],
                                        reason='no agreeing parity row at this concurrency'))
            present = [spec for spec in present if agreed(fixture, spec, algorithm)]
            if not present: continue
            group_steal, group_started = steal_ticks(), time.time()
            for repeat in range(a.warmups + a.repeats):
                # ABBA: a monotone drift moves the first and last variant in
                # opposite directions across the pair, so the comparison absorbs it.
                order = present if repeat % 2 == 0 else list(reversed(present))
                for spec in order:
                    found = sample(a.directory/spec['binary'], fixture, algorithm, a.tolerance,
                                   spec['concurrency'], a.workers, spec['args'])
                    found.update(variant=spec['key'], repeat=repeat, warmup=repeat < a.warmups,
                                 position=order.index(spec))
                    samples.append(found)
            groups[(fixture.name, algorithm)] = dict(
                steal_ticks=steal_ticks() - group_steal, seconds=round(time.time() - group_started, 2))
    after = steal_ticks()

    kept = [s for s in samples if not s['warmup']]
    cells = {}
    for s in kept:
        cells.setdefault((pathlib.Path(s['fixture']).name, s['algorithm'], s['variant']), []).append(s)
    report = dict(
        label=a.label, steal_ticks_over_run=after - before, seconds=round(time.time() - started, 1),
        tolerance=a.tolerance, warmups=a.warmups, repeats=a.repeats,
        workers=a.workers, concurrency=a.concurrency, unusable_dispersion=a.unusable_dispersion,
        # The allocator this run's participants all saw. Set for the container
        # by campaign.py or absent; never set for one participant and not
        # another, which would compare two allocators.
        glibc_tunables=os.environ.get('GLIBC_TUNABLES'),
        # Table rules, emitted with the data so a report cannot quietly drop them.
        notes=dict(
            width=('At full width, only participants declaring width_capable can use a second '
                   'thread. The others are shown with their times, labelled sequential by '
                   'construction, and no width-to-width ratio is drawn against them.'),
            lineage=('The lineage comparison - icebug to icecat to grustcat to grust - is valid '
                     'only at equal width, so it belongs to the one-thread run. At full width a '
                     'difference between them is a statement about threads, not about a rewrite.'),
            across=('Cells from runs at different widths are not divided by one another. A '
                    'scaling factor is its own table with its own heading.'),
            precision=('PageRank precision differs by participant: neo4j-graph accumulates and '
                       'returns f32; every other participant f64, except a Grust variant tagged '
                       '+f32, which runs pagerank_f32 and whose receipt and cells say f32. The '
                       'score array is half the bytes, so it is half the memory traffic on the one '
                       'array PageRank touches randomly per arc. An f32 kernel also stops at a '
                       'different iteration count under the same tolerance, so every PageRank '
                       'table carries the count beside the total, and where counts differ the '
                       'per-iteration figure is the one to compare. State it under every PageRank '
                       'table; it is a boundary, '
                       'not a rounding footnote. WCC and triangle counts carry no such difference '
                       '- component labels are indices and the triangle count is u64. '
                       'Size-dependent: at 65,536 nodes every working set fits in the measuring '
                       'host L3 with room to spare, so f32 buys bandwidth on one array and no '
                       'cache residency at all. The arrays cross a 24.8 MB L3 somewhere in the '
                       'hundreds of thousands of nodes at this density, and a run above that '
                       'must restate this sentence rather than inherit it.'),
            faults=('Every cell records the minor page faults of the call it times, read outside '
                    'the timer by the participant with getrusage(RUSAGE_SELF). B4 built the '
                    'transpose inside build_ms for every algorithm, including WCC and BFS, which '
                    'never read it; building and freeing it raised glibc dynamic mmap threshold, '
                    'and the first call after it took about 112 to 128 more minor faults. B5 '
                    'prepares it only where a kernel reads it and keeps the old behaviour as the '
                    '+eager rows, so the correction can be read off the counter and the time '
                    'together.'),
            calls=('A Grust row with call "first" is the first kernel call on a fresh projection, '
                   'which is what B3 published. On v0.22.0 (grust) that call also builds the '
                   'transpose the pull kernel needs; on the later commit (grust-next) the '
                   'transpose is built by prepare_incoming inside build_ms, as grustcat builds '
                   'its own inside its constructor, and incoming_ms says how much of build_ms '
                   'it was. Call "second" repeats the kernel on the same projection with '
                   'anything the first call built already cached; it also runs on warm caches, '
                   'which a first call does not. The two are separate rows, never averaged.'),
            accounting=('Every Grust row names its accounting mode. counted is the default and '
                        'what v0.22.0 always does: work is charged to a shared counter and '
                        'cancellation is observed. work-uncounted charges nothing and still '
                        'observes cancellation; unchecked does neither and cannot be stopped '
                        'once started. Memory admission is performed in every mode. neo4j-graph '
                        'performs no accounting, so unchecked is its like-for-like row; counted '
                        'is what the guarantee costs.'),
            dispersion=('dispersion is MAD / median. A cell at or above unusable_dispersion is '
                        'marked unusable and enters no table.')),
        participants={spec['key']: declared[spec['key']] for spec in specs},
        skipped=skipped, groups=[dict(fixture=f, algorithm=g, **v) for (f, g), v in groups.items()],
        cells=[], samples=samples)
    for (fixture, algorithm, key), rows in sorted(cells.items()):
        spec = next(s for s in specs if s['key'] == key)
        calls = [('first', 'kernel_ms')]
        if all('kernel_second_ms' in r for r in rows): calls.append(('second', 'kernel_second_ms'))
        for call, field in calls:
            kernel, kernel_spread = spread([r[field] for r in rows])
            iterations = rows[0].get('iterations')
            dispersion = kernel_spread / kernel if kernel else None
            incoming = [r['incoming_ms'] for r in rows if r.get('incoming_ms') is not None]
            report['cells'].append(dict(
                fixture=fixture, algorithm=algorithm, participant=key, binary=spec['binary'],
                call=call if len(calls) > 1 else None,
                accounting=rows[0].get('accounting'), grust_commit=rows[0].get('grust_commit'),
                concurrency=spec['concurrency'], workers=a.workers,
                iterations=iterations,
                # An f32 kernel's residual can sit at its arithmetic floor rather
                # than below the tolerance it was asked for, which the iteration
                # count alone does not show.
                residual=rows[0].get('residual', rows[0].get('error')),
                precision=declared[key].get('precision'),
                total_ms=kernel, total_mad=kernel_spread, dispersion=dispersion,
                unusable=dispersion is not None and dispersion >= a.unusable_dispersion,
                per_iteration_ms=(kernel / iterations) if iterations else None,
                # Read outside the timers by the participant, and reported here
                # beside the time it belongs to rather than folded into it.
                minflt=faults(rows, call),
                minflt_build=faults(rows, 'build'),
                prepare_incoming=rows[0].get('prepare_incoming'),
                reads_incoming=rows[0].get('reads_incoming'),
                build_ms=spread([r['build_ms'] for r in rows])[0],
                build_mad=spread([r['build_ms'] for r in rows])[1],
                incoming_ms=spread(incoming)[0] if incoming else None,
                transpose=transpose(spec, algorithm, rows, incoming),
                work_units=rows[0].get('work_units'), peak_bytes=rows[0].get('peak_bytes'),
                steal_ticks=groups[(fixture, algorithm)]['steal_ticks'],
                grust_family_floor=(eligibility(algorithm, rows[0]['nodes'], rows[0]['edges'])
                                    if spec['binary'] in GRUST_FAMILY else None),
                # Declared by the participant, not inferred here: two of the five
                # cannot use a second thread whatever --workers says, so a
                # width-to-width ratio against them is not a statement about width.
                width_capable=declared[key].get('width_capable'),
                parse_ms=spread([r['parse_ms'] for r in rows])[0],
                absent=sorted({s['binary'] for s in specs
                               if algorithm not in declared[s['key']]['algorithms']})))
    a.output.write_text(json.dumps(report, indent=1)+'\n')
    print(f"steal over the run: {after - before} ticks")
    print(f"{len(kept)} timed samples in {report['seconds']}s -> {a.output}")
    for entry in skipped:
        print(f"not timed: {entry['fixture']} {entry['algorithm']} {entry['participant']}: {entry['reason']}")
    width = max((len(c['participant']) for c in report['cells']), default=10)
    for cell in report['cells']:
        per = f"{cell['per_iteration_ms']:.4f}" if cell['per_iteration_ms'] else '-'
        flag = '  UNUSABLE' if cell['unusable'] else ''
        print(f"{cell['fixture']:<20} {cell['algorithm']:<10} {cell['participant']:<{width}} "
              f"{cell['call'] or '':<6} iters {str(cell['iterations'] or '-'):>4}  "
              f"total {cell['total_ms']:9.4f} ± {cell['total_mad']:.4f}  per-iter {per}  "
              f"build {cell['build_ms']:.2f}  minflt {cell['minflt'] if cell['minflt'] is not None else '-'}  "
              f"steal {cell['steal_ticks']}{flag}")

if __name__ == '__main__': sys.exit(main())
