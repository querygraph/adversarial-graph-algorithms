# B9 tables

Every PageRank cell, with its iteration count beside its total and its per-iteration time. The precision column is what the participant declared in its receipt. Two cells whose iteration counts differ did not do the same work, and their totals are not compared; their per-iteration times are. A row marked UNUSABLE is printed with its numbers and enters no comparison.

## `b9-one-thread.json`: b9-one-thread

workers 1, concurrency 1, allocator glibc default, not pinned, 1 warmup + 5 repeats, steal over the run 0 ticks, 29.0 s, unusable at MAD/median >= 0.25

| fixture | participant | precision | accounting | kernel | call | iters | converged | residual | total ms | MAD | MAD/median | per iter ms | build ms | incoming ms | minflt | steal | usable |
| --- | --- | --- | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| hub-16384 | `neo4j-graph` | f32 |  |  |  | 36 |  | 9.29e-09 | 13.079 | 0.020 | 0.002 | 0.3633 | 7.63 | - | 23 | 0 | yes |
| hub-16384 | `grust#1` | f64 | counted | pull | first | 17 | yes | 3.23e-09 | 11.602 | 0.039 | 0.003 | 0.6825 | 17.46 | - | 384 | 0 | yes |
| hub-16384 | `grust#1` | f64 | counted | pull | second | 17 | yes | 3.23e-09 | 9.645 | 0.016 | 0.002 | 0.5674 | 17.46 | - | 0 | 0 | yes |
| hub-16384 | `grust-next@counted#1` | f64 | counted | pull | first | 17 | yes | 3.23e-09 | 6.076 | 0.003 | 0.000 | 0.3574 | 10.70 | 1.05 | 64 | 0 | yes |
| hub-16384 | `grust-next@counted#1` | f64 | counted | pull | second | 17 | yes | 3.23e-09 | 5.930 | 0.010 | 0.002 | 0.3488 | 10.70 | 1.05 | 0 | 0 | yes |
| hub-16384 | `grust-next@unchecked#1` | f64 | unchecked | pull | first | 17 | yes | 3.23e-09 | 6.065 | 0.019 | 0.003 | 0.3568 | 8.28 | 0.85 | 64 | 0 | yes |
| hub-16384 | `grust-next@unchecked#1` | f64 | unchecked | pull | second | 17 | yes | 3.23e-09 | 5.916 | 0.007 | 0.001 | 0.3480 | 8.28 | 0.85 | 0 | 0 | yes |
| hub-16384 | `grust-next@counted+f32#1` | f32 | counted | pull | first | 20 | yes | 8.8e-09 | 7.326 | 0.010 | 0.001 | 0.3663 | 10.21 | 1.03 | 32 | 0 | yes |
| hub-16384 | `grust-next@counted+f32#1` | f32 | counted | pull | second | 20 | yes | 8.8e-09 | 7.254 | 0.004 | 0.001 | 0.3627 | 10.21 | 1.03 | 0 | 0 | yes |
| hub-16384 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | first | 20 | yes | 8.8e-09 | 7.340 | 0.014 | 0.002 | 0.3670 | 8.50 | 0.87 | 32 | 0 | yes |
| hub-16384 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | second | 20 | yes | 8.8e-09 | 7.268 | 0.009 | 0.001 | 0.3634 | 8.50 | 0.87 | 0 | 0 | yes |
| hub-16384 | `grust-next@counted#unset` | f64 | counted | push | first | 17 | yes | 3.23e-09 | 22.434 | 0.006 | 0.000 | 1.3197 | 12.42 | - | 128 | 0 | yes |
| hub-16384 | `grust-next@counted#unset` | f64 | counted | push | second | 17 | yes | 3.23e-09 | 22.230 | 0.016 | 0.001 | 1.3076 | 12.42 | - | 32 | 0 | yes |
| hub-16384 | `grust-next@unchecked#unset` | f64 | unchecked | push | first | 17 | yes | 3.23e-09 | 12.648 | 0.010 | 0.001 | 0.7440 | 8.51 | - | 128 | 0 | yes |
| hub-16384 | `grust-next@unchecked#unset` | f64 | unchecked | push | second | 17 | yes | 3.23e-09 | 12.441 | 0.036 | 0.003 | 0.7318 | 8.51 | - | 32 | 0 | yes |
| hub-16384 | `grust-next@counted+f32#unset` | f32 | counted | push | first | 21 | yes | 8.58e-09 | 26.823 | 0.008 | 0.000 | 1.2773 | 12.59 | - | 64 | 0 | yes |
| hub-16384 | `grust-next@counted+f32#unset` | f32 | counted | push | second | 21 | yes | 8.58e-09 | 26.669 | 0.014 | 0.001 | 1.2700 | 12.59 | - | 16 | 0 | yes |
| hub-16384 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | first | 21 | yes | 8.58e-09 | 15.047 | 0.014 | 0.001 | 0.7165 | 8.18 | - | 64 | 0 | yes |
| hub-16384 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | second | 21 | yes | 8.58e-09 | 14.944 | 0.034 | 0.002 | 0.7116 | 8.18 | - | 16 | 0 | yes |
| hub-65536 | `neo4j-graph` | f32 |  |  |  | 28 |  | 9.33e-09 | 36.075 | 0.055 | 0.002 | 1.2884 | 35.75 | - | 73 | 0 | yes |
| hub-65536 | `grust#1` | f64 | counted | pull | first | 17 | yes | 3.24e-09 | 53.185 | 1.199 | 0.023 | 3.1285 | 70.41 | - | 1024 | 0 | yes |
| hub-65536 | `grust#1` | f64 | counted | pull | second | 17 | yes | 3.24e-09 | 44.110 | 0.417 | 0.009 | 2.5947 | 70.41 | - | 0 | 0 | yes |
| hub-65536 | `grust-next@counted#1` | f64 | counted | pull | first | 17 | yes | 3.24e-09 | 24.609 | 0.047 | 0.002 | 1.4476 | 44.95 | 5.61 | 256 | 0 | yes |
| hub-65536 | `grust-next@counted#1` | f64 | counted | pull | second | 17 | yes | 3.24e-09 | 24.006 | 0.056 | 0.002 | 1.4121 | 44.95 | 5.61 | 0 | 0 | yes |
| hub-65536 | `grust-next@unchecked#1` | f64 | unchecked | pull | first | 17 | yes | 3.24e-09 | 24.489 | 0.017 | 0.001 | 1.4405 | 36.28 | 4.75 | 256 | 0 | yes |
| hub-65536 | `grust-next@unchecked#1` | f64 | unchecked | pull | second | 17 | yes | 3.24e-09 | 23.931 | 0.053 | 0.002 | 1.4077 | 36.28 | 4.75 | 0 | 0 | yes |
| hub-65536 | `grust-next@counted+f32#1` | f32 | counted | pull | first | 20 | yes | 8.44e-09 | 28.863 | 0.123 | 0.004 | 1.4432 | 44.92 | 5.37 | 128 | 0 | yes |
| hub-65536 | `grust-next@counted+f32#1` | f32 | counted | pull | second | 20 | yes | 8.44e-09 | 28.552 | 0.097 | 0.003 | 1.4276 | 44.92 | 5.37 | 0 | 0 | yes |
| hub-65536 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | first | 20 | yes | 8.44e-09 | 28.863 | 0.105 | 0.004 | 1.4432 | 37.14 | 4.67 | 128 | 0 | yes |
| hub-65536 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | second | 20 | yes | 8.44e-09 | 28.544 | 0.020 | 0.001 | 1.4272 | 37.14 | 4.67 | 0 | 0 | yes |
| hub-65536 | `grust-next@counted#unset` | f64 | counted | push | first | 17 | yes | 3.24e-09 | 91.231 | 0.491 | 0.005 | 5.3665 | 50.27 | - | 512 | 0 | yes |
| hub-65536 | `grust-next@counted#unset` | f64 | counted | push | second | 17 | yes | 3.24e-09 | 90.630 | 1.031 | 0.011 | 5.3312 | 50.27 | - | 128 | 0 | yes |
| hub-65536 | `grust-next@unchecked#unset` | f64 | unchecked | push | first | 17 | yes | 3.24e-09 | 51.727 | 0.085 | 0.002 | 3.0428 | 34.09 | - | 512 | 0 | yes |
| hub-65536 | `grust-next@unchecked#unset` | f64 | unchecked | push | second | 17 | yes | 3.24e-09 | 51.165 | 0.347 | 0.007 | 3.0097 | 34.09 | - | 128 | 0 | yes |
| hub-65536 | `grust-next@counted+f32#unset` | f32 | counted | push | first | 21 | yes | 8.04e-09 | 107.676 | 0.091 | 0.001 | 5.1274 | 49.53 | - | 256 | 0 | yes |
| hub-65536 | `grust-next@counted+f32#unset` | f32 | counted | push | second | 21 | yes | 8.04e-09 | 107.364 | 0.130 | 0.001 | 5.1126 | 49.53 | - | 64 | 0 | yes |
| hub-65536 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | first | 21 | yes | 8.04e-09 | 60.489 | 0.142 | 0.002 | 2.8804 | 33.76 | - | 256 | 0 | yes |
| hub-65536 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | second | 21 | yes | 8.04e-09 | 59.909 | 0.063 | 0.001 | 2.8528 | 33.76 | - | 64 | 0 | yes |
| uniform-16384 | `neo4j-graph` | f32 |  |  |  | 28 |  | 9.64e-09 | 10.360 | 0.011 | 0.001 | 0.3700 | 7.65 | - | 23 | 0 | yes |
| uniform-16384 | `grust#1` | f64 | counted | pull | first | 16 | yes | 3.36e-09 | 11.249 | 0.050 | 0.004 | 0.7030 | 17.24 | - | 384 | 0 | yes |
| uniform-16384 | `grust#1` | f64 | counted | pull | second | 16 | yes | 3.36e-09 | 9.247 | 0.009 | 0.001 | 0.5779 | 17.24 | - | 0 | 0 | yes |
| uniform-16384 | `grust-next@counted#1` | f64 | counted | pull | first | 16 | yes | 3.36e-09 | 5.775 | 0.005 | 0.001 | 0.3610 | 11.30 | 1.07 | 64 | 0 | yes |
| uniform-16384 | `grust-next@counted#1` | f64 | counted | pull | second | 16 | yes | 3.36e-09 | 5.619 | 0.009 | 0.002 | 0.3512 | 11.30 | 1.07 | 0 | 0 | yes |
| uniform-16384 | `grust-next@unchecked#1` | f64 | unchecked | pull | first | 16 | yes | 3.36e-09 | 5.768 | 0.012 | 0.002 | 0.3605 | 9.22 | 0.87 | 64 | 0 | yes |
| uniform-16384 | `grust-next@unchecked#1` | f64 | unchecked | pull | second | 16 | yes | 3.36e-09 | 5.611 | 0.009 | 0.002 | 0.3507 | 9.22 | 0.87 | 0 | 0 | yes |
| uniform-16384 | `grust-next@counted+f32#1` | f32 | counted | pull | first | 19 | yes | 8.76e-09 | 7.140 | 0.008 | 0.001 | 0.3758 | 10.58 | 1.07 | 32 | 0 | yes |
| uniform-16384 | `grust-next@counted+f32#1` | f32 | counted | pull | second | 19 | yes | 8.76e-09 | 7.053 | 0.013 | 0.002 | 0.3712 | 10.58 | 1.07 | 0 | 0 | yes |
| uniform-16384 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | first | 19 | yes | 8.76e-09 | 7.142 | 0.006 | 0.001 | 0.3759 | 9.08 | 0.89 | 32 | 0 | yes |
| uniform-16384 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | second | 19 | yes | 8.76e-09 | 7.060 | 0.010 | 0.001 | 0.3716 | 9.08 | 0.89 | 0 | 0 | yes |
| uniform-16384 | `grust-next@counted#unset` | f64 | counted | push | first | 16 | yes | 3.36e-09 | 21.536 | 0.149 | 0.007 | 1.3460 | 12.68 | - | 128 | 0 | yes |
| uniform-16384 | `grust-next@counted#unset` | f64 | counted | push | second | 16 | yes | 3.36e-09 | 21.325 | 0.180 | 0.008 | 1.3328 | 12.68 | - | 32 | 0 | yes |
| uniform-16384 | `grust-next@unchecked#unset` | f64 | unchecked | push | first | 16 | yes | 3.36e-09 | 11.831 | 0.020 | 0.002 | 0.7394 | 8.49 | - | 128 | 0 | yes |
| uniform-16384 | `grust-next@unchecked#unset` | f64 | unchecked | push | second | 16 | yes | 3.36e-09 | 11.614 | 0.007 | 0.001 | 0.7259 | 8.49 | - | 32 | 0 | yes |
| uniform-16384 | `grust-next@counted+f32#unset` | f32 | counted | push | first | 19 | yes | 9.5e-09 | 24.834 | 0.013 | 0.001 | 1.3070 | 12.23 | - | 64 | 0 | yes |
| uniform-16384 | `grust-next@counted+f32#unset` | f32 | counted | push | second | 19 | yes | 9.5e-09 | 24.707 | 0.012 | 0.000 | 1.3004 | 12.23 | - | 16 | 0 | yes |
| uniform-16384 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | first | 19 | yes | 9.5e-09 | 13.542 | 0.006 | 0.000 | 0.7128 | 7.94 | - | 64 | 0 | yes |
| uniform-16384 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | second | 19 | yes | 9.5e-09 | 13.453 | 0.025 | 0.002 | 0.7080 | 7.94 | - | 16 | 0 | yes |
| uniform-65536 | `neo4j-graph` | f32 |  |  |  | 34 |  | 9.7e-09 | 44.246 | 0.012 | 0.000 | 1.3014 | 34.03 | - | 72 | 0 | yes |
| uniform-65536 | `grust#1` | f64 | counted | pull | first | 16 | yes | 3.43e-09 | 51.816 | 0.480 | 0.009 | 3.2385 | 71.87 | - | 1025 | 0 | yes |
| uniform-65536 | `grust#1` | f64 | counted | pull | second | 16 | yes | 3.43e-09 | 43.330 | 0.533 | 0.012 | 2.7081 | 71.87 | - | 0 | 0 | yes |
| uniform-65536 | `grust-next@counted#1` | f64 | counted | pull | first | 16 | yes | 3.43e-09 | 23.374 | 0.063 | 0.003 | 1.4609 | 44.17 | 5.56 | 257 | 0 | yes |
| uniform-65536 | `grust-next@counted#1` | f64 | counted | pull | second | 16 | yes | 3.43e-09 | 22.741 | 0.060 | 0.003 | 1.4213 | 44.17 | 5.56 | 0 | 0 | yes |
| uniform-65536 | `grust-next@unchecked#1` | f64 | unchecked | pull | first | 16 | yes | 3.43e-09 | 23.353 | 0.067 | 0.003 | 1.4596 | 37.11 | 4.83 | 256 | 0 | yes |
| uniform-65536 | `grust-next@unchecked#1` | f64 | unchecked | pull | second | 16 | yes | 3.43e-09 | 22.705 | 0.027 | 0.001 | 1.4191 | 37.11 | 4.83 | 0 | 0 | yes |
| uniform-65536 | `grust-next@counted+f32#1` | f32 | counted | pull | first | 19 | yes | 8.53e-09 | 28.702 | 0.058 | 0.002 | 1.5106 | 44.47 | 5.45 | 128 | 0 | yes |
| uniform-65536 | `grust-next@counted+f32#1` | f32 | counted | pull | second | 19 | yes | 8.53e-09 | 28.362 | 0.019 | 0.001 | 1.4927 | 44.47 | 5.45 | 0 | 0 | yes |
| uniform-65536 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | first | 19 | yes | 8.53e-09 | 28.676 | 0.095 | 0.003 | 1.5093 | 36.51 | 4.85 | 128 | 0 | yes |
| uniform-65536 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | second | 19 | yes | 8.53e-09 | 28.373 | 0.126 | 0.004 | 1.4933 | 36.51 | 4.85 | 0 | 0 | yes |
| uniform-65536 | `grust-next@counted#unset` | f64 | counted | push | first | 16 | yes | 3.43e-09 | 86.813 | 0.436 | 0.005 | 5.4258 | 49.54 | - | 512 | 0 | yes |
| uniform-65536 | `grust-next@counted#unset` | f64 | counted | push | second | 16 | yes | 3.43e-09 | 85.893 | 0.077 | 0.001 | 5.3683 | 49.54 | - | 128 | 0 | yes |
| uniform-65536 | `grust-next@unchecked#unset` | f64 | unchecked | push | first | 16 | yes | 3.43e-09 | 48.771 | 0.070 | 0.001 | 3.0482 | 33.82 | - | 512 | 0 | yes |
| uniform-65536 | `grust-next@unchecked#unset` | f64 | unchecked | push | second | 16 | yes | 3.43e-09 | 47.812 | 0.213 | 0.004 | 2.9882 | 33.82 | - | 128 | 0 | yes |
| uniform-65536 | `grust-next@counted+f32#unset` | f32 | counted | push | first | 20 | yes | 8.39e-09 | 105.049 | 0.154 | 0.001 | 5.2525 | 50.72 | - | 256 | 0 | yes |
| uniform-65536 | `grust-next@counted+f32#unset` | f32 | counted | push | second | 20 | yes | 8.39e-09 | 104.585 | 0.047 | 0.000 | 5.2292 | 50.72 | - | 64 | 0 | yes |
| uniform-65536 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | first | 20 | yes | 8.39e-09 | 57.198 | 0.080 | 0.001 | 2.8599 | 34.47 | - | 256 | 0 | yes |
| uniform-65536 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | second | 20 | yes | 8.39e-09 | 56.642 | 0.082 | 0.001 | 2.8321 | 34.47 | - | 64 | 0 | yes |

