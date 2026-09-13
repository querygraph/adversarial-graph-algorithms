"""Exercise each IPC writer with both readers, checking complete algorithm outputs."""
import array
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from bench import ROOT, generate


def main():
    source = ROOT/'data/hub-16384.txt'
    if not source.exists():
        edges=generate('hub',16384)
        source.write_text(f'16384 {len(edges)}\n'+''.join(f'{u} {v} {w}\n' for u,v,w in edges))
    binaries=['icecat','grustcat']
    result=dict(nodes=16384,binary_sha256={b:hashlib.sha256((ROOT/b).read_bytes()).hexdigest() for b in binaries},checks=[])
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp)
        for writer in binaries:
            ipc=p/writer
            subprocess.run([str(ROOT/writer),str(source),'bfs',str(p/'unused'),'0',str(ipc)],check=True,capture_output=True,timeout=180)
            for alg in ['bfs','dijkstra','wcc','scc','pagerank']:
                values=[]
                for reader in binaries:
                    out=p/(reader+'.bin')
                    subprocess.run([str(ROOT/reader),str(ipc),alg,str(out),'0'],check=True,capture_output=True,timeout=180)
                    a=array.array('d');a.frombytes(out.read_bytes());values.append(a)
                assert all(len(a)==16384 for a in values)
                error=max(abs(a-b) for a,b in zip(*values))
                assert error <= (1e-9 if alg=='pagerank' else 0.), (writer,alg,error)
                result['checks'].append(dict(writer=writer,readers=binaries,algorithm=alg,max_abs_error=error,status='ok'))
    (ROOT/'results/grustcat-arrow-interop.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Both IPC writers -> both readers: all five algorithms agree')


if __name__=='__main__':
    main()
