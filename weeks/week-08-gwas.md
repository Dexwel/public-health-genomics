---
description: Run a genome-wide association study end to end - sample and SNP quality control, ancestry correction, logistic regression, Manhattan and QQ plots - and learn why most GWAS failures are confounding, not statistics.
---

# Week 8 — Genome-wide association studies

{% hint style="info" %}
**At a glance** · **Time:** ~8-10 h (the longest lab) · **Prerequisites:** Weeks 3-4 (R, PLINK, PCA) · **You will produce:** a QC log, a cleaned PLINK dataset, naive and adjusted association results, Manhattan and QQ plots, and a results paragraph · **Tools:** PLINK 1.9, R · **Data:** `data/gwas` (1,000 people, 500 cases and 500 controls, 3,160 SNPs)
{% endhint %}

{% tabs %}

{% tab title="1 · Start here" %}

## Why this matters

A genome-wide association study (GWAS) tests many variants for a statistical link with a disease or trait. GWAS have found thousands of associations and underpin polygenic scores (Week 9), drug-target discovery and risk stratification. They are also easy to get wrong: poor quality control, hidden relatives, mixed ancestries and multiple testing generate convincing but false results. In public health the cost of a false association is wasted programmes and unfounded risk labels for communities.

This week you run a GWAS on a synthetic cohort in which the answer is known: one strong causal SNP, one weaker one, a built-in ancestry confounder, and 85 planted data problems. You will find them, correct for them, and check your result against the truth.

## Learning objectives

By the end of this week you will be able to:

1. **Explain** the logic of a GWAS: case-control logistic regression, one SNP at a time.
2. **Perform** sample QC (missingness, sex check, relatedness, ancestry outliers) and SNP QC (missingness, MAF, HWE) and **justify** each threshold.
3. **Correct** for population structure with principal components and covariates.
4. **Compute and interpret** genomic inflation (λ), a Manhattan plot and a QQ plot.
5. **Apply** multiple-testing thresholds (5×10⁻⁸ and Bonferroni) and **explain** the difference.
6. **Describe** LD clumping and why a signal is a region, not a variant.
7. **Report** a GWAS result honestly: effect size, uncertainty, limits, replication.

## Roadmap

| Step | Time | Tab |
|---|---|---|
| Pre-check | 10 min | 1 · Start here |
| Concepts | 90 min | 2 · Concepts |
| Conversation | 20 min | 3 · Conversation |
| Lab | 4-5 h | 4 · Hands-on lab |
| Practice | 90 min | 5 · Practice |

## Key terms

| Term | Plain meaning |
|---|---|
| **Case / control** | Person with / without the condition |
| **Odds ratio (OR)** | How much the odds of disease change per copy of the allele |
| **Manhattan plot** | −log₁₀(P) for every SNP along the genome |
| **QQ plot** | Observed vs expected P-values; reveals inflation |
| **λ (lambda)** | Genomic inflation factor; ~1 is well calibrated |
| **Confounding** | A third factor (ancestry, site) linked to both genotype and disease |
| **LD clumping** | Group correlated SNPs around the strongest ("index") SNP |

## Pre-check

1. If 0.05 is the usual cut-off and you test 2,772 SNPs with no true associations, how many do you expect below 0.05 by chance?
2. An allele has an odds ratio of 2.0 per copy. Roughly, what are the odds ratios for 0, 1 and 2 copies relative to 0 copies?
3. Why might ancestry produce a false association?
4. What would λ = 1.25 suggest?

<details>

<summary>Show answers</summary>

1. About 139 (5% of 2,772).
2. 1, 2 and 4 under a log-additive model (the odds multiply per copy).
3. If ancestry groups differ in both allele frequency and disease risk, every SNP that differs in frequency will look associated.
4. Test statistics are inflated by about 25% at the median - suggesting confounding, relatedness or problems with quality control.

</details>

{% endtab %}

{% tab title="2 · Concepts" %}

## 2.1 The idea

For each SNP, compare genotypes between cases and controls. In **logistic regression** the model is

> log-odds(case) = β₀ + β₁ × (copies of allele A1) + β₂ × covariate₂ + …

The odds ratio per copy is exp(β₁). The test gives a P-value for β₁ = 0. Repeat for each SNP: it is "genome-wide" because a million or more tests are made. Including **covariates** (age, sex, study site, ancestry principal components) removes differences that would otherwise be mistaken for genetic effects.

