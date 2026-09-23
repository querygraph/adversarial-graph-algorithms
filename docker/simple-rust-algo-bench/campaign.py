#!/usr/bin/env python3
"""The rerun's host-side driver: parity, then timed runs, each on an idle host.

Runs on the measuring host, outside the image, because the checks it makes are
about the host and a container cannot see them:

- **Idle before and after every run.** No cargo, rustc, perf, other benchmark
  or other container may be running, and no process outside the run may use
  more than a tenth of a CPU over a two-second window. A run that starts on a
  busy host is not started; a run that ends on one is marked discarded.
- **Watched during every run.** A sampler looks for the same processes once a
  second for the whole run, outside the run's own container, because a build
  that starts and finishes between the two checks would pass both. Any sighting
  discards the run. The sampler reads /proc and nothing else.
- **Steal** is read by run.py per cell and over the run; this records it again
  over the whole docker invocation, and the load average at both ends.
- **Agent sessions are recorded by name**, before, during and after every run,
  whatever CPU they use. B4's one discarded run was caused by an agent session
  starting work on the host, so the record says whether one was resident
  instead of leaving that to be reconstructed. It is not a second gate: a
  session that uses CPU is discarded by the CPU rule like anything else.
- **The allocator is a property of a run.** A run may set `GLIBC_TUNABLES` for
  its whole container, which is every participant in it; `pinned-*` repeat
  `one-thread` and `full-width` with glibc's mmap threshold pinned, so what the
  threshold is worth is measured for all of them rather than assumed for one.

A discarded run's output is kept, renamed, and never published: the operator
decides whether to rerun it. Nothing here retries on its own, because a retry
loop on a shared host selects for the quiet moments and reports them as typical.

The matrix is data, in RUNS below, so the plan and the run are one artifact.
`--plan` selects which: `b6` is B5's protocol unchanged, `b7` the PageRank
precision campaign below it. Outputs of a plan other than `b6` carry the plan
name, so a B7 run in a B6 work directory overwrites nothing B6 wrote.
"""
import argparse, json, os, pathlib, re, subprocess, sys, threading, time

HERE = pathlib.Path(__file__).resolve().parent

# Processes whose presence means the host is not idle. Matched against the
# full command line of every process outside the run's own container.
BUSY = re.compile(r'(^|[/ ])(cargo|rustc|perf|cc1plus|ld\.lld|mold|bench-[\w-]+|icebug|'
                  r'run\.py|parity\.py|criterion|hyperfine|stress|yes)( |$)')
# Our own watcher and this driver are python3 campaign.py; never count them.
SELF = re.compile(r'campaign\.py')
# Agent sessions resident on the host. These are recorded by name in every
# snapshot and in every sighting, whatever CPU they are using, because B4's one
# discarded run was caused by an agent session and the record should say
# whether one was present rather than leave it to be reconstructed. They are
# not a separate gate: a session that uses CPU is caught by CPU_SHARE like any
# other process, and a session that uses none is reported and not guessed at.
RESIDENT = re.compile(r'(^|[/ ])(claude|codex|cursor-agent|aider)( |$)')

BASELINE = ['neo4j-graph', 'icebug', 'icecat', 'grustcat']
MODES = ['counted', 'work-uncounted', 'unchecked']
NEXT = [f'grust-next@{mode}' for mode in MODES]
# B4's placement of the transpose, kept as its own row: prepared inside
# build_ms for every algorithm, including the kernels that never read it.
EAGER = 'grust-next@counted+eager'

# The allocator, pinned for every participant in a run or for none of them.
# glibc raises its own mmap threshold when a large mmapped chunk is freed, so
# what a kernel's first call pays in page faults depends on what the build
# before it allocated and released. Pinning the threshold at its 128 KiB
# default disables that adaptation for every process in the container.
# Pinning it for the Grust participants alone would compare two allocators, so
# it is a property of a run: `pinned-*` runs repeat `one-thread` and
# `full-width` with it set, and are published as their own labelled table.
PINNED = dict(GLIBC_TUNABLES='glibc.malloc.mmap_threshold=131072')

