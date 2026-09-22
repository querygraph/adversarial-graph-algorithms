### `one-thread.json`: one-thread

workers 1, concurrency 1, allocator glibc default, not pinned, 1 warmup + 5 repeats, steal over the run 1 ticks, 256.6 s, unusable at MAD/median >= 0.25

Not timed (no agreeing parity row): neo4j-graph pagerank layered-16384.edges, neo4j-graph pagerank layered-65536.edges, neo4j-graph pagerank path-16384.edges, neo4j-graph pagerank path-65536.edges 

| fixture | algorithm | participant | call | accounting | iters | total ms | MAD | MAD/median | per iter | build ms | incoming ms | prepare | minflt | minflt build | work units | steal | usable |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |
| hub-16384 | bfs | `icebug` |  |  | - | 1.671 | 0.102 | 0.061 | - | 9.59 | - |  | 57 | 1018 | - | 0 | yes |
| hub-16384 | bfs | `icecat` |  |  | - | 0.829 | 0.013 | 0.016 | - | 6.51 | - |  | 96 | 2065 | - | 0 | yes |
| hub-16384 | bfs | `grustcat` |  |  | - | 0.675 | 0.037 | 0.055 | - | 84.72 | - |  | 0 | 10314 | - | 0 | yes |
| hub-16384 | bfs | `grust#1` | first | counted | - | 1.562 | 0.004 | 0.003 | - | 18.74 | - | needed | 36 | 1788 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust#1` | second | counted | - | 1.442 | 0.004 | 0.003 | - | 18.74 | - | needed | 0 | 1788 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust#unset` | first | counted | - | 1.578 | 0.015 | 0.010 | - | 19.26 | - | needed | 36 | 1772 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust#unset` | second | counted | - | 1.440 | 0.002 | 0.001 | - | 19.26 | - | needed | 0 | 1772 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted#1` | first | counted | - | 1.587 | 0.015 | 0.010 | - | 10.76 | - | needed | 32 | 1739 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted#1` | second | counted | - | 1.464 | 0.003 | 0.002 | - | 10.76 | - | needed | 0 | 1739 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@work-uncounted#1` | first | work-uncounted | - | 1.025 | 0.039 | 0.038 | - | 9.15 | - | needed | 32 | 1739 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@work-uncounted#1` | second | work-uncounted | - | 0.869 | 0.012 | 0.014 | - | 9.15 | - | needed | 0 | 1739 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@unchecked#1` | first | unchecked | - | 0.852 | 0.005 | 0.006 | - | 8.18 | - | needed | 32 | 1228 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@unchecked#1` | second | unchecked | - | 0.724 | 0.006 | 0.008 | - | 8.18 | - | needed | 0 | 1228 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@counted#unset` | first | counted | - | 1.598 | 0.018 | 0.011 | - | 13.44 | - | needed | 36 | 1723 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted#unset` | second | counted | - | 1.472 | 0.003 | 0.002 | - | 13.44 | - | needed | 0 | 1723 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 1.081 | 0.073 | 0.067 | - | 9.54 | - | needed | 36 | 1723 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 0.863 | 0.008 | 0.009 | - | 9.54 | - | needed | 0 | 1723 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@unchecked#unset` | first | unchecked | - | 0.897 | 0.059 | 0.066 | - | 9.15 | - | needed | 36 | 1723 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@unchecked#unset` | second | unchecked | - | 0.737 | 0.007 | 0.010 | - | 9.15 | - | needed | 0 | 1723 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@counted+eager#1` | first | counted | - | 2.816 | 0.001 | 0.000 | - | 12.43 | 1.52 | always | 32 | 2027 | 1489517 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted+eager#1` | second | counted | - | 2.681 | 0.018 | 0.007 | - | 12.43 | 1.52 | always | 0 | 2027 | 1489517 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted+eager#unset` | first | counted | - | 1.613 | 0.007 | 0.004 | - | 14.91 | 1.87 | always | 64 | 1501 | 1489517 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted+eager#unset` | second | counted | - | 1.461 | 0.006 | 0.004 | - | 14.91 | 1.87 | always | 0 | 1501 | 1489517 | 0 | yes |
| hub-16384 | pagerank | `neo4j-graph` |  |  | 36 | 13.374 | 0.100 | 0.008 | 0.371 | 7.83 | - |  | 24 | 667 | - | 0 | yes |
| hub-16384 | pagerank | `icebug` |  |  | 12 | 7.741 | 0.047 | 0.006 | 0.645 | 9.70 | - |  | 107 | 1018 | - | 0 | yes |
| hub-16384 | pagerank | `icecat` |  |  | 17 | 8.549 | 0.040 | 0.005 | 0.503 | 6.74 | - |  | 130 | 2065 | - | 0 | yes |
| hub-16384 | pagerank | `grustcat` |  |  | 17 | 7.294 | 0.008 | 0.001 | 0.429 | 88.55 | - |  | 0 | 9803 | - | 0 | yes |
| hub-16384 | pagerank | `grust#1` | first | counted | 17 | 11.592 | 0.017 | 0.001 | 0.682 | 18.76 | - | needed | 384 | 2298 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust#1` | second | counted | 17 | 9.599 | 0.009 | 0.001 | 0.565 | 18.76 | - | needed | 0 | 2298 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust#unset` | first | counted | 17 | 50.688 | 0.025 | 0.000 | 2.982 | 19.92 | - | needed | 128 | 2283 | 4567562 | 0 | yes |
| hub-16384 | pagerank | `grust#unset` | second | counted | 17 | 50.578 | 0.033 | 0.001 | 2.975 | 19.92 | - | needed | 32 | 2283 | 4567562 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted#1` | first | counted | 17 | 8.201 | 0.020 | 0.002 | 0.482 | 11.41 | 1.48 | needed | 96 | 1516 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted#1` | second | counted | 17 | 7.972 | 0.005 | 0.001 | 0.469 | 11.41 | 1.48 | needed | 0 | 1516 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 17 | 7.680 | 0.017 | 0.002 | 0.452 | 9.64 | 1.35 | needed | 96 | 1516 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 17 | 7.473 | 0.023 | 0.003 | 0.440 | 9.64 | 1.35 | needed | 0 | 1516 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@unchecked#1` | first | unchecked | 17 | 7.462 | 0.009 | 0.001 | 0.439 | 10.04 | 1.31 | needed | 96 | 2027 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@unchecked#1` | second | unchecked | 17 | 7.258 | 0.009 | 0.001 | 0.427 | 10.04 | 1.31 | needed | 0 | 2027 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted#unset` | first | counted | 17 | 23.402 | 0.046 | 0.002 | 1.377 | 13.41 | - | needed | 128 | 1723 | 4567562 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted#unset` | second | counted | 17 | 23.179 | 0.048 | 0.002 | 1.363 | 13.41 | - | needed | 32 | 1723 | 4567562 | 0 | yes |
| hub-16384 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 17 | 14.153 | 0.010 | 0.001 | 0.833 | 8.89 | - | needed | 128 | 1212 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 17 | 13.944 | 0.020 | 0.001 | 0.820 | 8.89 | - | needed | 32 | 1212 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 17 | 13.667 | 0.019 | 0.001 | 0.804 | 8.47 | - | needed | 128 | 1213 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 17 | 13.438 | 0.014 | 0.001 | 0.790 | 8.47 | - | needed | 32 | 1213 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted+eager#1` | first | counted | 17 | 8.216 | 0.039 | 0.005 | 0.483 | 12.15 | 1.50 | always | 96 | 2026 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted+eager#1` | second | counted | 17 | 7.990 | 0.004 | 0.001 | 0.470 | 12.15 | 1.50 | always | 0 | 2026 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted+eager#unset` | first | counted | 17 | 23.412 | 0.075 | 0.003 | 1.377 | 15.39 | 1.87 | always | 128 | 1500 | 5009502 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted+eager#unset` | second | counted | 17 | 23.208 | 0.083 | 0.004 | 1.365 | 15.39 | 1.87 | always | 32 | 1500 | 5009502 | 0 | yes |
| hub-16384 | triangles | `neo4j-graph` |  |  | - | 8.083 | 0.044 | 0.005 | - | 7.91 | - |  | 3 | 667 | - | 0 | yes |
| hub-16384 | triangles | `grust#1` | first | counted | - | 17.808 | 0.048 | 0.003 | - | 23.12 | - | needed | 927 | 2810 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust#1` | second | counted | - | 15.730 | 0.030 | 0.002 | - | 23.12 | - | needed | 32 | 2810 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust#unset` | first | counted | - | 17.642 | 0.058 | 0.003 | - | 23.07 | - | needed | 927 | 2284 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust#unset` | second | counted | - | 15.693 | 0.024 | 0.002 | - | 23.07 | - | needed | 32 | 2284 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted#1` | first | counted | - | 16.708 | 0.064 | 0.004 | - | 13.24 | - | needed | 417 | 719 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted#1` | second | counted | - | 16.438 | 0.059 | 0.004 | - | 13.24 | - | needed | 511 | 719 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@work-uncounted#1` | first | work-uncounted | - | 16.475 | 0.063 | 0.004 | - | 11.81 | - | needed | 417 | 1230 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@work-uncounted#1` | second | work-uncounted | - | 16.134 | 0.042 | 0.003 | - | 11.81 | - | needed | 511 | 1230 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@unchecked#1` | first | unchecked | - | 16.311 | 0.018 | 0.001 | - | 11.36 | - | needed | 417 | 719 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@unchecked#1` | second | unchecked | - | 15.981 | 0.141 | 0.009 | - | 11.36 | - | needed | 511 | 719 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@counted#unset` | first | counted | - | 16.692 | 0.005 | 0.000 | - | 17.08 | - | needed | 417 | 703 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted#unset` | second | counted | - | 16.332 | 0.065 | 0.004 | - | 17.08 | - | needed | 543 | 703 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 16.440 | 0.027 | 0.002 | - | 12.82 | - | needed | 417 | 1214 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 16.065 | 0.018 | 0.001 | - | 12.82 | - | needed | 543 | 1214 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@unchecked#unset` | first | unchecked | - | 16.327 | 0.098 | 0.006 | - | 13.09 | - | needed | 417 | 1214 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@unchecked#unset` | second | unchecked | - | 15.899 | 0.013 | 0.001 | - | 13.09 | - | needed | 543 | 1214 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@counted+eager#1` | first | counted | - | 16.656 | 0.001 | 0.000 | - | 13.70 | 0.00 | always | 417 | 1230 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted+eager#1` | second | counted | - | 16.450 | 0.116 | 0.007 | - | 13.70 | 0.00 | always | 511 | 1230 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted+eager#unset` | first | counted | - | 16.610 | 0.078 | 0.005 | - | 17.42 | 0.00 | always | 417 | 1214 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted+eager#unset` | second | counted | - | 16.302 | 0.065 | 0.004 | - | 17.42 | 0.00 | always | 543 | 1214 | 3742208 | 0 | yes |
| hub-16384 | wcc | `neo4j-graph` |  |  | - | 1.021 | 0.009 | 0.008 | - | 7.90 | - |  | 0 | 666 | - | 0 | yes |
| hub-16384 | wcc | `icebug` |  |  | - | 2.403 | 0.057 | 0.024 | - | 9.59 | - |  | 68 | 1018 | - | 0 | yes |
| hub-16384 | wcc | `icecat` |  |  | - | 0.922 | 0.005 | 0.005 | - | 6.62 | - |  | 66 | 2066 | - | 0 | yes |
| hub-16384 | wcc | `grustcat` |  |  | - | 0.606 | 0.001 | 0.002 | - | 87.18 | - |  | 0 | 10314 | - | 0 | yes |
| hub-16384 | wcc | `grust#1` | first | counted | - | 1.563 | 0.008 | 0.005 | - | 18.81 | - | needed | 32 | 1787 | 1031191 | 0 | yes |
| hub-16384 | wcc | `grust#1` | second | counted | - | 1.713 | 0.008 | 0.004 | - | 18.81 | - | needed | 32 | 1787 | 1031191 | 0 | yes |
| hub-16384 | wcc | `grust#unset` | first | counted | - | 4.160 | 0.006 | 0.001 | - | 19.16 | - | needed | 32 | 1772 | 1324773 | 0 | yes |
| hub-16384 | wcc | `grust#unset` | second | counted | - | 4.148 | 0.002 | 0.000 | - | 19.16 | - | needed | 31 | 1772 | 1324773 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted#1` | first | counted | - | 1.505 | 0.002 | 0.001 | - | 10.19 | - | needed | 32 | 1228 | 1031191 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted#1` | second | counted | - | 1.461 | 0.010 | 0.007 | - | 10.19 | - | needed | 16 | 1228 | 1031191 | 0 | yes |
| hub-16384 | wcc | `grust-next@work-uncounted#1` | first | work-uncounted | - | 0.828 | 0.009 | 0.011 | - | 8.84 | - | needed | 32 | 1738 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@work-uncounted#1` | second | work-uncounted | - | 0.771 | 0.001 | 0.001 | - | 8.84 | - | needed | 16 | 1738 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@unchecked#1` | first | unchecked | - | 0.601 | 0.003 | 0.005 | - | 8.55 | - | needed | 32 | 1228 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@unchecked#1` | second | unchecked | - | 0.558 | 0.002 | 0.004 | - | 8.55 | - | needed | 16 | 1228 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@counted#unset` | first | counted | - | 4.110 | 0.006 | 0.001 | - | 13.55 | - | needed | 32 | 1723 | 1324773 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted#unset` | second | counted | - | 4.033 | 0.002 | 0.000 | - | 13.55 | - | needed | 0 | 1723 | 1324773 | 0 | yes |
| hub-16384 | wcc | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 1.521 | 0.004 | 0.003 | - | 9.49 | - | needed | 32 | 1723 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 1.450 | 0.008 | 0.006 | - | 9.49 | - | needed | 0 | 1723 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@unchecked#unset` | first | unchecked | - | 1.281 | 0.009 | 0.007 | - | 9.18 | - | needed | 32 | 1723 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@unchecked#unset` | second | unchecked | - | 1.205 | 0.009 | 0.007 | - | 9.18 | - | needed | 0 | 1723 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@counted+eager#1` | first | counted | - | 1.496 | 0.009 | 0.006 | - | 12.03 | 1.50 | always | 32 | 1517 | 1473131 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted+eager#1` | second | counted | - | 1.493 | 0.009 | 0.006 | - | 12.03 | 1.50 | always | 32 | 1517 | 1473131 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted+eager#unset` | first | counted | - | 4.102 | 0.004 | 0.001 | - | 15.26 | 1.86 | always | 32 | 2011 | 1766713 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted+eager#unset` | second | counted | - | 4.037 | 0.005 | 0.001 | - | 15.26 | 1.86 | always | 0 | 2011 | 1766713 | 0 | yes |
| hub-65536 | bfs | `icebug` |  |  | - | 15.428 | 0.366 | 0.024 | - | 67.46 | - |  | 217 | 4057 | - | 0 | yes |
| hub-65536 | bfs | `icecat` |  |  | - | 4.570 | 0.346 | 0.076 | - | 21.60 | - |  | 172 | 2383 | - | 0 | yes |
| hub-65536 | bfs | `grustcat` |  |  | - | 5.724 | 0.013 | 0.002 | - | 468.90 | - |  | 0 | 38231 | - | 0 | yes |
| hub-65536 | bfs | `grust#1` | first | counted | - | 7.735 | 0.138 | 0.018 | - | 106.46 | - | needed | 146 | 3612 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust#1` | second | counted | - | 5.900 | 0.114 | 0.019 | - | 106.46 | - | needed | 0 | 3612 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust#unset` | first | counted | - | 9.602 | 0.247 | 0.026 | - | 107.44 | - | needed | 144 | 3597 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust#unset` | second | counted | - | 7.366 | 0.261 | 0.035 | - | 107.44 | - | needed | 0 | 3597 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted#1` | first | counted | - | 7.580 | 0.386 | 0.051 | - | 43.98 | - | needed | 130 | 2905 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted#1` | second | counted | - | 6.196 | 0.193 | 0.031 | - | 43.98 | - | needed | 0 | 2905 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust-next@work-uncounted#1` | first | work-uncounted | - | 7.165 | 0.223 | 0.031 | - | 38.53 | - | needed | 130 | 3417 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@work-uncounted#1` | second | work-uncounted | - | 6.074 | 0.129 | 0.021 | - | 38.53 | - | needed | 0 | 3417 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@unchecked#1` | first | unchecked | - | 7.249 | 0.236 | 0.033 | - | 39.16 | - | needed | 130 | 3417 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@unchecked#1` | second | unchecked | - | 6.062 | 0.160 | 0.026 | - | 39.16 | - | needed | 0 | 3417 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@counted#unset` | first | counted | - | 10.640 | 0.582 | 0.055 | - | 54.36 | - | needed | 144 | 2842 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted#unset` | second | counted | - | 8.078 | 0.769 | 0.095 | - | 54.36 | - | needed | 0 | 2842 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 7.844 | 0.375 | 0.048 | - | 39.91 | - | needed | 144 | 2843 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 6.102 | 0.441 | 0.072 | - | 39.91 | - | needed | 0 | 2843 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@unchecked#unset` | first | unchecked | - | 6.701 | 0.368 | 0.055 | - | 38.13 | - | needed | 144 | 2842 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@unchecked#unset` | second | unchecked | - | 4.904 | 0.189 | 0.039 | - | 38.13 | - | needed | 0 | 2842 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@counted+eager#1` | first | counted | - | 7.746 | 0.178 | 0.023 | - | 51.90 | 7.14 | always | 194 | 4057 | 5959069 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted+eager#1` | second | counted | - | 6.146 | 0.158 | 0.026 | - | 51.90 | 7.14 | always | 0 | 4057 | 5959069 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted+eager#unset` | first | counted | - | 9.867 | 0.440 | 0.045 | - | 62.59 | 8.70 | always | 256 | 3482 | 5959069 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted+eager#unset` | second | counted | - | 7.868 | 0.254 | 0.032 | - | 62.59 | 8.70 | always | 0 | 3482 | 5959069 | 0 | yes |
| hub-65536 | pagerank | `neo4j-graph` |  |  | 28 | 37.647 | 0.126 | 0.003 | 1.345 | 54.25 | - |  | 72 | 2173 | - | 0 | yes |
| hub-65536 | pagerank | `icebug` |  |  | 12 | 73.658 | 4.050 | 0.055 | 6.138 | 69.71 | - |  | 400 | 4057 | - | 0 | yes |
| hub-65536 | pagerank | `icecat` |  |  | 17 | 35.023 | 0.042 | 0.001 | 2.060 | 21.92 | - |  | 607 | 2510 | - | 0 | yes |
| hub-65536 | pagerank | `grustcat` |  |  | 17 | 32.587 | 0.380 | 0.012 | 1.917 | 471.21 | - |  | 0 | 38231 | - | 0 | yes |
| hub-65536 | pagerank | `grust#1` | first | counted | 17 | 68.114 | 2.526 | 0.037 | 4.007 | 110.04 | - | needed | 1024 | 3101 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust#1` | second | counted | 17 | 57.383 | 1.849 | 0.032 | 3.375 | 110.04 | - | needed | 0 | 3101 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust#unset` | first | counted | 17 | 205.286 | 0.307 | 0.001 | 12.076 | 109.71 | - | needed | 512 | 3597 | 18272770 | 0 | yes |
| hub-65536 | pagerank | `grust#unset` | second | counted | 17 | 204.556 | 0.321 | 0.002 | 12.033 | 109.71 | - | needed | 128 | 3597 | 18272770 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted#1` | first | counted | 17 | 35.209 | 0.226 | 0.006 | 2.071 | 51.66 | 7.32 | needed | 384 | 3546 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted#1` | second | counted | 17 | 34.593 | 0.036 | 0.001 | 2.035 | 51.66 | 7.32 | needed | 0 | 3546 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 17 | 33.141 | 0.100 | 0.003 | 1.949 | 44.95 | 6.72 | needed | 384 | 4057 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 17 | 32.337 | 0.343 | 0.011 | 1.902 | 44.95 | 6.72 | needed | 0 | 4057 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@unchecked#1` | first | unchecked | 17 | 32.405 | 0.271 | 0.008 | 1.906 | 45.35 | 6.62 | needed | 384 | 4056 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@unchecked#1` | second | unchecked | 17 | 31.274 | 0.421 | 0.013 | 1.840 | 45.35 | 6.62 | needed | 0 | 4056 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted#unset` | first | counted | 17 | 96.403 | 0.390 | 0.004 | 5.671 | 54.40 | - | needed | 512 | 3353 | 18272770 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted#unset` | second | counted | 17 | 95.012 | 0.199 | 0.002 | 5.589 | 54.40 | - | needed | 128 | 3353 | 18272770 | 0 | yes |
| hub-65536 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 17 | 58.939 | 0.157 | 0.003 | 3.467 | 39.90 | - | needed | 512 | 2842 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 17 | 58.822 | 0.522 | 0.009 | 3.460 | 39.90 | - | needed | 128 | 2842 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 17 | 57.394 | 1.058 | 0.018 | 3.376 | 39.00 | - | needed | 512 | 3353 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 17 | 56.439 | 0.683 | 0.012 | 3.320 | 39.00 | - | needed | 128 | 3353 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted+eager#1` | first | counted | 17 | 35.199 | 0.481 | 0.014 | 2.071 | 50.98 | 7.06 | always | 384 | 3546 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted+eager#1` | second | counted | 17 | 34.188 | 0.185 | 0.005 | 2.011 | 50.98 | 7.06 | always | 0 | 3546 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted+eager#unset` | first | counted | 17 | 95.746 | 0.107 | 0.001 | 5.632 | 63.69 | 9.13 | always | 512 | 3482 | 20040830 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted+eager#unset` | second | counted | 17 | 96.477 | 1.353 | 0.014 | 5.675 | 63.69 | 9.13 | always | 128 | 3482 | 20040830 | 0 | yes |
| hub-65536 | triangles | `neo4j-graph` |  |  | - | 38.743 | 1.004 | 0.026 | - | 43.92 | - |  | 4 | 2173 | - | 0 | yes |
| hub-65536 | triangles | `grust#1` | first | counted | - | 82.111 | 1.464 | 0.018 | - | 137.70 | - | needed | 1665 | 3614 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust#1` | second | counted | - | 77.928 | 1.041 | 0.013 | - | 137.70 | - | needed | 128 | 3614 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust#unset` | first | counted | - | 80.152 | 0.400 | 0.005 | - | 133.77 | - | needed | 1665 | 3088 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust#unset` | second | counted | - | 76.042 | 0.805 | 0.011 | - | 133.77 | - | needed | 128 | 3088 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted#1` | first | counted | - | 78.079 | 2.249 | 0.029 | - | 59.57 | - | needed | 1666 | 2910 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted#1` | second | counted | - | 75.830 | 1.419 | 0.019 | - | 59.57 | - | needed | 1535 | 2910 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@work-uncounted#1` | first | work-uncounted | - | 78.748 | 2.607 | 0.033 | - | 52.87 | - | needed | 1666 | 2910 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@work-uncounted#1` | second | work-uncounted | - | 76.168 | 0.694 | 0.009 | - | 52.87 | - | needed | 1535 | 2910 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@unchecked#1` | first | unchecked | - | 78.219 | 1.211 | 0.015 | - | 52.54 | - | needed | 1666 | 3421 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@unchecked#1` | second | unchecked | - | 77.281 | 1.840 | 0.024 | - | 52.54 | - | needed | 1535 | 3421 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@counted#unset` | first | counted | - | 78.800 | 1.256 | 0.016 | - | 88.47 | - | needed | 1666 | 3357 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted#unset` | second | counted | - | 76.579 | 1.942 | 0.025 | - | 88.47 | - | needed | 641 | 3357 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 77.599 | 0.175 | 0.002 | - | 65.73 | - | needed | 1666 | 2846 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 74.602 | 1.005 | 0.013 | - | 65.73 | - | needed | 641 | 2846 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@unchecked#unset` | first | unchecked | - | 78.143 | 0.856 | 0.011 | - | 65.83 | - | needed | 1666 | 2846 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@unchecked#unset` | second | unchecked | - | 74.322 | 0.555 | 0.007 | - | 65.83 | - | needed | 641 | 2846 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@counted+eager#1` | first | counted | - | 80.321 | 0.039 | 0.000 | - | 58.52 | 0.00 | always | 1666 | 2910 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted+eager#1` | second | counted | - | 78.523 | 2.228 | 0.028 | - | 58.52 | 0.00 | always | 1535 | 2910 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted+eager#unset` | first | counted | - | 78.293 | 0.273 | 0.003 | - | 89.79 | 0.00 | always | 1666 | 3357 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted+eager#unset` | second | counted | - | 75.562 | 0.598 | 0.008 | - | 89.79 | 0.00 | always | 641 | 3357 | 14971727 | 0 | yes |
| hub-65536 | wcc | `neo4j-graph` |  |  | - | 3.817 | 0.006 | 0.002 | - | 53.08 | - |  | 32 | 2172 | - | 0 | yes |
| hub-65536 | wcc | `icebug` |  |  | - | 21.581 | 0.391 | 0.018 | - | 69.25 | - |  | 240 | 4057 | - | 0 | yes |
| hub-65536 | wcc | `icecat` |  |  | - | 3.302 | 0.012 | 0.004 | - | 22.29 | - |  | 1 | 2544 | - | 0 | yes |
| hub-65536 | wcc | `grustcat` |  |  | - | 2.518 | 0.027 | 0.011 | - | 474.16 | - |  | 0 | 38231 | - | 0 | yes |
| hub-65536 | wcc | `grust#1` | first | counted | - | 7.120 | 0.013 | 0.002 | - | 109.99 | - | needed | 128 | 3101 | 4125471 | 0 | yes |
| hub-65536 | wcc | `grust#1` | second | counted | - | 7.533 | 0.005 | 0.001 | - | 109.99 | - | needed | 127 | 3101 | 4125471 | 0 | yes |
| hub-65536 | wcc | `grust#unset` | first | counted | - | 17.192 | 0.008 | 0.000 | - | 107.62 | - | needed | 128 | 3087 | 5303155 | 0 | yes |
| hub-65536 | wcc | `grust#unset` | second | counted | - | 17.137 | 0.018 | 0.001 | - | 107.62 | - | needed | 126 | 3087 | 5303155 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted#1` | first | counted | - | 6.993 | 0.066 | 0.009 | - | 43.43 | - | needed | 128 | 2906 | 4125471 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted#1` | second | counted | - | 6.762 | 0.004 | 0.001 | - | 43.43 | - | needed | 64 | 2906 | 4125471 | 0 | yes |
| hub-65536 | wcc | `grust-next@work-uncounted#1` | first | work-uncounted | - | 5.028 | 0.041 | 0.008 | - | 37.02 | - | needed | 128 | 3417 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@work-uncounted#1` | second | work-uncounted | - | 4.869 | 0.023 | 0.005 | - | 37.02 | - | needed | 64 | 3417 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@unchecked#1` | first | unchecked | - | 4.641 | 0.032 | 0.007 | - | 37.33 | - | needed | 128 | 2906 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@unchecked#1` | second | unchecked | - | 4.417 | 0.033 | 0.008 | - | 37.33 | - | needed | 64 | 2906 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@counted#unset` | first | counted | - | 16.999 | 0.004 | 0.000 | - | 54.46 | - | needed | 128 | 2842 | 5303155 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted#unset` | second | counted | - | 16.798 | 0.032 | 0.002 | - | 54.46 | - | needed | 0 | 2842 | 5303155 | 0 | yes |
| hub-65536 | wcc | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 7.958 | 0.072 | 0.009 | - | 39.86 | - | needed | 128 | 2842 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 7.677 | 0.060 | 0.008 | - | 39.86 | - | needed | 0 | 2842 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@unchecked#unset` | first | unchecked | - | 6.832 | 0.090 | 0.013 | - | 38.80 | - | needed | 128 | 2842 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@unchecked#unset` | second | unchecked | - | 6.551 | 0.024 | 0.004 | - | 38.80 | - | needed | 0 | 2842 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@counted+eager#1` | first | counted | - | 6.961 | 0.008 | 0.001 | - | 51.25 | 7.32 | always | 128 | 3546 | 5893531 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted+eager#1` | second | counted | - | 6.980 | 0.004 | 0.001 | - | 51.25 | 7.32 | always | 127 | 3546 | 5893531 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted+eager#unset` | first | counted | - | 16.948 | 0.065 | 0.004 | - | 62.96 | 9.05 | always | 128 | 3482 | 7071215 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted+eager#unset` | second | counted | - | 16.701 | 0.055 | 0.003 | - | 62.96 | 9.05 | always | 0 | 3482 | 7071215 | 0 | yes |
| layered-16384 | bfs | `icebug` |  |  | - | 0.530 | 0.011 | 0.020 | - | 2.83 | - |  | 36 | 458 | - | 0 | yes |
| layered-16384 | bfs | `icecat` |  |  | - | 0.395 | 0.003 | 0.008 | - | 1.69 | - |  | 66 | 525 | - | 0 | yes |
| layered-16384 | bfs | `grustcat` |  |  | - | 0.253 | 0.001 | 0.002 | - | 32.92 | - |  | 0 | 7350 | - | 0 | yes |
| layered-16384 | bfs | `grust#1` | first | counted | - | 0.458 | 0.001 | 0.002 | - | 7.02 | - | needed | 30 | 1031 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust#1` | second | counted | - | 0.387 | 0.001 | 0.003 | - | 7.02 | - | needed | 0 | 1031 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust#unset` | first | counted | - | 0.460 | 0.004 | 0.009 | - | 7.07 | - | needed | 30 | 1016 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust#unset` | second | counted | - | 0.386 | 0.001 | 0.002 | - | 7.07 | - | needed | 0 | 1016 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted#1` | first | counted | - | 0.445 | 0.001 | 0.003 | - | 5.57 | - | needed | 26 | 904 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted#1` | second | counted | - | 0.381 | 0.001 | 0.002 | - | 5.57 | - | needed | 0 | 904 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@work-uncounted#1` | first | work-uncounted | - | 0.357 | 0.003 | 0.007 | - | 4.64 | - | needed | 26 | 904 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@work-uncounted#1` | second | work-uncounted | - | 0.290 | 0.001 | 0.004 | - | 4.64 | - | needed | 0 | 904 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@unchecked#1` | first | unchecked | - | 0.317 | 0.001 | 0.003 | - | 4.57 | - | needed | 26 | 904 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@unchecked#1` | second | unchecked | - | 0.250 | 0.001 | 0.002 | - | 4.57 | - | needed | 0 | 904 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@counted#unset` | first | counted | - | 0.451 | 0.001 | 0.003 | - | 6.11 | - | needed | 30 | 888 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted#unset` | second | counted | - | 0.381 | 0.001 | 0.003 | - | 6.11 | - | needed | 0 | 888 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 0.363 | 0.003 | 0.008 | - | 4.74 | - | needed | 30 | 888 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 0.287 | 0.001 | 0.005 | - | 4.74 | - | needed | 0 | 888 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@unchecked#unset` | first | unchecked | - | 0.332 | 0.007 | 0.022 | - | 4.64 | - | needed | 30 | 888 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@unchecked#unset` | second | unchecked | - | 0.249 | 0.002 | 0.007 | - | 4.64 | - | needed | 0 | 888 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@counted+eager#1` | first | counted | - | 0.510 | 0.001 | 0.002 | - | 5.99 | 0.55 | always | 26 | 1000 | 493703 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted+eager#1` | second | counted | - | 0.452 | 0.001 | 0.002 | - | 5.99 | 0.55 | always | 0 | 1000 | 493703 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted+eager#unset` | first | counted | - | 0.509 | 0.001 | 0.001 | - | 6.78 | 0.75 | always | 58 | 984 | 493703 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted+eager#unset` | second | counted | - | 0.382 | 0.001 | 0.002 | - | 6.78 | 0.75 | always | 0 | 984 | 493703 | 0 | yes |
| layered-16384 | pagerank | `icebug` |  |  | 69 | 26.420 | 0.050 | 0.002 | 0.383 | 2.81 | - |  | 113 | 458 | - | 0 | yes |
| layered-16384 | pagerank | `icecat` |  |  | 84 | 27.811 | 0.058 | 0.002 | 0.331 | 1.75 | - |  | 128 | 526 | - | 0 | yes |
| layered-16384 | pagerank | `grustcat` |  |  | 84 | 26.275 | 0.006 | 0.000 | 0.313 | 33.80 | - |  | 1 | 7350 | - | 0 | yes |
| layered-16384 | pagerank | `grust#1` | first | counted | 84 | 30.235 | 0.006 | 0.000 | 0.360 | 7.08 | - | needed | 192 | 1031 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust#1` | second | counted | 84 | 29.353 | 0.015 | 0.001 | 0.349 | 7.08 | - | needed | 0 | 1031 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust#unset` | first | counted | 84 | 115.732 | 0.053 | 0.000 | 1.378 | 7.02 | - | needed | 128 | 1016 | 8667337 | 0 | yes |
| layered-16384 | pagerank | `grust#unset` | second | counted | 84 | 115.942 | 0.502 | 0.004 | 1.380 | 7.02 | - | needed | 32 | 1016 | 8667337 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted#1` | first | counted | 84 | 30.860 | 0.025 | 0.001 | 0.367 | 6.04 | 0.55 | needed | 96 | 1000 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted#1` | second | counted | 84 | 30.648 | 0.009 | 0.000 | 0.365 | 6.04 | 0.55 | needed | 0 | 1000 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 84 | 28.558 | 0.013 | 0.000 | 0.340 | 5.05 | 0.38 | needed | 96 | 1000 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 84 | 28.309 | 0.026 | 0.001 | 0.337 | 5.05 | 0.38 | needed | 0 | 1000 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@unchecked#1` | first | unchecked | 84 | 27.882 | 0.045 | 0.002 | 0.332 | 4.94 | 0.36 | needed | 96 | 1000 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@unchecked#1` | second | unchecked | 84 | 27.735 | 0.007 | 0.000 | 0.330 | 4.94 | 0.36 | needed | 0 | 1000 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted#unset` | first | counted | 84 | 89.612 | 0.131 | 0.001 | 1.067 | 6.20 | - | needed | 128 | 888 | 8667337 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted#unset` | second | counted | 84 | 88.684 | 0.093 | 0.001 | 1.056 | 6.20 | - | needed | 32 | 888 | 8667337 | 0 | yes |
| layered-16384 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 84 | 44.954 | 0.360 | 0.008 | 0.535 | 4.74 | - | needed | 128 | 888 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 84 | 45.070 | 0.265 | 0.006 | 0.537 | 4.74 | - | needed | 32 | 888 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 84 | 42.032 | 0.043 | 0.001 | 0.500 | 4.65 | - | needed | 128 | 888 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 84 | 41.786 | 0.011 | 0.000 | 0.497 | 4.65 | - | needed | 32 | 888 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted+eager#1` | first | counted | 84 | 30.926 | 0.040 | 0.001 | 0.368 | 5.97 | 0.55 | always | 96 | 1000 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted+eager#1` | second | counted | 84 | 30.656 | 0.013 | 0.000 | 0.365 | 5.97 | 0.55 | always | 0 | 1000 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted+eager#unset` | first | counted | 84 | 88.910 | 0.034 | 0.000 | 1.058 | 6.90 | 0.76 | always | 128 | 984 | 8813732 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted+eager#unset` | second | counted | 84 | 88.660 | 0.026 | 0.000 | 1.055 | 6.90 | 0.76 | always | 32 | 984 | 8813732 | 0 | yes |
| layered-16384 | triangles | `neo4j-graph` |  |  | - | 0.823 | 0.007 | 0.009 | - | 2.24 | - |  | 3 | 408 | - | 0 | yes |
| layered-16384 | triangles | `grust#1` | first | counted | - | 2.915 | 0.016 | 0.006 | - | 7.46 | - | needed | 350 | 1158 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust#1` | second | counted | - | 2.213 | 0.008 | 0.004 | - | 7.46 | - | needed | 32 | 1158 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust#unset` | first | counted | - | 2.887 | 0.008 | 0.003 | - | 7.38 | - | needed | 350 | 1143 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust#unset` | second | counted | - | 2.221 | 0.004 | 0.002 | - | 7.38 | - | needed | 32 | 1143 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted#1` | first | counted | - | 2.819 | 0.010 | 0.003 | - | 5.90 | - | needed | 350 | 1032 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted#1` | second | counted | - | 2.589 | 0.005 | 0.002 | - | 5.90 | - | needed | 350 | 1032 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@work-uncounted#1` | first | work-uncounted | - | 2.688 | 0.022 | 0.008 | - | 4.99 | - | needed | 350 | 1032 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@work-uncounted#1` | second | work-uncounted | - | 2.450 | 0.006 | 0.002 | - | 4.99 | - | needed | 350 | 1032 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@unchecked#1` | first | unchecked | - | 2.575 | 0.003 | 0.001 | - | 4.96 | - | needed | 350 | 1032 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@unchecked#1` | second | unchecked | - | 2.355 | 0.009 | 0.004 | - | 4.96 | - | needed | 350 | 1032 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@counted#unset` | first | counted | - | 2.828 | 0.005 | 0.002 | - | 6.51 | - | needed | 350 | 1016 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted#unset` | second | counted | - | 2.320 | 0.009 | 0.004 | - | 6.51 | - | needed | 159 | 1016 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 2.696 | 0.034 | 0.013 | - | 5.18 | - | needed | 350 | 1016 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 2.170 | 0.002 | 0.001 | - | 5.18 | - | needed | 159 | 1016 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@unchecked#unset` | first | unchecked | - | 2.573 | 0.013 | 0.005 | - | 5.12 | - | needed | 350 | 1016 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@unchecked#unset` | second | unchecked | - | 2.067 | 0.006 | 0.003 | - | 5.12 | - | needed | 159 | 1016 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@counted+eager#1` | first | counted | - | 2.847 | 0.013 | 0.005 | - | 5.88 | 0.00 | always | 350 | 1032 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted+eager#1` | second | counted | - | 2.609 | 0.025 | 0.010 | - | 5.88 | 0.00 | always | 350 | 1032 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted+eager#unset` | first | counted | - | 2.811 | 0.007 | 0.002 | - | 6.51 | 0.00 | always | 350 | 1016 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted+eager#unset` | second | counted | - | 2.306 | 0.002 | 0.001 | - | 6.51 | 0.00 | always | 159 | 1016 | 718265 | 0 | yes |
| layered-16384 | wcc | `neo4j-graph` |  |  | - | 0.933 | 0.004 | 0.005 | - | 2.23 | - |  | 0 | 408 | - | 0 | yes |
| layered-16384 | wcc | `icebug` |  |  | - | 1.014 | 0.021 | 0.021 | - | 2.82 | - |  | 42 | 458 | - | 0 | yes |
| layered-16384 | wcc | `icecat` |  |  | - | 0.501 | 0.001 | 0.001 | - | 1.68 | - |  | 65 | 525 | - | 0 | yes |
| layered-16384 | wcc | `grustcat` |  |  | - | 0.354 | 0.001 | 0.002 | - | 33.01 | - |  | 0 | 7350 | - | 0 | yes |
| layered-16384 | wcc | `grust#1` | first | counted | - | 0.631 | 0.003 | 0.004 | - | 7.02 | - | needed | 32 | 1031 | 341578 | 0 | yes |
| layered-16384 | wcc | `grust#1` | second | counted | - | 0.652 | 0.003 | 0.004 | - | 7.02 | - | needed | 27 | 1031 | 341578 | 0 | yes |
| layered-16384 | wcc | `grust#unset` | first | counted | - | 1.445 | 0.006 | 0.004 | - | 6.97 | - | needed | 32 | 1016 | 438267 | 0 | yes |
| layered-16384 | wcc | `grust#unset` | second | counted | - | 1.433 | 0.010 | 0.007 | - | 6.97 | - | needed | 25 | 1016 | 438267 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted#1` | first | counted | - | 0.692 | 0.000 | 0.000 | - | 5.47 | - | needed | 32 | 904 | 341578 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted#1` | second | counted | - | 0.654 | 0.007 | 0.011 | - | 5.47 | - | needed | 15 | 904 | 341578 | 0 | yes |
| layered-16384 | wcc | `grust-next@work-uncounted#1` | first | work-uncounted | - | 0.580 | 0.001 | 0.002 | - | 4.62 | - | needed | 32 | 904 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@work-uncounted#1` | second | work-uncounted | - | 0.538 | 0.005 | 0.009 | - | 4.62 | - | needed | 15 | 904 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@unchecked#1` | first | unchecked | - | 0.516 | 0.003 | 0.007 | - | 4.58 | - | needed | 32 | 904 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@unchecked#1` | second | unchecked | - | 0.474 | 0.002 | 0.005 | - | 4.58 | - | needed | 14 | 904 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@counted#unset` | first | counted | - | 1.435 | 0.007 | 0.005 | - | 6.10 | - | needed | 32 | 888 | 438267 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted#unset` | second | counted | - | 1.374 | 0.016 | 0.012 | - | 6.10 | - | needed | 0 | 888 | 438267 | 0 | yes |
| layered-16384 | wcc | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 0.698 | 0.001 | 0.001 | - | 4.68 | - | needed | 32 | 888 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 0.631 | 0.002 | 0.003 | - | 4.68 | - | needed | 0 | 888 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@unchecked#unset` | first | unchecked | - | 0.635 | 0.001 | 0.001 | - | 4.64 | - | needed | 32 | 888 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@unchecked#unset` | second | unchecked | - | 0.571 | 0.008 | 0.014 | - | 4.64 | - | needed | 0 | 888 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@counted+eager#1` | first | counted | - | 0.686 | 0.001 | 0.001 | - | 5.96 | 0.56 | always | 32 | 1000 | 487973 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted+eager#1` | second | counted | - | 0.689 | 0.002 | 0.004 | - | 5.96 | 0.56 | always | 28 | 1000 | 487973 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted+eager#unset` | first | counted | - | 1.430 | 0.006 | 0.004 | - | 6.83 | 0.75 | always | 32 | 984 | 584662 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted+eager#unset` | second | counted | - | 1.368 | 0.007 | 0.005 | - | 6.83 | 0.75 | always | 0 | 984 | 584662 | 0 | yes |
| layered-65536 | bfs | `icebug` |  |  | - | 2.661 | 0.070 | 0.026 | - | 11.32 | - |  | 132 | 1832 | - | 0 | yes |
| layered-65536 | bfs | `icecat` |  |  | - | 1.643 | 0.031 | 0.019 | - | 6.73 | - |  | 258 | 1636 | - | 0 | yes |
| layered-65536 | bfs | `grustcat` |  |  | - | 1.049 | 0.018 | 0.017 | - | 138.62 | - |  | 0 | 26635 | - | 0 | yes |
| layered-65536 | bfs | `grust#1` | first | counted | - | 1.884 | 0.001 | 0.000 | - | 31.01 | - | needed | 119 | 3142 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust#1` | second | counted | - | 1.585 | 0.005 | 0.003 | - | 31.01 | - | needed | 0 | 3142 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust#unset` | first | counted | - | 1.875 | 0.003 | 0.002 | - | 32.45 | - | needed | 119 | 3127 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust#unset` | second | counted | - | 1.585 | 0.005 | 0.003 | - | 32.45 | - | needed | 0 | 3127 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted#1` | first | counted | - | 1.844 | 0.006 | 0.003 | - | 23.85 | - | needed | 103 | 2631 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted#1` | second | counted | - | 1.571 | 0.008 | 0.005 | - | 23.85 | - | needed | 0 | 2631 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@work-uncounted#1` | first | work-uncounted | - | 1.480 | 0.023 | 0.016 | - | 19.49 | - | needed | 103 | 2631 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@work-uncounted#1` | second | work-uncounted | - | 1.210 | 0.007 | 0.006 | - | 19.49 | - | needed | 0 | 2631 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@unchecked#1` | first | unchecked | - | 1.306 | 0.009 | 0.007 | - | 19.57 | - | needed | 103 | 2631 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@unchecked#1` | second | unchecked | - | 1.040 | 0.002 | 0.002 | - | 19.57 | - | needed | 0 | 2631 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@counted#unset` | first | counted | - | 1.884 | 0.025 | 0.013 | - | 26.57 | - | needed | 119 | 2567 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted#unset` | second | counted | - | 1.591 | 0.012 | 0.007 | - | 26.57 | - | needed | 0 | 2567 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 1.504 | 0.010 | 0.006 | - | 20.50 | - | needed | 119 | 2567 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 1.207 | 0.014 | 0.012 | - | 20.50 | - | needed | 0 | 2567 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@unchecked#unset` | first | unchecked | - | 1.337 | 0.006 | 0.004 | - | 20.81 | - | needed | 119 | 2567 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@unchecked#unset` | second | unchecked | - | 1.037 | 0.010 | 0.010 | - | 20.81 | - | needed | 0 | 2567 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@counted+eager#1` | first | counted | - | 2.102 | 0.005 | 0.002 | - | 25.31 | 2.22 | always | 103 | 3013 | 1979713 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted+eager#1` | second | counted | - | 1.872 | 0.013 | 0.007 | - | 25.31 | 2.22 | always | 0 | 3013 | 1979713 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted+eager#unset` | first | counted | - | 2.065 | 0.011 | 0.005 | - | 28.70 | 3.04 | always | 231 | 2949 | 1979713 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted+eager#unset` | second | counted | - | 1.584 | 0.014 | 0.009 | - | 28.70 | 3.04 | always | 0 | 2949 | 1979713 | 0 | yes |
| layered-65536 | pagerank | `icebug` |  |  | 60 | 95.350 | 0.776 | 0.008 | 1.589 | 11.34 | - |  | 401 | 1832 | - | 0 | yes |
| layered-65536 | pagerank | `icecat` |  |  | 75 | 102.289 | 0.055 | 0.001 | 1.364 | 7.07 | - |  | 608 | 2147 | - | 0 | yes |
| layered-65536 | pagerank | `grustcat` |  |  | 75 | 94.480 | 0.054 | 0.001 | 1.260 | 139.70 | - |  | 0 | 26634 | - | 0 | yes |
| layered-65536 | pagerank | `grust#1` | first | counted | 75 | 108.934 | 0.148 | 0.001 | 1.452 | 31.44 | - | needed | 766 | 3142 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust#1` | second | counted | 75 | 105.205 | 0.093 | 0.001 | 1.403 | 31.44 | - | needed | 0 | 3142 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust#unset` | first | counted | 75 | 415.654 | 0.733 | 0.002 | 5.542 | 32.03 | - | needed | 512 | 3127 | 31164642 | 0 | yes |
| layered-65536 | pagerank | `grust#unset` | second | counted | 75 | 414.616 | 0.047 | 0.000 | 5.528 | 32.03 | - | needed | 128 | 3127 | 31164642 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted#1` | first | counted | 75 | 112.296 | 0.197 | 0.002 | 1.497 | 26.47 | 2.26 | needed | 384 | 3013 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted#1` | second | counted | 75 | 110.905 | 0.141 | 0.001 | 1.479 | 26.47 | 2.26 | needed | 0 | 3013 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 75 | 102.999 | 0.161 | 0.002 | 1.373 | 21.16 | 1.60 | needed | 384 | 3013 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 75 | 102.344 | 0.237 | 0.002 | 1.365 | 21.16 | 1.60 | needed | 0 | 3013 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@unchecked#1` | first | unchecked | 75 | 101.230 | 0.432 | 0.004 | 1.350 | 20.89 | 1.49 | needed | 384 | 3013 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@unchecked#1` | second | unchecked | 75 | 100.331 | 0.217 | 0.002 | 1.338 | 20.89 | 1.49 | needed | 0 | 3013 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted#unset` | first | counted | 75 | 319.231 | 0.438 | 0.001 | 4.256 | 25.88 | - | needed | 512 | 2567 | 31164642 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted#unset` | second | counted | 75 | 318.236 | 0.192 | 0.001 | 4.243 | 25.88 | - | needed | 128 | 2567 | 31164642 | 0 | yes |
| layered-65536 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 75 | 159.286 | 0.153 | 0.001 | 2.124 | 19.79 | - | needed | 512 | 2567 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 75 | 158.385 | 0.150 | 0.001 | 2.112 | 19.79 | - | needed | 128 | 2567 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 75 | 151.953 | 0.471 | 0.003 | 2.026 | 19.91 | - | needed | 512 | 2567 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 75 | 150.949 | 0.464 | 0.003 | 2.013 | 19.91 | - | needed | 128 | 2567 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted+eager#1` | first | counted | 75 | 111.729 | 0.508 | 0.005 | 1.490 | 25.93 | 2.22 | always | 384 | 3013 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted+eager#1` | second | counted | 75 | 110.646 | 0.061 | 0.001 | 1.475 | 25.93 | 2.22 | always | 0 | 3013 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted+eager#unset` | first | counted | 75 | 319.678 | 0.109 | 0.000 | 4.262 | 30.17 | 3.07 | always | 512 | 3460 | 31750996 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted+eager#unset` | second | counted | 75 | 318.156 | 0.542 | 0.002 | 4.242 | 30.17 | 3.07 | always | 128 | 3460 | 31750996 | 0 | yes |
| layered-65536 | triangles | `neo4j-graph` |  |  | - | 2.838 | 0.017 | 0.006 | - | 8.52 | - |  | 4 | 1650 | - | 0 | yes |
| layered-65536 | triangles | `grust#1` | first | counted | - | 11.549 | 0.112 | 0.010 | - | 32.11 | - | needed | 1401 | 3140 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust#1` | second | counted | - | 8.985 | 0.050 | 0.006 | - | 32.11 | - | needed | 128 | 3140 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust#unset` | first | counted | - | 11.533 | 0.026 | 0.002 | - | 32.66 | - | needed | 1401 | 3635 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust#unset` | second | counted | - | 8.961 | 0.016 | 0.002 | - | 32.66 | - | needed | 128 | 3635 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted#1` | first | counted | - | 11.344 | 0.015 | 0.001 | - | 25.68 | - | needed | 1402 | 3140 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted#1` | second | counted | - | 11.022 | 0.307 | 0.028 | - | 25.68 | - | needed | 1497 | 3140 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@work-uncounted#1` | first | work-uncounted | - | 10.781 | 0.028 | 0.003 | - | 20.85 | - | needed | 1402 | 3139 | - | 0 | yes |
| layered-65536 | triangles | `grust-next@work-uncounted#1` | second | work-uncounted | - | 10.495 | 0.059 | 0.006 | - | 20.85 | - | needed | 1497 | 3139 | - | 0 | yes |
| layered-65536 | triangles | `grust-next@unchecked#1` | first | unchecked | - | 10.342 | 0.009 | 0.001 | - | 21.54 | - | needed | 1402 | 3140 | - | 0 | yes |
| layered-65536 | triangles | `grust-next@unchecked#1` | second | unchecked | - | 10.073 | 0.031 | 0.003 | - | 21.54 | - | needed | 1497 | 3140 | - | 0 | yes |
| layered-65536 | triangles | `grust-next@counted#unset` | first | counted | - | 11.357 | 0.041 | 0.004 | - | 27.69 | - | needed | 1402 | 3076 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted#unset` | second | counted | - | 10.261 | 0.139 | 0.014 | - | 27.69 | - | needed | 635 | 3076 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 10.787 | 0.034 | 0.003 | - | 22.14 | - | needed | 1402 | 3076 | - | 0 | yes |
| layered-65536 | triangles | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 9.017 | 0.075 | 0.008 | - | 22.14 | - | needed | 635 | 3076 | - | 0 | yes |
| layered-65536 | triangles | `grust-next@unchecked#unset` | first | unchecked | - | 10.390 | 0.004 | 0.000 | - | 22.10 | - | needed | 1402 | 3076 | - | 0 | yes |
| layered-65536 | triangles | `grust-next@unchecked#unset` | second | unchecked | - | 8.591 | 0.033 | 0.004 | - | 22.10 | - | needed | 635 | 3076 | - | 0 | yes |
| layered-65536 | triangles | `grust-next@counted+eager#1` | first | counted | - | 11.396 | 0.014 | 0.001 | - | 25.46 | 0.00 | always | 1402 | 3140 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted+eager#1` | second | counted | - | 11.296 | 0.306 | 0.027 | - | 25.46 | 0.00 | always | 1497 | 3140 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted+eager#unset` | first | counted | - | 11.314 | 0.024 | 0.002 | - | 27.78 | 0.00 | always | 1402 | 3076 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted+eager#unset` | second | counted | - | 9.623 | 0.066 | 0.007 | - | 27.78 | 0.00 | always | 635 | 3076 | 2877576 | 0 | yes |
| layered-65536 | wcc | `neo4j-graph` |  |  | - | 3.512 | 0.008 | 0.002 | - | 8.64 | - |  | 32 | 1650 | - | 0 | yes |
| layered-65536 | wcc | `icebug` |  |  | - | 4.733 | 0.014 | 0.003 | - | 11.38 | - |  | 138 | 1832 | - | 0 | yes |
| layered-65536 | wcc | `icecat` |  |  | - | 2.117 | 0.010 | 0.005 | - | 7.40 | - |  | 255 | 2146 | - | 0 | yes |
| layered-65536 | wcc | `grustcat` |  |  | - | 1.447 | 0.009 | 0.007 | - | 140.05 | - |  | 0 | 26634 | - | 0 | yes |
| layered-65536 | wcc | `grust#1` | first | counted | - | 2.562 | 0.014 | 0.005 | - | 33.15 | - | needed | 128 | 3142 | 1368146 | 0 | yes |
| layered-65536 | wcc | `grust#1` | second | counted | - | 2.687 | 0.019 | 0.007 | - | 33.15 | - | needed | 122 | 3142 | 1368146 | 0 | yes |
| layered-65536 | wcc | `grust#unset` | first | counted | - | 5.823 | 0.026 | 0.004 | - | 32.66 | - | needed | 128 | 3127 | 1755282 | 0 | yes |
| layered-65536 | wcc | `grust#unset` | second | counted | - | 5.785 | 0.005 | 0.001 | - | 32.66 | - | needed | 122 | 3127 | 1755282 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted#1` | first | counted | - | 2.812 | 0.008 | 0.003 | - | 24.40 | - | needed | 128 | 2631 | 1368146 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted#1` | second | counted | - | 2.654 | 0.010 | 0.004 | - | 24.40 | - | needed | 61 | 2631 | 1368146 | 0 | yes |
| layered-65536 | wcc | `grust-next@work-uncounted#1` | first | work-uncounted | - | 2.380 | 0.010 | 0.004 | - | 20.47 | - | needed | 128 | 2631 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@work-uncounted#1` | second | work-uncounted | - | 2.196 | 0.007 | 0.003 | - | 20.47 | - | needed | 60 | 2631 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@unchecked#1` | first | unchecked | - | 2.103 | 0.005 | 0.002 | - | 19.98 | - | needed | 128 | 2631 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@unchecked#1` | second | unchecked | - | 1.970 | 0.004 | 0.002 | - | 19.98 | - | needed | 61 | 2631 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@counted#unset` | first | counted | - | 5.777 | 0.007 | 0.001 | - | 26.64 | - | needed | 128 | 2567 | 1755282 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted#unset` | second | counted | - | 5.528 | 0.010 | 0.002 | - | 26.64 | - | needed | 0 | 2567 | 1755282 | 0 | yes |
| layered-65536 | wcc | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 2.834 | 0.004 | 0.001 | - | 21.37 | - | needed | 128 | 2567 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 2.604 | 0.028 | 0.011 | - | 21.37 | - | needed | 0 | 2567 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@unchecked#unset` | first | unchecked | - | 2.579 | 0.016 | 0.006 | - | 20.47 | - | needed | 128 | 2567 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@unchecked#unset` | second | unchecked | - | 2.315 | 0.011 | 0.005 | - | 20.47 | - | needed | 0 | 2567 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@counted+eager#1` | first | counted | - | 2.808 | 0.025 | 0.009 | - | 26.08 | 2.27 | always | 128 | 3013 | 1954500 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted+eager#1` | second | counted | - | 2.802 | 0.009 | 0.003 | - | 26.08 | 2.27 | always | 122 | 3013 | 1954500 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted+eager#unset` | first | counted | - | 5.761 | 0.008 | 0.001 | - | 28.24 | 3.02 | always | 128 | 2949 | 2341636 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted+eager#unset` | second | counted | - | 5.507 | 0.004 | 0.001 | - | 28.24 | 3.02 | always | 0 | 2949 | 2341636 | 0 | yes |
| path-16384 | bfs | `icebug` |  |  | - | 0.268 | 0.005 | 0.019 | - | 1.79 | - |  | 36 | 450 | - | 0 | yes |
| path-16384 | bfs | `icecat` |  |  | - | 0.290 | 0.003 | 0.011 | - | 0.91 | - |  | 65 | 275 | - | 0 | yes |
| path-16384 | bfs | `grustcat` |  |  | - | 0.143 | 0.000 | 0.002 | - | 26.89 | - |  | 0 | 6429 | - | 0 | yes |
| path-16384 | bfs | `grust#1` | first | counted | - | 0.426 | 0.008 | 0.018 | - | 5.21 | - | needed | 36 | 741 | 245755 | 0 | yes |
| path-16384 | bfs | `grust#1` | second | counted | - | 0.340 | 0.001 | 0.003 | - | 5.21 | - | needed | 0 | 741 | 245755 | 0 | yes |
| path-16384 | bfs | `grust#unset` | first | counted | - | 0.422 | 0.001 | 0.002 | - | 5.16 | - | needed | 36 | 726 | 245755 | 0 | yes |
| path-16384 | bfs | `grust#unset` | second | counted | - | 0.340 | 0.001 | 0.003 | - | 5.16 | - | needed | 0 | 726 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@counted#1` | first | counted | - | 0.396 | 0.002 | 0.005 | - | 4.44 | - | needed | 32 | 686 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@counted#1` | second | counted | - | 0.326 | 0.000 | 0.001 | - | 4.44 | - | needed | 0 | 686 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@work-uncounted#1` | first | work-uncounted | - | 0.221 | 0.000 | 0.001 | - | 3.77 | - | needed | 32 | 686 | - | 0 | yes |
| path-16384 | bfs | `grust-next@work-uncounted#1` | second | work-uncounted | - | 0.151 | 0.000 | 0.002 | - | 3.77 | - | needed | 0 | 686 | - | 0 | yes |
| path-16384 | bfs | `grust-next@unchecked#1` | first | unchecked | - | 0.189 | 0.002 | 0.010 | - | 3.78 | - | needed | 32 | 686 | - | 0 | yes |
| path-16384 | bfs | `grust-next@unchecked#1` | second | unchecked | - | 0.118 | 0.001 | 0.006 | - | 3.78 | - | needed | 0 | 686 | - | 0 | yes |
| path-16384 | bfs | `grust-next@counted#unset` | first | counted | - | 0.407 | 0.000 | 0.001 | - | 4.76 | - | needed | 36 | 670 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@counted#unset` | second | counted | - | 0.326 | 0.000 | 0.001 | - | 4.76 | - | needed | 0 | 670 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 0.231 | 0.001 | 0.002 | - | 3.85 | - | needed | 36 | 670 | - | 0 | yes |
| path-16384 | bfs | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 0.150 | 0.000 | 0.002 | - | 3.85 | - | needed | 0 | 670 | - | 0 | yes |
| path-16384 | bfs | `grust-next@unchecked#unset` | first | unchecked | - | 0.190 | 0.000 | 0.000 | - | 3.71 | - | needed | 36 | 670 | - | 0 | yes |
| path-16384 | bfs | `grust-next@unchecked#unset` | second | unchecked | - | 0.112 | 0.000 | 0.002 | - | 3.71 | - | needed | 0 | 670 | - | 0 | yes |
| path-16384 | bfs | `grust-next@counted+eager#1` | first | counted | - | 0.395 | 0.000 | 0.000 | - | 4.97 | 0.45 | always | 32 | 750 | 344057 | 0 | yes |
| path-16384 | bfs | `grust-next@counted+eager#1` | second | counted | - | 0.326 | 0.000 | 0.001 | - | 4.97 | 0.45 | always | 0 | 750 | 344057 | 0 | yes |
| path-16384 | bfs | `grust-next@counted+eager#unset` | first | counted | - | 0.464 | 0.000 | 0.001 | - | 5.43 | 0.63 | always | 64 | 734 | 344057 | 0 | yes |
| path-16384 | bfs | `grust-next@counted+eager#unset` | second | counted | - | 0.327 | 0.000 | 0.001 | - | 5.43 | 0.63 | always | 0 | 734 | 344057 | 0 | yes |
| path-16384 | pagerank | `icebug` |  |  | 54 | 12.851 | 0.058 | 0.004 | 0.238 | 1.79 | - |  | 113 | 450 | - | 0 | yes |
| path-16384 | pagerank | `icecat` |  |  | 58 | 11.382 | 0.202 | 0.018 | 0.196 | 0.94 | - |  | 128 | 275 | - | 0 | yes |
| path-16384 | pagerank | `grustcat` |  |  | 58 | 9.864 | 0.051 | 0.005 | 0.170 | 27.02 | - |  | 0 | 6429 | - | 0 | yes |
| path-16384 | pagerank | `grust#1` | first | counted | 58 | 15.510 | 0.026 | 0.002 | 0.267 | 5.18 | - | needed | 160 | 741 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust#1` | second | counted | 58 | 14.708 | 0.024 | 0.002 | 0.254 | 5.18 | - | needed | 0 | 741 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust#unset` | first | counted | 58 | 66.720 | 0.050 | 0.001 | 1.150 | 5.16 | - | needed | 128 | 726 | 5062591 | 0 | yes |
| path-16384 | pagerank | `grust#unset` | second | counted | 58 | 66.442 | 0.035 | 0.001 | 1.146 | 5.16 | - | needed | 32 | 726 | 5062591 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted#1` | first | counted | 58 | 14.764 | 0.024 | 0.002 | 0.255 | 5.02 | 0.45 | needed | 96 | 750 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted#1` | second | counted | 58 | 14.653 | 0.012 | 0.001 | 0.253 | 5.02 | 0.45 | needed | 64 | 750 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 58 | 12.130 | 0.022 | 0.002 | 0.209 | 4.12 | 0.28 | needed | 96 | 750 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 58 | 12.048 | 0.083 | 0.007 | 0.208 | 4.12 | 0.28 | needed | 64 | 750 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@unchecked#1` | first | unchecked | 58 | 11.508 | 0.002 | 0.000 | 0.198 | 4.02 | 0.26 | needed | 96 | 750 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@unchecked#1` | second | unchecked | 58 | 11.399 | 0.011 | 0.001 | 0.197 | 4.02 | 0.26 | needed | 64 | 750 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@counted#unset` | first | counted | 58 | 60.547 | 0.099 | 0.002 | 1.044 | 4.78 | - | needed | 128 | 670 | 5062591 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted#unset` | second | counted | 58 | 60.353 | 0.122 | 0.002 | 1.041 | 4.78 | - | needed | 32 | 670 | 5062591 | 0 | yes |
| path-16384 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 58 | 29.098 | 0.067 | 0.002 | 0.502 | 3.89 | - | needed | 128 | 670 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 58 | 28.938 | 0.104 | 0.004 | 0.499 | 3.89 | - | needed | 32 | 670 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 58 | 27.178 | 0.055 | 0.002 | 0.469 | 3.80 | - | needed | 128 | 670 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 58 | 27.062 | 0.076 | 0.003 | 0.467 | 3.80 | - | needed | 32 | 670 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@counted+eager#1` | first | counted | 58 | 14.753 | 0.017 | 0.001 | 0.254 | 4.90 | 0.44 | always | 96 | 750 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted+eager#1` | second | counted | 58 | 14.654 | 0.035 | 0.002 | 0.253 | 4.90 | 0.44 | always | 64 | 750 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted+eager#unset` | first | counted | 58 | 60.606 | 0.051 | 0.001 | 1.045 | 5.43 | 0.63 | always | 128 | 734 | 5160893 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted+eager#unset` | second | counted | 58 | 60.409 | 0.065 | 0.001 | 1.042 | 5.43 | 0.63 | always | 32 | 734 | 5160893 | 0 | yes |
| path-16384 | triangles | `neo4j-graph` |  |  | - | 0.275 | 0.007 | 0.024 | - | 1.48 | - |  | 4 | 316 | - | 0 | yes |
| path-16384 | triangles | `grust#1` | first | counted | - | 1.543 | 0.008 | 0.005 | - | 5.33 | - | needed | 256 | 805 | 425970 | 0 | yes |
| path-16384 | triangles | `grust#1` | second | counted | - | 1.093 | 0.005 | 0.004 | - | 5.33 | - | needed | 32 | 805 | 425970 | 0 | yes |
| path-16384 | triangles | `grust#unset` | first | counted | - | 1.562 | 0.014 | 0.009 | - | 5.31 | - | needed | 256 | 790 | 425970 | 0 | yes |
| path-16384 | triangles | `grust#unset` | second | counted | - | 1.261 | 0.020 | 0.016 | - | 5.31 | - | needed | 32 | 790 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted#1` | first | counted | - | 1.577 | 0.009 | 0.006 | - | 4.72 | - | needed | 256 | 750 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted#1` | second | counted | - | 1.424 | 0.011 | 0.008 | - | 4.72 | - | needed | 256 | 750 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@work-uncounted#1` | first | work-uncounted | - | 1.378 | 0.013 | 0.009 | - | 3.99 | - | needed | 256 | 750 | - | 0 | yes |
| path-16384 | triangles | `grust-next@work-uncounted#1` | second | work-uncounted | - | 1.201 | 0.006 | 0.005 | - | 3.99 | - | needed | 256 | 750 | - | 0 | yes |
| path-16384 | triangles | `grust-next@unchecked#1` | first | unchecked | - | 1.301 | 0.021 | 0.016 | - | 3.97 | - | needed | 256 | 750 | - | 0 | yes |
| path-16384 | triangles | `grust-next@unchecked#1` | second | unchecked | - | 1.136 | 0.020 | 0.018 | - | 3.97 | - | needed | 256 | 750 | - | 0 | yes |
| path-16384 | triangles | `grust-next@counted#unset` | first | counted | - | 1.577 | 0.006 | 0.004 | - | 5.03 | - | needed | 256 | 734 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted#unset` | second | counted | - | 1.200 | 0.020 | 0.016 | - | 5.03 | - | needed | 96 | 734 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 1.373 | 0.001 | 0.001 | - | 4.04 | - | needed | 256 | 734 | - | 0 | yes |
| path-16384 | triangles | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 0.971 | 0.007 | 0.007 | - | 4.04 | - | needed | 96 | 734 | - | 0 | yes |
| path-16384 | triangles | `grust-next@unchecked#unset` | first | unchecked | - | 1.313 | 0.017 | 0.013 | - | 3.96 | - | needed | 256 | 734 | - | 0 | yes |
| path-16384 | triangles | `grust-next@unchecked#unset` | second | unchecked | - | 0.917 | 0.005 | 0.006 | - | 3.96 | - | needed | 96 | 734 | - | 0 | yes |
| path-16384 | triangles | `grust-next@counted+eager#1` | first | counted | - | 1.573 | 0.002 | 0.001 | - | 4.68 | 0.00 | always | 256 | 750 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted+eager#1` | second | counted | - | 1.406 | 0.006 | 0.005 | - | 4.68 | 0.00 | always | 256 | 750 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted+eager#unset` | first | counted | - | 1.569 | 0.014 | 0.009 | - | 4.99 | 0.00 | always | 256 | 734 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted+eager#unset` | second | counted | - | 1.195 | 0.014 | 0.012 | - | 4.99 | 0.00 | always | 96 | 734 | 425970 | 0 | yes |
| path-16384 | wcc | `neo4j-graph` |  |  | - | 0.775 | 0.002 | 0.003 | - | 1.48 | - |  | 31 | 316 | - | 0 | yes |
| path-16384 | wcc | `icebug` |  |  | - | 0.352 | 0.008 | 0.022 | - | 1.79 | - |  | 42 | 450 | - | 0 | yes |
| path-16384 | wcc | `icecat` |  |  | - | 0.282 | 0.004 | 0.014 | - | 0.87 | - |  | 64 | 275 | - | 0 | yes |
| path-16384 | wcc | `grustcat` |  |  | - | 0.165 | 0.005 | 0.032 | - | 26.72 | - |  | 1 | 6429 | - | 0 | yes |
| path-16384 | wcc | `grust#1` | first | counted | - | 0.446 | 0.003 | 0.007 | - | 5.23 | - | needed | 32 | 741 | 229369 | 0 | yes |
| path-16384 | wcc | `grust#1` | second | counted | - | 0.448 | 0.002 | 0.004 | - | 5.23 | - | needed | 31 | 741 | 229369 | 0 | yes |
| path-16384 | wcc | `grust#unset` | first | counted | - | 1.001 | 0.005 | 0.005 | - | 5.19 | - | needed | 32 | 726 | 294903 | 0 | yes |
| path-16384 | wcc | `grust#unset` | second | counted | - | 1.001 | 0.006 | 0.006 | - | 5.19 | - | needed | 31 | 726 | 294903 | 0 | yes |
| path-16384 | wcc | `grust-next@counted#1` | first | counted | - | 0.449 | 0.002 | 0.004 | - | 4.43 | - | needed | 32 | 686 | 229369 | 0 | yes |
| path-16384 | wcc | `grust-next@counted#1` | second | counted | - | 0.410 | 0.003 | 0.008 | - | 4.43 | - | needed | 16 | 686 | 229369 | 0 | yes |
| path-16384 | wcc | `grust-next@work-uncounted#1` | first | work-uncounted | - | 0.317 | 0.002 | 0.008 | - | 3.73 | - | needed | 32 | 686 | - | 0 | yes |
| path-16384 | wcc | `grust-next@work-uncounted#1` | second | work-uncounted | - | 0.274 | 0.000 | 0.001 | - | 3.73 | - | needed | 16 | 686 | - | 0 | yes |
| path-16384 | wcc | `grust-next@unchecked#1` | first | unchecked | - | 0.306 | 0.002 | 0.008 | - | 3.77 | - | needed | 32 | 686 | - | 0 | yes |
| path-16384 | wcc | `grust-next@unchecked#1` | second | unchecked | - | 0.264 | 0.001 | 0.003 | - | 3.77 | - | needed | 16 | 686 | - | 0 | yes |
| path-16384 | wcc | `grust-next@counted#unset` | first | counted | - | 0.988 | 0.002 | 0.002 | - | 4.74 | - | needed | 32 | 670 | 294903 | 0 | yes |
| path-16384 | wcc | `grust-next@counted#unset` | second | counted | - | 0.946 | 0.003 | 0.003 | - | 4.74 | - | needed | 16 | 670 | 294903 | 0 | yes |
| path-16384 | wcc | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 0.386 | 0.015 | 0.039 | - | 3.81 | - | needed | 32 | 670 | - | 0 | yes |
| path-16384 | wcc | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 0.344 | 0.002 | 0.007 | - | 3.81 | - | needed | 16 | 670 | - | 0 | yes |
| path-16384 | wcc | `grust-next@unchecked#unset` | first | unchecked | - | 0.350 | 0.002 | 0.005 | - | 3.76 | - | needed | 32 | 670 | - | 0 | yes |
| path-16384 | wcc | `grust-next@unchecked#unset` | second | unchecked | - | 0.303 | 0.000 | 0.002 | - | 3.76 | - | needed | 16 | 670 | - | 0 | yes |
| path-16384 | wcc | `grust-next@counted+eager#1` | first | counted | - | 0.451 | 0.003 | 0.006 | - | 4.92 | 0.45 | always | 32 | 750 | 327671 | 0 | yes |
| path-16384 | wcc | `grust-next@counted+eager#1` | second | counted | - | 0.454 | 0.009 | 0.019 | - | 4.92 | 0.45 | always | 32 | 750 | 327671 | 0 | yes |
| path-16384 | wcc | `grust-next@counted+eager#unset` | first | counted | - | 0.990 | 0.003 | 0.003 | - | 5.39 | 0.63 | always | 32 | 734 | 393205 | 0 | yes |
| path-16384 | wcc | `grust-next@counted+eager#unset` | second | counted | - | 0.947 | 0.002 | 0.002 | - | 5.39 | 0.63 | always | 16 | 734 | 393205 | 0 | yes |
| path-65536 | bfs | `icebug` |  |  | - | 1.057 | 0.006 | 0.006 | - | 7.16 | - |  | 132 | 1795 | - | 0 | yes |
| path-65536 | bfs | `icecat` |  |  | - | 1.191 | 0.017 | 0.014 | - | 4.51 | - |  | 257 | 1139 | - | 0 | yes |
| path-65536 | bfs | `grustcat` |  |  | - | 0.589 | 0.003 | 0.004 | - | 115.01 | - |  | 0 | 24215 | - | 0 | yes |
| path-65536 | bfs | `grust#1` | first | counted | - | 1.688 | 0.008 | 0.005 | - | 23.51 | - | needed | 144 | 2486 | 983035 | 0 | yes |
| path-65536 | bfs | `grust#1` | second | counted | - | 1.375 | 0.009 | 0.006 | - | 23.51 | - | needed | 0 | 2486 | 983035 | 0 | yes |
| path-65536 | bfs | `grust#unset` | first | counted | - | 1.690 | 0.005 | 0.003 | - | 23.56 | - | needed | 144 | 2471 | 983035 | 0 | yes |
| path-65536 | bfs | `grust#unset` | second | counted | - | 1.372 | 0.010 | 0.008 | - | 23.56 | - | needed | 0 | 2471 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@counted#1` | first | counted | - | 1.597 | 0.005 | 0.003 | - | 19.68 | - | needed | 128 | 2263 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@counted#1` | second | counted | - | 1.320 | 0.004 | 0.003 | - | 19.68 | - | needed | 0 | 2263 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@work-uncounted#1` | first | work-uncounted | - | 0.887 | 0.005 | 0.005 | - | 17.05 | - | needed | 128 | 2263 | - | 0 | yes |
| path-65536 | bfs | `grust-next@work-uncounted#1` | second | work-uncounted | - | 0.604 | 0.000 | 0.001 | - | 17.05 | - | needed | 0 | 2263 | - | 0 | yes |
| path-65536 | bfs | `grust-next@unchecked#1` | first | unchecked | - | 0.757 | 0.006 | 0.008 | - | 17.57 | - | needed | 128 | 2263 | - | 0 | yes |
| path-65536 | bfs | `grust-next@unchecked#1` | second | unchecked | - | 0.470 | 0.003 | 0.006 | - | 17.57 | - | needed | 0 | 2263 | - | 0 | yes |
| path-65536 | bfs | `grust-next@counted#unset` | first | counted | - | 1.632 | 0.007 | 0.004 | - | 21.52 | - | needed | 144 | 2199 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@counted#unset` | second | counted | - | 1.313 | 0.008 | 0.006 | - | 21.52 | - | needed | 0 | 2199 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 0.930 | 0.003 | 0.003 | - | 17.13 | - | needed | 144 | 2199 | - | 0 | yes |
| path-65536 | bfs | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 0.601 | 0.001 | 0.002 | - | 17.13 | - | needed | 0 | 2199 | - | 0 | yes |
| path-65536 | bfs | `grust-next@unchecked#unset` | first | unchecked | - | 0.786 | 0.014 | 0.018 | - | 17.24 | - | needed | 144 | 2199 | - | 0 | yes |
| path-65536 | bfs | `grust-next@unchecked#unset` | second | unchecked | - | 0.455 | 0.000 | 0.001 | - | 17.24 | - | needed | 0 | 2199 | - | 0 | yes |
| path-65536 | bfs | `grust-next@counted+eager#1` | first | counted | - | 1.601 | 0.012 | 0.007 | - | 21.88 | 1.80 | always | 128 | 2519 | 1376249 | 0 | yes |
| path-65536 | bfs | `grust-next@counted+eager#1` | second | counted | - | 1.316 | 0.003 | 0.003 | - | 21.88 | 1.80 | always | 0 | 2519 | 1376249 | 0 | yes |
| path-65536 | bfs | `grust-next@counted+eager#unset` | first | counted | - | 1.865 | 0.004 | 0.002 | - | 24.59 | 2.53 | always | 256 | 2455 | 1376249 | 0 | yes |
| path-65536 | bfs | `grust-next@counted+eager#unset` | second | counted | - | 1.316 | 0.001 | 0.001 | - | 24.59 | 2.53 | always | 0 | 2455 | 1376249 | 0 | yes |
| path-65536 | pagerank | `icebug` |  |  | 46 | 43.713 | 0.245 | 0.006 | 0.950 | 7.15 | - |  | 401 | 1795 | - | 0 | yes |
| path-65536 | pagerank | `icecat` |  |  | 50 | 39.342 | 0.129 | 0.003 | 0.787 | 4.55 | - |  | 607 | 1139 | - | 0 | yes |
| path-65536 | pagerank | `grustcat` |  |  | 50 | 34.199 | 0.077 | 0.002 | 0.684 | 114.04 | - |  | 0 | 24215 | - | 0 | yes |
| path-65536 | pagerank | `grust#1` | first | counted | 50 | 54.481 | 0.002 | 0.000 | 1.090 | 23.16 | - | needed | 640 | 2486 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust#1` | second | counted | 50 | 51.140 | 0.123 | 0.002 | 1.023 | 23.16 | - | needed | 0 | 2486 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust#unset` | first | counted | 50 | 231.825 | 0.299 | 0.001 | 4.637 | 25.04 | - | needed | 512 | 2472 | 17629127 | 0 | yes |
| path-65536 | pagerank | `grust#unset` | second | counted | 50 | 230.717 | 0.186 | 0.001 | 4.614 | 25.04 | - | needed | 128 | 2472 | 17629127 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted#1` | first | counted | 50 | 52.841 | 0.439 | 0.008 | 1.057 | 20.87 | 1.81 | needed | 384 | 2519 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted#1` | second | counted | 50 | 52.039 | 0.065 | 0.001 | 1.041 | 20.87 | 1.81 | needed | 352 | 2519 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 50 | 42.967 | 0.140 | 0.003 | 0.859 | 19.57 | 1.14 | needed | 384 | 2519 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 50 | 42.708 | 0.193 | 0.005 | 0.854 | 19.57 | 1.14 | needed | 352 | 2519 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@unchecked#1` | first | unchecked | 50 | 40.858 | 0.033 | 0.001 | 0.817 | 18.92 | 1.06 | needed | 384 | 2519 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@unchecked#1` | second | unchecked | 50 | 40.564 | 0.046 | 0.001 | 0.811 | 18.92 | 1.06 | needed | 352 | 2519 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@counted#unset` | first | counted | 50 | 210.639 | 0.650 | 0.003 | 4.213 | 21.69 | - | needed | 512 | 2199 | 17629127 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted#unset` | second | counted | 50 | 209.711 | 0.462 | 0.002 | 4.194 | 21.69 | - | needed | 128 | 2199 | 17629127 | 0 | yes |
| path-65536 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 50 | 101.347 | 0.134 | 0.001 | 2.027 | 18.76 | - | needed | 512 | 2199 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 50 | 99.670 | 0.309 | 0.003 | 1.993 | 18.76 | - | needed | 128 | 2199 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 50 | 94.324 | 0.118 | 0.001 | 1.886 | 17.73 | - | needed | 512 | 2200 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 50 | 93.600 | 0.143 | 0.002 | 1.872 | 17.73 | - | needed | 128 | 2200 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@counted+eager#1` | first | counted | 50 | 52.200 | 0.064 | 0.001 | 1.044 | 22.30 | 1.80 | always | 384 | 2519 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted+eager#1` | second | counted | 50 | 51.896 | 0.052 | 0.001 | 1.038 | 22.30 | 1.80 | always | 352 | 2519 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted+eager#unset` | first | counted | 50 | 210.116 | 0.294 | 0.001 | 4.202 | 23.86 | 2.56 | always | 512 | 2455 | 18022341 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted+eager#unset` | second | counted | 50 | 209.868 | 0.252 | 0.001 | 4.197 | 23.86 | 2.56 | always | 128 | 2455 | 18022341 | 0 | yes |
| path-65536 | triangles | `neo4j-graph` |  |  | - | 0.697 | 0.007 | 0.010 | - | 5.38 | - |  | 3 | 1277 | - | 0 | yes |
| path-65536 | triangles | `grust#1` | first | counted | - | 6.226 | 0.067 | 0.011 | - | 24.51 | - | needed | 1024 | 2743 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust#1` | second | counted | - | 4.385 | 0.014 | 0.003 | - | 24.51 | - | needed | 128 | 2743 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust#unset` | first | counted | - | 6.235 | 0.026 | 0.004 | - | 24.55 | - | needed | 1025 | 2726 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust#unset` | second | counted | - | 5.100 | 0.003 | 0.001 | - | 24.55 | - | needed | 128 | 2726 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted#1` | first | counted | - | 6.339 | 0.029 | 0.005 | - | 20.95 | - | needed | 1024 | 2519 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted#1` | second | counted | - | 6.103 | 0.088 | 0.014 | - | 20.95 | - | needed | 1120 | 2519 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@work-uncounted#1` | first | work-uncounted | - | 5.459 | 0.018 | 0.003 | - | 18.77 | - | needed | 1024 | 2520 | - | 0 | yes |
| path-65536 | triangles | `grust-next@work-uncounted#1` | second | work-uncounted | - | 5.238 | 0.046 | 0.009 | - | 18.77 | - | needed | 1120 | 2520 | - | 0 | yes |
| path-65536 | triangles | `grust-next@unchecked#1` | first | unchecked | - | 5.197 | 0.029 | 0.006 | - | 18.85 | - | needed | 1024 | 3029 | - | 0 | yes |
| path-65536 | triangles | `grust-next@unchecked#1` | second | unchecked | - | 4.849 | 0.085 | 0.018 | - | 18.85 | - | needed | 1120 | 3029 | - | 0 | yes |
| path-65536 | triangles | `grust-next@counted#unset` | first | counted | - | 6.296 | 0.017 | 0.003 | - | 22.47 | - | needed | 1024 | 2455 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted#unset` | second | counted | - | 4.836 | 0.032 | 0.007 | - | 22.47 | - | needed | 384 | 2455 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 5.456 | 0.007 | 0.001 | - | 18.27 | - | needed | 1024 | 2455 | - | 0 | yes |
| path-65536 | triangles | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 3.997 | 0.023 | 0.006 | - | 18.27 | - | needed | 384 | 2455 | - | 0 | yes |
| path-65536 | triangles | `grust-next@unchecked#unset` | first | unchecked | - | 5.174 | 0.009 | 0.002 | - | 18.17 | - | needed | 1024 | 2455 | - | 0 | yes |
| path-65536 | triangles | `grust-next@unchecked#unset` | second | unchecked | - | 3.689 | 0.013 | 0.004 | - | 18.17 | - | needed | 384 | 2455 | - | 0 | yes |
| path-65536 | triangles | `grust-next@counted+eager#1` | first | counted | - | 6.291 | 0.011 | 0.002 | - | 22.47 | 0.00 | always | 1024 | 3030 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted+eager#1` | second | counted | - | 6.053 | 0.042 | 0.007 | - | 22.47 | 0.00 | always | 1120 | 3030 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted+eager#unset` | first | counted | - | 6.305 | 0.023 | 0.004 | - | 22.85 | 0.00 | always | 1024 | 2966 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted+eager#unset` | second | counted | - | 4.830 | 0.010 | 0.002 | - | 22.85 | 0.00 | always | 384 | 2966 | 1703922 | 0 | yes |
| path-65536 | wcc | `neo4j-graph` |  |  | - | 2.598 | 0.004 | 0.002 | - | 5.31 | - |  | 32 | 1276 | - | 0 | yes |
| path-65536 | wcc | `icebug` |  |  | - | 1.298 | 0.016 | 0.012 | - | 7.17 | - |  | 138 | 1795 | - | 0 | yes |
| path-65536 | wcc | `icecat` |  |  | - | 1.140 | 0.012 | 0.010 | - | 4.42 | - |  | 256 | 1139 | - | 0 | yes |
| path-65536 | wcc | `grustcat` |  |  | - | 0.635 | 0.002 | 0.003 | - | 113.25 | - |  | 0 | 24215 | - | 0 | yes |
| path-65536 | wcc | `grust#1` | first | counted | - | 1.796 | 0.002 | 0.001 | - | 23.10 | - | needed | 128 | 2486 | 917497 | 0 | yes |
| path-65536 | wcc | `grust#1` | second | counted | - | 1.815 | 0.003 | 0.002 | - | 23.10 | - | needed | 128 | 2486 | 917497 | 0 | yes |
| path-65536 | wcc | `grust#unset` | first | counted | - | 4.018 | 0.001 | 0.000 | - | 23.62 | - | needed | 128 | 2471 | 1179639 | 0 | yes |
| path-65536 | wcc | `grust#unset` | second | counted | - | 4.029 | 0.016 | 0.004 | - | 23.62 | - | needed | 126 | 2471 | 1179639 | 0 | yes |
| path-65536 | wcc | `grust-next@counted#1` | first | counted | - | 1.830 | 0.008 | 0.004 | - | 19.77 | - | needed | 128 | 2263 | 917497 | 0 | yes |
| path-65536 | wcc | `grust-next@counted#1` | second | counted | - | 1.683 | 0.018 | 0.011 | - | 19.77 | - | needed | 64 | 2263 | 917497 | 0 | yes |
| path-65536 | wcc | `grust-next@work-uncounted#1` | first | work-uncounted | - | 1.294 | 0.004 | 0.003 | - | 17.94 | - | needed | 128 | 2774 | - | 0 | yes |
| path-65536 | wcc | `grust-next@work-uncounted#1` | second | work-uncounted | - | 1.135 | 0.006 | 0.005 | - | 17.94 | - | needed | 64 | 2774 | - | 0 | yes |
| path-65536 | wcc | `grust-next@unchecked#1` | first | unchecked | - | 1.244 | 0.003 | 0.002 | - | 17.17 | - | needed | 128 | 2263 | - | 0 | yes |
| path-65536 | wcc | `grust-next@unchecked#1` | second | unchecked | - | 1.090 | 0.009 | 0.008 | - | 17.17 | - | needed | 64 | 2263 | - | 0 | yes |
| path-65536 | wcc | `grust-next@counted#unset` | first | counted | - | 4.010 | 0.002 | 0.000 | - | 22.19 | - | needed | 128 | 2200 | 1179639 | 0 | yes |
| path-65536 | wcc | `grust-next@counted#unset` | second | counted | - | 3.878 | 0.019 | 0.005 | - | 22.19 | - | needed | 64 | 2200 | 1179639 | 0 | yes |
| path-65536 | wcc | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 1.551 | 0.009 | 0.006 | - | 17.96 | - | needed | 128 | 2199 | - | 0 | yes |
| path-65536 | wcc | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 1.437 | 0.022 | 0.015 | - | 17.96 | - | needed | 64 | 2199 | - | 0 | yes |
| path-65536 | wcc | `grust-next@unchecked#unset` | first | unchecked | - | 1.390 | 0.007 | 0.005 | - | 17.48 | - | needed | 128 | 2199 | - | 0 | yes |
| path-65536 | wcc | `grust-next@unchecked#unset` | second | unchecked | - | 1.289 | 0.016 | 0.012 | - | 17.48 | - | needed | 64 | 2199 | - | 0 | yes |
| path-65536 | wcc | `grust-next@counted+eager#1` | first | counted | - | 1.813 | 0.008 | 0.005 | - | 22.17 | 1.84 | always | 128 | 2519 | 1310711 | 0 | yes |
| path-65536 | wcc | `grust-next@counted+eager#1` | second | counted | - | 1.806 | 0.009 | 0.005 | - | 22.17 | 1.84 | always | 128 | 2519 | 1310711 | 0 | yes |
| path-65536 | wcc | `grust-next@counted+eager#unset` | first | counted | - | 3.995 | 0.007 | 0.002 | - | 24.25 | 2.55 | always | 128 | 2455 | 1572853 | 0 | yes |
| path-65536 | wcc | `grust-next@counted+eager#unset` | second | counted | - | 3.873 | 0.017 | 0.004 | - | 24.25 | 2.55 | always | 64 | 2455 | 1572853 | 0 | yes |
| uniform-16384 | bfs | `icebug` |  |  | - | 2.123 | 0.075 | 0.035 | - | 9.83 | - |  | 57 | 979 | - | 0 | yes |
| uniform-16384 | bfs | `icecat` |  |  | - | 0.912 | 0.009 | 0.010 | - | 7.08 | - |  | 97 | 2068 | - | 0 | yes |
| uniform-16384 | bfs | `grustcat` |  |  | - | 0.793 | 0.062 | 0.078 | - | 88.30 | - |  | 0 | 10541 | - | 0 | yes |
| uniform-16384 | bfs | `grust#1` | first | counted | - | 1.634 | 0.023 | 0.014 | - | 19.48 | - | needed | 36 | 1790 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust#1` | second | counted | - | 1.460 | 0.003 | 0.002 | - | 19.48 | - | needed | 0 | 1790 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust#unset` | first | counted | - | 1.668 | 0.038 | 0.023 | - | 18.86 | - | needed | 36 | 1773 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust#unset` | second | counted | - | 1.467 | 0.002 | 0.001 | - | 18.86 | - | needed | 0 | 1773 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted#1` | first | counted | - | 1.663 | 0.034 | 0.020 | - | 10.15 | - | needed | 32 | 1230 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted#1` | second | counted | - | 1.486 | 0.016 | 0.010 | - | 10.15 | - | needed | 0 | 1230 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@work-uncounted#1` | first | work-uncounted | - | 1.114 | 0.040 | 0.036 | - | 8.35 | - | needed | 32 | 1230 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@work-uncounted#1` | second | work-uncounted | - | 0.897 | 0.011 | 0.012 | - | 8.35 | - | needed | 0 | 1230 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@unchecked#1` | first | unchecked | - | 1.015 | 0.015 | 0.015 | - | 8.33 | - | needed | 32 | 1230 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@unchecked#1` | second | unchecked | - | 0.814 | 0.008 | 0.010 | - | 8.33 | - | needed | 0 | 1230 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted#unset` | first | counted | - | 1.751 | 0.047 | 0.027 | - | 13.61 | - | needed | 36 | 1725 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted#unset` | second | counted | - | 1.488 | 0.002 | 0.001 | - | 13.61 | - | needed | 0 | 1725 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 1.169 | 0.049 | 0.042 | - | 9.51 | - | needed | 36 | 1725 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 0.884 | 0.002 | 0.002 | - | 9.51 | - | needed | 0 | 1725 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@unchecked#unset` | first | unchecked | - | 1.045 | 0.063 | 0.060 | - | 9.30 | - | needed | 36 | 1725 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@unchecked#unset` | second | unchecked | - | 0.789 | 0.007 | 0.009 | - | 9.30 | - | needed | 0 | 1725 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted+eager#1` | first | counted | - | 2.848 | 0.017 | 0.006 | - | 12.21 | 1.53 | always | 32 | 2029 | 1490619 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted+eager#1` | second | counted | - | 2.747 | 0.014 | 0.005 | - | 12.21 | 1.53 | always | 0 | 2029 | 1490619 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted+eager#unset` | first | counted | - | 1.692 | 0.022 | 0.013 | - | 15.46 | 1.85 | always | 64 | 2013 | 1490619 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted+eager#unset` | second | counted | - | 1.479 | 0.008 | 0.005 | - | 15.46 | 1.85 | always | 0 | 2013 | 1490619 | 0 | yes |
| uniform-16384 | pagerank | `neo4j-graph` |  |  | 28 | 10.542 | 0.021 | 0.002 | 0.377 | 8.07 | - |  | 24 | 668 | - | 0 | yes |
| uniform-16384 | pagerank | `icebug` |  |  | 12 | 8.165 | 0.014 | 0.002 | 0.680 | 9.63 | - |  | 111 | 979 | - | 0 | yes |
| uniform-16384 | pagerank | `icecat` |  |  | 16 | 8.116 | 0.014 | 0.002 | 0.507 | 7.19 | - |  | 129 | 2067 | - | 0 | yes |
| uniform-16384 | pagerank | `grustcat` |  |  | 16 | 6.834 | 0.014 | 0.002 | 0.427 | 87.45 | - |  | 0 | 10030 | - | 0 | yes |
| uniform-16384 | pagerank | `grust#1` | first | counted | 16 | 11.265 | 0.049 | 0.004 | 0.704 | 19.81 | - | needed | 384 | 2300 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust#1` | second | counted | 16 | 9.230 | 0.023 | 0.003 | 0.577 | 19.81 | - | needed | 0 | 2300 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust#unset` | first | counted | 16 | 48.027 | 0.034 | 0.001 | 3.002 | 20.81 | - | needed | 128 | 2285 | 4373785 | 0 | yes |
| uniform-16384 | pagerank | `grust#unset` | second | counted | 16 | 48.531 | 0.740 | 0.015 | 3.033 | 20.81 | - | needed | 32 | 2285 | 4373785 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted#1` | first | counted | 16 | 7.776 | 0.007 | 0.001 | 0.486 | 11.90 | 1.50 | needed | 96 | 1518 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted#1` | second | counted | 16 | 7.541 | 0.011 | 0.002 | 0.471 | 11.90 | 1.50 | needed | 0 | 1518 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 16 | 7.294 | 0.008 | 0.001 | 0.456 | 9.75 | 1.35 | needed | 96 | 1518 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 16 | 7.065 | 0.009 | 0.001 | 0.442 | 9.75 | 1.35 | needed | 0 | 1518 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@unchecked#1` | first | unchecked | 16 | 7.106 | 0.014 | 0.002 | 0.444 | 9.76 | 1.34 | needed | 96 | 1518 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@unchecked#1` | second | unchecked | 16 | 6.861 | 0.005 | 0.001 | 0.429 | 9.76 | 1.34 | needed | 0 | 1518 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted#unset` | first | counted | 16 | 21.844 | 0.113 | 0.005 | 1.365 | 13.28 | - | needed | 128 | 1215 | 4373785 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted#unset` | second | counted | 16 | 21.660 | 0.107 | 0.005 | 1.354 | 13.28 | - | needed | 32 | 1215 | 4373785 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 16 | 13.278 | 0.035 | 0.003 | 0.830 | 9.62 | - | needed | 128 | 1725 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 16 | 13.083 | 0.017 | 0.001 | 0.818 | 9.62 | - | needed | 32 | 1725 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 16 | 12.792 | 0.002 | 0.000 | 0.799 | 8.75 | - | needed | 128 | 1214 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 16 | 12.612 | 0.029 | 0.002 | 0.788 | 8.75 | - | needed | 32 | 1214 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted+eager#1` | first | counted | 16 | 7.779 | 0.017 | 0.002 | 0.486 | 12.07 | 1.49 | always | 96 | 1518 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted+eager#1` | second | counted | 16 | 7.544 | 0.010 | 0.001 | 0.472 | 12.07 | 1.49 | always | 0 | 1518 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted+eager#unset` | first | counted | 16 | 21.726 | 0.027 | 0.001 | 1.358 | 14.83 | 1.86 | always | 128 | 1502 | 4816061 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted+eager#unset` | second | counted | 16 | 21.565 | 0.028 | 0.001 | 1.348 | 14.83 | 1.86 | always | 32 | 1502 | 4816061 | 0 | yes |
| uniform-16384 | triangles | `neo4j-graph` |  |  | - | 9.106 | 0.016 | 0.002 | - | 8.05 | - |  | 3 | 668 | - | 1 | yes |
| uniform-16384 | triangles | `grust#1` | first | counted | - | 19.194 | 0.128 | 0.007 | - | 24.02 | - | needed | 928 | 2300 | 3829630 | 1 | yes |
| uniform-16384 | triangles | `grust#1` | second | counted | - | 17.186 | 0.053 | 0.003 | - | 24.02 | - | needed | 32 | 2300 | 3829630 | 1 | yes |
| uniform-16384 | triangles | `grust#unset` | first | counted | - | 19.235 | 0.104 | 0.005 | - | 25.09 | - | needed | 928 | 2796 | 3829630 | 1 | yes |
| uniform-16384 | triangles | `grust#unset` | second | counted | - | 17.166 | 0.016 | 0.001 | - | 25.09 | - | needed | 32 | 2796 | 3829630 | 1 | yes |
| uniform-16384 | triangles | `grust-next@counted#1` | first | counted | - | 18.127 | 0.003 | 0.000 | - | 13.11 | - | needed | 417 | 720 | 3829630 | 1 | yes |
| uniform-16384 | triangles | `grust-next@counted#1` | second | counted | - | 17.819 | 0.129 | 0.007 | - | 13.11 | - | needed | 512 | 720 | 3829630 | 1 | yes |
| uniform-16384 | triangles | `grust-next@work-uncounted#1` | first | work-uncounted | - | 17.774 | 0.027 | 0.002 | - | 11.53 | - | needed | 417 | 1231 | - | 1 | yes |
| uniform-16384 | triangles | `grust-next@work-uncounted#1` | second | work-uncounted | - | 17.522 | 0.092 | 0.005 | - | 11.53 | - | needed | 512 | 1231 | - | 1 | yes |
| uniform-16384 | triangles | `grust-next@unchecked#1` | first | unchecked | - | 18.213 | 0.133 | 0.007 | - | 10.86 | - | needed | 417 | 720 | - | 1 | yes |
| uniform-16384 | triangles | `grust-next@unchecked#1` | second | unchecked | - | 17.354 | 0.057 | 0.003 | - | 10.86 | - | needed | 512 | 720 | - | 1 | yes |
| uniform-16384 | triangles | `grust-next@counted#unset` | first | counted | - | 18.100 | 0.119 | 0.007 | - | 16.49 | - | needed | 417 | 704 | 3829630 | 1 | yes |
| uniform-16384 | triangles | `grust-next@counted#unset` | second | counted | - | 17.818 | 0.036 | 0.002 | - | 16.49 | - | needed | 544 | 704 | 3829630 | 1 | yes |
| uniform-16384 | triangles | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 17.818 | 0.094 | 0.005 | - | 12.63 | - | needed | 417 | 1215 | - | 1 | yes |
| uniform-16384 | triangles | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 17.507 | 0.049 | 0.003 | - | 12.63 | - | needed | 544 | 1215 | - | 1 | yes |
| uniform-16384 | triangles | `grust-next@unchecked#unset` | first | unchecked | - | 17.699 | 0.073 | 0.004 | - | 12.20 | - | needed | 417 | 1215 | - | 1 | yes |
| uniform-16384 | triangles | `grust-next@unchecked#unset` | second | unchecked | - | 17.409 | 0.091 | 0.005 | - | 12.20 | - | needed | 544 | 1215 | - | 1 | yes |
| uniform-16384 | triangles | `grust-next@counted+eager#1` | first | counted | - | 18.078 | 0.038 | 0.002 | - | 12.90 | 0.00 | always | 417 | 720 | 3829630 | 1 | yes |
| uniform-16384 | triangles | `grust-next@counted+eager#1` | second | counted | - | 17.789 | 0.007 | 0.000 | - | 12.90 | 0.00 | always | 512 | 720 | 3829630 | 1 | yes |
| uniform-16384 | triangles | `grust-next@counted+eager#unset` | first | counted | - | 18.070 | 0.031 | 0.002 | - | 17.12 | 0.00 | always | 417 | 704 | 3829630 | 1 | yes |
| uniform-16384 | triangles | `grust-next@counted+eager#unset` | second | counted | - | 17.921 | 0.206 | 0.011 | - | 17.12 | 0.00 | always | 544 | 704 | 3829630 | 1 | yes |
| uniform-16384 | wcc | `neo4j-graph` |  |  | - | 1.039 | 0.008 | 0.007 | - | 7.96 | - |  | 1 | 667 | - | 0 | yes |
| uniform-16384 | wcc | `icebug` |  |  | - | 3.153 | 0.151 | 0.048 | - | 9.91 | - |  | 69 | 979 | - | 0 | yes |
| uniform-16384 | wcc | `icecat` |  |  | - | 1.092 | 0.005 | 0.004 | - | 6.95 | - |  | 64 | 1557 | - | 0 | yes |
| uniform-16384 | wcc | `grustcat` |  |  | - | 0.766 | 0.007 | 0.008 | - | 90.44 | - |  | 0 | 10541 | - | 0 | yes |
| uniform-16384 | wcc | `grust#1` | first | counted | - | 2.065 | 0.008 | 0.004 | - | 19.79 | - | needed | 32 | 2300 | 1031975 | 0 | yes |
| uniform-16384 | wcc | `grust#1` | second | counted | - | 2.286 | 0.003 | 0.001 | - | 19.79 | - | needed | 31 | 2300 | 1031975 | 0 | yes |
| uniform-16384 | wcc | `grust#unset` | first | counted | - | 4.175 | 0.010 | 0.002 | - | 19.67 | - | needed | 32 | 1774 | 1324427 | 0 | yes |
| uniform-16384 | wcc | `grust#unset` | second | counted | - | 4.173 | 0.016 | 0.004 | - | 19.67 | - | needed | 31 | 1774 | 1324427 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted#1` | first | counted | - | 2.347 | 0.009 | 0.004 | - | 10.96 | - | needed | 32 | 1741 | 1031975 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted#1` | second | counted | - | 2.302 | 0.005 | 0.002 | - | 10.96 | - | needed | 16 | 1741 | 1031975 | 0 | yes |
| uniform-16384 | wcc | `grust-next@work-uncounted#1` | first | work-uncounted | - | 2.060 | 0.030 | 0.015 | - | 8.91 | - | needed | 32 | 1230 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@work-uncounted#1` | second | work-uncounted | - | 2.009 | 0.001 | 0.000 | - | 8.91 | - | needed | 16 | 1230 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@unchecked#1` | first | unchecked | - | 1.886 | 0.000 | 0.000 | - | 9.09 | - | needed | 32 | 1741 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@unchecked#1` | second | unchecked | - | 1.862 | 0.004 | 0.002 | - | 9.09 | - | needed | 16 | 1741 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted#unset` | first | counted | - | 4.266 | 0.010 | 0.002 | - | 13.13 | - | needed | 32 | 1214 | 1324427 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted#unset` | second | counted | - | 4.184 | 0.005 | 0.001 | - | 13.13 | - | needed | 0 | 1214 | 1324427 | 0 | yes |
| uniform-16384 | wcc | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 1.693 | 0.009 | 0.006 | - | 9.69 | - | needed | 32 | 1725 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 1.637 | 0.012 | 0.007 | - | 9.69 | - | needed | 0 | 1725 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@unchecked#unset` | first | unchecked | - | 1.440 | 0.009 | 0.006 | - | 9.47 | - | needed | 32 | 1725 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@unchecked#unset` | second | unchecked | - | 1.386 | 0.022 | 0.016 | - | 9.47 | - | needed | 0 | 1725 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted+eager#1` | first | counted | - | 2.345 | 0.009 | 0.004 | - | 11.90 | 1.53 | always | 32 | 1518 | 1474251 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted+eager#1` | second | counted | - | 2.348 | 0.005 | 0.002 | - | 11.90 | 1.53 | always | 32 | 1518 | 1474251 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted+eager#unset` | first | counted | - | 4.935 | 0.013 | 0.003 | - | 14.94 | 1.89 | always | 32 | 1502 | 1766703 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted+eager#unset` | second | counted | - | 4.849 | 0.006 | 0.001 | - | 14.94 | 1.89 | always | 0 | 1502 | 1766703 | 0 | yes |
| uniform-65536 | bfs | `icebug` |  |  | - | 15.918 | 0.081 | 0.005 | - | 63.64 | - |  | 216 | 3889 | - | 0 | yes |
| uniform-65536 | bfs | `icecat` |  |  | - | 4.895 | 0.486 | 0.099 | - | 20.87 | - |  | 194 | 1488 | - | 0 | yes |
| uniform-65536 | bfs | `grustcat` |  |  | - | 5.892 | 0.055 | 0.009 | - | 465.61 | - |  | 0 | 37598 | - | 0 | yes |
| uniform-65536 | bfs | `grust#1` | first | counted | - | 8.602 | 0.170 | 0.020 | - | 106.96 | - | needed | 209 | 2596 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust#1` | second | counted | - | 6.633 | 0.193 | 0.029 | - | 106.96 | - | needed | 0 | 2596 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust#unset` | first | counted | - | 9.721 | 0.304 | 0.031 | - | 107.88 | - | needed | 144 | 3091 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust#unset` | second | counted | - | 7.586 | 0.484 | 0.064 | - | 107.88 | - | needed | 0 | 3091 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted#1` | first | counted | - | 8.276 | 0.545 | 0.066 | - | 43.56 | - | needed | 134 | 2912 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted#1` | second | counted | - | 7.176 | 0.265 | 0.037 | - | 43.56 | - | needed | 0 | 2912 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@work-uncounted#1` | first | work-uncounted | - | 7.616 | 0.062 | 0.008 | - | 37.52 | - | needed | 134 | 2912 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@work-uncounted#1` | second | work-uncounted | - | 6.138 | 0.224 | 0.036 | - | 37.52 | - | needed | 0 | 2912 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@unchecked#1` | first | unchecked | - | 7.530 | 0.509 | 0.068 | - | 35.97 | - | needed | 134 | 2402 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@unchecked#1` | second | unchecked | - | 5.936 | 0.050 | 0.008 | - | 35.97 | - | needed | 0 | 2402 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted#unset` | first | counted | - | 10.316 | 0.192 | 0.019 | - | 53.55 | - | needed | 144 | 2338 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted#unset` | second | counted | - | 8.055 | 0.422 | 0.052 | - | 53.55 | - | needed | 0 | 2338 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 7.712 | 0.161 | 0.021 | - | 38.67 | - | needed | 144 | 2337 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 5.774 | 0.096 | 0.017 | - | 38.67 | - | needed | 0 | 2337 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@unchecked#unset` | first | unchecked | - | 6.961 | 0.680 | 0.098 | - | 37.40 | - | needed | 144 | 2337 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@unchecked#unset` | second | unchecked | - | 5.431 | 0.549 | 0.101 | - | 37.40 | - | needed | 0 | 2337 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted+eager#1` | first | counted | - | 8.096 | 0.447 | 0.055 | - | 50.72 | 6.99 | always | 198 | 3042 | 5963146 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted+eager#1` | second | counted | - | 6.395 | 0.367 | 0.057 | - | 50.72 | 6.99 | always | 0 | 3042 | 5963146 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted+eager#unset` | first | counted | - | 10.864 | 0.283 | 0.026 | - | 62.74 | 8.91 | always | 256 | 2978 | 5963146 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted+eager#unset` | second | counted | - | 8.292 | 0.524 | 0.063 | - | 62.74 | 8.91 | always | 0 | 2978 | 5963146 | 0 | yes |
| uniform-65536 | pagerank | `neo4j-graph` |  |  | 34 | 45.657 | 0.310 | 0.007 | 1.343 | 46.73 | - |  | 71 | 1665 | - | 0 | yes |
| uniform-65536 | pagerank | `icebug` |  |  | 11 | 63.379 | 5.235 | 0.083 | 5.762 | 59.24 | - |  | 398 | 3889 | - | 0 | yes |
| uniform-65536 | pagerank | `icecat` |  |  | 16 | 33.537 | 0.613 | 0.018 | 2.096 | 21.43 | - |  | 606 | 1665 | - | 0 | yes |
| uniform-65536 | pagerank | `grustcat` |  |  | 16 | 30.884 | 0.279 | 0.009 | 1.930 | 471.34 | - |  | 0 | 37598 | - | 0 | yes |
| uniform-65536 | pagerank | `grust#1` | first | counted | 16 | 60.816 | 3.601 | 0.059 | 3.801 | 106.46 | - | needed | 1025 | 3108 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust#1` | second | counted | 16 | 48.701 | 3.011 | 0.062 | 3.044 | 106.46 | - | needed | 0 | 3108 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust#unset` | first | counted | 16 | 194.710 | 0.521 | 0.003 | 12.169 | 106.26 | - | needed | 512 | 3092 | 17497177 | 0 | yes |
| uniform-65536 | pagerank | `grust#unset` | second | counted | 16 | 194.226 | 0.498 | 0.003 | 12.139 | 106.26 | - | needed | 128 | 3092 | 17497177 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted#1` | first | counted | 16 | 32.857 | 0.374 | 0.011 | 2.054 | 51.82 | 7.13 | needed | 384 | 3553 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted#1` | second | counted | 16 | 31.896 | 0.349 | 0.011 | 1.994 | 51.82 | 7.13 | needed | 0 | 3553 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 16 | 31.058 | 0.433 | 0.014 | 1.941 | 42.56 | 6.45 | needed | 384 | 3042 | - | 0 | yes |
| uniform-65536 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 16 | 30.209 | 0.527 | 0.017 | 1.888 | 42.56 | 6.45 | needed | 0 | 3042 | - | 0 | yes |
| uniform-65536 | pagerank | `grust-next@unchecked#1` | first | unchecked | 16 | 30.116 | 0.220 | 0.007 | 1.882 | 41.36 | 6.33 | needed | 384 | 3043 | - | 0 | yes |
| uniform-65536 | pagerank | `grust-next@unchecked#1` | second | unchecked | 16 | 29.240 | 0.130 | 0.004 | 1.827 | 41.36 | 6.33 | needed | 0 | 3043 | - | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted#unset` | first | counted | 16 | 89.756 | 0.348 | 0.004 | 5.610 | 52.02 | - | needed | 512 | 2337 | 17497177 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted#unset` | second | counted | 16 | 88.523 | 0.495 | 0.006 | 5.533 | 52.02 | - | needed | 128 | 2337 | 17497177 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 16 | 55.683 | 1.204 | 0.022 | 3.480 | 39.35 | - | needed | 512 | 2848 | - | 0 | yes |
| uniform-65536 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 16 | 54.049 | 0.454 | 0.008 | 3.378 | 39.35 | - | needed | 128 | 2848 | - | 0 | yes |
| uniform-65536 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 16 | 54.696 | 0.520 | 0.009 | 3.419 | 38.01 | - | needed | 512 | 2337 | - | 0 | yes |
| uniform-65536 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 16 | 53.049 | 0.382 | 0.007 | 3.316 | 38.01 | - | needed | 128 | 2337 | - | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted+eager#1` | first | counted | 16 | 32.726 | 0.064 | 0.002 | 2.045 | 50.34 | 7.28 | always | 384 | 3042 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted+eager#1` | second | counted | 16 | 32.122 | 0.120 | 0.004 | 2.008 | 50.34 | 7.28 | always | 0 | 3042 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted+eager#unset` | first | counted | 16 | 89.973 | 0.913 | 0.010 | 5.623 | 61.03 | 8.63 | always | 512 | 2978 | 19266533 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted+eager#unset` | second | counted | 16 | 89.476 | 1.060 | 0.012 | 5.592 | 61.03 | 8.63 | always | 128 | 2978 | 19266533 | 0 | yes |
| uniform-65536 | triangles | `neo4j-graph` |  |  | - | 43.217 | 0.851 | 0.020 | - | 47.97 | - |  | 4 | 1664 | - | 0 | yes |
| uniform-65536 | triangles | `grust#1` | first | counted | - | 87.249 | 0.456 | 0.005 | - | 132.55 | - | needed | 1668 | 3110 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust#1` | second | counted | - | 82.221 | 0.983 | 0.012 | - | 132.55 | - | needed | 128 | 3110 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust#unset` | first | counted | - | 86.019 | 0.574 | 0.007 | - | 131.63 | - | needed | 1668 | 3095 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust#unset` | second | counted | - | 79.801 | 0.240 | 0.003 | - | 131.63 | - | needed | 128 | 3095 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted#1` | first | counted | - | 87.901 | 0.238 | 0.003 | - | 93.51 | - | needed | 1157 | 1383 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted#1` | second | counted | - | 86.473 | 1.255 | 0.015 | - | 93.51 | - | needed | 1537 | 1383 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@work-uncounted#1` | first | work-uncounted | - | 84.515 | 0.394 | 0.005 | - | 79.51 | - | needed | 1157 | 1893 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@work-uncounted#1` | second | work-uncounted | - | 84.559 | 0.900 | 0.011 | - | 79.51 | - | needed | 1537 | 1893 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@unchecked#1` | first | unchecked | - | 81.811 | 2.105 | 0.026 | - | 79.59 | - | needed | 1157 | 1383 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@unchecked#1` | second | unchecked | - | 79.857 | 0.647 | 0.008 | - | 79.59 | - | needed | 1537 | 1383 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted#unset` | first | counted | - | 84.664 | 0.678 | 0.008 | - | 113.11 | - | needed | 1157 | 1319 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted#unset` | second | counted | - | 83.884 | 0.637 | 0.008 | - | 113.11 | - | needed | 1154 | 1319 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 85.117 | 0.837 | 0.010 | - | 93.47 | - | needed | 1157 | 1319 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 83.037 | 0.730 | 0.009 | - | 93.47 | - | needed | 1154 | 1319 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@unchecked#unset` | first | unchecked | - | 82.983 | 1.281 | 0.015 | - | 89.70 | - | needed | 1157 | 1319 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@unchecked#unset` | second | unchecked | - | 81.627 | 1.109 | 0.014 | - | 89.70 | - | needed | 643 | 1319 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted+eager#1` | first | counted | - | 83.383 | 1.049 | 0.013 | - | 75.25 | 0.00 | always | 1157 | 1383 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted+eager#1` | second | counted | - | 82.702 | 1.298 | 0.016 | - | 75.25 | 0.00 | always | 1537 | 1383 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted+eager#unset` | first | counted | - | 87.171 | 0.141 | 0.002 | - | 112.52 | 0.00 | always | 1157 | 1319 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted+eager#unset` | second | counted | - | 83.855 | 0.480 | 0.006 | - | 112.52 | 0.00 | always | 1154 | 1319 | 15327135 | 0 | yes |
| uniform-65536 | wcc | `neo4j-graph` |  |  | - | 3.814 | 0.006 | 0.002 | - | 44.81 | - |  | 32 | 1664 | - | 0 | yes |
| uniform-65536 | wcc | `icebug` |  |  | - | 25.983 | 0.205 | 0.008 | - | 60.34 | - |  | 243 | 3889 | - | 0 | yes |
| uniform-65536 | wcc | `icecat` |  |  | - | 4.455 | 0.066 | 0.015 | - | 20.71 | - |  | 256 | 1665 | - | 0 | yes |
| uniform-65536 | wcc | `grustcat` |  |  | - | 3.108 | 0.003 | 0.001 | - | 467.71 | - |  | 0 | 37598 | - | 0 | yes |
| uniform-65536 | wcc | `grust#1` | first | counted | - | 9.362 | 0.051 | 0.005 | - | 108.70 | - | needed | 128 | 3107 | 4128495 | 0 | yes |
| uniform-65536 | wcc | `grust#1` | second | counted | - | 9.829 | 0.068 | 0.007 | - | 108.70 | - | needed | 128 | 3107 | 4128495 | 0 | yes |
| uniform-65536 | wcc | `grust#unset` | first | counted | - | 17.445 | 0.028 | 0.002 | - | 108.36 | - | needed | 128 | 3093 | 5298822 | 0 | yes |
| uniform-65536 | wcc | `grust#unset` | second | counted | - | 17.437 | 0.062 | 0.004 | - | 108.36 | - | needed | 126 | 3093 | 5298822 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted#1` | first | counted | - | 10.390 | 0.023 | 0.002 | - | 42.75 | - | needed | 128 | 2401 | 4128495 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted#1` | second | counted | - | 10.248 | 0.095 | 0.009 | - | 42.75 | - | needed | 64 | 2401 | 4128495 | 0 | yes |
| uniform-65536 | wcc | `grust-next@work-uncounted#1` | first | work-uncounted | - | 9.100 | 0.059 | 0.006 | - | 36.65 | - | needed | 128 | 2401 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@work-uncounted#1` | second | work-uncounted | - | 8.909 | 0.076 | 0.009 | - | 36.65 | - | needed | 64 | 2401 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@unchecked#1` | first | unchecked | - | 8.529 | 0.038 | 0.004 | - | 36.56 | - | needed | 128 | 2401 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@unchecked#1` | second | unchecked | - | 8.323 | 0.023 | 0.003 | - | 36.56 | - | needed | 64 | 2401 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted#unset` | first | counted | - | 17.391 | 0.019 | 0.001 | - | 52.23 | - | needed | 128 | 2337 | 5298822 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted#unset` | second | counted | - | 17.125 | 0.045 | 0.003 | - | 52.23 | - | needed | 0 | 2337 | 5298822 | 0 | yes |
| uniform-65536 | wcc | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 8.811 | 0.136 | 0.015 | - | 38.76 | - | needed | 128 | 2337 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 8.558 | 0.013 | 0.002 | - | 38.76 | - | needed | 0 | 2337 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@unchecked#unset` | first | unchecked | - | 7.588 | 0.188 | 0.025 | - | 37.43 | - | needed | 128 | 2337 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@unchecked#unset` | second | unchecked | - | 7.346 | 0.030 | 0.004 | - | 37.43 | - | needed | 0 | 2337 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted+eager#1` | first | counted | - | 10.293 | 0.018 | 0.002 | - | 49.67 | 6.99 | always | 128 | 3042 | 5897851 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted+eager#1` | second | counted | - | 10.286 | 0.069 | 0.007 | - | 49.67 | 6.99 | always | 128 | 3042 | 5897851 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted+eager#unset` | first | counted | - | 17.300 | 0.018 | 0.001 | - | 61.19 | 8.44 | always | 128 | 2477 | 7068178 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted+eager#unset` | second | counted | - | 17.110 | 0.072 | 0.004 | - | 61.19 | 8.44 | always | 0 | 2477 | 7068178 | 0 | yes |

