### `one-thread.json`: one-thread

workers 1, concurrency 1, 1 warmup + 5 repeats, steal over the run 1 ticks, 233.0 s, unusable at MAD/median >= 0.25

Not timed (no agreeing parity row): neo4j-graph pagerank layered-16384.edges, neo4j-graph pagerank layered-65536.edges, neo4j-graph pagerank path-16384.edges, neo4j-graph pagerank path-65536.edges 

| fixture | algorithm | participant | call | accounting | iters | total ms | MAD | MAD/median | per iter | build ms | incoming ms | work units | steal | usable |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| hub-16384 | bfs | `icebug` |  |  | - | 2.117 | 0.106 | 0.050 | - | 10.51 | - | - | 0 | yes |
| hub-16384 | bfs | `icecat` |  |  | - | 0.834 | 0.019 | 0.023 | - | 7.18 | - | - | 0 | yes |
| hub-16384 | bfs | `grustcat` |  |  | - | 0.700 | 0.031 | 0.045 | - | 91.63 | - | - | 0 | yes |
| hub-16384 | bfs | `grust#1` | first | counted | - | 1.630 | 0.023 | 0.014 | - | 22.04 | - | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust#1` | second | counted | - | 1.463 | 0.017 | 0.012 | - | 22.04 | - | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust#unset` | first | counted | - | 1.608 | 0.043 | 0.026 | - | 20.59 | - | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust#unset` | second | counted | - | 1.443 | 0.005 | 0.003 | - | 20.59 | - | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted#1` | first | counted | - | 1.611 | 0.015 | 0.009 | - | 22.36 | 1.79 | 1489517 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted#1` | second | counted | - | 1.469 | 0.017 | 0.011 | - | 22.36 | 1.79 | 1489517 | 0 | yes |
| hub-16384 | bfs | `grust-next@work-uncounted#1` | first | work-uncounted | - | 1.067 | 0.016 | 0.015 | - | 15.02 | 1.39 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@work-uncounted#1` | second | work-uncounted | - | 0.896 | 0.003 | 0.004 | - | 15.02 | 1.39 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@unchecked#1` | first | unchecked | - | 0.971 | 0.005 | 0.005 | - | 14.38 | 1.37 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@unchecked#1` | second | unchecked | - | 0.788 | 0.011 | 0.014 | - | 14.38 | 1.37 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@counted#unset` | first | counted | - | 1.618 | 0.011 | 0.007 | - | 23.35 | 1.82 | 1489517 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted#unset` | second | counted | - | 1.474 | 0.025 | 0.017 | - | 23.35 | 1.82 | 1489517 | 0 | yes |
| hub-16384 | bfs | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 1.060 | 0.029 | 0.028 | - | 14.69 | 1.35 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 0.901 | 0.010 | 0.012 | - | 14.69 | 1.35 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@unchecked#unset` | first | unchecked | - | 0.947 | 0.012 | 0.012 | - | 14.57 | 1.34 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@unchecked#unset` | second | unchecked | - | 0.786 | 0.016 | 0.021 | - | 14.57 | 1.34 | - | 0 | yes |
| hub-16384 | pagerank | `neo4j-graph` |  |  | 36 | 14.026 | 0.041 | 0.003 | 0.390 | 8.20 | - | - | 0 | yes |
| hub-16384 | pagerank | `icebug` |  |  | 12 | 7.991 | 0.154 | 0.019 | 0.666 | 10.60 | - | - | 0 | yes |
| hub-16384 | pagerank | `icecat` |  |  | 17 | 7.679 | 0.027 | 0.004 | 0.452 | 6.92 | - | - | 0 | yes |
| hub-16384 | pagerank | `grustcat` |  |  | 17 | 7.277 | 0.034 | 0.005 | 0.428 | 93.14 | - | - | 0 | yes |
| hub-16384 | pagerank | `grust#1` | first | counted | 17 | 11.562 | 0.054 | 0.005 | 0.680 | 19.67 | - | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust#1` | second | counted | 17 | 9.500 | 0.012 | 0.001 | 0.559 | 19.67 | - | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust#unset` | first | counted | 17 | 50.976 | 0.086 | 0.002 | 2.999 | 19.52 | - | 4567562 | 0 | yes |
| hub-16384 | pagerank | `grust#unset` | second | counted | 17 | 50.644 | 0.015 | 0.000 | 2.979 | 19.52 | - | 4567562 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted#1` | first | counted | 17 | 8.946 | 0.009 | 0.001 | 0.526 | 23.50 | 1.86 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted#1` | second | counted | 17 | 8.818 | 0.024 | 0.003 | 0.519 | 23.50 | 1.86 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 17 | 8.309 | 0.005 | 0.001 | 0.489 | 14.50 | 1.40 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 17 | 8.181 | 0.014 | 0.002 | 0.481 | 14.50 | 1.40 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@unchecked#1` | first | unchecked | 17 | 7.761 | 0.010 | 0.001 | 0.457 | 15.29 | 1.38 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@unchecked#1` | second | unchecked | 17 | 7.787 | 0.058 | 0.007 | 0.458 | 15.29 | 1.38 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted#unset` | first | counted | 17 | 23.043 | 0.123 | 0.005 | 1.355 | 22.36 | 1.82 | 5009502 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted#unset` | second | counted | 17 | 22.852 | 0.110 | 0.005 | 1.344 | 22.36 | 1.82 | 5009502 | 0 | yes |
| hub-16384 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 17 | 14.360 | 0.026 | 0.002 | 0.845 | 14.98 | 1.38 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 17 | 14.178 | 0.034 | 0.002 | 0.834 | 14.98 | 1.38 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 17 | 13.464 | 0.061 | 0.004 | 0.792 | 14.68 | 1.39 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 17 | 13.352 | 0.100 | 0.007 | 0.785 | 14.68 | 1.39 | - | 0 | yes |
| hub-16384 | triangles | `neo4j-graph` |  |  | - | 8.515 | 0.017 | 0.002 | - | 8.11 | - | - | 0 | yes |
| hub-16384 | triangles | `grust#1` | first | counted | - | 17.931 | 0.123 | 0.007 | - | 25.76 | - | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust#1` | second | counted | - | 15.811 | 0.057 | 0.004 | - | 25.76 | - | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust#unset` | first | counted | - | 17.741 | 0.123 | 0.007 | - | 24.57 | - | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust#unset` | second | counted | - | 15.681 | 0.072 | 0.005 | - | 24.57 | - | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted#1` | first | counted | - | 16.526 | 0.064 | 0.004 | - | 24.39 | 0.00 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted#1` | second | counted | - | 14.581 | 0.019 | 0.001 | - | 24.39 | 0.00 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@work-uncounted#1` | first | work-uncounted | - | 16.368 | 0.109 | 0.007 | - | 16.16 | 0.00 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@work-uncounted#1` | second | work-uncounted | - | 14.315 | 0.041 | 0.003 | - | 16.16 | 0.00 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@unchecked#1` | first | unchecked | - | 16.147 | 0.018 | 0.001 | - | 15.43 | 0.00 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@unchecked#1` | second | unchecked | - | 14.222 | 0.024 | 0.002 | - | 15.43 | 0.00 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@counted#unset` | first | counted | - | 16.715 | 0.144 | 0.009 | - | 25.80 | 0.00 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted#unset` | second | counted | - | 14.651 | 0.059 | 0.004 | - | 25.80 | 0.00 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 16.300 | 0.302 | 0.019 | - | 17.17 | 0.00 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 14.359 | 0.103 | 0.007 | - | 17.17 | 0.00 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@unchecked#unset` | first | unchecked | - | 16.353 | 0.071 | 0.004 | - | 16.19 | 0.00 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@unchecked#unset` | second | unchecked | - | 14.312 | 0.100 | 0.007 | - | 16.19 | 0.00 | - | 0 | yes |
| hub-16384 | wcc | `neo4j-graph` |  |  | - | 1.032 | 0.007 | 0.007 | - | 8.21 | - | - | 0 | yes |
| hub-16384 | wcc | `icebug` |  |  | - | 2.934 | 0.168 | 0.057 | - | 10.64 | - | - | 0 | yes |
| hub-16384 | wcc | `icecat` |  |  | - | 0.947 | 0.007 | 0.007 | - | 6.50 | - | - | 0 | yes |
| hub-16384 | wcc | `grustcat` |  |  | - | 0.587 | 0.005 | 0.009 | - | 94.82 | - | - | 0 | yes |
| hub-16384 | wcc | `grust#1` | first | counted | - | 1.578 | 0.014 | 0.009 | - | 19.09 | - | 1031191 | 0 | yes |
| hub-16384 | wcc | `grust#1` | second | counted | - | 1.735 | 0.017 | 0.010 | - | 19.09 | - | 1031191 | 0 | yes |
| hub-16384 | wcc | `grust#unset` | first | counted | - | 4.167 | 0.007 | 0.002 | - | 19.67 | - | 1324773 | 0 | yes |
| hub-16384 | wcc | `grust#unset` | second | counted | - | 4.153 | 0.005 | 0.001 | - | 19.67 | - | 1324773 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted#1` | first | counted | - | 1.622 | 0.023 | 0.014 | - | 21.99 | 1.80 | 1473131 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted#1` | second | counted | - | 1.446 | 0.015 | 0.010 | - | 21.99 | 1.80 | 1473131 | 0 | yes |
| hub-16384 | wcc | `grust-next@work-uncounted#1` | first | work-uncounted | - | 0.837 | 0.023 | 0.027 | - | 14.54 | 1.39 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@work-uncounted#1` | second | work-uncounted | - | 0.811 | 0.008 | 0.010 | - | 14.54 | 1.39 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@unchecked#1` | first | unchecked | - | 0.783 | 0.023 | 0.029 | - | 14.40 | 1.36 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@unchecked#1` | second | unchecked | - | 0.753 | 0.034 | 0.046 | - | 14.40 | 1.36 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@counted#unset` | first | counted | - | 4.682 | 0.005 | 0.001 | - | 22.18 | 1.80 | 1766713 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted#unset` | second | counted | - | 4.548 | 0.004 | 0.001 | - | 22.18 | 1.80 | 1766713 | 0 | yes |
| hub-16384 | wcc | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 1.934 | 0.013 | 0.007 | - | 15.10 | 1.37 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 1.944 | 0.012 | 0.006 | - | 15.10 | 1.37 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@unchecked#unset` | first | unchecked | - | 1.867 | 0.014 | 0.007 | - | 13.69 | 1.39 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@unchecked#unset` | second | unchecked | - | 1.895 | 0.019 | 0.010 | - | 13.69 | 1.39 | - | 0 | yes |
| hub-65536 | bfs | `icebug` |  |  | - | 16.074 | 0.282 | 0.018 | - | 72.99 | - | - | 0 | yes |
| hub-65536 | bfs | `icecat` |  |  | - | 4.787 | 0.135 | 0.028 | - | 22.74 | - | - | 0 | yes |
| hub-65536 | bfs | `grustcat` |  |  | - | 5.742 | 0.093 | 0.016 | - | 491.53 | - | - | 0 | yes |
| hub-65536 | bfs | `grust#1` | first | counted | - | 7.910 | 0.240 | 0.030 | - | 110.26 | - | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust#1` | second | counted | - | 6.260 | 0.187 | 0.030 | - | 110.26 | - | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust#unset` | first | counted | - | 10.492 | 0.283 | 0.027 | - | 112.85 | - | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust#unset` | second | counted | - | 8.307 | 0.176 | 0.021 | - | 112.85 | - | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted#1` | first | counted | - | 8.448 | 0.217 | 0.026 | - | 131.40 | 9.00 | 5959069 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted#1` | second | counted | - | 6.733 | 0.226 | 0.034 | - | 131.40 | 9.00 | 5959069 | 0 | yes |
| hub-65536 | bfs | `grust-next@work-uncounted#1` | first | work-uncounted | - | 8.048 | 0.083 | 0.010 | - | 74.51 | 7.06 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@work-uncounted#1` | second | work-uncounted | - | 6.259 | 0.070 | 0.011 | - | 74.51 | 7.06 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@unchecked#1` | first | unchecked | - | 7.968 | 0.388 | 0.049 | - | 74.56 | 6.75 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@unchecked#1` | second | unchecked | - | 6.395 | 0.181 | 0.028 | - | 74.56 | 6.75 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@counted#unset` | first | counted | - | 11.089 | 0.361 | 0.033 | - | 131.14 | 8.71 | 5959069 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted#unset` | second | counted | - | 8.676 | 0.327 | 0.038 | - | 131.14 | 8.71 | 5959069 | 0 | yes |
| hub-65536 | bfs | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 8.824 | 0.493 | 0.056 | - | 72.98 | 6.48 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 6.222 | 0.480 | 0.077 | - | 72.98 | 6.48 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@unchecked#unset` | first | unchecked | - | 8.651 | 0.618 | 0.071 | - | 73.73 | 6.89 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@unchecked#unset` | second | unchecked | - | 6.174 | 0.776 | 0.126 | - | 73.73 | 6.89 | - | 0 | yes |
| hub-65536 | pagerank | `neo4j-graph` |  |  | 28 | 40.032 | 0.402 | 0.010 | 1.430 | 59.09 | - | - | 0 | yes |
| hub-65536 | pagerank | `icebug` |  |  | 12 | 76.057 | 1.275 | 0.017 | 6.338 | 69.37 | - | - | 0 | yes |
| hub-65536 | pagerank | `icecat` |  |  | 17 | 31.736 | 0.085 | 0.003 | 1.867 | 22.76 | - | - | 0 | yes |
| hub-65536 | pagerank | `grustcat` |  |  | 17 | 34.010 | 0.344 | 0.010 | 2.001 | 482.83 | - | - | 0 | yes |
| hub-65536 | pagerank | `grust#1` | first | counted | 17 | 65.106 | 0.372 | 0.006 | 3.830 | 109.68 | - | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust#1` | second | counted | 17 | 55.678 | 4.071 | 0.073 | 3.275 | 109.68 | - | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust#unset` | first | counted | 17 | 206.767 | 0.876 | 0.004 | 12.163 | 110.51 | - | 18272770 | 0 | yes |
| hub-65536 | pagerank | `grust#unset` | second | counted | 17 | 207.566 | 2.733 | 0.013 | 12.210 | 110.51 | - | 18272770 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted#1` | first | counted | 17 | 36.897 | 0.071 | 0.002 | 2.170 | 127.68 | 8.52 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted#1` | second | counted | 17 | 36.547 | 0.184 | 0.005 | 2.150 | 127.68 | 8.52 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 17 | 34.151 | 0.220 | 0.006 | 2.009 | 71.95 | 6.50 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 17 | 33.720 | 0.233 | 0.007 | 1.984 | 71.95 | 6.50 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@unchecked#1` | first | unchecked | 17 | 32.425 | 0.382 | 0.012 | 1.907 | 69.54 | 6.54 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@unchecked#1` | second | unchecked | 17 | 32.060 | 0.201 | 0.006 | 1.886 | 69.54 | 6.54 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted#unset` | first | counted | 17 | 96.040 | 0.965 | 0.010 | 5.649 | 126.84 | 8.47 | 20040830 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted#unset` | second | counted | 17 | 94.263 | 0.599 | 0.006 | 5.545 | 126.84 | 8.47 | 20040830 | 0 | yes |
| hub-65536 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 17 | 61.089 | 0.514 | 0.008 | 3.593 | 74.75 | 6.77 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 17 | 59.620 | 0.258 | 0.004 | 3.507 | 74.75 | 6.77 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 17 | 58.184 | 0.510 | 0.009 | 3.423 | 71.30 | 6.64 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 17 | 56.862 | 1.624 | 0.029 | 3.345 | 71.30 | 6.64 | - | 0 | yes |
| hub-65536 | triangles | `neo4j-graph` |  |  | - | 42.308 | 0.737 | 0.017 | - | 58.07 | - | - | 0 | yes |
| hub-65536 | triangles | `grust#1` | first | counted | - | 83.893 | 2.647 | 0.032 | - | 135.93 | - | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust#1` | second | counted | - | 80.871 | 0.473 | 0.006 | - | 135.93 | - | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust#unset` | first | counted | - | 84.003 | 0.783 | 0.009 | - | 141.49 | - | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust#unset` | second | counted | - | 79.888 | 0.537 | 0.007 | - | 141.49 | - | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted#1` | first | counted | - | 77.024 | 1.574 | 0.020 | - | 149.41 | 0.00 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted#1` | second | counted | - | 73.685 | 0.362 | 0.005 | - | 149.41 | 0.00 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@work-uncounted#1` | first | work-uncounted | - | 77.258 | 0.608 | 0.008 | - | 81.46 | 0.00 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@work-uncounted#1` | second | work-uncounted | - | 72.362 | 0.939 | 0.013 | - | 81.46 | 0.00 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@unchecked#1` | first | unchecked | - | 75.895 | 0.708 | 0.009 | - | 84.82 | 0.00 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@unchecked#1` | second | unchecked | - | 71.628 | 0.811 | 0.011 | - | 84.82 | 0.00 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@counted#unset` | first | counted | - | 79.474 | 0.308 | 0.004 | - | 148.08 | 0.00 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted#unset` | second | counted | - | 73.800 | 0.409 | 0.006 | - | 148.08 | 0.00 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 76.281 | 0.759 | 0.010 | - | 85.43 | 0.00 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 71.399 | 1.757 | 0.025 | - | 85.43 | 0.00 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@unchecked#unset` | first | unchecked | - | 76.823 | 1.030 | 0.013 | - | 85.54 | 0.00 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@unchecked#unset` | second | unchecked | - | 72.293 | 0.586 | 0.008 | - | 85.54 | 0.00 | - | 0 | yes |
| hub-65536 | wcc | `neo4j-graph` |  |  | - | 3.843 | 0.007 | 0.002 | - | 61.52 | - | - | 0 | yes |
| hub-65536 | wcc | `icebug` |  |  | - | 22.335 | 0.594 | 0.027 | - | 75.84 | - | - | 0 | yes |
| hub-65536 | wcc | `icecat` |  |  | - | 3.802 | 0.004 | 0.001 | - | 23.14 | - | - | 0 | yes |
| hub-65536 | wcc | `grustcat` |  |  | - | 2.411 | 0.015 | 0.006 | - | 488.89 | - | - | 0 | yes |
| hub-65536 | wcc | `grust#1` | first | counted | - | 7.167 | 0.087 | 0.012 | - | 113.45 | - | 4125471 | 0 | yes |
| hub-65536 | wcc | `grust#1` | second | counted | - | 7.569 | 0.018 | 0.002 | - | 113.45 | - | 4125471 | 0 | yes |
| hub-65536 | wcc | `grust#unset` | first | counted | - | 17.280 | 0.104 | 0.006 | - | 113.02 | - | 5303155 | 0 | yes |
| hub-65536 | wcc | `grust#unset` | second | counted | - | 17.329 | 0.147 | 0.009 | - | 113.02 | - | 5303155 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted#1` | first | counted | - | 7.311 | 0.026 | 0.004 | - | 132.84 | 8.75 | 5893531 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted#1` | second | counted | - | 6.782 | 0.041 | 0.006 | - | 132.84 | 8.75 | 5893531 | 0 | yes |
| hub-65536 | wcc | `grust-next@work-uncounted#1` | first | work-uncounted | - | 4.930 | 0.067 | 0.014 | - | 73.41 | 6.92 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@work-uncounted#1` | second | work-uncounted | - | 4.972 | 0.051 | 0.010 | - | 73.41 | 6.92 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@unchecked#1` | first | unchecked | - | 4.625 | 0.045 | 0.010 | - | 73.16 | 6.67 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@unchecked#1` | second | unchecked | - | 4.633 | 0.067 | 0.015 | - | 73.16 | 6.67 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@counted#unset` | first | counted | - | 19.782 | 0.062 | 0.003 | - | 132.18 | 9.15 | 7071215 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted#unset` | second | counted | - | 18.862 | 0.022 | 0.001 | - | 132.18 | 9.15 | 7071215 | 0 | yes |
| hub-65536 | wcc | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 10.154 | 0.035 | 0.003 | - | 75.26 | 7.03 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 10.297 | 0.034 | 0.003 | - | 75.26 | 7.03 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@unchecked#unset` | first | unchecked | - | 9.519 | 0.128 | 0.013 | - | 73.11 | 7.00 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@unchecked#unset` | second | unchecked | - | 9.644 | 0.097 | 0.010 | - | 73.11 | 7.00 | - | 0 | yes |
| layered-16384 | bfs | `icebug` |  |  | - | 0.543 | 0.007 | 0.013 | - | 2.83 | - | - | 0 | yes |
| layered-16384 | bfs | `icecat` |  |  | - | 0.371 | 0.004 | 0.011 | - | 1.71 | - | - | 0 | yes |
| layered-16384 | bfs | `grustcat` |  |  | - | 0.259 | 0.002 | 0.007 | - | 34.42 | - | - | 0 | yes |
| layered-16384 | bfs | `grust#1` | first | counted | - | 0.458 | 0.002 | 0.004 | - | 7.17 | - | 347308 | 0 | yes |
| layered-16384 | bfs | `grust#1` | second | counted | - | 0.386 | 0.001 | 0.002 | - | 7.17 | - | 347308 | 0 | yes |
| layered-16384 | bfs | `grust#unset` | first | counted | - | 0.465 | 0.008 | 0.016 | - | 7.05 | - | 347308 | 0 | yes |
| layered-16384 | bfs | `grust#unset` | second | counted | - | 0.386 | 0.002 | 0.004 | - | 7.05 | - | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted#1` | first | counted | - | 0.509 | 0.002 | 0.004 | - | 7.96 | 0.73 | 493703 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted#1` | second | counted | - | 0.379 | 0.001 | 0.002 | - | 7.96 | 0.73 | 493703 | 0 | yes |
| layered-16384 | bfs | `grust-next@work-uncounted#1` | first | work-uncounted | - | 0.397 | 0.002 | 0.006 | - | 5.89 | 0.41 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@work-uncounted#1` | second | work-uncounted | - | 0.269 | 0.000 | 0.001 | - | 5.89 | 0.41 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@unchecked#1` | first | unchecked | - | 0.386 | 0.001 | 0.003 | - | 5.74 | 0.40 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@unchecked#1` | second | unchecked | - | 0.257 | 0.001 | 0.003 | - | 5.74 | 0.40 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@counted#unset` | first | counted | - | 0.514 | 0.004 | 0.008 | - | 8.04 | 0.75 | 493703 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted#unset` | second | counted | - | 0.381 | 0.002 | 0.006 | - | 8.04 | 0.75 | 493703 | 0 | yes |
| layered-16384 | bfs | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 0.395 | 0.002 | 0.006 | - | 5.85 | 0.41 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 0.270 | 0.001 | 0.005 | - | 5.85 | 0.41 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@unchecked#unset` | first | unchecked | - | 0.390 | 0.003 | 0.007 | - | 5.79 | 0.40 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@unchecked#unset` | second | unchecked | - | 0.258 | 0.001 | 0.003 | - | 5.79 | 0.40 | - | 0 | yes |
| layered-16384 | pagerank | `icebug` |  |  | 69 | 26.652 | 0.120 | 0.004 | 0.386 | 2.86 | - | - | 0 | yes |
| layered-16384 | pagerank | `icecat` |  |  | 84 | 23.276 | 0.025 | 0.001 | 0.277 | 1.76 | - | - | 0 | yes |
| layered-16384 | pagerank | `grustcat` |  |  | 84 | 26.661 | 0.047 | 0.002 | 0.317 | 34.28 | - | - | 0 | yes |
| layered-16384 | pagerank | `grust#1` | first | counted | 84 | 29.518 | 0.023 | 0.001 | 0.351 | 7.13 | - | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust#1` | second | counted | 84 | 28.565 | 0.022 | 0.001 | 0.340 | 7.13 | - | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust#unset` | first | counted | 84 | 116.150 | 0.115 | 0.001 | 1.383 | 7.27 | - | 8667337 | 0 | yes |
| layered-16384 | pagerank | `grust#unset` | second | counted | 84 | 115.651 | 0.078 | 0.001 | 1.377 | 7.27 | - | 8667337 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted#1` | first | counted | 84 | 30.378 | 0.106 | 0.003 | 0.362 | 8.02 | 0.74 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted#1` | second | counted | 84 | 30.256 | 0.046 | 0.002 | 0.360 | 8.02 | 0.74 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 84 | 28.168 | 0.078 | 0.003 | 0.335 | 5.87 | 0.41 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 84 | 28.100 | 0.028 | 0.001 | 0.335 | 5.87 | 0.41 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@unchecked#1` | first | unchecked | 84 | 27.543 | 0.055 | 0.002 | 0.328 | 5.80 | 0.40 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@unchecked#1` | second | unchecked | 84 | 27.377 | 0.029 | 0.001 | 0.326 | 5.80 | 0.40 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted#unset` | first | counted | 84 | 86.813 | 0.150 | 0.002 | 1.033 | 7.98 | 0.74 | 8813732 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted#unset` | second | counted | 84 | 86.597 | 0.065 | 0.001 | 1.031 | 7.98 | 0.74 | 8813732 | 0 | yes |
| layered-16384 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 84 | 45.998 | 0.067 | 0.001 | 0.548 | 5.91 | 0.41 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 84 | 45.811 | 0.051 | 0.001 | 0.545 | 5.91 | 0.41 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 84 | 40.191 | 0.085 | 0.002 | 0.478 | 5.83 | 0.40 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 84 | 40.126 | 0.040 | 0.001 | 0.478 | 5.83 | 0.40 | - | 0 | yes |
| layered-16384 | triangles | `neo4j-graph` |  |  | - | 0.876 | 0.017 | 0.019 | - | 2.33 | - | - | 0 | yes |
| layered-16384 | triangles | `grust#1` | first | counted | - | 2.869 | 0.006 | 0.002 | - | 7.57 | - | 718265 | 0 | yes |
| layered-16384 | triangles | `grust#1` | second | counted | - | 2.225 | 0.013 | 0.006 | - | 7.57 | - | 718265 | 0 | yes |
| layered-16384 | triangles | `grust#unset` | first | counted | - | 2.886 | 0.013 | 0.004 | - | 7.43 | - | 718265 | 0 | yes |
| layered-16384 | triangles | `grust#unset` | second | counted | - | 2.223 | 0.005 | 0.002 | - | 7.43 | - | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted#1` | first | counted | - | 2.892 | 0.023 | 0.008 | - | 7.65 | 0.00 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted#1` | second | counted | - | 2.241 | 0.012 | 0.005 | - | 7.65 | 0.00 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@work-uncounted#1` | first | work-uncounted | - | 2.711 | 0.009 | 0.003 | - | 5.80 | 0.00 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@work-uncounted#1` | second | work-uncounted | - | 2.038 | 0.011 | 0.005 | - | 5.80 | 0.00 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@unchecked#1` | first | unchecked | - | 2.676 | 0.022 | 0.008 | - | 5.73 | 0.00 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@unchecked#1` | second | unchecked | - | 1.999 | 0.009 | 0.005 | - | 5.73 | 0.00 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@counted#unset` | first | counted | - | 2.897 | 0.012 | 0.004 | - | 7.71 | 0.00 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted#unset` | second | counted | - | 2.232 | 0.015 | 0.007 | - | 7.71 | 0.00 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 2.704 | 0.009 | 0.003 | - | 5.86 | 0.00 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 2.040 | 0.005 | 0.002 | - | 5.86 | 0.00 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@unchecked#unset` | first | unchecked | - | 2.673 | 0.003 | 0.001 | - | 5.83 | 0.00 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@unchecked#unset` | second | unchecked | - | 1.995 | 0.009 | 0.004 | - | 5.83 | 0.00 | - | 0 | yes |
| layered-16384 | wcc | `neo4j-graph` |  |  | - | 0.945 | 0.005 | 0.005 | - | 2.36 | - | - | 0 | yes |
| layered-16384 | wcc | `icebug` |  |  | - | 1.060 | 0.016 | 0.015 | - | 2.83 | - | - | 0 | yes |
| layered-16384 | wcc | `icecat` |  |  | - | 0.517 | 0.003 | 0.007 | - | 1.74 | - | - | 0 | yes |
| layered-16384 | wcc | `grustcat` |  |  | - | 0.357 | 0.001 | 0.002 | - | 34.09 | - | - | 0 | yes |
| layered-16384 | wcc | `grust#1` | first | counted | - | 0.641 | 0.005 | 0.008 | - | 7.09 | - | 341578 | 0 | yes |
| layered-16384 | wcc | `grust#1` | second | counted | - | 0.664 | 0.003 | 0.005 | - | 7.09 | - | 341578 | 0 | yes |
| layered-16384 | wcc | `grust#unset` | first | counted | - | 1.456 | 0.006 | 0.004 | - | 7.01 | - | 438267 | 0 | yes |
| layered-16384 | wcc | `grust#unset` | second | counted | - | 1.421 | 0.002 | 0.001 | - | 7.01 | - | 438267 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted#1` | first | counted | - | 0.745 | 0.008 | 0.011 | - | 7.96 | 0.74 | 487973 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted#1` | second | counted | - | 0.588 | 0.002 | 0.003 | - | 7.96 | 0.74 | 487973 | 0 | yes |
| layered-16384 | wcc | `grust-next@work-uncounted#1` | first | work-uncounted | - | 0.532 | 0.001 | 0.001 | - | 5.82 | 0.41 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@work-uncounted#1` | second | work-uncounted | - | 0.529 | 0.006 | 0.012 | - | 5.82 | 0.41 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@unchecked#1` | first | unchecked | - | 0.492 | 0.001 | 0.001 | - | 5.74 | 0.40 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@unchecked#1` | second | unchecked | - | 0.487 | 0.002 | 0.004 | - | 5.74 | 0.40 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@counted#unset` | first | counted | - | 1.683 | 0.005 | 0.003 | - | 7.85 | 0.74 | 584662 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted#unset` | second | counted | - | 1.535 | 0.004 | 0.003 | - | 7.85 | 0.74 | 584662 | 0 | yes |
| layered-16384 | wcc | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 0.869 | 0.006 | 0.006 | - | 5.86 | 0.41 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 0.865 | 0.003 | 0.003 | - | 5.86 | 0.41 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@unchecked#unset` | first | unchecked | - | 0.833 | 0.005 | 0.006 | - | 5.61 | 0.40 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@unchecked#unset` | second | unchecked | - | 0.813 | 0.006 | 0.008 | - | 5.61 | 0.40 | - | 0 | yes |
| layered-65536 | bfs | `icebug` |  |  | - | 2.895 | 0.043 | 0.015 | - | 11.39 | - | - | 0 | yes |
| layered-65536 | bfs | `icecat` |  |  | - | 1.582 | 0.011 | 0.007 | - | 7.48 | - | - | 0 | yes |
| layered-65536 | bfs | `grustcat` |  |  | - | 1.051 | 0.031 | 0.030 | - | 144.36 | - | - | 0 | yes |
| layered-65536 | bfs | `grust#1` | first | counted | - | 1.885 | 0.001 | 0.001 | - | 32.99 | - | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust#1` | second | counted | - | 1.602 | 0.015 | 0.010 | - | 32.99 | - | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust#unset` | first | counted | - | 1.900 | 0.025 | 0.013 | - | 31.13 | - | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust#unset` | second | counted | - | 1.587 | 0.003 | 0.002 | - | 31.13 | - | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted#1` | first | counted | - | 2.073 | 0.011 | 0.006 | - | 37.66 | 3.04 | 1979713 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted#1` | second | counted | - | 1.594 | 0.027 | 0.017 | - | 37.66 | 3.04 | 1979713 | 0 | yes |
| layered-65536 | bfs | `grust-next@work-uncounted#1` | first | work-uncounted | - | 1.619 | 0.013 | 0.008 | - | 27.67 | 1.69 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@work-uncounted#1` | second | work-uncounted | - | 1.106 | 0.003 | 0.003 | - | 27.67 | 1.69 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@unchecked#1` | first | unchecked | - | 1.583 | 0.019 | 0.012 | - | 27.72 | 1.62 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@unchecked#1` | second | unchecked | - | 1.079 | 0.014 | 0.013 | - | 27.72 | 1.62 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@counted#unset` | first | counted | - | 2.082 | 0.023 | 0.011 | - | 37.19 | 3.01 | 1979713 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted#unset` | second | counted | - | 1.586 | 0.003 | 0.002 | - | 37.19 | 3.01 | 1979713 | 0 | yes |
| layered-65536 | bfs | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 1.636 | 0.027 | 0.017 | - | 25.78 | 1.64 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 1.093 | 0.006 | 0.005 | - | 25.78 | 1.64 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@unchecked#unset` | first | unchecked | - | 1.560 | 0.002 | 0.001 | - | 26.53 | 1.61 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@unchecked#unset` | second | unchecked | - | 1.069 | 0.004 | 0.003 | - | 26.53 | 1.61 | - | 0 | yes |
| layered-65536 | pagerank | `icebug` |  |  | 60 | 103.408 | 2.611 | 0.025 | 1.723 | 11.34 | - | - | 0 | yes |
| layered-65536 | pagerank | `icecat` |  |  | 75 | 88.140 | 0.108 | 0.001 | 1.175 | 6.96 | - | - | 0 | yes |
| layered-65536 | pagerank | `grustcat` |  |  | 75 | 95.941 | 0.211 | 0.002 | 1.279 | 143.24 | - | - | 0 | yes |
| layered-65536 | pagerank | `grust#1` | first | counted | 75 | 106.537 | 0.096 | 0.001 | 1.420 | 33.60 | - | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust#1` | second | counted | 75 | 102.595 | 0.016 | 0.000 | 1.368 | 33.60 | - | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust#unset` | first | counted | 75 | 417.200 | 0.576 | 0.001 | 5.563 | 34.06 | - | 31164642 | 0 | yes |
| layered-65536 | pagerank | `grust#unset` | second | counted | 75 | 416.216 | 0.373 | 0.001 | 5.550 | 34.06 | - | 31164642 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted#1` | first | counted | 75 | 107.984 | 0.408 | 0.004 | 1.440 | 37.16 | 3.02 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted#1` | second | counted | 75 | 107.576 | 0.135 | 0.001 | 1.434 | 37.16 | 3.02 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 75 | 100.440 | 0.151 | 0.002 | 1.339 | 27.01 | 1.69 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 75 | 99.913 | 0.043 | 0.000 | 1.332 | 27.01 | 1.69 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@unchecked#1` | first | unchecked | 75 | 98.311 | 0.464 | 0.005 | 1.311 | 26.99 | 1.61 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@unchecked#1` | second | unchecked | 75 | 97.534 | 0.107 | 0.001 | 1.300 | 26.99 | 1.61 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted#unset` | first | counted | 75 | 313.136 | 0.628 | 0.002 | 4.175 | 35.69 | 3.02 | 31750996 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted#unset` | second | counted | 75 | 311.475 | 0.471 | 0.002 | 4.153 | 35.69 | 3.02 | 31750996 | 0 | yes |
| layered-65536 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 75 | 164.986 | 0.115 | 0.001 | 2.200 | 27.84 | 1.66 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 75 | 164.212 | 0.837 | 0.005 | 2.189 | 27.84 | 1.66 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 75 | 145.102 | 0.207 | 0.001 | 1.935 | 25.83 | 1.60 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 75 | 144.123 | 0.330 | 0.002 | 1.922 | 25.83 | 1.60 | - | 0 | yes |
| layered-65536 | triangles | `neo4j-graph` |  |  | - | 2.970 | 0.023 | 0.008 | - | 8.80 | - | - | 0 | yes |
| layered-65536 | triangles | `grust#1` | first | counted | - | 11.570 | 0.062 | 0.005 | - | 33.52 | - | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust#1` | second | counted | - | 9.050 | 0.045 | 0.005 | - | 33.52 | - | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust#unset` | first | counted | - | 11.674 | 0.050 | 0.004 | - | 36.06 | - | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust#unset` | second | counted | - | 9.056 | 0.084 | 0.009 | - | 36.06 | - | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted#1` | first | counted | - | 11.635 | 0.009 | 0.001 | - | 36.11 | 0.00 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted#1` | second | counted | - | 9.043 | 0.009 | 0.001 | - | 36.11 | 0.00 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@work-uncounted#1` | first | work-uncounted | - | 10.943 | 0.029 | 0.003 | - | 27.00 | 0.00 | - | 0 | yes |
| layered-65536 | triangles | `grust-next@work-uncounted#1` | second | work-uncounted | - | 8.346 | 0.122 | 0.015 | - | 27.00 | 0.00 | - | 0 | yes |
| layered-65536 | triangles | `grust-next@unchecked#1` | first | unchecked | - | 10.699 | 0.037 | 0.003 | - | 26.86 | 0.00 | - | 0 | yes |
| layered-65536 | triangles | `grust-next@unchecked#1` | second | unchecked | - | 8.138 | 0.024 | 0.003 | - | 26.86 | 0.00 | - | 0 | yes |
| layered-65536 | triangles | `grust-next@counted#unset` | first | counted | - | 11.668 | 0.096 | 0.008 | - | 36.07 | 0.00 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted#unset` | second | counted | - | 9.039 | 0.031 | 0.003 | - | 36.07 | 0.00 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 10.865 | 0.042 | 0.004 | - | 26.52 | 0.00 | - | 0 | yes |
| layered-65536 | triangles | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 8.306 | 0.034 | 0.004 | - | 26.52 | 0.00 | - | 0 | yes |
| layered-65536 | triangles | `grust-next@unchecked#unset` | first | unchecked | - | 10.676 | 0.020 | 0.002 | - | 25.39 | 0.00 | - | 0 | yes |
| layered-65536 | triangles | `grust-next@unchecked#unset` | second | unchecked | - | 8.121 | 0.061 | 0.008 | - | 25.39 | 0.00 | - | 0 | yes |
| layered-65536 | wcc | `neo4j-graph` |  |  | - | 3.525 | 0.011 | 0.003 | - | 8.91 | - | - | 0 | yes |
| layered-65536 | wcc | `icebug` |  |  | - | 4.740 | 0.025 | 0.005 | - | 11.45 | - | - | 0 | yes |
| layered-65536 | wcc | `icecat` |  |  | - | 2.192 | 0.015 | 0.007 | - | 7.54 | - | - | 0 | yes |
| layered-65536 | wcc | `grustcat` |  |  | - | 1.466 | 0.015 | 0.010 | - | 142.63 | - | - | 0 | yes |
| layered-65536 | wcc | `grust#1` | first | counted | - | 2.632 | 0.012 | 0.005 | - | 32.61 | - | 1368146 | 0 | yes |
| layered-65536 | wcc | `grust#1` | second | counted | - | 2.745 | 0.019 | 0.007 | - | 32.61 | - | 1368146 | 0 | yes |
| layered-65536 | wcc | `grust#unset` | first | counted | - | 5.818 | 0.034 | 0.006 | - | 32.37 | - | 1755282 | 0 | yes |
| layered-65536 | wcc | `grust#unset` | second | counted | - | 5.774 | 0.013 | 0.002 | - | 32.37 | - | 1755282 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted#1` | first | counted | - | 3.006 | 0.009 | 0.003 | - | 36.88 | 3.00 | 1954500 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted#1` | second | counted | - | 2.448 | 0.036 | 0.015 | - | 36.88 | 3.00 | 1954500 | 0 | yes |
| layered-65536 | wcc | `grust-next@work-uncounted#1` | first | work-uncounted | - | 2.231 | 0.020 | 0.009 | - | 27.02 | 1.70 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@work-uncounted#1` | second | work-uncounted | - | 2.206 | 0.013 | 0.006 | - | 27.02 | 1.70 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@unchecked#1` | first | unchecked | - | 2.043 | 0.020 | 0.010 | - | 25.87 | 1.61 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@unchecked#1` | second | unchecked | - | 2.042 | 0.011 | 0.006 | - | 25.87 | 1.61 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@counted#unset` | first | counted | - | 6.776 | 0.014 | 0.002 | - | 37.27 | 3.00 | 2341636 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted#unset` | second | counted | - | 6.231 | 0.016 | 0.002 | - | 37.27 | 3.00 | 2341636 | 0 | yes |
| layered-65536 | wcc | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 3.548 | 0.030 | 0.008 | - | 27.41 | 1.68 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 3.552 | 0.010 | 0.003 | - | 27.41 | 1.68 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@unchecked#unset` | first | unchecked | - | 3.355 | 0.031 | 0.009 | - | 27.33 | 1.60 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@unchecked#unset` | second | unchecked | - | 3.357 | 0.017 | 0.005 | - | 27.33 | 1.60 | - | 0 | yes |
| path-16384 | bfs | `icebug` |  |  | - | 0.282 | 0.005 | 0.018 | - | 1.81 | - | - | 0 | yes |
| path-16384 | bfs | `icecat` |  |  | - | 0.249 | 0.003 | 0.011 | - | 0.90 | - | - | 0 | yes |
| path-16384 | bfs | `grustcat` |  |  | - | 0.139 | 0.001 | 0.005 | - | 27.40 | - | - | 0 | yes |
| path-16384 | bfs | `grust#1` | first | counted | - | 0.420 | 0.001 | 0.002 | - | 5.20 | - | 245755 | 0 | yes |
| path-16384 | bfs | `grust#1` | second | counted | - | 0.340 | 0.000 | 0.001 | - | 5.20 | - | 245755 | 0 | yes |
| path-16384 | bfs | `grust#unset` | first | counted | - | 0.428 | 0.010 | 0.022 | - | 5.15 | - | 245755 | 0 | yes |
| path-16384 | bfs | `grust#unset` | second | counted | - | 0.342 | 0.002 | 0.007 | - | 5.15 | - | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@counted#1` | first | counted | - | 0.459 | 0.002 | 0.005 | - | 5.91 | 0.63 | 344057 | 0 | yes |
| path-16384 | bfs | `grust-next@counted#1` | second | counted | - | 0.321 | 0.000 | 0.001 | - | 5.91 | 0.63 | 344057 | 0 | yes |
| path-16384 | bfs | `grust-next@work-uncounted#1` | first | work-uncounted | - | 0.258 | 0.008 | 0.031 | - | 4.37 | 0.29 | - | 0 | yes |
| path-16384 | bfs | `grust-next@work-uncounted#1` | second | work-uncounted | - | 0.114 | 0.000 | 0.001 | - | 4.37 | 0.29 | - | 0 | yes |
| path-16384 | bfs | `grust-next@unchecked#1` | first | unchecked | - | 0.245 | 0.003 | 0.011 | - | 4.34 | 0.28 | - | 0 | yes |
| path-16384 | bfs | `grust-next@unchecked#1` | second | unchecked | - | 0.105 | 0.000 | 0.004 | - | 4.34 | 0.28 | - | 0 | yes |
| path-16384 | bfs | `grust-next@counted#unset` | first | counted | - | 0.460 | 0.000 | 0.000 | - | 5.95 | 0.63 | 344057 | 0 | yes |
| path-16384 | bfs | `grust-next@counted#unset` | second | counted | - | 0.321 | 0.000 | 0.001 | - | 5.95 | 0.63 | 344057 | 0 | yes |
| path-16384 | bfs | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 0.254 | 0.002 | 0.009 | - | 4.47 | 0.29 | - | 0 | yes |
| path-16384 | bfs | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 0.114 | 0.001 | 0.005 | - | 4.47 | 0.29 | - | 0 | yes |
| path-16384 | bfs | `grust-next@unchecked#unset` | first | unchecked | - | 0.244 | 0.002 | 0.006 | - | 4.40 | 0.28 | - | 0 | yes |
| path-16384 | bfs | `grust-next@unchecked#unset` | second | unchecked | - | 0.105 | 0.000 | 0.001 | - | 4.40 | 0.28 | - | 0 | yes |
| path-16384 | pagerank | `icebug` |  |  | 54 | 12.902 | 0.046 | 0.004 | 0.239 | 1.79 | - | - | 0 | yes |
| path-16384 | pagerank | `icecat` |  |  | 58 | 9.703 | 0.007 | 0.001 | 0.167 | 0.92 | - | - | 0 | yes |
| path-16384 | pagerank | `grustcat` |  |  | 58 | 9.714 | 0.020 | 0.002 | 0.167 | 27.14 | - | - | 0 | yes |
| path-16384 | pagerank | `grust#1` | first | counted | 58 | 15.427 | 0.053 | 0.003 | 0.266 | 5.29 | - | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust#1` | second | counted | 58 | 14.689 | 0.085 | 0.006 | 0.253 | 5.29 | - | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust#unset` | first | counted | 58 | 67.304 | 0.265 | 0.004 | 1.160 | 5.32 | - | 5062591 | 0 | yes |
| path-16384 | pagerank | `grust#unset` | second | counted | 58 | 67.150 | 0.316 | 0.005 | 1.158 | 5.32 | - | 5062591 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted#1` | first | counted | 58 | 13.931 | 0.002 | 0.000 | 0.240 | 5.99 | 0.63 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted#1` | second | counted | 58 | 13.780 | 0.006 | 0.000 | 0.238 | 5.99 | 0.63 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 58 | 10.773 | 0.036 | 0.003 | 0.186 | 4.48 | 0.29 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 58 | 10.626 | 0.019 | 0.002 | 0.183 | 4.48 | 0.29 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@unchecked#1` | first | unchecked | 58 | 10.223 | 0.004 | 0.000 | 0.176 | 4.45 | 0.28 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@unchecked#1` | second | unchecked | 58 | 10.113 | 0.007 | 0.001 | 0.174 | 4.45 | 0.28 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@counted#unset` | first | counted | 58 | 59.310 | 0.207 | 0.003 | 1.023 | 6.04 | 0.63 | 5160893 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted#unset` | second | counted | 58 | 58.835 | 0.135 | 0.002 | 1.014 | 6.04 | 0.63 | 5160893 | 0 | yes |
| path-16384 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 58 | 29.756 | 0.055 | 0.002 | 0.513 | 4.50 | 0.29 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 58 | 29.529 | 0.027 | 0.001 | 0.509 | 4.50 | 0.29 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 58 | 26.516 | 0.153 | 0.006 | 0.457 | 4.49 | 0.28 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 58 | 26.427 | 0.074 | 0.003 | 0.456 | 4.49 | 0.28 | - | 0 | yes |
| path-16384 | triangles | `neo4j-graph` |  |  | - | 0.320 | 0.004 | 0.012 | - | 1.57 | - | - | 0 | yes |
| path-16384 | triangles | `grust#1` | first | counted | - | 1.561 | 0.015 | 0.009 | - | 5.42 | - | 425970 | 0 | yes |
| path-16384 | triangles | `grust#1` | second | counted | - | 1.082 | 0.007 | 0.006 | - | 5.42 | - | 425970 | 0 | yes |
| path-16384 | triangles | `grust#unset` | first | counted | - | 1.550 | 0.005 | 0.003 | - | 5.38 | - | 425970 | 0 | yes |
| path-16384 | triangles | `grust#unset` | second | counted | - | 1.079 | 0.003 | 0.003 | - | 5.38 | - | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted#1` | first | counted | - | 1.554 | 0.008 | 0.005 | - | 5.51 | 0.00 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted#1` | second | counted | - | 1.085 | 0.002 | 0.002 | - | 5.51 | 0.00 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@work-uncounted#1` | first | work-uncounted | - | 1.354 | 0.002 | 0.002 | - | 4.41 | 0.00 | - | 0 | yes |
| path-16384 | triangles | `grust-next@work-uncounted#1` | second | work-uncounted | - | 0.900 | 0.006 | 0.007 | - | 4.41 | 0.00 | - | 0 | yes |
| path-16384 | triangles | `grust-next@unchecked#1` | first | unchecked | - | 1.320 | 0.004 | 0.003 | - | 4.36 | 0.00 | - | 0 | yes |
| path-16384 | triangles | `grust-next@unchecked#1` | second | unchecked | - | 0.883 | 0.003 | 0.004 | - | 4.36 | 0.00 | - | 0 | yes |
| path-16384 | triangles | `grust-next@counted#unset` | first | counted | - | 1.565 | 0.017 | 0.011 | - | 5.42 | 0.00 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted#unset` | second | counted | - | 1.085 | 0.002 | 0.001 | - | 5.42 | 0.00 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 1.371 | 0.007 | 0.005 | - | 4.32 | 0.00 | - | 0 | yes |
| path-16384 | triangles | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 0.902 | 0.001 | 0.001 | - | 4.32 | 0.00 | - | 0 | yes |
| path-16384 | triangles | `grust-next@unchecked#unset` | first | unchecked | - | 1.317 | 0.011 | 0.008 | - | 4.32 | 0.00 | - | 0 | yes |
| path-16384 | triangles | `grust-next@unchecked#unset` | second | unchecked | - | 0.883 | 0.023 | 0.026 | - | 4.32 | 0.00 | - | 0 | yes |
| path-16384 | wcc | `neo4j-graph` |  |  | - | 0.783 | 0.001 | 0.001 | - | 1.51 | - | - | 0 | yes |
| path-16384 | wcc | `icebug` |  |  | - | 0.360 | 0.001 | 0.003 | - | 1.83 | - | - | 0 | yes |
| path-16384 | wcc | `icecat` |  |  | - | 0.297 | 0.004 | 0.014 | - | 0.91 | - | - | 0 | yes |
| path-16384 | wcc | `grustcat` |  |  | - | 0.159 | 0.001 | 0.005 | - | 27.46 | - | - | 0 | yes |
| path-16384 | wcc | `grust#1` | first | counted | - | 0.451 | 0.001 | 0.003 | - | 5.27 | - | 229369 | 0 | yes |
| path-16384 | wcc | `grust#1` | second | counted | - | 0.470 | 0.004 | 0.009 | - | 5.27 | - | 229369 | 0 | yes |
| path-16384 | wcc | `grust#unset` | first | counted | - | 0.992 | 0.000 | 0.000 | - | 5.18 | - | 294903 | 0 | yes |
| path-16384 | wcc | `grust#unset` | second | counted | - | 0.997 | 0.010 | 0.010 | - | 5.18 | - | 294903 | 0 | yes |
| path-16384 | wcc | `grust-next@counted#1` | first | counted | - | 0.536 | 0.001 | 0.002 | - | 5.98 | 0.63 | 327671 | 0 | yes |
| path-16384 | wcc | `grust-next@counted#1` | second | counted | - | 0.433 | 0.002 | 0.005 | - | 5.98 | 0.63 | 327671 | 0 | yes |
| path-16384 | wcc | `grust-next@work-uncounted#1` | first | work-uncounted | - | 0.320 | 0.002 | 0.005 | - | 4.42 | 0.29 | - | 0 | yes |
| path-16384 | wcc | `grust-next@work-uncounted#1` | second | work-uncounted | - | 0.316 | 0.000 | 0.000 | - | 4.42 | 0.29 | - | 0 | yes |
| path-16384 | wcc | `grust-next@unchecked#1` | first | unchecked | - | 0.308 | 0.001 | 0.003 | - | 4.39 | 0.28 | - | 0 | yes |
| path-16384 | wcc | `grust-next@unchecked#1` | second | unchecked | - | 0.304 | 0.001 | 0.004 | - | 4.39 | 0.28 | - | 0 | yes |
| path-16384 | wcc | `grust-next@counted#unset` | first | counted | - | 1.175 | 0.001 | 0.000 | - | 6.01 | 0.63 | 393205 | 0 | yes |
| path-16384 | wcc | `grust-next@counted#unset` | second | counted | - | 1.057 | 0.021 | 0.019 | - | 6.01 | 0.63 | 393205 | 0 | yes |
| path-16384 | wcc | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 0.507 | 0.004 | 0.008 | - | 4.42 | 0.29 | - | 0 | yes |
| path-16384 | wcc | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 0.530 | 0.027 | 0.051 | - | 4.42 | 0.29 | - | 0 | yes |
| path-16384 | wcc | `grust-next@unchecked#unset` | first | unchecked | - | 0.470 | 0.003 | 0.006 | - | 4.40 | 0.28 | - | 0 | yes |
| path-16384 | wcc | `grust-next@unchecked#unset` | second | unchecked | - | 0.467 | 0.005 | 0.010 | - | 4.40 | 0.28 | - | 0 | yes |
| path-65536 | bfs | `icebug` |  |  | - | 1.094 | 0.021 | 0.019 | - | 7.18 | - | - | 0 | yes |
| path-65536 | bfs | `icecat` |  |  | - | 1.050 | 0.015 | 0.014 | - | 4.49 | - | - | 0 | yes |
| path-65536 | bfs | `grustcat` |  |  | - | 0.573 | 0.003 | 0.006 | - | 115.58 | - | - | 0 | yes |
| path-65536 | bfs | `grust#1` | first | counted | - | 1.697 | 0.016 | 0.009 | - | 23.98 | - | 983035 | 0 | yes |
| path-65536 | bfs | `grust#1` | second | counted | - | 1.368 | 0.005 | 0.003 | - | 23.98 | - | 983035 | 0 | yes |
| path-65536 | bfs | `grust#unset` | first | counted | - | 1.703 | 0.010 | 0.006 | - | 24.19 | - | 983035 | 0 | yes |
| path-65536 | bfs | `grust#unset` | second | counted | - | 1.365 | 0.006 | 0.005 | - | 24.19 | - | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@counted#1` | first | counted | - | 1.832 | 0.005 | 0.003 | - | 26.99 | 2.53 | 1376249 | 0 | yes |
| path-65536 | bfs | `grust-next@counted#1` | second | counted | - | 1.304 | 0.010 | 0.008 | - | 26.99 | 2.53 | 1376249 | 0 | yes |
| path-65536 | bfs | `grust-next@work-uncounted#1` | first | work-uncounted | - | 1.011 | 0.011 | 0.011 | - | 21.23 | 1.16 | - | 0 | yes |
| path-65536 | bfs | `grust-next@work-uncounted#1` | second | work-uncounted | - | 0.484 | 0.031 | 0.064 | - | 21.23 | 1.16 | - | 0 | yes |
| path-65536 | bfs | `grust-next@unchecked#1` | first | unchecked | - | 0.960 | 0.003 | 0.003 | - | 21.10 | 1.11 | - | 0 | yes |
| path-65536 | bfs | `grust-next@unchecked#1` | second | unchecked | - | 0.425 | 0.004 | 0.008 | - | 21.10 | 1.11 | - | 0 | yes |
| path-65536 | bfs | `grust-next@counted#unset` | first | counted | - | 1.846 | 0.010 | 0.005 | - | 26.26 | 2.53 | 1376249 | 0 | yes |
| path-65536 | bfs | `grust-next@counted#unset` | second | counted | - | 1.293 | 0.002 | 0.002 | - | 26.26 | 2.53 | 1376249 | 0 | yes |
| path-65536 | bfs | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 1.002 | 0.005 | 0.005 | - | 20.56 | 1.18 | - | 0 | yes |
| path-65536 | bfs | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 0.456 | 0.001 | 0.002 | - | 20.56 | 1.18 | - | 0 | yes |
| path-65536 | bfs | `grust-next@unchecked#unset` | first | unchecked | - | 0.973 | 0.006 | 0.006 | - | 20.05 | 1.11 | - | 0 | yes |
| path-65536 | bfs | `grust-next@unchecked#unset` | second | unchecked | - | 0.425 | 0.003 | 0.007 | - | 20.05 | 1.11 | - | 0 | yes |
| path-65536 | pagerank | `icebug` |  |  | 46 | 44.089 | 0.085 | 0.002 | 0.958 | 7.15 | - | - | 0 | yes |
| path-65536 | pagerank | `icecat` |  |  | 50 | 34.272 | 0.062 | 0.002 | 0.685 | 4.47 | - | - | 0 | yes |
| path-65536 | pagerank | `grustcat` |  |  | 50 | 33.644 | 0.019 | 0.001 | 0.673 | 115.75 | - | - | 0 | yes |
| path-65536 | pagerank | `grust#1` | first | counted | 50 | 54.158 | 0.086 | 0.002 | 1.083 | 23.43 | - | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust#1` | second | counted | 50 | 50.940 | 0.105 | 0.002 | 1.019 | 23.43 | - | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust#unset` | first | counted | 50 | 232.658 | 0.399 | 0.002 | 4.653 | 23.83 | - | 17629127 | 0 | yes |
| path-65536 | pagerank | `grust#unset` | second | counted | 50 | 231.691 | 0.491 | 0.002 | 4.634 | 23.83 | - | 17629127 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted#1` | first | counted | 50 | 48.481 | 0.028 | 0.001 | 0.970 | 26.95 | 2.53 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted#1` | second | counted | 50 | 47.850 | 0.005 | 0.000 | 0.957 | 26.95 | 2.53 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 50 | 37.253 | 0.027 | 0.001 | 0.745 | 20.76 | 1.18 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 50 | 36.751 | 0.069 | 0.002 | 0.735 | 20.76 | 1.18 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@unchecked#1` | first | unchecked | 50 | 35.439 | 0.041 | 0.001 | 0.709 | 19.73 | 1.11 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@unchecked#1` | second | unchecked | 50 | 34.845 | 0.057 | 0.002 | 0.697 | 19.73 | 1.11 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@counted#unset` | first | counted | 50 | 204.872 | 0.032 | 0.000 | 4.097 | 25.74 | 2.54 | 18022341 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted#unset` | second | counted | 50 | 203.827 | 0.139 | 0.001 | 4.077 | 25.74 | 2.54 | 18022341 | 0 | yes |
| path-65536 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 50 | 103.232 | 0.120 | 0.001 | 2.065 | 21.20 | 1.18 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 50 | 102.685 | 0.093 | 0.001 | 2.054 | 21.20 | 1.18 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 50 | 92.019 | 0.222 | 0.002 | 1.840 | 20.06 | 1.10 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 50 | 91.148 | 0.253 | 0.003 | 1.823 | 20.06 | 1.10 | - | 0 | yes |
| path-65536 | triangles | `neo4j-graph` |  |  | - | 0.769 | 0.020 | 0.026 | - | 5.42 | - | - | 0 | yes |
| path-65536 | triangles | `grust#1` | first | counted | - | 6.245 | 0.010 | 0.002 | - | 24.86 | - | 1703922 | 0 | yes |
| path-65536 | triangles | `grust#1` | second | counted | - | 4.445 | 0.040 | 0.009 | - | 24.86 | - | 1703922 | 0 | yes |
| path-65536 | triangles | `grust#unset` | first | counted | - | 6.258 | 0.065 | 0.010 | - | 25.44 | - | 1703922 | 0 | yes |
| path-65536 | triangles | `grust#unset` | second | counted | - | 4.410 | 0.021 | 0.005 | - | 25.44 | - | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted#1` | first | counted | - | 6.273 | 0.030 | 0.005 | - | 25.86 | 0.00 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted#1` | second | counted | - | 4.484 | 0.007 | 0.002 | - | 25.86 | 0.00 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@work-uncounted#1` | first | work-uncounted | - | 5.513 | 0.050 | 0.009 | - | 20.59 | 0.00 | - | 0 | yes |
| path-65536 | triangles | `grust-next@work-uncounted#1` | second | work-uncounted | - | 3.674 | 0.010 | 0.003 | - | 20.59 | 0.00 | - | 0 | yes |
| path-65536 | triangles | `grust-next@unchecked#1` | first | unchecked | - | 5.344 | 0.020 | 0.004 | - | 19.89 | 0.00 | - | 0 | yes |
| path-65536 | triangles | `grust-next@unchecked#1` | second | unchecked | - | 3.480 | 0.012 | 0.003 | - | 19.89 | 0.00 | - | 0 | yes |
| path-65536 | triangles | `grust-next@counted#unset` | first | counted | - | 6.302 | 0.072 | 0.011 | - | 25.55 | 0.00 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted#unset` | second | counted | - | 4.445 | 0.018 | 0.004 | - | 25.55 | 0.00 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 5.490 | 0.032 | 0.006 | - | 20.13 | 0.00 | - | 0 | yes |
| path-65536 | triangles | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 3.680 | 0.012 | 0.003 | - | 20.13 | 0.00 | - | 0 | yes |
| path-65536 | triangles | `grust-next@unchecked#unset` | first | unchecked | - | 5.285 | 0.014 | 0.003 | - | 20.19 | 0.00 | - | 0 | yes |
| path-65536 | triangles | `grust-next@unchecked#unset` | second | unchecked | - | 3.461 | 0.011 | 0.003 | - | 20.19 | 0.00 | - | 0 | yes |
| path-65536 | wcc | `neo4j-graph` |  |  | - | 2.620 | 0.009 | 0.003 | - | 5.42 | - | - | 0 | yes |
| path-65536 | wcc | `icebug` |  |  | - | 1.320 | 0.008 | 0.006 | - | 7.16 | - | - | 0 | yes |
| path-65536 | wcc | `icecat` |  |  | - | 1.248 | 0.013 | 0.010 | - | 4.47 | - | - | 0 | yes |
| path-65536 | wcc | `grustcat` |  |  | - | 0.656 | 0.001 | 0.002 | - | 115.68 | - | - | 0 | yes |
| path-65536 | wcc | `grust#1` | first | counted | - | 1.842 | 0.025 | 0.014 | - | 24.07 | - | 917497 | 0 | yes |
| path-65536 | wcc | `grust#1` | second | counted | - | 1.855 | 0.006 | 0.003 | - | 24.07 | - | 917497 | 0 | yes |
| path-65536 | wcc | `grust#unset` | first | counted | - | 4.007 | 0.001 | 0.000 | - | 24.05 | - | 1179639 | 0 | yes |
| path-65536 | wcc | `grust#unset` | second | counted | - | 4.021 | 0.002 | 0.001 | - | 24.05 | - | 1179639 | 0 | yes |
| path-65536 | wcc | `grust-next@counted#1` | first | counted | - | 2.176 | 0.004 | 0.002 | - | 26.35 | 2.53 | 1310711 | 0 | yes |
| path-65536 | wcc | `grust-next@counted#1` | second | counted | - | 1.550 | 0.004 | 0.003 | - | 26.35 | 2.53 | 1310711 | 0 | yes |
| path-65536 | wcc | `grust-next@work-uncounted#1` | first | work-uncounted | - | 1.283 | 0.003 | 0.002 | - | 20.33 | 1.20 | - | 0 | yes |
| path-65536 | wcc | `grust-next@work-uncounted#1` | second | work-uncounted | - | 1.286 | 0.019 | 0.015 | - | 20.33 | 1.20 | - | 0 | yes |
| path-65536 | wcc | `grust-next@unchecked#1` | first | unchecked | - | 1.234 | 0.004 | 0.003 | - | 19.81 | 1.12 | - | 0 | yes |
| path-65536 | wcc | `grust-next@unchecked#1` | second | unchecked | - | 1.229 | 0.007 | 0.005 | - | 19.81 | 1.12 | - | 0 | yes |
| path-65536 | wcc | `grust-next@counted#unset` | first | counted | - | 4.762 | 0.047 | 0.010 | - | 26.68 | 2.55 | 1572853 | 0 | yes |
| path-65536 | wcc | `grust-next@counted#unset` | second | counted | - | 4.236 | 0.016 | 0.004 | - | 26.68 | 2.55 | 1572853 | 0 | yes |
| path-65536 | wcc | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 2.050 | 0.015 | 0.007 | - | 21.19 | 1.18 | - | 0 | yes |
| path-65536 | wcc | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 2.074 | 0.015 | 0.007 | - | 21.19 | 1.18 | - | 0 | yes |
| path-65536 | wcc | `grust-next@unchecked#unset` | first | unchecked | - | 1.894 | 0.019 | 0.010 | - | 19.38 | 1.11 | - | 0 | yes |
| path-65536 | wcc | `grust-next@unchecked#unset` | second | unchecked | - | 1.909 | 0.008 | 0.004 | - | 19.38 | 1.11 | - | 0 | yes |
| uniform-16384 | bfs | `icebug` |  |  | - | 2.122 | 0.034 | 0.016 | - | 10.63 | - | - | 0 | yes |
| uniform-16384 | bfs | `icecat` |  |  | - | 0.871 | 0.015 | 0.017 | - | 7.61 | - | - | 0 | yes |
| uniform-16384 | bfs | `grustcat` |  |  | - | 0.867 | 0.011 | 0.013 | - | 95.77 | - | - | 0 | yes |
| uniform-16384 | bfs | `grust#1` | first | counted | - | 1.764 | 0.053 | 0.030 | - | 19.27 | - | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust#1` | second | counted | - | 1.485 | 0.008 | 0.005 | - | 19.27 | - | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust#unset` | first | counted | - | 1.665 | 0.036 | 0.021 | - | 19.25 | - | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust#unset` | second | counted | - | 1.472 | 0.008 | 0.005 | - | 19.25 | - | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted#1` | first | counted | - | 1.694 | 0.024 | 0.014 | - | 23.47 | 1.83 | 1490619 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted#1` | second | counted | - | 1.475 | 0.010 | 0.006 | - | 23.47 | 1.83 | 1490619 | 0 | yes |
| uniform-16384 | bfs | `grust-next@work-uncounted#1` | first | work-uncounted | - | 1.117 | 0.013 | 0.012 | - | 15.31 | 1.39 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@work-uncounted#1` | second | work-uncounted | - | 0.920 | 0.009 | 0.010 | - | 15.31 | 1.39 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@unchecked#1` | first | unchecked | - | 1.023 | 0.016 | 0.016 | - | 14.72 | 1.35 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@unchecked#1` | second | unchecked | - | 0.815 | 0.008 | 0.010 | - | 14.72 | 1.35 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted#unset` | first | counted | - | 1.678 | 0.016 | 0.010 | - | 22.70 | 1.85 | 1490619 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted#unset` | second | counted | - | 1.480 | 0.012 | 0.008 | - | 22.70 | 1.85 | 1490619 | 0 | yes |
| uniform-16384 | bfs | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 1.155 | 0.007 | 0.006 | - | 15.22 | 1.37 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 0.915 | 0.012 | 0.013 | - | 15.22 | 1.37 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@unchecked#unset` | first | unchecked | - | 1.020 | 0.015 | 0.014 | - | 14.55 | 1.36 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@unchecked#unset` | second | unchecked | - | 0.825 | 0.009 | 0.011 | - | 14.55 | 1.36 | - | 0 | yes |
| uniform-16384 | pagerank | `neo4j-graph` |  |  | 28 | 11.099 | 0.017 | 0.002 | 0.396 | 8.24 | - | - | 0 | yes |
| uniform-16384 | pagerank | `icebug` |  |  | 12 | 8.178 | 0.199 | 0.024 | 0.682 | 10.34 | - | - | 0 | yes |
| uniform-16384 | pagerank | `icecat` |  |  | 16 | 7.231 | 0.045 | 0.006 | 0.452 | 7.40 | - | - | 0 | yes |
| uniform-16384 | pagerank | `grustcat` |  |  | 16 | 6.841 | 0.035 | 0.005 | 0.428 | 93.09 | - | - | 0 | yes |
| uniform-16384 | pagerank | `grust#1` | first | counted | 16 | 11.194 | 0.022 | 0.002 | 0.700 | 21.71 | - | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust#1` | second | counted | 16 | 9.119 | 0.010 | 0.001 | 0.570 | 21.71 | - | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust#unset` | first | counted | 16 | 48.271 | 0.116 | 0.002 | 3.017 | 22.18 | - | 4373785 | 0 | yes |
| uniform-16384 | pagerank | `grust#unset` | second | counted | 16 | 47.910 | 0.009 | 0.000 | 2.994 | 22.18 | - | 4373785 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted#1` | first | counted | 16 | 8.425 | 0.010 | 0.001 | 0.527 | 24.43 | 1.82 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted#1` | second | counted | 16 | 8.297 | 0.011 | 0.001 | 0.519 | 24.43 | 1.82 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 16 | 7.856 | 0.023 | 0.003 | 0.491 | 15.04 | 1.36 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 16 | 7.734 | 0.006 | 0.001 | 0.483 | 15.04 | 1.36 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@unchecked#1` | first | unchecked | 16 | 7.327 | 0.046 | 0.006 | 0.458 | 14.57 | 1.42 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@unchecked#1` | second | unchecked | 16 | 7.311 | 0.015 | 0.002 | 0.457 | 14.57 | 1.42 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted#unset` | first | counted | 16 | 21.470 | 0.075 | 0.004 | 1.342 | 23.35 | 1.82 | 4816061 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted#unset` | second | counted | 16 | 21.130 | 0.015 | 0.001 | 1.321 | 23.35 | 1.82 | 4816061 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 16 | 13.433 | 0.013 | 0.001 | 0.840 | 14.38 | 1.36 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 16 | 13.212 | 0.003 | 0.000 | 0.826 | 14.38 | 1.36 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 16 | 12.555 | 0.009 | 0.001 | 0.785 | 14.85 | 1.37 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 16 | 12.384 | 0.015 | 0.001 | 0.774 | 14.85 | 1.37 | - | 0 | yes |
| uniform-16384 | triangles | `neo4j-graph` |  |  | - | 9.504 | 0.057 | 0.006 | - | 8.21 | - | - | 0 | yes |
| uniform-16384 | triangles | `grust#1` | first | counted | - | 19.438 | 0.059 | 0.003 | - | 23.96 | - | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust#1` | second | counted | - | 17.297 | 0.050 | 0.003 | - | 23.96 | - | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust#unset` | first | counted | - | 19.244 | 0.094 | 0.005 | - | 24.93 | - | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust#unset` | second | counted | - | 17.203 | 0.086 | 0.005 | - | 24.93 | - | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted#1` | first | counted | - | 17.837 | 0.067 | 0.004 | - | 25.22 | 0.00 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted#1` | second | counted | - | 15.795 | 0.030 | 0.002 | - | 25.22 | 0.00 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@work-uncounted#1` | first | work-uncounted | - | 17.677 | 0.128 | 0.007 | - | 16.03 | 0.00 | - | 0 | yes |
| uniform-16384 | triangles | `grust-next@work-uncounted#1` | second | work-uncounted | - | 15.712 | 0.088 | 0.006 | - | 16.03 | 0.00 | - | 0 | yes |
| uniform-16384 | triangles | `grust-next@unchecked#1` | first | unchecked | - | 17.636 | 0.060 | 0.003 | - | 16.00 | 0.00 | - | 0 | yes |
| uniform-16384 | triangles | `grust-next@unchecked#1` | second | unchecked | - | 15.495 | 0.088 | 0.006 | - | 16.00 | 0.00 | - | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted#unset` | first | counted | - | 17.888 | 0.072 | 0.004 | - | 24.96 | 0.00 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted#unset` | second | counted | - | 15.864 | 0.065 | 0.004 | - | 24.96 | 0.00 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 17.536 | 0.063 | 0.004 | - | 17.50 | 0.00 | - | 0 | yes |
| uniform-16384 | triangles | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 15.681 | 0.037 | 0.002 | - | 17.50 | 0.00 | - | 0 | yes |
| uniform-16384 | triangles | `grust-next@unchecked#unset` | first | unchecked | - | 17.671 | 0.045 | 0.003 | - | 16.34 | 0.00 | - | 0 | yes |
| uniform-16384 | triangles | `grust-next@unchecked#unset` | second | unchecked | - | 15.527 | 0.040 | 0.003 | - | 16.34 | 0.00 | - | 0 | yes |
| uniform-16384 | wcc | `neo4j-graph` |  |  | - | 1.043 | 0.013 | 0.012 | - | 8.07 | - | - | 0 | yes |
| uniform-16384 | wcc | `icebug` |  |  | - | 2.935 | 0.176 | 0.060 | - | 10.22 | - | - | 0 | yes |
| uniform-16384 | wcc | `icecat` |  |  | - | 1.107 | 0.001 | 0.001 | - | 7.05 | - | - | 0 | yes |
| uniform-16384 | wcc | `grustcat` |  |  | - | 0.734 | 0.005 | 0.007 | - | 92.31 | - | - | 0 | yes |
| uniform-16384 | wcc | `grust#1` | first | counted | - | 2.070 | 0.016 | 0.008 | - | 20.02 | - | 1031975 | 0 | yes |
| uniform-16384 | wcc | `grust#1` | second | counted | - | 2.304 | 0.010 | 0.005 | - | 20.02 | - | 1031975 | 0 | yes |
| uniform-16384 | wcc | `grust#unset` | first | counted | - | 4.166 | 0.007 | 0.002 | - | 21.37 | - | 1324427 | 0 | yes |
| uniform-16384 | wcc | `grust#unset` | second | counted | - | 4.172 | 0.014 | 0.003 | - | 21.37 | - | 1324427 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted#1` | first | counted | - | 2.461 | 0.018 | 0.007 | - | 22.46 | 1.81 | 1474251 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted#1` | second | counted | - | 2.309 | 0.009 | 0.004 | - | 22.46 | 1.81 | 1474251 | 0 | yes |
| uniform-16384 | wcc | `grust-next@work-uncounted#1` | first | work-uncounted | - | 2.023 | 0.013 | 0.007 | - | 15.32 | 1.39 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@work-uncounted#1` | second | work-uncounted | - | 1.977 | 0.008 | 0.004 | - | 15.32 | 1.39 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@unchecked#1` | first | unchecked | - | 1.928 | 0.020 | 0.010 | - | 14.73 | 1.37 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@unchecked#1` | second | unchecked | - | 1.933 | 0.033 | 0.017 | - | 14.73 | 1.37 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted#unset` | first | counted | - | 4.719 | 0.012 | 0.003 | - | 23.51 | 1.81 | 1766703 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted#unset` | second | counted | - | 4.581 | 0.023 | 0.005 | - | 23.51 | 1.81 | 1766703 | 0 | yes |
| uniform-16384 | wcc | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 2.139 | 0.013 | 0.006 | - | 15.83 | 1.41 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 2.158 | 0.034 | 0.016 | - | 15.83 | 1.41 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@unchecked#unset` | first | unchecked | - | 2.071 | 0.007 | 0.003 | - | 15.09 | 1.39 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@unchecked#unset` | second | unchecked | - | 2.082 | 0.028 | 0.013 | - | 15.09 | 1.39 | - | 0 | yes |
| uniform-65536 | bfs | `icebug` |  |  | - | 15.146 | 0.678 | 0.045 | - | 65.82 | - | - | 0 | yes |
| uniform-65536 | bfs | `icecat` |  |  | - | 5.496 | 0.492 | 0.090 | - | 21.70 | - | - | 0 | yes |
| uniform-65536 | bfs | `grustcat` |  |  | - | 5.883 | 0.187 | 0.032 | - | 481.73 | - | - | 0 | yes |
| uniform-65536 | bfs | `grust#1` | first | counted | - | 8.474 | 0.461 | 0.054 | - | 110.26 | - | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust#1` | second | counted | - | 6.600 | 0.530 | 0.080 | - | 110.26 | - | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust#unset` | first | counted | - | 9.543 | 0.319 | 0.033 | - | 108.64 | - | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust#unset` | second | counted | - | 7.880 | 0.379 | 0.048 | - | 108.64 | - | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted#1` | first | counted | - | 8.437 | 0.487 | 0.058 | - | 126.52 | 8.70 | 5963146 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted#1` | second | counted | - | 6.391 | 0.468 | 0.073 | - | 126.52 | 8.70 | 5963146 | 0 | yes |
| uniform-65536 | bfs | `grust-next@work-uncounted#1` | first | work-uncounted | - | 8.229 | 0.121 | 0.015 | - | 74.17 | 6.78 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@work-uncounted#1` | second | work-uncounted | - | 6.018 | 0.248 | 0.041 | - | 74.17 | 6.78 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@unchecked#1` | first | unchecked | - | 8.934 | 0.418 | 0.047 | - | 70.06 | 6.72 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@unchecked#1` | second | unchecked | - | 6.678 | 0.506 | 0.076 | - | 70.06 | 6.72 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted#unset` | first | counted | - | 10.630 | 0.072 | 0.007 | - | 129.16 | 8.21 | 5963146 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted#unset` | second | counted | - | 8.051 | 0.436 | 0.054 | - | 129.16 | 8.21 | 5963146 | 0 | yes |
| uniform-65536 | bfs | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 8.935 | 1.517 | 0.170 | - | 73.18 | 6.99 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 6.534 | 0.758 | 0.116 | - | 73.18 | 6.99 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@unchecked#unset` | first | unchecked | - | 8.915 | 0.191 | 0.021 | - | 71.81 | 6.78 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@unchecked#unset` | second | unchecked | - | 5.618 | 0.114 | 0.020 | - | 71.81 | 6.78 | - | 0 | yes |
| uniform-65536 | pagerank | `neo4j-graph` |  |  | 34 | 48.491 | 0.198 | 0.004 | 1.426 | 47.62 | - | - | 1 | yes |
| uniform-65536 | pagerank | `icebug` |  |  | 11 | 69.770 | 0.566 | 0.008 | 6.343 | 65.97 | - | - | 1 | yes |
| uniform-65536 | pagerank | `icecat` |  |  | 16 | 30.237 | 0.193 | 0.006 | 1.890 | 21.65 | - | - | 1 | yes |
| uniform-65536 | pagerank | `grustcat` |  |  | 16 | 31.242 | 0.347 | 0.011 | 1.953 | 479.62 | - | - | 1 | yes |
| uniform-65536 | pagerank | `grust#1` | first | counted | 16 | 59.440 | 2.995 | 0.050 | 3.715 | 107.15 | - | 16907315 | 1 | yes |
| uniform-65536 | pagerank | `grust#1` | second | counted | 16 | 49.383 | 4.139 | 0.084 | 3.086 | 107.15 | - | 16907315 | 1 | yes |
| uniform-65536 | pagerank | `grust#unset` | first | counted | 16 | 196.003 | 0.706 | 0.004 | 12.250 | 107.37 | - | 17497177 | 1 | yes |
| uniform-65536 | pagerank | `grust#unset` | second | counted | 16 | 195.330 | 0.757 | 0.004 | 12.208 | 107.37 | - | 17497177 | 1 | yes |
| uniform-65536 | pagerank | `grust-next@counted#1` | first | counted | 16 | 35.020 | 0.100 | 0.003 | 2.189 | 118.87 | 8.77 | 16907315 | 1 | yes |
| uniform-65536 | pagerank | `grust-next@counted#1` | second | counted | 16 | 34.050 | 0.064 | 0.002 | 2.128 | 118.87 | 8.77 | 16907315 | 1 | yes |
| uniform-65536 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 16 | 32.530 | 0.085 | 0.003 | 2.033 | 71.08 | 6.38 | - | 1 | yes |
| uniform-65536 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 16 | 31.857 | 0.017 | 0.001 | 1.991 | 71.08 | 6.38 | - | 1 | yes |
| uniform-65536 | pagerank | `grust-next@unchecked#1` | first | unchecked | 16 | 30.890 | 0.163 | 0.005 | 1.931 | 69.97 | 6.60 | - | 1 | yes |
| uniform-65536 | pagerank | `grust-next@unchecked#1` | second | unchecked | 16 | 30.803 | 0.396 | 0.013 | 1.925 | 69.97 | 6.60 | - | 1 | yes |
| uniform-65536 | pagerank | `grust-next@counted#unset` | first | counted | 16 | 88.772 | 0.659 | 0.007 | 5.548 | 129.26 | 8.82 | 19266533 | 1 | yes |
| uniform-65536 | pagerank | `grust-next@counted#unset` | second | counted | 16 | 88.790 | 0.906 | 0.010 | 5.549 | 129.26 | 8.82 | 19266533 | 1 | yes |
| uniform-65536 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 16 | 57.111 | 0.444 | 0.008 | 3.569 | 70.93 | 6.66 | - | 1 | yes |
| uniform-65536 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 16 | 57.350 | 0.911 | 0.016 | 3.584 | 70.93 | 6.66 | - | 1 | yes |
| uniform-65536 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 16 | 53.626 | 0.391 | 0.007 | 3.352 | 71.44 | 7.02 | - | 1 | yes |
| uniform-65536 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 16 | 52.932 | 0.697 | 0.013 | 3.308 | 71.44 | 7.02 | - | 1 | yes |
| uniform-65536 | triangles | `neo4j-graph` |  |  | - | 46.936 | 1.053 | 0.022 | - | 49.73 | - | - | 0 | yes |
| uniform-65536 | triangles | `grust#1` | first | counted | - | 87.413 | 0.795 | 0.009 | - | 137.97 | - | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust#1` | second | counted | - | 84.774 | 2.379 | 0.028 | - | 137.97 | - | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust#unset` | first | counted | - | 90.428 | 1.395 | 0.015 | - | 138.95 | - | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust#unset` | second | counted | - | 85.540 | 1.607 | 0.019 | - | 138.95 | - | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted#1` | first | counted | - | 80.430 | 0.609 | 0.008 | - | 143.88 | 0.00 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted#1` | second | counted | - | 76.819 | 0.901 | 0.012 | - | 143.88 | 0.00 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@work-uncounted#1` | first | work-uncounted | - | 80.843 | 0.952 | 0.012 | - | 83.93 | 0.00 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@work-uncounted#1` | second | work-uncounted | - | 77.277 | 1.041 | 0.013 | - | 83.93 | 0.00 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@unchecked#1` | first | unchecked | - | 81.735 | 0.382 | 0.005 | - | 80.70 | 0.00 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@unchecked#1` | second | unchecked | - | 76.488 | 0.932 | 0.012 | - | 80.70 | 0.00 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted#unset` | first | counted | - | 83.229 | 1.014 | 0.012 | - | 140.72 | 0.00 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted#unset` | second | counted | - | 77.115 | 1.725 | 0.022 | - | 140.72 | 0.00 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 81.655 | 1.925 | 0.024 | - | 82.77 | 0.00 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 77.138 | 0.985 | 0.013 | - | 82.77 | 0.00 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@unchecked#unset` | first | unchecked | - | 81.048 | 0.308 | 0.004 | - | 82.32 | 0.00 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@unchecked#unset` | second | unchecked | - | 76.150 | 0.578 | 0.008 | - | 82.32 | 0.00 | - | 0 | yes |
| uniform-65536 | wcc | `neo4j-graph` |  |  | - | 3.865 | 0.007 | 0.002 | - | 52.61 | - | - | 0 | yes |
| uniform-65536 | wcc | `icebug` |  |  | - | 24.759 | 1.286 | 0.052 | - | 64.36 | - | - | 0 | yes |
| uniform-65536 | wcc | `icecat` |  |  | - | 4.506 | 0.013 | 0.003 | - | 21.57 | - | - | 0 | yes |
| uniform-65536 | wcc | `grustcat` |  |  | - | 3.015 | 0.032 | 0.011 | - | 485.76 | - | - | 0 | yes |
| uniform-65536 | wcc | `grust#1` | first | counted | - | 9.450 | 0.022 | 0.002 | - | 102.68 | - | 4128495 | 0 | yes |
| uniform-65536 | wcc | `grust#1` | second | counted | - | 9.779 | 0.012 | 0.001 | - | 102.68 | - | 4128495 | 0 | yes |
| uniform-65536 | wcc | `grust#unset` | first | counted | - | 17.417 | 0.030 | 0.002 | - | 108.96 | - | 5298822 | 0 | yes |
| uniform-65536 | wcc | `grust#unset` | second | counted | - | 17.588 | 0.039 | 0.002 | - | 108.96 | - | 5298822 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted#1` | first | counted | - | 10.700 | 0.101 | 0.009 | - | 124.99 | 8.68 | 5897851 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted#1` | second | counted | - | 10.040 | 0.035 | 0.004 | - | 124.99 | 8.68 | 5897851 | 0 | yes |
| uniform-65536 | wcc | `grust-next@work-uncounted#1` | first | work-uncounted | - | 8.745 | 0.023 | 0.003 | - | 68.36 | 6.25 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@work-uncounted#1` | second | work-uncounted | - | 8.836 | 0.009 | 0.001 | - | 68.36 | 6.25 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@unchecked#1` | first | unchecked | - | 8.444 | 0.019 | 0.002 | - | 72.96 | 6.70 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@unchecked#1` | second | unchecked | - | 8.475 | 0.016 | 0.002 | - | 72.96 | 6.70 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted#unset` | first | counted | - | 20.233 | 0.090 | 0.004 | - | 129.78 | 8.69 | 7068178 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted#unset` | second | counted | - | 19.829 | 0.065 | 0.003 | - | 129.78 | 8.69 | 7068178 | 0 | yes |
| uniform-65536 | wcc | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 11.132 | 0.082 | 0.007 | - | 73.37 | 6.49 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 11.308 | 0.215 | 0.019 | - | 73.37 | 6.49 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@unchecked#unset` | first | unchecked | - | 10.579 | 0.126 | 0.012 | - | 70.59 | 6.43 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@unchecked#unset` | second | unchecked | - | 10.449 | 0.048 | 0.005 | - | 70.59 | 6.43 | - | 0 | yes |

