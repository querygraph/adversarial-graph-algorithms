#include <algorithm>
#include <chrono>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <map>
#include <networkit/auxiliary/Parallelism.hpp>
#include <networkit/auxiliary/Vector2Arrow.hpp>
#include <networkit/centrality/PageRank.hpp>
#include <networkit/components/StronglyConnectedComponents.hpp>
#include <networkit/components/WeaklyConnectedComponents.hpp>
#include <networkit/distance/BFS.hpp>
#include <networkit/distance/Dijkstra.hpp>
#include <networkit/graph/GraphR.hpp>
using namespace NetworKit;
int main(int argc, char **argv) {
  try {
    if (argc != 5)
      throw std::runtime_error("input algorithm output source required");
    Aux::setNumberOfThreads(1);
    std::ifstream f(argv[1]);
    count n, m;
    f >> n >> m;
    std::vector<std::vector<std::pair<node, double>>> out(n), in(n);
    for (count i = 0; i < m; ++i) {
      node u, v;
      double w;
      f >> u >> v >> w;
      if (!f || u >= n || v >= n)
        throw std::runtime_error("bad input");
      out[u].emplace_back(v, w);
      in[v].emplace_back(u, w);
    }
    std::vector<node> ot, it;
    std::vector<count> oo{0}, io{0};
    std::vector<double> ow, iw;
    for (node u = 0; u < n; ++u) {
      std::sort(out[u].begin(), out[u].end());
      std::sort(in[u].begin(), in[u].end());
      for (auto [v, w] : out[u]) {
        ot.push_back(v);
        ow.push_back(w);
      }
      for (auto [v, w] : in[u]) {
        it.push_back(v);
        iw.push_back(w);
      }
      oo.push_back(ot.size());
      io.push_back(it.size());
    }
    GraphR storage(
        n, true, Aux::vectorToArrow<node, arrow::UInt64Array>(std::move(ot)),
        Aux::vectorToArrow<count, arrow::UInt64Array>(std::move(oo)),
        Aux::vectorToArrow<node, arrow::UInt64Array>(std::move(it)),
        Aux::vectorToArrow<count, arrow::UInt64Array>(std::move(io)),
        Aux::vectorToArrow<double, arrow::DoubleArray>(std::move(ow)),
        Aux::vectorToArrow<double, arrow::DoubleArray>(std::move(iw)));
    auto g = storage.asGraph();
    std::string alg = argv[2];
    node source = std::stoull(argv[4]);
    std::vector<double> result;
    double ms = 0;
    count iterations = 0, reachable = 0, path_entries = 0, node_sum = 0;
    double cost_sum = 0;
    auto timed = [&](auto &algorithm) {
      auto start = std::chrono::steady_clock::now();
      algorithm.run();
      ms = std::chrono::duration<double, std::milli>(
               std::chrono::steady_clock::now() - start)
               .count();
    };
    if (alg == "pagerank") {
      PageRank p(g, .85, 1e-8, false, PageRank::DISTRIBUTE_SINKS);
      p.norm = PageRank::Norm::L1_NORM;
      p.maxIterations = 1000;
      timed(p);
      result = p.scores();
      iterations = p.numberOfIterations();
      if (iterations >= 1000)
        throw std::runtime_error("PageRank cap reached");
    } else if (alg == "bfs") {
      BFS b(g, source, false, false);
      timed(b);
      result = b.getDistances();
    } else if (alg == "dijkstra-full") {
      auto start = std::chrono::steady_clock::now();
      Dijkstra d(g, source, true, false);
      d.run();
      result = d.getDistances();
      for (node target = 0; target < n; ++target) {
        if (result[target] == std::numeric_limits<double>::max()) continue;
        auto nodes = target == source ? std::vector<node>{source} : d.getPath(target);
        std::vector<double> costs;
        costs.reserve(nodes.size());
        for (node u : nodes) costs.push_back(result[u]);
        ++reachable;
        path_entries += nodes.size();
        for (node u : nodes) node_sum += u;
        for (double cost : costs) cost_sum += cost;
      }
      ms = std::chrono::duration<double, std::milli>(
          std::chrono::steady_clock::now() - start).count();
    } else if (alg == "dijkstra") {
      Dijkstra d(g, source, false, false);
      timed(d);
      result = d.getDistances();
    } else {
      auto extract = [&](auto &c) {
        timed(c);
        std::map<count, node> minima;
        for (node u = 0; u < n; ++u) {
          auto id = c.componentOfNode(u);
          auto [it, inserted] = minima.emplace(id, u);
          if (!inserted)
            it->second = std::min(it->second, u);
        }
        for (node u = 0; u < n; ++u)
          result.push_back(minima.at(c.componentOfNode(u)));
      };
      if (alg == "wcc") {
        WeaklyConnectedComponents c(g);
        extract(c);
      } else if (alg == "scc") {
        StronglyConnectedComponents c(g);
        extract(c);
      } else
        throw std::runtime_error("unknown algorithm");
    }
    std::ofstream output(argv[3], std::ios::binary);
    for (auto x : result) {
      if (x == std::numeric_limits<double>::max())
        x = -1.;
      output.write(reinterpret_cast<const char *>(&x), sizeof(x));
    }
    std::cout << std::setprecision(17) << "{\"ms\":" << ms
              << ",\"iterations\":" << iterations
              << ",\"reachable\":" << reachable << ",\"path_entries\":" << path_entries
              << ",\"node_sum\":" << node_sum << ",\"cost_sum\":" << cost_sum << "}\n";
  } catch (const std::exception &e) {
    std::cerr << e.what() << '\n';
    return 1;
  }
}
