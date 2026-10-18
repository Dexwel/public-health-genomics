---
description: Predict what each variant does to a gene with bcftools csq, name it in HGVS, and learn the evidence logic (ACMG/AMP) that turns a variant into a classification - without over-claiming.
---

# Week 7 — Annotation and interpretation

{% hint style="info" %}
**At a glance** · **Time:** ~6-8 h · **Prerequisites:** Week 6 (VCFs in `results/week06/`) · **You will produce:** annotated VCFs, a hand-checked codon table, a variant report and a short interpretation memo · **Tools:** bcftools csq, bgzip/tabix, R · **Data:** `data/seq` (reference, gene annotation GFF3)
{% endhint %}

{% tabs %}

{% tab title="1 · Start here" %}

## Why this matters

A VCF line says *where* a sample differs; it does not say *whether it matters*. A synonymous change usually does nothing; a premature stop codon can destroy a protein. Public health uses this step for drug-resistance genes, for vaccine-escape mutations, and - in human genomics - for screening and diagnosis. The same variant can be harmless, uncertain or dangerous depending on **where** it falls, **how common** it is and **what is known** about it.

This week you annotate the variants you called in Week 6, check the predictions yourself by hand, learn the standard names (HGVS), and meet the evidence framework (ACMG/AMP) used to classify variants. The key discipline is humility: a *predicted* effect is not a *proven* effect.

## Learning objectives

By the end of this week you will be able to:

1. **Explain** the genetic code, codons and the main consequence types (synonymous, missense, nonsense, frameshift, in-frame indel).
2. **Annotate** a VCF with `bcftools csq` using a reference and a GFF3 gene file.
3. **Verify** an annotation by hand: coordinate → codon → amino acid, including a gene on the minus strand.
4. **Write** variants in HGVS notation (`c.` and `p.`).
5. **Describe** the ACMG/AMP evidence logic and why population frequency is central.
6. **Build** a variant report and **write** a cautious interpretation.

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
| **Codon** | Three bases that code for one amino acid |
| **Synonymous** | Changes the DNA but not the amino acid |
| **Missense** | Changes one amino acid to another |
| **Nonsense / stop-gained** | Creates a stop codon too early |
| **Frameshift** | Insertion or deletion not a multiple of 3: scrambles everything downstream |
| **HGVS** | Standard variant names, e.g. `c.301A>C`, `p.Lys101Gln` |
| **ClinVar** | Public archive of variant interpretations |
| **ACMG/AMP** | The standard framework for classifying human variants |

## Pre-check

1. A codon changes from `CCC` to `CCA`; both code for proline. What is this called?
2. A 1-base insertion in a coding region: in-frame or frameshift?
3. A gene is on the minus strand. The VCF says the reference base is `A`. What base does the *gene* read?
4. If a variant is common (frequency 10%) in healthy people, can it plausibly cause a rare severe disease?

<details>

<summary>Show answers</summary>

1. Synonymous (silent).
2. Frameshift - the reading frame moves by one base.
3. `T` (the complement); a minus-strand gene is read on the opposite strand.
4. Very unlikely for a fully penetrant rare disease; high frequency in healthy people is strong evidence against that. (This is the idea behind the ACMG criterion BA1.)

</details>

{% endtab %}

{% tab title="2 · Concepts" %}

## 2.1 The genetic code in practice

DNA is read in codons. Of 64 codons, 61 code for 20 amino acids and 3 are stops. Because several codons code for the same amino acid, many changes are silent. The effect of a change depends on the type:

| Consequence | What happens | Typical impact |
|---|---|---|
| Synonymous | Same amino acid | Usually none (can affect splicing or expression) |
| Missense | One amino acid replaced | Ranges from none to severe, depending on position and chemistry |
| Stop-gained (nonsense) | Premature stop codon | Truncated protein; often loss of function |
| Frameshift | Indel not a multiple of 3 | Downstream sequence scrambled; usually loss of function |
| Inframe insertion/deletion | Residues added/removed | Often milder, but can disrupt a domain |
| Intergenic / non-coding | Outside genes | Often none; may affect regulation |

## 2.2 Annotating with bcftools csq

