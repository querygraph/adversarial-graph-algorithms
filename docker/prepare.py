"""Stage only build sources from the three sibling checkouts, with provenance."""
import argparse
import hashlib
import json
import shutil
import tarfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IGNORE = shutil.ignore_patterns('.git', 'target', '__pycache__', '.venv', '*.pyc')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--icecat', type=Path, default=ROOT.parent/'icecat')
    p.add_argument('--grust', type=Path, default=ROOT.parent/'grust')
    p.add_argument("--local", action="store_true", help="Stage current sibling checkouts instead of the published measured snapshot")
    p.add_argument('--output', type=Path, help='New isolated context directory; refuses an existing path')
    a = p.parse_args()
    dest = a.output or ROOT/'.docker-context'
    if a.output and dest.exists(): p.error('--output must not exist')
    if not a.local and not (ROOT/'publication/measured-source.tar.gz').exists():
        p.error('Frozen snapshot missing; use --local explicitly for development sources')
    if dest.exists(): shutil.rmtree(dest)
    dest.mkdir()
    def copy(source, target):
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir(): shutil.copytree(source, target, ignore=IGNORE)
        else: shutil.copy2(source, target)
    snapshot = ROOT/'publication/measured-source.tar.gz'
    if snapshot.exists() and not a.local:
        receipt=json.loads((ROOT/'publication/source.json').read_text())
        if hashlib.sha256(snapshot.read_bytes()).hexdigest()!=receipt['sha256']:
            raise SystemExit('Measured source checksum mismatch')
        with tarfile.open(snapshot,'r:gz') as archive:
            archive.extractall(dest, filter='data')
        print('Using published measured source snapshot',flush=True)
    else:
        for name in ['CMakeLists.txt','networkit.pc','include','networkit','extlibs','rust']:
            if name == 'rust':
                for child in ['Cargo.toml','Cargo.lock','rust-toolchain.toml','README.md','LICENSE','crates']:
                    copy(a.icecat/name/child, dest/'icecat'/name/child)
            else: copy(a.icecat/name,dest/'icecat'/name)
        for name in ['Cargo.toml','Cargo.lock','README.md','crates','examples']:
            copy(a.grust/name,dest/'grust'/name)
        for name in ['Cargo.toml','Cargo.lock','rust-toolchain.toml','legacy.cpp','src','bench.py','compare_grustcat.py','check_arrow.py','check_cypher.py','neo4j/compare.py','neo4j/requirements.txt','neo4j/downloads.json','neo4j/user-logs.xml','neo4j/server-logs.xml']:
            copy(ROOT/name,dest/'benchmark'/name)
        for name in ['Dockerfile','entrypoint.py','report.py','neo4j.conf']:
            copy(ROOT/'docker'/name,dest/name)
        required = dest/'icecat/extlibs/tlx/CMakeLists.txt'
        if not required.exists(): raise SystemExit('Initialize Icecat submodules: git submodule update --init --recursive')
    releases=json.loads((ROOT/'neo4j/downloads.json').read_text())
    for name in ['gds.jar', 'neo4j.tar.gz']:
        release=releases[name]
        archive=ROOT/'neo4j'/name
        archive.parent.mkdir(parents=True,exist_ok=True)
        if not archive.exists():
            print(f'Downloading official {name}',flush=True)
            urllib.request.urlretrieve(release['url'],archive)
        if hashlib.sha256(archive.read_bytes()).hexdigest()!=release['sha256']:
            raise SystemExit(f'{name} checksum mismatch')
        copy(archive,dest/'benchmark/neo4j'/name)
    manifest={str(f.relative_to(dest)):hashlib.sha256(f.read_bytes()).hexdigest()
              for f in sorted(dest.rglob('*')) if f.is_file() and f != dest/'sources.json'}
    (dest/'sources.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'Staged {len(manifest)} files in {dest}')


if __name__=='__main__':main()
