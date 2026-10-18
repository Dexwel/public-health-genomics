---
description: How sequencers work, how to read FASTQ and Phred scores, and how to judge and trim reads with FastQC and fastp - without being fooled by warnings.
---

# Week 5 — Sequencing and quality control

{% hint style="info" %}
**At a glance** · **Time:** ~6-8 h · **Prerequisites:** Weeks 2-3 · **You will produce:** a QC report on three samples, trimmed FASTQ files, a per-position quality plot and a keep/repeat decision for each sample · **Tools:** FastQC 0.12.1, fastp 0.23.4, R · **Data:** `data/seq`
{% endhint %}

{% tabs %}

{% tab title="1 · Start here" %}

## Why this matters

Every genomic result is only as good as the reads it came from. A sample with poor chemistry, adapter contamination or too little DNA produces confident but wrong variant calls. Public health genomics runs on **many samples from many labs**, so QC is how you decide, quickly and defensibly, which sequences enter the surveillance database and which go back for repeat.

This week you learn what a sequencer produces, how to read a FASTQ file, what a Phred score means, and how to judge three samples: a good one, a good one with a hidden sub-population, and a poor one.

## Learning objectives

By the end of this week you will be able to:

1. **Describe** how short-read (Illumina-type) and long-read sequencing differ, and where each fits in public health.
2. **Read** a FASTQ record and **decode** Phred quality scores.
3. **Run** FastQC and **interpret** each module, including when a warning does not matter.
4. **Trim** adapters and low-quality reads with fastp and **report** what was removed.
5. **Compute** simple QC numbers in R (mean quality by position) and plot them.
6. **Decide** keep, trim, or repeat for each sample, and write down why.

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
| **Read** | One sequenced fragment of DNA (here 100 bases) |
| **Paired-end** | Both ends of a fragment are read: R1 and R2 |
| **FASTQ** | Text format: read name, bases, `+`, quality characters |
| **Phred score (Q)** | Quality: Q = −10 × log₁₀(error probability) |
| **Adapter** | Synthetic DNA added in library prep; appears in reads if the fragment is short |
| **Coverage / depth** | How many reads, on average, cover each position |
| **Duplicate** | Reads from the same original fragment, copied by PCR |

## Pre-check

1. What error probability corresponds to Q20? To Q30?
2. A read shows `AGATCGGAAGAGC` near its end. What is it likely to be?
3. Why might R2 be of lower quality than R1 on the same run?
4. What does "45× depth" mean?

<details>

<summary>Show answers</summary>

1. Q20 = 1 error in 100 (1%). Q30 = 1 in 1,000 (0.1%).
2. Part of an Illumina TruSeq adapter - the fragment was shorter than the read, so the sequencer read into the adapter.
3. R2 is read second, after the chemistry has had more cycles to degrade, so its quality is typically lower, especially near the end.
4. On average each position is covered by 45 reads.

</details>

{% endtab %}

{% tab title="2 · Concepts" %}

## 2.1 From a sample to reads

1. **Extract** DNA or RNA (from a patient sample, an isolate, a wastewater sample).
2. **Prepare a library:** fragment the DNA, attach **adapters** and sample barcodes.
3. **Sequence:** the machine reads each fragment and reports bases with a quality estimate.
4. **Demultiplex:** split reads by barcode into one file per sample.

| Technology | Read length | Strength | Public health use |
|---|---|---|---|
| Short-read (Illumina-type) | 50-300 bases | Accurate, cheap per base | Pathogen genomes, exomes, GWAS arrays complement |
| Long-read (Oxford Nanopore, PacBio) | thousands to many thousands of bases | Structural variants, portable (Nanopore) | Field and outbreak sequencing |

The toy data here imitate paired-end short reads.

## 2.2 The FASTQ record

Four lines per read:

```text
@VL00123:45:AAAXYZ123:1:1104:1865:11236 1:N:0:ACGTAC     <- name (instrument, run, lane, tile, position; read 1)
AGATTAGCGATGAGTTCGATATGGAGG...                           <- bases
+                                                        <- separator
CCEGGBFFDHDCBEHGDCGFEECDCBG...                           <- one quality character per base
```

Each quality character encodes a Phred score: take its ASCII code and subtract 33. For example `C` is ASCII 67, so Q = 34; `5` is ASCII 53, so Q = 20; `#` is ASCII 35, so Q = 2.

| Phred Q | Chance the base is wrong | Accuracy |
|---|---|---|
| 10 | 1 in 10 | 90% |
| 20 | 1 in 100 | 99% |
| 30 | 1 in 1,000 | 99.9% |
| 40 | 1 in 10,000 | 99.99% |

**Q30** is the common benchmark: "% of bases ≥ Q30".

{% hint style="warning" %}
**Gotcha from Week 2:** quality strings can begin with `@`, so counting lines that start with `@` over-counts reads. Count lines and divide by 4.
{% endhint %}

## 2.3 Why quality falls along the read

The sequencer reads one base per cycle, and errors accumulate: phasing (molecules in a cluster drift out of step) and signal decay. So quality is highest at the start and lower at the end, and **R2 is usually worse than R1**. A steep drop is normal; a collapse to Q10 means trouble.

## 2.4 What QC tools look for

| Check | Problem it finds |
|---|---|
| Per-base quality | Degraded chemistry, bad tiles, over-clustering |
| Per-sequence quality | A sub-set of terrible reads |
| Adapter content | Fragments shorter than the read; poor library size selection |
| Duplication | Low input DNA, over-amplification |
| GC content | Contamination by another species, or a genome with unusual GC |
| Overrepresented sequences | Adapters, primers, a contaminant |
| N content | Failed cycles |

### FastQC warnings are rules of thumb

FastQC is written for large genomes. **Its thresholds can fire for perfectly good data.** In this course the genome is a 6 kb toy, so even the good sample gets "Per sequence GC content" and "Overrepresented sequences" warnings: with only 6,000 bases and ~45× depth, individual 50-mers genuinely recur. A good analyst asks: *Is this warning plausible for my organism and library design?*

## 2.5 Trimming and filtering

**fastp** (one tool, fast) can detect adapters from paired reads, trim them, cut low-quality bases and discard reads that remain too short or too poor. Choices you must record:

| Setting | Meaning | Trade-off |
|---|---|---|
| `-q 20` | a base counts as "qualified" if Q ≥ 20 | stricter = fewer bases kept |
| `-u 30` | discard a read if more than 30% of bases are *un*qualified | stricter = more reads removed |
| `-l 50` | discard reads shorter than 50 after trimming | protects alignment |
| `--detect_adapter_for_pe` | find adapters by overlap of R1 and R2 | no adapter file needed |

**Do not over-trim.** Throwing away good data lowers coverage. **Do not under-trim.** Adapters can align to the wrong place and produce false variants.

## 2.6 Coverage and what it buys you

For a genome of length G sequenced with N reads of length L, the mean depth is about N × L / G. At 40-50× each position is covered by dozens of reads, enough for confident haploid calls; at 5-7× many positions are covered by too few reads for a confident call (Week 6).

{% hint style="info" %}
**Public health lens.** Surveillance programmes set **acceptance criteria** (for example, a minimum % genome covered at ≥10× and a minimum Q30). A sequence that fails QC is not "bad news"; it is a *request for a repeat*. Sharing a poor sequence can mislead other analysts and trigger false alarms about a "new variant".
{% endhint %}

{% endtab %}

{% tab title="3 · Conversation" %}

*The lab bench is a mess of tube racks. Zainab is holding a printout of a FastQC report with a green tick, an amber triangle and several red crosses. Tunde looks over her shoulder.*

**Zainab:** Three samples. Sample A is all ticks except two amber triangles, B is the same, and C is a sea of red. So: A and B are good, C is bad. Done?

**Tunde:** Almost. Why are A's two warnings fine?

