---
description: The synthetic datasets used in the labs - what they contain, how they were made, and how to check them.
---

# The datasets

{% hint style="warning" %}
**Everything here is synthetic.** No real person, patient or outbreak is represented. Place names ("district A", "Savanna North") and genes ("toyR1") are fictional. The datasets are small on purpose so every lab runs on a laptop in minutes.
{% endhint %}

## Reproducible by design

All files are created by one script with a fixed seed:

```bash
python3 scripts/make_toy_data.py            # needs numpy; takes a few seconds
sha256sum -c data/CHECKSUMS.sha256          # confirms every file is byte-identical
```

Because the data are deterministic, every number printed in the labs can be reproduced by anyone, and any accidental edit is detected by the checksum.

## Overview

| Folder | What it is | Size | Used in |
|---|---|---|---|
| `data/seq/` | A 6 kb reference "genome" with two genes, and paired-end reads for three samples (A good, B with a minor sub-population, C poor quality) | ~1 MB | 1, 2, 5, 6, 7, 12 |
| `data/gwas/` | A case-control cohort of 1,000 people in PLINK binary format, with covariates and deliberately planted quality problems | ~1 MB | 4, 8, 12 |
| `data/prs/` | Base GWAS summary statistics (10,000 people) and a target cohort of 800 people from two ancestry groups | ~0.5 MB | 9, 12 |
| `data/outbreak/` | 73 pathogen isolates: a 4,000-bp alignment and metadata | <1 MB | 1, 10, 12 |
| `data/linelist/` | A deliberately messy surveillance line list (600 cases) | <1 MB | 3, 10, 11, 12 |
| `data/linux/` | Practice files for the command line: a sample sheet, a run log, a "messy" project folder, tiny FASTQ files | <1 MB | 2 |

## `data/seq/`

| File | Contents |
|---|---|
| `ref/toy_ref.fa` | The 6,000-bp reference sequence `chrToy` |
| `ref/toy_ref.gff3` | Annotation of two genes: `toyR1` (+ strand, 1001-1900) and `toyR2` (- strand, 3501-4199) |
| `ref/toy_cds_toyR1.fa` | The coding sequence of `toyR1` |
| `ref/adapters.fa` | Illumina-style adapter sequences |
| `reads/sample{A,B,C}_R{1,2}.fastq.gz` | 2 × 100 bp paired-end reads; A ~45× depth, B ~39× with a ~30% minor sub-population, C ~7× with poor quality, short fragments and contaminant reads |
| `samples.tsv` | Sample sheet |
| `answers/truth_variants.tsv` | The variants that were really planted (**do not open until the lab says so**) |

## `data/gwas/`

`cohort.{bed,bim,fam}` (PLINK binary), `covariates.tsv` (age, sex, site). 1,000 people (500 cases, 500 controls), 3,160 SNPs: 2,860 autosomal in linkage-disequilibrium blocks plus 300 independent X-chromosome SNPs (coded chromosome 23). Planted: samples and SNPs with high missingness, SNPs failing Hardy-Weinberg, sex-label mismatches, duplicate individuals, sibling pairs, ancestry outliers, and ancestry structure that confounds a naive analysis. Answer key: `answers/`.

## `data/prs/`

`base_gwas_sumstats.tsv` (SNP, CHR, BP, A1, A2, FREQ_A1, BETA, SE, P, N), target genotypes (`target.*`) and phenotypes (`target_pheno.tsv`). The base file contains labelled allele-coding traps (alleles swapped, strands flipped). The target holds two ancestry groups, G1 (like the base study) and G2 (more distant), so you can measure how a risk score travels.

## `data/outbreak/`

`outbreak_alignment.fasta`, `outbreak_metadata.tsv`, `outbreak_reference.fasta`. A fictional bacterial outbreak with clusters, sporadic cases, one resistance mutation that arises more than once, and planted data errors.

## `data/linelist/`

`linelist_messy.csv`: mixed date formats, impossible ages, inconsistent categories, duplicates, and uneven sequencing coverage across districts (a surveillance-bias lesson).

## Rules

- **Read-only.** Never edit or write into `data/`; write outputs to `results/weekNN/`.
- **Answer keys** are in `data/**/answers/`. Open them only at the "check your answer" step.
- **Adding or changing data:** see the [data policy](../contribute/data-policy.md).