## 2.2 Quality control is most of the work

| Level | Check | Typical rule | Why |
|---|---|---|---|
| Sample | Missingness | remove > 5% missing genotypes | Poor DNA or genotyping |
| Sample | Sex check | declared sex disagrees with X-chromosome heterozygosity | Sample swaps |
| Sample | Relatedness | keep one of each pair with PI_HAT > 0.4 (or 0.1875 in real data) | Duplicates and relatives break independence |
| Sample | Ancestry outliers | remove extreme PCs | Different population or error |
| SNP | Missingness | remove > 5% missing | Poor assay |
| SNP | MAF | remove very rare SNPs (small studies lack power) | Unreliable tests |
| SNP | HWE in **controls** | remove P < 10⁻⁶ | Genotyping artefacts |

Cases are excluded from the HWE test because a true causal variant can depart from HWE among cases. Real studies add further checks (batch effects, heterozygosity, imputation quality).

{% hint style="warning" %}
**Thresholds are conventions, not laws.** Write down the thresholds *before* looking at the association results, and report them.
{% endhint %}

## 2.3 Population structure and confounding

If cases are over-represented from one ancestry group and that group also has different allele frequencies, almost every SNP that differs in frequency between groups appears associated. Remedies:

- **Principal components** as covariates (what we do);
- study-site and batch covariates;
- **mixed models** (for related individuals; Week 8 stretch);
- matched or within-group designs.

The QQ plot shows the problem: with confounding the whole line lifts above the diagonal, not just the tail.

## 2.4 Genomic inflation (λ)

λ is the median observed χ² statistic divided by the median expected under the null (0.455 for 1 degree of freedom). λ ≈ 1 is calibrated; values above ~1.05-1.1 are a concern. Caution: for a trait with many true small effects (polygenic) λ rises legitimately. In a small cohort with few causal SNPs, a λ well above 1 mostly means bias.

## 2.5 Multiple testing

Testing M SNPs inflates false positives. Two common thresholds:

| Threshold | Value | Meaning |
|---|---|---|
| Bonferroni | 0.05 / M | Controls family-wise error for the M tests you actually ran |
| Genome-wide significance | 5×10⁻⁸ | Conventional for common variants in human genomes (about a million independent tests) |

Here M = 2,772, so Bonferroni is 1.8×10⁻⁵, much less strict than 5×10⁻⁸ - because our toy panel has few SNPs. Pick the threshold in advance and say which.

## 2.6 Reading the results

- **Effect size matters more than P:** report OR with a confidence interval.
- **A signal is a region:** SNPs in LD with the causal one are also significant. **Clumping** groups them around an *index SNP*.
- **Association is not causation.** The associated SNP may merely tag the causal variant.
- **Winner's curse:** the estimated effect of the top SNP is usually exaggerated; replication in an independent cohort is the real test.
- **Ancestry:** a GWAS in one population may not transfer (Week 9).

{% hint style="info" %}
**Public health lens.** A GWAS result becomes a policy only after replication, functional follow-up and equity review. Who was in the study, who was not, and who might be harmed by a risk label are part of the result.
{% endhint %}

{% endtab %}

{% tab title="3 · Conversation" %}

*Zainab has two Manhattan plots taped side by side on the wall. They look almost identical: a lonely tower of dots on chromosome 6. Tunde is holding a QQ plot.*

**Zainab:** I'm confused. The two Manhattan plots look the same. If the "naive" analysis and the "adjusted" analysis find the same SNP, why bother with all this correction?

**Tunde:** Look at the QQ plot instead. Same data, different lines.

**Zainab:** The naive line lifts off the diagonal early. The adjusted one hugs it, then shoots up at the end for the real hits.

**Dr. Mensah:** And what does the early lift mean?

**Zainab:** That the p-values are too small across the board. Something systematic is pushing everything.

**Tunde:** That is λ: 1.25 for the naive model, 0.98 for the adjusted. Close to one is what we want.

**Zainab:** But the top hit is the same. So the strong signal survives anyway.

**Dr. Mensah:** A very strong real signal often does. The danger is what lies *just* below it. Tunde, count the SNPs with P below one in a thousand.

**Tunde:** Naive: twelve. Adjusted: eight. By chance alone I'd expect about three.

**Zainab:** So the adjusted model still has more than chance - those would be real signals.

**Tunde:** And the naive model has six extra ones that vanish when we adjust. Six false leads.