**Zainab:** I… assumed they were minor. They're amber, not red.

**Dr. Mensah:** An amber triangle is a question, not an answer. What does "Per sequence GC content" compare?

**Zainab:** GC content of the reads against a smooth curve.

**Dr. Mensah:** A smooth curve that FastQC *expects* for a large genome. What is our genome?

**Zainab:** Six thousand bases. A toy. (pause) So the reads cannot look like they came from a human.

**Tunde:** Right. And the overrepresented sequences?

**Zainab:** Three copies of a 50-mer out of fourteen hundred reads. In a human genome that would be suspicious. In six thousand bases at forty-five times coverage, some 50-mers have to repeat. By chance.

**Dr. Mensah:** Good. So the warnings reflect the organism. Now sample C. The red crosses.

**Zainab:** Quality collapses. Read 2 ends near Q11. And an adapter-content failure.

**Tunde:** Adapters mean the fragment was shorter than the read. In sample C, we sequenced 100 bases from a fragment of perhaps 70, so the last 30 are adapter.

**Zainab:** And I can just trim it.

**Dr. Mensah:** You can. Let us see what that costs. Tunde, what did fastp keep?

**Tunde:** C started with 560 reads. After filtering: 100.

**Zainab:** Hundred? That's 18 percent. The rest was thrown away?

**Tunde:** Four hundred sixty failed the quality filter, and a hundred and forty-two had adapters trimmed.

**Zainab:** Is that too aggressive? My instinct is to rescue them.

**Dr. Mensah:** What would "rescue" mean?

**Zainab:** Relax the filter. Keep reads with lower quality.

**Dr. Mensah:** And what do you expect to happen to the variants called from those reads?

**Zainab:** More errors. False variants. (pause) And because C has so few reads, every false base has a bigger share.

**Dr. Mensah:** Which brings us to the decision. A sequence that goes into a surveillance database informs a public health response. What is the cost of a false variant there?

**Zainab:** Someone declares a new lineage that isn't one. Or links two outbreaks that are unrelated.

**Tunde:** And the cost of repeating the sequencing?

**Zainab:** A few days and some reagents.

**Dr. Mensah:** So for C the answer is…

**Zainab:** Repeat the library. Report it as "failed QC, repeat requested". Not a "bad result", a missing result that we know is missing.

**Tunde:** And one more story. First time through I ran the quality check only on read 1. It looked fine. Read 2 was a disaster.

**Zainab:** Because R2 degrades more.

**Tunde:** Always check both reads. Always.

**Dr. Mensah:** Write your rule: *a warning is a prompt to look, a fail is a prompt to decide, and the decision is mine - not the software's*.

### Talking points for the forum

1. Which QC thresholds would you set for accepting a pathogen genome into your national database, and who should agree to them?
2. A reference lab is under pressure to release results fast. How do you respond to a request to "just use what we have" from a failing sample?
3. Name a FastQC warning that could be harmless in one project and critical in another.

{% endtab %}

{% tab title="4 · Hands-on lab" %}

{% hint style="success" %}
**Lab goal.** QC and trim three paired-end samples. Everything below was run on the course data with FastQC 0.12.1, fastp 0.23.4 and R 4.3.3. Work **from the repository root**; check tools with `bash scripts/check_setup.sh`.
{% endhint %}

```bash
mkdir -p results/week05/qc results/week05/trim && cd results/week05
R=../../data/seq/reads
```

## Part A - Look at the reads (30 min)

### Step 1. Count reads

```bash
for s in A B C; do
  n=$(zcat $R/sample${s}_R1.fastq.gz | wc -l)
  echo "sample$s R1: $((n/4)) reads"
done
```

```text
sampleA R1: 1400 reads
sampleB R1: 1200 reads
sampleC R1: 280 reads
```

Lines divided by 4 (not `grep -c '^@'`). Sample C has five times fewer reads than A.

### Step 2. Decode a quality string

```bash
zcat $R/sampleA_R1.fastq.gz | head -4
```

