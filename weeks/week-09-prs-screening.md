---
description: Build a polygenic score from summary statistics - harmonise alleles, clump, score, evaluate - then test it as a screening tool and confront its poor portability across ancestries.
---

# Week 9 — Polygenic risk scores and screening

{% hint style="info" %}
**At a glance** · **Time:** ~7-9 h · **Prerequisites:** Weeks 3, 4, 8 · **You will produce:** a harmonised score file, a clumped set of SNPs, scores at seven p-value thresholds, an evaluation by ancestry group, and a screening-performance table · **Tools:** PLINK 1.9, R · **Data:** `data/prs`
{% endhint %}

{% tabs %}

{% tab title="1 · Start here" %}

## Why this matters

A polygenic score (PGS or PRS) adds up the small effects of many variants into one number that estimates a person's genetic predisposition to a trait. Scores are being studied for risk stratification and targeted screening. They can also mislead: the score depends on who was in the discovery study, on how alleles were aligned, and on how the threshold was chosen. A score that performs well in one ancestry can perform far worse in another, which risks widening health inequities if it is introduced without evidence.

This week you build a score from a 10,000-person discovery study and test it in 400 people from the *same* ancestry (G1) and 400 from a *different* one (G2). Then you ask the public-health question: would this be a good **screening test**?

## Learning objectives

By the end of this week you will be able to:

1. **Explain** what a polygenic score is and what it cannot do.
2. **Harmonise** summary statistics to a target dataset: matches, swaps, strand flips and palindromic SNPs.
3. **Clump** SNPs by LD and **score** people with PLINK.
4. **Choose** a p-value threshold and **evaluate** the score with incremental R² - and explain why selecting and evaluating on the same people is optimistic.
5. **Measure** portability across ancestry groups.
6. **Judge** the score as a screening test using sensitivity, PPV and AUC, against the Wilson-Jungner principles.

## Roadmap

| Step | Time | Tab |
|---|---|---|
| Pre-check | 10 min | 1 · Start here |
| Concepts | 90 min | 2 · Concepts |
| Conversation | 20 min | 3 · Conversation |
| Lab | 3-4 h | 4 · Hands-on lab |
| Practice | 90 min | 5 · Practice |

## Key terms

| Term | Plain meaning |
|---|---|
| **Base (discovery) data** | Summary statistics from a large GWAS |
| **Target data** | The people you want to score |
| **PRS / PGS** | Weighted sum of effect-allele counts |
| **Harmonisation** | Making allele labels agree between datasets |
| **Palindromic SNP** | A/T or C/G: the complement is the same pair, so strand is ambiguous |
| **Clumping** | Keep the most significant SNP in each LD block |
| **Incremental R²** | Extra variance explained by the score beyond covariates |
| **Portability** | How well a score transfers to another ancestry group |

## Pre-check

1. A person has genotypes 2, 1, 0 for three SNPs with effect sizes 0.10, −0.05, 0.20. What is the score?
2. Why is an A/T SNP hard to harmonise between datasets that may be on different strands?
3. If the discovery GWAS included only people of one ancestry, would you expect the score to work equally well elsewhere?
4. A test flags 40 people, 14 of whom truly have the condition. What is the PPV?

<details>

<summary>Show answers</summary>

1. 2 × 0.10 + 1 × (−0.05) + 0 × 0.20 = **0.15**.
2. The complement of A/T is T/A, so you cannot tell whether the labels are the same or flipped; frequencies may help, but the safest approach is to exclude them (or use frequency checks).
3. No - allele frequencies, LD and sometimes effects differ, so accuracy usually drops.
4. 14 / 40 = 0.35.

</details>

{% endtab %}

{% tab title="2 · Concepts" %}

## 2.1 The score

For a person with allele counts *gⱼ* (0, 1 or 2 copies of the effect allele) at *M* SNPs with weights *βⱼ* from a GWAS:

> PRS = Σ βⱼ × gⱼ

Weights are the GWAS effect sizes (log odds ratios for binary traits, or per-allele effects for continuous traits). Most traits are **polygenic**: thousands of variants each contribute a tiny amount. The score is therefore a *relative* measure: you compare a person with the distribution of scores in a reference group, usually as a z-score or percentile.

