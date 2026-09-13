#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 docker/prepare.py
docker compose build
mkdir -p "${BENCH_OUTPUT:-docker-results}"
# This Compose project is dedicated to benchmarking; retain output on failure.
trap 'docker compose down' EXIT
docker compose up -d --wait neo4j
docker version --format '{{json .Server}}' > "${BENCH_OUTPUT:-docker-results}/docker-engine.json"
docker image inspect graph-bench:local graph-bench-neo4j:local > "${BENCH_OUTPUT:-docker-results}/docker-images.json"
docker compose run --rm --user "$(id -u):$(id -g)" benchmark "$@"