The first read begins `@VL00123:45:AAAXYZ123:1:1104:1865:11236 1:N:0:ACGTAC`. Take the first quality character, `C`: its ASCII code is 67; minus 33 is **Q34**. In R you can check any character:

```r
utf8ToInt("C") - 33     # 34
utf8ToInt("#") - 33     # 2
```

### Step 3. Mean quality by position (R)

This shows *where* quality falls. Run it from `results/week05`:

```bash
Rscript -e '
suppressMessages(library(ggplot2))
meanq <- function(f){ x <- readLines(gzfile(f)); q <- x[seq(4, length(x), 4)]
  m <- sapply(strsplit(q, ""), function(s) utf8ToInt(paste(s, collapse="")) - 33)
  data.frame(pos = seq_len(nrow(m)), q = rowMeans(m)) }
files <- c("A R1"="sampleA_R1","A R2"="sampleA_R2","C R1"="sampleC_R1","C R2"="sampleC_R2")
d <- do.call(rbind, lapply(names(files), function(n) cbind(meanq(file.path("../../data/seq/reads", paste0(files[[n]], ".fastq.gz"))), read = n)))
print(subset(d, pos %in% c(1, 50, 100)))
p <- ggplot(d, aes(pos, q, colour = read)) + geom_line() + geom_hline(yintercept = c(20, 30), linetype = 2) +
  theme_minimal() + labs(x = "Position in read", y = "Mean Phred quality", title = "Per-position quality")
ggsave("quality_by_position.png", p, width = 6.5, height = 4, dpi = 110)'
```

```text
    pos        q read
1     1 36.99714 A R1
50   50 34.51643 A R1
100 100 32.07714 A R1
101   1 36.98286 A R2
150  50 31.95286 A R2
200 100 27.10286 A R2
201   1 33.01786 C R1
250  50 28.00357 C R1
300 100 23.21429 C R1
301   1 33.03214 C R2
350  50 22.18214 C R2
400 100 11.11429 C R2
```

Open `quality_by_position.png`. **Stop and check:** (1) quality falls along each read; (2) R2 falls faster than R1; (3) sample C R2 ends at about Q11 - a 1-in-13 error rate - while A R2 ends near Q27.

## Part B - FastQC (45 min)

### Step 4. Run FastQC on all six files

```bash
fastqc -o qc -t 2 $R/sample*_R*.fastq.gz 2>&1 | tail -2
ls qc | head -4
```

Each input produces an `.html` report (open it in a browser) and a `.zip` with the same data as text. List the modules that are not PASS:

```bash
for f in qc/*.zip; do
  b=$(basename $f _fastqc.zip); echo "== $b"
  unzip -p $f ${b}_fastqc/summary.txt | awk -F'\t' '$1!="PASS"{print "  "$1": "$2}'
done
```

```text
== sampleA_R1
  WARN: Per sequence GC content
  WARN: Overrepresented sequences
== sampleA_R2
  WARN: Per sequence GC content
  WARN: Overrepresented sequences
== sampleB_R1
  WARN: Per sequence GC content
  WARN: Overrepresented sequences
== sampleB_R2
  WARN: Per sequence GC content
  WARN: Overrepresented sequences
== sampleC_R1
  WARN: Per base sequence quality
  WARN: Per base sequence content
  FAIL: Per sequence GC content
  FAIL: Overrepresented sequences
  FAIL: Adapter Content
== sampleC_R2
  FAIL: Per base sequence quality
  WARN: Per sequence quality scores
  WARN: Per base sequence content
  WARN: Per sequence GC content
  FAIL: Overrepresented sequences
  WARN: Adapter Content
```

### Step 5. Interpret

Fill this table in your notebook (the answers are in the *Practice* tab):

| Sample | Real problem? | Which modules are *expected* artefacts of the 6 kb toy genome? |
|---|---|---|
| A | | |
| B | | |
| C | | |

Look at the `Overrepresented sequences` section for sample A: do they match an adapter? (They show "No Hit".)

