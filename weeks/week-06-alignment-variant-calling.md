---
description: Map reads to a reference with bwa, inspect SAM/BAM with samtools, call variants with bcftools, and check the calls against a truth set - including a sub-population and a failing sample.
---

# Week 6 — Alignment and variant calling

{% hint style="info" %}
**At a glance** · **Time:** ~7-9 h · **Prerequisites:** Weeks 2, 5 (trimmed reads in `results/week05/trim/`) · **You will produce:** sorted, indexed BAM files, a depth summary, VCF files for three samples, and a truth-set comparison · **Tools:** bwa 0.7.17, samtools 1.19.2, bcftools 1.19 · **Data:** `data/seq`
{% endhint %}

{% tabs %}

{% tab title="1 · Start here" %}

## Why this matters

Reads on their own are just strings. To learn that a patient's virus carries a mutation, you must **align** each read to a reference genome and then **call** the positions where the sample differs. Every drug-resistance report, every lineage assignment and every outbreak tree starts here. Variant calling is also where quality problems turn into false findings, so you will learn to ask of each call: *how much evidence is there?*

You will align the three samples from Week 5 to a 6 kb toy reference and compare your calls with the answer key. You will see a perfect result (two good samples), a sub-population visible only in allele counts, and a failing sample whose few reads lead to missed variants.

## Learning objectives

By the end of this week you will be able to:

1. **Explain** what alignment does and what a mapping quality score means.
2. **Index** a reference, **align** paired reads with bwa mem, and **sort and index** the BAM.
3. **Read** SAM fields (flag, position, CIGAR) and **summarise** alignment with flagstat and depth.
4. **Call** variants with bcftools, **read** a VCF record, and **explain** GT, DP and AD.
5. **Compare** calls with a truth set and count true positives, false negatives and false positives.
6. **Explain** why ploidy matters and how a sub-population shows up in allele counts.
7. **Choose** filters for depth and quality and describe the trade-off.

## Roadmap

| Step | Time | Tab |
|---|---|---|
| Pre-check | 10 min | 1 · Start here |
| Concepts | 90 min | 2 · Concepts |
| Conversation | 20 min | 3 · Conversation |
| Lab | 3-4 h | 4 · Hands-on lab |
| Practice | 60-90 min | 5 · Practice |

## Key terms

| Term | Plain meaning |
|---|---|
| **Reference** | The genome sequence reads are compared with |
| **Alignment / mapping** | Finding where each read best fits in the reference |
| **SAM / BAM** | Text / compressed binary alignment file |
| **MAPQ** | Mapping quality: confidence a read is in the right place |
| **CIGAR** | Compact description of how a read matches (e.g. `100M` = 100 matches) |
| **Variant call** | A position where the sample differs from the reference |
| **VCF** | Variant Call Format: one line per variant |
| **GT / DP / AD** | Genotype / total depth / depth per allele |
| **Ploidy** | Number of copies of the genome (bacteria and viruses: 1; humans: 2) |

## Pre-check

1. A bacterial isolate has one copy of its chromosome. What genotype values do you expect at a variant: `0/1` or `1`?
2. A read maps to two places equally well. Should its mapping quality be high or low?
3. At a position, 30 reads show A and 11 show C. What fraction is C?
4. Which is worse in a surveillance database: a false negative or a false positive? (Defend either answer.)

<details>

<summary>Show answers</summary>

1. `1` (haploid) - there is only one allele.
2. Low (MAPQ near 0): the aligner cannot say which place is correct.
3. 11 / 41 = 27%.
4. Either, with reasoning. A false positive can create a false cluster or false "new variant" alarm; a false negative can hide a real mutation (for example drug resistance). Programmes usually favour **specificity** for sharing and **sensitivity** for clinical resistance screening.

</details>

{% endtab %}

{% tab title="2 · Concepts" %}

## 2.1 The pipeline in one picture

```text
reads (FASTQ) --bwa mem--> alignments (SAM) --samtools sort--> sorted BAM --samtools index--> .bai
sorted BAM --bcftools mpileup--> per-position evidence --bcftools call--> variants (VCF) --bcftools norm/filter--> final VCF
```

Every arrow is a tool you can run, inspect and replace. The *reference* must be the **same file** (and the same version) at every step.

## 2.2 Alignment

