# B3, the timed run — quegee, 2026-09-21

What produced these files, so a reader can tell what they are evidence of.

## Provenance

| tree | commit | working tree |
| --- | --- | --- |
| Grust | `2182cdb82acb0666b80f483dc4c9666941962145` (`v0.22.0`) | clean |
| Icecat | `57b443ec1d16809893950b080cf8d0971f8da174` | clean, `extlibs/tlx` and `extlibs/ttmath` initialised |
| this repo | `8fd82234` | clean |

Host: quegee, 16 vCPU on 8 physical cores, 24.8 MB L3, not burstable. Image
`simple-rust-algo-bench:quegee2`, built on this box: a participant binary built
elsewhere is not the binary being timed.

**The Grust columns are the release**, not main, so the label and the SHA agree.

## Files

| file | what it is |
| --- | --- |
| `fixtures-manifest.json` | the eight fixtures by name, node and edge count, size and SHA-256. The edge lists are regenerated from the seeded generator rather than stored; the hashes say a rerun uses the same bytes. |
| `parity-unset.json`, `parity-1.json`, `parity-16.json` | correctness before timing, at each thread configuration. Concurrency selects a *kernel* in Grust rather than a thread count, so each configuration is gated as itself. 160 checks, 4 mismatches, the same four in all three. |
| `one-thread.json` | table 1, `--cpus 1 --workers 1`. The kernel comparison, and the only configuration in which the lineage claim is valid. |
| `full-width.json` | table 2, `--cpus 16 --workers 16`. What a user of either library gets. |

Both timed files carry a `notes` block stating the table rules as data: no
width-to-width ratio against a participant that cannot use width, the lineage
comparison belongs to the one-thread run, and cells from runs at different widths
are not divided by one another.

## What the parity mismatches are

All four are `library` PageRank, on `layered-16384`, `layered-65536`,
`path-16384` and `path-65536` — the two families with dangling nodes, at both
sizes, and neither family without them. `graph 0.3.2` has no sink handling, so
mass leaks and the score sum falls short of 1.0 in proportion to the dangling
share. **PageRank therefore publishes on `hub` and `uniform` only**, and these
rows are the stated reason rather than a silent omission.

## Two cells not to read as measurements

- `icebug` PageRank on `hub-16384` at full width: `54.09 ± 51.01 ms`. A MAD the
  size of the median is not a measurement. Reported as unusable.
- `path-65536` PageRank argmax is undetermined at `1e-8` for every participant:
  every interior node of a uniform chain has the same rank, so the maximum's
  identity is a tie-break rather than a result.

## Two boundaries that belong under any PageRank table

- **`library` computes in `f32`; every other participant in `f64`.** At these
  sizes the working set is inside this host's 24.8 MB L3, so single precision buys
  bandwidth on one array rather than cache residency. That qualification is
  size-dependent and stops being true somewhere in the hundreds of thousands of
  nodes at this density.
- **Participants stop on different rules**, so `total` and `per iteration` are both
  reported. `library` runs 28 and 34 iterations where the `f64` participants run 17
  and 16: a kernel that runs more iterations is not slower, it did more of them.

## Grust's parallel floors are recorded per cell

Every Grust-family cell carries `units`, `floor` and `parallel_eligible`. BFS at
16,384 is 147,313 units against a 262,144 floor, so it is sequential at any
requested width — 1.63 ms at one thread and 1.66 at sixteen — and clears the floor
at 65,536, where it goes 7.86 to 4.30. A reader can therefore tell a kernel that
declined to parallelise from one that parallelised badly, which is the difference
16,384 alone would have hidden.
