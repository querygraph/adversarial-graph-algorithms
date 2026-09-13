"""Validate the Cypher backend against direct kernels and cross-read Arrow IPC."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import bench


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bin-dir', type=Path, default=bench.ROOT)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    binaries = ['icecat', 'grustcat', 'grustcat-cypher']
    checks = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for family in ['path', 'hub', 'clusters', 'layered', 'uniform', 'rmat']:
            edges = bench.generate(family, 128)
            source = root/'graph.txt'
            source.write_text(f'128 {len(edges)}\n' + ''.join(f'{u} {v} {w}\n' for u,v,w in edges))
            for alg in ['bfs', 'dijkstra', 'dijkstra-full', 'wcc', 'scc', 'pagerank']:
                results = [bench.execute(args.bin_dir/b,source,alg,0,root/'out') for b in binaries]
                for metrics, values in results:
                    assert len(values) == 128
                    assert max(abs(a-b) for a,b in zip(results[0][1],values)) <= (1e-9 if alg == 'pagerank' else 0.)
                    if alg == 'pagerank': assert metrics['iterations'] == results[0][0]['iterations']
                    if alg == 'dijkstra-full' and family == 'path':
                        assert metrics['path_entries'] == 128*129//2
                        assert metrics['node_sum'] == sum(i*(128-i) for i in range(128))
                        assert metrics['cost_sum'] == sum(d*(128-i) for i,d in enumerate(values))
                assert results[-1][0]['execution_class'] == 'grust-parser-arrow-backend'
                assert results[-1][0]['query'].startswith('CALL grustcat.')
                checks.append({'family':family,'algorithm':alg,'status':'ok'})
        # All writers and readers preserve graph properties and full-path output.
        for writer in binaries:
            ipc=root/writer
            subprocess.run([str(args.bin_dir/writer),str(source),'dijkstra-full',str(root/'out'),'0',str(ipc)],check=True,capture_output=True)
            reference=bench.execute(args.bin_dir/'grustcat',source,'dijkstra-full',0,root/'out')[1]
            for reader in binaries:
                _,actual=bench.execute(args.bin_dir/reader,ipc,'dijkstra-full',0,root/'out')
                assert actual == reference
                checks.append({'writer':writer,'reader':reader,'format':'Arrow IPC','status':'ok'})
    report={'binary_sha256':{b:hashlib.sha256((args.bin_dir/b).read_bytes()).hexdigest() for b in binaries},'checks':checks}
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(f'{len(checks)} Cypher/kernel and Arrow interchange checks passed')


if __name__ == '__main__':
    main()
