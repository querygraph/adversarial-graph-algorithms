# B7 tables

Every PageRank cell, with its iteration count beside its total and its per-iteration time. The precision column is what the participant declared in its receipt. Two cells whose iteration counts differ did not do the same work, and their totals are not compared; their per-iteration times are. A row marked UNUSABLE is printed with its numbers and enters no comparison.

## `b7-one-thread.json`: b7-one-thread

workers 1, concurrency 1, allocator glibc default, not pinned, 1 warmup + 5 repeats, steal over the run 0 ticks, 31.3 s, unusable at MAD/median >= 0.25

| fixture | participant | precision | accounting | kernel | call | iters | converged | residual | total ms | MAD | MAD/median | per iter ms | build ms | incoming ms | minflt | steal | usable |
| --- | --- | --- | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| hub-16384 | `neo4j-graph` | f32 |  |  |  | 36 |  | 9.29e-09 | 13.257 | 0.031 | 0.002 | 0.3683 | 7.90 | - | 24 | 0 | yes |
| hub-16384 | `grust#1` | f64 | counted | pull | first | 17 | yes | 3.23e-09 | 11.628 | 0.041 | 0.003 | 0.6840 | 18.83 | - | 384 | 0 | yes |
| hub-16384 | `grust#1` | f64 | counted | pull | second | 17 | yes | 3.23e-09 | 9.658 | 0.016 | 0.002 | 0.5681 | 18.83 | - | 0 | 0 | yes |
| hub-16384 | `grust-next@counted#1` | f64 | counted | pull | first | 17 | yes | 3.23e-09 | 8.124 | 0.013 | 0.002 | 0.4779 | 12.00 | 1.50 | 96 | 0 | yes |
| hub-16384 | `grust-next@counted#1` | f64 | counted | pull | second | 17 | yes | 3.23e-09 | 7.889 | 0.006 | 0.001 | 0.4640 | 12.00 | 1.50 | 0 | 0 | yes |
| hub-16384 | `grust-next@unchecked#1` | f64 | unchecked | pull | first | 17 | yes | 3.23e-09 | 7.769 | 0.013 | 0.002 | 0.4570 | 9.91 | 1.33 | 96 | 0 | yes |
| hub-16384 | `grust-next@unchecked#1` | f64 | unchecked | pull | second | 17 | yes | 3.23e-09 | 7.552 | 0.008 | 0.001 | 0.4442 | 9.91 | 1.33 | 0 | 0 | yes |
| hub-16384 | `grust-next@counted+f32#1` | f32 | counted | pull | first | 20 | yes | 8.8e-09 | 9.369 | 0.015 | 0.002 | 0.4685 | 12.04 | 1.51 | 48 | 0 | yes |
| hub-16384 | `grust-next@counted+f32#1` | f32 | counted | pull | second | 20 | yes | 8.8e-09 | 9.260 | 0.005 | 0.001 | 0.4630 | 12.04 | 1.51 | 0 | 0 | yes |
| hub-16384 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | first | 20 | yes | 8.8e-09 | 9.213 | 0.027 | 0.003 | 0.4606 | 10.21 | 1.37 | 48 | 0 | yes |
| hub-16384 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | second | 20 | yes | 8.8e-09 | 9.055 | 0.013 | 0.001 | 0.4527 | 10.21 | 1.37 | 0 | 0 | yes |
| hub-16384 | `grust-next@counted#unset` | f64 | counted | push | first | 17 | yes | 3.23e-09 | 23.479 | 0.036 | 0.002 | 1.3811 | 12.86 | - | 128 | 0 | yes |
| hub-16384 | `grust-next@counted#unset` | f64 | counted | push | second | 17 | yes | 3.23e-09 | 23.254 | 0.046 | 0.002 | 1.3679 | 12.86 | - | 32 | 0 | yes |
| hub-16384 | `grust-next@unchecked#unset` | f64 | unchecked | push | first | 17 | yes | 3.23e-09 | 13.765 | 0.150 | 0.011 | 0.8097 | 8.70 | - | 128 | 0 | yes |
| hub-16384 | `grust-next@unchecked#unset` | f64 | unchecked | push | second | 17 | yes | 3.23e-09 | 13.468 | 0.034 | 0.003 | 0.7923 | 8.70 | - | 32 | 0 | yes |
| hub-16384 | `grust-next@counted+f32#unset` | f32 | counted | push | first | 21 | yes | 8.58e-09 | 27.966 | 0.034 | 0.001 | 1.3317 | 13.03 | - | 64 | 0 | yes |
| hub-16384 | `grust-next@counted+f32#unset` | f32 | counted | push | second | 21 | yes | 8.58e-09 | 27.904 | 0.040 | 0.001 | 1.3288 | 13.03 | - | 32 | 0 | yes |
| hub-16384 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | first | 21 | yes | 8.58e-09 | 16.416 | 0.008 | 0.000 | 0.7817 | 9.16 | - | 64 | 0 | yes |
| hub-16384 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | second | 21 | yes | 8.58e-09 | 16.320 | 0.016 | 0.001 | 0.7772 | 9.16 | - | 32 | 0 | yes |
| hub-65536 | `neo4j-graph` | f32 |  |  |  | 28 |  | 9.33e-09 | 36.606 | 0.277 | 0.008 | 1.3074 | 41.61 | - | 70 | 0 | yes |
| hub-65536 | `grust#1` | f64 | counted | pull | first | 17 | yes | 3.24e-09 | 62.395 | 2.973 | 0.048 | 3.6703 | 105.03 | - | 1024 | 0 | yes |
| hub-65536 | `grust#1` | f64 | counted | pull | second | 17 | yes | 3.24e-09 | 50.673 | 1.322 | 0.026 | 2.9808 | 105.03 | - | 0 | 0 | yes |
| hub-65536 | `grust-next@counted#1` | f64 | counted | pull | first | 17 | yes | 3.24e-09 | 34.386 | 0.576 | 0.017 | 2.0227 | 50.45 | 7.28 | 384 | 0 | yes |
| hub-65536 | `grust-next@counted#1` | f64 | counted | pull | second | 17 | yes | 3.24e-09 | 33.414 | 0.437 | 0.013 | 1.9655 | 50.45 | 7.28 | 0 | 0 | yes |
| hub-65536 | `grust-next@unchecked#1` | f64 | unchecked | pull | first | 17 | yes | 3.24e-09 | 32.369 | 0.072 | 0.002 | 1.9041 | 42.07 | 5.95 | 384 | 0 | yes |
| hub-65536 | `grust-next@unchecked#1` | f64 | unchecked | pull | second | 17 | yes | 3.24e-09 | 31.583 | 0.144 | 0.005 | 1.8578 | 42.07 | 5.95 | 0 | 0 | yes |
| hub-65536 | `grust-next@counted+f32#1` | f32 | counted | pull | first | 20 | yes | 8.44e-09 | 38.416 | 0.005 | 0.000 | 1.9208 | 51.35 | 6.88 | 192 | 0 | yes |
| hub-65536 | `grust-next@counted+f32#1` | f32 | counted | pull | second | 20 | yes | 8.44e-09 | 37.903 | 0.020 | 0.001 | 1.8952 | 51.35 | 6.88 | 0 | 0 | yes |
| hub-65536 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | first | 20 | yes | 8.44e-09 | 37.204 | 0.115 | 0.003 | 1.8602 | 44.02 | 6.13 | 192 | 0 | yes |
| hub-65536 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | second | 20 | yes | 8.44e-09 | 36.674 | 0.065 | 0.002 | 1.8337 | 44.02 | 6.13 | 0 | 0 | yes |
| hub-65536 | `grust-next@counted#unset` | f64 | counted | push | first | 17 | yes | 3.24e-09 | 96.804 | 0.963 | 0.010 | 5.6943 | 53.60 | - | 512 | 0 | yes |
| hub-65536 | `grust-next@counted#unset` | f64 | counted | push | second | 17 | yes | 3.24e-09 | 95.080 | 0.346 | 0.004 | 5.5929 | 53.60 | - | 128 | 0 | yes |
| hub-65536 | `grust-next@unchecked#unset` | f64 | unchecked | push | first | 17 | yes | 3.24e-09 | 59.116 | 1.837 | 0.031 | 3.4774 | 38.94 | - | 512 | 0 | yes |
| hub-65536 | `grust-next@unchecked#unset` | f64 | unchecked | push | second | 17 | yes | 3.24e-09 | 57.928 | 0.744 | 0.013 | 3.4075 | 38.94 | - | 128 | 0 | yes |
| hub-65536 | `grust-next@counted+f32#unset` | f32 | counted | push | first | 21 | yes | 8.04e-09 | 112.531 | 0.534 | 0.005 | 5.3586 | 53.87 | - | 256 | 0 | yes |
| hub-65536 | `grust-next@counted+f32#unset` | f32 | counted | push | second | 21 | yes | 8.04e-09 | 112.062 | 0.582 | 0.005 | 5.3363 | 53.87 | - | 128 | 0 | yes |
| hub-65536 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | first | 21 | yes | 8.04e-09 | 65.790 | 0.158 | 0.002 | 3.1328 | 38.34 | - | 256 | 0 | yes |
| hub-65536 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | second | 21 | yes | 8.04e-09 | 65.418 | 0.015 | 0.000 | 3.1151 | 38.34 | - | 128 | 0 | yes |
| uniform-16384 | `neo4j-graph` | f32 |  |  |  | 28 |  | 9.64e-09 | 10.511 | 0.028 | 0.003 | 0.3754 | 7.83 | - | 25 | 0 | yes |
| uniform-16384 | `grust#1` | f64 | counted | pull | first | 16 | yes | 3.36e-09 | 11.257 | 0.037 | 0.003 | 0.7035 | 18.74 | - | 385 | 0 | yes |
| uniform-16384 | `grust#1` | f64 | counted | pull | second | 16 | yes | 3.36e-09 | 9.243 | 0.008 | 0.001 | 0.5777 | 18.74 | - | 0 | 0 | yes |
| uniform-16384 | `grust-next@counted#1` | f64 | counted | pull | first | 16 | yes | 3.36e-09 | 7.694 | 0.005 | 0.001 | 0.4809 | 12.00 | 1.48 | 96 | 0 | yes |
| uniform-16384 | `grust-next@counted#1` | f64 | counted | pull | second | 16 | yes | 3.36e-09 | 7.485 | 0.007 | 0.001 | 0.4678 | 12.00 | 1.48 | 0 | 0 | yes |
| uniform-16384 | `grust-next@unchecked#1` | f64 | unchecked | pull | first | 16 | yes | 3.36e-09 | 7.339 | 0.008 | 0.001 | 0.4587 | 9.92 | 1.31 | 96 | 0 | yes |
| uniform-16384 | `grust-next@unchecked#1` | f64 | unchecked | pull | second | 16 | yes | 3.36e-09 | 7.121 | 0.015 | 0.002 | 0.4451 | 9.92 | 1.31 | 0 | 0 | yes |
| uniform-16384 | `grust-next@counted+f32#1` | f32 | counted | pull | first | 19 | yes | 8.76e-09 | 8.926 | 0.017 | 0.002 | 0.4698 | 11.51 | 1.48 | 48 | 0 | yes |
| uniform-16384 | `grust-next@counted+f32#1` | f32 | counted | pull | second | 19 | yes | 8.76e-09 | 8.808 | 0.003 | 0.000 | 0.4636 | 11.51 | 1.48 | 0 | 0 | yes |
| uniform-16384 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | first | 19 | yes | 8.76e-09 | 8.699 | 0.002 | 0.000 | 0.4578 | 9.89 | 1.31 | 48 | 0 | yes |
| uniform-16384 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | second | 19 | yes | 8.76e-09 | 8.577 | 0.009 | 0.001 | 0.4514 | 9.89 | 1.31 | 0 | 0 | yes |
| uniform-16384 | `grust-next@counted#unset` | f64 | counted | push | first | 16 | yes | 3.36e-09 | 21.778 | 0.071 | 0.003 | 1.3611 | 13.27 | - | 128 | 0 | yes |
| uniform-16384 | `grust-next@counted#unset` | f64 | counted | push | second | 16 | yes | 3.36e-09 | 21.543 | 0.024 | 0.001 | 1.3464 | 13.27 | - | 32 | 0 | yes |
| uniform-16384 | `grust-next@unchecked#unset` | f64 | unchecked | push | first | 16 | yes | 3.36e-09 | 12.880 | 0.002 | 0.000 | 0.8050 | 8.71 | - | 128 | 0 | yes |
| uniform-16384 | `grust-next@unchecked#unset` | f64 | unchecked | push | second | 16 | yes | 3.36e-09 | 12.683 | 0.015 | 0.001 | 0.7927 | 8.71 | - | 32 | 0 | yes |
| uniform-16384 | `grust-next@counted+f32#unset` | f32 | counted | push | first | 19 | yes | 9.5e-09 | 25.635 | 0.315 | 0.012 | 1.3492 | 13.48 | - | 64 | 0 | yes |
| uniform-16384 | `grust-next@counted+f32#unset` | f32 | counted | push | second | 19 | yes | 9.5e-09 | 25.103 | 0.026 | 0.001 | 1.3212 | 13.48 | - | 32 | 0 | yes |
| uniform-16384 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | first | 19 | yes | 9.5e-09 | 14.752 | 0.008 | 0.001 | 0.7764 | 9.07 | - | 64 | 0 | yes |
| uniform-16384 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | second | 19 | yes | 9.5e-09 | 14.703 | 0.008 | 0.001 | 0.7739 | 9.07 | - | 32 | 0 | yes |
| uniform-65536 | `neo4j-graph` | f32 |  |  |  | 34 |  | 9.7e-09 | 45.111 | 0.164 | 0.004 | 1.3268 | 43.57 | - | 72 | 0 | yes |
| uniform-65536 | `grust#1` | f64 | counted | pull | first | 16 | yes | 3.43e-09 | 59.214 | 1.135 | 0.019 | 3.7009 | 100.75 | - | 1025 | 0 | yes |
| uniform-65536 | `grust#1` | f64 | counted | pull | second | 16 | yes | 3.43e-09 | 46.248 | 0.336 | 0.007 | 2.8905 | 100.75 | - | 0 | 0 | yes |
| uniform-65536 | `grust-next@counted#1` | f64 | counted | pull | first | 16 | yes | 3.43e-09 | 33.026 | 0.262 | 0.008 | 2.0641 | 49.69 | 6.76 | 384 | 0 | yes |
| uniform-65536 | `grust-next@counted#1` | f64 | counted | pull | second | 16 | yes | 3.43e-09 | 31.978 | 0.340 | 0.011 | 1.9986 | 49.69 | 6.76 | 0 | 0 | yes |
| uniform-65536 | `grust-next@unchecked#1` | f64 | unchecked | pull | first | 16 | yes | 3.43e-09 | 30.424 | 0.143 | 0.005 | 1.9015 | 40.65 | 5.98 | 384 | 0 | yes |
| uniform-65536 | `grust-next@unchecked#1` | f64 | unchecked | pull | second | 16 | yes | 3.43e-09 | 29.631 | 0.155 | 0.005 | 1.8520 | 40.65 | 5.98 | 0 | 0 | yes |
| uniform-65536 | `grust-next@counted+f32#1` | f32 | counted | pull | first | 19 | yes | 8.53e-09 | 36.743 | 0.067 | 0.002 | 1.9339 | 51.07 | 6.88 | 192 | 0 | yes |
| uniform-65536 | `grust-next@counted+f32#1` | f32 | counted | pull | second | 19 | yes | 8.53e-09 | 36.131 | 0.079 | 0.002 | 1.9016 | 51.07 | 6.88 | 0 | 0 | yes |
| uniform-65536 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | first | 19 | yes | 8.53e-09 | 35.260 | 0.065 | 0.002 | 1.8558 | 42.15 | 6.04 | 192 | 0 | yes |
| uniform-65536 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | second | 19 | yes | 8.53e-09 | 34.879 | 0.085 | 0.002 | 1.8358 | 42.15 | 6.04 | 0 | 0 | yes |
| uniform-65536 | `grust-next@counted#unset` | f64 | counted | push | first | 16 | yes | 3.43e-09 | 90.444 | 0.689 | 0.008 | 5.6528 | 53.63 | - | 512 | 0 | yes |
| uniform-65536 | `grust-next@counted#unset` | f64 | counted | push | second | 16 | yes | 3.43e-09 | 89.702 | 0.529 | 0.006 | 5.6064 | 53.63 | - | 128 | 0 | yes |
| uniform-65536 | `grust-next@unchecked#unset` | f64 | unchecked | push | first | 16 | yes | 3.43e-09 | 54.043 | 0.509 | 0.009 | 3.3777 | 36.38 | - | 512 | 0 | yes |
| uniform-65536 | `grust-next@unchecked#unset` | f64 | unchecked | push | second | 16 | yes | 3.43e-09 | 55.451 | 2.122 | 0.038 | 3.4657 | 36.38 | - | 128 | 0 | yes |
| uniform-65536 | `grust-next@counted+f32#unset` | f32 | counted | push | first | 20 | yes | 8.39e-09 | 106.531 | 0.128 | 0.001 | 5.3266 | 52.25 | - | 256 | 0 | yes |
| uniform-65536 | `grust-next@counted+f32#unset` | f32 | counted | push | second | 20 | yes | 8.39e-09 | 106.233 | 0.246 | 0.002 | 5.3117 | 52.25 | - | 128 | 0 | yes |
| uniform-65536 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | first | 20 | yes | 8.39e-09 | 62.573 | 0.276 | 0.004 | 3.1286 | 37.15 | - | 256 | 0 | yes |
| uniform-65536 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | second | 20 | yes | 8.39e-09 | 62.132 | 0.223 | 0.004 | 3.1066 | 37.15 | - | 128 | 0 | yes |