### `full-width.json`: full-width

workers 16, concurrency 16, 1 warmup + 5 repeats, steal over the run 0 ticks, 112.2 s, unusable at MAD/median >= 0.25

Not timed (no agreeing parity row): neo4j-graph pagerank layered-16384.edges, neo4j-graph pagerank layered-65536.edges, neo4j-graph pagerank path-16384.edges, neo4j-graph pagerank path-65536.edges 

| fixture | algorithm | participant | call | accounting | iters | total ms | MAD | MAD/median | per iter | build ms | incoming ms | work units | steal | usable |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| hub-16384 | bfs | `icebug` |  |  | - | 2.290 | 0.091 | 0.040 | - | 10.65 | - | - | 0 | yes |
| hub-16384 | bfs | `icecat` |  |  | - | 0.817 | 0.013 | 0.015 | - | 6.46 | - | - | 0 | yes |
| hub-16384 | bfs | `grustcat` |  |  | - | 0.704 | 0.061 | 0.087 | - | 95.51 | - | - | 0 | yes |
| hub-16384 | bfs | `grust` | first | counted | - | 1.618 | 0.049 | 0.030 | - | 19.40 | - | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust` | second | counted | - | 1.443 | 0.016 | 0.011 | - | 19.40 | - | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted` | first | counted | - | 1.628 | 0.014 | 0.008 | - | 22.82 | 1.82 | 1489517 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted` | second | counted | - | 1.451 | 0.002 | 0.002 | - | 22.82 | 1.82 | 1489517 | 0 | yes |
| hub-16384 | bfs | `grust-next@work-uncounted` | first | work-uncounted | - | 1.051 | 0.005 | 0.005 | - | 14.78 | 1.38 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@work-uncounted` | second | work-uncounted | - | 0.891 | 0.016 | 0.018 | - | 14.78 | 1.38 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@unchecked` | first | unchecked | - | 0.958 | 0.010 | 0.010 | - | 14.87 | 1.37 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@unchecked` | second | unchecked | - | 0.790 | 0.007 | 0.009 | - | 14.87 | 1.37 | - | 0 | yes |
| hub-16384 | pagerank | `neo4j-graph` |  |  | 36 | 14.341 | 0.040 | 0.003 | 0.398 | 4.71 | - | - | 0 | yes |
| hub-16384 | pagerank | `icebug` |  |  | 12 | 3.036 | 0.023 | 0.007 | 0.253 | 10.75 | - | - | 0 | yes |
| hub-16384 | pagerank | `icecat` |  |  | 17 | 7.774 | 0.049 | 0.006 | 0.457 | 6.59 | - | - | 0 | yes |
| hub-16384 | pagerank | `grustcat` |  |  | 17 | 7.295 | 0.002 | 0.000 | 0.429 | 97.16 | - | - | 0 | yes |
| hub-16384 | pagerank | `grust` | first | counted | 17 | 6.574 | 0.137 | 0.021 | 0.387 | 21.01 | - | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust` | second | counted | 17 | 3.489 | 0.066 | 0.019 | 0.205 | 21.01 | - | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted` | first | counted | 17 | 4.719 | 0.113 | 0.024 | 0.278 | 24.61 | 1.83 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted` | second | counted | 17 | 3.631 | 0.109 | 0.030 | 0.214 | 24.61 | 1.83 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 17 | 4.049 | 0.012 | 0.003 | 0.238 | 14.98 | 1.38 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 17 | 2.991 | 0.046 | 0.015 | 0.176 | 14.98 | 1.38 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@unchecked` | first | unchecked | 17 | 4.088 | 0.029 | 0.007 | 0.240 | 14.67 | 1.38 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@unchecked` | second | unchecked | 17 | 3.032 | 0.035 | 0.011 | 0.178 | 14.67 | 1.38 | - | 0 | yes |
| hub-16384 | triangles | `neo4j-graph` |  |  | - | 1.328 | 0.020 | 0.015 | - | 4.67 | - | - | 0 | yes |
| hub-16384 | triangles | `grust` | first | counted | - | 9.175 | 0.126 | 0.014 | - | 24.48 | - | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust` | second | counted | - | 6.397 | 0.058 | 0.009 | - | 24.48 | - | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted` | first | counted | - | 8.956 | 0.091 | 0.010 | - | 25.44 | 0.00 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted` | second | counted | - | 6.328 | 0.079 | 0.012 | - | 25.44 | 0.00 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@work-uncounted` | first | work-uncounted | - | 8.793 | 0.068 | 0.008 | - | 16.45 | 0.00 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@work-uncounted` | second | work-uncounted | - | 6.098 | 0.063 | 0.010 | - | 16.45 | 0.00 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@unchecked` | first | unchecked | - | 8.903 | 0.155 | 0.017 | - | 16.31 | 0.00 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@unchecked` | second | unchecked | - | 6.065 | 0.072 | 0.012 | - | 16.31 | 0.00 | - | 0 | yes |
| hub-16384 | wcc | `neo4j-graph` |  |  | - | 1.131 | 0.013 | 0.011 | - | 4.74 | - | - | 0 | yes |
| hub-16384 | wcc | `icebug` |  |  | - | 2.665 | 0.223 | 0.084 | - | 10.32 | - | - | 0 | yes |
| hub-16384 | wcc | `icecat` |  |  | - | 0.936 | 0.010 | 0.011 | - | 6.54 | - | - | 0 | yes |
| hub-16384 | wcc | `grustcat` |  |  | - | 0.583 | 0.002 | 0.003 | - | 93.00 | - | - | 0 | yes |
| hub-16384 | wcc | `grust` | first | counted | - | 1.281 | 0.013 | 0.010 | - | 20.17 | - | 1031219 | 0 | yes |
| hub-16384 | wcc | `grust` | second | counted | - | 0.618 | 0.037 | 0.060 | - | 20.17 | - | 1031219 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted` | first | counted | - | 1.376 | 0.022 | 0.016 | - | 23.06 | 1.81 | 1473149 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted` | second | counted | - | 0.553 | 0.031 | 0.056 | - | 23.06 | 1.81 | 1473149 | 0 | yes |
| hub-16384 | wcc | `grust-next@work-uncounted` | first | work-uncounted | - | 1.241 | 0.057 | 0.046 | - | 14.29 | 1.40 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@work-uncounted` | second | work-uncounted | - | 0.507 | 0.030 | 0.060 | - | 14.29 | 1.40 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@unchecked` | first | unchecked | - | 1.222 | 0.045 | 0.037 | - | 15.28 | 1.41 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@unchecked` | second | unchecked | - | 0.538 | 0.033 | 0.061 | - | 15.28 | 1.41 | - | 0 | yes |
| hub-65536 | bfs | `icebug` |  |  | - | 16.032 | 0.326 | 0.020 | - | 61.50 | - | - | 0 | yes |
| hub-65536 | bfs | `icecat` |  |  | - | 4.549 | 0.146 | 0.032 | - | 22.05 | - | - | 0 | yes |
| hub-65536 | bfs | `grustcat` |  |  | - | 5.202 | 0.067 | 0.013 | - | 461.21 | - | - | 0 | yes |
| hub-65536 | bfs | `grust` | first | counted | - | 4.563 | 0.186 | 0.041 | - | 106.08 | - | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust` | second | counted | - | 3.292 | 0.061 | 0.019 | - | 106.08 | - | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted` | first | counted | - | 4.359 | 0.060 | 0.014 | - | 127.10 | 8.35 | 5959069 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted` | second | counted | - | 3.280 | 0.034 | 0.010 | - | 127.10 | 8.35 | 5959069 | 0 | yes |
| hub-65536 | bfs | `grust-next@work-uncounted` | first | work-uncounted | - | 4.088 | 0.122 | 0.030 | - | 70.58 | 6.68 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@work-uncounted` | second | work-uncounted | - | 2.990 | 0.081 | 0.027 | - | 70.58 | 6.68 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@unchecked` | first | unchecked | - | 4.175 | 0.059 | 0.014 | - | 69.08 | 6.22 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@unchecked` | second | unchecked | - | 3.176 | 0.071 | 0.022 | - | 69.08 | 6.22 | - | 0 | yes |
| hub-65536 | pagerank | `neo4j-graph` |  |  | 29 | 15.422 | 0.729 | 0.047 | 0.532 | 15.36 | - | - | 0 | yes |
| hub-65536 | pagerank | `icebug` |  |  | 12 | 9.066 | 0.575 | 0.063 | 0.756 | 70.12 | - | - | 0 | yes |
| hub-65536 | pagerank | `icecat` |  |  | 17 | 31.594 | 0.067 | 0.002 | 1.858 | 22.72 | - | - | 0 | yes |
| hub-65536 | pagerank | `grustcat` |  |  | 17 | 33.986 | 0.705 | 0.021 | 1.999 | 485.31 | - | - | 0 | yes |
| hub-65536 | pagerank | `grust` | first | counted | 17 | 19.111 | 0.116 | 0.006 | 1.124 | 105.48 | - | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust` | second | counted | 17 | 8.647 | 0.216 | 0.025 | 0.509 | 105.48 | - | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted` | first | counted | 17 | 9.064 | 0.107 | 0.012 | 0.533 | 126.63 | 8.42 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted` | second | counted | 17 | 7.695 | 0.105 | 0.014 | 0.453 | 126.63 | 8.42 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 17 | 6.968 | 0.216 | 0.031 | 0.410 | 72.02 | 6.96 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 17 | 5.470 | 0.129 | 0.024 | 0.322 | 72.02 | 6.96 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@unchecked` | first | unchecked | 17 | 6.524 | 0.047 | 0.007 | 0.384 | 70.93 | 6.82 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@unchecked` | second | unchecked | 17 | 5.258 | 0.057 | 0.011 | 0.309 | 70.93 | 6.82 | - | 0 | yes |
| hub-65536 | triangles | `neo4j-graph` |  |  | - | 3.788 | 0.016 | 0.004 | - | 15.41 | - | - | 0 | yes |
| hub-65536 | triangles | `grust` | first | counted | - | 32.137 | 0.694 | 0.022 | - | 127.83 | - | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust` | second | counted | - | 25.991 | 0.059 | 0.002 | - | 127.83 | - | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted` | first | counted | - | 31.371 | 0.178 | 0.006 | - | 136.06 | 0.00 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted` | second | counted | - | 25.448 | 0.129 | 0.005 | - | 136.06 | 0.00 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@work-uncounted` | first | work-uncounted | - | 30.695 | 0.147 | 0.005 | - | 76.42 | 0.00 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@work-uncounted` | second | work-uncounted | - | 24.639 | 0.119 | 0.005 | - | 76.42 | 0.00 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@unchecked` | first | unchecked | - | 30.936 | 0.339 | 0.011 | - | 78.47 | 0.00 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@unchecked` | second | unchecked | - | 24.476 | 0.061 | 0.002 | - | 78.47 | 0.00 | - | 0 | yes |
| hub-65536 | wcc | `neo4j-graph` |  |  | - | 3.103 | 0.233 | 0.075 | - | 15.04 | - | - | 0 | yes |
| hub-65536 | wcc | `icebug` |  |  | - | 21.316 | 0.462 | 0.022 | - | 65.23 | - | - | 0 | yes |
| hub-65536 | wcc | `icecat` |  |  | - | 3.362 | 0.062 | 0.018 | - | 22.10 | - | - | 0 | yes |
| hub-65536 | wcc | `grustcat` |  |  | - | 2.387 | 0.019 | 0.008 | - | 466.97 | - | - | 0 | yes |
| hub-65536 | wcc | `grust` | first | counted | - | 2.481 | 0.041 | 0.017 | - | 103.98 | - | 4125489 | 0 | yes |
| hub-65536 | wcc | `grust` | second | counted | - | 1.755 | 0.037 | 0.021 | - | 103.98 | - | 4125489 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted` | first | counted | - | 2.845 | 0.074 | 0.026 | - | 121.67 | 8.40 | 5893548 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted` | second | counted | - | 1.609 | 0.071 | 0.044 | - | 121.67 | 8.40 | 5893548 | 0 | yes |
| hub-65536 | wcc | `grust-next@work-uncounted` | first | work-uncounted | - | 2.361 | 0.051 | 0.022 | - | 74.38 | 6.71 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@work-uncounted` | second | work-uncounted | - | 1.637 | 0.089 | 0.055 | - | 74.38 | 6.71 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@unchecked` | first | unchecked | - | 2.310 | 0.134 | 0.058 | - | 71.54 | 7.05 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@unchecked` | second | unchecked | - | 1.646 | 0.054 | 0.033 | - | 71.54 | 7.05 | - | 0 | yes |
| layered-16384 | bfs | `icebug` |  |  | - | 0.529 | 0.032 | 0.060 | - | 2.80 | - | - | 0 | yes |
| layered-16384 | bfs | `icecat` |  |  | - | 0.364 | 0.005 | 0.014 | - | 1.70 | - | - | 0 | yes |
| layered-16384 | bfs | `grustcat` |  |  | - | 0.257 | 0.004 | 0.017 | - | 33.53 | - | - | 0 | yes |
| layered-16384 | bfs | `grust` | first | counted | - | 0.470 | 0.007 | 0.014 | - | 7.04 | - | 347308 | 0 | yes |
| layered-16384 | bfs | `grust` | second | counted | - | 0.388 | 0.001 | 0.003 | - | 7.04 | - | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted` | first | counted | - | 0.511 | 0.001 | 0.002 | - | 7.98 | 0.74 | 493703 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted` | second | counted | - | 0.380 | 0.001 | 0.002 | - | 7.98 | 0.74 | 493703 | 0 | yes |
| layered-16384 | bfs | `grust-next@work-uncounted` | first | work-uncounted | - | 0.397 | 0.001 | 0.003 | - | 5.77 | 0.42 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@work-uncounted` | second | work-uncounted | - | 0.270 | 0.004 | 0.015 | - | 5.77 | 0.42 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@unchecked` | first | unchecked | - | 0.390 | 0.001 | 0.002 | - | 5.70 | 0.40 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@unchecked` | second | unchecked | - | 0.257 | 0.000 | 0.001 | - | 5.70 | 0.40 | - | 0 | yes |
| layered-16384 | pagerank | `icebug` |  |  | 69 | 9.008 | 0.103 | 0.011 | 0.131 | 2.82 | - | - | 0 | yes |
| layered-16384 | pagerank | `icecat` |  |  | 84 | 23.288 | 0.013 | 0.001 | 0.277 | 1.74 | - | - | 0 | yes |
| layered-16384 | pagerank | `grustcat` |  |  | 84 | 26.626 | 0.053 | 0.002 | 0.317 | 33.73 | - | - | 0 | yes |
| layered-16384 | pagerank | `grust` | first | counted | 84 | 15.514 | 0.153 | 0.010 | 0.185 | 7.01 | - | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust` | second | counted | 84 | 13.737 | 0.107 | 0.008 | 0.164 | 7.01 | - | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted` | first | counted | 84 | 15.790 | 0.053 | 0.003 | 0.188 | 7.91 | 0.73 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted` | second | counted | 84 | 14.509 | 0.200 | 0.014 | 0.173 | 7.91 | 0.73 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 84 | 13.749 | 0.071 | 0.005 | 0.164 | 5.74 | 0.41 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 84 | 12.548 | 0.077 | 0.006 | 0.149 | 5.74 | 0.41 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@unchecked` | first | unchecked | 84 | 13.745 | 0.041 | 0.003 | 0.164 | 5.68 | 0.40 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@unchecked` | second | unchecked | 84 | 12.570 | 0.072 | 0.006 | 0.150 | 5.68 | 0.40 | - | 0 | yes |
| layered-16384 | triangles | `neo4j-graph` |  |  | - | 0.732 | 0.015 | 0.021 | - | 2.29 | - | - | 0 | yes |
| layered-16384 | triangles | `grust` | first | counted | - | 3.112 | 0.032 | 0.010 | - | 7.48 | - | 718265 | 0 | yes |
| layered-16384 | triangles | `grust` | second | counted | - | 1.697 | 0.019 | 0.011 | - | 7.48 | - | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted` | first | counted | - | 3.132 | 0.020 | 0.006 | - | 7.53 | 0.00 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted` | second | counted | - | 1.744 | 0.027 | 0.015 | - | 7.53 | 0.00 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@work-uncounted` | first | work-uncounted | - | 2.977 | 0.026 | 0.009 | - | 5.60 | 0.00 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@work-uncounted` | second | work-uncounted | - | 1.542 | 0.016 | 0.010 | - | 5.60 | 0.00 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@unchecked` | first | unchecked | - | 2.993 | 0.021 | 0.007 | - | 5.71 | 0.00 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@unchecked` | second | unchecked | - | 1.517 | 0.024 | 0.016 | - | 5.71 | 0.00 | - | 0 | yes |
| layered-16384 | wcc | `neo4j-graph` |  |  | - | 1.066 | 0.008 | 0.007 | - | 2.30 | - | - | 0 | yes |
| layered-16384 | wcc | `icebug` |  |  | - | 1.006 | 0.035 | 0.035 | - | 2.81 | - | - | 0 | yes |
| layered-16384 | wcc | `icecat` |  |  | - | 0.516 | 0.002 | 0.004 | - | 1.79 | - | - | 0 | yes |
| layered-16384 | wcc | `grustcat` |  |  | - | 0.356 | 0.003 | 0.007 | - | 33.45 | - | - | 0 | yes |
| layered-16384 | wcc | `grust` | first | counted | - | 1.069 | 0.012 | 0.011 | - | 7.05 | - | 341579 | 0 | yes |
| layered-16384 | wcc | `grust` | second | counted | - | 0.330 | 0.003 | 0.009 | - | 7.05 | - | 341579 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted` | first | counted | - | 1.083 | 0.018 | 0.017 | - | 7.91 | 0.74 | 487985 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted` | second | counted | - | 0.317 | 0.012 | 0.037 | - | 7.91 | 0.74 | 487985 | 0 | yes |
| layered-16384 | wcc | `grust-next@work-uncounted` | first | work-uncounted | - | 1.039 | 0.022 | 0.022 | - | 5.79 | 0.41 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@work-uncounted` | second | work-uncounted | - | 0.305 | 0.007 | 0.022 | - | 5.79 | 0.41 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@unchecked` | first | unchecked | - | 0.999 | 0.027 | 0.027 | - | 5.71 | 0.40 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@unchecked` | second | unchecked | - | 0.305 | 0.017 | 0.057 | - | 5.71 | 0.40 | - | 0 | yes |
| layered-65536 | bfs | `icebug` |  |  | - | 2.748 | 0.021 | 0.008 | - | 11.43 | - | - | 0 | yes |
| layered-65536 | bfs | `icecat` |  |  | - | 1.569 | 0.035 | 0.022 | - | 7.34 | - | - | 0 | yes |
| layered-65536 | bfs | `grustcat` |  |  | - | 1.019 | 0.004 | 0.004 | - | 142.08 | - | - | 0 | yes |
| layered-65536 | bfs | `grust` | first | counted | - | 1.885 | 0.008 | 0.004 | - | 32.44 | - | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust` | second | counted | - | 1.604 | 0.013 | 0.008 | - | 32.44 | - | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted` | first | counted | - | 2.070 | 0.009 | 0.005 | - | 37.39 | 2.99 | 1979713 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted` | second | counted | - | 1.579 | 0.006 | 0.004 | - | 37.39 | 2.99 | 1979713 | 0 | yes |
| layered-65536 | bfs | `grust-next@work-uncounted` | first | work-uncounted | - | 1.625 | 0.010 | 0.006 | - | 25.91 | 1.67 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@work-uncounted` | second | work-uncounted | - | 1.112 | 0.021 | 0.019 | - | 25.91 | 1.67 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@unchecked` | first | unchecked | - | 1.603 | 0.013 | 0.008 | - | 25.21 | 1.60 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@unchecked` | second | unchecked | - | 1.063 | 0.006 | 0.006 | - | 25.21 | 1.60 | - | 0 | yes |
| layered-65536 | pagerank | `icebug` |  |  | 60 | 14.256 | 0.257 | 0.018 | 0.238 | 11.45 | - | - | 0 | yes |
| layered-65536 | pagerank | `icecat` |  |  | 75 | 87.674 | 0.311 | 0.004 | 1.169 | 7.10 | - | - | 0 | yes |
| layered-65536 | pagerank | `grustcat` |  |  | 75 | 95.772 | 0.183 | 0.002 | 1.277 | 142.11 | - | - | 0 | yes |
| layered-65536 | pagerank | `grust` | first | counted | 75 | 25.945 | 0.202 | 0.008 | 0.346 | 32.60 | - | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust` | second | counted | 75 | 21.307 | 0.088 | 0.004 | 0.284 | 32.60 | - | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted` | first | counted | 75 | 22.611 | 0.137 | 0.006 | 0.301 | 35.16 | 3.01 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted` | second | counted | 75 | 21.586 | 0.107 | 0.005 | 0.288 | 35.16 | 3.01 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 75 | 17.105 | 0.479 | 0.028 | 0.228 | 26.83 | 1.66 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 75 | 15.700 | 0.091 | 0.006 | 0.209 | 26.83 | 1.66 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@unchecked` | first | unchecked | 75 | 17.059 | 0.026 | 0.002 | 0.227 | 25.31 | 1.63 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@unchecked` | second | unchecked | 75 | 15.135 | 0.231 | 0.015 | 0.202 | 25.31 | 1.63 | - | 0 | yes |
| layered-65536 | triangles | `neo4j-graph` |  |  | - | 1.144 | 0.025 | 0.022 | - | 5.33 | - | - | 0 | yes |
| layered-65536 | triangles | `grust` | first | counted | - | 10.190 | 0.033 | 0.003 | - | 33.06 | - | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust` | second | counted | - | 6.524 | 0.047 | 0.007 | - | 33.06 | - | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted` | first | counted | - | 10.194 | 0.118 | 0.012 | - | 34.14 | 0.00 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted` | second | counted | - | 6.580 | 0.015 | 0.002 | - | 34.14 | 0.00 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@work-uncounted` | first | work-uncounted | - | 9.610 | 0.033 | 0.003 | - | 26.57 | 0.00 | - | 0 | yes |
| layered-65536 | triangles | `grust-next@work-uncounted` | second | work-uncounted | - | 5.912 | 0.009 | 0.002 | - | 26.57 | 0.00 | - | 0 | yes |
| layered-65536 | triangles | `grust-next@unchecked` | first | unchecked | - | 9.467 | 0.091 | 0.010 | - | 26.27 | 0.00 | - | 0 | yes |
| layered-65536 | triangles | `grust-next@unchecked` | second | unchecked | - | 5.821 | 0.015 | 0.003 | - | 26.27 | 0.00 | - | 0 | yes |
| layered-65536 | wcc | `neo4j-graph` |  |  | - | 2.622 | 0.244 | 0.093 | - | 5.69 | - | - | 0 | yes |
| layered-65536 | wcc | `icebug` |  |  | - | 4.744 | 0.101 | 0.021 | - | 11.49 | - | - | 0 | yes |
| layered-65536 | wcc | `icecat` |  |  | - | 2.160 | 0.028 | 0.013 | - | 6.87 | - | - | 0 | yes |
| layered-65536 | wcc | `grustcat` |  |  | - | 1.428 | 0.008 | 0.006 | - | 140.64 | - | - | 0 | yes |
| layered-65536 | wcc | `grust` | first | counted | - | 1.563 | 0.009 | 0.006 | - | 31.21 | - | 1368149 | 0 | yes |
| layered-65536 | wcc | `grust` | second | counted | - | 0.860 | 0.005 | 0.006 | - | 31.21 | - | 1368149 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted` | first | counted | - | 1.843 | 0.007 | 0.004 | - | 35.37 | 2.98 | 1954505 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted` | second | counted | - | 0.625 | 0.010 | 0.016 | - | 35.37 | 2.98 | 1954505 | 0 | yes |
| layered-65536 | wcc | `grust-next@work-uncounted` | first | work-uncounted | - | 1.453 | 0.024 | 0.017 | - | 26.18 | 1.68 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@work-uncounted` | second | work-uncounted | - | 0.753 | 0.010 | 0.013 | - | 26.18 | 1.68 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@unchecked` | first | unchecked | - | 1.489 | 0.017 | 0.011 | - | 24.57 | 1.60 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@unchecked` | second | unchecked | - | 0.763 | 0.020 | 0.026 | - | 24.57 | 1.60 | - | 0 | yes |
| path-16384 | bfs | `icebug` |  |  | - | 0.264 | 0.006 | 0.024 | - | 1.81 | - | - | 0 | yes |
| path-16384 | bfs | `icecat` |  |  | - | 0.248 | 0.002 | 0.008 | - | 0.88 | - | - | 0 | yes |
| path-16384 | bfs | `grustcat` |  |  | - | 0.139 | 0.001 | 0.005 | - | 27.07 | - | - | 0 | yes |
| path-16384 | bfs | `grust` | first | counted | - | 0.420 | 0.003 | 0.007 | - | 5.31 | - | 245755 | 0 | yes |
| path-16384 | bfs | `grust` | second | counted | - | 0.340 | 0.000 | 0.001 | - | 5.31 | - | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@counted` | first | counted | - | 0.460 | 0.002 | 0.005 | - | 5.95 | 0.63 | 344057 | 0 | yes |
| path-16384 | bfs | `grust-next@counted` | second | counted | - | 0.321 | 0.000 | 0.001 | - | 5.95 | 0.63 | 344057 | 0 | yes |
| path-16384 | bfs | `grust-next@work-uncounted` | first | work-uncounted | - | 0.253 | 0.003 | 0.014 | - | 4.44 | 0.29 | - | 0 | yes |
| path-16384 | bfs | `grust-next@work-uncounted` | second | work-uncounted | - | 0.114 | 0.001 | 0.009 | - | 4.44 | 0.29 | - | 0 | yes |
| path-16384 | bfs | `grust-next@unchecked` | first | unchecked | - | 0.244 | 0.001 | 0.004 | - | 4.40 | 0.28 | - | 0 | yes |
| path-16384 | bfs | `grust-next@unchecked` | second | unchecked | - | 0.105 | 0.001 | 0.006 | - | 4.40 | 0.28 | - | 0 | yes |
| path-16384 | pagerank | `icebug` |  |  | 54 | 6.925 | 0.143 | 0.021 | 0.128 | 1.79 | - | - | 0 | yes |
| path-16384 | pagerank | `icecat` |  |  | 58 | 9.707 | 0.032 | 0.003 | 0.167 | 0.94 | - | - | 0 | yes |
| path-16384 | pagerank | `grustcat` |  |  | 58 | 9.697 | 0.021 | 0.002 | 0.167 | 27.06 | - | - | 0 | yes |
| path-16384 | pagerank | `grust` | first | counted | 58 | 10.603 | 0.153 | 0.014 | 0.183 | 5.23 | - | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust` | second | counted | 58 | 8.901 | 0.036 | 0.004 | 0.153 | 5.23 | - | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted` | first | counted | 58 | 11.054 | 0.123 | 0.011 | 0.191 | 5.90 | 0.63 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted` | second | counted | 58 | 9.893 | 0.066 | 0.007 | 0.171 | 5.90 | 0.63 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 58 | 9.472 | 0.151 | 0.016 | 0.163 | 4.49 | 0.29 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 58 | 8.231 | 0.046 | 0.006 | 0.142 | 4.49 | 0.29 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@unchecked` | first | unchecked | 58 | 9.057 | 0.181 | 0.020 | 0.156 | 4.41 | 0.28 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@unchecked` | second | unchecked | 58 | 8.123 | 0.032 | 0.004 | 0.140 | 4.41 | 0.28 | - | 0 | yes |
| path-16384 | triangles | `neo4j-graph` |  |  | - | 0.559 | 0.027 | 0.049 | - | 2.13 | - | - | 0 | yes |
| path-16384 | triangles | `grust` | first | counted | - | 2.186 | 0.027 | 0.012 | - | 5.40 | - | 425970 | 0 | yes |
| path-16384 | triangles | `grust` | second | counted | - | 0.975 | 0.023 | 0.023 | - | 5.40 | - | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted` | first | counted | - | 2.186 | 0.032 | 0.015 | - | 5.46 | 0.00 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted` | second | counted | - | 0.981 | 0.011 | 0.011 | - | 5.46 | 0.00 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@work-uncounted` | first | work-uncounted | - | 2.050 | 0.004 | 0.002 | - | 4.44 | 0.00 | - | 0 | yes |
| path-16384 | triangles | `grust-next@work-uncounted` | second | work-uncounted | - | 0.826 | 0.018 | 0.022 | - | 4.44 | 0.00 | - | 0 | yes |
| path-16384 | triangles | `grust-next@unchecked` | first | unchecked | - | 2.037 | 0.030 | 0.015 | - | 4.37 | 0.00 | - | 0 | yes |
| path-16384 | triangles | `grust-next@unchecked` | second | unchecked | - | 0.820 | 0.029 | 0.036 | - | 4.37 | 0.00 | - | 0 | yes |
| path-16384 | wcc | `neo4j-graph` |  |  | - | 0.858 | 0.019 | 0.022 | - | 2.12 | - | - | 0 | yes |
| path-16384 | wcc | `icebug` |  |  | - | 0.361 | 0.001 | 0.003 | - | 1.79 | - | - | 0 | yes |
| path-16384 | wcc | `icecat` |  |  | - | 0.295 | 0.003 | 0.010 | - | 0.93 | - | - | 0 | yes |
| path-16384 | wcc | `grustcat` |  |  | - | 0.163 | 0.005 | 0.033 | - | 26.84 | - | - | 0 | yes |
| path-16384 | wcc | `grust` | first | counted | - | 0.989 | 0.028 | 0.029 | - | 5.24 | - | 229369 | 0 | yes |
| path-16384 | wcc | `grust` | second | counted | - | 0.305 | 0.008 | 0.026 | - | 5.24 | - | 229369 | 0 | yes |
| path-16384 | wcc | `grust-next@counted` | first | counted | - | 1.020 | 0.022 | 0.022 | - | 5.91 | 0.63 | 327671 | 0 | yes |
| path-16384 | wcc | `grust-next@counted` | second | counted | - | 0.302 | 0.007 | 0.024 | - | 5.91 | 0.63 | 327671 | 0 | yes |
| path-16384 | wcc | `grust-next@work-uncounted` | first | work-uncounted | - | 0.955 | 0.014 | 0.014 | - | 4.47 | 0.29 | - | 0 | yes |
| path-16384 | wcc | `grust-next@work-uncounted` | second | work-uncounted | - | 0.263 | 0.008 | 0.030 | - | 4.47 | 0.29 | - | 0 | yes |
| path-16384 | wcc | `grust-next@unchecked` | first | unchecked | - | 0.931 | 0.023 | 0.025 | - | 4.48 | 0.28 | - | 0 | yes |
| path-16384 | wcc | `grust-next@unchecked` | second | unchecked | - | 0.269 | 0.005 | 0.017 | - | 4.48 | 0.28 | - | 0 | yes |
| path-65536 | bfs | `icebug` |  |  | - | 1.042 | 0.019 | 0.018 | - | 7.26 | - | - | 0 | yes |
| path-65536 | bfs | `icecat` |  |  | - | 1.004 | 0.006 | 0.006 | - | 4.36 | - | - | 0 | yes |
| path-65536 | bfs | `grustcat` |  |  | - | 0.573 | 0.008 | 0.013 | - | 113.03 | - | - | 0 | yes |
| path-65536 | bfs | `grust` | first | counted | - | 1.695 | 0.009 | 0.005 | - | 22.93 | - | 983035 | 0 | yes |
| path-65536 | bfs | `grust` | second | counted | - | 1.387 | 0.009 | 0.007 | - | 22.93 | - | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@counted` | first | counted | - | 1.838 | 0.009 | 0.005 | - | 27.76 | 2.52 | 1376249 | 0 | yes |
| path-65536 | bfs | `grust-next@counted` | second | counted | - | 1.288 | 0.003 | 0.002 | - | 27.76 | 2.52 | 1376249 | 0 | yes |
| path-65536 | bfs | `grust-next@work-uncounted` | first | work-uncounted | - | 1.014 | 0.017 | 0.017 | - | 21.07 | 1.17 | - | 0 | yes |
| path-65536 | bfs | `grust-next@work-uncounted` | second | work-uncounted | - | 0.457 | 0.001 | 0.002 | - | 21.07 | 1.17 | - | 0 | yes |
| path-65536 | bfs | `grust-next@unchecked` | first | unchecked | - | 0.974 | 0.016 | 0.016 | - | 20.20 | 1.12 | - | 0 | yes |
| path-65536 | bfs | `grust-next@unchecked` | second | unchecked | - | 0.423 | 0.001 | 0.002 | - | 20.20 | 1.12 | - | 0 | yes |
| path-65536 | pagerank | `icebug` |  |  | 46 | 11.091 | 0.201 | 0.018 | 0.241 | 7.33 | - | - | 0 | yes |
| path-65536 | pagerank | `icecat` |  |  | 50 | 34.305 | 0.088 | 0.003 | 0.686 | 4.50 | - | - | 0 | yes |
| path-65536 | pagerank | `grustcat` |  |  | 50 | 33.662 | 0.039 | 0.001 | 0.673 | 115.73 | - | - | 0 | yes |
| path-65536 | pagerank | `grust` | first | counted | 50 | 17.222 | 0.937 | 0.054 | 0.344 | 24.82 | - | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust` | second | counted | 50 | 12.408 | 0.243 | 0.020 | 0.248 | 24.82 | - | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted` | first | counted | 50 | 13.542 | 0.173 | 0.013 | 0.271 | 26.64 | 2.54 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted` | second | counted | 50 | 12.197 | 0.128 | 0.010 | 0.244 | 26.64 | 2.54 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 50 | 9.906 | 0.220 | 0.022 | 0.198 | 18.68 | 1.17 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 50 | 8.835 | 0.084 | 0.009 | 0.177 | 18.68 | 1.17 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@unchecked` | first | unchecked | 50 | 9.539 | 0.108 | 0.011 | 0.191 | 19.20 | 1.11 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@unchecked` | second | unchecked | 50 | 8.472 | 0.111 | 0.013 | 0.169 | 19.20 | 1.11 | - | 0 | yes |
| path-65536 | triangles | `neo4j-graph` |  |  | - | 0.807 | 0.018 | 0.022 | - | 4.88 | - | - | 0 | yes |
| path-65536 | triangles | `grust` | first | counted | - | 6.408 | 0.015 | 0.002 | - | 24.89 | - | 1703922 | 0 | yes |
| path-65536 | triangles | `grust` | second | counted | - | 3.629 | 0.038 | 0.010 | - | 24.89 | - | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted` | first | counted | - | 6.514 | 0.100 | 0.015 | - | 26.06 | 0.00 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted` | second | counted | - | 3.713 | 0.031 | 0.008 | - | 26.06 | 0.00 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@work-uncounted` | first | work-uncounted | - | 5.819 | 0.033 | 0.006 | - | 19.82 | 0.00 | - | 0 | yes |
| path-65536 | triangles | `grust-next@work-uncounted` | second | work-uncounted | - | 3.000 | 0.012 | 0.004 | - | 19.82 | 0.00 | - | 0 | yes |
| path-65536 | triangles | `grust-next@unchecked` | first | unchecked | - | 5.699 | 0.026 | 0.005 | - | 20.31 | 0.00 | - | 0 | yes |
| path-65536 | triangles | `grust-next@unchecked` | second | unchecked | - | 2.855 | 0.021 | 0.007 | - | 20.31 | 0.00 | - | 0 | yes |
| path-65536 | wcc | `neo4j-graph` |  |  | - | 2.236 | 0.059 | 0.027 | - | 4.94 | - | - | 0 | yes |
| path-65536 | wcc | `icebug` |  |  | - | 1.345 | 0.005 | 0.004 | - | 7.19 | - | - | 0 | yes |
| path-65536 | wcc | `icecat` |  |  | - | 1.201 | 0.013 | 0.011 | - | 4.44 | - | - | 0 | yes |
| path-65536 | wcc | `grustcat` |  |  | - | 0.662 | 0.004 | 0.006 | - | 114.17 | - | - | 0 | yes |
| path-65536 | wcc | `grust` | first | counted | - | 1.511 | 0.044 | 0.029 | - | 23.03 | - | 917497 | 0 | yes |
| path-65536 | wcc | `grust` | second | counted | - | 0.784 | 0.014 | 0.018 | - | 23.03 | - | 917497 | 0 | yes |
| path-65536 | wcc | `grust-next@counted` | first | counted | - | 1.748 | 0.028 | 0.016 | - | 26.05 | 2.53 | 1310711 | 0 | yes |
| path-65536 | wcc | `grust-next@counted` | second | counted | - | 0.543 | 0.000 | 0.001 | - | 26.05 | 2.53 | 1310711 | 0 | yes |
| path-65536 | wcc | `grust-next@work-uncounted` | first | work-uncounted | - | 1.351 | 0.001 | 0.001 | - | 19.55 | 1.16 | - | 0 | yes |
| path-65536 | wcc | `grust-next@work-uncounted` | second | work-uncounted | - | 0.674 | 0.014 | 0.020 | - | 19.55 | 1.16 | - | 0 | yes |
| path-65536 | wcc | `grust-next@unchecked` | first | unchecked | - | 1.322 | 0.014 | 0.011 | - | 20.58 | 1.12 | - | 0 | yes |
| path-65536 | wcc | `grust-next@unchecked` | second | unchecked | - | 0.624 | 0.005 | 0.008 | - | 20.58 | 1.12 | - | 0 | yes |
| uniform-16384 | bfs | `icebug` |  |  | - | 2.097 | 0.033 | 0.016 | - | 10.13 | - | - | 0 | yes |
| uniform-16384 | bfs | `icecat` |  |  | - | 0.885 | 0.021 | 0.024 | - | 7.00 | - | - | 0 | yes |
| uniform-16384 | bfs | `grustcat` |  |  | - | 0.883 | 0.059 | 0.067 | - | 94.61 | - | - | 0 | yes |
| uniform-16384 | bfs | `grust` | first | counted | - | 1.682 | 0.041 | 0.024 | - | 20.47 | - | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust` | second | counted | - | 1.484 | 0.011 | 0.007 | - | 20.47 | - | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted` | first | counted | - | 1.689 | 0.009 | 0.006 | - | 23.91 | 1.84 | 1490619 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted` | second | counted | - | 1.496 | 0.006 | 0.004 | - | 23.91 | 1.84 | 1490619 | 0 | yes |
| uniform-16384 | bfs | `grust-next@work-uncounted` | first | work-uncounted | - | 1.153 | 0.020 | 0.017 | - | 15.58 | 1.39 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@work-uncounted` | second | work-uncounted | - | 0.936 | 0.011 | 0.011 | - | 15.58 | 1.39 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@unchecked` | first | unchecked | - | 1.030 | 0.003 | 0.003 | - | 15.39 | 1.36 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@unchecked` | second | unchecked | - | 0.821 | 0.002 | 0.002 | - | 15.39 | 1.36 | - | 0 | yes |
| uniform-16384 | pagerank | `neo4j-graph` |  |  | 28 | 11.261 | 0.059 | 0.005 | 0.402 | 4.38 | - | - | 0 | yes |
| uniform-16384 | pagerank | `icebug` |  |  | 12 | 2.950 | 0.067 | 0.023 | 0.246 | 10.28 | - | - | 0 | yes |
| uniform-16384 | pagerank | `icecat` |  |  | 16 | 7.242 | 0.016 | 0.002 | 0.453 | 6.87 | - | - | 0 | yes |
| uniform-16384 | pagerank | `grustcat` |  |  | 16 | 6.818 | 0.007 | 0.001 | 0.426 | 90.84 | - | - | 0 | yes |
| uniform-16384 | pagerank | `grust` | first | counted | 16 | 6.158 | 0.113 | 0.018 | 0.385 | 21.50 | - | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust` | second | counted | 16 | 3.279 | 0.096 | 0.029 | 0.205 | 21.50 | - | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted` | first | counted | 16 | 4.377 | 0.041 | 0.009 | 0.274 | 22.26 | 1.80 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted` | second | counted | 16 | 3.462 | 0.032 | 0.009 | 0.216 | 22.26 | 1.80 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 16 | 3.817 | 0.057 | 0.015 | 0.239 | 14.78 | 1.40 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 16 | 2.865 | 0.056 | 0.020 | 0.179 | 14.78 | 1.40 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@unchecked` | first | unchecked | 16 | 3.751 | 0.107 | 0.029 | 0.234 | 14.21 | 1.36 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@unchecked` | second | unchecked | 16 | 2.778 | 0.035 | 0.013 | 0.174 | 14.21 | 1.36 | - | 0 | yes |
| uniform-16384 | triangles | `neo4j-graph` |  |  | - | 1.390 | 0.020 | 0.014 | - | 4.37 | - | - | 0 | yes |
| uniform-16384 | triangles | `grust` | first | counted | - | 9.393 | 0.132 | 0.014 | - | 24.95 | - | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust` | second | counted | - | 6.649 | 0.020 | 0.003 | - | 24.95 | - | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted` | first | counted | - | 9.158 | 0.061 | 0.007 | - | 23.30 | 0.00 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted` | second | counted | - | 6.458 | 0.043 | 0.007 | - | 23.30 | 0.00 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@work-uncounted` | first | work-uncounted | - | 9.035 | 0.013 | 0.001 | - | 15.92 | 0.00 | - | 0 | yes |
| uniform-16384 | triangles | `grust-next@work-uncounted` | second | work-uncounted | - | 6.246 | 0.032 | 0.005 | - | 15.92 | 0.00 | - | 0 | yes |
| uniform-16384 | triangles | `grust-next@unchecked` | first | unchecked | - | 8.947 | 0.035 | 0.004 | - | 15.05 | 0.00 | - | 0 | yes |
| uniform-16384 | triangles | `grust-next@unchecked` | second | unchecked | - | 6.243 | 0.046 | 0.007 | - | 15.05 | 0.00 | - | 0 | yes |
| uniform-16384 | wcc | `neo4j-graph` |  |  | - | 1.189 | 0.045 | 0.038 | - | 4.47 | - | - | 0 | yes |
| uniform-16384 | wcc | `icebug` |  |  | - | 3.238 | 0.162 | 0.050 | - | 10.18 | - | - | 0 | yes |
| uniform-16384 | wcc | `icecat` |  |  | - | 1.101 | 0.008 | 0.007 | - | 7.00 | - | - | 0 | yes |
| uniform-16384 | wcc | `grustcat` |  |  | - | 0.726 | 0.003 | 0.004 | - | 92.87 | - | - | 0 | yes |
| uniform-16384 | wcc | `grust` | first | counted | - | 1.460 | 0.016 | 0.011 | - | 18.91 | - | 1031990 | 0 | yes |
| uniform-16384 | wcc | `grust` | second | counted | - | 0.641 | 0.006 | 0.010 | - | 18.91 | - | 1031990 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted` | first | counted | - | 1.464 | 0.029 | 0.020 | - | 22.55 | 1.83 | 1474271 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted` | second | counted | - | 0.661 | 0.008 | 0.013 | - | 22.55 | 1.83 | 1474271 | 0 | yes |
| uniform-16384 | wcc | `grust-next@work-uncounted` | first | work-uncounted | - | 1.441 | 0.020 | 0.014 | - | 15.04 | 1.41 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@work-uncounted` | second | work-uncounted | - | 0.573 | 0.033 | 0.057 | - | 15.04 | 1.41 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@unchecked` | first | unchecked | - | 1.476 | 0.073 | 0.050 | - | 13.93 | 1.38 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@unchecked` | second | unchecked | - | 0.651 | 0.039 | 0.060 | - | 13.93 | 1.38 | - | 0 | yes |
| uniform-65536 | bfs | `icebug` |  |  | - | 14.314 | 0.540 | 0.038 | - | 61.82 | - | - | 0 | yes |
| uniform-65536 | bfs | `icecat` |  |  | - | 4.426 | 0.370 | 0.084 | - | 21.48 | - | - | 0 | yes |
| uniform-65536 | bfs | `grustcat` |  |  | - | 5.955 | 0.040 | 0.007 | - | 465.84 | - | - | 0 | yes |
| uniform-65536 | bfs | `grust` | first | counted | - | 4.435 | 0.154 | 0.035 | - | 101.82 | - | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust` | second | counted | - | 3.430 | 0.053 | 0.015 | - | 101.82 | - | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted` | first | counted | - | 4.653 | 0.166 | 0.036 | - | 123.56 | 8.68 | 5963146 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted` | second | counted | - | 3.401 | 0.009 | 0.003 | - | 123.56 | 8.68 | 5963146 | 0 | yes |
| uniform-65536 | bfs | `grust-next@work-uncounted` | first | work-uncounted | - | 4.326 | 0.044 | 0.010 | - | 70.55 | 6.42 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@work-uncounted` | second | work-uncounted | - | 3.223 | 0.088 | 0.027 | - | 70.55 | 6.42 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@unchecked` | first | unchecked | - | 4.253 | 0.096 | 0.023 | - | 68.97 | 6.64 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@unchecked` | second | unchecked | - | 3.174 | 0.054 | 0.017 | - | 68.97 | 6.64 | - | 0 | yes |
| uniform-65536 | pagerank | `neo4j-graph` |  |  | 34 | 17.195 | 0.363 | 0.021 | 0.506 | 14.62 | - | - | 0 | yes |
| uniform-65536 | pagerank | `icebug` |  |  | 11 | 8.313 | 0.236 | 0.028 | 0.756 | 67.28 | - | - | 0 | yes |
| uniform-65536 | pagerank | `icecat` |  |  | 16 | 30.059 | 0.230 | 0.008 | 1.879 | 21.81 | - | - | 0 | yes |
| uniform-65536 | pagerank | `grustcat` |  |  | 16 | 31.326 | 0.453 | 0.014 | 1.958 | 469.38 | - | - | 0 | yes |
| uniform-65536 | pagerank | `grust` | first | counted | 16 | 18.612 | 0.729 | 0.039 | 1.163 | 107.25 | - | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust` | second | counted | 16 | 8.326 | 0.084 | 0.010 | 0.520 | 107.25 | - | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted` | first | counted | 16 | 8.946 | 0.155 | 0.017 | 0.559 | 121.85 | 8.68 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted` | second | counted | 16 | 7.244 | 0.153 | 0.021 | 0.453 | 121.85 | 8.68 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 16 | 6.467 | 0.144 | 0.022 | 0.404 | 70.82 | 6.88 | - | 0 | yes |
| uniform-65536 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 16 | 5.148 | 0.049 | 0.010 | 0.322 | 70.82 | 6.88 | - | 0 | yes |
| uniform-65536 | pagerank | `grust-next@unchecked` | first | unchecked | 16 | 6.498 | 0.064 | 0.010 | 0.406 | 69.01 | 6.59 | - | 0 | yes |
| uniform-65536 | pagerank | `grust-next@unchecked` | second | unchecked | 16 | 5.161 | 0.048 | 0.009 | 0.323 | 69.01 | 6.59 | - | 0 | yes |
| uniform-65536 | triangles | `neo4j-graph` |  |  | - | 4.091 | 0.079 | 0.019 | - | 14.83 | - | - | 0 | yes |
| uniform-65536 | triangles | `grust` | first | counted | - | 33.277 | 0.109 | 0.003 | - | 130.87 | - | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust` | second | counted | - | 27.083 | 0.047 | 0.002 | - | 130.87 | - | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted` | first | counted | - | 32.979 | 0.146 | 0.004 | - | 138.07 | 0.00 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted` | second | counted | - | 26.674 | 0.096 | 0.004 | - | 138.07 | 0.00 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@work-uncounted` | first | work-uncounted | - | 32.204 | 0.235 | 0.007 | - | 79.40 | 0.00 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@work-uncounted` | second | work-uncounted | - | 25.743 | 0.063 | 0.002 | - | 79.40 | 0.00 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@unchecked` | first | unchecked | - | 32.100 | 0.118 | 0.004 | - | 79.56 | 0.00 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@unchecked` | second | unchecked | - | 25.950 | 0.204 | 0.008 | - | 79.56 | 0.00 | - | 0 | yes |
| uniform-65536 | wcc | `neo4j-graph` |  |  | - | 3.179 | 0.177 | 0.056 | - | 14.80 | - | - | 0 | yes |
| uniform-65536 | wcc | `icebug` |  |  | - | 25.800 | 1.568 | 0.061 | - | 66.23 | - | - | 0 | yes |
| uniform-65536 | wcc | `icecat` |  |  | - | 4.030 | 0.010 | 0.002 | - | 21.45 | - | - | 0 | yes |
| uniform-65536 | wcc | `grustcat` |  |  | - | 3.020 | 0.007 | 0.002 | - | 473.99 | - | - | 0 | yes |
| uniform-65536 | wcc | `grust` | first | counted | - | 2.933 | 0.182 | 0.062 | - | 109.78 | - | 4128512 | 0 | yes |
| uniform-65536 | wcc | `grust` | second | counted | - | 2.068 | 0.081 | 0.039 | - | 109.78 | - | 4128512 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted` | first | counted | - | 3.211 | 0.053 | 0.017 | - | 122.30 | 8.77 | 5897873 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted` | second | counted | - | 1.709 | 0.064 | 0.038 | - | 122.30 | 8.77 | 5897873 | 0 | yes |
| uniform-65536 | wcc | `grust-next@work-uncounted` | first | work-uncounted | - | 2.597 | 0.170 | 0.065 | - | 67.85 | 6.39 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@work-uncounted` | second | work-uncounted | - | 2.027 | 0.080 | 0.040 | - | 67.85 | 6.39 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@unchecked` | first | unchecked | - | 2.735 | 0.029 | 0.011 | - | 69.39 | 6.31 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@unchecked` | second | unchecked | - | 2.142 | 0.175 | 0.082 | - | 69.39 | 6.31 | - | 0 | yes |

