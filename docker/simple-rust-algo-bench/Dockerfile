# simple-rust-algo-bench: five in-memory participants and nothing else.
#
# No JVM, no Neo4j, no GDS, no Turso — none of which belongs in a library
# comparison. The C++ NetworKit build stays, because `icebug` is that build: it
# is a participant rather than baggage, and it is also the reason this image
# exists at all, since Arrow C++ development headers are not present on the
# build hosts.
ARG ARROW_VERSION=24.0.0-1

FROM rust:1.97.1-bookworm AS cpp
ARG BUILD_JOBS=4
ARG ARROW_VERSION
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl cmake ninja-build pkg-config \
    && curl -fsSL https://packages.apache.org/artifactory/arrow/debian/apache-arrow-apt-source-latest-bookworm.deb -o /tmp/arrow.deb \
    && apt-get install -y /tmp/arrow.deb && apt-get update \
    && apt-get install -y --no-install-recommends libarrow-dev=${ARROW_VERSION} \
    && rm -rf /var/lib/apt/lists/* /tmp/arrow.deb
COPY icecat/CMakeLists.txt icecat/networkit.pc /src/icecat/
COPY icecat/include /src/icecat/include
COPY icecat/networkit /src/icecat/networkit
COPY icecat/extlibs /src/icecat/extlibs
# NetworKit compiles 372 objects and the driver is forty lines. Copying the
# driver after the library build means iterating on the driver does not
# recompile the library: the layer that changes often goes last.
RUN mkdir -p /out && cmake -S /src/icecat -B /build/cpp -G Ninja -DNETWORKIT_BUILD_TESTS=OFF -DNETWORKIT_NATIVE=OFF -DCMAKE_BUILD_TYPE=Release \
    && cmake --build /build/cpp --target networkit --parallel ${BUILD_JOBS}
COPY bench/icebug/icebug.cpp /src/bench/icebug.cpp
ARG ICEBUG_COMMIT=unknown
ARG ICEBUG_VERSION=unknown
RUN c++ -std=c++20 -O3 -fopenmp /src/bench/icebug.cpp \
       -DBENCH_COMMIT='"'${ICEBUG_COMMIT}'"' -DBENCH_VERSION='"'${ICEBUG_VERSION}'"' \
       -I/src/icecat/include -I/src/icecat/extlibs/tlx -I/src/icecat/extlibs/ttmath \
       -L/build/cpp -lnetworkit $(pkg-config --cflags --libs arrow) \
       -Wl,-rpath,/opt/bench/lib -o /out/icebug

FROM rust:1.97.1-bookworm AS rust
ARG BUILD_JOBS=4
COPY grust /src/grust
COPY icecat/rust /src/icecat/rust
# The participants' path dependencies are written relative to the host layout,
# so the image reproduces that layout rather than rewriting every manifest: a
# participant whose manifest the harness edited is not the participant.
COPY bench /src/adversarial-graph-algorithms/docker/simple-rust-algo-bench
# One participant per manifest: a workspace would unify features across them and
# a participant would stop being the code its own project builds.
ENV BENCH=/src/adversarial-graph-algorithms/docker/simple-rust-algo-bench
RUN mkdir -p /out && for participant in library grust icecat grustcat; do \
        cargo build --release --manifest-path $BENCH/$participant/Cargo.toml --jobs ${BUILD_JOBS} \
        && cp $BENCH/$participant/target/release/bench-$participant /out/$participant; \
    done

FROM debian:bookworm-slim AS bench
ARG ARROW_VERSION
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl python3 \
    && curl -fsSL https://packages.apache.org/artifactory/arrow/debian/apache-arrow-apt-source-latest-bookworm.deb -o /tmp/arrow.deb \
    && apt-get install -y /tmp/arrow.deb && apt-get update \
    && apt-get install -y --no-install-recommends libarrow2400=${ARROW_VERSION} libgomp1 \
    && rm -rf /var/lib/apt/lists/* /tmp/arrow.deb
COPY --from=cpp /out/icebug /opt/bench/
COPY --from=cpp /build/cpp/libnetworkit.so* /opt/bench/lib/
COPY --from=rust /out/ /opt/bench/
COPY bench/fixtures.py bench/reference.py bench/audit.py /opt/bench/
WORKDIR /opt/bench