## `b7-full-width.json`: b7-full-width

workers 16, concurrency 16, allocator glibc default, not pinned, 1 warmup + 5 repeats, steal over the run 0 ticks, 10.6 s, unusable at MAD/median >= 0.25

| fixture | participant | precision | accounting | kernel | call | iters | converged | residual | total ms | MAD | MAD/median | per iter ms | build ms | incoming ms | minflt | steal | usable |
| --- | --- | --- | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| hub-16384 | `neo4j-graph` | f32 |  |  |  | 36 |  | 9.29e-09 | 13.533 | 0.088 | 0.006 | 0.3759 | 4.51 | - | 39 | 0 | yes |
| hub-16384 | `grust` | f64 | counted | pull | first | 17 | yes | 3.23e-09 | 6.419 | 0.139 | 0.022 | 0.3776 | 19.69 | - | 484 | 0 | yes |
| hub-16384 | `grust` | f64 | counted | pull | second | 17 | yes | 3.23e-09 | 3.513 | 0.052 | 0.015 | 0.2066 | 19.69 | - | 0 | 0 | yes |
| hub-16384 | `grust-next@counted` | f64 | counted | pull | first | 17 | yes | 3.23e-09 | 3.765 | 0.176 | 0.047 | 0.2215 | 12.45 | 1.62 | 4 | 0 | yes |
| hub-16384 | `grust-next@counted` | f64 | counted | pull | second | 17 | yes | 3.23e-09 | 3.408 | 0.134 | 0.039 | 0.2005 | 12.45 | 1.62 | 1 | 0 | yes |
| hub-16384 | `grust-next@unchecked` | f64 | unchecked | pull | first | 17 | yes | 3.23e-09 | 2.854 | 0.043 | 0.015 | 0.1679 | 10.41 | 1.42 | 4 | 0 | yes |
| hub-16384 | `grust-next@unchecked` | f64 | unchecked | pull | second | 17 | yes | 3.23e-09 | 2.815 | 0.041 | 0.015 | 0.1656 | 10.41 | 1.42 | 0 | 0 | yes |
| hub-16384 | `grust-next@counted+f32` | f32 | counted | pull | first | 20 | yes | 8.8e-09 | 4.147 | 0.076 | 0.018 | 0.2073 | 12.92 | 1.61 | 5 | 0 | yes |
| hub-16384 | `grust-next@counted+f32` | f32 | counted | pull | second | 20 | yes | 8.8e-09 | 3.909 | 0.066 | 0.017 | 0.1955 | 12.92 | 1.61 | 0 | 0 | yes |
| hub-16384 | `grust-next@unchecked+f32` | f32 | unchecked | pull | first | 20 | yes | 8.8e-09 | 3.363 | 0.026 | 0.008 | 0.1682 | 10.74 | 1.43 | 3 | 0 | yes |
| hub-16384 | `grust-next@unchecked+f32` | f32 | unchecked | pull | second | 20 | yes | 8.8e-09 | 3.288 | 0.042 | 0.013 | 0.1644 | 10.74 | 1.43 | 1 | 0 | yes |
| hub-65536 | `neo4j-graph` | f32 |  |  |  | 33 |  | 7.91e-09 | 15.216 | 0.166 | 0.011 | 0.4611 | 14.68 | - | 95 | 0 | yes |
| hub-65536 | `grust` | f64 | counted | pull | first | 17 | yes | 3.24e-09 | 18.409 | 0.710 | 0.039 | 1.0829 | 103.28 | - | 1133 | 0 | yes |
| hub-65536 | `grust` | f64 | counted | pull | second | 17 | yes | 3.24e-09 | 8.617 | 0.081 | 0.009 | 0.5069 | 103.28 | - | 5 | 0 | yes |
| hub-65536 | `grust-next@counted` | f64 | counted | pull | first | 17 | yes | 3.24e-09 | 7.241 | 0.129 | 0.018 | 0.4259 | 44.25 | 5.38 | 19 | 0 | yes |
| hub-65536 | `grust-next@counted` | f64 | counted | pull | second | 17 | yes | 3.24e-09 | 7.232 | 0.267 | 0.037 | 0.4254 | 44.25 | 5.38 | 3 | 0 | yes |
| hub-65536 | `grust-next@unchecked` | f64 | unchecked | pull | first | 17 | yes | 3.24e-09 | 4.844 | 0.135 | 0.028 | 0.2849 | 36.45 | 4.47 | 13 | 0 | yes |
| hub-65536 | `grust-next@unchecked` | f64 | unchecked | pull | second | 17 | yes | 3.24e-09 | 4.646 | 0.087 | 0.019 | 0.2733 | 36.45 | 4.47 | 5 | 0 | yes |
| hub-65536 | `grust-next@counted+f32` | f32 | counted | pull | first | 20 | yes | 8.44e-09 | 7.806 | 0.099 | 0.013 | 0.3903 | 45.03 | 5.19 | 16 | 0 | yes |
| hub-65536 | `grust-next@counted+f32` | f32 | counted | pull | second | 20 | yes | 8.44e-09 | 7.709 | 0.061 | 0.008 | 0.3854 | 45.03 | 5.19 | 4 | 0 | yes |
| hub-65536 | `grust-next@unchecked+f32` | f32 | unchecked | pull | first | 20 | yes | 8.44e-09 | 5.226 | 0.090 | 0.017 | 0.2613 | 37.23 | 4.44 | 12 | 0 | yes |
| hub-65536 | `grust-next@unchecked+f32` | f32 | unchecked | pull | second | 20 | yes | 8.44e-09 | 5.016 | 0.078 | 0.016 | 0.2508 | 37.23 | 4.44 | 3 | 0 | yes |
| uniform-16384 | `neo4j-graph` | f32 |  |  |  | 28 |  | 9.64e-09 | 10.771 | 0.062 | 0.006 | 0.3847 | 4.30 | - | 38 | 0 | yes |
| uniform-16384 | `grust` | f64 | counted | pull | first | 16 | yes | 3.36e-09 | 6.218 | 0.123 | 0.020 | 0.3886 | 20.98 | - | 484 | 0 | yes |
| uniform-16384 | `grust` | f64 | counted | pull | second | 16 | yes | 3.36e-09 | 3.349 | 0.061 | 0.018 | 0.2093 | 20.98 | - | 1 | 0 | yes |
| uniform-16384 | `grust-next@counted` | f64 | counted | pull | first | 16 | yes | 3.36e-09 | 3.326 | 0.042 | 0.013 | 0.2079 | 12.49 | 1.66 | 5 | 0 | yes |
| uniform-16384 | `grust-next@counted` | f64 | counted | pull | second | 16 | yes | 3.36e-09 | 3.262 | 0.157 | 0.048 | 0.2039 | 12.49 | 1.66 | 0 | 0 | yes |
| uniform-16384 | `grust-next@unchecked` | f64 | unchecked | pull | first | 16 | yes | 3.36e-09 | 2.667 | 0.044 | 0.017 | 0.1667 | 10.71 | 1.50 | 5 | 0 | yes |
| uniform-16384 | `grust-next@unchecked` | f64 | unchecked | pull | second | 16 | yes | 3.36e-09 | 2.655 | 0.074 | 0.028 | 0.1659 | 10.71 | 1.50 | 1 | 0 | yes |
| uniform-16384 | `grust-next@counted+f32` | f32 | counted | pull | first | 19 | yes | 8.76e-09 | 4.024 | 0.104 | 0.026 | 0.2118 | 12.83 | 1.63 | 6 | 0 | yes |
| uniform-16384 | `grust-next@counted+f32` | f32 | counted | pull | second | 19 | yes | 8.76e-09 | 3.840 | 0.139 | 0.036 | 0.2021 | 12.83 | 1.63 | 0 | 0 | yes |
| uniform-16384 | `grust-next@unchecked+f32` | f32 | unchecked | pull | first | 19 | yes | 8.76e-09 | 3.275 | 0.069 | 0.021 | 0.1724 | 10.34 | 1.48 | 6 | 0 | yes |
| uniform-16384 | `grust-next@unchecked+f32` | f32 | unchecked | pull | second | 19 | yes | 8.76e-09 | 3.102 | 0.006 | 0.002 | 0.1633 | 10.34 | 1.48 | 1 | 0 | yes |
| uniform-65536 | `neo4j-graph` | f32 |  |  |  | 34 |  | 9.04e-09 | 16.220 | 0.089 | 0.005 | 0.4771 | 14.66 | - | 95 | 0 | yes |
| uniform-65536 | `grust` | f64 | counted | pull | first | 16 | yes | 3.43e-09 | 18.401 | 0.955 | 0.052 | 1.1501 | 105.57 | - | 1135 | 0 | yes |
| uniform-65536 | `grust` | f64 | counted | pull | second | 16 | yes | 3.43e-09 | 8.359 | 0.254 | 0.030 | 0.5224 | 105.57 | - | 2 | 0 | yes |
| uniform-65536 | `grust-next@counted` | f64 | counted | pull | first | 16 | yes | 3.43e-09 | 6.937 | 0.077 | 0.011 | 0.4335 | 43.93 | 5.29 | 13 | 0 | yes |
| uniform-65536 | `grust-next@counted` | f64 | counted | pull | second | 16 | yes | 3.43e-09 | 6.692 | 0.105 | 0.016 | 0.4183 | 43.93 | 5.29 | 4 | 0 | yes |
| uniform-65536 | `grust-next@unchecked` | f64 | unchecked | pull | first | 16 | yes | 3.43e-09 | 4.496 | 0.112 | 0.025 | 0.2810 | 36.90 | 4.52 | 11 | 0 | yes |
| uniform-65536 | `grust-next@unchecked` | f64 | unchecked | pull | second | 16 | yes | 3.43e-09 | 4.353 | 0.113 | 0.026 | 0.2720 | 36.90 | 4.52 | 3 | 0 | yes |
| uniform-65536 | `grust-next@counted+f32` | f32 | counted | pull | first | 19 | yes | 8.53e-09 | 7.431 | 0.028 | 0.004 | 0.3911 | 45.16 | 5.29 | 17 | 0 | yes |
| uniform-65536 | `grust-next@counted+f32` | f32 | counted | pull | second | 19 | yes | 8.53e-09 | 7.359 | 0.010 | 0.001 | 0.3873 | 45.16 | 5.29 | 4 | 0 | yes |
| uniform-65536 | `grust-next@unchecked+f32` | f32 | unchecked | pull | first | 19 | yes | 8.53e-09 | 5.046 | 0.043 | 0.009 | 0.2656 | 36.45 | 4.49 | 12 | 0 | yes |
| uniform-65536 | `grust-next@unchecked+f32` | f32 | unchecked | pull | second | 19 | yes | 8.53e-09 | 4.741 | 0.013 | 0.003 | 0.2495 | 36.45 | 4.49 | 3 | 0 | yes |