## 2.2 Three rules for a trustworthy score

1. **Discovery and target must be independent** (no overlapping people), or the evaluation is inflated.
2. **Alleles must be aligned.** A sign error on one SNP is small; on a hundred, it destroys the score.
3. **Evaluate in the population where you will use it.**

## 2.3 Harmonisation

Base and target files can disagree on which allele is called A1:

| Case | Base A1/A2 | Target | Action |
|---|---|---|---|
| Match | C/A | C/A | none |
| **Swap** | A/C | C/A | flip the effect sign (beta → −beta) |
| **Strand flip** | G/T | C/A | take the complement; the beta sign is unchanged |
| Flip + swap | T/G | C/A | complement and flip the sign |
| Palindromic | A/T | T/A | ambiguous; drop (or resolve by frequency) |

In this course's data there are 2,850 matches, 4 swaps and 6 strand flips and no palindromic SNPs.

## 2.4 Clumping and thresholds

Neighbouring SNPs are correlated (Week 4), so adding all of them double-counts the same signal. **Clumping** keeps the most significant SNP in each LD block (here r² > 0.1 within 250 kb). Then choose which SNPs enter by **P-value threshold**: a strict threshold (1×10⁻⁴) includes few, reliable SNPs; a lenient one (1.0) includes everything, adding noise but sometimes more true signal. The "best" threshold depends on the trait's architecture and sample sizes.

{% hint style="warning" %}
**Picking the best threshold on the same people you evaluate on is optimistic.** The reported R² is biased upward. Real studies tune on a **validation** set and report on a separate **test** set (or use cross-validation).
{% endhint %}

## 2.5 Measuring performance

| Measure | Use |
|---|---|
| **Incremental R²** | continuous traits: variance explained beyond age, sex |
| **AUC** | binary outcomes: probability that a random case scores higher than a random non-case (0.5 = coin toss, 1.0 = perfect) |
| **Odds ratio per SD, top-decile vs rest** | how risk rises at the high end |
| **Calibration** | do predicted risks match observed risks? |

## 2.6 Portability and equity

Most large GWAS are of European ancestry. In practice, scores predict best in the group the weights came from and typically lose substantial accuracy in others (Martin et al., 2019, *Nature Genetics*). Reasons: different allele frequencies, different LD (the tagging SNP is not the causal variant), and sometimes different environments and effect sizes. A clinic that deploys a score trained in one ancestry for everyone may overdiagnose some people and miss others.

{% hint style="info" %}
**Public health lens.** The question is not "does the score predict?" but "for whom, how well, compared with simple alternatives (age, family history, blood pressure), and with what benefit and harm if it is used to decide who gets screened?"
{% endhint %}

## 2.7 Screening principles (Wilson-Jungner)

A programme should screen only if: the condition is an important problem; there is an accepted treatment; there is a latent stage; a **suitable test** exists, acceptable to the population; the natural history is understood; the cost is balanced against benefit; and case-finding is continuing. For a PRS-based programme, the key weaknesses are test validity (in every group), the availability of effective action, and the harm of false positives. The metrics:

| | Condition present | Absent |
|---|---|---|
| **Flagged** | TP | FP |
| **Not flagged** | FN | TN |

Sensitivity = TP/(TP+FN); PPV = TP/(TP+FP). PPV depends on prevalence: the lower the prevalence, the more false positives per true positive (as in Week 1).

{% endtab %}

{% tab title="3 · Conversation" %}

*The meeting room has a slide titled "Genetic risk score: the future of screening." Zainab is staring at it with her arms crossed. Tunde has just put two bars side by side on the screen: a tall blue one and a short orange one.*

**Zainab:** I was told this was a breakthrough. What am I looking at?

**Tunde:** The same score, tested in two groups. Blue is the group whose genomes built the score. Orange is a different ancestry group. The height is how much of the variation in the trait the score explains.

**Zainab:** Blue is twenty-two percent, orange is ten. So it works less than half as well for the orange group.

**Dr. Mensah:** Why do you think?

**Zainab:** The weights came from the blue group. If the allele frequencies differ…