An aligner finds, for each read, the reference position where it matches best, allowing for mismatches and gaps. **bwa mem** is the standard for short reads. It needs the reference indexed first (`bwa index`), and it reports:

- **FLAG:** a bitwise code (paired, mapped, strand, first/second in pair...). `samtools flagstat` summarises them.
- **MAPQ:** 0-60, how unique the placement is. Repeats get low MAPQ.
- **CIGAR:** operations such as `M` (match/mismatch), `I` (insertion), `D` (deletion), `S` (soft-clipped, ignored ends).
- **Read group (`@RG`):** which sample and library a read came from. Always add it; many tools need it.

Reads that do not map (about 3% here) are mostly adapter-contaminated, chimeric or contaminating sequences.

## 2.3 SAM, BAM, sorting and indexing

SAM is text; **BAM** is compressed binary; **CRAM** is more compressed still. Tools that look at one region quickly need the BAM **sorted by position** and **indexed** (`.bai`).

## 2.4 Depth and coverage

**Depth** at a position is the number of reads covering it. Report **mean depth** and **breadth** (% of the genome covered at ≥10×). A mean of 45× can still hide regions with zero reads.

| Depth | What you can say |
|---|---|
| ≥ 30× (haploid) | Confident calls, even for subpopulations at ~20% |
| 10-30× | Fine for clear variants; weak for minority alleles |
| < 10× | Many positions uncallable; real variants missed |
| 0× | Nothing is known - **not** "same as reference" |

{% hint style="warning" %}
**A missing call is not a reference call.** Always carry depth with the result: "no variant at 2600" means different things at 50× and at 1×.
{% endhint %}

## 2.5 Variant calling

The caller looks at all reads at each position and asks: *is the evidence for a non-reference allele strong enough to rule out sequencing error?* `bcftools mpileup` collects evidence; `bcftools call -m -v` makes calls (`-m` multiallelic model, `-v` variants only).

**Ploidy matters.** For haploid organisms use `--ploidy 1`: every variant is `1`. Use `--ploidy 2` to allow heterozygous (`0/1`) calls, and to see mixtures or sub-populations.

## 2.6 The VCF line

```text
#CHROM POS  ID REF ALT QUAL    FILTER INFO ...   FORMAT        sampleA
chrToy 1301 .  A   C   225.417 .      DP=51 ...  GT:PL:AD      1:255,0:0,51
```

| Field | Meaning |
|---|---|
| POS, REF, ALT | position, reference and sample alleles |
| QUAL | Phred-scaled confidence that the site is variable |
| DP | depth at the site |
| GT | genotype (`1` haploid alt; `0/1` het; `1/1` hom alt) |
| AD | read counts per allele: reference, alternative |

### Insertions and deletions (indels)

Indels are written with an **anchor base**: `AGCT → A` is a 3-base deletion; `T → TG` is a 1-base insertion. Indels can be written several ways in repeat regions, so run **`bcftools norm -f ref.fa`** to put them in one standard (left-aligned) form before comparing.

## 2.7 Filtering and the trade-off

A filter such as `QUAL>=30 && DP>=10` removes weak calls. It lowers false positives and raises false negatives. Rules of thumb must be tuned to the organism, depth and use. Record the filter, the tool version and the reference with the VCF.

## 2.8 Truth sets

To know how good a pipeline is, run it on samples where the answer is known and count:

| | In truth | Not in truth |
|---|---|---|
| **Called** | True positive (TP) | False positive (FP) |
| **Not called** | False negative (FN) | - |

Sensitivity = TP / (TP + FN); precision = TP / (TP + FP). Real programmes use reference materials such as Genome in a Bottle for humans; here the generator provides the answer.

{% hint style="info" %}
**Public health lens.** Share the **evidence**, not only the call: depth, mapping quality and the fraction of reads supporting each allele. A "new mutation" reported at 3 reads is a hypothesis, not a finding.
{% endhint %}

{% endtab %}

{% tab title="3 · Conversation" %}

*Tunde has the alignment of sample B open on the big screen. A strip of coloured reads, stacked like bricks, with a few coloured letters where a read disagrees with the grey reference.*

**Zainab:** Why is it all stacked like a wall?

**Tunde:** Each brick is one read, placed where it fits the reference. A column through the wall is everything we know about one base. Count the bricks: forty-one at this position.

**Zainab:** And the coloured letters?

