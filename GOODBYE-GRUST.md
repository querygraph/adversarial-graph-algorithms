# Decommissioning host `grust`: what to carry to quegee and what to let go

Written 2026-09-22, before shutdown. `grust` is an 8-vCPU t2-class instance
(Xeon E5-2686 v4, 31 GB RAM, 985 GB disk at 95% full) that served as the
algorithms benchmark's build-and-verify host. It never published a timing:
1.889% lifetime hypervisor steal against quegee's 0.00045% is why.

**Nothing on this box is unpushed.** `git log --branches --not --remotes` is
empty in every repository. Nothing is running: no background jobs, no user
crontab, no containers. What is at risk is not code — it is two evidence
archives that exist here and nowhere else.

## 1. The two archives, and why only a slice of each matters

| archive | total | irreplaceable core | the rest |
| --- | ---: | ---: | --- |
| `adversarial-graph-algorithms/.measurements` | 29 GB | **180 MB** | `context/` + `frozen-context/` (~18 GB) are staged sources, regenerable from `docker/upstream-pins.json` and each run's preserved `upstream-Cargo.lock`; `variants/` is 10 GB of exported binaries |
| `adversarial-graph/reports` | 24 GB | **6.4 MB** | `work/` is datasets and databases |

`.measurements` is **git-ignored** (`.gitignore:1`) and `reports/` is untracked,
so neither is in any remote. 41 algorithm runs and 139 strain runs.

The cores are the receipts, resolve logs, dependency locks, sample files,
per-run `results/` directories and `historical-binary-parity.json` — everything
a published number is accountable to.

## 2. Packaged and ready to copy

Both cores are already archived on this box:

```
/home/admin/migration/algorithms-measurements-core.tgz    29 MB    923 files
/home/admin/migration/strain-reports-core.tgz           397 KB    255 files

SHA256SUMS (alongside them, so the check below is executable rather than
something to retype):

34ca6245e7c77bd5afe06f702717f96d3d991ad42b8da094971a748bafbfe09a  algorithms-measurements-core.tgz
1156d9f502af9cac305443d4a53ae016485ea87fc7630403ac6d0cc289fc10b5  strain-reports-core.tgz
```

Built with, respectively:

```
tar czf algorithms-measurements-core.tgz \
    --exclude='*/context' --exclude='*/frozen-context' --exclude='variants' .measurements
find reports \( -name '*.json' -o -name '*.md' -o -name '*.jsonl' \
                -o -name '*.csv' -o -name '*.log' \) -print0 | tar czf strain-reports-core.tgz --null -T -
```

### Steps

1. **Copy both files to quegee and verify the digests there**, not here — a
   digest checked only on the source proves the archive was written, not that it
   arrived.
   ```
   scp /home/admin/migration/*.tgz /home/admin/migration/SHA256SUMS quegee:~/migration/
   ssh quegee 'cd ~/migration && sha256sum -c SHA256SUMS'
   ```
2. **Unpack in place** so paths match what the documents cite:
   ```
   ssh quegee 'cd ~/src/adversarial-graph-algorithms && tar xzf ~/migration/algorithms-measurements-core.tgz'
   ssh quegee 'cd ~/src/adversarial-graph            && tar xzf ~/migration/strain-reports-core.tgz'
   ```
3. **Confirm the run count survived**: `ls .measurements | wc -l` should print 41,
   `ls reports | wc -l` should print 139. A short count means a partial transfer,
   which is silent otherwise.

**Do not shut this machine down until step 3 has passed on quegee.**

## 3. The one open decision: `variants/`, 10 GB

`.measurements/variants/` holds the exported participant binaries — six
executables and two receipts per variant, nine variants.

- Their **sha256 digests are already recorded** in each run's
  `build-receipt.json` and `sources.json`, which is what
  `historical-binary-parity.json` asserts against. That claim survives without
  the bytes.
- The bytes **cannot be reproduced exactly**. Staging runs
  `cargo update --workspace` when no `--lockfile` is passed, so a rebuild
  resolves its own dependency versions. A future re-verification of
  byte-identity needs these files or it needs nothing.

