### `full-width.json`: full-width

workers 16, concurrency 16, allocator glibc default, not pinned, 1 warmup + 5 repeats, steal over the run 0 ticks, 101.8 s, unusable at MAD/median >= 0.25

Not timed (no agreeing parity row): neo4j-graph pagerank layered-16384.edges, neo4j-graph pagerank layered-65536.edges, neo4j-graph pagerank path-16384.edges, neo4j-graph pagerank path-65536.edges 

| fixture | algorithm | participant | call | accounting | iters | total ms | MAD | MAD/median | per iter | build ms | incoming ms | prepare | minflt | minflt build | work units | steal | usable |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |
| hub-16384 | bfs | `icebug` |  |  | - | 1.448 | 0.053 | 0.036 | - | 9.31 | - |  | 57 | 1018 | - | 0 | yes |
| hub-16384 | bfs | `icecat` |  |  | - | 0.813 | 0.012 | 0.015 | - | 5.71 | - |  | 97 | 1554 | - | 0 | yes |
| hub-16384 | bfs | `grustcat` |  |  | - | 0.582 | 0.007 | 0.011 | - | 78.17 | - |  | 0 | 9804 | - | 0 | yes |
| hub-16384 | bfs | `grust` | first | counted | - | 1.522 | 0.004 | 0.002 | - | 17.20 | - | needed | 36 | 1787 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust` | second | counted | - | 1.466 | 0.009 | 0.006 | - | 17.20 | - | needed | 0 | 1787 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted` | first | counted | - | 1.543 | 0.007 | 0.004 | - | 10.68 | - | needed | 0 | 2045 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted` | second | counted | - | 1.470 | 0.009 | 0.006 | - | 10.68 | - | needed | 0 | 2045 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@work-uncounted` | first | work-uncounted | - | 0.941 | 0.049 | 0.052 | - | 9.14 | - | needed | 0 | 2039 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@work-uncounted` | second | work-uncounted | - | 0.850 | 0.014 | 0.016 | - | 9.14 | - | needed | 0 | 2039 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@unchecked` | first | unchecked | - | 0.807 | 0.012 | 0.015 | - | 8.62 | - | needed | 0 | 2042 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@unchecked` | second | unchecked | - | 0.729 | 0.005 | 0.007 | - | 8.62 | - | needed | 0 | 2042 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@counted+eager` | first | counted | - | 1.471 | 0.011 | 0.008 | - | 11.92 | 1.62 | always | 0 | 1790 | 1489517 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted+eager` | second | counted | - | 1.446 | 0.003 | 0.002 | - | 11.92 | 1.62 | always | 0 | 1790 | 1489517 | 0 | yes |
| hub-16384 | pagerank | `neo4j-graph` |  |  | 36 | 13.371 | 0.071 | 0.005 | 0.371 | 4.41 | - |  | 36 | 882 | - | 0 | yes |
| hub-16384 | pagerank | `icebug` |  |  | 12 | 2.799 | 0.031 | 0.011 | 0.233 | 9.40 | - |  | 201 | 1018 | - | 0 | yes |
| hub-16384 | pagerank | `icecat` |  |  | 17 | 8.479 | 0.008 | 0.001 | 0.499 | 5.81 | - |  | 130 | 1555 | - | 0 | yes |
| hub-16384 | pagerank | `grustcat` |  |  | 17 | 7.255 | 0.003 | 0.000 | 0.427 | 77.86 | - |  | 1 | 9804 | - | 0 | yes |
| hub-16384 | pagerank | `grust` | first | counted | 17 | 6.245 | 0.121 | 0.019 | 0.367 | 16.86 | - | needed | 484 | 1787 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust` | second | counted | 17 | 3.462 | 0.017 | 0.005 | 0.204 | 16.86 | - | needed | 0 | 1787 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted` | first | counted | 17 | 3.499 | 0.064 | 0.018 | 0.206 | 12.54 | 1.60 | needed | 5 | 2300 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted` | second | counted | 17 | 3.293 | 0.011 | 0.003 | 0.194 | 12.54 | 1.60 | needed | 1 | 2300 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 17 | 2.977 | 0.111 | 0.037 | 0.175 | 10.03 | 1.41 | needed | 4 | 1791 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 17 | 2.797 | 0.003 | 0.001 | 0.165 | 10.03 | 1.41 | needed | 0 | 1791 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@unchecked` | first | unchecked | 17 | 2.873 | 0.027 | 0.009 | 0.169 | 9.92 | 1.39 | needed | 6 | 2300 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@unchecked` | second | unchecked | 17 | 2.785 | 0.048 | 0.017 | 0.164 | 9.92 | 1.39 | needed | 0 | 2300 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted+eager` | first | counted | 17 | 3.427 | 0.013 | 0.004 | 0.202 | 12.41 | 1.62 | always | 5 | 2300 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted+eager` | second | counted | 17 | 3.277 | 0.105 | 0.032 | 0.193 | 12.41 | 1.62 | always | 0 | 2300 | 4403580 | 0 | yes |
| hub-16384 | triangles | `neo4j-graph` |  |  | - | 1.229 | 0.025 | 0.020 | - | 4.41 | - |  | 52 | 886 | - | 0 | yes |
| hub-16384 | triangles | `grust` | first | counted | - | 8.924 | 0.036 | 0.004 | - | 19.76 | - | needed | 1029 | 2299 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust` | second | counted | - | 6.189 | 0.033 | 0.005 | - | 19.76 | - | needed | 2 | 2299 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted` | first | counted | - | 7.033 | 0.036 | 0.005 | - | 10.72 | - | needed | 257 | 1534 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted` | second | counted | - | 7.051 | 0.024 | 0.003 | - | 10.72 | - | needed | 512 | 1534 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@work-uncounted` | first | work-uncounted | - | 6.891 | 0.038 | 0.006 | - | 9.13 | - | needed | 257 | 1535 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@work-uncounted` | second | work-uncounted | - | 6.900 | 0.016 | 0.002 | - | 9.13 | - | needed | 512 | 1535 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@unchecked` | first | unchecked | - | 6.742 | 0.013 | 0.002 | - | 8.91 | - | needed | 257 | 1025 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@unchecked` | second | unchecked | - | 6.811 | 0.023 | 0.003 | - | 8.91 | - | needed | 512 | 1025 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@counted+eager` | first | counted | - | 7.015 | 0.018 | 0.003 | - | 11.33 | 0.00 | always | 257 | 1536 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted+eager` | second | counted | - | 7.053 | 0.018 | 0.003 | - | 11.33 | 0.00 | always | 511 | 1536 | 3742208 | 0 | yes |
| hub-16384 | wcc | `neo4j-graph` |  |  | - | 1.121 | 0.031 | 0.027 | - | 4.27 | - |  | 0 | 861 | - | 0 | yes |
| hub-16384 | wcc | `icebug` |  |  | - | 1.911 | 0.017 | 0.009 | - | 9.32 | - |  | 69 | 1018 | - | 0 | yes |
| hub-16384 | wcc | `icecat` |  |  | - | 0.896 | 0.003 | 0.004 | - | 5.72 | - |  | 65 | 1556 | - | 0 | yes |
| hub-16384 | wcc | `grustcat` |  |  | - | 0.600 | 0.001 | 0.001 | - | 78.58 | - |  | 0 | 10314 | - | 0 | yes |
| hub-16384 | wcc | `grust` | first | counted | - | 1.198 | 0.041 | 0.034 | - | 17.93 | - | needed | 141 | 2298 | 1031202 | 0 | yes |
| hub-16384 | wcc | `grust` | second | counted | - | 0.589 | 0.024 | 0.040 | - | 17.93 | - | needed | 36 | 2298 | 1031202 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted` | first | counted | - | 0.486 | 0.005 | 0.011 | - | 10.76 | - | needed | 4 | 1534 | 1031211 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted` | second | counted | - | 0.447 | 0.012 | 0.027 | - | 10.76 | - | needed | 3 | 1534 | 1031211 | 0 | yes |
| hub-16384 | wcc | `grust-next@work-uncounted` | first | work-uncounted | - | 0.387 | 0.029 | 0.074 | - | 9.00 | - | needed | 2 | 2044 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@work-uncounted` | second | work-uncounted | - | 0.393 | 0.043 | 0.110 | - | 9.00 | - | needed | 1 | 2044 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@unchecked` | first | unchecked | - | 0.452 | 0.037 | 0.083 | - | 8.27 | - | needed | 3 | 2042 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@unchecked` | second | unchecked | - | 0.383 | 0.028 | 0.074 | - | 8.27 | - | needed | 1 | 2042 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@counted+eager` | first | counted | - | 0.450 | 0.008 | 0.019 | - | 12.34 | 1.61 | always | 2 | 2300 | 1473152 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted+eager` | second | counted | - | 0.474 | 0.026 | 0.056 | - | 12.34 | 1.61 | always | 2 | 2300 | 1473152 | 0 | yes |
| hub-65536 | bfs | `icebug` |  |  | - | 8.408 | 0.052 | 0.006 | - | 43.34 | - |  | 216 | 4057 | - | 0 | yes |
| hub-65536 | bfs | `icecat` |  |  | - | 3.791 | 0.030 | 0.008 | - | 18.87 | - |  | 109 | 2445 | - | 0 | yes |
| hub-65536 | bfs | `grustcat` |  |  | - | 3.982 | 0.076 | 0.019 | - | 359.53 | - |  | 0 | 38230 | - | 0 | yes |
| hub-65536 | bfs | `grust` | first | counted | - | 4.065 | 0.085 | 0.021 | - | 70.37 | - | needed | 390 | 3612 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust` | second | counted | - | 3.243 | 0.052 | 0.016 | - | 70.37 | - | needed | 176 | 3612 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted` | first | counted | - | 3.172 | 0.013 | 0.004 | - | 37.75 | - | needed | 131 | 3790 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted` | second | counted | - | 3.026 | 0.034 | 0.011 | - | 37.75 | - | needed | 77 | 3790 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust-next@work-uncounted` | first | work-uncounted | - | 3.004 | 0.022 | 0.007 | - | 30.18 | - | needed | 118 | 3281 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@work-uncounted` | second | work-uncounted | - | 2.817 | 0.034 | 0.012 | - | 30.18 | - | needed | 94 | 3281 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@unchecked` | first | unchecked | - | 3.099 | 0.026 | 0.008 | - | 29.29 | - | needed | 119 | 3283 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@unchecked` | second | unchecked | - | 2.837 | 0.043 | 0.015 | - | 29.29 | - | needed | 93 | 3283 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@counted+eager` | first | counted | - | 3.009 | 0.024 | 0.008 | - | 41.67 | 5.07 | always | 119 | 3789 | 5959069 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted+eager` | second | counted | - | 2.906 | 0.007 | 0.003 | - | 41.67 | 5.07 | always | 88 | 3789 | 5959069 | 0 | yes |
| hub-65536 | pagerank | `neo4j-graph` |  |  | 32 | 15.033 | 0.043 | 0.003 | 0.470 | 13.79 | - |  | 94 | 2378 | - | 0 | yes |
| hub-65536 | pagerank | `icebug` |  |  | 12 | 7.453 | 0.040 | 0.005 | 0.621 | 44.35 | - |  | 502 | 4057 | - | 0 | yes |
| hub-65536 | pagerank | `icecat` |  |  | 17 | 34.074 | 0.066 | 0.002 | 2.004 | 18.92 | - |  | 608 | 2498 | - | 0 | yes |
| hub-65536 | pagerank | `grustcat` |  |  | 17 | 30.276 | 0.219 | 0.007 | 1.781 | 362.37 | - |  | 0 | 39253 | - | 0 | yes |
| hub-65536 | pagerank | `grust` | first | counted | 17 | 17.785 | 0.260 | 0.015 | 1.046 | 70.31 | - | needed | 1133 | 3102 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust` | second | counted | 17 | 8.708 | 0.144 | 0.017 | 0.512 | 70.31 | - | needed | 3 | 3102 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted` | first | counted | 17 | 7.218 | 0.039 | 0.005 | 0.425 | 41.72 | 5.14 | needed | 13 | 3795 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted` | second | counted | 17 | 7.102 | 0.057 | 0.008 | 0.418 | 41.72 | 5.14 | needed | 5 | 3795 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 17 | 4.701 | 0.010 | 0.002 | 0.277 | 34.04 | 4.41 | needed | 15 | 3791 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 17 | 4.633 | 0.076 | 0.016 | 0.273 | 34.04 | 4.41 | needed | 3 | 3791 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@unchecked` | first | unchecked | 17 | 4.693 | 0.017 | 0.004 | 0.276 | 34.29 | 4.36 | needed | 11 | 3792 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@unchecked` | second | unchecked | 17 | 4.629 | 0.125 | 0.027 | 0.272 | 34.29 | 4.36 | needed | 4 | 3792 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted+eager` | first | counted | 17 | 7.102 | 0.070 | 0.010 | 0.418 | 41.58 | 5.06 | always | 13 | 3792 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted+eager` | second | counted | 17 | 6.693 | 0.120 | 0.018 | 0.394 | 41.58 | 5.06 | always | 3 | 3792 | 17616940 | 0 | yes |
| hub-65536 | triangles | `neo4j-graph` |  |  | - | 3.502 | 0.049 | 0.014 | - | 13.74 | - |  | 52 | 2379 | - | 0 | yes |
| hub-65536 | triangles | `grust` | first | counted | - | 31.157 | 0.110 | 0.004 | - | 86.98 | - | needed | 1768 | 3614 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust` | second | counted | - | 25.056 | 0.042 | 0.002 | - | 86.98 | - | needed | 1 | 3614 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted` | first | counted | - | 28.783 | 0.093 | 0.003 | - | 41.52 | - | needed | 1026 | 3282 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted` | second | counted | - | 26.365 | 0.152 | 0.006 | - | 41.52 | - | needed | 1025 | 3282 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@work-uncounted` | first | work-uncounted | - | 28.140 | 0.677 | 0.024 | - | 34.85 | - | needed | 1026 | 3282 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@work-uncounted` | second | work-uncounted | - | 26.061 | 0.202 | 0.008 | - | 34.85 | - | needed | 1025 | 3282 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@unchecked` | first | unchecked | - | 27.392 | 0.300 | 0.011 | - | 33.87 | - | needed | 1026 | 3281 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@unchecked` | second | unchecked | - | 25.595 | 0.100 | 0.004 | - | 33.87 | - | needed | 1025 | 3281 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@counted+eager` | first | counted | - | 28.447 | 0.031 | 0.001 | - | 41.18 | 0.00 | always | 1026 | 3285 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted+eager` | second | counted | - | 26.536 | 0.166 | 0.006 | - | 41.18 | 0.00 | always | 1024 | 3285 | 14971727 | 0 | yes |
| hub-65536 | wcc | `neo4j-graph` |  |  | - | 3.177 | 0.054 | 0.017 | - | 13.75 | - |  | 226 | 2365 | - | 0 | yes |
| hub-65536 | wcc | `icebug` |  |  | - | 11.207 | 0.085 | 0.008 | - | 43.10 | - |  | 239 | 4057 | - | 0 | yes |
| hub-65536 | wcc | `icecat` |  |  | - | 3.715 | 0.024 | 0.006 | - | 19.09 | - |  | 256 | 2680 | - | 0 | yes |
| hub-65536 | wcc | `grustcat` |  |  | - | 2.457 | 0.011 | 0.004 | - | 361.59 | - |  | 0 | 39763 | - | 0 | yes |
| hub-65536 | wcc | `grust` | first | counted | - | 2.385 | 0.031 | 0.013 | - | 71.54 | - | needed | 239 | 3612 | 4125504 | 0 | yes |
| hub-65536 | wcc | `grust` | second | counted | - | 1.624 | 0.025 | 0.015 | - | 71.54 | - | needed | 132 | 3612 | 4125504 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted` | first | counted | - | 1.477 | 0.049 | 0.033 | - | 36.78 | - | needed | 6 | 3280 | 4125495 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted` | second | counted | - | 1.498 | 0.040 | 0.027 | - | 36.78 | - | needed | 2 | 3280 | 4125495 | 0 | yes |
| hub-65536 | wcc | `grust-next@work-uncounted` | first | work-uncounted | - | 1.240 | 0.016 | 0.013 | - | 29.81 | - | needed | 3 | 3280 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@work-uncounted` | second | work-uncounted | - | 1.261 | 0.035 | 0.028 | - | 29.81 | - | needed | 2 | 3280 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@unchecked` | first | unchecked | - | 1.296 | 0.089 | 0.069 | - | 30.21 | - | needed | 6 | 3283 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@unchecked` | second | unchecked | - | 1.301 | 0.126 | 0.097 | - | 30.21 | - | needed | 2 | 3283 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@counted+eager` | first | counted | - | 1.500 | 0.050 | 0.033 | - | 42.13 | 5.05 | always | 3 | 3789 | 5893557 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted+eager` | second | counted | - | 1.496 | 0.048 | 0.032 | - | 42.13 | 5.05 | always | 2 | 3789 | 5893557 | 0 | yes |
| layered-16384 | bfs | `icebug` |  |  | - | 0.499 | 0.006 | 0.013 | - | 2.80 | - |  | 37 | 458 | - | 0 | yes |
| layered-16384 | bfs | `icecat` |  |  | - | 0.386 | 0.002 | 0.005 | - | 1.55 | - |  | 66 | 526 | - | 0 | yes |
| layered-16384 | bfs | `grustcat` |  |  | - | 0.259 | 0.002 | 0.009 | - | 30.55 | - |  | 1 | 7350 | - | 0 | yes |
| layered-16384 | bfs | `grust` | first | counted | - | 0.455 | 0.001 | 0.003 | - | 6.85 | - | needed | 30 | 1031 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust` | second | counted | - | 0.386 | 0.000 | 0.001 | - | 6.85 | - | needed | 0 | 1031 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted` | first | counted | - | 0.456 | 0.002 | 0.005 | - | 6.00 | - | needed | 26 | 1014 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted` | second | counted | - | 0.381 | 0.000 | 0.001 | - | 6.00 | - | needed | 0 | 1014 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@work-uncounted` | first | work-uncounted | - | 0.370 | 0.004 | 0.012 | - | 5.27 | - | needed | 26 | 1013 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@work-uncounted` | second | work-uncounted | - | 0.290 | 0.001 | 0.003 | - | 5.27 | - | needed | 0 | 1013 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@unchecked` | first | unchecked | - | 0.326 | 0.006 | 0.018 | - | 5.20 | - | needed | 26 | 1012 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@unchecked` | second | unchecked | - | 0.254 | 0.003 | 0.011 | - | 5.20 | - | needed | 0 | 1012 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@counted+eager` | first | counted | - | 0.452 | 0.003 | 0.007 | - | 7.03 | 0.81 | always | 26 | 1111 | 493703 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted+eager` | second | counted | - | 0.381 | 0.001 | 0.003 | - | 7.03 | 0.81 | always | 0 | 1111 | 493703 | 0 | yes |
| layered-16384 | pagerank | `icebug` |  |  | 69 | 8.888 | 0.164 | 0.018 | 0.129 | 2.79 | - |  | 201 | 458 | - | 0 | yes |
| layered-16384 | pagerank | `icecat` |  |  | 84 | 27.710 | 0.031 | 0.001 | 0.330 | 1.68 | - |  | 128 | 525 | - | 0 | yes |
| layered-16384 | pagerank | `grustcat` |  |  | 84 | 26.383 | 0.055 | 0.002 | 0.314 | 31.04 | - |  | 0 | 7350 | - | 0 | yes |
| layered-16384 | pagerank | `grust` | first | counted | 84 | 15.125 | 0.141 | 0.009 | 0.180 | 6.49 | - | needed | 293 | 1031 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust` | second | counted | 84 | 13.369 | 0.178 | 0.013 | 0.159 | 6.49 | - | needed | 0 | 1031 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted` | first | counted | 84 | 14.719 | 0.150 | 0.010 | 0.175 | 6.69 | 0.80 | needed | 103 | 1110 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted` | second | counted | 84 | 14.138 | 0.192 | 0.014 | 0.168 | 6.69 | 0.80 | needed | 0 | 1110 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 84 | 12.333 | 0.108 | 0.009 | 0.147 | 5.94 | 0.65 | needed | 106 | 1106 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 84 | 12.099 | 0.107 | 0.009 | 0.144 | 5.94 | 0.65 | needed | 0 | 1106 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@unchecked` | first | unchecked | 84 | 12.406 | 0.135 | 0.011 | 0.148 | 5.85 | 0.60 | needed | 103 | 1110 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@unchecked` | second | unchecked | 84 | 12.021 | 0.112 | 0.009 | 0.143 | 5.85 | 0.60 | needed | 0 | 1110 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted+eager` | first | counted | 84 | 14.346 | 0.113 | 0.008 | 0.171 | 6.64 | 0.80 | always | 104 | 1111 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted+eager` | second | counted | 84 | 14.242 | 0.227 | 0.016 | 0.170 | 6.64 | 0.80 | always | 0 | 1111 | 7307112 | 0 | yes |
| layered-16384 | triangles | `neo4j-graph` |  |  | - | 0.709 | 0.031 | 0.044 | - | 2.12 | - |  | 31 | 539 | - | 0 | yes |
| layered-16384 | triangles | `grust` | first | counted | - | 3.052 | 0.025 | 0.008 | - | 7.25 | - | needed | 452 | 1158 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust` | second | counted | - | 1.656 | 0.005 | 0.003 | - | 7.25 | - | needed | 1 | 1158 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted` | first | counted | - | 2.429 | 0.022 | 0.009 | - | 6.49 | - | needed | 351 | 1141 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted` | second | counted | - | 2.138 | 0.034 | 0.016 | - | 6.49 | - | needed | 318 | 1141 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@work-uncounted` | first | work-uncounted | - | 2.228 | 0.019 | 0.009 | - | 5.74 | - | needed | 351 | 1139 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@work-uncounted` | second | work-uncounted | - | 1.967 | 0.015 | 0.008 | - | 5.74 | - | needed | 318 | 1139 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@unchecked` | first | unchecked | - | 2.195 | 0.033 | 0.015 | - | 5.55 | - | needed | 350 | 1141 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@unchecked` | second | unchecked | - | 1.873 | 0.009 | 0.005 | - | 5.55 | - | needed | 318 | 1141 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@counted+eager` | first | counted | - | 2.403 | 0.030 | 0.013 | - | 6.49 | 0.00 | always | 351 | 1140 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted+eager` | second | counted | - | 2.076 | 0.007 | 0.003 | - | 6.49 | 0.00 | always | 319 | 1140 | 718265 | 0 | yes |
| layered-16384 | wcc | `neo4j-graph` |  |  | - | 1.086 | 0.016 | 0.014 | - | 2.20 | - |  | 1 | 539 | - | 0 | yes |
| layered-16384 | wcc | `icebug` |  |  | - | 0.941 | 0.024 | 0.025 | - | 2.76 | - |  | 42 | 458 | - | 0 | yes |
| layered-16384 | wcc | `icecat` |  |  | - | 0.503 | 0.009 | 0.017 | - | 1.69 | - |  | 64 | 526 | - | 0 | yes |
| layered-16384 | wcc | `grustcat` |  |  | - | 0.351 | 0.001 | 0.004 | - | 30.21 | - |  | 0 | 6840 | - | 0 | yes |
| layered-16384 | wcc | `grust` | first | counted | - | 0.982 | 0.023 | 0.023 | - | 6.77 | - | needed | 140 | 1031 | 341582 | 0 | yes |
| layered-16384 | wcc | `grust` | second | counted | - | 0.329 | 0.003 | 0.010 | - | 6.77 | - | needed | 32 | 1031 | 341582 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted` | first | counted | - | 0.380 | 0.024 | 0.062 | - | 6.05 | - | needed | 35 | 1014 | 341586 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted` | second | counted | - | 0.336 | 0.014 | 0.042 | - | 6.05 | - | needed | 30 | 1014 | 341586 | 0 | yes |
| layered-16384 | wcc | `grust-next@work-uncounted` | first | work-uncounted | - | 0.292 | 0.012 | 0.042 | - | 5.11 | - | needed | 35 | 1012 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@work-uncounted` | second | work-uncounted | - | 0.299 | 0.008 | 0.028 | - | 5.11 | - | needed | 28 | 1012 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@unchecked` | first | unchecked | - | 0.313 | 0.026 | 0.083 | - | 5.21 | - | needed | 35 | 1013 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@unchecked` | second | unchecked | - | 0.291 | 0.002 | 0.007 | - | 5.21 | - | needed | 30 | 1013 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@counted+eager` | first | counted | - | 0.312 | 0.003 | 0.010 | - | 6.95 | 0.79 | always | 34 | 1108 | 487976 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted+eager` | second | counted | - | 0.351 | 0.006 | 0.018 | - | 6.95 | 0.79 | always | 30 | 1108 | 487976 | 0 | yes |
| layered-65536 | bfs | `icebug` |  |  | - | 2.037 | 0.023 | 0.011 | - | 11.15 | - |  | 132 | 1832 | - | 0 | yes |
| layered-65536 | bfs | `icecat` |  |  | - | 1.567 | 0.004 | 0.003 | - | 6.31 | - |  | 257 | 1636 | - | 0 | yes |
| layered-65536 | bfs | `grustcat` |  |  | - | 1.010 | 0.003 | 0.003 | - | 128.57 | - |  | 0 | 26634 | - | 0 | yes |
| layered-65536 | bfs | `grust` | first | counted | - | 1.836 | 0.008 | 0.005 | - | 28.54 | - | needed | 119 | 3142 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust` | second | counted | - | 1.579 | 0.008 | 0.005 | - | 28.54 | - | needed | 0 | 3142 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted` | first | counted | - | 1.848 | 0.032 | 0.017 | - | 21.08 | - | needed | 103 | 2743 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted` | second | counted | - | 1.553 | 0.001 | 0.001 | - | 21.08 | - | needed | 0 | 2743 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@work-uncounted` | first | work-uncounted | - | 1.452 | 0.002 | 0.001 | - | 17.82 | - | needed | 103 | 2742 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@work-uncounted` | second | work-uncounted | - | 1.192 | 0.009 | 0.008 | - | 17.82 | - | needed | 0 | 2742 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@unchecked` | first | unchecked | - | 1.293 | 0.002 | 0.002 | - | 17.29 | - | needed | 103 | 2743 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@unchecked` | second | unchecked | - | 1.026 | 0.001 | 0.001 | - | 17.29 | - | needed | 0 | 2743 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@counted+eager` | first | counted | - | 1.837 | 0.037 | 0.020 | - | 23.49 | 2.50 | always | 102 | 3127 | 1979713 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted+eager` | second | counted | - | 1.549 | 0.001 | 0.001 | - | 23.49 | 2.50 | always | 0 | 3127 | 1979713 | 0 | yes |
| layered-65536 | pagerank | `icebug` |  |  | 60 | 13.843 | 0.144 | 0.010 | 0.231 | 11.19 | - |  | 489 | 1832 | - | 0 | yes |
| layered-65536 | pagerank | `icecat` |  |  | 75 | 101.568 | 0.066 | 0.001 | 1.354 | 6.24 | - |  | 608 | 1636 | - | 0 | yes |
| layered-65536 | pagerank | `grustcat` |  |  | 75 | 94.166 | 0.090 | 0.001 | 1.256 | 129.04 | - |  | 1 | 26636 | - | 0 | yes |
| layered-65536 | pagerank | `grust` | first | counted | 75 | 25.492 | 0.106 | 0.004 | 0.340 | 28.36 | - | needed | 883 | 3142 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust` | second | counted | 75 | 21.094 | 0.087 | 0.004 | 0.281 | 28.36 | - | needed | 3 | 3142 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted` | first | counted | 75 | 21.107 | 0.150 | 0.007 | 0.281 | 23.79 | 2.52 | needed | 407 | 3128 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted` | second | counted | 75 | 20.071 | 0.208 | 0.010 | 0.268 | 23.79 | 2.52 | needed | 3 | 3128 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 75 | 15.837 | 0.075 | 0.005 | 0.211 | 19.44 | 1.87 | needed | 404 | 3124 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 75 | 14.862 | 0.126 | 0.008 | 0.198 | 19.44 | 1.87 | needed | 2 | 3124 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@unchecked` | first | unchecked | 75 | 15.592 | 0.029 | 0.002 | 0.208 | 18.30 | 1.80 | needed | 406 | 3125 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@unchecked` | second | unchecked | 75 | 14.605 | 0.148 | 0.010 | 0.195 | 18.30 | 1.80 | needed | 2 | 3125 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted+eager` | first | counted | 75 | 20.688 | 0.055 | 0.003 | 0.276 | 23.65 | 2.56 | always | 406 | 3128 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted+eager` | second | counted | 75 | 19.638 | 0.015 | 0.001 | 0.262 | 23.65 | 2.56 | always | 2 | 3128 | 26313822 | 0 | yes |
| layered-65536 | triangles | `neo4j-graph` |  |  | - | 1.058 | 0.021 | 0.020 | - | 5.06 | - |  | 49 | 1805 | - | 0 | yes |
| layered-65536 | triangles | `grust` | first | counted | - | 9.878 | 0.033 | 0.003 | - | 28.75 | - | needed | 1503 | 3649 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust` | second | counted | - | 6.411 | 0.016 | 0.002 | - | 28.75 | - | needed | 2 | 3649 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted` | first | counted | - | 9.210 | 0.032 | 0.003 | - | 22.52 | - | needed | 1401 | 3252 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted` | second | counted | - | 7.068 | 0.077 | 0.011 | - | 22.52 | - | needed | 508 | 3252 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@work-uncounted` | first | work-uncounted | - | 8.633 | 0.025 | 0.003 | - | 19.50 | - | needed | 1402 | 3254 | - | 0 | yes |
| layered-65536 | triangles | `grust-next@work-uncounted` | second | work-uncounted | - | 6.341 | 0.008 | 0.001 | - | 19.50 | - | needed | 508 | 3254 | - | 0 | yes |
| layered-65536 | triangles | `grust-next@unchecked` | first | unchecked | - | 8.323 | 0.030 | 0.004 | - | 18.93 | - | needed | 1402 | 3253 | - | 0 | yes |
| layered-65536 | triangles | `grust-next@unchecked` | second | unchecked | - | 6.062 | 0.001 | 0.000 | - | 18.93 | - | needed | 508 | 3253 | - | 0 | yes |
| layered-65536 | triangles | `grust-next@counted+eager` | first | counted | - | 9.167 | 0.040 | 0.004 | - | 22.73 | 0.00 | always | 1401 | 3253 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted+eager` | second | counted | - | 6.938 | 0.036 | 0.005 | - | 22.73 | 0.00 | always | 508 | 3253 | 2877576 | 0 | yes |
| layered-65536 | wcc | `neo4j-graph` |  |  | - | 2.673 | 0.266 | 0.099 | - | 5.08 | - |  | 258 | 1807 | - | 0 | yes |
| layered-65536 | wcc | `icebug` |  |  | - | 3.768 | 0.013 | 0.003 | - | 11.07 | - |  | 137 | 1832 | - | 0 | yes |
| layered-65536 | wcc | `icecat` |  |  | - | 1.988 | 0.013 | 0.006 | - | 6.28 | - |  | 255 | 1636 | - | 0 | yes |
| layered-65536 | wcc | `grustcat` |  |  | - | 1.430 | 0.017 | 0.012 | - | 128.15 | - |  | 1 | 26635 | - | 0 | yes |
| layered-65536 | wcc | `grust` | first | counted | - | 1.505 | 0.010 | 0.007 | - | 27.89 | - | needed | 239 | 3143 | 1368146 | 0 | yes |
| layered-65536 | wcc | `grust` | second | counted | - | 0.836 | 0.010 | 0.012 | - | 27.89 | - | needed | 129 | 3143 | 1368146 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted` | first | counted | - | 0.892 | 0.013 | 0.014 | - | 21.00 | - | needed | 133 | 2745 | 1368150 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted` | second | counted | - | 0.842 | 0.024 | 0.029 | - | 21.00 | - | needed | 125 | 2745 | 1368150 | 0 | yes |
| layered-65536 | wcc | `grust-next@work-uncounted` | first | work-uncounted | - | 0.787 | 0.050 | 0.064 | - | 17.59 | - | needed | 134 | 2742 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@work-uncounted` | second | work-uncounted | - | 0.711 | 0.006 | 0.008 | - | 17.59 | - | needed | 125 | 2742 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@unchecked` | first | unchecked | - | 0.725 | 0.019 | 0.026 | - | 16.68 | - | needed | 134 | 2237 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@unchecked` | second | unchecked | - | 0.684 | 0.009 | 0.014 | - | 16.68 | - | needed | 123 | 2237 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@counted+eager` | first | counted | - | 0.862 | 0.011 | 0.013 | - | 23.72 | 2.55 | always | 132 | 3127 | 1954504 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted+eager` | second | counted | - | 0.830 | 0.010 | 0.012 | - | 23.72 | 2.55 | always | 124 | 3127 | 1954504 | 0 | yes |
| path-16384 | bfs | `icebug` |  |  | - | 0.250 | 0.011 | 0.045 | - | 1.76 | - |  | 36 | 450 | - | 0 | yes |
| path-16384 | bfs | `icecat` |  |  | - | 0.282 | 0.001 | 0.004 | - | 0.91 | - |  | 64 | 275 | - | 0 | yes |
| path-16384 | bfs | `grustcat` |  |  | - | 0.142 | 0.000 | 0.002 | - | 24.46 | - |  | 0 | 6429 | - | 0 | yes |
| path-16384 | bfs | `grust` | first | counted | - | 0.418 | 0.004 | 0.009 | - | 5.09 | - | needed | 36 | 741 | 245755 | 0 | yes |
| path-16384 | bfs | `grust` | second | counted | - | 0.341 | 0.001 | 0.004 | - | 5.09 | - | needed | 0 | 741 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@counted` | first | counted | - | 0.408 | 0.002 | 0.005 | - | 5.09 | - | needed | 32 | 791 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@counted` | second | counted | - | 0.326 | 0.000 | 0.001 | - | 5.09 | - | needed | 0 | 791 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@work-uncounted` | first | work-uncounted | - | 0.248 | 0.008 | 0.031 | - | 4.63 | - | needed | 32 | 790 | - | 0 | yes |
| path-16384 | bfs | `grust-next@work-uncounted` | second | work-uncounted | - | 0.152 | 0.001 | 0.003 | - | 4.63 | - | needed | 0 | 790 | - | 0 | yes |
| path-16384 | bfs | `grust-next@unchecked` | first | unchecked | - | 0.197 | 0.002 | 0.011 | - | 4.41 | - | needed | 32 | 790 | - | 0 | yes |
| path-16384 | bfs | `grust-next@unchecked` | second | unchecked | - | 0.117 | 0.001 | 0.006 | - | 4.41 | - | needed | 0 | 790 | - | 0 | yes |
| path-16384 | bfs | `grust-next@counted+eager` | first | counted | - | 0.402 | 0.007 | 0.018 | - | 5.92 | 0.65 | always | 32 | 855 | 344057 | 0 | yes |
| path-16384 | bfs | `grust-next@counted+eager` | second | counted | - | 0.326 | 0.000 | 0.000 | - | 5.92 | 0.65 | always | 0 | 855 | 344057 | 0 | yes |
| path-16384 | pagerank | `icebug` |  |  | 54 | 6.683 | 0.137 | 0.020 | 0.124 | 1.73 | - |  | 200 | 450 | - | 0 | yes |
| path-16384 | pagerank | `icecat` |  |  | 58 | 11.174 | 0.005 | 0.000 | 0.193 | 0.89 | - |  | 129 | 274 | - | 0 | yes |
| path-16384 | pagerank | `grustcat` |  |  | 58 | 9.966 | 0.165 | 0.017 | 0.172 | 24.26 | - |  | 0 | 6429 | - | 0 | yes |
| path-16384 | pagerank | `grust` | first | counted | 58 | 10.443 | 0.168 | 0.016 | 0.180 | 5.14 | - | needed | 262 | 741 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust` | second | counted | 58 | 8.653 | 0.124 | 0.014 | 0.149 | 5.14 | - | needed | 0 | 741 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted` | first | counted | 58 | 15.446 | 0.689 | 0.045 | 0.266 | 5.92 | 0.64 | needed | 108 | 856 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted` | second | counted | 58 | 16.143 | 0.363 | 0.022 | 0.278 | 5.92 | 0.64 | needed | 64 | 856 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 58 | 8.403 | 0.095 | 0.011 | 0.145 | 5.10 | 0.47 | needed | 108 | 855 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 58 | 8.025 | 0.158 | 0.020 | 0.138 | 5.10 | 0.47 | needed | 65 | 855 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@unchecked` | first | unchecked | 58 | 8.259 | 0.037 | 0.005 | 0.142 | 4.82 | 0.46 | needed | 108 | 856 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@unchecked` | second | unchecked | 58 | 7.999 | 0.168 | 0.021 | 0.138 | 4.82 | 0.46 | needed | 65 | 856 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@counted+eager` | first | counted | 58 | 16.525 | 0.257 | 0.016 | 0.285 | 5.78 | 0.65 | always | 108 | 855 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted+eager` | second | counted | 58 | 15.896 | 0.418 | 0.026 | 0.274 | 5.78 | 0.65 | always | 64 | 855 | 4112319 | 0 | yes |
| path-16384 | triangles | `neo4j-graph` |  |  | - | 0.527 | 0.026 | 0.049 | - | 2.03 | - |  | 18 | 435 | - | 0 | yes |
| path-16384 | triangles | `grust` | first | counted | - | 2.100 | 0.021 | 0.010 | - | 5.28 | - | needed | 359 | 805 | 425970 | 0 | yes |
| path-16384 | triangles | `grust` | second | counted | - | 0.940 | 0.007 | 0.008 | - | 5.28 | - | needed | 1 | 805 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted` | first | counted | - | 1.550 | 0.051 | 0.033 | - | 5.31 | - | needed | 256 | 854 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted` | second | counted | - | 1.445 | 0.010 | 0.007 | - | 5.31 | - | needed | 256 | 854 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@work-uncounted` | first | work-uncounted | - | 1.366 | 0.031 | 0.023 | - | 4.64 | - | needed | 257 | 854 | - | 0 | yes |
| path-16384 | triangles | `grust-next@work-uncounted` | second | work-uncounted | - | 1.162 | 0.011 | 0.009 | - | 4.64 | - | needed | 256 | 854 | - | 0 | yes |
| path-16384 | triangles | `grust-next@unchecked` | first | unchecked | - | 1.290 | 0.029 | 0.022 | - | 4.76 | - | needed | 256 | 854 | - | 0 | yes |
| path-16384 | triangles | `grust-next@unchecked` | second | unchecked | - | 1.142 | 0.029 | 0.025 | - | 4.76 | - | needed | 256 | 854 | - | 0 | yes |
| path-16384 | triangles | `grust-next@counted+eager` | first | counted | - | 1.556 | 0.024 | 0.015 | - | 5.48 | 0.00 | always | 256 | 854 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted+eager` | second | counted | - | 1.438 | 0.024 | 0.017 | - | 5.48 | 0.00 | always | 256 | 854 | 425970 | 0 | yes |
| path-16384 | wcc | `neo4j-graph` |  |  | - | 0.827 | 0.009 | 0.011 | - | 2.05 | - |  | 45 | 438 | - | 0 | yes |
| path-16384 | wcc | `icebug` |  |  | - | 0.341 | 0.004 | 0.012 | - | 1.77 | - |  | 41 | 450 | - | 0 | yes |
| path-16384 | wcc | `icecat` |  |  | - | 0.275 | 0.003 | 0.010 | - | 0.93 | - |  | 65 | 275 | - | 0 | yes |
| path-16384 | wcc | `grustcat` |  |  | - | 0.158 | 0.001 | 0.004 | - | 24.18 | - |  | 0 | 6429 | - | 0 | yes |
| path-16384 | wcc | `grust` | first | counted | - | 0.931 | 0.069 | 0.074 | - | 5.07 | - | needed | 137 | 741 | 229369 | 0 | yes |
| path-16384 | wcc | `grust` | second | counted | - | 0.293 | 0.009 | 0.032 | - | 5.07 | - | needed | 33 | 741 | 229369 | 0 | yes |
| path-16384 | wcc | `grust-next@counted` | first | counted | - | 0.471 | 0.018 | 0.038 | - | 5.28 | - | needed | 35 | 791 | 229369 | 0 | yes |
| path-16384 | wcc | `grust-next@counted` | second | counted | - | 0.410 | 0.033 | 0.081 | - | 5.28 | - | needed | 17 | 791 | 229369 | 0 | yes |
| path-16384 | wcc | `grust-next@work-uncounted` | first | work-uncounted | - | 0.258 | 0.005 | 0.018 | - | 4.58 | - | needed | 34 | 789 | - | 0 | yes |
| path-16384 | wcc | `grust-next@work-uncounted` | second | work-uncounted | - | 0.156 | 0.006 | 0.039 | - | 4.58 | - | needed | 2 | 789 | - | 0 | yes |
| path-16384 | wcc | `grust-next@unchecked` | first | unchecked | - | 0.259 | 0.004 | 0.015 | - | 4.35 | - | needed | 34 | 790 | - | 0 | yes |
| path-16384 | wcc | `grust-next@unchecked` | second | unchecked | - | 0.148 | 0.006 | 0.041 | - | 4.35 | - | needed | 2 | 790 | - | 0 | yes |
| path-16384 | wcc | `grust-next@counted+eager` | first | counted | - | 0.410 | 0.019 | 0.046 | - | 5.81 | 0.64 | always | 35 | 855 | 327671 | 0 | yes |
| path-16384 | wcc | `grust-next@counted+eager` | second | counted | - | 0.399 | 0.073 | 0.184 | - | 5.81 | 0.64 | always | 33 | 855 | 327671 | 0 | yes |
| path-65536 | bfs | `icebug` |  |  | - | 0.931 | 0.012 | 0.013 | - | 7.03 | - |  | 132 | 1795 | - | 0 | yes |
| path-65536 | bfs | `icecat` |  |  | - | 1.125 | 0.006 | 0.005 | - | 4.32 | - |  | 257 | 1139 | - | 0 | yes |
| path-65536 | bfs | `grustcat` |  |  | - | 0.563 | 0.002 | 0.003 | - | 101.77 | - |  | 0 | 24215 | - | 0 | yes |
| path-65536 | bfs | `grust` | first | counted | - | 1.688 | 0.011 | 0.006 | - | 20.80 | - | needed | 144 | 2487 | 983035 | 0 | yes |
| path-65536 | bfs | `grust` | second | counted | - | 1.359 | 0.001 | 0.000 | - | 20.80 | - | needed | 0 | 2487 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@counted` | first | counted | - | 1.629 | 0.015 | 0.009 | - | 18.21 | - | needed | 128 | 2375 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@counted` | second | counted | - | 1.305 | 0.003 | 0.002 | - | 18.21 | - | needed | 0 | 2375 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@work-uncounted` | first | work-uncounted | - | 0.900 | 0.005 | 0.006 | - | 15.29 | - | needed | 128 | 2373 | - | 0 | yes |
| path-65536 | bfs | `grust-next@work-uncounted` | second | work-uncounted | - | 0.602 | 0.001 | 0.002 | - | 15.29 | - | needed | 0 | 2373 | - | 0 | yes |
| path-65536 | bfs | `grust-next@unchecked` | first | unchecked | - | 0.765 | 0.003 | 0.004 | - | 15.58 | - | needed | 128 | 2376 | - | 0 | yes |
| path-65536 | bfs | `grust-next@unchecked` | second | unchecked | - | 0.465 | 0.001 | 0.002 | - | 15.58 | - | needed | 0 | 2376 | - | 0 | yes |
| path-65536 | bfs | `grust-next@counted+eager` | first | counted | - | 1.625 | 0.017 | 0.011 | - | 20.13 | 2.01 | always | 128 | 2633 | 1376249 | 0 | yes |
| path-65536 | bfs | `grust-next@counted+eager` | second | counted | - | 1.312 | 0.009 | 0.007 | - | 20.13 | 2.01 | always | 0 | 2633 | 1376249 | 0 | yes |
| path-65536 | pagerank | `icebug` |  |  | 46 | 10.428 | 0.035 | 0.003 | 0.227 | 7.11 | - |  | 489 | 1795 | - | 0 | yes |
| path-65536 | pagerank | `icecat` |  |  | 50 | 39.114 | 0.085 | 0.002 | 0.782 | 4.36 | - |  | 607 | 1139 | - | 0 | yes |
| path-65536 | pagerank | `grustcat` |  |  | 50 | 34.835 | 0.541 | 0.016 | 0.697 | 103.75 | - |  | 0 | 24216 | - | 0 | yes |
| path-65536 | pagerank | `grust` | first | counted | 50 | 16.311 | 0.016 | 0.001 | 0.326 | 21.16 | - | needed | 754 | 2486 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust` | second | counted | 50 | 12.244 | 0.216 | 0.018 | 0.245 | 21.16 | - | needed | 2 | 2486 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted` | first | counted | 50 | 26.272 | 2.309 | 0.088 | 0.525 | 20.53 | 2.05 | needed | 401 | 2633 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted` | second | counted | 50 | 26.616 | 0.471 | 0.018 | 0.532 | 20.53 | 2.05 | needed | 355 | 2633 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 50 | 9.273 | 0.106 | 0.011 | 0.185 | 17.08 | 1.37 | needed | 404 | 2633 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 50 | 8.732 | 0.197 | 0.023 | 0.175 | 17.08 | 1.37 | needed | 355 | 2633 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@unchecked` | first | unchecked | 50 | 9.027 | 0.123 | 0.014 | 0.181 | 16.00 | 1.26 | needed | 401 | 2637 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@unchecked` | second | unchecked | 50 | 8.379 | 0.103 | 0.012 | 0.168 | 16.00 | 1.26 | needed | 355 | 2637 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@counted+eager` | first | counted | 50 | 25.875 | 0.604 | 0.023 | 0.517 | 20.35 | 2.01 | always | 404 | 2634 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted+eager` | second | counted | 50 | 26.513 | 1.752 | 0.066 | 0.530 | 20.35 | 2.01 | always | 354 | 2634 | 14352327 | 0 | yes |
| path-65536 | triangles | `neo4j-graph` |  |  | - | 0.725 | 0.009 | 0.012 | - | 4.67 | - |  | 32 | 1409 | - | 0 | yes |
| path-65536 | triangles | `grust` | first | counted | - | 6.259 | 0.007 | 0.001 | - | 21.63 | - | needed | 1127 | 2742 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust` | second | counted | - | 3.533 | 0.028 | 0.008 | - | 21.63 | - | needed | 1 | 2742 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted` | first | counted | - | 6.060 | 0.138 | 0.023 | - | 19.30 | - | needed | 1024 | 2632 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted` | second | counted | - | 5.801 | 0.057 | 0.010 | - | 19.30 | - | needed | 1120 | 2632 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@work-uncounted` | first | work-uncounted | - | 5.075 | 0.017 | 0.003 | - | 16.64 | - | needed | 1024 | 2631 | - | 0 | yes |
| path-65536 | triangles | `grust-next@work-uncounted` | second | work-uncounted | - | 4.672 | 0.017 | 0.004 | - | 16.64 | - | needed | 1120 | 2631 | - | 0 | yes |
| path-65536 | triangles | `grust-next@unchecked` | first | unchecked | - | 4.854 | 0.014 | 0.003 | - | 16.64 | - | needed | 1024 | 2633 | - | 0 | yes |
| path-65536 | triangles | `grust-next@unchecked` | second | unchecked | - | 4.442 | 0.054 | 0.012 | - | 16.64 | - | needed | 1120 | 2633 | - | 0 | yes |
| path-65536 | triangles | `grust-next@counted+eager` | first | counted | - | 6.016 | 0.042 | 0.007 | - | 19.07 | 0.00 | always | 1024 | 2634 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted+eager` | second | counted | - | 5.689 | 0.128 | 0.023 | - | 19.07 | 0.00 | always | 1120 | 2634 | 1703922 | 0 | yes |
| path-65536 | wcc | `neo4j-graph` |  |  | - | 2.322 | 0.132 | 0.057 | - | 4.64 | - |  | 231 | 1412 | - | 0 | yes |
| path-65536 | wcc | `icebug` |  |  | - | 1.219 | 0.010 | 0.008 | - | 7.05 | - |  | 137 | 1795 | - | 0 | yes |
| path-65536 | wcc | `icecat` |  |  | - | 1.081 | 0.012 | 0.011 | - | 4.33 | - |  | 257 | 1139 | - | 0 | yes |
| path-65536 | wcc | `grustcat` |  |  | - | 0.627 | 0.004 | 0.006 | - | 102.85 | - |  | 0 | 24216 | - | 0 | yes |
| path-65536 | wcc | `grust` | first | counted | - | 1.425 | 0.011 | 0.008 | - | 20.82 | - | needed | 238 | 2486 | 917497 | 0 | yes |
| path-65536 | wcc | `grust` | second | counted | - | 0.762 | 0.001 | 0.001 | - | 20.82 | - | needed | 133 | 2486 | 917497 | 0 | yes |
| path-65536 | wcc | `grust-next@counted` | first | counted | - | 1.043 | 0.041 | 0.039 | - | 18.58 | - | needed | 133 | 2377 | 917497 | 0 | yes |
| path-65536 | wcc | `grust-next@counted` | second | counted | - | 0.814 | 0.081 | 0.100 | - | 18.58 | - | needed | 66 | 2377 | 917497 | 0 | yes |
| path-65536 | wcc | `grust-next@work-uncounted` | first | work-uncounted | - | 0.709 | 0.044 | 0.062 | - | 15.62 | - | needed | 133 | 2375 | - | 0 | yes |
| path-65536 | wcc | `grust-next@work-uncounted` | second | work-uncounted | - | 0.351 | 0.011 | 0.031 | - | 15.62 | - | needed | 2 | 2375 | - | 0 | yes |
| path-65536 | wcc | `grust-next@unchecked` | first | unchecked | - | 0.622 | 0.002 | 0.004 | - | 15.52 | - | needed | 133 | 2374 | - | 0 | yes |
| path-65536 | wcc | `grust-next@unchecked` | second | unchecked | - | 0.330 | 0.004 | 0.012 | - | 15.52 | - | needed | 2 | 2374 | - | 0 | yes |
| path-65536 | wcc | `grust-next@counted+eager` | first | counted | - | 1.228 | 0.030 | 0.024 | - | 20.23 | 2.00 | always | 133 | 2635 | 1310711 | 0 | yes |
| path-65536 | wcc | `grust-next@counted+eager` | second | counted | - | 1.211 | 0.060 | 0.050 | - | 20.23 | 2.00 | always | 132 | 2635 | 1310711 | 0 | yes |
| uniform-16384 | bfs | `icebug` |  |  | - | 1.490 | 0.021 | 0.014 | - | 8.97 | - |  | 57 | 979 | - | 0 | yes |
| uniform-16384 | bfs | `icecat` |  |  | - | 0.872 | 0.007 | 0.008 | - | 6.45 | - |  | 97 | 2067 | - | 0 | yes |
| uniform-16384 | bfs | `grustcat` |  |  | - | 0.669 | 0.011 | 0.016 | - | 79.31 | - |  | 0 | 10541 | - | 0 | yes |
| uniform-16384 | bfs | `grust` | first | counted | - | 1.560 | 0.004 | 0.003 | - | 17.56 | - | needed | 36 | 2299 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust` | second | counted | - | 1.475 | 0.003 | 0.002 | - | 17.56 | - | needed | 0 | 2299 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted` | first | counted | - | 1.707 | 0.022 | 0.013 | - | 10.83 | - | needed | 0 | 2048 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted` | second | counted | - | 1.511 | 0.033 | 0.022 | - | 10.83 | - | needed | 0 | 2048 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@work-uncounted` | first | work-uncounted | - | 1.062 | 0.004 | 0.004 | - | 8.85 | - | needed | 0 | 2042 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@work-uncounted` | second | work-uncounted | - | 0.892 | 0.008 | 0.009 | - | 8.85 | - | needed | 0 | 2042 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@unchecked` | first | unchecked | - | 0.975 | 0.018 | 0.018 | - | 8.44 | - | needed | 0 | 1538 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@unchecked` | second | unchecked | - | 0.777 | 0.007 | 0.009 | - | 8.44 | - | needed | 0 | 1538 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted+eager` | first | counted | - | 1.532 | 0.013 | 0.009 | - | 12.40 | 1.61 | always | 0 | 2302 | 1490619 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted+eager` | second | counted | - | 1.466 | 0.006 | 0.004 | - | 12.40 | 1.61 | always | 0 | 2302 | 1490619 | 0 | yes |
| uniform-16384 | pagerank | `neo4j-graph` |  |  | 28 | 10.499 | 0.068 | 0.006 | 0.375 | 4.05 | - |  | 38 | 853 | - | 0 | yes |
| uniform-16384 | pagerank | `icebug` |  |  | 12 | 2.934 | 0.170 | 0.058 | 0.244 | 9.14 | - |  | 201 | 979 | - | 0 | yes |
| uniform-16384 | pagerank | `icecat` |  |  | 16 | 8.017 | 0.007 | 0.001 | 0.501 | 6.28 | - |  | 128 | 1557 | - | 0 | yes |
| uniform-16384 | pagerank | `grustcat` |  |  | 16 | 6.805 | 0.018 | 0.003 | 0.425 | 79.36 | - |  | 0 | 10541 | - | 0 | yes |
| uniform-16384 | pagerank | `grust` | first | counted | 16 | 6.007 | 0.071 | 0.012 | 0.375 | 17.32 | - | needed | 484 | 2299 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust` | second | counted | 16 | 3.299 | 0.074 | 0.023 | 0.206 | 17.32 | - | needed | 1 | 2299 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted` | first | counted | 16 | 3.376 | 0.104 | 0.031 | 0.211 | 11.89 | 1.60 | needed | 6 | 1792 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted` | second | counted | 16 | 3.388 | 0.252 | 0.075 | 0.212 | 11.89 | 1.60 | needed | 0 | 1792 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 16 | 2.695 | 0.026 | 0.010 | 0.168 | 9.89 | 1.41 | needed | 4 | 2299 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 16 | 2.607 | 0.009 | 0.003 | 0.163 | 9.89 | 1.41 | needed | 1 | 2299 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@unchecked` | first | unchecked | 16 | 2.678 | 0.074 | 0.028 | 0.167 | 9.85 | 1.39 | needed | 3 | 1793 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@unchecked` | second | unchecked | 16 | 2.602 | 0.029 | 0.011 | 0.163 | 9.85 | 1.39 | needed | 0 | 1793 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted+eager` | first | counted | 16 | 3.180 | 0.050 | 0.016 | 0.199 | 12.05 | 1.61 | always | 4 | 2299 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted+eager` | second | counted | 16 | 3.029 | 0.091 | 0.030 | 0.189 | 12.05 | 1.61 | always | 0 | 2299 | 4226299 | 0 | yes |
| uniform-16384 | triangles | `neo4j-graph` |  |  | - | 1.280 | 0.014 | 0.011 | - | 4.01 | - |  | 51 | 853 | - | 0 | yes |
| uniform-16384 | triangles | `grust` | first | counted | - | 9.042 | 0.085 | 0.009 | - | 19.63 | - | needed | 1031 | 2301 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust` | second | counted | - | 6.417 | 0.028 | 0.004 | - | 19.63 | - | needed | 1 | 2301 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted` | first | counted | - | 7.248 | 0.030 | 0.004 | - | 10.78 | - | needed | 257 | 1025 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted` | second | counted | - | 7.271 | 0.013 | 0.002 | - | 10.78 | - | needed | 512 | 1025 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@work-uncounted` | first | work-uncounted | - | 7.090 | 0.053 | 0.007 | - | 9.56 | - | needed | 257 | 1025 | - | 0 | yes |
| uniform-16384 | triangles | `grust-next@work-uncounted` | second | work-uncounted | - | 7.134 | 0.023 | 0.003 | - | 9.56 | - | needed | 512 | 1025 | - | 0 | yes |
| uniform-16384 | triangles | `grust-next@unchecked` | first | unchecked | - | 6.982 | 0.045 | 0.006 | - | 8.81 | - | needed | 257 | 1024 | - | 0 | yes |
| uniform-16384 | triangles | `grust-next@unchecked` | second | unchecked | - | 7.011 | 0.006 | 0.001 | - | 8.81 | - | needed | 512 | 1024 | - | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted+eager` | first | counted | - | 7.238 | 0.019 | 0.003 | - | 10.82 | 0.00 | always | 257 | 1026 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted+eager` | second | counted | - | 7.314 | 0.012 | 0.002 | - | 10.82 | 0.00 | always | 512 | 1026 | 3829630 | 0 | yes |
| uniform-16384 | wcc | `neo4j-graph` |  |  | - | 1.109 | 0.000 | 0.000 | - | 4.01 | - |  | 1 | 852 | - | 0 | yes |
| uniform-16384 | wcc | `icebug` |  |  | - | 2.211 | 0.038 | 0.017 | - | 9.17 | - |  | 69 | 979 | - | 0 | yes |
| uniform-16384 | wcc | `icecat` |  |  | - | 1.067 | 0.004 | 0.004 | - | 6.73 | - |  | 65 | 2068 | - | 0 | yes |
| uniform-16384 | wcc | `grustcat` |  |  | - | 0.742 | 0.002 | 0.002 | - | 78.97 | - |  | 0 | 10030 | - | 0 | yes |
| uniform-16384 | wcc | `grust` | first | counted | - | 1.316 | 0.034 | 0.026 | - | 17.65 | - | needed | 142 | 2299 | 1031986 | 0 | yes |
| uniform-16384 | wcc | `grust` | second | counted | - | 0.641 | 0.003 | 0.005 | - | 17.65 | - | needed | 34 | 2299 | 1031986 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted` | first | counted | - | 0.574 | 0.013 | 0.022 | - | 10.72 | - | needed | 3 | 2047 | 1031997 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted` | second | counted | - | 0.564 | 0.016 | 0.029 | - | 10.72 | - | needed | 2 | 2047 | 1031997 | 0 | yes |
| uniform-16384 | wcc | `grust-next@work-uncounted` | first | work-uncounted | - | 0.494 | 0.057 | 0.115 | - | 8.42 | - | needed | 3 | 2045 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@work-uncounted` | second | work-uncounted | - | 0.461 | 0.019 | 0.040 | - | 8.42 | - | needed | 2 | 2045 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@unchecked` | first | unchecked | - | 0.545 | 0.043 | 0.079 | - | 8.36 | - | needed | 3 | 1535 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@unchecked` | second | unchecked | - | 0.534 | 0.038 | 0.072 | - | 8.36 | - | needed | 3 | 1535 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted+eager` | first | counted | - | 0.510 | 0.032 | 0.063 | - | 12.49 | 1.60 | always | 3 | 2302 | 1474270 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted+eager` | second | counted | - | 0.551 | 0.009 | 0.016 | - | 12.49 | 1.60 | always | 1 | 2302 | 1474270 | 0 | yes |
| uniform-65536 | bfs | `icebug` |  |  | - | 8.577 | 0.260 | 0.030 | - | 42.95 | - |  | 216 | 3889 | - | 0 | yes |
| uniform-65536 | bfs | `icecat` |  |  | - | 4.030 | 0.305 | 0.076 | - | 18.40 | - |  | 253 | 1532 | - | 0 | yes |
| uniform-65536 | bfs | `grustcat` |  |  | - | 4.354 | 0.079 | 0.018 | - | 358.89 | - |  | 0 | 37597 | - | 0 | yes |
| uniform-65536 | bfs | `grust` | first | counted | - | 4.204 | 0.035 | 0.008 | - | 71.70 | - | needed | 367 | 2597 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust` | second | counted | - | 3.184 | 0.012 | 0.004 | - | 71.70 | - | needed | 197 | 2597 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted` | first | counted | - | 3.272 | 0.079 | 0.024 | - | 36.80 | - | needed | 118 | 2772 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted` | second | counted | - | 3.061 | 0.054 | 0.018 | - | 36.80 | - | needed | 78 | 2772 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@work-uncounted` | first | work-uncounted | - | 3.171 | 0.106 | 0.033 | - | 29.93 | - | needed | 119 | 2776 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@work-uncounted` | second | work-uncounted | - | 2.921 | 0.085 | 0.029 | - | 29.93 | - | needed | 90 | 2776 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@unchecked` | first | unchecked | - | 3.140 | 0.040 | 0.013 | - | 28.86 | - | needed | 112 | 2777 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@unchecked` | second | unchecked | - | 2.975 | 0.073 | 0.025 | - | 28.86 | - | needed | 78 | 2777 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted+eager` | first | counted | - | 3.159 | 0.012 | 0.004 | - | 42.50 | 5.11 | always | 123 | 3288 | 5963146 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted+eager` | second | counted | - | 3.048 | 0.073 | 0.024 | - | 42.50 | 5.11 | always | 82 | 3288 | 5963146 | 0 | yes |
| uniform-65536 | pagerank | `neo4j-graph` |  |  | 34 | 16.302 | 0.283 | 0.017 | 0.479 | 13.08 | - |  | 94 | 1867 | - | 0 | yes |
| uniform-65536 | pagerank | `icebug` |  |  | 11 | 7.375 | 0.063 | 0.009 | 0.670 | 42.60 | - |  | 488 | 3889 | - | 0 | yes |
| uniform-65536 | pagerank | `icecat` |  |  | 16 | 32.716 | 0.054 | 0.002 | 2.045 | 18.40 | - |  | 606 | 1565 | - | 0 | yes |
| uniform-65536 | pagerank | `grustcat` |  |  | 16 | 29.495 | 0.100 | 0.003 | 1.843 | 367.94 | - |  | 0 | 37597 | - | 0 | yes |
| uniform-65536 | pagerank | `grust` | first | counted | 16 | 17.406 | 0.345 | 0.020 | 1.088 | 69.24 | - | needed | 1134 | 3106 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust` | second | counted | 16 | 8.156 | 0.075 | 0.009 | 0.510 | 69.24 | - | needed | 5 | 3106 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted` | first | counted | 16 | 7.008 | 0.159 | 0.023 | 0.438 | 41.61 | 5.20 | needed | 12 | 3290 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted` | second | counted | 16 | 6.683 | 0.097 | 0.014 | 0.418 | 41.61 | 5.20 | needed | 3 | 3290 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 16 | 4.480 | 0.049 | 0.011 | 0.280 | 33.43 | 4.47 | needed | 13 | 3286 | - | 0 | yes |
| uniform-65536 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 16 | 4.467 | 0.080 | 0.018 | 0.279 | 33.43 | 4.47 | needed | 3 | 3286 | - | 0 | yes |
| uniform-65536 | pagerank | `grust-next@unchecked` | first | unchecked | 16 | 4.505 | 0.044 | 0.010 | 0.282 | 34.17 | 4.38 | needed | 13 | 3795 | - | 0 | yes |
| uniform-65536 | pagerank | `grust-next@unchecked` | second | unchecked | 16 | 4.342 | 0.150 | 0.035 | 0.271 | 34.17 | 4.38 | needed | 3 | 3795 | - | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted+eager` | first | counted | 16 | 6.538 | 0.006 | 0.001 | 0.409 | 42.58 | 5.14 | always | 14 | 3795 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted+eager` | second | counted | 16 | 6.368 | 0.107 | 0.017 | 0.398 | 42.58 | 5.14 | always | 4 | 3795 | 16907315 | 0 | yes |
| uniform-65536 | triangles | `neo4j-graph` |  |  | - | 3.990 | 0.036 | 0.009 | - | 13.25 | - |  | 51 | 1876 | - | 0 | yes |
| uniform-65536 | triangles | `grust` | first | counted | - | 32.539 | 0.323 | 0.010 | - | 85.85 | - | needed | 1770 | 2599 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust` | second | counted | - | 26.149 | 0.080 | 0.003 | - | 85.85 | - | needed | 1 | 2599 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted` | first | counted | - | 29.058 | 0.085 | 0.003 | - | 40.29 | - | needed | 517 | 1755 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted` | second | counted | - | 27.611 | 0.158 | 0.006 | - | 40.29 | - | needed | 1026 | 1755 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@work-uncounted` | first | work-uncounted | - | 28.248 | 0.059 | 0.002 | - | 33.87 | - | needed | 517 | 1756 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@work-uncounted` | second | work-uncounted | - | 27.288 | 0.112 | 0.004 | - | 33.87 | - | needed | 1026 | 1756 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@unchecked` | first | unchecked | - | 27.897 | 0.015 | 0.001 | - | 33.60 | - | needed | 517 | 2266 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@unchecked` | second | unchecked | - | 27.008 | 0.220 | 0.008 | - | 33.60 | - | needed | 1026 | 2266 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted+eager` | first | counted | - | 28.914 | 0.112 | 0.004 | - | 40.24 | 0.00 | always | 517 | 1758 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted+eager` | second | counted | - | 27.538 | 0.155 | 0.006 | - | 40.24 | 0.00 | always | 1026 | 1758 | 15327135 | 0 | yes |
| uniform-65536 | wcc | `neo4j-graph` |  |  | - | 3.080 | 0.134 | 0.044 | - | 13.26 | - |  | 228 | 1871 | - | 0 | yes |
| uniform-65536 | wcc | `icebug` |  |  | - | 13.062 | 0.110 | 0.008 | - | 43.26 | - |  | 244 | 3889 | - | 0 | yes |
| uniform-65536 | wcc | `icecat` |  |  | - | 3.958 | 0.013 | 0.003 | - | 18.26 | - |  | 3 | 1420 | - | 0 | yes |
| uniform-65536 | wcc | `grustcat` |  |  | - | 3.077 | 0.023 | 0.008 | - | 364.89 | - |  | 0 | 37597 | - | 0 | yes |
| uniform-65536 | wcc | `grust` | first | counted | - | 2.711 | 0.162 | 0.060 | - | 69.98 | - | needed | 241 | 3107 | 4128513 | 0 | yes |
| uniform-65536 | wcc | `grust` | second | counted | - | 1.997 | 0.027 | 0.013 | - | 69.98 | - | needed | 132 | 3107 | 4128513 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted` | first | counted | - | 1.797 | 0.057 | 0.032 | - | 37.96 | - | needed | 4 | 3282 | 4128523 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted` | second | counted | - | 1.653 | 0.044 | 0.026 | - | 37.96 | - | needed | 2 | 3282 | 4128523 | 0 | yes |
| uniform-65536 | wcc | `grust-next@work-uncounted` | first | work-uncounted | - | 1.515 | 0.093 | 0.062 | - | 29.02 | - | needed | 3 | 2772 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@work-uncounted` | second | work-uncounted | - | 1.568 | 0.040 | 0.026 | - | 29.02 | - | needed | 2 | 2772 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@unchecked` | first | unchecked | - | 1.540 | 0.053 | 0.034 | - | 29.38 | - | needed | 3 | 2773 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@unchecked` | second | unchecked | - | 1.605 | 0.099 | 0.062 | - | 29.38 | - | needed | 3 | 2773 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted+eager` | first | counted | - | 1.650 | 0.036 | 0.022 | - | 41.40 | 5.15 | always | 4 | 3288 | 5897876 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted+eager` | second | counted | - | 1.656 | 0.018 | 0.011 | - | 41.40 | 5.15 | always | 2 | 3288 | 5897876 | 0 | yes |