**Tunde:** Disagreement. Look at position 1301: every brick says C where the reference says A.

**Zainab:** Every one? That is a variant, then. A *real* one, not a typo of the machine.

**Dr. Mensah:** Why not a typo?

**Zainab:** Because a typo is random. Forty-one different reads would not all make the same error.

**Dr. Mensah:** Exactly: **independent agreement is the evidence**. Now Tunde, take her to 2200.

**Tunde:** Here. Forty-one reads. Thirty are A, the reference. Eleven are C.

**Zainab:** Some reads are wrong?

**Tunde:** Eleven out of forty-one is twenty-seven percent. A sequencing error rate of 0.1% could not explain that.

**Zainab:** Then there are two kinds of molecule in the tube. Most carry A, some carry C.

**Dr. Mensah:** In a patient with a mixed infection, or a culture with a minority sub-population, that happens. And what would the haploid calling mode do with it?

**Zainab:** If the program assumes one copy, it has to pick: A or C. It will report A and hide the C.

**Tunde:** That's what happened when I ran it first. With `--ploidy 1` it said nothing at 2200. With `--ploidy 2` it called `0/1` with allele depths 30 and 11.

**Zainab:** So the setting changes what I see?

**Dr. Mensah:** It changes what the software is *willing to say*. Every tool encodes assumptions. For a bacterium you usually want haploid calls for the dominant strain, *and* a separate look at minority alleles. Which should you report?

**Zainab:** Both, labelled differently?

**Dr. Mensah:** Yes. Now, sample C.

**Tunde:** After the strict filtering from last week, C had a hundred reads. Mean depth: one point three.

**Zainab:** A hundred reads over six thousand bases. So most of the genome has zero or one read.

**Tunde:** Three thousand two hundred positions have no read at all. And the calls?

**Zainab:** One variant, at 1153, supported by two reads.

**Tunde:** The answer key says C has two variants. We missed one.

**Zainab:** So the sample *has* the variant at 2600, but we reported nothing. If I wrote "no variant at 2600" I'd be wrong - and I'd not even know it.

**Dr. Mensah:** What should the report say?

**Zainab:** "Position 2600: not callable, depth 0."

**Dr. Mensah:** And if we use the more lenient filter, all 560 reads?

**Tunde:** Depth rises to 7.7. Both variants appear, at 8 and 5 reads. But if I apply a rule "depth at least ten", both calls are filtered out.

**Zainab:** So it's a choice. Lenient: more variants, less certainty. Strict: fewer calls, fewer lies.

**Dr. Mensah:** There is no free option. You decide the trade-off *in advance*, write it down, and apply it equally to every sample. What you must not do is choose the filter after seeing which answer you like.

**Zainab:** I'll put that on the wall.

### Talking points for the forum

1. A colleague reports "no resistance mutations found" from a 1× sequence. What do you write back?
2. When would you report a 27% minority allele, and when would you ignore it?
3. How should a national laboratory set and document its variant filters?

{% endtab %}

{% tab title="4 · Hands-on lab" %}

{% hint style="success" %}
**Lab goal.** Align the three samples, call variants, and compare with the truth. Everything below was run with bwa 0.7.17, samtools 1.19.2 and bcftools 1.19. You need the trimmed reads from Week 5 (`results/week05/trim/`); if you skipped Week 5, run its Step 6 first. Work **from the repository root**.
{% endhint %}

```bash
mkdir -p results/week06 && cd results/week06
S=../../data/seq
T=../week05/trim
```

## Part A - Reference and alignment (45 min)

### Step 1. Prepare the reference

```bash
cp $S/ref/toy_ref.fa ref.fa
bwa index ref.fa 2>&1 | tail -1
samtools faidx ref.fa
cat ref.fa.fai
head -2 ref.fa | cut -c1-70
```

```text
[main] Real time: 0.005 sec; CPU: 0.004 sec
chrToy	6000	51	60	61
>chrToy synthetic 6 kb reference (course toy data)
CCATTCAGTAGATTGACAGGGCGAGTAGAGCCTCCAAGCTGAAACGGACAATATGGTTTT
```

One sequence called `chrToy`, 6,000 bases. (The `bwa index` timing line will differ on your machine.)

### Step 2. Align, sort, index

