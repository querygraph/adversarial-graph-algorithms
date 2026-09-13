"""Three-way paired benchmark, with complete result validation on every sample."""
import argparse
import hashlib
import math
import json
import platform
import statistics
import tempfile
import time
from pathlib import Path
from bench import ROOT, generate, execute


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sizes', type=int, nargs='+', default=[16384, 65536])
    parser.add_argument('--repeats', type=int, default=5)
    parser.add_argument('--label', default='grustcat-optimized')
    parser.add_argument('--families', nargs='+', choices=['path','hub','clusters','layered','uniform','rmat'], default=['path','hub','clusters','layered','uniform','rmat'])
    parser.add_argument('--algorithms', nargs='+', choices=['bfs','dijkstra','wcc','scc','pagerank'], default=['bfs','dijkstra','wcc','scc','pagerank'])
    parser.add_argument('--skip-baseline', action='store_true')
    args = parser.parse_args()
    if args.repeats < 1 or any(n < 128 or n & (n-1) for n in args.sizes):
        parser.error('positive repeats and power-of-two sizes >=128 required')
    exes = {'icebug': ROOT/'legacy', 'icecat': ROOT/'icecat', 'grustcat': ROOT/'grustcat', 'grustcat_before': ROOT/'grustcat-baseline'}
    if args.skip_baseline: exes.pop('grustcat_before')
    report = dict(date=time.strftime('%Y-%m-%d'), platform=platform.platform(),
                  repeats=args.repeats, warmups=1, concurrency=1,
                  timing='kernel only; Rust includes Arrow result construction; graph loading and index construction excluded',
                  binaries={k:dict(path=str(v), sha256=hashlib.sha256(v.read_bytes()).hexdigest()) for k,v in exes.items()}, results=[])
    output = ROOT/'results'/f'{args.label}.json'
    names = list(exes)
    with tempfile.TemporaryDirectory() as tmp:
        for n in args.sizes:
            for family in args.families:
                graph = ROOT/'data'/f'{family}-{n}.txt'
                if not graph.exists():
                    edges=generate(family,n)
                    graph.write_text(f'{n} {len(edges)}\n'+''.join(f'{u} {v} {w}\n' for u,v,w in edges))
                digest = hashlib.sha256(graph.read_bytes()).hexdigest()
                for alg in args.algorithms:
                    row=dict(family=family,n=n,algorithm=alg,graph_sha256=digest,status='running',samples={k:[] for k in names},max_abs_error=0.)
                    report['results'].append(row)
                    try:
                        for repeat in range(args.repeats+1):
                            values={}; metrics={}
                            order=names[repeat%len(names):]+names[:repeat%len(names)]
                            for name in order:
                                metrics[name], values[name] = execute(exes[name],graph,alg,0,Path(tmp)/f'{name}.bin')
                                if repeat: row['samples'][name].append(metrics[name])
                            for name in names:
                                if not all(math.isfinite(x) for x in values[name]): raise ValueError(f'{name} nonfinite output')
                                if len(values[name]) != n: raise ValueError('incorrect output length')
                                error=max((abs(a-b) for a,b in zip(values['icebug'],values[name])),default=0.)
                                row['max_abs_error']=max(row['max_abs_error'],error)
                                if error > (1e-9 if alg=='pagerank' else 0.): raise ValueError(f'{name} mismatch: {error}')
                                if alg=='pagerank':
                                    if abs(sum(values[name])-1.)>1e-8: raise ValueError('PageRank mass mismatch')
                                    if metrics[name]['iterations'] != metrics['icebug']['iterations']: raise ValueError('iteration mismatch')
                        row['status']='ok'
                        row['median_ms']={k:statistics.median(s['ms'] for s in row['samples'][k]) for k in names}
                        row['grustcat_match_gate'] = row['median_ms']['grustcat'] <= max(1.10*row['median_ms']['icecat'],row['median_ms']['icecat']+0.1)
                        print(f'{family} {n} {alg}: {row["median_ms"]}',flush=True)
                    except Exception as exc:
                        row['status']='error';row['error']=repr(exc)
                        raise
                    finally:
                        output.write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':
    main()
