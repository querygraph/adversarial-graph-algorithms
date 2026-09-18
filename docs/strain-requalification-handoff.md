# Strain re-qualification on the lock-free work meter

Prepared 2026-09-18 on host `grust`. The strain benchmark runs on `quegee`; this
document asks for a decision and, if taken, a re-measurement there. Nothing in
the strain repository has been changed from here.

## What changed and why it may matter to strain

Grust commit `23de753` on branch `work/algorithms-performance`, forked from
`3a739544c3d9e6581bdac7563d8cc3a66cdcf828`, removes the execution mutex from the
cooperative work meter. `ExecutionContext::charge_work` now holds `work_units`
and `cancelled` as atomics and admits each charge through a compare-exchange
that recomputes admission against the value it replaces. Budgets are still
enforced exactly, granularity is still per unit, and cancellation is published
before wakers are collected, so no caller observes a behavioral difference.
Memory reservations, peak accounting and wakers keep the lock.

The algorithms benchmark found this by profiling, not by guessing: on a
16384-node weighted chain with full path reconstruction, 72.8% of kernel self
time was `charge_work`, against 14.8% for visiting paths and 6.6% for advancing
path buffers. The meter is called once per visited entry and once per
reconstructed path step, which is roughly 134 million times in that case.

Strain never calls `charge_work` itself. It reaches the meter through
`grust-cypher`, which charges in `read_budget.rs`, `read_budget_live.rs` and
`read/streaming_fusion.rs`. Strain's **Cypher read** arms therefore execute the
patched code; its durable write and loading arms mostly do not. Whether the
change is visible at strain's call frequency is unknown and unmeasured: the
algorithms case charges per graph entry, while a row-oriented read charges far
less often per unit of wall time. Do not assume the algorithms speedup transfers.

## Cheap decision first

Before committing to a re-measurement, measure one Cypher-read arm on both
binaries on `quegee`, same dataset and envelope, alternating order, with the
usual warmups and at least five measured samples. If the medians do not separate
beyond their dispersion, record that and stop; the current strain results stand
and need no re-run. This costs one arm, not a campaign.

## If the change is visible

Strain pins Grust by revision in `Cargo.toml`: `grust`, `grust-helix`,
`grust-ladybug`, `grust-cypher` and `grust-postgres-core` all read
`rev = "a04ebd7578c7ab87d29d31575e12db1193b1e9b1"`. That pin is code-identical to
this patch's base: every commit between `3a73954` and `a04ebd7` changes only
`docs/book/chapters/turso-under-strain.md`. Moving all five to the patched
commit is therefore a pure meter change, with no other source difference.

Re-measurement scope, stated honestly: every arm that shares a results table
with a moved number needs the same binary, not only the arms expected to move.
Write and loading arms are not expected to change, but they cannot be pooled
with new read numbers while they were produced by the old binary. Keep the old
results as their own pinned set, publish the new set beside them, and do not
restate one as the other.

## Sequencing

Measure one host at a time. This host finished its own overnight pipeline of
completion tests and a paired before/after comparison of the same patch, so its
results are available as prior evidence but must not be pooled with strain's:
different host, different workload, different envelope.

If a strain re-run is approved, run it while `grust` is idle, or accept and
disclose that the two hosts were busy concurrently. Do not start a strain
campaign and an algorithms campaign at the same time on the same machine.

## Commands

```sh
git -C ~/src/grust fetch origin work/algorithms-performance
# Point strain's five Grust dependencies at the patched commit:
#   rev = "23de753..."   (full sha from the fetched branch)
# then rebuild and measure exactly as the strain protocol specifies.
```

Record in the strain evidence: the Grust commit, that this is the lock-free work
meter, the unchanged budget and cancellation semantics, and which arms were
re-measured against which prior set.
