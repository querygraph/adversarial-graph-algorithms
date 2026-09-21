# Rerun preparation — parity on quegee, 2026-09-21

Parity for the rerun, run before anything was timed, against a Grust commit
that is **not** the one the rerun will time. It is kept because the results
document's second correction to B3 cites it; the rerun reruns parity against
its final commit and publishes that alongside its timings.

| tree | commit |
| --- | --- |
| Grust, `grust` participant | `2182cdb` (v0.22.0) |
| Grust, `grust-next` participant | `44aa421` (`integration/0.23`, pre-merge) |
| Icecat | `57b443ec` |
| this repo | `dc40e4e` (see `sources.json`) |

Image `simple-rust-algo-bench:rerun-44aa421`, built on quegee. Fixtures are the
eight B3 fixtures, byte-identical to `b3-quegee/fixtures-manifest.json`.

| file | what it is |
| --- | --- |
| `parity-fixtures-unset.json`, `-1.json`, `-16.json` | 256 checks each: eight variants (`grust-next` in three accounting modes) × four algorithms × eight fixtures. 220 agree, 32 absent, 4 mismatch in each — the same four `neo4j-graph` dangling-mass rows as B3. Every PageRank row carries its maximum's bits against the reference; Grust rows carry the whole vector compared with the reference; `grust-next` rows carry `bits_identical_to` v0.22.0, true on 24 of 24 in each file. |
| `campaign.jsonl` | the host-side record of each parity invocation: idle before and after, steal, and the watcher's sightings. |

`campaign.jsonl` marks all three "failed" and records sightings. Both are the
harness's own bugs, fixed after this run and before any timing: parity exits 1
whenever any row mismatches, which the four known rows always do, and the
watcher matched this run's own `docker run` client, whose command line names
`parity.py`. One sighting in `parity-unset` is real: a resident `claude resume`
process on the host above a tenth of a CPU for one second. Parity is not timed;
a timed run with that sighting would be discarded.