## `b7-large-one-thread.json`: b7-large-one-thread

workers 1, concurrency 1, allocator glibc default, not pinned, 1 warmup + 5 repeats, steal over the run 6 ticks, 1511.9 s, unusable at MAD/median >= 0.25

| fixture | participant | precision | accounting | kernel | call | iters | converged | residual | total ms | MAD | MAD/median | per iter ms | build ms | incoming ms | minflt | steal | usable |
| --- | --- | --- | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| hub-2097152 | `neo4j-graph` | f32 |  |  |  | 26 |  | 9.49e-09 | 2559.784 | 166.853 | 0.065 | 98.4532 | 3664.32 | - | 1038 | 3 | yes |
| hub-2097152 | `grust#1` | f64 | counted | pull | first | 16 | yes | 9.96e-09 | 6249.805 | 63.563 | 0.010 | 390.6128 | 4046.08 | - | 3142 | 3 | yes |
| hub-2097152 | `grust#1` | f64 | counted | pull | second | 16 | yes | 9.96e-09 | 5502.701 | 59.609 | 0.011 | 343.9188 | 4046.08 | - | 0 | 3 | yes |
| hub-2097152 | `grust-next@counted#1` | f64 | counted | pull | first | 16 | yes | 9.96e-09 | 3564.170 | 306.386 | 0.086 | 222.7607 | 2267.64 | 667.29 | 1559 | 3 | yes |
| hub-2097152 | `grust-next@counted#1` | f64 | counted | pull | second | 16 | yes | 9.96e-09 | 3674.285 | 195.601 | 0.053 | 229.6428 | 2267.64 | 667.29 | 517 | 3 | yes |
| hub-2097152 | `grust-next@unchecked#1` | f64 | unchecked | pull | first | 16 | yes | 9.96e-09 | 3235.203 | 65.378 | 0.020 | 202.2002 | 1959.68 | 609.72 | 1559 | 3 | yes |
| hub-2097152 | `grust-next@unchecked#1` | f64 | unchecked | pull | second | 16 | yes | 9.96e-09 | 3240.033 | 49.121 | 0.015 | 202.5021 | 1959.68 | 609.72 | 517 | 3 | yes |
| hub-2097152 | `grust-next@counted+f32#1` | f32 | counted | pull | first | 20 | yes | 8.19e-09 | 2729.812 | 88.705 | 0.032 | 136.4906 | 2232.66 | 660.77 | 1545 | 3 | yes |
| hub-2097152 | `grust-next@counted+f32#1` | f32 | counted | pull | second | 20 | yes | 8.19e-09 | 2846.565 | 152.305 | 0.054 | 142.3282 | 2232.66 | 660.77 | 0 | 3 | yes |
| hub-2097152 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | first | 20 | yes | 8.19e-09 | 2405.627 | 58.188 | 0.024 | 120.2813 | 1973.05 | 601.69 | 1545 | 3 | yes |
| hub-2097152 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | second | 20 | yes | 8.19e-09 | 2391.995 | 109.605 | 0.046 | 119.5998 | 1973.05 | 601.69 | 0 | 3 | yes |
| hub-2097152 | `grust-next@counted#unset` | f64 | counted | push | first | 16 | yes | 9.96e-09 | 6905.151 | 71.851 | 0.010 | 431.5719 | 1913.63 | - | 2595 | 3 | yes |
| hub-2097152 | `grust-next@counted#unset` | f64 | counted | push | second | 16 | yes | 9.96e-09 | 6930.574 | 40.088 | 0.006 | 433.1609 | 1913.63 | - | 519 | 3 | yes |
| hub-2097152 | `grust-next@unchecked#unset` | f64 | unchecked | push | first | 16 | yes | 9.96e-09 | 5669.136 | 82.202 | 0.014 | 354.3210 | 1406.09 | - | 2595 | 3 | yes |
| hub-2097152 | `grust-next@unchecked#unset` | f64 | unchecked | push | second | 16 | yes | 9.96e-09 | 5715.692 | 63.268 | 0.011 | 357.2307 | 1406.09 | - | 519 | 3 | yes |
| hub-2097152 | `grust-next@counted+f32#unset` | f32 | counted | push | first | 21 | yes | 8.2e-09 | 5937.559 | 101.152 | 0.017 | 282.7409 | 1910.66 | - | 2579 | 3 | yes |
| hub-2097152 | `grust-next@counted+f32#unset` | f32 | counted | push | second | 21 | yes | 8.2e-09 | 5857.052 | 92.954 | 0.016 | 278.9072 | 1910.66 | - | 1030 | 3 | yes |
| hub-2097152 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | first | 21 | yes | 8.2e-09 | 4182.279 | 81.181 | 0.019 | 199.1561 | 1404.95 | - | 2579 | 3 | yes |
| hub-2097152 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | second | 21 | yes | 8.2e-09 | 4135.766 | 38.310 | 0.009 | 196.9412 | 1404.95 | - | 1030 | 3 | yes |
| uniform-2097152 | `neo4j-graph` | f32 |  |  |  | 26 |  | 8.04e-09 | 2378.459 | 11.424 | 0.005 | 91.4792 | 3550.30 | - | 1038 | 3 | yes |
| uniform-2097152 | `grust#1` | f64 | counted | pull | first | 16 | yes | 3.46e-09 | 6446.494 | 53.920 | 0.008 | 402.9059 | 4058.71 | - | 2659 | 3 | yes |
| uniform-2097152 | `grust#1` | f64 | counted | pull | second | 16 | yes | 3.46e-09 | 5826.544 | 39.648 | 0.007 | 364.1590 | 4058.71 | - | 0 | 3 | yes |
| uniform-2097152 | `grust-next@counted#1` | f64 | counted | pull | first | 16 | yes | 3.46e-09 | 3424.043 | 46.213 | 0.013 | 214.0027 | 2180.18 | 614.27 | 1559 | 3 | yes |
| uniform-2097152 | `grust-next@counted#1` | f64 | counted | pull | second | 16 | yes | 3.46e-09 | 3421.734 | 43.305 | 0.013 | 213.8584 | 2180.18 | 614.27 | 517 | 3 | yes |
| uniform-2097152 | `grust-next@unchecked#1` | f64 | unchecked | pull | first | 16 | yes | 3.46e-09 | 3199.159 | 12.769 | 0.004 | 199.9475 | 1962.17 | 582.54 | 1559 | 3 | yes |
| uniform-2097152 | `grust-next@unchecked#1` | f64 | unchecked | pull | second | 16 | yes | 3.46e-09 | 3185.564 | 203.039 | 0.064 | 199.0977 | 1962.17 | 582.54 | 517 | 3 | yes |
| uniform-2097152 | `grust-next@counted+f32#1` | f32 | counted | pull | first | 19 | yes | 8.59e-09 | 2465.666 | 84.487 | 0.034 | 129.7719 | 2225.81 | 623.99 | 1545 | 3 | yes |
| uniform-2097152 | `grust-next@counted+f32#1` | f32 | counted | pull | second | 19 | yes | 8.59e-09 | 2414.525 | 16.056 | 0.007 | 127.0803 | 2225.81 | 623.99 | 0 | 3 | yes |
| uniform-2097152 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | first | 19 | yes | 8.59e-09 | 2154.581 | 35.972 | 0.017 | 113.3990 | 1952.87 | 601.43 | 1545 | 3 | yes |
| uniform-2097152 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | second | 19 | yes | 8.59e-09 | 2175.484 | 43.252 | 0.020 | 114.4991 | 1952.87 | 601.43 | 0 | 3 | yes |
| uniform-2097152 | `grust-next@counted#unset` | f64 | counted | push | first | 16 | yes | 3.46e-09 | 6540.173 | 150.849 | 0.023 | 408.7608 | 1906.76 | - | 2595 | 3 | yes |
| uniform-2097152 | `grust-next@counted#unset` | f64 | counted | push | second | 16 | yes | 3.46e-09 | 6517.604 | 90.641 | 0.014 | 407.3502 | 1906.76 | - | 519 | 3 | yes |
| uniform-2097152 | `grust-next@unchecked#unset` | f64 | unchecked | push | first | 16 | yes | 3.46e-09 | 5530.183 | 40.294 | 0.007 | 345.6365 | 1407.92 | - | 2595 | 3 | yes |
| uniform-2097152 | `grust-next@unchecked#unset` | f64 | unchecked | push | second | 16 | yes | 3.46e-09 | 5485.693 | 60.692 | 0.011 | 342.8558 | 1407.92 | - | 519 | 3 | yes |
| uniform-2097152 | `grust-next@counted+f32#unset` | f32 | counted | push | first | 20 | yes | 8.43e-09 | 5645.555 | 183.150 | 0.032 | 282.2778 | 1913.77 | - | 2579 | 3 | yes |
| uniform-2097152 | `grust-next@counted+f32#unset` | f32 | counted | push | second | 20 | yes | 8.43e-09 | 5466.825 | 179.986 | 0.033 | 273.3412 | 1913.77 | - | 1030 | 3 | yes |
| uniform-2097152 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | first | 20 | yes | 8.43e-09 | 3733.104 | 93.395 | 0.025 | 186.6552 | 1407.33 | - | 2579 | 3 | yes |
| uniform-2097152 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | second | 20 | yes | 8.43e-09 | 3703.307 | 84.242 | 0.023 | 185.1654 | 1407.33 | - | 1030 | 3 | yes |

## `b7-large-full-width.json`: b7-large-full-width

workers 16, concurrency 16, allocator glibc default, not pinned, 1 warmup + 5 repeats, steal over the run 2 ticks, 326.9 s, unusable at MAD/median >= 0.25

