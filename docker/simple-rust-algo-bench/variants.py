"""What a participant name on a command line means: a binary and how it is run.

A plain name is a binary run as B3 ran it. Two suffixes make a variant of it:

- `@mode` passes `--accounting mode` (`counted`, `work-uncounted`, `unchecked`).
  Only the Grust participants accept it; `grust` at v0.22.0 accepts `counted`
  alone and exits non-zero on anything else, so parity records an error rather
  than a mode that never ran.
- `#N` or `#unset` fixes this variant's `--concurrency`, overriding the run's.
  In Grust that selects a kernel, not a width: unset is PageRank's push loop and
  any number is the pull kernel. Letting a variant carry it puts both kernels in
  one counterbalanced run instead of two runs at different times.

The whole spec is the variant's key in every output, so a row always says which
binary, which mode and which kernel produced it. Parity keys drop the `#` part
and record concurrency as its own field, because parity runs one concurrency at
a time and a timed run looks each variant up under its own.
"""

MODES = ('counted', 'work-uncounted', 'unchecked')

def parse(spec, concurrency=None):
    base, marker, fixed = spec.partition('#')
    binary, _, mode = base.partition('@')
    if mode and mode not in MODES:
        raise SystemExit(f'{spec}: accounting mode must be one of {", ".join(MODES)}')
    if marker:
        concurrency = None if fixed == 'unset' else int(fixed)
    return dict(key=spec, parity_key=base, binary=binary, mode=mode or None,
                args=['--accounting', mode] if mode else [], concurrency=concurrency)
