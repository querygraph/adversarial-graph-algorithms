#!/usr/bin/env python3
"""Generate paired-trial tables from retained samples; no ranking acceptance gate."""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import statistics


def stats(values):
    median = statistics.median(values)
    return dict(n=len(values), median=median, mad=statistics.median(abs(x-median) for x in values), minimum=min(values), maximum=max(values))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('results', type=Path)
    a = p.parse_args()
    data = json.loads(a.results.read_text())
    groups = defaultdict(list)
    outcomes = defaultdict(int)
    for case in data['results']:
        for sample in case['samples']:
            outcomes[sample['status']] += 1
            if sample['status'] != 'pass' or sample['warmup']: continue
            key = tuple(sample[k] for k in ['family', 'n', 'algorithm', 'participant', 'variant', 'group_commit'])
            groups[key].append(sample['metrics'])
    rows = []
    lines = ['# Paired optimization trials', '', 'Times are milliseconds, median ± median absolute deviation. Every warmup, measured sample and failure remains in the source JSON and process audit. Alternating variant order; fresh process and Turso database per sample. No cross-host pooling.', '',
             'Turso uses Grust algorithms over a materialized database snapshot. Its loading and snapshot phases are outside the kernel/query timer. Group-commit settings change only concurrent durable statement loading; they are not kernel optimizations.', '',
             '| Graph | Nodes | Algorithm | Participant | Variant | Group | Phase | n | Median ± MAD, ms |',
             '|---|---:|---|---|---|---|---|---:|---:|']
    for key, samples in groups.items():
        row = dict(zip(['family', 'n', 'algorithm', 'participant', 'variant', 'group_commit'], key), phases={})
        for phase in ['ms', 'loading_ms', 'preparation_ms', 'verification_ms', 'serialization_ms', 'end_to_end_ms', 'process_seconds', 'setup_ms', 'database_load_ms', 'snapshot_ms', 'snapshot_verification_ms', 'snapshot_ordering_ms', 'conversion_ms', 'datafusion_preparation_ms', 'projection_ms']:
            values = [s.get(phase, (s.get('backend_details') or {}).get(phase, (s.get('arrow_details') or {}).get(phase))) for s in samples]
            values = [v*(1000 if phase == 'process_seconds' else 1) for v in values if v is not None]
            if not values: continue
            st = stats(values)
            row['phases'][phase] = st
            lines.append('| ' + ' | '.join(map(str, key)) + f" | {phase} | {st['n']} | {st['median']:.4f} ± {st['mad']:.4f} |")
        rows.append(row)
    lines += ['', f'All outcomes, including warmups: {dict(outcomes)}.', '', 'Ratios must compare the same graph, algorithm, participant, source lock, resource envelope and phase. Kernel/query ratios between direct and Cypher are not pure dispatch overhead.', '']
    a.results.with_name('summary.json').write_text(json.dumps(dict(outcomes=outcomes, rows=rows), indent=2)+'\n')
    a.results.with_suffix('.md').write_text('\n'.join(lines))


if __name__ == '__main__': main()