# Parity: one file per concurrency, every variant that any timed run uses.
# `--bits-identical` makes a grust-next PageRank that differs from v0.22.0 by a
# single bit a mismatch, so it is never timed.
PARITY = {
    'unset': dict(concurrency=None),
    '1': dict(concurrency=1),
    '16': dict(concurrency=16),
}
PARITY_PARTICIPANTS = BASELINE + ['grust'] + NEXT + [EAGER]

# Timed runs. `#N`/`#unset` fixes a Grust variant's kernel (see variants.py).
RUNS = {
    # The kernel comparison and the only valid lineage comparison, as in B3,
    # with both Grust PageRank kernels: pull (#1, what B3 timed) and push
    # (#unset, where the per-arc charge was removed).
    'one-thread': dict(
        cpus=1, workers=1, concurrency=1, fixtures='fixtures',
        participants=BASELINE + ['grust#1', 'grust#unset']
                     + [f'{v}#1' for v in NEXT] + [f'{v}#unset' for v in NEXT]
                     + [f'{EAGER}#1', f'{EAGER}#unset']),
    # What a user of each library gets. Push is sequential by construction and
    # is not repeated here.
    'full-width': dict(
        cpus=16, workers=16, concurrency=16, fixtures='fixtures',
        participants=BASELINE + ['grust'] + NEXT + [EAGER]),
    # The same two runs with the allocator pinned for every participant, to
    # measure rather than assume whose times the threshold moves. Counted only:
    # this probe is about the allocator, not about accounting, and the rows it
    # must be comparable with are the counted ones.
    'pinned-one-thread': dict(
        cpus=1, workers=1, concurrency=1, fixtures='fixtures', env=PINNED,
        participants=BASELINE + ['grust#1', 'grust#unset',
                                 'grust-next@counted#1', 'grust-next@counted#unset']),
    'pinned-full-width': dict(
        cpus=16, workers=16, concurrency=16, fixtures='fixtures', env=PINNED,
        participants=BASELINE + ['grust', 'grust-next@counted']),
    # Above L3: the hoist was never measured where its randomly indexed arrays
    # stop fitting. PageRank only, the kernel the hoist changed, on the two
    # dangling-free families. `fixtures-large` is 2,097,152 nodes, where
    # v0.22.0's two per-node arrays under the random index (32 MB) exceed the
    # 24.8 MB L3 and the later commit's one (16 MB) does not; `fixtures-xlarge`
    # is 4,194,304, where both exceed it. The first is the regime the hoist's
    # own comment predicts it helps most, so it is not run without the second.
    'large-one-thread': dict(
        cpus=1, workers=1, concurrency=1, fixtures='fixtures-large', algorithms=['pagerank'],
        participants=BASELINE + ['grust#1', 'grust#unset']
                     + [f'{v}#1' for v in NEXT] + [f'{v}#unset' for v in NEXT]),
    'large-full-width': dict(
        cpus=16, workers=16, concurrency=16, fixtures='fixtures-large', algorithms=['pagerank'],
        participants=BASELINE + ['grust'] + NEXT),
    'xlarge-one-thread': dict(
        cpus=1, workers=1, concurrency=1, fixtures='fixtures-xlarge', algorithms=['pagerank'],
        participants=BASELINE + ['grust#1', 'grust#unset']
                     + [f'{v}#1' for v in NEXT] + [f'{v}#unset' for v in NEXT]),
    'xlarge-full-width': dict(
        cpus=16, workers=16, concurrency=16, fixtures='fixtures-xlarge', algorithms=['pagerank'],
        participants=BASELINE + ['grust'] + NEXT),
}