**Zainab:** In a real study with a million SNPs it would be thousands.

**Dr. Mensah:** Which is why the threshold is five times ten to the minus eight. Let me test you. The top SNP has a p-value of seven times ten to the minus thirteen. What can you say?

**Zainab:** That the association is very unlikely to be chance.

**Dr. Mensah:** And?

**Zainab:** That this SNP *causes* the disease?

**Dr. Mensah:** Look at the Manhattan plot. How many dots are in the tower?

**Zainab:** Two. Two SNPs on chromosome 6, close together.

**Tunde:** Five thousand base pairs apart. They are correlated - LD - so both are high. One may be causal; the other just rides along.

**Zainab:** So I can't tell which is the culprit.

**Dr. Mensah:** From these data, no. You need more: a bigger study, fine-mapping, functional work. Another question. The second signal, on chromosome 12, has a p-value of 2.6 times ten to the minus seven. Is it a discovery?

**Zainab:** It doesn't pass five times ten to the minus eight.

**Tunde:** It passes the Bonferroni threshold for this panel.

**Zainab:** So "significant" depends on which threshold I picked. I should have chosen before looking.

**Dr. Mensah:** Exactly. And what would you say about it?

**Zainab:** "Suggestive; needs replication."

**Dr. Mensah:** Last. When we started, how many people did we remove before the analysis?

**Tunde:** Twenty-five of the thousand. High missingness, sex mismatches, duplicates and relatives, ancestry outliers.

**Zainab:** I kept thinking of them as "bad data". But a sex mismatch means a *sample swap*. That's a person whose genotype is attached to someone else's phenotype.

**Dr. Mensah:** Which is why sample QC is not bureaucracy. One swapped sample is a lie in the dataset, and if it happens to a case carrying the causal allele, you lose power; if it is systematic you lose the study.

**Zainab:** I'll write that on the wall. "QC protects the people in the data."

### Talking points for the forum

1. A published GWAS reports P = 3×10⁻⁹ for a SNP and says it "causes" a disease. List three questions you would ask the authors.
2. Your team can only afford a GWAS on 500 people from one ethnic group. What claims can the results support?
3. How should a GWAS team communicate with the community whose genomes were studied before publishing results that could stigmatise them?

{% endtab %}

{% tab title="4 · Hands-on lab" %}

{% hint style="success" %}
**Lab goal.** QC the cohort, correct for ancestry, run the association, and compare with the answer key. Everything below was run with PLINK 1.90b7.2 and R 4.3.3. You can copy the two scripts, or type the steps. Work in `results/week08` created from the repository root.
{% endhint %}

```bash
mkdir -p results/week08 && cd results/week08
```

## Part A - Know your data (20 min)

```bash
D=../../data/gwas
head -3 $D/cohort.fam; head -3 $D/covariates.tsv
plink --bfile $D/cohort --freq --out f 2>&1 | grep -i "loaded"
```

Cohort: 1,000 people, 3,160 SNPs on chromosomes 1-22 and X (coded 23). Covariates: age, sex, and study-site indicators `SITE_B`, `SITE_C`.

**Stop and plan.** Before continuing, write down in a notebook the QC checks you will run and your thresholds.

## Part B - Sample QC step by step (60 min)

### Step 1. Missingness

```bash
plink --bfile $D/cohort --missing --out miss >/dev/null
awk 'NR>1 && $6>0.05' miss.imiss | wc -l          # people with >5% missing
awk 'NR>1 && $5>0.05' miss.lmiss | wc -l          # SNPs with >5% missing
```

```text
12
60
```

12 people and 60 SNPs have more than 5% missing genotypes.

### Step 2. Sex check

```bash
plink --bfile $D/cohort --check-sex --out sex 2>&1 | grep -i "problems"
awk 'NR>1 && $5=="PROBLEM"{print $3,$4}' sex.sexcheck | sort | uniq -c
awk 'NR>1 && $5=="PROBLEM" && $3!=0 && $4!=0' sex.sexcheck | cut -c1-70
```

```text
--check-sex: 300 Xchr and 0 Ychr variant(s) scanned, 15 problems detected.
      3 1 2
      9 2 0
      3 2 1
  P0548   P0548            2            1      PROBLEM            1
  P0433   P0433            1            2      PROBLEM     -0.00123
  P0875   P0875            2            1      PROBLEM            1
  P0647   P0647            1            2      PROBLEM     0.006607
  P0800   P0800            2            1      PROBLEM            1
  P0604   P0604            1            2      PROBLEM       0.1122
```