```bash
for s in A B C; do
  bwa mem -R "@RG\tID:$s\tSM:sample$s\tPL:ILLUMINA" ref.fa $T/s${s}_R1.fq.gz $T/s${s}_R2.fq.gz 2>/dev/null \
    | samtools sort -o s$s.bam -
  samtools index s$s.bam
done
ls -1 *.bam *.bai
```

The pipe (`|`) sends alignments straight into `samtools sort`, so no large SAM file is written. `-R` adds the read group.

### Step 3. How well did the reads map?

```bash
for s in A B C; do
  echo "== $s"; samtools flagstat s$s.bam | grep "in total\|primary mapped"
done
```

```text
== A
2800 + 0 in total (QC-passed reads + QC-failed reads)
2724 + 0 primary mapped (97.29% : N/A)
== B
2400 + 0 in total (QC-passed reads + QC-failed reads)
2334 + 0 primary mapped (97.25% : N/A)
== C
100 + 0 in total (QC-passed reads + QC-failed reads)
100 + 0 primary mapped (100.00% : N/A)
```

About 97% of A and B reads map; 76 and 66 do not (adapter remnants and reads that do not fit). C has only 100 reads because of Week 5's strict filter; they all map.

### Step 4. Look at an alignment

```bash
samtools view sA.bam | head -1 | cut -f1-9
samtools view sA.bam | awk '{c[$6~/S|H/ ? "clipped":"full-length"]++} END{for(k in c)print k, c[k]}'
```

The first line shows read name, FLAG, `chrToy`, position, MAPQ, CIGAR (`100M` means all 100 bases align), mate position and fragment length. Almost all reads are full-length with no soft-clipping (trimming has removed adapters).

## Part B - Depth (30 min)

### Step 5. Mean depth and breadth

```bash
for s in A B C; do
  samtools depth -a s$s.bam | awk -v s=$s '{t+=$3;n++; if($3>=10)c++; if($3==0)z++}
    END{printf "%s mean depth %.2f ; >=10x: %.1f%% ; zero-coverage positions %d of %d\n", s, t/n, 100*c/n, z, n}'
done
```

```text
A mean depth 44.95 ; >=10x: 98.3% ; zero-coverage positions 5 of 6000
B mean depth 38.57 ; >=10x: 98.3% ; zero-coverage positions 7 of 6000
C mean depth 1.32 ; >=10x: 0.0% ; zero-coverage positions 3201 of 6000
```

`-a` includes positions with zero depth. A and B are covered everywhere but at a handful of positions. **C has 3,201 of 6,000 positions with no read at all.**

## Part C - Variant calling (60 min)

### Step 6. Call variants in haploid mode

```bash
for s in A B C; do
  bcftools mpileup -f ref.fa -a AD -Ou s$s.bam 2>/dev/null \
    | bcftools call -mv --ploidy 1 -Ov 2>/dev/null \
    | bcftools norm -f ref.fa -Ov 2>/dev/null > s$s.vcf
  echo "== sample $s"
  bcftools query -f '%POS\t%REF\t%ALT\t%QUAL\t[%GT]\t[%AD]\t%DP\n' s$s.vcf
done
```

```text
== sample A
1153	C	A	225.417	1	0,46	46
1301	A	C	225.417	1	0,51	51
1449	AGCT	A	228.399	1	2,32	34
2600	T	A	225.417	1	0,50	50
4019	A	T	225.417	1	0,56	56
5200	G	C	225.417	1	0,52	52
== sample B
1301	A	C	225.417	1	0,41	41
1606	T	A	225.417	1	0,35	35
1751	T	TG	228.419	1	1,49	50
2600	T	A	225.417	1	0,38	38
5200	G	C	225.417	1	0,31	31
== sample C
1153	C	A	77.4149	1	0,2	4
```

Columns: position, reference, alternative, QUAL, genotype (`1` = alternative, haploid), allele depths (reference,alternative) and depth. Sample A has six variants, including a 3-base deletion at 1449 (`AGCT → A`); sample B has five, including a 1-base insertion (`T → TG`) at 1751. Sample C has **one** call, with only 2 supporting reads. (`-a AD` asks mpileup to record per-allele depth; `norm` left-aligns indels.)

### Step 7. Compare with the answer key