# ---- B7: PageRank's score precision --------------------------------------
# B6 found that neo4j-graph, which accumulates and returns f32, stops PageRank
# at a different iteration count from Grust's f64 kernel under the same 1e-8
# tolerance (at hub-65536 one-thread: 28 against 17), so its total time was
# never one kernel's cost against another's. B7 runs Grust's PageRank at f32
# as well (`+f32`, see variants.py), PageRank only, on the two dangling-free
# families at the protocol, large and xlarge sizes, so that each table has the
# iteration count beside the total and a reader can see whether the f32 rows
# stopped where neo4j-graph stopped. Where the counts still differ, the
# per-iteration time is the comparable figure.
#
# Participants: neo4j-graph; grust-next counted and unchecked, at f64 and at
# f32; and v0.22.0 (`grust`) as the anchor, at the pull kernel and at full
# width. The anchor's push loop (`grust#unset`) is left out: at xlarge it is 83
# s a sample, the most expensive row of B6's matrix, it is the one row nothing
# in B7 is compared with, and its per-arc charge was B5's question, not this
# one. `b7_report.py estimate` computes the campaign's expected duration from
# B6's own sample walls; the choice was made on that (see its output).
#
# Protocol as B6: parity first for every fixture set and concurrency, with the
# bits gate in two groups, the f64 builds against v0.22.0 and the f32 builds
# against their own counted row; then the timed runs in this order, one
# warmup and five repeats, idle-checked, watched, steal recorded, the MAD rule
# and the discard rule unchanged. No pinned runs: the allocator was B5's
# question and B6 re-decided it on the counter.
B7_FAMILIES = ['hub', 'uniform']
B7_ALGORITHMS = ['pagerank']
B7_NEXT = ['grust-next@counted', 'grust-next@unchecked']
B7_F32 = [f'{v}+f32' for v in B7_NEXT]
B7_PARITY_PARTICIPANTS = ['neo4j-graph', 'grust'] + B7_NEXT + B7_F32
# One bits group per base: an f32 vector is never bit-identical to an f64 one.
B7_BITS = [['grust', *B7_NEXT], [B7_F32[0], B7_F32[1]]]

def b7_runs():
    runs = {}
    for prefix, fixtures in (('', 'fixtures'), ('large-', 'fixtures-large'), ('xlarge-', 'fixtures-xlarge')):
        common = dict(fixtures=fixtures, algorithms=B7_ALGORITHMS, families=B7_FAMILIES)
        # Both Grust kernels for every grust-next variant, as B6's one-thread
        # runs did; the anchor at the pull kernel alone, for the reason above.
        runs[f'{prefix}one-thread'] = dict(
            cpus=1, workers=1, concurrency=1, **common,
            participants=['neo4j-graph', 'grust#1'] + [f'{v}#1' for v in B7_NEXT + B7_F32]
                         + [f'{v}#unset' for v in B7_NEXT + B7_F32])
        runs[f'{prefix}full-width'] = dict(
            cpus=16, workers=16, concurrency=16, **common,
            participants=['neo4j-graph', 'grust'] + B7_NEXT + B7_F32)
    return runs

PLANS = {
    'b6': dict(parity=PARITY, parity_participants=PARITY_PARTICIPANTS, bits_identical=[['grust', *NEXT]],
               algorithms=None, families=None, runs=RUNS),
    'b7': dict(parity=PARITY, parity_participants=B7_PARITY_PARTICIPANTS, bits_identical=B7_BITS,
               algorithms=B7_ALGORITHMS, families=B7_FAMILIES, runs=b7_runs()),
    # B8: the B7 plan, unchanged, on the commit that fuses the pull kernel's
    # three node passes into one (Grust 2985fac on top of ead3568). Its scores
    # are asserted bit-identical at both precisions, so the same bits gates
    # apply; the outputs carry `b8-` so they sit beside B7's in one directory.
    'b8': dict(parity=PARITY, parity_participants=B7_PARITY_PARTICIPANTS, bits_identical=B7_BITS,
               algorithms=B7_ALGORITHMS, families=B7_FAMILIES, runs=b7_runs()),
    # B9: the same plan again, on the head of the kernel branch stack (Grust
    # 4a9e7f5 over 2985fac): four-byte CSR targets and row bounds, work charged
    # a reduction block at a time rather than a node, PageRank's inner loop
    # without the ArticleRank term, and its non-finite test moved to the block.
    # Every commit in the stack asserts bit-identical scores at both precisions
    # and every width, so the same bits gates apply and B8's rows are the
    # before. The outputs carry `b9-` so all four campaigns sit in one
    # directory.
    'b9': dict(parity=PARITY, parity_participants=B7_PARITY_PARTICIPANTS, bits_identical=B7_BITS,
               algorithms=B7_ALGORITHMS, families=B7_FAMILIES, runs=b7_runs()),
}

# A process outside the run using more than this share of one CPU over a sample
# window is load, whatever its name. The name list above catches a build that
# is starting; this catches everything the list did not think of - it was added
# after a fixture generator in plain python3 passed the name check.
CPU_SHARE = 0.10
TICKS = os.sysconf('SC_CLK_TCK')

