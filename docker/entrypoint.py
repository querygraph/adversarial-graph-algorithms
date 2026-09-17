"""Collect provenance and retain terminal status even when validation aborts."""
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback

ROOT = Path('/opt/benchmark')
WORK = Path('/work')


def main():
    for directory in ['results', 'data']:
        (WORK/directory).mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, BENCH_RESULTS_DIR=str(WORK/'results'), BENCH_DATA_DIR=str(WORK/'data'))
    args = sys.argv[1:]
    label = 'docker-neo4j'
    for i, arg in enumerate(args):
        if arg == '--label' and i+1 < len(args): label = args[i+1]
        elif arg.startswith('--label='): label = arg.split('=', 1)[1]
    if not label or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in label):
        raise SystemExit('Invalid label')
    # Exclusive reservation prevents stale results and audit logs from being pooled.
    reservation = WORK/'results'/f'{label}-status.json'
    status = dict(status='running', args=args, started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    with reservation.open('x') as f:
        json.dump(status, f, indent=2)
    try:
        provenance = {'environment': {k: v for k, v in os.environ.items() if k.startswith('BENCH_')}}
        for name in ['sources.json', 'rust-version.txt', 'upstream-rust-version.txt', 'cpp-version.txt', 'packages.txt', 'build-receipt.json', 'cypher-validation.json', 'upstream-validation.json']:
            if (ROOT/name).exists(): provenance[name] = (ROOT/name).read_text()
        for name in ['/sys/fs/cgroup/cpu.max', '/sys/fs/cgroup/memory.max', '/proc/cpuinfo', '/proc/loadavg', '/proc/stat']:
            if Path(name).exists(): provenance[name] = Path(name).read_text()
        (WORK/'results'/f'{label}-environment.json').write_text(json.dumps(provenance, indent=2)+'\n')
        command = [sys.executable, str(ROOT/'neo4j/compare.py'), '--include-grustcat', '--include-grustcat-cypher', '--label', label]+args
        result = subprocess.run(command, env=env)
        status.update(status='pass' if result.returncode == 0 else 'failed', exit_code=result.returncode)
    except BaseException:
        status.update(status='error', error=traceback.format_exc())
        raise
    finally:
        status['finished_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        status['host_load_end'] = Path('/proc/loadavg').read_text()
        status['host_cpu_end'] = Path('/proc/stat').read_text()
        reservation.write_text(json.dumps(status, indent=2)+'\n')
    output = WORK/'results'/f'{label}.json'
    if output.exists():
        report = subprocess.run([sys.executable, str(ROOT/'docker/report.py'), str(output)])
        if report.returncode and result.returncode == 0: return report.returncode
    return result.returncode


if __name__ == '__main__':
    raise SystemExit(main())