PLINK flags 15 people, of two kinds. **Six** have a clear conflict: recorded female but genetically male (F ≈ 1) or recorded male but genetically female (F ≈ 0) - these are probable sample swaps. **Nine** have `SNPSEX = 0` (the X-chromosome signal is ambiguous: F between 0.2 and 0.8); in a real study you would check them, but for now we remove only the six clear ones. (The `Warning: ... het. haploid genotypes` lines you may see are males with heterozygous X calls; PLINK treats them as missing.)

### Step 3. Relatedness

```bash
plink --bfile $D/cohort --chr 1-22 --geno 0.05 --maf 0.05 --indep-pairwise 50 5 0.2 --out prune >/dev/null
plink --bfile $D/cohort --extract prune.prune.in --min 0.4 --genome --out ibd >/dev/null
awk 'NR>1{print $2,$4,$10}' ibd.genome
```

```text
P0409 P0734 0.5442
P0350 P0936 0.9952
P0072 P0438 0.5331
P0370 P0782 0.9857
P0576 P0173 0.5744
```

`PI_HAT` is the estimated proportion of the genome shared identical-by-descent. Two pairs are essentially identical (0.99: duplicate samples or twins) and three are about 0.5 (full siblings). Close relatives break the independence assumption, so we keep one of each pair. (We use `--min 0.4`, a deliberately high cut-off, because in this toy cohort the mixture of two ancestry groups inflates PI_HAT for thousands of unrelated pairs - a good illustration of why relatedness is estimated *within* ancestry groups in real studies.)

### Step 4. Ancestry outliers

```bash
plink --bfile $D/cohort --extract prune.prune.in --pca 10 --out pca0 >/dev/null
awk 'function a(x){return x<0?-x:x} a($4)>0.2{print $1,$2}' pca0.eigenvec
```

```text
P0367 P0367
P0158 P0158
P0611 P0611
```

Three people sit far away on PC2 (Week 4). We use the **absolute value** because the sign of a principal component is arbitrary: the same data can return PC2 = +0.34 on one run and −0.34 on another.

## Part C - One script for QC (30 min)

Save this as `run_gwas.sh` in `results/week08` and run it. It repeats Steps 1-4 and the rest of the QC, then runs the association.

```bash
#!/usr/bin/env bash
# run_gwas.sh - QC and association for the toy cohort (Week 8). Run from results/week08.
set -euo pipefail
D=../../data/gwas
q() { grep -i "$1" "$2" || true; }

echo "### 1. Sample QC"
plink --bfile $D/cohort --missing --out miss >/dev/null
awk 'NR>1 && $6>0.05{print $1,$2}' miss.imiss > rm_missing.txt
plink --bfile $D/cohort --check-sex --out sex >/dev/null
awk 'NR>1 && $5=="PROBLEM" && $3!=0 && $4!=0{print $1,$2}' sex.sexcheck > rm_sex.txt
plink --bfile $D/cohort --chr 1-22 --geno 0.05 --maf 0.05 --indep-pairwise 50 5 0.2 --out prune >/dev/null
plink --bfile $D/cohort --extract prune.prune.in --min 0.4 --genome --out ibd >/dev/null
awk 'NR>1{print $3,$4}' ibd.genome > rm_related.txt
plink --bfile $D/cohort --extract prune.prune.in --pca 10 --out pca0 >/dev/null
awk 'function a(x){return x<0?-x:x} a($4)>0.2{print $1,$2}' pca0.eigenvec > rm_outlier.txt
echo "high missingness: $(wc -l < rm_missing.txt)  sex mismatch: $(wc -l < rm_sex.txt)  related (2nd of pair): $(wc -l < rm_related.txt)  ancestry outliers: $(wc -l < rm_outlier.txt)"
cat rm_missing.txt rm_sex.txt rm_related.txt rm_outlier.txt | sort -u > rm_all.txt
echo "people to remove (unique): $(wc -l < rm_all.txt)"

echo "### 2. Sample + SNP QC"
plink --bfile $D/cohort --remove rm_all.txt --geno 0.05 --maf 0.01 --hwe 1e-6 midp --make-bed --out qc 2>&1 \
  | grep -i "people remaining\|removed due\|pass filters\|cases and"

echo "### 3. Structure in the cleaned data"
plink --bfile qc --chr 1-22 --maf 0.05 --indep-pairwise 50 5 0.2 --out qcprune >/dev/null
plink --bfile qc --extract qcprune.prune.in --pca 10 --out qcpca >/dev/null
Rscript -e 'cv <- read.table("'$D'/covariates.tsv", header=TRUE)
pc <- read.table("qcpca.eigenvec", col.names=c("FID","IID",paste0("PC",1:10)))
m <- merge(cv, pc[,c("FID","IID","PC1","PC2","PC3","PC4")], by=c("FID","IID"))
write.table(m, "covar.txt", quote=FALSE, row.names=FALSE, sep="\t"); cat("covariate rows:", nrow(m), "\n")'

echo "### 4. Association (autosomes)"
plink --bfile qc --chr 1-22 --logistic --out naive >/dev/null
plink --bfile qc --chr 1-22 --logistic hide-covar --covar covar.txt \
      --covar-name AGE,SITE_B,SITE_C,PC1,PC2,PC3,PC4 --out adj >/dev/null
echo "done"
```