```bash
for pair in "sA sampleA" "sB sampleB" "sC sampleC"; do
  set -- $pair
  awk -F'\t' -v s=$2 '$1==s && $7==1.0{print $3"\t"$4"\t"$5}' $S/answers/truth_variants.tsv | sort > t.txt
  bcftools query -f '%POS\t%REF\t%ALT\n' $1.vcf | sort > c.txt
  echo "$1 truth=$(wc -l <t.txt) called=$(wc -l <c.txt) TP=$(comm -12 t.txt c.txt | wc -l) FN=$(comm -23 t.txt c.txt | wc -l) FP=$(comm -13 t.txt c.txt | wc -l)"
done
```

```text
sA truth=6 called=6 TP=6 FN=0 FP=0
sB truth=5 called=5 TP=5 FN=0 FP=0
sC truth=2 called=1 TP=1 FN=1 FP=0
```

(The `$7==1.0` condition keeps only variants present in all reads; the minor sub-population in B is handled next.) **A and B are perfect. C misses one of two variants (FN=1)** - the one at position 2600 - because there is no evidence at that position.

## Part D - The sub-population (30 min)

### Step 8. Diploid mode reveals a mixture

```bash
bcftools mpileup -f ref.fa -a AD -Ou sB.bam 2>/dev/null \
  | bcftools call -mv --ploidy 2 -Ov 2>/dev/null \
  | bcftools norm -f ref.fa -Ov 2>/dev/null \
  | bcftools query -f '%POS\t%REF\t%ALT\t%QUAL\t[%GT]\t[%AD]\t%DP\n'
```

```text
1301	A	C	225.417	1/1	0,41	41
1606	T	A	225.417	1/1	0,35	35
1751	T	TG	228.411	1/1	1,49	50
2200	A	C	103.348	0/1	30,11	41
2600	T	A	225.417	1/1	0,38	38
5200	G	C	225.417	1/1	0,31	31
```

A sixth variant appears at **2200: `0/1` with 30 reference and 11 alternative reads** (11/41 = 27%; the answer key says the planted fraction is 30%). Haploid mode hid it; diploid mode could see it. The five "fixed" variants become `1/1`.

{% hint style="warning" %}
`--ploidy 2` is a way to *see a mixture* here, not a claim that the organism is diploid. Minority alleles near 10-30% should be reported separately, with their counts.
{% endhint %}

## Part E - Rescuing sample C? Filters and trade-offs (45 min)

### Step 9. Re-trim C leniently and re-call

```bash
R=$S/reads
fastp -i $R/sampleC_R1.fastq.gz -I $R/sampleC_R2.fastq.gz -o cL_R1.fq.gz -O cL_R2.fq.gz \
      --detect_adapter_for_pe -q 20 -u 50 -l 50 -j cL.json -h cL.html >/dev/null 2>&1
bwa mem -R "@RG\tID:Cl\tSM:sampleC\tPL:ILLUMINA" ref.fa cL_R1.fq.gz cL_R2.fq.gz 2>/dev/null \
  | samtools sort -o sCL.bam -
samtools index sCL.bam
samtools flagstat sCL.bam | grep "primary mapped"
samtools depth -a sCL.bam | awk '{s+=$3;n++; if($3>=10)c++} END{printf "mean depth %.2f ; >=10x: %.1f%%\n",s/n,100*c/n}'
bcftools mpileup -f ref.fa -a AD -Ou sCL.bam 2>/dev/null | bcftools call -mv --ploidy 1 -Ov 2>/dev/null \
  | bcftools norm -f ref.fa -Ov 2>/dev/null > sCL.vcf
bcftools query -f '%POS\t%REF\t%ALT\t%QUAL\t[%GT]\t[%AD]\t%DP\n' sCL.vcf
```

```text
484 + 0 primary mapped (86.43% : N/A)
mean depth 7.67 ; >=10x: 22.6%
1153	C	A	138.416	1	0,6	8
2600	T	A	82.415	1	0,4	5
```

All 560 reads were kept; 86% map; mean depth is 7.7×; both true variants are found (TP=2, FN=0), but each rests on only 4-6 reads, and only 22.6% of the genome has ≥10×.

### Step 10. Apply a depth filter

```bash
for v in sA sB sCL; do
  echo "$v $(bcftools view -H $v.vcf | wc -l) calls -> $(bcftools view -H -i 'QUAL>=30 && DP>=10' $v.vcf | wc -l) with QUAL>=30 and DP>=10"
done
```

