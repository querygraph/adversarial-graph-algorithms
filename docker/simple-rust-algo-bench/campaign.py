#!/usr/bin/env python3
"""The rerun's host-side driver: parity, then timed runs, each on an idle host.

Runs on the measuring host, outside the image, because the checks it makes are
about the host and a container cannot see them:

- **Idle before and after every run.** No cargo, rustc, perf, other benchmark
  or other container may be running. A run that starts on a busy host is not
  started; a run that ends on one is marked discarded.
- **Watched during every run.** A sampler looks for the same processes once a
  second for the whole run, outside the run's own container, because a build
  that starts and finishes between the two checks would pass both. Any sighting
  discards the run. The sampler reads /proc and nothing else.
- **Steal** is read by run.py per cell and over the run; this records it again
  over the whole docker invocation, and the load average at both ends.

A discarded run's output is kept, renamed, and never published: the operator
decides whether to rerun it. Nothing here retries on its own, because a retry
loop on a shared host selects for the quiet moments and reports them as typical.

The matrix is data, in RUNS below, so the plan and the run are one artifact.
"""
import argparse, json, os, pathlib, re, subprocess, sys, threading, time

HERE = pathlib.Path(__file__).resolve().parent

# Processes whose presence means the host is not idle. Matched against the
# full command line of every process outside the run's own container.
BUSY = re.compile(r'(^|[/ ])(cargo|rustc|perf|cc1plus|ld\.lld|mold|bench-[\w-]+|icebug|'
                  r'run\.py|parity\.py|criterion|hyperfine|stress|yes)( |$)')
# Our own watcher and this driver are python3 campaign.py; never count them.
SELF = re.compile(r'campaign\.py')

BASELINE = ['neo4j-graph', 'icebug', 'icecat', 'grustcat']
MODES = ['counted', 'work-uncounted', 'unchecked']
NEXT = [f'grust-next@{mode}' for mode in MODES]

# Parity: one file per concurrency, every variant that any timed run uses.
# `--bits-identical` makes a grust-next PageRank that differs from v0.22.0 by a
# single bit a mismatch, so it is never timed.
PARITY = {
    'unset': dict(concurrency=None),
    '1': dict(concurrency=1),
    '16': dict(concurrency=16),
}
PARITY_PARTICIPANTS = BASELINE + ['grust'] + NEXT

# Timed runs. `#N`/`#unset` fixes a Grust variant's kernel (see variants.py).
RUNS = {
    # The kernel comparison and the only valid lineage comparison, as in B3,
    # with both Grust PageRank kernels: pull (#1, what B3 timed) and push
    # (#unset, where the per-arc charge was removed).
    'one-thread': dict(
        cpus=1, workers=1, concurrency=1, fixtures='fixtures',
        participants=BASELINE + ['grust#1', 'grust#unset']
                     + [f'{v}#1' for v in NEXT] + [f'{v}#unset' for v in NEXT]),
    # What a user of each library gets. Push is sequential by construction and
    # is not repeated here.
    'full-width': dict(
        cpus=16, workers=16, concurrency=16, fixtures='fixtures',
        participants=BASELINE + ['grust'] + NEXT),
    # Above L3: the hoist was never measured where its randomly indexed arrays
    # stop fitting. PageRank only, the kernel the hoist changed.
    'large-one-thread': dict(
        cpus=1, workers=1, concurrency=1, fixtures='fixtures-large', algorithms=['pagerank'],
        participants=BASELINE + ['grust#1', 'grust#unset']
                     + [f'{v}#1' for v in NEXT] + [f'{v}#unset' for v in NEXT]),
    'large-full-width': dict(
        cpus=16, workers=16, concurrency=16, fixtures='fixtures-large', algorithms=['pagerank'],
        participants=BASELINE + ['grust'] + NEXT),
}

def container_ids():
    out = subprocess.run(['docker', 'ps', '-q', '--no-trunc'], capture_output=True, text=True)
    return [line for line in out.stdout.split() if line]

def busy_processes(container=None):
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
        if command and BUSY.search(command) and not SELF.search(command):
            found.append(f'{entry} {command[:160]}')
    return found

def snapshot(container=None):
    with open('/proc/stat') as handle:
        steal = int(handle.readline().split()[8])
    others = [c for c in container_ids() if c != container]
    return dict(at=time.strftime('%Y-%m-%dT%H:%M:%S%z'), loadavg=pathlib.Path('/proc/loadavg').read_text().split()[:3],
                steal_ticks=steal, busy=busy_processes(container), other_containers=others)

def idle(state):
    return not state['busy'] and not state['other_containers']

class Watcher(threading.Thread):
    def __init__(self, name):
        super().__init__(daemon=True)
        self.name_, self.sightings, self.container, self.done = name, [], None, threading.Event()
    def run(self):
        while not self.done.wait(1.0):
            if self.container is None:
                ids = subprocess.run(['docker', 'ps', '-q', '--no-trunc', '--filter', f'name={self.name_}'],
                                     capture_output=True, text=True).stdout.split()
                self.container = ids[0] if ids else None
            busy = busy_processes(self.container)
            others = [c for c in container_ids() if c != self.container] if self.container else []
            if busy or others:
                self.sightings.append(dict(at=time.strftime('%H:%M:%S'), busy=busy, other_containers=others))