**Recommendation: let them go**, and record their absence rather than leave a
reader to discover it — a line in `docs/optimization-results.md` saying the
historical binaries were retired with host `grust` and their digests stand in
their place. If anyone wants re-verifiability instead, it is a 10 GB copy and
this document is wrong about it; say so before the instance stops.

## 4. What to reconstruct on quegee, and in what order

Nothing is in flight. B1, B2 and B3 are complete and their artifacts are in git
(PR #1 on this repository). For a working benchmark host:

1. `git clone git@github.com:querygraph/adversarial-graph-algorithms.git`
2. `git clone https://github.com/querygraph/grust.git`
3. `git clone git@github.com:querygraph/icecat.git && cd icecat && git submodule update --init --recursive`
   — **`extlibs/tlx` and `extlibs/ttmath` are mandatory.** `docker/prepare.py` and
   `docker/simple-rust-algo-bench/build.py` both refuse to stage without them,
   which is deliberate: the failure otherwise arrives ten minutes later inside a
   container as a CMake error that reads like a CMake problem.
4. `git clone https://github.com/tursodatabase/turso.git` for the database columns.
5. The clones must sit as **siblings under one directory**. Participant manifests
   name their projects by relative path (`../../../../grust/crates/...`), and the
   image reproduces that layout rather than rewriting them: a participant whose
   dependency edges the harness edited is not the participant.

Restore `.measurements` from the tarball only if past runs need to be cited; new
runs write there regardless.

## 5. What to delete without ceremony

- **Docker**: 83 images, 175 GB of volumes, 83 GB of build cache. All
  regenerable. This is where the disk went.
- **`grust-0722-probe`, `grust-main-probe`, `grust-gate`, `grust-0722-*`, and the
  other worktrees**: their only untracked file, `crates/grust-turso/tests/dangling_edges.rs`,
  is **already in grust main**. Superseded.
- **`adversarial-graph`** scratch: `Cargo.toml.bak-1909`, `Cargo.toml.pre-main`,
  `build-*.log`, `probe-pg-A/`.
- **`eigentimes`** untracked `fit-hn4/`, `shard/` — check with whoever ran them if
  they are not reproducible; they are not this benchmark's.
- Session scratchpads under `/tmp/claude-*`.

## 6. What changes about the work once it lives on quegee

Several rules in this harness exist only because **this** box is burstable. They
should not be carried across as though they were properties of the code:

- **The one-hour rule** — no sweep within an hour of a saturating gate — is a
  statement about a t2 credit balance. quegee is a c5n and has none; it was
  withdrawn there and replaced with a concurrency rule: the host stays quiet for
  the *duration* of a sweep, because counterbalancing cancels a monotone drift
  and cannot cancel a step change.
- **"Shared-host, not portable"** labelling on absolute timings stops applying.
  quegee's are publishable, with steal read as an interval across the run rather
  than as a lifetime counter.
- **Cache-residency statements name their host.** This box has 45 MiB of L3 and
  quegee 24.8 MB; "the working set fits" is a fact about a machine, like steal.

The measurement rules that are *not* about this box travel unchanged: parity
gates timing, a label follows its SHA, a sub-5% single-cell move is not
attributed to a diff without a layout control, and the instrument records its own
commit and working-tree state in every receipt.

## 7. Final check before the instance stops

```
git -C ~/src/adversarial-graph-algorithms log --branches --not --remotes   # empty
git -C ~/src/grust                        log --branches --not --remotes   # empty
git -C ~/src/adversarial-graph            log --branches --not --remotes   # empty
git -C ~/src/icecat                       log --branches --not --remotes   # empty
ssh quegee 'ls ~/src/adversarial-graph-algorithms/.measurements | wc -l'   # 41
ssh quegee 'ls ~/src/adversarial-graph/reports | wc -l'                    # 139
```

Two of those are on the other machine on purpose. The archives are the only
thing here that a rebuild cannot produce.