```bash
unzip -p qc/sampleA_R1_fastqc.zip sampleA_R1_fastqc/fastqc_data.txt | grep -A4 "Overrepresented" | head -6
```

Each sequence occurs 3 times in 1,400 reads (0.21%) with source "No Hit": at ~45× depth of a small genome, repeats are expected.

## Part C - Trim with fastp (45 min)

### Step 6. Run fastp on each sample

```bash
for s in A B C; do
  fastp -i $R/sample${s}_R1.fastq.gz -I $R/sample${s}_R2.fastq.gz \
        -o trim/s${s}_R1.fq.gz -O trim/s${s}_R2.fq.gz \
        --detect_adapter_for_pe -q 20 -u 30 -l 50 \
        -h trim/s$s.html -j trim/s$s.json 2>&1 | grep -i "reads passed\|low quality\|too short\|adapter trimmed"
  echo "-- sample $s"
done
```

```text
reads passed filter: 2800
reads failed due to low quality: 0
reads failed due to too short: 0
reads with adapter trimmed: 148
-- sample A
reads passed filter: 2400
reads failed due to low quality: 0
reads failed due to too short: 0
reads with adapter trimmed: 102
-- sample B
reads passed filter: 100
reads failed due to low quality: 460
reads failed due to too short: 0
reads with adapter trimmed: 142
-- sample C
```

fastp counts **reads** (R1 + R2), so 1,400 pairs = 2,800 reads. A and B lose nothing; 148 and 102 reads have adapters trimmed. **C loses 460 of its 560 reads to the quality filter.**

### Step 7. Summarise from the JSON

```bash
python3 - <<'E'
import json
for s in "ABC":
    j = json.load(open(f"trim/s{s}.json")); b = j["summary"]["before_filtering"]; a = j["summary"]["after_filtering"]
    print(s, "reads", b["total_reads"], "->", a["total_reads"],
          "| Q30", round(b["q30_rate"]*100,1), "->", round(a["q30_rate"]*100,1),
          "| GC", round(b["gc_content"]*100,1), "| dup %", round(j["duplication"]["rate"]*100,2))
E
```

```text
A reads 2800 -> 2800 | Q30 86.3 -> 86.5 | GC 46.0 | dup % 2.14
B reads 2400 -> 2400 | Q30 79.3 -> 79.6 | GC 46.1 | dup % 1.0
C reads 560 -> 100 | Q30 26.2 -> 32.9 | GC 46.7 | dup % 0.36
```

**Interpret.** A and B pass cleanly; Q30 is 86% and 79%. C: only 26% of bases are Q30 and filtering leaves 100 reads - about 18% of the sample; the genome would be barely covered.

## Part D - Decide (30 min)

Write `results/week05/decision.md` with one row per sample: **keep / repeat**, three numbers (reads kept, Q30 after trimming, adapter reads) and one sentence. Example for C:

> Sample C - **REPEAT**. 100 of 560 reads survive filtering (18%); Q30 after trimming 32.9%; R2 mean quality falls to Q11 by position 100. Not suitable for variant calling.

Sample B: note that it passes QC but is said to have "a minor sub-population"; QC cannot detect that - it will show up in Week 6.

## If it breaks

| Message or symptom | Likely cause | Fix |
|---|---|---|
| `fastqc: command not found` | Tool not installed | Run `bash scripts/check_setup.sh`; follow the setup page |
| `Unable to find` input file | Wrong directory or `R` unset | `pwd`; `echo $R`; `ls $R` |
| Java warnings appear | Java environment message | Harmless; FastQC still runs |
| fastp reports fewer reads than lines/4 | fastp counts reads, not pairs | Multiply pairs by 2 |
| Different numbers from this page | Different fastp settings | Re-run with exactly `-q 20 -u 30 -l 50` |
| `Rscript: command not found` | R missing | Re-run setup |

## Stretch challenge