Run it:

```bash
bash run_gwas.sh
```

```text
### 1. Sample QC
high missingness: 12  sex mismatch: 6  related (2nd of pair): 5  ancestry outliers: 3
people to remove (unique): 25
### 2. Sample + SNP QC
--remove: 975 people remaining.
60 variants removed due to missing genotype data (--geno).
--hwe: 28 variants removed due to Hardy-Weinberg exact test.
0 variants removed due to minor allele threshold(s)
3072 variants and 975 people pass filters and QC.
Among remaining phenotypes, 492 are cases and 483 are controls.
### 3. Structure in the cleaned data
covariate rows: 975 
### 4. Association (autosomes)
done
```

(Two harmless `Warning: 355 het. haploid genotypes` messages appear first.) The 25 removed people are the **union** of the four lists (some people fall into more than one). After QC: 975 people (492 cases, 483 controls) and 3,072 SNPs, of which 2,772 are autosomal and tested.

**What does `set -euo pipefail` do?** It makes the script stop at the first error, on unset variables, and on failures inside pipes - so a failed step cannot silently produce an empty file that is analysed anyway (Week 2).

## Part D - Results and plots (60 min)

Save as `plot_gwas.R` and run `Rscript plot_gwas.R`:

```r
# plot_gwas.R - lambda, top hits, Manhattan and QQ plots (Week 8)
suppressPackageStartupMessages({library(dplyr); library(ggplot2)})
read_assoc <- function(f) { d <- read.table(f, header = TRUE); d[d$TEST == "ADD" & !is.na(d$P), ] }
lambda <- function(p) median(qchisq(p, 1, lower.tail = FALSE)) / qchisq(0.5, 1)
naive <- read_assoc("naive.assoc.logistic"); adj <- read_assoc("adj.assoc.logistic")
n <- nrow(adj); bonf <- 0.05 / n
cat(sprintf("SNPs tested: %d   Bonferroni threshold 0.05/%d = %.2g\n", n, n, bonf))
cat(sprintf("lambda  naive: %.2f   adjusted: %.2f\n", lambda(naive$P), lambda(adj$P)))
cat(sprintf("P < 5e-8:   naive %d   adjusted %d\n", sum(naive$P < 5e-8), sum(adj$P < 5e-8)))
cat(sprintf("P < Bonf:   naive %d   adjusted %d\n", sum(naive$P < bonf), sum(adj$P < bonf)))
cat("\nTop adjusted results:\n")
print(head(adj[order(adj$P), c("CHR", "SNP", "BP", "A1", "OR", "P")], 5), row.names = FALSE)
cat("\nSame SNPs, naive model:\n")
print(naive[naive$SNP %in% head(adj$SNP[order(adj$P)], 3), c("SNP", "OR", "P")], row.names = FALSE)

manh <- function(d, title, file) {
  d <- d %>% arrange(CHR, BP) %>% mutate(idx = row_number(), col = factor(CHR %% 2))
  p <- ggplot(d, aes(idx, -log10(P), colour = col)) + geom_point(size = 1, show.legend = FALSE) +
    scale_colour_manual(values = c("#2b6cb0", "#718096")) +
    geom_hline(yintercept = -log10(5e-8), colour = "red", linetype = 2) +
    geom_hline(yintercept = -log10(bonf), colour = "darkgreen", linetype = 3) +
    labs(title = title, x = "SNPs in genome order (chr 1-22)", y = expression(-log[10](P))) + theme_minimal()
  ggsave(file, p, width = 8, height = 3.8, dpi = 110)
}
manh(naive, "Manhattan - naive model", "manhattan_naive.png")
manh(adj, "Manhattan - adjusted for age, site and PC1-4", "manhattan_adjusted.png")
qq <- bind_rows(
  naive %>% arrange(P) %>% transmute(model = "naive", obs = -log10(P), exp = -log10(ppoints(n()))),
  adj   %>% arrange(P) %>% transmute(model = "adjusted", obs = -log10(P), exp = -log10(ppoints(n()))))
p <- ggplot(qq, aes(exp, obs, colour = model)) + geom_point(size = 1) + geom_abline(linetype = 2) +
  labs(title = "QQ plot", x = "Expected -log10(P)", y = "Observed -log10(P)") + theme_minimal()
ggsave("qq.png", p, width = 5.5, height = 4.5, dpi = 110)
```

