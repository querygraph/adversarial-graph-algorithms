"""Retain raw process evidence before correctness validation, including failures."""
import array
import datetime
import functools
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import time


@functools.lru_cache(maxsize=32)
def _binary_hash(path, identity):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def binary_sha256(path):
    path = Path(path).resolve()
    stat = path.stat()
    # Benchmark images and exported variant mounts are immutable. Also include
    # file identity and change times so local development replacements invalidate
    # the cache instead of retaining the preceding executable's identity.
    return _binary_hash(str(path), (stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns))


def capture(execute):
    @functools.wraps(execute)
    def run(exe, graph, algorithm, source, output):
        label = os.environ.get('BENCH_AUDIT_LABEL', 'validation')
        if not label or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in label):
            raise ValueError('invalid audit label')
        directory = Path(os.environ.get('BENCH_RESULTS_DIR', '/work/results'))
        directory.mkdir(parents=True, exist_ok=True)
        receipt = dict(timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                       executable=str(exe), graph=str(graph), algorithm=algorithm, source=source,
                       graph_sha256=hashlib.sha256(graph.read_bytes()).hexdigest())
        start = time.monotonic()
        cpu = resource.getrusage(resource.RUSAGE_CHILDREN)
        try:
            receipt['binary_sha256'] = binary_sha256(exe)
            # A successful process must produce its own output, never reuse a
            # preceding sample's vector after failing to write one.
            Path(output).unlink(missing_ok=True)
            start = time.monotonic()
            result = subprocess.run([str(exe), str(graph), algorithm, str(output), str(source)],
                capture_output=True, text=True, timeout=None if algorithm == 'dijkstra-full' else 180,
                env=dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1'))
            elapsed = time.monotonic()-start
            receipt.update(exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr)
            result.check_returncode()
            metrics = json.loads(result.stdout)
            metrics['process_seconds'] = elapsed
            values = array.array('d')
            raw = output.read_bytes()
            values.frombytes(raw)
            receipt.update(status='completed', metrics=metrics, output_sha256=hashlib.sha256(raw).hexdigest())
            return metrics, values
        except subprocess.TimeoutExpired as error:
            receipt.update(status='timeout', error=str(error), stdout=str(error.stdout), stderr=str(error.stderr))
            raise
        except FileNotFoundError as error:
            receipt.update(status='error' if 'exit_code' in receipt else 'unavailable', error=str(error))
            raise
        except Exception as error:
            receipt.update(status='error', error=str(error))
            raise
        finally:
            after = resource.getrusage(resource.RUSAGE_CHILDREN)
            receipt.update(process_seconds=receipt.get('metrics', {}).get('process_seconds', time.monotonic()-start), process_cpu_seconds=
                           after.ru_utime+after.ru_stime-cpu.ru_utime-cpu.ru_stime)
            with (directory/f'{label}-processes.jsonl').open('a') as stream:
                stream.write(json.dumps(receipt)+'\n')
    return run