| fixture | participant | precision | accounting | kernel | call | iters | converged | residual | total ms | MAD | MAD/median | per iter ms | build ms | incoming ms | minflt | steal | usable |
| --- | --- | --- | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| hub-2097152 | `neo4j-graph` | f32 |  |  |  | 28 |  | 8.7e-09 | 270.984 | 3.423 | 0.013 | 9.6780 | 409.04 | - | 1109 | 1 | yes |
| hub-2097152 | `grust` | f64 | counted | pull | first | 16 | yes | 9.96e-09 | 1148.604 | 52.112 | 0.045 | 71.7877 | 3807.14 | - | 3309 | 1 | yes |
| hub-2097152 | `grust` | f64 | counted | pull | second | 16 | yes | 9.96e-09 | 496.693 | 3.206 | 0.006 | 31.0433 | 3807.14 | - | 12 | 1 | yes |
| hub-2097152 | `grust-next@counted` | f64 | counted | pull | first | 16 | yes | 9.96e-09 | 246.341 | 8.394 | 0.034 | 15.3963 | 1529.88 | 231.09 | 1621 | 1 | yes |
| hub-2097152 | `grust-next@counted` | f64 | counted | pull | second | 16 | yes | 9.96e-09 | 246.473 | 4.913 | 0.020 | 15.4045 | 1529.88 | 231.09 | 2053 | 1 | yes |
| hub-2097152 | `grust-next@unchecked` | f64 | unchecked | pull | first | 16 | yes | 9.96e-09 | 225.635 | 7.316 | 0.032 | 14.1022 | 1279.38 | 208.66 | 1621 | 1 | yes |
| hub-2097152 | `grust-next@unchecked` | f64 | unchecked | pull | second | 16 | yes | 9.96e-09 | 211.994 | 0.535 | 0.003 | 13.2496 | 1279.38 | 208.66 | 2052 | 1 | yes |
| hub-2097152 | `grust-next@counted+f32` | f32 | counted | pull | first | 20 | yes | 8.19e-09 | 250.223 | 1.599 | 0.006 | 12.5112 | 1514.26 | 229.15 | 1101 | 1 | yes |
| hub-2097152 | `grust-next@counted+f32` | f32 | counted | pull | second | 20 | yes | 8.19e-09 | 252.414 | 2.243 | 0.009 | 12.6207 | 1514.26 | 229.15 | 2042 | 1 | yes |
| hub-2097152 | `grust-next@unchecked+f32` | f32 | unchecked | pull | first | 20 | yes | 8.19e-09 | 229.773 | 0.906 | 0.004 | 11.4886 | 1257.52 | 207.39 | 1101 | 1 | yes |
| hub-2097152 | `grust-next@unchecked+f32` | f32 | unchecked | pull | second | 20 | yes | 8.19e-09 | 232.809 | 1.437 | 0.006 | 11.6404 | 1257.52 | 207.39 | 2042 | 1 | yes |
| uniform-2097152 | `neo4j-graph` | f32 |  |  |  | 27 |  | 9.88e-09 | 274.848 | 4.509 | 0.016 | 10.1796 | 446.02 | - | 1119 | 1 | yes |
| uniform-2097152 | `grust` | f64 | counted | pull | first | 16 | yes | 3.46e-09 | 1304.485 | 39.510 | 0.030 | 81.5303 | 4051.80 | - | 2824 | 1 | yes |
| uniform-2097152 | `grust` | f64 | counted | pull | second | 16 | yes | 3.46e-09 | 600.746 | 8.957 | 0.015 | 37.5466 | 4051.80 | - | 14 | 1 | yes |
| uniform-2097152 | `grust-next@counted` | f64 | counted | pull | first | 16 | yes | 3.46e-09 | 281.882 | 16.810 | 0.060 | 17.6176 | 1677.08 | 249.60 | 1623 | 1 | yes |
| uniform-2097152 | `grust-next@counted` | f64 | counted | pull | second | 16 | yes | 3.46e-09 | 270.471 | 21.406 | 0.079 | 16.9044 | 1677.08 | 249.60 | 2054 | 1 | yes |
| uniform-2097152 | `grust-next@unchecked` | f64 | unchecked | pull | first | 16 | yes | 3.46e-09 | 254.091 | 27.340 | 0.108 | 15.8807 | 1403.92 | 229.04 | 1623 | 1 | yes |
| uniform-2097152 | `grust-next@unchecked` | f64 | unchecked | pull | second | 16 | yes | 3.46e-09 | 260.613 | 11.689 | 0.045 | 16.2883 | 1403.92 | 229.04 | 2055 | 1 | yes |
| uniform-2097152 | `grust-next@counted+f32` | f32 | counted | pull | first | 19 | yes | 8.59e-09 | 252.866 | 6.425 | 0.025 | 13.3088 | 1670.44 | 250.39 | 1102 | 1 | yes |
| uniform-2097152 | `grust-next@counted+f32` | f32 | counted | pull | second | 19 | yes | 8.59e-09 | 256.148 | 0.621 | 0.002 | 13.4814 | 1670.44 | 250.39 | 2040 | 1 | yes |
| uniform-2097152 | `grust-next@unchecked+f32` | f32 | unchecked | pull | first | 19 | yes | 8.59e-09 | 231.575 | 1.474 | 0.006 | 12.1881 | 1420.60 | 227.31 | 1102 | 1 | yes |
| uniform-2097152 | `grust-next@unchecked+f32` | f32 | unchecked | pull | second | 19 | yes | 8.59e-09 | 240.314 | 2.400 | 0.010 | 12.6481 | 1420.60 | 227.31 | 2040 | 1 | yes |

## `b7-xlarge-one-thread.json`: b7-xlarge-one-thread

workers 1, concurrency 1, allocator glibc default, not pinned, 1 warmup + 5 repeats, steal over the run 14 ticks, 3558.0 s, unusable at MAD/median >= 0.25

| fixture | participant | precision | accounting | kernel | call | iters | converged | residual | total ms | MAD | MAD/median | per iter ms | build ms | incoming ms | minflt | steal | usable |
| --- | --- | --- | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| hub-4194304 | `neo4j-graph` | f32 |  |  |  | 23 |  | 8.29e-09 | 6292.371 | 217.864 | 0.035 | 273.5814 | 7522.17 | - | 1046 | 7 | yes |
| hub-4194304 | `grust#1` | f64 | counted | pull | first | 16 | yes | 9.96e-09 | 14218.237 | 134.022 | 0.009 | 888.6398 | 8186.11 | - | 3229 | 7 | yes |
| hub-4194304 | `grust#1` | f64 | counted | pull | second | 16 | yes | 9.96e-09 | 12614.115 | 170.815 | 0.014 | 788.3822 | 8186.11 | - | 1584 | 7 | yes |
| hub-4194304 | `grust-next@counted#1` | f64 | counted | pull | first | 16 | yes | 9.96e-09 | 8248.781 | 7.258 | 0.001 | 515.5488 | 4603.40 | 1398.98 | 2112 | 7 | yes |
| hub-4194304 | `grust-next@counted#1` | f64 | counted | pull | second | 16 | yes | 9.96e-09 | 8257.339 | 125.180 | 0.015 | 516.0837 | 4603.40 | 1398.98 | 2112 | 7 | yes |
| hub-4194304 | `grust-next@unchecked#1` | f64 | unchecked | pull | first | 16 | yes | 9.96e-09 | 7716.874 | 83.974 | 0.011 | 482.3046 | 4104.86 | 1353.29 | 2112 | 7 | yes |
| hub-4194304 | `grust-next@unchecked#1` | f64 | unchecked | pull | second | 16 | yes | 9.96e-09 | 7802.651 | 97.011 | 0.012 | 487.6657 | 4104.86 | 1353.29 | 2112 | 7 | yes |
| hub-4194304 | `grust-next@counted+f32#1` | f32 | counted | pull | first | 20 | yes | 8.21e-09 | 8398.168 | 289.103 | 0.034 | 419.9084 | 4634.82 | 1406.80 | 1560 | 7 | yes |
| hub-4194304 | `grust-next@counted+f32#1` | f32 | counted | pull | second | 20 | yes | 8.21e-09 | 8275.853 | 259.971 | 0.031 | 413.7926 | 4634.82 | 1406.80 | 516 | 7 | yes |
| hub-4194304 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | first | 20 | yes | 8.21e-09 | 7456.611 | 70.433 | 0.009 | 372.8306 | 4114.03 | 1362.66 | 1560 | 7 | yes |
| hub-4194304 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | second | 20 | yes | 8.21e-09 | 7600.195 | 89.060 | 0.012 | 380.0098 | 4114.03 | 1362.66 | 516 | 7 | yes |
| hub-4194304 | `grust-next@counted#unset` | f64 | counted | push | first | 16 | yes | 9.96e-09 | 15350.367 | 135.657 | 0.009 | 959.3979 | 3836.40 | - | 2640 | 7 | yes |
| hub-4194304 | `grust-next@counted#unset` | f64 | counted | push | second | 16 | yes | 9.96e-09 | 15247.295 | 31.809 | 0.002 | 952.9559 | 3836.40 | - | 2640 | 7 | yes |
| hub-4194304 | `grust-next@unchecked#unset` | f64 | unchecked | push | first | 16 | yes | 9.96e-09 | 12847.216 | 94.276 | 0.007 | 802.9510 | 2859.21 | - | 2640 | 7 | yes |
| hub-4194304 | `grust-next@unchecked#unset` | f64 | unchecked | push | second | 16 | yes | 9.96e-09 | 12868.343 | 85.013 | 0.007 | 804.2715 | 2859.21 | - | 2640 | 7 | yes |
| hub-4194304 | `grust-next@counted+f32#unset` | f32 | counted | push | first | 21 | yes | 8.31e-09 | 16410.340 | 112.692 | 0.007 | 781.4448 | 3849.63 | - | 2608 | 7 | yes |
| hub-4194304 | `grust-next@counted+f32#unset` | f32 | counted | push | second | 21 | yes | 8.31e-09 | 16554.149 | 617.348 | 0.037 | 788.2928 | 3849.63 | - | 2604 | 7 | yes |
| hub-4194304 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | first | 21 | yes | 8.31e-09 | 14142.522 | 109.236 | 0.008 | 673.4534 | 2839.59 | - | 2608 | 7 | yes |
| hub-4194304 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | second | 21 | yes | 8.31e-09 | 13808.212 | 317.200 | 0.023 | 657.5339 | 2839.59 | - | 2604 | 7 | yes |
| uniform-4194304 | `neo4j-graph` | f32 |  |  |  | 29 |  | 8.64e-09 | 7717.037 | 48.571 | 0.006 | 266.1047 | 7405.10 | - | 1046 | 7 | yes |
| uniform-4194304 | `grust#1` | f64 | counted | pull | first | 16 | yes | 3.47e-09 | 14991.417 | 58.610 | 0.004 | 936.9636 | 8179.97 | - | 2261 | 7 | yes |
| uniform-4194304 | `grust#1` | f64 | counted | pull | second | 16 | yes | 3.47e-09 | 13365.330 | 74.467 | 0.006 | 835.3331 | 8179.97 | - | 1073 | 7 | yes |
| uniform-4194304 | `grust-next@counted#1` | f64 | counted | pull | first | 16 | yes | 3.47e-09 | 8367.527 | 37.676 | 0.005 | 522.9704 | 4563.91 | 1355.26 | 2112 | 7 | yes |
| uniform-4194304 | `grust-next@counted#1` | f64 | counted | pull | second | 16 | yes | 3.47e-09 | 8418.237 | 63.587 | 0.008 | 526.1398 | 4563.91 | 1355.26 | 2112 | 7 | yes |
| uniform-4194304 | `grust-next@unchecked#1` | f64 | unchecked | pull | first | 16 | yes | 3.47e-09 | 7969.135 | 120.775 | 0.015 | 498.0709 | 4098.05 | 1341.06 | 2112 | 7 | yes |
| uniform-4194304 | `grust-next@unchecked#1` | f64 | unchecked | pull | second | 16 | yes | 3.47e-09 | 7905.373 | 28.253 | 0.004 | 494.0858 | 4098.05 | 1341.06 | 2112 | 7 | yes |
| uniform-4194304 | `grust-next@counted+f32#1` | f32 | counted | pull | first | 19 | yes | 8.61e-09 | 7443.881 | 231.388 | 0.031 | 391.7832 | 4562.56 | 1358.31 | 1560 | 7 | yes |
| uniform-4194304 | `grust-next@counted+f32#1` | f32 | counted | pull | second | 19 | yes | 8.61e-09 | 7612.897 | 50.968 | 0.007 | 400.6788 | 4562.56 | 1358.31 | 516 | 7 | yes |
| uniform-4194304 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | first | 19 | yes | 8.61e-09 | 7129.681 | 55.235 | 0.008 | 375.2464 | 4154.67 | 1365.14 | 1560 | 7 | yes |
| uniform-4194304 | `grust-next@unchecked+f32#1` | f32 | unchecked | pull | second | 19 | yes | 8.61e-09 | 7410.010 | 211.732 | 0.029 | 390.0005 | 4154.67 | 1365.14 | 516 | 7 | yes |
| uniform-4194304 | `grust-next@counted#unset` | f64 | counted | push | first | 16 | yes | 3.47e-09 | 14675.194 | 86.003 | 0.006 | 917.1996 | 3846.99 | - | 2129 | 7 | yes |
| uniform-4194304 | `grust-next@counted#unset` | f64 | counted | push | second | 16 | yes | 3.47e-09 | 14839.196 | 147.878 | 0.010 | 927.4498 | 3846.99 | - | 2129 | 7 | yes |
| uniform-4194304 | `grust-next@unchecked#unset` | f64 | unchecked | push | first | 16 | yes | 3.47e-09 | 12244.289 | 74.325 | 0.006 | 765.2681 | 2858.14 | - | 2129 | 7 | yes |
| uniform-4194304 | `grust-next@unchecked#unset` | f64 | unchecked | push | second | 16 | yes | 3.47e-09 | 12264.493 | 133.197 | 0.011 | 766.5308 | 2858.14 | - | 2129 | 7 | yes |
| uniform-4194304 | `grust-next@counted+f32#unset` | f32 | counted | push | first | 20 | yes | 8.48e-09 | 15409.078 | 293.430 | 0.019 | 770.4539 | 3846.52 | - | 2097 | 7 | yes |
| uniform-4194304 | `grust-next@counted+f32#unset` | f32 | counted | push | second | 20 | yes | 8.48e-09 | 15328.092 | 715.846 | 0.047 | 766.4046 | 3846.52 | - | 2093 | 7 | yes |
| uniform-4194304 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | first | 20 | yes | 8.48e-09 | 12119.536 | 182.077 | 0.015 | 605.9768 | 2860.19 | - | 2097 | 7 | yes |
| uniform-4194304 | `grust-next@unchecked+f32#unset` | f32 | unchecked | push | second | 20 | yes | 8.48e-09 | 12140.001 | 143.587 | 0.012 | 607.0000 | 2860.19 | - | 2093 | 7 | yes |