### `full-width.json`: full-width

workers 16, concurrency 16, allocator glibc default, not pinned, 1 warmup + 5 repeats, steal over the run 0 ticks, 113.9 s, unusable at MAD/median >= 0.25

Not timed (no agreeing parity row): neo4j-graph pagerank layered-16384.edges, neo4j-graph pagerank layered-65536.edges, neo4j-graph pagerank path-16384.edges, neo4j-graph pagerank path-65536.edges 

| fixture | algorithm | participant | call | accounting | iters | total ms | MAD | MAD/median | per iter | build ms | incoming ms | prepare | minflt | minflt build | work units | steal | usable |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |
| hub-16384 | bfs | `icebug` |  |  | - | 2.018 | 0.108 | 0.054 | - | 9.78 | - |  | 57 | 1018 | - | 0 | yes |
| hub-16384 | bfs | `icecat` |  |  | - | 0.861 | 0.009 | 0.011 | - | 6.21 | - |  | 96 | 1555 | - | 0 | yes |
| hub-16384 | bfs | `grustcat` |  |  | - | 0.672 | 0.010 | 0.015 | - | 88.68 | - |  | 0 | 10314 | - | 0 | yes |
| hub-16384 | bfs | `grust` | first | counted | - | 1.569 | 0.027 | 0.017 | - | 19.15 | - | needed | 36 | 1787 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust` | second | counted | - | 1.447 | 0.007 | 0.005 | - | 19.15 | - | needed | 0 | 1787 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted` | first | counted | - | 1.579 | 0.043 | 0.027 | - | 10.87 | - | needed | 0 | 1537 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted` | second | counted | - | 1.481 | 0.008 | 0.005 | - | 10.87 | - | needed | 0 | 1537 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@work-uncounted` | first | work-uncounted | - | 1.005 | 0.029 | 0.029 | - | 9.46 | - | needed | 0 | 2044 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@work-uncounted` | second | work-uncounted | - | 0.879 | 0.009 | 0.010 | - | 9.46 | - | needed | 0 | 2044 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@unchecked` | first | unchecked | - | 0.862 | 0.048 | 0.056 | - | 9.27 | - | needed | 0 | 2043 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@unchecked` | second | unchecked | - | 0.733 | 0.007 | 0.009 | - | 9.27 | - | needed | 0 | 2043 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@counted+eager` | first | counted | - | 1.502 | 0.003 | 0.002 | - | 12.33 | 1.62 | always | 0 | 1793 | 1489517 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted+eager` | second | counted | - | 1.463 | 0.012 | 0.008 | - | 12.33 | 1.62 | always | 0 | 1793 | 1489517 | 0 | yes |
| hub-16384 | pagerank | `neo4j-graph` |  |  | 36 | 13.573 | 0.103 | 0.008 | 0.377 | 4.61 | - |  | 34 | 875 | - | 0 | yes |
| hub-16384 | pagerank | `icebug` |  |  | 12 | 3.003 | 0.076 | 0.025 | 0.250 | 10.10 | - |  | 201 | 1018 | - | 0 | yes |
| hub-16384 | pagerank | `icecat` |  |  | 17 | 8.604 | 0.048 | 0.006 | 0.506 | 6.63 | - |  | 130 | 1555 | - | 0 | yes |
| hub-16384 | pagerank | `grustcat` |  |  | 17 | 7.351 | 0.009 | 0.001 | 0.432 | 88.62 | - |  | 0 | 9803 | - | 0 | yes |
| hub-16384 | pagerank | `grust` | first | counted | 17 | 6.462 | 0.058 | 0.009 | 0.380 | 19.61 | - | needed | 485 | 2297 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust` | second | counted | 17 | 3.420 | 0.032 | 0.009 | 0.201 | 19.61 | - | needed | 0 | 2297 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted` | first | counted | 17 | 3.471 | 0.012 | 0.003 | 0.204 | 12.84 | 1.61 | needed | 5 | 2298 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted` | second | counted | 17 | 3.436 | 0.032 | 0.009 | 0.202 | 12.84 | 1.61 | needed | 0 | 2298 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 17 | 2.908 | 0.019 | 0.007 | 0.171 | 10.71 | 1.46 | needed | 5 | 1791 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 17 | 2.805 | 0.037 | 0.013 | 0.165 | 10.71 | 1.46 | needed | 1 | 1791 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@unchecked` | first | unchecked | 17 | 2.931 | 0.028 | 0.010 | 0.172 | 10.78 | 1.44 | needed | 4 | 2296 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@unchecked` | second | unchecked | 17 | 2.851 | 0.074 | 0.026 | 0.168 | 10.78 | 1.44 | needed | 1 | 2296 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted+eager` | first | counted | 17 | 3.443 | 0.050 | 0.014 | 0.203 | 12.97 | 1.63 | always | 5 | 2299 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted+eager` | second | counted | 17 | 3.395 | 0.030 | 0.009 | 0.200 | 12.97 | 1.63 | always | 0 | 2299 | 4403580 | 0 | yes |
| hub-16384 | triangles | `neo4j-graph` |  |  | - | 1.257 | 0.016 | 0.013 | - | 4.70 | - |  | 53 | 883 | - | 0 | yes |
| hub-16384 | triangles | `grust` | first | counted | - | 8.939 | 0.053 | 0.006 | - | 23.45 | - | needed | 1029 | 2300 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust` | second | counted | - | 6.275 | 0.013 | 0.002 | - | 23.45 | - | needed | 1 | 2300 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted` | first | counted | - | 7.193 | 0.008 | 0.001 | - | 11.16 | - | needed | 257 | 1026 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted` | second | counted | - | 7.231 | 0.053 | 0.007 | - | 11.16 | - | needed | 512 | 1026 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@work-uncounted` | first | work-uncounted | - | 7.032 | 0.036 | 0.005 | - | 9.33 | - | needed | 257 | 1024 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@work-uncounted` | second | work-uncounted | - | 7.026 | 0.043 | 0.006 | - | 9.33 | - | needed | 512 | 1024 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@unchecked` | first | unchecked | - | 6.904 | 0.062 | 0.009 | - | 10.05 | - | needed | 257 | 1534 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@unchecked` | second | unchecked | - | 6.875 | 0.013 | 0.002 | - | 10.05 | - | needed | 512 | 1534 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@counted+eager` | first | counted | - | 7.176 | 0.050 | 0.007 | - | 11.74 | 0.00 | always | 257 | 1534 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted+eager` | second | counted | - | 7.199 | 0.068 | 0.009 | - | 11.74 | 0.00 | always | 511 | 1534 | 3742208 | 0 | yes |
| hub-16384 | wcc | `neo4j-graph` |  |  | - | 1.138 | 0.015 | 0.013 | - | 4.63 | - |  | 1 | 872 | - | 0 | yes |
| hub-16384 | wcc | `icebug` |  |  | - | 2.753 | 0.138 | 0.050 | - | 10.10 | - |  | 69 | 1018 | - | 0 | yes |
| hub-16384 | wcc | `icecat` |  |  | - | 0.930 | 0.009 | 0.010 | - | 6.36 | - |  | 65 | 1555 | - | 0 | yes |
| hub-16384 | wcc | `grustcat` |  |  | - | 0.611 | 0.006 | 0.010 | - | 92.45 | - |  | 0 | 10314 | - | 0 | yes |
| hub-16384 | wcc | `grust` | first | counted | - | 1.310 | 0.025 | 0.019 | - | 19.75 | - | needed | 142 | 1788 | 1031210 | 0 | yes |
| hub-16384 | wcc | `grust` | second | counted | - | 0.598 | 0.032 | 0.053 | - | 19.75 | - | needed | 36 | 1788 | 1031210 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted` | first | counted | - | 0.488 | 0.028 | 0.058 | - | 11.63 | - | needed | 3 | 2043 | 1031212 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted` | second | counted | - | 0.502 | 0.035 | 0.069 | - | 11.63 | - | needed | 0 | 2043 | 1031212 | 0 | yes |
| hub-16384 | wcc | `grust-next@work-uncounted` | first | work-uncounted | - | 0.399 | 0.007 | 0.016 | - | 9.07 | - | needed | 1 | 1534 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@work-uncounted` | second | work-uncounted | - | 0.404 | 0.015 | 0.038 | - | 9.07 | - | needed | 2 | 1534 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@unchecked` | first | unchecked | - | 0.450 | 0.047 | 0.104 | - | 8.89 | - | needed | 4 | 1536 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@unchecked` | second | unchecked | - | 0.428 | 0.058 | 0.137 | - | 8.89 | - | needed | 1 | 1536 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@counted+eager` | first | counted | - | 0.485 | 0.015 | 0.031 | - | 13.13 | 1.64 | always | 3 | 2298 | 1473149 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted+eager` | second | counted | - | 0.512 | 0.035 | 0.068 | - | 13.13 | 1.64 | always | 2 | 2298 | 1473149 | 0 | yes |
| hub-65536 | bfs | `icebug` |  |  | - | 15.849 | 0.503 | 0.032 | - | 63.49 | - |  | 216 | 4057 | - | 0 | yes |
| hub-65536 | bfs | `icecat` |  |  | - | 4.928 | 0.145 | 0.029 | - | 21.95 | - |  | 195 | 2522 | - | 0 | yes |
| hub-65536 | bfs | `grustcat` |  |  | - | 5.484 | 0.211 | 0.038 | - | 468.13 | - |  | 1 | 39252 | - | 0 | yes |
| hub-65536 | bfs | `grust` | first | counted | - | 4.301 | 0.226 | 0.052 | - | 105.11 | - | needed | 396 | 3611 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust` | second | counted | - | 3.281 | 0.027 | 0.008 | - | 105.11 | - | needed | 201 | 3611 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted` | first | counted | - | 3.330 | 0.035 | 0.010 | - | 39.49 | - | needed | 118 | 3278 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted` | second | counted | - | 3.106 | 0.031 | 0.010 | - | 39.49 | - | needed | 77 | 3278 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust-next@work-uncounted` | first | work-uncounted | - | 3.183 | 0.060 | 0.019 | - | 34.06 | - | needed | 116 | 3282 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@work-uncounted` | second | work-uncounted | - | 2.928 | 0.026 | 0.009 | - | 34.06 | - | needed | 93 | 3282 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@unchecked` | first | unchecked | - | 3.262 | 0.067 | 0.020 | - | 33.17 | - | needed | 131 | 3279 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@unchecked` | second | unchecked | - | 2.983 | 0.049 | 0.016 | - | 33.17 | - | needed | 86 | 3279 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@counted+eager` | first | counted | - | 3.088 | 0.041 | 0.013 | - | 46.68 | 5.30 | always | 119 | 3793 | 5959069 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted+eager` | second | counted | - | 3.093 | 0.031 | 0.010 | - | 46.68 | 5.30 | always | 78 | 3793 | 5959069 | 0 | yes |
| hub-65536 | pagerank | `neo4j-graph` |  |  | 29 | 15.178 | 0.898 | 0.059 | 0.523 | 15.33 | - |  | 96 | 2468 | - | 0 | yes |
| hub-65536 | pagerank | `icebug` |  |  | 12 | 8.725 | 0.069 | 0.008 | 0.727 | 66.34 | - |  | 502 | 4057 | - | 0 | yes |
| hub-65536 | pagerank | `icecat` |  |  | 17 | 34.878 | 0.068 | 0.002 | 2.052 | 22.52 | - |  | 607 | 2412 | - | 0 | yes |
| hub-65536 | pagerank | `grustcat` |  |  | 17 | 33.603 | 0.455 | 0.014 | 1.977 | 473.35 | - |  | 0 | 38231 | - | 0 | yes |
| hub-65536 | pagerank | `grust` | first | counted | 17 | 19.679 | 0.394 | 0.020 | 1.158 | 111.76 | - | needed | 1133 | 3612 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust` | second | counted | 17 | 8.902 | 0.186 | 0.021 | 0.524 | 111.76 | - | needed | 5 | 3612 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted` | first | counted | 17 | 7.268 | 0.140 | 0.019 | 0.428 | 45.97 | 5.35 | needed | 15 | 3793 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted` | second | counted | 17 | 7.577 | 0.242 | 0.032 | 0.446 | 45.97 | 5.35 | needed | 2 | 3793 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 17 | 5.015 | 0.107 | 0.021 | 0.295 | 38.74 | 4.65 | needed | 14 | 3790 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 17 | 4.826 | 0.036 | 0.007 | 0.284 | 38.74 | 4.65 | needed | 3 | 3790 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@unchecked` | first | unchecked | 17 | 4.871 | 0.096 | 0.020 | 0.287 | 39.64 | 4.57 | needed | 15 | 4301 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@unchecked` | second | unchecked | 17 | 4.818 | 0.078 | 0.016 | 0.283 | 39.64 | 4.57 | needed | 4 | 4301 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted+eager` | first | counted | 17 | 6.993 | 0.084 | 0.012 | 0.411 | 47.01 | 5.44 | always | 15 | 4811 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted+eager` | second | counted | 17 | 6.975 | 0.198 | 0.028 | 0.410 | 47.01 | 5.44 | always | 6 | 4811 | 17616940 | 0 | yes |
| hub-65536 | triangles | `neo4j-graph` |  |  | - | 3.648 | 0.028 | 0.008 | - | 15.19 | - |  | 51 | 2372 | - | 0 | yes |
| hub-65536 | triangles | `grust` | first | counted | - | 31.992 | 0.468 | 0.015 | - | 128.02 | - | needed | 1768 | 3614 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust` | second | counted | - | 25.663 | 0.043 | 0.002 | - | 128.02 | - | needed | 1 | 3614 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted` | first | counted | - | 29.375 | 0.166 | 0.006 | - | 45.37 | - | needed | 1026 | 3285 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted` | second | counted | - | 28.001 | 0.556 | 0.020 | - | 45.37 | - | needed | 1025 | 3285 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@work-uncounted` | first | work-uncounted | - | 28.212 | 0.215 | 0.008 | - | 39.18 | - | needed | 1026 | 3793 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@work-uncounted` | second | work-uncounted | - | 27.226 | 0.146 | 0.005 | - | 39.18 | - | needed | 1025 | 3793 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@unchecked` | first | unchecked | - | 28.031 | 0.196 | 0.007 | - | 36.37 | - | needed | 1026 | 3282 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@unchecked` | second | unchecked | - | 26.865 | 0.074 | 0.003 | - | 36.37 | - | needed | 1025 | 3282 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@counted+eager` | first | counted | - | 29.020 | 0.254 | 0.009 | - | 43.82 | 0.00 | always | 1026 | 3283 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted+eager` | second | counted | - | 27.483 | 0.033 | 0.001 | - | 43.82 | 0.00 | always | 1024 | 3283 | 14971727 | 0 | yes |
| hub-65536 | wcc | `neo4j-graph` |  |  | - | 3.121 | 0.042 | 0.013 | - | 15.11 | - |  | 227 | 2406 | - | 0 | yes |
| hub-65536 | wcc | `icebug` |  |  | - | 21.868 | 0.425 | 0.019 | - | 67.59 | - |  | 240 | 4057 | - | 0 | yes |
| hub-65536 | wcc | `icecat` |  |  | - | 3.489 | 0.059 | 0.017 | - | 21.53 | - |  | 102 | 2367 | - | 0 | yes |
| hub-65536 | wcc | `grustcat` |  |  | - | 2.501 | 0.015 | 0.006 | - | 463.81 | - |  | 0 | 38231 | - | 0 | yes |
| hub-65536 | wcc | `grust` | first | counted | - | 2.525 | 0.012 | 0.005 | - | 108.97 | - | needed | 241 | 3613 | 4125488 | 0 | yes |
| hub-65536 | wcc | `grust` | second | counted | - | 1.813 | 0.095 | 0.052 | - | 108.97 | - | needed | 132 | 3613 | 4125488 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted` | first | counted | - | 1.620 | 0.047 | 0.029 | - | 40.79 | - | needed | 3 | 3277 | 4125491 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted` | second | counted | - | 1.567 | 0.085 | 0.054 | - | 40.79 | - | needed | 2 | 3277 | 4125491 | 0 | yes |
| hub-65536 | wcc | `grust-next@work-uncounted` | first | work-uncounted | - | 1.327 | 0.025 | 0.019 | - | 32.72 | - | needed | 4 | 3279 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@work-uncounted` | second | work-uncounted | - | 1.319 | 0.033 | 0.025 | - | 32.72 | - | needed | 2 | 3279 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@unchecked` | first | unchecked | - | 1.310 | 0.148 | 0.113 | - | 32.62 | - | needed | 2 | 3281 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@unchecked` | second | unchecked | - | 1.403 | 0.085 | 0.061 | - | 32.62 | - | needed | 2 | 3281 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@counted+eager` | first | counted | - | 1.596 | 0.056 | 0.035 | - | 45.34 | 5.26 | always | 4 | 3793 | 5893552 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted+eager` | second | counted | - | 1.587 | 0.025 | 0.016 | - | 45.34 | 5.26 | always | 1 | 3793 | 5893552 | 0 | yes |
| layered-16384 | bfs | `icebug` |  |  | - | 0.532 | 0.021 | 0.040 | - | 2.84 | - |  | 36 | 458 | - | 0 | yes |
| layered-16384 | bfs | `icecat` |  |  | - | 0.397 | 0.010 | 0.025 | - | 1.76 | - |  | 66 | 525 | - | 0 | yes |
| layered-16384 | bfs | `grustcat` |  |  | - | 0.260 | 0.003 | 0.011 | - | 32.83 | - |  | 1 | 7350 | - | 0 | yes |
| layered-16384 | bfs | `grust` | first | counted | - | 0.460 | 0.006 | 0.012 | - | 6.96 | - | needed | 30 | 1032 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust` | second | counted | - | 0.386 | 0.000 | 0.001 | - | 6.96 | - | needed | 0 | 1032 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted` | first | counted | - | 0.460 | 0.005 | 0.010 | - | 6.26 | - | needed | 26 | 1015 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted` | second | counted | - | 0.383 | 0.003 | 0.007 | - | 6.26 | - | needed | 0 | 1015 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@work-uncounted` | first | work-uncounted | - | 0.374 | 0.002 | 0.006 | - | 5.41 | - | needed | 26 | 1011 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@work-uncounted` | second | work-uncounted | - | 0.292 | 0.002 | 0.007 | - | 5.41 | - | needed | 0 | 1011 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@unchecked` | first | unchecked | - | 0.337 | 0.008 | 0.024 | - | 5.41 | - | needed | 26 | 1013 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@unchecked` | second | unchecked | - | 0.254 | 0.002 | 0.006 | - | 5.41 | - | needed | 0 | 1013 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@counted+eager` | first | counted | - | 0.456 | 0.002 | 0.004 | - | 7.18 | 0.83 | always | 26 | 1110 | 493703 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted+eager` | second | counted | - | 0.381 | 0.000 | 0.000 | - | 7.18 | 0.83 | always | 0 | 1110 | 493703 | 0 | yes |
| layered-16384 | pagerank | `icebug` |  |  | 69 | 8.920 | 0.116 | 0.013 | 0.129 | 2.83 | - |  | 200 | 458 | - | 0 | yes |
| layered-16384 | pagerank | `icecat` |  |  | 84 | 27.726 | 0.041 | 0.001 | 0.330 | 1.77 | - |  | 128 | 526 | - | 0 | yes |
| layered-16384 | pagerank | `grustcat` |  |  | 84 | 26.270 | 0.030 | 0.001 | 0.313 | 33.16 | - |  | 0 | 6840 | - | 0 | yes |
| layered-16384 | pagerank | `grust` | first | counted | 84 | 15.662 | 0.052 | 0.003 | 0.186 | 7.06 | - | needed | 293 | 1032 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust` | second | counted | 84 | 13.833 | 0.323 | 0.023 | 0.165 | 7.06 | - | needed | 0 | 1032 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted` | first | counted | 84 | 14.752 | 0.136 | 0.009 | 0.176 | 7.25 | 0.82 | needed | 105 | 1108 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted` | second | counted | 84 | 14.423 | 0.167 | 0.012 | 0.172 | 7.25 | 0.82 | needed | 0 | 1108 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 84 | 12.797 | 0.017 | 0.001 | 0.152 | 6.18 | 0.65 | needed | 105 | 1108 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 84 | 12.246 | 0.013 | 0.001 | 0.146 | 6.18 | 0.65 | needed | 0 | 1108 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@unchecked` | first | unchecked | 84 | 12.813 | 0.292 | 0.023 | 0.153 | 6.12 | 0.62 | needed | 103 | 1110 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@unchecked` | second | unchecked | 84 | 12.312 | 0.058 | 0.005 | 0.147 | 6.12 | 0.62 | needed | 1 | 1110 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted+eager` | first | counted | 84 | 14.907 | 0.061 | 0.004 | 0.177 | 7.18 | 0.82 | always | 103 | 1110 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted+eager` | second | counted | 84 | 14.617 | 0.352 | 0.024 | 0.174 | 7.18 | 0.82 | always | 0 | 1110 | 7307112 | 0 | yes |
| layered-16384 | triangles | `neo4j-graph` |  |  | - | 0.741 | 0.036 | 0.049 | - | 2.27 | - |  | 31 | 538 | - | 0 | yes |
| layered-16384 | triangles | `grust` | first | counted | - | 3.138 | 0.030 | 0.009 | - | 7.44 | - | needed | 452 | 1158 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust` | second | counted | - | 1.703 | 0.008 | 0.005 | - | 7.44 | - | needed | 1 | 1158 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted` | first | counted | - | 2.404 | 0.015 | 0.006 | - | 6.86 | - | needed | 351 | 1141 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted` | second | counted | - | 2.169 | 0.049 | 0.023 | - | 6.86 | - | needed | 318 | 1141 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@work-uncounted` | first | work-uncounted | - | 2.284 | 0.031 | 0.014 | - | 5.96 | - | needed | 350 | 1139 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@work-uncounted` | second | work-uncounted | - | 2.032 | 0.033 | 0.016 | - | 5.96 | - | needed | 318 | 1139 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@unchecked` | first | unchecked | - | 2.220 | 0.013 | 0.006 | - | 5.92 | - | needed | 350 | 1140 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@unchecked` | second | unchecked | - | 1.985 | 0.037 | 0.019 | - | 5.92 | - | needed | 318 | 1140 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@counted+eager` | first | counted | - | 2.472 | 0.008 | 0.003 | - | 6.85 | 0.00 | always | 351 | 1140 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted+eager` | second | counted | - | 2.173 | 0.029 | 0.013 | - | 6.85 | 0.00 | always | 318 | 1140 | 718265 | 0 | yes |
| layered-16384 | wcc | `neo4j-graph` |  |  | - | 1.048 | 0.017 | 0.016 | - | 2.29 | - |  | 3 | 541 | - | 0 | yes |
| layered-16384 | wcc | `icebug` |  |  | - | 1.004 | 0.017 | 0.017 | - | 2.82 | - |  | 43 | 458 | - | 0 | yes |
| layered-16384 | wcc | `icecat` |  |  | - | 0.500 | 0.001 | 0.001 | - | 1.74 | - |  | 64 | 526 | - | 0 | yes |
| layered-16384 | wcc | `grustcat` |  |  | - | 0.359 | 0.001 | 0.001 | - | 33.33 | - |  | 1 | 7351 | - | 0 | yes |
| layered-16384 | wcc | `grust` | first | counted | - | 1.065 | 0.013 | 0.013 | - | 7.01 | - | needed | 140 | 1031 | 341583 | 0 | yes |
| layered-16384 | wcc | `grust` | second | counted | - | 0.340 | 0.013 | 0.037 | - | 7.01 | - | needed | 30 | 1031 | 341583 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted` | first | counted | - | 0.377 | 0.003 | 0.009 | - | 6.34 | - | needed | 35 | 1014 | 341583 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted` | second | counted | - | 0.361 | 0.011 | 0.029 | - | 6.34 | - | needed | 30 | 1014 | 341583 | 0 | yes |
| layered-16384 | wcc | `grust-next@work-uncounted` | first | work-uncounted | - | 0.335 | 0.011 | 0.032 | - | 5.39 | - | needed | 36 | 1011 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@work-uncounted` | second | work-uncounted | - | 0.317 | 0.021 | 0.066 | - | 5.39 | - | needed | 28 | 1011 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@unchecked` | first | unchecked | - | 0.323 | 0.003 | 0.009 | - | 5.50 | - | needed | 34 | 1013 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@unchecked` | second | unchecked | - | 0.302 | 0.007 | 0.024 | - | 5.50 | - | needed | 28 | 1013 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@counted+eager` | first | counted | - | 0.335 | 0.009 | 0.026 | - | 7.17 | 0.81 | always | 35 | 1110 | 487978 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted+eager` | second | counted | - | 0.347 | 0.004 | 0.012 | - | 7.17 | 0.81 | always | 28 | 1110 | 487978 | 0 | yes |
| layered-65536 | bfs | `icebug` |  |  | - | 2.832 | 0.003 | 0.001 | - | 11.31 | - |  | 132 | 1832 | - | 0 | yes |
| layered-65536 | bfs | `icecat` |  |  | - | 1.715 | 0.011 | 0.006 | - | 7.37 | - |  | 257 | 2147 | - | 0 | yes |
| layered-65536 | bfs | `grustcat` |  |  | - | 1.068 | 0.014 | 0.013 | - | 139.56 | - |  | 0 | 26634 | - | 0 | yes |
| layered-65536 | bfs | `grust` | first | counted | - | 1.886 | 0.012 | 0.006 | - | 34.12 | - | needed | 119 | 3142 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust` | second | counted | - | 1.602 | 0.009 | 0.006 | - | 34.12 | - | needed | 0 | 3142 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted` | first | counted | - | 1.879 | 0.002 | 0.001 | - | 22.76 | - | needed | 103 | 2745 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted` | second | counted | - | 1.600 | 0.012 | 0.008 | - | 22.76 | - | needed | 0 | 2745 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@work-uncounted` | first | work-uncounted | - | 1.517 | 0.004 | 0.003 | - | 19.11 | - | needed | 103 | 2743 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@work-uncounted` | second | work-uncounted | - | 1.214 | 0.010 | 0.008 | - | 19.11 | - | needed | 0 | 2743 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@unchecked` | first | unchecked | - | 1.347 | 0.007 | 0.005 | - | 19.44 | - | needed | 103 | 2744 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@unchecked` | second | unchecked | - | 1.054 | 0.016 | 0.015 | - | 19.44 | - | needed | 0 | 2744 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@counted+eager` | first | counted | - | 1.818 | 0.013 | 0.007 | - | 25.65 | 2.57 | always | 102 | 3130 | 1979713 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted+eager` | second | counted | - | 1.587 | 0.002 | 0.001 | - | 25.65 | 2.57 | always | 0 | 3130 | 1979713 | 0 | yes |
| layered-65536 | pagerank | `icebug` |  |  | 60 | 14.359 | 0.130 | 0.009 | 0.239 | 11.51 | - |  | 489 | 1832 | - | 0 | yes |
| layered-65536 | pagerank | `icecat` |  |  | 75 | 102.398 | 0.234 | 0.002 | 1.365 | 6.79 | - |  | 608 | 1636 | - | 0 | yes |
| layered-65536 | pagerank | `grustcat` |  |  | 75 | 94.510 | 0.043 | 0.000 | 1.260 | 138.26 | - |  | 0 | 26635 | - | 0 | yes |
| layered-65536 | pagerank | `grust` | first | counted | 75 | 25.844 | 0.107 | 0.004 | 0.345 | 32.52 | - | needed | 882 | 3143 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust` | second | counted | 75 | 21.546 | 0.328 | 0.015 | 0.287 | 32.52 | - | needed | 1 | 3143 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted` | first | counted | 75 | 21.060 | 0.095 | 0.005 | 0.281 | 25.08 | 2.60 | needed | 406 | 3128 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted` | second | counted | 75 | 20.459 | 0.556 | 0.027 | 0.273 | 25.08 | 2.60 | needed | 4 | 3128 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 75 | 16.032 | 0.010 | 0.001 | 0.214 | 21.05 | 1.95 | needed | 404 | 3129 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 75 | 14.524 | 0.233 | 0.016 | 0.194 | 21.05 | 1.95 | needed | 2 | 3129 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@unchecked` | first | unchecked | 75 | 15.193 | 0.335 | 0.022 | 0.203 | 21.08 | 1.85 | needed | 405 | 3127 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@unchecked` | second | unchecked | 75 | 14.019 | 0.088 | 0.006 | 0.187 | 21.08 | 1.85 | needed | 2 | 3127 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted+eager` | first | counted | 75 | 20.862 | 0.297 | 0.014 | 0.278 | 25.74 | 2.57 | always | 405 | 3128 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted+eager` | second | counted | 75 | 19.996 | 0.225 | 0.011 | 0.267 | 25.74 | 2.57 | always | 4 | 3128 | 26313822 | 0 | yes |
| layered-65536 | triangles | `neo4j-graph` |  |  | - | 1.178 | 0.023 | 0.019 | - | 5.34 | - |  | 50 | 1806 | - | 0 | yes |
| layered-65536 | triangles | `grust` | first | counted | - | 10.221 | 0.155 | 0.015 | - | 34.99 | - | needed | 1503 | 3650 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust` | second | counted | - | 6.565 | 0.012 | 0.002 | - | 34.99 | - | needed | 1 | 3650 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted` | first | counted | - | 9.325 | 0.041 | 0.004 | - | 26.12 | - | needed | 1401 | 3253 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted` | second | counted | - | 7.294 | 0.005 | 0.001 | - | 26.12 | - | needed | 508 | 3253 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@work-uncounted` | first | work-uncounted | - | 8.824 | 0.015 | 0.002 | - | 21.61 | - | needed | 1402 | 3251 | - | 0 | yes |
| layered-65536 | triangles | `grust-next@work-uncounted` | second | work-uncounted | - | 6.766 | 0.021 | 0.003 | - | 21.61 | - | needed | 508 | 3251 | - | 0 | yes |
| layered-65536 | triangles | `grust-next@unchecked` | first | unchecked | - | 8.491 | 0.038 | 0.004 | - | 21.37 | - | needed | 1402 | 3248 | - | 0 | yes |
| layered-65536 | triangles | `grust-next@unchecked` | second | unchecked | - | 6.357 | 0.029 | 0.005 | - | 21.37 | - | needed | 508 | 3248 | - | 0 | yes |
| layered-65536 | triangles | `grust-next@counted+eager` | first | counted | - | 9.333 | 0.056 | 0.006 | - | 25.68 | 0.00 | always | 1401 | 3254 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted+eager` | second | counted | - | 7.251 | 0.048 | 0.007 | - | 25.68 | 0.00 | always | 508 | 3254 | 2877576 | 0 | yes |
| layered-65536 | wcc | `neo4j-graph` |  |  | - | 2.323 | 0.140 | 0.060 | - | 5.46 | - |  | 257 | 1814 | - | 0 | yes |
| layered-65536 | wcc | `icebug` |  |  | - | 4.781 | 0.043 | 0.009 | - | 11.54 | - |  | 138 | 1832 | - | 0 | yes |
| layered-65536 | wcc | `icecat` |  |  | - | 2.106 | 0.025 | 0.012 | - | 6.91 | - |  | 255 | 1637 | - | 0 | yes |
| layered-65536 | wcc | `grustcat` |  |  | - | 1.458 | 0.006 | 0.004 | - | 138.81 | - |  | 0 | 26635 | - | 0 | yes |
| layered-65536 | wcc | `grust` | first | counted | - | 1.599 | 0.024 | 0.015 | - | 30.98 | - | needed | 241 | 2631 | 1368151 | 0 | yes |
| layered-65536 | wcc | `grust` | second | counted | - | 0.881 | 0.027 | 0.031 | - | 30.98 | - | needed | 125 | 2631 | 1368151 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted` | first | counted | - | 0.899 | 0.013 | 0.015 | - | 23.66 | - | needed | 132 | 2743 | 1368152 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted` | second | counted | - | 0.862 | 0.013 | 0.016 | - | 23.66 | - | needed | 123 | 2743 | 1368152 | 0 | yes |
| layered-65536 | wcc | `grust-next@work-uncounted` | first | work-uncounted | - | 0.793 | 0.028 | 0.035 | - | 20.04 | - | needed | 134 | 2743 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@work-uncounted` | second | work-uncounted | - | 0.748 | 0.009 | 0.012 | - | 20.04 | - | needed | 124 | 2743 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@unchecked` | first | unchecked | - | 0.749 | 0.023 | 0.030 | - | 19.71 | - | needed | 132 | 2744 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@unchecked` | second | unchecked | - | 0.721 | 0.005 | 0.007 | - | 19.71 | - | needed | 125 | 2744 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@counted+eager` | first | counted | - | 0.884 | 0.012 | 0.013 | - | 26.69 | 2.58 | always | 133 | 3127 | 1954502 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted+eager` | second | counted | - | 0.858 | 0.005 | 0.006 | - | 26.69 | 2.58 | always | 123 | 3127 | 1954502 | 0 | yes |
| path-16384 | bfs | `icebug` |  |  | - | 0.265 | 0.001 | 0.002 | - | 1.80 | - |  | 36 | 450 | - | 0 | yes |
| path-16384 | bfs | `icecat` |  |  | - | 0.284 | 0.002 | 0.007 | - | 0.95 | - |  | 65 | 275 | - | 0 | yes |
| path-16384 | bfs | `grustcat` |  |  | - | 0.144 | 0.002 | 0.015 | - | 27.08 | - |  | 0 | 6430 | - | 0 | yes |
| path-16384 | bfs | `grust` | first | counted | - | 0.441 | 0.008 | 0.019 | - | 5.22 | - | needed | 36 | 741 | 245755 | 0 | yes |
| path-16384 | bfs | `grust` | second | counted | - | 0.340 | 0.000 | 0.000 | - | 5.22 | - | needed | 0 | 741 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@counted` | first | counted | - | 0.410 | 0.004 | 0.009 | - | 5.44 | - | needed | 32 | 791 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@counted` | second | counted | - | 0.326 | 0.000 | 0.001 | - | 5.44 | - | needed | 0 | 791 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@work-uncounted` | first | work-uncounted | - | 0.238 | 0.002 | 0.008 | - | 4.74 | - | needed | 32 | 790 | - | 0 | yes |
| path-16384 | bfs | `grust-next@work-uncounted` | second | work-uncounted | - | 0.153 | 0.000 | 0.003 | - | 4.74 | - | needed | 0 | 790 | - | 0 | yes |
| path-16384 | bfs | `grust-next@unchecked` | first | unchecked | - | 0.201 | 0.003 | 0.015 | - | 4.74 | - | needed | 32 | 790 | - | 0 | yes |
| path-16384 | bfs | `grust-next@unchecked` | second | unchecked | - | 0.117 | 0.001 | 0.005 | - | 4.74 | - | needed | 0 | 790 | - | 0 | yes |
| path-16384 | bfs | `grust-next@counted+eager` | first | counted | - | 0.411 | 0.004 | 0.009 | - | 6.13 | 0.65 | always | 32 | 855 | 344057 | 0 | yes |
| path-16384 | bfs | `grust-next@counted+eager` | second | counted | - | 0.327 | 0.000 | 0.001 | - | 6.13 | 0.65 | always | 0 | 855 | 344057 | 0 | yes |
| path-16384 | pagerank | `icebug` |  |  | 54 | 6.917 | 0.150 | 0.022 | 0.128 | 1.81 | - |  | 199 | 450 | - | 0 | yes |
| path-16384 | pagerank | `icecat` |  |  | 58 | 11.219 | 0.023 | 0.002 | 0.193 | 0.94 | - |  | 128 | 275 | - | 0 | yes |
| path-16384 | pagerank | `grustcat` |  |  | 58 | 9.778 | 0.060 | 0.006 | 0.169 | 27.05 | - |  | 0 | 6429 | - | 0 | yes |
| path-16384 | pagerank | `grust` | first | counted | 58 | 10.602 | 0.078 | 0.007 | 0.183 | 5.30 | - | needed | 261 | 741 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust` | second | counted | 58 | 8.858 | 0.125 | 0.014 | 0.153 | 5.30 | - | needed | 0 | 741 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted` | first | counted | 58 | 9.910 | 0.190 | 0.019 | 0.171 | 6.08 | 0.66 | needed | 108 | 855 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted` | second | counted | 58 | 9.680 | 0.054 | 0.006 | 0.167 | 6.08 | 0.66 | needed | 64 | 855 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 58 | 8.511 | 0.128 | 0.015 | 0.147 | 5.33 | 0.49 | needed | 108 | 855 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 58 | 8.253 | 0.030 | 0.004 | 0.142 | 5.33 | 0.49 | needed | 65 | 855 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@unchecked` | first | unchecked | 58 | 8.376 | 0.033 | 0.004 | 0.144 | 5.23 | 0.47 | needed | 106 | 857 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@unchecked` | second | unchecked | 58 | 8.169 | 0.115 | 0.014 | 0.141 | 5.23 | 0.47 | needed | 65 | 857 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@counted+eager` | first | counted | 58 | 9.959 | 0.148 | 0.015 | 0.172 | 6.11 | 0.65 | always | 108 | 854 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted+eager` | second | counted | 58 | 9.648 | 0.057 | 0.006 | 0.166 | 6.11 | 0.65 | always | 65 | 854 | 4112319 | 0 | yes |
| path-16384 | triangles | `neo4j-graph` |  |  | - | 0.551 | 0.008 | 0.015 | - | 2.11 | - |  | 21 | 439 | - | 0 | yes |
| path-16384 | triangles | `grust` | first | counted | - | 2.176 | 0.016 | 0.008 | - | 5.37 | - | needed | 358 | 805 | 425970 | 0 | yes |
| path-16384 | triangles | `grust` | second | counted | - | 0.974 | 0.016 | 0.017 | - | 5.37 | - | needed | 2 | 805 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted` | first | counted | - | 1.534 | 0.005 | 0.003 | - | 5.62 | - | needed | 257 | 854 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted` | second | counted | - | 1.389 | 0.015 | 0.011 | - | 5.62 | - | needed | 256 | 854 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@work-uncounted` | first | work-uncounted | - | 1.373 | 0.015 | 0.011 | - | 4.97 | - | needed | 256 | 854 | - | 0 | yes |
| path-16384 | triangles | `grust-next@work-uncounted` | second | work-uncounted | - | 1.198 | 0.018 | 0.015 | - | 4.97 | - | needed | 256 | 854 | - | 0 | yes |
| path-16384 | triangles | `grust-next@unchecked` | first | unchecked | - | 1.315 | 0.011 | 0.009 | - | 4.92 | - | needed | 256 | 855 | - | 0 | yes |
| path-16384 | triangles | `grust-next@unchecked` | second | unchecked | - | 1.165 | 0.016 | 0.014 | - | 4.92 | - | needed | 256 | 855 | - | 0 | yes |
| path-16384 | triangles | `grust-next@counted+eager` | first | counted | - | 1.560 | 0.025 | 0.016 | - | 5.57 | 0.00 | always | 257 | 853 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted+eager` | second | counted | - | 1.396 | 0.031 | 0.022 | - | 5.57 | 0.00 | always | 256 | 853 | 425970 | 0 | yes |
| path-16384 | wcc | `neo4j-graph` |  |  | - | 0.845 | 0.017 | 0.020 | - | 2.16 | - |  | 47 | 438 | - | 0 | yes |
| path-16384 | wcc | `icebug` |  |  | - | 0.353 | 0.002 | 0.006 | - | 1.80 | - |  | 42 | 450 | - | 0 | yes |
| path-16384 | wcc | `icecat` |  |  | - | 0.280 | 0.001 | 0.005 | - | 0.94 | - |  | 64 | 274 | - | 0 | yes |
| path-16384 | wcc | `grustcat` |  |  | - | 0.165 | 0.003 | 0.018 | - | 27.41 | - |  | 0 | 6429 | - | 0 | yes |
| path-16384 | wcc | `grust` | first | counted | - | 1.001 | 0.006 | 0.006 | - | 5.23 | - | needed | 137 | 741 | 229369 | 0 | yes |
| path-16384 | wcc | `grust` | second | counted | - | 0.300 | 0.000 | 0.001 | - | 5.23 | - | needed | 33 | 741 | 229369 | 0 | yes |
| path-16384 | wcc | `grust-next@counted` | first | counted | - | 0.311 | 0.008 | 0.025 | - | 5.43 | - | needed | 35 | 790 | 229369 | 0 | yes |
| path-16384 | wcc | `grust-next@counted` | second | counted | - | 0.300 | 0.019 | 0.063 | - | 5.43 | - | needed | 17 | 790 | 229369 | 0 | yes |
| path-16384 | wcc | `grust-next@work-uncounted` | first | work-uncounted | - | 0.282 | 0.001 | 0.005 | - | 4.81 | - | needed | 34 | 790 | - | 0 | yes |
| path-16384 | wcc | `grust-next@work-uncounted` | second | work-uncounted | - | 0.154 | 0.005 | 0.032 | - | 4.81 | - | needed | 2 | 790 | - | 0 | yes |
| path-16384 | wcc | `grust-next@unchecked` | first | unchecked | - | 0.270 | 0.012 | 0.046 | - | 4.71 | - | needed | 36 | 789 | - | 0 | yes |
| path-16384 | wcc | `grust-next@unchecked` | second | unchecked | - | 0.158 | 0.011 | 0.071 | - | 4.71 | - | needed | 2 | 789 | - | 0 | yes |
| path-16384 | wcc | `grust-next@counted+eager` | first | counted | - | 0.324 | 0.017 | 0.051 | - | 6.20 | 0.65 | always | 35 | 854 | 327671 | 0 | yes |
| path-16384 | wcc | `grust-next@counted+eager` | second | counted | - | 0.334 | 0.009 | 0.028 | - | 6.20 | 0.65 | always | 33 | 854 | 327671 | 0 | yes |
| path-65536 | bfs | `icebug` |  |  | - | 1.074 | 0.021 | 0.019 | - | 7.22 | - |  | 132 | 1795 | - | 0 | yes |
| path-65536 | bfs | `icecat` |  |  | - | 1.214 | 0.014 | 0.011 | - | 4.51 | - |  | 257 | 1139 | - | 0 | yes |
| path-65536 | bfs | `grustcat` |  |  | - | 0.591 | 0.008 | 0.013 | - | 114.28 | - |  | 0 | 24215 | - | 0 | yes |
| path-65536 | bfs | `grust` | first | counted | - | 1.704 | 0.026 | 0.016 | - | 24.61 | - | needed | 144 | 2486 | 983035 | 0 | yes |
| path-65536 | bfs | `grust` | second | counted | - | 1.374 | 0.009 | 0.006 | - | 24.61 | - | needed | 0 | 2486 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@counted` | first | counted | - | 1.626 | 0.005 | 0.003 | - | 21.44 | - | needed | 128 | 2374 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@counted` | second | counted | - | 1.324 | 0.004 | 0.003 | - | 21.44 | - | needed | 0 | 2374 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@work-uncounted` | first | work-uncounted | - | 0.905 | 0.007 | 0.008 | - | 18.07 | - | needed | 128 | 2376 | - | 0 | yes |
| path-65536 | bfs | `grust-next@work-uncounted` | second | work-uncounted | - | 0.603 | 0.000 | 0.001 | - | 18.07 | - | needed | 0 | 2376 | - | 0 | yes |
| path-65536 | bfs | `grust-next@unchecked` | first | unchecked | - | 0.774 | 0.003 | 0.003 | - | 18.49 | - | needed | 128 | 2378 | - | 0 | yes |
| path-65536 | bfs | `grust-next@unchecked` | second | unchecked | - | 0.468 | 0.002 | 0.004 | - | 18.49 | - | needed | 0 | 2378 | - | 0 | yes |
| path-65536 | bfs | `grust-next@counted+eager` | first | counted | - | 1.607 | 0.004 | 0.002 | - | 23.27 | 2.07 | always | 128 | 2635 | 1376249 | 0 | yes |
| path-65536 | bfs | `grust-next@counted+eager` | second | counted | - | 1.313 | 0.005 | 0.004 | - | 23.27 | 2.07 | always | 0 | 2635 | 1376249 | 0 | yes |
| path-65536 | pagerank | `icebug` |  |  | 46 | 10.889 | 0.188 | 0.017 | 0.237 | 7.30 | - |  | 503 | 1795 | - | 0 | yes |
| path-65536 | pagerank | `icecat` |  |  | 50 | 39.459 | 0.237 | 0.006 | 0.789 | 4.61 | - |  | 606 | 1139 | - | 0 | yes |
| path-65536 | pagerank | `grustcat` |  |  | 50 | 34.056 | 0.071 | 0.002 | 0.681 | 115.18 | - |  | 0 | 24215 | - | 0 | yes |
| path-65536 | pagerank | `grust` | first | counted | 50 | 16.725 | 0.240 | 0.014 | 0.334 | 22.99 | - | needed | 755 | 2486 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust` | second | counted | 50 | 12.239 | 0.162 | 0.013 | 0.245 | 22.99 | - | needed | 2 | 2486 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted` | first | counted | 50 | 12.723 | 0.047 | 0.004 | 0.254 | 22.49 | 2.08 | needed | 407 | 2632 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted` | second | counted | 50 | 12.287 | 0.135 | 0.011 | 0.246 | 22.49 | 2.08 | needed | 353 | 2632 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 50 | 9.444 | 0.205 | 0.022 | 0.189 | 19.28 | 1.41 | needed | 403 | 2632 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 50 | 8.647 | 0.084 | 0.010 | 0.173 | 19.28 | 1.41 | needed | 354 | 2632 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@unchecked` | first | unchecked | 50 | 9.163 | 0.110 | 0.012 | 0.183 | 18.90 | 1.32 | needed | 403 | 3143 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@unchecked` | second | unchecked | 50 | 8.484 | 0.157 | 0.019 | 0.170 | 18.90 | 1.32 | needed | 356 | 3143 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@counted+eager` | first | counted | 50 | 12.277 | 0.006 | 0.000 | 0.246 | 22.12 | 2.08 | always | 403 | 2636 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted+eager` | second | counted | 50 | 12.054 | 0.057 | 0.005 | 0.241 | 22.12 | 2.08 | always | 354 | 2636 | 14352327 | 0 | yes |
| path-65536 | triangles | `neo4j-graph` |  |  | - | 0.801 | 0.030 | 0.038 | - | 4.94 | - |  | 29 | 1411 | - | 0 | yes |
| path-65536 | triangles | `grust` | first | counted | - | 6.352 | 0.042 | 0.007 | - | 24.25 | - | needed | 1127 | 2743 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust` | second | counted | - | 3.630 | 0.037 | 0.010 | - | 24.25 | - | needed | 1 | 2743 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted` | first | counted | - | 5.807 | 0.045 | 0.008 | - | 21.38 | - | needed | 1024 | 2630 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted` | second | counted | - | 5.543 | 0.082 | 0.015 | - | 21.38 | - | needed | 1120 | 2630 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@work-uncounted` | first | work-uncounted | - | 5.142 | 0.033 | 0.006 | - | 18.42 | - | needed | 1024 | 2631 | - | 0 | yes |
| path-65536 | triangles | `grust-next@work-uncounted` | second | work-uncounted | - | 4.957 | 0.022 | 0.004 | - | 18.42 | - | needed | 1120 | 2631 | - | 0 | yes |
| path-65536 | triangles | `grust-next@unchecked` | first | unchecked | - | 4.901 | 0.016 | 0.003 | - | 17.84 | - | needed | 1024 | 2631 | - | 0 | yes |
| path-65536 | triangles | `grust-next@unchecked` | second | unchecked | - | 4.612 | 0.014 | 0.003 | - | 17.84 | - | needed | 1120 | 2631 | - | 0 | yes |
| path-65536 | triangles | `grust-next@counted+eager` | first | counted | - | 5.821 | 0.027 | 0.005 | - | 21.08 | 0.00 | always | 1024 | 2630 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted+eager` | second | counted | - | 5.624 | 0.011 | 0.002 | - | 21.08 | 0.00 | always | 1120 | 2630 | 1703922 | 0 | yes |
| path-65536 | wcc | `neo4j-graph` |  |  | - | 2.246 | 0.022 | 0.010 | - | 4.83 | - |  | 231 | 1409 | - | 0 | yes |
| path-65536 | wcc | `icebug` |  |  | - | 1.351 | 0.020 | 0.015 | - | 7.32 | - |  | 137 | 1795 | - | 0 | yes |
| path-65536 | wcc | `icecat` |  |  | - | 1.154 | 0.013 | 0.012 | - | 4.55 | - |  | 256 | 1139 | - | 0 | yes |
| path-65536 | wcc | `grustcat` |  |  | - | 0.652 | 0.007 | 0.010 | - | 115.75 | - |  | 0 | 24215 | - | 0 | yes |
| path-65536 | wcc | `grust` | first | counted | - | 1.520 | 0.003 | 0.002 | - | 24.03 | - | needed | 241 | 2486 | 917497 | 0 | yes |
| path-65536 | wcc | `grust` | second | counted | - | 0.777 | 0.010 | 0.013 | - | 24.03 | - | needed | 132 | 2486 | 917497 | 0 | yes |
| path-65536 | wcc | `grust-next@counted` | first | counted | - | 0.823 | 0.009 | 0.011 | - | 20.58 | - | needed | 132 | 2377 | 917497 | 0 | yes |
| path-65536 | wcc | `grust-next@counted` | second | counted | - | 0.667 | 0.016 | 0.025 | - | 20.58 | - | needed | 68 | 2377 | 917497 | 0 | yes |
| path-65536 | wcc | `grust-next@work-uncounted` | first | work-uncounted | - | 0.651 | 0.002 | 0.004 | - | 18.33 | - | needed | 132 | 2378 | - | 0 | yes |
| path-65536 | wcc | `grust-next@work-uncounted` | second | work-uncounted | - | 0.380 | 0.017 | 0.046 | - | 18.33 | - | needed | 1 | 2378 | - | 0 | yes |
| path-65536 | wcc | `grust-next@unchecked` | first | unchecked | - | 0.634 | 0.004 | 0.007 | - | 17.09 | - | needed | 132 | 2374 | - | 0 | yes |
| path-65536 | wcc | `grust-next@unchecked` | second | unchecked | - | 0.380 | 0.007 | 0.018 | - | 17.09 | - | needed | 3 | 2374 | - | 0 | yes |
| path-65536 | wcc | `grust-next@counted+eager` | first | counted | - | 0.803 | 0.017 | 0.021 | - | 23.27 | 2.05 | always | 132 | 2636 | 1310711 | 0 | yes |
| path-65536 | wcc | `grust-next@counted+eager` | second | counted | - | 0.795 | 0.013 | 0.016 | - | 23.27 | 2.05 | always | 130 | 2636 | 1310711 | 0 | yes |
| uniform-16384 | bfs | `icebug` |  |  | - | 2.265 | 0.079 | 0.035 | - | 9.88 | - |  | 57 | 979 | - | 0 | yes |
| uniform-16384 | bfs | `icecat` |  |  | - | 0.937 | 0.013 | 0.014 | - | 6.79 | - |  | 97 | 1557 | - | 0 | yes |
| uniform-16384 | bfs | `grustcat` |  |  | - | 0.874 | 0.012 | 0.014 | - | 88.59 | - |  | 0 | 10030 | - | 0 | yes |
| uniform-16384 | bfs | `grust` | first | counted | - | 1.675 | 0.037 | 0.022 | - | 19.83 | - | needed | 36 | 1789 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust` | second | counted | - | 1.470 | 0.004 | 0.003 | - | 19.83 | - | needed | 0 | 1789 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted` | first | counted | - | 1.840 | 0.053 | 0.029 | - | 11.46 | - | needed | 0 | 1535 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted` | second | counted | - | 1.503 | 0.010 | 0.007 | - | 11.46 | - | needed | 0 | 1535 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@work-uncounted` | first | work-uncounted | - | 1.268 | 0.018 | 0.014 | - | 9.56 | - | needed | 0 | 2040 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@work-uncounted` | second | work-uncounted | - | 0.912 | 0.019 | 0.021 | - | 9.56 | - | needed | 0 | 2040 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@unchecked` | first | unchecked | - | 1.112 | 0.033 | 0.030 | - | 8.91 | - | needed | 0 | 1536 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@unchecked` | second | unchecked | - | 0.847 | 0.015 | 0.018 | - | 8.91 | - | needed | 0 | 1536 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted+eager` | first | counted | - | 1.602 | 0.008 | 0.005 | - | 13.01 | 1.64 | always | 0 | 2300 | 1490619 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted+eager` | second | counted | - | 1.488 | 0.006 | 0.004 | - | 13.01 | 1.64 | always | 0 | 2300 | 1490619 | 0 | yes |
| uniform-16384 | pagerank | `neo4j-graph` |  |  | 28 | 10.722 | 0.150 | 0.014 | 0.383 | 4.24 | - |  | 40 | 853 | - | 0 | yes |
| uniform-16384 | pagerank | `icebug` |  |  | 12 | 2.979 | 0.065 | 0.022 | 0.248 | 9.64 | - |  | 201 | 979 | - | 0 | yes |
| uniform-16384 | pagerank | `icecat` |  |  | 16 | 8.094 | 0.005 | 0.001 | 0.506 | 7.03 | - |  | 129 | 1557 | - | 0 | yes |
| uniform-16384 | pagerank | `grustcat` |  |  | 16 | 6.888 | 0.025 | 0.004 | 0.431 | 87.78 | - |  | 1 | 10031 | - | 0 | yes |
| uniform-16384 | pagerank | `grust` | first | counted | 16 | 6.283 | 0.130 | 0.021 | 0.393 | 19.74 | - | needed | 484 | 2300 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust` | second | counted | 16 | 3.299 | 0.048 | 0.014 | 0.206 | 19.74 | - | needed | 1 | 2300 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted` | first | counted | 16 | 3.365 | 0.071 | 0.021 | 0.210 | 12.98 | 1.70 | needed | 4 | 2302 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted` | second | counted | 16 | 3.327 | 0.126 | 0.038 | 0.208 | 12.98 | 1.70 | needed | 0 | 2302 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 16 | 2.749 | 0.031 | 0.011 | 0.172 | 11.10 | 1.46 | needed | 5 | 2302 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 16 | 2.660 | 0.034 | 0.013 | 0.166 | 11.10 | 1.46 | needed | 1 | 2302 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@unchecked` | first | unchecked | 16 | 2.782 | 0.026 | 0.009 | 0.174 | 10.96 | 1.46 | needed | 3 | 2303 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@unchecked` | second | unchecked | 16 | 2.601 | 0.002 | 0.001 | 0.163 | 10.96 | 1.46 | needed | 1 | 2303 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted+eager` | first | counted | 16 | 3.387 | 0.069 | 0.020 | 0.212 | 13.24 | 1.67 | always | 6 | 2302 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted+eager` | second | counted | 16 | 3.088 | 0.123 | 0.040 | 0.193 | 13.24 | 1.67 | always | 0 | 2302 | 4226299 | 0 | yes |
| uniform-16384 | triangles | `neo4j-graph` |  |  | - | 1.365 | 0.034 | 0.025 | - | 4.28 | - |  | 52 | 858 | - | 0 | yes |
| uniform-16384 | triangles | `grust` | first | counted | - | 9.179 | 0.096 | 0.010 | - | 23.28 | - | needed | 1031 | 2811 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust` | second | counted | - | 6.493 | 0.024 | 0.004 | - | 23.28 | - | needed | 1 | 2811 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted` | first | counted | - | 7.369 | 0.021 | 0.003 | - | 11.50 | - | needed | 257 | 1027 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted` | second | counted | - | 7.373 | 0.046 | 0.006 | - | 11.50 | - | needed | 512 | 1027 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@work-uncounted` | first | work-uncounted | - | 7.192 | 0.052 | 0.007 | - | 9.99 | - | needed | 257 | 1534 | - | 0 | yes |
| uniform-16384 | triangles | `grust-next@work-uncounted` | second | work-uncounted | - | 7.249 | 0.019 | 0.003 | - | 9.99 | - | needed | 512 | 1534 | - | 0 | yes |
| uniform-16384 | triangles | `grust-next@unchecked` | first | unchecked | - | 7.063 | 0.014 | 0.002 | - | 9.84 | - | needed | 257 | 1530 | - | 0 | yes |
| uniform-16384 | triangles | `grust-next@unchecked` | second | unchecked | - | 7.118 | 0.049 | 0.007 | - | 9.84 | - | needed | 512 | 1530 | - | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted+eager` | first | counted | - | 7.411 | 0.021 | 0.003 | - | 11.78 | 0.00 | always | 257 | 1536 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted+eager` | second | counted | - | 7.484 | 0.144 | 0.019 | - | 11.78 | 0.00 | always | 512 | 1536 | 3829630 | 0 | yes |
| uniform-16384 | wcc | `neo4j-graph` |  |  | - | 1.130 | 0.010 | 0.009 | - | 4.34 | - |  | 0 | 858 | - | 0 | yes |
| uniform-16384 | wcc | `icebug` |  |  | - | 3.057 | 0.019 | 0.006 | - | 9.93 | - |  | 69 | 979 | - | 0 | yes |
| uniform-16384 | wcc | `icecat` |  |  | - | 1.094 | 0.012 | 0.011 | - | 6.91 | - |  | 64 | 1558 | - | 0 | yes |
| uniform-16384 | wcc | `grustcat` |  |  | - | 0.757 | 0.005 | 0.006 | - | 90.41 | - |  | 0 | 10031 | - | 0 | yes |
| uniform-16384 | wcc | `grust` | first | counted | - | 1.506 | 0.042 | 0.028 | - | 20.51 | - | needed | 140 | 2299 | 1031992 | 0 | yes |
| uniform-16384 | wcc | `grust` | second | counted | - | 0.677 | 0.009 | 0.014 | - | 20.51 | - | needed | 35 | 2299 | 1031992 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted` | first | counted | - | 0.601 | 0.014 | 0.023 | - | 10.94 | - | needed | 4 | 1534 | 1031986 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted` | second | counted | - | 0.595 | 0.014 | 0.023 | - | 10.94 | - | needed | 1 | 1534 | 1031986 | 0 | yes |
| uniform-16384 | wcc | `grust-next@work-uncounted` | first | work-uncounted | - | 0.538 | 0.041 | 0.075 | - | 9.55 | - | needed | 3 | 2044 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@work-uncounted` | second | work-uncounted | - | 0.476 | 0.005 | 0.010 | - | 9.55 | - | needed | 1 | 2044 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@unchecked` | first | unchecked | - | 0.562 | 0.011 | 0.019 | - | 9.57 | - | needed | 3 | 2043 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@unchecked` | second | unchecked | - | 0.528 | 0.052 | 0.099 | - | 9.57 | - | needed | 1 | 2043 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted+eager` | first | counted | - | 0.567 | 0.006 | 0.010 | - | 13.16 | 1.68 | always | 4 | 2301 | 1474283 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted+eager` | second | counted | - | 0.569 | 0.016 | 0.028 | - | 13.16 | 1.68 | always | 1 | 2301 | 1474283 | 0 | yes |
| uniform-65536 | bfs | `icebug` |  |  | - | 15.580 | 0.461 | 0.030 | - | 63.02 | - |  | 216 | 3889 | - | 0 | yes |
| uniform-65536 | bfs | `icecat` |  |  | - | 5.657 | 0.084 | 0.015 | - | 20.94 | - |  | 386 | 1665 | - | 0 | yes |
| uniform-65536 | bfs | `grustcat` |  |  | - | 5.996 | 0.181 | 0.030 | - | 475.84 | - |  | 0 | 37597 | - | 0 | yes |
| uniform-65536 | bfs | `grust` | first | counted | - | 4.432 | 0.131 | 0.030 | - | 107.86 | - | needed | 315 | 3107 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust` | second | counted | - | 3.330 | 0.072 | 0.022 | - | 107.86 | - | needed | 153 | 3107 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted` | first | counted | - | 3.416 | 0.042 | 0.012 | - | 39.28 | - | needed | 116 | 2774 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted` | second | counted | - | 3.118 | 0.007 | 0.002 | - | 39.28 | - | needed | 73 | 2774 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@work-uncounted` | first | work-uncounted | - | 3.326 | 0.063 | 0.019 | - | 32.86 | - | needed | 123 | 2772 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@work-uncounted` | second | work-uncounted | - | 2.908 | 0.018 | 0.006 | - | 32.86 | - | needed | 72 | 2772 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@unchecked` | first | unchecked | - | 3.416 | 0.045 | 0.013 | - | 32.45 | - | needed | 114 | 2774 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@unchecked` | second | unchecked | - | 3.096 | 0.025 | 0.008 | - | 32.45 | - | needed | 77 | 2774 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted+eager` | first | counted | - | 3.087 | 0.020 | 0.006 | - | 44.75 | 5.24 | always | 129 | 3284 | 5963146 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted+eager` | second | counted | - | 3.154 | 0.049 | 0.015 | - | 44.75 | 5.24 | always | 79 | 3284 | 5963146 | 0 | yes |
| uniform-65536 | pagerank | `neo4j-graph` |  |  | 34 | 16.417 | 0.120 | 0.007 | 0.483 | 14.46 | - |  | 95 | 1874 | - | 0 | yes |
| uniform-65536 | pagerank | `icebug` |  |  | 11 | 8.565 | 0.438 | 0.051 | 0.779 | 64.11 | - |  | 489 | 3889 | - | 0 | yes |
| uniform-65536 | pagerank | `icecat` |  |  | 16 | 33.593 | 0.132 | 0.004 | 2.100 | 21.49 | - |  | 607 | 1480 | - | 0 | yes |
| uniform-65536 | pagerank | `grustcat` |  |  | 16 | 31.891 | 0.821 | 0.026 | 1.993 | 475.67 | - |  | 0 | 38108 | - | 0 | yes |
| uniform-65536 | pagerank | `grust` | first | counted | 16 | 18.838 | 0.167 | 0.009 | 1.177 | 106.46 | - | needed | 1132 | 3107 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust` | second | counted | 16 | 8.402 | 0.075 | 0.009 | 0.525 | 106.46 | - | needed | 4 | 3107 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted` | first | counted | 16 | 7.016 | 0.088 | 0.013 | 0.438 | 44.90 | 5.36 | needed | 17 | 3286 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted` | second | counted | 16 | 6.772 | 0.137 | 0.020 | 0.423 | 44.90 | 5.36 | needed | 4 | 3286 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 16 | 4.585 | 0.025 | 0.005 | 0.287 | 37.53 | 4.67 | needed | 12 | 3286 | - | 0 | yes |
| uniform-65536 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 16 | 4.567 | 0.049 | 0.011 | 0.285 | 37.53 | 4.67 | needed | 4 | 3286 | - | 0 | yes |
| uniform-65536 | pagerank | `grust-next@unchecked` | first | unchecked | 16 | 4.523 | 0.104 | 0.023 | 0.283 | 38.38 | 4.63 | needed | 13 | 3286 | - | 0 | yes |
| uniform-65536 | pagerank | `grust-next@unchecked` | second | unchecked | 16 | 4.443 | 0.138 | 0.031 | 0.278 | 38.38 | 4.63 | needed | 3 | 3286 | - | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted+eager` | first | counted | 16 | 6.871 | 0.228 | 0.033 | 0.429 | 46.25 | 5.49 | always | 15 | 4306 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted+eager` | second | counted | 16 | 6.718 | 0.285 | 0.042 | 0.420 | 46.25 | 5.49 | always | 4 | 4306 | 16907315 | 0 | yes |
| uniform-65536 | triangles | `neo4j-graph` |  |  | - | 4.060 | 0.118 | 0.029 | - | 14.56 | - |  | 52 | 1873 | - | 0 | yes |
| uniform-65536 | triangles | `grust` | first | counted | - | 33.079 | 0.213 | 0.006 | - | 131.22 | - | needed | 1770 | 2600 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust` | second | counted | - | 26.562 | 0.068 | 0.003 | - | 131.22 | - | needed | 1 | 2600 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted` | first | counted | - | 28.921 | 0.124 | 0.004 | - | 44.66 | - | needed | 517 | 2266 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted` | second | counted | - | 28.660 | 0.486 | 0.017 | - | 44.66 | - | needed | 1026 | 2266 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@work-uncounted` | first | work-uncounted | - | 28.126 | 0.241 | 0.009 | - | 37.28 | - | needed | 517 | 2266 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@work-uncounted` | second | work-uncounted | - | 27.924 | 0.477 | 0.017 | - | 37.28 | - | needed | 1026 | 2266 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@unchecked` | first | unchecked | - | 28.276 | 0.058 | 0.002 | - | 37.32 | - | needed | 517 | 1759 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@unchecked` | second | unchecked | - | 27.952 | 0.165 | 0.006 | - | 37.32 | - | needed | 1026 | 1759 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted+eager` | first | counted | - | 29.188 | 0.119 | 0.004 | - | 44.24 | 0.00 | always | 517 | 1757 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted+eager` | second | counted | - | 28.539 | 0.015 | 0.001 | - | 44.24 | 0.00 | always | 1026 | 1757 | 15327135 | 0 | yes |
| uniform-65536 | wcc | `neo4j-graph` |  |  | - | 3.610 | 0.166 | 0.046 | - | 14.30 | - |  | 224 | 1876 | - | 0 | yes |
| uniform-65536 | wcc | `icebug` |  |  | - | 23.604 | 1.149 | 0.049 | - | 53.74 | - |  | 244 | 3889 | - | 0 | yes |
| uniform-65536 | wcc | `icecat` |  |  | - | 4.148 | 0.180 | 0.043 | - | 20.94 | - |  | 105 | 1531 | - | 0 | yes |
| uniform-65536 | wcc | `grustcat` |  |  | - | 3.114 | 0.036 | 0.012 | - | 475.83 | - |  | 0 | 37598 | - | 0 | yes |
| uniform-65536 | wcc | `grust` | first | counted | - | 2.679 | 0.059 | 0.022 | - | 102.94 | - | needed | 241 | 2596 | 4128513 | 0 | yes |
| uniform-65536 | wcc | `grust` | second | counted | - | 2.005 | 0.105 | 0.052 | - | 102.94 | - | needed | 131 | 2596 | 4128513 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted` | first | counted | - | 1.909 | 0.109 | 0.057 | - | 39.47 | - | needed | 6 | 2772 | 4128522 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted` | second | counted | - | 1.841 | 0.164 | 0.089 | - | 39.47 | - | needed | 1 | 2772 | 4128522 | 0 | yes |
| uniform-65536 | wcc | `grust-next@work-uncounted` | first | work-uncounted | - | 1.544 | 0.106 | 0.069 | - | 32.15 | - | needed | 5 | 2777 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@work-uncounted` | second | work-uncounted | - | 1.726 | 0.021 | 0.012 | - | 32.15 | - | needed | 2 | 2777 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@unchecked` | first | unchecked | - | 1.722 | 0.055 | 0.032 | - | 33.07 | - | needed | 4 | 2774 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@unchecked` | second | unchecked | - | 2.004 | 0.220 | 0.110 | - | 33.07 | - | needed | 1 | 2774 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted+eager` | first | counted | - | 1.734 | 0.010 | 0.006 | - | 45.70 | 5.46 | always | 3 | 3287 | 5897871 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted+eager` | second | counted | - | 1.789 | 0.072 | 0.040 | - | 45.70 | 5.46 | always | 1 | 3287 | 5897871 | 0 | yes |