```text
SNPs tested: 2772   Bonferroni threshold 0.05/2772 = 1.8e-05
lambda  naive: 1.25   adjusted: 0.98
P < 5e-8:   naive 2   adjusted 2
P < Bonf:   naive 3   adjusted 3

Top adjusted results:
 CHR      SNP      BP A1    OR         P
   6 ts06_067 5079921  C 2.133 7.210e-13
   6 ts06_064 5044295  C 2.018 2.414e-11
  12 ts12_048 3312381  A 1.692 2.638e-07
  12 ts12_042 3263822  G 1.502 3.147e-05
  12 ts12_049 3324700  G 1.492 4.329e-05

Same SNPs, naive model:
      SNP    OR         P
 ts06_064 2.080 3.170e-13
 ts06_067 2.202 8.218e-15
 ts12_048 1.555 6.260e-06
```

**Interpret.**

1. **Calibration.** λ falls from 1.25 (naive) to 0.98 (adjusted). Open `qq.png`: the naive points lift off the diagonal along the whole range; the adjusted points follow the line until the true signals at the top.
2. **Main signal.** `ts06_067` (chromosome 6, 5,079,921): OR 2.13 per copy of allele `C`, P = 7×10⁻¹³ - far past 5×10⁻⁸. Its neighbour `ts06_064` (5 kb away) is also significant because of LD.
3. **Suggestive signal.** `ts12_048`: OR 1.69, P = 2.6×10⁻⁷; passes the Bonferroni threshold (1.8×10⁻⁵) but **not** 5×10⁻⁸. Report it as suggestive and needing replication. Note that its estimated OR is subject to winner's curse.
4. **False leads removed.** Count how many SNPs fall below P = 0.001:

```bash
Rscript -e '
r <- function(f){d <- read.table(f, header=TRUE); d[d$TEST=="ADD" & !is.na(d$P),]}
n <- r("naive.assoc.logistic"); a <- r("adj.assoc.logistic")
for (t in c(0.05, 0.001)) cat("P <", t, ": naive", sum(n$P<t), " adjusted", sum(a$P<t), " expected by chance", round(t*nrow(n)), "\n")'
```

```text
P < 0.05 : naive 228  adjusted 159  expected by chance 139
P < 0.001 : naive 12  adjusted 8  expected by chance 3
```

Adjustment removes about 70 nominal and 4 stricter false signals; some excess remains (8 vs 3 expected) because there are true associations in the data.

### Step 5. Clump the signals

```bash
plink --bfile qc --chr 1-22 --clump adj.assoc.logistic --clump-p1 5e-8 --clump-p2 1e-5 \
      --clump-r2 0.2 --clump-kb 500 --out clump 2>&1 | grep "clump formed"
cut -c1-110 clump.clumped
```

```text
--clump: 1 clump formed from 2 top variants.
 CHR    F        SNP         BP        P    TOTAL   NSIG    S05    S01   S001  S0001    SP2
   6    1   ts06_067    5079921   7.21e-13        4      0      0      2      1      1 ts06_064(1)
```

Two significant SNPs are collapsed into **one** locus indexed by `ts06_067`, with `ts06_064` as a clumped member (`SP2`). One locus, one finding.

## Part E - Compare with the truth and write up (45 min)