## `b9-full-width.json`: b9-full-width

workers 16, concurrency 16, allocator glibc default, not pinned, 1 warmup + 5 repeats, steal over the run 0 ticks, 9.7 s, unusable at MAD/median >= 0.25

| fixture | participant | precision | accounting | kernel | call | iters | converged | residual | total ms | MAD | MAD/median | per iter ms | build ms | incoming ms | minflt | steal | usable |
| --- | --- | --- | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| hub-16384 | `neo4j-graph` | f32 |  |  |  | 36 |  | 9.29e-09 | 13.192 | 0.056 | 0.004 | 0.3664 | 4.28 | - | 38 | 0 | yes |
| hub-16384 | `grust` | f64 | counted | pull | first | 17 | yes | 3.23e-09 | 6.045 | 0.019 | 0.003 | 0.3556 | 17.78 | - | 484 | 0 | yes |
| hub-16384 | `grust` | f64 | counted | pull | second | 17 | yes | 3.23e-09 | 3.436 | 0.063 | 0.018 | 0.2021 | 17.78 | - | 0 | 0 | yes |
| hub-16384 | `grust-next@counted` | f64 | counted | pull | first | 17 | yes | 3.23e-09 | 2.800 | 0.056 | 0.020 | 0.1647 | 11.31 | 1.65 | 2 | 0 | yes |
| hub-16384 | `grust-next@counted` | f64 | counted | pull | second | 17 | yes | 3.23e-09 | 2.794 | 0.029 | 0.010 | 0.1643 | 11.31 | 1.65 | 1 | 0 | yes |
| hub-16384 | `grust-next@unchecked` | f64 | unchecked | pull | first | 17 | yes | 3.23e-09 | 2.768 | 0.015 | 0.005 | 0.1628 | 9.02 | 1.49 | 2 | 0 | yes |
| hub-16384 | `grust-next@unchecked` | f64 | unchecked | pull | second | 17 | yes | 3.23e-09 | 2.725 | 0.025 | 0.009 | 0.1603 | 9.02 | 1.49 | 1 | 0 | yes |
| hub-16384 | `grust-next@counted+f32` | f32 | counted | pull | first | 20 | yes | 8.8e-09 | 3.310 | 0.023 | 0.007 | 0.1655 | 11.51 | 1.67 | 1 | 0 | yes |
| hub-16384 | `grust-next@counted+f32` | f32 | counted | pull | second | 20 | yes | 8.8e-09 | 3.273 | 0.016 | 0.005 | 0.1636 | 11.51 | 1.67 | 1 | 0 | yes |
| hub-16384 | `grust-next@unchecked+f32` | f32 | unchecked | pull | first | 20 | yes | 8.8e-09 | 3.384 | 0.029 | 0.008 | 0.1692 | 9.01 | 1.50 | 1 | 0 | yes |
| hub-16384 | `grust-next@unchecked+f32` | f32 | unchecked | pull | second | 20 | yes | 8.8e-09 | 3.213 | 0.030 | 0.009 | 0.1607 | 9.01 | 1.50 | 0 | 0 | yes |
| hub-65536 | `neo4j-graph` | f32 |  |  |  | 26 |  | 9.96e-09 | 14.417 | 0.524 | 0.036 | 0.5545 | 13.57 | - | 94 | 0 | yes |
| hub-65536 | `grust` | f64 | counted | pull | first | 17 | yes | 3.24e-09 | 17.472 | 0.165 | 0.009 | 1.0278 | 71.60 | - | 1134 | 0 | yes |
| hub-65536 | `grust` | f64 | counted | pull | second | 17 | yes | 3.24e-09 | 8.530 | 0.020 | 0.002 | 0.5018 | 71.60 | - | 3 | 0 | yes |
| hub-65536 | `grust-next@counted` | f64 | counted | pull | first | 17 | yes | 3.24e-09 | 3.256 | 0.111 | 0.034 | 0.1915 | 41.36 | 5.92 | 3 | 0 | yes |
| hub-65536 | `grust-next@counted` | f64 | counted | pull | second | 17 | yes | 3.24e-09 | 3.110 | 0.018 | 0.006 | 0.1829 | 41.36 | 5.92 | 1 | 0 | yes |
| hub-65536 | `grust-next@unchecked` | f64 | unchecked | pull | first | 17 | yes | 3.24e-09 | 2.945 | 0.057 | 0.019 | 0.1733 | 33.54 | 5.16 | 2 | 0 | yes |
| hub-65536 | `grust-next@unchecked` | f64 | unchecked | pull | second | 17 | yes | 3.24e-09 | 2.946 | 0.077 | 0.026 | 0.1733 | 33.54 | 5.16 | 1 | 0 | yes |
| hub-65536 | `grust-next@counted+f32` | f32 | counted | pull | first | 20 | yes | 8.44e-09 | 3.554 | 0.024 | 0.007 | 0.1777 | 42.28 | 5.94 | 3 | 0 | yes |
| hub-65536 | `grust-next@counted+f32` | f32 | counted | pull | second | 20 | yes | 8.44e-09 | 3.408 | 0.021 | 0.006 | 0.1704 | 42.28 | 5.94 | 1 | 0 | yes |
| hub-65536 | `grust-next@unchecked+f32` | f32 | unchecked | pull | first | 20 | yes | 8.44e-09 | 3.289 | 0.016 | 0.005 | 0.1645 | 33.75 | 5.19 | 3 | 0 | yes |
| hub-65536 | `grust-next@unchecked+f32` | f32 | unchecked | pull | second | 20 | yes | 8.44e-09 | 3.188 | 0.008 | 0.003 | 0.1594 | 33.75 | 5.19 | 1 | 0 | yes |
| uniform-16384 | `neo4j-graph` | f32 |  |  |  | 28 |  | 9.64e-09 | 10.410 | 0.050 | 0.005 | 0.3718 | 4.07 | - | 38 | 0 | yes |
| uniform-16384 | `grust` | f64 | counted | pull | first | 16 | yes | 3.36e-09 | 5.854 | 0.084 | 0.014 | 0.3659 | 17.95 | - | 485 | 0 | yes |
| uniform-16384 | `grust` | f64 | counted | pull | second | 16 | yes | 3.36e-09 | 3.328 | 0.059 | 0.018 | 0.2080 | 17.95 | - | 0 | 0 | yes |
| uniform-16384 | `grust-next@counted` | f64 | counted | pull | first | 16 | yes | 3.36e-09 | 2.606 | 0.010 | 0.004 | 0.1629 | 11.19 | 1.69 | 2 | 0 | yes |
| uniform-16384 | `grust-next@counted` | f64 | counted | pull | second | 16 | yes | 3.36e-09 | 2.605 | 0.055 | 0.021 | 0.1628 | 11.19 | 1.69 | 1 | 0 | yes |
| uniform-16384 | `grust-next@unchecked` | f64 | unchecked | pull | first | 16 | yes | 3.36e-09 | 2.659 | 0.050 | 0.019 | 0.1662 | 8.84 | 1.50 | 2 | 0 | yes |
| uniform-16384 | `grust-next@unchecked` | f64 | unchecked | pull | second | 16 | yes | 3.36e-09 | 2.587 | 0.015 | 0.006 | 0.1617 | 8.84 | 1.50 | 1 | 0 | yes |
| uniform-16384 | `grust-next@counted+f32` | f32 | counted | pull | first | 19 | yes | 8.76e-09 | 3.215 | 0.018 | 0.006 | 0.1692 | 11.53 | 1.70 | 2 | 0 | yes |
| uniform-16384 | `grust-next@counted+f32` | f32 | counted | pull | second | 19 | yes | 8.76e-09 | 3.180 | 0.018 | 0.006 | 0.1674 | 11.53 | 1.70 | 1 | 0 | yes |
| uniform-16384 | `grust-next@unchecked+f32` | f32 | unchecked | pull | first | 19 | yes | 8.76e-09 | 3.132 | 0.008 | 0.003 | 0.1648 | 9.18 | 1.47 | 2 | 0 | yes |
| uniform-16384 | `grust-next@unchecked+f32` | f32 | unchecked | pull | second | 19 | yes | 8.76e-09 | 3.077 | 0.026 | 0.009 | 0.1620 | 9.18 | 1.47 | 1 | 0 | yes |
| uniform-65536 | `neo4j-graph` | f32 |  |  |  | 34 |  | 9.67e-09 | 16.298 | 0.188 | 0.012 | 0.4793 | 13.37 | - | 93 | 0 | yes |
| uniform-65536 | `grust` | f64 | counted | pull | first | 16 | yes | 3.43e-09 | 17.564 | 0.143 | 0.008 | 1.0977 | 70.01 | - | 1132 | 0 | yes |
| uniform-65536 | `grust` | f64 | counted | pull | second | 16 | yes | 3.43e-09 | 8.178 | 0.080 | 0.010 | 0.5112 | 70.01 | - | 5 | 0 | yes |
| uniform-65536 | `grust-next@counted` | f64 | counted | pull | first | 16 | yes | 3.43e-09 | 3.001 | 0.034 | 0.011 | 0.1876 | 41.98 | 6.08 | 3 | 0 | yes |
| uniform-65536 | `grust-next@counted` | f64 | counted | pull | second | 16 | yes | 3.43e-09 | 2.949 | 0.010 | 0.003 | 0.1843 | 41.98 | 6.08 | 1 | 0 | yes |
| uniform-65536 | `grust-next@unchecked` | f64 | unchecked | pull | first | 16 | yes | 3.43e-09 | 2.794 | 0.009 | 0.003 | 0.1746 | 33.14 | 5.30 | 3 | 0 | yes |
| uniform-65536 | `grust-next@unchecked` | f64 | unchecked | pull | second | 16 | yes | 3.43e-09 | 2.744 | 0.047 | 0.017 | 0.1715 | 33.14 | 5.30 | 1 | 0 | yes |
| uniform-65536 | `grust-next@counted+f32` | f32 | counted | pull | first | 19 | yes | 8.53e-09 | 3.350 | 0.082 | 0.025 | 0.1763 | 42.01 | 6.08 | 4 | 0 | yes |
| uniform-65536 | `grust-next@counted+f32` | f32 | counted | pull | second | 19 | yes | 8.53e-09 | 3.283 | 0.009 | 0.003 | 0.1728 | 42.01 | 6.08 | 1 | 0 | yes |
| uniform-65536 | `grust-next@unchecked+f32` | f32 | unchecked | pull | first | 19 | yes | 8.53e-09 | 3.201 | 0.130 | 0.041 | 0.1685 | 33.31 | 5.36 | 3 | 0 | yes |
| uniform-65536 | `grust-next@unchecked+f32` | f32 | unchecked | pull | second | 19 | yes | 8.53e-09 | 3.058 | 0.103 | 0.034 | 0.1610 | 33.31 | 5.36 | 1 | 0 | yes |

