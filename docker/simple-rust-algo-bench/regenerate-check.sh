#!/bin/sh
# Every generated table in the evidence bundles and in the results document
# must come back byte for byte from the bundle it claims to be computed from.
# Run from the repository root; it writes nothing into the tree.
#
#   docker/simple-rust-algo-bench/regenerate-check.sh
#
# It regenerates each campaign's tables.md and each campaign's results section
# and `cmp`s them against what is committed. The section is the slice of
# docs/simple-rust-algo-bench-results.md from "## <C>: results" up to the
# hand-written "### The boundary" heading that follows it; the introduction and
# the boundary paragraphs are written by hand and are not checked here.
set -e
ROOT=$(git rev-parse --show-toplevel)
cd "$ROOT"
DOC=docs/simple-rust-algo-bench-results.md
EV=docs/simple-rust-algo-bench-evidence
GEN=docker/simple-rust-algo-bench/b7_report.py
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

slice() {   # slice CAMPAIGN -> the committed results section for that campaign
  awk -v start="## $(printf '%s' "$1" | tr 'a-z' 'A-Z'): results" '
    $0 == start { on = 1 }
    on && /^### The boundary/ { exit }
    on { print }
  ' "$DOC"
}

status=0
for c in b7 b9; do
  python3 "$GEN" --campaign "$c" tables "$EV/$c-quegee" > "$TMP/$c-tables.md"
  if cmp -s "$TMP/$c-tables.md" "$EV/$c-quegee/tables.md"; then
    echo "regenerate-check: $c tables.md byte-identical"
  else
    echo "regenerate-check: $c tables.md DIFFERS from $EV/$c-quegee/tables.md"
    status=1
  fi
  python3 "$GEN" --campaign "$c" section "$EV/$c-quegee" > "$TMP/$c-section.md"
  slice "$c" > "$TMP/$c-committed.md"
  # The committed slice carries the blank line that separates it from the
  # boundary heading; the generator's output ends without it.
  printf '\n' >> "$TMP/$c-section.md"
  if cmp -s "$TMP/$c-section.md" "$TMP/$c-committed.md"; then
    echo "regenerate-check: $c results section byte-identical"
  else
    echo "regenerate-check: $c results section DIFFERS from $DOC"
    diff "$TMP/$c-committed.md" "$TMP/$c-section.md" | head -40 || true
    status=1
  fi
done
[ "$status" -eq 0 ] && echo "regenerate-check: PASSED, every generated table came back from its bundle"
exit "$status"
