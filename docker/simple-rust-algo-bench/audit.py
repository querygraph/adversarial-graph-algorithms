#!/usr/bin/env python3
"""Identify the five participant binaries and refuse a set that is not five.

Five binaries from four source trees in one image is the shape in which a build
system quietly hands you the same artifact twice: a stale copy, a symlink, a
COPY that overwrote a sibling. A table of five columns whose numbers came from
four binaries is wrong in a way no timing can reveal, so the check runs before
anything is timed and is fatal.
"""
import argparse, hashlib, json, pathlib, subprocess, sys

PARTICIPANTS = ['library', 'icebug', 'icecat', 'grustcat', 'grust']

def receipt(binary):
    # Each participant prints its own identity; the digest is taken here rather
    # than trusted from the binary, which could report anything.
    out = subprocess.run([str(binary), '--receipt'], capture_output=True, text=True, timeout=120)
    if out.returncode: raise SystemExit(f'{binary}: --receipt exited {out.returncode}: {out.stderr.strip()[:400]}')
    try: declared = json.loads(out.stdout)
    except json.JSONDecodeError as error: raise SystemExit(f'{binary}: --receipt is not JSON: {error}')
    for field in ('participant', 'version', 'commit'):
        if not declared.get(field): raise SystemExit(f'{binary}: --receipt has no {field}')
    declared['sha256'] = hashlib.sha256(pathlib.Path(binary).read_bytes()).hexdigest()
    declared['path'] = str(binary)
    return declared

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--directory', type=pathlib.Path, required=True)
    p.add_argument('--participants', nargs='+', default=PARTICIPANTS)
    p.add_argument('--output', type=pathlib.Path)
    a = p.parse_args()
    receipts = []
    for name in a.participants:
        binary = a.directory/name
        if not binary.exists(): raise SystemExit(f'missing participant binary: {binary}')
        found = receipt(binary)
        if found['participant'] != name:
            raise SystemExit(f'{binary}: declares participant {found["participant"]!r}, expected {name!r}')
        receipts.append(found)
    width = max(len(r['participant']) for r in receipts)
    for found in receipts:
        print(f'{found["participant"]:<{width}}  {found["sha256"][:16]}  {found["version"]:<12}  {found["commit"][:12]}')
    digests = {}
    for found in receipts: digests.setdefault(found['sha256'], []).append(found['participant'])
    collisions = {digest: names for digest, names in digests.items() if len(names) > 1}
    if collisions:
        for digest, names in collisions.items():
            print(f'IDENTICAL BINARIES: {", ".join(names)} all hash to {digest}', file=sys.stderr)
        raise SystemExit('participants are not distinct; refusing to measure')
    print(f'{len(receipts)} participants, {len(digests)} distinct binaries')
    if a.output: a.output.write_text(json.dumps(receipts, indent=1)+'\n')

if __name__ == '__main__': main()