## `b9-large-one-thread.json`: b9-large-one-thread

workers 1, concurrency 1, allocator glibc default, not pinned, 1 warmup + 5 repeats, steal over the run 4 ticks, 1097.0 s, unusable at MAD/median >= 0.25

| fixture | participant | precision | accounting | kernel | call | iters | converged | residual | total ms | MAD | MAD/median | per iter ms | build ms | incoming ms | minflt | steal | usable |
| --- | --- | --- | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| hub-2097152 | `neo4j-graph` | f32 |  |  |  | 26 |  | 9.49e-09 | 2081.648 | 11.635 | 0.006 | 80.0634 | 2657.11 | - | 1037 | 2 | yes |
| hub-2097152 | `grust#1` | f64 | counted | pull | first | 16 | yes | 9.96e-09 | 4767.296 | 16.541 | 0.003 | 297.9560 | 3716.62 | - | 3142 | 2 | yes |
| hub-2097152 | `grust#1` | f64 | counted | pull | second | 16 | yes | 9.96e-09 | 4202.364 | 38.867 | 0.009 | 262.6478 | 3716.62 | - | 0 | 2 | yes |
| hub-2097152 | `grust-next@counted#1` | f64 | counted | pull | first | 16 | yes | 9.96e-09 | 1324.956 | 19.655 | 0.015 | 82.8098 | 1906.22 | 462.56 | 1557 | 2 | yes |
| hub-2097152 | `grust-next@counted#1` | f64 | counted | pull | second | 16 | yes | 9.96e-09 | 1242.206 | 13.724 | 0.011 | 77.6379 | 1906.22 | 462.56 | 1006 | 2 | yes |
| hub-2097152 | `grust-next@unchecked#1` | f64 | unchecked | pull | first | 16 | yes | 9.96e-09 | 1342.859 | 91.548 | 0.068 | 83.9287 | 1632.23 | 433.29 | 1557 | 2 | yes |
| hub-2097152 | `grust-next@unchecked#1` | f64 | unchecked | pull | second | 16 | yes | 9.96e-09 | 1305.149 | 79.775 | 0.061 | 81.5718 | 1632.23 | 433.29 | 1006 | 2 | yes |
| hub-2097152 | `grust-next@counted+f32#1` | f32 | counted | pull | first | 20 | yes | 8.19e-09 | 1405.849 | 13.846 | 0.010 | 70.2924 | 1905.46 | 466.09 | 1030 | 2 | yes |
| hub-2097152 | `grust-next@counted+f32#1` | f32 | counted | pull | second | 20 | yes | 8.19e-09 | 1401.197 | 17.447 | 0.012 | 70.0598 | 1905.46 | 466.09 | 0 | 2 | yes |
| hub-2097152 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | first | 20 | yes | 8.19e-09 | 1366.517 | 7.608 | 0.006 | 68.3258 | 1599.66 | 432.50 | 1030 | 2 | yes |
| hub-2097152 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | second | 20 | yes | 8.19e-09 | 1370.215 | 17.470 | 0.013 | 68.5107 | 1599.66 | 432.50 | 0 | 2 | yes |
| hub-2097152 | `grust-next@counted#unset` | f64 | counted | push | first | 16 | yes | 9.96e-09 | 3800.617 | 85.449 | 0.022 | 237.5386 | 1765.32 | - | 2595 | 2 | yes |
| hub-2097152 | `grust-next@counted#unset` | f64 | counted | push | second | 16 | yes | 9.96e-09 | 3817.028 | 128.997 | 0.034 | 238.5643 | 1765.32 | - | 519 | 2 | yes |
| hub-2097152 | `grust-next@unchecked#unset` | f64 | unchecked | push | first | 16 | yes | 9.96e-09 | 2698.363 | 12.367 | 0.005 | 168.6477 | 1268.68 | - | 2595 | 2 | yes |
| hub-2097152 | `grust-next@unchecked#unset` | f64 | unchecked | push | second | 16 | yes | 9.96e-09 | 2683.633 | 177.363 | 0.066 | 167.7271 | 1268.68 | - | 519 | 2 | yes |
| hub-2097152 | `grust-next@counted+f32#unset` | f32 | counted | push | first | 21 | yes | 8.2e-09 | 4452.779 | 15.367 | 0.003 | 212.0371 | 1735.12 | - | 2579 | 2 | yes |
| hub-2097152 | `grust-next@counted+f32#unset` | f32 | counted | push | second | 21 | yes | 8.2e-09 | 4445.597 | 22.449 | 0.005 | 211.6951 | 1735.12 | - | 515 | 2 | yes |
| hub-2097152 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | first | 21 | yes | 8.2e-09 | 2948.378 | 79.349 | 0.027 | 140.3989 | 1277.20 | - | 2579 | 2 | yes |
| hub-2097152 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | second | 21 | yes | 8.2e-09 | 2894.063 | 38.619 | 0.013 | 137.8125 | 1277.20 | - | 515 | 2 | yes |
| uniform-2097152 | `neo4j-graph` | f32 |  |  |  | 26 |  | 8.04e-09 | 2154.732 | 14.332 | 0.007 | 82.8743 | 2601.00 | - | 1038 | 2 | yes |
| uniform-2097152 | `grust#1` | f64 | counted | pull | first | 16 | yes | 3.46e-09 | 4963.203 | 39.383 | 0.008 | 310.2002 | 3751.86 | - | 2659 | 2 | yes |
| uniform-2097152 | `grust#1` | f64 | counted | pull | second | 16 | yes | 3.46e-09 | 4382.386 | 15.006 | 0.003 | 273.8991 | 3751.86 | - | 0 | 2 | yes |
| uniform-2097152 | `grust-next@counted#1` | f64 | counted | pull | first | 16 | yes | 3.46e-09 | 1410.579 | 129.367 | 0.092 | 88.1612 | 1860.06 | 441.33 | 1557 | 2 | yes |
| uniform-2097152 | `grust-next@counted#1` | f64 | counted | pull | second | 16 | yes | 3.46e-09 | 1461.399 | 181.686 | 0.124 | 91.3375 | 1860.06 | 441.33 | 1006 | 2 | yes |
| uniform-2097152 | `grust-next@unchecked#1` | f64 | unchecked | pull | first | 16 | yes | 3.46e-09 | 1381.632 | 62.161 | 0.045 | 86.3520 | 1599.45 | 415.70 | 1557 | 2 | yes |
| uniform-2097152 | `grust-next@unchecked#1` | f64 | unchecked | pull | second | 16 | yes | 3.46e-09 | 1503.779 | 57.064 | 0.038 | 93.9862 | 1599.45 | 415.70 | 1006 | 2 | yes |
| uniform-2097152 | `grust-next@counted+f32#1` | f32 | counted | pull | first | 19 | yes | 8.59e-09 | 1348.980 | 4.634 | 0.003 | 70.9990 | 1859.82 | 436.43 | 1030 | 2 | yes |
| uniform-2097152 | `grust-next@counted+f32#1` | f32 | counted | pull | second | 19 | yes | 8.59e-09 | 1346.180 | 4.698 | 0.003 | 70.8516 | 1859.82 | 436.43 | 0 | 2 | yes |
| uniform-2097152 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | first | 19 | yes | 8.59e-09 | 1387.974 | 9.535 | 0.007 | 73.0513 | 1627.54 | 424.97 | 1030 | 2 | yes |
| uniform-2097152 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | second | 19 | yes | 8.59e-09 | 1388.653 | 4.764 | 0.003 | 73.0870 | 1627.54 | 424.97 | 0 | 2 | yes |
| uniform-2097152 | `grust-next@counted#unset` | f64 | counted | push | first | 16 | yes | 3.46e-09 | 4245.225 | 156.044 | 0.037 | 265.3265 | 1760.50 | - | 2595 | 2 | yes |
| uniform-2097152 | `grust-next@counted#unset` | f64 | counted | push | second | 16 | yes | 3.46e-09 | 4231.909 | 367.831 | 0.087 | 264.4943 | 1760.50 | - | 519 | 2 | yes |
| uniform-2097152 | `grust-next@unchecked#unset` | f64 | unchecked | push | first | 16 | yes | 3.46e-09 | 2885.298 | 161.746 | 0.056 | 180.3311 | 1264.47 | - | 2595 | 2 | yes |
| uniform-2097152 | `grust-next@unchecked#unset` | f64 | unchecked | push | second | 16 | yes | 3.46e-09 | 2860.518 | 273.871 | 0.096 | 178.7824 | 1264.47 | - | 519 | 2 | yes |
| uniform-2097152 | `grust-next@counted+f32#unset` | f32 | counted | push | first | 20 | yes | 8.43e-09 | 4301.890 | 31.599 | 0.007 | 215.0945 | 1744.43 | - | 2579 | 2 | yes |
| uniform-2097152 | `grust-next@counted+f32#unset` | f32 | counted | push | second | 20 | yes | 8.43e-09 | 4311.278 | 7.057 | 0.002 | 215.5639 | 1744.43 | - | 515 | 2 | yes |
| uniform-2097152 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | first | 20 | yes | 8.43e-09 | 2864.163 | 11.325 | 0.004 | 143.2081 | 1272.37 | - | 2579 | 2 | yes |
| uniform-2097152 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | second | 20 | yes | 8.43e-09 | 2804.551 | 51.544 | 0.018 | 140.2276 | 1272.37 | - | 515 | 2 | yes |

## `b9-large-full-width.json`: b9-large-full-width

workers 16, concurrency 16, allocator glibc default, not pinned, 1 warmup + 5 repeats, steal over the run 1 ticks, 307.9 s, unusable at MAD/median >= 0.25

