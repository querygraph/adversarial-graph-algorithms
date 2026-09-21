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
| `parity-fixtures-large-*.json`, `parity-fixtures-xlarge-*.json` | PageRank only, on `hub` and `uniform` at 2,097,152 and 4,194,304 nodes, at each concurrency: 16 of 16 agree in every file, `grust-next` bit-identical to v0.22.0 on 6 of 6. Built by image `rerun-44aa421` at harness `483dc86`. |
| `campaign.jsonl` | the host-side record of each parity invocation: idle before and after, steal, and the watcher's sightings. |

`campaign.jsonl` marks all three "failed" and records sightings. Both are the
harness's own bugs, fixed after this run and before any timing: parity exits 1
whenever any row mismatches, which the four known rows always do, and the
watcher matched this run's own `docker run` client, whose command line names
`parity.py`. One sighting in `parity-unset` is real: a resident `claude resume`
process on the host above a tenth of a CPU for one second. Parity is not timed;
a timed run with that sighting would be discarded.

The large-size invocations are marked `DISCARDED: host shared`. Every sighting
in them is that same resident `claude resume` process, above a tenth of a CPU
in about one sample in twenty, at up to 63% of a CPU. Parity verdicts do not
depend on sharing; timings would, and this is why no timed run has been made.
