#!/usr/bin/env python3
"""Every cell of a timed run as a Markdown table, recomputed from the run's JSON.

Rows are in a fixed order — fixture, algorithm, then participant as the run
listed them — never sorted by time, so a table does not rank. Every cell prints
its steal, its dispersion and whether it is unusable; an unusable cell is
printed, marked, and its numbers are kept, because dropping it would hide it.
"""
import argparse, json, pathlib

def fmt(value, digits=3):
    return '-' if value is None else f'{value:.{digits}f}'

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('runs', type=pathlib.Path, nargs='+')
    a = p.parse_args()
    for path in a.runs:
        report = json.loads(path.read_text())
        order = list(report['participants'])
        print(f"### `{path.name}`: {report['label']}\n")
        pinned = report.get('glibc_tunables')
        print(f"workers {report['workers']}, concurrency {report['concurrency']}, "
              f"allocator {'pinned: ' + pinned if pinned else 'glibc default, not pinned'}, "
              f"{report['warmups']} warmup + {report['repeats']} repeats, "
              f"steal over the run {report['steal_ticks_over_run']} ticks, {report['seconds']} s, "
              f"unusable at MAD/median >= {report['unusable_dispersion']}\n")
        if report['skipped']:
            print('Not timed (no agreeing parity row):', ', '.join(
                f"{s['participant']} {s['algorithm']} {s['fixture']}" for s in report['skipped']), '\n')
        print('| fixture | algorithm | participant | call | accounting | precision | iters | total ms | '
              'MAD | MAD/median | per iter | build ms | incoming ms | prepare | minflt | minflt build | '
              'work units | steal | usable |')
        print('| --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- '
              '| ---: | ---: | ---: | ---: | --- |')
        cells = sorted(report['cells'], key=lambda c: (c['fixture'], c['algorithm'],
                                                        order.index(c['participant']), c['call'] or ''))
        for c in cells:
            print(f"| {c['fixture'].removesuffix('.edges')} | {c['algorithm']} | `{c['participant']}` | "
                  f"{c['call'] or ''} | {c['accounting'] or ''} | "
                  f"{(c.get('precision') or '') if c['algorithm'] == 'pagerank' else ''} | "
                  f"{c['iterations'] or '-'} | "
                  f"{fmt(c['total_ms'])} | {fmt(c['total_mad'])} | {fmt(c['dispersion'], 3)} | "
                  f"{fmt(c['per_iteration_ms'])} | {fmt(c['build_ms'], 2)} | {fmt(c['incoming_ms'], 2)} | "
                  f"{c.get('prepare_incoming') or ''} | "
                  f"{fmt(c.get('minflt'), 0)} | {fmt(c.get('minflt_build'), 0)} | "
                  f"{c['work_units'] if c['work_units'] is not None else '-'} | {c['steal_ticks']} | "
                  f"{'**UNUSABLE**' if c['unusable'] else 'yes'} |")
        print()

if __name__ == '__main__': main()
