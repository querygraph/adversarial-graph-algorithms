"""What a participant name on a command line means: a binary and how it is run.

A plain name is a binary run as B3 ran it. Three suffixes make a variant of it:

- `@mode` passes `--accounting mode` (`counted`, `work-uncounted`, `unchecked`).
  Only the Grust participants accept it; `grust` at v0.22.0 accepts `counted`
  alone and exits non-zero on anything else, so parity records an error rather
  than a mode that never ran.
- `+tag` passes another flag that changes how the participant runs rather than
  what it computes. `+eager` is `--prepare-incoming always`, which is what B4
  did: build the transpose inside the build timer for every algorithm,
  including the three kernels that never read it. B5 prepares it only where it
  is read, so `+eager` is how B4's behaviour stays available as its own
  labelled row beside the corrected one.
- `#N` or `#unset` fixes this variant's `--concurrency`, overriding the run's.
  In Grust that selects a kernel, not a width: unset is PageRank's push loop and
  any number is the pull kernel. Letting a variant carry it puts both kernels in
  one counterbalanced run instead of two runs at different times.

The whole spec is the variant's key in every output, so a row always says which
binary, which mode, which preparation and which kernel produced it. Parity keys
drop the `#` part alone and record concurrency as its own field, because parity
runs one concurrency at a time and a timed run looks each variant up under its
own; `@mode` and `+tag` stay in the parity key, so a variant that is timed has
a parity row of its own rather than inheriting a neighbour's.

The allocator's configuration is deliberately not a suffix. `GLIBC_TUNABLES` is
set by `campaign.py` for a whole run and for every participant in it, because
pinning it for one participant and not another would compare two allocators.
"""

MODES = ('counted', 'work-uncounted', 'unchecked')
# tag -> the flags it adds. Timing conditions only, and each still runs parity.
TAGS = {'eager': ['--prepare-incoming', 'always']}

def parse(spec, concurrency=None):
    base, marker, fixed = spec.partition('#')
    head, *tags = base.split('+')
    binary, _, mode = head.partition('@')
    if mode and mode not in MODES:
        raise SystemExit(f'{spec}: accounting mode must be one of {", ".join(MODES)}')
    unknown = [tag for tag in tags if tag not in TAGS]
    if unknown:
        raise SystemExit(f'{spec}: unknown tag {", ".join(unknown)}; known tags: {", ".join(TAGS)}')
    if marker:
        concurrency = None if fixed == 'unset' else int(fixed)
    args = (['--accounting', mode] if mode else []) + [flag for tag in tags for flag in TAGS[tag]]
    return dict(key=spec, parity_key=base, binary=binary, mode=mode or None,
                tags=tags, args=args, concurrency=concurrency)
