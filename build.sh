#!/usr/bin/env bash
set -euo pipefail
BENCH_ROOT="$(cd "$(dirname "$0")" && pwd)"
ICECAT_ROOT="${ICECAT_ROOT:-$BENCH_ROOT/../icecat}"
# This build recipe targets the measured macOS/Homebrew environment.
BREW_ROOT="$(brew --prefix)"
OMP_ROOT="$(brew --prefix libomp)"
cmake -S "$ICECAT_ROOT" -B "$ICECAT_ROOT/rust/legacy-build" \
  -DNETWORKIT_BUILD_TESTS=ON -DNETWORKIT_NATIVE=OFF -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="$BREW_ROOT" -DOpenMP_CXX_FLAGS='-Xpreprocessor -fopenmp' \
  -DOpenMP_CXX_LIB_NAMES=omp -DOpenMP_omp_LIBRARY="$OMP_ROOT/lib/libomp.dylib" \
  -DCMAKE_CXX_FLAGS="-I$OMP_ROOT/include"
cmake --build "$ICECAT_ROOT/rust/legacy-build" --target networkit -j 8
c++ -std=c++20 -O3 -I"$ICECAT_ROOT/include" -I"$ICECAT_ROOT/extlibs/tlx" \
  -I"$ICECAT_ROOT/extlibs/ttmath" -I"$BREW_ROOT/include" -I"$OMP_ROOT/include" \
  -Xpreprocessor -fopenmp "$BENCH_ROOT/legacy.cpp" \
  -L"$ICECAT_ROOT/rust/legacy-build" -lnetworkit -L"$BREW_ROOT/lib" -larrow \
  -L"$OMP_ROOT/lib" -lomp -Wl,-rpath,"$BREW_ROOT/lib" -Wl,-rpath,"$OMP_ROOT/lib" \
  -Wl,-rpath,"$ICECAT_ROOT/rust/legacy-build" -o "$BENCH_ROOT/legacy"
cargo build --release --locked --manifest-path "$BENCH_ROOT/Cargo.toml" \
  --target-dir "$ICECAT_ROOT/rust/target"
cp "$ICECAT_ROOT/rust/target/release/icecat" "$BENCH_ROOT/rust-bench"

cp "$ICECAT_ROOT/rust/target/release/grustcat" "$BENCH_ROOT/grust-bench"
cp "$ICECAT_ROOT/rust/target/release/icecat" "$BENCH_ROOT/rust-bench-arrow"

cp "$ICECAT_ROOT/rust/target/release/icecat" "$BENCH_ROOT/icecat"
cp "$ICECAT_ROOT/rust/target/release/grustcat" "$BENCH_ROOT/grustcat"

cp "$ICECAT_ROOT/rust/target/release/grustcat-cypher" "$BENCH_ROOT/grustcat-cypher"
