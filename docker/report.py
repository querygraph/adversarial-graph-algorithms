"""Portable report retaining Neo4j semantic/timing boundaries and all outcomes."""
import json
from pathlib import Path
import statistics
import sys
p=Path(sys.argv[1]);data=json.loads(p.read_text());meta=data['metadata']
lines=['# Docker benchmark: Icebug, Icecat, Grustcat, Grustcat Cypher and Neo4j GDS','',
       f"Neo4j {meta['database'][0]['versions'][0]}, official GDS {meta['gds']}; algorithm concurrency 1.",'',
       'Direct native columns are kernel milliseconds including Arrow result construction in Rust; Grustcat Cypher additionally includes query compilation and execution. Neo4j uses reported computeMillis except Dijkstra, which consumes the full-path stream and reports server query time including reconstruction and aggregation. Dijkstra mode: ' + meta.get('dijkstra_mode','distance-only-native') + '. ' + ('All included engines construct source-first node and cumulative-cost arrays for every reachable target and consume their entries. Native timers include path construction and aggregation; GDS server query time also includes Cypher execution. Equivalent output work does not imply identical runtimes or allocation strategies.' if meta.get('dijkstra_mode') == 'full-path' else 'Native distance-only and GDS full-path columns are not equivalent work.') + ' Zero GDS compute times are below timer resolution.', '',
       'PageRank uses uniform weighted ranks. Native stopping is L1 1e-8; GDS uses per-node tolerance 1e-10. GDS scores are normalized before validation. Equal stopping rules or equal iteration work are not claimed. Graph loading, projection and transport are excluded from compute timers.','',
       '| Graph | Nodes | Algorithm | Icebug ms | Icecat ms | Grustcat ms | Grustcat Cypher ms | GDS ms | GDS boundary/status |',
       '|---|---:|---|---:|---:|---:|---:|---:|---|']
for r in data['results']:
    native=r['native_ms'];med=lambda k:f"{statistics.median(native[k]):.4f}" if native.get(k) else '—'
    if r.get('samples'):
        metric='server_query_ms' if r['algorithm']=='dijkstra' else 'computeMillis'
        val=f"{statistics.median(s[metric] for s in r['samples']):.3f}"
        status=r['timing_kind']
    else:val='—';status=r.get('status','incomplete')
    lines.append(f"| {r['family']} | {r['n']} | {r['algorithm']} | {med('cpp')} | {med('rust')} | {med('grustcat')} | {med('grustcat_cypher')} | {val} | {status} |")
lines+=['','Grustcat Cypher includes Grust parsing, semantic checks, planning, typed Arrow execution and result construction. Its documented query subset uses fused streaming path aggregation; it is not the materializing Grust reference executor or the same query text as Neo4j.','',f"{len(data['results'])} recorded cases. See [{p.name}]({p.name}) for complete validation, configuration, warmups, samples and hashes. Container/VM measurements are separate from the earlier macOS results.",'']
p.with_suffix('.md').write_text('\n'.join(lines))
print('Report:',p.with_suffix('.md'))
