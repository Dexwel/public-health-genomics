#!/usr/bin/env bash
# check_setup.sh - confirm the course tools are installed and the data are intact.
# Run from the repository root:  bash scripts/check_setup.sh
set -uo pipefail
ok=0; bad=0
check() {  # check <label> <command...>
  local label="$1"; shift
  if "$@" >/dev/null 2>&1; then printf '  [ ok ] %s\n' "$label"; ok=$((ok+1));
  else printf '  [FAIL] %s\n' "$label"; bad=$((bad+1)); fi
}
echo "Tools"
check "bash"            bash --version
check "git"             git --version
check "python3"         python3 --version
check "R"               R --version
check "Rscript"         Rscript --version
check "R: ggplot2/dplyr/readr/tidyr/ape" Rscript -e 'for (p in c("ggplot2","dplyr","readr","tidyr","ape")) library(p, character.only=TRUE)'
if command -v plink >/dev/null 2>&1; then check "plink (1.9)" plink --version
else check "plink1.9 (alias it: ln -s \$(which plink1.9) ~/bin/plink)" plink1.9 --version; fi
check "samtools"        samtools --version
check "bcftools"        bcftools --version
check "bgzip/tabix"     bgzip --version
check "bwa"             bash -c 'bwa 2>&1 | grep -q Version'
check "fastp"           fastp --version
check "fastqc"          fastqc --version
check "seqtk"           bash -c 'seqtk 2>&1 | grep -q Version'
echo
echo "Data (run from the repo root)"
if [ -f data/CHECKSUMS.sha256 ]; then
  if sha256sum --quiet -c data/CHECKSUMS.sha256 2>/dev/null; then echo "  [ ok ] all data files match data/CHECKSUMS.sha256"; ok=$((ok+1));
  else echo "  [FAIL] data files differ from data/CHECKSUMS.sha256 (regenerate with: python scripts/make_toy_data.py)"; bad=$((bad+1)); fi
else
  echo "  [skip] data/CHECKSUMS.sha256 not found"
fi
echo
echo "Summary: $ok ok, $bad failed"
[ "$bad" -eq 0 ] && echo "You are ready for Week 1." || echo "Fix the failed items (see start-here/setup.md) before the labs."
exit "$bad"