### `large-one-thread.json`: large-one-thread

workers 1, concurrency 1, 1 warmup + 5 repeats, steal over the run 10 ticks, 2504.2 s, unusable at MAD/median >= 0.25

| fixture | algorithm | participant | call | accounting | iters | total ms | MAD | MAD/median | per iter | build ms | incoming ms | work units | steal | usable |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| hub-2097152 | pagerank | `neo4j-graph` |  |  | 26 | 2585.376 | 139.555 | 0.054 | 99.438 | 4284.66 | - | - | 5 | yes |
| hub-2097152 | pagerank | `icebug` |  |  | 10 | 5114.278 | 242.081 | 0.047 | 511.428 | 3600.16 | - | - | 5 | yes |
| hub-2097152 | pagerank | `icecat` |  |  | 16 | 2825.278 | 8.172 | 0.003 | 176.580 | 612.56 | - | - | 5 | yes |
| hub-2097152 | pagerank | `grustcat` |  |  | 16 | 3112.822 | 12.534 | 0.004 | 194.551 | 20419.09 | - | - | 5 | yes |
| hub-2097152 | pagerank | `grust#1` | first | counted | 16 | 6388.559 | 29.424 | 0.005 | 399.285 | 4051.76 | - | 540705943 | 5 | yes |
| hub-2097152 | pagerank | `grust#1` | second | counted | 16 | 5625.493 | 67.256 | 0.012 | 351.593 | 4051.76 | - | 540705943 | 5 | yes |
| hub-2097152 | pagerank | `grust#unset` | first | counted | 16 | 16162.431 | 664.333 | 0.041 | 1010.152 | 4064.82 | - | 559594681 | 5 | yes |
| hub-2097152 | pagerank | `grust#unset` | second | counted | 16 | 16114.663 | 40.172 | 0.002 | 1007.166 | 4064.82 | - | 559594681 | 5 | yes |
| hub-2097152 | pagerank | `grust-next@counted#1` | first | counted | 16 | 3460.550 | 110.016 | 0.032 | 216.284 | 5787.20 | 723.86 | 540705943 | 5 | yes |
| hub-2097152 | pagerank | `grust-next@counted#1` | second | counted | 16 | 3564.079 | 88.065 | 0.025 | 222.755 | 5787.20 | 723.86 | 540705943 | 5 | yes |
| hub-2097152 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 16 | 3514.411 | 35.928 | 0.010 | 219.651 | 3975.40 | 720.15 | - | 5 | yes |
| hub-2097152 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 16 | 3416.864 | 202.260 | 0.059 | 213.554 | 3975.40 | 720.15 | - | 5 | yes |
| hub-2097152 | pagerank | `grust-next@unchecked#1` | first | unchecked | 16 | 3186.544 | 21.137 | 0.007 | 199.159 | 3920.89 | 730.10 | - | 5 | yes |
| hub-2097152 | pagerank | `grust-next@unchecked#1` | second | unchecked | 16 | 3259.115 | 157.731 | 0.048 | 203.695 | 3920.89 | 730.10 | - | 5 | yes |
| hub-2097152 | pagerank | `grust-next@counted#unset` | first | counted | 16 | 6980.047 | 561.778 | 0.080 | 436.253 | 5767.01 | 705.53 | 616174673 | 5 | yes |
| hub-2097152 | pagerank | `grust-next@counted#unset` | second | counted | 16 | 7141.829 | 235.416 | 0.033 | 446.364 | 5767.01 | 705.53 | 616174673 | 5 | yes |
| hub-2097152 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 16 | 5839.022 | 239.396 | 0.041 | 364.939 | 3920.18 | 704.32 | - | 5 | yes |
| hub-2097152 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 16 | 6044.877 | 92.762 | 0.015 | 377.805 | 3920.18 | 704.32 | - | 5 | yes |
| hub-2097152 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 16 | 5862.376 | 75.514 | 0.013 | 366.399 | 3867.32 | 690.51 | - | 5 | yes |
| hub-2097152 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 16 | 5917.328 | 228.470 | 0.039 | 369.833 | 3867.32 | 690.51 | - | 5 | yes |
| uniform-2097152 | pagerank | `neo4j-graph` |  |  | 26 | 2553.544 | 75.830 | 0.030 | 98.213 | 4305.17 | - | - | 5 | yes |
| uniform-2097152 | pagerank | `icebug` |  |  | 10 | 5212.101 | 84.363 | 0.016 | 521.210 | 3280.51 | - | - | 5 | yes |
| uniform-2097152 | pagerank | `icecat` |  |  | 16 | 2883.612 | 68.352 | 0.024 | 180.226 | 603.87 | - | - | 5 | yes |
| uniform-2097152 | pagerank | `grustcat` |  |  | 16 | 3512.282 | 41.732 | 0.012 | 219.518 | 22756.89 | - | - | 5 | yes |
| uniform-2097152 | pagerank | `grust#1` | first | counted | 16 | 6661.300 | 59.639 | 0.009 | 416.331 | 4088.94 | - | 541064143 | 5 | yes |
| uniform-2097152 | pagerank | `grust#1` | second | counted | 16 | 5957.462 | 26.037 | 0.004 | 372.341 | 4088.94 | - | 541064143 | 5 | yes |
| uniform-2097152 | pagerank | `grust#unset` | first | counted | 16 | 16749.269 | 219.561 | 0.013 | 1046.829 | 4112.12 | - | 559938553 | 5 | yes |
| uniform-2097152 | pagerank | `grust#unset` | second | counted | 16 | 16646.027 | 302.704 | 0.018 | 1040.377 | 4112.12 | - | 559938553 | 5 | yes |
| uniform-2097152 | pagerank | `grust-next@counted#1` | first | counted | 16 | 3696.771 | 24.862 | 0.007 | 231.048 | 5806.79 | 708.88 | 541064143 | 5 | yes |
| uniform-2097152 | pagerank | `grust-next@counted#1` | second | counted | 16 | 3592.637 | 35.022 | 0.010 | 224.540 | 5806.79 | 708.88 | 541064143 | 5 | yes |
| uniform-2097152 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 16 | 3581.358 | 134.976 | 0.038 | 223.835 | 3987.00 | 732.86 | - | 5 | yes |
| uniform-2097152 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 16 | 3553.945 | 38.131 | 0.011 | 222.122 | 3987.00 | 732.86 | - | 5 | yes |
| uniform-2097152 | pagerank | `grust-next@unchecked#1` | first | unchecked | 16 | 3363.087 | 63.648 | 0.019 | 210.193 | 3957.21 | 718.47 | - | 5 | yes |
| uniform-2097152 | pagerank | `grust-next@unchecked#1` | second | unchecked | 16 | 3260.495 | 223.970 | 0.069 | 203.781 | 3957.21 | 718.47 | - | 5 | yes |
| uniform-2097152 | pagerank | `grust-next@counted#unset` | first | counted | 16 | 7015.627 | 49.706 | 0.007 | 438.477 | 5753.82 | 694.94 | 616561529 | 5 | yes |
| uniform-2097152 | pagerank | `grust-next@counted#unset` | second | counted | 16 | 7030.664 | 38.471 | 0.005 | 439.416 | 5753.82 | 694.94 | 616561529 | 5 | yes |
| uniform-2097152 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 16 | 5733.411 | 3.365 | 0.001 | 358.338 | 3938.97 | 700.19 | - | 5 | yes |
| uniform-2097152 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 16 | 5851.537 | 165.518 | 0.028 | 365.721 | 3938.97 | 700.19 | - | 5 | yes |
| uniform-2097152 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 16 | 5596.274 | 20.626 | 0.004 | 349.767 | 3882.87 | 692.33 | - | 5 | yes |
| uniform-2097152 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 16 | 5731.193 | 148.835 | 0.026 | 358.200 | 3882.87 | 692.33 | - | 5 | yes |

