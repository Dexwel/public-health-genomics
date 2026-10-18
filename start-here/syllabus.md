---
description: Week-by-week objectives, tools, datasets and deliverables at a glance.
---

# Syllabus and schedule

## Structure at a glance

The course has four movements.

| Movement | Weeks | Purpose |
|---|---|---|
| **I. Foundations and tools** | 1-3 | Why public health genomics; Linux; R |
| **II. From reads to variants** | 4-7 | Population genetics, sequencing, alignment, variant calling, annotation |
| **III. From variants to populations** | 8-10 | GWAS, polygenic scores and screening, pathogen genomics and surveillance |
| **IV. From evidence to action** | 11-12 | Ethics, governance, implementation; capstone |

## Week by week

| Wk | Title | Key skills | Main tools | Dataset | Deliverable |
|---|---|---|---|---|---|
| 1 | What is public health genomics? | Frame genomic questions; appraise a screening programme; read a VCF line and HGVS name | text tools, spreadsheet | `data/seq`, `data/outbreak` (peek) | Screening appraisal |
| 2 | Linux and the command line | Navigate, search, pipe, loop, script; basic Git | bash, grep, awk, git | `data/linux`, `data/seq` | Script + run log |
| 3 | R for genomic and surveillance data | Clean messy data; tidy verbs; plots | R, dplyr, ggplot2 | `data/linelist` | Clean line list, epi curve |
| 4 | Human genetic variation and population genetics | Allele frequency, HWE, LD, Fst, PCA | PLINK, R | `data/gwas` | Frequency, HWE, PCA plots |
| 5 | Sequencing and quality control | Read FASTQ; Phred; QC and trimming; pass/fail policy | FastQC, fastp, R | `data/seq` | QC decision table |
| 6 | Alignment and variant calling | Align, sort, index, call, normalise, validate | bwa, samtools, bcftools | `data/seq` | Pipeline script, VCF |
| 7 | Variant annotation and interpretation | Consequences, HGVS, population frequency, ACMG/AMP logic | bcftools csq, R | `data/seq` | Annotated report |
| 8 | Genome-wide association studies | QC, structure, PCA, association, Manhattan/QQ | PLINK, R | `data/gwas` | QC log, plots |
| 9 | Polygenic risk scores and screening | Harmonise, clump, score, validate, portability | R, PLINK | `data/prs` | PRS + equity note |
| 10 | Pathogen genomics and surveillance | SNP distances, NJ tree, clusters, resistance, bias | R (ape), IQ-TREE 2 (optional) | `data/outbreak` | Outbreak briefing |
| 11 | Ethics, equity and implementation | Consent, governance, re-identification risk, implementation planning | R, templates | Your Week 3 clean line list | Data-sharing decision, implementation roadmap |
| 12 | Capstone | Plan, execute, document, peer review | everything | choose a track | Project + review |

## Prerequisites

- Basic epidemiology and statistics: proportions, risk, odds ratios, confidence intervals, p-values.
- Willingness to type commands and read error messages.
- A computer (8 GB RAM is plenty) or a web browser (see [setup](setup.md), the Codespaces option).
- **No** prior programming, Linux or genomics.

## Competencies (what the capstone checks)

| # | Competency | Weeks |
|---|---|---|
| C1 | Frame genomic questions and evidence needs for public health | 1, 9, 11 |
| C2 | Work reproducibly on the command line and in R | 2, 3 |
| C3 | Describe and test population genetic structure | 4, 8 |
| C4 | Assess sequencing data quality and make pass/fail calls | 5 |
| C5 | Produce and validate variant calls | 6 |
| C6 | Annotate and interpret variants with appropriate caution | 7 |
| C7 | Run and critique association and risk-score analyses | 8, 9 |
| C8 | Analyse pathogen genomes and communicate outbreak findings | 10 |
| C9 | Apply ethical, legal and governance principles; plan evaluation | 11 |
| C10 | Communicate, document and peer-review scientific work | 12 |

## Suggested calendars

| Pace | Calendar |
|---|---|
| Intensive | 12 weeks, ~8 h/week |
| Part-time | 24 weeks, ~4 h/week (one week's content every two weeks) |
| Workshop | Weeks 2-3 as a 2-day bootcamp, Weeks 5-6 as a 2-day bootcamp, others online |