### `pinned-one-thread.json`: pinned-one-thread

workers 1, concurrency 1, allocator pinned: glibc.malloc.mmap_threshold=131072, 1 warmup + 5 repeats, steal over the run 1 ticks, 153.5 s, unusable at MAD/median >= 0.25

Not timed (no agreeing parity row): neo4j-graph pagerank layered-16384.edges, neo4j-graph pagerank layered-65536.edges, neo4j-graph pagerank path-16384.edges, neo4j-graph pagerank path-65536.edges 

| fixture | algorithm | participant | call | accounting | iters | total ms | MAD | MAD/median | per iter | build ms | incoming ms | prepare | minflt | minflt build | work units | steal | usable |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |
| hub-16384 | bfs | `icebug` |  |  | - | 2.239 | 0.048 | 0.021 | - | 10.40 | - |  | 57 | 1018 | - | 0 | yes |
| hub-16384 | bfs | `icecat` |  |  | - | 0.928 | 0.016 | 0.017 | - | 6.75 | - |  | 100 | 2082 | - | 0 | yes |
| hub-16384 | bfs | `grustcat` |  |  | - | 0.796 | 0.020 | 0.025 | - | 92.41 | - |  | 34 | 10355 | - | 0 | yes |
| hub-16384 | bfs | `grust#1` | first | counted | - | 1.657 | 0.015 | 0.009 | - | 20.90 | - | needed | 69 | 1792 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust#1` | second | counted | - | 1.812 | 0.010 | 0.005 | - | 20.90 | - | needed | 33 | 1792 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust#unset` | first | counted | - | 1.658 | 0.011 | 0.007 | - | 20.52 | - | needed | 69 | 1777 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust#unset` | second | counted | - | 1.527 | 0.007 | 0.005 | - | 20.52 | - | needed | 33 | 1777 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted#1` | first | counted | - | 1.637 | 0.011 | 0.007 | - | 10.91 | - | needed | 33 | 1741 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted#1` | second | counted | - | 1.554 | 0.009 | 0.006 | - | 10.91 | - | needed | 33 | 1741 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted#unset` | first | counted | - | 1.705 | 0.016 | 0.009 | - | 13.04 | - | needed | 69 | 1217 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted#unset` | second | counted | - | 1.562 | 0.019 | 0.012 | - | 13.04 | - | needed | 33 | 1217 | 1047577 | 0 | yes |
| hub-16384 | pagerank | `neo4j-graph` |  |  | 36 | 13.287 | 0.116 | 0.009 | 0.369 | 8.03 | - |  | 24 | 717 | - | 0 | yes |
| hub-16384 | pagerank | `icebug` |  |  | 12 | 7.863 | 0.103 | 0.013 | 0.655 | 9.84 | - |  | 107 | 1018 | - | 0 | yes |
| hub-16384 | pagerank | `icecat` |  |  | 17 | 8.728 | 0.017 | 0.002 | 0.513 | 6.62 | - |  | 230 | 2083 | - | 0 | yes |
| hub-16384 | pagerank | `grustcat` |  |  | 17 | 7.538 | 0.007 | 0.001 | 0.443 | 92.88 | - |  | 99 | 10864 | - | 0 | yes |
| hub-16384 | pagerank | `grust#1` | first | counted | 17 | 11.728 | 0.035 | 0.003 | 0.690 | 19.56 | - | needed | 421 | 2303 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust#1` | second | counted | 17 | 9.850 | 0.020 | 0.002 | 0.579 | 19.56 | - | needed | 99 | 2303 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust#unset` | first | counted | 17 | 50.925 | 0.099 | 0.002 | 2.996 | 20.12 | - | needed | 165 | 1777 | 4567562 | 0 | yes |
| hub-16384 | pagerank | `grust#unset` | second | counted | 17 | 50.729 | 0.039 | 0.001 | 2.984 | 20.12 | - | needed | 165 | 1777 | 4567562 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted#1` | first | counted | 17 | 8.264 | 0.009 | 0.001 | 0.486 | 12.38 | 1.53 | needed | 99 | 2030 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted#1` | second | counted | 17 | 8.167 | 0.014 | 0.002 | 0.480 | 12.38 | 1.53 | needed | 99 | 2030 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted#unset` | first | counted | 17 | 23.595 | 0.010 | 0.000 | 1.388 | 12.93 | - | needed | 165 | 1216 | 4567562 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted#unset` | second | counted | 17 | 23.530 | 0.069 | 0.003 | 1.384 | 12.93 | - | needed | 165 | 1216 | 4567562 | 0 | yes |
| hub-16384 | triangles | `neo4j-graph` |  |  | - | 7.729 | 0.006 | 0.001 | - | 8.35 | - |  | 3 | 717 | - | 0 | yes |
| hub-16384 | triangles | `grust#1` | first | counted | - | 17.318 | 0.032 | 0.002 | - | 24.12 | - | needed | 456 | 1282 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust#1` | second | counted | - | 17.133 | 0.088 | 0.005 | - | 24.12 | - | needed | 455 | 1282 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust#unset` | first | counted | - | 17.247 | 0.040 | 0.002 | - | 23.57 | - | needed | 455 | 1268 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust#unset` | second | counted | - | 17.202 | 0.143 | 0.008 | - | 23.57 | - | needed | 455 | 1268 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted#1` | first | counted | - | 16.895 | 0.088 | 0.005 | - | 13.56 | - | needed | 422 | 721 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted#1` | second | counted | - | 16.593 | 0.129 | 0.008 | - | 13.56 | - | needed | 422 | 721 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted#unset` | first | counted | - | 17.017 | 0.085 | 0.005 | - | 17.81 | - | needed | 455 | 1217 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted#unset` | second | counted | - | 16.802 | 0.188 | 0.011 | - | 17.81 | - | needed | 455 | 1217 | 3742208 | 0 | yes |
| hub-16384 | wcc | `neo4j-graph` |  |  | - | 1.226 | 0.009 | 0.007 | - | 8.10 | - |  | 99 | 717 | - | 0 | yes |
| hub-16384 | wcc | `icebug` |  |  | - | 2.585 | 0.194 | 0.075 | - | 9.85 | - |  | 68 | 1018 | - | 0 | yes |
| hub-16384 | wcc | `icecat` |  |  | - | 0.935 | 0.012 | 0.013 | - | 6.54 | - |  | 66 | 1572 | - | 0 | yes |
| hub-16384 | wcc | `grustcat` |  |  | - | 0.614 | 0.002 | 0.003 | - | 92.89 | - |  | 0 | 10354 | - | 0 | yes |
| hub-16384 | wcc | `grust#1` | first | counted | - | 1.642 | 0.022 | 0.014 | - | 19.85 | - | needed | 66 | 2303 | 1031191 | 0 | yes |
| hub-16384 | wcc | `grust#1` | second | counted | - | 1.616 | 0.003 | 0.002 | - | 19.85 | - | needed | 66 | 2303 | 1031191 | 0 | yes |
| hub-16384 | wcc | `grust#unset` | first | counted | - | 4.263 | 0.002 | 0.001 | - | 19.10 | - | needed | 66 | 1777 | 1324773 | 0 | yes |
| hub-16384 | wcc | `grust#unset` | second | counted | - | 4.232 | 0.006 | 0.002 | - | 19.10 | - | needed | 66 | 1777 | 1324773 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted#1` | first | counted | - | 1.508 | 0.005 | 0.003 | - | 10.40 | - | needed | 33 | 1232 | 1031191 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted#1` | second | counted | - | 1.563 | 0.008 | 0.005 | - | 10.40 | - | needed | 66 | 1232 | 1031191 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted#unset` | first | counted | - | 4.200 | 0.008 | 0.002 | - | 13.22 | - | needed | 66 | 1217 | 1324773 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted#unset` | second | counted | - | 4.184 | 0.017 | 0.004 | - | 13.22 | - | needed | 66 | 1217 | 1324773 | 0 | yes |
| hub-65536 | bfs | `icebug` |  |  | - | 14.899 | 0.335 | 0.023 | - | 63.27 | - |  | 216 | 4057 | - | 1 | yes |
| hub-65536 | bfs | `icecat` |  |  | - | 4.864 | 0.019 | 0.004 | - | 21.75 | - |  | 388 | 2698 | - | 1 | yes |
| hub-65536 | bfs | `grustcat` |  |  | - | 5.801 | 0.068 | 0.012 | - | 486.72 | - |  | 129 | 38258 | - | 1 | yes |
| hub-65536 | bfs | `grust#1` | first | counted | - | 8.414 | 0.146 | 0.017 | - | 107.88 | - | needed | 420 | 2596 | 4191009 | 1 | yes |
| hub-65536 | bfs | `grust#1` | second | counted | - | 6.808 | 0.025 | 0.004 | - | 107.88 | - | needed | 372 | 2596 | 4191009 | 1 | yes |
| hub-65536 | bfs | `grust#unset` | first | counted | - | 9.943 | 0.359 | 0.036 | - | 111.36 | - | needed | 274 | 2581 | 4191009 | 1 | yes |
| hub-65536 | bfs | `grust#unset` | second | counted | - | 8.716 | 0.340 | 0.039 | - | 111.36 | - | needed | 274 | 2581 | 4191009 | 1 | yes |
| hub-65536 | bfs | `grust-next@counted#1` | first | counted | - | 8.081 | 0.428 | 0.053 | - | 43.49 | - | needed | 435 | 1907 | 4191009 | 1 | yes |
| hub-65536 | bfs | `grust-next@counted#1` | second | counted | - | 7.127 | 0.370 | 0.052 | - | 43.49 | - | needed | 372 | 1907 | 4191009 | 1 | yes |
| hub-65536 | bfs | `grust-next@counted#unset` | first | counted | - | 10.002 | 0.855 | 0.085 | - | 53.62 | - | needed | 258 | 1842 | 4191009 | 1 | yes |
| hub-65536 | bfs | `grust-next@counted#unset` | second | counted | - | 8.278 | 0.524 | 0.063 | - | 53.62 | - | needed | 274 | 1842 | 4191009 | 1 | yes |
| hub-65536 | pagerank | `neo4j-graph` |  |  | 28 | 36.960 | 0.323 | 0.009 | 1.320 | 41.88 | - |  | 138 | 1299 | - | 0 | yes |
| hub-65536 | pagerank | `icebug` |  |  | 12 | 71.567 | 2.806 | 0.039 | 5.964 | 60.45 | - |  | 400 | 4057 | - | 0 | yes |
| hub-65536 | pagerank | `icecat` |  |  | 17 | 35.376 | 0.278 | 0.008 | 2.081 | 21.78 | - |  | 902 | 2698 | - | 0 | yes |
| hub-65536 | pagerank | `grustcat` |  |  | 17 | 33.162 | 0.940 | 0.028 | 1.951 | 479.03 | - |  | 388 | 38258 | - | 0 | yes |
| hub-65536 | pagerank | `grust#1` | first | counted | 17 | 61.098 | 1.368 | 0.022 | 3.594 | 108.88 | - | needed | 647 | 2597 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust#1` | second | counted | 17 | 50.703 | 1.402 | 0.028 | 2.983 | 108.88 | - | needed | 387 | 2597 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust#unset` | first | counted | 17 | 205.584 | 0.102 | 0.000 | 12.093 | 100.63 | - | needed | 645 | 2581 | 18272770 | 0 | yes |
| hub-65536 | pagerank | `grust#unset` | second | counted | 17 | 205.485 | 0.548 | 0.003 | 12.087 | 100.63 | - | needed | 645 | 2581 | 18272770 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted#1` | first | counted | 17 | 35.065 | 0.293 | 0.008 | 2.063 | 49.41 | 6.48 | needed | 516 | 2232 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted#1` | second | counted | 17 | 34.901 | 0.942 | 0.027 | 2.053 | 49.41 | 6.48 | needed | 516 | 2232 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted#unset` | first | counted | 17 | 96.056 | 0.107 | 0.001 | 5.650 | 53.74 | - | needed | 645 | 1843 | 18272770 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted#unset` | second | counted | 17 | 95.938 | 0.207 | 0.002 | 5.643 | 53.74 | - | needed | 645 | 1843 | 18272770 | 0 | yes |
| hub-65536 | triangles | `neo4j-graph` |  |  | - | 38.001 | 1.117 | 0.029 | - | 41.17 | - |  | 4 | 1299 | - | 0 | yes |
| hub-65536 | triangles | `grust#1` | first | counted | - | 79.442 | 0.642 | 0.008 | - | 134.94 | - | needed | 1290 | 3620 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust#1` | second | counted | - | 78.986 | 1.637 | 0.021 | - | 134.94 | - | needed | 1290 | 3620 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust#unset` | first | counted | - | 79.732 | 0.716 | 0.009 | - | 137.10 | - | needed | 1290 | 3605 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust#unset` | second | counted | - | 79.736 | 1.878 | 0.024 | - | 137.10 | - | needed | 1290 | 3605 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted#1` | first | counted | - | 80.011 | 0.854 | 0.011 | - | 60.56 | - | needed | 1290 | 2932 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted#1` | second | counted | - | 80.047 | 0.403 | 0.005 | - | 60.56 | - | needed | 1290 | 2932 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted#unset` | first | counted | - | 76.902 | 1.823 | 0.024 | - | 88.97 | - | needed | 1290 | 3377 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted#unset` | second | counted | - | 76.778 | 0.902 | 0.012 | - | 88.97 | - | needed | 1290 | 3377 | 14971727 | 0 | yes |
| hub-65536 | wcc | `neo4j-graph` |  |  | - | 4.580 | 0.019 | 0.004 | - | 46.74 | - |  | 394 | 1299 | - | 0 | yes |
| hub-65536 | wcc | `icebug` |  |  | - | 21.161 | 0.538 | 0.025 | - | 62.65 | - |  | 239 | 4057 | - | 0 | yes |
| hub-65536 | wcc | `icecat` |  |  | - | 3.783 | 0.014 | 0.004 | - | 22.01 | - |  | 258 | 2698 | - | 0 | yes |
| hub-65536 | wcc | `grustcat` |  |  | - | 2.524 | 0.015 | 0.006 | - | 490.35 | - |  | 0 | 38258 | - | 0 | yes |
| hub-65536 | wcc | `grust#1` | first | counted | - | 7.256 | 0.004 | 0.001 | - | 103.31 | - | needed | 258 | 2596 | 4125471 | 0 | yes |
| hub-65536 | wcc | `grust#1` | second | counted | - | 7.163 | 0.022 | 0.003 | - | 103.31 | - | needed | 258 | 2596 | 4125471 | 0 | yes |
| hub-65536 | wcc | `grust#unset` | first | counted | - | 17.440 | 0.039 | 0.002 | - | 104.73 | - | needed | 258 | 2581 | 5303155 | 0 | yes |
| hub-65536 | wcc | `grust#unset` | second | counted | - | 17.232 | 0.023 | 0.001 | - | 104.73 | - | needed | 258 | 2581 | 5303155 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted#1` | first | counted | - | 7.201 | 0.007 | 0.001 | - | 41.70 | - | needed | 258 | 1907 | 4125471 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted#1` | second | counted | - | 7.079 | 0.030 | 0.004 | - | 41.70 | - | needed | 258 | 1907 | 4125471 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted#unset` | first | counted | - | 17.279 | 0.064 | 0.004 | - | 53.62 | - | needed | 258 | 1842 | 5303155 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted#unset` | second | counted | - | 17.137 | 0.051 | 0.003 | - | 53.62 | - | needed | 258 | 1842 | 5303155 | 0 | yes |
| layered-16384 | bfs | `icebug` |  |  | - | 0.564 | 0.012 | 0.020 | - | 2.83 | - |  | 36 | 458 | - | 0 | yes |
| layered-16384 | bfs | `icecat` |  |  | - | 0.396 | 0.003 | 0.008 | - | 1.79 | - |  | 67 | 544 | - | 0 | yes |
| layered-16384 | bfs | `grustcat` |  |  | - | 0.256 | 0.003 | 0.012 | - | 33.43 | - |  | 0 | 7383 | - | 0 | yes |
| layered-16384 | bfs | `grust#1` | first | counted | - | 0.531 | 0.007 | 0.014 | - | 7.10 | - | needed | 62 | 1036 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust#1` | second | counted | - | 0.509 | 0.001 | 0.003 | - | 7.10 | - | needed | 26 | 1036 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust#unset` | first | counted | - | 0.521 | 0.005 | 0.010 | - | 7.01 | - | needed | 62 | 1021 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust#unset` | second | counted | - | 0.436 | 0.000 | 0.001 | - | 7.01 | - | needed | 26 | 1021 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted#1` | first | counted | - | 0.470 | 0.001 | 0.002 | - | 5.48 | - | needed | 26 | 908 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted#1` | second | counted | - | 0.440 | 0.005 | 0.011 | - | 5.48 | - | needed | 26 | 908 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted#unset` | first | counted | - | 0.530 | 0.006 | 0.012 | - | 6.27 | - | needed | 61 | 894 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted#unset` | second | counted | - | 0.433 | 0.002 | 0.005 | - | 6.27 | - | needed | 26 | 894 | 347308 | 0 | yes |
| layered-16384 | pagerank | `icebug` |  |  | 69 | 26.498 | 0.045 | 0.002 | 0.384 | 2.84 | - |  | 114 | 458 | - | 0 | yes |
| layered-16384 | pagerank | `icecat` |  |  | 84 | 27.918 | 0.032 | 0.001 | 0.332 | 1.80 | - |  | 228 | 543 | - | 0 | yes |
| layered-16384 | pagerank | `grustcat` |  |  | 84 | 26.361 | 0.036 | 0.001 | 0.314 | 33.71 | - |  | 33 | 7383 | - | 0 | yes |
| layered-16384 | pagerank | `grust#1` | first | counted | 84 | 30.139 | 0.047 | 0.002 | 0.359 | 7.16 | - | needed | 229 | 1036 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust#1` | second | counted | 84 | 29.291 | 0.011 | 0.000 | 0.349 | 7.16 | - | needed | 99 | 1036 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust#unset` | first | counted | 84 | 115.724 | 0.150 | 0.001 | 1.378 | 7.14 | - | needed | 165 | 1021 | 8667337 | 0 | yes |
| layered-16384 | pagerank | `grust#unset` | second | counted | 84 | 115.565 | 0.146 | 0.001 | 1.376 | 7.14 | - | needed | 165 | 1021 | 8667337 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted#1` | first | counted | 84 | 30.920 | 0.142 | 0.005 | 0.368 | 6.07 | 0.56 | needed | 99 | 1004 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted#1` | second | counted | 84 | 30.763 | 0.066 | 0.002 | 0.366 | 6.07 | 0.56 | needed | 99 | 1004 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted#unset` | first | counted | 84 | 89.114 | 0.035 | 0.000 | 1.061 | 6.18 | - | needed | 165 | 894 | 8667337 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted#unset` | second | counted | 84 | 89.058 | 0.069 | 0.001 | 1.060 | 6.18 | - | needed | 165 | 894 | 8667337 | 0 | yes |
| layered-16384 | triangles | `neo4j-graph` |  |  | - | 0.817 | 0.016 | 0.019 | - | 2.42 | - |  | 4 | 459 | - | 0 | yes |
| layered-16384 | triangles | `grust#1` | first | counted | - | 3.039 | 0.013 | 0.004 | - | 7.43 | - | needed | 389 | 1162 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust#1` | second | counted | - | 2.890 | 0.022 | 0.008 | - | 7.43 | - | needed | 389 | 1162 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust#unset` | first | counted | - | 3.061 | 0.017 | 0.006 | - | 7.41 | - | needed | 389 | 1147 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust#unset` | second | counted | - | 2.878 | 0.013 | 0.005 | - | 7.41 | - | needed | 389 | 1147 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted#1` | first | counted | - | 2.891 | 0.014 | 0.005 | - | 5.88 | - | needed | 356 | 1034 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted#1` | second | counted | - | 2.714 | 0.004 | 0.002 | - | 5.88 | - | needed | 356 | 1034 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted#unset` | first | counted | - | 2.970 | 0.016 | 0.005 | - | 6.68 | - | needed | 389 | 1020 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted#unset` | second | counted | - | 2.790 | 0.003 | 0.001 | - | 6.68 | - | needed | 389 | 1020 | 718265 | 0 | yes |
| layered-16384 | wcc | `neo4j-graph` |  |  | - | 1.136 | 0.002 | 0.002 | - | 2.40 | - |  | 100 | 460 | - | 0 | yes |
| layered-16384 | wcc | `icebug` |  |  | - | 1.008 | 0.022 | 0.022 | - | 2.80 | - |  | 43 | 458 | - | 0 | yes |
| layered-16384 | wcc | `icecat` |  |  | - | 0.506 | 0.002 | 0.004 | - | 1.76 | - |  | 66 | 544 | - | 0 | yes |
| layered-16384 | wcc | `grustcat` |  |  | - | 0.361 | 0.006 | 0.017 | - | 33.34 | - |  | 0 | 7383 | - | 0 | yes |
| layered-16384 | wcc | `grust#1` | first | counted | - | 0.704 | 0.008 | 0.012 | - | 7.09 | - | needed | 66 | 1036 | 341578 | 0 | yes |
| layered-16384 | wcc | `grust#1` | second | counted | - | 0.679 | 0.002 | 0.002 | - | 7.09 | - | needed | 66 | 1036 | 341578 | 0 | yes |
| layered-16384 | wcc | `grust#unset` | first | counted | - | 1.524 | 0.008 | 0.005 | - | 7.02 | - | needed | 66 | 1021 | 438267 | 0 | yes |
| layered-16384 | wcc | `grust#unset` | second | counted | - | 1.492 | 0.008 | 0.005 | - | 7.02 | - | needed | 66 | 1021 | 438267 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted#1` | first | counted | - | 0.695 | 0.003 | 0.004 | - | 5.50 | - | needed | 33 | 908 | 341578 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted#1` | second | counted | - | 0.749 | 0.004 | 0.005 | - | 5.50 | - | needed | 66 | 908 | 341578 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted#unset` | first | counted | - | 1.517 | 0.011 | 0.007 | - | 6.10 | - | needed | 66 | 894 | 438267 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted#unset` | second | counted | - | 1.494 | 0.009 | 0.006 | - | 6.10 | - | needed | 66 | 894 | 438267 | 0 | yes |
| layered-65536 | bfs | `icebug` |  |  | - | 2.905 | 0.079 | 0.027 | - | 11.52 | - |  | 132 | 1832 | - | 0 | yes |
| layered-65536 | bfs | `icecat` |  |  | - | 1.682 | 0.011 | 0.007 | - | 6.68 | - |  | 259 | 1651 | - | 0 | yes |
| layered-65536 | bfs | `grustcat` |  |  | - | 1.077 | 0.022 | 0.020 | - | 142.33 | - |  | 0 | 26649 | - | 0 | yes |
| layered-65536 | bfs | `grust#1` | first | counted | - | 2.101 | 0.007 | 0.003 | - | 33.15 | - | needed | 247 | 3146 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust#1` | second | counted | - | 2.335 | 0.023 | 0.010 | - | 33.15 | - | needed | 247 | 3146 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust#unset` | first | counted | - | 2.089 | 0.016 | 0.008 | - | 31.27 | - | needed | 248 | 3131 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust#unset` | second | counted | - | 2.007 | 0.009 | 0.005 | - | 31.27 | - | needed | 247 | 3131 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted#1` | first | counted | - | 2.076 | 0.017 | 0.008 | - | 23.59 | - | needed | 243 | 2640 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted#1` | second | counted | - | 2.019 | 0.013 | 0.006 | - | 23.59 | - | needed | 247 | 2640 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted#unset` | first | counted | - | 2.105 | 0.012 | 0.006 | - | 26.51 | - | needed | 243 | 2575 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted#unset` | second | counted | - | 2.007 | 0.008 | 0.004 | - | 26.51 | - | needed | 247 | 2575 | 1393359 | 0 | yes |
| layered-65536 | pagerank | `icebug` |  |  | 60 | 100.397 | 3.900 | 0.039 | 1.673 | 11.45 | - |  | 401 | 1832 | - | 0 | yes |
| layered-65536 | pagerank | `icecat` |  |  | 75 | 100.672 | 0.060 | 0.001 | 1.342 | 6.87 | - |  | 901 | 1652 | - | 0 | yes |
| layered-65536 | pagerank | `grustcat` |  |  | 75 | 95.184 | 0.125 | 0.001 | 1.269 | 140.30 | - |  | 387 | 26649 | - | 0 | yes |
| layered-65536 | pagerank | `grust#1` | first | counted | 75 | 109.038 | 0.083 | 0.001 | 1.454 | 33.35 | - | needed | 899 | 3146 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust#1` | second | counted | 75 | 105.721 | 0.184 | 0.002 | 1.410 | 33.35 | - | needed | 387 | 3146 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust#unset` | first | counted | 75 | 416.267 | 0.507 | 0.001 | 5.550 | 33.33 | - | needed | 645 | 3131 | 31164642 | 0 | yes |
| layered-65536 | pagerank | `grust#unset` | second | counted | 75 | 415.397 | 0.031 | 0.000 | 5.539 | 33.33 | - | needed | 645 | 3131 | 31164642 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted#1` | first | counted | 75 | 111.853 | 0.271 | 0.002 | 1.491 | 27.12 | 2.61 | needed | 516 | 3217 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted#1` | second | counted | 75 | 111.538 | 0.069 | 0.001 | 1.487 | 27.12 | 2.61 | needed | 516 | 3217 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted#unset` | first | counted | 75 | 319.890 | 0.616 | 0.002 | 4.265 | 26.42 | - | needed | 645 | 2575 | 31164642 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted#unset` | second | counted | 75 | 319.663 | 0.423 | 0.001 | 4.262 | 26.42 | - | needed | 645 | 2575 | 31164642 | 0 | yes |
| layered-65536 | triangles | `neo4j-graph` |  |  | - | 2.844 | 0.005 | 0.002 | - | 9.05 | - |  | 3 | 1796 | - | 0 | yes |
| layered-65536 | triangles | `grust#1` | first | counted | - | 12.133 | 0.029 | 0.002 | - | 35.02 | - | needed | 1536 | 3654 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust#1` | second | counted | - | 11.978 | 0.039 | 0.003 | - | 35.02 | - | needed | 1536 | 3654 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust#unset` | first | counted | - | 12.101 | 0.010 | 0.001 | - | 35.20 | - | needed | 1536 | 3639 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust#unset` | second | counted | - | 11.955 | 0.042 | 0.004 | - | 35.20 | - | needed | 1536 | 3639 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted#1` | first | counted | - | 11.780 | 0.068 | 0.006 | - | 26.67 | - | needed | 1536 | 3149 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted#1` | second | counted | - | 11.678 | 0.091 | 0.008 | - | 26.67 | - | needed | 1536 | 3149 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted#unset` | first | counted | - | 11.815 | 0.089 | 0.007 | - | 28.59 | - | needed | 1536 | 3083 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted#unset` | second | counted | - | 11.692 | 0.135 | 0.012 | - | 28.59 | - | needed | 1536 | 3083 | 2877576 | 0 | yes |
| layered-65536 | wcc | `neo4j-graph` |  |  | - | 4.251 | 0.015 | 0.003 | - | 9.00 | - |  | 393 | 1796 | - | 0 | yes |
| layered-65536 | wcc | `icebug` |  |  | - | 4.706 | 0.042 | 0.009 | - | 11.33 | - |  | 137 | 1832 | - | 0 | yes |
| layered-65536 | wcc | `icecat` |  |  | - | 2.121 | 0.004 | 0.002 | - | 6.76 | - |  | 259 | 1652 | - | 0 | yes |
| layered-65536 | wcc | `grustcat` |  |  | - | 1.457 | 0.014 | 0.010 | - | 139.70 | - |  | 0 | 26650 | - | 0 | yes |
| layered-65536 | wcc | `grust#1` | first | counted | - | 2.832 | 0.011 | 0.004 | - | 32.83 | - | needed | 258 | 3146 | 1368146 | 0 | yes |
| layered-65536 | wcc | `grust#1` | second | counted | - | 2.763 | 0.009 | 0.003 | - | 32.83 | - | needed | 258 | 3146 | 1368146 | 0 | yes |
| layered-65536 | wcc | `grust#unset` | first | counted | - | 6.086 | 0.011 | 0.002 | - | 32.91 | - | needed | 258 | 3131 | 1755282 | 0 | yes |
| layered-65536 | wcc | `grust#unset` | second | counted | - | 6.045 | 0.028 | 0.005 | - | 32.91 | - | needed | 258 | 3131 | 1755282 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted#1` | first | counted | - | 3.025 | 0.012 | 0.004 | - | 24.67 | - | needed | 258 | 2640 | 1368146 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted#1` | second | counted | - | 2.994 | 0.019 | 0.006 | - | 24.67 | - | needed | 258 | 2640 | 1368146 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted#unset` | first | counted | - | 6.032 | 0.023 | 0.004 | - | 26.22 | - | needed | 258 | 2575 | 1755282 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted#unset` | second | counted | - | 5.960 | 0.017 | 0.003 | - | 26.22 | - | needed | 258 | 2575 | 1755282 | 0 | yes |
| path-16384 | bfs | `icebug` |  |  | - | 0.265 | 0.002 | 0.007 | - | 1.80 | - |  | 36 | 450 | - | 0 | yes |
| path-16384 | bfs | `icecat` |  |  | - | 0.294 | 0.001 | 0.005 | - | 0.99 | - |  | 66 | 292 | - | 0 | yes |
| path-16384 | bfs | `grustcat` |  |  | - | 0.144 | 0.001 | 0.006 | - | 27.16 | - |  | 0 | 6429 | - | 0 | yes |
| path-16384 | bfs | `grust#1` | first | counted | - | 0.485 | 0.002 | 0.005 | - | 5.33 | - | needed | 69 | 745 | 245755 | 0 | yes |
| path-16384 | bfs | `grust#1` | second | counted | - | 0.436 | 0.002 | 0.005 | - | 5.33 | - | needed | 33 | 745 | 245755 | 0 | yes |
| path-16384 | bfs | `grust#unset` | first | counted | - | 0.485 | 0.002 | 0.004 | - | 5.29 | - | needed | 69 | 730 | 245755 | 0 | yes |
| path-16384 | bfs | `grust#unset` | second | counted | - | 0.402 | 0.004 | 0.009 | - | 5.29 | - | needed | 33 | 730 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@counted#1` | first | counted | - | 0.463 | 0.001 | 0.003 | - | 4.58 | - | needed | 66 | 689 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@counted#1` | second | counted | - | 0.433 | 0.001 | 0.003 | - | 4.58 | - | needed | 66 | 689 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@counted#unset` | first | counted | - | 0.474 | 0.005 | 0.010 | - | 4.86 | - | needed | 69 | 674 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@counted#unset` | second | counted | - | 0.389 | 0.006 | 0.015 | - | 4.86 | - | needed | 33 | 674 | 245755 | 0 | yes |
| path-16384 | pagerank | `icebug` |  |  | 54 | 12.954 | 0.047 | 0.004 | 0.240 | 1.79 | - |  | 113 | 450 | - | 0 | yes |
| path-16384 | pagerank | `icecat` |  |  | 58 | 11.449 | 0.032 | 0.003 | 0.197 | 0.99 | - |  | 230 | 293 | - | 0 | yes |
| path-16384 | pagerank | `grustcat` |  |  | 58 | 9.923 | 0.069 | 0.007 | 0.171 | 27.25 | - |  | 0 | 6429 | - | 0 | yes |
| path-16384 | pagerank | `grust#1` | first | counted | 58 | 14.887 | 0.073 | 0.005 | 0.257 | 5.38 | - | needed | 198 | 745 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust#1` | second | counted | 58 | 14.117 | 0.009 | 0.001 | 0.243 | 5.38 | - | needed | 99 | 745 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust#unset` | first | counted | 58 | 66.919 | 0.094 | 0.001 | 1.154 | 5.29 | - | needed | 165 | 730 | 5062591 | 0 | yes |
| path-16384 | pagerank | `grust#unset` | second | counted | 58 | 66.892 | 0.147 | 0.002 | 1.153 | 5.29 | - | needed | 165 | 730 | 5062591 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted#1` | first | counted | 58 | 14.749 | 0.002 | 0.000 | 0.254 | 5.08 | 0.49 | needed | 99 | 787 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted#1` | second | counted | 58 | 14.682 | 0.008 | 0.001 | 0.253 | 5.08 | 0.49 | needed | 99 | 787 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted#unset` | first | counted | 58 | 60.895 | 0.121 | 0.002 | 1.050 | 4.90 | - | needed | 165 | 674 | 5062591 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted#unset` | second | counted | 58 | 60.641 | 0.020 | 0.000 | 1.046 | 4.90 | - | needed | 165 | 674 | 5062591 | 0 | yes |
| path-16384 | triangles | `neo4j-graph` |  |  | - | 0.295 | 0.008 | 0.027 | - | 1.65 | - |  | 4 | 335 | - | 0 | yes |
| path-16384 | triangles | `grust#1` | first | counted | - | 1.726 | 0.009 | 0.005 | - | 5.50 | - | needed | 295 | 807 | 425970 | 0 | yes |
| path-16384 | triangles | `grust#1` | second | counted | - | 1.596 | 0.010 | 0.006 | - | 5.50 | - | needed | 295 | 807 | 425970 | 0 | yes |
| path-16384 | triangles | `grust#unset` | first | counted | - | 1.728 | 0.019 | 0.011 | - | 5.42 | - | needed | 295 | 792 | 425970 | 0 | yes |
| path-16384 | triangles | `grust#unset` | second | counted | - | 1.570 | 0.009 | 0.005 | - | 5.42 | - | needed | 295 | 792 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted#1` | first | counted | - | 1.692 | 0.029 | 0.017 | - | 4.73 | - | needed | 262 | 751 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted#1` | second | counted | - | 1.545 | 0.004 | 0.003 | - | 4.73 | - | needed | 262 | 751 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted#unset` | first | counted | - | 1.742 | 0.012 | 0.007 | - | 5.13 | - | needed | 295 | 736 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted#unset` | second | counted | - | 1.601 | 0.008 | 0.005 | - | 5.13 | - | needed | 295 | 736 | 425970 | 0 | yes |
| path-16384 | wcc | `neo4j-graph` |  |  | - | 0.936 | 0.004 | 0.005 | - | 1.62 | - |  | 99 | 334 | - | 0 | yes |
| path-16384 | wcc | `icebug` |  |  | - | 0.358 | 0.004 | 0.012 | - | 1.81 | - |  | 42 | 450 | - | 0 | yes |
| path-16384 | wcc | `icecat` |  |  | - | 0.284 | 0.003 | 0.009 | - | 0.98 | - |  | 66 | 292 | - | 0 | yes |
| path-16384 | wcc | `grustcat` |  |  | - | 0.159 | 0.000 | 0.001 | - | 27.65 | - |  | 0 | 6429 | - | 0 | yes |
| path-16384 | wcc | `grust#1` | first | counted | - | 0.513 | 0.003 | 0.005 | - | 5.27 | - | needed | 66 | 745 | 229369 | 0 | yes |
| path-16384 | wcc | `grust#1` | second | counted | - | 0.499 | 0.003 | 0.006 | - | 5.27 | - | needed | 66 | 745 | 229369 | 0 | yes |
| path-16384 | wcc | `grust#unset` | first | counted | - | 1.069 | 0.006 | 0.006 | - | 5.27 | - | needed | 66 | 730 | 294903 | 0 | yes |
| path-16384 | wcc | `grust#unset` | second | counted | - | 1.045 | 0.003 | 0.003 | - | 5.27 | - | needed | 66 | 730 | 294903 | 0 | yes |
| path-16384 | wcc | `grust-next@counted#1` | first | counted | - | 0.518 | 0.001 | 0.001 | - | 4.55 | - | needed | 66 | 689 | 229369 | 0 | yes |
| path-16384 | wcc | `grust-next@counted#1` | second | counted | - | 0.484 | 0.004 | 0.008 | - | 4.55 | - | needed | 65 | 689 | 229369 | 0 | yes |
| path-16384 | wcc | `grust-next@counted#unset` | first | counted | - | 1.064 | 0.003 | 0.003 | - | 4.87 | - | needed | 66 | 674 | 294903 | 0 | yes |
| path-16384 | wcc | `grust-next@counted#unset` | second | counted | - | 1.053 | 0.004 | 0.004 | - | 4.87 | - | needed | 66 | 674 | 294903 | 0 | yes |
| path-65536 | bfs | `icebug` |  |  | - | 1.065 | 0.027 | 0.026 | - | 7.15 | - |  | 132 | 1795 | - | 0 | yes |
| path-65536 | bfs | `icecat` |  |  | - | 1.218 | 0.000 | 0.000 | - | 4.51 | - |  | 259 | 1156 | - | 0 | yes |
| path-65536 | bfs | `grustcat` |  |  | - | 0.785 | 0.003 | 0.003 | - | 115.00 | - |  | 129 | 24248 | - | 0 | yes |
| path-65536 | bfs | `grust#1` | first | counted | - | 1.909 | 0.008 | 0.004 | - | 24.84 | - | needed | 274 | 2490 | 983035 | 0 | yes |
| path-65536 | bfs | `grust#1` | second | counted | - | 1.980 | 0.005 | 0.002 | - | 24.84 | - | needed | 274 | 2490 | 983035 | 0 | yes |
| path-65536 | bfs | `grust#unset` | first | counted | - | 1.933 | 0.019 | 0.010 | - | 24.69 | - | needed | 274 | 2476 | 983035 | 0 | yes |
| path-65536 | bfs | `grust#unset` | second | counted | - | 1.846 | 0.012 | 0.006 | - | 24.69 | - | needed | 274 | 2476 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@counted#1` | first | counted | - | 1.843 | 0.004 | 0.002 | - | 21.08 | - | needed | 272 | 2270 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@counted#1` | second | counted | - | 1.789 | 0.010 | 0.005 | - | 21.08 | - | needed | 274 | 2270 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@counted#unset` | first | counted | - | 1.868 | 0.012 | 0.006 | - | 21.19 | - | needed | 272 | 2206 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@counted#unset` | second | counted | - | 1.797 | 0.004 | 0.002 | - | 21.19 | - | needed | 274 | 2206 | 983035 | 0 | yes |
| path-65536 | pagerank | `icebug` |  |  | 46 | 43.948 | 0.161 | 0.004 | 0.955 | 7.16 | - |  | 401 | 1795 | - | 0 | yes |
| path-65536 | pagerank | `icecat` |  |  | 50 | 39.982 | 0.047 | 0.001 | 0.800 | 4.53 | - |  | 901 | 1156 | - | 0 | yes |
| path-65536 | pagerank | `grustcat` |  |  | 50 | 35.314 | 0.026 | 0.001 | 0.706 | 115.16 | - |  | 516 | 24248 | - | 0 | yes |
| path-65536 | pagerank | `grust#1` | first | counted | 50 | 52.392 | 0.081 | 0.002 | 1.048 | 24.77 | - | needed | 774 | 2490 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust#1` | second | counted | 50 | 49.401 | 0.008 | 0.000 | 0.988 | 24.77 | - | needed | 387 | 2490 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust#unset` | first | counted | 50 | 233.094 | 0.866 | 0.004 | 4.662 | 24.57 | - | needed | 645 | 2475 | 17629127 | 0 | yes |
| path-65536 | pagerank | `grust#unset` | second | counted | 50 | 232.340 | 0.201 | 0.001 | 4.647 | 24.57 | - | needed | 645 | 2475 | 17629127 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted#1` | first | counted | 50 | 52.394 | 0.025 | 0.000 | 1.048 | 23.37 | 2.13 | needed | 516 | 2722 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted#1` | second | counted | 50 | 52.263 | 0.019 | 0.000 | 1.045 | 23.37 | 2.13 | needed | 516 | 2722 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted#unset` | first | counted | 50 | 211.499 | 0.154 | 0.001 | 4.230 | 23.12 | - | needed | 645 | 2206 | 17629127 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted#unset` | second | counted | 50 | 210.805 | 0.467 | 0.002 | 4.216 | 23.12 | - | needed | 645 | 2206 | 17629127 | 0 | yes |
| path-65536 | triangles | `neo4j-graph` |  |  | - | 0.680 | 0.006 | 0.010 | - | 5.65 | - |  | 3 | 1295 | - | 0 | yes |
| path-65536 | triangles | `grust#1` | first | counted | - | 6.641 | 0.054 | 0.008 | - | 24.15 | - | needed | 1159 | 2744 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust#1` | second | counted | - | 6.420 | 0.020 | 0.003 | - | 24.15 | - | needed | 1159 | 2744 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust#unset` | first | counted | - | 6.627 | 0.025 | 0.004 | - | 24.51 | - | needed | 1159 | 2729 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust#unset` | second | counted | - | 6.277 | 0.072 | 0.012 | - | 24.51 | - | needed | 1159 | 2729 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted#1` | first | counted | - | 6.609 | 0.065 | 0.010 | - | 20.81 | - | needed | 1159 | 2524 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted#1` | second | counted | - | 6.357 | 0.029 | 0.004 | - | 20.81 | - | needed | 1159 | 2524 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted#unset` | first | counted | - | 6.652 | 0.004 | 0.001 | - | 22.52 | - | needed | 1159 | 2459 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted#unset` | second | counted | - | 6.392 | 0.052 | 0.008 | - | 22.52 | - | needed | 1159 | 2459 | 1703922 | 0 | yes |
| path-65536 | wcc | `neo4j-graph` |  |  | - | 3.349 | 0.009 | 0.003 | - | 5.63 | - |  | 393 | 1295 | - | 0 | yes |
| path-65536 | wcc | `icebug` |  |  | - | 1.340 | 0.039 | 0.029 | - | 7.19 | - |  | 137 | 1795 | - | 0 | yes |
| path-65536 | wcc | `icecat` |  |  | - | 1.193 | 0.014 | 0.012 | - | 4.55 | - |  | 258 | 1157 | - | 0 | yes |
| path-65536 | wcc | `grustcat` |  |  | - | 0.864 | 0.002 | 0.002 | - | 114.97 | - |  | 129 | 24249 | - | 0 | yes |
| path-65536 | wcc | `grust#1` | first | counted | - | 2.029 | 0.006 | 0.003 | - | 24.20 | - | needed | 258 | 2490 | 917497 | 0 | yes |
| path-65536 | wcc | `grust#1` | second | counted | - | 1.991 | 0.016 | 0.008 | - | 24.20 | - | needed | 258 | 2490 | 917497 | 0 | yes |
| path-65536 | wcc | `grust#unset` | first | counted | - | 4.271 | 0.008 | 0.002 | - | 24.47 | - | needed | 258 | 2476 | 1179639 | 0 | yes |
| path-65536 | wcc | `grust#unset` | second | counted | - | 4.220 | 0.009 | 0.002 | - | 24.47 | - | needed | 258 | 2476 | 1179639 | 0 | yes |
| path-65536 | wcc | `grust-next@counted#1` | first | counted | - | 2.041 | 0.002 | 0.001 | - | 20.38 | - | needed | 258 | 2270 | 917497 | 0 | yes |
| path-65536 | wcc | `grust-next@counted#1` | second | counted | - | 1.999 | 0.006 | 0.003 | - | 20.38 | - | needed | 258 | 2270 | 917497 | 0 | yes |
| path-65536 | wcc | `grust-next@counted#unset` | first | counted | - | 4.254 | 0.008 | 0.002 | - | 21.97 | - | needed | 258 | 2205 | 1179639 | 0 | yes |
| path-65536 | wcc | `grust-next@counted#unset` | second | counted | - | 4.209 | 0.010 | 0.002 | - | 21.97 | - | needed | 258 | 2205 | 1179639 | 0 | yes |
| uniform-16384 | bfs | `icebug` |  |  | - | 2.273 | 0.083 | 0.036 | - | 10.01 | - |  | 57 | 979 | - | 0 | yes |
| uniform-16384 | bfs | `icecat` |  |  | - | 0.972 | 0.011 | 0.012 | - | 7.40 | - |  | 98 | 2083 | - | 0 | yes |
| uniform-16384 | bfs | `grustcat` |  |  | - | 0.929 | 0.032 | 0.035 | - | 93.19 | - |  | 0 | 10816 | - | 0 | yes |
| uniform-16384 | bfs | `grust#1` | first | counted | - | 1.757 | 0.016 | 0.009 | - | 20.53 | - | needed | 68 | 2304 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust#1` | second | counted | - | 1.839 | 0.012 | 0.007 | - | 20.53 | - | needed | 32 | 2304 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust#unset` | first | counted | - | 1.772 | 0.025 | 0.014 | - | 19.91 | - | needed | 68 | 1778 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust#unset` | second | counted | - | 1.554 | 0.006 | 0.004 | - | 19.91 | - | needed | 32 | 1778 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted#1` | first | counted | - | 1.754 | 0.029 | 0.017 | - | 10.52 | - | needed | 32 | 1232 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted#1` | second | counted | - | 1.576 | 0.011 | 0.007 | - | 10.52 | - | needed | 32 | 1232 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted#unset` | first | counted | - | 1.902 | 0.069 | 0.036 | - | 13.96 | - | needed | 68 | 1728 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted#unset` | second | counted | - | 1.569 | 0.009 | 0.006 | - | 13.96 | - | needed | 32 | 1728 | 1048343 | 0 | yes |
| uniform-16384 | pagerank | `neo4j-graph` |  |  | 28 | 10.502 | 0.032 | 0.003 | 0.375 | 8.39 | - |  | 24 | 718 | - | 0 | yes |
| uniform-16384 | pagerank | `icebug` |  |  | 12 | 8.037 | 0.120 | 0.015 | 0.670 | 9.86 | - |  | 112 | 979 | - | 0 | yes |
| uniform-16384 | pagerank | `icecat` |  |  | 16 | 8.325 | 0.028 | 0.003 | 0.520 | 6.80 | - |  | 229 | 1573 | - | 0 | yes |
| uniform-16384 | pagerank | `grustcat` |  |  | 16 | 6.970 | 0.051 | 0.007 | 0.436 | 91.63 | - |  | 33 | 10816 | - | 0 | yes |
| uniform-16384 | pagerank | `grust#1` | first | counted | 16 | 11.385 | 0.008 | 0.001 | 0.712 | 20.49 | - | needed | 421 | 2304 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust#1` | second | counted | 16 | 9.446 | 0.004 | 0.000 | 0.590 | 20.49 | - | needed | 99 | 2304 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust#unset` | first | counted | 16 | 48.309 | 0.073 | 0.002 | 3.019 | 20.55 | - | needed | 165 | 1779 | 4373785 | 0 | yes |
| uniform-16384 | pagerank | `grust#unset` | second | counted | 16 | 48.096 | 0.019 | 0.000 | 3.006 | 20.55 | - | needed | 165 | 1779 | 4373785 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted#1` | first | counted | 16 | 7.805 | 0.013 | 0.002 | 0.488 | 12.03 | 1.56 | needed | 99 | 1521 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted#1` | second | counted | 16 | 7.707 | 0.014 | 0.002 | 0.482 | 12.03 | 1.56 | needed | 99 | 1521 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted#unset` | first | counted | 16 | 22.000 | 0.062 | 0.003 | 1.375 | 13.15 | - | needed | 165 | 1217 | 4373785 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted#unset` | second | counted | 16 | 21.904 | 0.040 | 0.002 | 1.369 | 13.15 | - | needed | 165 | 1217 | 4373785 | 0 | yes |
| uniform-16384 | triangles | `neo4j-graph` |  |  | - | 8.757 | 0.043 | 0.005 | - | 8.27 | - |  | 3 | 717 | - | 0 | yes |
| uniform-16384 | triangles | `grust#1` | first | counted | - | 18.803 | 0.020 | 0.001 | - | 23.96 | - | needed | 455 | 1794 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust#1` | second | counted | - | 18.606 | 0.051 | 0.003 | - | 23.96 | - | needed | 455 | 1794 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust#unset` | first | counted | - | 18.761 | 0.021 | 0.001 | - | 23.67 | - | needed | 455 | 1268 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust#unset` | second | counted | - | 18.629 | 0.070 | 0.004 | - | 23.67 | - | needed | 455 | 1268 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted#1` | first | counted | - | 18.244 | 0.090 | 0.005 | - | 13.20 | - | needed | 422 | 722 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted#1` | second | counted | - | 18.044 | 0.083 | 0.005 | - | 13.20 | - | needed | 422 | 722 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted#unset` | first | counted | - | 18.295 | 0.055 | 0.003 | - | 17.25 | - | needed | 455 | 1218 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted#unset` | second | counted | - | 17.906 | 0.019 | 0.001 | - | 17.25 | - | needed | 455 | 1218 | 3829630 | 0 | yes |
| uniform-16384 | wcc | `neo4j-graph` |  |  | - | 1.234 | 0.007 | 0.006 | - | 8.22 | - |  | 99 | 717 | - | 0 | yes |
| uniform-16384 | wcc | `icebug` |  |  | - | 3.153 | 0.325 | 0.103 | - | 9.65 | - |  | 68 | 979 | - | 0 | yes |
| uniform-16384 | wcc | `icecat` |  |  | - | 1.103 | 0.016 | 0.015 | - | 6.78 | - |  | 66 | 1573 | - | 0 | yes |
| uniform-16384 | wcc | `grustcat` |  |  | - | 0.761 | 0.006 | 0.008 | - | 92.13 | - |  | 1 | 10306 | - | 0 | yes |
| uniform-16384 | wcc | `grust#1` | first | counted | - | 2.181 | 0.004 | 0.002 | - | 20.61 | - | needed | 66 | 2304 | 1031975 | 0 | yes |
| uniform-16384 | wcc | `grust#1` | second | counted | - | 2.179 | 0.019 | 0.009 | - | 20.61 | - | needed | 66 | 2304 | 1031975 | 0 | yes |
| uniform-16384 | wcc | `grust#unset` | first | counted | - | 4.275 | 0.005 | 0.001 | - | 21.00 | - | needed | 66 | 1778 | 1324427 | 0 | yes |
| uniform-16384 | wcc | `grust#unset` | second | counted | - | 4.235 | 0.011 | 0.003 | - | 21.00 | - | needed | 66 | 1778 | 1324427 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted#1` | first | counted | - | 2.362 | 0.017 | 0.007 | - | 10.99 | - | needed | 33 | 1743 | 1031975 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted#1` | second | counted | - | 2.428 | 0.018 | 0.008 | - | 10.99 | - | needed | 66 | 1743 | 1031975 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted#unset` | first | counted | - | 4.226 | 0.005 | 0.001 | - | 13.53 | - | needed | 66 | 1217 | 1324427 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted#unset` | second | counted | - | 4.194 | 0.002 | 0.000 | - | 13.53 | - | needed | 66 | 1217 | 1324427 | 0 | yes |
| uniform-65536 | bfs | `icebug` |  |  | - | 14.661 | 0.612 | 0.042 | - | 59.58 | - |  | 216 | 3889 | - | 0 | yes |
| uniform-65536 | bfs | `icecat` |  |  | - | 4.874 | 0.197 | 0.040 | - | 20.71 | - |  | 387 | 1680 | - | 0 | yes |
| uniform-65536 | bfs | `grustcat` |  |  | - | 5.823 | 0.075 | 0.013 | - | 478.53 | - |  | 0 | 35594 | - | 0 | yes |
| uniform-65536 | bfs | `grust#1` | first | counted | - | 9.178 | 0.208 | 0.023 | - | 105.68 | - | needed | 428 | 2089 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust#1` | second | counted | - | 6.982 | 0.008 | 0.001 | - | 105.68 | - | needed | 380 | 2089 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust#unset` | first | counted | - | 8.873 | 1.069 | 0.121 | - | 105.33 | - | needed | 273 | 2074 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust#unset` | second | counted | - | 7.602 | 0.559 | 0.073 | - | 105.33 | - | needed | 273 | 2074 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted#1` | first | counted | - | 8.204 | 0.054 | 0.007 | - | 43.02 | - | needed | 420 | 1911 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted#1` | second | counted | - | 7.099 | 0.070 | 0.010 | - | 43.02 | - | needed | 380 | 1911 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted#unset` | first | counted | - | 11.202 | 0.264 | 0.024 | - | 52.15 | - | needed | 257 | 1335 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted#unset` | second | counted | - | 9.218 | 0.192 | 0.021 | - | 52.15 | - | needed | 273 | 1335 | 4193790 | 0 | yes |
| uniform-65536 | pagerank | `neo4j-graph` |  |  | 34 | 44.803 | 0.436 | 0.010 | 1.318 | 42.56 | - |  | 139 | 789 | - | 0 | yes |
| uniform-65536 | pagerank | `icebug` |  |  | 11 | 69.763 | 1.083 | 0.016 | 6.342 | 64.46 | - |  | 399 | 3889 | - | 0 | yes |
| uniform-65536 | pagerank | `icecat` |  |  | 16 | 33.483 | 0.076 | 0.002 | 2.093 | 21.02 | - |  | 901 | 1681 | - | 0 | yes |
| uniform-65536 | pagerank | `grustcat` |  |  | 16 | 31.258 | 1.129 | 0.036 | 1.954 | 492.03 | - |  | 0 | 36104 | - | 0 | yes |
| uniform-65536 | pagerank | `grust#1` | first | counted | 16 | 58.792 | 0.937 | 0.016 | 3.674 | 99.73 | - | needed | 647 | 2088 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust#1` | second | counted | 16 | 50.493 | 0.665 | 0.013 | 3.156 | 99.73 | - | needed | 387 | 2088 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust#unset` | first | counted | 16 | 194.833 | 0.068 | 0.000 | 12.177 | 105.35 | - | needed | 645 | 2074 | 17497177 | 0 | yes |
| uniform-65536 | pagerank | `grust#unset` | second | counted | 16 | 194.950 | 0.234 | 0.001 | 12.184 | 105.35 | - | needed | 645 | 2074 | 17497177 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted#1` | first | counted | 16 | 32.807 | 0.116 | 0.004 | 2.050 | 48.53 | 6.48 | needed | 516 | 1725 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted#1` | second | counted | 16 | 32.530 | 0.199 | 0.006 | 2.033 | 48.53 | 6.48 | needed | 516 | 1725 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted#unset` | first | counted | 16 | 89.686 | 0.251 | 0.003 | 5.605 | 52.88 | - | needed | 645 | 1846 | 17497177 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted#unset` | second | counted | 16 | 89.677 | 0.202 | 0.002 | 5.605 | 52.88 | - | needed | 645 | 1846 | 17497177 | 0 | yes |
| uniform-65536 | triangles | `neo4j-graph` |  |  | - | 42.545 | 1.050 | 0.025 | - | 47.15 | - |  | 4 | 788 | - | 0 | yes |
| uniform-65536 | triangles | `grust#1` | first | counted | - | 87.367 | 2.208 | 0.025 | - | 158.66 | - | needed | 780 | 2093 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust#1` | second | counted | - | 87.639 | 1.120 | 0.013 | - | 158.66 | - | needed | 780 | 2093 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust#unset` | first | counted | - | 84.855 | 1.045 | 0.012 | - | 151.61 | - | needed | 780 | 2078 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust#unset` | second | counted | - | 86.472 | 3.554 | 0.041 | - | 151.61 | - | needed | 780 | 2078 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted#1` | first | counted | - | 84.006 | 0.459 | 0.005 | - | 88.91 | - | needed | 780 | 1915 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted#1` | second | counted | - | 84.515 | 1.526 | 0.018 | - | 88.91 | - | needed | 780 | 1915 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted#unset` | first | counted | - | 84.627 | 1.312 | 0.016 | - | 115.22 | - | needed | 780 | 1339 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted#unset` | second | counted | - | 84.026 | 1.308 | 0.016 | - | 115.22 | - | needed | 780 | 1339 | 15327135 | 0 | yes |
| uniform-65536 | wcc | `neo4j-graph` |  |  | - | 4.588 | 0.011 | 0.002 | - | 44.13 | - |  | 393 | 789 | - | 0 | yes |
| uniform-65536 | wcc | `icebug` |  |  | - | 26.696 | 0.138 | 0.005 | - | 66.89 | - |  | 244 | 3889 | - | 0 | yes |
| uniform-65536 | wcc | `icecat` |  |  | - | 4.476 | 0.020 | 0.005 | - | 21.11 | - |  | 259 | 1681 | - | 0 | yes |
| uniform-65536 | wcc | `grustcat` |  |  | - | 3.107 | 0.005 | 0.002 | - | 476.48 | - |  | 0 | 36104 | - | 0 | yes |
| uniform-65536 | wcc | `grust#1` | first | counted | - | 9.478 | 0.028 | 0.003 | - | 103.87 | - | needed | 258 | 2089 | 4128495 | 0 | yes |
| uniform-65536 | wcc | `grust#1` | second | counted | - | 9.371 | 0.007 | 0.001 | - | 103.87 | - | needed | 258 | 2089 | 4128495 | 0 | yes |
| uniform-65536 | wcc | `grust#unset` | first | counted | - | 17.806 | 0.069 | 0.004 | - | 105.50 | - | needed | 258 | 2074 | 5298822 | 0 | yes |
| uniform-65536 | wcc | `grust#unset` | second | counted | - | 17.564 | 0.080 | 0.005 | - | 105.50 | - | needed | 258 | 2074 | 5298822 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted#1` | first | counted | - | 10.672 | 0.040 | 0.004 | - | 42.50 | - | needed | 258 | 1911 | 4128495 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted#1` | second | counted | - | 10.578 | 0.018 | 0.002 | - | 42.50 | - | needed | 258 | 1911 | 4128495 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted#unset` | first | counted | - | 17.737 | 0.034 | 0.002 | - | 52.96 | - | needed | 258 | 1846 | 5298822 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted#unset` | second | counted | - | 17.613 | 0.028 | 0.002 | - | 52.96 | - | needed | 258 | 1846 | 5298822 | 0 | yes |