### `large-full-width.json`: large-full-width

workers 16, concurrency 16, 1 warmup + 5 repeats, steal over the run 4 ticks, 906.8 s, unusable at MAD/median >= 0.25

| fixture | algorithm | participant | call | accounting | iters | total ms | MAD | MAD/median | per iter | build ms | incoming ms | work units | steal | usable |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| hub-2097152 | pagerank | `neo4j-graph` |  |  | 28 | 272.614 | 2.042 | 0.007 | 9.736 | 478.67 | - | - | 2 | yes |
| hub-2097152 | pagerank | `icebug` |  |  | 10 | 502.144 | 14.867 | 0.030 | 50.214 | 3594.60 | - | - | 2 | yes |
| hub-2097152 | pagerank | `icecat` |  |  | 16 | 2813.720 | 84.315 | 0.030 | 175.858 | 606.15 | - | - | 2 | yes |
| hub-2097152 | pagerank | `grustcat` |  |  | 16 | 3084.544 | 72.544 | 0.024 | 192.784 | 20319.52 | - | - | 2 | yes |
| hub-2097152 | pagerank | `grust` | first | counted | 16 | 1308.364 | 7.448 | 0.006 | 81.773 | 4061.79 | - | 540705943 | 2 | yes |
| hub-2097152 | pagerank | `grust` | second | counted | 16 | 562.117 | 8.637 | 0.015 | 35.132 | 4061.79 | - | 540705943 | 2 | yes |
| hub-2097152 | pagerank | `grust-next@counted` | first | counted | 16 | 264.984 | 8.926 | 0.034 | 16.562 | 5820.88 | 729.60 | 540705943 | 2 | yes |
| hub-2097152 | pagerank | `grust-next@counted` | second | counted | 16 | 271.025 | 17.648 | 0.065 | 16.939 | 5820.88 | 729.60 | 540705943 | 2 | yes |
| hub-2097152 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 16 | 244.463 | 3.462 | 0.014 | 15.279 | 3940.89 | 714.49 | - | 2 | yes |
| hub-2097152 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 16 | 257.579 | 9.019 | 0.035 | 16.099 | 3940.89 | 714.49 | - | 2 | yes |
| hub-2097152 | pagerank | `grust-next@unchecked` | first | unchecked | 16 | 241.988 | 6.301 | 0.026 | 15.124 | 3879.28 | 699.02 | - | 2 | yes |
| hub-2097152 | pagerank | `grust-next@unchecked` | second | unchecked | 16 | 257.906 | 16.440 | 0.064 | 16.119 | 3879.28 | 699.02 | - | 2 | yes |
| uniform-2097152 | pagerank | `neo4j-graph` |  |  | 27 | 283.887 | 1.334 | 0.005 | 10.514 | 480.52 | - | - | 2 | yes |
| uniform-2097152 | pagerank | `icebug` |  |  | 10 | 534.290 | 5.620 | 0.011 | 53.429 | 3307.84 | - | - | 2 | yes |
| uniform-2097152 | pagerank | `icecat` |  |  | 16 | 3024.946 | 46.034 | 0.015 | 189.059 | 609.74 | - | - | 2 | yes |
| uniform-2097152 | pagerank | `grustcat` |  |  | 16 | 3426.904 | 31.333 | 0.009 | 214.182 | 22761.30 | - | - | 2 | yes |
| uniform-2097152 | pagerank | `grust` | first | counted | 16 | 1374.806 | 8.660 | 0.006 | 85.925 | 4064.81 | - | 541064143 | 2 | yes |
| uniform-2097152 | pagerank | `grust` | second | counted | 16 | 640.057 | 14.201 | 0.022 | 40.004 | 4064.81 | - | 541064143 | 2 | yes |
| uniform-2097152 | pagerank | `grust-next@counted` | first | counted | 16 | 267.938 | 6.188 | 0.023 | 16.746 | 5835.17 | 709.07 | 541064143 | 2 | yes |
| uniform-2097152 | pagerank | `grust-next@counted` | second | counted | 16 | 277.586 | 13.380 | 0.048 | 17.349 | 5835.17 | 709.07 | 541064143 | 2 | yes |
| uniform-2097152 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 16 | 261.485 | 12.042 | 0.046 | 16.343 | 4009.21 | 724.75 | - | 2 | yes |
| uniform-2097152 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 16 | 251.184 | 13.248 | 0.053 | 15.699 | 4009.21 | 724.75 | - | 2 | yes |
| uniform-2097152 | pagerank | `grust-next@unchecked` | first | unchecked | 16 | 268.626 | 8.118 | 0.030 | 16.789 | 3940.07 | 739.29 | - | 2 | yes |
| uniform-2097152 | pagerank | `grust-next@unchecked` | second | unchecked | 16 | 236.523 | 4.001 | 0.017 | 14.783 | 3940.07 | 739.29 | - | 2 | yes |

