"""Container entry point: collect provenance, run all engines, render a report."""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT=Path('/opt/benchmark')
WORK=Path('/work')

def main():
    for directory in ['results','data']: (WORK/directory).mkdir(parents=True,exist_ok=True)
    env=dict(os.environ,BENCH_RESULTS_DIR=str(WORK/'results'),BENCH_DATA_DIR=str(WORK/'data'))
    args=sys.argv[1:]
    label='docker-neo4j'
    for i,arg in enumerate(args):
        if arg=='--label' and i+1<len(args): label=args[i+1]
        elif arg.startswith('--label='):label=arg.split('=',1)[1]
    if not label or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in label):
        raise SystemExit('Invalid label')
    provenance={}
    for name in ['sources.json','rust-version.txt','cpp-version.txt','packages.txt']:
        provenance[name]=(ROOT/name).read_text()
    for name in ['/sys/fs/cgroup/cpu.max','/sys/fs/cgroup/memory.max','/proc/cpuinfo']:
        if Path(name).exists(): provenance[name]=Path(name).read_text()
    (WORK/'results'/f'{label}-environment.json').write_text(json.dumps(provenance,indent=2)+'\n')
    try:
        subprocess.run([sys.executable,str(ROOT/'neo4j/compare.py'),'--include-grustcat','--include-grustcat-cypher','--label',label]+args,env=env,check=True)
    finally:
        result=WORK/'results'/f'{label}.json'
        if result.exists():
            subprocess.run([sys.executable,str(ROOT/'docker/report.py'),str(result)],check=True)

if __name__=='__main__':main()
