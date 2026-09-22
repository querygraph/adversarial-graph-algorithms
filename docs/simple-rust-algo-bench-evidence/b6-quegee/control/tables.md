### `large-full-width-control.json`: large-full-width-control2

workers 16, concurrency 16, allocator glibc default, not pinned, 1 warmup + 5 repeats, steal over the run 4 ticks, 810.0 s, unusable at MAD/median >= 0.25

| fixture | algorithm | participant | call | accounting | iters | total ms | MAD | MAD/median | per iter | build ms | incoming ms | prepare | minflt | minflt build | work units | steal | usable |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |
| hub-2097152 | pagerank | `neo4j-graph` |  |  | 28 | 275.658 | 1.118 | 0.004 | 9.845 | 459.51 | - |  | 1119 | 4013 | - | 2 | yes |
| hub-2097152 | pagerank | `icebug` |  |  | 10 | 530.389 | 10.804 | 0.020 | 53.039 | 3622.89 | - |  | 1677 | 106004 | - | 2 | yes |
| hub-2097152 | pagerank | `icecat` |  |  | 16 | 3101.102 | 81.858 | 0.026 | 193.819 | 602.96 | - |  | 10705 | 6456 | - | 2 | yes |
| hub-2097152 | pagerank | `grustcat` |  |  | 16 | 3303.962 | 64.003 | 0.019 | 206.498 | 20459.56 | - |  | 6626 | 1090034 | - | 2 | yes |
| hub-2097152 | pagerank | `grust` | first | counted | 16 | 1396.680 | 12.950 | 0.009 | 87.293 | 4116.32 | - | needed | 3305 | 20942 | 540705943 | 2 | yes |
| hub-2097152 | pagerank | `grust` | second | counted | 16 | 599.372 | 17.262 | 0.029 | 37.461 | 4116.32 | - | needed | 16 | 20942 | 540705943 | 2 | yes |
| hub-2097152 | pagerank | `grust-next@counted` | first | counted | 16 | 286.179 | 7.794 | 0.027 | 17.886 | 1692.61 | 260.45 | needed | 1622 | 22631 | 540705943 | 2 | yes |
| hub-2097152 | pagerank | `grust-next@counted` | second | counted | 16 | 307.201 | 25.791 | 0.084 | 19.200 | 1692.61 | 260.45 | needed | 2057 | 22631 | 540705943 | 2 | yes |
| hub-2097152 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 16 | 297.974 | 12.618 | 0.042 | 18.623 | 1456.14 | 235.65 | needed | 1622 | 22634 | - | 2 | yes |
| hub-2097152 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 16 | 252.825 | 5.190 | 0.021 | 15.802 | 1456.14 | 235.65 | needed | 2055 | 22634 | - | 2 | yes |
| hub-2097152 | pagerank | `grust-next@unchecked` | first | unchecked | 16 | 260.875 | 5.997 | 0.023 | 16.305 | 1468.05 | 238.83 | needed | 1625 | 22633 | - | 2 | yes |
| hub-2097152 | pagerank | `grust-next@unchecked` | second | unchecked | 16 | 278.295 | 17.560 | 0.063 | 17.393 | 1468.05 | 238.83 | needed | 2056 | 22633 | - | 2 | yes |
| uniform-2097152 | pagerank | `neo4j-graph` |  |  | 27 | 277.189 | 2.628 | 0.009 | 10.266 | 459.80 | - |  | 1116 | 2581 | - | 2 | yes |
| uniform-2097152 | pagerank | `icebug` |  |  | 10 | 541.238 | 18.439 | 0.034 | 54.124 | 3307.87 | - |  | 1676 | 100284 | - | 2 | yes |
| uniform-2097152 | pagerank | `icecat` |  |  | 16 | 3096.829 | 70.853 | 0.023 | 193.552 | 601.23 | - |  | 10704 | 5123 | - | 2 | yes |
| uniform-2097152 | pagerank | `grustcat` |  |  | 16 | 3825.667 | 31.149 | 0.008 | 239.104 | 23055.44 | - |  | 0 | 1081010 | - | 2 | yes |
| uniform-2097152 | pagerank | `grust` | first | counted | 16 | 1390.529 | 15.813 | 0.011 | 86.908 | 4113.14 | - | needed | 2821 | 19093 | 541064143 | 2 | yes |
| uniform-2097152 | pagerank | `grust` | second | counted | 16 | 640.344 | 7.529 | 0.012 | 40.021 | 4113.14 | - | needed | 14 | 19093 | 541064143 | 2 | yes |
| uniform-2097152 | pagerank | `grust-next@counted` | first | counted | 16 | 268.470 | 5.408 | 0.020 | 16.779 | 1696.83 | 258.67 | needed | 1621 | 20813 | 541064143 | 2 | yes |
| uniform-2097152 | pagerank | `grust-next@counted` | second | counted | 16 | 277.015 | 5.975 | 0.022 | 17.313 | 1696.83 | 258.67 | needed | 2055 | 20813 | 541064143 | 2 | yes |
| uniform-2097152 | pagerank | `grust-next@work-uncounted` | first | work-uncounted | 16 | 256.739 | 4.832 | 0.019 | 16.046 | 1466.57 | 240.90 | needed | 1626 | 20810 | - | 2 | yes |
| uniform-2097152 | pagerank | `grust-next@work-uncounted` | second | work-uncounted | 16 | 252.352 | 6.358 | 0.025 | 15.772 | 1466.57 | 240.90 | needed | 2054 | 20810 | - | 2 | yes |
| uniform-2097152 | pagerank | `grust-next@unchecked` | first | unchecked | 16 | 251.336 | 6.267 | 0.025 | 15.709 | 1447.89 | 233.22 | needed | 1624 | 20813 | - | 2 | yes |
| uniform-2097152 | pagerank | `grust-next@unchecked` | second | unchecked | 16 | 274.083 | 4.981 | 0.018 | 17.130 | 1447.89 | 233.22 | needed | 2056 | 20813 | - | 2 | yes |

