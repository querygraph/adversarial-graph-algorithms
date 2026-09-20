"""Add actual Arrow and DataFusion preparation participants to staged sources."""
from pathlib import Path
import shutil


def extend(target, allocator, replace_once):
    def rewrite(path, old, new):
        path.write_text(replace_once(path.read_text(), old, new))
    crate = target/'grust-upstream/crates/grust-algorithm-procedures'
    manifest = crate/'Cargo.toml'
    # Later upstream commits declare some of these themselves. Add only what is
    # missing: a second declaration is a TOML duplicate key, which fails the
    # whole workspace manifest rather than this crate alone.
    text = manifest.read_text()
    if 'path = "../grust-algorithms", features = ["arrow"] }' not in text:
        text = replace_once(text, 'path = "../grust-algorithms" }',
                            'path = "../grust-algorithms", features = ["arrow"] }')
    additions = [line for key, line in [
        ('arrow-array', 'arrow-array = "59.3.0"'),
        ('grust-arrow', 'grust-arrow = { path = "../grust-arrow" }'),
        ('grust-datafusion', 'grust-datafusion = { path = "../grust-datafusion" }'),
    ] if not any(l.split('=')[0].strip() == key for l in text.splitlines())]
    if additions:
        text = replace_once(text, '[dev-dependencies]', '\n'.join(['[dev-dependencies]'] + additions))
    manifest.write_text(text)
    lock = target/'grust-upstream/Cargo.lock'
    parts = lock.read_text().split('[[package]]')
    for i, part in enumerate(parts):
        if '\nname = "grust-algorithm-procedures"\n' in part:
            for dependency in ['arrow-array 59.3.0', 'grust-arrow', 'grust-datafusion']:
                if f' "{dependency}",' not in part:
                    part = replace_once(part, 'dependencies = [\n', f'dependencies = [\n "{dependency}",\n')
            parts[i] = part
    lock.write_text('[[package]]'.join(parts))
    protocol = crate/'examples/protocol/mod.rs'
    rewrite(protocol, '    Cypher,\n}', '    Cypher,\n    Arrow,\n    DataFusion,\n}')
    rewrite(protocol, 'struct Output {', 'struct Output {\n    arrow_details: Option<serde_json::Value>,')
    rewrite(protocol, 'mod turso_adapter;', 'mod turso_adapter;\nmod arrow_adapter;')
    shutil.copy2(Path(__file__).with_name('arrow_adapter.rs'), protocol.parent/'arrow_adapter.rs')
    rewrite(protocol, '        Mode::Cypher => cypher(&graph, &args[2], &args[4])?,',
            '        Mode::Cypher => cypher(&graph, &args[2], &args[4])?,\n        Mode::Arrow => arrow_adapter::run(&graph, &args[2], &args[4], false)?,\n        Mode::DataFusion => arrow_adapter::run(&graph, &args[2], &args[4], true)?,')
    rewrite(protocol, '(true, Mode::Cypher) => "turso_cypher" }', '(true, Mode::Cypher) => "turso_cypher", (false, Mode::Arrow) => "grust_arrow", (false, Mode::DataFusion) => "grust_datafusion", _ => unreachable!("Turso Arrow mode is not exposed") }')
    rewrite(protocol, 'else { "explicit_local_snapshot" }', 'else { match mode { Mode::Arrow => "arrow_preparation_native_kernels_arrow_results", Mode::DataFusion => "datafusion_preparation_native_kernels_arrow_results", _ => "explicit_local_snapshot" } }')
    rewrite(protocol, '"backend_details": backend,', '"backend_details": backend, "arrow_details": output.arrow_details,')
    rewrite(protocol, 'Mode::Direct => None, Mode::Cypher => Some(86400)', 'Mode::Direct | Mode::Arrow | Mode::DataFusion => None, Mode::Cypher => Some(86400)')
    rewrite(protocol, '"timer_boundary": match mode {', '"timer_boundary": match mode { Mode::Arrow | Mode::DataFusion => "Grust kernels, Arrow result construction and full consumption; Arrow/DataFusion preparation separate",')
    global_allocator = '#[global_allocator]\nstatic ALLOCATOR: mimalloc::MiMalloc = mimalloc::MiMalloc;\n' if allocator == 'mimalloc' else ''
    for name, mode in [('grust-arrow', 'Arrow'), ('grust-datafusion', 'DataFusion')]:
        (crate/'examples'/f'{name}.rs').write_text(global_allocator + 'mod protocol;\nfn main() -> Result<(), Box<dyn std::error::Error>> { protocol::run(protocol::Mode::' + mode + ') }\n')


def extend_harness(target, replace_once):
    path = target/'benchmark/neo4j/compare.py'
    text = replace_once(path.read_text(), 'turso_cypher="turso-cypher")', 'turso_cypher="turso-cypher", grust_arrow="grust-arrow", grust_datafusion="grust-datafusion")')
    text = text.replace('("grust_upstream", "turso")', '("grust_", "turso")')
    text = text.replace('"turso_cypher": "Turso snapshot / Grust Cypher"}', '"turso_cypher": "Turso snapshot / Grust Cypher", "grust_arrow": "Grust Arrow", "grust_datafusion": "DataFusion preparation / Grust Arrow kernels"}')
    path.write_text(text)
    path = target/'benchmark/check_upstream.py'
    path.write_text(replace_once(path.read_text(), '"turso-direct", "turso-cypher"]', '"turso-direct", "turso-cypher", "grust-arrow", "grust-datafusion"]'))
    path = target/'Dockerfile'
    text = replace_once(path.read_text(), '--example turso-direct --example turso-cypher', '--example turso-direct --example turso-cypher --example grust-arrow --example grust-datafusion')
    text = replace_once(text, 'COPY build-receipt.json /opt/benchmark/', 'COPY --from=upstream /src/grust-upstream/target/release/examples/grust-arrow /src/grust-upstream/target/release/examples/grust-datafusion /opt/benchmark/\nCOPY build-receipt.json /opt/benchmark/')
    path.write_text(text)
