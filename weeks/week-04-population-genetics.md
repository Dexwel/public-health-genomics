---
description: Allele frequencies, Hardy-Weinberg, linkage disequilibrium, Fst and PCA - the population-genetics toolkit behind every genomic study - practised with PLINK and R.
---

# Week 4 — Genetic variation and population genetics

{% hint style="info" %}
**At a glance** · **Time:** ~6-8 h · **Prerequisites:** Weeks 2-3 (shell, R) · **You will produce:** a MAF histogram, a Hardy-Weinberg screen, an Fst estimate, an LD summary and a PCA plot · **Tools:** PLINK 1.9, R (readr, dplyr, ggplot2) · **Data:** `data/gwas`
{% endhint %}

{% tabs %}

{% tab title="1 · Start here" %}

## Why this matters

Almost every claim in public health genomics - "this variant is rare", "this score works less well in group X", "these cases form one cluster" - rests on **population genetics**. Allele frequencies tell you how common a variant is. Hardy-Weinberg tests tell you when genotype data are suspect. Linkage disequilibrium explains why one signal drags its neighbours along. Fst and principal components describe ancestry structure, the single biggest trap in association studies (Week 8) and risk scores (Week 9).

This week you explore a 1,000-person synthetic cohort with 3,160 SNPs. You will find the planted data-quality problems, measure the genetic distance between two simulated groups, and see structure appear on a PCA plot.

## Learning objectives

By the end of this week you will be able to:

1. **Compute and interpret** allele frequencies and the minor allele frequency (MAF) spectrum.
2. **State** Hardy-Weinberg expectations, **test** them, and **explain** two reasons for failure (genotyping error; population structure).
3. **Explain** linkage disequilibrium (LD) and measure it with r².
4. **Estimate and interpret** Fst between groups.
5. **Run** a PCA on LD-pruned data and **read** the plot.
6. **Explain** why reference databases such as gnomAD must be read with their ancestry composition in mind.

## Roadmap

| Step | Time | Tab |
|---|---|---|
| Pre-check | 10 min | 1 · Start here |
| Concepts | 90 min | 2 · Concepts |
| Conversation | 20 min | 3 · Conversation |
| Lab | 3 h | 4 · Hands-on lab |
| Practice | 60-90 min | 5 · Practice |

## Key terms

| Term | Plain meaning |
|---|---|
| **SNP** | A single-nucleotide position where people differ |
| **Allele** | One version of a variant (e.g. `C` or `T`) |
| **Genotype** | The two alleles a person carries (`CC`, `CT`, `TT`) |
| **MAF** | Frequency of the less common allele |
| **HWE** | Hardy-Weinberg equilibrium: expected genotype frequencies from allele frequencies |
| **LD** | Alleles at nearby SNPs travel together more than chance predicts |
| **Fst** | 0-1 measure of genetic differentiation between groups |
| **PCA** | Summarises many SNPs into a few axes of variation |

## Pre-check

1. If the allele `A` has frequency p = 0.3, what frequency does Hardy-Weinberg predict for genotype `AA`? For `Aa`?
2. Two SNPs 20 kb apart: would you expect them to be more or less correlated than two SNPs on different chromosomes?
3. If Fst between two groups is 0.04, is that "huge" or "small"?
4. Why might a variant that is "rare" in a database be common in your patients?

<details>

<summary>Show answers</summary>

1. AA = p² = 0.09; Aa = 2pq = 2 × 0.3 × 0.7 = 0.42 (aa = 0.49).
2. More correlated (they are physically close and recombination has not yet separated them).
3. Small in absolute terms (most human Fst values between continental groups are in the range of a few hundredths), yet large enough to bias association tests.
4. The database may contain few people of your patients' ancestry, so "rare" there does not mean rare in your population.

</details>

{% endtab %}

{% tab title="2 · Concepts" %}

## 2.1 Alleles, genotypes and frequencies

At a SNP with alleles `A` and `a`, each person carries two copies, giving genotypes `AA`, `Aa`, `aa`. If you count alleles in a sample of N people (2N chromosomes):