def cpu_ticks(container=None):
    """utime+stime per process outside `container`, with its command line."""
    found = {}
    for entry in os.listdir('/proc'):
        if not entry.isdigit(): continue
        try:
            if container and container[:12] in pathlib.Path(f'/proc/{entry}/cgroup').read_text():
                continue
            stat = pathlib.Path(f'/proc/{entry}/stat').read_text()
            fields = stat[stat.rindex(')') + 2:].split()
            command = pathlib.Path(f'/proc/{entry}/cmdline').read_bytes().replace(b'\0', b' ').decode(errors='replace').strip()
            found[entry] = (int(fields[11]) + int(fields[12]), command or stat[stat.index('(') + 1:stat.rindex(')')])
        except (OSError, ValueError, IndexError):
            continue
    return found

def hungry(earlier, later, seconds):
    """Processes that used more than CPU_SHARE of a CPU between two cpu_ticks readings."""
    return [f'{pid} {100 * (ticks - earlier[pid][0]) / TICKS / seconds:.0f}% {command[:120]}'
            for pid, (ticks, command) in later.items()
            if pid in earlier and SELF.search(command) is None
            and (ticks - earlier[pid][0]) / TICKS / seconds > CPU_SHARE]

def container_ids():
    out = subprocess.run(['docker', 'ps', '-q', '--no-trunc'], capture_output=True, text=True)
    return [line for line in out.stdout.split() if line]

def busy_processes(container=None, own=None):
    """Command lines of processes that make the host not idle.

    A process inside `container` is the run itself and is excluded; any other
    container's process is not, since a second container is a second workload.
    """
    found = []
    for entry in os.listdir('/proc'):
        if not entry.isdigit(): continue
        try:
            command = pathlib.Path(f'/proc/{entry}/cmdline').read_bytes().replace(b'\0', b' ').decode(errors='replace').strip()
            if container and container[:12] in pathlib.Path(f'/proc/{entry}/cgroup').read_text():
                continue
        except OSError:
            continue
        # `own` is this run's docker client, whose command line names run.py or
        # parity.py; it waits on the container and is not a second workload.
        if own and own in command: continue
        if command and BUSY.search(command) and not SELF.search(command):
            found.append(f'{entry} {command[:160]}')
    return found

def snapshot(container=None, window=2.0):
    earlier = cpu_ticks(container)
    time.sleep(window)
    with open('/proc/stat') as handle:
        steal = int(handle.readline().split()[8])
    others = [c for c in container_ids() if c != container]
    later = cpu_ticks(container)
    return dict(at=time.strftime('%Y-%m-%dT%H:%M:%S%z'), loadavg=pathlib.Path('/proc/loadavg').read_text().split()[:3],
                steal_ticks=steal, busy=busy_processes(container), other_containers=others,
                hungry=hungry(earlier, later, window),
                resident_sessions=[f'{pid} {command[:120]}' for pid, (_, command) in later.items()
                                   if RESIDENT.search(command) and not SELF.search(command)])

def idle(state):
    return not state['busy'] and not state['other_containers'] and not state['hungry']

class Watcher(threading.Thread):
    def __init__(self, name):
        super().__init__(daemon=True)
        self.name_, self.sightings, self.container, self.done = name, [], None, threading.Event()
        # Agent sessions seen at any point of the run, at any CPU. Recorded so
        # the run's record says whether one was resident rather than leaving it
        # to be reconstructed later; the discard rule is CPU, not this.
        self.residents = set()
    def run(self):
        earlier, then = None, time.time()
        while not self.done.wait(1.0):
            if self.container is None:
                ids = subprocess.run(['docker', 'ps', '-q', '--no-trunc', '--filter', f'name={self.name_}'],
                                     capture_output=True, text=True).stdout.split()
                self.container = ids[0] if ids else None
                continue
            # Until the container id is known its processes cannot be told
            # apart from anyone else's, so CPU is only judged after that.
            busy = busy_processes(self.container, own=f'--name {self.name_} ')
            others = [c for c in container_ids() if c != self.container]
            later, now = cpu_ticks(self.container), time.time()
            for pid, (_, command) in later.items():
                if RESIDENT.search(command) and not SELF.search(command):
                    self.residents.add(f'{pid} {command[:120]}')
            # docker run itself and the containerd shim do a little work for the
            # run; they are part of it, not a second workload.
            eaten = [h for h in hungry(earlier, later, now - then)
                     if not re.search(r'docker|containerd', h)] if earlier else []
            earlier, then = later, now
            if busy or others or eaten:
                self.sightings.append(dict(at=time.strftime('%H:%M:%S'), busy=busy,
                                           other_containers=others, hungry=eaten))

