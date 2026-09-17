#!/usr/bin/env python3
"""Export an immutable image's benchmark binaries and identity for paired trials."""
import argparse
import json
from pathlib import Path
import subprocess


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('image')
    p.add_argument('output', type=Path)
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=False)
    identity = json.loads(subprocess.check_output(['docker', 'image', 'inspect', a.image]))[0]
    (a.output/'image.json').write_text(json.dumps(identity, indent=2)+'\n')
    container = subprocess.check_output(['docker', 'create', identity['Id']], text=True).strip()
    try:
        for name in ['grust-upstream-direct', 'grust-upstream-cypher', 'turso-direct', 'turso-cypher', 'grust-arrow', 'grust-datafusion',
                     'build-receipt.json', 'sources.json', 'upstream-rust-version.txt', 'upstream-validation.json', 'cypher-validation.json']:
            subprocess.run(['docker', 'cp', f'{container}:/opt/benchmark/{name}', str(a.output/name)], check=True)
    finally:
        subprocess.run(['docker', 'rm', container], check=True, stdout=subprocess.DEVNULL)


if __name__ == '__main__': main()
