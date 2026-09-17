#!/usr/bin/env python3
"""Extend the pinned upstream integration in an isolated, receipt-bearing context."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib
import stage_arrow

HERE = Path(__file__).resolve().parent


def replace_once(text, old, new):
    if text.count(old) != 1:
        raise ValueError(f'integration anchor changed: {old[:100]!r}')
    return text.replace(old, new, 1)


def rewrite(path, old, new):
    path.write_text(replace_once(path.read_text(), old, new))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--grust', type=Path, required=True)
    p.add_argument('--frozen-context', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--turso', type=Path, required=True, help='Checkout of Turso main at the recorded commit')
    p.add_argument('--lockfile', type=Path, help='Previously resolved lockfile for exactly these source inputs')
    allocator = p.add_mutually_exclusive_group()
    allocator.add_argument('--allocator', choices=['system', 'mimalloc'], default='mimalloc')
    allocator.add_argument('--mimalloc', dest='allocator', action='store_const', const='mimalloc', help='Build current participants with the mimalloc global allocator')
    p.add_argument('--profile', choices=['default', 'thin'], default='default')
    a = p.parse_args()
    source = a.grust.resolve()
    subprocess.run([sys.executable, str(source/'benchmarks/algorithms/stage_companion.py'),
                    '--frozen-context', str(a.frozen_context), '--output', str(a.output)], check=True)
    target = a.output.resolve()
    turso = a.turso.resolve()
    shutil.copytree(turso, target/'turso-main', ignore=shutil.ignore_patterns('.git', 'target', '__pycache__'))
    rewrite(target/'grust-upstream/Cargo.toml', 'turso = { version = "0.7.2", default-features = false }',
            'turso = { path = "../turso-main/bindings/rust", default-features = false }')
    crate = target/'grust-upstream/crates/grust-algorithm-procedures'
    manifest = crate/'Cargo.toml'
    with (source/'Cargo.lock').open('rb') as f:
        locked = tomllib.load(f)
    version = lambda name: next(x['version'] for x in locked['package'] if x['name'] == name)
    text = manifest.read_text()
    text = replace_once(text, '[dev-dependencies]', '[dev-dependencies]\ngrust-turso = { path = "../grust-turso", default-features = false }\ntokio.workspace = true\ntempfile.workspace = true\nmimalloc = "=' + version('mimalloc') + '"')
    manifest.write_text(text)
    # All added dependencies already exist in the pinned lock. Only this package's
    # dependency edges change; cargo --locked verifies the resulting resolution.
    lock = target/'grust-upstream/Cargo.lock'
    text = lock.read_text()
    anchor = 'name = "grust-algorithm-procedures"\nversion = "' + version('grust-algorithm-procedures') + '"\ndependencies = [\n'
    rewrite(lock, anchor, anchor + ' "grust-turso",\n "mimalloc",\n "tempfile",\n "tokio",\n')
    if a.lockfile:
        shutil.copy2(a.lockfile, lock)
    protocol = crate/'examples/protocol/mod.rs'
    rewrite(protocol, 'pub fn run(mode: Mode) -> Result<()> {',
            'mod turso_adapter;\npub fn run(mode: Mode) -> Result<()> { run_backend(mode, false) }\n'
            'pub fn run_turso(mode: Mode) -> Result<()> { run_backend(mode, true) }\n'
            'fn run_backend(mode: Mode, turso: bool) -> Result<()> {')
    rewrite(protocol, '    let output = match mode {',
            '    let (graph, backend) = if turso { turso_adapter::prepare(graph)? } else { (graph, serde_json::Value::Null) };\n    let output = match mode {')
    rewrite(protocol, '"participant": match mode { Mode::Direct => "grust_upstream_direct", Mode::Cypher => "grust_upstream_cypher" }',
            '"participant": match (turso, &mode) { (false, Mode::Direct) => "grust_upstream_direct", (false, Mode::Cypher) => "grust_upstream_cypher", (true, Mode::Direct) => "turso_direct", (true, Mode::Cypher) => "turso_cypher" }, "backend_details": backend, "allocator": "' + a.allocator + '"')
    rewrite(protocol, '"execution_class": "explicit_local_snapshot"',
            '"execution_class": if turso { "turso_materialized_snapshot_grust_algorithms" } else { "explicit_local_snapshot" }')
    shutil.copy2(HERE/'turso_adapter.rs', protocol.parent/'turso_adapter.rs')
    allocator = '#[global_allocator]\nstatic ALLOCATOR: mimalloc::MiMalloc = mimalloc::MiMalloc;\n' if a.allocator == 'mimalloc' else ''
    for name, mode in [('grust-upstream-direct', 'Direct'), ('grust-upstream-cypher', 'Cypher'), ('turso-direct', 'Direct'), ('turso-cypher', 'Cypher')]:
        (crate/'examples'/f'{name}.rs').write_text(allocator + 'mod protocol;\nfn main() -> Result<(), Box<dyn std::error::Error>> { protocol::' + ('run_turso' if name.startswith('turso') else 'run') + '(protocol::Mode::' + mode + ') }\n')
    stage_arrow.extend(target, a.allocator, replace_once)
    if a.profile == 'thin':
        with (target/'grust-upstream/Cargo.toml').open('a') as f:
            f.write('\n[profile.release]\nlto = "thin"\ncodegen-units = 1\n')
    dockerfile = target/'Dockerfile'
    rewrite(dockerfile, 'COPY grust-upstream /src/grust-upstream', 'COPY turso-main /src/turso-main\nCOPY grust-upstream /src/grust-upstream')
    rewrite(dockerfile, '--example grust-upstream-direct --example grust-upstream-cypher',
            '--example grust-upstream-direct --example grust-upstream-cypher --example turso-direct --example turso-cypher\nRUN rustc -vV > /src/upstream-rust-version.txt')
    rewrite(dockerfile, 'COPY --from=build /out /opt/benchmark\n',
            'COPY --from=build /out /opt/benchmark\nCOPY --from=upstream /src/upstream-rust-version.txt /opt/benchmark/\nCOPY --from=upstream /src/grust-upstream/target/release/examples/turso-direct /src/grust-upstream/target/release/examples/turso-cypher /opt/benchmark/\nCOPY build-receipt.json /opt/benchmark/\n')
    compare = target/'benchmark/neo4j/compare.py'
    rewrite(compare, 'grust_upstream_cypher="grust-upstream-cypher")',
            'grust_upstream_cypher="grust-upstream-cypher", turso_direct="turso-direct", turso_cypher="turso-cypher")')
    text = compare.read_text().replace('backend.startswith("grust_upstream")', 'backend.startswith(("grust_upstream", "turso"))')
    text = text.replace('"grust_upstream_cypher": "Grust upstream Cypher"}', '"grust_upstream_cypher": "Grust upstream Cypher", "turso_direct": "Turso snapshot / Grust direct", "turso_cypher": "Turso snapshot / Grust Cypher"}')
    compare.write_text(text)
    shutil.copy2(HERE/'participant_audit.py', target/'benchmark/participant_audit.py')
    check = target/'benchmark/check_upstream.py'
    rewrite(check, '["grust-upstream-direct", "grust-upstream-cypher"]', '["grust-upstream-direct", "grust-upstream-cypher", "turso-direct", "turso-cypher"]')
    for name in ['entrypoint.py', 'report_current.py']:
        shutil.copy2(HERE/name, target/('report.py' if name == 'report_current.py' else name))
    rewrite(target/'entrypoint.py', "'--include-grustcat-cypher',", "'--include-grustcat-cypher','--include-upstream',")
    stage_arrow.extend_harness(target, replace_once)
    def git(*args):
        return subprocess.check_output(['git', '-C', str(source), *args], text=True)
    receipt = dict(upstream_commit=git('rev-parse', 'HEAD').strip(), upstream_status=git('status', '--porcelain'),
                   upstream_diff=git('diff', 'HEAD'), allocator=a.allocator, release_profile=a.profile, arrow_version='59.3.0', datafusion_version=next(dep.split()[1] for pkg in locked['package'] if pkg['name'] == 'grust-datafusion' for dep in pkg['dependencies'] if dep.startswith('datafusion ')),
                   datafusion_boundary='input preparation only; native Grust kernels and Arrow result consumption',
                   rustflags='', target_cpu='portable default', turso_version=tomllib.loads((turso/'Cargo.toml').read_text())['workspace']['package']['version'],
                   turso_commit=subprocess.check_output(['git', '-C', str(turso), 'rev-parse', 'HEAD'], text=True).strip(),
                   turso_status=subprocess.check_output(['git', '-C', str(turso), 'status', '--porcelain'], text=True),
                   mimalloc_version=version('mimalloc') if a.allocator == 'mimalloc' else None,
                   staging_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (target/'build-receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
    hashes = {str(f.relative_to(target)): hashlib.sha256(f.read_bytes()).hexdigest()
              for f in sorted(target.rglob('*')) if f.is_file() and f != target/'sources.json'}
    (target/'sources.json').write_text(json.dumps(hashes, indent=2)+'\n')
    print(f'Staged current Grust and Turso: {target}')


if __name__ == '__main__':
    main()