Open `data/gwas/answers/truth.md`: the main causal SNP is `ts06_067` (simulated OR 2.0; you estimated 2.13) and the suggestive SNP is `ts12_048` (simulated OR 1.6; you estimated 1.69). Write `results/week08/results.md` (≤250 words) covering: the data and QC (counts removed); the model; λ before and after; the loci with OR, 95% confidence interval or standard error and P; threshold used; limitations (single cohort, small, simulated); and what replication you would request.

## If it breaks

| Message or symptom | Likely cause | Fix |
|---|---|---|
| `Error: Failed to open ../../data/gwas/cohort.bed` | Wrong directory | Run from `results/week08`; check `ls ../../data/gwas` |
| `Warning: ... het. haploid genotypes` | Males with het X calls | Harmless; PLINK sets them to missing |
| `--covar-name ... not found` | Typo in column names | Header of `covar.txt` must contain the names exactly |
| All PCs identical to a different run | Signs of PCs flip | Use absolute values or compare plots, not signs |
| λ very different from 1.25/0.98 | Different QC choices | Compare removed counts with the table above |
| `plink: command not found` | Tool missing | `bash scripts/check_setup.sh` |
| Different `P` in the last digits | PLINK version | Compare ORs and ranks, not every digit |

## Stretch challenge

1. Add `SEX` as a covariate and extend the analysis to the X chromosome (23). What changes?
2. Remove PC1-4 from the adjusted model. How much of the lift in λ is due to the PCs alone, and how much to age and site?
3. Run the analysis separately in each ancestry group (use `qcpca.eigenvec`). Are the effect sizes consistent?

{% endtab %}

{% tab title="5 · Practice" %}

## Exercises

### Basic

**Exercise 1.** What is the odds ratio for a person with two copies of an allele with OR = 1.7 per copy, relative to zero copies (log-additive model)?

**Exercise 2.** Why do we test HWE in controls only?

**Exercise 3.** What does λ = 0.98 tell you?

<details>

<summary>Show answers (1-3)</summary>

1. 1.7² = 2.89.
2. A genuinely associated variant can deviate from HWE among cases; filtering on all samples would discard true signals.
3. The test statistics are well calibrated, with no evidence of inflation (slightly below 1 is normal sampling variation).

</details>

### Intermediate

**Exercise 4.** From the output: how many SNPs would you expect below 5×10⁻⁸ by chance among 2,772 tests? How about below the Bonferroni level?

**Exercise 5.** The naive model reports `ts06_067` with OR 2.20 and the adjusted model 2.13. Which estimate would you report, and why?

**Exercise 6.** Compute a 95% confidence interval for the log-odds if the standard error is 0.18 and the OR is 2.13.

<details>

<summary>Show answers (4-6)</summary>

4. 2,772 × 5×10⁻⁸ ≈ 0.00014 (essentially none). At the Bonferroni level: 2,772 × 1.8×10⁻⁵ ≈ 0.05 (about a 5% chance of one false hit in the whole study, by definition).
5. The adjusted estimate; it controls for ancestry, age and site and is better calibrated. The two are close here because the main signal is strong.
6. log(2.13) = 0.756. 0.756 ± 1.96 × 0.18 = (0.403, 1.109). On the OR scale: (1.50, 3.03).

</details>

### Challenge

**Exercise 7.** The six sex-check conflicts and nine ambiguous people were handled differently. Propose a protocol for the ambiguous nine (what additional checks, who decides, what you record).

**Exercise 8.** You are asked to repeat this GWAS with 100 cases and 100 controls. Without calculating, what happens to power, to winner's curse, and to the plausibility of `ts12_048`? What study design would you recommend?

<details>

<summary>Show answers (7-8)</summary>

7. Check the X-chromosome call rate and heterozygosity; compare with the reported sex and any other information (for example hormone treatment, intersex conditions or chromosomal variation); contact the sample source; record the decision and whether samples were excluded or retained. Sensitive handling matters: a mismatch is not always an error, and decisions should avoid assuming a mistake.
8. Power falls sharply, so only very large effects are detectable; winner's curse gets worse (a significant SNP's estimated effect is exaggerated); `ts12_048` would probably not be detectable at all. Recommend collaborating to increase sample size, meta-analysing with other cohorts, or a targeted candidate-variant design with pre-specified hypotheses.

</details>

## Self-test (8 questions)

