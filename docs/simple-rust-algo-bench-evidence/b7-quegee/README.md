# B7, PageRank at f32 under B5's protocol — quegee, 2026-09-22

What produced these files, so a reader can tell what they are evidence of.

## Why there is a B7

B6's tables show `neo4j-graph`, which accumulates and returns f32, stopping
PageRank between 20 and 36 iterations under tolerance 1e-8 where Grust's f64
kernel stopped at 16 or 17, so no total of one was the same number of sweeps
as a total of the other. Grust `ead3568` adds `pagerank_f32`, the same kernel
with f32 scores and the residual summed in f64 as `neo4j-graph` sums it. B7
times that beside Grust's f64 kernel and beside `neo4j-graph`, PageRank alone,
on the two dangling-free families at the protocol, large and xlarge sizes,
with the iteration count in every table beside the total.

## Provenance

| tree | commit | staged from |
| --- | --- | --- |
| Grust, `grust` participant | `2182cdb82acb` (v0.22.0) | `git archive v0.22.0` |
| Grust, `grust-next` participant | `ead35685968685e11b201deb172840ab6a84c17d` (`work/pagerank-f32`) | `git archive ead3568` |
| Icecat | `57b443ec1d16` | working tree, clean |
| this repo, as built into the image | `fdf85a917551` (`work/bench-b7`) | working tree, clean |

All of this is in `sources.json`, written by `build.py` when it staged the
image; the two Grust trees were archived from the named commits rather than
hardlinked from checkouts, so no working-tree state could reach them.
`receipts/image.json` is the image, `simple-rust-algo-bench:b7-ead3568`, built
on quegee under a 20 GB memory cap with four jobs (`systemd-run --user --scope
-p MemoryMax=20G -p MemorySwapMax=0`, `--jobs 4`; `build.log`), and not
rebuilt afterwards: every parity and timed invocation in `campaign.jsonl`
names that tag. `receipts/audit.json` has each of the six binaries' receipt
and SHA-256, and they are six distinct binaries; `icebug` is byte-identical to
B6's and B5's. The audit, the image receipt, the manifest and `plan.json` were
taken before parity began, not during a run.

Grust `ead3568` passed `scripts/ci-local.sh` on Linux x86_64 on host grust
before the image was built (`ci-local: PASSED every gate at ead3568 on Linux
x86_64 in 2417s`); the verdict was read after waiting on the gate's process,
not on a string in its log.

Host: quegee, 16 vCPU on 8 physical cores, 24.8 MB L3, not burstable.

## What did not change since B6

- **The fixtures.** The eight hub and uniform files of B6's twelve, read from
  B6's work directory; `fixtures-manifest.json` records every SHA-256 and byte
  count checked against `b6-quegee/fixtures-manifest.json` before the build
  (`identical_to_b6`).
- **The protocol.** Parity first, every fixture set at concurrency unset, 1
  and 16; the page cache dropped after parity and before the first timed run
  (`DROP-CACHES` in `parity.log`); one warmup and five repeats,
  counterbalanced; every run idle-checked before and after and sampled once a
  second during; steal per cell and per run; the sightings discard rule; a
  cell at or above 0.25 MAD/median unusable.
- **The v0.22.0 baseline.** `grust` is the same commit as in B3 through B6.

## What is different from B6

- **The harness**, `fdf85a9` against `633ff36`: the `--precision` flag on the
  Grust participant behind the `pagerank-f32` feature, the `+f32` variant tag,
  `--families`, one bits group per base, the `not converged` verdict,
  `--plan b7`, `b7_report.py`, and `build.py`'s `--grust-commit` and
  `--grust-next-commit`. The B6 plan and its outputs are unchanged under
  `campaign.py`'s default.
- **The matrix.** PageRank alone; hub and uniform alone; participants
  `neo4j-graph`, `grust-next` counted and unchecked at f64 and at f32, and
  v0.22.0 at the pull kernel (`grust#1` at one thread, `grust` at full width).
  No pinned runs, no `+eager` row, no `grust#unset`: the push loop of v0.22.0
  is B6's most expensive cell and nothing in B7 is compared with it, and
  `b7_report.py estimate` over B6's bundle is the basis of that choice.
- **The work directory** is B6's, `~/src/b6-work`, so B6's reference cache
  was reused; every B7 output there carries a `b7-` prefix and no B6 file was
  written.

## Files

| file | what it is |
| --- | --- |
| `sources.json` | the four trees' commits and how each was staged, written by `build.py`. |
| `plan.json` | `campaign.py plan --plan b7` from the harness as built: parity configurations, participants, bits groups, families, and the six runs. |
| `fixtures-manifest.json` | the eight fixtures with node and edge count, bytes and SHA-256, checked identical to B6's. |
| `receipts/image.json`, `receipts/audit.json` | the image and the six binaries. |
| `parity/parity-b7-fixtures{,-large,-xlarge}-{unset,1,16}.json` | parity at `ead3568` before timing: every row, its iteration count, residual, `converged`, its vector against the reference, and the bits gate. |
| `timed/b7-*.json` | the six timed runs: every cell with its iteration count, residual, `converged` and precision, every raw sample. |
| `tables.md` | every cell of every run, the iteration counts side by side, and the parity rows, generated by `docker/simple-rust-algo-bench/b7_report.py tables`. |
| `campaign.jsonl` | the host-side record of every parity and timed invocation: idle checks before and after, steal, the watcher's sightings, resident sessions, exit code, status. |
| `campaign.log`, `parity.log`, `build.log` | the drivers' logs, with their start and end times. |

The B7 section of the results document is generated from this directory by
`b7_report.py section`, with the B6 bundle beside it read for the
unchanged-code comparison; every number in it is computed from these files
rather than transcribed. The introduction and the boundary paragraphs of that
section are written by hand and cite the commit's message and these files.

## Things in the record that look like failures, and things that do not

- **No parity invocation exited non-zero.** B6's did, on the protocol set's
  `neo4j-graph` dangling-mass rows; B7 excludes those families, and every one
  of its 144 PageRank rows agrees. No row is `not converged`.
- **No run was discarded and no run was rerun.** All six ran once, in plan
  order, on an idle host: 0 sightings over 6 timed invocations, steal 0 to 14
  ticks per run, 102 minutes from `CAMPAIGN-START` to `CAMPAIGN-END`. The one
  agent session resident on the host, a `codex` session asleep and using no
  CPU, is recorded by name in every snapshot. The driver was watched by one
  ssh loop reading its log once every fifteen minutes and nothing else was
  started on the host while a run was in progress.
- **The host's slower state since B5 persists.** B6 found every participant
  1.2 to 2.2 times slower above L3 than in B5 without a cause. B7's v0.22.0
  and `neo4j-graph` cells, unchanged code, sit within a few per cent of B6's
  on the same cells (the results section computes the ratio); the cause is
  still not established, and it is why no B7 cell is compared with a B5 cell.
- **The estimate.** `b7_report.py estimate` predicted 106 minutes of timed
  runs from B6's sample walls, taking each f32 row at its f64 row's wall; the
  runs took 102 minutes, the f32 rows running more iterations at less time
  per iteration than assumed.

## The B6 bundle

`b6-quegee/` was not modified. Its `fixtures-manifest.json` is what the B7
manifest was checked against, and its run files are read by `b7_report.py
section` for the unchanged-code comparison.