**Dr. Mensah:** And?

**Zainab:** And the SNPs on the array aren't the causal ones, they only *tag* them. In another population the tag and the causal variant may not travel together.

**Tunde:** In this dataset the causal variants are hidden. All we have are tags. In the blue group the tags work. In the orange group the LD is different, so the tags work worse.

**Zainab:** A medical test that works well for me but not for you.

**Dr. Mensah:** Keep that thought. Tunde, tell her what happened when you first built the score.

**Tunde:** I had a few SNPs where the alleles didn't match. In the base file the effect allele was A. In my target file the first allele was G. If I'd used the effect size as it was, the sign would be wrong.

**Zainab:** Wrong how? The score would be nonsense?

**Tunde:** For four SNPs, the sign was backwards, and for six the strand was flipped. Ten out of nearly three thousand. Not a disaster, but those SNPs would push people the wrong way.

**Dr. Mensah:** And in a real dataset?

**Tunde:** Thousands of them. It's the first check you run: *do my alleles agree?* And watch the A/T and C/G pairs, because you can't tell the strand from the letters.

**Zainab:** Wait. You chose the "best" threshold by looking at which gave the highest R², and then reported that R². Isn't that cheating?

**Tunde:** (pause) Mildly. It is called overfitting the threshold. The honest approach is to choose on one sample and report on another.

**Dr. Mensah:** She spotted what you glossed over. Zainab, would you make this score a screening test?

**Zainab:** I'd want numbers. Tunde?

**Tunde:** Take the top ten percent of the score as "flagged". The condition is being in the top ten percent of the trait. In blue: forty people flagged, fourteen truly have the condition. PPV thirty-five percent, sensitivity thirty-four. In orange: forty flagged, six truly have it. PPV fifteen percent.

**Zainab:** So for orange, eighty-five percent of the people we flag are false alarms.

**Dr. Mensah:** And for blue, sixty-five percent. Still a lot. What does that tell you?

**Zainab:** That this is not a screening test. Not on its own. The AUC is eighty-two in blue and sixty-three in orange. Sixty-three is barely better than flipping a coin.

**Dr. Mensah:** What would you recommend?

**Zainab:** Don't deploy it. Not until it is validated in the groups where it will be used. And compare it with simple things like age and blood pressure.

**Tunde:** And if you did use it, never tell someone "your genes put you at high risk" without saying how uncertain it is.

**Zainab:** I came here thinking this was the future. I still think it might be. But the future needs a bigger, more diverse discovery study, first.

**Dr. Mensah:** Write that down. It is the equity argument in one sentence.

### Talking points for the forum

1. A company offers a PRS for a common disease to your national health service. List five questions you would ask before considering it.
2. Where do you think the *causal* variants and the *tag* SNPs will differ most between ancestry groups, and why does that matter for your region?
3. When, if ever, is a screening test that works for only one group still worth using?

{% endtab %}

{% tab title="4 · Hands-on lab" %}

{% hint style="success" %}
**Lab goal.** Build, evaluate and critique a polygenic score. Everything below was run with PLINK 1.90b7.2 and R 4.3.3. Work in `results/week09` created from the repository root.
{% endhint %}

```bash
mkdir -p results/week09 && cd results/week09
D=../../data/prs
head -3 $D/base_gwas_sumstats.tsv; head -3 $D/target_pheno.tsv
wc -l $D/base_gwas_sumstats.tsv $D/target.bim $D/target.fam
```

The **base** file has 2,860 SNPs (autosomes only) with effect allele `A1`, effect size `BETA`, `P` and `N = 10,000`. The **target** has 800 people (400 per ancestry group `G1`/`G2`) with a continuous `TRAIT`, `AGE`, `SEX` and `GROUP`. The causal variants are hidden; the array SNPs only tag them.

## Part A - Harmonise (45 min)

Save the first script as `prs.R` and run `Rscript prs.R`:

```r
# prs.R - harmonise summary statistics to the target dataset (Week 9). Run from results/week09.
suppressPackageStartupMessages({library(readr); library(dplyr)})
D <- "../../data/prs"
base <- read_tsv(file.path(D, "base_gwas_sumstats.tsv"), show_col_types = FALSE)
bim  <- read.table(file.path(D, "target.bim"), col.names = c("CHR", "SNP", "cM", "BP", "T1", "T2"),
                   stringsAsFactors = FALSE)
comp <- function(x) chartr("ACGT", "TGCA", x)

# 1. Harmonise: make the base effect allele match the target's allele labels -------------------
h <- inner_join(base, bim[, c("SNP", "T1", "T2")], by = "SNP") %>%
  mutate(status = case_when(
    A1 == T1 & A2 == T2             ~ "match",
    A1 == T2 & A2 == T1             ~ "swap",
    comp(A1) == T1 & comp(A2) == T2 ~ "flip",
    comp(A1) == T2 & comp(A2) == T1 ~ "flip+swap",
    TRUE                            ~ "unresolved"),
    pal = A1 %in% c("A", "T") & A2 %in% c("A", "T") | A1 %in% c("C", "G") & A2 %in% c("C", "G"))
cat("Harmonisation status:\n"); print(table(h$status))
cat("Palindromic (A/T or C/G) SNPs:", sum(h$pal), "\n")
h <- h %>% filter(status != "unresolved", !pal) %>%
  mutate(BETA_T1 = ifelse(status %in% c("swap", "flip+swap"), -BETA, BETA))
write_tsv(h %>% transmute(SNP, A1 = T1, BETA = BETA_T1, P), "score_input.tsv")
write_tsv(h %>% select(SNP, P), "snp_pvalues.tsv")
```

```text
Harmonisation status:

 flip match  swap
    6  2850     4
Palindromic (A/T or C/G) SNPs: 0
```

