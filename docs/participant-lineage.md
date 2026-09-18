# Participant lineage

Every column in this benchmark descends from something. This document records
that chain, how it is verified, and the rules that keep it verifiable. It is a
proposal for the tracking scheme plus the provenance recovered so far.

## The chain

```
NetworKit (upstream C++)
  └── Icebug        querygraph/icecat        C++/Arrow update of NetworKit
        └── Icecat  querygraph/icecat        Rust/Arrow rewrite (icebug-core, -algorithms, -io)
              └── Grustcat        querygraph/icecat   adapts the Rust kernels to the Grust API
              └── Grustcat Cypher querygraph/icecat   adds a parser and typed Arrow backend
                    ⇢ targets Grust        querygraph/grust
Grust (current)
  └── direct, ordinary Cypher, Arrow, DataFusion, Turso snapshot
        querygraph/grust, crates/grust-algorithm-procedures/examples
```

Two properties of that layout are deliberate and should stay.

Icebug, Icecat, Grustcat and Grustcat Cypher all live in `querygraph/icecat`,
and the two Grustcat crates are excluded from that repository's Cargo workspace
(`exclude = ["crates/grustcat", "crates/grustcat-cypher"]`) because they answer
to Grust's dependency graph rather than to Icebug's. The current participants
live in `querygraph/grust` as examples of `grust-algorithm-procedures`.

**Frozen sources live in `icecat`; moving sources live in `grust`.** A published
measurement's inputs must not sit on a branch under release rotation, so the
historical participants are not moved into Grust, and the current participants
are not copied into the benchmark.

## Recovered provenance of the published snapshot

`publication/measured-source.tar.gz` is checksum-verified against
`publication/source.json` before every frozen run, but that receipt records only
`archive`, `sha256`, `description` and `licenses` — it proves the bytes have not
changed and says nothing about where they came from. The origins below were
recovered by hashing every staged file against repository history.

| Staged tree | Commit | Verification |
|---|---|---|
| `grust/` | `62b8b0fa2b12ec84ee02b5296969efeaf0367a58` (2026-09-13) | 303 of 303 files match exactly |
| `icecat/` | `3cbc07a510c0bf1803f83a10776d40d0e6f556ba` (2026-09-13) | 1,085 of 1,087 tracked files match |

Two files in the Icecat tree — `rust/README.md` and
`rust/crates/grustcat-cypher/README.md` — match **no commit in the repository**,
so that tree was staged from a working directory with uncommitted edits. A
further 601 files under `extlibs/` are submodule contents and are not in the
commit tree at all.

This is a provenance gap, not a correctness one: the measured bytes are fixed
and verified, the two files are documentation, and no participant's behaviour
depends on them. It is recorded because an unrecorded gap becomes an unanswerable
question later, and because it is precisely what the rules below prevent.

## The scheme

### 1. Each component declares its parents in-tree

A `lineage.json` beside each component, identical in shape everywhere:

```json
{
  "component": "grustcat",
  "role": "adapts the Icecat Rust kernels to the Grust API",
  "derives_from": [
    {"component": "icecat", "repo": "querygraph/icecat", "commit": "…", "relation": "kernels"},
    {"component": "grust", "repo": "querygraph/grust", "commit": "…", "relation": "api"}
  ],
  "license": "MIT"
}
```

Icebug names its NetworKit fork point; Icecat names the Icebug revision it
reimplements; Grustcat names both the Icecat kernels it wraps and the Grust
revision it targets; the current participants name Grust alone. Walking the
files reconstructs the chain without anyone remembering it.

### 2. One participant manifest in this repository

`docker/upstream-pins.json` already pins the moving sources and is read by the
runner. It gains the frozen participants, so a single file answers "what
produced this column": role, repository, commit, archive checksum, license, and
whether the entry is frozen.

`docker/prepare.py` continues to verify the archive checksum, and records the
named commits into each run receipt so a result carries its own provenance.

### 3. Frozen entries never change

Changing a frozen entry is a new publication, not an update. If a historical
participant must be rebuilt differently, it gets a new pin, a new archive and a
new result set, and the old one stays where it is.

### 4. Stage from a committed tree, and record dirt when it exists

Nothing may be staged from a working directory whose tracked files differ from
its commit without recording that fact. The current-source runner already does
this for Grust and Turso — the build receipt carries `upstream_status` and
`upstream_diff`, and an explicitly supplied checkout is recorded as unpinned.
The frozen path did not, which is how the two READMEs above went unnoticed.

### 5. Tag the commits

`git tag algorithms-benchmark-2026-09-13` in `icecat` and `grust` at the two
commits above, so provenance resolves by name rather than by a hash recovered
from a tarball.

## On publishing crates

The Rust components are already crates; the question is only whether they go to
crates.io.

`icebug-core`, `icebug-algorithms` and `icebug-io` would gain immutable,
checksummed, archived versions — genuinely useful for reproduction — at the cost
of release obligations and an API-stability expectation for code whose purpose is
to be a frozen benchmark participant. The git tag and the existing archive
checksum already deliver the immutability the benchmark needs, so publish these
only if the kernels are meant to be depended on, which is a product decision
rather than a provenance one.

`grustcat` and `grustcat-cypher` should not be published. They are adapters
pinned to one Grust revision, they are excluded from their own workspace for that
reason, and publishing them would imply support for a compatibility shim.
