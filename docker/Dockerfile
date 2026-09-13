# syntax=docker/dockerfile:1
FROM eclipse-temurin:21-jre-jammy AS neo4j
COPY benchmark/neo4j/neo4j.tar.gz /tmp/neo4j.tar.gz
RUN mkdir /opt/neo4j && tar xzf /tmp/neo4j.tar.gz --strip-components=1 -C /opt/neo4j \
    && rm /tmp/neo4j.tar.gz && useradd -m neo4j
COPY benchmark/neo4j/gds.jar /opt/neo4j/plugins/gds.jar
COPY benchmark/neo4j/user-logs.xml benchmark/neo4j/server-logs.xml /opt/neo4j/conf/
COPY neo4j.conf /opt/neo4j/conf/neo4j.conf
RUN mkdir /versions && java -version > /versions/java.txt 2>&1 \
    && sha256sum /opt/neo4j/plugins/gds.jar > /versions/gds.sha256 \
    && chown -R neo4j:neo4j /opt/neo4j
ENV PATH="/opt/neo4j/bin:$PATH" NEO4J_HOME=/opt/neo4j
USER neo4j
WORKDIR /opt/neo4j
CMD ["neo4j", "console"]

FROM rust:1.97.1-bookworm AS build
ARG BUILD_JOBS=4
ARG ARROW_VERSION=24.0.0-1
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl cmake ninja-build pkg-config python3 python3-venv \
    && curl -fsSL https://packages.apache.org/artifactory/arrow/debian/apache-arrow-apt-source-latest-bookworm.deb -o /tmp/arrow.deb \
    && apt-get install -y /tmp/arrow.deb && apt-get update \
    && apt-get install -y --no-install-recommends libarrow-dev=${ARROW_VERSION} \
    && rm -rf /var/lib/apt/lists/* /tmp/arrow.deb
COPY icecat/CMakeLists.txt icecat/networkit.pc /src/icecat/
COPY icecat/include /src/icecat/include
COPY icecat/networkit /src/icecat/networkit
COPY icecat/extlibs /src/icecat/extlibs
COPY benchmark/legacy.cpp /src/benchmark/legacy.cpp
WORKDIR /src/benchmark
RUN cmake -S /src/icecat -B /build/cpp -G Ninja -DNETWORKIT_BUILD_TESTS=OFF -DNETWORKIT_NATIVE=OFF -DCMAKE_BUILD_TYPE=Release \
    && cmake --build /build/cpp --target networkit --parallel ${BUILD_JOBS} \
    && c++ -std=c++20 -O3 -fopenmp legacy.cpp -I/src/icecat/include -I/src/icecat/extlibs/tlx -I/src/icecat/extlibs/ttmath \
       -L/build/cpp -lnetworkit $(pkg-config --cflags --libs arrow) -Wl,-rpath,/opt/benchmark/lib -o legacy
COPY icecat/rust /src/icecat/rust
COPY grust /src/grust
COPY benchmark/Cargo.toml benchmark/Cargo.lock benchmark/rust-toolchain.toml /src/benchmark/
COPY benchmark/src /src/benchmark/src
COPY benchmark/neo4j/requirements.txt /src/benchmark/neo4j/requirements.txt
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    cargo build --release --locked --jobs ${BUILD_JOBS} \
    && cargo test --locked --manifest-path /src/icecat/rust/crates/grustcat/Cargo.toml --jobs ${BUILD_JOBS} \
    && cargo test --locked --manifest-path /src/icecat/rust/crates/grustcat-cypher/Cargo.toml --jobs ${BUILD_JOBS} \
    && mkdir -p /out/lib \
    && cp target/release/icecat target/release/grustcat target/release/grustcat-cypher legacy /out/ \
    && cp /build/cpp/libnetworkit.so* /out/lib/ \
    && ldd /out/legacy > /out/ldd.txt \
    && rustc --version > /out/rust-version.txt \
    && c++ --version > /out/cpp-version.txt \
    && dpkg-query -W > /out/packages.txt
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install --no-cache-dir -r neo4j/requirements.txt

FROM debian:bookworm-slim AS benchmark
ARG ARROW_VERSION=24.0.0-1
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl python3 libgomp1 \
    && curl -fsSL https://packages.apache.org/artifactory/arrow/debian/apache-arrow-apt-source-latest-bookworm.deb -o /tmp/arrow.deb \
    && apt-get install -y /tmp/arrow.deb && apt-get update \
    && apt-get install -y --no-install-recommends libarrow2400=${ARROW_VERSION} \
    && rm -rf /var/lib/apt/lists/* /tmp/arrow.deb
COPY --from=build /opt/venv /opt/venv
COPY --from=build /out /opt/benchmark
COPY benchmark/*.py /opt/benchmark/
COPY benchmark/neo4j/*.py benchmark/neo4j/*.json benchmark/neo4j/gds.jar /opt/benchmark/neo4j/
COPY --from=neo4j /versions/java.txt /opt/benchmark/neo4j/java-version.txt
COPY sources.json /opt/benchmark/sources.json
COPY entrypoint.py report.py /opt/benchmark/docker/
ENV PATH="/opt/venv/bin:$PATH" OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN ln -s icecat /opt/benchmark/rust-bench && mkdir /work && chmod 1777 /work
WORKDIR /opt/benchmark
RUN python3 check_cypher.py --output /opt/benchmark/cypher-validation.json
ENTRYPOINT ["python3", "/opt/benchmark/docker/entrypoint.py"]
CMD ["--full-path", "--sizes", "16384", "65536", "--repeats", "3", "--warmups", "1", "--label", "docker-full-path"]