`bcftools csq` takes (1) the reference FASTA, (2) a gene annotation in GFF3, and (3) a VCF, and writes a `BCSQ` field. The fields are separated by `|`:

```text
consequence | gene | transcript | biotype | strand | amino_acid_change | dna_change
```

An asterisk before the consequence (`*frameshift`) means the change is *incomplete* (for example, the effect runs past the end of the transcript or involves a deletion that spans more than one annotation); read those with care. Use `-p a` (phase "assume") for haploid data. Your VCF must be bgzip-compressed and indexed (`tabix` or `bcftools index`).

Real genomes need an annotation matched to the reference version: **Ensembl** and **RefSeq/MANE** gene sets differ; always record which. For effect prediction in human data, the Ensembl Variant Effect Predictor (**VEP**) is a standard tool ([ensembl.org](https://www.ensembl.org)).

## 2.3 Coordinates: genome, cDNA, protein

Three numbering systems exist, and mixing them is the commonest annotation error:

| System | Prefix | Example | Counts from |
|---|---|---|---|
| Genomic | `g.` | `g.1301A>C` | start of the chromosome |
| Coding DNA | `c.` | `c.301A>C` | the first base of the start codon `ATG` |
| Protein | `p.` | `p.Lys101Gln` | the first amino acid (Met = 1) |

For a plus-strand gene starting at genomic position G, `c.` = genomic position − G + 1. For a **minus-strand** gene the arithmetic runs backwards from the gene end, and the bases are complemented.

### HGVS in brief

| Variant | HGVS |
|---|---|
| substitution | `c.301A>C` |
| protein change | `p.Lys101Gln` (or `p.K101Q`); synonymous: `p.Pro51=`; stop: `p.Tyr202Ter` (`p.Tyr202*`) |
| deletion | `c.450_452del` |
| insertion | `c.751_752insG` |

Always quote the **transcript and its version** (for example `NM_...:c.301A>C`) - `c.` numbers mean nothing without it. Indel notation has a "3' rule" (shift as far downstream as possible) so two tools may number the same deletion slightly differently; csq's protein description (`150QL>150Q`) and an HGVS name for the same event can differ in which residue is called deleted.

## 2.4 Reading frame arithmetic

An insertion or deletion of length *n* is **in-frame** if *n* is a multiple of 3. The toy deletion `AGCT → A` removes 3 bases (in-frame; one amino acid lost). The insertion `T → TG` adds 1 base (frameshift).

## 2.5 Interpretation: from prediction to classification

**Prediction** says what a change *does to the sequence*. **Classification** says whether it *causes disease or a phenotype*, using several kinds of evidence. The ACMG/AMP framework (Richards et al., 2015) combines them:

| Evidence type | Examples (criteria names) | Why it matters |
|---|---|---|
| Population data | **BA1** (frequency > 5%: stand-alone benign), **PM2** (absent or extremely rare in controls) | A variant common in healthy people cannot be a rare severe cause |
| Computational | **PVS1** (null variant in a gene where loss of function causes disease), **PP3** (predictors agree on damage), **PM4** (protein length change from in-frame indel), **BP7** (synonymous, no splice effect) | Predictions are supporting, not decisive |
| Functional | **PS3 / BS3** (well-established assay shows damage / no damage) | Laboratory evidence |
| Segregation and case data | Co-segregation with disease in families, de novo status | Genetic and clinical evidence |
| Database | **PS1/PM5** (same or different change at an amino acid already known pathogenic) | Prior knowledge (check ClinVar for the *evidence*, not just the label) |

Evidence is combined by rules into five classes: **pathogenic, likely pathogenic, uncertain significance (VUS), likely benign, benign.** Later work (Tavtigian et al., 2018) shows the rules can be expressed as a Bayesian points system. Most variants in a typical patient are VUS; **a VUS is not a diagnosis and must not change medical management.**

{% hint style="warning" %}
**Never classify from a predictor alone.** A tool that says "damaging" is one weak line of evidence. Use gene-disease validity (ClinGen), population frequency (gnomAD, with ancestry in mind), ClinVar's submitted evidence, and the clinical context.
{% endhint %}

## 2.6 Pathogens: different questions, same logic

For bacteria and viruses the questions are: *does this mutation confer resistance, escape immunity, or change transmissibility?* The evidence comes from curated catalogues (for example, WHO's catalogue of *Mycobacterium tuberculosis* mutations and resistance), phylogenetic distribution and experiments. The logic "prediction → evidence → graded confidence" is the same.

{% hint style="info" %}
**Public health lens.** Annotation is cheap and automatic; interpretation is slow and needs expertise. Programmes need a *workflow for uncertainty*: who reviews a VUS, how often interpretations are re-reviewed, and how patients are re-contacted if a classification changes.
{% endhint %}

{% endtab %}

{% tab title="3 · Conversation" %}

*On the whiteboard, Tunde has drawn a gene as a long arrow and a vertical line labelled "1301". Zainab holds a printout of a VCF.*

**Zainab:** My VCF says position 1301, A to C. What does that *do*?

**Tunde:** Let's find out. The gene `toyR1` starts at 1001. Position 1301 is the 301st base of the gene.

**Zainab:** So `c.301`.

**Tunde:** Right. Codons are triplets. Which codon contains base 301?

**Zainab:** Divide by three. Ninety-nine and a third, so codon 101. And it's the first base of that codon.

**Tunde:** The codon was `AAA`. Changing the first A to C gives…

**Zainab:** `CAA`. Lysine becomes glutamine. A missense. `p.Lys101Gln`. I could have done that on paper!

**Dr. Mensah:** You just did. And that is the point of today. The software gave the same answer, but now you can *check it*. Next: position 4019 in the other gene. Tunde says it is on the minus strand.

**Zainab:** The VCF says A to T. But the gene reads the other strand, so…

**Tunde:** Complement them.

**Zainab:** The gene sees T to A. And the arithmetic goes backwards from the end of the gene: 4199 minus 4019 plus one: base 181. Codon 61, first base. `TCA` becomes `ACA`. Serine to threonine.

**Dr. Mensah:** If you had forgotten the strand?

**Zainab:** I'd have read A→T as a codon change from `TCA`… no, I'd have used the wrong base entirely and got nonsense.

**Dr. Mensah:** Strand mistakes are among the commonest and quietest in annotation. Good. Now sample B. Position 1606: T to A. What does that do?

**Zainab:** Codon 202, `TAT` to `TAA`. `TAA` is a stop. So the protein stops at amino acid 202.

**Tunde:** And the protein is three hundred amino acids long. So…

**Zainab:** It's cut in a third of the way. Almost certainly non-functional.

**Dr. Mensah:** "Almost certainly." Let me ask you something. Suppose the gene is `toyR1`, and the enzyme turns out to have its important active site in the first hundred amino acids. Is the stop still damaging?

**Zainab:** It could be that the truncated protein still works. Or the cell might need only part of it. I don't know.

**Dr. Mensah:** Excellent answer: *I don't know, here is what I'd look up.* Where?

**Zainab:** The literature on the gene. Functional assays. ClinVar, if this were a human gene. And whether loss of the gene is a known disease mechanism.

**Tunde:** That last one is the criterion PVS1: a null variant counts as very strong evidence only in a gene where *loss of function* causes disease.

**Zainab:** So the same stop codon is damning in one gene and meaningless in another.

**Dr. Mensah:** Now the frameshift at 1751, one inserted G.

**Zainab:** It shifts everything after it. The whole rest of the protein is nonsense. The annotation shows a long string of letters.

**Tunde:** And a star in front of "frameshift". Careful - that means the prediction is incomplete.

**Zainab:** Why incomplete?

**Tunde:** The software translated until the end of the transcript, but the new reading frame has a different end. Treat it as "likely loss of function", not as a fully described protein.

**Zainab:** And the two variants in the middle of nowhere, 2600 and 5200?

**Dr. Mensah:** Outside both genes. In this toy world they do nothing. In real genomes, "intergenic" variants can sit in a regulatory region that matters a great deal, which is why "no annotated effect" is not "no effect". One more: how common is `p.Lys101Gln` in healthy people?

**Zainab:** I'd look it up in gnomAD.

**Dr. Mensah:** And if gnomAD has few people from your region?

**Zainab:** Then absence there tells me little. I'd need local data.

**Dr. Mensah:** You are doing public health genomics. The code was the easy part.

### Talking points for the forum

1. Who should review a VUS in your setting, and how often?
2. A predictor and a laboratory assay disagree. Which do you weight more heavily, and why?
3. How should a result report distinguish "no variant found" from "not covered at sufficient depth" from "variant of uncertain significance"?

{% endtab %}

{% tab title="4 · Hands-on lab" %}

{% hint style="success" %}
**Lab goal.** Annotate the Week 6 calls for samples A and B, verify four of them by hand in R, and build a variant report. Everything below was run with bcftools 1.19, bgzip/tabix (htslib 1.19) and R 4.3.3. You need `results/week06/` (the VCFs and `ref.fa`). Work **from the repository root**.
{% endhint %}

```bash
mkdir -p results/week07 && cd results/week07
S=../../data/seq
W=../week06
```

## Part A - Look at the gene model (15 min)

```bash
cat $S/ref/toy_ref.gff3
```

Two genes: `toyR1` (positions 1001-1900, **plus** strand, a "hypothetical enzyme") and `toyR2` (3501-4199, **minus** strand, a "hypothetical transporter"). Each has a single exon and CDS (the coding sequence).

**Stop and check:** how long is each coding sequence, and is it a multiple of 3? (`1900−1001+1 = 900` = 300 codons; `4199−3501+1 = 699` = 233 codons.)

## Part B - Annotate with bcftools csq (30 min)

### Step 1. Compress and index the VCFs

```bash
for s in sA sB; do
  bgzip -c $W/$s.vcf > $s.vcf.gz
  bcftools index -f $s.vcf.gz
done
```

`bcftools csq` requires a bgzipped and indexed file.

### Step 2. Annotate

```bash
for s in sA sB; do
  bcftools csq -f $W/ref.fa -g $S/ref/toy_ref.gff3 -p a $s.vcf.gz -Ov 2>csq_$s.log > $s.csq.vcf
  echo "== $s"; head -3 csq_$s.log
  bcftools query -f '%POS\t%REF\t%ALT\t%INFO/BCSQ\n' $s.csq.vcf
done
```

```text
== sA
Parsing ../../data/seq/ref/toy_ref.gff3 ...
Indexed 2 transcripts, 2 exons, 2 CDSs, 0 UTRs
Calling...
1153	C	A	synonymous|toyR1|toyR1.1|protein_coding|+|51P|1153C>A
1301	A	C	missense|toyR1|toyR1.1|protein_coding|+|101K>101Q|1301A>C
1449	AGCT	A	inframe_deletion|toyR1|toyR1.1|protein_coding|+|150QL>150Q|1449AGCT>A
2600	T	A	.
4019	A	T	missense|toyR2|toyR2.1|protein_coding|-|61S>61T|4019A>T
5200	G	C	.
== sB
Parsing ../../data/seq/ref/toy_ref.gff3 ...
Indexed 2 transcripts, 2 exons, 2 CDSs, 0 UTRs
Calling...
1301	A	C	missense|toyR1|toyR1.1|protein_coding|+|101K>101Q|1301A>C
1606	T	A	stop_gained|toyR1|toyR1.1|protein_coding|+|202Y>202*|1606T>A
1751	T	TG	*frameshift|toyR1|toyR1.1|protein_coding|+|251LLVAVILTRGVQTGSWPHISAITYPGAHKAGRRTTWATSVRSFYHLPAD*>251CASGCHPHSWCSDRVLAAHFRHNLSRSS*|1751T>TG
2600	T	A	.
5200	G	C	.
```

Read it field by field: position 1301 is a **missense** in `toyR1`: lysine (K) at codon 101 becomes glutamine (Q). Position 4019 is a missense in `toyR2` on the **minus** (`-`) strand: serine 61 becomes threonine. 1606 is a **stop gained** at codon 202 (`Y>*`). 1751 is a **frameshift**; the asterisk before the word and the long string show the downstream protein is replaced. Positions 2600 and 5200 have `.` - no gene.

## Part C - Verify by hand (45 min)

Never accept a tool's output you cannot check. Save this as `results/week07/codon_check.R`:

```r
# codon_check.R - verify a missense/synonymous/stop call by hand (Week 7)
bases <- c("T","C","A","G")
codons <- expand.grid(b3 = bases, b2 = bases, b1 = bases)[, 3:1]
codons <- paste0(codons$b1, codons$b2, codons$b3)
aa <- strsplit("FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG", "")[[1]]
code <- setNames(aa, codons)
three <- c(A="Ala",R="Arg",N="Asn",D="Asp",C="Cys",Q="Gln",E="Glu",G="Gly",H="His",I="Ile",L="Leu",
           K="Lys",M="Met",F="Phe",P="Pro",S="Ser",T="Thr",W="Trp",Y="Tyr",V="Val","*"="Ter")
ref <- paste(readLines("../week06/ref.fa")[-1], collapse = "")
comp <- function(x) chartr("ACGT", "TGCA", x)
revcomp <- function(x) paste(rev(strsplit(comp(x), "")[[1]]), collapse = "")
check <- function(pos, alt, gene_start, gene_end, strand) {
  if (strand == "+") { cpos <- pos - gene_start + 1; ref_b <- substr(ref, pos, pos); alt_b <- alt }
  else               { cpos <- gene_end - pos + 1;   ref_b <- comp(substr(ref, pos, pos)); alt_b <- comp(alt) }
  cds <- substr(ref, gene_start, gene_end); if (strand == "-") cds <- revcomp(cds)
  cod_n <- (cpos - 1) %/% 3 + 1; i <- (cpos - 1) %% 3 + 1
  old <- substr(cds, 3 * cod_n - 2, 3 * cod_n); new <- old; substr(new, i, i) <- alt_b
  cat(sprintf("pos %d: c.%d%s>%s  codon %d %s>%s  p.%s%d%s\n", pos, cpos, ref_b, alt_b, cod_n, old, new,
              three[[code[[old]]]], cod_n, if (code[[new]] == code[[old]]) "=" else three[[code[[new]]]]))
}
check(1153, "A", 1001, 1900, "+")
check(1301, "C", 1001, 1900, "+")
check(1606, "A", 1001, 1900, "+")
check(4019, "T", 3501, 4199, "-")
cat("bases 1747-1756:", substr(ref, 1747, 1756), "\n")
cat("bases 1446-1455:", substr(ref, 1446, 1455), "\n")
```

Run it from `results/week07`:

```bash
Rscript codon_check.R
```

```text
pos 1153: c.153C>A  codon 51 CCC>CCA  p.Pro51=
pos 1301: c.301A>C  codon 101 AAA>CAA  p.Lys101Gln
pos 1606: c.606T>A  codon 202 TAT>TAA  p.Tyr202Ter
pos 4019: c.181T>A  codon 61 TCA>ACA  p.Ser61Thr
bases 1747-1756: ATGGTTGCTA 
bases 1446-1455: CGCAGCTGGT
```

All four agree with bcftools (synonymous P51; K101Q; Y202*; S61T). Note how, for position 4019, the VCF alleles `A>T` become `T>A` from the gene's point of view, and the `c.` number counts back from the end of the gene (`4199 − 4019 + 1 = 181`).

**The two indels, by reasoning.** The reference around 1751 is `…G G T T…` with the first T at 1751 (`ATGGTTGCTA` starts at 1747: A1747 T1748 G1749 G1750 **T1751** T1752). Inserting a G after position 1751 is `c.751_752insG` - one base, so a frameshift. Around 1449 the reference reads `CGC AGCT GGT` (positions 1446-1455): the deletion `AGCT → A` removes the 3 bases `GCT` (1450-1452), which is `c.450_452del` and removes one amino acid: in-frame.

## Part D - Build a variant report in R (45 min)

Collect the annotated calls into a table (the `calls.tsv` file is just `bcftools query` output with the sample name added):

```bash
for s in sA sB; do
  bcftools query -f '%POS\t%REF\t%ALT\t%INFO/BCSQ\t[%GT]\t[%AD]\t%DP\n' $s.csq.vcf | awk -v s=$s 'BEGIN{FS=OFS="\t"}{print s,$0}'
done > calls.tsv
```

Save as `make_report.R`:

```r
# make_report.R - turn annotated calls into a small interpretation table (Week 7)
suppressPackageStartupMessages({library(readr); library(dplyr); library(tidyr)})
calls <- read_tsv("calls.tsv", col_names = c("sample","pos","ref","alt","bcsq","gt","ad","dp"),
                  col_types = cols(.default = col_character()))
rep <- calls %>%
  separate(bcsq, c("consequence","gene","transcript","biotype","strand","aa","dna"),
           sep = "\\|", fill = "right", extra = "drop") %>%
  mutate(consequence = sub("^\\*", "", consequence),
         consequence = ifelse(consequence == ".", "intergenic", consequence),
         priority = case_when(consequence %in% c("stop_gained","frameshift") ~ "HIGH: likely loss of function",
                              consequence %in% c("missense","inframe_deletion") ~ "MODERATE: changes the protein",
                              consequence == "synonymous" ~ "LOW: same amino acid",
                              TRUE ~ "NONE in genes: outside coding regions"),
         dp = as.integer(dp)) %>%
  select(sample, pos, ref, alt, gene, consequence, aa, dp, priority)
print(as.data.frame(rep %>% mutate(aa = substr(aa, 1, 12))), row.names = FALSE)
cat("\nBy priority:\n"); print(table(rep$sample, sub(":.*", "", rep$priority)))
write_csv(rep, "variant_report.csv")
```

```bash
Rscript make_report.R
```

```text
 sample  pos  ref alt  gene      consequence           aa dp
     sA 1153    C   A toyR1       synonymous          51P 46
     sA 1301    A   C toyR1         missense    101K>101Q 51
     sA 1449 AGCT   A toyR1 inframe_deletion   150QL>150Q 34
     sA 2600    T   A  <NA>       intergenic         <NA> 50
     sA 4019    A   T toyR2         missense      61S>61T 56
     sA 5200    G   C  <NA>       intergenic         <NA> 52
     sB 1301    A   C toyR1         missense    101K>101Q 41
     sB 1606    T   A toyR1      stop_gained    202Y>202* 35
     sB 1751    T  TG toyR1       frameshift 251LLVAVILTR 50
     sB 2600    T   A  <NA>       intergenic         <NA> 38
     sB 5200    G   C  <NA>       intergenic         <NA> 31

By priority:
    
     HIGH LOW MODERATE NONE in genes
  sA    0   1        3             2
  sB    2   0        1             2
```

(The `priority` column is printed to the right; it reads LOW, MODERATE, MODERATE, NONE, MODERATE, NONE for A, and MODERATE, HIGH, HIGH, NONE, NONE for B.) **Sample A** carries one synonymous, three protein-changing and two non-coding variants; **sample B** carries a stop-gained and a frameshift - both likely to destroy `toyR1` - plus one missense.

**Stop and check:** both samples share `1301 A>C` (K101Q), `2600` and `5200`. Shared variants hint at shared ancestry (Week 10).

## Part E - A cautious interpretation memo (45 min)

Write `results/week07/memo.md` (≤300 words) for a hypothetical reader. State: (1) what was found in each gene; (2) which results are *predictions only*; (3) what further evidence you would seek for the stop-gained and the frameshift (literature on `toyR1`, functional test, frequency in a regional collection); (4) what you would **not** conclude.

Example opening: *"Sample B carries two variants predicted to disrupt toyR1 (a stop at codon 202 and a frameshift at codon 251). These are predictions from sequence alone. We have not tested whether toyR1 is required for the phenotype of interest, nor how often these changes occur in comparable isolates."*

## If it breaks

| Message or symptom | Likely cause | Fix |
|---|---|---|
| `Failed to open ... .vcf.gz` | VCF not compressed | `bgzip -c in.vcf > in.vcf.gz` |
| `no index` / `could not load index` | Not indexed | `bcftools index in.vcf.gz` |
| `bgzip: command not found` | htslib tools missing | `bash scripts/check_setup.sh`; install `tabix` |
| All consequences `.` | Contig names differ between VCF and GFF3 | Both must say `chrToy` |
| `Unknown ... (phase)` | Missing `-p` | Add `-p a` |
| Different amino-acid numbers | Wrong transcript or version | Fix the GFF3; always record the transcript |
| R error `object 'code' not found` | Script run out of order | Run `codon_check.R` from the top |

## Stretch challenge

1. Add the position and alternative base of a *new* variant in `toyR2` and predict by hand what happens, then confirm with `bcftools csq` (write a small VCF).
2. Use `bcftools csq` on the diploid VCF of B from Week 6 (the sub-population at 2200). Is the minority variant in a gene?
3. Write HGVS names for all six variants in sample A.

{% endtab %}

{% tab title="5 · Practice" %}

## Exercises

### Basic

**Exercise 1.** Classify each as synonymous, missense, nonsense or frameshift: (a) `GAA → GAG` (b) `GAA → TAA` (c) `GAA → GCA` (d) deletion of one base.

**Exercise 2.** A plus-strand gene begins at genomic position 500. What is the `c.` position of genomic position 650?

**Exercise 3.** Is a deletion of 6 bases in a coding region in-frame?

<details>

<summary>Show answers (1-3)</summary>

1. (a) synonymous (Glu→Glu); (b) nonsense (Glu→stop); (c) missense (Glu→Ala); (d) frameshift.
2. `c.151` (650 − 500 + 1).
3. Yes, 6 is a multiple of 3, so two amino acids are removed (if the deletion does not hit a stop).

</details>

### Intermediate

**Exercise 4.** At genomic position 1301 the `toyR1` codon is `AAA` and the variant is `A>C` (first base). What would `A>G` at the same position do, and what would `A>T` do? Write the `p.` names.

**Exercise 5.** Variant `2600 T>A` has consequence `.` in both samples. List two reasons it could still matter in a real genome.

**Exercise 6.** Write the HGVS `c.` and `p.` names for the sample B stop-gained variant.

<details>

<summary>Show answers (4-6)</summary>

4. `A>G`: `AAA → GAA`, Lys → Glu: `p.Lys101Glu` (missense). `A>T`: `AAA → TAA`, a stop codon: `p.Lys101Ter` (nonsense). Same position, three different outcomes - the *alternative allele* matters as much as the position.
5. It might lie in a promoter or enhancer, a non-coding RNA or a splicing region not in the simple gene model; the annotation file may be incomplete.
6. `c.606T>A`, `p.Tyr202Ter` (also written `p.Tyr202*` or `p.Y202*`), with the transcript identifier, for example `toyR1.1:c.606T>A`.

</details>

### Challenge

**Exercise 7.** Apply the ACMG/AMP *logic* (not a final classification) to sample B's stop-gained in `toyR1`: which criteria are relevant, what evidence is missing, and what would you call it?

**Exercise 8.** A human variant is `p.Arg100Trp`, absent from gnomAD (which has few people of the patient's ancestry), predicted damaging by two tools, and with no ClinVar entry. What can you say? What is the most responsible report?

<details>

<summary>Show answers (7-8)</summary>

7. Relevant: PVS1 (null variant) *only if* loss of function of `toyR1` is a known mechanism; PM2 (absence in comparison collections) *only if* you have a suitable comparison set. Missing: gene function evidence, functional assays, case data. Without these the honest label is "predicted loss of function; significance not established" (in ACMG terms, uncertain).
8. Absence from gnomAD is weak evidence because of ancestry; predictors are supporting evidence only; no ClinVar entry means no community evidence. Most responsible: **variant of uncertain significance**, with a recommendation to seek family segregation and functional data and to re-review periodically.

</details>

## Self-test (8 questions)

1. A synonymous variant changes: (a) the amino acid (b) the DNA but not the amino acid (c) the reading frame (d) the gene name
2. A 2-base deletion in a coding region is: (a) in-frame (b) a frameshift (c) synonymous (d) intergenic
3. `c.` numbering counts from: (a) chromosome start (b) the A of the start codon ATG (c) the end of the gene only (d) the protein
4. A minus-strand gene: the VCF's reference base `G` appears to the gene as: (a) G (b) C (c) A (d) T
5. BA1 means: (a) frequency so high the variant is benign (b) absent in controls (c) null variant (d) functional assay
6. A VUS should: (a) trigger treatment (b) not change clinical management; be reviewed over time (c) be called pathogenic (d) be deleted
7. Why record the transcript version? (a) for style (b) `c.` numbers depend on it (c) to save space (d) no reason
8. A predictor says "damaging". The proper weight is: (a) decisive (b) one supporting line of evidence (c) none (d) overrides ClinVar

<details>

<summary>Show answers and reasons</summary>

1. **(b)**
2. **(b)** 2 is not a multiple of 3.
3. **(b)** `c.1` is the A of ATG.
4. **(b)** Complement of G is C.
5. **(a)** Stand-alone evidence for benign.
6. **(b)**
7. **(b)** Different transcripts have different coordinates.
8. **(b)** Computational evidence is supporting.

</details>

## Reflection prompt (150-250 words)

Write a short reporting policy for a laboratory: how will it label predicted effects, who reviews uncertain variants, and how will it communicate a change of classification to the people affected?

## Portfolio mini-deliverable

`results/week07/`: both annotated VCFs, `codon_check.R` output, `variant_report.csv`, and your `memo.md`.

{% endtab %}

{% tab title="6 · Go deeper" %}

## Core resources

- **Richards S, et al.** *Standards and guidelines for the interpretation of sequence variants: a joint consensus recommendation of the ACMG and AMP.* Genetics in Medicine, 2015 (search by title).
- **Tavtigian SV, et al.** *Modeling the ACMG/AMP variant classification guidelines as a Bayesian classification framework.* Genetics in Medicine, 2018 (search by title).
- **ClinGen** ([clinicalgenome.org](https://clinicalgenome.org)): gene-disease validity, variant curation expert panels (VCEPs) and specification of ACMG criteria per gene.
- **ACMG** ([acmg.net](https://www.acmg.net)): professional guidance on variant interpretation and reporting.
- **ClinVar** ([ncbi.nlm.nih.gov/clinvar](https://www.ncbi.nlm.nih.gov/clinvar/)): look up a known gene and read the *evidence* behind entries, not only the label.
- **gnomAD** ([gnomad.broadinstitute.org](https://gnomad.broadinstitute.org)): population frequencies; note the ancestry composition and sample counts.
- **Ensembl** ([ensembl.org](https://www.ensembl.org)): gene models, transcripts and the Variant Effect Predictor (VEP).
- **HGVS nomenclature**: search "HGVS nomenclature" for the current specification and examples.

## Training

- **EMBL-EBI Training** ([ebi.ac.uk/training](https://www.ebi.ac.uk/training)): courses on Ensembl, VEP and variant interpretation.
- **Galaxy Training Network** ([training.galaxyproject.org](https://training.galaxyproject.org)): variant annotation tutorials.
- **HTSlib** ([htslib.org/doc](http://www.htslib.org/doc/)): the `bcftools csq` manual page explains its options and the BCSQ field.

## Pathogens

- **WHO** ([who.int](https://www.who.int)): search for the catalogue of mutations in *Mycobacterium tuberculosis* complex and their association with drug resistance, an example of curated evidence for pathogen variants.
- **Nextstrain** ([nextstrain.org](https://nextstrain.org)): see how mutations are annotated on trees (Week 10).

{% endtab %}

{% tab title="7 · Contribute" %}

You can help improve this week. Open an issue with the label **`week-07`** or edit the file directly - see [How to contribute](../contribute/README.md).

## Ideas for experts

1. **VEP walk-through:** a tested Ensembl VEP example on a small public human region (with licence-clean input).
2. **ACMG worked examples:** replace the exercises with cited, openly licensed worked classifications from ClinGen specifications.
3. **Resistance catalogue:** a real pathogen example using a published resistance catalogue with a tiny sample VCF.
4. **Splicing:** extend the toy gene to include an intron so learners meet splice-site variants.
5. **Gene-specific population data:** show how ancestry-specific frequencies change a classification.
6. **Translations:** the *Concepts* tab (label `translation`).

**Version notes:** tested with bcftools 1.19 (htslib 1.19) and R 4.3.3 on Ubuntu 24.04 (October 2026). The BCSQ text may differ slightly in other versions.

{% endtab %}

{% endtabs %}
