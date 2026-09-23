# B9, the B7 plan on the head of the kernel stack — quegee, 2026-09-23

What produced these files, so a reader can tell what they are evidence of.

## Why there is a B9

B7 measured Grust's f32 PageRank at `ead3568` under B5's protocol, and B8 ran
the same plan at `2985fac`. B9 runs that same plan, unchanged, at the head of
the kernel branch stack, `4a9e7f5` on `work/narrow-offsets`. Over B8's
`2985fac` the stack adds four-byte CSR targets (`48598b4`), work charged one
reduction block at a time rather than one node (`eec1693`), PageRank's inner
loop without the ArticleRank term (`ca77603`), four-byte CSR row offsets
(`13b21d2`), and the non-finite test moved to the block (`4a9e7f5`). Every one
of those commits asserts bit-identical scores at both precisions and at every
width, and B9's parity checks that claim against v0.22.0 on this host before
anything is timed.

Nothing about the matrix changed: PageRank alone, hub and uniform alone, the
protocol, large and xlarge sizes, one thread and full width, parity first at
concurrency unset, 1 and 16, v0.22.0 as the anchor and `neo4j-graph` as the
reference participant.

## Provenance

| tree | commit | staged from |
| --- | --- | --- |
| Grust, `grust` participant | `2182cdb82acb` (v0.22.0) | `git archive v0.22.0` |
| Grust, `grust-next` participant | `4a9e7f5eab7724c6fb0e7714032386bdfb98ae89` (`work/narrow-offsets`) | `git archive 4a9e7f5` |
| Icecat | `57b443ec1d16` | working tree, clean |
| this repo, as built into the image | `cea69ee0b2ce` (`work/bench-b9`) | working tree, clean |

All of this is in `sources.json`, written by `build.py` when it staged the
image; the two Grust trees were archived from the named commits rather than
hardlinked from checkouts, so no working-tree state could reach them.
`receipts/image.json` is the image, `simple-rust-algo-bench:b9-4a9e7f5`, built
on quegee under a 20 GB memory cap with four jobs (`systemd-run --user --scope
-p MemoryMax=20G -p MemorySwapMax=0`, `--jobs 4`; `build.log`), and not
rebuilt afterwards: every parity and timed invocation in `campaign.jsonl`
names that tag. `receipts/audit.json` has each of the six binaries' receipt
and SHA-256, and they are six distinct binaries. The audit, the image receipt,
the manifest and `plan.json` were taken before parity began, not during a run.

Grust `4a9e7f5` passed `scripts/ci-local.sh` on both platforms before the
image was built: `ci-local: PASSED every gate at 4a9e7f5 on Linux x86_64 in
2412s` and `ci-local: PASSED every gate at 4a9e7f5 on Darwin x86_64 in 2704s`.

Host: quegee, 16 vCPU on 8 physical cores, 24.8 MB L3, not burstable.

## Where the receipt and the manifest came from

`b9-postbuild.sh` on the host calls `b8-postbuild.py`, which writes the image
receipt and the fixture manifest to paths whose `b8-` prefix is hard-coded.
Running it for B9 therefore wrote B9's image receipt over
`b6-work/b8-receipts/image.json` and B9's manifest over
`b6-work/b8-fixtures-manifest.json`, and left `b6-work/b9-receipts/` holding
only `audit.json`. The two files in this bundle are those B9 writes, copied
from the `b8-` paths they landed in and named for this bundle; the image
receipt in `receipts/image.json` names `simple-rust-algo-bench:b9-4a9e7f5`,
which is the tag every invocation in `campaign.jsonl` ran, and the manifest's
SHA-256s are checked in it against `b6-quegee/fixtures-manifest.json`. The
manifest's `note` field still says "B7" because `b8-postbuild.py` carries B7's
wording; the fixtures it describes are the same eight files in all three
campaigns, and `b7-fixtures-manifest.json` and the file written here are byte
for byte the same. What was lost is B8's own image receipt, which this write
overwrote; it was read back from the `simple-rust-algo-bench:b8-2985fac` image,
still present on the host, and kept with the rest of B8's unbundled outputs.
A campaign that reuses these scripts should parameterise that prefix first.

## What did not change since B7

- **The fixtures.** The same eight hub and uniform files, read from the same
  work directory; `fixtures-manifest.json` records every SHA-256 and byte
  count checked against `b6-quegee/fixtures-manifest.json`
  (`identical_to_b6`).
- **The protocol.** Parity first, every fixture set at concurrency unset, 1
  and 16; the page cache dropped after parity and before the first timed run;
  one warmup and five repeats, counterbalanced; every run idle-checked before
  and after and sampled once a second during; steal per cell and per run; the
  sightings discard rule; a cell at or above 0.25 MAD/median unusable.