### `large-full-width.json`: large-full-width

workers 16, concurrency 16, allocator glibc default, not pinned, 1 warmup + 5 repeats, steal over the run 3 ticks, 708.5 s, unusable at MAD/median >= 0.25

| fixture | algorithm | participant | call | accounting | iters | total ms | MAD | MAD/median | per iter | build ms | incoming ms | prepare | minflt | minflt build | work units | steal | usable |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |
| hub-2097152 | pagerank | `neo4j-graph` |  |  | 28 | 260.044 | 1.677 | 0.006 | 9.287 | 409.29 | - |  | 1119 | 3993 | - | 1 | yes |
| hub-2097152 | pagerank | `icebug` |  |  | 10 | 455.574 | 6.232 | 0.014 | 45.557 | 3300.23 | - |  | 1676 | 106004 | - | 1 | yes |
| hub-2097152 | pagerank | `icecat` |  |  | 16 | 1713.891 | 3.465 | 0.002 | 107.118 | 585.76 | - |  | 10704 | 6432 | - | 1 | yes |
| hub-2097152 | pagerank | `grustcat` |  |  | 16 | 2161.983 | 199.825 | 0.092 | 135.124 | 17404.62 | - |  | 6625 | 1090545 | - | 1 | yes |
| hub-2097152 | pagerank | `grust` | first | counted | 16 | 1084.330 | 7.683 | 0.007 | 67.771 | 3779.21 | - | needed | 3306 | 21451 | 540705943 | 1 | yes |
| hub-2097152 | pagerank | `grust` | second | counted | 16 | 502.373 | 9.550 | 0.019 | 31.398 | 3779.21 | - | needed | 13 | 21451 | 540705943 | 1 | yes |
| hub-2097152 | pagerank | `grust-next@counted` | first | counted | 16 | 274.752 | 15.172 | 0.055 | 17.172 | 1523.44 | 230.28 | needed | 1625 | 22638 | 540705943 | 1 | yes |
| hub-2097152 | pagerank | `grust-next@counted` | second | counted | 16 | 233.439 | 1.366 | 0.006 | 14.590 | 1523.44 | 230.28 | needed | 2056 | 22638 | 540705943 | 1 | yes |
| hub-2097152 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 16 | 219.871 | 5.686 | 0.026 | 13.742 | 1260.21 | 205.01 | needed | 1624 | 22636 | - | 1 | yes |
| hub-2097152 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 16 | 227.123 | 1.468 | 0.006 | 14.195 | 1260.21 | 205.01 | needed | 2054 | 22636 | - | 1 | yes |
| hub-2097152 | pagerank | `grust-next@unchecked` | first | unchecked | 16 | 209.830 | 0.637 | 0.003 | 13.114 | 1257.25 | 203.57 | needed | 1623 | 22125 | - | 1 | yes |
| hub-2097152 | pagerank | `grust-next@unchecked` | second | unchecked | 16 | 216.359 | 4.122 | 0.019 | 13.522 | 1257.25 | 203.57 | needed | 2055 | 22125 | - | 1 | yes |
| uniform-2097152 | pagerank | `neo4j-graph` |  |  | 28 | 262.937 | 2.498 | 0.009 | 9.391 | 410.61 | - |  | 1120 | 2567 | - | 2 | yes |
| uniform-2097152 | pagerank | `icebug` |  |  | 10 | 483.902 | 8.912 | 0.018 | 48.390 | 3050.69 | - |  | 1676 | 100284 | - | 2 | yes |
| uniform-2097152 | pagerank | `icecat` |  |  | 16 | 2005.722 | 109.563 | 0.055 | 125.358 | 585.81 | - |  | 10705 | 5123 | - | 2 | yes |
| uniform-2097152 | pagerank | `grustcat` |  |  | 16 | 2640.273 | 28.742 | 0.011 | 165.017 | 19916.72 | - |  | 0 | 1081010 | - | 2 | yes |
| uniform-2097152 | pagerank | `grust` | first | counted | 16 | 1131.940 | 8.184 | 0.007 | 70.746 | 3804.92 | - | needed | 2827 | 19093 | 541064143 | 2 | yes |
| uniform-2097152 | pagerank | `grust` | second | counted | 16 | 548.049 | 17.238 | 0.031 | 34.253 | 3804.92 | - | needed | 12 | 19093 | 541064143 | 2 | yes |
| uniform-2097152 | pagerank | `grust-next@counted` | first | counted | 16 | 248.589 | 6.982 | 0.028 | 15.537 | 1547.84 | 237.10 | needed | 1622 | 20300 | 541064143 | 2 | yes |
| uniform-2097152 | pagerank | `grust-next@counted` | second | counted | 16 | 253.451 | 9.764 | 0.039 | 15.841 | 1547.84 | 237.10 | needed | 2057 | 20300 | 541064143 | 2 | yes |
| uniform-2097152 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 16 | 228.119 | 3.917 | 0.017 | 14.257 | 1279.23 | 214.81 | needed | 1625 | 20814 | - | 2 | yes |
| uniform-2097152 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 16 | 228.784 | 5.439 | 0.024 | 14.299 | 1279.23 | 214.81 | needed | 2057 | 20814 | - | 2 | yes |
| uniform-2097152 | pagerank | `grust-next@unchecked` | first | unchecked | 16 | 226.017 | 1.635 | 0.007 | 14.126 | 1281.28 | 216.93 | needed | 1624 | 20814 | - | 2 | yes |
| uniform-2097152 | pagerank | `grust-next@unchecked` | second | unchecked | 16 | 228.262 | 6.733 | 0.029 | 14.266 | 1281.28 | 216.93 | needed | 2057 | 20814 | - | 2 | yes |

### `large-one-thread.json`: large-one-thread

workers 1, concurrency 1, allocator glibc default, not pinned, 1 warmup + 5 repeats, steal over the run 7 ticks, 1671.6 s, unusable at MAD/median >= 0.25

| fixture | algorithm | participant | call | accounting | iters | total ms | MAD | MAD/median | per iter | build ms | incoming ms | prepare | minflt | minflt build | work units | steal | usable |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |
| hub-2097152 | pagerank | `neo4j-graph` |  |  | 26 | 2091.593 | 5.881 | 0.003 | 80.446 | 2616.87 | - |  | 1038 | 3272 | - | 3 | yes |
| hub-2097152 | pagerank | `icebug` |  |  | 10 | 4305.737 | 358.393 | 0.083 | 430.574 | 3316.26 | - |  | 1569 | 106004 | - | 3 | yes |
| hub-2097152 | pagerank | `icecat` |  |  | 16 | 1713.810 | 21.947 | 0.013 | 107.113 | 580.99 | - |  | 10705 | 6433 | - | 3 | yes |
| hub-2097152 | pagerank | `grustcat` |  |  | 16 | 1946.085 | 46.228 | 0.024 | 121.630 | 17606.01 | - |  | 6625 | 1090545 | - | 3 | yes |
| hub-2097152 | pagerank | `grust#1` | first | counted | 16 | 4987.081 | 70.651 | 0.014 | 311.693 | 3741.76 | - | needed | 3142 | 20942 | 540705943 | 3 | yes |
| hub-2097152 | pagerank | `grust#1` | second | counted | 16 | 4398.600 | 71.313 | 0.016 | 274.913 | 3741.76 | - | needed | 0 | 20942 | 540705943 | 3 | yes |
| hub-2097152 | pagerank | `grust#unset` | first | counted | 16 | 7810.226 | 196.876 | 0.025 | 488.139 | 3780.73 | - | needed | 2595 | 20926 | 559594681 | 3 | yes |
| hub-2097152 | pagerank | `grust#unset` | second | counted | 16 | 7772.384 | 75.864 | 0.010 | 485.774 | 3780.73 | - | needed | 519 | 20926 | 559594681 | 3 | yes |
| hub-2097152 | pagerank | `grust-next@counted#1` | first | counted | 16 | 2170.695 | 43.135 | 0.020 | 135.668 | 1991.76 | 552.73 | needed | 1559 | 22900 | 540705943 | 3 | yes |
| hub-2097152 | pagerank | `grust-next@counted#1` | second | counted | 16 | 1935.325 | 23.387 | 0.012 | 120.958 | 1991.76 | 552.73 | needed | 517 | 22900 | 540705943 | 3 | yes |
| hub-2097152 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 16 | 2013.592 | 101.382 | 0.050 | 125.849 | 1761.51 | 536.32 | needed | 1559 | 22900 | - | 3 | yes |
| hub-2097152 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 16 | 1691.744 | 14.341 | 0.008 | 105.734 | 1761.51 | 536.32 | needed | 517 | 22900 | - | 3 | yes |
| hub-2097152 | pagerank | `grust-next@unchecked#1` | first | unchecked | 16 | 1935.463 | 322.660 | 0.167 | 120.966 | 1730.72 | 523.81 | needed | 1559 | 22900 | - | 3 | yes |
| hub-2097152 | pagerank | `grust-next@unchecked#1` | second | unchecked | 16 | 1774.220 | 116.992 | 0.066 | 110.889 | 1730.72 | 523.81 | needed | 517 | 22900 | - | 3 | yes |
| hub-2097152 | pagerank | `grust-next@counted#unset` | first | counted | 16 | 4025.057 | 132.514 | 0.033 | 251.566 | 1756.67 | - | needed | 2595 | 20289 | 559594681 | 3 | yes |
| hub-2097152 | pagerank | `grust-next@counted#unset` | second | counted | 16 | 4115.769 | 46.295 | 0.011 | 257.236 | 1756.67 | - | needed | 519 | 20289 | 559594681 | 3 | yes |
| hub-2097152 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 16 | 3436.314 | 43.293 | 0.013 | 214.770 | 1281.31 | - | needed | 2595 | 20799 | - | 3 | yes |
| hub-2097152 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 16 | 3183.435 | 173.108 | 0.054 | 198.965 | 1281.31 | - | needed | 519 | 20799 | - | 3 | yes |
| hub-2097152 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 16 | 2917.493 | 44.540 | 0.015 | 182.343 | 1263.90 | - | needed | 2595 | 20288 | - | 3 | yes |
| hub-2097152 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 16 | 3292.096 | 318.972 | 0.097 | 205.756 | 1263.90 | - | needed | 519 | 20288 | - | 3 | yes |
| uniform-2097152 | pagerank | `neo4j-graph` |  |  | 26 | 2162.612 | 19.685 | 0.009 | 83.177 | 2584.38 | - |  | 1037 | 2360 | - | 4 | yes |
| uniform-2097152 | pagerank | `icebug` |  |  | 10 | 4140.888 | 40.401 | 0.010 | 414.089 | 3035.71 | - |  | 1573 | 100284 | - | 4 | yes |
| uniform-2097152 | pagerank | `icecat` |  |  | 16 | 2063.808 | 324.691 | 0.157 | 128.988 | 577.38 | - |  | 10705 | 5122 | - | 4 | yes |
| uniform-2097152 | pagerank | `grustcat` |  |  | 16 | 2399.054 | 35.568 | 0.015 | 149.941 | 19647.67 | - |  | 0 | 1081010 | - | 4 | yes |
| uniform-2097152 | pagerank | `grust#1` | first | counted | 16 | 5186.498 | 59.959 | 0.012 | 324.156 | 3768.90 | - | needed | 2659 | 19093 | 541064143 | 4 | yes |
| uniform-2097152 | pagerank | `grust#1` | second | counted | 16 | 4575.575 | 48.021 | 0.010 | 285.973 | 3768.90 | - | needed | 0 | 19093 | 541064143 | 4 | yes |
| uniform-2097152 | pagerank | `grust#unset` | first | counted | 16 | 7639.664 | 159.360 | 0.021 | 477.479 | 3742.21 | - | needed | 2595 | 19093 | 559938553 | 4 | yes |
| uniform-2097152 | pagerank | `grust#unset` | second | counted | 16 | 7545.628 | 82.125 | 0.011 | 471.602 | 3742.21 | - | needed | 519 | 19093 | 559938553 | 4 | yes |
| uniform-2097152 | pagerank | `grust-next@counted#1` | first | counted | 16 | 2207.803 | 62.263 | 0.028 | 137.988 | 1968.95 | 529.75 | needed | 1559 | 21081 | 541064143 | 4 | yes |
| uniform-2097152 | pagerank | `grust-next@counted#1` | second | counted | 16 | 2010.087 | 52.547 | 0.026 | 125.630 | 1968.95 | 529.75 | needed | 517 | 21081 | 541064143 | 4 | yes |
| uniform-2097152 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 16 | 1791.578 | 24.649 | 0.014 | 111.974 | 1742.62 | 517.71 | needed | 1559 | 21081 | - | 4 | yes |
| uniform-2097152 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 16 | 1683.808 | 10.799 | 0.006 | 105.238 | 1742.62 | 517.71 | needed | 517 | 21081 | - | 4 | yes |
| uniform-2097152 | pagerank | `grust-next@unchecked#1` | first | unchecked | 16 | 1968.106 | 30.860 | 0.016 | 123.007 | 1712.73 | 505.35 | needed | 1559 | 21081 | - | 4 | yes |
| uniform-2097152 | pagerank | `grust-next@unchecked#1` | second | unchecked | 16 | 1845.729 | 240.591 | 0.130 | 115.358 | 1712.73 | 505.35 | needed | 517 | 21081 | - | 4 | yes |
| uniform-2097152 | pagerank | `grust-next@counted#unset` | first | counted | 16 | 4023.105 | 11.138 | 0.003 | 251.444 | 1769.40 | - | needed | 2595 | 18952 | 559938553 | 4 | yes |
| uniform-2097152 | pagerank | `grust-next@counted#unset` | second | counted | 16 | 4300.807 | 153.476 | 0.036 | 268.800 | 1769.40 | - | needed | 519 | 18952 | 559938553 | 4 | yes |
| uniform-2097152 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 16 | 3184.505 | 89.668 | 0.028 | 199.032 | 1281.86 | - | needed | 2595 | 18952 | - | 4 | yes |
| uniform-2097152 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 16 | 3247.638 | 191.605 | 0.059 | 202.977 | 1281.86 | - | needed | 519 | 18952 | - | 4 | yes |
| uniform-2097152 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 16 | 3133.056 | 182.933 | 0.058 | 195.816 | 1259.97 | - | needed | 2595 | 18952 | - | 4 | yes |
| uniform-2097152 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 16 | 3007.613 | 42.731 | 0.014 | 187.976 | 1259.97 | - | needed | 519 | 18952 | - | 4 | yes |

