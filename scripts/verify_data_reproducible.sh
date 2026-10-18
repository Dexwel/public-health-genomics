#!/usr/bin/env bash
# verify_data_reproducible.sh - regenerate the toy data in a temp folder and check that it matches
# data/CHECKSUMS.sha256 (and that the committed data match too).
#
#   bash scripts/verify_data_reproducible.sh            # check
#   bash scripts/verify_data_reproducible.sh --write    # rewrite data/CHECKSUMS.sha256 after an intentional data change
#
# Run from the repository root. Only files created by scripts/make_toy_data.py are listed
# (docs such as data/README.md and the instructor-only .npz, which embeds timestamps, are excluded).
set -euo pipefail
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
python3 scripts/make_toy_data.py --out "$tmp/data" >/dev/null
regen=$(cd "$tmp" && find data -type f ! -name '_hidden_effects.npz' -print0 | LC_ALL=C sort -z | xargs -0 sha256sum)
if [ "${1:-}" == "--write" ]; then
  echo "$regen" > data/CHECKSUMS.sha256
  echo "Wrote data/CHECKSUMS.sha256 ($(echo "$regen" | wc -l) files)."
  exit 0
fi
expected=$(cat data/CHECKSUMS.sha256)
if [ "$regen" == "$expected" ]; then
  echo "OK: regenerated data are byte-identical to data/CHECKSUMS.sha256 ($(echo "$expected" | wc -l) files)."
else
  echo "MISMATCH between regenerated data and data/CHECKSUMS.sha256:"
  diff <(echo "$expected") <(echo "$regen") | head -20
  exit 1
fi
if sha256sum --quiet -c data/CHECKSUMS.sha256; then echo "OK: the files in data/ match the checksums."; else echo "The files in data/ differ from the checksums (re-run: python3 scripts/make_toy_data.py)."; exit 1; fi
