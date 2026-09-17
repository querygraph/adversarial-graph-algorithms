"""Workflow regression checks; run with python3 -m unittest discover -s docker."""
import array
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent


def module(name):
    spec = importlib.util.spec_from_file_location(name, HERE/f'{name}.py')
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


class WorkflowTests(unittest.TestCase):
    def test_changed_upstream_anchor_is_rejected(self):
        stage = module('stage_upstream')
        with self.assertRaises(ValueError): stage.replace_once('old old', 'old', 'new')
        with self.assertRaises(ValueError): stage.replace_once('changed', 'old', 'new')

    def test_audit_identity_tracks_replaced_executable(self):
        audit = module('participant_audit')
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'binary'
            path.write_bytes(b'first')
            original = audit.binary_sha256(path)
            replacement = Path(tmp)/'replacement'
            replacement.write_bytes(b'other')
            replacement.replace(path)
            self.assertNotEqual(audit.binary_sha256(path), original)

    def test_process_failure_retains_stdout_and_exit(self):
        audit = module('participant_audit')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            exe = root/'fail'
            exe.write_text('#!/bin/sh\necho retained-output\necho failure >&2\nexit 7\n')
            exe.chmod(0o755)
            graph = root/'graph'
            graph.write_text('128 0\n')
            with patch.dict(os.environ, BENCH_RESULTS_DIR=tmp, BENCH_AUDIT_LABEL='failure'):
                with self.assertRaises(subprocess.CalledProcessError):
                    audit.capture(lambda: None)(exe, graph, 'bfs', 0, root/'out')
            row = json.loads((root/'failure-processes.jsonl').read_text())
            self.assertEqual(row['status'], 'error')
            self.assertEqual(row['exit_code'], 7)
            self.assertEqual(row['stdout'], 'retained-output\n')
            self.assertEqual(row['stderr'], 'failure\n')
            self.assertIn('graph_sha256', row)

    def test_terminal_failure_and_collision(self):
        entry = module('entrypoint')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entry.ROOT = root
            entry.WORK = root
            with patch('sys.argv', ['entrypoint.py', '--label', 'case']), patch.object(entry.subprocess, 'run', return_value=subprocess.CompletedProcess([], 7)):
                self.assertEqual(entry.main(), 7)
                receipt = (root/'results/case-status.json').read_text()
                self.assertEqual(json.loads(receipt)['status'], 'failed')
                with self.assertRaises(FileExistsError): entry.main()
                self.assertEqual((root/'results/case-status.json').read_text(), receipt)

    def test_success_without_output_cannot_reuse_previous_vector(self):
        audit = module('participant_audit')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            exe = root/'no-output'
            exe.write_text("#!/bin/sh\necho '{}'\n")
            exe.chmod(0o755)
            graph = root/'graph'
            graph.write_text('128 0\n')
            output = root/'out'
            output.write_bytes(array.array('d', [0.] * 128).tobytes())
            with patch.dict(os.environ, BENCH_RESULTS_DIR=tmp, BENCH_AUDIT_LABEL='missing-output'):
                with self.assertRaises(FileNotFoundError):
                    audit.capture(lambda: None)(exe, graph, 'bfs', 0, output)
            row = json.loads((root/'missing-output-processes.jsonl').read_text())
            self.assertEqual(row['status'], 'error')
            self.assertEqual(row['exit_code'], 0)
            self.assertFalse(output.exists())

    def test_report_empty_samples_not_zero_or_pass(self):
        report = module('report_current')
        self.assertEqual(report.summary([]), '—')
        self.assertEqual(report.summary([1, 2, 3]), '2.0000 ± 1.0000 (3)')

    def test_runner_preserves_failed_run_and_uses_isolated_context(self):
        runner = module('run_current')
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)/'run'
            commands = []
            def run(command, **kwargs):
                commands.append((command, kwargs))
                if 'docker/stage_upstream.py' in command:
                    context = output/'context'
                    (context/'grust-upstream').mkdir(parents=True)
                    (context/'grust-upstream/Cargo.lock').write_text('locked')
                    (context/'sources.json').write_text('{}')
                failed = 'benchmark' in command and 'run' in command
                return subprocess.CompletedProcess(command, 7 if failed else 0)
            with patch('sys.argv', ['run_current.py', '--upstream-grust', tmp, '--turso', tmp,
                                    '--lockfile', str(Path(tmp)/'lock'), '--output', str(output),
                                    '--', '--sizes', '128']), patch.object(runner.subprocess, 'run', side_effect=run):
                with self.assertRaises(subprocess.CalledProcessError): runner.main()
            self.assertEqual(json.loads((output/'run.json').read_text())['status'], 'error')
            self.assertEqual((output/'upstream-Cargo.lock').read_text(), 'locked')
            self.assertFalse(any('update' in command for command, _ in commands))
            stage = next(c for c, _ in commands if 'docker/stage_upstream.py' in c)
            self.assertEqual(stage[stage.index('--allocator') + 1], 'mimalloc')
            benchmark, kwargs = next((c,k) for c,k in commands if 'benchmark' in c)
            self.assertEqual(benchmark[-2:], ['--sizes', '128'])
            self.assertEqual(kwargs['env']['BENCH_CONTEXT'], str(output/'context'))
            self.assertTrue(any('down' in command for command, _ in commands))

    def test_staged_participant_and_allocator(self):
        # An optional integration fixture is built by the real staging command.
        value = os.environ.get('BENCH_TEST_CONTEXT')
        if not value: self.skipTest('set BENCH_TEST_CONTEXT for source-stage integration checks')
        root = Path(value)
        receipt = json.loads((root/'build-receipt.json').read_text())
        source = root/'grust-upstream/crates/grust-algorithm-procedures/examples'
        for name in ['grust-upstream-direct', 'grust-upstream-cypher', 'turso-direct', 'turso-cypher', 'grust-arrow', 'grust-datafusion']:
            text = (source/f'{name}.rs').read_text()
            self.assertEqual('#[global_allocator]' in text, receipt['allocator'] == 'mimalloc')
        compare = (root/'benchmark/neo4j/compare.py').read_text()
        self.assertIn('metrics.get("provider") != "grust.algorithms"', compare)
        self.assertIn('turso_direct="turso-direct"', compare)
        self.assertIn("'--include-upstream'", (root/'entrypoint.py').read_text())
        self.assertIn('cargo build --release --locked', (root/'Dockerfile').read_text())
        self.assertIn('turso-main/bindings/rust', (root/'grust-upstream/Cargo.toml').read_text())


if __name__ == '__main__': unittest.main()
