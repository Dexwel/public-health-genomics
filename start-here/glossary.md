---
description: Plain-language definitions of the terms used across the course.
---

# Glossary

Terms are alphabetical. The week where each is first taught is in brackets.

**ACMG/AMP** - American College of Medical Genetics and Genomics / Association for Molecular Pathology; their 2015 guideline classifies variants as pathogenic, likely pathogenic, uncertain significance (VUS), likely benign or benign. [7]

**Adapter** - Short synthetic DNA attached to fragments for sequencing; if a fragment is shorter than the read, the read runs into adapter, which must be trimmed. [5]

**Allele** - One version of a gene or variant at a position. [1, 4]

**Allele frequency (AF)** - The proportion of copies of a gene in a population that are a given allele. Minor allele frequency (MAF) is the frequency of the less common allele. [4]

**Alignment (mapping)** - Finding where each read best matches a reference genome. [6]

**AMR (antimicrobial resistance)** - Ability of a microbe to survive a drug that would normally stop it; genomic AMR prediction links resistance genes or mutations to phenotype. [10]

**Ancestry** - Genetic similarity to reference groups, usually continuous; not the same as race or ethnicity (social categories). [4]

**BAM / SAM / CRAM** - File formats for aligned reads (text SAM; compressed binary BAM; reference-compressed CRAM). [6]

**Base calling / Phred score (Q)** - The machine's guess of each base and its confidence; Q = −10·log10(error probability). Q20 = 1% error, Q30 = 0.1%. [5]

**BED / BIM / FAM** - PLINK's binary genotype files (.bed genotypes, .bim variants, .fam people). [4]

**Bonferroni / genome-wide significance** - Correcting for many tests; for GWAS in people of European ancestry the conventional threshold is P < 5×10⁻⁸. [8]

**Case-control study** - Compares people with a disease (cases) to people without (controls). [8]

**Clumping** - Keeping one representative SNP per correlated region (by P-value) so variants are not counted twice in a polygenic score. [9]

**Cluster (outbreak)** - Isolates so genetically similar that they are likely linked by recent transmission. [10]

**Consequence** - The predicted effect of a variant on a gene product (synonymous, missense, stop-gained, frameshift...). [7]

**Coverage / depth** - How many reads cover a position (depth); the fraction of the genome covered at least once (breadth). [5, 6]

**CIGAR** - A string that describes how a read aligns (e.g. 60M2D40M: 60 matches, 2 deleted, 40 matches). [6]

**CNV (copy-number variant)** - A gain or loss of a segment of DNA. [1]

**Denominator problem** - Not knowing how many people could have been sequenced or tested, so rates are misleading. [10]

**Diploid / haploid** - Two copies of each chromosome (humans) vs one (most bacteria and viruses). [6]

**Duplicate (read)** - Reads from the same original molecule; they can inflate confidence in a variant. [5, 6]

**EQA** - External quality assessment (proficiency testing) for laboratories. [11]

**Exome / genome** - Sequencing the protein-coding portion (~1-2% of the genome) or all of it. [5]

**FASTA / FASTQ** - Text formats for sequences (FASTA) and for sequencing reads with qualities (FASTQ). [2, 5]

**FAIR / CARE** - Principles for data: Findable, Accessible, Interoperable, Reusable / Collective benefit, Authority to control, Responsibility, Ethics. [11]

**Fine-mapping** - Narrowing a GWAS signal to the likely causal variant(s). [8]

**Fst** - A measure (0-1) of how much allele frequencies differ between populations. [4]

**GFF3 / GTF** - Annotation file formats listing genes, exons and other features. [7]

**Genome-wide association study (GWAS)** - Testing millions of variants across many people for association with a trait. [8]

**Genotype** - The pair of alleles a person carries at a position (e.g. A/G). [1]

**GWAS Catalog** - A curated database of published GWAS results. [8]

**Hardy-Weinberg equilibrium (HWE)** - The expected genotype proportions p², 2pq, q² when mating is random and nothing else changes; deviations can flag genotyping errors or structure. [4]

**Heritability (h²)** - The fraction of variation in a trait in a population explained by genetic differences; says nothing about individuals. [1]

**HGVS** - Standard variant names, such as `c.1301A>C` (coding DNA) and `p.Lys101Gln` (protein). [7]

**Imputation** - Statistically inferring untyped variants using a reference panel. [8]

**Indel** - A small insertion or deletion. [6]

**Inflation (λ, lambda GC)** - Ratio of observed to expected median association statistic; ~1 is good, well above 1 suggests confounding. [8]

**Isolate** - A pure culture or sample of a pathogen taken from one patient or source. [10]

**Linkage disequilibrium (LD)** - Non-random association of alleles at nearby positions because they are inherited together. [4]

**Line list** - A table with one row per case in surveillance data. [3]

**Manhattan plot / QQ plot** - Plots of GWAS −log10 P by position / of observed vs expected P-values. [8]

**MAPQ** - Mapping quality: the confidence that a read is placed correctly. [6]

**Mendelian disease** - Caused mainly by variants in a single gene. [1]

**Mixed model** - A regression that accounts for relatedness and structure among individuals. [8]

**Neighbour-joining (NJ) tree** - A fast method that builds a tree from pairwise distances. [10]

**Odds ratio (OR)** - Ratio of the odds of disease with one genotype vs another. [8]

**Palindromic SNP** - A SNP whose alleles are complements (A/T or C/G); strand cannot be resolved from alleles alone. [9]

**PCA (principal component analysis)** - A method that summarises genetic variation into a few axes; in GWAS the leading PCs capture ancestry. [4, 8]

**Phenotype** - An observable trait or disease. [1]

**PI_HAT** - PLINK's estimate of the proportion of genome shared identical-by-descent (≈1 duplicates, ≈0.5 first-degree relatives). [8]

**PLINK** - A widely used program for genotype data and GWAS. [4]

**Polygenic risk score (PRS)** - A weighted sum of risk-allele counts across many variants. [9]

**Population stratification** - Differences in ancestry between cases and controls that cause false associations. [8]

**Portability (PRS)** - How well a risk score works in a population different from the one it was built in. [9]

**PPV / NPV** - Positive/negative predictive value: the probability that a positive/negative result is correct; depends on prevalence. [1, 9]

**Reference genome** - A consensus sequence used as a coordinate system for alignment. [6]

**SNP / SNV** - Single-nucleotide polymorphism / variant: a single-base change. [1]

**Sensitivity / specificity** - The fraction of true positives detected / true negatives correctly cleared. [1]

**Sequencing by synthesis** - Illumina's method: reading bases as a copy strand is built. [5]

**Surveillance bias** - Distortion arising because some places, groups or cases are sampled more than others. [10]

**Variant calling** - Deciding, from aligned reads, where a sample differs from the reference. [6]

**VCF** - Variant Call Format: the standard text file of variants, with genotype and quality per sample. [6]

**VUS (variant of uncertain significance)** - A variant with insufficient evidence to call pathogenic or benign. [7]

**Wahlund effect** - Apparent excess of homozygotes (HWE deviation) when subpopulations are mixed. [4]

**Whole-genome sequencing (WGS)** - Sequencing essentially all of an organism's DNA. [5]

**Wilson-Jungner criteria** - Ten principles (1968) for deciding whether a condition suits population screening. [1, 9]