Of 2,860 SNPs, 2,850 match, **4 are swapped** (A1/A2 reversed: the effect sign must be flipped) and **6 are strand-flipped** (the labels are complements: use the target's label with the same sign). There are no palindromic SNPs. The script writes the effect allele and beta in the target's own labelling to `score_input.tsv`. Check one swapped SNP by hand:

```bash
grep -w ts13_078 score_input.tsv ../../data/prs/base_gwas_sumstats.tsv ../../data/prs/target.bim
```

```text
score_input.tsv:ts13_078	G	0.02658	0.07753
../../data/prs/base_gwas_sumstats.tsv:ts13_078	13	5164655	A	G	0.6639	-0.02658	0.01506	0.07753	10000
../../data/prs/target.bim:13	ts13_078	0	5164655	G	A
```

In the base file the effect allele is `A` with beta −0.02658; in the target the first allele is `G`. Having `G` means *not* having `A`, so the effect of `G` is **+0.02658**. Without harmonisation the sign would be wrong.

## Part B - Clump (30 min)

LD is estimated in the 400 G1 people (the ancestry of the discovery study):

```bash
awk 'NR>1 && $6=="G1"{print $1,$2}' $D/target_pheno.tsv > g1.txt
plink --bfile $D/target --keep g1.txt --clump snp_pvalues.tsv --clump-field P --clump-snp-field SNP \
      --clump-p1 1 --clump-p2 1 --clump-r2 0.1 --clump-kb 250 --out clump 2>&1 | grep -i "clump formed"
awk 'NR>1 && NF>0{print $3}' clump.clumped > clumped_snps.txt
wc -l < clumped_snps.txt
```

```text
921
```

Of the 2,860 SNPs, **921** remain as index SNPs (one per LD block at r² ≥ 0.1 within 250 kb). Setting `--clump-p1 1` keeps every SNP as a possible index; the P-value threshold is applied later.

## Part C - Score at seven thresholds (30 min)

```bash
printf "T1 0 0.0001\nT2 0 0.001\nT3 0 0.01\nT4 0 0.05\nT5 0 0.1\nT6 0 0.5\nT7 0 1\n" > ranges.txt
plink --bfile $D/target --extract clumped_snps.txt \
      --score score_input.tsv 1 2 3 header sum \
      --q-score-range ranges.txt snp_pvalues.tsv 1 2 header --out prs >/dev/null 2>&1
ls prs.*.profile
head -2 prs.T3.profile
```

`--score file 1 2 3` means: SNP in column 1, effect allele in column 2, weight in column 3; `sum` adds weights (not averages). `--q-score-range` makes one score per range of P-values: `T1` uses SNPs with 0 ≤ P ≤ 0.0001, and so on. PLINK writes one `.profile` per range, with `SCORESUM` per person. (PLINK may warn that some lines are skipped "due to variant ID mismatch": these are SNPs outside the clumped set - harmless.)

## Part D - Evaluate (45 min)

Save as `evaluate_prs.R` and run `Rscript evaluate_prs.R`:

```r
# evaluate_prs.R - how well does each p-value threshold predict the trait, by ancestry group? (Week 9)
suppressPackageStartupMessages({library(readr); library(dplyr); library(ggplot2)})
ph <- read_tsv("../../data/prs/target_pheno.tsv", show_col_types = FALSE)
th <- c(T1 = 1e-4, T2 = 1e-3, T3 = 1e-2, T4 = 0.05, T5 = 0.1, T6 = 0.5, T7 = 1)
res <- do.call(rbind, lapply(names(th), function(k) {
  s <- read.table(paste0("prs.", k, ".profile"), header = TRUE)[, c("IID", "CNT", "SCORESUM")]
  d <- inner_join(ph, s, by = "IID") %>% mutate(prs = as.numeric(scale(SCORESUM)))
  do.call(rbind, lapply(c("G1", "G2"), function(g) {
    x <- d[d$GROUP == g, ]
    r0 <- summary(lm(TRAIT ~ AGE + SEX, x))$r.squared
    r1 <- summary(lm(TRAIT ~ AGE + SEX + prs, x))$r.squared
    data.frame(threshold = th[[k]], SNPs = round(mean(x$CNT) / 2), group = g, R2_prs = round(r1 - r0, 3),
               beta = round(coef(lm(TRAIT ~ AGE + SEX + prs, x))[["prs"]], 3))
  }))
}))
print(res, row.names = FALSE)
best <- res %>% filter(group == "G1") %>% slice_max(R2_prs, n = 1)
cat("\nBest threshold in G1:", best$threshold, "\n")
write_csv(res, "prs_thresholds.csv")
p <- ggplot(res, aes(factor(threshold), R2_prs, fill = group)) + geom_col(position = "dodge") +
  scale_fill_manual(values = c(G1 = "#2b6cb0", G2 = "#dd6b20")) +
  labs(x = "P-value threshold for SNP inclusion", y = "Incremental R2 (score beyond age and sex)",
       title = "Prediction by threshold and ancestry group") + theme_minimal()
ggsave("prs_by_group.png", p, width = 7, height = 4, dpi = 110)
# Best-threshold score: distribution and tail enrichment
s <- read.table(paste0("prs.", names(th)[th == best$threshold], ".profile"), header = TRUE)
d <- inner_join(ph, s[, c("IID", "SCORESUM")], by = "IID") %>% group_by(GROUP) %>%
  mutate(prs = as.numeric(scale(SCORESUM)), top10 = prs >= quantile(prs, 0.9), bot10 = prs <= quantile(prs, 0.1))
cat("\nMean trait, top decile vs bottom decile of the score:\n")
print(d %>% group_by(GROUP) %>% summarise(top = round(mean(TRAIT[top10]), 2), bottom = round(mean(TRAIT[bot10]), 2),
      difference = round(top - bottom, 2)), width = 100)
write_csv(d, "prs_best.csv")
```

```text
 threshold SNPs group R2_prs  beta
     1e-04   57    G1  0.222 0.486
     1e-04   57    G2  0.096 0.327
     1e-03   77    G1  0.211 0.470
     1e-03   77    G2  0.101 0.335
     1e-02  119    G1  0.201 0.472
     1e-02  119    G2  0.090 0.305
     5e-02  185    G1  0.188 0.475
     5e-02  185    G2  0.086 0.298
     1e-01  266    G1  0.179 0.468
     1e-01  266    G2  0.073 0.263
     5e-01  683    G1  0.173 0.480
     5e-01  683    G2  0.058 0.229
     1e+00  919    G1  0.174 0.484
     1e+00  919    G2  0.058 0.227

Best threshold in G1: 1e-04

Mean trait, top decile vs bottom decile of the score:
# A tibble: 2 x 4
  GROUP   top bottom difference
  <chr> <dbl>  <dbl>      <dbl>
1 G1     0.82  -0.93       1.75
2 G2     0.29  -0.57       0.86
```

(`SNPs` is the approximate number of SNPs in the score.) **Interpret.**

1. **Incremental R²** is the extra variance explained by the score over age and sex. In G1 the best score explains **22.2%** (57 SNPs, threshold 10⁻⁴); in G2 only **9.6%** - **43% as much**.
2. **Threshold.** In G1 stricter thresholds perform slightly better; adding hundreds of weak SNPs adds noise (R² falls to 17%). In G2 the ranking is flatter (the best is 10⁻³). The "best" threshold differs by group - a reason for care.
3. **Beta per SD** is about 0.47-0.49 in G1 but 0.23-0.34 in G2: one standard deviation of the score shifts the trait by about half as much in G2.
4. **Top vs bottom decile.** In G1 the top-decile mean trait is 0.82 and the bottom −0.93 (difference 1.75); in G2 0.29 and −0.57 (0.86). The score separates people in both groups but about half as well in G2.
5. **Optimism.** The best threshold was chosen *and* evaluated on the same G1 people, so 22.2% is probably a little too high. A clean analysis would tune on one subset and test on another (Exercise 7).

Open `prs_by_group.png`: the orange (G2) bars are everywhere shorter than the blue (G1) bars.

## Part E - Is it a screening test? (45 min)

Save as `screening.R` and run `Rscript screening.R`. We define the "condition" as being in the top 10% of the trait (cut-off 1.25) and "flag" people in the top 10% of the score within their own group:

```r
# screening.R - treat the score as a screening test for "high trait" (Week 9)
suppressPackageStartupMessages({library(readr); library(dplyr)})
d <- read_csv("prs_best.csv", show_col_types = FALSE)
cut_trait <- quantile(d$TRAIT, 0.90)                       # "condition" = top 10% of the trait
d <- d %>% mutate(case = TRAIT >= cut_trait)
auc <- function(score, y) { r <- rank(score); n1 <- sum(y); n0 <- sum(!y); (sum(r[y]) - n1 * (n1 + 1) / 2) / (n1 * n0) }
tab <- d %>% group_by(GROUP) %>% summarise(
  n = n(), prevalence = round(mean(case), 3), AUC = round(auc(prs, case), 3),
  flagged = sum(top10), TP = sum(top10 & case), sens = round(TP / sum(case), 3),
  PPV = round(TP / flagged, 3), FP = sum(top10 & !case))
print(as.data.frame(tab), row.names = FALSE)
cat("\nTrait cut-off for 'condition':", round(cut_trait, 2), "\n")
```

```text
 GROUP   n prevalence   AUC flagged TP  sens  PPV FP
    G1 400      0.102 0.818      40 14 0.341 0.35 26
    G2 400      0.098 0.627      40  6 0.154 0.15 34

Trait cut-off for 'condition': 1.25
```

**Read it with the Wilson-Jungner lens.**

| | G1 | G2 |
|---|---|---|
| AUC | 0.82 | 0.63 (barely better than chance) |
| Sensitivity | 34% (14 of 41 cases found) | 15% (6 of 39) |
| PPV | 35% | 15% |
| False positives | 26 of 40 flagged | 34 of 40 flagged |

Even in the group with the best performance, about two flagged people in three do not have the condition and about two cases in three are missed. In G2 the test is close to useless. **A score that is "significantly associated" with a trait is not necessarily a useful screening test.** Write `results/week09/memo.md` (≤250 words) with your recommendation to a health ministry: deploy, pilot, or defer; for whom; and what evidence you would need first.

## If it breaks

| Message or symptom | Likely cause | Fix |
|---|---|---|
| `Warning: ... lines skipped ... variant ID mismatch` | Score file has SNPs outside the clumped set | Harmless; PLINK keeps only matching SNPs |
| `--score: 0 valid predictors loaded` | Wrong columns | Check `1 2 3 header` match the file |
| `cannot open file 'prs.T1.profile'` | The scoring step failed | Re-run Part C without `>/dev/null` to see the error |
| Different R² | Different clumping set | Check that LD was from `g1.txt` and `--clump-p1 1` |
| Scores all zero | Alleles unmatched | Check `score_input.tsv` has the target's allele labels |
| `could not find function "slice_max"` | Old dplyr | Update dplyr (≥ 1.0) |

## Stretch challenge

1. Re-run Part B with LD from **all** 800 people and from **G2 only**. How does R² change in each group?
2. Split G1 into two halves: choose the threshold on one half and report R² on the other. How much lower is the honest R²?
3. Set the "flag" threshold using the *pooled* top 10% instead of within-group. What happens to the number of G2 people flagged?

{% endtab %}

{% tab title="5 · Practice" %}

## Exercises

### Basic

**Exercise 1.** A SNP is `A/C` in the base file (effect allele A, beta 0.04) and `C/A` in the target (first allele C). What weight and effect allele do you put in the score file?

**Exercise 2.** Why exclude A/T and C/G SNPs when strand is unknown?

**Exercise 3.** In Part D, which threshold gave the highest R² in G1? In G2?

<details>

<summary>Show answers (1-3)</summary>

1. Effect allele `C` with weight **−0.04** (having C means not having A).
2. The complement of A/T is T/A, so a flipped SNP looks identical to a matching one; getting it wrong reverses the effect. Drop them, or resolve using allele frequencies.
3. G1: 10⁻⁴ (R² 0.222). G2: 10⁻³ (R² 0.101).

</details>

### Intermediate

**Exercise 4.** Compute the portability ratio (R² in G2 divided by R² in G1) for thresholds 10⁻⁴ and 1. What do the two values tell you?

**Exercise 5.** In the screening table, G2 flags 40 people and finds 6 of 39 cases. If a programme invited all 40 flagged people for follow-up costing 100 units each, what is the cost per true case found, in G1 and in G2?

**Exercise 6.** Prevalence is about 10% here. What would the PPV in G1 be if the prevalence of the condition were 1%, keeping sensitivity at 34% and the false-positive rate at 7.2% (26 false positives among 359 non-cases)?

<details>

<summary>Show answers (4-6)</summary>

4. 0.096/0.222 = 0.43 at 10⁻⁴; 0.058/0.174 = 0.33 at threshold 1. Transfer is worse when many weak SNPs are included, because their tagging relationships are population-specific.
5. G1: 40 × 100 / 14 = 285.7 per true case. G2: 4,000 / 6 = 666.7 per true case, over twice as costly.
6. In 10,000 people at 1% prevalence: 100 cases (34 detected) and 9,900 non-cases (7.2% false positives → 717). PPV = 34 / (34 + 717) = **4.5%**: more than 95% of flagged people would not have the condition.

</details>

### Challenge

**Exercise 7.** Design an honest evaluation for this score: how would you split the data, what do you tune where, and what do you report?

**Exercise 8.** Draft a one-paragraph statement for a patient information leaflet about a polygenic score, in plain language, that conveys uncertainty and avoids determinism. Then list two things you deliberately left out and why.

<details>

<summary>Show answers (7-8)</summary>

7. Split by person into a *tuning* set and a *test* set (for example 50/50, stratified by group, or use k-fold cross-validation). Choose the clumping and threshold only on the tuning set; report R², AUC, sensitivity and PPV on the test set, separately for each group, with confidence intervals; keep the discovery study independent of both.
8. Example: "This score estimates how common certain genetic variations are in your DNA compared with other people. It does not say whether you will or will not develop the condition. Many people with a high score never develop it, and many with a low score do. The score may be less accurate for people whose ancestry differs from the people used to build it." Left out: any numeric risk (it would suggest false precision); and any statement about family members (the score does not describe them).

</details>

## Self-test (8 questions)

1. A polygenic score is: (a) a single causal SNP (b) a weighted sum over many SNPs (c) a diagnosis (d) a haplotype
2. In harmonisation, a swap requires you to: (a) delete the SNP (b) flip the sign of beta (c) change the P-value (d) do nothing
3. Which SNPs are ambiguous for strand? (a) A/G (b) A/T (c) C/T (d) G/T
4. Clumping is for: (a) removing people (b) reducing redundancy among correlated SNPs (c) fixing HWE (d) imputing
5. Choosing the best threshold and reporting its R² on the same people leads to: (a) a conservative estimate (b) an optimistic estimate (c) no bias (d) a correct estimate
6. The main reason a score works worse in G2: (a) laboratory error (b) differences in allele frequencies and LD from the discovery group (c) lower age (d) smaller SNPs
7. An AUC of 0.5 means: (a) perfect discrimination (b) chance-level discrimination (c) 50% prevalence (d) 50% error
8. In screening, a low prevalence tends to: (a) raise the PPV (b) lower the PPV (c) have no effect (d) raise sensitivity

<details>

<summary>Show answers and reasons</summary>

1. **(b)**
2. **(b)**
3. **(b)** A/T and C/G are palindromic.
4. **(b)**
5. **(b)** The threshold is tuned to the data it is tested on.
6. **(b)**
7. **(b)**
8. **(b)** More false positives per true positive.

</details>

## Reflection prompt (150-250 words)

You are asked to advise a ministry that wants to adopt a polygenic score trained in a different ancestry group. Describe the pilot study you would require before any national roll-out and the equity safeguards you would insist on.

## Portfolio mini-deliverable

`results/week09/`: `prs.R`, `evaluate_prs.R`, `screening.R`, `prs_by_group.png`, `prs_thresholds.csv`, and `memo.md`.

{% endtab %}

{% tab title="6 · Go deeper" %}

## Core resources

- **Choi SW, Mak TS-H, O'Reilly PF.** *Tutorial: a guide to performing polygenic risk score analyses.* Nature Protocols, 2020 (search by title): the standard step-by-step guide; this week follows its logic.
- **Martin AR, et al.** *Clinical use of current polygenic risk scores may exacerbate health disparities.* Nature Genetics, 2019 (search by title): the portability and equity problem in numbers.
- **PGS Catalog** ([pgscatalog.org](https://www.pgscatalog.org)): published scores with their evaluation and the ancestry of the discovery and evaluation cohorts; look for the "ancestry distribution" of a score you know.
- **PLINK 1.9 documentation** ([cog-genomics.org/plink/1.9](https://www.cog-genomics.org/plink/1.9/)): `--score` and `--q-score-range`.
- **Wilson JMG, Jungner G.** *Principles and practice of screening for disease.* WHO Public Health Papers 34, 1968 (search by title).
- **PHG Foundation** ([phgfoundation.org](https://www.phgfoundation.org)) and **WHO** ([who.int](https://www.who.int)): policy analysis and guidance on genomics in screening.
- **H3Africa** ([h3africa.org](https://h3africa.org)): work on genomic diversity in African populations, including its implications for risk prediction.

## Beyond this week

- **Methods that model LD and effects jointly**: search for PRS-CS, LDpred2 and SBayesR for alternatives to clumping and thresholding.
- **Multi-ancestry scores**: search "PRS-CSx" and "multi-ancestry polygenic scores".
- **Reporting standards**: search for the "PRS-RS" (Polygenic Risk Score Reporting Standards) statement.

{% endtab %}

{% tab title="7 · Contribute" %}

You can help improve this week. Open an issue with the label **`week-09`** or edit the file directly - see [How to contribute](../contribute/README.md).

## Ideas for experts

1. **LDpred2 or PRS-CS** worked example using the same data.
2. **Real PGS Catalog score:** a tested example that applies a published score to a tiny public dataset, with licence notes.
3. **Calibration:** add a section on calibration plots and absolute risk.
4. **Binary-trait variant:** a second generator option with a case-control outcome and odds-ratio weights.
5. **Fairness metrics:** an exercise on thresholds that equalise sensitivity across groups, and the trade-offs.
6. **Communication:** user-tested wording for results letters.

**Version notes:** tested with PLINK 1.90b7.2 and R 4.3.3 (dplyr 1.1.4, ggplot2 3.4.4) on Ubuntu 24.04 (October 2026).

{% endtab %}

{% endtabs %}