### `pinned-full-width.json`: pinned-full-width

workers 16, concurrency 16, allocator pinned: glibc.malloc.mmap_threshold=131072, 1 warmup + 5 repeats, steal over the run 0 ticks, 83.7 s, unusable at MAD/median >= 0.25

Not timed (no agreeing parity row): neo4j-graph pagerank layered-16384.edges, neo4j-graph pagerank layered-65536.edges, neo4j-graph pagerank path-16384.edges, neo4j-graph pagerank path-65536.edges 

| fixture | algorithm | participant | call | accounting | iters | total ms | MAD | MAD/median | per iter | build ms | incoming ms | prepare | minflt | minflt build | work units | steal | usable |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |
| hub-16384 | bfs | `icebug` |  |  | - | 2.187 | 0.122 | 0.056 | - | 10.00 | - |  | 57 | 1018 | - | 0 | yes |
| hub-16384 | bfs | `icecat` |  |  | - | 0.934 | 0.013 | 0.014 | - | 6.08 | - |  | 100 | 1572 | - | 0 | yes |
| hub-16384 | bfs | `grustcat` |  |  | - | 0.752 | 0.028 | 0.037 | - | 91.59 | - |  | 33 | 10864 | - | 0 | yes |
| hub-16384 | bfs | `grust` | first | counted | - | 1.629 | 0.016 | 0.010 | - | 19.50 | - | needed | 69 | 1792 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust` | second | counted | - | 1.795 | 0.008 | 0.005 | - | 19.50 | - | needed | 33 | 1792 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted` | first | counted | - | 1.723 | 0.018 | 0.010 | - | 10.89 | - | needed | 66 | 1576 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted` | second | counted | - | 1.605 | 0.003 | 0.002 | - | 10.89 | - | needed | 66 | 1576 | 1047577 | 0 | yes |
| hub-16384 | pagerank | `neo4j-graph` |  |  | 36 | 13.555 | 0.047 | 0.003 | 0.377 | 5.05 | - |  | 66 | 901 | - | 0 | yes |
| hub-16384 | pagerank | `icebug` |  |  | 12 | 2.924 | 0.027 | 0.009 | 0.244 | 10.08 | - |  | 216 | 1018 | - | 0 | yes |
| hub-16384 | pagerank | `icecat` |  |  | 17 | 8.732 | 0.020 | 0.002 | 0.514 | 6.60 | - |  | 229 | 2082 | - | 0 | yes |
| hub-16384 | pagerank | `grustcat` |  |  | 17 | 7.537 | 0.034 | 0.004 | 0.443 | 93.94 | - |  | 100 | 10354 | - | 0 | yes |
| hub-16384 | pagerank | `grust` | first | counted | 17 | 6.579 | 0.122 | 0.019 | 0.387 | 20.67 | - | needed | 538 | 2303 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust` | second | counted | 17 | 3.812 | 0.043 | 0.011 | 0.224 | 20.67 | - | needed | 99 | 2303 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted` | first | counted | 17 | 3.976 | 0.090 | 0.023 | 0.234 | 14.09 | 2.27 | needed | 138 | 2649 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted` | second | counted | 17 | 3.802 | 0.041 | 0.011 | 0.224 | 14.09 | 2.27 | needed | 132 | 2649 | 4403580 | 0 | yes |
| hub-16384 | triangles | `neo4j-graph` |  |  | - | 1.200 | 0.003 | 0.002 | - | 5.05 | - |  | 53 | 921 | - | 0 | yes |
| hub-16384 | triangles | `grust` | first | counted | - | 8.523 | 0.017 | 0.002 | - | 24.29 | - | needed | 557 | 1283 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust` | second | counted | - | 7.582 | 0.025 | 0.003 | - | 24.29 | - | needed | 455 | 1283 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted` | first | counted | - | 7.704 | 0.008 | 0.001 | - | 11.63 | - | needed | 455 | 1065 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted` | second | counted | - | 7.462 | 0.038 | 0.005 | - | 11.63 | - | needed | 455 | 1065 | 3742208 | 0 | yes |
| hub-16384 | wcc | `neo4j-graph` |  |  | - | 1.309 | 0.006 | 0.004 | - | 5.11 | - |  | 113 | 918 | - | 0 | yes |
| hub-16384 | wcc | `icebug` |  |  | - | 2.587 | 0.150 | 0.058 | - | 9.96 | - |  | 69 | 1018 | - | 0 | yes |
| hub-16384 | wcc | `icecat` |  |  | - | 0.951 | 0.005 | 0.005 | - | 6.28 | - |  | 67 | 1572 | - | 0 | yes |
| hub-16384 | wcc | `grustcat` |  |  | - | 0.617 | 0.003 | 0.005 | - | 92.32 | - |  | 1 | 10355 | - | 0 | yes |
| hub-16384 | wcc | `grust` | first | counted | - | 1.467 | 0.036 | 0.025 | - | 19.54 | - | needed | 174 | 2304 | 1031211 | 0 | yes |
| hub-16384 | wcc | `grust` | second | counted | - | 0.683 | 0.026 | 0.038 | - | 19.54 | - | needed | 68 | 2304 | 1031211 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted` | first | counted | - | 0.725 | 0.023 | 0.032 | - | 11.43 | - | needed | 69 | 1578 | 1031207 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted` | second | counted | - | 0.729 | 0.058 | 0.080 | - | 11.43 | - | needed | 68 | 1578 | 1031207 | 0 | yes |
| hub-65536 | bfs | `icebug` |  |  | - | 15.697 | 0.346 | 0.022 | - | 65.98 | - |  | 216 | 4057 | - | 0 | yes |
| hub-65536 | bfs | `icecat` |  |  | - | 4.913 | 0.164 | 0.033 | - | 21.95 | - |  | 387 | 2698 | - | 0 | yes |
| hub-65536 | bfs | `grustcat` |  |  | - | 5.726 | 0.091 | 0.016 | - | 488.07 | - |  | 130 | 38258 | - | 0 | yes |
| hub-65536 | bfs | `grust` | first | counted | - | 5.018 | 0.044 | 0.009 | - | 106.25 | - | needed | 599 | 2596 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust` | second | counted | - | 3.883 | 0.080 | 0.020 | - | 106.25 | - | needed | 395 | 2596 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted` | first | counted | - | 3.996 | 0.007 | 0.002 | - | 38.95 | - | needed | 417 | 2917 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted` | second | counted | - | 3.712 | 0.034 | 0.009 | - | 38.95 | - | needed | 371 | 2917 | 4191009 | 0 | yes |
| hub-65536 | pagerank | `neo4j-graph` |  |  | 32 | 15.356 | 0.113 | 0.007 | 0.480 | 16.61 | - |  | 174 | 1448 | - | 0 | yes |
| hub-65536 | pagerank | `icebug` |  |  | 12 | 8.640 | 0.173 | 0.020 | 0.720 | 66.90 | - |  | 502 | 4057 | - | 0 | yes |
| hub-65536 | pagerank | `icecat` |  |  | 17 | 35.149 | 0.039 | 0.001 | 2.068 | 21.62 | - |  | 901 | 2697 | - | 0 | yes |
| hub-65536 | pagerank | `grustcat` |  |  | 17 | 32.924 | 0.861 | 0.026 | 1.937 | 480.02 | - |  | 387 | 37747 | - | 0 | yes |
| hub-65536 | pagerank | `grust` | first | counted | 17 | 18.232 | 0.302 | 0.017 | 1.072 | 101.77 | - | needed | 774 | 2596 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust` | second | counted | 17 | 9.503 | 0.203 | 0.021 | 0.559 | 101.77 | - | needed | 391 | 2596 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted` | first | counted | 17 | 8.391 | 0.161 | 0.019 | 0.494 | 45.37 | 6.40 | needed | 530 | 3121 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted` | second | counted | 17 | 8.180 | 0.123 | 0.015 | 0.481 | 45.37 | 6.40 | needed | 519 | 3121 | 17616940 | 0 | yes |
| hub-65536 | triangles | `neo4j-graph` |  |  | - | 3.476 | 0.026 | 0.008 | - | 16.28 | - |  | 53 | 1451 | - | 0 | yes |
| hub-65536 | triangles | `grust` | first | counted | - | 31.687 | 0.458 | 0.014 | - | 129.16 | - | needed | 1393 | 3620 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust` | second | counted | - | 30.762 | 0.072 | 0.002 | - | 129.16 | - | needed | 1291 | 3620 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted` | first | counted | - | 29.988 | 0.129 | 0.004 | - | 44.86 | - | needed | 1290 | 3942 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted` | second | counted | - | 29.903 | 0.101 | 0.003 | - | 44.86 | - | needed | 1290 | 3942 | 14971727 | 0 | yes |
| hub-65536 | wcc | `neo4j-graph` |  |  | - | 3.460 | 0.087 | 0.025 | - | 16.58 | - |  | 416 | 1452 | - | 0 | yes |
| hub-65536 | wcc | `icebug` |  |  | - | 20.497 | 0.600 | 0.029 | - | 61.53 | - |  | 239 | 4057 | - | 0 | yes |
| hub-65536 | wcc | `icecat` |  |  | - | 3.809 | 0.012 | 0.003 | - | 22.18 | - |  | 258 | 2698 | - | 0 | yes |
| hub-65536 | wcc | `grustcat` |  |  | - | 2.521 | 0.024 | 0.009 | - | 490.01 | - |  | 0 | 38258 | - | 0 | yes |
| hub-65536 | wcc | `grust` | first | counted | - | 2.815 | 0.038 | 0.014 | - | 108.94 | - | needed | 370 | 2596 | 4125496 | 0 | yes |
| hub-65536 | wcc | `grust` | second | counted | - | 2.059 | 0.097 | 0.047 | - | 108.94 | - | needed | 262 | 2596 | 4125496 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted` | first | counted | - | 2.202 | 0.052 | 0.024 | - | 39.77 | - | needed | 262 | 2410 | 4125491 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted` | second | counted | - | 2.147 | 0.015 | 0.007 | - | 39.77 | - | needed | 259 | 2410 | 4125491 | 0 | yes |
| layered-16384 | bfs | `icebug` |  |  | - | 0.562 | 0.025 | 0.044 | - | 2.82 | - |  | 36 | 458 | - | 0 | yes |
| layered-16384 | bfs | `icecat` |  |  | - | 0.400 | 0.001 | 0.002 | - | 1.81 | - |  | 67 | 544 | - | 0 | yes |
| layered-16384 | bfs | `grustcat` |  |  | - | 0.257 | 0.002 | 0.010 | - | 33.43 | - |  | 0 | 6872 | - | 0 | yes |
| layered-16384 | bfs | `grust` | first | counted | - | 0.531 | 0.009 | 0.018 | - | 7.20 | - | needed | 62 | 1036 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust` | second | counted | - | 0.508 | 0.002 | 0.003 | - | 7.20 | - | needed | 26 | 1036 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted` | first | counted | - | 0.531 | 0.004 | 0.007 | - | 6.71 | - | needed | 62 | 1053 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted` | second | counted | - | 0.482 | 0.002 | 0.005 | - | 6.71 | - | needed | 59 | 1053 | 347308 | 0 | yes |
| layered-16384 | pagerank | `icebug` |  |  | 69 | 9.039 | 0.188 | 0.021 | 0.131 | 2.87 | - |  | 200 | 458 | - | 0 | yes |
| layered-16384 | pagerank | `icecat` |  |  | 84 | 27.897 | 0.028 | 0.001 | 0.332 | 1.78 | - |  | 229 | 544 | - | 0 | yes |
| layered-16384 | pagerank | `grustcat` |  |  | 84 | 26.368 | 0.033 | 0.001 | 0.314 | 33.57 | - |  | 33 | 7383 | - | 0 | yes |
| layered-16384 | pagerank | `grust` | first | counted | 84 | 15.799 | 0.141 | 0.009 | 0.188 | 7.10 | - | needed | 346 | 1036 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust` | second | counted | 84 | 13.850 | 0.216 | 0.016 | 0.165 | 7.10 | - | needed | 99 | 1036 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted` | first | counted | 84 | 14.808 | 0.064 | 0.004 | 0.176 | 7.60 | 1.06 | needed | 139 | 1232 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted` | second | counted | 84 | 14.625 | 0.139 | 0.010 | 0.174 | 7.60 | 1.06 | needed | 132 | 1232 | 7307112 | 0 | yes |
| layered-16384 | triangles | `neo4j-graph` |  |  | - | 0.724 | 0.029 | 0.039 | - | 2.62 | - |  | 32 | 585 | - | 0 | yes |
| layered-16384 | triangles | `grust` | first | counted | - | 3.332 | 0.015 | 0.004 | - | 7.49 | - | needed | 491 | 1162 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust` | second | counted | - | 2.441 | 0.013 | 0.005 | - | 7.49 | - | needed | 390 | 1162 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted` | first | counted | - | 2.569 | 0.003 | 0.001 | - | 6.94 | - | needed | 389 | 1177 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted` | second | counted | - | 2.393 | 0.045 | 0.019 | - | 6.94 | - | needed | 389 | 1177 | 718265 | 0 | yes |
| layered-16384 | wcc | `neo4j-graph` |  |  | - | 1.220 | 0.020 | 0.017 | - | 2.62 | - |  | 116 | 580 | - | 0 | yes |
| layered-16384 | wcc | `icebug` |  |  | - | 1.011 | 0.018 | 0.018 | - | 2.82 | - |  | 43 | 458 | - | 0 | yes |
| layered-16384 | wcc | `icecat` |  |  | - | 0.505 | 0.003 | 0.006 | - | 1.81 | - |  | 66 | 544 | - | 0 | yes |
| layered-16384 | wcc | `grustcat` |  |  | - | 0.354 | 0.001 | 0.002 | - | 33.44 | - |  | 0 | 7383 | - | 0 | yes |
| layered-16384 | wcc | `grust` | first | counted | - | 1.168 | 0.025 | 0.021 | - | 7.08 | - | needed | 173 | 1036 | 341582 | 0 | yes |
| layered-16384 | wcc | `grust` | second | counted | - | 0.447 | 0.005 | 0.012 | - | 7.08 | - | needed | 68 | 1036 | 341582 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted` | first | counted | - | 0.464 | 0.003 | 0.005 | - | 6.47 | - | needed | 68 | 1052 | 341580 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted` | second | counted | - | 0.464 | 0.016 | 0.033 | - | 6.47 | - | needed | 67 | 1052 | 341580 | 0 | yes |
| layered-65536 | bfs | `icebug` |  |  | - | 2.836 | 0.024 | 0.009 | - | 11.42 | - |  | 132 | 1832 | - | 0 | yes |
| layered-65536 | bfs | `icecat` |  |  | - | 1.698 | 0.028 | 0.017 | - | 6.74 | - |  | 259 | 1652 | - | 0 | yes |
| layered-65536 | bfs | `grustcat` |  |  | - | 1.084 | 0.015 | 0.014 | - | 140.55 | - |  | 0 | 26649 | - | 0 | yes |
| layered-65536 | bfs | `grust` | first | counted | - | 2.105 | 0.009 | 0.004 | - | 33.16 | - | needed | 247 | 3145 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust` | second | counted | - | 2.332 | 0.005 | 0.002 | - | 33.16 | - | needed | 247 | 3145 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted` | first | counted | - | 2.113 | 0.007 | 0.003 | - | 24.57 | - | needed | 243 | 2881 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted` | second | counted | - | 2.015 | 0.016 | 0.008 | - | 24.57 | - | needed | 231 | 2881 | 1393359 | 0 | yes |
| layered-65536 | pagerank | `icebug` |  |  | 60 | 14.071 | 0.073 | 0.005 | 0.235 | 11.35 | - |  | 489 | 1832 | - | 0 | yes |
| layered-65536 | pagerank | `icecat` |  |  | 75 | 100.697 | 0.082 | 0.001 | 1.343 | 6.75 | - |  | 900 | 1652 | - | 0 | yes |
| layered-65536 | pagerank | `grustcat` |  |  | 75 | 95.139 | 0.053 | 0.001 | 1.269 | 139.57 | - |  | 388 | 26650 | - | 0 | yes |
| layered-65536 | pagerank | `grust` | first | counted | 75 | 26.262 | 0.339 | 0.013 | 0.350 | 33.04 | - | needed | 1031 | 3146 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust` | second | counted | 75 | 22.494 | 0.285 | 0.013 | 0.300 | 33.04 | - | needed | 389 | 3146 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted` | first | counted | 75 | 21.543 | 0.181 | 0.008 | 0.287 | 27.41 | 3.22 | needed | 537 | 3587 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted` | second | counted | 75 | 21.376 | 0.160 | 0.007 | 0.285 | 27.41 | 3.22 | needed | 518 | 3587 | 26313822 | 0 | yes |
| layered-65536 | triangles | `neo4j-graph` |  |  | - | 1.093 | 0.029 | 0.026 | - | 5.87 | - |  | 51 | 1937 | - | 0 | yes |
| layered-65536 | triangles | `grust` | first | counted | - | 10.700 | 0.104 | 0.010 | - | 34.95 | - | needed | 1638 | 3654 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust` | second | counted | - | 9.829 | 0.012 | 0.001 | - | 34.95 | - | needed | 1537 | 3654 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted` | first | counted | - | 9.769 | 0.039 | 0.004 | - | 26.81 | - | needed | 1536 | 3389 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted` | second | counted | - | 9.522 | 0.048 | 0.005 | - | 26.81 | - | needed | 1536 | 3389 | 2877576 | 0 | yes |
| layered-65536 | wcc | `neo4j-graph` |  |  | - | 3.164 | 0.053 | 0.017 | - | 5.78 | - |  | 416 | 1936 | - | 0 | yes |
| layered-65536 | wcc | `icebug` |  |  | - | 4.758 | 0.059 | 0.012 | - | 11.42 | - |  | 138 | 1832 | - | 0 | yes |
| layered-65536 | wcc | `icecat` |  |  | - | 2.128 | 0.014 | 0.006 | - | 7.31 | - |  | 259 | 2163 | - | 0 | yes |
| layered-65536 | wcc | `grustcat` |  |  | - | 1.468 | 0.008 | 0.005 | - | 140.18 | - |  | 0 | 26649 | - | 0 | yes |
| layered-65536 | wcc | `grust` | first | counted | - | 1.877 | 0.042 | 0.022 | - | 34.40 | - | needed | 371 | 3146 | 1368148 | 0 | yes |
| layered-65536 | wcc | `grust` | second | counted | - | 1.113 | 0.005 | 0.004 | - | 34.40 | - | needed | 262 | 3146 | 1368148 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted` | first | counted | - | 1.161 | 0.017 | 0.015 | - | 23.17 | - | needed | 263 | 2883 | 1368151 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted` | second | counted | - | 1.122 | 0.011 | 0.010 | - | 23.17 | - | needed | 260 | 2883 | 1368151 | 0 | yes |
| path-16384 | bfs | `icebug` |  |  | - | 0.266 | 0.003 | 0.012 | - | 1.80 | - |  | 36 | 450 | - | 0 | yes |
| path-16384 | bfs | `icecat` |  |  | - | 0.300 | 0.001 | 0.003 | - | 1.00 | - |  | 67 | 293 | - | 0 | yes |
| path-16384 | bfs | `grustcat` |  |  | - | 0.149 | 0.002 | 0.013 | - | 27.33 | - |  | 1 | 6430 | - | 0 | yes |
| path-16384 | bfs | `grust` | first | counted | - | 0.483 | 0.002 | 0.004 | - | 5.31 | - | needed | 69 | 745 | 245755 | 0 | yes |
| path-16384 | bfs | `grust` | second | counted | - | 0.437 | 0.001 | 0.002 | - | 5.31 | - | needed | 33 | 745 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@counted` | first | counted | - | 0.482 | 0.002 | 0.004 | - | 5.53 | - | needed | 66 | 794 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@counted` | second | counted | - | 0.435 | 0.003 | 0.007 | - | 5.53 | - | needed | 66 | 794 | 245755 | 0 | yes |
| path-16384 | pagerank | `icebug` |  |  | 54 | 6.767 | 0.016 | 0.002 | 0.125 | 1.80 | - |  | 200 | 450 | - | 0 | yes |
| path-16384 | pagerank | `icecat` |  |  | 58 | 11.415 | 0.017 | 0.001 | 0.197 | 0.99 | - |  | 230 | 293 | - | 0 | yes |
| path-16384 | pagerank | `grustcat` |  |  | 58 | 9.865 | 0.004 | 0.000 | 0.170 | 27.24 | - |  | 0 | 6430 | - | 0 | yes |
| path-16384 | pagerank | `grust` | first | counted | 58 | 10.875 | 0.486 | 0.045 | 0.188 | 5.26 | - | needed | 316 | 745 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust` | second | counted | 58 | 9.252 | 0.176 | 0.019 | 0.160 | 5.26 | - | needed | 99 | 745 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted` | first | counted | 58 | 10.073 | 0.203 | 0.020 | 0.174 | 6.34 | 0.79 | needed | 144 | 911 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted` | second | counted | 58 | 10.034 | 0.265 | 0.026 | 0.173 | 6.34 | 0.79 | needed | 134 | 911 | 4112319 | 0 | yes |
| path-16384 | triangles | `neo4j-graph` |  |  | - | 0.558 | 0.021 | 0.038 | - | 2.32 | - |  | 21 | 446 | - | 0 | yes |
| path-16384 | triangles | `grust` | first | counted | - | 2.336 | 0.035 | 0.015 | - | 5.39 | - | needed | 397 | 807 | 425970 | 0 | yes |
| path-16384 | triangles | `grust` | second | counted | - | 1.590 | 0.027 | 0.017 | - | 5.39 | - | needed | 296 | 807 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted` | first | counted | - | 1.690 | 0.015 | 0.009 | - | 5.69 | - | needed | 295 | 856 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted` | second | counted | - | 1.519 | 0.013 | 0.009 | - | 5.69 | - | needed | 296 | 856 | 425970 | 0 | yes |
| path-16384 | wcc | `neo4j-graph` |  |  | - | 0.984 | 0.016 | 0.016 | - | 2.32 | - |  | 110 | 441 | - | 0 | yes |
| path-16384 | wcc | `icebug` |  |  | - | 0.355 | 0.004 | 0.012 | - | 1.79 | - |  | 42 | 450 | - | 0 | yes |
| path-16384 | wcc | `icecat` |  |  | - | 0.283 | 0.003 | 0.011 | - | 0.97 | - |  | 67 | 293 | - | 0 | yes |
| path-16384 | wcc | `grustcat` |  |  | - | 0.160 | 0.002 | 0.015 | - | 27.14 | - |  | 0 | 6429 | - | 0 | yes |
| path-16384 | wcc | `grust` | first | counted | - | 1.145 | 0.009 | 0.008 | - | 5.28 | - | needed | 171 | 745 | 229369 | 0 | yes |
| path-16384 | wcc | `grust` | second | counted | - | 0.397 | 0.005 | 0.013 | - | 5.28 | - | needed | 68 | 745 | 229369 | 0 | yes |
| path-16384 | wcc | `grust-next@counted` | first | counted | - | 0.440 | 0.019 | 0.043 | - | 5.56 | - | needed | 68 | 795 | 229369 | 0 | yes |
| path-16384 | wcc | `grust-next@counted` | second | counted | - | 0.402 | 0.013 | 0.032 | - | 5.56 | - | needed | 66 | 795 | 229369 | 0 | yes |
| path-65536 | bfs | `icebug` |  |  | - | 1.050 | 0.006 | 0.005 | - | 7.19 | - |  | 133 | 1795 | - | 0 | yes |
| path-65536 | bfs | `icecat` |  |  | - | 1.181 | 0.025 | 0.021 | - | 4.37 | - |  | 259 | 1157 | - | 0 | yes |
| path-65536 | bfs | `grustcat` |  |  | - | 0.782 | 0.012 | 0.015 | - | 112.87 | - |  | 129 | 24248 | - | 0 | yes |
| path-65536 | bfs | `grust` | first | counted | - | 1.904 | 0.019 | 0.010 | - | 22.86 | - | needed | 274 | 2490 | 983035 | 0 | yes |
| path-65536 | bfs | `grust` | second | counted | - | 1.972 | 0.007 | 0.004 | - | 22.86 | - | needed | 274 | 2490 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@counted` | first | counted | - | 1.886 | 0.034 | 0.018 | - | 21.16 | - | needed | 272 | 2383 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@counted` | second | counted | - | 1.799 | 0.017 | 0.009 | - | 21.16 | - | needed | 258 | 2383 | 983035 | 0 | yes |
| path-65536 | pagerank | `icebug` |  |  | 46 | 10.763 | 0.014 | 0.001 | 0.234 | 7.16 | - |  | 503 | 1795 | - | 0 | yes |
| path-65536 | pagerank | `icecat` |  |  | 50 | 39.790 | 0.053 | 0.001 | 0.796 | 4.37 | - |  | 901 | 1157 | - | 0 | yes |
| path-65536 | pagerank | `grustcat` |  |  | 50 | 35.243 | 0.502 | 0.014 | 0.705 | 113.83 | - |  | 516 | 24248 | - | 0 | yes |
| path-65536 | pagerank | `grust` | first | counted | 50 | 16.404 | 0.064 | 0.004 | 0.328 | 24.45 | - | needed | 907 | 2490 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust` | second | counted | 50 | 12.655 | 0.177 | 0.014 | 0.253 | 24.45 | - | needed | 388 | 2490 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted` | first | counted | 50 | 13.076 | 0.286 | 0.022 | 0.262 | 23.37 | 2.53 | needed | 539 | 2834 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted` | second | counted | 50 | 12.867 | 0.419 | 0.033 | 0.257 | 23.37 | 2.53 | needed | 518 | 2834 | 14352327 | 0 | yes |
| path-65536 | triangles | `neo4j-graph` |  |  | - | 0.728 | 0.014 | 0.019 | - | 4.70 | - |  | 30 | 1423 | - | 0 | yes |
| path-65536 | triangles | `grust` | first | counted | - | 6.910 | 0.063 | 0.009 | - | 25.50 | - | needed | 1262 | 3255 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust` | second | counted | - | 5.862 | 0.047 | 0.008 | - | 25.50 | - | needed | 1160 | 3255 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted` | first | counted | - | 6.227 | 0.028 | 0.004 | - | 22.65 | - | needed | 1159 | 2636 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted` | second | counted | - | 5.860 | 0.036 | 0.006 | - | 22.65 | - | needed | 1159 | 2636 | 1703922 | 0 | yes |
| path-65536 | wcc | `neo4j-graph` |  |  | - | 2.597 | 0.152 | 0.058 | - | 4.70 | - |  | 428 | 1420 | - | 0 | yes |
| path-65536 | wcc | `icebug` |  |  | - | 1.321 | 0.018 | 0.014 | - | 7.14 | - |  | 138 | 1795 | - | 0 | yes |
| path-65536 | wcc | `icecat` |  |  | - | 1.189 | 0.011 | 0.009 | - | 4.40 | - |  | 258 | 1157 | - | 0 | yes |
| path-65536 | wcc | `grustcat` |  |  | - | 0.853 | 0.004 | 0.005 | - | 113.31 | - |  | 129 | 24248 | - | 0 | yes |
| path-65536 | wcc | `grust` | first | counted | - | 1.737 | 0.056 | 0.032 | - | 23.78 | - | needed | 369 | 2490 | 917497 | 0 | yes |
| path-65536 | wcc | `grust` | second | counted | - | 1.073 | 0.054 | 0.050 | - | 23.78 | - | needed | 262 | 2490 | 917497 | 0 | yes |
| path-65536 | wcc | `grust-next@counted` | first | counted | - | 1.084 | 0.025 | 0.023 | - | 22.08 | - | needed | 264 | 2383 | 917497 | 0 | yes |
| path-65536 | wcc | `grust-next@counted` | second | counted | - | 1.082 | 0.004 | 0.003 | - | 22.08 | - | needed | 261 | 2383 | 917497 | 0 | yes |
| uniform-16384 | bfs | `icebug` |  |  | - | 2.096 | 0.065 | 0.031 | - | 9.83 | - |  | 57 | 979 | - | 0 | yes |
| uniform-16384 | bfs | `icecat` |  |  | - | 0.970 | 0.012 | 0.013 | - | 7.24 | - |  | 99 | 2083 | - | 0 | yes |
| uniform-16384 | bfs | `grustcat` |  |  | - | 0.886 | 0.025 | 0.029 | - | 91.07 | - |  | 0 | 10816 | - | 0 | yes |
| uniform-16384 | bfs | `grust` | first | counted | - | 1.751 | 0.006 | 0.003 | - | 19.58 | - | needed | 68 | 1793 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust` | second | counted | - | 1.833 | 0.007 | 0.004 | - | 19.58 | - | needed | 32 | 1793 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted` | first | counted | - | 2.073 | 0.025 | 0.012 | - | 11.57 | - | needed | 65 | 2090 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted` | second | counted | - | 1.643 | 0.023 | 0.014 | - | 11.57 | - | needed | 65 | 2090 | 1048343 | 0 | yes |
| uniform-16384 | pagerank | `neo4j-graph` |  |  | 28 | 10.623 | 0.097 | 0.009 | 0.379 | 4.61 | - |  | 60 | 883 | - | 0 | yes |
| uniform-16384 | pagerank | `icebug` |  |  | 12 | 3.014 | 0.015 | 0.005 | 0.251 | 9.86 | - |  | 201 | 979 | - | 0 | yes |
| uniform-16384 | pagerank | `icecat` |  |  | 16 | 8.316 | 0.051 | 0.006 | 0.520 | 7.34 | - |  | 230 | 2083 | - | 0 | yes |
| uniform-16384 | pagerank | `grustcat` |  |  | 16 | 6.967 | 0.002 | 0.000 | 0.435 | 93.55 | - |  | 33 | 10816 | - | 0 | yes |
| uniform-16384 | pagerank | `grust` | first | counted | 16 | 6.422 | 0.126 | 0.020 | 0.401 | 20.31 | - | needed | 537 | 1793 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust` | second | counted | 16 | 3.596 | 0.043 | 0.012 | 0.225 | 20.31 | - | needed | 99 | 1793 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted` | first | counted | 16 | 3.700 | 0.130 | 0.035 | 0.231 | 13.40 | 2.28 | needed | 136 | 2143 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted` | second | counted | 16 | 3.585 | 0.019 | 0.005 | 0.224 | 13.40 | 2.28 | needed | 132 | 2143 | 4226299 | 0 | yes |
| uniform-16384 | triangles | `neo4j-graph` |  |  | - | 1.289 | 0.009 | 0.007 | - | 4.65 | - |  | 55 | 884 | - | 0 | yes |
| uniform-16384 | triangles | `grust` | first | counted | - | 8.698 | 0.007 | 0.001 | - | 23.49 | - | needed | 556 | 1794 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust` | second | counted | - | 7.770 | 0.032 | 0.004 | - | 23.49 | - | needed | 456 | 1794 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted` | first | counted | - | 7.881 | 0.021 | 0.003 | - | 11.40 | - | needed | 455 | 1065 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted` | second | counted | - | 7.513 | 0.038 | 0.005 | - | 11.40 | - | needed | 455 | 1065 | 3829630 | 0 | yes |
| uniform-16384 | wcc | `neo4j-graph` |  |  | - | 1.311 | 0.005 | 0.004 | - | 4.73 | - |  | 111 | 892 | - | 0 | yes |
| uniform-16384 | wcc | `icebug` |  |  | - | 2.866 | 0.061 | 0.021 | - | 9.84 | - |  | 68 | 979 | - | 0 | yes |
| uniform-16384 | wcc | `icecat` |  |  | - | 1.096 | 0.004 | 0.003 | - | 6.61 | - |  | 66 | 1573 | - | 0 | yes |
| uniform-16384 | wcc | `grustcat` |  |  | - | 0.754 | 0.005 | 0.007 | - | 91.57 | - |  | 0 | 10306 | - | 0 | yes |
| uniform-16384 | wcc | `grust` | first | counted | - | 1.533 | 0.010 | 0.007 | - | 19.11 | - | needed | 177 | 1793 | 1031991 | 0 | yes |
| uniform-16384 | wcc | `grust` | second | counted | - | 0.839 | 0.013 | 0.016 | - | 19.11 | - | needed | 70 | 1793 | 1031991 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted` | first | counted | - | 0.904 | 0.036 | 0.040 | - | 11.56 | - | needed | 68 | 2086 | 1032003 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted` | second | counted | - | 0.845 | 0.025 | 0.030 | - | 11.56 | - | needed | 67 | 2086 | 1032003 | 0 | yes |
| uniform-65536 | bfs | `icebug` |  |  | - | 15.713 | 0.095 | 0.006 | - | 66.57 | - |  | 216 | 3889 | - | 0 | yes |
| uniform-65536 | bfs | `icecat` |  |  | - | 5.231 | 0.117 | 0.022 | - | 21.33 | - |  | 387 | 1681 | - | 0 | yes |
| uniform-65536 | bfs | `grustcat` |  |  | - | 6.243 | 0.112 | 0.018 | - | 503.24 | - |  | 0 | 36104 | - | 0 | yes |
| uniform-65536 | bfs | `grust` | first | counted | - | 5.007 | 0.036 | 0.007 | - | 106.85 | - | needed | 560 | 2089 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust` | second | counted | - | 4.132 | 0.090 | 0.022 | - | 106.85 | - | needed | 414 | 2089 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted` | first | counted | - | 4.253 | 0.105 | 0.025 | - | 39.72 | - | needed | 433 | 2410 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted` | second | counted | - | 3.960 | 0.076 | 0.019 | - | 39.72 | - | needed | 391 | 2410 | 4193790 | 0 | yes |
| uniform-65536 | pagerank | `neo4j-graph` |  |  | 34 | 16.563 | 0.239 | 0.014 | 0.487 | 15.72 | - |  | 172 | 940 | - | 0 | yes |
| uniform-65536 | pagerank | `icebug` |  |  | 11 | 8.134 | 0.271 | 0.033 | 0.739 | 59.08 | - |  | 489 | 3889 | - | 0 | yes |
| uniform-65536 | pagerank | `icecat` |  |  | 16 | 33.430 | 0.116 | 0.003 | 2.089 | 20.65 | - |  | 902 | 1681 | - | 0 | yes |
| uniform-65536 | pagerank | `grustcat` |  |  | 16 | 30.157 | 0.450 | 0.015 | 1.885 | 480.12 | - |  | 0 | 36104 | - | 0 | yes |
| uniform-65536 | pagerank | `grust` | first | counted | 16 | 17.790 | 0.529 | 0.030 | 1.112 | 99.91 | - | needed | 773 | 2089 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust` | second | counted | 16 | 9.381 | 0.392 | 0.042 | 0.586 | 99.91 | - | needed | 389 | 2089 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted` | first | counted | 16 | 7.974 | 0.140 | 0.018 | 0.498 | 45.87 | 6.44 | needed | 532 | 3123 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted` | second | counted | 16 | 7.810 | 0.064 | 0.008 | 0.488 | 45.87 | 6.44 | needed | 519 | 3123 | 16907315 | 0 | yes |
| uniform-65536 | triangles | `neo4j-graph` |  |  | - | 4.075 | 0.132 | 0.032 | - | 15.92 | - |  | 54 | 948 | - | 0 | yes |
| uniform-65536 | triangles | `grust` | first | counted | - | 33.365 | 1.196 | 0.036 | - | 163.50 | - | needed | 883 | 2093 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust` | second | counted | - | 31.278 | 0.221 | 0.007 | - | 163.50 | - | needed | 781 | 2093 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted` | first | counted | - | 30.355 | 0.016 | 0.001 | - | 45.52 | - | needed | 780 | 2415 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted` | second | counted | - | 30.174 | 0.058 | 0.002 | - | 45.52 | - | needed | 780 | 2415 | 15327135 | 0 | yes |
| uniform-65536 | wcc | `neo4j-graph` |  |  | - | 3.655 | 0.190 | 0.052 | - | 15.69 | - |  | 417 | 940 | - | 0 | yes |
| uniform-65536 | wcc | `icebug` |  |  | - | 25.919 | 0.320 | 0.012 | - | 61.93 | - |  | 244 | 3889 | - | 0 | yes |
| uniform-65536 | wcc | `icecat` |  |  | - | 4.487 | 0.021 | 0.005 | - | 20.67 | - |  | 259 | 1681 | - | 0 | yes |
| uniform-65536 | wcc | `grustcat` |  |  | - | 3.111 | 0.013 | 0.004 | - | 488.60 | - |  | 0 | 36104 | - | 0 | yes |
| uniform-65536 | wcc | `grust` | first | counted | - | 3.313 | 0.203 | 0.061 | - | 106.01 | - | needed | 371 | 2089 | 4128524 | 0 | yes |
| uniform-65536 | wcc | `grust` | second | counted | - | 2.463 | 0.168 | 0.068 | - | 106.01 | - | needed | 262 | 2089 | 4128524 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted` | first | counted | - | 2.440 | 0.049 | 0.020 | - | 39.86 | - | needed | 264 | 2410 | 4128524 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted` | second | counted | - | 2.476 | 0.096 | 0.039 | - | 39.86 | - | needed | 260 | 2410 | 4128524 | 0 | yes |

### `large-one-thread.json`: large-one-thread

workers 1, concurrency 1, allocator glibc default, not pinned, 1 warmup + 5 repeats, steal over the run 10 ticks, 2331.5 s, unusable at MAD/median >= 0.25

| fixture | algorithm | participant | call | accounting | iters | total ms | MAD | MAD/median | per iter | build ms | incoming ms | prepare | minflt | minflt build | work units | steal | usable |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |
| hub-2097152 | pagerank | `neo4j-graph` |  |  | 26 | 2799.308 | 14.781 | 0.005 | 107.666 | 3696.16 | - |  | 1040 | 3782 | - | 5 | yes |
| hub-2097152 | pagerank | `icebug` |  |  | 10 | 5183.161 | 63.781 | 0.012 | 518.316 | 3628.08 | - |  | 1569 | 106004 | - | 5 | yes |
| hub-2097152 | pagerank | `icecat` |  |  | 16 | 3050.719 | 95.919 | 0.031 | 190.670 | 601.16 | - |  | 10704 | 6432 | - | 5 | yes |
| hub-2097152 | pagerank | `grustcat` |  |  | 16 | 3310.953 | 24.321 | 0.007 | 206.935 | 20336.71 | - |  | 6625 | 1090544 | - | 5 | yes |
| hub-2097152 | pagerank | `grust#1` | first | counted | 16 | 6581.110 | 71.456 | 0.011 | 411.319 | 4089.66 | - | needed | 3142 | 20941 | 540705943 | 5 | yes |
| hub-2097152 | pagerank | `grust#1` | second | counted | 16 | 5802.031 | 38.387 | 0.007 | 362.627 | 4089.66 | - | needed | 0 | 20941 | 540705943 | 5 | yes |
| hub-2097152 | pagerank | `grust#unset` | first | counted | 16 | 17228.595 | 33.901 | 0.002 | 1076.787 | 4104.10 | - | needed | 2595 | 21437 | 559594681 | 5 | yes |
| hub-2097152 | pagerank | `grust#unset` | second | counted | 16 | 17246.717 | 220.626 | 0.013 | 1077.920 | 4104.10 | - | needed | 519 | 21437 | 559594681 | 5 | yes |
| hub-2097152 | pagerank | `grust-next@counted#1` | first | counted | 16 | 3859.961 | 2.752 | 0.001 | 241.248 | 2290.40 | 686.14 | needed | 1559 | 22900 | 540705943 | 5 | yes |
| hub-2097152 | pagerank | `grust-next@counted#1` | second | counted | 16 | 3812.725 | 101.138 | 0.027 | 238.295 | 2290.40 | 686.14 | needed | 517 | 22900 | 540705943 | 5 | yes |
| hub-2097152 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 16 | 3658.758 | 72.118 | 0.020 | 228.672 | 2060.04 | 668.09 | needed | 1559 | 22901 | - | 5 | yes |
| hub-2097152 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 16 | 3657.490 | 87.738 | 0.024 | 228.593 | 2060.04 | 668.09 | needed | 517 | 22901 | - | 5 | yes |
| hub-2097152 | pagerank | `grust-next@unchecked#1` | first | unchecked | 16 | 3522.522 | 66.728 | 0.019 | 220.158 | 2030.08 | 650.92 | needed | 1559 | 23410 | - | 5 | yes |
| hub-2097152 | pagerank | `grust-next@unchecked#1` | second | unchecked | 16 | 3547.821 | 51.460 | 0.015 | 221.739 | 2030.08 | 650.92 | needed | 517 | 23410 | - | 5 | yes |
| hub-2097152 | pagerank | `grust-next@counted#unset` | first | counted | 16 | 7310.901 | 133.018 | 0.018 | 456.931 | 1923.44 | - | needed | 2595 | 20288 | 559594681 | 5 | yes |
| hub-2097152 | pagerank | `grust-next@counted#unset` | second | counted | 16 | 7378.805 | 66.927 | 0.009 | 461.175 | 1923.44 | - | needed | 519 | 20288 | 559594681 | 5 | yes |
| hub-2097152 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 16 | 5932.335 | 97.077 | 0.016 | 370.771 | 1457.88 | - | needed | 2595 | 20799 | - | 5 | yes |
| hub-2097152 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 16 | 6014.222 | 58.261 | 0.010 | 375.889 | 1457.88 | - | needed | 519 | 20799 | - | 5 | yes |
| hub-2097152 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 16 | 5925.811 | 42.847 | 0.007 | 370.363 | 1424.42 | - | needed | 2595 | 20799 | - | 5 | yes |
| hub-2097152 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 16 | 5894.268 | 109.628 | 0.019 | 368.392 | 1424.42 | - | needed | 519 | 20799 | - | 5 | yes |
| uniform-2097152 | pagerank | `neo4j-graph` |  |  | 26 | 2743.317 | 60.237 | 0.022 | 105.512 | 3690.72 | - |  | 1038 | 1851 | - | 5 | yes |
| uniform-2097152 | pagerank | `icebug` |  |  | 10 | 5312.451 | 138.110 | 0.026 | 531.245 | 3288.96 | - |  | 1573 | 100284 | - | 5 | yes |
| uniform-2097152 | pagerank | `icecat` |  |  | 16 | 3081.580 | 62.086 | 0.020 | 192.599 | 600.56 | - |  | 10704 | 5123 | - | 5 | yes |
| uniform-2097152 | pagerank | `grustcat` |  |  | 16 | 3836.222 | 12.175 | 0.003 | 239.764 | 22929.62 | - |  | 1 | 1081011 | - | 5 | yes |
| uniform-2097152 | pagerank | `grust#1` | first | counted | 16 | 6999.183 | 112.795 | 0.016 | 437.449 | 4088.92 | - | needed | 2659 | 19093 | 541064143 | 5 | yes |
| uniform-2097152 | pagerank | `grust#1` | second | counted | 16 | 6164.164 | 55.862 | 0.009 | 385.260 | 4088.92 | - | needed | 0 | 19093 | 541064143 | 5 | yes |
| uniform-2097152 | pagerank | `grust#unset` | first | counted | 16 | 17040.905 | 206.425 | 0.012 | 1065.057 | 4061.65 | - | needed | 2595 | 19093 | 559938553 | 5 | yes |
| uniform-2097152 | pagerank | `grust#unset` | second | counted | 16 | 17070.930 | 105.844 | 0.006 | 1066.933 | 4061.65 | - | needed | 519 | 19093 | 559938553 | 5 | yes |
| uniform-2097152 | pagerank | `grust-next@counted#1` | first | counted | 16 | 3821.938 | 99.411 | 0.026 | 238.871 | 2231.97 | 636.85 | needed | 1559 | 21081 | 541064143 | 5 | yes |
| uniform-2097152 | pagerank | `grust-next@counted#1` | second | counted | 16 | 3797.860 | 144.290 | 0.038 | 237.366 | 2231.97 | 636.85 | needed | 517 | 21081 | 541064143 | 5 | yes |
| uniform-2097152 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 16 | 3781.660 | 156.426 | 0.041 | 236.354 | 2005.28 | 619.71 | needed | 1559 | 21081 | - | 5 | yes |
| uniform-2097152 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 16 | 3630.696 | 335.717 | 0.092 | 226.919 | 2005.28 | 619.71 | needed | 517 | 21081 | - | 5 | yes |
| uniform-2097152 | pagerank | `grust-next@unchecked#1` | first | unchecked | 16 | 3610.510 | 272.063 | 0.075 | 225.657 | 2006.67 | 621.99 | needed | 1559 | 21081 | - | 5 | yes |
| uniform-2097152 | pagerank | `grust-next@unchecked#1` | second | unchecked | 16 | 3615.813 | 71.834 | 0.020 | 225.988 | 2006.67 | 621.99 | needed | 517 | 21081 | - | 5 | yes |
| uniform-2097152 | pagerank | `grust-next@counted#unset` | first | counted | 16 | 6961.878 | 126.419 | 0.018 | 435.117 | 1911.22 | - | needed | 2595 | 18952 | 559938553 | 5 | yes |
| uniform-2097152 | pagerank | `grust-next@counted#unset` | second | counted | 16 | 7023.501 | 278.988 | 0.040 | 438.969 | 1911.22 | - | needed | 519 | 18952 | 559938553 | 5 | yes |
| uniform-2097152 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 16 | 5649.177 | 291.572 | 0.052 | 353.074 | 1433.02 | - | needed | 2595 | 18952 | - | 5 | yes |
| uniform-2097152 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 16 | 5756.655 | 230.337 | 0.040 | 359.791 | 1433.02 | - | needed | 519 | 18952 | - | 5 | yes |
| uniform-2097152 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 16 | 5656.099 | 147.644 | 0.026 | 353.506 | 1418.61 | - | needed | 2595 | 18952 | - | 5 | yes |
| uniform-2097152 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 16 | 5693.098 | 108.522 | 0.019 | 355.819 | 1418.61 | - | needed | 519 | 18952 | - | 5 | yes |