def docker(image, work, name, cpus, command, env=None):
    cpu = ['--cpus', str(cpus)] if cpus else []
    # Environment is set for the whole container, so every participant in the
    # run gets it; a run either pins the allocator for all of them or for none.
    settings = [flag for key, value in (env or {}).items() for flag in ('-e', f'{key}={value}')]
    return ['docker', 'run', '--rm', '--name', name, *cpu, *settings, '-v', f'{work}:/work', image, *command]

def guarded(name, command, record, nonzero_ok=False):
    """Run one docker invocation between two idle checks, watched throughout."""
    before = snapshot()
    record.update(name=name, command=command, before=before)
    if not idle(before):
        record.update(status='not started: host busy')
        return False
    watcher = Watcher(command[command.index('--name') + 1])
    watcher.start()
    started = time.time()
    result = subprocess.run(command)
    watcher.done.set(); watcher.join()
    after = snapshot()
    record.update(after=after, seconds=round(time.time() - started, 1), exit=result.returncode,
                  sightings=watcher.sightings, resident_sessions=sorted(watcher.residents),
                  steal_ticks=after['steal_ticks'] - before['steal_ticks'])
    shared = bool(watcher.sightings) or not idle(after)
    record['status'] = ('failed' if result.returncode and not nonzero_ok else
                        'DISCARDED: host shared during the run' if shared else 'clean')
    return record['status'] == 'clean'

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('stage', choices=['idle', 'parity', 'timed', 'plan'])
    p.add_argument('--plan', choices=list(PLANS), default='b6', help='which matrix; see PLANS')
    p.add_argument('--width', type=int,
                   help='a host narrower than 16 CPUs: its full-width runs and the widest parity configuration '
                        'take this width instead, and are named by it, so a file never claims a width the host '
                        'did not have. Never used on the measuring host.')
    p.add_argument('--image', required=False)
    p.add_argument('--work', type=pathlib.Path, help='host directory mounted at /work: fixtures, parity, timed')
    p.add_argument('--runs', nargs='+', help='default: every run of the plan, in its order')
    p.add_argument('--configs', nargs='+', help='default: every parity configuration of the plan')
    p.add_argument('--fixtures', default='fixtures', help='parity: the fixture directory under --work')
    p.add_argument('--algorithms', nargs='+')
    p.add_argument('--repeats', type=int, default=5)
    p.add_argument('--warmups', type=int, default=1)
    p.add_argument('--only-fixture', help='dry run: time only fixtures matching this glob')
    p.add_argument('--tag', default='', help='suffix for output names, e.g. dry')
    a = p.parse_args()
    plan = PLANS[a.plan]
    if a.width:
        # The plan is data; a narrower host gets the same plan with 16 read as
        # its own width, in the parity configurations and in the runs alike.
        parity = {('unset' if v['concurrency'] is None else str(a.width if v['concurrency'] == 16 else v['concurrency'])): v
                  for k, v in plan['parity'].items()}
        for v in parity.values():
            if v['concurrency'] == 16: v['concurrency'] = a.width
        runs_ = {}
        for name, spec in plan['runs'].items():
            spec = dict(spec)
            if spec['cpus'] == 16: spec.update(cpus=a.width, workers=a.width, concurrency=a.width)
            runs_[name] = spec
        plan = dict(plan, parity=parity, runs=runs_, width=a.width)
    runs, configs = a.runs or list(plan['runs']), a.configs or list(plan['parity'])
    algorithms = a.algorithms or plan['algorithms']
    # B6's names stay exactly what they were; any other plan's carry its name.
    prefix = '' if a.plan == 'b6' else f'{a.plan}-'

    if a.stage == 'idle':
        state = snapshot()
        print(json.dumps(state, indent=1))
        return 0 if idle(state) else 1
    if a.stage == 'plan':
        print(json.dumps(dict(plan=a.plan, **plan), indent=1))
        return 0

    log = a.work/f'campaign-{a.plan}{a.tag}.jsonl' if prefix else a.work/f'campaign{a.tag}.jsonl'
    ok = True
    if a.stage == 'parity':
        (a.work/'parity').mkdir(exist_ok=True)
        for config in configs:
            concurrency = plan['parity'][config]['concurrency']
            output = f'/work/parity/parity-{prefix}{a.fixtures}-{config}{a.tag}.json'
            command = ['python3', '/opt/bench/parity.py', '--fixtures', f'/work/{a.fixtures}',
                       '--reference-cache', '/work/reference-cache',
                       '--participants', *plan['parity_participants'], '--output', output]
            for group in plan['bits_identical']: command += ['--bits-identical', *group]
            if plan['families']: command += ['--families', *plan['families']]
            if algorithms: command += ['--algorithms', *algorithms]
            if concurrency is not None: command += ['--concurrency', str(concurrency)]
            record = {}
            # Parity is not timed, so it needs no quota, but it still runs on an
            # idle host: it is the gate, and a gate run beside a build is a gate
            # nobody can vouch for.
            # parity.py exits 1 whenever any row mismatches, and four known
            # neo4j-graph rows always do; its verdict is the file, not the code.
            guarded(f'parity-{prefix}{config}', docker(a.image, a.work, f'parity-{prefix}{config}', None, command),
                    record, nonzero_ok=True)
            with log.open('a') as out: out.write(json.dumps(record)+'\n')
            print(f"parity {config}: {record['status']}", flush=True)
            ok &= record['status'] == 'clean'
        return 0 if ok else 1

    (a.work/'timed').mkdir(exist_ok=True)
    for run in runs:
        spec = plan['runs'][run]
        fixtures = f"/work/{spec['fixtures']}"
        if a.only_fixture:
            # A dry run copies one fixture into its own directory rather than
            # teaching run.py a filter nobody uses for real.
            dry = a.work/f"dry-{spec['fixtures']}"
            dry.mkdir(exist_ok=True)
            for old in dry.glob('*.edges'): old.unlink()
            for source in (a.work/spec['fixtures']).glob(a.only_fixture):
                (dry/source.name).write_bytes(source.read_bytes())
            fixtures = f'/work/{dry.name}'
        concurrencies = sorted({'unset' if '#unset' in name else (name.split('#')[1] if '#' in name else str(spec['concurrency']))
                                for name in spec['participants'] if name.startswith('grust')} | {str(spec['concurrency'])})
        parity_files = [f"/work/parity/parity-{prefix}{spec['fixtures']}-{c}.json" for c in concurrencies]
        output = f'/work/timed/{prefix}{run}{a.tag}.json'
        command = ['python3', '/opt/bench/run.py', '--fixtures', fixtures,
                   '--participants', *spec['participants'], '--parity', *parity_files,
                   '--concurrency', str(spec['concurrency']), '--workers', str(spec['workers']),
                   '--warmups', str(a.warmups), '--repeats', str(a.repeats),
                   '--label', f'{prefix}{run}{a.tag}', '--output', output]
        if spec.get('algorithms') or a.algorithms:
            command += ['--algorithms', *(a.algorithms or spec['algorithms'])]
        if spec.get('families'): command += ['--families', *spec['families']]
        record = {}
        guarded(f'{prefix}{run}', docker(a.image, a.work, f'timed-{prefix}{run}', spec['cpus'], command,
                                          spec.get('env')), record)
        record.update(run=run, plan=a.plan, cpus=spec['cpus'], env=spec.get('env'))
        if record['status'].startswith('DISCARDED'):
            produced = a.work/'timed'/f'{prefix}{run}{a.tag}.json'
            if produced.exists(): produced.rename(produced.with_suffix('.discarded.json'))
        with log.open('a') as out: out.write(json.dumps(record)+'\n')
        print(f"{run}: {record['status']}, {record.get('seconds')}s, steal {record.get('steal_ticks')} ticks, "
              f"{len(record.get('sightings', []))} sightings", flush=True)
        ok &= record['status'] == 'clean'
    return 0 if ok else 1

if __name__ == '__main__': sys.exit(main())
