#!/usr/bin/env python3
"""Stage a build context for the image and build it, recording what went in.

The image needs three trees that live outside this directory — Grust, Icecat and
the participants — and Docker will not follow symlinks out of a context. They
are hardlinked in, which costs no space on one filesystem, and each tree's
commit is recorded so the image can say what it was built from.

A Grust tree may instead be named by commit: `--grust-next-commit SHA` stages
`git archive SHA` from the repository at `--grust-next`, so the tree in the
image is that commit and nothing else, whatever the checkout there has on
disk. `--grust-commit` does the same for the release. A commit that the
repository does not have is refused rather than fetched.
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

def archive(repository, ref, destination):
    """Stage exactly one commit of a repository, and return what it resolved to."""
    resolved = subprocess.run(['git', '-C', str(repository), 'rev-parse', '--verify', f'{ref}^{{commit}}'],
                              capture_output=True, text=True)
    if resolved.returncode:
        raise SystemExit(f'{repository} has no commit {ref}: fetch it first ({resolved.stderr.strip()})')
    sha = resolved.stdout.strip()
    destination.mkdir(parents=True, exist_ok=True)
    tar = subprocess.run(['git', '-C', str(repository), 'archive', '--format=tar', sha],
                         capture_output=True, check=True)
    subprocess.run(['tar', '-x', '-C', str(destination)], input=tar.stdout, check=True)
    return dict(commit=sha, uncommitted='', staged=f'git archive {ref} from {repository}')

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
    p.add_argument('--grust-next', type=pathlib.Path, default=HERE.parents[2]/'grust-next',
                   help='the Grust commit under test, linked by the grust-next participant; '
                        '--grust stays the published release it is compared against')
    p.add_argument('--grust-commit', metavar='REF',
                   help='stage this commit of the repository at --grust instead of its working tree')
    p.add_argument('--grust-next-commit', metavar='REF',
                   help='stage this commit of the repository at --grust-next instead of its working tree')
    p.add_argument('--icecat', type=pathlib.Path, default=HERE.parents[2]/'icecat')
    p.add_argument('--allow-dirty', action='store_true',
                   help='stage trees with uncommitted changes; the commit stamped into a '
                        'binary then does not describe it, so the default refuses')
    p.add_argument('--context', type=pathlib.Path, required=True)
    p.add_argument('--tag', default='simple-rust-algo-bench:local')
    p.add_argument('--jobs', type=int, default=4)
    a = p.parse_args()
    # prepare.py learned this the same way: a clone without submodules configures
    # for minutes and then fails on a message that reads like a CMake problem.
    tlx = a.icecat.resolve()/'extlibs/tlx/CMakeLists.txt'
    if not tlx.exists():
        raise SystemExit(f'Initialize Icecat submodules first: git -C {a.icecat} submodule update --init --recursive')
    if a.context.exists(): shutil.rmtree(a.context)
    a.context.mkdir(parents=True)
    # A tree named by commit is archived, so it cannot be dirty; a tree taken
    # from disk is checked, because its commit must describe it.
    trees = dict(grust=(archive(a.grust.resolve(), a.grust_commit, a.context/'grust') if a.grust_commit
                        else commit(a.grust.resolve())),
                 grust_next=(archive(a.grust_next.resolve(), a.grust_next_commit, a.context/'grust-next')
                             if a.grust_next_commit else commit(a.grust_next.resolve())),
                 icecat=commit(a.icecat.resolve()), bench=commit(HERE))
    dirty = [name for name, tree in trees.items() if tree['uncommitted']]
    if dirty and not a.allow_dirty:
        raise SystemExit(f'uncommitted changes in {", ".join(dirty)}: a binary stamped with a commit '
                         'must be built from that commit')
    if trees['grust']['commit'] == trees['grust_next']['commit']:
        print('warning: grust and grust-next are the same commit', file=sys.stderr)
    if not a.grust_commit: stage(a.grust.resolve(), a.context/'grust')
    if not a.grust_next_commit: stage(a.grust_next.resolve(), a.context/'grust-next')
    stage(a.icecat.resolve(), a.context/'icecat')
    stage(HERE, a.context/'bench', skip=('.git', 'target', '__pycache__', 'context'))
    shutil.copy2(HERE/'Dockerfile', a.context/'Dockerfile')
    (a.context/'sources.json').write_text(json.dumps(trees, indent=1)+'\n')
    command = ['docker', 'build', '-t', a.tag,
               '--build-arg', f'BUILD_JOBS={a.jobs}',
               '--build-arg', f'ICEBUG_COMMIT={trees["icecat"]["commit"][:12]}',
               '--build-arg', 'ICEBUG_VERSION=icecat-cpp',
               '--build-arg', f'BENCH_COMMIT={trees["bench"]["commit"][:12]}',
               '--build-arg', f'GRUST_COMMIT={trees["grust"]["commit"]}',
               '--build-arg', f'GRUST_NEXT_COMMIT={trees["grust_next"]["commit"]}',
               str(a.context)]
    print(' '.join(command), flush=True)
    raise SystemExit(subprocess.run(command).returncode)

if __name__ == '__main__': main()