### `one-thread.json`: one-thread

workers 1, concurrency 1, allocator glibc default, not pinned, 1 warmup + 5 repeats, steal over the run 1 ticks, 233.5 s, unusable at MAD/median >= 0.25

Not timed (no agreeing parity row): neo4j-graph pagerank layered-16384.edges, neo4j-graph pagerank layered-65536.edges, neo4j-graph pagerank path-16384.edges, neo4j-graph pagerank path-65536.edges 

| fixture | algorithm | participant | call | accounting | iters | total ms | MAD | MAD/median | per iter | build ms | incoming ms | prepare | minflt | minflt build | work units | steal | usable |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |
| hub-16384 | bfs | `icebug` |  |  | - | 1.399 | 0.002 | 0.001 | - | 9.21 | - |  | 58 | 1018 | - | 0 | yes |
| hub-16384 | bfs | `icecat` |  |  | - | 0.811 | 0.009 | 0.011 | - | 6.20 | - |  | 96 | 2066 | - | 0 | yes |
| hub-16384 | bfs | `grustcat` |  |  | - | 0.582 | 0.002 | 0.004 | - | 77.71 | - |  | 1 | 9804 | - | 0 | yes |
| hub-16384 | bfs | `grust#1` | first | counted | - | 1.515 | 0.007 | 0.004 | - | 17.22 | - | needed | 36 | 2298 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust#1` | second | counted | - | 1.463 | 0.028 | 0.019 | - | 17.22 | - | needed | 0 | 2298 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust#unset` | first | counted | - | 1.513 | 0.005 | 0.004 | - | 16.81 | - | needed | 36 | 1773 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust#unset` | second | counted | - | 1.441 | 0.012 | 0.009 | - | 16.81 | - | needed | 0 | 1773 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted#1` | first | counted | - | 1.529 | 0.002 | 0.001 | - | 9.67 | - | needed | 32 | 1228 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted#1` | second | counted | - | 1.464 | 0.002 | 0.002 | - | 9.67 | - | needed | 0 | 1228 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@work-uncounted#1` | first | work-uncounted | - | 0.952 | 0.002 | 0.002 | - | 7.85 | - | needed | 32 | 1739 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@work-uncounted#1` | second | work-uncounted | - | 0.856 | 0.015 | 0.017 | - | 7.85 | - | needed | 0 | 1739 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@unchecked#1` | first | unchecked | - | 0.805 | 0.012 | 0.015 | - | 7.25 | - | needed | 32 | 1228 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@unchecked#1` | second | unchecked | - | 0.715 | 0.009 | 0.012 | - | 7.25 | - | needed | 0 | 1228 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@counted#unset` | first | counted | - | 1.552 | 0.003 | 0.002 | - | 12.58 | - | needed | 36 | 1723 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted#unset` | second | counted | - | 1.444 | 0.002 | 0.001 | - | 12.58 | - | needed | 0 | 1723 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 0.948 | 0.011 | 0.012 | - | 8.57 | - | needed | 36 | 1723 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 0.839 | 0.005 | 0.006 | - | 8.57 | - | needed | 0 | 1723 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@unchecked#unset` | first | unchecked | - | 0.822 | 0.013 | 0.016 | - | 7.77 | - | needed | 36 | 1212 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@unchecked#unset` | second | unchecked | - | 0.706 | 0.005 | 0.006 | - | 7.77 | - | needed | 0 | 1212 | - | 0 | yes |
| hub-16384 | bfs | `grust-next@counted+eager#1` | first | counted | - | 1.544 | 0.013 | 0.008 | - | 11.18 | 1.44 | always | 32 | 1517 | 1489517 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted+eager#1` | second | counted | - | 1.444 | 0.000 | 0.000 | - | 11.18 | 1.44 | always | 0 | 1517 | 1489517 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted+eager#unset` | first | counted | - | 1.590 | 0.011 | 0.007 | - | 13.89 | 1.77 | always | 64 | 1500 | 1489517 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted+eager#unset` | second | counted | - | 1.462 | 0.019 | 0.013 | - | 13.89 | 1.77 | always | 0 | 1500 | 1489517 | 0 | yes |
| hub-16384 | pagerank | `neo4j-graph` |  |  | 36 | 13.092 | 0.029 | 0.002 | 0.364 | 7.63 | - |  | 22 | 666 | - | 0 | yes |
| hub-16384 | pagerank | `icebug` |  |  | 12 | 7.610 | 0.100 | 0.013 | 0.634 | 9.21 | - |  | 107 | 1018 | - | 0 | yes |
| hub-16384 | pagerank | `icecat` |  |  | 17 | 8.484 | 0.003 | 0.000 | 0.499 | 6.18 | - |  | 129 | 2066 | - | 0 | yes |
| hub-16384 | pagerank | `grustcat` |  |  | 17 | 7.276 | 0.038 | 0.005 | 0.428 | 78.10 | - |  | 0 | 9803 | - | 0 | yes |
| hub-16384 | pagerank | `grust#1` | first | counted | 17 | 11.515 | 0.036 | 0.003 | 0.677 | 16.92 | - | needed | 384 | 1787 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust#1` | second | counted | 17 | 9.603 | 0.014 | 0.001 | 0.565 | 16.92 | - | needed | 0 | 1787 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust#unset` | first | counted | 17 | 50.621 | 0.030 | 0.001 | 2.978 | 17.86 | - | needed | 128 | 2282 | 4567562 | 0 | yes |
| hub-16384 | pagerank | `grust#unset` | second | counted | 17 | 50.400 | 0.009 | 0.000 | 2.965 | 17.86 | - | needed | 32 | 2282 | 4567562 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted#1` | first | counted | 17 | 8.194 | 0.001 | 0.000 | 0.482 | 11.88 | 1.44 | needed | 96 | 2027 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted#1` | second | counted | 17 | 7.978 | 0.004 | 0.000 | 0.469 | 11.88 | 1.44 | needed | 0 | 2027 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 17 | 7.659 | 0.007 | 0.001 | 0.451 | 9.35 | 1.28 | needed | 96 | 1516 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 17 | 7.445 | 0.007 | 0.001 | 0.438 | 9.35 | 1.28 | needed | 0 | 1516 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@unchecked#1` | first | unchecked | 17 | 7.437 | 0.010 | 0.001 | 0.437 | 9.14 | 1.23 | needed | 96 | 1517 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@unchecked#1` | second | unchecked | 17 | 7.239 | 0.007 | 0.001 | 0.426 | 9.14 | 1.23 | needed | 0 | 1517 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted#unset` | first | counted | 17 | 23.361 | 0.047 | 0.002 | 1.374 | 12.61 | - | needed | 128 | 1212 | 4567562 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted#unset` | second | counted | 17 | 23.164 | 0.039 | 0.002 | 1.363 | 12.61 | - | needed | 32 | 1212 | 4567562 | 0 | yes |
| hub-16384 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 17 | 14.075 | 0.021 | 0.001 | 0.828 | 8.59 | - | needed | 128 | 1723 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 17 | 13.948 | 0.034 | 0.002 | 0.820 | 8.59 | - | needed | 32 | 1723 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 17 | 13.657 | 0.027 | 0.002 | 0.803 | 8.36 | - | needed | 128 | 1723 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 17 | 13.436 | 0.050 | 0.004 | 0.790 | 8.36 | - | needed | 32 | 1723 | - | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted+eager#1` | first | counted | 17 | 8.178 | 0.025 | 0.003 | 0.481 | 11.26 | 1.44 | always | 96 | 2027 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted+eager#1` | second | counted | 17 | 7.968 | 0.011 | 0.001 | 0.469 | 11.26 | 1.44 | always | 0 | 2027 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted+eager#unset` | first | counted | 17 | 23.376 | 0.009 | 0.000 | 1.375 | 14.52 | 1.79 | always | 128 | 2011 | 5009502 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted+eager#unset` | second | counted | 17 | 23.164 | 0.014 | 0.001 | 1.363 | 14.52 | 1.79 | always | 32 | 2011 | 5009502 | 0 | yes |
| hub-16384 | triangles | `neo4j-graph` |  |  | - | 7.951 | 0.060 | 0.008 | - | 7.67 | - |  | 4 | 666 | - | 0 | yes |
| hub-16384 | triangles | `grust#1` | first | counted | - | 17.433 | 0.019 | 0.001 | - | 19.35 | - | needed | 927 | 2299 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust#1` | second | counted | - | 15.576 | 0.027 | 0.002 | - | 19.35 | - | needed | 32 | 2299 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust#unset` | first | counted | - | 17.449 | 0.071 | 0.004 | - | 19.90 | - | needed | 927 | 2795 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust#unset` | second | counted | - | 15.557 | 0.060 | 0.004 | - | 19.90 | - | needed | 32 | 2795 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted#1` | first | counted | - | 16.514 | 0.039 | 0.002 | - | 12.76 | - | needed | 417 | 719 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted#1` | second | counted | - | 16.188 | 0.050 | 0.003 | - | 12.76 | - | needed | 511 | 719 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@work-uncounted#1` | first | work-uncounted | - | 16.306 | 0.098 | 0.006 | - | 11.06 | - | needed | 416 | 1230 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@work-uncounted#1` | second | work-uncounted | - | 15.935 | 0.030 | 0.002 | - | 11.06 | - | needed | 512 | 1230 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@unchecked#1` | first | unchecked | - | 16.150 | 0.150 | 0.009 | - | 10.92 | - | needed | 416 | 1230 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@unchecked#1` | second | unchecked | - | 15.830 | 0.013 | 0.001 | - | 10.92 | - | needed | 512 | 1230 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@counted#unset` | first | counted | - | 16.550 | 0.045 | 0.003 | - | 16.29 | - | needed | 417 | 1214 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted#unset` | second | counted | - | 16.156 | 0.083 | 0.005 | - | 16.29 | - | needed | 543 | 1214 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 16.242 | 0.129 | 0.008 | - | 11.69 | - | needed | 417 | 703 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 15.896 | 0.074 | 0.005 | - | 11.69 | - | needed | 543 | 703 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@unchecked#unset` | first | unchecked | - | 16.122 | 0.015 | 0.001 | - | 11.62 | - | needed | 417 | 703 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@unchecked#unset` | second | unchecked | - | 15.703 | 0.084 | 0.005 | - | 11.62 | - | needed | 543 | 703 | - | 0 | yes |
| hub-16384 | triangles | `grust-next@counted+eager#1` | first | counted | - | 16.531 | 0.029 | 0.002 | - | 13.08 | 0.00 | always | 417 | 1230 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted+eager#1` | second | counted | - | 16.154 | 0.059 | 0.004 | - | 13.08 | 0.00 | always | 511 | 1230 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted+eager#unset` | first | counted | - | 16.460 | 0.013 | 0.001 | - | 16.30 | 0.00 | always | 417 | 1214 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted+eager#unset` | second | counted | - | 16.123 | 0.027 | 0.002 | - | 16.30 | 0.00 | always | 543 | 1214 | 3742208 | 0 | yes |
| hub-16384 | wcc | `neo4j-graph` |  |  | - | 0.988 | 0.002 | 0.002 | - | 7.53 | - |  | 0 | 667 | - | 0 | yes |
| hub-16384 | wcc | `icebug` |  |  | - | 1.887 | 0.012 | 0.006 | - | 9.01 | - |  | 69 | 1018 | - | 0 | yes |
| hub-16384 | wcc | `icecat` |  |  | - | 0.905 | 0.011 | 0.013 | - | 5.75 | - |  | 66 | 1555 | - | 0 | yes |
| hub-16384 | wcc | `grustcat` |  |  | - | 0.606 | 0.005 | 0.009 | - | 78.30 | - |  | 1 | 10314 | - | 0 | yes |
| hub-16384 | wcc | `grust#1` | first | counted | - | 1.543 | 0.011 | 0.007 | - | 17.51 | - | needed | 33 | 2297 | 1031191 | 0 | yes |
| hub-16384 | wcc | `grust#1` | second | counted | - | 1.691 | 0.007 | 0.004 | - | 17.51 | - | needed | 31 | 2297 | 1031191 | 0 | yes |
| hub-16384 | wcc | `grust#unset` | first | counted | - | 4.138 | 0.002 | 0.001 | - | 17.01 | - | needed | 33 | 1772 | 1324773 | 0 | yes |
| hub-16384 | wcc | `grust#unset` | second | counted | - | 4.134 | 0.003 | 0.001 | - | 17.01 | - | needed | 31 | 1772 | 1324773 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted#1` | first | counted | - | 1.483 | 0.009 | 0.006 | - | 9.76 | - | needed | 32 | 1229 | 1031191 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted#1` | second | counted | - | 1.453 | 0.010 | 0.007 | - | 9.76 | - | needed | 16 | 1229 | 1031191 | 0 | yes |
| hub-16384 | wcc | `grust-next@work-uncounted#1` | first | work-uncounted | - | 0.803 | 0.007 | 0.009 | - | 7.47 | - | needed | 32 | 1228 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@work-uncounted#1` | second | work-uncounted | - | 0.772 | 0.007 | 0.010 | - | 7.47 | - | needed | 16 | 1228 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@unchecked#1` | first | unchecked | - | 0.597 | 0.006 | 0.010 | - | 7.91 | - | needed | 32 | 1228 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@unchecked#1` | second | unchecked | - | 0.553 | 0.003 | 0.006 | - | 7.91 | - | needed | 16 | 1228 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@counted#unset` | first | counted | - | 4.087 | 0.005 | 0.001 | - | 12.54 | - | needed | 32 | 1212 | 1324773 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted#unset` | second | counted | - | 4.089 | 0.003 | 0.001 | - | 12.54 | - | needed | 30 | 1212 | 1324773 | 0 | yes |
| hub-16384 | wcc | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 1.504 | 0.002 | 0.001 | - | 8.63 | - | needed | 32 | 1723 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 1.522 | 0.001 | 0.001 | - | 8.63 | - | needed | 30 | 1723 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@unchecked#unset` | first | unchecked | - | 1.262 | 0.008 | 0.006 | - | 8.22 | - | needed | 32 | 1213 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@unchecked#unset` | second | unchecked | - | 1.260 | 0.006 | 0.005 | - | 8.22 | - | needed | 31 | 1213 | - | 0 | yes |
| hub-16384 | wcc | `grust-next@counted+eager#1` | first | counted | - | 1.480 | 0.002 | 0.001 | - | 11.13 | 1.42 | always | 32 | 1517 | 1473131 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted+eager#1` | second | counted | - | 1.497 | 0.008 | 0.005 | - | 11.13 | 1.42 | always | 32 | 1517 | 1473131 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted+eager#unset` | first | counted | - | 4.089 | 0.004 | 0.001 | - | 13.88 | 1.76 | always | 32 | 1501 | 1766713 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted+eager#unset` | second | counted | - | 4.082 | 0.006 | 0.001 | - | 13.88 | 1.76 | always | 31 | 1501 | 1766713 | 0 | yes |
| hub-65536 | bfs | `icebug` |  |  | - | 8.407 | 0.231 | 0.027 | - | 43.46 | - |  | 216 | 4057 | - | 0 | yes |
| hub-65536 | bfs | `icecat` |  |  | - | 4.374 | 0.013 | 0.003 | - | 18.91 | - |  | 385 | 2681 | - | 0 | yes |
| hub-65536 | bfs | `grustcat` |  |  | - | 4.057 | 0.129 | 0.032 | - | 361.98 | - |  | 1 | 39254 | - | 0 | yes |
| hub-65536 | bfs | `grust#1` | first | counted | - | 5.900 | 0.023 | 0.004 | - | 69.95 | - | needed | 146 | 3612 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust#1` | second | counted | - | 5.291 | 0.011 | 0.002 | - | 69.95 | - | needed | 0 | 3612 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust#unset` | first | counted | - | 6.972 | 0.130 | 0.019 | - | 70.66 | - | needed | 144 | 3596 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust#unset` | second | counted | - | 6.260 | 0.003 | 0.001 | - | 70.66 | - | needed | 0 | 3596 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted#1` | first | counted | - | 6.253 | 0.067 | 0.011 | - | 40.18 | - | needed | 130 | 2906 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted#1` | second | counted | - | 5.470 | 0.056 | 0.010 | - | 40.18 | - | needed | 0 | 2906 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust-next@work-uncounted#1` | first | work-uncounted | - | 6.069 | 0.073 | 0.012 | - | 32.32 | - | needed | 130 | 2906 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@work-uncounted#1` | second | work-uncounted | - | 5.241 | 0.008 | 0.002 | - | 32.32 | - | needed | 0 | 2906 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@unchecked#1` | first | unchecked | - | 5.971 | 0.101 | 0.017 | - | 32.75 | - | needed | 130 | 3417 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@unchecked#1` | second | unchecked | - | 5.147 | 0.015 | 0.003 | - | 32.75 | - | needed | 0 | 3417 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@counted#unset` | first | counted | - | 7.396 | 0.057 | 0.008 | - | 49.79 | - | needed | 144 | 2842 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted#unset` | second | counted | - | 6.389 | 0.010 | 0.002 | - | 49.79 | - | needed | 0 | 2842 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 6.129 | 0.029 | 0.005 | - | 34.55 | - | needed | 144 | 2842 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 4.977 | 0.033 | 0.007 | - | 34.55 | - | needed | 0 | 2842 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@unchecked#unset` | first | unchecked | - | 5.274 | 0.047 | 0.009 | - | 33.65 | - | needed | 144 | 2842 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@unchecked#unset` | second | unchecked | - | 4.280 | 0.028 | 0.007 | - | 33.65 | - | needed | 0 | 2842 | - | 0 | yes |
| hub-65536 | bfs | `grust-next@counted+eager#1` | first | counted | - | 6.069 | 0.001 | 0.000 | - | 47.13 | 6.46 | always | 194 | 4056 | 5959069 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted+eager#1` | second | counted | - | 5.470 | 0.033 | 0.006 | - | 47.13 | 6.46 | always | 0 | 4056 | 5959069 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted+eager#unset` | first | counted | - | 7.171 | 0.047 | 0.007 | - | 58.24 | 7.88 | always | 256 | 3482 | 5959069 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted+eager#unset` | second | counted | - | 6.436 | 0.039 | 0.006 | - | 58.24 | 7.88 | always | 0 | 3482 | 5959069 | 0 | yes |
| hub-65536 | pagerank | `neo4j-graph` |  |  | 28 | 35.933 | 0.138 | 0.004 | 1.283 | 33.58 | - |  | 70 | 2172 | - | 0 | yes |
| hub-65536 | pagerank | `icebug` |  |  | 12 | 42.128 | 0.800 | 0.019 | 3.511 | 43.26 | - |  | 400 | 4057 | - | 0 | yes |
| hub-65536 | pagerank | `icecat` |  |  | 17 | 34.123 | 0.015 | 0.000 | 2.007 | 18.97 | - |  | 607 | 2680 | - | 0 | yes |
| hub-65536 | pagerank | `grustcat` |  |  | 17 | 30.228 | 0.031 | 0.001 | 1.778 | 360.47 | - |  | 0 | 38230 | - | 0 | yes |
| hub-65536 | pagerank | `grust#1` | first | counted | 17 | 52.589 | 0.209 | 0.004 | 3.093 | 70.65 | - | needed | 1024 | 3612 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust#1` | second | counted | 17 | 44.005 | 0.174 | 0.004 | 2.589 | 70.65 | - | needed | 0 | 3612 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust#unset` | first | counted | 17 | 203.554 | 0.337 | 0.002 | 11.974 | 69.75 | - | needed | 512 | 3087 | 18272770 | 0 | yes |
| hub-65536 | pagerank | `grust#unset` | second | counted | 17 | 202.188 | 0.138 | 0.001 | 11.893 | 69.75 | - | needed | 128 | 3087 | 18272770 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted#1` | first | counted | 17 | 34.017 | 0.128 | 0.004 | 2.001 | 47.07 | 6.41 | needed | 384 | 4057 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted#1` | second | counted | 17 | 33.202 | 0.100 | 0.003 | 1.953 | 47.07 | 6.41 | needed | 0 | 4057 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 17 | 31.923 | 0.122 | 0.004 | 1.878 | 38.00 | 5.68 | needed | 384 | 3546 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 17 | 31.208 | 0.192 | 0.006 | 1.836 | 38.00 | 5.68 | needed | 0 | 3546 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@unchecked#1` | first | unchecked | 17 | 31.143 | 0.262 | 0.008 | 1.832 | 37.56 | 5.71 | needed | 384 | 3546 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@unchecked#1` | second | unchecked | 17 | 30.343 | 0.261 | 0.009 | 1.785 | 37.56 | 5.71 | needed | 0 | 3546 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted#unset` | first | counted | 17 | 95.141 | 0.470 | 0.005 | 5.597 | 50.30 | - | needed | 512 | 2842 | 18272770 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted#unset` | second | counted | 17 | 95.603 | 0.557 | 0.006 | 5.624 | 50.30 | - | needed | 128 | 2842 | 18272770 | 0 | yes |
| hub-65536 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 17 | 58.502 | 0.099 | 0.002 | 3.441 | 34.51 | - | needed | 512 | 2842 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 17 | 57.629 | 0.082 | 0.001 | 3.390 | 34.51 | - | needed | 128 | 2842 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 17 | 56.149 | 0.253 | 0.005 | 3.303 | 33.62 | - | needed | 512 | 2842 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 17 | 55.791 | 0.316 | 0.006 | 3.282 | 33.62 | - | needed | 128 | 2842 | - | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted+eager#1` | first | counted | 17 | 34.125 | 0.214 | 0.006 | 2.007 | 45.93 | 6.41 | always | 384 | 3546 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted+eager#1` | second | counted | 17 | 33.344 | 0.222 | 0.007 | 1.961 | 45.93 | 6.41 | always | 0 | 3546 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted+eager#unset` | first | counted | 17 | 95.298 | 0.161 | 0.002 | 5.606 | 59.00 | 7.84 | always | 512 | 3993 | 20040830 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted+eager#unset` | second | counted | 17 | 94.287 | 0.086 | 0.001 | 5.546 | 59.00 | 7.84 | always | 128 | 3993 | 20040830 | 0 | yes |
| hub-65536 | triangles | `neo4j-graph` |  |  | - | 35.337 | 0.147 | 0.004 | - | 34.33 | - |  | 4 | 2172 | - | 0 | yes |
| hub-65536 | triangles | `grust#1` | first | counted | - | 74.247 | 0.238 | 0.003 | - | 83.76 | - | needed | 1665 | 3104 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust#1` | second | counted | - | 68.496 | 0.389 | 0.006 | - | 83.76 | - | needed | 128 | 3104 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust#unset` | first | counted | - | 73.800 | 0.181 | 0.002 | - | 83.97 | - | needed | 1665 | 3599 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust#unset` | second | counted | - | 68.508 | 0.090 | 0.001 | - | 83.97 | - | needed | 128 | 3599 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted#1` | first | counted | - | 72.514 | 0.017 | 0.000 | - | 51.44 | - | needed | 1666 | 3421 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted#1` | second | counted | - | 70.268 | 0.062 | 0.001 | - | 51.44 | - | needed | 1535 | 3421 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@work-uncounted#1` | first | work-uncounted | - | 71.639 | 0.114 | 0.002 | - | 44.17 | - | needed | 1666 | 2910 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@work-uncounted#1` | second | work-uncounted | - | 69.731 | 0.461 | 0.007 | - | 44.17 | - | needed | 1535 | 2910 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@unchecked#1` | first | unchecked | - | 71.102 | 0.328 | 0.005 | - | 43.11 | - | needed | 1666 | 2910 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@unchecked#1` | second | unchecked | - | 68.809 | 0.215 | 0.003 | - | 43.11 | - | needed | 1535 | 2910 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@counted#unset` | first | counted | - | 72.294 | 0.061 | 0.001 | - | 67.32 | - | needed | 1666 | 3357 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted#unset` | second | counted | - | 69.140 | 0.733 | 0.011 | - | 67.32 | - | needed | 1152 | 3357 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 71.363 | 0.040 | 0.001 | - | 50.08 | - | needed | 1666 | 2847 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 68.219 | 0.152 | 0.002 | - | 50.08 | - | needed | 641 | 2847 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@unchecked#unset` | first | unchecked | - | 70.872 | 0.110 | 0.002 | - | 50.81 | - | needed | 1666 | 3357 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@unchecked#unset` | second | unchecked | - | 67.675 | 0.054 | 0.001 | - | 50.81 | - | needed | 1152 | 3357 | - | 0 | yes |
| hub-65536 | triangles | `grust-next@counted+eager#1` | first | counted | - | 72.565 | 0.069 | 0.001 | - | 50.93 | 0.00 | always | 1666 | 2911 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted+eager#1` | second | counted | - | 70.637 | 0.488 | 0.007 | - | 50.93 | 0.00 | always | 1535 | 2911 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted+eager#unset` | first | counted | - | 72.549 | 0.297 | 0.004 | - | 66.79 | 0.00 | always | 1666 | 2846 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted+eager#unset` | second | counted | - | 69.430 | 0.774 | 0.011 | - | 66.79 | 0.00 | always | 641 | 2846 | 14971727 | 0 | yes |
| hub-65536 | wcc | `neo4j-graph` |  |  | - | 3.754 | 0.011 | 0.003 | - | 35.01 | - |  | 32 | 2173 | - | 0 | yes |
| hub-65536 | wcc | `icebug` |  |  | - | 11.249 | 0.411 | 0.037 | - | 43.34 | - |  | 239 | 4057 | - | 0 | yes |
| hub-65536 | wcc | `icecat` |  |  | - | 3.483 | 0.225 | 0.065 | - | 18.80 | - |  | 127 | 2552 | - | 0 | yes |
| hub-65536 | wcc | `grustcat` |  |  | - | 2.442 | 0.012 | 0.005 | - | 356.74 | - |  | 0 | 38230 | - | 0 | yes |
| hub-65536 | wcc | `grust#1` | first | counted | - | 6.660 | 0.010 | 0.002 | - | 71.47 | - | needed | 128 | 3612 | 4125471 | 0 | yes |
| hub-65536 | wcc | `grust#1` | second | counted | - | 7.128 | 0.004 | 0.000 | - | 71.47 | - | needed | 128 | 3612 | 4125471 | 0 | yes |
| hub-65536 | wcc | `grust#unset` | first | counted | - | 16.883 | 0.010 | 0.001 | - | 71.55 | - | needed | 128 | 3597 | 5303155 | 0 | yes |
| hub-65536 | wcc | `grust#unset` | second | counted | - | 16.788 | 0.023 | 0.001 | - | 71.55 | - | needed | 126 | 3597 | 5303155 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted#1` | first | counted | - | 6.460 | 0.040 | 0.006 | - | 40.37 | - | needed | 128 | 2906 | 4125471 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted#1` | second | counted | - | 6.218 | 0.084 | 0.014 | - | 40.37 | - | needed | 64 | 2906 | 4125471 | 0 | yes |
| hub-65536 | wcc | `grust-next@work-uncounted#1` | first | work-uncounted | - | 4.284 | 0.024 | 0.006 | - | 32.15 | - | needed | 128 | 2906 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@work-uncounted#1` | second | work-uncounted | - | 3.945 | 0.008 | 0.002 | - | 32.15 | - | needed | 64 | 2906 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@unchecked#1` | first | unchecked | - | 3.842 | 0.050 | 0.013 | - | 31.78 | - | needed | 128 | 2906 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@unchecked#1` | second | unchecked | - | 3.533 | 0.010 | 0.003 | - | 31.78 | - | needed | 64 | 2906 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@counted#unset` | first | counted | - | 16.666 | 0.008 | 0.001 | - | 49.93 | - | needed | 128 | 2843 | 5303155 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted#unset` | second | counted | - | 16.602 | 0.018 | 0.001 | - | 49.93 | - | needed | 126 | 2843 | 5303155 | 0 | yes |
| hub-65536 | wcc | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 7.105 | 0.054 | 0.008 | - | 34.55 | - | needed | 128 | 2842 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 6.974 | 0.028 | 0.004 | - | 34.55 | - | needed | 126 | 2842 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@unchecked#unset` | first | unchecked | - | 6.028 | 0.005 | 0.001 | - | 33.39 | - | needed | 128 | 2842 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@unchecked#unset` | second | unchecked | - | 5.900 | 0.015 | 0.002 | - | 33.39 | - | needed | 126 | 2842 | - | 0 | yes |
| hub-65536 | wcc | `grust-next@counted+eager#1` | first | counted | - | 6.541 | 0.027 | 0.004 | - | 45.67 | 6.46 | always | 128 | 3547 | 5893531 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted+eager#1` | second | counted | - | 6.486 | 0.034 | 0.005 | - | 45.67 | 6.46 | always | 128 | 3547 | 5893531 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted+eager#unset` | first | counted | - | 16.677 | 0.028 | 0.002 | - | 58.28 | 7.88 | always | 128 | 3483 | 7071215 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted+eager#unset` | second | counted | - | 16.669 | 0.003 | 0.000 | - | 58.28 | 7.88 | always | 127 | 3483 | 7071215 | 0 | yes |
| layered-16384 | bfs | `icebug` |  |  | - | 0.498 | 0.022 | 0.044 | - | 2.76 | - |  | 36 | 458 | - | 0 | yes |
| layered-16384 | bfs | `icecat` |  |  | - | 0.393 | 0.009 | 0.022 | - | 1.56 | - |  | 65 | 525 | - | 0 | yes |
| layered-16384 | bfs | `grustcat` |  |  | - | 0.257 | 0.006 | 0.022 | - | 29.57 | - |  | 0 | 6840 | - | 0 | yes |
| layered-16384 | bfs | `grust#1` | first | counted | - | 0.446 | 0.006 | 0.014 | - | 6.59 | - | needed | 30 | 1031 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust#1` | second | counted | - | 0.386 | 0.000 | 0.001 | - | 6.59 | - | needed | 0 | 1031 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust#unset` | first | counted | - | 0.454 | 0.002 | 0.004 | - | 6.87 | - | needed | 30 | 1017 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust#unset` | second | counted | - | 0.387 | 0.000 | 0.000 | - | 6.87 | - | needed | 0 | 1017 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted#1` | first | counted | - | 0.443 | 0.006 | 0.014 | - | 5.32 | - | needed | 26 | 904 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted#1` | second | counted | - | 0.380 | 0.000 | 0.000 | - | 5.32 | - | needed | 0 | 904 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@work-uncounted#1` | first | work-uncounted | - | 0.353 | 0.010 | 0.027 | - | 3.93 | - | needed | 26 | 904 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@work-uncounted#1` | second | work-uncounted | - | 0.289 | 0.003 | 0.010 | - | 3.93 | - | needed | 0 | 904 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@unchecked#1` | first | unchecked | - | 0.302 | 0.002 | 0.008 | - | 3.94 | - | needed | 26 | 904 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@unchecked#1` | second | unchecked | - | 0.251 | 0.001 | 0.003 | - | 3.94 | - | needed | 0 | 904 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@counted#unset` | first | counted | - | 0.437 | 0.002 | 0.005 | - | 5.49 | - | needed | 30 | 888 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted#unset` | second | counted | - | 0.381 | 0.000 | 0.001 | - | 5.49 | - | needed | 0 | 888 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 0.350 | 0.005 | 0.014 | - | 4.28 | - | needed | 30 | 888 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 0.287 | 0.002 | 0.008 | - | 4.28 | - | needed | 0 | 888 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@unchecked#unset` | first | unchecked | - | 0.307 | 0.003 | 0.011 | - | 3.98 | - | needed | 30 | 889 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@unchecked#unset` | second | unchecked | - | 0.253 | 0.004 | 0.018 | - | 3.98 | - | needed | 0 | 889 | - | 0 | yes |
| layered-16384 | bfs | `grust-next@counted+eager#1` | first | counted | - | 0.437 | 0.001 | 0.002 | - | 5.51 | 0.54 | always | 26 | 1000 | 493703 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted+eager#1` | second | counted | - | 0.381 | 0.000 | 0.001 | - | 5.51 | 0.54 | always | 0 | 1000 | 493703 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted+eager#unset` | first | counted | - | 0.494 | 0.007 | 0.015 | - | 6.22 | 0.72 | always | 58 | 984 | 493703 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted+eager#unset` | second | counted | - | 0.380 | 0.000 | 0.000 | - | 6.22 | 0.72 | always | 0 | 984 | 493703 | 0 | yes |
| layered-16384 | pagerank | `icebug` |  |  | 69 | 26.212 | 0.033 | 0.001 | 0.380 | 2.60 | - |  | 114 | 458 | - | 0 | yes |
| layered-16384 | pagerank | `icecat` |  |  | 84 | 27.668 | 0.006 | 0.000 | 0.329 | 1.68 | - |  | 128 | 526 | - | 0 | yes |
| layered-16384 | pagerank | `grustcat` |  |  | 84 | 26.307 | 0.063 | 0.002 | 0.313 | 29.97 | - |  | 0 | 7350 | - | 0 | yes |
| layered-16384 | pagerank | `grust#1` | first | counted | 84 | 30.174 | 0.050 | 0.002 | 0.359 | 6.70 | - | needed | 192 | 1032 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust#1` | second | counted | 84 | 29.339 | 0.078 | 0.003 | 0.349 | 6.70 | - | needed | 0 | 1032 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust#unset` | first | counted | 84 | 115.403 | 0.064 | 0.001 | 1.374 | 6.28 | - | needed | 128 | 1016 | 8667337 | 0 | yes |
| layered-16384 | pagerank | `grust#unset` | second | counted | 84 | 115.154 | 0.005 | 0.000 | 1.371 | 6.28 | - | needed | 32 | 1016 | 8667337 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted#1` | first | counted | 84 | 30.824 | 0.066 | 0.002 | 0.367 | 5.28 | 0.49 | needed | 96 | 1000 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted#1` | second | counted | 84 | 30.534 | 0.007 | 0.000 | 0.364 | 5.28 | 0.49 | needed | 0 | 1000 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 84 | 28.545 | 0.032 | 0.001 | 0.340 | 4.86 | 0.33 | needed | 96 | 1000 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 84 | 28.296 | 0.041 | 0.001 | 0.337 | 4.86 | 0.33 | needed | 0 | 1000 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@unchecked#1` | first | unchecked | 84 | 27.900 | 0.020 | 0.001 | 0.332 | 4.22 | 0.30 | needed | 96 | 1000 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@unchecked#1` | second | unchecked | 84 | 27.714 | 0.013 | 0.000 | 0.330 | 4.22 | 0.30 | needed | 0 | 1000 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted#unset` | first | counted | 84 | 88.775 | 0.115 | 0.001 | 1.057 | 5.80 | - | needed | 128 | 888 | 8667337 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted#unset` | second | counted | 84 | 88.490 | 0.099 | 0.001 | 1.053 | 5.80 | - | needed | 32 | 888 | 8667337 | 0 | yes |
| layered-16384 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 84 | 44.798 | 0.264 | 0.006 | 0.533 | 4.14 | - | needed | 128 | 888 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 84 | 44.399 | 0.035 | 0.001 | 0.529 | 4.14 | - | needed | 32 | 888 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 84 | 41.895 | 0.033 | 0.001 | 0.499 | 3.98 | - | needed | 128 | 888 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 84 | 41.741 | 0.008 | 0.000 | 0.497 | 3.98 | - | needed | 32 | 888 | - | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted+eager#1` | first | counted | 84 | 30.809 | 0.042 | 0.001 | 0.367 | 5.49 | 0.52 | always | 96 | 1000 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted+eager#1` | second | counted | 84 | 30.556 | 0.023 | 0.001 | 0.364 | 5.49 | 0.52 | always | 0 | 1000 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted+eager#unset` | first | counted | 84 | 88.797 | 0.182 | 0.002 | 1.057 | 6.16 | 0.69 | always | 128 | 984 | 8813732 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted+eager#unset` | second | counted | 84 | 88.571 | 0.061 | 0.001 | 1.054 | 6.16 | 0.69 | always | 32 | 984 | 8813732 | 0 | yes |
| layered-16384 | triangles | `neo4j-graph` |  |  | - | 0.778 | 0.015 | 0.019 | - | 2.01 | - |  | 3 | 408 | - | 0 | yes |
| layered-16384 | triangles | `grust#1` | first | counted | - | 2.868 | 0.040 | 0.014 | - | 7.31 | - | needed | 350 | 1158 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust#1` | second | counted | - | 2.182 | 0.015 | 0.007 | - | 7.31 | - | needed | 32 | 1158 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust#unset` | first | counted | - | 2.704 | 0.026 | 0.010 | - | 6.72 | - | needed | 350 | 1143 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust#unset` | second | counted | - | 2.189 | 0.026 | 0.012 | - | 6.72 | - | needed | 32 | 1143 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted#1` | first | counted | - | 2.683 | 0.038 | 0.014 | - | 5.19 | - | needed | 350 | 1032 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted#1` | second | counted | - | 2.538 | 0.010 | 0.004 | - | 5.19 | - | needed | 350 | 1032 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@work-uncounted#1` | first | work-uncounted | - | 2.468 | 0.021 | 0.009 | - | 4.28 | - | needed | 350 | 1032 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@work-uncounted#1` | second | work-uncounted | - | 2.402 | 0.025 | 0.011 | - | 4.28 | - | needed | 350 | 1032 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@unchecked#1` | first | unchecked | - | 2.367 | 0.014 | 0.006 | - | 4.22 | - | needed | 350 | 1032 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@unchecked#1` | second | unchecked | - | 2.291 | 0.009 | 0.004 | - | 4.22 | - | needed | 350 | 1032 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@counted#unset` | first | counted | - | 2.600 | 0.022 | 0.009 | - | 5.79 | - | needed | 350 | 1016 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted#unset` | second | counted | - | 2.274 | 0.006 | 0.002 | - | 5.79 | - | needed | 159 | 1016 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 2.464 | 0.021 | 0.009 | - | 4.43 | - | needed | 350 | 1016 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 2.130 | 0.017 | 0.008 | - | 4.43 | - | needed | 159 | 1016 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@unchecked#unset` | first | unchecked | - | 2.365 | 0.024 | 0.010 | - | 4.33 | - | needed | 350 | 1016 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@unchecked#unset` | second | unchecked | - | 2.033 | 0.021 | 0.010 | - | 4.33 | - | needed | 159 | 1016 | - | 0 | yes |
| layered-16384 | triangles | `grust-next@counted+eager#1` | first | counted | - | 2.595 | 0.023 | 0.009 | - | 5.10 | 0.00 | always | 350 | 1032 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted+eager#1` | second | counted | - | 2.535 | 0.004 | 0.002 | - | 5.10 | 0.00 | always | 350 | 1032 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted+eager#unset` | first | counted | - | 2.604 | 0.005 | 0.002 | - | 5.76 | 0.00 | always | 350 | 1016 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted+eager#unset` | second | counted | - | 2.253 | 0.011 | 0.005 | - | 5.76 | 0.00 | always | 159 | 1016 | 718265 | 0 | yes |
| layered-16384 | wcc | `neo4j-graph` |  |  | - | 0.930 | 0.008 | 0.008 | - | 2.10 | - |  | 1 | 409 | - | 0 | yes |
| layered-16384 | wcc | `icebug` |  |  | - | 0.911 | 0.015 | 0.016 | - | 2.59 | - |  | 43 | 458 | - | 0 | yes |
| layered-16384 | wcc | `icecat` |  |  | - | 0.498 | 0.002 | 0.003 | - | 1.58 | - |  | 64 | 526 | - | 0 | yes |
| layered-16384 | wcc | `grustcat` |  |  | - | 0.353 | 0.002 | 0.005 | - | 29.64 | - |  | 0 | 6840 | - | 0 | yes |
| layered-16384 | wcc | `grust#1` | first | counted | - | 0.623 | 0.010 | 0.015 | - | 6.69 | - | needed | 32 | 1031 | 341578 | 0 | yes |
| layered-16384 | wcc | `grust#1` | second | counted | - | 0.649 | 0.009 | 0.014 | - | 6.69 | - | needed | 28 | 1031 | 341578 | 0 | yes |
| layered-16384 | wcc | `grust#unset` | first | counted | - | 1.428 | 0.014 | 0.009 | - | 6.40 | - | needed | 32 | 1016 | 438267 | 0 | yes |
| layered-16384 | wcc | `grust#unset` | second | counted | - | 1.428 | 0.020 | 0.014 | - | 6.40 | - | needed | 29 | 1016 | 438267 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted#1` | first | counted | - | 0.686 | 0.013 | 0.019 | - | 5.07 | - | needed | 32 | 904 | 341578 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted#1` | second | counted | - | 0.648 | 0.000 | 0.001 | - | 5.07 | - | needed | 13 | 904 | 341578 | 0 | yes |
| layered-16384 | wcc | `grust-next@work-uncounted#1` | first | work-uncounted | - | 0.558 | 0.003 | 0.005 | - | 4.00 | - | needed | 32 | 904 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@work-uncounted#1` | second | work-uncounted | - | 0.526 | 0.000 | 0.001 | - | 4.00 | - | needed | 15 | 904 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@unchecked#1` | first | unchecked | - | 0.503 | 0.008 | 0.016 | - | 3.86 | - | needed | 32 | 904 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@unchecked#1` | second | unchecked | - | 0.465 | 0.002 | 0.004 | - | 3.86 | - | needed | 15 | 904 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@counted#unset` | first | counted | - | 1.409 | 0.003 | 0.002 | - | 5.42 | - | needed | 32 | 888 | 438267 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted#unset` | second | counted | - | 1.393 | 0.003 | 0.002 | - | 5.42 | - | needed | 26 | 888 | 438267 | 0 | yes |
| layered-16384 | wcc | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 0.692 | 0.018 | 0.027 | - | 4.05 | - | needed | 32 | 888 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 0.673 | 0.010 | 0.014 | - | 4.05 | - | needed | 26 | 888 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@unchecked#unset` | first | unchecked | - | 0.621 | 0.002 | 0.004 | - | 3.96 | - | needed | 32 | 888 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@unchecked#unset` | second | unchecked | - | 0.604 | 0.004 | 0.007 | - | 3.96 | - | needed | 27 | 888 | - | 0 | yes |
| layered-16384 | wcc | `grust-next@counted+eager#1` | first | counted | - | 0.667 | 0.005 | 0.008 | - | 5.27 | 0.49 | always | 32 | 1000 | 487973 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted+eager#1` | second | counted | - | 0.675 | 0.015 | 0.023 | - | 5.27 | 0.49 | always | 29 | 1000 | 487973 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted+eager#unset` | first | counted | - | 1.420 | 0.022 | 0.016 | - | 6.11 | 0.68 | always | 32 | 984 | 584662 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted+eager#unset` | second | counted | - | 1.422 | 0.001 | 0.001 | - | 6.11 | 0.68 | always | 28 | 984 | 584662 | 0 | yes |
| layered-65536 | bfs | `icebug` |  |  | - | 2.010 | 0.025 | 0.012 | - | 11.13 | - |  | 132 | 1832 | - | 0 | yes |
| layered-65536 | bfs | `icecat` |  |  | - | 1.553 | 0.010 | 0.006 | - | 6.37 | - |  | 258 | 1637 | - | 0 | yes |
| layered-65536 | bfs | `grustcat` |  |  | - | 1.013 | 0.011 | 0.011 | - | 126.20 | - |  | 0 | 26635 | - | 0 | yes |
| layered-65536 | bfs | `grust#1` | first | counted | - | 1.832 | 0.006 | 0.003 | - | 27.68 | - | needed | 119 | 3142 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust#1` | second | counted | - | 1.570 | 0.002 | 0.002 | - | 27.68 | - | needed | 0 | 3142 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust#unset` | first | counted | - | 1.840 | 0.017 | 0.009 | - | 27.85 | - | needed | 119 | 3127 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust#unset` | second | counted | - | 1.573 | 0.004 | 0.003 | - | 27.85 | - | needed | 0 | 3127 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted#1` | first | counted | - | 1.794 | 0.011 | 0.006 | - | 20.77 | - | needed | 103 | 2631 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted#1` | second | counted | - | 1.548 | 0.001 | 0.001 | - | 20.77 | - | needed | 0 | 2631 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@work-uncounted#1` | first | work-uncounted | - | 1.436 | 0.017 | 0.012 | - | 17.39 | - | needed | 103 | 2631 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@work-uncounted#1` | second | work-uncounted | - | 1.184 | 0.008 | 0.007 | - | 17.39 | - | needed | 0 | 2631 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@unchecked#1` | first | unchecked | - | 1.273 | 0.005 | 0.004 | - | 17.15 | - | needed | 103 | 2631 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@unchecked#1` | second | unchecked | - | 1.039 | 0.014 | 0.014 | - | 17.15 | - | needed | 0 | 2631 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@counted#unset` | first | counted | - | 1.822 | 0.009 | 0.005 | - | 23.93 | - | needed | 119 | 3078 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted#unset` | second | counted | - | 1.558 | 0.010 | 0.007 | - | 23.93 | - | needed | 0 | 3078 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 1.447 | 0.006 | 0.004 | - | 18.09 | - | needed | 119 | 2567 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 1.207 | 0.009 | 0.008 | - | 18.09 | - | needed | 0 | 2567 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@unchecked#unset` | first | unchecked | - | 1.307 | 0.008 | 0.006 | - | 17.69 | - | needed | 119 | 2567 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@unchecked#unset` | second | unchecked | - | 1.021 | 0.002 | 0.002 | - | 17.69 | - | needed | 0 | 2567 | - | 0 | yes |
| layered-65536 | bfs | `grust-next@counted+eager#1` | first | counted | - | 1.781 | 0.014 | 0.008 | - | 22.97 | 2.16 | always | 103 | 3013 | 1979713 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted+eager#1` | second | counted | - | 1.574 | 0.005 | 0.003 | - | 22.97 | 2.16 | always | 0 | 3013 | 1979713 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted+eager#unset` | first | counted | - | 2.036 | 0.004 | 0.002 | - | 26.64 | 3.00 | always | 231 | 2949 | 1979713 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted+eager#unset` | second | counted | - | 1.576 | 0.004 | 0.002 | - | 26.64 | 3.00 | always | 0 | 2949 | 1979713 | 0 | yes |
| layered-65536 | pagerank | `icebug` |  |  | 60 | 91.821 | 0.199 | 0.002 | 1.530 | 11.19 | - |  | 401 | 1832 | - | 0 | yes |
| layered-65536 | pagerank | `icecat` |  |  | 75 | 102.060 | 0.190 | 0.002 | 1.361 | 6.44 | - |  | 607 | 1636 | - | 0 | yes |
| layered-65536 | pagerank | `grustcat` |  |  | 75 | 94.260 | 0.188 | 0.002 | 1.257 | 128.61 | - |  | 0 | 26634 | - | 0 | yes |
| layered-65536 | pagerank | `grust#1` | first | counted | 75 | 108.548 | 0.049 | 0.000 | 1.447 | 28.12 | - | needed | 766 | 3142 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust#1` | second | counted | 75 | 104.830 | 0.082 | 0.001 | 1.398 | 28.12 | - | needed | 0 | 3142 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust#unset` | first | counted | 75 | 414.370 | 0.648 | 0.002 | 5.525 | 28.04 | - | needed | 512 | 3127 | 31164642 | 0 | yes |
| layered-65536 | pagerank | `grust#unset` | second | counted | 75 | 412.827 | 0.094 | 0.000 | 5.504 | 28.04 | - | needed | 128 | 3127 | 31164642 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted#1` | first | counted | 75 | 111.185 | 0.094 | 0.001 | 1.482 | 24.09 | 2.19 | needed | 384 | 3523 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted#1` | second | counted | 75 | 110.151 | 0.124 | 0.001 | 1.469 | 24.09 | 2.19 | needed | 0 | 3523 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 75 | 102.694 | 0.041 | 0.000 | 1.369 | 19.15 | 1.54 | needed | 384 | 3013 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 75 | 101.916 | 0.032 | 0.000 | 1.359 | 19.15 | 1.54 | needed | 0 | 3013 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@unchecked#1` | first | unchecked | 75 | 100.955 | 0.228 | 0.002 | 1.346 | 18.93 | 1.44 | needed | 384 | 3012 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@unchecked#1` | second | unchecked | 75 | 100.081 | 0.129 | 0.001 | 1.334 | 18.93 | 1.44 | needed | 0 | 3012 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted#unset` | first | counted | 75 | 318.683 | 0.090 | 0.000 | 4.249 | 23.32 | - | needed | 512 | 2567 | 31164642 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted#unset` | second | counted | 75 | 317.913 | 0.151 | 0.000 | 4.239 | 23.32 | - | needed | 128 | 2567 | 31164642 | 0 | yes |
| layered-65536 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 75 | 158.881 | 0.386 | 0.002 | 2.118 | 18.07 | - | needed | 512 | 2567 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 75 | 157.805 | 0.168 | 0.001 | 2.104 | 18.07 | - | needed | 128 | 2567 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 75 | 150.978 | 0.117 | 0.001 | 2.013 | 17.90 | - | needed | 512 | 2567 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 75 | 150.173 | 0.094 | 0.001 | 2.002 | 17.90 | - | needed | 128 | 2567 | - | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted+eager#1` | first | counted | 75 | 110.998 | 0.021 | 0.000 | 1.480 | 22.97 | 2.17 | always | 384 | 3013 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted+eager#1` | second | counted | 75 | 110.182 | 0.186 | 0.002 | 1.469 | 22.97 | 2.17 | always | 0 | 3013 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted+eager#unset` | first | counted | 75 | 318.634 | 0.496 | 0.002 | 4.248 | 26.86 | 2.99 | always | 512 | 2949 | 31750996 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted+eager#unset` | second | counted | 75 | 317.548 | 0.224 | 0.001 | 4.234 | 26.86 | 2.99 | always | 128 | 2949 | 31750996 | 0 | yes |
| layered-65536 | triangles | `neo4j-graph` |  |  | - | 2.746 | 0.001 | 0.000 | - | 8.11 | - |  | 3 | 1650 | - | 1 | yes |
| layered-65536 | triangles | `grust#1` | first | counted | - | 11.467 | 0.048 | 0.004 | - | 29.34 | - | needed | 1401 | 3650 | 2877576 | 1 | yes |
| layered-65536 | triangles | `grust#1` | second | counted | - | 8.791 | 0.012 | 0.001 | - | 29.34 | - | needed | 128 | 3650 | 2877576 | 1 | yes |
| layered-65536 | triangles | `grust#unset` | first | counted | - | 11.406 | 0.008 | 0.001 | - | 29.53 | - | needed | 1401 | 3635 | 2877576 | 1 | yes |
| layered-65536 | triangles | `grust#unset` | second | counted | - | 8.784 | 0.005 | 0.001 | - | 29.53 | - | needed | 128 | 3635 | 2877576 | 1 | yes |
| layered-65536 | triangles | `grust-next@counted#1` | first | counted | - | 11.170 | 0.024 | 0.002 | - | 22.39 | - | needed | 1402 | 3140 | 2877576 | 1 | yes |
| layered-65536 | triangles | `grust-next@counted#1` | second | counted | - | 10.439 | 0.036 | 0.003 | - | 22.39 | - | needed | 1497 | 3140 | 2877576 | 1 | yes |
| layered-65536 | triangles | `grust-next@work-uncounted#1` | first | work-uncounted | - | 10.586 | 0.013 | 0.001 | - | 19.35 | - | needed | 1402 | 3140 | - | 1 | yes |
| layered-65536 | triangles | `grust-next@work-uncounted#1` | second | work-uncounted | - | 9.865 | 0.020 | 0.002 | - | 19.35 | - | needed | 1497 | 3140 | - | 1 | yes |
| layered-65536 | triangles | `grust-next@unchecked#1` | first | unchecked | - | 10.197 | 0.006 | 0.001 | - | 18.94 | - | needed | 1402 | 3140 | - | 1 | yes |
| layered-65536 | triangles | `grust-next@unchecked#1` | second | unchecked | - | 9.487 | 0.009 | 0.001 | - | 18.94 | - | needed | 1497 | 3140 | - | 1 | yes |
| layered-65536 | triangles | `grust-next@counted#unset` | first | counted | - | 11.141 | 0.040 | 0.004 | - | 25.25 | - | needed | 1402 | 3076 | 2877576 | 1 | yes |
| layered-65536 | triangles | `grust-next@counted#unset` | second | counted | - | 9.179 | 0.010 | 0.001 | - | 25.25 | - | needed | 635 | 3076 | 2877576 | 1 | yes |
| layered-65536 | triangles | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 10.564 | 0.024 | 0.002 | - | 19.73 | - | needed | 1402 | 3076 | - | 1 | yes |
| layered-65536 | triangles | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 8.604 | 0.018 | 0.002 | - | 19.73 | - | needed | 635 | 3076 | - | 1 | yes |
| layered-65536 | triangles | `grust-next@unchecked#unset` | first | unchecked | - | 10.197 | 0.020 | 0.002 | - | 19.31 | - | needed | 1402 | 3076 | - | 1 | yes |
| layered-65536 | triangles | `grust-next@unchecked#unset` | second | unchecked | - | 8.217 | 0.010 | 0.001 | - | 19.31 | - | needed | 635 | 3076 | - | 1 | yes |
| layered-65536 | triangles | `grust-next@counted+eager#1` | first | counted | - | 11.146 | 0.007 | 0.001 | - | 21.69 | 0.00 | always | 1402 | 2629 | 2877576 | 1 | yes |
| layered-65536 | triangles | `grust-next@counted+eager#1` | second | counted | - | 10.467 | 0.025 | 0.002 | - | 21.69 | 0.00 | always | 1497 | 2629 | 2877576 | 1 | yes |
| layered-65536 | triangles | `grust-next@counted+eager#unset` | first | counted | - | 11.147 | 0.014 | 0.001 | - | 25.31 | 0.00 | always | 1402 | 3076 | 2877576 | 1 | yes |
| layered-65536 | triangles | `grust-next@counted+eager#unset` | second | counted | - | 9.155 | 0.020 | 0.002 | - | 25.31 | 0.00 | always | 635 | 3076 | 2877576 | 1 | yes |
| layered-65536 | wcc | `neo4j-graph` |  |  | - | 3.461 | 0.001 | 0.000 | - | 8.04 | - |  | 32 | 1650 | - | 0 | yes |
| layered-65536 | wcc | `icebug` |  |  | - | 3.765 | 0.026 | 0.007 | - | 11.04 | - |  | 138 | 1832 | - | 0 | yes |
| layered-65536 | wcc | `icecat` |  |  | - | 1.993 | 0.011 | 0.005 | - | 6.70 | - |  | 256 | 2146 | - | 0 | yes |
| layered-65536 | wcc | `grustcat` |  |  | - | 1.413 | 0.008 | 0.005 | - | 127.23 | - |  | 0 | 26634 | - | 0 | yes |
| layered-65536 | wcc | `grust#1` | first | counted | - | 2.503 | 0.008 | 0.003 | - | 28.80 | - | needed | 128 | 3143 | 1368146 | 0 | yes |
| layered-65536 | wcc | `grust#1` | second | counted | - | 2.628 | 0.003 | 0.001 | - | 28.80 | - | needed | 123 | 3143 | 1368146 | 0 | yes |
| layered-65536 | wcc | `grust#unset` | first | counted | - | 5.744 | 0.011 | 0.002 | - | 28.08 | - | needed | 128 | 3127 | 1755282 | 0 | yes |
| layered-65536 | wcc | `grust#unset` | second | counted | - | 5.725 | 0.014 | 0.002 | - | 28.08 | - | needed | 121 | 3127 | 1755282 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted#1` | first | counted | - | 2.777 | 0.002 | 0.001 | - | 20.77 | - | needed | 128 | 2631 | 1368146 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted#1` | second | counted | - | 2.626 | 0.006 | 0.002 | - | 20.77 | - | needed | 61 | 2631 | 1368146 | 0 | yes |
| layered-65536 | wcc | `grust-next@work-uncounted#1` | first | work-uncounted | - | 2.321 | 0.008 | 0.003 | - | 17.11 | - | needed | 128 | 2630 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@work-uncounted#1` | second | work-uncounted | - | 2.165 | 0.012 | 0.006 | - | 17.11 | - | needed | 61 | 2630 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@unchecked#1` | first | unchecked | - | 2.059 | 0.006 | 0.003 | - | 17.25 | - | needed | 128 | 2631 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@unchecked#1` | second | unchecked | - | 1.911 | 0.005 | 0.003 | - | 17.25 | - | needed | 60 | 2631 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@counted#unset` | first | counted | - | 5.716 | 0.004 | 0.001 | - | 23.21 | - | needed | 128 | 2567 | 1755282 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted#unset` | second | counted | - | 5.699 | 0.002 | 0.000 | - | 23.21 | - | needed | 120 | 2567 | 1755282 | 0 | yes |
| layered-65536 | wcc | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 2.782 | 0.006 | 0.002 | - | 17.91 | - | needed | 128 | 2567 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 2.777 | 0.019 | 0.007 | - | 17.91 | - | needed | 121 | 2567 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@unchecked#unset` | first | unchecked | - | 2.516 | 0.011 | 0.004 | - | 17.61 | - | needed | 128 | 2567 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@unchecked#unset` | second | unchecked | - | 2.508 | 0.012 | 0.005 | - | 17.61 | - | needed | 121 | 2567 | - | 0 | yes |
| layered-65536 | wcc | `grust-next@counted+eager#1` | first | counted | - | 2.762 | 0.019 | 0.007 | - | 23.22 | 2.18 | always | 128 | 3013 | 1954500 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted+eager#1` | second | counted | - | 2.758 | 0.004 | 0.002 | - | 23.22 | 2.18 | always | 122 | 3013 | 1954500 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted+eager#unset` | first | counted | - | 5.720 | 0.001 | 0.000 | - | 26.32 | 2.98 | always | 128 | 2949 | 2341636 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted+eager#unset` | second | counted | - | 5.699 | 0.005 | 0.001 | - | 26.32 | 2.98 | always | 120 | 2949 | 2341636 | 0 | yes |
| path-16384 | bfs | `icebug` |  |  | - | 0.247 | 0.003 | 0.011 | - | 1.75 | - |  | 36 | 450 | - | 0 | yes |
| path-16384 | bfs | `icecat` |  |  | - | 0.280 | 0.004 | 0.014 | - | 0.80 | - |  | 65 | 275 | - | 0 | yes |
| path-16384 | bfs | `grustcat` |  |  | - | 0.143 | 0.002 | 0.011 | - | 23.90 | - |  | 0 | 6429 | - | 0 | yes |
| path-16384 | bfs | `grust#1` | first | counted | - | 0.419 | 0.005 | 0.012 | - | 4.98 | - | needed | 36 | 741 | 245755 | 0 | yes |
| path-16384 | bfs | `grust#1` | second | counted | - | 0.339 | 0.000 | 0.000 | - | 4.98 | - | needed | 0 | 741 | 245755 | 0 | yes |
| path-16384 | bfs | `grust#unset` | first | counted | - | 0.410 | 0.009 | 0.022 | - | 4.73 | - | needed | 37 | 726 | 245755 | 0 | yes |
| path-16384 | bfs | `grust#unset` | second | counted | - | 0.339 | 0.000 | 0.001 | - | 4.73 | - | needed | 0 | 726 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@counted#1` | first | counted | - | 0.380 | 0.005 | 0.013 | - | 4.02 | - | needed | 32 | 686 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@counted#1` | second | counted | - | 0.326 | 0.000 | 0.001 | - | 4.02 | - | needed | 0 | 686 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@work-uncounted#1` | first | work-uncounted | - | 0.206 | 0.004 | 0.021 | - | 3.33 | - | needed | 32 | 686 | - | 0 | yes |
| path-16384 | bfs | `grust-next@work-uncounted#1` | second | work-uncounted | - | 0.150 | 0.000 | 0.001 | - | 3.33 | - | needed | 0 | 686 | - | 0 | yes |
| path-16384 | bfs | `grust-next@unchecked#1` | first | unchecked | - | 0.168 | 0.000 | 0.001 | - | 3.27 | - | needed | 32 | 686 | - | 0 | yes |
| path-16384 | bfs | `grust-next@unchecked#1` | second | unchecked | - | 0.117 | 0.000 | 0.003 | - | 3.27 | - | needed | 0 | 686 | - | 0 | yes |
| path-16384 | bfs | `grust-next@counted#unset` | first | counted | - | 0.384 | 0.002 | 0.005 | - | 4.34 | - | needed | 36 | 670 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@counted#unset` | second | counted | - | 0.326 | 0.000 | 0.001 | - | 4.34 | - | needed | 0 | 670 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 0.207 | 0.000 | 0.002 | - | 3.36 | - | needed | 36 | 670 | - | 0 | yes |
| path-16384 | bfs | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 0.150 | 0.000 | 0.001 | - | 3.36 | - | needed | 0 | 670 | - | 0 | yes |
| path-16384 | bfs | `grust-next@unchecked#unset` | first | unchecked | - | 0.169 | 0.001 | 0.005 | - | 3.32 | - | needed | 36 | 671 | - | 0 | yes |
| path-16384 | bfs | `grust-next@unchecked#unset` | second | unchecked | - | 0.111 | 0.000 | 0.002 | - | 3.32 | - | needed | 0 | 671 | - | 0 | yes |
| path-16384 | bfs | `grust-next@counted+eager#1` | first | counted | - | 0.375 | 0.001 | 0.004 | - | 4.39 | 0.41 | always | 32 | 750 | 344057 | 0 | yes |
| path-16384 | bfs | `grust-next@counted+eager#1` | second | counted | - | 0.326 | 0.000 | 0.000 | - | 4.39 | 0.41 | always | 0 | 750 | 344057 | 0 | yes |
| path-16384 | bfs | `grust-next@counted+eager#unset` | first | counted | - | 0.460 | 0.002 | 0.004 | - | 4.90 | 0.60 | always | 64 | 734 | 344057 | 0 | yes |
| path-16384 | bfs | `grust-next@counted+eager#unset` | second | counted | - | 0.326 | 0.000 | 0.001 | - | 4.90 | 0.60 | always | 0 | 734 | 344057 | 0 | yes |
| path-16384 | pagerank | `icebug` |  |  | 54 | 12.865 | 0.156 | 0.012 | 0.238 | 1.76 | - |  | 113 | 450 | - | 0 | yes |
| path-16384 | pagerank | `icecat` |  |  | 58 | 11.147 | 0.005 | 0.000 | 0.192 | 0.83 | - |  | 129 | 275 | - | 0 | yes |
| path-16384 | pagerank | `grustcat` |  |  | 58 | 9.967 | 0.164 | 0.016 | 0.172 | 24.20 | - |  | 0 | 6430 | - | 0 | yes |
| path-16384 | pagerank | `grust#1` | first | counted | 58 | 15.377 | 0.068 | 0.004 | 0.265 | 5.05 | - | needed | 160 | 741 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust#1` | second | counted | 58 | 14.608 | 0.034 | 0.002 | 0.252 | 5.05 | - | needed | 0 | 741 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust#unset` | first | counted | 58 | 66.511 | 0.038 | 0.001 | 1.147 | 4.73 | - | needed | 128 | 726 | 5062591 | 0 | yes |
| path-16384 | pagerank | `grust#unset` | second | counted | 58 | 66.308 | 0.011 | 0.000 | 1.143 | 4.73 | - | needed | 32 | 726 | 5062591 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted#1` | first | counted | 58 | 14.718 | 0.034 | 0.002 | 0.254 | 4.87 | 0.44 | needed | 96 | 750 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted#1` | second | counted | 58 | 14.603 | 0.022 | 0.001 | 0.252 | 4.87 | 0.44 | needed | 64 | 750 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 58 | 12.063 | 0.020 | 0.002 | 0.208 | 3.74 | 0.26 | needed | 96 | 750 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 58 | 11.963 | 0.025 | 0.002 | 0.206 | 3.74 | 0.26 | needed | 64 | 750 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@unchecked#1` | first | unchecked | 58 | 11.469 | 0.045 | 0.004 | 0.198 | 3.94 | 0.25 | needed | 96 | 750 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@unchecked#1` | second | unchecked | 58 | 11.388 | 0.002 | 0.000 | 0.196 | 3.94 | 0.25 | needed | 64 | 750 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@counted#unset` | first | counted | 58 | 60.320 | 0.133 | 0.002 | 1.040 | 4.29 | - | needed | 128 | 670 | 5062591 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted#unset` | second | counted | 58 | 60.178 | 0.113 | 0.002 | 1.038 | 4.29 | - | needed | 32 | 670 | 5062591 | 0 | yes |
| path-16384 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 58 | 28.999 | 0.037 | 0.001 | 0.500 | 3.38 | - | needed | 128 | 670 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 58 | 28.825 | 0.025 | 0.001 | 0.497 | 3.38 | - | needed | 32 | 670 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 58 | 27.016 | 0.044 | 0.002 | 0.466 | 3.30 | - | needed | 128 | 670 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 58 | 26.896 | 0.014 | 0.001 | 0.464 | 3.30 | - | needed | 32 | 670 | - | 0 | yes |
| path-16384 | pagerank | `grust-next@counted+eager#1` | first | counted | 58 | 14.661 | 0.006 | 0.000 | 0.253 | 4.38 | 0.41 | always | 96 | 750 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted+eager#1` | second | counted | 58 | 14.617 | 0.006 | 0.000 | 0.252 | 4.38 | 0.41 | always | 64 | 750 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted+eager#unset` | first | counted | 58 | 60.412 | 0.006 | 0.000 | 1.042 | 5.14 | 0.63 | always | 128 | 734 | 5160893 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted+eager#unset` | second | counted | 58 | 60.229 | 0.019 | 0.000 | 1.038 | 5.14 | 0.63 | always | 32 | 734 | 5160893 | 0 | yes |
| path-16384 | triangles | `neo4j-graph` |  |  | - | 0.252 | 0.009 | 0.037 | - | 1.43 | - |  | 3 | 316 | - | 0 | yes |
| path-16384 | triangles | `grust#1` | first | counted | - | 1.520 | 0.096 | 0.063 | - | 5.11 | - | needed | 256 | 805 | 425970 | 0 | yes |
| path-16384 | triangles | `grust#1` | second | counted | - | 1.085 | 0.038 | 0.035 | - | 5.11 | - | needed | 32 | 805 | 425970 | 0 | yes |
| path-16384 | triangles | `grust#unset` | first | counted | - | 1.461 | 0.051 | 0.035 | - | 5.07 | - | needed | 256 | 790 | 425970 | 0 | yes |
| path-16384 | triangles | `grust#unset` | second | counted | - | 1.231 | 0.013 | 0.010 | - | 5.07 | - | needed | 32 | 790 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted#1` | first | counted | - | 1.561 | 0.045 | 0.029 | - | 4.46 | - | needed | 256 | 750 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted#1` | second | counted | - | 1.391 | 0.020 | 0.014 | - | 4.46 | - | needed | 256 | 750 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@work-uncounted#1` | first | work-uncounted | - | 1.233 | 0.021 | 0.017 | - | 3.55 | - | needed | 256 | 750 | - | 0 | yes |
| path-16384 | triangles | `grust-next@work-uncounted#1` | second | work-uncounted | - | 1.169 | 0.019 | 0.016 | - | 3.55 | - | needed | 256 | 750 | - | 0 | yes |
| path-16384 | triangles | `grust-next@unchecked#1` | first | unchecked | - | 1.158 | 0.019 | 0.017 | - | 3.45 | - | needed | 256 | 750 | - | 0 | yes |
| path-16384 | triangles | `grust-next@unchecked#1` | second | unchecked | - | 1.090 | 0.000 | 0.000 | - | 3.45 | - | needed | 256 | 750 | - | 0 | yes |
| path-16384 | triangles | `grust-next@counted#unset` | first | counted | - | 1.430 | 0.020 | 0.014 | - | 4.53 | - | needed | 256 | 734 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted#unset` | second | counted | - | 1.162 | 0.011 | 0.010 | - | 4.53 | - | needed | 96 | 734 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 1.210 | 0.011 | 0.009 | - | 3.55 | - | needed | 256 | 734 | - | 0 | yes |
| path-16384 | triangles | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 0.943 | 0.008 | 0.008 | - | 3.55 | - | needed | 96 | 734 | - | 0 | yes |
| path-16384 | triangles | `grust-next@unchecked#unset` | first | unchecked | - | 1.135 | 0.014 | 0.012 | - | 3.48 | - | needed | 256 | 735 | - | 0 | yes |
| path-16384 | triangles | `grust-next@unchecked#unset` | second | unchecked | - | 0.873 | 0.003 | 0.003 | - | 3.48 | - | needed | 96 | 735 | - | 0 | yes |
| path-16384 | triangles | `grust-next@counted+eager#1` | first | counted | - | 1.418 | 0.005 | 0.003 | - | 4.19 | 0.00 | always | 256 | 750 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted+eager#1` | second | counted | - | 1.399 | 0.031 | 0.022 | - | 4.19 | 0.00 | always | 256 | 750 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted+eager#unset` | first | counted | - | 1.431 | 0.009 | 0.006 | - | 4.50 | 0.00 | always | 256 | 734 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted+eager#unset` | second | counted | - | 1.156 | 0.003 | 0.002 | - | 4.50 | 0.00 | always | 96 | 734 | 425970 | 0 | yes |
| path-16384 | wcc | `neo4j-graph` |  |  | - | 0.764 | 0.003 | 0.003 | - | 1.41 | - |  | 31 | 316 | - | 0 | yes |
| path-16384 | wcc | `icebug` |  |  | - | 0.339 | 0.006 | 0.019 | - | 1.78 | - |  | 41 | 450 | - | 0 | yes |
| path-16384 | wcc | `icecat` |  |  | - | 0.273 | 0.000 | 0.001 | - | 0.80 | - |  | 64 | 275 | - | 0 | yes |
| path-16384 | wcc | `grustcat` |  |  | - | 0.158 | 0.000 | 0.003 | - | 24.43 | - |  | 0 | 6429 | - | 0 | yes |
| path-16384 | wcc | `grust#1` | first | counted | - | 0.429 | 0.005 | 0.012 | - | 4.85 | - | needed | 32 | 741 | 229369 | 0 | yes |
| path-16384 | wcc | `grust#1` | second | counted | - | 0.440 | 0.009 | 0.020 | - | 4.85 | - | needed | 32 | 741 | 229369 | 0 | yes |
| path-16384 | wcc | `grust#unset` | first | counted | - | 0.993 | 0.012 | 0.012 | - | 5.09 | - | needed | 32 | 726 | 294903 | 0 | yes |
| path-16384 | wcc | `grust#unset` | second | counted | - | 0.993 | 0.016 | 0.016 | - | 5.09 | - | needed | 30 | 726 | 294903 | 0 | yes |
| path-16384 | wcc | `grust-next@counted#1` | first | counted | - | 0.447 | 0.012 | 0.026 | - | 4.37 | - | needed | 32 | 686 | 229369 | 0 | yes |
| path-16384 | wcc | `grust-next@counted#1` | second | counted | - | 0.405 | 0.001 | 0.003 | - | 4.37 | - | needed | 16 | 686 | 229369 | 0 | yes |
| path-16384 | wcc | `grust-next@work-uncounted#1` | first | work-uncounted | - | 0.296 | 0.001 | 0.005 | - | 3.36 | - | needed | 32 | 686 | - | 0 | yes |
| path-16384 | wcc | `grust-next@work-uncounted#1` | second | work-uncounted | - | 0.271 | 0.001 | 0.004 | - | 3.36 | - | needed | 16 | 686 | - | 0 | yes |
| path-16384 | wcc | `grust-next@unchecked#1` | first | unchecked | - | 0.300 | 0.005 | 0.016 | - | 3.52 | - | needed | 32 | 686 | - | 0 | yes |
| path-16384 | wcc | `grust-next@unchecked#1` | second | unchecked | - | 0.260 | 0.002 | 0.006 | - | 3.52 | - | needed | 16 | 686 | - | 0 | yes |
| path-16384 | wcc | `grust-next@counted#unset` | first | counted | - | 0.966 | 0.001 | 0.001 | - | 4.34 | - | needed | 32 | 670 | 294903 | 0 | yes |
| path-16384 | wcc | `grust-next@counted#unset` | second | counted | - | 1.003 | 0.010 | 0.010 | - | 4.34 | - | needed | 48 | 670 | 294903 | 0 | yes |
| path-16384 | wcc | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 0.372 | 0.009 | 0.024 | - | 3.40 | - | needed | 32 | 670 | - | 0 | yes |
| path-16384 | wcc | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 0.398 | 0.013 | 0.033 | - | 3.40 | - | needed | 48 | 670 | - | 0 | yes |
| path-16384 | wcc | `grust-next@unchecked#unset` | first | unchecked | - | 0.328 | 0.001 | 0.004 | - | 3.34 | - | needed | 32 | 670 | - | 0 | yes |
| path-16384 | wcc | `grust-next@unchecked#unset` | second | unchecked | - | 0.349 | 0.002 | 0.007 | - | 3.34 | - | needed | 48 | 670 | - | 0 | yes |
| path-16384 | wcc | `grust-next@counted+eager#1` | first | counted | - | 0.439 | 0.007 | 0.015 | - | 4.41 | 0.40 | always | 32 | 750 | 327671 | 0 | yes |
| path-16384 | wcc | `grust-next@counted+eager#1` | second | counted | - | 0.441 | 0.004 | 0.009 | - | 4.41 | 0.40 | always | 32 | 750 | 327671 | 0 | yes |
| path-16384 | wcc | `grust-next@counted+eager#unset` | first | counted | - | 0.985 | 0.001 | 0.001 | - | 4.93 | 0.62 | always | 32 | 734 | 393205 | 0 | yes |
| path-16384 | wcc | `grust-next@counted+eager#unset` | second | counted | - | 1.010 | 0.018 | 0.018 | - | 4.93 | 0.62 | always | 48 | 734 | 393205 | 0 | yes |
| path-65536 | bfs | `icebug` |  |  | - | 0.946 | 0.011 | 0.012 | - | 6.90 | - |  | 132 | 1795 | - | 0 | yes |
| path-65536 | bfs | `icecat` |  |  | - | 1.121 | 0.002 | 0.002 | - | 4.16 | - |  | 256 | 1138 | - | 0 | yes |
| path-65536 | bfs | `grustcat` |  |  | - | 0.565 | 0.001 | 0.001 | - | 103.05 | - |  | 0 | 24215 | - | 0 | yes |
| path-65536 | bfs | `grust#1` | first | counted | - | 1.677 | 0.015 | 0.009 | - | 21.06 | - | needed | 144 | 2997 | 983035 | 0 | yes |
| path-65536 | bfs | `grust#1` | second | counted | - | 1.359 | 0.002 | 0.002 | - | 21.06 | - | needed | 0 | 2997 | 983035 | 0 | yes |
| path-65536 | bfs | `grust#unset` | first | counted | - | 1.677 | 0.012 | 0.007 | - | 20.88 | - | needed | 144 | 2471 | 983035 | 0 | yes |
| path-65536 | bfs | `grust#unset` | second | counted | - | 1.381 | 0.011 | 0.008 | - | 20.88 | - | needed | 0 | 2471 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@counted#1` | first | counted | - | 1.581 | 0.026 | 0.017 | - | 17.96 | - | needed | 128 | 2264 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@counted#1` | second | counted | - | 1.303 | 0.000 | 0.000 | - | 17.96 | - | needed | 0 | 2264 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@work-uncounted#1` | first | work-uncounted | - | 0.881 | 0.008 | 0.009 | - | 15.45 | - | needed | 128 | 2263 | - | 0 | yes |
| path-65536 | bfs | `grust-next@work-uncounted#1` | second | work-uncounted | - | 0.604 | 0.002 | 0.004 | - | 15.45 | - | needed | 0 | 2263 | - | 0 | yes |
| path-65536 | bfs | `grust-next@unchecked#1` | first | unchecked | - | 0.738 | 0.008 | 0.011 | - | 14.27 | - | needed | 128 | 2263 | - | 0 | yes |
| path-65536 | bfs | `grust-next@unchecked#1` | second | unchecked | - | 0.470 | 0.000 | 0.001 | - | 14.27 | - | needed | 0 | 2263 | - | 0 | yes |
| path-65536 | bfs | `grust-next@counted#unset` | first | counted | - | 1.636 | 0.006 | 0.004 | - | 19.30 | - | needed | 144 | 2199 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@counted#unset` | second | counted | - | 1.303 | 0.000 | 0.000 | - | 19.30 | - | needed | 0 | 2199 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 0.882 | 0.002 | 0.003 | - | 14.48 | - | needed | 144 | 2199 | - | 0 | yes |
| path-65536 | bfs | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 0.600 | 0.000 | 0.001 | - | 14.48 | - | needed | 0 | 2199 | - | 0 | yes |
| path-65536 | bfs | `grust-next@unchecked#unset` | first | unchecked | - | 0.773 | 0.018 | 0.023 | - | 14.82 | - | needed | 144 | 2199 | - | 0 | yes |
| path-65536 | bfs | `grust-next@unchecked#unset` | second | unchecked | - | 0.453 | 0.001 | 0.001 | - | 14.82 | - | needed | 0 | 2199 | - | 0 | yes |
| path-65536 | bfs | `grust-next@counted+eager#1` | first | counted | - | 1.573 | 0.002 | 0.002 | - | 19.37 | 1.76 | always | 128 | 2519 | 1376249 | 0 | yes |
| path-65536 | bfs | `grust-next@counted+eager#1` | second | counted | - | 1.305 | 0.001 | 0.000 | - | 19.37 | 1.76 | always | 0 | 2519 | 1376249 | 0 | yes |
| path-65536 | bfs | `grust-next@counted+eager#unset` | first | counted | - | 1.840 | 0.009 | 0.005 | - | 21.79 | 2.52 | always | 256 | 2455 | 1376249 | 0 | yes |
| path-65536 | bfs | `grust-next@counted+eager#unset` | second | counted | - | 1.306 | 0.001 | 0.001 | - | 21.79 | 2.52 | always | 0 | 2455 | 1376249 | 0 | yes |
| path-65536 | pagerank | `icebug` |  |  | 46 | 42.969 | 0.019 | 0.000 | 0.934 | 7.02 | - |  | 401 | 1795 | - | 0 | yes |
| path-65536 | pagerank | `icecat` |  |  | 50 | 39.038 | 0.058 | 0.001 | 0.781 | 4.28 | - |  | 606 | 1139 | - | 0 | yes |
| path-65536 | pagerank | `grustcat` |  |  | 50 | 34.375 | 0.263 | 0.008 | 0.688 | 102.72 | - |  | 0 | 24215 | - | 0 | yes |
| path-65536 | pagerank | `grust#1` | first | counted | 50 | 54.122 | 0.081 | 0.001 | 1.082 | 21.08 | - | needed | 640 | 2486 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust#1` | second | counted | 50 | 51.005 | 0.102 | 0.002 | 1.020 | 21.08 | - | needed | 0 | 2486 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust#unset` | first | counted | 50 | 230.708 | 0.185 | 0.001 | 4.614 | 21.25 | - | needed | 512 | 2471 | 17629127 | 0 | yes |
| path-65536 | pagerank | `grust#unset` | second | counted | 50 | 229.680 | 0.089 | 0.000 | 4.594 | 21.25 | - | needed | 128 | 2471 | 17629127 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted#1` | first | counted | 50 | 52.145 | 0.223 | 0.004 | 1.043 | 19.49 | 1.79 | needed | 384 | 2519 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted#1` | second | counted | 50 | 51.758 | 0.108 | 0.002 | 1.035 | 19.49 | 1.79 | needed | 352 | 2519 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 50 | 42.730 | 0.077 | 0.002 | 0.855 | 16.18 | 1.13 | needed | 384 | 2519 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 50 | 42.441 | 0.046 | 0.001 | 0.849 | 16.18 | 1.13 | needed | 352 | 2519 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@unchecked#1` | first | unchecked | 50 | 40.624 | 0.071 | 0.002 | 0.812 | 16.06 | 1.04 | needed | 384 | 2519 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@unchecked#1` | second | unchecked | 50 | 40.365 | 0.119 | 0.003 | 0.807 | 16.06 | 1.04 | needed | 352 | 2519 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@counted#unset` | first | counted | 50 | 210.256 | 0.687 | 0.003 | 4.205 | 19.14 | - | needed | 512 | 2199 | 17629127 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted#unset` | second | counted | 50 | 208.672 | 0.183 | 0.001 | 4.173 | 19.14 | - | needed | 128 | 2199 | 17629127 | 0 | yes |
| path-65536 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 50 | 100.111 | 0.304 | 0.003 | 2.002 | 15.57 | - | needed | 512 | 2200 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 50 | 99.222 | 0.259 | 0.003 | 1.984 | 15.57 | - | needed | 128 | 2200 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 50 | 94.445 | 0.199 | 0.002 | 1.889 | 15.04 | - | needed | 512 | 2199 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 50 | 93.257 | 0.036 | 0.000 | 1.865 | 15.04 | - | needed | 128 | 2199 | - | 0 | yes |
| path-65536 | pagerank | `grust-next@counted+eager#1` | first | counted | 50 | 52.000 | 0.070 | 0.001 | 1.040 | 19.54 | 1.80 | always | 384 | 2519 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted+eager#1` | second | counted | 50 | 51.697 | 0.029 | 0.001 | 1.034 | 19.54 | 1.80 | always | 352 | 2519 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted+eager#unset` | first | counted | 50 | 209.902 | 0.083 | 0.000 | 4.198 | 21.33 | 2.49 | always | 512 | 2455 | 18022341 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted+eager#unset` | second | counted | 50 | 208.895 | 0.322 | 0.002 | 4.178 | 21.33 | 2.49 | always | 128 | 2455 | 18022341 | 0 | yes |
| path-65536 | triangles | `neo4j-graph` |  |  | - | 0.644 | 0.012 | 0.018 | - | 5.12 | - |  | 3 | 1277 | - | 0 | yes |
| path-65536 | triangles | `grust#1` | first | counted | - | 6.138 | 0.029 | 0.005 | - | 21.62 | - | needed | 1024 | 2742 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust#1` | second | counted | - | 4.320 | 0.007 | 0.002 | - | 21.62 | - | needed | 128 | 2742 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust#unset` | first | counted | - | 6.175 | 0.030 | 0.005 | - | 21.81 | - | needed | 1024 | 2727 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust#unset` | second | counted | - | 4.994 | 0.013 | 0.003 | - | 21.81 | - | needed | 128 | 2727 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted#1` | first | counted | - | 6.175 | 0.017 | 0.003 | - | 18.32 | - | needed | 1024 | 2519 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted#1` | second | counted | - | 5.788 | 0.028 | 0.005 | - | 18.32 | - | needed | 1120 | 2519 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@work-uncounted#1` | first | work-uncounted | - | 5.391 | 0.037 | 0.007 | - | 16.07 | - | needed | 1024 | 2519 | - | 0 | yes |
| path-65536 | triangles | `grust-next@work-uncounted#1` | second | work-uncounted | - | 4.936 | 0.015 | 0.003 | - | 16.07 | - | needed | 1120 | 2519 | - | 0 | yes |
| path-65536 | triangles | `grust-next@unchecked#1` | first | unchecked | - | 5.118 | 0.050 | 0.010 | - | 16.49 | - | needed | 1024 | 3030 | - | 0 | yes |
| path-65536 | triangles | `grust-next@unchecked#1` | second | unchecked | - | 4.680 | 0.026 | 0.006 | - | 16.49 | - | needed | 1120 | 3030 | - | 0 | yes |
| path-65536 | triangles | `grust-next@counted#unset` | first | counted | - | 6.213 | 0.064 | 0.010 | - | 19.92 | - | needed | 1024 | 2455 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted#unset` | second | counted | - | 4.745 | 0.046 | 0.010 | - | 19.92 | - | needed | 384 | 2455 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 5.373 | 0.039 | 0.007 | - | 16.05 | - | needed | 1024 | 2455 | - | 0 | yes |
| path-65536 | triangles | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 3.836 | 0.005 | 0.001 | - | 16.05 | - | needed | 384 | 2455 | - | 0 | yes |
| path-65536 | triangles | `grust-next@unchecked#unset` | first | unchecked | - | 5.175 | 0.060 | 0.012 | - | 16.12 | - | needed | 1024 | 2455 | - | 0 | yes |
| path-65536 | triangles | `grust-next@unchecked#unset` | second | unchecked | - | 3.571 | 0.005 | 0.001 | - | 16.12 | - | needed | 384 | 2455 | - | 0 | yes |
| path-65536 | triangles | `grust-next@counted+eager#1` | first | counted | - | 6.218 | 0.026 | 0.004 | - | 18.69 | 0.00 | always | 1024 | 2519 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted+eager#1` | second | counted | - | 5.797 | 0.029 | 0.005 | - | 18.69 | 0.00 | always | 1120 | 2519 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted+eager#unset` | first | counted | - | 6.407 | 0.148 | 0.023 | - | 19.74 | 0.00 | always | 1024 | 2455 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted+eager#unset` | second | counted | - | 4.728 | 0.021 | 0.004 | - | 19.74 | 0.00 | always | 384 | 2455 | 1703922 | 0 | yes |
| path-65536 | wcc | `neo4j-graph` |  |  | - | 2.596 | 0.004 | 0.002 | - | 4.88 | - |  | 33 | 1276 | - | 0 | yes |
| path-65536 | wcc | `icebug` |  |  | - | 1.214 | 0.006 | 0.005 | - | 7.05 | - |  | 137 | 1795 | - | 0 | yes |
| path-65536 | wcc | `icecat` |  |  | - | 1.082 | 0.010 | 0.009 | - | 4.18 | - |  | 256 | 1138 | - | 0 | yes |
| path-65536 | wcc | `grustcat` |  |  | - | 0.629 | 0.004 | 0.006 | - | 102.85 | - |  | 1 | 24215 | - | 0 | yes |
| path-65536 | wcc | `grust#1` | first | counted | - | 1.773 | 0.002 | 0.001 | - | 21.01 | - | needed | 128 | 2486 | 917497 | 0 | yes |
| path-65536 | wcc | `grust#1` | second | counted | - | 1.813 | 0.010 | 0.005 | - | 21.01 | - | needed | 127 | 2486 | 917497 | 0 | yes |
| path-65536 | wcc | `grust#unset` | first | counted | - | 3.982 | 0.010 | 0.002 | - | 20.82 | - | needed | 128 | 2471 | 1179639 | 0 | yes |
| path-65536 | wcc | `grust#unset` | second | counted | - | 3.974 | 0.005 | 0.001 | - | 20.82 | - | needed | 126 | 2471 | 1179639 | 0 | yes |
| path-65536 | wcc | `grust-next@counted#1` | first | counted | - | 1.788 | 0.011 | 0.006 | - | 17.82 | - | needed | 128 | 2264 | 917497 | 0 | yes |
| path-65536 | wcc | `grust-next@counted#1` | second | counted | - | 1.636 | 0.002 | 0.001 | - | 17.82 | - | needed | 64 | 2264 | 917497 | 0 | yes |
| path-65536 | wcc | `grust-next@work-uncounted#1` | first | work-uncounted | - | 1.267 | 0.013 | 0.010 | - | 14.73 | - | needed | 128 | 2263 | - | 0 | yes |
| path-65536 | wcc | `grust-next@work-uncounted#1` | second | work-uncounted | - | 1.112 | 0.002 | 0.002 | - | 14.73 | - | needed | 64 | 2263 | - | 0 | yes |
| path-65536 | wcc | `grust-next@unchecked#1` | first | unchecked | - | 1.212 | 0.011 | 0.009 | - | 14.56 | - | needed | 128 | 2263 | - | 0 | yes |
| path-65536 | wcc | `grust-next@unchecked#1` | second | unchecked | - | 1.061 | 0.003 | 0.003 | - | 14.56 | - | needed | 64 | 2263 | - | 0 | yes |
| path-65536 | wcc | `grust-next@counted#unset` | first | counted | - | 3.957 | 0.009 | 0.002 | - | 18.38 | - | needed | 128 | 2199 | 1179639 | 0 | yes |
| path-65536 | wcc | `grust-next@counted#unset` | second | counted | - | 4.069 | 0.009 | 0.002 | - | 18.38 | - | needed | 192 | 2199 | 1179639 | 0 | yes |
| path-65536 | wcc | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 1.518 | 0.008 | 0.005 | - | 14.79 | - | needed | 128 | 2199 | - | 0 | yes |
| path-65536 | wcc | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 1.652 | 0.011 | 0.007 | - | 14.79 | - | needed | 192 | 2199 | - | 0 | yes |
| path-65536 | wcc | `grust-next@unchecked#unset` | first | unchecked | - | 1.387 | 0.010 | 0.007 | - | 15.26 | - | needed | 128 | 2199 | - | 0 | yes |
| path-65536 | wcc | `grust-next@unchecked#unset` | second | unchecked | - | 1.496 | 0.009 | 0.006 | - | 15.26 | - | needed | 192 | 2199 | - | 0 | yes |
| path-65536 | wcc | `grust-next@counted+eager#1` | first | counted | - | 1.810 | 0.016 | 0.009 | - | 19.62 | 1.78 | always | 128 | 2519 | 1310711 | 0 | yes |
| path-65536 | wcc | `grust-next@counted+eager#1` | second | counted | - | 1.771 | 0.012 | 0.007 | - | 19.62 | 1.78 | always | 128 | 2519 | 1310711 | 0 | yes |
| path-65536 | wcc | `grust-next@counted+eager#unset` | first | counted | - | 3.966 | 0.008 | 0.002 | - | 21.02 | 2.50 | always | 128 | 2455 | 1572853 | 0 | yes |
| path-65536 | wcc | `grust-next@counted+eager#unset` | second | counted | - | 4.087 | 0.021 | 0.005 | - | 21.02 | 2.50 | always | 192 | 2455 | 1572853 | 0 | yes |
| uniform-16384 | bfs | `icebug` |  |  | - | 1.456 | 0.021 | 0.015 | - | 9.06 | - |  | 57 | 979 | - | 0 | yes |
| uniform-16384 | bfs | `icecat` |  |  | - | 0.892 | 0.013 | 0.014 | - | 6.84 | - |  | 97 | 2068 | - | 0 | yes |
| uniform-16384 | bfs | `grustcat` |  |  | - | 0.674 | 0.019 | 0.028 | - | 78.29 | - |  | 0 | 10541 | - | 0 | yes |
| uniform-16384 | bfs | `grust#1` | first | counted | - | 1.577 | 0.011 | 0.007 | - | 17.27 | - | needed | 36 | 1789 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust#1` | second | counted | - | 1.461 | 0.006 | 0.004 | - | 17.27 | - | needed | 0 | 1789 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust#unset` | first | counted | - | 1.571 | 0.014 | 0.009 | - | 16.98 | - | needed | 36 | 1775 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust#unset` | second | counted | - | 1.472 | 0.016 | 0.011 | - | 16.98 | - | needed | 0 | 1775 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted#1` | first | counted | - | 1.592 | 0.008 | 0.005 | - | 10.47 | - | needed | 32 | 1741 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted#1` | second | counted | - | 1.460 | 0.004 | 0.002 | - | 10.47 | - | needed | 0 | 1741 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@work-uncounted#1` | first | work-uncounted | - | 1.025 | 0.020 | 0.019 | - | 8.74 | - | needed | 32 | 1741 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@work-uncounted#1` | second | work-uncounted | - | 0.894 | 0.023 | 0.025 | - | 8.74 | - | needed | 0 | 1741 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@unchecked#1` | first | unchecked | - | 0.933 | 0.013 | 0.014 | - | 7.93 | - | needed | 32 | 1741 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@unchecked#1` | second | unchecked | - | 0.778 | 0.007 | 0.009 | - | 7.93 | - | needed | 0 | 1741 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted#unset` | first | counted | - | 1.616 | 0.004 | 0.003 | - | 12.62 | - | needed | 36 | 1725 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted#unset` | second | counted | - | 1.465 | 0.005 | 0.003 | - | 12.62 | - | needed | 0 | 1725 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 1.044 | 0.021 | 0.020 | - | 8.72 | - | needed | 36 | 1725 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 0.873 | 0.003 | 0.003 | - | 8.72 | - | needed | 0 | 1725 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@unchecked#unset` | first | unchecked | - | 0.951 | 0.017 | 0.017 | - | 8.56 | - | needed | 36 | 1725 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@unchecked#unset` | second | unchecked | - | 0.789 | 0.001 | 0.002 | - | 8.56 | - | needed | 0 | 1725 | - | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted+eager#1` | first | counted | - | 1.595 | 0.035 | 0.022 | - | 11.25 | 1.43 | always | 32 | 1519 | 1490619 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted+eager#1` | second | counted | - | 1.471 | 0.007 | 0.005 | - | 11.25 | 1.43 | always | 0 | 1519 | 1490619 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted+eager#unset` | first | counted | - | 1.653 | 0.029 | 0.018 | - | 14.50 | 1.79 | always | 64 | 1502 | 1490619 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted+eager#unset` | second | counted | - | 1.482 | 0.013 | 0.009 | - | 14.50 | 1.79 | always | 0 | 1502 | 1490619 | 0 | yes |
| uniform-16384 | pagerank | `neo4j-graph` |  |  | 28 | 10.402 | 0.038 | 0.004 | 0.371 | 7.37 | - |  | 23 | 668 | - | 0 | yes |
| uniform-16384 | pagerank | `icebug` |  |  | 12 | 7.778 | 0.056 | 0.007 | 0.648 | 9.19 | - |  | 111 | 979 | - | 0 | yes |
| uniform-16384 | pagerank | `icecat` |  |  | 16 | 8.018 | 0.007 | 0.001 | 0.501 | 6.75 | - |  | 128 | 2067 | - | 0 | yes |
| uniform-16384 | pagerank | `grustcat` |  |  | 16 | 6.796 | 0.028 | 0.004 | 0.425 | 79.21 | - |  | 0 | 10541 | - | 0 | yes |
| uniform-16384 | pagerank | `grust#1` | first | counted | 16 | 11.113 | 0.011 | 0.001 | 0.695 | 16.99 | - | needed | 384 | 1789 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust#1` | second | counted | 16 | 9.203 | 0.002 | 0.000 | 0.575 | 16.99 | - | needed | 0 | 1789 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust#unset` | first | counted | 16 | 47.938 | 0.015 | 0.000 | 2.996 | 17.58 | - | needed | 128 | 2285 | 4373785 | 0 | yes |
| uniform-16384 | pagerank | `grust#unset` | second | counted | 16 | 47.727 | 0.014 | 0.000 | 2.983 | 17.58 | - | needed | 32 | 2285 | 4373785 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted#1` | first | counted | 16 | 7.752 | 0.023 | 0.003 | 0.484 | 11.29 | 1.45 | needed | 96 | 2029 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted#1` | second | counted | 16 | 7.540 | 0.018 | 0.002 | 0.471 | 11.29 | 1.45 | needed | 0 | 2029 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 16 | 7.279 | 0.015 | 0.002 | 0.455 | 9.41 | 1.28 | needed | 96 | 2029 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 16 | 7.061 | 0.006 | 0.001 | 0.441 | 9.41 | 1.28 | needed | 0 | 2029 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@unchecked#1` | first | unchecked | 16 | 7.068 | 0.006 | 0.001 | 0.442 | 9.15 | 1.25 | needed | 96 | 2029 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@unchecked#1` | second | unchecked | 16 | 6.851 | 0.005 | 0.001 | 0.428 | 9.15 | 1.25 | needed | 0 | 2029 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted#unset` | first | counted | 16 | 21.700 | 0.019 | 0.001 | 1.356 | 12.58 | - | needed | 128 | 1214 | 4373785 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted#unset` | second | counted | 16 | 21.498 | 0.010 | 0.000 | 1.344 | 12.58 | - | needed | 32 | 1214 | 4373785 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 16 | 13.194 | 0.020 | 0.001 | 0.825 | 8.73 | - | needed | 128 | 1214 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 16 | 13.033 | 0.011 | 0.001 | 0.815 | 8.73 | - | needed | 32 | 1214 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 16 | 12.750 | 0.014 | 0.001 | 0.797 | 8.37 | - | needed | 128 | 1214 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 16 | 12.574 | 0.018 | 0.001 | 0.786 | 8.37 | - | needed | 32 | 1214 | - | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted+eager#1` | first | counted | 16 | 7.743 | 0.016 | 0.002 | 0.484 | 11.24 | 1.44 | always | 96 | 2029 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted+eager#1` | second | counted | 16 | 7.537 | 0.004 | 0.000 | 0.471 | 11.24 | 1.44 | always | 0 | 2029 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted+eager#unset` | first | counted | 16 | 22.325 | 0.615 | 0.028 | 1.395 | 14.99 | 1.79 | always | 128 | 2013 | 4816061 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted+eager#unset` | second | counted | 16 | 21.557 | 0.057 | 0.003 | 1.347 | 14.99 | 1.79 | always | 32 | 2013 | 4816061 | 0 | yes |
| uniform-16384 | triangles | `neo4j-graph` |  |  | - | 8.882 | 0.190 | 0.021 | - | 7.37 | - |  | 4 | 668 | - | 0 | yes |
| uniform-16384 | triangles | `grust#1` | first | counted | - | 18.948 | 0.062 | 0.003 | - | 19.97 | - | needed | 928 | 2300 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust#1` | second | counted | - | 16.972 | 0.039 | 0.002 | - | 19.97 | - | needed | 32 | 2300 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust#unset` | first | counted | - | 19.034 | 0.009 | 0.000 | - | 20.58 | - | needed | 928 | 2796 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust#unset` | second | counted | - | 17.023 | 0.014 | 0.001 | - | 20.58 | - | needed | 32 | 2796 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted#1` | first | counted | - | 17.947 | 0.018 | 0.001 | - | 12.79 | - | needed | 417 | 1231 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted#1` | second | counted | - | 17.663 | 0.025 | 0.001 | - | 12.79 | - | needed | 512 | 1231 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@work-uncounted#1` | first | work-uncounted | - | 17.744 | 0.017 | 0.001 | - | 11.20 | - | needed | 417 | 1231 | - | 0 | yes |
| uniform-16384 | triangles | `grust-next@work-uncounted#1` | second | work-uncounted | - | 17.463 | 0.013 | 0.001 | - | 11.20 | - | needed | 512 | 1231 | - | 0 | yes |
| uniform-16384 | triangles | `grust-next@unchecked#1` | first | unchecked | - | 17.519 | 0.038 | 0.002 | - | 10.94 | - | needed | 417 | 1231 | - | 0 | yes |
| uniform-16384 | triangles | `grust-next@unchecked#1` | second | unchecked | - | 17.225 | 0.050 | 0.003 | - | 10.94 | - | needed | 512 | 1231 | - | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted#unset` | first | counted | - | 17.951 | 0.017 | 0.001 | - | 15.71 | - | needed | 417 | 704 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted#unset` | second | counted | - | 17.683 | 0.032 | 0.002 | - | 15.71 | - | needed | 544 | 704 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 17.688 | 0.025 | 0.001 | - | 11.71 | - | needed | 417 | 704 | - | 0 | yes |
| uniform-16384 | triangles | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 17.354 | 0.024 | 0.001 | - | 11.71 | - | needed | 544 | 704 | - | 0 | yes |
| uniform-16384 | triangles | `grust-next@unchecked#unset` | first | unchecked | - | 17.574 | 0.046 | 0.003 | - | 11.28 | - | needed | 417 | 704 | - | 0 | yes |
| uniform-16384 | triangles | `grust-next@unchecked#unset` | second | unchecked | - | 17.211 | 0.053 | 0.003 | - | 11.28 | - | needed | 544 | 704 | - | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted+eager#1` | first | counted | - | 17.929 | 0.098 | 0.005 | - | 12.84 | 0.00 | always | 417 | 1230 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted+eager#1` | second | counted | - | 17.667 | 0.049 | 0.003 | - | 12.84 | 0.00 | always | 512 | 1230 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted+eager#unset` | first | counted | - | 17.933 | 0.088 | 0.005 | - | 16.30 | 0.00 | always | 417 | 1215 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted+eager#unset` | second | counted | - | 17.608 | 0.025 | 0.001 | - | 16.30 | 0.00 | always | 544 | 1215 | 3829630 | 0 | yes |
| uniform-16384 | wcc | `neo4j-graph` |  |  | - | 1.003 | 0.003 | 0.003 | - | 7.71 | - |  | 0 | 668 | - | 0 | yes |
| uniform-16384 | wcc | `icebug` |  |  | - | 2.266 | 0.020 | 0.009 | - | 9.11 | - |  | 68 | 979 | - | 0 | yes |
| uniform-16384 | wcc | `icecat` |  |  | - | 1.073 | 0.004 | 0.004 | - | 6.82 | - |  | 65 | 2067 | - | 0 | yes |
| uniform-16384 | wcc | `grustcat` |  |  | - | 0.741 | 0.002 | 0.002 | - | 78.54 | - |  | 0 | 10541 | - | 0 | yes |
| uniform-16384 | wcc | `grust#1` | first | counted | - | 2.039 | 0.005 | 0.002 | - | 17.28 | - | needed | 32 | 1789 | 1031975 | 0 | yes |
| uniform-16384 | wcc | `grust#1` | second | counted | - | 2.261 | 0.015 | 0.007 | - | 17.28 | - | needed | 31 | 1789 | 1031975 | 0 | yes |
| uniform-16384 | wcc | `grust#unset` | first | counted | - | 4.145 | 0.001 | 0.000 | - | 17.17 | - | needed | 32 | 1774 | 1324427 | 0 | yes |
| uniform-16384 | wcc | `grust#unset` | second | counted | - | 4.141 | 0.004 | 0.001 | - | 17.17 | - | needed | 31 | 1774 | 1324427 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted#1` | first | counted | - | 2.316 | 0.007 | 0.003 | - | 9.96 | - | needed | 32 | 1230 | 1031975 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted#1` | second | counted | - | 2.271 | 0.008 | 0.003 | - | 9.96 | - | needed | 15 | 1230 | 1031975 | 0 | yes |
| uniform-16384 | wcc | `grust-next@work-uncounted#1` | first | work-uncounted | - | 2.018 | 0.006 | 0.003 | - | 7.40 | - | needed | 32 | 1230 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@work-uncounted#1` | second | work-uncounted | - | 1.963 | 0.004 | 0.002 | - | 7.40 | - | needed | 16 | 1230 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@unchecked#1` | first | unchecked | - | 1.858 | 0.010 | 0.006 | - | 7.46 | - | needed | 32 | 1230 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@unchecked#1` | second | unchecked | - | 1.821 | 0.010 | 0.006 | - | 7.46 | - | needed | 16 | 1230 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted#unset` | first | counted | - | 4.094 | 0.002 | 0.001 | - | 12.64 | - | needed | 32 | 1725 | 1324427 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted#unset` | second | counted | - | 4.091 | 0.006 | 0.001 | - | 12.64 | - | needed | 31 | 1725 | 1324427 | 0 | yes |
| uniform-16384 | wcc | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 1.692 | 0.002 | 0.001 | - | 8.75 | - | needed | 32 | 1214 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 1.679 | 0.011 | 0.006 | - | 8.75 | - | needed | 31 | 1214 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@unchecked#unset` | first | unchecked | - | 1.431 | 0.009 | 0.007 | - | 8.57 | - | needed | 32 | 1725 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@unchecked#unset` | second | unchecked | - | 1.427 | 0.002 | 0.002 | - | 8.57 | - | needed | 30 | 1725 | - | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted+eager#1` | first | counted | - | 2.318 | 0.007 | 0.003 | - | 11.35 | 1.45 | always | 32 | 1518 | 1474251 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted+eager#1` | second | counted | - | 2.320 | 0.011 | 0.005 | - | 11.35 | 1.45 | always | 31 | 1518 | 1474251 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted+eager#unset` | first | counted | - | 4.096 | 0.002 | 0.001 | - | 13.95 | 1.75 | always | 32 | 1503 | 1766703 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted+eager#unset` | second | counted | - | 4.093 | 0.004 | 0.001 | - | 13.95 | 1.75 | always | 31 | 1503 | 1766703 | 0 | yes |
| uniform-65536 | bfs | `icebug` |  |  | - | 8.435 | 0.144 | 0.017 | - | 42.09 | - |  | 216 | 3889 | - | 0 | yes |
| uniform-65536 | bfs | `icecat` |  |  | - | 3.932 | 0.042 | 0.011 | - | 17.95 | - |  | 180 | 1438 | - | 0 | yes |
| uniform-65536 | bfs | `grustcat` |  |  | - | 4.358 | 0.115 | 0.026 | - | 361.29 | - |  | 0 | 37597 | - | 0 | yes |
| uniform-65536 | bfs | `grust#1` | first | counted | - | 6.389 | 0.048 | 0.008 | - | 69.63 | - | needed | 210 | 2596 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust#1` | second | counted | - | 5.516 | 0.009 | 0.002 | - | 69.63 | - | needed | 0 | 2596 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust#unset` | first | counted | - | 7.065 | 0.111 | 0.016 | - | 70.84 | - | needed | 144 | 3092 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust#unset` | second | counted | - | 6.366 | 0.059 | 0.009 | - | 70.84 | - | needed | 0 | 3092 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted#1` | first | counted | - | 6.629 | 0.036 | 0.005 | - | 39.34 | - | needed | 134 | 2401 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted#1` | second | counted | - | 5.601 | 0.007 | 0.001 | - | 39.34 | - | needed | 0 | 2401 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@work-uncounted#1` | first | work-uncounted | - | 6.291 | 0.173 | 0.027 | - | 31.81 | - | needed | 134 | 2401 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@work-uncounted#1` | second | work-uncounted | - | 5.333 | 0.017 | 0.003 | - | 31.81 | - | needed | 0 | 2401 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@unchecked#1` | first | unchecked | - | 6.379 | 0.025 | 0.004 | - | 31.61 | - | needed | 134 | 2401 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@unchecked#1` | second | unchecked | - | 5.350 | 0.024 | 0.004 | - | 31.61 | - | needed | 0 | 2401 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted#unset` | first | counted | - | 7.540 | 0.045 | 0.006 | - | 49.17 | - | needed | 144 | 2337 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted#unset` | second | counted | - | 6.458 | 0.022 | 0.003 | - | 49.17 | - | needed | 0 | 2337 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 6.234 | 0.050 | 0.008 | - | 34.35 | - | needed | 144 | 2337 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 5.124 | 0.048 | 0.009 | - | 34.35 | - | needed | 0 | 2337 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@unchecked#unset` | first | unchecked | - | 5.730 | 0.064 | 0.011 | - | 33.05 | - | needed | 144 | 2337 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@unchecked#unset` | second | unchecked | - | 4.543 | 0.084 | 0.019 | - | 33.05 | - | needed | 0 | 2337 | - | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted+eager#1` | first | counted | - | 6.217 | 0.052 | 0.008 | - | 45.53 | 6.51 | always | 198 | 3042 | 5963146 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted+eager#1` | second | counted | - | 5.591 | 0.013 | 0.002 | - | 45.53 | 6.51 | always | 0 | 3042 | 5963146 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted+eager#unset` | first | counted | - | 7.324 | 0.090 | 0.012 | - | 58.44 | 7.90 | always | 256 | 3489 | 5963146 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted+eager#unset` | second | counted | - | 6.438 | 0.011 | 0.002 | - | 58.44 | 7.90 | always | 0 | 3489 | 5963146 | 0 | yes |
| uniform-65536 | pagerank | `neo4j-graph` |  |  | 34 | 44.243 | 0.082 | 0.002 | 1.301 | 33.89 | - |  | 71 | 1664 | - | 0 | yes |
| uniform-65536 | pagerank | `icebug` |  |  | 11 | 39.495 | 0.778 | 0.020 | 3.590 | 42.53 | - |  | 398 | 3889 | - | 0 | yes |
| uniform-65536 | pagerank | `icecat` |  |  | 16 | 32.695 | 0.016 | 0.000 | 2.043 | 18.20 | - |  | 607 | 1665 | - | 0 | yes |
| uniform-65536 | pagerank | `grustcat` |  |  | 16 | 29.269 | 0.117 | 0.004 | 1.829 | 362.75 | - |  | 0 | 37597 | - | 0 | yes |
| uniform-65536 | pagerank | `grust#1` | first | counted | 16 | 51.509 | 0.434 | 0.008 | 3.219 | 71.17 | - | needed | 1025 | 3107 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust#1` | second | counted | 16 | 42.867 | 0.335 | 0.008 | 2.679 | 71.17 | - | needed | 0 | 3107 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust#unset` | first | counted | 16 | 192.337 | 0.359 | 0.002 | 12.021 | 70.30 | - | needed | 512 | 3092 | 17497177 | 0 | yes |
| uniform-65536 | pagerank | `grust#unset` | second | counted | 16 | 191.544 | 0.131 | 0.001 | 11.972 | 70.30 | - | needed | 128 | 3092 | 17497177 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted#1` | first | counted | 16 | 32.483 | 0.203 | 0.006 | 2.030 | 46.79 | 6.36 | needed | 384 | 3042 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted#1` | second | counted | 16 | 31.611 | 0.250 | 0.008 | 1.976 | 46.79 | 6.36 | needed | 0 | 3042 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 16 | 30.664 | 0.176 | 0.006 | 1.917 | 38.78 | 5.86 | needed | 384 | 3553 | - | 0 | yes |
| uniform-65536 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 16 | 29.817 | 0.363 | 0.012 | 1.864 | 38.78 | 5.86 | needed | 0 | 3553 | - | 0 | yes |
| uniform-65536 | pagerank | `grust-next@unchecked#1` | first | unchecked | 16 | 29.583 | 0.106 | 0.004 | 1.849 | 37.21 | 5.78 | needed | 384 | 3042 | - | 0 | yes |
| uniform-65536 | pagerank | `grust-next@unchecked#1` | second | unchecked | 16 | 28.801 | 0.148 | 0.005 | 1.800 | 37.21 | 5.78 | needed | 0 | 3042 | - | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted#unset` | first | counted | 16 | 88.768 | 0.677 | 0.008 | 5.548 | 49.68 | - | needed | 512 | 2337 | 17497177 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted#unset` | second | counted | 16 | 88.625 | 0.720 | 0.008 | 5.539 | 49.68 | - | needed | 128 | 2337 | 17497177 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 16 | 55.194 | 0.252 | 0.005 | 3.450 | 34.10 | - | needed | 512 | 2337 | - | 0 | yes |
| uniform-65536 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 16 | 54.107 | 0.139 | 0.003 | 3.382 | 34.10 | - | needed | 128 | 2337 | - | 0 | yes |
| uniform-65536 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 16 | 53.939 | 0.239 | 0.004 | 3.371 | 34.12 | - | needed | 512 | 2848 | - | 0 | yes |
| uniform-65536 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 16 | 52.984 | 0.694 | 0.013 | 3.311 | 34.12 | - | needed | 128 | 2848 | - | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted+eager#1` | first | counted | 16 | 32.568 | 0.360 | 0.011 | 2.036 | 46.24 | 6.57 | always | 384 | 3042 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted+eager#1` | second | counted | 16 | 31.582 | 0.258 | 0.008 | 1.974 | 46.24 | 6.57 | always | 0 | 3042 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted+eager#unset` | first | counted | 16 | 88.636 | 0.042 | 0.000 | 5.540 | 57.47 | 7.84 | always | 512 | 2979 | 19266533 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted+eager#unset` | second | counted | 16 | 87.877 | 0.161 | 0.002 | 5.492 | 57.47 | 7.84 | always | 128 | 2979 | 19266533 | 0 | yes |
| uniform-65536 | triangles | `neo4j-graph` |  |  | - | 39.465 | 0.138 | 0.003 | - | 33.79 | - |  | 4 | 1664 | - | 0 | yes |
| uniform-65536 | triangles | `grust#1` | first | counted | - | 80.935 | 0.521 | 0.006 | - | 84.59 | - | needed | 1668 | 3110 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust#1` | second | counted | - | 75.732 | 0.501 | 0.007 | - | 84.59 | - | needed | 128 | 3110 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust#unset` | first | counted | - | 81.491 | 0.347 | 0.004 | - | 85.66 | - | needed | 1668 | 3095 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust#unset` | second | counted | - | 76.005 | 0.053 | 0.001 | - | 85.66 | - | needed | 128 | 3095 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted#1` | first | counted | - | 78.553 | 0.998 | 0.013 | - | 55.60 | - | needed | 1157 | 1384 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted#1` | second | counted | - | 77.531 | 0.311 | 0.004 | - | 55.60 | - | needed | 1537 | 1384 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@work-uncounted#1` | first | work-uncounted | - | 77.719 | 0.059 | 0.001 | - | 47.84 | - | needed | 1157 | 1894 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@work-uncounted#1` | second | work-uncounted | - | 76.381 | 0.084 | 0.001 | - | 47.84 | - | needed | 1537 | 1894 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@unchecked#1` | first | unchecked | - | 77.836 | 0.196 | 0.003 | - | 46.11 | - | needed | 1157 | 1383 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@unchecked#1` | second | unchecked | - | 76.368 | 0.307 | 0.004 | - | 46.11 | - | needed | 1537 | 1383 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted#unset` | first | counted | - | 78.435 | 0.029 | 0.000 | - | 70.26 | - | needed | 1157 | 1319 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted#unset` | second | counted | - | 76.059 | 0.359 | 0.005 | - | 70.26 | - | needed | 1154 | 1319 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 78.371 | 0.225 | 0.003 | - | 53.35 | - | needed | 1157 | 1319 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 75.158 | 0.100 | 0.001 | - | 53.35 | - | needed | 643 | 1319 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@unchecked#unset` | first | unchecked | - | 77.149 | 0.091 | 0.001 | - | 51.08 | - | needed | 1157 | 1319 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@unchecked#unset` | second | unchecked | - | 74.030 | 0.167 | 0.002 | - | 51.08 | - | needed | 643 | 1319 | - | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted+eager#1` | first | counted | - | 79.141 | 0.187 | 0.002 | - | 54.55 | 0.00 | always | 1157 | 1383 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted+eager#1` | second | counted | - | 77.759 | 0.215 | 0.003 | - | 54.55 | 0.00 | always | 1537 | 1383 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted+eager#unset` | first | counted | - | 79.105 | 0.388 | 0.005 | - | 70.65 | 0.00 | always | 1157 | 1320 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted+eager#unset` | second | counted | - | 76.308 | 0.502 | 0.007 | - | 70.65 | 0.00 | always | 1154 | 1320 | 15327135 | 0 | yes |
| uniform-65536 | wcc | `neo4j-graph` |  |  | - | 3.751 | 0.005 | 0.001 | - | 34.08 | - |  | 32 | 1665 | - | 0 | yes |
| uniform-65536 | wcc | `icebug` |  |  | - | 12.825 | 0.083 | 0.006 | - | 42.40 | - |  | 244 | 3889 | - | 0 | yes |
| uniform-65536 | wcc | `icecat` |  |  | - | 4.023 | 0.070 | 0.017 | - | 17.95 | - |  | 35 | 1489 | - | 0 | yes |
| uniform-65536 | wcc | `grustcat` |  |  | - | 3.045 | 0.041 | 0.014 | - | 360.59 | - |  | 0 | 37597 | - | 0 | yes |
| uniform-65536 | wcc | `grust#1` | first | counted | - | 8.875 | 0.050 | 0.006 | - | 70.21 | - | needed | 128 | 3107 | 4128495 | 0 | yes |
| uniform-65536 | wcc | `grust#1` | second | counted | - | 9.246 | 0.016 | 0.002 | - | 70.21 | - | needed | 128 | 3107 | 4128495 | 0 | yes |
| uniform-65536 | wcc | `grust#unset` | first | counted | - | 17.078 | 0.048 | 0.003 | - | 70.85 | - | needed | 128 | 3092 | 5298822 | 0 | yes |
| uniform-65536 | wcc | `grust#unset` | second | counted | - | 16.972 | 0.015 | 0.001 | - | 70.85 | - | needed | 127 | 3092 | 5298822 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted#1` | first | counted | - | 9.805 | 0.034 | 0.003 | - | 40.21 | - | needed | 128 | 2912 | 4128495 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted#1` | second | counted | - | 9.613 | 0.054 | 0.006 | - | 40.21 | - | needed | 64 | 2912 | 4128495 | 0 | yes |
| uniform-65536 | wcc | `grust-next@work-uncounted#1` | first | work-uncounted | - | 8.494 | 0.010 | 0.001 | - | 31.70 | - | needed | 128 | 2401 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@work-uncounted#1` | second | work-uncounted | - | 8.249 | 0.023 | 0.003 | - | 31.70 | - | needed | 64 | 2401 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@unchecked#1` | first | unchecked | - | 7.877 | 0.046 | 0.006 | - | 31.90 | - | needed | 128 | 2401 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@unchecked#1` | second | unchecked | - | 7.638 | 0.046 | 0.006 | - | 31.90 | - | needed | 64 | 2401 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted#unset` | first | counted | - | 16.956 | 0.033 | 0.002 | - | 50.93 | - | needed | 128 | 2337 | 5298822 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted#unset` | second | counted | - | 16.892 | 0.015 | 0.001 | - | 50.93 | - | needed | 127 | 2337 | 5298822 | 0 | yes |
| uniform-65536 | wcc | `grust-next@work-uncounted#unset` | first | work-uncounted | - | 8.061 | 0.041 | 0.005 | - | 34.28 | - | needed | 128 | 2337 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@work-uncounted#unset` | second | work-uncounted | - | 8.062 | 0.187 | 0.023 | - | 34.28 | - | needed | 127 | 2337 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@unchecked#unset` | first | unchecked | - | 6.846 | 0.106 | 0.015 | - | 32.78 | - | needed | 128 | 2337 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@unchecked#unset` | second | unchecked | - | 6.721 | 0.031 | 0.005 | - | 32.78 | - | needed | 127 | 2337 | - | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted+eager#1` | first | counted | - | 9.905 | 0.059 | 0.006 | - | 45.05 | 6.34 | always | 128 | 3042 | 5897851 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted+eager#1` | second | counted | - | 9.968 | 0.051 | 0.005 | - | 45.05 | 6.34 | always | 127 | 3042 | 5897851 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted+eager#unset` | first | counted | - | 17.044 | 0.016 | 0.001 | - | 57.28 | 7.86 | always | 128 | 2978 | 7068178 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted+eager#unset` | second | counted | - | 17.082 | 0.030 | 0.002 | - | 57.28 | 7.86 | always | 127 | 2978 | 7068178 | 0 | yes |