| fixture | participant | precision | accounting | kernel | call | iters | converged | residual | total ms | MAD | MAD/median | per iter ms | build ms | incoming ms | minflt | steal | usable |
| --- | --- | --- | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| hub-2097152 | `neo4j-graph` | f32 |  |  |  | 28 |  | 9.51e-09 | 259.569 | 0.590 | 0.002 | 9.2703 | 409.62 | - | 1117 | 0 | yes |
| hub-2097152 | `grust` | f64 | counted | pull | first | 16 | yes | 9.96e-09 | 1094.322 | 7.952 | 0.007 | 68.3951 | 3735.65 | - | 3312 | 0 | yes |
| hub-2097152 | `grust` | f64 | counted | pull | second | 16 | yes | 9.96e-09 | 507.501 | 13.270 | 0.026 | 31.7188 | 3735.65 | - | 12 | 0 | yes |
| hub-2097152 | `grust-next@counted` | f64 | counted | pull | first | 16 | yes | 9.96e-09 | 152.567 | 2.194 | 0.014 | 9.5354 | 1459.07 | 201.02 | 1064 | 0 | yes |
| hub-2097152 | `grust-next@counted` | f64 | counted | pull | second | 16 | yes | 9.96e-09 | 163.453 | 4.003 | 0.024 | 10.2158 | 1459.07 | 201.02 | 1530 | 0 | yes |
| hub-2097152 | `grust-next@unchecked` | f64 | unchecked | pull | first | 16 | yes | 9.96e-09 | 153.660 | 3.743 | 0.024 | 9.6038 | 1210.02 | 176.12 | 1067 | 0 | yes |
| hub-2097152 | `grust-next@unchecked` | f64 | unchecked | pull | second | 16 | yes | 9.96e-09 | 168.385 | 4.452 | 0.026 | 10.5241 | 1210.02 | 176.12 | 1534 | 0 | yes |
| hub-2097152 | `grust-next@counted+f32` | f32 | counted | pull | first | 20 | yes | 8.19e-09 | 152.613 | 0.252 | 0.002 | 7.6307 | 1485.34 | 199.32 | 542 | 0 | yes |
| hub-2097152 | `grust-next@counted+f32` | f32 | counted | pull | second | 20 | yes | 8.19e-09 | 152.455 | 0.315 | 0.002 | 7.6227 | 1485.34 | 199.32 | 1520 | 0 | yes |
| hub-2097152 | `grust-next@unchecked+f32` | f32 | unchecked | pull | first | 20 | yes | 8.19e-09 | 150.537 | 0.248 | 0.002 | 7.5268 | 1211.68 | 177.65 | 542 | 0 | yes |
| hub-2097152 | `grust-next@unchecked+f32` | f32 | unchecked | pull | second | 20 | yes | 8.19e-09 | 155.917 | 3.222 | 0.021 | 7.7959 | 1211.68 | 177.65 | 1519 | 0 | yes |
| uniform-2097152 | `neo4j-graph` | f32 |  |  |  | 28 |  | 8.02e-09 | 268.099 | 1.878 | 0.007 | 9.5750 | 404.90 | - | 1112 | 1 | yes |
| uniform-2097152 | `grust` | f64 | counted | pull | first | 16 | yes | 3.46e-09 | 1089.841 | 9.436 | 0.009 | 68.1150 | 3744.63 | - | 2827 | 1 | yes |
| uniform-2097152 | `grust` | f64 | counted | pull | second | 16 | yes | 3.46e-09 | 540.642 | 6.068 | 0.011 | 33.7902 | 3744.63 | - | 13 | 1 | yes |
| uniform-2097152 | `grust-next@counted` | f64 | counted | pull | first | 16 | yes | 3.46e-09 | 160.269 | 2.443 | 0.015 | 10.0168 | 1480.94 | 203.58 | 1063 | 1 | yes |
| uniform-2097152 | `grust-next@counted` | f64 | counted | pull | second | 16 | yes | 3.46e-09 | 163.105 | 1.935 | 0.012 | 10.1941 | 1480.94 | 203.58 | 1532 | 1 | yes |
| uniform-2097152 | `grust-next@unchecked` | f64 | unchecked | pull | first | 16 | yes | 3.46e-09 | 158.187 | 1.976 | 0.012 | 9.8867 | 1217.65 | 181.77 | 1065 | 1 | yes |
| uniform-2097152 | `grust-next@unchecked` | f64 | unchecked | pull | second | 16 | yes | 3.46e-09 | 163.112 | 1.594 | 0.010 | 10.1945 | 1217.65 | 181.77 | 1532 | 1 | yes |
| uniform-2097152 | `grust-next@counted+f32` | f32 | counted | pull | first | 19 | yes | 8.59e-09 | 151.915 | 0.657 | 0.004 | 7.9955 | 1485.28 | 211.88 | 543 | 1 | yes |
| uniform-2097152 | `grust-next@counted+f32` | f32 | counted | pull | second | 19 | yes | 8.59e-09 | 157.264 | 5.715 | 0.036 | 8.2771 | 1485.28 | 211.88 | 1519 | 1 | yes |
| uniform-2097152 | `grust-next@unchecked+f32` | f32 | unchecked | pull | first | 19 | yes | 8.59e-09 | 150.608 | 1.080 | 0.007 | 7.9267 | 1219.77 | 183.69 | 542 | 1 | yes |
| uniform-2097152 | `grust-next@unchecked+f32` | f32 | unchecked | pull | second | 19 | yes | 8.59e-09 | 152.491 | 0.078 | 0.001 | 8.0258 | 1219.77 | 183.69 | 1519 | 1 | yes |

## `b9-xlarge-one-thread.json`: b9-xlarge-one-thread

workers 1, concurrency 1, allocator glibc default, not pinned, 1 warmup + 5 repeats, steal over the run 10 ticks, 2640.5 s, unusable at MAD/median >= 0.25

| fixture | participant | precision | accounting | kernel | call | iters | converged | residual | total ms | MAD | MAD/median | per iter ms | build ms | incoming ms | minflt | steal | usable |
| --- | --- | --- | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| hub-4194304 | `neo4j-graph` | f32 |  |  |  | 23 |  | 8.29e-09 | 4050.949 | 110.843 | 0.027 | 176.1282 | 6328.00 | - | 1047 | 5 | yes |
| hub-4194304 | `grust#1` | f64 | counted | pull | first | 16 | yes | 9.96e-09 | 11814.079 | 10.614 | 0.001 | 738.3799 | 7709.06 | - | 3227 | 5 | yes |
| hub-4194304 | `grust#1` | f64 | counted | pull | second | 16 | yes | 9.96e-09 | 10471.699 | 4.829 | 0.000 | 654.4812 | 7709.06 | - | 1584 | 5 | yes |
| hub-4194304 | `grust-next@counted#1` | f64 | counted | pull | first | 16 | yes | 9.96e-09 | 4373.365 | 10.257 | 0.002 | 273.3353 | 3885.35 | 1010.54 | 2112 | 5 | yes |
| hub-4194304 | `grust-next@counted#1` | f64 | counted | pull | second | 16 | yes | 9.96e-09 | 4369.689 | 15.981 | 0.004 | 273.1056 | 3885.35 | 1010.54 | 2112 | 5 | yes |
| hub-4194304 | `grust-next@unchecked#1` | f64 | unchecked | pull | first | 16 | yes | 9.96e-09 | 4339.478 | 18.064 | 0.004 | 271.2173 | 3421.91 | 975.44 | 2112 | 5 | yes |
| hub-4194304 | `grust-next@unchecked#1` | f64 | unchecked | pull | second | 16 | yes | 9.96e-09 | 4358.809 | 25.425 | 0.006 | 272.4256 | 3421.91 | 975.44 | 2112 | 5 | yes |
| hub-4194304 | `grust-next@counted+f32#1` | f32 | counted | pull | first | 20 | yes | 8.21e-09 | 3642.630 | 141.707 | 0.039 | 182.1315 | 3911.81 | 1006.58 | 1557 | 5 | yes |
| hub-4194304 | `grust-next@counted+f32#1` | f32 | counted | pull | second | 20 | yes | 8.21e-09 | 3330.711 | 130.061 | 0.039 | 166.5355 | 3911.81 | 1006.58 | 1006 | 5 | yes |
| hub-4194304 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | first | 20 | yes | 8.21e-09 | 3372.225 | 271.092 | 0.080 | 168.6113 | 3409.73 | 976.59 | 1557 | 5 | yes |
| hub-4194304 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | second | 20 | yes | 8.21e-09 | 3245.984 | 45.568 | 0.014 | 162.2992 | 3409.73 | 976.59 | 1006 | 5 | yes |
| hub-4194304 | `grust-next@counted#unset` | f64 | counted | push | first | 16 | yes | 9.96e-09 | 11942.177 | 23.759 | 0.002 | 746.3861 | 3556.39 | - | 2640 | 5 | yes |
| hub-4194304 | `grust-next@counted#unset` | f64 | counted | push | second | 16 | yes | 9.96e-09 | 11963.175 | 189.716 | 0.016 | 747.6984 | 3556.39 | - | 2640 | 5 | yes |
| hub-4194304 | `grust-next@unchecked#unset` | f64 | unchecked | push | first | 16 | yes | 9.96e-09 | 9469.756 | 65.314 | 0.007 | 591.8597 | 2572.48 | - | 2640 | 5 | yes |
| hub-4194304 | `grust-next@unchecked#unset` | f64 | unchecked | push | second | 16 | yes | 9.96e-09 | 9296.285 | 84.262 | 0.009 | 581.0178 | 2572.48 | - | 2640 | 5 | yes |
| hub-4194304 | `grust-next@counted+f32#unset` | f32 | counted | push | first | 21 | yes | 8.31e-09 | 9468.726 | 284.752 | 0.030 | 450.8917 | 3559.72 | - | 2608 | 5 | yes |
| hub-4194304 | `grust-next@counted+f32#unset` | f32 | counted | push | second | 21 | yes | 8.31e-09 | 9711.130 | 235.866 | 0.024 | 462.4348 | 3559.72 | - | 2604 | 5 | yes |
| hub-4194304 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | first | 21 | yes | 8.31e-09 | 6756.643 | 656.603 | 0.097 | 321.7449 | 2549.17 | - | 2608 | 5 | yes |
| hub-4194304 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | second | 21 | yes | 8.31e-09 | 6650.388 | 137.914 | 0.021 | 316.6851 | 2549.17 | - | 2604 | 5 | yes |
| uniform-4194304 | `neo4j-graph` | f32 |  |  |  | 29 |  | 8.64e-09 | 7301.026 | 8.387 | 0.001 | 251.7595 | 6311.91 | - | 1046 | 5 | yes |
| uniform-4194304 | `grust#1` | f64 | counted | pull | first | 16 | yes | 3.47e-09 | 12490.078 | 21.399 | 0.002 | 780.6299 | 7688.70 | - | 2261 | 5 | yes |
| uniform-4194304 | `grust#1` | f64 | counted | pull | second | 16 | yes | 3.47e-09 | 11171.752 | 33.336 | 0.003 | 698.2345 | 7688.70 | - | 1073 | 5 | yes |
| uniform-4194304 | `grust-next@counted#1` | f64 | counted | pull | first | 16 | yes | 3.47e-09 | 4557.870 | 35.221 | 0.008 | 284.8669 | 3885.66 | 991.89 | 579 | 5 | yes |
| uniform-4194304 | `grust-next@counted#1` | f64 | counted | pull | second | 16 | yes | 3.47e-09 | 4577.397 | 63.776 | 0.014 | 286.0873 | 3885.66 | 991.89 | 579 | 5 | yes |
| uniform-4194304 | `grust-next@unchecked#1` | f64 | unchecked | pull | first | 16 | yes | 3.47e-09 | 4531.479 | 50.943 | 0.011 | 283.2174 | 3383.98 | 959.27 | 579 | 5 | yes |
| uniform-4194304 | `grust-next@unchecked#1` | f64 | unchecked | pull | second | 16 | yes | 3.47e-09 | 4549.540 | 23.857 | 0.005 | 284.3462 | 3383.98 | 959.27 | 579 | 5 | yes |
| uniform-4194304 | `grust-next@counted+f32#1` | f32 | counted | pull | first | 19 | yes | 8.61e-09 | 3139.157 | 163.800 | 0.052 | 165.2188 | 3893.82 | 1014.87 | 1557 | 5 | yes |
| uniform-4194304 | `grust-next@counted+f32#1` | f32 | counted | pull | second | 19 | yes | 8.61e-09 | 3634.686 | 281.873 | 0.078 | 191.2992 | 3893.82 | 1014.87 | 1006 | 5 | yes |
| uniform-4194304 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | first | 19 | yes | 8.61e-09 | 3340.296 | 208.047 | 0.062 | 175.8050 | 3416.58 | 966.19 | 1557 | 5 | yes |
| uniform-4194304 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | second | 19 | yes | 8.61e-09 | 3805.595 | 23.425 | 0.006 | 200.2945 | 3416.58 | 966.19 | 1006 | 5 | yes |
| uniform-4194304 | `grust-next@counted#unset` | f64 | counted | push | first | 16 | yes | 3.47e-09 | 11647.030 | 104.220 | 0.009 | 727.9394 | 3553.53 | - | 2129 | 5 | yes |
| uniform-4194304 | `grust-next@counted#unset` | f64 | counted | push | second | 16 | yes | 3.47e-09 | 11580.648 | 24.205 | 0.002 | 723.7905 | 3553.53 | - | 2129 | 5 | yes |
| uniform-4194304 | `grust-next@unchecked#unset` | f64 | unchecked | push | first | 16 | yes | 3.47e-09 | 9004.277 | 40.072 | 0.004 | 562.7673 | 2566.54 | - | 2129 | 5 | yes |
| uniform-4194304 | `grust-next@unchecked#unset` | f64 | unchecked | push | second | 16 | yes | 3.47e-09 | 9012.386 | 41.143 | 0.005 | 563.2741 | 2566.54 | - | 2129 | 5 | yes |
| uniform-4194304 | `grust-next@counted+f32#unset` | f32 | counted | push | first | 20 | yes | 8.48e-09 | 9904.532 | 354.952 | 0.036 | 495.2266 | 3562.24 | - | 2097 | 5 | yes |
| uniform-4194304 | `grust-next@counted+f32#unset` | f32 | counted | push | second | 20 | yes | 8.48e-09 | 9211.620 | 166.426 | 0.018 | 460.5810 | 3562.24 | - | 2093 | 5 | yes |
| uniform-4194304 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | first | 20 | yes | 8.48e-09 | 6827.097 | 599.982 | 0.088 | 341.3549 | 2573.27 | - | 2097 | 5 | yes |
| uniform-4194304 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | second | 20 | yes | 8.48e-09 | 7108.304 | 468.222 | 0.066 | 355.4152 | 2573.27 | - | 2093 | 5 | yes |