### `xlarge-one-thread.json`: xlarge-one-thread

workers 1, concurrency 1, 1 warmup + 5 repeats, steal over the run 20 ticks, 5118.2 s, unusable at MAD/median >= 0.25

| fixture | algorithm | participant | call | accounting | iters | total ms | MAD | MAD/median | per iter | build ms | incoming ms | work units | steal | usable |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| hub-4194304 | pagerank | `neo4j-graph` |  |  | 23 | 6158.301 | 164.906 | 0.027 | 267.752 | 9022.43 | - | - | 11 | yes |
| hub-4194304 | pagerank | `icebug` |  |  | 10 | 11019.399 | 348.465 | 0.032 | 1101.940 | 7425.86 | - | - | 11 | yes |
| hub-4194304 | pagerank | `icecat` |  |  | 16 | 6677.338 | 16.194 | 0.002 | 417.334 | 1212.16 | - | - | 11 | yes |
| hub-4194304 | pagerank | `grustcat` |  |  | 16 | 7014.938 | 55.223 | 0.008 | 438.434 | 45503.66 | - | - | 11 | yes |
| hub-4194304 | pagerank | `grust#1` | first | counted | 16 | 14198.592 | 88.393 | 0.006 | 887.412 | 8158.46 | - | 1081412859 | 11 | yes |
| hub-4194304 | pagerank | `grust#1` | second | counted | 16 | 12486.676 | 74.790 | 0.006 | 780.417 | 8158.46 | - | 1081412859 | 11 | yes |
| hub-4194304 | pagerank | `grust#unset` | first | counted | 16 | 34034.512 | 285.554 | 0.008 | 2127.157 | 8130.22 | - | 1119190297 | 11 | yes |
| hub-4194304 | pagerank | `grust#unset` | second | counted | 16 | 34026.707 | 75.389 | 0.002 | 2126.669 | 8130.22 | - | 1119190297 | 11 | yes |
| hub-4194304 | pagerank | `grust-next@counted#1` | first | counted | 16 | 8180.584 | 42.200 | 0.005 | 511.286 | 11752.45 | 1552.63 | 1081412859 | 11 | yes |
| hub-4194304 | pagerank | `grust-next@counted#1` | second | counted | 16 | 8040.038 | 88.573 | 0.011 | 502.502 | 11752.45 | 1552.63 | 1081412859 | 11 | yes |
| hub-4194304 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 16 | 7677.629 | 18.035 | 0.002 | 479.852 | 8043.11 | 1527.19 | - | 11 | yes |
| hub-4194304 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 16 | 7662.404 | 49.127 | 0.006 | 478.900 | 8043.11 | 1527.19 | - | 11 | yes |
| hub-4194304 | pagerank | `grust-next@unchecked#1` | first | unchecked | 16 | 7494.930 | 36.378 | 0.005 | 468.433 | 8020.53 | 1569.64 | - | 11 | yes |
| hub-4194304 | pagerank | `grust-next@unchecked#1` | second | unchecked | 16 | 7478.863 | 111.176 | 0.015 | 467.429 | 8020.53 | 1569.64 | - | 11 | yes |
| hub-4194304 | pagerank | `grust-next@counted#unset` | first | counted | 16 | 15152.098 | 70.988 | 0.005 | 947.006 | 11760.73 | 1568.90 | 1232350397 | 11 | yes |
| hub-4194304 | pagerank | `grust-next@counted#unset` | second | counted | 16 | 15106.917 | 140.468 | 0.009 | 944.182 | 11760.73 | 1568.90 | 1232350397 | 11 | yes |
| hub-4194304 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 16 | 12675.257 | 63.879 | 0.005 | 792.204 | 8099.10 | 1532.71 | - | 11 | yes |
| hub-4194304 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 16 | 12589.724 | 100.975 | 0.008 | 786.858 | 8099.10 | 1532.71 | - | 11 | yes |
| hub-4194304 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 16 | 12707.474 | 12.407 | 0.001 | 794.217 | 8080.30 | 1588.78 | - | 11 | yes |
| hub-4194304 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 16 | 12663.395 | 39.030 | 0.003 | 791.462 | 8080.30 | 1588.78 | - | 11 | yes |
| uniform-4194304 | pagerank | `neo4j-graph` |  |  | 29 | 5328.148 | 153.341 | 0.029 | 183.729 | 7468.53 | - | - | 9 | yes |
| uniform-4194304 | pagerank | `icebug` |  |  | 9 | 9309.602 | 112.684 | 0.012 | 1034.400 | 6517.91 | - | - | 9 | yes |
| uniform-4194304 | pagerank | `icecat` |  |  | 16 | 5794.690 | 56.230 | 0.010 | 362.168 | 1187.10 | - | - | 9 | yes |
| uniform-4194304 | pagerank | `grustcat` |  |  | 16 | 7052.948 | 62.842 | 0.009 | 440.809 | 43513.50 | - | - | 9 | yes |
| uniform-4194304 | pagerank | `grust#1` | first | counted | 16 | 13314.922 | 61.017 | 0.005 | 832.183 | 7735.60 | - | 1082129509 | 9 | yes |
| uniform-4194304 | pagerank | `grust#1` | second | counted | 16 | 11981.429 | 23.080 | 0.002 | 748.839 | 7735.60 | - | 1082129509 | 9 | yes |
| uniform-4194304 | pagerank | `grust#unset` | first | counted | 16 | 26598.317 | 1473.410 | 0.055 | 1662.395 | 7763.50 | - | 1119878281 | 9 | yes |
| uniform-4194304 | pagerank | `grust#unset` | second | counted | 16 | 26102.825 | 517.146 | 0.020 | 1631.427 | 7763.50 | - | 1119878281 | 9 | yes |
| uniform-4194304 | pagerank | `grust-next@counted#1` | first | counted | 16 | 7268.495 | 229.656 | 0.032 | 454.281 | 10941.97 | 1365.16 | 1082129509 | 9 | yes |
| uniform-4194304 | pagerank | `grust-next@counted#1` | second | counted | 16 | 7227.700 | 115.876 | 0.016 | 451.731 | 10941.97 | 1365.16 | 1082129509 | 9 | yes |
| uniform-4194304 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 16 | 7031.976 | 142.724 | 0.020 | 439.499 | 7266.22 | 1315.71 | - | 9 | yes |
| uniform-4194304 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 16 | 6983.360 | 196.790 | 0.028 | 436.460 | 7266.22 | 1315.71 | - | 9 | yes |
| uniform-4194304 | pagerank | `grust-next@unchecked#1` | first | unchecked | 16 | 6828.027 | 232.253 | 0.034 | 426.752 | 7221.17 | 1354.05 | - | 9 | yes |
| uniform-4194304 | pagerank | `grust-next@unchecked#1` | second | unchecked | 16 | 6906.207 | 261.550 | 0.038 | 431.638 | 7221.17 | 1354.05 | - | 9 | yes |
| uniform-4194304 | pagerank | `grust-next@counted#unset` | first | counted | 16 | 12873.932 | 345.519 | 0.027 | 804.621 | 10942.47 | 1339.92 | 1233124379 | 9 | yes |
| uniform-4194304 | pagerank | `grust-next@counted#unset` | second | counted | 16 | 13142.198 | 105.129 | 0.008 | 821.387 | 10942.47 | 1339.92 | 1233124379 | 9 | yes |
| uniform-4194304 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 16 | 10783.822 | 317.824 | 0.029 | 673.989 | 7340.28 | 1345.39 | - | 9 | yes |
| uniform-4194304 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 16 | 10565.668 | 46.309 | 0.004 | 660.354 | 7340.28 | 1345.39 | - | 9 | yes |
| uniform-4194304 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 16 | 10736.381 | 588.456 | 0.055 | 671.024 | 7242.90 | 1372.56 | - | 9 | yes |
| uniform-4194304 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 16 | 10586.268 | 317.402 | 0.030 | 661.642 | 7242.90 | 1372.56 | - | 9 | yes |