### `large-full-width.json`: large-full-width

workers 16, concurrency 16, allocator glibc default, not pinned, 1 warmup + 5 repeats, steal over the run 3 ticks, 812.4 s, unusable at MAD/median >= 0.25

| fixture | algorithm | participant | call | accounting | iters | total ms | MAD | MAD/median | per iter | build ms | incoming ms | prepare | minflt | minflt build | work units | steal | usable |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |
| hub-2097152 | pagerank | `neo4j-graph` |  |  | 28 | 277.246 | 1.974 | 0.007 | 9.902 | 463.79 | - |  | 1112 | 3985 | - | 2 | yes |
| hub-2097152 | pagerank | `icebug` |  |  | 10 | 518.716 | 7.089 | 0.014 | 51.872 | 3624.16 | - |  | 1659 | 106004 | - | 2 | yes |
| hub-2097152 | pagerank | `icecat` |  |  | 16 | 3147.449 | 26.396 | 0.008 | 196.716 | 605.64 | - |  | 10704 | 6447 | - | 2 | yes |
| hub-2097152 | pagerank | `grustcat` |  |  | 16 | 3292.034 | 63.314 | 0.019 | 205.752 | 20510.65 | - |  | 6625 | 1090544 | - | 2 | yes |
| hub-2097152 | pagerank | `grust` | first | counted | 16 | 1385.340 | 22.932 | 0.017 | 86.584 | 4110.23 | - | needed | 3308 | 20941 | 540705943 | 2 | yes |
| hub-2097152 | pagerank | `grust` | second | counted | 16 | 584.947 | 5.365 | 0.009 | 36.559 | 4110.23 | - | needed | 14 | 20941 | 540705943 | 2 | yes |
| hub-2097152 | pagerank | `grust-next@counted` | first | counted | 16 | 278.456 | 2.120 | 0.008 | 17.404 | 1692.12 | 253.64 | needed | 1625 | 22632 | 540705943 | 2 | yes |
| hub-2097152 | pagerank | `grust-next@counted` | second | counted | 16 | 263.120 | 22.097 | 0.084 | 16.445 | 1692.12 | 253.64 | needed | 2054 | 22632 | 540705943 | 2 | yes |
| hub-2097152 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 16 | 256.360 | 16.475 | 0.064 | 16.022 | 1458.02 | 234.91 | needed | 1625 | 22634 | - | 2 | yes |
| hub-2097152 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 16 | 273.485 | 14.689 | 0.054 | 17.093 | 1458.02 | 234.91 | needed | 2055 | 22634 | - | 2 | yes |
| hub-2097152 | pagerank | `grust-next@unchecked` | first | unchecked | 16 | 240.618 | 1.854 | 0.008 | 15.039 | 1439.30 | 231.73 | needed | 1622 | 22634 | - | 2 | yes |
| hub-2097152 | pagerank | `grust-next@unchecked` | second | unchecked | 16 | 286.428 | 16.390 | 0.057 | 17.902 | 1439.30 | 231.73 | needed | 2054 | 22634 | - | 2 | yes |
| uniform-2097152 | pagerank | `neo4j-graph` |  |  | 28 | 283.995 | 3.720 | 0.013 | 10.143 | 464.31 | - |  | 1110 | 2582 | - | 1 | yes |
| uniform-2097152 | pagerank | `icebug` |  |  | 10 | 555.115 | 28.871 | 0.052 | 55.511 | 3306.78 | - |  | 1660 | 100284 | - | 1 | yes |
| uniform-2097152 | pagerank | `icecat` |  |  | 16 | 3121.823 | 32.915 | 0.011 | 195.114 | 598.48 | - |  | 10705 | 5122 | - | 1 | yes |
| uniform-2097152 | pagerank | `grustcat` |  |  | 16 | 3850.627 | 43.416 | 0.011 | 240.664 | 23195.37 | - |  | 0 | 1081010 | - | 1 | yes |
| uniform-2097152 | pagerank | `grust` | first | counted | 16 | 1375.912 | 31.938 | 0.023 | 85.994 | 4136.32 | - | needed | 2828 | 19093 | 541064143 | 1 | yes |
| uniform-2097152 | pagerank | `grust` | second | counted | 16 | 614.915 | 11.231 | 0.018 | 38.432 | 4136.32 | - | needed | 12 | 19093 | 541064143 | 1 | yes |
| uniform-2097152 | pagerank | `grust-next@counted` | first | counted | 16 | 275.172 | 3.470 | 0.013 | 17.198 | 1699.25 | 257.62 | needed | 1626 | 20812 | 541064143 | 1 | yes |
| uniform-2097152 | pagerank | `grust-next@counted` | second | counted | 16 | 274.660 | 18.413 | 0.067 | 17.166 | 1699.25 | 257.62 | needed | 2053 | 20812 | 541064143 | 1 | yes |
| uniform-2097152 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 16 | 258.630 | 15.606 | 0.060 | 16.164 | 1457.46 | 241.52 | needed | 1625 | 20810 | - | 1 | yes |
| uniform-2097152 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 16 | 253.565 | 6.500 | 0.026 | 15.848 | 1457.46 | 241.52 | needed | 2055 | 20810 | - | 1 | yes |
| uniform-2097152 | pagerank | `grust-next@unchecked` | first | unchecked | 16 | 250.919 | 5.431 | 0.022 | 15.682 | 1445.28 | 236.23 | needed | 1626 | 20813 | - | 1 | yes |
| uniform-2097152 | pagerank | `grust-next@unchecked` | second | unchecked | 16 | 251.233 | 8.173 | 0.033 | 15.702 | 1445.28 | 236.23 | needed | 2053 | 20813 | - | 1 | yes |