> **p** = (2 × n_AA + n_Aa) / 2N,  **q** = 1 − p

The **minor allele frequency (MAF)** is the smaller of p and q. Rare variants (MAF < 1%) matter for severe single-gene disease; common variants (MAF ≥ 5%) are the raw material of GWAS and polygenic scores.

{% hint style="warning" %}
**Which allele is the "reference" and which is "effect"?** PLINK reports `A1` (by default the minor allele in the file) and `A2`. These labels are *per dataset*; the same SNP can have swapped labels in another dataset. We return to this in Week 9.
{% endhint %}

## 2.2 Hardy-Weinberg equilibrium

In a large, randomly mating population with no selection, migration or mutation, genotype frequencies after one generation are:

| Genotype | Expected frequency |
|---|---|
| AA | p² |
| Aa | 2pq |
| aa | q² |

We use HWE as a **quality-control screen**. A SNP whose observed genotypes disagree strongly with HWE in **controls** (or in a single ancestry group) is usually *mis-genotyped* - for example, two nearby genes that the assay cannot tell apart produce an excess of heterozygotes. We test in controls only, because a true disease association distorts HWE in cases.

Two causes of departure to keep apart:

- **Genotyping artefact:** persists within each ancestry group; usually an *excess* of heterozygotes.
- **Population structure (Wahlund effect):** mixing two groups with different frequencies produces a *deficit* of heterozygotes in the pooled sample, but each group alone looks fine.

## 2.3 Linkage disequilibrium

Chromosomes are inherited in blocks. Alleles at nearby SNPs are correlated because recombination has not had time to shuffle them. We measure that correlation as **r²** (0 = independent, 1 = perfect). LD has three practical consequences:

1. A GWAS signal is a **region**, not a single causal variant (Week 8).
2. Many SNPs are redundant; for PCA we **prune** to keep one of each correlated group.
3. LD patterns differ between ancestries, so scores built in one group transfer imperfectly to another (Week 9).

## 2.4 Fst

Fst measures how much of the genetic variation lies *between* groups rather than within them. It ranges from 0 (identical frequencies) to 1 (fixed differences). Values between continental human groups are small (a few hundredths), because most human genetic variation is within populations. Fst is a property of a *pair of defined groups* in a *particular dataset*; it does not define "races".

## 2.5 Principal component analysis

PCA finds the directions along which people vary most, using many SNPs at once. Plot PC1 against PC2: people with similar ancestry cluster together. Rules of practice:

1. Prune for LD first (otherwise a single region dominates).
2. Remove very rare SNPs (MAF < 5% here).
3. Plot, do not just compute. Outliers and clusters are visible by eye.
4. The percentage of variance of each PC depends on how many PCs you computed - report it carefully.
5. PCs are *statistical summaries*, not labelled ancestries.

## 2.6 Reference databases