## `b9-xlarge-full-width.json`: b9-xlarge-full-width

workers 16, concurrency 16, allocator glibc default, not pinned, 1 warmup + 5 repeats, steal over the run 2 ticks, 619.3 s, unusable at MAD/median >= 0.25

| fixture | participant | precision | accounting | kernel | call | iters | converged | residual | total ms | MAD | MAD/median | per iter ms | build ms | incoming ms | minflt | steal | usable |
| --- | --- | --- | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| hub-4194304 | `neo4j-graph` | f32 |  |  |  | 14 |  | 9.01e-09 | 343.066 | 49.317 | 0.144 | 24.5047 | 866.67 | - | 1116 | 1 | yes |
| hub-4194304 | `grust` | f64 | counted | pull | first | 16 | yes | 9.96e-09 | 2669.312 | 3.380 | 0.001 | 166.8320 | 7652.63 | - | 3447 | 1 | yes |
| hub-4194304 | `grust` | f64 | counted | pull | second | 16 | yes | 9.96e-09 | 1322.329 | 10.206 | 0.008 | 82.6455 | 7652.63 | - | 1608 | 1 | yes |
| hub-4194304 | `grust-next@counted` | f64 | counted | pull | first | 16 | yes | 9.96e-09 | 524.667 | 2.841 | 0.005 | 32.7917 | 3075.56 | 458.23 | 1643 | 1 | yes |
| hub-4194304 | `grust-next@counted` | f64 | counted | pull | second | 16 | yes | 9.96e-09 | 511.742 | 1.897 | 0.004 | 31.9839 | 3075.56 | 458.23 | 1609 | 1 | yes |
| hub-4194304 | `grust-next@unchecked` | f64 | unchecked | pull | first | 16 | yes | 9.96e-09 | 523.548 | 16.567 | 0.032 | 32.7217 | 2570.94 | 413.38 | 1644 | 1 | yes |
| hub-4194304 | `grust-next@unchecked` | f64 | unchecked | pull | second | 16 | yes | 9.96e-09 | 535.302 | 29.128 | 0.054 | 33.4563 | 2570.94 | 413.38 | 1608 | 1 | yes |
| hub-4194304 | `grust-next@counted+f32` | f32 | counted | pull | first | 20 | yes | 8.21e-09 | 352.493 | 8.952 | 0.025 | 17.6246 | 3012.30 | 453.13 | 2108 | 1 | yes |
| hub-4194304 | `grust-next@counted+f32` | f32 | counted | pull | second | 20 | yes | 8.21e-09 | 346.778 | 2.338 | 0.007 | 17.3389 | 3012.30 | 453.13 | 1538 | 1 | yes |
| hub-4194304 | `grust-next@unchecked+f32` | f32 | unchecked | pull | first | 20 | yes | 8.21e-09 | 350.594 | 11.735 | 0.033 | 17.5297 | 2563.31 | 421.59 | 1610 | 1 | yes |
| hub-4194304 | `grust-next@unchecked+f32` | f32 | unchecked | pull | second | 20 | yes | 8.21e-09 | 338.374 | 4.823 | 0.014 | 16.9187 | 2563.31 | 421.59 | 1539 | 1 | yes |
| uniform-4194304 | `neo4j-graph` | f32 |  |  |  | 29 |  | 8.23e-09 | 583.773 | 14.834 | 0.025 | 20.1301 | 866.00 | - | 1113 | 1 | yes |
| uniform-4194304 | `grust` | f64 | counted | pull | first | 16 | yes | 3.47e-09 | 2730.520 | 6.327 | 0.002 | 170.6575 | 7673.31 | - | 2482 | 1 | yes |
| uniform-4194304 | `grust` | f64 | counted | pull | second | 16 | yes | 3.47e-09 | 1426.669 | 7.822 | 0.005 | 89.1668 | 7673.31 | - | 1094 | 1 | yes |
| uniform-4194304 | `grust-next@counted` | f64 | counted | pull | first | 16 | yes | 3.47e-09 | 540.415 | 13.847 | 0.026 | 33.7760 | 3064.88 | 467.33 | 1130 | 1 | yes |
| uniform-4194304 | `grust-next@counted` | f64 | counted | pull | second | 16 | yes | 3.47e-09 | 539.516 | 11.526 | 0.021 | 33.7197 | 3064.88 | 467.33 | 1095 | 1 | yes |
| uniform-4194304 | `grust-next@unchecked` | f64 | unchecked | pull | first | 16 | yes | 3.47e-09 | 537.255 | 5.987 | 0.011 | 33.5784 | 2550.81 | 420.89 | 1645 | 1 | yes |
| uniform-4194304 | `grust-next@unchecked` | f64 | unchecked | pull | second | 16 | yes | 3.47e-09 | 547.535 | 3.923 | 0.007 | 34.2210 | 2550.81 | 420.89 | 1606 | 1 | yes |
| uniform-4194304 | `grust-next@counted+f32` | f32 | counted | pull | first | 19 | yes | 8.61e-09 | 353.724 | 10.748 | 0.030 | 18.6171 | 3036.98 | 466.42 | 2117 | 1 | yes |
| uniform-4194304 | `grust-next@counted+f32` | f32 | counted | pull | second | 19 | yes | 8.61e-09 | 356.109 | 7.093 | 0.020 | 18.7426 | 3036.98 | 466.42 | 1535 | 1 | yes |
| uniform-4194304 | `grust-next@unchecked+f32` | f32 | unchecked | pull | first | 19 | yes | 8.61e-09 | 351.392 | 8.186 | 0.023 | 18.4943 | 2536.35 | 423.23 | 1607 | 1 | yes |
| uniform-4194304 | `grust-next@unchecked+f32` | f32 | unchecked | pull | second | 19 | yes | 8.61e-09 | 348.942 | 17.817 | 0.051 | 18.3654 | 2536.35 | 423.23 | 1535 | 1 | yes |

## Iteration counts side by side

Each cell is the iteration count the participant reported for that fixture in that run (a Grust row reports the same count on both calls, so one is shown). `neo4j-graph` first, then the `+f32` rows, which are the rows that could stop where it stops, then the f64 rows. Where a count differs from `neo4j-graph`'s in the same row, the two totals were not the same number of sweeps over the arcs, and only the per-iteration column of the table above compares them.

| fixture | run | `neo4j-graph` | `grust-next@counted+f32#1` | `grust-next@counted+f32#unset` | `grust-next@unchecked+f32#1` | `grust-next@unchecked+f32#unset` | `grust-next@counted+f32` | `grust-next@unchecked+f32` | `grust#1` | `grust-next@counted#1` | `grust-next@counted#unset` | `grust-next@unchecked#1` | `grust-next@unchecked#unset` | `grust` | `grust-next@counted` | `grust-next@unchecked` |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| hub-16384 | b9-one-thread | 36 | 20 | 21 | 20 | 21 | - | - | 17 | 17 | 17 | 17 | 17 | - | - | - |
| hub-65536 | b9-one-thread | 28 | 20 | 21 | 20 | 21 | - | - | 17 | 17 | 17 | 17 | 17 | - | - | - |
| uniform-16384 | b9-one-thread | 28 | 19 | 19 | 19 | 19 | - | - | 16 | 16 | 16 | 16 | 16 | - | - | - |
| uniform-65536 | b9-one-thread | 34 | 19 | 20 | 19 | 20 | - | - | 16 | 16 | 16 | 16 | 16 | - | - | - |
| hub-16384 | b9-full-width | 36 | - | - | - | - | 20 | 20 | - | - | - | - | - | 17 | 17 | 17 |
| hub-65536 | b9-full-width | 26 | - | - | - | - | 20 | 20 | - | - | - | - | - | 17 | 17 | 17 |
| uniform-16384 | b9-full-width | 28 | - | - | - | - | 19 | 19 | - | - | - | - | - | 16 | 16 | 16 |
| uniform-65536 | b9-full-width | 34 | - | - | - | - | 19 | 19 | - | - | - | - | - | 16 | 16 | 16 |
| hub-2097152 | b9-large-one-thread | 26 | 20 | 21 | 20 | 21 | - | - | 16 | 16 | 16 | 16 | 16 | - | - | - |
| uniform-2097152 | b9-large-one-thread | 26 | 19 | 20 | 19 | 20 | - | - | 16 | 16 | 16 | 16 | 16 | - | - | - |
| hub-2097152 | b9-large-full-width | 28 | - | - | - | - | 20 | 20 | - | - | - | - | - | 16 | 16 | 16 |
| uniform-2097152 | b9-large-full-width | 28 | - | - | - | - | 19 | 19 | - | - | - | - | - | 16 | 16 | 16 |
| hub-4194304 | b9-xlarge-one-thread | 23 | 20 | 21 | 20 | 21 | - | - | 16 | 16 | 16 | 16 | 16 | - | - | - |
| uniform-4194304 | b9-xlarge-one-thread | 29 | 19 | 20 | 19 | 20 | - | - | 16 | 16 | 16 | 16 | 16 | - | - | - |
| hub-4194304 | b9-xlarge-full-width | 14 | - | - | - | - | 20 | 20 | - | - | - | - | - | 16 | 16 | 16 |
| uniform-4194304 | b9-xlarge-full-width | 29 | - | - | - | - | 19 | 19 | - | - | - | - | - | 16 | 16 | 16 |

Of 48 `+f32` cells, 0 stopped at the same count as `neo4j-graph` on the same fixture in the same run and 48 did not. For those, the totals are not comparable and the per-iteration times are:

- hub-16384, b9-one-thread: `grust-next@counted+f32#1` stopped at 20, `neo4j-graph` at 36.
- hub-16384, b9-one-thread: `grust-next@counted+f32#unset` stopped at 21, `neo4j-graph` at 36.
- hub-16384, b9-one-thread: `grust-next@unchecked+f32#1` stopped at 20, `neo4j-graph` at 36.
- hub-16384, b9-one-thread: `grust-next@unchecked+f32#unset` stopped at 21, `neo4j-graph` at 36.
- hub-65536, b9-one-thread: `grust-next@counted+f32#1` stopped at 20, `neo4j-graph` at 28.
- hub-65536, b9-one-thread: `grust-next@counted+f32#unset` stopped at 21, `neo4j-graph` at 28.
- hub-65536, b9-one-thread: `grust-next@unchecked+f32#1` stopped at 20, `neo4j-graph` at 28.
- hub-65536, b9-one-thread: `grust-next@unchecked+f32#unset` stopped at 21, `neo4j-graph` at 28.
- uniform-16384, b9-one-thread: `grust-next@counted+f32#1` stopped at 19, `neo4j-graph` at 28.
- uniform-16384, b9-one-thread: `grust-next@counted+f32#unset` stopped at 19, `neo4j-graph` at 28.
- uniform-16384, b9-one-thread: `grust-next@unchecked+f32#1` stopped at 19, `neo4j-graph` at 28.
- uniform-16384, b9-one-thread: `grust-next@unchecked+f32#unset` stopped at 19, `neo4j-graph` at 28.
- uniform-65536, b9-one-thread: `grust-next@counted+f32#1` stopped at 19, `neo4j-graph` at 34.
- uniform-65536, b9-one-thread: `grust-next@counted+f32#unset` stopped at 20, `neo4j-graph` at 34.
- uniform-65536, b9-one-thread: `grust-next@unchecked+f32#1` stopped at 19, `neo4j-graph` at 34.
- uniform-65536, b9-one-thread: `grust-next@unchecked+f32#unset` stopped at 20, `neo4j-graph` at 34.
- hub-16384, b9-full-width: `grust-next@counted+f32` stopped at 20, `neo4j-graph` at 36.
- hub-16384, b9-full-width: `grust-next@unchecked+f32` stopped at 20, `neo4j-graph` at 36.
- hub-65536, b9-full-width: `grust-next@counted+f32` stopped at 20, `neo4j-graph` at 26.
- hub-65536, b9-full-width: `grust-next@unchecked+f32` stopped at 20, `neo4j-graph` at 26.
- uniform-16384, b9-full-width: `grust-next@counted+f32` stopped at 19, `neo4j-graph` at 28.
- uniform-16384, b9-full-width: `grust-next@unchecked+f32` stopped at 19, `neo4j-graph` at 28.
- uniform-65536, b9-full-width: `grust-next@counted+f32` stopped at 19, `neo4j-graph` at 34.
- uniform-65536, b9-full-width: `grust-next@unchecked+f32` stopped at 19, `neo4j-graph` at 34.
- hub-2097152, b9-large-one-thread: `grust-next@counted+f32#1` stopped at 20, `neo4j-graph` at 26.
- hub-2097152, b9-large-one-thread: `grust-next@counted+f32#unset` stopped at 21, `neo4j-graph` at 26.
- hub-2097152, b9-large-one-thread: `grust-next@unchecked+f32#1` stopped at 20, `neo4j-graph` at 26.
- hub-2097152, b9-large-one-thread: `grust-next@unchecked+f32#unset` stopped at 21, `neo4j-graph` at 26.
- uniform-2097152, b9-large-one-thread: `grust-next@counted+f32#1` stopped at 19, `neo4j-graph` at 26.
- uniform-2097152, b9-large-one-thread: `grust-next@counted+f32#unset` stopped at 20, `neo4j-graph` at 26.
- uniform-2097152, b9-large-one-thread: `grust-next@unchecked+f32#1` stopped at 19, `neo4j-graph` at 26.
- uniform-2097152, b9-large-one-thread: `grust-next@unchecked+f32#unset` stopped at 20, `neo4j-graph` at 26.
- hub-2097152, b9-large-full-width: `grust-next@counted+f32` stopped at 20, `neo4j-graph` at 28.
- hub-2097152, b9-large-full-width: `grust-next@unchecked+f32` stopped at 20, `neo4j-graph` at 28.
- uniform-2097152, b9-large-full-width: `grust-next@counted+f32` stopped at 19, `neo4j-graph` at 28.
- uniform-2097152, b9-large-full-width: `grust-next@unchecked+f32` stopped at 19, `neo4j-graph` at 28.
- hub-4194304, b9-xlarge-one-thread: `grust-next@counted+f32#1` stopped at 20, `neo4j-graph` at 23.
- hub-4194304, b9-xlarge-one-thread: `grust-next@counted+f32#unset` stopped at 21, `neo4j-graph` at 23.
- hub-4194304, b9-xlarge-one-thread: `grust-next@unchecked+f32#1` stopped at 20, `neo4j-graph` at 23.
- hub-4194304, b9-xlarge-one-thread: `grust-next@unchecked+f32#unset` stopped at 21, `neo4j-graph` at 23.
- uniform-4194304, b9-xlarge-one-thread: `grust-next@counted+f32#1` stopped at 19, `neo4j-graph` at 29.
- uniform-4194304, b9-xlarge-one-thread: `grust-next@counted+f32#unset` stopped at 20, `neo4j-graph` at 29.
- uniform-4194304, b9-xlarge-one-thread: `grust-next@unchecked+f32#1` stopped at 19, `neo4j-graph` at 29.
- uniform-4194304, b9-xlarge-one-thread: `grust-next@unchecked+f32#unset` stopped at 20, `neo4j-graph` at 29.
- hub-4194304, b9-xlarge-full-width: `grust-next@counted+f32` stopped at 20, `neo4j-graph` at 14.
- hub-4194304, b9-xlarge-full-width: `grust-next@unchecked+f32` stopped at 20, `neo4j-graph` at 14.
- uniform-4194304, b9-xlarge-full-width: `grust-next@counted+f32` stopped at 19, `neo4j-graph` at 29.
- uniform-4194304, b9-xlarge-full-width: `grust-next@unchecked+f32` stopped at 19, `neo4j-graph` at 29.

## Parity

Every row parity produced for the participants B9 times, PageRank only. `vector` is how many of the n scores were bit-identical to the reference's f64 scores and the largest distance, in f64 ulps and in absolute terms; for an f32 row, widened to f64, the ulp figure is meaningless and the absolute one is the distance. It is recorded and not gated, as it is for every row. `bits` is the bit gate: f64 builds against v0.22.0, `+f32` builds against their counted row.