### `xlarge-one-thread.json`: xlarge-one-thread

workers 1, concurrency 1, allocator glibc default, not pinned, 1 warmup + 5 repeats, steal over the run 21 ticks, 5128.8 s, unusable at MAD/median >= 0.25

| fixture | algorithm | participant | call | accounting | iters | total ms | MAD | MAD/median | per iter | build ms | incoming ms | prepare | minflt | minflt build | work units | steal | usable |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |
| hub-4194304 | pagerank | `neo4j-graph` |  |  | 23 | 6991.528 | 176.589 | 0.025 | 303.979 | 7715.62 | - |  | 1045 | 4484 | - | 11 | yes |
| hub-4194304 | pagerank | `icebug` |  |  | 10 | 11825.667 | 206.462 | 0.017 | 1182.567 | 7636.23 | - |  | 1597 | 210997 | - | 11 | yes |
| hub-4194304 | pagerank | `icecat` |  |  | 16 | 7064.356 | 28.875 | 0.004 | 441.522 | 1191.87 | - |  | 19024 | 7749 | - | 11 | yes |
| hub-4194304 | pagerank | `grustcat` |  |  | 16 | 7349.000 | 45.757 | 0.006 | 459.312 | 46257.51 | - |  | 10832 | 2170076 | - | 11 | yes |
| hub-4194304 | pagerank | `grust#1` | first | counted | 16 | 14778.234 | 100.498 | 0.007 | 923.640 | 8254.67 | - | needed | 3227 | 38314 | 1081412859 | 11 | yes |
| hub-4194304 | pagerank | `grust#1` | second | counted | 16 | 13074.011 | 130.005 | 0.010 | 817.126 | 8254.67 | - | needed | 1584 | 38314 | 1081412859 | 11 | yes |
| hub-4194304 | pagerank | `grust#unset` | first | counted | 16 | 35911.291 | 191.930 | 0.005 | 2244.456 | 8232.86 | - | needed | 2640 | 38810 | 1119190297 | 11 | yes |
| hub-4194304 | pagerank | `grust#unset` | second | counted | 16 | 35862.504 | 212.075 | 0.006 | 2241.407 | 8232.86 | - | needed | 2640 | 38810 | 1119190297 | 11 | yes |
| hub-4194304 | pagerank | `grust-next@counted#1` | first | counted | 16 | 8695.933 | 24.388 | 0.003 | 543.496 | 4727.68 | 1482.25 | needed | 2112 | 40197 | 1081412859 | 11 | yes |
| hub-4194304 | pagerank | `grust-next@counted#1` | second | counted | 16 | 8709.381 | 18.385 | 0.002 | 544.336 | 4727.68 | 1482.25 | needed | 2112 | 40197 | 1081412859 | 11 | yes |
| hub-4194304 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 16 | 8472.429 | 101.714 | 0.012 | 529.527 | 4281.78 | 1455.54 | needed | 2112 | 40707 | - | 11 | yes |
| hub-4194304 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 16 | 8411.730 | 44.556 | 0.005 | 525.733 | 4281.78 | 1455.54 | needed | 2112 | 40707 | - | 11 | yes |
| hub-4194304 | pagerank | `grust-next@unchecked#1` | first | unchecked | 16 | 8058.375 | 69.092 | 0.009 | 503.648 | 4197.08 | 1413.80 | needed | 2112 | 40707 | - | 11 | yes |
| hub-4194304 | pagerank | `grust-next@unchecked#1` | second | unchecked | 16 | 8057.104 | 87.847 | 0.011 | 503.569 | 4197.08 | 1413.80 | needed | 2112 | 40707 | - | 11 | yes |
| hub-4194304 | pagerank | `grust-next@counted#unset` | first | counted | 16 | 15647.713 | 133.877 | 0.009 | 977.982 | 3880.24 | - | needed | 2640 | 37007 | 1119190297 | 11 | yes |
| hub-4194304 | pagerank | `grust-next@counted#unset` | second | counted | 16 | 15597.024 | 106.249 | 0.007 | 974.814 | 3880.24 | - | needed | 2640 | 37007 | 1119190297 | 11 | yes |
| hub-4194304 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 16 | 13012.930 | 35.064 | 0.003 | 813.308 | 2940.24 | - | needed | 2640 | 37518 | - | 11 | yes |
| hub-4194304 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 16 | 13045.409 | 28.795 | 0.002 | 815.338 | 2940.24 | - | needed | 2640 | 37518 | - | 11 | yes |
| hub-4194304 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 16 | 12983.581 | 130.981 | 0.010 | 811.474 | 2895.15 | - | needed | 2640 | 37014 | - | 11 | yes |
| hub-4194304 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 16 | 13001.529 | 160.046 | 0.012 | 812.596 | 2895.15 | - | needed | 2640 | 37014 | - | 11 | yes |
| uniform-4194304 | pagerank | `neo4j-graph` |  |  | 29 | 9137.708 | 260.539 | 0.029 | 315.093 | 7653.94 | - |  | 1046 | 1642 | - | 10 | yes |
| uniform-4194304 | pagerank | `icebug` |  |  | 9 | 11464.329 | 235.676 | 0.021 | 1273.814 | 7094.76 | - |  | 1592 | 200030 | - | 10 | yes |
| uniform-4194304 | pagerank | `icecat` |  |  | 16 | 7517.185 | 19.792 | 0.003 | 469.824 | 1197.98 | - |  | 18513 | 6154 | - | 10 | yes |
| uniform-4194304 | pagerank | `grustcat` |  |  | 16 | 8617.930 | 93.537 | 0.011 | 538.621 | 48358.32 | - |  | 17 | 2157409 | - | 10 | yes |
| uniform-4194304 | pagerank | `grust#1` | first | counted | 16 | 15671.379 | 112.879 | 0.007 | 979.461 | 8205.82 | - | needed | 2261 | 36151 | 1082129509 | 10 | yes |
| uniform-4194304 | pagerank | `grust#1` | second | counted | 16 | 14150.995 | 74.580 | 0.005 | 884.437 | 8205.82 | - | needed | 1073 | 36151 | 1082129509 | 10 | yes |
| uniform-4194304 | pagerank | `grust#unset` | first | counted | 16 | 35726.687 | 89.212 | 0.002 | 2232.918 | 8344.81 | - | needed | 2129 | 36151 | 1119878281 | 10 | yes |
| uniform-4194304 | pagerank | `grust#unset` | second | counted | 16 | 35547.340 | 61.751 | 0.002 | 2221.709 | 8344.81 | - | needed | 2129 | 36151 | 1119878281 | 10 | yes |
| uniform-4194304 | pagerank | `grust-next@counted#1` | first | counted | 16 | 9001.380 | 40.232 | 0.004 | 562.586 | 4715.27 | 1469.27 | needed | 2112 | 37579 | 1082129509 | 10 | yes |
| uniform-4194304 | pagerank | `grust-next@counted#1` | second | counted | 16 | 8987.694 | 46.435 | 0.005 | 561.731 | 4715.27 | 1469.27 | needed | 2112 | 37579 | 1082129509 | 10 | yes |
| uniform-4194304 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 16 | 8836.784 | 54.051 | 0.006 | 552.299 | 4315.40 | 1455.38 | needed | 2112 | 37579 | - | 10 | yes |
| uniform-4194304 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 16 | 8817.652 | 22.241 | 0.003 | 551.103 | 4315.40 | 1455.38 | needed | 2112 | 37579 | - | 10 | yes |
| uniform-4194304 | pagerank | `grust-next@unchecked#1` | first | unchecked | 16 | 8452.580 | 44.065 | 0.005 | 528.286 | 4243.43 | 1431.33 | needed | 2112 | 37579 | - | 10 | yes |
| uniform-4194304 | pagerank | `grust-next@unchecked#1` | second | unchecked | 16 | 8523.079 | 70.791 | 0.008 | 532.692 | 4243.43 | 1431.33 | needed | 2112 | 37579 | - | 10 | yes |
| uniform-4194304 | pagerank | `grust-next@counted#unset` | first | counted | 16 | 15124.712 | 144.475 | 0.010 | 945.294 | 3910.66 | - | needed | 2129 | 35867 | 1119878281 | 10 | yes |
| uniform-4194304 | pagerank | `grust-next@counted#unset` | second | counted | 16 | 15050.219 | 172.932 | 0.011 | 940.639 | 3910.66 | - | needed | 2129 | 35867 | 1119878281 | 10 | yes |
| uniform-4194304 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 16 | 12422.129 | 13.693 | 0.001 | 776.383 | 2947.30 | - | needed | 2129 | 35867 | - | 10 | yes |
| uniform-4194304 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 16 | 12466.857 | 64.737 | 0.005 | 779.179 | 2947.30 | - | needed | 2129 | 35867 | - | 10 | yes |
| uniform-4194304 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 16 | 12418.804 | 121.387 | 0.010 | 776.175 | 2930.69 | - | needed | 2129 | 35867 | - | 10 | yes |
| uniform-4194304 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 16 | 12369.031 | 54.061 | 0.004 | 773.064 | 2930.69 | - | needed | 2129 | 35867 | - | 10 | yes |