### `pinned-full-width.json`: pinned-full-width

workers 16, concurrency 16, allocator pinned: glibc.malloc.mmap_threshold=131072, 1 warmup + 5 repeats, steal over the run 0 ticks, 73.5 s, unusable at MAD/median >= 0.25

Not timed (no agreeing parity row): neo4j-graph pagerank layered-16384.edges, neo4j-graph pagerank layered-65536.edges, neo4j-graph pagerank path-16384.edges, neo4j-graph pagerank path-65536.edges 

| fixture | algorithm | participant | call | accounting | iters | total ms | MAD | MAD/median | per iter | build ms | incoming ms | prepare | minflt | minflt build | work units | steal | usable |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |
| hub-16384 | bfs | `icebug` |  |  | - | 1.430 | 0.015 | 0.011 | - | 9.18 | - |  | 58 | 1018 | - | 0 | yes |
| hub-16384 | bfs | `icecat` |  |  | - | 0.856 | 0.006 | 0.007 | - | 5.72 | - |  | 100 | 1572 | - | 0 | yes |
| hub-16384 | bfs | `grustcat` |  |  | - | 0.643 | 0.011 | 0.018 | - | 79.06 | - |  | 33 | 10354 | - | 0 | yes |
| hub-16384 | bfs | `grust` | first | counted | - | 1.600 | 0.009 | 0.005 | - | 17.52 | - | needed | 69 | 1792 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust` | second | counted | - | 1.765 | 0.010 | 0.005 | - | 17.52 | - | needed | 33 | 1792 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted` | first | counted | - | 1.648 | 0.011 | 0.007 | - | 10.35 | - | needed | 66 | 1575 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted` | second | counted | - | 1.624 | 0.003 | 0.002 | - | 10.35 | - | needed | 66 | 1575 | 1047577 | 0 | yes |
| hub-16384 | pagerank | `neo4j-graph` |  |  | 36 | 13.305 | 0.027 | 0.002 | 0.370 | 4.83 | - |  | 61 | 936 | - | 0 | yes |
| hub-16384 | pagerank | `icebug` |  |  | 12 | 3.042 | 0.122 | 0.040 | 0.253 | 9.28 | - |  | 213 | 1018 | - | 0 | yes |
| hub-16384 | pagerank | `icecat` |  |  | 17 | 8.646 | 0.013 | 0.002 | 0.509 | 5.46 | - |  | 230 | 1572 | - | 0 | yes |
| hub-16384 | pagerank | `grustcat` |  |  | 17 | 7.431 | 0.007 | 0.001 | 0.437 | 80.84 | - |  | 100 | 10864 | - | 0 | yes |
| hub-16384 | pagerank | `grust` | first | counted | 17 | 6.346 | 0.089 | 0.014 | 0.373 | 17.65 | - | needed | 536 | 1793 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust` | second | counted | 17 | 3.746 | 0.134 | 0.036 | 0.220 | 17.65 | - | needed | 100 | 1793 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted` | first | counted | 17 | 3.762 | 0.067 | 0.018 | 0.221 | 12.92 | 2.16 | needed | 136 | 2649 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted` | second | counted | 17 | 3.774 | 0.223 | 0.059 | 0.222 | 12.92 | 2.16 | needed | 132 | 2649 | 4403580 | 0 | yes |
| hub-16384 | triangles | `neo4j-graph` |  |  | - | 1.132 | 0.013 | 0.011 | - | 4.72 | - |  | 52 | 897 | - | 0 | yes |
| hub-16384 | triangles | `grust` | first | counted | - | 8.055 | 0.051 | 0.006 | - | 20.87 | - | needed | 556 | 1282 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust` | second | counted | - | 7.237 | 0.025 | 0.003 | - | 20.87 | - | needed | 457 | 1282 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted` | first | counted | - | 7.449 | 0.006 | 0.001 | - | 11.06 | - | needed | 455 | 1065 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted` | second | counted | - | 7.065 | 0.028 | 0.004 | - | 11.06 | - | needed | 455 | 1065 | 3742208 | 0 | yes |
| hub-16384 | wcc | `neo4j-graph` |  |  | - | 1.285 | 0.011 | 0.009 | - | 4.59 | - |  | 109 | 906 | - | 0 | yes |
| hub-16384 | wcc | `icebug` |  |  | - | 1.972 | 0.023 | 0.011 | - | 9.11 | - |  | 69 | 1018 | - | 0 | yes |
| hub-16384 | wcc | `icecat` |  |  | - | 0.899 | 0.002 | 0.003 | - | 5.65 | - |  | 66 | 1572 | - | 0 | yes |
| hub-16384 | wcc | `grustcat` |  |  | - | 0.606 | 0.006 | 0.009 | - | 79.61 | - |  | 0 | 10864 | - | 0 | yes |
| hub-16384 | wcc | `grust` | first | counted | - | 1.352 | 0.102 | 0.076 | - | 17.67 | - | needed | 176 | 2303 | 1031212 | 0 | yes |
| hub-16384 | wcc | `grust` | second | counted | - | 0.678 | 0.055 | 0.081 | - | 17.67 | - | needed | 70 | 2303 | 1031212 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted` | first | counted | - | 0.736 | 0.034 | 0.047 | - | 10.86 | - | needed | 68 | 1578 | 1031209 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted` | second | counted | - | 0.673 | 0.026 | 0.039 | - | 10.86 | - | needed | 68 | 1578 | 1031209 | 0 | yes |
| hub-65536 | bfs | `icebug` |  |  | - | 8.377 | 0.062 | 0.007 | - | 43.22 | - |  | 216 | 4057 | - | 0 | yes |
| hub-65536 | bfs | `icecat` |  |  | - | 4.388 | 0.098 | 0.022 | - | 18.58 | - |  | 388 | 2697 | - | 0 | yes |
| hub-65536 | bfs | `grustcat` |  |  | - | 4.620 | 0.038 | 0.008 | - | 372.51 | - |  | 129 | 38258 | - | 0 | yes |
| hub-65536 | bfs | `grust` | first | counted | - | 4.730 | 0.079 | 0.017 | - | 69.59 | - | needed | 598 | 2596 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust` | second | counted | - | 3.746 | 0.013 | 0.003 | - | 69.59 | - | needed | 388 | 2596 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted` | first | counted | - | 3.821 | 0.057 | 0.015 | - | 37.09 | - | needed | 414 | 2914 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted` | second | counted | - | 3.552 | 0.068 | 0.019 | - | 37.09 | - | needed | 354 | 2914 | 4191009 | 0 | yes |
| hub-65536 | pagerank | `neo4j-graph` |  |  | 31 | 15.207 | 0.044 | 0.003 | 0.491 | 14.86 | - |  | 170 | 1450 | - | 0 | yes |
| hub-65536 | pagerank | `icebug` |  |  | 12 | 7.452 | 0.043 | 0.006 | 0.621 | 43.86 | - |  | 487 | 4057 | - | 0 | yes |
| hub-65536 | pagerank | `icecat` |  |  | 17 | 34.597 | 0.015 | 0.000 | 2.035 | 18.82 | - |  | 901 | 2697 | - | 0 | yes |
| hub-65536 | pagerank | `grustcat` |  |  | 17 | 30.529 | 0.084 | 0.003 | 1.796 | 370.74 | - |  | 387 | 38258 | - | 0 | yes |
| hub-65536 | pagerank | `grust` | first | counted | 17 | 16.967 | 0.119 | 0.007 | 0.998 | 71.41 | - | needed | 771 | 2596 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust` | second | counted | 17 | 9.285 | 0.145 | 0.016 | 0.546 | 71.41 | - | needed | 390 | 2596 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted` | first | counted | 17 | 8.300 | 0.118 | 0.014 | 0.488 | 43.23 | 6.17 | needed | 533 | 3627 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted` | second | counted | 17 | 7.951 | 0.111 | 0.014 | 0.468 | 43.23 | 6.17 | needed | 519 | 3627 | 17616940 | 0 | yes |
| hub-65536 | triangles | `neo4j-graph` |  |  | - | 3.558 | 0.053 | 0.015 | - | 14.99 | - |  | 52 | 1453 | - | 0 | yes |
| hub-65536 | triangles | `grust` | first | counted | - | 30.922 | 0.179 | 0.006 | - | 85.63 | - | needed | 1393 | 3620 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust` | second | counted | - | 29.076 | 0.155 | 0.005 | - | 85.63 | - | needed | 1291 | 3620 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted` | first | counted | - | 29.605 | 0.065 | 0.002 | - | 43.26 | - | needed | 1290 | 4450 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted` | second | counted | - | 28.574 | 0.458 | 0.016 | - | 43.26 | - | needed | 1290 | 4450 | 14971727 | 0 | yes |
| hub-65536 | wcc | `neo4j-graph` |  |  | - | 3.374 | 0.088 | 0.026 | - | 14.94 | - |  | 415 | 1447 | - | 0 | yes |
| hub-65536 | wcc | `icebug` |  |  | - | 11.040 | 0.224 | 0.020 | - | 43.01 | - |  | 239 | 4057 | - | 0 | yes |
| hub-65536 | wcc | `icecat` |  |  | - | 3.741 | 0.011 | 0.003 | - | 18.68 | - |  | 259 | 2698 | - | 0 | yes |
| hub-65536 | wcc | `grustcat` |  |  | - | 2.437 | 0.003 | 0.001 | - | 370.86 | - |  | 0 | 38258 | - | 0 | yes |
| hub-65536 | wcc | `grust` | first | counted | - | 2.655 | 0.052 | 0.020 | - | 69.00 | - | needed | 368 | 2596 | 4125497 | 0 | yes |
| hub-65536 | wcc | `grust` | second | counted | - | 2.078 | 0.030 | 0.014 | - | 69.00 | - | needed | 264 | 2596 | 4125497 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted` | first | counted | - | 2.124 | 0.035 | 0.016 | - | 37.96 | - | needed | 261 | 2919 | 4125486 | 0 | yes |
| hub-65536 | wcc | `grust-next@counted` | second | counted | - | 1.949 | 0.035 | 0.018 | - | 37.96 | - | needed | 260 | 2919 | 4125486 | 0 | yes |
| layered-16384 | bfs | `icebug` |  |  | - | 0.480 | 0.002 | 0.004 | - | 2.75 | - |  | 37 | 458 | - | 0 | yes |
| layered-16384 | bfs | `icecat` |  |  | - | 0.390 | 0.002 | 0.004 | - | 1.71 | - |  | 66 | 544 | - | 0 | yes |
| layered-16384 | bfs | `grustcat` |  |  | - | 0.253 | 0.001 | 0.003 | - | 29.93 | - |  | 0 | 6873 | - | 0 | yes |
| layered-16384 | bfs | `grust` | first | counted | - | 0.512 | 0.004 | 0.008 | - | 6.82 | - | needed | 62 | 1036 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust` | second | counted | - | 0.506 | 0.002 | 0.003 | - | 6.82 | - | needed | 26 | 1036 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted` | first | counted | - | 0.526 | 0.004 | 0.008 | - | 6.22 | - | needed | 62 | 1052 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted` | second | counted | - | 0.478 | 0.002 | 0.003 | - | 6.22 | - | needed | 59 | 1052 | 347308 | 0 | yes |
| layered-16384 | pagerank | `icebug` |  |  | 69 | 8.800 | 0.299 | 0.034 | 0.128 | 2.76 | - |  | 200 | 458 | - | 0 | yes |
| layered-16384 | pagerank | `icecat` |  |  | 84 | 27.804 | 0.021 | 0.001 | 0.331 | 1.71 | - |  | 229 | 544 | - | 0 | yes |
| layered-16384 | pagerank | `grustcat` |  |  | 84 | 26.317 | 0.048 | 0.002 | 0.313 | 30.47 | - |  | 33 | 7383 | - | 0 | yes |
| layered-16384 | pagerank | `grust` | first | counted | 84 | 15.279 | 0.223 | 0.015 | 0.182 | 6.92 | - | needed | 347 | 1036 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust` | second | counted | 84 | 13.705 | 0.196 | 0.014 | 0.163 | 6.92 | - | needed | 99 | 1036 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted` | first | counted | 84 | 14.302 | 0.249 | 0.017 | 0.170 | 7.28 | 1.06 | needed | 141 | 1231 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted` | second | counted | 84 | 14.350 | 0.153 | 0.011 | 0.171 | 7.28 | 1.06 | needed | 132 | 1231 | 7307112 | 0 | yes |
| layered-16384 | triangles | `neo4j-graph` |  |  | - | 0.663 | 0.021 | 0.031 | - | 2.56 | - |  | 31 | 587 | - | 0 | yes |
| layered-16384 | triangles | `grust` | first | counted | - | 3.231 | 0.055 | 0.017 | - | 6.98 | - | needed | 491 | 1162 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust` | second | counted | - | 2.409 | 0.038 | 0.016 | - | 6.98 | - | needed | 390 | 1162 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted` | first | counted | - | 2.539 | 0.092 | 0.036 | - | 6.65 | - | needed | 389 | 1176 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted` | second | counted | - | 2.289 | 0.017 | 0.008 | - | 6.65 | - | needed | 389 | 1176 | 718265 | 0 | yes |
| layered-16384 | wcc | `neo4j-graph` |  |  | - | 1.217 | 0.017 | 0.014 | - | 2.52 | - |  | 114 | 583 | - | 0 | yes |
| layered-16384 | wcc | `icebug` |  |  | - | 0.952 | 0.014 | 0.015 | - | 2.78 | - |  | 43 | 458 | - | 0 | yes |
| layered-16384 | wcc | `icecat` |  |  | - | 0.505 | 0.003 | 0.006 | - | 1.70 | - |  | 67 | 544 | - | 0 | yes |
| layered-16384 | wcc | `grustcat` |  |  | - | 0.353 | 0.001 | 0.003 | - | 30.33 | - |  | 0 | 7383 | - | 0 | yes |
| layered-16384 | wcc | `grust` | first | counted | - | 1.115 | 0.026 | 0.024 | - | 6.95 | - | needed | 173 | 1036 | 341584 | 0 | yes |
| layered-16384 | wcc | `grust` | second | counted | - | 0.422 | 0.005 | 0.013 | - | 6.95 | - | needed | 70 | 1036 | 341584 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted` | first | counted | - | 0.453 | 0.009 | 0.020 | - | 5.97 | - | needed | 69 | 1051 | 341582 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted` | second | counted | - | 0.436 | 0.019 | 0.043 | - | 5.97 | - | needed | 67 | 1051 | 341582 | 0 | yes |
| layered-65536 | bfs | `icebug` |  |  | - | 2.040 | 0.005 | 0.002 | - | 11.07 | - |  | 132 | 1832 | - | 0 | yes |
| layered-65536 | bfs | `icecat` |  |  | - | 1.563 | 0.005 | 0.004 | - | 6.62 | - |  | 258 | 2162 | - | 0 | yes |
| layered-65536 | bfs | `grustcat` |  |  | - | 1.025 | 0.002 | 0.002 | - | 128.54 | - |  | 0 | 26650 | - | 0 | yes |
| layered-65536 | bfs | `grust` | first | counted | - | 2.032 | 0.005 | 0.002 | - | 28.45 | - | needed | 248 | 3146 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust` | second | counted | - | 2.300 | 0.007 | 0.003 | - | 28.45 | - | needed | 247 | 3146 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted` | first | counted | - | 2.112 | 0.030 | 0.014 | - | 21.19 | - | needed | 243 | 2880 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted` | second | counted | - | 1.928 | 0.004 | 0.002 | - | 21.19 | - | needed | 231 | 2880 | 1393359 | 0 | yes |
| layered-65536 | pagerank | `icebug` |  |  | 60 | 14.553 | 0.499 | 0.034 | 0.243 | 11.06 | - |  | 503 | 1832 | - | 0 | yes |
| layered-65536 | pagerank | `icecat` |  |  | 75 | 99.808 | 0.064 | 0.001 | 1.331 | 6.20 | - |  | 900 | 1652 | - | 0 | yes |
| layered-65536 | pagerank | `grustcat` |  |  | 75 | 94.826 | 0.078 | 0.001 | 1.264 | 129.29 | - |  | 387 | 26649 | - | 0 | yes |
| layered-65536 | pagerank | `grust` | first | counted | 75 | 26.031 | 0.327 | 0.013 | 0.347 | 28.03 | - | needed | 1033 | 3146 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust` | second | counted | 75 | 21.619 | 0.142 | 0.007 | 0.288 | 28.03 | - | needed | 389 | 3146 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted` | first | counted | 75 | 21.181 | 0.358 | 0.017 | 0.282 | 24.55 | 3.16 | needed | 538 | 3587 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted` | second | counted | 75 | 21.521 | 0.361 | 0.017 | 0.287 | 24.55 | 3.16 | needed | 521 | 3587 | 26313822 | 0 | yes |
| layered-65536 | triangles | `neo4j-graph` |  |  | - | 1.028 | 0.032 | 0.031 | - | 5.47 | - |  | 50 | 1938 | - | 0 | yes |
| layered-65536 | triangles | `grust` | first | counted | - | 10.340 | 0.138 | 0.013 | - | 29.23 | - | needed | 1638 | 3655 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust` | second | counted | - | 9.129 | 0.041 | 0.005 | - | 29.23 | - | needed | 1538 | 3655 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted` | first | counted | - | 9.563 | 0.033 | 0.004 | - | 23.05 | - | needed | 1536 | 3389 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted` | second | counted | - | 8.825 | 0.085 | 0.010 | - | 23.05 | - | needed | 1536 | 3389 | 2877576 | 0 | yes |
| layered-65536 | wcc | `neo4j-graph` |  |  | - | 2.973 | 0.228 | 0.077 | - | 5.39 | - |  | 422 | 1936 | - | 0 | yes |
| layered-65536 | wcc | `icebug` |  |  | - | 3.847 | 0.067 | 0.017 | - | 11.19 | - |  | 138 | 1832 | - | 0 | yes |
| layered-65536 | wcc | `icecat` |  |  | - | 1.981 | 0.016 | 0.008 | - | 6.83 | - |  | 258 | 2163 | - | 0 | yes |
| layered-65536 | wcc | `grustcat` |  |  | - | 1.423 | 0.015 | 0.011 | - | 128.42 | - |  | 0 | 26649 | - | 0 | yes |
| layered-65536 | wcc | `grust` | first | counted | - | 1.733 | 0.013 | 0.008 | - | 28.19 | - | needed | 369 | 3147 | 1368149 | 0 | yes |
| layered-65536 | wcc | `grust` | second | counted | - | 1.072 | 0.018 | 0.016 | - | 28.19 | - | needed | 264 | 3147 | 1368149 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted` | first | counted | - | 1.121 | 0.026 | 0.023 | - | 21.32 | - | needed | 262 | 2879 | 1368147 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted` | second | counted | - | 1.092 | 0.011 | 0.010 | - | 21.32 | - | needed | 261 | 2879 | 1368147 | 0 | yes |
| path-16384 | bfs | `icebug` |  |  | - | 0.256 | 0.004 | 0.015 | - | 1.77 | - |  | 37 | 450 | - | 0 | yes |
| path-16384 | bfs | `icecat` |  |  | - | 0.293 | 0.003 | 0.010 | - | 0.92 | - |  | 67 | 293 | - | 0 | yes |
| path-16384 | bfs | `grustcat` |  |  | - | 0.146 | 0.001 | 0.004 | - | 24.08 | - |  | 0 | 6429 | - | 0 | yes |
| path-16384 | bfs | `grust` | first | counted | - | 0.476 | 0.002 | 0.004 | - | 5.16 | - | needed | 69 | 746 | 245755 | 0 | yes |
| path-16384 | bfs | `grust` | second | counted | - | 0.435 | 0.002 | 0.004 | - | 5.16 | - | needed | 33 | 746 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@counted` | first | counted | - | 0.476 | 0.004 | 0.009 | - | 5.33 | - | needed | 66 | 794 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@counted` | second | counted | - | 0.432 | 0.001 | 0.002 | - | 5.33 | - | needed | 66 | 794 | 245755 | 0 | yes |
| path-16384 | pagerank | `icebug` |  |  | 54 | 6.573 | 0.089 | 0.014 | 0.122 | 1.77 | - |  | 199 | 450 | - | 0 | yes |
| path-16384 | pagerank | `icecat` |  |  | 58 | 11.333 | 0.015 | 0.001 | 0.195 | 0.95 | - |  | 229 | 292 | - | 0 | yes |
| path-16384 | pagerank | `grustcat` |  |  | 58 | 10.063 | 0.175 | 0.017 | 0.174 | 24.36 | - |  | 0 | 6429 | - | 0 | yes |
| path-16384 | pagerank | `grust` | first | counted | 58 | 10.221 | 0.025 | 0.002 | 0.176 | 5.12 | - | needed | 316 | 745 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust` | second | counted | 58 | 8.648 | 0.106 | 0.012 | 0.149 | 5.12 | - | needed | 99 | 745 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted` | first | counted | 58 | 15.811 | 0.541 | 0.034 | 0.273 | 6.09 | 0.76 | needed | 144 | 911 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted` | second | counted | 58 | 15.855 | 0.511 | 0.032 | 0.273 | 6.09 | 0.76 | needed | 132 | 911 | 4112319 | 0 | yes |
| path-16384 | triangles | `neo4j-graph` |  |  | - | 0.491 | 0.016 | 0.033 | - | 2.26 | - |  | 19 | 448 | - | 0 | yes |
| path-16384 | triangles | `grust` | first | counted | - | 2.251 | 0.013 | 0.006 | - | 5.19 | - | needed | 397 | 807 | 425970 | 0 | yes |
| path-16384 | triangles | `grust` | second | counted | - | 1.546 | 0.015 | 0.010 | - | 5.19 | - | needed | 296 | 807 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted` | first | counted | - | 1.679 | 0.027 | 0.016 | - | 5.55 | - | needed | 295 | 857 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted` | second | counted | - | 1.584 | 0.017 | 0.011 | - | 5.55 | - | needed | 295 | 857 | 425970 | 0 | yes |
| path-16384 | wcc | `neo4j-graph` |  |  | - | 0.994 | 0.032 | 0.032 | - | 2.24 | - |  | 115 | 452 | - | 0 | yes |
| path-16384 | wcc | `icebug` |  |  | - | 0.336 | 0.003 | 0.010 | - | 1.77 | - |  | 42 | 450 | - | 0 | yes |
| path-16384 | wcc | `icecat` |  |  | - | 0.281 | 0.001 | 0.004 | - | 0.94 | - |  | 66 | 292 | - | 0 | yes |
| path-16384 | wcc | `grustcat` |  |  | - | 0.157 | 0.001 | 0.007 | - | 24.46 | - |  | 0 | 6429 | - | 0 | yes |
| path-16384 | wcc | `grust` | first | counted | - | 1.049 | 0.022 | 0.021 | - | 5.13 | - | needed | 170 | 745 | 229369 | 0 | yes |
| path-16384 | wcc | `grust` | second | counted | - | 0.394 | 0.022 | 0.056 | - | 5.13 | - | needed | 67 | 745 | 229369 | 0 | yes |
| path-16384 | wcc | `grust-next@counted` | first | counted | - | 0.551 | 0.017 | 0.030 | - | 5.30 | - | needed | 68 | 794 | 229369 | 0 | yes |
| path-16384 | wcc | `grust-next@counted` | second | counted | - | 0.551 | 0.043 | 0.078 | - | 5.30 | - | needed | 67 | 794 | 229369 | 0 | yes |
| path-65536 | bfs | `icebug` |  |  | - | 0.933 | 0.014 | 0.015 | - | 6.97 | - |  | 132 | 1795 | - | 0 | yes |
| path-65536 | bfs | `icecat` |  |  | - | 1.136 | 0.004 | 0.004 | - | 4.20 | - |  | 259 | 1157 | - | 0 | yes |
| path-65536 | bfs | `grustcat` |  |  | - | 0.755 | 0.000 | 0.000 | - | 102.80 | - |  | 130 | 24249 | - | 0 | yes |
| path-65536 | bfs | `grust` | first | counted | - | 1.871 | 0.008 | 0.004 | - | 21.13 | - | needed | 274 | 2491 | 983035 | 0 | yes |
| path-65536 | bfs | `grust` | second | counted | - | 1.967 | 0.008 | 0.004 | - | 21.13 | - | needed | 274 | 2491 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@counted` | first | counted | - | 1.860 | 0.023 | 0.012 | - | 18.33 | - | needed | 272 | 2382 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@counted` | second | counted | - | 1.717 | 0.015 | 0.009 | - | 18.33 | - | needed | 258 | 2382 | 983035 | 0 | yes |
| path-65536 | pagerank | `icebug` |  |  | 46 | 10.504 | 0.065 | 0.006 | 0.228 | 7.07 | - |  | 503 | 1795 | - | 0 | yes |
| path-65536 | pagerank | `icecat` |  |  | 50 | 39.506 | 0.049 | 0.001 | 0.790 | 4.22 | - |  | 902 | 1157 | - | 0 | yes |
| path-65536 | pagerank | `grustcat` |  |  | 50 | 36.355 | 0.984 | 0.027 | 0.727 | 102.73 | - |  | 516 | 24248 | - | 0 | yes |
| path-65536 | pagerank | `grust` | first | counted | 50 | 16.783 | 0.290 | 0.017 | 0.336 | 21.37 | - | needed | 905 | 2491 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust` | second | counted | 50 | 12.739 | 0.345 | 0.027 | 0.255 | 21.37 | - | needed | 390 | 2491 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted` | first | counted | 50 | 48.206 | 12.260 | 0.254 | 0.964 | 21.08 | 2.42 | needed | 537 | 2839 | 14352327 | 0 | **UNUSABLE** |
| path-65536 | pagerank | `grust-next@counted` | second | counted | 50 | 52.191 | 11.187 | 0.214 | 1.044 | 21.08 | 2.42 | needed | 518 | 2839 | 14352327 | 0 | yes |
| path-65536 | triangles | `neo4j-graph` |  |  | - | 0.678 | 0.009 | 0.014 | - | 4.46 | - |  | 29 | 1428 | - | 0 | yes |
| path-65536 | triangles | `grust` | first | counted | - | 6.663 | 0.063 | 0.009 | - | 21.58 | - | needed | 1261 | 2744 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust` | second | counted | - | 5.620 | 0.016 | 0.003 | - | 21.58 | - | needed | 1160 | 2744 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted` | first | counted | - | 6.358 | 0.032 | 0.005 | - | 18.70 | - | needed | 1159 | 2637 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted` | second | counted | - | 5.904 | 0.039 | 0.007 | - | 18.70 | - | needed | 1159 | 2637 | 1703922 | 0 | yes |
| path-65536 | wcc | `neo4j-graph` |  |  | - | 2.456 | 0.073 | 0.030 | - | 4.28 | - |  | 423 | 1422 | - | 0 | yes |
| path-65536 | wcc | `icebug` |  |  | - | 1.236 | 0.010 | 0.008 | - | 7.04 | - |  | 138 | 1795 | - | 0 | yes |
| path-65536 | wcc | `icecat` |  |  | - | 1.108 | 0.026 | 0.023 | - | 4.20 | - |  | 259 | 1157 | - | 0 | yes |
| path-65536 | wcc | `grustcat` |  |  | - | 0.813 | 0.002 | 0.002 | - | 102.37 | - |  | 129 | 24249 | - | 0 | yes |
| path-65536 | wcc | `grust` | first | counted | - | 1.638 | 0.023 | 0.014 | - | 21.08 | - | needed | 370 | 2490 | 917497 | 0 | yes |
| path-65536 | wcc | `grust` | second | counted | - | 0.974 | 0.015 | 0.015 | - | 21.08 | - | needed | 263 | 2490 | 917497 | 0 | yes |
| path-65536 | wcc | `grust-next@counted` | first | counted | - | 1.260 | 0.048 | 0.038 | - | 18.60 | - | needed | 261 | 2383 | 917497 | 0 | yes |
| path-65536 | wcc | `grust-next@counted` | second | counted | - | 1.215 | 0.087 | 0.071 | - | 18.60 | - | needed | 260 | 2383 | 917497 | 0 | yes |
| uniform-16384 | bfs | `icebug` |  |  | - | 1.475 | 0.017 | 0.012 | - | 9.08 | - |  | 57 | 979 | - | 0 | yes |
| uniform-16384 | bfs | `icecat` |  |  | - | 0.910 | 0.009 | 0.009 | - | 6.46 | - |  | 99 | 2084 | - | 0 | yes |
| uniform-16384 | bfs | `grustcat` |  |  | - | 0.688 | 0.012 | 0.018 | - | 79.89 | - |  | 0 | 10305 | - | 0 | yes |
| uniform-16384 | bfs | `grust` | first | counted | - | 1.671 | 0.002 | 0.001 | - | 17.26 | - | needed | 68 | 1793 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust` | second | counted | - | 1.819 | 0.011 | 0.006 | - | 17.26 | - | needed | 32 | 1793 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted` | first | counted | - | 1.742 | 0.006 | 0.003 | - | 10.64 | - | needed | 65 | 2084 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted` | second | counted | - | 1.631 | 0.010 | 0.006 | - | 10.64 | - | needed | 65 | 2084 | 1048343 | 0 | yes |
| uniform-16384 | pagerank | `neo4j-graph` |  |  | 28 | 10.496 | 0.024 | 0.002 | 0.375 | 4.44 | - |  | 59 | 892 | - | 0 | yes |
| uniform-16384 | pagerank | `icebug` |  |  | 12 | 2.892 | 0.008 | 0.003 | 0.241 | 9.06 | - |  | 215 | 979 | - | 0 | yes |
| uniform-16384 | pagerank | `icecat` |  |  | 16 | 8.202 | 0.012 | 0.001 | 0.513 | 6.01 | - |  | 230 | 1572 | - | 0 | yes |
| uniform-16384 | pagerank | `grustcat` |  |  | 16 | 6.916 | 0.023 | 0.003 | 0.432 | 80.33 | - |  | 33 | 10816 | - | 0 | yes |
| uniform-16384 | pagerank | `grust` | first | counted | 16 | 6.036 | 0.107 | 0.018 | 0.377 | 17.47 | - | needed | 536 | 1794 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust` | second | counted | 16 | 3.450 | 0.038 | 0.011 | 0.216 | 17.47 | - | needed | 99 | 1794 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted` | first | counted | 16 | 3.629 | 0.131 | 0.036 | 0.227 | 12.54 | 2.20 | needed | 137 | 2140 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted` | second | counted | 16 | 3.477 | 0.055 | 0.016 | 0.217 | 12.54 | 2.20 | needed | 132 | 2140 | 4226299 | 0 | yes |
| uniform-16384 | triangles | `neo4j-graph` |  |  | - | 1.225 | 0.021 | 0.017 | - | 4.51 | - |  | 52 | 886 | - | 0 | yes |
| uniform-16384 | triangles | `grust` | first | counted | - | 8.308 | 0.027 | 0.003 | - | 21.05 | - | needed | 557 | 1794 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust` | second | counted | - | 7.533 | 0.053 | 0.007 | - | 21.05 | - | needed | 456 | 1794 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted` | first | counted | - | 7.697 | 0.013 | 0.002 | - | 11.41 | - | needed | 455 | 1574 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted` | second | counted | - | 7.295 | 0.009 | 0.001 | - | 11.41 | - | needed | 455 | 1574 | 3829630 | 0 | yes |
| uniform-16384 | wcc | `neo4j-graph` |  |  | - | 1.286 | 0.003 | 0.003 | - | 4.40 | - |  | 108 | 890 | - | 0 | yes |
| uniform-16384 | wcc | `icebug` |  |  | - | 2.289 | 0.032 | 0.014 | - | 9.09 | - |  | 69 | 979 | - | 0 | yes |
| uniform-16384 | wcc | `icecat` |  |  | - | 1.073 | 0.006 | 0.006 | - | 6.46 | - |  | 67 | 1572 | - | 0 | yes |
| uniform-16384 | wcc | `grustcat` |  |  | - | 0.745 | 0.004 | 0.006 | - | 79.28 | - |  | 1 | 10816 | - | 0 | yes |
| uniform-16384 | wcc | `grust` | first | counted | - | 1.502 | 0.010 | 0.007 | - | 17.78 | - | needed | 176 | 2303 | 1031987 | 0 | yes |
| uniform-16384 | wcc | `grust` | second | counted | - | 0.812 | 0.020 | 0.025 | - | 17.78 | - | needed | 69 | 2303 | 1031987 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted` | first | counted | - | 0.865 | 0.004 | 0.005 | - | 10.29 | - | needed | 68 | 1579 | 1032002 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted` | second | counted | - | 0.774 | 0.040 | 0.051 | - | 10.29 | - | needed | 67 | 1579 | 1032002 | 0 | yes |
| uniform-65536 | bfs | `icebug` |  |  | - | 8.581 | 0.051 | 0.006 | - | 42.43 | - |  | 216 | 3889 | - | 0 | yes |
| uniform-65536 | bfs | `icecat` |  |  | - | 4.260 | 0.023 | 0.005 | - | 17.67 | - |  | 386 | 1681 | - | 0 | yes |
| uniform-65536 | bfs | `grustcat` |  |  | - | 4.380 | 0.053 | 0.012 | - | 366.18 | - |  | 0 | 36104 | - | 0 | yes |
| uniform-65536 | bfs | `grust` | first | counted | - | 4.752 | 0.074 | 0.015 | - | 69.37 | - | needed | 556 | 2089 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust` | second | counted | - | 3.936 | 0.065 | 0.017 | - | 69.37 | - | needed | 398 | 2089 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted` | first | counted | - | 4.027 | 0.036 | 0.009 | - | 36.70 | - | needed | 453 | 2921 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted` | second | counted | - | 3.672 | 0.088 | 0.024 | - | 36.70 | - | needed | 381 | 2921 | 4193790 | 0 | yes |
| uniform-65536 | pagerank | `neo4j-graph` |  |  | 34 | 16.092 | 0.099 | 0.006 | 0.473 | 14.45 | - |  | 173 | 940 | - | 0 | yes |
| uniform-65536 | pagerank | `icebug` |  |  | 11 | 7.140 | 0.119 | 0.017 | 0.649 | 42.42 | - |  | 489 | 3889 | - | 0 | yes |
| uniform-65536 | pagerank | `icecat` |  |  | 16 | 32.901 | 0.114 | 0.003 | 2.056 | 17.87 | - |  | 902 | 1680 | - | 0 | yes |
| uniform-65536 | pagerank | `grustcat` |  |  | 16 | 29.017 | 0.065 | 0.002 | 1.814 | 366.89 | - |  | 0 | 36105 | - | 0 | yes |
| uniform-65536 | pagerank | `grust` | first | counted | 16 | 16.797 | 0.193 | 0.012 | 1.050 | 71.03 | - | needed | 771 | 2089 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust` | second | counted | 16 | 8.792 | 0.059 | 0.007 | 0.549 | 71.03 | - | needed | 390 | 2089 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted` | first | counted | 16 | 7.853 | 0.125 | 0.016 | 0.491 | 42.37 | 6.23 | needed | 531 | 3119 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted` | second | counted | 16 | 7.651 | 0.185 | 0.024 | 0.478 | 42.37 | 6.23 | needed | 519 | 3119 | 16907315 | 0 | yes |
| uniform-65536 | triangles | `neo4j-graph` |  |  | - | 3.767 | 0.025 | 0.007 | - | 14.33 | - |  | 55 | 939 | - | 0 | yes |
| uniform-65536 | triangles | `grust` | first | counted | - | 31.271 | 0.047 | 0.002 | - | 88.12 | - | needed | 882 | 2093 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust` | second | counted | - | 29.248 | 0.032 | 0.001 | - | 88.12 | - | needed | 781 | 2093 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted` | first | counted | - | 29.744 | 0.088 | 0.003 | - | 41.49 | - | needed | 780 | 2418 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted` | second | counted | - | 28.824 | 0.535 | 0.019 | - | 41.49 | - | needed | 780 | 2418 | 15327135 | 0 | yes |
| uniform-65536 | wcc | `neo4j-graph` |  |  | - | 3.884 | 0.055 | 0.014 | - | 14.43 | - |  | 413 | 940 | - | 0 | yes |
| uniform-65536 | wcc | `icebug` |  |  | - | 12.821 | 0.074 | 0.006 | - | 42.63 | - |  | 243 | 3889 | - | 0 | yes |
| uniform-65536 | wcc | `icecat` |  |  | - | 4.349 | 0.006 | 0.001 | - | 17.73 | - |  | 258 | 1681 | - | 0 | yes |
| uniform-65536 | wcc | `grustcat` |  |  | - | 3.068 | 0.006 | 0.002 | - | 371.46 | - |  | 0 | 36104 | - | 0 | yes |
| uniform-65536 | wcc | `grust` | first | counted | - | 2.964 | 0.080 | 0.027 | - | 68.72 | - | needed | 370 | 2089 | 4128522 | 0 | yes |
| uniform-65536 | wcc | `grust` | second | counted | - | 2.234 | 0.085 | 0.038 | - | 68.72 | - | needed | 262 | 2089 | 4128522 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted` | first | counted | - | 2.368 | 0.080 | 0.034 | - | 37.17 | - | needed | 262 | 2919 | 4128521 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted` | second | counted | - | 2.249 | 0.071 | 0.032 | - | 37.17 | - | needed | 260 | 2919 | 4128521 | 0 | yes |

### `pinned-one-thread.json`: pinned-one-thread

workers 1, concurrency 1, allocator pinned: glibc.malloc.mmap_threshold=131072, 1 warmup + 5 repeats, steal over the run 1 ticks, 136.6 s, unusable at MAD/median >= 0.25

Not timed (no agreeing parity row): neo4j-graph pagerank layered-16384.edges, neo4j-graph pagerank layered-65536.edges, neo4j-graph pagerank path-16384.edges, neo4j-graph pagerank path-65536.edges 

| fixture | algorithm | participant | call | accounting | iters | total ms | MAD | MAD/median | per iter | build ms | incoming ms | prepare | minflt | minflt build | work units | steal | usable |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |
| hub-16384 | bfs | `icebug` |  |  | - | 1.423 | 0.003 | 0.002 | - | 9.11 | - |  | 57 | 1018 | - | 0 | yes |
| hub-16384 | bfs | `icecat` |  |  | - | 0.860 | 0.002 | 0.003 | - | 6.21 | - |  | 100 | 2083 | - | 0 | yes |
| hub-16384 | bfs | `grustcat` |  |  | - | 0.650 | 0.004 | 0.006 | - | 79.79 | - |  | 33 | 10354 | - | 0 | yes |
| hub-16384 | bfs | `grust#1` | first | counted | - | 1.601 | 0.012 | 0.008 | - | 17.45 | - | needed | 69 | 1792 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust#1` | second | counted | - | 1.776 | 0.010 | 0.006 | - | 17.45 | - | needed | 33 | 1792 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust#unset` | first | counted | - | 1.602 | 0.016 | 0.010 | - | 16.82 | - | needed | 69 | 1777 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust#unset` | second | counted | - | 1.509 | 0.011 | 0.008 | - | 16.82 | - | needed | 33 | 1777 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted#1` | first | counted | - | 1.571 | 0.011 | 0.007 | - | 9.68 | - | needed | 33 | 1231 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted#1` | second | counted | - | 1.542 | 0.001 | 0.001 | - | 9.68 | - | needed | 33 | 1231 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted#unset` | first | counted | - | 1.652 | 0.008 | 0.005 | - | 12.67 | - | needed | 69 | 1727 | 1047577 | 0 | yes |
| hub-16384 | bfs | `grust-next@counted#unset` | second | counted | - | 1.537 | 0.012 | 0.008 | - | 12.67 | - | needed | 33 | 1727 | 1047577 | 0 | yes |
| hub-16384 | pagerank | `neo4j-graph` |  |  | 36 | 13.105 | 0.065 | 0.005 | 0.364 | 7.61 | - |  | 24 | 718 | - | 0 | yes |
| hub-16384 | pagerank | `icebug` |  |  | 12 | 7.666 | 0.027 | 0.004 | 0.639 | 9.30 | - |  | 107 | 1018 | - | 0 | yes |
| hub-16384 | pagerank | `icecat` |  |  | 17 | 8.638 | 0.003 | 0.000 | 0.508 | 5.57 | - |  | 230 | 1572 | - | 0 | yes |
| hub-16384 | pagerank | `grustcat` |  |  | 17 | 7.431 | 0.016 | 0.002 | 0.437 | 79.77 | - |  | 99 | 10864 | - | 0 | yes |
| hub-16384 | pagerank | `grust#1` | first | counted | 17 | 11.594 | 0.021 | 0.002 | 0.682 | 17.14 | - | needed | 421 | 1792 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust#1` | second | counted | 17 | 9.775 | 0.005 | 0.000 | 0.575 | 17.14 | - | needed | 99 | 1792 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust#unset` | first | counted | 17 | 50.767 | 0.060 | 0.001 | 2.986 | 17.49 | - | needed | 165 | 1778 | 4567562 | 0 | yes |
| hub-16384 | pagerank | `grust#unset` | second | counted | 17 | 50.663 | 0.025 | 0.001 | 2.980 | 17.49 | - | needed | 165 | 1778 | 4567562 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted#1` | first | counted | 17 | 8.203 | 0.013 | 0.002 | 0.483 | 11.39 | 1.45 | needed | 99 | 2030 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted#1` | second | counted | 17 | 8.125 | 0.016 | 0.002 | 0.478 | 11.39 | 1.45 | needed | 99 | 2030 | 4403580 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted#unset` | first | counted | 17 | 23.494 | 0.021 | 0.001 | 1.382 | 12.68 | - | needed | 165 | 1217 | 4567562 | 0 | yes |
| hub-16384 | pagerank | `grust-next@counted#unset` | second | counted | 17 | 23.415 | 0.043 | 0.002 | 1.377 | 12.68 | - | needed | 165 | 1217 | 4567562 | 0 | yes |
| hub-16384 | triangles | `neo4j-graph` |  |  | - | 7.628 | 0.021 | 0.003 | - | 7.82 | - |  | 4 | 717 | - | 0 | yes |
| hub-16384 | triangles | `grust#1` | first | counted | - | 16.785 | 0.027 | 0.002 | - | 20.84 | - | needed | 455 | 1282 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust#1` | second | counted | - | 16.468 | 0.051 | 0.003 | - | 20.84 | - | needed | 455 | 1282 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust#unset` | first | counted | - | 16.764 | 0.060 | 0.004 | - | 20.90 | - | needed | 455 | 1268 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust#unset` | second | counted | - | 16.449 | 0.030 | 0.002 | - | 20.90 | - | needed | 455 | 1268 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted#1` | first | counted | - | 16.610 | 0.052 | 0.003 | - | 12.97 | - | needed | 422 | 1232 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted#1` | second | counted | - | 16.006 | 0.016 | 0.001 | - | 12.97 | - | needed | 422 | 1232 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted#unset` | first | counted | - | 16.714 | 0.040 | 0.002 | - | 16.15 | - | needed | 455 | 707 | 3742208 | 0 | yes |
| hub-16384 | triangles | `grust-next@counted#unset` | second | counted | - | 16.106 | 0.040 | 0.002 | - | 16.15 | - | needed | 455 | 707 | 3742208 | 0 | yes |
| hub-16384 | wcc | `neo4j-graph` |  |  | - | 1.197 | 0.010 | 0.008 | - | 7.89 | - |  | 99 | 718 | - | 0 | yes |
| hub-16384 | wcc | `icebug` |  |  | - | 1.963 | 0.021 | 0.011 | - | 9.27 | - |  | 69 | 1018 | - | 0 | yes |
| hub-16384 | wcc | `icecat` |  |  | - | 0.917 | 0.013 | 0.014 | - | 5.70 | - |  | 66 | 1572 | - | 0 | yes |
| hub-16384 | wcc | `grustcat` |  |  | - | 0.601 | 0.001 | 0.002 | - | 79.59 | - |  | 0 | 10864 | - | 0 | yes |
| hub-16384 | wcc | `grust#1` | first | counted | - | 1.625 | 0.026 | 0.016 | - | 17.15 | - | needed | 66 | 1792 | 1031191 | 0 | yes |
| hub-16384 | wcc | `grust#1` | second | counted | - | 1.569 | 0.007 | 0.005 | - | 17.15 | - | needed | 66 | 1792 | 1031191 | 0 | yes |
| hub-16384 | wcc | `grust#unset` | first | counted | - | 4.235 | 0.010 | 0.002 | - | 17.61 | - | needed | 66 | 2288 | 1324773 | 0 | yes |
| hub-16384 | wcc | `grust#unset` | second | counted | - | 4.204 | 0.001 | 0.000 | - | 17.61 | - | needed | 66 | 2288 | 1324773 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted#1` | first | counted | - | 1.502 | 0.012 | 0.008 | - | 10.01 | - | needed | 33 | 1742 | 1031191 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted#1` | second | counted | - | 1.543 | 0.011 | 0.007 | - | 10.01 | - | needed | 66 | 1742 | 1031191 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted#unset` | first | counted | - | 4.167 | 0.002 | 0.001 | - | 13.20 | - | needed | 66 | 1216 | 1324773 | 0 | yes |
| hub-16384 | wcc | `grust-next@counted#unset` | second | counted | - | 4.144 | 0.004 | 0.001 | - | 13.20 | - | needed | 66 | 1216 | 1324773 | 0 | yes |
| hub-65536 | bfs | `icebug` |  |  | - | 8.452 | 0.073 | 0.009 | - | 43.65 | - |  | 216 | 4057 | - | 0 | yes |
| hub-65536 | bfs | `icecat` |  |  | - | 4.505 | 0.033 | 0.007 | - | 18.99 | - |  | 388 | 2698 | - | 0 | yes |
| hub-65536 | bfs | `grustcat` |  |  | - | 4.614 | 0.204 | 0.044 | - | 371.80 | - |  | 129 | 38258 | - | 0 | yes |
| hub-65536 | bfs | `grust#1` | first | counted | - | 6.282 | 0.083 | 0.013 | - | 69.41 | - | needed | 420 | 2597 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust#1` | second | counted | - | 6.037 | 0.073 | 0.012 | - | 69.41 | - | needed | 372 | 2597 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust#unset` | first | counted | - | 6.986 | 0.062 | 0.009 | - | 69.40 | - | needed | 274 | 2581 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust#unset` | second | counted | - | 6.819 | 0.030 | 0.004 | - | 69.40 | - | needed | 274 | 2581 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted#1` | first | counted | - | 6.594 | 0.040 | 0.006 | - | 39.90 | - | needed | 435 | 2418 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted#1` | second | counted | - | 6.118 | 0.043 | 0.007 | - | 39.90 | - | needed | 372 | 2418 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted#unset` | first | counted | - | 7.275 | 0.083 | 0.011 | - | 49.09 | - | needed | 258 | 1842 | 4191009 | 0 | yes |
| hub-65536 | bfs | `grust-next@counted#unset` | second | counted | - | 6.954 | 0.117 | 0.017 | - | 49.09 | - | needed | 274 | 1842 | 4191009 | 0 | yes |
| hub-65536 | pagerank | `neo4j-graph` |  |  | 28 | 36.033 | 0.127 | 0.004 | 1.287 | 33.87 | - |  | 137 | 1299 | - | 0 | yes |
| hub-65536 | pagerank | `icebug` |  |  | 12 | 43.072 | 0.799 | 0.019 | 3.589 | 43.61 | - |  | 400 | 4057 | - | 0 | yes |
| hub-65536 | pagerank | `icecat` |  |  | 17 | 34.662 | 0.051 | 0.001 | 2.039 | 18.99 | - |  | 902 | 2698 | - | 0 | yes |
| hub-65536 | pagerank | `grustcat` |  |  | 17 | 30.563 | 0.090 | 0.003 | 1.798 | 369.48 | - |  | 387 | 38258 | - | 0 | yes |
| hub-65536 | pagerank | `grust#1` | first | counted | 17 | 53.303 | 0.053 | 0.001 | 3.135 | 70.76 | - | needed | 647 | 2596 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust#1` | second | counted | 17 | 45.663 | 0.073 | 0.002 | 2.686 | 70.76 | - | needed | 387 | 2596 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust#unset` | first | counted | 17 | 204.430 | 0.196 | 0.001 | 12.025 | 69.97 | - | needed | 645 | 2581 | 18272770 | 0 | yes |
| hub-65536 | pagerank | `grust#unset` | second | counted | 17 | 203.211 | 0.374 | 0.002 | 11.954 | 69.97 | - | needed | 645 | 2581 | 18272770 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted#1` | first | counted | 17 | 34.517 | 0.332 | 0.010 | 2.030 | 44.94 | 5.98 | needed | 516 | 2232 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted#1` | second | counted | 17 | 34.397 | 0.284 | 0.008 | 2.023 | 44.94 | 5.98 | needed | 516 | 2232 | 17616940 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted#unset` | first | counted | 17 | 95.384 | 0.685 | 0.007 | 5.611 | 49.10 | - | needed | 645 | 1843 | 18272770 | 0 | yes |
| hub-65536 | pagerank | `grust-next@counted#unset` | second | counted | 17 | 95.556 | 0.863 | 0.009 | 5.621 | 49.10 | - | needed | 645 | 1843 | 18272770 | 0 | yes |
| hub-65536 | triangles | `neo4j-graph` |  |  | - | 35.093 | 0.156 | 0.004 | - | 33.84 | - |  | 4 | 1299 | - | 0 | yes |
| hub-65536 | triangles | `grust#1` | first | counted | - | 73.728 | 0.710 | 0.010 | - | 85.42 | - | needed | 1290 | 3620 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust#1` | second | counted | - | 71.924 | 0.377 | 0.005 | - | 85.42 | - | needed | 1290 | 3620 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust#unset` | first | counted | - | 73.371 | 0.154 | 0.002 | - | 85.99 | - | needed | 1290 | 3605 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust#unset` | second | counted | - | 71.683 | 0.086 | 0.001 | - | 85.99 | - | needed | 1290 | 3605 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted#1` | first | counted | - | 71.710 | 0.345 | 0.005 | - | 50.76 | - | needed | 1290 | 2932 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted#1` | second | counted | - | 70.167 | 0.303 | 0.004 | - | 50.76 | - | needed | 1290 | 2932 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted#unset` | first | counted | - | 71.808 | 0.273 | 0.004 | - | 67.85 | - | needed | 1290 | 3377 | 14971727 | 0 | yes |
| hub-65536 | triangles | `grust-next@counted#unset` | second | counted | - | 70.238 | 0.324 | 0.005 | - | 67.85 | - | needed | 1290 | 3377 | 14971727 | 0 | yes |
| hub-65536 | wcc | `neo4j-graph` |  |  | - | 4.481 | 0.015 | 0.003 | - | 33.55 | - |  | 393 | 1299 | - | 1 | yes |
| hub-65536 | wcc | `icebug` |  |  | - | 11.359 | 0.055 | 0.005 | - | 43.62 | - |  | 240 | 4057 | - | 1 | yes |
| hub-65536 | wcc | `icecat` |  |  | - | 3.729 | 0.007 | 0.002 | - | 18.73 | - |  | 258 | 2698 | - | 1 | yes |
| hub-65536 | wcc | `grustcat` |  |  | - | 2.462 | 0.020 | 0.008 | - | 377.19 | - |  | 0 | 38259 | - | 1 | yes |
| hub-65536 | wcc | `grust#1` | first | counted | - | 6.835 | 0.015 | 0.002 | - | 70.05 | - | needed | 258 | 2596 | 4125471 | 1 | yes |
| hub-65536 | wcc | `grust#1` | second | counted | - | 6.715 | 0.033 | 0.005 | - | 70.05 | - | needed | 258 | 2596 | 4125471 | 1 | yes |
| hub-65536 | wcc | `grust#unset` | first | counted | - | 17.100 | 0.014 | 0.001 | - | 71.08 | - | needed | 258 | 2581 | 5303155 | 1 | yes |
| hub-65536 | wcc | `grust#unset` | second | counted | - | 16.983 | 0.008 | 0.000 | - | 71.08 | - | needed | 258 | 2581 | 5303155 | 1 | yes |
| hub-65536 | wcc | `grust-next@counted#1` | first | counted | - | 6.723 | 0.007 | 0.001 | - | 39.86 | - | needed | 258 | 2418 | 4125471 | 1 | yes |
| hub-65536 | wcc | `grust-next@counted#1` | second | counted | - | 6.590 | 0.029 | 0.004 | - | 39.86 | - | needed | 258 | 2418 | 4125471 | 1 | yes |
| hub-65536 | wcc | `grust-next@counted#unset` | first | counted | - | 16.970 | 0.003 | 0.000 | - | 50.13 | - | needed | 258 | 2353 | 5303155 | 1 | yes |
| hub-65536 | wcc | `grust-next@counted#unset` | second | counted | - | 16.788 | 0.033 | 0.002 | - | 50.13 | - | needed | 258 | 2353 | 5303155 | 1 | yes |
| layered-16384 | bfs | `icebug` |  |  | - | 0.492 | 0.011 | 0.023 | - | 2.79 | - |  | 36 | 458 | - | 0 | yes |
| layered-16384 | bfs | `icecat` |  |  | - | 0.394 | 0.001 | 0.004 | - | 1.58 | - |  | 67 | 543 | - | 0 | yes |
| layered-16384 | bfs | `grustcat` |  |  | - | 0.257 | 0.004 | 0.014 | - | 29.95 | - |  | 0 | 7383 | - | 0 | yes |
| layered-16384 | bfs | `grust#1` | first | counted | - | 0.518 | 0.012 | 0.023 | - | 6.81 | - | needed | 62 | 1036 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust#1` | second | counted | - | 0.509 | 0.005 | 0.010 | - | 6.81 | - | needed | 26 | 1036 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust#unset` | first | counted | - | 0.520 | 0.021 | 0.041 | - | 6.45 | - | needed | 62 | 1021 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust#unset` | second | counted | - | 0.437 | 0.002 | 0.004 | - | 6.45 | - | needed | 26 | 1021 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted#1` | first | counted | - | 0.458 | 0.003 | 0.007 | - | 4.87 | - | needed | 26 | 908 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted#1` | second | counted | - | 0.432 | 0.001 | 0.002 | - | 4.87 | - | needed | 26 | 908 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted#unset` | first | counted | - | 0.499 | 0.007 | 0.014 | - | 5.69 | - | needed | 61 | 894 | 347308 | 0 | yes |
| layered-16384 | bfs | `grust-next@counted#unset` | second | counted | - | 0.431 | 0.000 | 0.001 | - | 5.69 | - | needed | 26 | 894 | 347308 | 0 | yes |
| layered-16384 | pagerank | `icebug` |  |  | 69 | 26.251 | 0.085 | 0.003 | 0.380 | 2.77 | - |  | 114 | 458 | - | 0 | yes |
| layered-16384 | pagerank | `icecat` |  |  | 84 | 27.770 | 0.010 | 0.000 | 0.331 | 1.56 | - |  | 229 | 544 | - | 0 | yes |
| layered-16384 | pagerank | `grustcat` |  |  | 84 | 26.255 | 0.036 | 0.001 | 0.313 | 31.00 | - |  | 34 | 7383 | - | 0 | yes |
| layered-16384 | pagerank | `grust#1` | first | counted | 84 | 30.018 | 0.008 | 0.000 | 0.357 | 6.90 | - | needed | 229 | 1036 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust#1` | second | counted | 84 | 29.209 | 0.035 | 0.001 | 0.348 | 6.90 | - | needed | 99 | 1036 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust#unset` | first | counted | 84 | 115.501 | 0.084 | 0.001 | 1.375 | 6.80 | - | needed | 165 | 1021 | 8667337 | 0 | yes |
| layered-16384 | pagerank | `grust#unset` | second | counted | 84 | 115.340 | 0.041 | 0.000 | 1.373 | 6.80 | - | needed | 165 | 1021 | 8667337 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted#1` | first | counted | 84 | 30.750 | 0.030 | 0.001 | 0.366 | 5.87 | 0.55 | needed | 99 | 1004 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted#1` | second | counted | 84 | 30.709 | 0.040 | 0.001 | 0.366 | 5.87 | 0.55 | needed | 99 | 1004 | 7307112 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted#unset` | first | counted | 84 | 88.927 | 0.147 | 0.002 | 1.059 | 5.97 | - | needed | 165 | 894 | 8667337 | 0 | yes |
| layered-16384 | pagerank | `grust-next@counted#unset` | second | counted | 84 | 88.803 | 0.077 | 0.001 | 1.057 | 5.97 | - | needed | 165 | 894 | 8667337 | 0 | yes |
| layered-16384 | triangles | `neo4j-graph` |  |  | - | 0.783 | 0.009 | 0.012 | - | 2.29 | - |  | 3 | 459 | - | 0 | yes |
| layered-16384 | triangles | `grust#1` | first | counted | - | 2.836 | 0.018 | 0.006 | - | 6.70 | - | needed | 389 | 1162 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust#1` | second | counted | - | 2.818 | 0.020 | 0.007 | - | 6.70 | - | needed | 389 | 1162 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust#unset` | first | counted | - | 2.856 | 0.019 | 0.006 | - | 6.73 | - | needed | 389 | 1147 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust#unset` | second | counted | - | 2.806 | 0.019 | 0.007 | - | 6.73 | - | needed | 389 | 1147 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted#1` | first | counted | - | 2.884 | 0.005 | 0.002 | - | 5.68 | - | needed | 356 | 1034 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted#1` | second | counted | - | 2.668 | 0.018 | 0.007 | - | 5.68 | - | needed | 356 | 1034 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted#unset` | first | counted | - | 2.777 | 0.032 | 0.012 | - | 5.88 | - | needed | 389 | 1020 | 718265 | 0 | yes |
| layered-16384 | triangles | `grust-next@counted#unset` | second | counted | - | 2.741 | 0.010 | 0.004 | - | 5.88 | - | needed | 389 | 1020 | 718265 | 0 | yes |
| layered-16384 | wcc | `neo4j-graph` |  |  | - | 1.136 | 0.008 | 0.007 | - | 2.31 | - |  | 99 | 460 | - | 0 | yes |
| layered-16384 | wcc | `icebug` |  |  | - | 0.945 | 0.003 | 0.003 | - | 2.78 | - |  | 42 | 458 | - | 0 | yes |
| layered-16384 | wcc | `icecat` |  |  | - | 0.537 | 0.017 | 0.032 | - | 1.66 | - |  | 66 | 544 | - | 0 | yes |
| layered-16384 | wcc | `grustcat` |  |  | - | 0.352 | 0.000 | 0.001 | - | 29.81 | - |  | 0 | 6872 | - | 0 | yes |
| layered-16384 | wcc | `grust#1` | first | counted | - | 0.677 | 0.004 | 0.006 | - | 6.51 | - | needed | 66 | 1036 | 341578 | 0 | yes |
| layered-16384 | wcc | `grust#1` | second | counted | - | 0.675 | 0.006 | 0.009 | - | 6.51 | - | needed | 66 | 1036 | 341578 | 0 | yes |
| layered-16384 | wcc | `grust#unset` | first | counted | - | 1.497 | 0.003 | 0.002 | - | 6.49 | - | needed | 66 | 1021 | 438267 | 0 | yes |
| layered-16384 | wcc | `grust#unset` | second | counted | - | 1.476 | 0.004 | 0.003 | - | 6.49 | - | needed | 66 | 1021 | 438267 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted#1` | first | counted | - | 0.689 | 0.002 | 0.003 | - | 5.31 | - | needed | 33 | 908 | 341578 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted#1` | second | counted | - | 0.743 | 0.004 | 0.006 | - | 5.31 | - | needed | 66 | 908 | 341578 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted#unset` | first | counted | - | 1.496 | 0.018 | 0.012 | - | 5.51 | - | needed | 66 | 894 | 438267 | 0 | yes |
| layered-16384 | wcc | `grust-next@counted#unset` | second | counted | - | 1.465 | 0.003 | 0.002 | - | 5.51 | - | needed | 66 | 894 | 438267 | 0 | yes |
| layered-65536 | bfs | `icebug` |  |  | - | 2.016 | 0.004 | 0.002 | - | 11.08 | - |  | 132 | 1832 | - | 0 | yes |
| layered-65536 | bfs | `icecat` |  |  | - | 1.540 | 0.009 | 0.006 | - | 6.80 | - |  | 259 | 2163 | - | 0 | yes |
| layered-65536 | bfs | `grustcat` |  |  | - | 1.022 | 0.011 | 0.011 | - | 127.35 | - |  | 0 | 26649 | - | 0 | yes |
| layered-65536 | bfs | `grust#1` | first | counted | - | 2.037 | 0.011 | 0.005 | - | 27.93 | - | needed | 247 | 3146 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust#1` | second | counted | - | 2.267 | 0.006 | 0.002 | - | 27.93 | - | needed | 247 | 3146 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust#unset` | first | counted | - | 2.054 | 0.012 | 0.006 | - | 27.69 | - | needed | 247 | 2621 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust#unset` | second | counted | - | 2.002 | 0.004 | 0.002 | - | 27.69 | - | needed | 247 | 2621 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted#1` | first | counted | - | 2.013 | 0.010 | 0.005 | - | 20.69 | - | needed | 243 | 2641 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted#1` | second | counted | - | 1.961 | 0.018 | 0.009 | - | 20.69 | - | needed | 247 | 2641 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted#unset` | first | counted | - | 2.010 | 0.005 | 0.003 | - | 23.32 | - | needed | 243 | 2575 | 1393359 | 0 | yes |
| layered-65536 | bfs | `grust-next@counted#unset` | second | counted | - | 1.983 | 0.006 | 0.003 | - | 23.32 | - | needed | 247 | 2575 | 1393359 | 0 | yes |
| layered-65536 | pagerank | `icebug` |  |  | 60 | 91.615 | 0.067 | 0.001 | 1.527 | 11.16 | - |  | 401 | 1832 | - | 0 | yes |
| layered-65536 | pagerank | `icecat` |  |  | 75 | 99.835 | 0.041 | 0.000 | 1.331 | 6.63 | - |  | 901 | 2162 | - | 0 | yes |
| layered-65536 | pagerank | `grustcat` |  |  | 75 | 95.060 | 0.119 | 0.001 | 1.267 | 129.00 | - |  | 387 | 26650 | - | 0 | yes |
| layered-65536 | pagerank | `grust#1` | first | counted | 75 | 108.842 | 0.378 | 0.003 | 1.451 | 28.28 | - | needed | 899 | 3146 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust#1` | second | counted | 75 | 105.216 | 0.106 | 0.001 | 1.403 | 28.28 | - | needed | 387 | 3146 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust#unset` | first | counted | 75 | 413.646 | 0.040 | 0.000 | 5.515 | 27.89 | - | needed | 645 | 3131 | 31164642 | 0 | yes |
| layered-65536 | pagerank | `grust#unset` | second | counted | 75 | 413.158 | 0.045 | 0.000 | 5.509 | 27.89 | - | needed | 645 | 3131 | 31164642 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted#1` | first | counted | 75 | 111.382 | 0.097 | 0.001 | 1.485 | 23.43 | 2.51 | needed | 516 | 3217 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted#1` | second | counted | 75 | 110.898 | 0.043 | 0.000 | 1.479 | 23.43 | 2.51 | needed | 516 | 3217 | 26313822 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted#unset` | first | counted | 75 | 318.795 | 0.232 | 0.001 | 4.251 | 23.81 | - | needed | 645 | 2575 | 31164642 | 0 | yes |
| layered-65536 | pagerank | `grust-next@counted#unset` | second | counted | 75 | 318.377 | 0.319 | 0.001 | 4.245 | 23.81 | - | needed | 645 | 2575 | 31164642 | 0 | yes |
| layered-65536 | triangles | `neo4j-graph` |  |  | - | 2.761 | 0.017 | 0.006 | - | 8.65 | - |  | 4 | 1796 | - | 0 | yes |
| layered-65536 | triangles | `grust#1` | first | counted | - | 11.885 | 0.107 | 0.009 | - | 29.63 | - | needed | 1536 | 3654 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust#1` | second | counted | - | 11.145 | 0.046 | 0.004 | - | 29.63 | - | needed | 1536 | 3654 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust#unset` | first | counted | - | 11.854 | 0.019 | 0.002 | - | 29.60 | - | needed | 1536 | 3639 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust#unset` | second | counted | - | 11.124 | 0.026 | 0.002 | - | 29.60 | - | needed | 1536 | 3639 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted#1` | first | counted | - | 11.535 | 0.055 | 0.005 | - | 22.79 | - | needed | 1536 | 3148 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted#1` | second | counted | - | 10.787 | 0.050 | 0.005 | - | 22.79 | - | needed | 1536 | 3148 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted#unset` | first | counted | - | 11.468 | 0.024 | 0.002 | - | 25.35 | - | needed | 1536 | 3083 | 2877576 | 0 | yes |
| layered-65536 | triangles | `grust-next@counted#unset` | second | counted | - | 10.789 | 0.018 | 0.002 | - | 25.35 | - | needed | 1536 | 3083 | 2877576 | 0 | yes |
| layered-65536 | wcc | `neo4j-graph` |  |  | - | 4.190 | 0.019 | 0.005 | - | 8.40 | - |  | 393 | 1796 | - | 0 | yes |
| layered-65536 | wcc | `icebug` |  |  | - | 3.787 | 0.031 | 0.008 | - | 11.17 | - |  | 138 | 1832 | - | 0 | yes |
| layered-65536 | wcc | `icecat` |  |  | - | 1.996 | 0.024 | 0.012 | - | 6.39 | - |  | 258 | 2162 | - | 0 | yes |
| layered-65536 | wcc | `grustcat` |  |  | - | 1.408 | 0.004 | 0.003 | - | 128.84 | - |  | 0 | 26649 | - | 0 | yes |
| layered-65536 | wcc | `grust#1` | first | counted | - | 2.720 | 0.012 | 0.004 | - | 27.98 | - | needed | 258 | 3146 | 1368146 | 0 | yes |
| layered-65536 | wcc | `grust#1` | second | counted | - | 2.671 | 0.004 | 0.001 | - | 27.98 | - | needed | 258 | 3146 | 1368146 | 0 | yes |
| layered-65536 | wcc | `grust#unset` | first | counted | - | 5.975 | 0.004 | 0.001 | - | 28.32 | - | needed | 258 | 3131 | 1755282 | 0 | yes |
| layered-65536 | wcc | `grust#unset` | second | counted | - | 5.932 | 0.003 | 0.001 | - | 28.32 | - | needed | 258 | 3131 | 1755282 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted#1` | first | counted | - | 2.971 | 0.007 | 0.002 | - | 21.03 | - | needed | 258 | 2640 | 1368146 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted#1` | second | counted | - | 2.941 | 0.003 | 0.001 | - | 21.03 | - | needed | 258 | 2640 | 1368146 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted#unset` | first | counted | - | 5.948 | 0.007 | 0.001 | - | 24.00 | - | needed | 258 | 2575 | 1755282 | 0 | yes |
| layered-65536 | wcc | `grust-next@counted#unset` | second | counted | - | 5.898 | 0.007 | 0.001 | - | 24.00 | - | needed | 258 | 2575 | 1755282 | 0 | yes |
| path-16384 | bfs | `icebug` |  |  | - | 0.252 | 0.006 | 0.026 | - | 1.77 | - |  | 37 | 450 | - | 0 | yes |
| path-16384 | bfs | `icecat` |  |  | - | 0.288 | 0.004 | 0.013 | - | 0.87 | - |  | 66 | 292 | - | 0 | yes |
| path-16384 | bfs | `grustcat` |  |  | - | 0.143 | 0.000 | 0.002 | - | 24.02 | - |  | 0 | 6429 | - | 0 | yes |
| path-16384 | bfs | `grust#1` | first | counted | - | 0.478 | 0.006 | 0.012 | - | 4.99 | - | needed | 69 | 745 | 245755 | 0 | yes |
| path-16384 | bfs | `grust#1` | second | counted | - | 0.435 | 0.002 | 0.004 | - | 4.99 | - | needed | 33 | 745 | 245755 | 0 | yes |
| path-16384 | bfs | `grust#unset` | first | counted | - | 0.475 | 0.005 | 0.010 | - | 5.05 | - | needed | 69 | 731 | 245755 | 0 | yes |
| path-16384 | bfs | `grust#unset` | second | counted | - | 0.400 | 0.000 | 0.001 | - | 5.05 | - | needed | 33 | 731 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@counted#1` | first | counted | - | 0.448 | 0.001 | 0.002 | - | 4.02 | - | needed | 66 | 689 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@counted#1` | second | counted | - | 0.430 | 0.001 | 0.002 | - | 4.02 | - | needed | 66 | 689 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@counted#unset` | first | counted | - | 0.445 | 0.003 | 0.007 | - | 4.31 | - | needed | 69 | 674 | 245755 | 0 | yes |
| path-16384 | bfs | `grust-next@counted#unset` | second | counted | - | 0.388 | 0.001 | 0.002 | - | 4.31 | - | needed | 33 | 674 | 245755 | 0 | yes |
| path-16384 | pagerank | `icebug` |  |  | 54 | 12.791 | 0.029 | 0.002 | 0.237 | 1.74 | - |  | 113 | 450 | - | 0 | yes |
| path-16384 | pagerank | `icecat` |  |  | 58 | 11.322 | 0.004 | 0.000 | 0.195 | 0.91 | - |  | 230 | 293 | - | 0 | yes |
| path-16384 | pagerank | `grustcat` |  |  | 58 | 9.748 | 0.036 | 0.004 | 0.168 | 24.25 | - |  | 0 | 6429 | - | 0 | yes |
| path-16384 | pagerank | `grust#1` | first | counted | 58 | 14.767 | 0.028 | 0.002 | 0.255 | 5.03 | - | needed | 198 | 745 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust#1` | second | counted | 58 | 14.030 | 0.006 | 0.000 | 0.242 | 5.03 | - | needed | 99 | 745 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust#unset` | first | counted | 58 | 67.277 | 0.602 | 0.009 | 1.160 | 4.75 | - | needed | 165 | 730 | 5062591 | 0 | yes |
| path-16384 | pagerank | `grust#unset` | second | counted | 58 | 66.632 | 0.057 | 0.001 | 1.149 | 4.75 | - | needed | 165 | 730 | 5062591 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted#1` | first | counted | 58 | 14.691 | 0.036 | 0.002 | 0.253 | 4.59 | 0.46 | needed | 99 | 787 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted#1` | second | counted | 58 | 14.627 | 0.005 | 0.000 | 0.252 | 4.59 | 0.46 | needed | 99 | 787 | 4112319 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted#unset` | first | counted | 58 | 60.533 | 0.048 | 0.001 | 1.044 | 4.36 | - | needed | 165 | 674 | 5062591 | 0 | yes |
| path-16384 | pagerank | `grust-next@counted#unset` | second | counted | 58 | 60.539 | 0.052 | 0.001 | 1.044 | 4.36 | - | needed | 165 | 674 | 5062591 | 0 | yes |
| path-16384 | triangles | `neo4j-graph` |  |  | - | 0.246 | 0.007 | 0.029 | - | 1.49 | - |  | 3 | 335 | - | 0 | yes |
| path-16384 | triangles | `grust#1` | first | counted | - | 1.599 | 0.062 | 0.039 | - | 4.95 | - | needed | 295 | 807 | 425970 | 0 | yes |
| path-16384 | triangles | `grust#1` | second | counted | - | 1.542 | 0.003 | 0.002 | - | 4.95 | - | needed | 295 | 807 | 425970 | 0 | yes |
| path-16384 | triangles | `grust#unset` | first | counted | - | 1.679 | 0.048 | 0.029 | - | 5.12 | - | needed | 295 | 792 | 425970 | 0 | yes |
| path-16384 | triangles | `grust#unset` | second | counted | - | 1.553 | 0.010 | 0.007 | - | 5.12 | - | needed | 295 | 792 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted#1` | first | counted | - | 1.538 | 0.033 | 0.021 | - | 4.24 | - | needed | 262 | 751 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted#1` | second | counted | - | 1.481 | 0.019 | 0.013 | - | 4.24 | - | needed | 262 | 751 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted#unset` | first | counted | - | 1.570 | 0.003 | 0.002 | - | 4.57 | - | needed | 295 | 736 | 425970 | 0 | yes |
| path-16384 | triangles | `grust-next@counted#unset` | second | counted | - | 1.540 | 0.013 | 0.008 | - | 4.57 | - | needed | 295 | 736 | 425970 | 0 | yes |
| path-16384 | wcc | `neo4j-graph` |  |  | - | 0.906 | 0.008 | 0.009 | - | 1.47 | - |  | 99 | 334 | - | 0 | yes |
| path-16384 | wcc | `icebug` |  |  | - | 0.347 | 0.020 | 0.056 | - | 1.76 | - |  | 42 | 450 | - | 0 | yes |
| path-16384 | wcc | `icecat` |  |  | - | 0.280 | 0.003 | 0.012 | - | 0.84 | - |  | 67 | 292 | - | 0 | yes |
| path-16384 | wcc | `grustcat` |  |  | - | 0.158 | 0.001 | 0.006 | - | 24.41 | - |  | 0 | 6429 | - | 0 | yes |
| path-16384 | wcc | `grust#1` | first | counted | - | 0.490 | 0.003 | 0.006 | - | 4.80 | - | needed | 66 | 745 | 229369 | 0 | yes |
| path-16384 | wcc | `grust#1` | second | counted | - | 0.485 | 0.004 | 0.008 | - | 4.80 | - | needed | 66 | 745 | 229369 | 0 | yes |
| path-16384 | wcc | `grust#unset` | first | counted | - | 1.056 | 0.002 | 0.002 | - | 5.14 | - | needed | 66 | 730 | 294903 | 0 | yes |
| path-16384 | wcc | `grust#unset` | second | counted | - | 1.039 | 0.003 | 0.003 | - | 5.14 | - | needed | 66 | 730 | 294903 | 0 | yes |
| path-16384 | wcc | `grust-next@counted#1` | first | counted | - | 0.504 | 0.005 | 0.009 | - | 4.09 | - | needed | 66 | 689 | 229369 | 0 | yes |
| path-16384 | wcc | `grust-next@counted#1` | second | counted | - | 0.477 | 0.001 | 0.002 | - | 4.09 | - | needed | 65 | 689 | 229369 | 0 | yes |
| path-16384 | wcc | `grust-next@counted#unset` | first | counted | - | 1.050 | 0.006 | 0.006 | - | 4.37 | - | needed | 66 | 675 | 294903 | 0 | yes |
| path-16384 | wcc | `grust-next@counted#unset` | second | counted | - | 1.035 | 0.010 | 0.010 | - | 4.37 | - | needed | 66 | 675 | 294903 | 0 | yes |
| path-65536 | bfs | `icebug` |  |  | - | 0.942 | 0.009 | 0.010 | - | 7.06 | - |  | 132 | 1795 | - | 0 | yes |
| path-65536 | bfs | `icecat` |  |  | - | 1.126 | 0.004 | 0.004 | - | 4.25 | - |  | 258 | 1157 | - | 0 | yes |
| path-65536 | bfs | `grustcat` |  |  | - | 0.761 | 0.003 | 0.005 | - | 103.30 | - |  | 130 | 24249 | - | 0 | yes |
| path-65536 | bfs | `grust#1` | first | counted | - | 1.874 | 0.016 | 0.009 | - | 21.05 | - | needed | 274 | 2490 | 983035 | 0 | yes |
| path-65536 | bfs | `grust#1` | second | counted | - | 1.942 | 0.008 | 0.004 | - | 21.05 | - | needed | 274 | 2490 | 983035 | 0 | yes |
| path-65536 | bfs | `grust#unset` | first | counted | - | 1.862 | 0.016 | 0.009 | - | 21.05 | - | needed | 274 | 2475 | 983035 | 0 | yes |
| path-65536 | bfs | `grust#unset` | second | counted | - | 1.818 | 0.002 | 0.001 | - | 21.05 | - | needed | 274 | 2475 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@counted#1` | first | counted | - | 1.808 | 0.017 | 0.009 | - | 17.21 | - | needed | 272 | 2270 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@counted#1` | second | counted | - | 1.751 | 0.012 | 0.007 | - | 17.21 | - | needed | 274 | 2270 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@counted#unset` | first | counted | - | 1.817 | 0.015 | 0.008 | - | 18.45 | - | needed | 272 | 2205 | 983035 | 0 | yes |
| path-65536 | bfs | `grust-next@counted#unset` | second | counted | - | 1.740 | 0.003 | 0.002 | - | 18.45 | - | needed | 274 | 2205 | 983035 | 0 | yes |
| path-65536 | pagerank | `icebug` |  |  | 46 | 42.933 | 0.029 | 0.001 | 0.933 | 7.06 | - |  | 401 | 1795 | - | 0 | yes |
| path-65536 | pagerank | `icecat` |  |  | 50 | 39.495 | 0.039 | 0.001 | 0.790 | 4.21 | - |  | 901 | 1157 | - | 0 | yes |
| path-65536 | pagerank | `grustcat` |  |  | 50 | 35.577 | 0.205 | 0.006 | 0.712 | 102.61 | - |  | 516 | 24248 | - | 0 | yes |
| path-65536 | pagerank | `grust#1` | first | counted | 50 | 51.963 | 0.031 | 0.001 | 1.039 | 21.05 | - | needed | 774 | 2491 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust#1` | second | counted | 50 | 49.211 | 0.053 | 0.001 | 0.984 | 21.05 | - | needed | 387 | 2491 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust#unset` | first | counted | 50 | 230.930 | 0.053 | 0.000 | 4.619 | 21.13 | - | needed | 645 | 2475 | 17629127 | 0 | yes |
| path-65536 | pagerank | `grust#unset` | second | counted | 50 | 230.672 | 0.196 | 0.001 | 4.613 | 21.13 | - | needed | 645 | 2475 | 17629127 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted#1` | first | counted | 50 | 52.058 | 0.077 | 0.001 | 1.041 | 19.85 | 2.09 | needed | 516 | 2723 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted#1` | second | counted | 50 | 51.726 | 0.038 | 0.001 | 1.035 | 19.85 | 2.09 | needed | 516 | 2723 | 14352327 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted#unset` | first | counted | 50 | 209.988 | 0.144 | 0.001 | 4.200 | 19.67 | - | needed | 645 | 2716 | 17629127 | 0 | yes |
| path-65536 | pagerank | `grust-next@counted#unset` | second | counted | 50 | 209.643 | 0.059 | 0.000 | 4.193 | 19.67 | - | needed | 645 | 2716 | 17629127 | 0 | yes |
| path-65536 | triangles | `neo4j-graph` |  |  | - | 0.637 | 0.013 | 0.020 | - | 5.31 | - |  | 3 | 1294 | - | 0 | yes |
| path-65536 | triangles | `grust#1` | first | counted | - | 6.586 | 0.053 | 0.008 | - | 21.70 | - | needed | 1159 | 2744 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust#1` | second | counted | - | 5.967 | 0.031 | 0.005 | - | 21.70 | - | needed | 1159 | 2744 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust#unset` | first | counted | - | 6.507 | 0.042 | 0.007 | - | 21.27 | - | needed | 1159 | 2730 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust#unset` | second | counted | - | 5.982 | 0.043 | 0.007 | - | 21.27 | - | needed | 1159 | 2730 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted#1` | first | counted | - | 6.445 | 0.061 | 0.009 | - | 18.13 | - | needed | 1159 | 2524 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted#1` | second | counted | - | 5.959 | 0.004 | 0.001 | - | 18.13 | - | needed | 1159 | 2524 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted#unset` | first | counted | - | 6.511 | 0.059 | 0.009 | - | 19.42 | - | needed | 1159 | 2459 | 1703922 | 0 | yes |
| path-65536 | triangles | `grust-next@counted#unset` | second | counted | - | 6.004 | 0.041 | 0.007 | - | 19.42 | - | needed | 1159 | 2459 | 1703922 | 0 | yes |
| path-65536 | wcc | `neo4j-graph` |  |  | - | 3.336 | 0.010 | 0.003 | - | 5.19 | - |  | 393 | 1295 | - | 0 | yes |
| path-65536 | wcc | `icebug` |  |  | - | 1.224 | 0.009 | 0.008 | - | 6.98 | - |  | 138 | 1795 | - | 0 | yes |
| path-65536 | wcc | `icecat` |  |  | - | 1.084 | 0.008 | 0.008 | - | 4.16 | - |  | 258 | 1157 | - | 0 | yes |
| path-65536 | wcc | `grustcat` |  |  | - | 0.819 | 0.002 | 0.003 | - | 102.21 | - |  | 129 | 24248 | - | 0 | yes |
| path-65536 | wcc | `grust#1` | first | counted | - | 1.977 | 0.005 | 0.003 | - | 21.15 | - | needed | 258 | 2491 | 917497 | 0 | yes |
| path-65536 | wcc | `grust#1` | second | counted | - | 1.955 | 0.013 | 0.007 | - | 21.15 | - | needed | 258 | 2491 | 917497 | 0 | yes |
| path-65536 | wcc | `grust#unset` | first | counted | - | 4.216 | 0.013 | 0.003 | - | 21.08 | - | needed | 258 | 2476 | 1179639 | 0 | yes |
| path-65536 | wcc | `grust#unset` | second | counted | - | 4.163 | 0.010 | 0.003 | - | 21.08 | - | needed | 258 | 2476 | 1179639 | 0 | yes |
| path-65536 | wcc | `grust-next@counted#1` | first | counted | - | 2.004 | 0.019 | 0.009 | - | 17.48 | - | needed | 258 | 2270 | 917497 | 0 | yes |
| path-65536 | wcc | `grust-next@counted#1` | second | counted | - | 1.969 | 0.016 | 0.008 | - | 17.48 | - | needed | 258 | 2270 | 917497 | 0 | yes |
| path-65536 | wcc | `grust-next@counted#unset` | first | counted | - | 4.194 | 0.002 | 0.001 | - | 19.42 | - | needed | 258 | 2716 | 1179639 | 0 | yes |
| path-65536 | wcc | `grust-next@counted#unset` | second | counted | - | 4.149 | 0.005 | 0.001 | - | 19.42 | - | needed | 258 | 2716 | 1179639 | 0 | yes |
| uniform-16384 | bfs | `icebug` |  |  | - | 1.445 | 0.042 | 0.029 | - | 8.90 | - |  | 57 | 979 | - | 0 | yes |
| uniform-16384 | bfs | `icecat` |  |  | - | 0.916 | 0.015 | 0.016 | - | 6.66 | - |  | 99 | 2083 | - | 0 | yes |
| uniform-16384 | bfs | `grustcat` |  |  | - | 0.662 | 0.003 | 0.005 | - | 79.62 | - |  | 0 | 10816 | - | 0 | yes |
| uniform-16384 | bfs | `grust#1` | first | counted | - | 1.631 | 0.004 | 0.002 | - | 17.20 | - | needed | 68 | 2304 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust#1` | second | counted | - | 1.823 | 0.012 | 0.006 | - | 17.20 | - | needed | 32 | 2304 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust#unset` | first | counted | - | 1.648 | 0.008 | 0.005 | - | 17.36 | - | needed | 68 | 1779 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust#unset` | second | counted | - | 1.537 | 0.012 | 0.008 | - | 17.36 | - | needed | 32 | 1779 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted#1` | first | counted | - | 1.618 | 0.003 | 0.002 | - | 9.88 | - | needed | 32 | 1233 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted#1` | second | counted | - | 1.571 | 0.017 | 0.011 | - | 9.88 | - | needed | 32 | 1233 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted#unset` | first | counted | - | 1.675 | 0.008 | 0.005 | - | 12.86 | - | needed | 68 | 1728 | 1048343 | 0 | yes |
| uniform-16384 | bfs | `grust-next@counted#unset` | second | counted | - | 1.543 | 0.003 | 0.002 | - | 12.86 | - | needed | 32 | 1728 | 1048343 | 0 | yes |
| uniform-16384 | pagerank | `neo4j-graph` |  |  | 28 | 10.358 | 0.033 | 0.003 | 0.370 | 7.73 | - |  | 24 | 718 | - | 0 | yes |
| uniform-16384 | pagerank | `icebug` |  |  | 12 | 7.843 | 0.116 | 0.015 | 0.654 | 9.02 | - |  | 111 | 979 | - | 0 | yes |
| uniform-16384 | pagerank | `icecat` |  |  | 16 | 8.195 | 0.006 | 0.001 | 0.512 | 6.51 | - |  | 229 | 2084 | - | 0 | yes |
| uniform-16384 | pagerank | `grustcat` |  |  | 16 | 6.867 | 0.023 | 0.003 | 0.429 | 81.19 | - |  | 33 | 10816 | - | 0 | yes |
| uniform-16384 | pagerank | `grust#1` | first | counted | 16 | 11.172 | 0.036 | 0.003 | 0.698 | 16.85 | - | needed | 421 | 1793 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust#1` | second | counted | 16 | 9.370 | 0.017 | 0.002 | 0.586 | 16.85 | - | needed | 99 | 1793 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust#unset` | first | counted | 16 | 47.956 | 0.020 | 0.000 | 2.997 | 16.99 | - | needed | 165 | 1779 | 4373785 | 0 | yes |
| uniform-16384 | pagerank | `grust#unset` | second | counted | 16 | 47.894 | 0.020 | 0.000 | 2.993 | 16.99 | - | needed | 165 | 1779 | 4373785 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted#1` | first | counted | 16 | 7.718 | 0.008 | 0.001 | 0.482 | 10.73 | 1.40 | needed | 99 | 1521 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted#1` | second | counted | 16 | 7.656 | 0.003 | 0.000 | 0.478 | 10.73 | 1.40 | needed | 99 | 1521 | 4226299 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted#unset` | first | counted | 16 | 21.872 | 0.042 | 0.002 | 1.367 | 12.73 | - | needed | 165 | 1728 | 4373785 | 0 | yes |
| uniform-16384 | pagerank | `grust-next@counted#unset` | second | counted | 16 | 21.775 | 0.061 | 0.003 | 1.361 | 12.73 | - | needed | 165 | 1728 | 4373785 | 0 | yes |
| uniform-16384 | triangles | `neo4j-graph` |  |  | - | 8.610 | 0.050 | 0.006 | - | 7.76 | - |  | 4 | 717 | - | 0 | yes |
| uniform-16384 | triangles | `grust#1` | first | counted | - | 18.202 | 0.023 | 0.001 | - | 21.29 | - | needed | 455 | 1794 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust#1` | second | counted | - | 17.911 | 0.035 | 0.002 | - | 21.29 | - | needed | 455 | 1794 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust#unset` | first | counted | - | 18.555 | 0.301 | 0.016 | - | 20.88 | - | needed | 455 | 1269 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust#unset` | second | counted | - | 17.926 | 0.013 | 0.001 | - | 20.88 | - | needed | 455 | 1269 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted#1` | first | counted | - | 18.052 | 0.038 | 0.002 | - | 12.87 | - | needed | 422 | 1233 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted#1` | second | counted | - | 17.420 | 0.023 | 0.001 | - | 12.87 | - | needed | 422 | 1233 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted#unset` | first | counted | - | 18.079 | 0.014 | 0.001 | - | 16.29 | - | needed | 455 | 1218 | 3829630 | 0 | yes |
| uniform-16384 | triangles | `grust-next@counted#unset` | second | counted | - | 17.502 | 0.008 | 0.000 | - | 16.29 | - | needed | 455 | 1218 | 3829630 | 0 | yes |
| uniform-16384 | wcc | `neo4j-graph` |  |  | - | 1.206 | 0.008 | 0.007 | - | 7.78 | - |  | 99 | 718 | - | 0 | yes |
| uniform-16384 | wcc | `icebug` |  |  | - | 2.234 | 0.033 | 0.015 | - | 9.12 | - |  | 69 | 979 | - | 0 | yes |
| uniform-16384 | wcc | `icecat` |  |  | - | 1.070 | 0.004 | 0.004 | - | 6.29 | - |  | 66 | 2084 | - | 0 | yes |
| uniform-16384 | wcc | `grustcat` |  |  | - | 0.742 | 0.001 | 0.001 | - | 79.40 | - |  | 0 | 10305 | - | 0 | yes |
| uniform-16384 | wcc | `grust#1` | first | counted | - | 2.108 | 0.007 | 0.003 | - | 17.32 | - | needed | 66 | 2304 | 1031975 | 0 | yes |
| uniform-16384 | wcc | `grust#1` | second | counted | - | 2.097 | 0.021 | 0.010 | - | 17.32 | - | needed | 66 | 2304 | 1031975 | 0 | yes |
| uniform-16384 | wcc | `grust#unset` | first | counted | - | 4.222 | 0.004 | 0.001 | - | 17.26 | - | needed | 66 | 1778 | 1324427 | 0 | yes |
| uniform-16384 | wcc | `grust#unset` | second | counted | - | 4.202 | 0.004 | 0.001 | - | 17.26 | - | needed | 66 | 1778 | 1324427 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted#1` | first | counted | - | 2.316 | 0.004 | 0.002 | - | 9.84 | - | needed | 33 | 1743 | 1031975 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted#1` | second | counted | - | 2.376 | 0.012 | 0.005 | - | 9.84 | - | needed | 66 | 1743 | 1031975 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted#unset` | first | counted | - | 4.173 | 0.009 | 0.002 | - | 12.14 | - | needed | 66 | 1217 | 1324427 | 0 | yes |
| uniform-16384 | wcc | `grust-next@counted#unset` | second | counted | - | 4.147 | 0.000 | 0.000 | - | 12.14 | - | needed | 66 | 1217 | 1324427 | 0 | yes |
| uniform-65536 | bfs | `icebug` |  |  | - | 8.338 | 0.109 | 0.013 | - | 41.98 | - |  | 217 | 3889 | - | 0 | yes |
| uniform-65536 | bfs | `icecat` |  |  | - | 4.199 | 0.030 | 0.007 | - | 17.55 | - |  | 386 | 1680 | - | 0 | yes |
| uniform-65536 | bfs | `grustcat` |  |  | - | 4.430 | 0.040 | 0.009 | - | 367.15 | - |  | 0 | 36104 | - | 0 | yes |
| uniform-65536 | bfs | `grust#1` | first | counted | - | 6.400 | 0.055 | 0.009 | - | 68.69 | - | needed | 428 | 2089 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust#1` | second | counted | - | 6.096 | 0.005 | 0.001 | - | 68.69 | - | needed | 380 | 2089 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust#unset` | first | counted | - | 6.928 | 0.035 | 0.005 | - | 68.96 | - | needed | 273 | 2074 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust#unset` | second | counted | - | 6.720 | 0.017 | 0.003 | - | 68.96 | - | needed | 273 | 2074 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted#1` | first | counted | - | 6.715 | 0.047 | 0.007 | - | 37.68 | - | needed | 420 | 1400 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted#1` | second | counted | - | 6.197 | 0.012 | 0.002 | - | 37.68 | - | needed | 380 | 1400 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted#unset` | first | counted | - | 7.171 | 0.032 | 0.004 | - | 48.36 | - | needed | 257 | 1336 | 4193790 | 0 | yes |
| uniform-65536 | bfs | `grust-next@counted#unset` | second | counted | - | 6.843 | 0.011 | 0.002 | - | 48.36 | - | needed | 273 | 1336 | 4193790 | 0 | yes |
| uniform-65536 | pagerank | `neo4j-graph` |  |  | 34 | 43.987 | 0.029 | 0.001 | 1.294 | 33.29 | - |  | 138 | 788 | - | 0 | yes |
| uniform-65536 | pagerank | `icebug` |  |  | 11 | 38.969 | 0.240 | 0.006 | 3.543 | 42.46 | - |  | 398 | 3889 | - | 0 | yes |
| uniform-65536 | pagerank | `icecat` |  |  | 16 | 32.830 | 0.062 | 0.002 | 2.052 | 17.85 | - |  | 902 | 1681 | - | 0 | yes |
| uniform-65536 | pagerank | `grustcat` |  |  | 16 | 28.850 | 0.099 | 0.003 | 1.803 | 371.29 | - |  | 0 | 36105 | - | 0 | yes |
| uniform-65536 | pagerank | `grust#1` | first | counted | 16 | 50.343 | 0.126 | 0.002 | 3.146 | 68.76 | - | needed | 647 | 2089 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust#1` | second | counted | 16 | 42.999 | 0.052 | 0.001 | 2.687 | 68.76 | - | needed | 387 | 2089 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust#unset` | first | counted | 16 | 192.561 | 0.261 | 0.001 | 12.035 | 68.83 | - | needed | 645 | 2074 | 17497177 | 0 | yes |
| uniform-65536 | pagerank | `grust#unset` | second | counted | 16 | 192.885 | 0.834 | 0.004 | 12.055 | 68.83 | - | needed | 645 | 2074 | 17497177 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted#1` | first | counted | 16 | 32.178 | 0.394 | 0.012 | 2.011 | 45.21 | 5.93 | needed | 516 | 2236 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted#1` | second | counted | 16 | 31.989 | 0.301 | 0.009 | 1.999 | 45.21 | 5.93 | needed | 516 | 2236 | 16907315 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted#unset` | first | counted | 16 | 89.061 | 0.284 | 0.003 | 5.566 | 49.72 | - | needed | 645 | 1846 | 17497177 | 0 | yes |
| uniform-65536 | pagerank | `grust-next@counted#unset` | second | counted | 16 | 88.792 | 0.178 | 0.002 | 5.550 | 49.72 | - | needed | 645 | 1846 | 17497177 | 0 | yes |
| uniform-65536 | triangles | `neo4j-graph` |  |  | - | 39.250 | 0.057 | 0.001 | - | 32.96 | - |  | 4 | 789 | - | 0 | yes |
| uniform-65536 | triangles | `grust#1` | first | counted | - | 78.905 | 0.042 | 0.001 | - | 87.57 | - | needed | 780 | 2093 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust#1` | second | counted | - | 77.205 | 0.137 | 0.002 | - | 87.57 | - | needed | 780 | 2093 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust#unset` | first | counted | - | 78.908 | 0.025 | 0.000 | - | 90.05 | - | needed | 780 | 2078 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust#unset` | second | counted | - | 77.345 | 0.032 | 0.000 | - | 90.05 | - | needed | 780 | 2078 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted#1` | first | counted | - | 77.409 | 0.117 | 0.002 | - | 53.76 | - | needed | 780 | 1915 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted#1` | second | counted | - | 75.635 | 0.228 | 0.003 | - | 53.76 | - | needed | 780 | 1915 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted#unset` | first | counted | - | 77.304 | 0.064 | 0.001 | - | 69.81 | - | needed | 780 | 1850 | 15327135 | 0 | yes |
| uniform-65536 | triangles | `grust-next@counted#unset` | second | counted | - | 76.063 | 0.163 | 0.002 | - | 69.81 | - | needed | 780 | 1850 | 15327135 | 0 | yes |
| uniform-65536 | wcc | `neo4j-graph` |  |  | - | 4.489 | 0.019 | 0.004 | - | 32.70 | - |  | 393 | 789 | - | 0 | yes |
| uniform-65536 | wcc | `icebug` |  |  | - | 12.813 | 0.259 | 0.020 | - | 41.88 | - |  | 243 | 3889 | - | 0 | yes |
| uniform-65536 | wcc | `icecat` |  |  | - | 4.340 | 0.005 | 0.001 | - | 17.88 | - |  | 259 | 1680 | - | 0 | yes |
| uniform-65536 | wcc | `grustcat` |  |  | - | 3.060 | 0.005 | 0.002 | - | 368.16 | - |  | 0 | 36104 | - | 0 | yes |
| uniform-65536 | wcc | `grust#1` | first | counted | - | 8.872 | 0.016 | 0.002 | - | 68.02 | - | needed | 258 | 2089 | 4128495 | 0 | yes |
| uniform-65536 | wcc | `grust#1` | second | counted | - | 8.832 | 0.028 | 0.003 | - | 68.02 | - | needed | 258 | 2089 | 4128495 | 0 | yes |
| uniform-65536 | wcc | `grust#unset` | first | counted | - | 17.294 | 0.059 | 0.003 | - | 69.20 | - | needed | 258 | 2074 | 5298822 | 0 | yes |
| uniform-65536 | wcc | `grust#unset` | second | counted | - | 17.163 | 0.022 | 0.001 | - | 69.20 | - | needed | 258 | 2074 | 5298822 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted#1` | first | counted | - | 10.033 | 0.038 | 0.004 | - | 39.08 | - | needed | 258 | 1911 | 4128495 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted#1` | second | counted | - | 9.932 | 0.059 | 0.006 | - | 39.08 | - | needed | 258 | 1911 | 4128495 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted#unset` | first | counted | - | 17.327 | 0.045 | 0.003 | - | 50.29 | - | needed | 258 | 1846 | 5298822 | 0 | yes |
| uniform-65536 | wcc | `grust-next@counted#unset` | second | counted | - | 17.131 | 0.041 | 0.002 | - | 50.29 | - | needed | 258 | 1846 | 5298822 | 0 | yes |

