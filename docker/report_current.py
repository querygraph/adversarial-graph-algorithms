"""Render all participant timings, phase boundaries and median absolute deviation."""
import json
from pathlib import Path
import statistics
import sys


def summary(values):
    if not values: return '—'
    median = statistics.median(values)
    mad = statistics.median(abs(x-median) for x in values)
    return f'{median:.4f} ± {mad:.4f} ({len(values)})'


def main():
    path = Path(sys.argv[1])
    data = json.loads(path.read_text())
    rows = data['results']
    engines = list(dict.fromkeys(k for r in rows for k in r['native_ms']))
    lines = ['# Algorithm benchmark', '',
             'Milliseconds: median ± median absolute deviation (measured samples). All raw samples remain in JSON. Single samples establish completion only.', '',
             'Historical native columns include kernel and Arrow result construction; Grustcat Cypher uses its typed Arrow adapter. Upstream Grust direct includes kernel and result conversion with projection separate; upstream Cypher includes parsing, policy checks, projection and ordinary query execution. Full-path distance verification is outside that query timer.', '',
             'Grust Arrow converts the input to Arrow, prepares the native graph projection, and consumes Arrow result batches. The DataFusion column executes node/edge preparation plans before those same native kernels and Arrow result consumption. It is not a DataFusion graph-kernel implementation. Conversion, DataFusion preparation and projection are separately timed.', '',
             '**Turso columns use Grust algorithms over a full snapshot read from a temporary file-backed Turso database. They are not Turso-native SQL graph kernels.** Database setup, durable loading, snapshot capture and snapshot validation are separate phases. Group commit affects the statements load, not the algorithm timer. Neo4j GDS projection uses generated edge parameters rather than a durable database load; these loading phases are not equivalent ingestion comparisons.', '',
             'GDS reports computeMillis except full-path Dijkstra, which reports the server query including reconstruction and aggregation. Distance-only native Dijkstra and full-path GDS are unequal work. BFS output and PageRank stopping criteria differ across GDS and native participants as documented in docker/README.md. Upstream logical working allowance is 256 MiB; each service has a separate 4 GiB cgroup ceiling. No per-participant RSS is inferred.', '',
             '| Graph | Nodes | Algorithm | ' + ' | '.join(engines) + ' | GDS | Status/boundary |',
             '|---|---:|---|' + '---:|'*(len(engines)+1) + '---|']
    for row in rows:
        metric = 'server_query_ms' if row['algorithm'] == 'dijkstra' else 'computeMillis'
        values = [s[metric] for s in row.get('samples', []) if metric in s]
        lines.append('| '+ ' | '.join([row['family'], str(row['n']), row['algorithm'],
            *[summary(row['native_ms'].get(k, [])) for k in engines], summary(values),
            row.get('status', row.get('timing_kind', 'incomplete'))]) + ' |')
    lines += ['', '## Upstream and Turso phases', '', '| Graph | Nodes | Algorithm | Participant | Phase | Median ± MAD (n), ms |', '|---|---:|---|---|---|---:|']
    for row in rows:
        for name, details in row.get('native_details', {}).items():
            samples = [s for s in details if not s.get('warmup')]
            for phase in ['loading_ms', 'preparation_ms', 'ms', 'verification_ms', 'serialization_ms', 'end_to_end_ms', 'process_seconds', 'setup_ms', 'database_load_ms', 'snapshot_ms', 'snapshot_verification_ms', 'snapshot_ordering_ms', 'conversion_ms', 'datafusion_preparation_ms', 'projection_ms']:
                values = []
                for s in samples:
                    value = s.get(phase, (s.get('backend_details') or {}).get(phase, (s.get('arrow_details') or {}).get(phase)))
                    if value is not None: values.append(value * (1000 if phase == 'process_seconds' else 1))
                if values:
                    lines.append(f"| {row['family']} | {row['n']} | {row['algorithm']} | {name} | {phase} | {summary(values)} |")
    lines += ['', f'See [{path.name}]({path.name}), environment, terminal-status and process-audit receipts for identities, settings, validations and failures.', '']
    path.with_suffix('.md').write_text('\n'.join(lines))


if __name__ == '__main__': main()