### `xlarge-full-width.json`: xlarge-full-width

workers 16, concurrency 16, allocator glibc default, not pinned, 1 warmup + 5 repeats, steal over the run 7 ticks, 1693.3 s, unusable at MAD/median >= 0.25

| fixture | algorithm | participant | call | accounting | iters | total ms | MAD | MAD/median | per iter | build ms | incoming ms | prepare | minflt | minflt build | work units | steal | usable |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |
| hub-4194304 | pagerank | `neo4j-graph` |  |  | 19 | 416.488 | 0.577 | 0.001 | 21.920 | 985.01 | - |  | 1123 | 4766 | - | 3 | yes |
| hub-4194304 | pagerank | `icebug` |  |  | 10 | 1192.337 | 5.136 | 0.004 | 119.234 | 7732.37 | - |  | 1686 | 210997 | - | 3 | yes |
| hub-4194304 | pagerank | `icecat` |  |  | 16 | 6956.019 | 125.065 | 0.018 | 434.751 | 1217.44 | - |  | 19025 | 7749 | - | 3 | yes |
| hub-4194304 | pagerank | `grustcat` |  |  | 16 | 7494.994 | 66.690 | 0.009 | 468.437 | 46252.42 | - |  | 10832 | 2170076 | - | 3 | yes |
| hub-4194304 | pagerank | `grust` | first | counted | 16 | 3136.148 | 52.845 | 0.017 | 196.009 | 8238.19 | - | needed | 3448 | 37803 | 1081412859 | 3 | yes |
| hub-4194304 | pagerank | `grust` | second | counted | 16 | 1455.253 | 24.860 | 0.017 | 90.953 | 8238.19 | - | needed | 1602 | 37803 | 1081412859 | 3 | yes |
| hub-4194304 | pagerank | `grust-next@counted` | first | counted | 16 | 792.726 | 38.460 | 0.049 | 49.545 | 3463.73 | 539.23 | needed | 1707 | 39014 | 1081412859 | 3 | yes |
| hub-4194304 | pagerank | `grust-next@counted` | second | counted | 16 | 815.819 | 16.574 | 0.020 | 50.989 | 3463.73 | 539.23 | needed | 1619 | 39014 | 1081412859 | 3 | yes |
| hub-4194304 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 16 | 772.109 | 41.042 | 0.053 | 48.257 | 2961.44 | 493.13 | needed | 1703 | 39526 | - | 3 | yes |
| hub-4194304 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 16 | 784.262 | 16.776 | 0.021 | 49.016 | 2961.44 | 493.13 | needed | 1621 | 39526 | - | 3 | yes |
| hub-4194304 | pagerank | `grust-next@unchecked` | first | unchecked | 16 | 749.199 | 27.727 | 0.037 | 46.825 | 2971.26 | 487.19 | needed | 1207 | 39016 | - | 3 | yes |
| hub-4194304 | pagerank | `grust-next@unchecked` | second | unchecked | 16 | 766.823 | 24.526 | 0.032 | 47.926 | 2971.26 | 487.19 | needed | 1117 | 39016 | - | 3 | yes |
| uniform-4194304 | pagerank | `neo4j-graph` |  |  | 29 | 651.095 | 26.695 | 0.041 | 22.452 | 994.75 | - |  | 1129 | 1864 | - | 4 | yes |
| uniform-4194304 | pagerank | `icebug` |  |  | 9 | 1186.872 | 12.166 | 0.010 | 131.875 | 7147.06 | - |  | 1690 | 200030 | - | 4 | yes |
| uniform-4194304 | pagerank | `icecat` |  |  | 16 | 7546.967 | 59.778 | 0.008 | 471.685 | 1225.62 | - |  | 18513 | 6154 | - | 4 | yes |
| uniform-4194304 | pagerank | `grustcat` |  |  | 16 | 8827.123 | 59.574 | 0.007 | 551.695 | 48526.24 | - |  | 17 | 2157408 | - | 4 | yes |
| uniform-4194304 | pagerank | `grust` | first | counted | 16 | 3272.918 | 23.784 | 0.007 | 204.557 | 8340.10 | - | needed | 2482 | 36151 | 1082129509 | 4 | yes |
| uniform-4194304 | pagerank | `grust` | second | counted | 16 | 1630.547 | 1.228 | 0.001 | 101.909 | 8340.10 | - | needed | 1094 | 36151 | 1082129509 | 4 | yes |
| uniform-4194304 | pagerank | `grust-next@counted` | first | counted | 16 | 871.095 | 9.447 | 0.011 | 54.443 | 3533.60 | 580.25 | needed | 1196 | 36400 | 1082129509 | 4 | yes |
| uniform-4194304 | pagerank | `grust-next@counted` | second | counted | 16 | 880.330 | 12.045 | 0.014 | 55.021 | 3533.60 | 580.25 | needed | 1110 | 36400 | 1082129509 | 4 | yes |
| uniform-4194304 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 16 | 877.400 | 3.118 | 0.004 | 54.837 | 3012.88 | 530.67 | needed | 1199 | 36401 | - | 4 | yes |
| uniform-4194304 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 16 | 874.011 | 7.125 | 0.008 | 54.626 | 3012.88 | 530.67 | needed | 1111 | 36401 | - | 4 | yes |
| uniform-4194304 | pagerank | `grust-next@unchecked` | first | unchecked | 16 | 857.589 | 15.764 | 0.018 | 53.599 | 3031.82 | 529.64 | needed | 1200 | 36401 | - | 4 | yes |
| uniform-4194304 | pagerank | `grust-next@unchecked` | second | unchecked | 16 | 853.973 | 4.374 | 0.005 | 53.373 | 3031.82 | 529.64 | needed | 1110 | 36401 | - | 4 | yes |

