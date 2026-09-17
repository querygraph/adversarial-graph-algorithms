#!/usr/bin/env python3
"""One command to stage, build, validate and run current Grust plus Turso."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--upstream-grust', type=Path, required=True)
    p.add_argument('--turso', type=Path, required=True)
    allocator = p.add_mutually_exclusive_group()
    allocator.add_argument('--allocator', choices=['system', 'mimalloc'], default='mimalloc')
    allocator.add_argument('--mimalloc', dest='allocator', action='store_const', const='mimalloc', help='Build current participants with the mimalloc global allocator')
    p.add_argument('--profile', choices=['default', 'thin'], default='default')
    p.add_argument('--lockfile', type=Path)
    p.add_argument('--output', type=Path)
    p.add_argument('benchmark_args', nargs=argparse.REMAINDER)
    a = p.parse_args()
    args = a.benchmark_args
    if args[:1] == ['--']: args = args[1:]
    if not args: args = ['--full-path', '--sizes', '128', '1024', '--warmups', '1', '--repeats', '5', '--label', 'current']
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    output = (a.output or ROOT/'docker-results'/stamp).resolve()
    output.mkdir(parents=True, exist_ok=False)
    context = output/'context'
    frozen = output/'frozen-context'
    project = 'algorithms-'+uuid.uuid4().hex[:12]
    env = dict(os.environ, BENCH_CONTEXT=str(context), BENCH_OUTPUT=str(output),
               BENCH_IMAGE=project+':local', BENCH_NEO4J_IMAGE=project+'-neo4j:local')
    compose = ['docker', 'compose', '-f', str(ROOT/'compose.yaml'), '-p', project]
    receipt = dict(status='running', argv=sys.argv, host=os.uname().nodename, output=str(output))
    (output/'run.json').write_text(json.dumps(receipt, indent=2)+'\n')
    def run(command, log):
        print(f'{log}: {output/log}', flush=True)
        with (output/log).open('w') as stream:
            result = subprocess.run(command, cwd=ROOT, env=env, stdout=stream, stderr=subprocess.STDOUT)
        if result.returncode: raise subprocess.CalledProcessError(result.returncode, command)
    try:
        run([sys.executable, 'docker/prepare.py', '--output', str(frozen)], 'prepare.log')
        stage = [sys.executable, 'docker/stage_upstream.py', '--grust', str(a.upstream_grust.resolve()),
                 '--turso', str(a.turso.resolve()), '--frozen-context', str(frozen), '--output', str(context),
                 '--allocator', a.allocator, '--profile', a.profile]
        if a.lockfile: stage += ['--lockfile', str(a.lockfile.resolve())]
        run(stage, 'stage.log')
        if not a.lockfile:
            run(['docker', 'run', '--rm', '-v', f'{context}:/src', '-w', '/src/grust-upstream',
                 'rust:1.97.1-bookworm', 'cargo', 'update', '--workspace'], 'resolve.log')
        # Preserve the resolved lock and hash it before the locked build.
        lock = context/'grust-upstream/Cargo.lock'
        (output/'upstream-Cargo.lock').write_bytes(lock.read_bytes())
        hashes = json.loads((context/'sources.json').read_text())
        hashes['grust-upstream/Cargo.lock'] = hashlib.sha256(lock.read_bytes()).hexdigest()
        (context/'sources.json').write_text(json.dumps(hashes, indent=2)+'\n')
        run(compose+['build'], 'build.log')
        run(compose+['up', '-d', '--wait', 'neo4j'], 'neo4j-start.log')
        run(['docker', 'version', '--format', '{{json .Server}}'], 'docker-engine.json')
        run(['docker', 'image', 'inspect', env['BENCH_IMAGE'], env['BENCH_NEO4J_IMAGE']], 'docker-images.json')
        print(f'Running; evidence: {output}', flush=True)
        run(compose+['run', '--rm', '--user', f'{os.getuid()}:{os.getgid()}', 'benchmark']+args, 'benchmark.log')
        receipt['status'] = 'pass'
    except BaseException as error:
        receipt.update(status='error', error=str(error))
        raise
    finally:
        (output/'run.json').write_text(json.dumps(receipt, indent=2)+'\n')
        with (output/'neo4j.log').open('w') as log:
            subprocess.run(compose+['logs', '--no-color', 'neo4j'], cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT, check=False)
        subprocess.run(compose+['down'], cwd=ROOT, env=env, check=False)
    print(output)


if __name__ == '__main__': main()