def docker(image, work, name, cpus, command):
    cpu = ['--cpus', str(cpus)] if cpus else []
    return ['docker', 'run', '--rm', '--name', name, *cpu, '-v', f'{work}:/work', image, *command]

def guarded(name, command, record):
    """Run one docker invocation between two idle checks, watched throughout."""
    before = snapshot()
    record.update(name=name, command=command, before=before)
    if not idle(before):
        record.update(status='not started: host busy')
        return False
    watcher = Watcher(name)
    watcher.start()
    started = time.time()
    result = subprocess.run(command)
    watcher.done.set(); watcher.join()
    after = snapshot()
    record.update(after=after, seconds=round(time.time() - started, 1), exit=result.returncode,
                  sightings=watcher.sightings,
                  steal_ticks=after['steal_ticks'] - before['steal_ticks'])
    shared = bool(watcher.sightings) or not idle(after)
    record['status'] = ('failed' if result.returncode else
                        'DISCARDED: host shared during the run' if shared else 'clean')
    return record['status'] == 'clean'

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('stage', choices=['idle', 'parity', 'timed', 'plan'])
    p.add_argument('--image', required=False)
    p.add_argument('--work', type=pathlib.Path, help='host directory mounted at /work: fixtures, parity, timed')
    p.add_argument('--runs', nargs='+', default=list(RUNS))
    p.add_argument('--configs', nargs='+', default=list(PARITY))
    p.add_argument('--fixtures', default='fixtures', help='parity: the fixture directory under --work')
    p.add_argument('--algorithms', nargs='+')
    p.add_argument('--repeats', type=int, default=5)
    p.add_argument('--warmups', type=int, default=1)
    p.add_argument('--only-fixture', help='dry run: time only fixtures matching this glob')
    p.add_argument('--tag', default='', help='suffix for output names, e.g. dry')
    a = p.parse_args()

    if a.stage == 'idle':
        state = snapshot()
        print(json.dumps(state, indent=1))
        return 0 if idle(state) else 1
    if a.stage == 'plan':
        print(json.dumps(dict(parity=PARITY, parity_participants=PARITY_PARTICIPANTS, runs=RUNS), indent=1))
        return 0

    log = a.work/f'campaign{a.tag}.jsonl'
    ok = True
    if a.stage == 'parity':
        (a.work/'parity').mkdir(exist_ok=True)
        for config in a.configs:
            concurrency = PARITY[config]['concurrency']
            output = f'/work/parity/parity-{a.fixtures}-{config}{a.tag}.json'
            command = ['python3', '/opt/bench/parity.py', '--fixtures', f'/work/{a.fixtures}',
                       '--participants', *PARITY_PARTICIPANTS, '--bits-identical', 'grust', *NEXT,
                       '--output', output]
            if a.algorithms: command += ['--algorithms', *a.algorithms]
            if concurrency is not None: command += ['--concurrency', str(concurrency)]
            record = {}
            # Parity is not timed, so it needs no quota, but it still runs on an
            # idle host: it is the gate, and a gate run beside a build is a gate
            # nobody can vouch for.
            guarded(f'parity-{config}', docker(a.image, a.work, f'parity-{config}', None, command), record)
            with log.open('a') as out: out.write(json.dumps(record)+'\n')
            print(f"parity {config}: {record['status']}", flush=True)
            ok &= record['status'] == 'clean'
        return 0 if ok else 1

    (a.work/'timed').mkdir(exist_ok=True)
    for run in a.runs:
        spec = RUNS[run]
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
        parity_files = [f"/work/parity/parity-{spec['fixtures']}-{c}.json" for c in concurrencies]
        output = f'/work/timed/{run}{a.tag}.json'
        command = ['python3', '/opt/bench/run.py', '--fixtures', fixtures,
                   '--participants', *spec['participants'], '--parity', *parity_files,
                   '--concurrency', str(spec['concurrency']), '--workers', str(spec['workers']),
                   '--warmups', str(a.warmups), '--repeats', str(a.repeats),
                   '--label', f'{run}{a.tag}', '--output', output]
        if spec.get('algorithms') or a.algorithms:
            command += ['--algorithms', *(a.algorithms or spec['algorithms'])]
        record = {}
        guarded(run, docker(a.image, a.work, f'timed-{run}', spec['cpus'], command), record)
        record.update(run=run, cpus=spec['cpus'])
        if record['status'].startswith('DISCARDED'):
            produced = a.work/'timed'/f'{run}{a.tag}.json'
            if produced.exists(): produced.rename(produced.with_suffix('.discarded.json'))
        with log.open('a') as out: out.write(json.dumps(record)+'\n')
        print(f"{run}: {record['status']}, {record.get('seconds')}s, steal {record.get('steal_ticks')} ticks, "
              f"{len(record.get('sightings', []))} sightings", flush=True)
        ok &= record['status'] == 'clean'
    return 0 if ok else 1

if __name__ == '__main__': sys.exit(main())