- **The v0.22.0 baseline.** `grust` is the same commit as in B3 through B8.
- **The harness plan.** `campaign.py plan --plan b9` is B7's plan with the
  `b9-` prefix; `plan.json` is what the image was driven with.

## What is different

- **The commit under test**, `4a9e7f5` against B7's `ead3568`, with B8's
  `2985fac` between them.
- **The generator.** `b7_report.py` gains `--campaign b9`, and with it three
  subsections computed from this bundle: one sweep of
  `grust-next@unchecked+f32` against one sweep of `neo4j-graph`; what work
  accounting costs per sweep here and in B7; and the unchanged-code table that
  says why no B9 time is compared with a B7 or B8 time.
- **What is not in the section.** B8 ran on this host between B7 and B9 and
  was never bundled, so there is no `b8-quegee/` for the generator's
  campaign-to-campaign tables to read, and it prints none.

## Files

| file | what it is |
| --- | --- |
| `sources.json` | the four trees' commits and how each was staged, written by `build.py`. |
| `plan.json` | `campaign.py plan --plan b9` from the harness as built: parity configurations, participants, bits groups, families, and the six runs. |
| `fixtures-manifest.json` | the eight fixtures with node and edge count, bytes and SHA-256, checked identical to B6's. |
| `receipts/image.json`, `receipts/audit.json` | the image and the six binaries. |
| `parity/parity-b9-fixtures{,-large,-xlarge}-{unset,1,16}.json` | parity at `4a9e7f5` before timing: every row, its iteration count, residual, `converged`, its vector against the reference, and the bits gate. |
| `timed/b9-*.json` | the six timed runs: every cell with its iteration count, residual, `converged` and precision, every raw sample. |
| `tables.md` | every cell of every run, the iteration counts side by side, and the parity rows, generated by `docker/simple-rust-algo-bench/b7_report.py --campaign b9 tables`. |
| `campaign.jsonl` | the host-side record of every parity and timed invocation: idle checks before and after, steal, the watcher's sightings, resident sessions, exit code, status. |
| `campaign.log`, `build.log` | the drivers' logs, with their start and end times. |

The B9 section of the results document is generated from this directory by
`b7_report.py --campaign b9 section`, with the B7 bundle beside it read for the
two figures that are formed inside each campaign separately; every number in it
is computed from these files rather than transcribed. The introduction and the
boundary paragraphs of that section are written by hand and cite the commits'
messages and these files.

## Things in the record that look like failures, and things that do not

- **No parity invocation exited non-zero.** All nine are `clean` with exit 0,
  and all 144 PageRank rows are `agrees`. No row is `not converged`. The 48
  f64 rows are bit-identical to v0.22.0's vectors and the 24 `+f32` unchecked
  rows are bit-identical to their counted rows, at every concurrency and every
  size.
- **No run was discarded and no run was rerun.** All six ran once, in plan
  order, on an idle host: 0 sightings over 6 timed invocations, steal 0 to 10
  ticks per run, 79 minutes of timed runs and 25 of parity: `PARITY-START`
  2026-09-23T15:05:46Z, `CAMPAIGN-START` 2026-09-23T15:30:57Z, `CAMPAIGN-END`
  2026-09-23T16:49:49Z. No agent
  session was resident on the host during any invocation; every snapshot in
  `campaign.jsonl` records an empty list, where B7's recorded a sleeping
  `codex` session by name.
- **No cell is unusable.** 240 PageRank cells, 0 at or above the 0.25
  MAD/median threshold; the largest dispersion is 0.144, `neo4j-graph` on
  `hub-4194304` in `xlarge-full-width`.
- **The push kernel's work accounting got more expensive**, not less. The
  results section prints the cells. The block-at-a-time change is in the
  pull kernel's reduction, and the push loop pays the meter per node still;
  nothing here explains why its figure moved the way it did, and the section
  does not claim to.
- **The host is not the host B7 measured.** It was restarted between the
  campaigns, and the unchanged participants' per-sweep figures moved by cell
  and in both directions — `neo4j-graph` from 0.644 to 1.203 of its B7 figure.
  No B9 absolute is compared with a B7 or B8 absolute anywhere, and the table
  that shows this is in the section for that purpose.

## The B7 bundle

`b7-quegee/` was not modified. Its run files are read by `b7_report.py
--campaign b9 section` for the two figures each campaign forms inside itself,
and its `fixtures-manifest.json` is byte-identical to this one.