[gnomAD](https://gnomad.broadinstitute.org) and the [1000 Genomes Project](https://www.internationalgenome.org) report allele frequencies by genetic ancestry group. Their value depends on who was sampled. A variant labelled "absent" may simply not have been seen in the few people from your region. [H3Africa](https://h3africa.org) and similar efforts exist precisely because African genetic diversity is under-represented.

{% hint style="info" %}
**Public health lens.** "Absence from gnomAD" is evidence only about gnomAD's participants. Reporting a variant as "novel" should be preceded by a check of regional and local data.
{% endhint %}

{% endtab %}

{% tab title="3 · Conversation" %}

*Tunde has pasted a plot into the shared notes: two tidy blobs of points, one red, one green, far apart on the horizontal axis. Zainab leans in.*

**Zainab:** Pretty. What am I looking at?

**Tunde:** The PCA of our cohort. A thousand people, and the computer was never told who is who. It separated them anyway.

**Zainab:** So there are two kinds of people in the cohort?

**Dr. Mensah:** There are two groups with slightly different allele frequencies. "Kinds" is a dangerous word. Think of it as: if you had to summarise a person's genome in one number, the best number distinguishes these two groups. Why does that matter to a public health scientist?

**Zainab:** Because if I compare cases and controls and the cases mostly come from one group…

**Dr. Mensah:** …you find "associations" that are really just the group. We will come to that in Week 8. For today, stay with the building blocks. Zainab, you have a SNP and its genotype counts: 64 people with `CC`, 361 with `CT`, 75 with `TT`. Is the SNP behaving?

**Zainab:** I'd count the alleles first. C is 2 × 64 plus 361, that's 489, out of 1,000 chromosomes. So C is about 0.49.

**Tunde:** And Hardy-Weinberg predicts how many heterozygotes?

**Zainab:** 2pq, so 2 × 0.49 × 0.51, about 0.50. So 250 people.

**Tunde:** And we observe 361.

**Zainab:** That's a hundred more than expected. Wait - I'd say that is wrong, not interesting.

**Dr. Mensah:** Say more.

**Zainab:** Biology doesn't produce a surplus of heterozygotes in a whole population by itself. It would take heterozygote advantage that strong. More likely the assay is calling two similar genes as one. The "heterozygote" is a person who has one version in gene A and another in gene B.

**Dr. Mensah:** That is an excellent instinct - and it is the usual explanation. Now suppose it were the opposite: fewer heterozygotes than expected. What then?

**Zainab:** (thinking) Maybe the population is mixed. Two groups with different frequencies, and I pooled them.

**Tunde:** The Wahlund effect. Which is why the first thing I did was test the SNPs in each group *separately*. For the SNP Zainab just worked out, the excess of heterozygotes is still there in both groups.

**Zainab:** So that is the assay, not the ancestry. We drop it.

**Dr. Mensah:** And why test in controls only?

**Zainab:** Because a real disease SNP might distort the genotype frequencies in cases. Is that right? We'd throw away the very signal we want.

**Dr. Mensah:** Exactly right. QC must not destroy what it is looking for.

**Tunde:** Okay, quick confession. First time through I ran the test on everybody, cases and controls together, and the numbers inflated. The right design is cases excluded.

**Zainab:** What about the "Fst" in your notes? You wrote 0.04.

**Tunde:** It means that about four percent of the variation in this cohort lies *between* the two groups, and ninety-six percent lies *within* them.

**Zainab:** Ninety-six percent within. That sounds like the opposite of the plot, where the two blobs are completely separated.

**Dr. Mensah:** That is the most important idea this week. Look again: PC1 separates the groups perfectly *because it combines thousands of SNPs*, each of which differs only slightly. Add up many tiny differences and you can tell the groups apart, yet any single SNP tells you almost nothing about an individual. Both statements are true at once.

**Zainab:** So the groups are distinguishable statistically, but they do not have different "kinds" of genes.

**Dr. Mensah:** Say it in the language of the people who will read your report.

**Zainab:** "Individuals from these two groups differ slightly in the frequency of many variants. Most variation is shared. Do not use a single SNP to infer someone's group." Is that safe?

**Dr. Mensah:** I would sign that. One more thing - the three little dots at the top of the plot.

**Zainab:** Far up the vertical axis, far from everyone. Three people.

**Tunde:** In a real project I would not delete them. I would ask where they come from. They might be a third ancestry, or a sample mix-up, or relatives of each other. The outlier is a question, not a nuisance.

**Dr. Mensah:** Good. Bring the question to the forum.

### Talking points for the forum

1. A variant is absent from gnomAD but common among your patients. List three explanations.
2. Why is a small Fst (0.04) still enough to bias a case-control study?
3. How would you write a report sentence about two groups on a PCA plot that avoids implying fixed "types" of people?

{% endtab %}

{% tab title="4 · Hands-on lab" %}

{% hint style="success" %}
**Lab goal.** Explore `data/gwas` with PLINK and R. Everything below was run on the course data with PLINK 1.90b7.2, R 4.3.3 and ggplot2 3.4.4. Work **from the repository root**. The data contain 1,000 people and 3,160 SNPs on chromosomes 1-22 and X; we use the autosomes (`--chr 1-22`), which leaves 2,860 SNPs.
{% endhint %}

```bash
mkdir -p results/week04 && cd results/week04
D=../../data/gwas
```

(Keep the variable `D` for the whole lab; if you open a new terminal, set it again.)

## Part A - Allele frequencies (30 min)

### Step 1. Compute frequencies

```bash
plink --bfile $D/cohort --chr 1-22 --freq --out freq 2>&1 | grep -i "variants\|people"
head -4 freq.frq
```

```text
2860 out of 3160 variants loaded from .bim file.
1000 people (478 males, 522 females) loaded from .fam.
 CHR        SNP   A1   A2          MAF  NCHROBS
   1   ts01_001    C    A        0.379     1984
   1   ts01_002    T    C       0.3139     1994
   1   ts01_003    G    A       0.2402     1990
```

`NCHROBS` is the number of chromosomes observed (2 × people with a genotype). The first SNP has 1,984 of 2,000, so 8 are missing.

### Step 2. The MAF spectrum

```bash
awk 'NR>1{m=($5<0.5)?$5:1-$5; if(m<0.01)a++; else if(m<0.05)b++; else c++}
     END{print "MAF<1%:",a+0,"  1-5%:",b+0,"  >=5%:",c+0}' freq.frq
```

```text
MAF<1%: 0   1-5%: 131   >=5%: 2729
```

This toy panel has been designed with common SNPs (95% have MAF ≥ 5%). A real array or exome would have many more rare variants.

### Step 3. Draw it in R

```bash
Rscript -e '
suppressMessages({library(ggplot2)})
fr <- read.table("freq.frq", header = TRUE)
print(summary(fr$MAF))
p <- ggplot(fr, aes(MAF)) + geom_histogram(bins = 25, fill = "#2b6cb0") +
  theme_minimal() + labs(title = "Minor allele frequency spectrum", x = "MAF", y = "SNPs")
ggsave("maf.png", p, width = 6, height = 4, dpi = 110)'
```

```text
   Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
0.01454 0.15002 0.26580 0.26484 0.38330 0.50000 
```

**Stop and check:** `maf.png` shows a roughly flat distribution from about 0.05 to 0.5. Why can the MAF never exceed 0.5?

## Part B - Hardy-Weinberg screening (40 min)

### Step 4. Test in controls only

```bash
plink --bfile $D/cohort --chr 1-22 --filter-controls --hardy --out hwe 2>&1 | grep -i "removed"
head -3 hwe.hwe
```

With `--filter-controls`, PLINK writes rows labelled `ALL`, `AFF` and `UNAFF`; because only controls remain, we use the `ALL` rows. Count SNPs by threshold:

```bash
awk 'NR>1 && $3=="ALL"{n++; if($9<1e-6)f++; if($9<0.05)k++} END{print "SNPs",n,"  p<1e-6:",f,"  p<0.05:",k}' hwe.hwe
```

```text
SNPs 2860   p<1e-6: 30   p<0.05: 384
```

By chance, about 5% of 2,860 tests (≈143) would be below 0.05, yet 384 are, and 30 are below 1×10⁻⁶. The threshold 1×10⁻⁶ is a conventional QC cut-off for controls.

### Step 5. Look at the worst offenders

```bash
sort -g -k9,9 hwe.hwe | head -3 | cut -c1-100
```

```text
 CHR        SNP     TEST   A1   A2                 GENO   O(HET)   E(HET)            P 
  17   ts17_053      ALL    C    T            64/361/75    0.722   0.4998    1.263e-23
  17   ts17_053    UNAFF    C    T            64/361/75    0.722   0.4998    1.263e-23
```

`GENO` shows 64 `CC`, 361 `CT`, 75 `TT`; **O(HET)** is the observed heterozygosity (0.722) and **E(HET)** the expected (0.50): a large *excess* of heterozygotes - the signature of a genotyping artefact. The sample size is 500 controls.

### Step 6. Is it structure or error? Test within each group

The course has an answer key of true groups. (In real data you would use clusters from a PCA instead; see Part D.) Build a clusters file and rerun the test within each group on the 30 failing SNPs:

```bash
awk 'NR>1{print $1,$1,$2}' $D/answers/true_ancestry.tsv > clusters.txt
awk 'NR>1 && $3=="ALL" && $9<1e-6{print $2}' hwe.hwe > hwefail.txt
for g in POP1 POP2; do
  awk -v g=$g '$3==g{print $1,$2}' clusters.txt > keep_$g.txt
  plink --bfile $D/cohort --chr 1-22 --filter-controls --keep keep_$g.txt \
        --extract hwefail.txt --hardy --out h_$g >/dev/null 2>&1
  awk -v g=$g 'NR>1 && $3=="ALL"{n++; if($9<1e-6)f++; if($9<0.001)f3++}
       END{print g, "of", n, "failing SNPs: still p<1e-6:", f, "  p<0.001:", f3}' h_$g.hwe
done
```

```text
POP1 of 30 failing SNPs: still p<1e-6: 22   p<0.001: 25
POP2 of 30 failing SNPs: still p<1e-6: 19   p<0.001: 25
```

(Each group alone has fewer people, so p-values are less extreme.) Most failing SNPs *stay* failing inside each group - 25 of 30 reach p < 0.001 in both - so these are genotyping artefacts, not a mixture effect. The answer key plants exactly **25** SNPs with excess heterozygosity; the other 5 flagged SNPs are chance or mild stratification.

**What would you do?** Remove all 30 before analysis - the QC rule is conservative by design, and the cost of losing 5 SNPs is small.

## Part C - LD and Fst (45 min)

### Step 7. Linkage disequilibrium on chromosome 6

```bash
plink --bfile $D/cohort --chr 6 --r2 --ld-window-kb 1000 --ld-window 99999 \
      --ld-window-r2 0 --out ld6 2>&1 | grep -i "written"
awk 'NR>1{d=$5-$2; if(d<0)d=-d; b=(d<100000)?"<100kb":(d<500000)?"100-500kb":">=500kb";
          s[b]+=$7; n[b]++}
     END{for(k in s) printf "%s  pairs=%d  mean r2=%.3f\n",k,n[k],s[k]/n[k]}' ld6.ld
```

```text
>=500kb  pairs=962  mean r2=0.003
100-500kb  pairs=483  mean r2=0.002
<100kb  pairs=584  mean r2=0.183
```

Pairs closer than 100 kb have a mean r² of 0.18; beyond 100 kb it is ≈0. LD decays with distance. (The row order from `awk` may differ on your machine.) Real genomes have much more variable LD, with long blocks in some ancestries and short ones in others - a topic for Week 9.

### Step 8. Fst between two groups

```bash
awk '$3=="POP1"||$3=="POP2"' clusters.txt > c2.txt
plink --bfile $D/cohort --chr 1-22 --within c2.txt --fst --out fst2 2>&1 | grep -i "fst estimate"
sort -g -k5,5 -r fst2.fst | head -3
```

```text
Mean Fst estimate: 0.0412682
Weighted Fst estimate: 0.0452946
CHR	SNP	POS	NMISS	FST
...
20	ts20_020	1182752	994	0.385855
10	ts10_030	3601301	994	0.382427
17	ts17_083	7644374	992	0.348536
```

(The `sort` output shows the three highest values; the header line may appear elsewhere in your listing.) **Interpret:** the genome-wide Fst is about 0.045, but individual SNPs reach 0.39 - a handful of highly differentiated SNPs and many with almost none. This heterogeneity is why a single SNP can mislead you about ancestry, while thousands together separate the groups.

## Part D - PCA (45 min)

### Step 9. Prune, then PCA

```bash
plink --bfile $D/cohort --chr 1-22 --geno 0.05 --mind 0.05 --maf 0.05 \
      --indep-pairwise 50 5 0.2 --out prune 2>&1 | grep -i "pass filters\|removed\|Pruning"
plink --bfile $D/cohort --chr 1-22 --extract prune.prune.in --pca 10 --out pca 2>&1 | grep -i "Results saved"
awk '{s+=$1;a[NR]=$1} END{for(i=1;i<=4;i++) printf "PC%d %.1f%% of the top 10\n",i,100*a[i]/s}' pca.eigenval
```

```text
12 people removed due to missing genotype data (--mind).
60 variants removed due to missing genotype data (--geno).
128 variants removed due to minor allele threshold(s)
2672 variants and 988 people pass filters and QC.
Pruning complete.  1825 of 2672 variants removed.
[extracting eigenvalues and eigenvectors]--pca: Results saved to pca.eigenval and pca.eigenvec .
PC1 51.3% of the top 10
PC2 6.0% of the top 10
PC3 5.6% of the top 10
PC4 5.5% of the top 10
```

`--indep-pairwise 50 5 0.2` slides a window of 50 SNPs in steps of 5 and removes one of each pair with r² > 0.2. Note: the percentages are shares of the *ten* eigenvalues PLINK reported, not of all variance. PC1 dominates; PC2-PC10 look like noise.

### Step 10. Plot and compare with the truth

```bash
Rscript -e '
suppressMessages({library(readr);library(dplyr);library(ggplot2)})
ev <- read.table("pca.eigenvec", col.names = c("FID","IID",paste0("PC",1:10)))
tr <- read_tsv("../../data/gwas/answers/true_ancestry.tsv", show_col_types = FALSE)
d  <- ev %>% left_join(tr, by = "IID")
print(d %>% group_by(true_group) %>%
  summarise(n = n(), pc1 = round(mean(PC1),4), sd1 = round(sd(PC1),4), pc2 = round(mean(PC2),4)))
print(table(d$true_group, d$PC1 > 0))
p <- ggplot(d, aes(PC1, PC2, colour = true_group, shape = true_group)) +
  geom_point(alpha = .7) + theme_minimal() +
  labs(title = "PCA of the toy cohort", colour = "Group", shape = "Group")
ggsave("pca.png", p, width = 6, height = 4.5, dpi = 110)'
```

```text
# A tibble: 3 x 5
  true_group       n     pc1    sd1     pc2
  <chr>        <int>   <dbl>  <dbl>   <dbl>
1 POP1           509 -0.0306 0.0049  0.0006
2 POP2           488  0.0317 0.006  -0.0027
3 POP3_outlier     3  0.0399 0.005   0.343 

              
               FALSE TRUE
  POP1           509    0
  POP2             0  488
  POP3_outlier     0    3
```

Open `pca.png`. Two compact clusters are separated along PC1; **the sign of PC1 recovers the group perfectly (PC1 > 0 for 488/488 POP2 people and PC1 < 0 for 509/509 POP1)**; note that the *sign* of a PC is arbitrary and can flip when you change the SNP set, so compare patterns, not signs. Three people sit far up PC2 (≈ 0.3) - the ancestry outliers. PC2 onwards carries little signal for everyone else.

**Interpret.** (1) The groups differ systematically. (2) In a GWAS, PC1 would be added as a covariate. (3) The three outliers need investigating before they enter any analysis: a distinct ancestry, relatives, or sample swaps.

## Part E - Write it up (20 min)

Create `results/week04/README.md` with the two figures and five sentences: (1) MAF spectrum; (2) number of SNPs failing HWE and your conclusion (error vs structure); (3) Fst; (4) what PC1 shows; (5) one limitation.

## If it breaks

| Message or symptom | Likely cause | Fix |
|---|---|---|
| `Error: Failed to open ../../data/gwas/cohort.bed` | Wrong directory or `D` unset | `pwd`; `echo $D`; `ls $D` |
| `--within` ignores everyone | Clusters file has wrong columns | Needs `FID IID cluster` (three columns, space separated) |
| Fewer HWE rows than expected | `TEST` column: rows for `AFF`/`UNAFF` | Filter on `$3=="ALL"` |
| `awk` prints `0` for MAF<1% | There really are none | Check with `sort -g -k5,5 freq.frq | head` |
| PCA gives odd axes | Forgot pruning | Redo Step 9 |
| `there is no package called 'ggplot2'` | R packages missing | Re-run the setup for your route |

## Stretch challenge

1. Run the HWE test on **all** samples (omit `--filter-controls`). How many more SNPs fail at 1×10⁻⁶? Why?
2. Repeat the PCA *without* pruning. How do PC1 and the outliers change?
3. Plot PC1 against sample missingness (`plink --missing`). Is there a relationship?

{% endtab %}

{% tab title="5 · Practice" %}

## Exercises

### Basic

**Exercise 1.** A sample of 500 people has 64 `CC`, 361 `CT`, 75 `TT`. Compute the frequency of `C` and the expected number of `CT` under HWE.

**Exercise 2.** Why is HWE tested in controls only?

**Exercise 3.** Which is more reliable evidence for "this SNP is mis-genotyped": a departure that appears in the pooled sample only, or one that persists in each ancestry group separately? Why?

<details>

<summary>Show answers (1-3)</summary>

1. C count = 2 × 64 + 361 = 489 of 1,000 chromosomes, so p = 0.489. Expected CT = 2 × 0.489 × 0.511 × 500 ≈ **250**. Observed 361 - a large excess.
2. A causal variant changes genotype frequencies in cases, so testing there would flag the signal as an error and discard it.
3. A departure that persists in each group; a pooled-only departure can be the Wahlund effect from mixing groups.

</details>

### Intermediate

**Exercise 4.** For SNP `ts06_067`, compute the allele frequency in the whole sample and in each true group. (Hint: `plink --within clusters.txt --freq --extract` a one-line SNP list.)

**Exercise 5.** In the PCA, define an automatic rule to flag ancestry outliers using the first two PCs, and check it against the truth.

**Exercise 6.** Explain the apparent paradox: Fst = 0.045, yet PC1 separates the groups perfectly.

<details>

<summary>Show answers (4-6)</summary>

4. Example: `echo ts06_067 > snp.txt; plink --bfile $D/cohort --within clusters.txt --freq --extract snp.txt --out f6` produces one row per group (`CLST` column). Real output: POP1 MAF 0.2525, POP2 MAF 0.4211 (allele `C`) - this is the SNP planted as causal in Week 8, and it differs a lot between groups, which is why ancestry confounds it.
5. Example rule: flag anyone with a large absolute value on PC2 - for example `awk 'function a(x){return x<0?-x:x} a($4)>0.2' pca.eigenvec` (use the absolute value, because PC signs are arbitrary; a rule of `PC2 > 0.1` can miss outliers if the axis flips). In this cohort the rule flags exactly three people - P0158, P0367 and P0611 - the three `POP3_outlier` people. Always view the plot first; a threshold chosen blindly may misfire.
6. Fst averages differentiation over many SNPs, most of which differ slightly; PCA *adds up* the small, consistent differences across thousands of SNPs, so individuals can be classified even though any one SNP is almost uninformative.

</details>

### Challenge

**Exercise 7.** The `planted_problems.tsv` file lists 25 SNPs with excess heterozygosity. Which of the 30 HWE-failing SNPs are *not* in the list? Propose how to examine them.

**Exercise 8.** Write a short paragraph (≤120 words) for a non-specialist explaining why a variant "absent from gnomAD" is not evidence that it is "novel" in your population.

<details>

<summary>Show answers (7-8)</summary>

7. `comm -23 <(sort hwefail.txt) <(awk -F'\t' '$3~/HWE/{print $2}' $D/answers/planted_problems.tsv | sort)` lists five: ts04_056, ts10_030, ts17_084, ts20_018 and ts20_020. Examine their genotype counts (excess or deficit?), repeat the test within each group, and check their missingness. (Chance plus structure could explain a few at p < 10⁻⁶ when thousands of SNPs are tested.)
8. Include: database samples are not a random sample of the world; some regions are poorly represented; absence means "not seen in these participants"; check local data and report the ancestry composition of any reference used.

</details>

## Self-test (8 questions)

1. HWE expected frequency of `Aa` when p(A) = 0.2: (a) 0.04 (b) 0.16 (c) 0.32 (d) 0.64
2. A big **excess** of heterozygotes in both ancestry groups most suggests: (a) genotyping artefact (b) Wahlund effect (c) strong selection (d) good data
3. LD between two SNPs generally: (a) increases with distance (b) decreases with distance (c) is unrelated to distance (d) is always 1
4. Why prune before PCA? (a) to speed plotting (b) to avoid dominance by correlated regions (c) to add noise (d) to find rare variants
5. Fst = 0 means: (a) groups are identical in frequencies (b) groups never mix (c) all variants are fixed (d) the data are wrong
6. MAF cannot exceed: (a) 0.1 (b) 0.25 (c) 0.5 (d) 1
7. In gnomAD, the best practice is to: (a) use only the total frequency (b) look at ancestry-specific frequencies and sample counts (c) ignore it (d) use it as proof of novelty
8. Outliers on a PCA plot should be: (a) deleted at once (b) investigated (c) renamed (d) averaged in

<details>

<summary>Show answers and reasons</summary>

1. **(c)** 2pq = 2 × 0.2 × 0.8 = 0.32.
2. **(a)** The Wahlund effect gives a *deficit* of heterozygotes and disappears within groups.
3. **(b)** Recombination erodes LD with distance.
4. **(b)** Correlated SNPs from one region would dominate the components.
5. **(a)** Identical allele frequencies in the two groups.
6. **(c)** MAF is by definition the *less* common allele.
7. **(b)** Use ancestry-specific frequencies and their sample sizes.
8. **(b)** An outlier is a question: relatedness, distinct ancestry, swap.

</details>

## Reflection prompt (150-250 words)

Think of a reference database you rely on. Who is in it, and who is missing? Give one concrete example of how that could mislead a public health decision in your setting.

## Portfolio mini-deliverable

`results/week04/`: `maf.png`, `pca.png`, the `hwe.hwe` summary line (counts), and a `README.md` with five sentences (see Part E).

{% endtab %}

{% tab title="6 · Go deeper" %}

## Core resources

- **PLINK 1.9 documentation** ([cog-genomics.org/plink/1.9](https://www.cog-genomics.org/plink/1.9/)): the pages for `--freq`, `--hardy`, `--r2`, `--fst`, `--indep-pairwise` and `--pca` are exactly what you used.
- **Marees AT, et al.** *A tutorial on conducting genome-wide association studies: Quality control and statistical analysis.* International Journal of Methods in Psychiatric Research, 2018 - a step-by-step QC guide (search by title).
- **gnomAD** ([gnomad.broadinstitute.org](https://gnomad.broadinstitute.org)): look up a gene and compare allele frequencies by ancestry group; note the sample counts.
- **1000 Genomes** ([internationalgenome.org](https://www.internationalgenome.org)): the classic public reference panel for LD and ancestry.

## Training

- **EMBL-EBI Training** ([ebi.ac.uk/training](https://www.ebi.ac.uk/training)): look for courses on human genetic variation and population genetics.
- **Galaxy Training Network** ([training.galaxyproject.org](https://training.galaxyproject.org)): search for "population genetics" and "GWAS".

## Equity and diversity

- **H3Africa** ([h3africa.org](https://h3africa.org)): African genomic diversity, data and capacity building.
- **Martin AR, et al.** *Clinical use of current polygenic risk scores may exacerbate health disparities.* Nature Genetics, 2019 (search by title) - previews the Week 9 discussion.

{% endtab %}

{% tab title="7 · Contribute" %}

You can help improve this week. Open an issue with the label **`week-04`** or edit the file directly - see [How to contribute](../contribute/README.md).

## Ideas for experts

1. **A real-data variant:** replace one lab step with a small, openly licensed public panel (check the licence and add it under the [data policy](../contribute/data-policy.md)).
2. **R-only route:** provide an equivalent of Parts A-D that uses Bioconductor packages (for example `SNPRelate`) for readers who cannot install PLINK.
3. **Relatedness:** add an exercise on kinship estimation and why close relatives distort PCA.
4. **Admixture:** add a short, tested ADMIXTURE or similar example.
5. **Visuals:** colour-blind-safe palette and alt text for the PCA figure.
6. **Translations:** the *Concepts* tab (label `translation`).

**Version notes:** tested with PLINK 1.90b7.2 and R 4.3.3 on Ubuntu 24.04 (October 2026). PLINK 2 uses different flags; the commands here are PLINK 1.9.

{% endtab %}

{% endtabs %}