### `xlarge-full-width.json`: xlarge-full-width

workers 16, concurrency 16, allocator glibc default, not pinned, 1 warmup + 5 repeats, steal over the run 7 ticks, 1548.6 s, unusable at MAD/median >= 0.25

| fixture | algorithm | participant | call | accounting | iters | total ms | MAD | MAD/median | per iter | build ms | incoming ms | prepare | minflt | minflt build | work units | steal | usable |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |
| hub-4194304 | pagerank | `neo4j-graph` |  |  | 18 | 388.186 | 36.494 | 0.094 | 21.566 | 869.93 | - |  | 1125 | 4739 | - | 4 | yes |
| hub-4194304 | pagerank | `icebug` |  |  | 10 | 1089.025 | 2.762 | 0.003 | 108.902 | 6926.28 | - |  | 1686 | 210997 | - | 4 | yes |
| hub-4194304 | pagerank | `icecat` |  |  | 16 | 5549.368 | 15.719 | 0.003 | 346.835 | 1151.82 | - |  | 19025 | 7448 | - | 4 | yes |
| hub-4194304 | pagerank | `grustcat` |  |  | 16 | 5934.813 | 32.054 | 0.005 | 370.926 | 41501.18 | - |  | 10832 | 2169565 | - | 4 | yes |
| hub-4194304 | pagerank | `grust` | first | counted | 16 | 2780.117 | 7.493 | 0.003 | 173.757 | 7733.75 | - | needed | 3450 | 38314 | 1081412859 | 4 | yes |
| hub-4194304 | pagerank | `grust` | second | counted | 16 | 1347.791 | 3.818 | 0.003 | 84.237 | 7733.75 | - | needed | 1604 | 38314 | 1081412859 | 4 | yes |
| hub-4194304 | pagerank | `grust-next@counted` | first | counted | 16 | 734.537 | 19.960 | 0.027 | 45.909 | 3150.97 | 516.00 | needed | 1707 | 39016 | 1081412859 | 4 | yes |
| hub-4194304 | pagerank | `grust-next@counted` | second | counted | 16 | 710.508 | 15.550 | 0.022 | 44.407 | 3150.97 | 516.00 | needed | 1613 | 39016 | 1081412859 | 4 | yes |
| hub-4194304 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 16 | 714.564 | 8.582 | 0.012 | 44.660 | 2651.23 | 464.80 | needed | 1707 | 39015 | - | 4 | yes |
| hub-4194304 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 16 | 690.579 | 2.439 | 0.004 | 43.161 | 2651.23 | 464.80 | needed | 1620 | 39015 | - | 4 | yes |
| hub-4194304 | pagerank | `grust-next@unchecked` | first | unchecked | 16 | 685.875 | 10.294 | 0.015 | 42.867 | 2640.82 | 471.74 | needed | 1707 | 39014 | - | 4 | yes |
| hub-4194304 | pagerank | `grust-next@unchecked` | second | unchecked | 16 | 691.143 | 9.547 | 0.014 | 43.196 | 2640.82 | 471.74 | needed | 1623 | 39014 | - | 4 | yes |
| uniform-4194304 | pagerank | `neo4j-graph` |  |  | 29 | 578.253 | 1.814 | 0.003 | 19.940 | 881.42 | - |  | 1120 | 1863 | - | 3 | yes |
| uniform-4194304 | pagerank | `icebug` |  |  | 9 | 1041.135 | 8.755 | 0.008 | 115.682 | 6389.36 | - |  | 1688 | 200030 | - | 3 | yes |
| uniform-4194304 | pagerank | `icecat` |  |  | 16 | 5928.574 | 73.205 | 0.012 | 370.536 | 1217.80 | - |  | 18513 | 6154 | - | 3 | yes |
| uniform-4194304 | pagerank | `grustcat` |  |  | 16 | 7109.014 | 114.640 | 0.016 | 444.313 | 43605.91 | - |  | 17 | 2157409 | - | 3 | yes |
| uniform-4194304 | pagerank | `grust` | first | counted | 16 | 2833.464 | 22.817 | 0.008 | 177.092 | 7818.53 | - | needed | 2483 | 36151 | 1082129509 | 3 | yes |
| uniform-4194304 | pagerank | `grust` | second | counted | 16 | 1446.167 | 3.870 | 0.003 | 90.385 | 7818.53 | - | needed | 1095 | 36151 | 1082129509 | 3 | yes |
| uniform-4194304 | pagerank | `grust-next@counted` | first | counted | 16 | 747.764 | 13.217 | 0.018 | 46.735 | 3219.84 | 547.74 | needed | 1194 | 37421 | 1082129509 | 3 | yes |
| uniform-4194304 | pagerank | `grust-next@counted` | second | counted | 16 | 750.560 | 21.852 | 0.029 | 46.910 | 3219.84 | 547.74 | needed | 1103 | 37421 | 1082129509 | 3 | yes |
| uniform-4194304 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 16 | 735.390 | 11.019 | 0.015 | 45.962 | 2752.22 | 504.62 | needed | 1199 | 36908 | - | 3 | yes |
| uniform-4194304 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 16 | 736.145 | 8.993 | 0.012 | 46.009 | 2752.22 | 504.62 | needed | 1115 | 36908 | - | 3 | yes |
| uniform-4194304 | pagerank | `grust-next@unchecked` | first | unchecked | 16 | 720.942 | 15.135 | 0.021 | 45.059 | 2708.37 | 496.41 | needed | 1200 | 36400 | - | 3 | yes |
| uniform-4194304 | pagerank | `grust-next@unchecked` | second | unchecked | 16 | 719.298 | 9.369 | 0.013 | 44.956 | 2708.37 | 496.41 | needed | 1109 | 36400 | - | 3 | yes |