## `b7-xlarge-full-width.json`: b7-xlarge-full-width

workers 16, concurrency 16, allocator glibc default, not pinned, 1 warmup + 5 repeats, steal over the run 3 ticks, 662.7 s, unusable at MAD/median >= 0.25

| fixture | participant | precision | accounting | kernel | call | iters | converged | residual | total ms | MAD | MAD/median | per iter ms | build ms | incoming ms | minflt | steal | usable |
| --- | --- | --- | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| hub-4194304 | `neo4j-graph` | f32 |  |  |  | 19 |  | 8.67e-09 | 406.324 | 4.203 | 0.010 | 21.3854 | 938.95 | - | 1127 | 1 | yes |
| hub-4194304 | `grust` | f64 | counted | pull | first | 16 | yes | 9.96e-09 | 3017.579 | 6.467 | 0.002 | 188.5987 | 8163.97 | - | 3454 | 1 | yes |
| hub-4194304 | `grust` | f64 | counted | pull | second | 16 | yes | 9.96e-09 | 1424.910 | 10.839 | 0.008 | 89.0569 | 8163.97 | - | 1604 | 1 | yes |
| hub-4194304 | `grust-next@counted` | f64 | counted | pull | first | 16 | yes | 9.96e-09 | 776.344 | 5.546 | 0.007 | 48.5215 | 3404.77 | 531.18 | 1197 | 1 | yes |
| hub-4194304 | `grust-next@counted` | f64 | counted | pull | second | 16 | yes | 9.96e-09 | 798.966 | 9.987 | 0.013 | 49.9354 | 3404.77 | 531.18 | 1108 | 1 | yes |
| hub-4194304 | `grust-next@unchecked` | f64 | unchecked | pull | first | 16 | yes | 9.96e-09 | 752.543 | 11.191 | 0.015 | 47.0339 | 2926.65 | 483.11 | 1705 | 1 | yes |
| hub-4194304 | `grust-next@unchecked` | f64 | unchecked | pull | second | 16 | yes | 9.96e-09 | 766.651 | 3.649 | 0.005 | 47.9157 | 2926.65 | 483.11 | 1617 | 1 | yes |
| hub-4194304 | `grust-next@counted+f32` | f32 | counted | pull | first | 20 | yes | 8.21e-09 | 569.537 | 24.259 | 0.043 | 28.4769 | 3440.20 | 549.13 | 2193 | 1 | yes |
| hub-4194304 | `grust-next@counted+f32` | f32 | counted | pull | second | 20 | yes | 8.21e-09 | 623.241 | 42.746 | 0.069 | 31.1620 | 3440.20 | 549.13 | 2092 | 1 | yes |
| hub-4194304 | `grust-next@unchecked+f32` | f32 | unchecked | pull | first | 20 | yes | 8.21e-09 | 511.390 | 19.369 | 0.038 | 25.5695 | 2932.62 | 492.98 | 1686 | 1 | yes |
| hub-4194304 | `grust-next@unchecked+f32` | f32 | unchecked | pull | second | 20 | yes | 8.21e-09 | 565.318 | 8.243 | 0.015 | 28.2659 | 2932.62 | 492.98 | 2097 | 1 | yes |
| uniform-4194304 | `neo4j-graph` | f32 |  |  |  | 29 |  | 8.75e-09 | 622.343 | 11.305 | 0.018 | 21.4601 | 961.93 | - | 1119 | 2 | yes |
| uniform-4194304 | `grust` | f64 | counted | pull | first | 16 | yes | 3.47e-09 | 3118.080 | 20.058 | 0.006 | 194.8800 | 8211.56 | - | 2484 | 2 | yes |
| uniform-4194304 | `grust` | f64 | counted | pull | second | 16 | yes | 3.47e-09 | 1559.551 | 9.308 | 0.006 | 97.4719 | 8211.56 | - | 1094 | 2 | yes |
| uniform-4194304 | `grust-next@counted` | f64 | counted | pull | first | 16 | yes | 3.47e-09 | 846.338 | 14.036 | 0.017 | 52.8961 | 3445.46 | 545.58 | 1191 | 2 | yes |
| uniform-4194304 | `grust-next@counted` | f64 | counted | pull | second | 16 | yes | 3.47e-09 | 859.262 | 7.468 | 0.009 | 53.7038 | 3445.46 | 545.58 | 1108 | 2 | yes |
| uniform-4194304 | `grust-next@unchecked` | f64 | unchecked | pull | first | 16 | yes | 3.47e-09 | 813.120 | 20.480 | 0.025 | 50.8200 | 2978.27 | 519.90 | 1198 | 2 | yes |
| uniform-4194304 | `grust-next@unchecked` | f64 | unchecked | pull | second | 16 | yes | 3.47e-09 | 788.048 | 17.466 | 0.022 | 49.2530 | 2978.27 | 519.90 | 1113 | 2 | yes |
| uniform-4194304 | `grust-next@counted+f32` | f32 | counted | pull | first | 19 | yes | 8.61e-09 | 550.859 | 17.953 | 0.033 | 28.9926 | 3471.08 | 562.23 | 1689 | 2 | yes |
| uniform-4194304 | `grust-next@counted+f32` | f32 | counted | pull | second | 19 | yes | 8.61e-09 | 568.300 | 7.827 | 0.014 | 29.9105 | 3471.08 | 562.23 | 2096 | 2 | yes |
| uniform-4194304 | `grust-next@unchecked+f32` | f32 | unchecked | pull | first | 19 | yes | 8.61e-09 | 511.963 | 8.759 | 0.017 | 26.9454 | 2960.34 | 512.21 | 1685 | 2 | yes |
| uniform-4194304 | `grust-next@unchecked+f32` | f32 | unchecked | pull | second | 19 | yes | 8.61e-09 | 534.079 | 50.271 | 0.094 | 28.1094 | 2960.34 | 512.21 | 2092 | 2 | yes |

## Iteration counts side by side

Each cell is the iteration count the participant reported for that fixture in that run (a Grust row reports the same count on both calls, so one is shown). `neo4j-graph` first, then the `+f32` rows, which are the rows that could stop where it stops, then the f64 rows. Where a count differs from `neo4j-graph`'s in the same row, the two totals were not the same number of sweeps over the arcs, and only the per-iteration column of the table above compares them.

| fixture | run | `neo4j-graph` | `grust-next@counted+f32#1` | `grust-next@counted+f32#unset` | `grust-next@unchecked+f32#1` | `grust-next@unchecked+f32#unset` | `grust-next@counted+f32` | `grust-next@unchecked+f32` | `grust#1` | `grust-next@counted#1` | `grust-next@counted#unset` | `grust-next@unchecked#1` | `grust-next@unchecked#unset` | `grust` | `grust-next@counted` | `grust-next@unchecked` |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| hub-16384 | b7-one-thread | 36 | 20 | 21 | 20 | 21 | - | - | 17 | 17 | 17 | 17 | 17 | - | - | - |
| hub-65536 | b7-one-thread | 28 | 20 | 21 | 20 | 21 | - | - | 17 | 17 | 17 | 17 | 17 | - | - | - |
| uniform-16384 | b7-one-thread | 28 | 19 | 19 | 19 | 19 | - | - | 16 | 16 | 16 | 16 | 16 | - | - | - |
| uniform-65536 | b7-one-thread | 34 | 19 | 20 | 19 | 20 | - | - | 16 | 16 | 16 | 16 | 16 | - | - | - |
| hub-16384 | b7-full-width | 36 | - | - | - | - | 20 | 20 | - | - | - | - | - | 17 | 17 | 17 |
| hub-65536 | b7-full-width | 33 | - | - | - | - | 20 | 20 | - | - | - | - | - | 17 | 17 | 17 |
| uniform-16384 | b7-full-width | 28 | - | - | - | - | 19 | 19 | - | - | - | - | - | 16 | 16 | 16 |
| uniform-65536 | b7-full-width | 34 | - | - | - | - | 19 | 19 | - | - | - | - | - | 16 | 16 | 16 |
| hub-2097152 | b7-large-one-thread | 26 | 20 | 21 | 20 | 21 | - | - | 16 | 16 | 16 | 16 | 16 | - | - | - |
| uniform-2097152 | b7-large-one-thread | 26 | 19 | 20 | 19 | 20 | - | - | 16 | 16 | 16 | 16 | 16 | - | - | - |
| hub-2097152 | b7-large-full-width | 28 | - | - | - | - | 20 | 20 | - | - | - | - | - | 16 | 16 | 16 |
| uniform-2097152 | b7-large-full-width | 27 | - | - | - | - | 19 | 19 | - | - | - | - | - | 16 | 16 | 16 |
| hub-4194304 | b7-xlarge-one-thread | 23 | 20 | 21 | 20 | 21 | - | - | 16 | 16 | 16 | 16 | 16 | - | - | - |
| uniform-4194304 | b7-xlarge-one-thread | 29 | 19 | 20 | 19 | 20 | - | - | 16 | 16 | 16 | 16 | 16 | - | - | - |
| hub-4194304 | b7-xlarge-full-width | 19 | - | - | - | - | 20 | 20 | - | - | - | - | - | 16 | 16 | 16 |
| uniform-4194304 | b7-xlarge-full-width | 29 | - | - | - | - | 19 | 19 | - | - | - | - | - | 16 | 16 | 16 |

Of 48 `+f32` cells, 0 stopped at the same count as `neo4j-graph` on the same fixture in the same run and 48 did not. For those, the totals are not comparable and the per-iteration times are:

- hub-16384, b7-one-thread: `grust-next@counted+f32#1` stopped at 20, `neo4j-graph` at 36.
- hub-16384, b7-one-thread: `grust-next@counted+f32#unset` stopped at 21, `neo4j-graph` at 36.
- hub-16384, b7-one-thread: `grust-next@unchecked+f32#1` stopped at 20, `neo4j-graph` at 36.
- hub-16384, b7-one-thread: `grust-next@unchecked+f32#unset` stopped at 21, `neo4j-graph` at 36.
- hub-65536, b7-one-thread: `grust-next@counted+f32#1` stopped at 20, `neo4j-graph` at 28.
- hub-65536, b7-one-thread: `grust-next@counted+f32#unset` stopped at 21, `neo4j-graph` at 28.
- hub-65536, b7-one-thread: `grust-next@unchecked+f32#1` stopped at 20, `neo4j-graph` at 28.
- hub-65536, b7-one-thread: `grust-next@unchecked+f32#unset` stopped at 21, `neo4j-graph` at 28.
- uniform-16384, b7-one-thread: `grust-next@counted+f32#1` stopped at 19, `neo4j-graph` at 28.
- uniform-16384, b7-one-thread: `grust-next@counted+f32#unset` stopped at 19, `neo4j-graph` at 28.
- uniform-16384, b7-one-thread: `grust-next@unchecked+f32#1` stopped at 19, `neo4j-graph` at 28.
- uniform-16384, b7-one-thread: `grust-next@unchecked+f32#unset` stopped at 19, `neo4j-graph` at 28.
- uniform-65536, b7-one-thread: `grust-next@counted+f32#1` stopped at 19, `neo4j-graph` at 34.
- uniform-65536, b7-one-thread: `grust-next@counted+f32#unset` stopped at 20, `neo4j-graph` at 34.
- uniform-65536, b7-one-thread: `grust-next@unchecked+f32#1` stopped at 19, `neo4j-graph` at 34.
- uniform-65536, b7-one-thread: `grust-next@unchecked+f32#unset` stopped at 20, `neo4j-graph` at 34.
- hub-16384, b7-full-width: `grust-next@counted+f32` stopped at 20, `neo4j-graph` at 36.
- hub-16384, b7-full-width: `grust-next@unchecked+f32` stopped at 20, `neo4j-graph` at 36.
- hub-65536, b7-full-width: `grust-next@counted+f32` stopped at 20, `neo4j-graph` at 33.
- hub-65536, b7-full-width: `grust-next@unchecked+f32` stopped at 20, `neo4j-graph` at 33.
- uniform-16384, b7-full-width: `grust-next@counted+f32` stopped at 19, `neo4j-graph` at 28.
- uniform-16384, b7-full-width: `grust-next@unchecked+f32` stopped at 19, `neo4j-graph` at 28.
- uniform-65536, b7-full-width: `grust-next@counted+f32` stopped at 19, `neo4j-graph` at 34.
- uniform-65536, b7-full-width: `grust-next@unchecked+f32` stopped at 19, `neo4j-graph` at 34.
- hub-2097152, b7-large-one-thread: `grust-next@counted+f32#1` stopped at 20, `neo4j-graph` at 26.
- hub-2097152, b7-large-one-thread: `grust-next@counted+f32#unset` stopped at 21, `neo4j-graph` at 26.
- hub-2097152, b7-large-one-thread: `grust-next@unchecked+f32#1` stopped at 20, `neo4j-graph` at 26.
- hub-2097152, b7-large-one-thread: `grust-next@unchecked+f32#unset` stopped at 21, `neo4j-graph` at 26.
- uniform-2097152, b7-large-one-thread: `grust-next@counted+f32#1` stopped at 19, `neo4j-graph` at 26.
- uniform-2097152, b7-large-one-thread: `grust-next@counted+f32#unset` stopped at 20, `neo4j-graph` at 26.
- uniform-2097152, b7-large-one-thread: `grust-next@unchecked+f32#1` stopped at 19, `neo4j-graph` at 26.
- uniform-2097152, b7-large-one-thread: `grust-next@unchecked+f32#unset` stopped at 20, `neo4j-graph` at 26.
- hub-2097152, b7-large-full-width: `grust-next@counted+f32` stopped at 20, `neo4j-graph` at 28.
- hub-2097152, b7-large-full-width: `grust-next@unchecked+f32` stopped at 20, `neo4j-graph` at 28.
- uniform-2097152, b7-large-full-width: `grust-next@counted+f32` stopped at 19, `neo4j-graph` at 27.
- uniform-2097152, b7-large-full-width: `grust-next@unchecked+f32` stopped at 19, `neo4j-graph` at 27.
- hub-4194304, b7-xlarge-one-thread: `grust-next@counted+f32#1` stopped at 20, `neo4j-graph` at 23.
- hub-4194304, b7-xlarge-one-thread: `grust-next@counted+f32#unset` stopped at 21, `neo4j-graph` at 23.
- hub-4194304, b7-xlarge-one-thread: `grust-next@unchecked+f32#1` stopped at 20, `neo4j-graph` at 23.
- hub-4194304, b7-xlarge-one-thread: `grust-next@unchecked+f32#unset` stopped at 21, `neo4j-graph` at 23.
- uniform-4194304, b7-xlarge-one-thread: `grust-next@counted+f32#1` stopped at 19, `neo4j-graph` at 29.
- uniform-4194304, b7-xlarge-one-thread: `grust-next@counted+f32#unset` stopped at 20, `neo4j-graph` at 29.
- uniform-4194304, b7-xlarge-one-thread: `grust-next@unchecked+f32#1` stopped at 19, `neo4j-graph` at 29.
- uniform-4194304, b7-xlarge-one-thread: `grust-next@unchecked+f32#unset` stopped at 20, `neo4j-graph` at 29.
- hub-4194304, b7-xlarge-full-width: `grust-next@counted+f32` stopped at 20, `neo4j-graph` at 19.
- hub-4194304, b7-xlarge-full-width: `grust-next@unchecked+f32` stopped at 20, `neo4j-graph` at 19.
- uniform-4194304, b7-xlarge-full-width: `grust-next@counted+f32` stopped at 19, `neo4j-graph` at 29.
- uniform-4194304, b7-xlarge-full-width: `grust-next@unchecked+f32` stopped at 19, `neo4j-graph` at 29.

## Parity

Every row parity produced for the participants B7 times, PageRank only. `vector` is how many of the n scores were bit-identical to the reference's f64 scores and the largest distance, in f64 ulps and in absolute terms; for an f32 row, widened to f64, the ulp figure is meaningless and the absolute one is the distance. It is recorded and not gated, as it is for every row. `bits` is the bit gate: f64 builds against v0.22.0, `+f32` builds against their counted row.

