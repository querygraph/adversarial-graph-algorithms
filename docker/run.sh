#!/usr/bin/env bash
# Default: current upstream Grust and Turso with Arrow, DataFusion and mimalloc.
# --frozen reproduces the published measurement from the historical snapshot.
set -euo pipefail
cd "$(dirname "$0")/.."
frozen=
rest=()
for arg in "$@"; do
    if [[ "$arg" == "--frozen" ]]; then frozen=1; else rest+=("$arg"); fi
done
if [[ -z "$frozen" ]]; then
    exec python3 docker/run_current.py "$@"
fi
set -- ${rest+"${rest[@]}"}
python3 docker/prepare.py
docker compose build
mkdir -p "${BENCH_OUTPUT:-docker-results}"
# This Compose project is dedicated to benchmarking; retain output on failure.
trap 'docker compose down' EXIT
docker compose up -d --wait neo4j
docker version --format '{{json .Server}}' > "${BENCH_OUTPUT:-docker-results}/docker-engine.json"
docker image inspect graph-bench:local graph-bench-neo4j:local > "${BENCH_OUTPUT:-docker-results}/docker-images.json"
docker compose run --rm --user "$(id -u):$(id -g)" benchmark "$@"