### `xlarge-one-thread.json`: xlarge-one-thread

workers 1, concurrency 1, allocator glibc default, not pinned, 1 warmup + 5 repeats, steal over the run 129 ticks, 4297.7 s, unusable at MAD/median >= 0.25

| fixture | algorithm | participant | call | accounting | iters | total ms | MAD | MAD/median | per iter | build ms | incoming ms | prepare | minflt | minflt build | work units | steal | usable |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |
| hub-4194304 | pagerank | `neo4j-graph` |  |  | 23 | 4610.199 | 513.815 | 0.111 | 200.443 | 6594.12 | - |  | 1045 | 3463 | - | 121 | yes |
| hub-4194304 | pagerank | `icebug` |  |  | 10 | 9735.125 | 74.544 | 0.008 | 973.512 | 6965.18 | - |  | 1598 | 210997 | - | 121 | yes |
| hub-4194304 | pagerank | `icecat` |  |  | 16 | 5627.610 | 16.786 | 0.003 | 351.726 | 1150.46 | - |  | 19024 | 7430 | - | 121 | yes |
| hub-4194304 | pagerank | `grustcat` |  |  | 16 | 6040.221 | 40.645 | 0.007 | 377.514 | 42001.96 | - |  | 10832 | 2170078 | - | 121 | yes |
| hub-4194304 | pagerank | `grust#1` | first | counted | 16 | 12663.281 | 36.710 | 0.003 | 791.455 | 7687.17 | - | needed | 3227 | 37803 | 1081412859 | 121 | yes |
| hub-4194304 | pagerank | `grust#1` | second | counted | 16 | 11300.514 | 50.551 | 0.004 | 706.282 | 7687.17 | - | needed | 1584 | 37803 | 1081412859 | 121 | yes |
| hub-4194304 | pagerank | `grust#unset` | first | counted | 16 | 26184.631 | 328.736 | 0.013 | 1636.539 | 7818.23 | - | needed | 2640 | 38300 | 1119190297 | 121 | yes |
| hub-4194304 | pagerank | `grust#unset` | second | counted | 16 | 26010.008 | 279.412 | 0.011 | 1625.626 | 7818.23 | - | needed | 2640 | 38300 | 1119190297 | 121 | yes |
| hub-4194304 | pagerank | `grust-next@counted#1` | first | counted | 16 | 6941.344 | 23.396 | 0.003 | 433.834 | 4173.53 | 1184.65 | needed | 2112 | 40197 | 1081412859 | 121 | yes |
| hub-4194304 | pagerank | `grust-next@counted#1` | second | counted | 16 | 6969.360 | 27.735 | 0.004 | 435.585 | 4173.53 | 1184.65 | needed | 2112 | 40197 | 1081412859 | 121 | yes |
| hub-4194304 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 16 | 6696.584 | 21.591 | 0.003 | 418.536 | 3626.40 | 1141.38 | needed | 2112 | 39685 | - | 121 | yes |
| hub-4194304 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 16 | 6744.069 | 101.711 | 0.015 | 421.504 | 3626.40 | 1141.38 | needed | 2112 | 39685 | - | 121 | yes |
| hub-4194304 | pagerank | `grust-next@unchecked#1` | first | unchecked | 16 | 6493.191 | 37.520 | 0.006 | 405.824 | 3642.73 | 1151.13 | needed | 2112 | 39685 | - | 121 | yes |
| hub-4194304 | pagerank | `grust-next@unchecked#1` | second | unchecked | 16 | 6435.537 | 47.902 | 0.007 | 402.221 | 3642.73 | 1151.13 | needed | 2112 | 39685 | - | 121 | yes |
| hub-4194304 | pagerank | `grust-next@counted#unset` | first | counted | 16 | 13050.807 | 144.211 | 0.011 | 815.675 | 3595.17 | - | needed | 2640 | 38029 | 1119190297 | 121 | yes |
| hub-4194304 | pagerank | `grust-next@counted#unset` | second | counted | 16 | 12936.738 | 26.412 | 0.002 | 808.546 | 3595.17 | - | needed | 2640 | 38029 | 1119190297 | 121 | yes |
| hub-4194304 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 16 | 10628.128 | 52.990 | 0.005 | 664.258 | 2676.13 | - | needed | 2640 | 37007 | - | 121 | yes |
| hub-4194304 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 16 | 10538.512 | 42.893 | 0.004 | 658.657 | 2676.13 | - | needed | 2640 | 37007 | - | 121 | yes |
| hub-4194304 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 16 | 10623.605 | 256.945 | 0.024 | 663.975 | 2620.30 | - | needed | 2640 | 38029 | - | 121 | yes |
| hub-4194304 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 16 | 10370.789 | 35.142 | 0.003 | 648.174 | 2620.30 | - | needed | 2640 | 38029 | - | 121 | yes |
| uniform-4194304 | pagerank | `neo4j-graph` |  |  | 29 | 5387.873 | 359.628 | 0.067 | 185.789 | 6315.85 | - |  | 1046 | 2153 | - | 8 | yes |
| uniform-4194304 | pagerank | `icebug` |  |  | 9 | 9144.445 | 104.250 | 0.011 | 1016.049 | 6368.66 | - |  | 1592 | 200030 | - | 8 | yes |
| uniform-4194304 | pagerank | `icecat` |  |  | 16 | 5853.907 | 22.436 | 0.004 | 365.869 | 1150.67 | - |  | 18513 | 6154 | - | 8 | yes |
| uniform-4194304 | pagerank | `grustcat` |  |  | 16 | 7113.242 | 94.558 | 0.013 | 444.578 | 42988.10 | - |  | 17 | 2157409 | - | 8 | yes |
| uniform-4194304 | pagerank | `grust#1` | first | counted | 16 | 13286.454 | 45.867 | 0.003 | 830.403 | 7701.95 | - | needed | 2261 | 36151 | 1082129509 | 8 | yes |
| uniform-4194304 | pagerank | `grust#1` | second | counted | 16 | 11878.256 | 54.010 | 0.005 | 742.391 | 7701.95 | - | needed | 1073 | 36151 | 1082129509 | 8 | yes |
| uniform-4194304 | pagerank | `grust#unset` | first | counted | 16 | 24235.234 | 476.778 | 0.020 | 1514.702 | 7698.39 | - | needed | 2129 | 36151 | 1119878281 | 8 | yes |
| uniform-4194304 | pagerank | `grust#unset` | second | counted | 16 | 24393.093 | 778.503 | 0.032 | 1524.568 | 7698.39 | - | needed | 2129 | 36151 | 1119878281 | 8 | yes |
| uniform-4194304 | pagerank | `grust-next@counted#1` | first | counted | 16 | 7030.834 | 59.570 | 0.008 | 439.427 | 4112.13 | 1173.68 | needed | 2112 | 37579 | 1082129509 | 8 | yes |
| uniform-4194304 | pagerank | `grust-next@counted#1` | second | counted | 16 | 7036.390 | 65.962 | 0.009 | 439.774 | 4112.13 | 1173.68 | needed | 2112 | 37579 | 1082129509 | 8 | yes |
| uniform-4194304 | pagerank | `grust-next@work-uncounted#1` | first | work-uncounted | 16 | 6737.939 | 17.016 | 0.003 | 421.121 | 3576.12 | 1112.48 | needed | 2112 | 37579 | - | 8 | yes |
| uniform-4194304 | pagerank | `grust-next@work-uncounted#1` | second | work-uncounted | 16 | 6734.283 | 12.462 | 0.002 | 420.893 | 3576.12 | 1112.48 | needed | 2112 | 37579 | - | 8 | yes |
| uniform-4194304 | pagerank | `grust-next@unchecked#1` | first | unchecked | 16 | 6604.334 | 13.993 | 0.002 | 412.771 | 3610.13 | 1121.66 | needed | 2112 | 37579 | - | 8 | yes |
| uniform-4194304 | pagerank | `grust-next@unchecked#1` | second | unchecked | 16 | 6618.004 | 29.723 | 0.004 | 413.625 | 3610.13 | 1121.66 | needed | 2112 | 37579 | - | 8 | yes |
| uniform-4194304 | pagerank | `grust-next@counted#unset` | first | counted | 16 | 12327.003 | 48.969 | 0.004 | 770.438 | 3558.65 | - | needed | 2129 | 35867 | 1119878281 | 8 | yes |
| uniform-4194304 | pagerank | `grust-next@counted#unset` | second | counted | 16 | 12394.911 | 269.459 | 0.022 | 774.682 | 3558.65 | - | needed | 2129 | 35867 | 1119878281 | 8 | yes |
| uniform-4194304 | pagerank | `grust-next@work-uncounted#unset` | first | work-uncounted | 16 | 10187.555 | 121.807 | 0.012 | 636.722 | 2631.62 | - | needed | 2129 | 35867 | - | 8 | yes |
| uniform-4194304 | pagerank | `grust-next@work-uncounted#unset` | second | work-uncounted | 16 | 10042.719 | 136.600 | 0.014 | 627.670 | 2631.62 | - | needed | 2129 | 35867 | - | 8 | yes |
| uniform-4194304 | pagerank | `grust-next@unchecked#unset` | first | unchecked | 16 | 10020.108 | 338.234 | 0.034 | 626.257 | 2579.59 | - | needed | 2129 | 35867 | - | 8 | yes |
| uniform-4194304 | pagerank | `grust-next@unchecked#unset` | second | unchecked | 16 | 9926.584 | 207.571 | 0.021 | 620.411 | 2579.59 | - | needed | 2129 | 35867 | - | 8 | yes |