| file | fixture | participant | concurrency | verdict | iters | residual | vector | bits | detail |
| --- | --- | --- | --- | --- | ---: | ---: | --- | --- | --- |
| parity-b7-fixtures-1.json | hub-16384 | `neo4j-graph` | 1 | agrees | 36 | 9.29e-09 |  |  |  |
| parity-b7-fixtures-1.json | hub-16384 | `grust` | 1 | agrees | 17 | 3.23e-09 | 7352/16384, max 4 f64 ulps, 8.13e-20 abs |  |  |
| parity-b7-fixtures-1.json | hub-16384 | `grust-next@counted` | 1 | agrees | 17 | 3.23e-09 | 7352/16384, max 4 f64 ulps, 8.13e-20 abs | same as `grust` |  |
| parity-b7-fixtures-1.json | hub-16384 | `grust-next@unchecked` | 1 | agrees | 17 | 3.23e-09 | 7352/16384, max 4 f64 ulps, 8.13e-20 abs | same as `grust` |  |
| parity-b7-fixtures-1.json | hub-16384 | `grust-next@counted+f32` | 1 | agrees | 20 | 8.8e-09 | 0/16384, max 2621868491 f64 ulps, 4.38e-11 abs |  |  |
| parity-b7-fixtures-1.json | hub-16384 | `grust-next@unchecked+f32` | 1 | agrees | 20 | 8.8e-09 | 0/16384, max 2621868491 f64 ulps, 4.38e-11 abs | same as `grust-next@counted+f32` |  |
| parity-b7-fixtures-1.json | hub-65536 | `neo4j-graph` | 1 | agrees | 30 | 9.52e-09 |  |  |  |
| parity-b7-fixtures-1.json | hub-65536 | `grust` | 1 | agrees | 17 | 3.24e-09 | 29623/65536, max 4 f64 ulps, 1.36e-20 abs |  |  |
| parity-b7-fixtures-1.json | hub-65536 | `grust-next@counted` | 1 | agrees | 17 | 3.24e-09 | 29623/65536, max 4 f64 ulps, 1.36e-20 abs | same as `grust` |  |
| parity-b7-fixtures-1.json | hub-65536 | `grust-next@unchecked` | 1 | agrees | 17 | 3.24e-09 | 29623/65536, max 4 f64 ulps, 1.36e-20 abs | same as `grust` |  |
| parity-b7-fixtures-1.json | hub-65536 | `grust-next@counted+f32` | 1 | agrees | 20 | 8.44e-09 | 0/65536, max 2944077174 f64 ulps, 1.5e-11 abs |  |  |
| parity-b7-fixtures-1.json | hub-65536 | `grust-next@unchecked+f32` | 1 | agrees | 20 | 8.44e-09 | 0/65536, max 2944077174 f64 ulps, 1.5e-11 abs | same as `grust-next@counted+f32` |  |
| parity-b7-fixtures-1.json | uniform-16384 | `neo4j-graph` | 1 | agrees | 28 | 9.64e-09 |  |  |  |
| parity-b7-fixtures-1.json | uniform-16384 | `grust` | 1 | agrees | 16 | 3.36e-09 | 7355/16384, max 4 f64 ulps, 5.42e-20 abs |  |  |
| parity-b7-fixtures-1.json | uniform-16384 | `grust-next@counted` | 1 | agrees | 16 | 3.36e-09 | 7355/16384, max 4 f64 ulps, 5.42e-20 abs | same as `grust` |  |
| parity-b7-fixtures-1.json | uniform-16384 | `grust-next@unchecked` | 1 | agrees | 16 | 3.36e-09 | 7355/16384, max 4 f64 ulps, 5.42e-20 abs | same as `grust` |  |
| parity-b7-fixtures-1.json | uniform-16384 | `grust-next@counted+f32` | 1 | agrees | 19 | 8.76e-09 | 0/16384, max 2959917052 f64 ulps, 4.48e-11 abs |  |  |
| parity-b7-fixtures-1.json | uniform-16384 | `grust-next@unchecked+f32` | 1 | agrees | 19 | 8.76e-09 | 0/16384, max 2959917052 f64 ulps, 4.48e-11 abs | same as `grust-next@counted+f32` |  |
| parity-b7-fixtures-1.json | uniform-65536 | `neo4j-graph` | 1 | agrees | 34 | 9.7e-09 |  |  |  |
| parity-b7-fixtures-1.json | uniform-65536 | `grust` | 1 | agrees | 16 | 3.43e-09 | 29430/65536, max 4 f64 ulps, 2.03e-20 abs |  |  |
| parity-b7-fixtures-1.json | uniform-65536 | `grust-next@counted` | 1 | agrees | 16 | 3.43e-09 | 29430/65536, max 4 f64 ulps, 2.03e-20 abs | same as `grust` |  |
| parity-b7-fixtures-1.json | uniform-65536 | `grust-next@unchecked` | 1 | agrees | 16 | 3.43e-09 | 29430/65536, max 4 f64 ulps, 2.03e-20 abs | same as `grust` |  |
| parity-b7-fixtures-1.json | uniform-65536 | `grust-next@counted+f32` | 1 | agrees | 19 | 8.53e-09 | 0/65536, max 3047578129 f64 ulps, 1.15e-11 abs |  |  |
| parity-b7-fixtures-1.json | uniform-65536 | `grust-next@unchecked+f32` | 1 | agrees | 19 | 8.53e-09 | 0/65536, max 3047578129 f64 ulps, 1.15e-11 abs | same as `grust-next@counted+f32` |  |
| parity-b7-fixtures-16.json | hub-16384 | `neo4j-graph` | 16 | agrees | 36 | 9.29e-09 |  |  |  |
| parity-b7-fixtures-16.json | hub-16384 | `grust` | 16 | agrees | 17 | 3.23e-09 | 7352/16384, max 4 f64 ulps, 8.13e-20 abs |  |  |
| parity-b7-fixtures-16.json | hub-16384 | `grust-next@counted` | 16 | agrees | 17 | 3.23e-09 | 7352/16384, max 4 f64 ulps, 8.13e-20 abs | same as `grust` |  |
| parity-b7-fixtures-16.json | hub-16384 | `grust-next@unchecked` | 16 | agrees | 17 | 3.23e-09 | 7352/16384, max 4 f64 ulps, 8.13e-20 abs | same as `grust` |  |
| parity-b7-fixtures-16.json | hub-16384 | `grust-next@counted+f32` | 16 | agrees | 20 | 8.8e-09 | 0/16384, max 2621868491 f64 ulps, 4.38e-11 abs |  |  |
| parity-b7-fixtures-16.json | hub-16384 | `grust-next@unchecked+f32` | 16 | agrees | 20 | 8.8e-09 | 0/16384, max 2621868491 f64 ulps, 4.38e-11 abs | same as `grust-next@counted+f32` |  |
| parity-b7-fixtures-16.json | hub-65536 | `neo4j-graph` | 16 | agrees | 33 | 8.57e-09 |  |  |  |
| parity-b7-fixtures-16.json | hub-65536 | `grust` | 16 | agrees | 17 | 3.24e-09 | 29623/65536, max 4 f64 ulps, 1.36e-20 abs |  |  |
| parity-b7-fixtures-16.json | hub-65536 | `grust-next@counted` | 16 | agrees | 17 | 3.24e-09 | 29623/65536, max 4 f64 ulps, 1.36e-20 abs | same as `grust` |  |
| parity-b7-fixtures-16.json | hub-65536 | `grust-next@unchecked` | 16 | agrees | 17 | 3.24e-09 | 29623/65536, max 4 f64 ulps, 1.36e-20 abs | same as `grust` |  |
| parity-b7-fixtures-16.json | hub-65536 | `grust-next@counted+f32` | 16 | agrees | 20 | 8.44e-09 | 0/65536, max 2944077174 f64 ulps, 1.5e-11 abs |  |  |
| parity-b7-fixtures-16.json | hub-65536 | `grust-next@unchecked+f32` | 16 | agrees | 20 | 8.44e-09 | 0/65536, max 2944077174 f64 ulps, 1.5e-11 abs | same as `grust-next@counted+f32` |  |
| parity-b7-fixtures-16.json | uniform-16384 | `neo4j-graph` | 16 | agrees | 28 | 9.64e-09 |  |  |  |
| parity-b7-fixtures-16.json | uniform-16384 | `grust` | 16 | agrees | 16 | 3.36e-09 | 7355/16384, max 4 f64 ulps, 5.42e-20 abs |  |  |
| parity-b7-fixtures-16.json | uniform-16384 | `grust-next@counted` | 16 | agrees | 16 | 3.36e-09 | 7355/16384, max 4 f64 ulps, 5.42e-20 abs | same as `grust` |  |
| parity-b7-fixtures-16.json | uniform-16384 | `grust-next@unchecked` | 16 | agrees | 16 | 3.36e-09 | 7355/16384, max 4 f64 ulps, 5.42e-20 abs | same as `grust` |  |
| parity-b7-fixtures-16.json | uniform-16384 | `grust-next@counted+f32` | 16 | agrees | 19 | 8.76e-09 | 0/16384, max 2959917052 f64 ulps, 4.48e-11 abs |  |  |
| parity-b7-fixtures-16.json | uniform-16384 | `grust-next@unchecked+f32` | 16 | agrees | 19 | 8.76e-09 | 0/16384, max 2959917052 f64 ulps, 4.48e-11 abs | same as `grust-next@counted+f32` |  |
| parity-b7-fixtures-16.json | uniform-65536 | `neo4j-graph` | 16 | agrees | 34 | 8.83e-09 |  |  |  |
| parity-b7-fixtures-16.json | uniform-65536 | `grust` | 16 | agrees | 16 | 3.43e-09 | 29430/65536, max 4 f64 ulps, 2.03e-20 abs |  |  |
| parity-b7-fixtures-16.json | uniform-65536 | `grust-next@counted` | 16 | agrees | 16 | 3.43e-09 | 29430/65536, max 4 f64 ulps, 2.03e-20 abs | same as `grust` |  |
| parity-b7-fixtures-16.json | uniform-65536 | `grust-next@unchecked` | 16 | agrees | 16 | 3.43e-09 | 29430/65536, max 4 f64 ulps, 2.03e-20 abs | same as `grust` |  |
| parity-b7-fixtures-16.json | uniform-65536 | `grust-next@counted+f32` | 16 | agrees | 19 | 8.53e-09 | 0/65536, max 3047578129 f64 ulps, 1.15e-11 abs |  |  |
| parity-b7-fixtures-16.json | uniform-65536 | `grust-next@unchecked+f32` | 16 | agrees | 19 | 8.53e-09 | 0/65536, max 3047578129 f64 ulps, 1.15e-11 abs | same as `grust-next@counted+f32` |  |
| parity-b7-fixtures-large-1.json | hub-2097152 | `neo4j-graph` | 1 | agrees | 28 | 8.74e-09 |  |  |  |
| parity-b7-fixtures-large-1.json | hub-2097152 | `grust` | 1 | agrees | 16 | 9.96e-09 | 937899/2097152, max 6 f64 ulps, 8.47e-22 abs |  |  |
| parity-b7-fixtures-large-1.json | hub-2097152 | `grust-next@counted` | 1 | agrees | 16 | 9.96e-09 | 937899/2097152, max 6 f64 ulps, 8.47e-22 abs | same as `grust` |  |
| parity-b7-fixtures-large-1.json | hub-2097152 | `grust-next@unchecked` | 1 | agrees | 16 | 9.96e-09 | 937899/2097152, max 6 f64 ulps, 8.47e-22 abs | same as `grust` |  |
| parity-b7-fixtures-large-1.json | hub-2097152 | `grust-next@counted+f32` | 1 | agrees | 20 | 8.19e-09 | 0/2097152, max 3109437963 f64 ulps, 4.95e-13 abs |  |  |
| parity-b7-fixtures-large-1.json | hub-2097152 | `grust-next@unchecked+f32` | 1 | agrees | 20 | 8.19e-09 | 0/2097152, max 3109437963 f64 ulps, 4.95e-13 abs | same as `grust-next@counted+f32` |  |
| parity-b7-fixtures-large-1.json | uniform-2097152 | `neo4j-graph` | 1 | agrees | 27 | 8.23e-09 |  |  |  |
| parity-b7-fixtures-large-1.json | uniform-2097152 | `grust` | 1 | agrees | 16 | 3.46e-09 | 943172/2097152, max 6 f64 ulps, 8.47e-22 abs |  |  |
| parity-b7-fixtures-large-1.json | uniform-2097152 | `grust-next@counted` | 1 | agrees | 16 | 3.46e-09 | 943172/2097152, max 6 f64 ulps, 8.47e-22 abs | same as `grust` |  |
| parity-b7-fixtures-large-1.json | uniform-2097152 | `grust-next@unchecked` | 1 | agrees | 16 | 3.46e-09 | 943172/2097152, max 6 f64 ulps, 8.47e-22 abs | same as `grust` |  |
| parity-b7-fixtures-large-1.json | uniform-2097152 | `grust-next@counted+f32` | 1 | agrees | 19 | 8.59e-09 | 0/2097152, max 3389236176 f64 ulps, 4.79e-13 abs |  |  |
| parity-b7-fixtures-large-1.json | uniform-2097152 | `grust-next@unchecked+f32` | 1 | agrees | 19 | 8.59e-09 | 0/2097152, max 3389236176 f64 ulps, 4.79e-13 abs | same as `grust-next@counted+f32` |  |
| parity-b7-fixtures-large-16.json | hub-2097152 | `neo4j-graph` | 16 | agrees | 28 | 9.19e-09 |  |  |  |
| parity-b7-fixtures-large-16.json | hub-2097152 | `grust` | 16 | agrees | 16 | 9.96e-09 | 937899/2097152, max 6 f64 ulps, 8.47e-22 abs |  |  |
| parity-b7-fixtures-large-16.json | hub-2097152 | `grust-next@counted` | 16 | agrees | 16 | 9.96e-09 | 937899/2097152, max 6 f64 ulps, 8.47e-22 abs | same as `grust` |  |
| parity-b7-fixtures-large-16.json | hub-2097152 | `grust-next@unchecked` | 16 | agrees | 16 | 9.96e-09 | 937899/2097152, max 6 f64 ulps, 8.47e-22 abs | same as `grust` |  |
| parity-b7-fixtures-large-16.json | hub-2097152 | `grust-next@counted+f32` | 16 | agrees | 20 | 8.19e-09 | 0/2097152, max 3109437963 f64 ulps, 4.95e-13 abs |  |  |
| parity-b7-fixtures-large-16.json | hub-2097152 | `grust-next@unchecked+f32` | 16 | agrees | 20 | 8.19e-09 | 0/2097152, max 3109437963 f64 ulps, 4.95e-13 abs | same as `grust-next@counted+f32` |  |
| parity-b7-fixtures-large-16.json | uniform-2097152 | `neo4j-graph` | 16 | agrees | 28 | 8.19e-09 |  |  |  |
| parity-b7-fixtures-large-16.json | uniform-2097152 | `grust` | 16 | agrees | 16 | 3.46e-09 | 943172/2097152, max 6 f64 ulps, 8.47e-22 abs |  |  |
| parity-b7-fixtures-large-16.json | uniform-2097152 | `grust-next@counted` | 16 | agrees | 16 | 3.46e-09 | 943172/2097152, max 6 f64 ulps, 8.47e-22 abs | same as `grust` |  |
| parity-b7-fixtures-large-16.json | uniform-2097152 | `grust-next@unchecked` | 16 | agrees | 16 | 3.46e-09 | 943172/2097152, max 6 f64 ulps, 8.47e-22 abs | same as `grust` |  |
| parity-b7-fixtures-large-16.json | uniform-2097152 | `grust-next@counted+f32` | 16 | agrees | 19 | 8.59e-09 | 0/2097152, max 3389236176 f64 ulps, 4.79e-13 abs |  |  |
| parity-b7-fixtures-large-16.json | uniform-2097152 | `grust-next@unchecked+f32` | 16 | agrees | 19 | 8.59e-09 | 0/2097152, max 3389236176 f64 ulps, 4.79e-13 abs | same as `grust-next@counted+f32` |  |
| parity-b7-fixtures-large-unset.json | hub-2097152 | `neo4j-graph` | unset | agrees | 28 | 8.5e-09 |  |  |  |
| parity-b7-fixtures-large-unset.json | hub-2097152 | `grust` | unset | agrees | 16 | 9.96e-09 | 106053/2097152, max 8 f64 ulps, 1.06e-21 abs |  |  |
| parity-b7-fixtures-large-unset.json | hub-2097152 | `grust-next@counted` | unset | agrees | 16 | 9.96e-09 | 106053/2097152, max 8 f64 ulps, 1.06e-21 abs | same as `grust` |  |
| parity-b7-fixtures-large-unset.json | hub-2097152 | `grust-next@unchecked` | unset | agrees | 16 | 9.96e-09 | 106053/2097152, max 8 f64 ulps, 1.06e-21 abs | same as `grust` |  |
| parity-b7-fixtures-large-unset.json | hub-2097152 | `grust-next@counted+f32` | unset | agrees | 21 | 8.2e-09 | 0/2097152, max 6097654486 f64 ulps, 9.28e-13 abs |  |  |
| parity-b7-fixtures-large-unset.json | hub-2097152 | `grust-next@unchecked+f32` | unset | agrees | 21 | 8.2e-09 | 0/2097152, max 6097654486 f64 ulps, 9.28e-13 abs | same as `grust-next@counted+f32` |  |
| parity-b7-fixtures-large-unset.json | uniform-2097152 | `neo4j-graph` | unset | agrees | 28 | 8.25e-09 |  |  |  |
| parity-b7-fixtures-large-unset.json | uniform-2097152 | `grust` | unset | agrees | 16 | 3.46e-09 | 2097053/2097152, max 2 f64 ulps, 2.12e-22 abs |  |  |
| parity-b7-fixtures-large-unset.json | uniform-2097152 | `grust-next@counted` | unset | agrees | 16 | 3.46e-09 | 2097053/2097152, max 2 f64 ulps, 2.12e-22 abs | same as `grust` |  |
| parity-b7-fixtures-large-unset.json | uniform-2097152 | `grust-next@unchecked` | unset | agrees | 16 | 3.46e-09 | 2097053/2097152, max 2 f64 ulps, 2.12e-22 abs | same as `grust` |  |
| parity-b7-fixtures-large-unset.json | uniform-2097152 | `grust-next@counted+f32` | unset | agrees | 20 | 8.43e-09 | 0/2097152, max 3561951160 f64 ulps, 4.88e-13 abs |  |  |
| parity-b7-fixtures-large-unset.json | uniform-2097152 | `grust-next@unchecked+f32` | unset | agrees | 20 | 8.43e-09 | 0/2097152, max 3561951160 f64 ulps, 4.88e-13 abs | same as `grust-next@counted+f32` |  |
| parity-b7-fixtures-unset.json | hub-16384 | `neo4j-graph` | unset | agrees | 36 | 9.29e-09 |  |  |  |
| parity-b7-fixtures-unset.json | hub-16384 | `grust` | unset | agrees | 17 | 3.23e-09 | 699/16384, max 6 f64 ulps, 1.08e-19 abs |  |  |
| parity-b7-fixtures-unset.json | hub-16384 | `grust-next@counted` | unset | agrees | 17 | 3.23e-09 | 699/16384, max 6 f64 ulps, 1.08e-19 abs | same as `grust` |  |
| parity-b7-fixtures-unset.json | hub-16384 | `grust-next@unchecked` | unset | agrees | 17 | 3.23e-09 | 699/16384, max 6 f64 ulps, 1.08e-19 abs | same as `grust` |  |
| parity-b7-fixtures-unset.json | hub-16384 | `grust-next@counted+f32` | unset | agrees | 21 | 8.58e-09 | 0/16384, max 5491328727 f64 ulps, 9.72e-11 abs |  |  |
| parity-b7-fixtures-unset.json | hub-16384 | `grust-next@unchecked+f32` | unset | agrees | 21 | 8.58e-09 | 0/16384, max 5491328727 f64 ulps, 9.72e-11 abs | same as `grust-next@counted+f32` |  |
| parity-b7-fixtures-unset.json | hub-65536 | `neo4j-graph` | unset | agrees | 32 | 9.76e-09 |  |  |  |
| parity-b7-fixtures-unset.json | hub-65536 | `grust` | unset | agrees | 17 | 3.24e-09 | 3230/65536, max 7 f64 ulps, 2.71e-20 abs |  |  |
| parity-b7-fixtures-unset.json | hub-65536 | `grust-next@counted` | unset | agrees | 17 | 3.24e-09 | 3230/65536, max 7 f64 ulps, 2.71e-20 abs | same as `grust` |  |
| parity-b7-fixtures-unset.json | hub-65536 | `grust-next@unchecked` | unset | agrees | 17 | 3.24e-09 | 3230/65536, max 7 f64 ulps, 2.71e-20 abs | same as `grust` |  |
| parity-b7-fixtures-unset.json | hub-65536 | `grust-next@counted+f32` | unset | agrees | 21 | 8.04e-09 | 0/65536, max 6037950115 f64 ulps, 2.41e-11 abs |  |  |
| parity-b7-fixtures-unset.json | hub-65536 | `grust-next@unchecked+f32` | unset | agrees | 21 | 8.04e-09 | 0/65536, max 6037950115 f64 ulps, 2.41e-11 abs | same as `grust-next@counted+f32` |  |
| parity-b7-fixtures-unset.json | uniform-16384 | `neo4j-graph` | unset | agrees | 28 | 9.64e-09 |  |  |  |
| parity-b7-fixtures-unset.json | uniform-16384 | `grust` | unset | agrees | 16 | 3.36e-09 | 16325/16384, max 2 f64 ulps, 2.71e-20 abs |  |  |
| parity-b7-fixtures-unset.json | uniform-16384 | `grust-next@counted` | unset | agrees | 16 | 3.36e-09 | 16325/16384, max 2 f64 ulps, 2.71e-20 abs | same as `grust` |  |
| parity-b7-fixtures-unset.json | uniform-16384 | `grust-next@unchecked` | unset | agrees | 16 | 3.36e-09 | 16325/16384, max 2 f64 ulps, 2.71e-20 abs | same as `grust` |  |
| parity-b7-fixtures-unset.json | uniform-16384 | `grust-next@counted+f32` | unset | agrees | 19 | 9.5e-09 | 0/16384, max 2960955813 f64 ulps, 4.28e-11 abs |  |  |
| parity-b7-fixtures-unset.json | uniform-16384 | `grust-next@unchecked+f32` | unset | agrees | 19 | 9.5e-09 | 0/16384, max 2960955813 f64 ulps, 4.28e-11 abs | same as `grust-next@counted+f32` |  |
| parity-b7-fixtures-unset.json | uniform-65536 | `neo4j-graph` | unset | agrees | 34 | 9.87e-09 |  |  |  |
| parity-b7-fixtures-unset.json | uniform-65536 | `grust` | unset | agrees | 16 | 3.43e-09 | 65467/65536, max 2 f64 ulps, 6.78e-21 abs |  |  |
| parity-b7-fixtures-unset.json | uniform-65536 | `grust-next@counted` | unset | agrees | 16 | 3.43e-09 | 65467/65536, max 2 f64 ulps, 6.78e-21 abs | same as `grust` |  |
| parity-b7-fixtures-unset.json | uniform-65536 | `grust-next@unchecked` | unset | agrees | 16 | 3.43e-09 | 65467/65536, max 2 f64 ulps, 6.78e-21 abs | same as `grust` |  |
| parity-b7-fixtures-unset.json | uniform-65536 | `grust-next@counted+f32` | unset | agrees | 20 | 8.39e-09 | 0/65536, max 3317924464 f64 ulps, 1.36e-11 abs |  |  |
| parity-b7-fixtures-unset.json | uniform-65536 | `grust-next@unchecked+f32` | unset | agrees | 20 | 8.39e-09 | 0/65536, max 3317924464 f64 ulps, 1.36e-11 abs | same as `grust-next@counted+f32` |  |
| parity-b7-fixtures-xlarge-1.json | hub-4194304 | `neo4j-graph` | 1 | agrees | 20 | 8.41e-09 |  |  |  |
| parity-b7-fixtures-xlarge-1.json | hub-4194304 | `grust` | 1 | agrees | 16 | 9.96e-09 | 1874065/4194304, max 6 f64 ulps, 4.24e-22 abs |  |  |
| parity-b7-fixtures-xlarge-1.json | hub-4194304 | `grust-next@counted` | 1 | agrees | 16 | 9.96e-09 | 1874065/4194304, max 6 f64 ulps, 4.24e-22 abs | same as `grust` |  |
| parity-b7-fixtures-xlarge-1.json | hub-4194304 | `grust-next@unchecked` | 1 | agrees | 16 | 9.96e-09 | 1874065/4194304, max 6 f64 ulps, 4.24e-22 abs | same as `grust` |  |
| parity-b7-fixtures-xlarge-1.json | hub-4194304 | `grust-next@counted+f32` | 1 | agrees | 20 | 8.21e-09 | 0/4194304, max 3452255767 f64 ulps, 2.6e-13 abs |  |  |
| parity-b7-fixtures-xlarge-1.json | hub-4194304 | `grust-next@unchecked+f32` | 1 | agrees | 20 | 8.21e-09 | 0/4194304, max 3452255767 f64 ulps, 2.6e-13 abs | same as `grust-next@counted+f32` |  |
| parity-b7-fixtures-xlarge-1.json | uniform-4194304 | `neo4j-graph` | 1 | agrees | 29 | 8.33e-09 |  |  |  |
| parity-b7-fixtures-xlarge-1.json | uniform-4194304 | `grust` | 1 | agrees | 16 | 3.47e-09 | 1884240/4194304, max 6 f64 ulps, 4.24e-22 abs |  |  |
| parity-b7-fixtures-xlarge-1.json | uniform-4194304 | `grust-next@counted` | 1 | agrees | 16 | 3.47e-09 | 1884240/4194304, max 6 f64 ulps, 4.24e-22 abs | same as `grust` |  |
| parity-b7-fixtures-xlarge-1.json | uniform-4194304 | `grust-next@unchecked` | 1 | agrees | 16 | 3.47e-09 | 1884240/4194304, max 6 f64 ulps, 4.24e-22 abs | same as `grust` |  |
| parity-b7-fixtures-xlarge-1.json | uniform-4194304 | `grust-next@counted+f32` | 1 | agrees | 19 | 8.61e-09 | 0/4194304, max 3146797518 f64 ulps, 2.6e-13 abs |  |  |
| parity-b7-fixtures-xlarge-1.json | uniform-4194304 | `grust-next@unchecked+f32` | 1 | agrees | 19 | 8.61e-09 | 0/4194304, max 3146797518 f64 ulps, 2.6e-13 abs | same as `grust-next@counted+f32` |  |
| parity-b7-fixtures-xlarge-16.json | hub-4194304 | `neo4j-graph` | 16 | agrees | 18 | 7.63e-09 |  |  |  |
| parity-b7-fixtures-xlarge-16.json | hub-4194304 | `grust` | 16 | agrees | 16 | 9.96e-09 | 1874065/4194304, max 6 f64 ulps, 4.24e-22 abs |  |  |
| parity-b7-fixtures-xlarge-16.json | hub-4194304 | `grust-next@counted` | 16 | agrees | 16 | 9.96e-09 | 1874065/4194304, max 6 f64 ulps, 4.24e-22 abs | same as `grust` |  |
| parity-b7-fixtures-xlarge-16.json | hub-4194304 | `grust-next@unchecked` | 16 | agrees | 16 | 9.96e-09 | 1874065/4194304, max 6 f64 ulps, 4.24e-22 abs | same as `grust` |  |
| parity-b7-fixtures-xlarge-16.json | hub-4194304 | `grust-next@counted+f32` | 16 | agrees | 20 | 8.21e-09 | 0/4194304, max 3452255767 f64 ulps, 2.6e-13 abs |  |  |
| parity-b7-fixtures-xlarge-16.json | hub-4194304 | `grust-next@unchecked+f32` | 16 | agrees | 20 | 8.21e-09 | 0/4194304, max 3452255767 f64 ulps, 2.6e-13 abs | same as `grust-next@counted+f32` |  |
| parity-b7-fixtures-xlarge-16.json | uniform-4194304 | `neo4j-graph` | 16 | agrees | 29 | 8.38e-09 |  |  |  |
| parity-b7-fixtures-xlarge-16.json | uniform-4194304 | `grust` | 16 | agrees | 16 | 3.47e-09 | 1884240/4194304, max 6 f64 ulps, 4.24e-22 abs |  |  |
| parity-b7-fixtures-xlarge-16.json | uniform-4194304 | `grust-next@counted` | 16 | agrees | 16 | 3.47e-09 | 1884240/4194304, max 6 f64 ulps, 4.24e-22 abs | same as `grust` |  |
| parity-b7-fixtures-xlarge-16.json | uniform-4194304 | `grust-next@unchecked` | 16 | agrees | 16 | 3.47e-09 | 1884240/4194304, max 6 f64 ulps, 4.24e-22 abs | same as `grust` |  |
| parity-b7-fixtures-xlarge-16.json | uniform-4194304 | `grust-next@counted+f32` | 16 | agrees | 19 | 8.61e-09 | 0/4194304, max 3146797518 f64 ulps, 2.6e-13 abs |  |  |
| parity-b7-fixtures-xlarge-16.json | uniform-4194304 | `grust-next@unchecked+f32` | 16 | agrees | 19 | 8.61e-09 | 0/4194304, max 3146797518 f64 ulps, 2.6e-13 abs | same as `grust-next@counted+f32` |  |
| parity-b7-fixtures-xlarge-unset.json | hub-4194304 | `neo4j-graph` | unset | agrees | 17 | 8.26e-09 |  |  |  |
| parity-b7-fixtures-xlarge-unset.json | hub-4194304 | `grust` | unset | agrees | 16 | 9.96e-09 | 211043/4194304, max 8 f64 ulps, 5.29e-22 abs |  |  |
| parity-b7-fixtures-xlarge-unset.json | hub-4194304 | `grust-next@counted` | unset | agrees | 16 | 9.96e-09 | 211043/4194304, max 8 f64 ulps, 5.29e-22 abs | same as `grust` |  |
| parity-b7-fixtures-xlarge-unset.json | hub-4194304 | `grust-next@unchecked` | unset | agrees | 16 | 9.96e-09 | 211043/4194304, max 8 f64 ulps, 5.29e-22 abs | same as `grust` |  |
| parity-b7-fixtures-xlarge-unset.json | hub-4194304 | `grust-next@counted+f32` | unset | agrees | 21 | 8.31e-09 | 0/4194304, max 6393034292 f64 ulps, 4.45e-13 abs |  |  |
| parity-b7-fixtures-xlarge-unset.json | hub-4194304 | `grust-next@unchecked+f32` | unset | agrees | 21 | 8.31e-09 | 0/4194304, max 6393034292 f64 ulps, 4.45e-13 abs | same as `grust-next@counted+f32` |  |
| parity-b7-fixtures-xlarge-unset.json | uniform-4194304 | `neo4j-graph` | unset | agrees | 29 | 8.05e-09 |  |  |  |
| parity-b7-fixtures-xlarge-unset.json | uniform-4194304 | `grust` | unset | agrees | 16 | 3.47e-09 | 4194236/4194304, max 2 f64 ulps, 1.06e-22 abs |  |  |
| parity-b7-fixtures-xlarge-unset.json | uniform-4194304 | `grust-next@counted` | unset | agrees | 16 | 3.47e-09 | 4194236/4194304, max 2 f64 ulps, 1.06e-22 abs | same as `grust` |  |
| parity-b7-fixtures-xlarge-unset.json | uniform-4194304 | `grust-next@unchecked` | unset | agrees | 16 | 3.47e-09 | 4194236/4194304, max 2 f64 ulps, 1.06e-22 abs | same as `grust` |  |
| parity-b7-fixtures-xlarge-unset.json | uniform-4194304 | `grust-next@counted+f32` | unset | agrees | 20 | 8.48e-09 | 0/4194304, max 3709657623 f64 ulps, 2.74e-13 abs |  |  |
| parity-b7-fixtures-xlarge-unset.json | uniform-4194304 | `grust-next@unchecked+f32` | unset | agrees | 20 | 8.48e-09 | 0/4194304, max 3709657623 f64 ulps, 2.74e-13 abs | same as `grust-next@counted+f32` |  |

