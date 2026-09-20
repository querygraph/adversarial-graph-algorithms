#!/usr/bin/env python3
"""Stage a build context for the image and build it, recording what went in.

The image needs three trees that live outside this directory — Grust, Icecat and
the participants — and Docker will not follow symlinks out of a context. They
are hardlinked in, which costs no space on one filesystem, and each tree's
commit is recorded so the image can say what it was built from.
"""
import argparse, json, pathlib, shutil, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent

def commit(tree):
    try:
        out = subprocess.run(['git', '-C', str(tree), 'rev-parse', 'HEAD'], capture_output=True, text=True)
        dirty = subprocess.run(['git', '-C', str(tree), 'status', '--porcelain'], capture_output=True, text=True)
        return dict(commit=(out.stdout or '').strip() or 'unknown', uncommitted=(dirty.stdout or ''))
    except OSError:
        return dict(commit='unknown', uncommitted='')

def stage(source, destination, skip=('.git', 'target', '__pycache__')):
    destination.mkdir(parents=True, exist_ok=True)
    for child in source.iterdir():
        if child.name in skip: continue
        target = destination/child.name
        if child.is_dir(): stage(child, target, skip)
        else:
            if target.exists(): target.unlink()
            try: target.hardlink_to(child)
            except OSError: shutil.copy2(child, target)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--grust', type=pathlib.Path, default=HERE.parents[2]/'grust')
    p.add_argument('--icecat', type=pathlib.Path, default=HERE.parents[2]/'icecat')
    p.add_argument('--context', type=pathlib.Path, required=True)
    p.add_argument('--tag', default='simple-rust-algo-bench:local')
    p.add_argument('--jobs', type=int, default=4)
    a = p.parse_args()
    if a.context.exists(): shutil.rmtree(a.context)
    a.context.mkdir(parents=True)
    trees = dict(grust=commit(a.grust.resolve()), icecat=commit(a.icecat.resolve()), bench=commit(HERE))
    stage(a.grust.resolve(), a.context/'grust')
    stage(a.icecat.resolve(), a.context/'icecat')
    stage(HERE, a.context/'bench', skip=('.git', 'target', '__pycache__', 'context'))
    shutil.copy2(HERE/'Dockerfile', a.context/'Dockerfile')
    (a.context/'sources.json').write_text(json.dumps(trees, indent=1)+'\n')
    command = ['docker', 'build', '-t', a.tag,
               '--build-arg', f'BUILD_JOBS={a.jobs}',
               '--build-arg', f'ICEBUG_COMMIT={trees["icecat"]["commit"][:12]}',
               '--build-arg', 'ICEBUG_VERSION=icecat-cpp',
               str(a.context)]
    print(' '.join(command), flush=True)
    raise SystemExit(subprocess.run(command).returncode)

if __name__ == '__main__': main()