1. The usual genome-wide significance threshold for common variants is: (a) 0.05 (b) 0.001 (c) 5×10⁻⁸ (d) 10⁻³
2. A QQ plot lifted off the diagonal along its whole length suggests: (a) many true effects only (b) confounding or bias (c) perfect calibration (d) too few SNPs
3. An OR of 1.0 means: (a) no association (b) strong risk (c) strong protection (d) error
4. Clumping is used to: (a) remove people (b) group correlated significant SNPs into loci (c) fix HWE (d) compute PCs
5. Why drop one of each close-relative pair? (a) they cost more (b) they violate independence and inflate statistics (c) they are low quality (d) to balance sexes
6. A sex-check "PROBLEM" with F≈1 and recorded female suggests: (a) a possible sample swap (b) perfect data (c) low depth (d) a relative
7. The best test of a GWAS discovery is: (a) a lower P-value (b) replication in an independent cohort (c) a nicer plot (d) a larger OR
8. A SNP significant at 10⁻¹² in a single-ancestry study: (a) is proven causal (b) may not transfer to other ancestries (c) is a lab error (d) must be rare

<details>

<summary>Show answers and reasons</summary>

1. **(c)**
2. **(b)** A global lift suggests systematic inflation, not a few true hits.
3. **(a)**
4. **(b)**
5. **(b)**
6. **(a)** Declared and genetic sex disagree.
7. **(b)**
8. **(b)** Frequencies and LD differ between ancestries.

</details>

## Reflection prompt (150-250 words)

Describe a GWAS finding you have read about. Using this week's checklist (QC, ancestry, threshold, replication, effect size, equity), which of the six did the paper report clearly, and which would you ask for?

## Portfolio mini-deliverable

`results/week08/`: `run_gwas.sh`, `plot_gwas.R`, `manhattan_adjusted.png`, `qq.png`, `clump.clumped`, and `results.md`.

{% endtab %}

{% tab title="6 · Go deeper" %}

## Core resources

- **Marees AT, et al.** *A tutorial on conducting genome-wide association studies: Quality control and statistical analysis.* International Journal of Methods in Psychiatric Research, 2018 (search by title): the standard QC walk-through this week follows.
- **Uffelmann E, et al.** *Genome-wide association studies.* Nature Reviews Methods Primers, 2021 (search by title): an accessible overview of design, analysis and interpretation.
- **GWAS Catalog** ([ebi.ac.uk/gwas](https://www.ebi.ac.uk/gwas/)): browse published associations; note sample ancestry and sample size for each study.
- **PLINK 1.9 documentation** ([cog-genomics.org/plink/1.9](https://www.cog-genomics.org/plink/1.9/)): `--logistic`, `--clump`, `--genome`, `--check-sex`.
- **H3Africa** ([h3africa.org](https://h3africa.org)): African GWAS and data-sharing experience, including ethics and capacity building.
- **Galaxy Training Network** ([training.galaxyproject.org](https://training.galaxyproject.org)): GWAS tutorials with browser-based tools.
- **EMBL-EBI Training** ([ebi.ac.uk/training](https://www.ebi.ac.uk/training)): courses on statistical genetics and GWAS.

## Beyond this week

- **Mixed models** (for relatedness and structure): search for the tools REGENIE, SAIGE and GCTA-MLMA and their papers.
- **Fine-mapping**: search for "statistical fine-mapping GWAS" to see how causal variants are prioritised.
- **GA4GH** ([ga4gh.org](https://www.ga4gh.org)): standards for sharing summary statistics and consent.

{% endtab %}

{% tab title="7 · Contribute" %}

You can help improve this week. Open an issue with the label **`week-08`** or edit the file directly - see [How to contribute](../contribute/README.md).

## Ideas for experts

1. **Mixed model:** add a tested REGENIE or similar run and compare with PCs.
2. **Imputation:** a short tested block on pre-imputation checks.
3. **Meta-analysis:** split the cohort by site and meta-analyse with PLINK `--meta-analysis`.
4. **Power calculation:** an R exercise on power versus sample size, effect size and allele frequency.
5. **R-only route:** a compact `glm`-based analysis for a handful of SNPs, for readers without PLINK.
6. **Communication:** a short guide on communicating GWAS results to communities.

**Version notes:** tested with PLINK 1.90b7.2 and R 4.3.3 on Ubuntu 24.04 (October 2026). P-values may differ in their last digits across PLINK builds.

{% endtab %}

{% endtabs %}