### `xlarge-full-width.json`: xlarge-full-width

workers 16, concurrency 16, 1 warmup + 5 repeats, steal over the run 8 ticks, 1769.4 s, unusable at MAD/median >= 0.25

| fixture | algorithm | participant | call | accounting | iters | total ms | MAD | MAD/median | per iter | build ms | incoming ms | work units | steal | usable |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| hub-4194304 | pagerank | `neo4j-graph` |  |  | 15 | 342.472 | 39.572 | 0.116 | 22.831 | 918.07 | - | - | 4 | yes |
| hub-4194304 | pagerank | `icebug` |  |  | 10 | 1108.039 | 6.604 | 0.006 | 110.804 | 7018.11 | - | - | 4 | yes |
| hub-4194304 | pagerank | `icecat` |  |  | 16 | 5789.883 | 100.468 | 0.017 | 361.868 | 1183.82 | - | - | 4 | yes |
| hub-4194304 | pagerank | `grustcat` |  |  | 16 | 6041.858 | 14.586 | 0.002 | 377.616 | 42230.78 | - | - | 4 | yes |
| hub-4194304 | pagerank | `grust` | first | counted | 16 | 2778.108 | 4.193 | 0.002 | 173.632 | 7709.28 | - | 1081412859 | 4 | yes |
| hub-4194304 | pagerank | `grust` | second | counted | 16 | 1362.080 | 1.528 | 0.001 | 85.130 | 7709.28 | - | 1081412859 | 4 | yes |
| hub-4194304 | pagerank | `grust-next@counted` | first | counted | 16 | 730.845 | 3.546 | 0.005 | 45.678 | 10973.76 | 1404.36 | 1081412859 | 4 | yes |
| hub-4194304 | pagerank | `grust-next@counted` | second | counted | 16 | 731.328 | 16.296 | 0.022 | 45.708 | 10973.76 | 1404.36 | 1081412859 | 4 | yes |
| hub-4194304 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 16 | 698.166 | 18.592 | 0.027 | 43.635 | 7293.84 | 1344.76 | - | 4 | yes |
| hub-4194304 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 16 | 705.901 | 25.589 | 0.036 | 44.119 | 7293.84 | 1344.76 | - | 4 | yes |
| hub-4194304 | pagerank | `grust-next@unchecked` | first | unchecked | 16 | 695.379 | 15.318 | 0.022 | 43.461 | 7062.89 | 1325.68 | - | 4 | yes |
| hub-4194304 | pagerank | `grust-next@unchecked` | second | unchecked | 16 | 695.942 | 22.209 | 0.032 | 43.496 | 7062.89 | 1325.68 | - | 4 | yes |
| uniform-4194304 | pagerank | `neo4j-graph` |  |  | 29 | 620.222 | 22.724 | 0.037 | 21.387 | 918.44 | - | - | 4 | yes |
| uniform-4194304 | pagerank | `icebug` |  |  | 9 | 1072.436 | 10.246 | 0.010 | 119.160 | 6515.61 | - | - | 4 | yes |
| uniform-4194304 | pagerank | `icecat` |  |  | 16 | 5998.564 | 58.188 | 0.010 | 374.910 | 1195.45 | - | - | 4 | yes |
| uniform-4194304 | pagerank | `grustcat` |  |  | 16 | 7243.926 | 203.006 | 0.028 | 452.745 | 44153.61 | - | - | 4 | yes |
| uniform-4194304 | pagerank | `grust` | first | counted | 16 | 2870.004 | 25.636 | 0.009 | 179.375 | 7727.75 | - | 1082129509 | 4 | yes |
| uniform-4194304 | pagerank | `grust` | second | counted | 16 | 1458.504 | 2.956 | 0.002 | 91.157 | 7727.75 | - | 1082129509 | 4 | yes |
| uniform-4194304 | pagerank | `grust-next@counted` | first | counted | 16 | 757.055 | 6.563 | 0.009 | 47.316 | 11013.46 | 1357.58 | 1082129509 | 4 | yes |
| uniform-4194304 | pagerank | `grust-next@counted` | second | counted | 16 | 761.342 | 8.272 | 0.011 | 47.584 | 11013.46 | 1357.58 | 1082129509 | 4 | yes |
| uniform-4194304 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 16 | 733.257 | 11.328 | 0.015 | 45.829 | 7371.99 | 1305.07 | - | 4 | yes |
| uniform-4194304 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 16 | 722.042 | 16.644 | 0.023 | 45.128 | 7371.99 | 1305.07 | - | 4 | yes |
| uniform-4194304 | pagerank | `grust-next@unchecked` | first | unchecked | 16 | 723.807 | 13.014 | 0.018 | 45.238 | 7286.67 | 1359.36 | - | 4 | yes |
| uniform-4194304 | pagerank | `grust-next@unchecked` | second | unchecked | 16 | 718.002 | 4.933 | 0.007 | 44.875 | 7286.67 | 1359.36 | - | 4 | yes |