1. Re-run fastp on sample C with the more tolerant `-u 50` (write outputs to a scratch folder, not over your earlier files). How many reads survive, and what is Q30? Is the result trustworthy?
2. Add `--cut_tail` (sliding-window trimming of low-quality tails) to the original settings. Compare reads kept and Q30 (real values: 560 reads, Q30 32.5%).
3. Open the fastp HTML report for sample C and list the two plots that justify the "repeat" decision.

{% endtab %}

{% tab title="5 · Practice" %}

## Exercises

### Basic

**Exercise 1.** A base has quality character `5`. What is its Phred score and error probability?

**Exercise 2.** Why must you check R1 **and** R2?

**Exercise 3.** Why do the "Per sequence GC content" and "Overrepresented sequences" warnings in sample A not worry us?

<details>

<summary>Show answers (1-3)</summary>

1. ASCII 53 − 33 = **Q20**; error probability 0.01.
2. R2 is read second and degrades more; a good R1 can hide a bad R2 (in sample C, R2 mean quality at position 100 is 11.1, versus 23.2 for R1).
3. The toy genome is only 6 kb, so GC distributions are not smooth and 50-mers recur by chance at 45× depth; they have "No Hit" sources, not adapters.

</details>

### Intermediate

**Exercise 4.** Fill in the Step 5 table.

**Exercise 5.** Compute the expected mean depth for sample A if the toy genome is 6,000 bases: 2,800 reads × 100 bases. Compare with the 44.95× measured in Week 6.

**Exercise 6.** Set `-u 50` for sample C. Report reads kept. Would you use the result?

<details>

<summary>Show answers (4-6)</summary>

4. A: no real problem; the warnings are toy-genome artefacts. B: same. C: real problems in quality, adapter content and overrepresentation; GC fail and base-content warnings follow from low read numbers and adapters.
5. 2,800 × 100 / 6,000 ≈ 46.7×; the measured 44.95× is a little lower because some reads do not map and fragment ends are trimmed. (Mean depth is always lower than the naive figure.)
6. Real result: with `-u 50` all **560** reads pass (no read has more than half its bases below Q20), but Q30 is only **27.3%** - the filter has simply stopped filtering. Using `--cut_tail` with the original `-u 30` also keeps all 560 reads (the bad tails are trimmed instead of the whole read being dropped) and raises Q30 to **32.5%**. Both keep many more reads than the strict setting, yet the data are still poor and the sample has only 280 pairs, so a repeat remains the right decision. Lesson: a filter setting changes *how many* reads you keep, not how good the library is.

</details>

### Challenge

**Exercise 7.** Write a shell loop that, for every FASTQ in `data/seq/reads`, prints the file name and the percentage of bases at Q30 or better, using base-R or awk. Compare with fastp's `q30_rate`.

**Exercise 8.** Draft three acceptance criteria for a surveillance programme (reads, Q30, adapter fraction) and one action for each failure.

<details>

<summary>Show answers (7-8)</summary>

7. A reasonable answer reads the quality line, converts each character to Q (in R: `utf8ToInt(ch) - 33`), and counts `>= 30`; the totals for R1 and R2 combined should agree with fastp to within rounding (for A: 86.3%).
8. Example: ≥ 1,000 reads per pair → otherwise "repeat library"; Q30 ≥ 75% → otherwise "investigate run"; adapter reads ≤ 20% → otherwise "retrim, check size selection". The point is that criteria are written down in advance and agreed with the data owners.

</details>

## Self-test (8 questions)

1. Q30 means an error chance of: (a) 3% (b) 1% (c) 0.1% (d) 0.01%
2. Adapter sequences in reads mean: (a) the fragment was shorter than the read (b) the genome is large (c) the sample is human (d) the run is perfect
3. Each FASTQ record has: (a) 2 lines (b) 3 lines (c) 4 lines (d) 8 lines
4. Which read is usually lower in quality? (a) R1 (b) R2 (c) neither (d) both identical
5. FastQC warnings should be read: (a) as a pass/fail verdict (b) as prompts to check against your organism and design (c) never (d) only for human data
6. Over-trimming causes: (a) lower coverage (b) higher accuracy only (c) more adapters (d) no effect
7. A sample with 18% of reads remaining after filtering should usually: (a) be uploaded (b) be repeated (c) be averaged with others (d) be renamed
8. QC alone can detect a minor sub-population in a sample: (a) always (b) never (c) sometimes, and only with later analysis (d) only with FastQC

