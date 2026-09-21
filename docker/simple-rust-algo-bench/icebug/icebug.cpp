// The `icebug` participant: the Arrow update of the NetworKit C++ codebase,
// called through NetworKit's own headers.
//
// Sink handling is DISTRIBUTE_SINKS rather than the library default, because
// every other participant redistributes dangling mass and a column that does
// not is computing a different function. The fixtures are dangling-free where
// PageRank runs, so this setting changes nothing there; it is set so that the
// participant is right rather than accidentally right.
#include <chrono>
#include <cstdio>
#include <cstring>
#include <fstream>
#include <string>
#include <unordered_set>
#include <vector>

#include <networkit/centrality/PageRank.hpp>
#include <networkit/components/WeaklyConnectedComponents.hpp>
#include <networkit/distance/BFS.hpp>
#include <networkit/graph/Graph.hpp>
#include <networkit/graph/GraphW.hpp>

using clock_type = std::chrono::steady_clock;
static double since(clock_type::time_point start) {
    return std::chrono::duration<double, std::milli>(clock_type::now() - start).count();
}

int main(int argc, char **argv) {
    std::string fixture, algorithm;
    double tolerance = 1e-8;
    for (int i = 1; i < argc; ++i) {
        if (!std::strcmp(argv[i], "--receipt")) {
            std::printf("{\"participant\":\"icebug\",\"version\":\"%s\",\"commit\":\"%s\","
                        "\"precision\":\"f64\",\"algorithms\":[\"pagerank\",\"wcc\",\"bfs\"],"
                        "\"parallel\":\"NetworKit OpenMP defaults\",\"width_capable\":true}\n",
                        BENCH_VERSION, BENCH_COMMIT);
            return 0;
        }
        if (!std::strcmp(argv[i], "--fixture") && i + 1 < argc) fixture = argv[++i];
        if (!std::strcmp(argv[i], "--algorithm") && i + 1 < argc) algorithm = argv[++i];
        if (!std::strcmp(argv[i], "--tolerance") && i + 1 < argc) tolerance = std::stod(argv[++i]);
    }

    auto started = clock_type::now();
    std::ifstream input(fixture);
    if (!input) { std::fprintf(stderr, "cannot open %s\n", fixture.c_str()); return 2; }
    std::size_t nodes = 0, declared = 0;
    input >> nodes >> declared;
    std::vector<std::pair<std::size_t, std::size_t>> edges;
    edges.reserve(declared);
    for (std::size_t source, target; input >> source >> target;) edges.emplace_back(source, target);
    if (edges.size() != declared) { std::fprintf(stderr, "fixture header disagrees with its body\n"); return 2; }
    const double parse_ms = since(started);

    started = clock_type::now();
    // This NetworKit is the Arrow update: `Graph` is an immutable reference view
    // and `GraphW` is the writable form. Build the writable one, then view it.
    NetworKit::GraphW writable(nodes, false, true);
    for (const auto &edge : edges) writable.addEdge(edge.first, edge.second);
    const NetworKit::Graph graph(writable);
    const double build_ms = since(started);

    std::string summary;
    double materialise_ms = 0;
    started = clock_type::now();
    if (algorithm == "pagerank") {
        NetworKit::PageRank kernel(graph, 0.85, tolerance, false,
                                   NetworKit::PageRank::SinkHandling::DISTRIBUTE_SINKS);
        kernel.run();
        const double kernel_ms = since(started);
        started = clock_type::now();
        const auto &scores = kernel.scores();
        double sum = 0, max = -1;
        std::size_t argmax = 0;
        for (std::size_t node = 0; node < scores.size(); ++node) {
            sum += scores[node];
            if (scores[node] > max) { max = scores[node]; argmax = node; }
        }
        materialise_ms = since(started);
        char buffer[512];
        std::snprintf(buffer, sizeof buffer,
                      "\"kernel_ms\":%.6f,\"iterations\":%zu,\"sum\":%.17g,\"max\":%.17g,\"argmax\":%zu",
                      kernel_ms, static_cast<std::size_t>(kernel.numberOfIterations()), sum, max, argmax);
        summary = buffer;
    } else if (algorithm == "wcc") {
        NetworKit::WeaklyConnectedComponents kernel(graph);
        kernel.run();
        const double kernel_ms = since(started);
        started = clock_type::now();
        const auto components = kernel.getPartition();
        std::unordered_set<NetworKit::index> distinct;
        for (std::size_t node = 0; node < nodes; ++node) distinct.insert(components[node]);
        materialise_ms = since(started);
        char buffer[256];
        std::snprintf(buffer, sizeof buffer, "\"kernel_ms\":%.6f,\"count\":%zu,\"probe_label\":%zu",
                      kernel_ms, distinct.size(), static_cast<std::size_t>(components[0]));
        summary = buffer;
    } else if (algorithm == "bfs") {
        NetworKit::BFS kernel(graph, 0, false);
        kernel.run();
        const double kernel_ms = since(started);
        started = clock_type::now();
        const auto &distances = kernel.getDistances();
        std::size_t reached = 0;
        long long total = 0;
        for (std::size_t node = 0; node < distances.size(); ++node) {
            const double distance = distances[node];
            if (distance < std::numeric_limits<double>::max()) {
                ++reached;
                total += static_cast<long long>(distance);
            }
        }
        materialise_ms = since(started);
        char buffer[256];
        std::snprintf(buffer, sizeof buffer, "\"kernel_ms\":%.6f,\"reached\":%zu,\"distance_sum\":%lld",
                      kernel_ms, reached, total);
        summary = buffer;
    } else {
        std::fprintf(stderr, "unknown or absent algorithm %s\n", algorithm.c_str());
        return 2;
    }

    std::printf("{\"participant\":\"icebug\",\"algorithm\":\"%s\",\"fixture\":\"%s\",\"nodes\":%zu,"
                "\"edges\":%zu,\"parse_ms\":%.6f,\"build_ms\":%.6f,%s,\"materialise_ms\":%.6f}\n",
                algorithm.c_str(), fixture.c_str(), nodes, edges.size(), parse_ms, build_ms,
                summary.c_str(), materialise_ms);
    return 0;
}