```text
sA 6 calls -> 6 with QUAL>=30 and DP>=10
sB 5 calls -> 5 with QUAL>=30 and DP>=10
sCL 2 calls -> 0 with QUAL>=30 and DP>=10
```

The filter leaves A and B untouched and removes **both** calls in the rescued C. **Decision for the report:** C is "insufficient evidence"; the two calls, though correct here, cannot be trusted without the answer key. The right action is to repeat the sequencing.

## Part F - Write up (20 min)

Create `results/week06/README.md` with a table:

| Sample | Mean depth | % ≥10× | Calls (haploid) | TP / FN / FP | Report as |
|---|---|---|---|---|---|

and 150 words on the trade-off between sensitivity and specificity for sample C.

## If it breaks

| Message or symptom | Likely cause | Fix |
|---|---|---|
| `fail to open file ... trim/sA_R1.fq.gz` | Week 5 not done | Run Week 5 Step 6 |
| `[E::bwa_idx_load_from_disk] fail to locate the index files` | Reference not indexed | `bwa index ref.fa` |
| `[E::hts_idx_push] unsorted positions` | BAM not sorted | Always pipe through `samtools sort` |
| `bcftools: command not found` | Tools missing | `bash scripts/check_setup.sh` |
| `Failed to open ... ref.fa.fai` | Reference not faidx'ed | `samtools faidx ref.fa` |
| Empty VCF | No variants or wrong reference | Check `samtools flagstat` and the reference file used |
| Slightly different QUAL values | Tool versions differ | Compare positions and genotypes, not exact QUAL |

## Stretch challenge

1. For sample A, list reads that did **not** map (`samtools view -f 4 sA.bam | head`). Do they carry adapter sequence?
2. Use `bcftools mpileup -q 20 -Q 20` and see whether the calls in C change.
3. Compute sensitivity and precision for all samples in one table, using a small shell or R script.

{% endtab %}

{% tab title="5 · Practice" %}

## Exercises

### Basic

**Exercise 1.** What does the CIGAR `60M2D40M` describe?

**Exercise 2.** In the VCF, what does `AD = 0,46` mean? And `GT = 1`?

**Exercise 3.** Why do we index a BAM?

<details>

<summary>Show answers (1-3)</summary>

1. 60 bases aligned, then a 2-base deletion in the read relative to the reference, then 40 aligned bases.
2. 0 reads support the reference allele, 46 the alternative. `GT = 1` is the haploid genotype "alternative allele".
3. An index lets tools jump to a region without reading the whole file; most tools also require it.

</details>

### Intermediate

**Exercise 4.** Sample A has 2,800 reads and 2,724 mapped. Explain what the 76 unmapped reads could be and how to check.

**Exercise 5.** Explain why `--ploidy 2` found position 2200 in B but `--ploidy 1` did not.

**Exercise 6.** Compute the breadth (percent of positions with depth ≥10) for each sample from the Step 5 output.

<details>

<summary>Show answers (4-6)</summary>

4. Adapter-contaminated fragments, chimeras, or contaminating reads. Check with `samtools view -f 4` and BLAST or Kraken; compare with adapter content in FastQC.
5. In haploid mode each position has a single allele, so the caller reports the dominant one; diploid mode allows two alleles, so 30 A and 11 C is modelled as `0/1`.
6. A 98.3%, B 98.3%, C 0.0%.

</details>

### Challenge

**Exercise 7.** The answer key says the minor allele in B has a true fraction of 0.30, but you measured 11/41 = 0.27. Is this a discrepancy? Quantify the sampling uncertainty (binomial standard error) for n = 41.

**Exercise 8.** Design a short validation plan for a laboratory introducing this pipeline: what reference material, what metrics, what acceptance thresholds, and what happens when a version changes.

<details>

<summary>Show answers (7-8)</summary>

7. No. The standard error of a proportion is √(p(1−p)/n) = √(0.3 × 0.7 / 41) ≈ 0.07, so 0.27 is well within one standard error of 0.30. Always give counts alongside percentages.
8. A good plan includes: a characterised reference material or truth set; metrics (sensitivity, precision, depth, breadth) per variant type; acceptance thresholds set in advance; re-validation on every software, reference or chemistry change; archived versions and parameters (see the reproducibility advice in Week 2).

</details>

## Self-test (8 questions)