<details>

<summary>Show answers and reasons</summary>

1. **(c)** Q = −10 log₁₀(p); Q30 is p = 0.001.
2. **(a)** Short fragments let the read run through into the adapter.
3. **(c)** Name, bases, `+`, qualities.
4. **(b)** R2 degrades more.
5. **(b)** Context decides.
6. **(a)** Throwing away good bases lowers depth.
7. **(b)** Too few good reads for reliable calls.
8. **(c)** It appears in variant allele fractions after mapping, not in FastQC.

</details>

## Reflection prompt (150-250 words)

You are the analyst on duty and a laboratory director asks you to release a genome that failed QC "because the outbreak is urgent". Write the response you would send, including what you offer instead.

## Portfolio mini-deliverable

`results/week05/`: `quality_by_position.png`, the fastp JSON files, `decision.md`, and a 150-word note explaining why two FastQC warnings on sample A were ignored.

{% endtab %}

{% tab title="6 · Go deeper" %}

## Core resources

- **FastQC** documentation and example reports: search for "FastQC Babraham" (the project page includes good and bad example reports and explanations of every module).
- **fastp** documentation: search "fastp OpenGene GitHub" for the option reference and the paper describing the tool.
- **EMBL-EBI Training** ([ebi.ac.uk/training](https://www.ebi.ac.uk/training)): courses on next-generation sequencing and file formats.
- **Galaxy Training Network** ([training.galaxyproject.org](https://training.galaxyproject.org)): tutorials on "Quality Control" with FastQC and trimming, usable in a browser without a command line.
- **The Carpentries - Data Carpentry Genomics** ([carpentries.org](https://carpentries.org)): a lesson on assessing read quality with FastQC.
- **HTSlib / samtools documentation** ([htslib.org/doc](http://www.htslib.org/doc/)): file-format specifications (FASTQ, SAM, VCF) are linked from there.

## Sequencing technology

- **Oxford Nanopore** and **PacBio** training material: search each company's learning pages for library preparation and basecalling.
- **Africa CDC** ([africacdc.org](https://africacdc.org)): the Pathogen Genomics Initiative describes how African laboratories are building sequencing capacity.

## Data sharing

- **European Nucleotide Archive** ([ebi.ac.uk/ena](https://www.ebi.ac.uk/ena)) and **NCBI** ([ncbi.nlm.nih.gov](https://www.ncbi.nlm.nih.gov)): where raw reads are deposited; their submission pages list minimum metadata and QC expectations.

{% endtab %}

{% tab title="7 · Contribute" %}

You can help improve this week. Open an issue with the label **`week-05`** or edit the file directly - see [How to contribute](../contribute/README.md).

## Ideas for experts

1. **MultiQC:** add a tested MultiQC step that summarises all FastQC and fastp reports in one page.
2. **Long reads:** add a short Nanopore QC lab with a small, openly licensed dataset (see the [data policy](../contribute/data-policy.md)).
3. **Contamination:** add a `kraken2`-style example and a synthetic contaminant to the generator.
4. **Wet-lab context:** a short box from a laboratory scientist on sample handling and library prep failures.
5. **Acceptance criteria:** replace the example criteria with a cited real-world programme standard.
6. **Translations:** the *Concepts* tab (label `translation`).

**Version notes:** tested with FastQC 0.12.1, fastp 0.23.4, R 4.3.3, ggplot2 3.4.4 on Ubuntu 24.04 (October 2026). Newer fastp releases may print slightly different messages.

{% endtab %}

{% endtabs %}
