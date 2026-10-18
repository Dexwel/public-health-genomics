#!/usr/bin/env bash
# capstone_check.sh - tells you which weeks' key results you have reproduced (Week 12).
# Run from the repository root:  bash scripts/capstone_check.sh
# It only READS your results/ folder; nothing is changed. A missing week is reported as SKIP, not as a failure.
ok=0; bad=0; skip=0
say() { printf "%-6s %s\n" "$1" "$2"; }
check() {  # check <label> <file> <test command...>   (test runs only if the file exists)
  local label="$1" file="$2"; shift 2
  if [ ! -e "$file" ]; then say SKIP "$label (missing $file)"; skip=$((skip+1)); return; fi
  if "$@"; then say PASS "$label"; ok=$((ok+1)); else say FAIL "$label"; bad=$((bad+1)); fi
}
nrows() { awk 'END{print NR-1}' "$1"; }

{   # errors from checks on missing files are expected; the SKIP lines say it better
check "W3 clean line list has 600 rows"             results/week03/linelist_clean.csv   test "$(nrows results/week03/linelist_clean.csv 2>/dev/null)" = 600
check "W4 PCA file has 1000 people"                 results/week04/pca.eigenvec         test "$(wc -l < results/week04/pca.eigenvec 2>/dev/null)" = 1000
check "W5 fastp report for sample C exists"         results/week05/trim/sC.json         grep -q '"total_reads"' results/week05/trim/sC.json
check "W6 sample A VCF has 6 variants"              results/week06/sA.vcf               test "$(grep -vc '^#' results/week06/sA.vcf 2>/dev/null)" = 6
check "W6 sample B VCF has 5 variants"              results/week06/sB.vcf               test "$(grep -vc '^#' results/week06/sB.vcf 2>/dev/null)" = 5
check "W7 annotated VCF has a stop_gained call"     results/week07/sB.csq.vcf           grep -q 'stop_gained' results/week07/sB.csq.vcf
check "W8 QC leaves 975 people"                     results/week08/qc.fam               test "$(wc -l < results/week08/qc.fam 2>/dev/null)" = 975
check "W8 top hit is ts06_067"                      results/week08/adj.assoc.logistic   test "$(awk 'NR>1&&$5=="ADD"&&$9!="NA"{print $9,$2}' results/week08/adj.assoc.logistic 2>/dev/null | sort -g | head -1 | cut -d' ' -f2)" = ts06_067
check "W9 scores exist for 7 thresholds"            results/week09/prs.T7.profile       test "$(ls results/week09/prs.T?.profile 2>/dev/null | wc -l)" = 7
check "W10 5-SNP clusters of 30, 15 and 8"          results/week10/clusters_5snp.tsv    test "$(awk 'NR>1{print $2}' results/week10/clusters_5snp.tsv | sort | uniq -c | awk '$1>=5{print $1}' | sort -n | tr '\n' ' ')" = "8 15 30 "
check "W11 re-identification script saved"         results/week11/reidentification_risk.R test -s results/week11/reidentification_risk.R
} 2>/dev/null
echo
echo "Summary: $ok passed, $bad failed, $skip skipped"
[ "$bad" -eq 0 ]