| file | fixture | participant | concurrency | verdict | iters | residual | vector | bits | detail |
| --- | --- | --- | --- | --- | ---: | ---: | --- | --- | --- |
| parity-b9-fixtures-1.json | hub-16384 | `neo4j-graph` | 1 | agrees | 36 | 9.29e-09 |  |  |  |
| parity-b9-fixtures-1.json | hub-16384 | `grust` | 1 | agrees | 17 | 3.23e-09 | 7352/16384, max 4 f64 ulps, 8.13e-20 abs |  |  |
| parity-b9-fixtures-1.json | hub-16384 | `grust-next@counted` | 1 | agrees | 17 | 3.23e-09 | 7352/16384, max 4 f64 ulps, 8.13e-20 abs | same as `grust` |  |
| parity-b9-fixtures-1.json | hub-16384 | `grust-next@unchecked` | 1 | agrees | 17 | 3.23e-09 | 7352/16384, max 4 f64 ulps, 8.13e-20 abs | same as `grust` |  |
| parity-b9-fixtures-1.json | hub-16384 | `grust-next@counted+f32` | 1 | agrees | 20 | 8.8e-09 | 0/16384, max 2621868491 f64 ulps, 4.38e-11 abs |  |  |
| parity-b9-fixtures-1.json | hub-16384 | `grust-next@unchecked+f32` | 1 | agrees | 20 | 8.8e-09 | 0/16384, max 2621868491 f64 ulps, 4.38e-11 abs | same as `grust-next@counted+f32` |  |
| parity-b9-fixtures-1.json | hub-65536 | `neo4j-graph` | 1 | agrees | 33 | 8.89e-09 |  |  |  |
| parity-b9-fixtures-1.json | hub-65536 | `grust` | 1 | agrees | 17 | 3.24e-09 | 29623/65536, max 4 f64 ulps, 1.36e-20 abs |  |  |
| parity-b9-fixtures-1.json | hub-65536 | `grust-next@counted` | 1 | agrees | 17 | 3.24e-09 | 29623/65536, max 4 f64 ulps, 1.36e-20 abs | same as `grust` |  |
| parity-b9-fixtures-1.json | hub-65536 | `grust-next@unchecked` | 1 | agrees | 17 | 3.24e-09 | 29623/65536, max 4 f64 ulps, 1.36e-20 abs | same as `grust` |  |
| parity-b9-fixtures-1.json | hub-65536 | `grust-next@counted+f32` | 1 | agrees | 20 | 8.44e-09 | 0/65536, max 2944077174 f64 ulps, 1.5e-11 abs |  |  |
| parity-b9-fixtures-1.json | hub-65536 | `grust-next@unchecked+f32` | 1 | agrees | 20 | 8.44e-09 | 0/65536, max 2944077174 f64 ulps, 1.5e-11 abs | same as `grust-next@counted+f32` |  |
| parity-b9-fixtures-1.json | uniform-16384 | `neo4j-graph` | 1 | agrees | 28 | 9.64e-09 |  |  |  |
| parity-b9-fixtures-1.json | uniform-16384 | `grust` | 1 | agrees | 16 | 3.36e-09 | 7355/16384, max 4 f64 ulps, 5.42e-20 abs |  |  |
| parity-b9-fixtures-1.json | uniform-16384 | `grust-next@counted` | 1 | agrees | 16 | 3.36e-09 | 7355/16384, max 4 f64 ulps, 5.42e-20 abs | same as `grust` |  |
| parity-b9-fixtures-1.json | uniform-16384 | `grust-next@unchecked` | 1 | agrees | 16 | 3.36e-09 | 7355/16384, max 4 f64 ulps, 5.42e-20 abs | same as `grust` |  |
| parity-b9-fixtures-1.json | uniform-16384 | `grust-next@counted+f32` | 1 | agrees | 19 | 8.76e-09 | 0/16384, max 2959917052 f64 ulps, 4.48e-11 abs |  |  |
| parity-b9-fixtures-1.json | uniform-16384 | `grust-next@unchecked+f32` | 1 | agrees | 19 | 8.76e-09 | 0/16384, max 2959917052 f64 ulps, 4.48e-11 abs | same as `grust-next@counted+f32` |  |
| parity-b9-fixtures-1.json | uniform-65536 | `neo4j-graph` | 1 | agrees | 34 | 9.64e-09 |  |  |  |
| parity-b9-fixtures-1.json | uniform-65536 | `grust` | 1 | agrees | 16 | 3.43e-09 | 29430/65536, max 4 f64 ulps, 2.03e-20 abs |  |  |
| parity-b9-fixtures-1.json | uniform-65536 | `grust-next@counted` | 1 | agrees | 16 | 3.43e-09 | 29430/65536, max 4 f64 ulps, 2.03e-20 abs | same as `grust` |  |
| parity-b9-fixtures-1.json | uniform-65536 | `grust-next@unchecked` | 1 | agrees | 16 | 3.43e-09 | 29430/65536, max 4 f64 ulps, 2.03e-20 abs | same as `grust` |  |
| parity-b9-fixtures-1.json | uniform-65536 | `grust-next@counted+f32` | 1 | agrees | 19 | 8.53e-09 | 0/65536, max 3047578129 f64 ulps, 1.15e-11 abs |  |  |
| parity-b9-fixtures-1.json | uniform-65536 | `grust-next@unchecked+f32` | 1 | agrees | 19 | 8.53e-09 | 0/65536, max 3047578129 f64 ulps, 1.15e-11 abs | same as `grust-next@counted+f32` |  |
| parity-b9-fixtures-16.json | hub-16384 | `neo4j-graph` | 16 | agrees | 36 | 9.29e-09 |  |  |  |
| parity-b9-fixtures-16.json | hub-16384 | `grust` | 16 | agrees | 17 | 3.23e-09 | 7352/16384, max 4 f64 ulps, 8.13e-20 abs |  |  |
| parity-b9-fixtures-16.json | hub-16384 | `grust-next@counted` | 16 | agrees | 17 | 3.23e-09 | 7352/16384, max 4 f64 ulps, 8.13e-20 abs | same as `grust` |  |
| parity-b9-fixtures-16.json | hub-16384 | `grust-next@unchecked` | 16 | agrees | 17 | 3.23e-09 | 7352/16384, max 4 f64 ulps, 8.13e-20 abs | same as `grust` |  |
| parity-b9-fixtures-16.json | hub-16384 | `grust-next@counted+f32` | 16 | agrees | 20 | 8.8e-09 | 0/16384, max 2621868491 f64 ulps, 4.38e-11 abs |  |  |
| parity-b9-fixtures-16.json | hub-16384 | `grust-next@unchecked+f32` | 16 | agrees | 20 | 8.8e-09 | 0/16384, max 2621868491 f64 ulps, 4.38e-11 abs | same as `grust-next@counted+f32` |  |
| parity-b9-fixtures-16.json | hub-65536 | `neo4j-graph` | 16 | agrees | 30 | 9.45e-09 |  |  |  |
| parity-b9-fixtures-16.json | hub-65536 | `grust` | 16 | agrees | 17 | 3.24e-09 | 29623/65536, max 4 f64 ulps, 1.36e-20 abs |  |  |
| parity-b9-fixtures-16.json | hub-65536 | `grust-next@counted` | 16 | agrees | 17 | 3.24e-09 | 29623/65536, max 4 f64 ulps, 1.36e-20 abs | same as `grust` |  |
| parity-b9-fixtures-16.json | hub-65536 | `grust-next@unchecked` | 16 | agrees | 17 | 3.24e-09 | 29623/65536, max 4 f64 ulps, 1.36e-20 abs | same as `grust` |  |
| parity-b9-fixtures-16.json | hub-65536 | `grust-next@counted+f32` | 16 | agrees | 20 | 8.44e-09 | 0/65536, max 2944077174 f64 ulps, 1.5e-11 abs |  |  |
| parity-b9-fixtures-16.json | hub-65536 | `grust-next@unchecked+f32` | 16 | agrees | 20 | 8.44e-09 | 0/65536, max 2944077174 f64 ulps, 1.5e-11 abs | same as `grust-next@counted+f32` |  |
| parity-b9-fixtures-16.json | uniform-16384 | `neo4j-graph` | 16 | agrees | 28 | 9.64e-09 |  |  |  |
| parity-b9-fixtures-16.json | uniform-16384 | `grust` | 16 | agrees | 16 | 3.36e-09 | 7355/16384, max 4 f64 ulps, 5.42e-20 abs |  |  |
| parity-b9-fixtures-16.json | uniform-16384 | `grust-next@counted` | 16 | agrees | 16 | 3.36e-09 | 7355/16384, max 4 f64 ulps, 5.42e-20 abs | same as `grust` |  |
| parity-b9-fixtures-16.json | uniform-16384 | `grust-next@unchecked` | 16 | agrees | 16 | 3.36e-09 | 7355/16384, max 4 f64 ulps, 5.42e-20 abs | same as `grust` |  |
| parity-b9-fixtures-16.json | uniform-16384 | `grust-next@counted+f32` | 16 | agrees | 19 | 8.76e-09 | 0/16384, max 2959917052 f64 ulps, 4.48e-11 abs |  |  |
| parity-b9-fixtures-16.json | uniform-16384 | `grust-next@unchecked+f32` | 16 | agrees | 19 | 8.76e-09 | 0/16384, max 2959917052 f64 ulps, 4.48e-11 abs | same as `grust-next@counted+f32` |  |
| parity-b9-fixtures-16.json | uniform-65536 | `neo4j-graph` | 16 | agrees | 34 | 9.61e-09 |  |  |  |
| parity-b9-fixtures-16.json | uniform-65536 | `grust` | 16 | agrees | 16 | 3.43e-09 | 29430/65536, max 4 f64 ulps, 2.03e-20 abs |  |  |
| parity-b9-fixtures-16.json | uniform-65536 | `grust-next@counted` | 16 | agrees | 16 | 3.43e-09 | 29430/65536, max 4 f64 ulps, 2.03e-20 abs | same as `grust` |  |
| parity-b9-fixtures-16.json | uniform-65536 | `grust-next@unchecked` | 16 | agrees | 16 | 3.43e-09 | 29430/65536, max 4 f64 ulps, 2.03e-20 abs | same as `grust` |  |
| parity-b9-fixtures-16.json | uniform-65536 | `grust-next@counted+f32` | 16 | agrees | 19 | 8.53e-09 | 0/65536, max 3047578129 f64 ulps, 1.15e-11 abs |  |  |
| parity-b9-fixtures-16.json | uniform-65536 | `grust-next@unchecked+f32` | 16 | agrees | 19 | 8.53e-09 | 0/65536, max 3047578129 f64 ulps, 1.15e-11 abs | same as `grust-next@counted+f32` |  |
| parity-b9-fixtures-large-1.json | hub-2097152 | `neo4j-graph` | 1 | agrees | 28 | 8.34e-09 |  |  |  |
| parity-b9-fixtures-large-1.json | hub-2097152 | `grust` | 1 | agrees | 16 | 9.96e-09 | 937899/2097152, max 6 f64 ulps, 8.47e-22 abs |  |  |
| parity-b9-fixtures-large-1.json | hub-2097152 | `grust-next@counted` | 1 | agrees | 16 | 9.96e-09 | 937899/2097152, max 6 f64 ulps, 8.47e-22 abs | same as `grust` |  |
| parity-b9-fixtures-large-1.json | hub-2097152 | `grust-next@unchecked` | 1 | agrees | 16 | 9.96e-09 | 937899/2097152, max 6 f64 ulps, 8.47e-22 abs | same as `grust` |  |
| parity-b9-fixtures-large-1.json | hub-2097152 | `grust-next@counted+f32` | 1 | agrees | 20 | 8.19e-09 | 0/2097152, max 3109437963 f64 ulps, 4.95e-13 abs |  |  |
| parity-b9-fixtures-large-1.json | hub-2097152 | `grust-next@unchecked+f32` | 1 | agrees | 20 | 8.19e-09 | 0/2097152, max 3109437963 f64 ulps, 4.95e-13 abs | same as `grust-next@counted+f32` |  |
| parity-b9-fixtures-large-1.json | uniform-2097152 | `neo4j-graph` | 1 | agrees | 28 | 8.31e-09 |  |  |  |
| parity-b9-fixtures-large-1.json | uniform-2097152 | `grust` | 1 | agrees | 16 | 3.46e-09 | 943172/2097152, max 6 f64 ulps, 8.47e-22 abs |  |  |
| parity-b9-fixtures-large-1.json | uniform-2097152 | `grust-next@counted` | 1 | agrees | 16 | 3.46e-09 | 943172/2097152, max 6 f64 ulps, 8.47e-22 abs | same as `grust` |  |
| parity-b9-fixtures-large-1.json | uniform-2097152 | `grust-next@unchecked` | 1 | agrees | 16 | 3.46e-09 | 943172/2097152, max 6 f64 ulps, 8.47e-22 abs | same as `grust` |  |
| parity-b9-fixtures-large-1.json | uniform-2097152 | `grust-next@counted+f32` | 1 | agrees | 19 | 8.59e-09 | 0/2097152, max 3389236176 f64 ulps, 4.79e-13 abs |  |  |
| parity-b9-fixtures-large-1.json | uniform-2097152 | `grust-next@unchecked+f32` | 1 | agrees | 19 | 8.59e-09 | 0/2097152, max 3389236176 f64 ulps, 4.79e-13 abs | same as `grust-next@counted+f32` |  |
| parity-b9-fixtures-large-16.json | hub-2097152 | `neo4j-graph` | 16 | agrees | 28 | 8.21e-09 |  |  |  |
| parity-b9-fixtures-large-16.json | hub-2097152 | `grust` | 16 | agrees | 16 | 9.96e-09 | 937899/2097152, max 6 f64 ulps, 8.47e-22 abs |  |  |
| parity-b9-fixtures-large-16.json | hub-2097152 | `grust-next@counted` | 16 | agrees | 16 | 9.96e-09 | 937899/2097152, max 6 f64 ulps, 8.47e-22 abs | same as `grust` |  |
| parity-b9-fixtures-large-16.json | hub-2097152 | `grust-next@unchecked` | 16 | agrees | 16 | 9.96e-09 | 937899/2097152, max 6 f64 ulps, 8.47e-22 abs | same as `grust` |  |
| parity-b9-fixtures-large-16.json | hub-2097152 | `grust-next@counted+f32` | 16 | agrees | 20 | 8.19e-09 | 0/2097152, max 3109437963 f64 ulps, 4.95e-13 abs |  |  |
| parity-b9-fixtures-large-16.json | hub-2097152 | `grust-next@unchecked+f32` | 16 | agrees | 20 | 8.19e-09 | 0/2097152, max 3109437963 f64 ulps, 4.95e-13 abs | same as `grust-next@counted+f32` |  |
| parity-b9-fixtures-large-16.json | uniform-2097152 | `neo4j-graph` | 16 | agrees | 28 | 8.76e-09 |  |  |  |
| parity-b9-fixtures-large-16.json | uniform-2097152 | `grust` | 16 | agrees | 16 | 3.46e-09 | 943172/2097152, max 6 f64 ulps, 8.47e-22 abs |  |  |
| parity-b9-fixtures-large-16.json | uniform-2097152 | `grust-next@counted` | 16 | agrees | 16 | 3.46e-09 | 943172/2097152, max 6 f64 ulps, 8.47e-22 abs | same as `grust` |  |
| parity-b9-fixtures-large-16.json | uniform-2097152 | `grust-next@unchecked` | 16 | agrees | 16 | 3.46e-09 | 943172/2097152, max 6 f64 ulps, 8.47e-22 abs | same as `grust` |  |
| parity-b9-fixtures-large-16.json | uniform-2097152 | `grust-next@counted+f32` | 16 | agrees | 19 | 8.59e-09 | 0/2097152, max 3389236176 f64 ulps, 4.79e-13 abs |  |  |
| parity-b9-fixtures-large-16.json | uniform-2097152 | `grust-next@unchecked+f32` | 16 | agrees | 19 | 8.59e-09 | 0/2097152, max 3389236176 f64 ulps, 4.79e-13 abs | same as `grust-next@counted+f32` |  |
| parity-b9-fixtures-large-unset.json | hub-2097152 | `neo4j-graph` | unset | agrees | 28 | 8.79e-09 |  |  |  |
| parity-b9-fixtures-large-unset.json | hub-2097152 | `grust` | unset | agrees | 16 | 9.96e-09 | 106053/2097152, max 8 f64 ulps, 1.06e-21 abs |  |  |
| parity-b9-fixtures-large-unset.json | hub-2097152 | `grust-next@counted` | unset | agrees | 16 | 9.96e-09 | 106053/2097152, max 8 f64 ulps, 1.06e-21 abs | same as `grust` |  |
| parity-b9-fixtures-large-unset.json | hub-2097152 | `grust-next@unchecked` | unset | agrees | 16 | 9.96e-09 | 106053/2097152, max 8 f64 ulps, 1.06e-21 abs | same as `grust` |  |
| parity-b9-fixtures-large-unset.json | hub-2097152 | `grust-next@counted+f32` | unset | agrees | 21 | 8.2e-09 | 0/2097152, max 6097654486 f64 ulps, 9.28e-13 abs |  |  |
| parity-b9-fixtures-large-unset.json | hub-2097152 | `grust-next@unchecked+f32` | unset | agrees | 21 | 8.2e-09 | 0/2097152, max 6097654486 f64 ulps, 9.28e-13 abs | same as `grust-next@counted+f32` |  |
| parity-b9-fixtures-large-unset.json | uniform-2097152 | `neo4j-graph` | unset | agrees | 27 | 8.85e-09 |  |  |  |
| parity-b9-fixtures-large-unset.json | uniform-2097152 | `grust` | unset | agrees | 16 | 3.46e-09 | 2097053/2097152, max 2 f64 ulps, 2.12e-22 abs |  |  |
| parity-b9-fixtures-large-unset.json | uniform-2097152 | `grust-next@counted` | unset | agrees | 16 | 3.46e-09 | 2097053/2097152, max 2 f64 ulps, 2.12e-22 abs | same as `grust` |  |
| parity-b9-fixtures-large-unset.json | uniform-2097152 | `grust-next@unchecked` | unset | agrees | 16 | 3.46e-09 | 2097053/2097152, max 2 f64 ulps, 2.12e-22 abs | same as `grust` |  |
| parity-b9-fixtures-large-unset.json | uniform-2097152 | `grust-next@counted+f32` | unset | agrees | 20 | 8.43e-09 | 0/2097152, max 3561951160 f64 ulps, 4.88e-13 abs |  |  |
| parity-b9-fixtures-large-unset.json | uniform-2097152 | `grust-next@unchecked+f32` | unset | agrees | 20 | 8.43e-09 | 0/2097152, max 3561951160 f64 ulps, 4.88e-13 abs | same as `grust-next@counted+f32` |  |
| parity-b9-fixtures-unset.json | hub-16384 | `neo4j-graph` | unset | agrees | 36 | 9.29e-09 |  |  |  |
| parity-b9-fixtures-unset.json | hub-16384 | `grust` | unset | agrees | 17 | 3.23e-09 | 699/16384, max 6 f64 ulps, 1.08e-19 abs |  |  |
| parity-b9-fixtures-unset.json | hub-16384 | `grust-next@counted` | unset | agrees | 17 | 3.23e-09 | 699/16384, max 6 f64 ulps, 1.08e-19 abs | same as `grust` |  |
| parity-b9-fixtures-unset.json | hub-16384 | `grust-next@unchecked` | unset | agrees | 17 | 3.23e-09 | 699/16384, max 6 f64 ulps, 1.08e-19 abs | same as `grust` |  |
| parity-b9-fixtures-unset.json | hub-16384 | `grust-next@counted+f32` | unset | agrees | 21 | 8.58e-09 | 0/16384, max 5491328727 f64 ulps, 9.72e-11 abs |  |  |
| parity-b9-fixtures-unset.json | hub-16384 | `grust-next@unchecked+f32` | unset | agrees | 21 | 8.58e-09 | 0/16384, max 5491328727 f64 ulps, 9.72e-11 abs | same as `grust-next@counted+f32` |  |
| parity-b9-fixtures-unset.json | hub-65536 | `neo4j-graph` | unset | agrees | 31 | 7.92e-09 |  |  |  |
| parity-b9-fixtures-unset.json | hub-65536 | `grust` | unset | agrees | 17 | 3.24e-09 | 3230/65536, max 7 f64 ulps, 2.71e-20 abs |  |  |
| parity-b9-fixtures-unset.json | hub-65536 | `grust-next@counted` | unset | agrees | 17 | 3.24e-09 | 3230/65536, max 7 f64 ulps, 2.71e-20 abs | same as `grust` |  |
| parity-b9-fixtures-unset.json | hub-65536 | `grust-next@unchecked` | unset | agrees | 17 | 3.24e-09 | 3230/65536, max 7 f64 ulps, 2.71e-20 abs | same as `grust` |  |
| parity-b9-fixtures-unset.json | hub-65536 | `grust-next@counted+f32` | unset | agrees | 21 | 8.04e-09 | 0/65536, max 6037950115 f64 ulps, 2.41e-11 abs |  |  |
| parity-b9-fixtures-unset.json | hub-65536 | `grust-next@unchecked+f32` | unset | agrees | 21 | 8.04e-09 | 0/65536, max 6037950115 f64 ulps, 2.41e-11 abs | same as `grust-next@counted+f32` |  |
| parity-b9-fixtures-unset.json | uniform-16384 | `neo4j-graph` | unset | agrees | 28 | 9.64e-09 |  |  |  |
| parity-b9-fixtures-unset.json | uniform-16384 | `grust` | unset | agrees | 16 | 3.36e-09 | 16325/16384, max 2 f64 ulps, 2.71e-20 abs |  |  |
| parity-b9-fixtures-unset.json | uniform-16384 | `grust-next@counted` | unset | agrees | 16 | 3.36e-09 | 16325/16384, max 2 f64 ulps, 2.71e-20 abs | same as `grust` |  |
| parity-b9-fixtures-unset.json | uniform-16384 | `grust-next@unchecked` | unset | agrees | 16 | 3.36e-09 | 16325/16384, max 2 f64 ulps, 2.71e-20 abs | same as `grust` |  |
| parity-b9-fixtures-unset.json | uniform-16384 | `grust-next@counted+f32` | unset | agrees | 19 | 9.5e-09 | 0/16384, max 2960955813 f64 ulps, 4.28e-11 abs |  |  |
| parity-b9-fixtures-unset.json | uniform-16384 | `grust-next@unchecked+f32` | unset | agrees | 19 | 9.5e-09 | 0/16384, max 2960955813 f64 ulps, 4.28e-11 abs | same as `grust-next@counted+f32` |  |
| parity-b9-fixtures-unset.json | uniform-65536 | `neo4j-graph` | unset | agrees | 34 | 8.89e-09 |  |  |  |
| parity-b9-fixtures-unset.json | uniform-65536 | `grust` | unset | agrees | 16 | 3.43e-09 | 65467/65536, max 2 f64 ulps, 6.78e-21 abs |  |  |
| parity-b9-fixtures-unset.json | uniform-65536 | `grust-next@counted` | unset | agrees | 16 | 3.43e-09 | 65467/65536, max 2 f64 ulps, 6.78e-21 abs | same as `grust` |  |
| parity-b9-fixtures-unset.json | uniform-65536 | `grust-next@unchecked` | unset | agrees | 16 | 3.43e-09 | 65467/65536, max 2 f64 ulps, 6.78e-21 abs | same as `grust` |  |
| parity-b9-fixtures-unset.json | uniform-65536 | `grust-next@counted+f32` | unset | agrees | 20 | 8.39e-09 | 0/65536, max 3317924464 f64 ulps, 1.36e-11 abs |  |  |
| parity-b9-fixtures-unset.json | uniform-65536 | `grust-next@unchecked+f32` | unset | agrees | 20 | 8.39e-09 | 0/65536, max 3317924464 f64 ulps, 1.36e-11 abs | same as `grust-next@counted+f32` |  |
| parity-b9-fixtures-xlarge-1.json | hub-4194304 | `neo4j-graph` | 1 | agrees | 20 | 9.64e-09 |  |  |  |
| parity-b9-fixtures-xlarge-1.json | hub-4194304 | `grust` | 1 | agrees | 16 | 9.96e-09 | 1874065/4194304, max 6 f64 ulps, 4.24e-22 abs |  |  |
| parity-b9-fixtures-xlarge-1.json | hub-4194304 | `grust-next@counted` | 1 | agrees | 16 | 9.96e-09 | 1874065/4194304, max 6 f64 ulps, 4.24e-22 abs | same as `grust` |  |
| parity-b9-fixtures-xlarge-1.json | hub-4194304 | `grust-next@unchecked` | 1 | agrees | 16 | 9.96e-09 | 1874065/4194304, max 6 f64 ulps, 4.24e-22 abs | same as `grust` |  |
| parity-b9-fixtures-xlarge-1.json | hub-4194304 | `grust-next@counted+f32` | 1 | agrees | 20 | 8.21e-09 | 0/4194304, max 3452255767 f64 ulps, 2.6e-13 abs |  |  |
| parity-b9-fixtures-xlarge-1.json | hub-4194304 | `grust-next@unchecked+f32` | 1 | agrees | 20 | 8.21e-09 | 0/4194304, max 3452255767 f64 ulps, 2.6e-13 abs | same as `grust-next@counted+f32` |  |
| parity-b9-fixtures-xlarge-1.json | uniform-4194304 | `neo4j-graph` | 1 | agrees | 29 | 7.9e-09 |  |  |  |
| parity-b9-fixtures-xlarge-1.json | uniform-4194304 | `grust` | 1 | agrees | 16 | 3.47e-09 | 1884240/4194304, max 6 f64 ulps, 4.24e-22 abs |  |  |
| parity-b9-fixtures-xlarge-1.json | uniform-4194304 | `grust-next@counted` | 1 | agrees | 16 | 3.47e-09 | 1884240/4194304, max 6 f64 ulps, 4.24e-22 abs | same as `grust` |  |
| parity-b9-fixtures-xlarge-1.json | uniform-4194304 | `grust-next@unchecked` | 1 | agrees | 16 | 3.47e-09 | 1884240/4194304, max 6 f64 ulps, 4.24e-22 abs | same as `grust` |  |
| parity-b9-fixtures-xlarge-1.json | uniform-4194304 | `grust-next@counted+f32` | 1 | agrees | 19 | 8.61e-09 | 0/4194304, max 3146797518 f64 ulps, 2.6e-13 abs |  |  |
| parity-b9-fixtures-xlarge-1.json | uniform-4194304 | `grust-next@unchecked+f32` | 1 | agrees | 19 | 8.61e-09 | 0/4194304, max 3146797518 f64 ulps, 2.6e-13 abs | same as `grust-next@counted+f32` |  |
| parity-b9-fixtures-xlarge-16.json | hub-4194304 | `neo4j-graph` | 16 | agrees | 14 | 9.9e-09 |  |  |  |
| parity-b9-fixtures-xlarge-16.json | hub-4194304 | `grust` | 16 | agrees | 16 | 9.96e-09 | 1874065/4194304, max 6 f64 ulps, 4.24e-22 abs |  |  |
| parity-b9-fixtures-xlarge-16.json | hub-4194304 | `grust-next@counted` | 16 | agrees | 16 | 9.96e-09 | 1874065/4194304, max 6 f64 ulps, 4.24e-22 abs | same as `grust` |  |
| parity-b9-fixtures-xlarge-16.json | hub-4194304 | `grust-next@unchecked` | 16 | agrees | 16 | 9.96e-09 | 1874065/4194304, max 6 f64 ulps, 4.24e-22 abs | same as `grust` |  |
| parity-b9-fixtures-xlarge-16.json | hub-4194304 | `grust-next@counted+f32` | 16 | agrees | 20 | 8.21e-09 | 0/4194304, max 3452255767 f64 ulps, 2.6e-13 abs |  |  |
| parity-b9-fixtures-xlarge-16.json | hub-4194304 | `grust-next@unchecked+f32` | 16 | agrees | 20 | 8.21e-09 | 0/4194304, max 3452255767 f64 ulps, 2.6e-13 abs | same as `grust-next@counted+f32` |  |
| parity-b9-fixtures-xlarge-16.json | uniform-4194304 | `neo4j-graph` | 16 | agrees | 29 | 8.48e-09 |  |  |  |
| parity-b9-fixtures-xlarge-16.json | uniform-4194304 | `grust` | 16 | agrees | 16 | 3.47e-09 | 1884240/4194304, max 6 f64 ulps, 4.24e-22 abs |  |  |
| parity-b9-fixtures-xlarge-16.json | uniform-4194304 | `grust-next@counted` | 16 | agrees | 16 | 3.47e-09 | 1884240/4194304, max 6 f64 ulps, 4.24e-22 abs | same as `grust` |  |
| parity-b9-fixtures-xlarge-16.json | uniform-4194304 | `grust-next@unchecked` | 16 | agrees | 16 | 3.47e-09 | 1884240/4194304, max 6 f64 ulps, 4.24e-22 abs | same as `grust` |  |
| parity-b9-fixtures-xlarge-16.json | uniform-4194304 | `grust-next@counted+f32` | 16 | agrees | 19 | 8.61e-09 | 0/4194304, max 3146797518 f64 ulps, 2.6e-13 abs |  |  |
| parity-b9-fixtures-xlarge-16.json | uniform-4194304 | `grust-next@unchecked+f32` | 16 | agrees | 19 | 8.61e-09 | 0/4194304, max 3146797518 f64 ulps, 2.6e-13 abs | same as `grust-next@counted+f32` |  |
| parity-b9-fixtures-xlarge-unset.json | hub-4194304 | `neo4j-graph` | unset | agrees | 16 | 9.4e-09 |  |  |  |
| parity-b9-fixtures-xlarge-unset.json | hub-4194304 | `grust` | unset | agrees | 16 | 9.96e-09 | 211043/4194304, max 8 f64 ulps, 5.29e-22 abs |  |  |
| parity-b9-fixtures-xlarge-unset.json | hub-4194304 | `grust-next@counted` | unset | agrees | 16 | 9.96e-09 | 211043/4194304, max 8 f64 ulps, 5.29e-22 abs | same as `grust` |  |
| parity-b9-fixtures-xlarge-unset.json | hub-4194304 | `grust-next@unchecked` | unset | agrees | 16 | 9.96e-09 | 211043/4194304, max 8 f64 ulps, 5.29e-22 abs | same as `grust` |  |
| parity-b9-fixtures-xlarge-unset.json | hub-4194304 | `grust-next@counted+f32` | unset | agrees | 21 | 8.31e-09 | 0/4194304, max 6393034292 f64 ulps, 4.45e-13 abs |  |  |
| parity-b9-fixtures-xlarge-unset.json | hub-4194304 | `grust-next@unchecked+f32` | unset | agrees | 21 | 8.31e-09 | 0/4194304, max 6393034292 f64 ulps, 4.45e-13 abs | same as `grust-next@counted+f32` |  |
| parity-b9-fixtures-xlarge-unset.json | uniform-4194304 | `neo4j-graph` | unset | agrees | 29 | 9.05e-09 |  |  |  |
| parity-b9-fixtures-xlarge-unset.json | uniform-4194304 | `grust` | unset | agrees | 16 | 3.47e-09 | 4194236/4194304, max 2 f64 ulps, 1.06e-22 abs |  |  |
| parity-b9-fixtures-xlarge-unset.json | uniform-4194304 | `grust-next@counted` | unset | agrees | 16 | 3.47e-09 | 4194236/4194304, max 2 f64 ulps, 1.06e-22 abs | same as `grust` |  |
| parity-b9-fixtures-xlarge-unset.json | uniform-4194304 | `grust-next@unchecked` | unset | agrees | 16 | 3.47e-09 | 4194236/4194304, max 2 f64 ulps, 1.06e-22 abs | same as `grust` |  |
| parity-b9-fixtures-xlarge-unset.json | uniform-4194304 | `grust-next@counted+f32` | unset | agrees | 20 | 8.48e-09 | 0/4194304, max 3709657623 f64 ulps, 2.74e-13 abs |  |  |
| parity-b9-fixtures-xlarge-unset.json | uniform-4194304 | `grust-next@unchecked+f32` | unset | agrees | 20 | 8.48e-09 | 0/4194304, max 3709657623 f64 ulps, 2.74e-13 abs | same as `grust-next@counted+f32` |  |