1. Which command sorts a BAM? (a) `bwa mem` (b) `samtools sort` (c) `bcftools call` (d) `samtools flagstat`
2. A haploid organism's expected genotype for a fixed variant: (a) `0/1` (b) `1/1` (c) `1` (d) `0/0`
3. MAPQ near 0 means: (a) perfect (b) ambiguous placement (c) deletion (d) paired
4. A mean depth of 45× guarantees: (a) no zero-coverage positions (b) nothing about every position - check breadth (c) no errors (d) diploid calls
5. `AGCT → A` is: (a) an insertion (b) a SNV (c) a deletion of 3 bases (d) an inversion
6. The best defence against false conclusions from a low-depth sample: (a) delete it (b) report depth with the call and repeat if needed (c) relax filters (d) rename it
7. A minority allele at 27% can be detected in a haploid sample: (a) never (b) with enough depth, if the caller allows mixtures (c) only by FastQC (d) only in diploid organisms
8. `bcftools norm -f ref.fa` does what? (a) removes variants (b) left-aligns and normalises indels (c) filters by quality (d) sorts the BAM

<details>

<summary>Show answers and reasons</summary>

1. **(b)** 
2. **(c)** One copy, one allele.
3. **(b)** The read could belong in several places.
4. **(b)** Mean depth hides gaps.
5. **(c)** The 4-base reference allele is reduced to one base.
6. **(b)** Evidence travels with the call.
7. **(b)** Needs depth and a mixture-aware calling mode.
8. **(b)** Standardises how indels are written.

</details>

## Reflection prompt (150-250 words)

A hospital laboratory sends you a genome from a patient with a drug-resistant infection. Mean depth is 8×. Write the report you would return, including what you can and cannot claim and what you request next.

## Portfolio mini-deliverable

`results/week06/`: the three VCF files, the depth summary table, the TP/FN/FP table, and a `README.md` with your trade-off paragraph and the Step 10 result.

{% endtab %}

{% tab title="6 · Go deeper" %}

## Core resources

- **HTSlib / samtools / bcftools documentation** ([htslib.org/doc](http://www.htslib.org/doc/)): manuals for every command used here, and the SAM/BAM and VCF format specifications.
- **bwa**: search "BWA Heng Li" for the manual; the original paper (Li & Durbin) is titled *Fast and accurate short read alignment with Burrows-Wheeler transform*.
- **The Carpentries - Data Carpentry Genomics** ([carpentries.org](https://carpentries.org)): a "Variant Calling Workflow" lesson, with real *E. coli* data.
- **Galaxy Training Network** ([training.galaxyproject.org](https://training.galaxyproject.org)): "Mapping" and "Variant calling" tutorials, usable in a browser.
- **EMBL-EBI Training** ([ebi.ac.uk/training](https://www.ebi.ac.uk/training)): courses on NGS data formats and analysis.

## Benchmarking and good practice

- **Genome in a Bottle (NIST)**: search the name; high-confidence truth sets for benchmarking human variant calling.
- **GA4GH** ([ga4gh.org](https://www.ga4gh.org)): benchmarking and file-format standards for variant data.

## For pathogens

- **Nextstrain** ([nextstrain.org](https://nextstrain.org)): see how consensus genomes and mutation calls feed outbreak analyses (Week 10).
- **Africa CDC** ([africacdc.org](https://africacdc.org)): the Pathogen Genomics Initiative and its quality guidance.

{% endtab %}

{% tab title="7 · Contribute" %}

You can help improve this week. Open an issue with the label **`week-06`** or edit the file directly - see [How to contribute](../contribute/README.md).

## Ideas for experts

1. **Snakemake / Nextflow:** add a tested workflow that runs Steps 1-8 in one command.
2. **IGV walk-through:** annotated screenshots of loading `sB.bam` in IGV at position 2200.
3. **Other callers:** a side-by-side with `freebayes` or `lofreq` for minority variants.
4. **Real data:** a small public bacterial or viral dataset with an accession, under the [data policy](../contribute/data-policy.md).
5. **Human context:** diploid variant calling with a small region of a public reference sample.
6. **Translations:** the *Concepts* tab (label `translation`).

**Version notes:** tested with bwa 0.7.17, samtools 1.19.2, bcftools 1.19 and fastp 0.23.4 on Ubuntu 24.04 (October 2026). QUAL values may differ by a fraction in other versions.

{% endtab %}

{% endtabs %}
