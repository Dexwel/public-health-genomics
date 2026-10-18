---
description: Define public health genomics, learn the vocabulary and the evidence standards, and practise reading genomic data and appraising a screening programme.
---

# Week 1 — What is public health genomics?

{% hint style="info" %}
**At a glance** · **Time:** ~6-8 h (2 h concepts, 3 h lab, 1-2 h practice) · **Prerequisites:** basic epidemiology (prevalence, sensitivity, specificity) · **You will produce:** a screening-programme appraisal and a decoded variant · **Tools:** a terminal (only `head`, `cut`, `sort`, `uniq`, `wc` - Week 2 teaches these properly), a calculator or spreadsheet
{% endhint %}

{% tabs %}

{% tab title="1 · Start here" %}

## Why this matters

On 25 November 2021, scientists in southern Africa announced a new SARS-CoV-2 variant, later named Omicron. They could do so within days of noticing an odd pattern because laboratories in South Africa and Botswana had been sequencing viral genomes routinely, and because they were willing to share what they saw quickly. Within weeks, governments around the world changed travel rules and hospital planning. A *genome* - a few tens of thousands of letters of RNA - had become an input to public policy.

At the same time, in the same region, hundreds of thousands of children are born each year with sickle cell disease (estimates vary; roughly three-quarters of affected births are in sub-Saharan Africa). The condition is caused by a single well-understood DNA change. Yet in many places, diagnosis happens only after a child is gravely ill. A cheap test exists, and a few simple measures (penicillin prophylaxis, vaccination, malaria prevention, hydroxyurea where available) save lives. The hard questions are not scientific but *public-health* questions: who gets tested, when, by whom, paid for how, and with what consent and follow-up?

**Public health genomics** sits at exactly this junction: using genome-based knowledge and technologies, responsibly, to improve the health of populations. It is as much about *programmes, evidence, ethics and equity* as it is about sequencers and software.

## Learning objectives

By the end of this week you will be able to:

1. **Define** public health genomics and distinguish it from clinical genetics and from basic genomics research.
2. **Describe** the main types of genetic variation and the difference between Mendelian and complex disease.
3. **Explain** why heritability is a population statistic and not a measure of how "genetic" a person's disease is.
4. **Apply** the Wilson-Jungner principles and the ACCE framework to appraise a proposed genomic screening programme.
5. **Calculate** sensitivity, specificity, positive predictive value (PPV) and negative predictive value (NPV) at different prevalences and interpret them for decision makers.
6. **Read** a VCF line, an HGVS variant name and an rsID, and trace one variant from genome position to protein change.
7. **Map** the 12 weeks of this course to the genomic data life cycle.

## Roadmap

| Step | Time | Tab |
|---|---|---|
| Pre-check (below) | 10 min | 1 · Start here |
| Read the concepts | 90-120 min | 2 · Concepts |
| Read the conversation and argue back | 20 min | 3 · Conversation |
| Lab: explore the files, appraise a screen, decode a variant | 3 h | 4 · Hands-on lab |
| Exercises and self-test | 60-90 min | 5 · Practice |
| Read more (optional) | as you like | 6 · Go deeper |

## Key terms

| Term | Plain meaning |
|---|---|
| **Genome** | All of an organism's DNA (or RNA, for some viruses) |
| **Gene** | A stretch of DNA that is a unit of heredity, often encoding a protein |
| **Variant / allele** | A position where individuals differ; each version is an allele |
| **Genotype / phenotype** | The alleles a person carries / the observable trait or disease |
| **Penetrance** | The probability that a person with a genotype develops the trait |
| **Heritability** | Proportion of variation *in a population* attributable to genetic differences |
| **Screening** | Testing apparently healthy people to find those at higher risk of a condition |
| **Sensitivity / specificity** | Ability of a test to detect those with / clear those without the condition |
| **PPV / NPV** | Probability that a positive / negative result is correct (depends on prevalence) |
| **Genomic surveillance** | Using pathogen genomes to detect, track and respond to disease threats |

## Pre-check (5 questions - do not worry if you miss some)

1. A test has 99% sensitivity and 99% specificity. In a population where 1 in 1,000 people have the condition, roughly what fraction of positive results are true positives?
2. True or false: "Height is 80% heritable" means 80% of *your* height comes from your genes.
3. Name one difference between a *germline* and a *somatic* variant.
4. Why might the same genetic test have a different PPV in two countries?
5. What does "R" stand for in a typical public health programme evaluation framework RE-AIM? (If you do not know, make a guess - you will meet it in Week 11.)

<details>

<summary>Show answers</summary>

1. About **9%**. Of 100,000 people, 100 have the condition (99 detected) and 99,900 do not (999 false positives): PPV = 99 / (99 + 999) ≈ 9%. You will compute this in the lab.
2. **False.** Heritability describes how much of the *variation between people in a population* is attributable to genetic differences, in that environment. It says nothing about the contribution of genes to one individual.
3. Germline variants are inherited (present in egg or sperm) and in every cell; somatic variants arise during life in some cells (for example in a tumour) and are not passed on.
4. Because PPV depends on **prevalence** (and the test may also perform differently if the populations differ in ancestry, sample quality or the spectrum of variants).
5. **R**each (also Effectiveness, Adoption, Implementation, Maintenance).

</details>

{% endtab %}

{% tab title="2 · Concepts" %}

## 2.1 What is public health genomics?

**Genetics** is the study of single genes and their inheritance. **Genomics** studies the whole genome - all genes, the DNA between them, and how they interact with each other and with the environment. **Public health genomics** applies that knowledge to *populations*, with the standard public health toolkit: assessment, policy development and assurance.

It has two big halves that this course teaches side by side:

| Human genomics for population health | Pathogen genomics for surveillance |
|---|---|
| Newborn screening, carrier screening, cascade testing in families with inherited cancer or high cholesterol, pharmacogenomics, polygenic risk | Outbreak detection, tracking transmission, monitoring antimicrobial resistance and vaccine escape, tracing spread between countries |
| Questions: *Who should be offered what, when, and at what cost and benefit?* | Questions: *Are these cases linked? Is a new lineage spreading? Is resistance emerging?* |
| Evidence: clinical validity and utility, cost-effectiveness, equity | Evidence: timeliness, representativeness, actionability |
| Typical data: SNP arrays, exomes, genomes from people | Typical data: whole genomes of bacteria, viruses, parasites |

Both depend on the same skills: reproducible data handling, careful quality control, statistics that respect population structure, and ethics.

### The translation continuum

Knowledge does not leap from the laboratory to the population. A common way to picture it (often called the T1-T4 continuum) is:

| Phase | Question | Example |
|---|---|---|
| **T1** Discovery → candidate application | Does the variant matter? | A gene linked to a disease |
| **T2** Candidate → evidence-based guideline | Does using it improve health outcomes? | A trial or modelling study; a guideline recommends testing |
| **T3** Guideline → practice | Is it being used, and by whom? | Implementation in clinics; uptake studies |
| **T4** Practice → population health outcome | Is the population healthier, and equitably so? | Reduced deaths; reduced disparities |

Most public health work happens in T3 and T4 - the least glamorous and most neglected stages.

## 2.2 A refresher on the biology (at the level you need)

- **DNA** is a long chain of four bases (A, C, G, T). The human genome has about 3.1 billion base pairs, organised in 23 pairs of chromosomes (we inherit one copy of each from each parent: we are *diploid*). Bacteria usually have one circular chromosome (*haploid*); many viruses have RNA genomes of 10-30 thousand bases.
- **Central dogma**: DNA → RNA → protein. A **gene** is transcribed into RNA; in protein-coding genes, groups of three bases (**codons**) specify amino acids (the *genetic code*). Three codons (TAA, TAG, TGA) are **stop** signals.
- **Variants** are differences between genomes. Types:

| Type | What changes | Example | Typical consequence |
|---|---|---|---|
| **SNV / SNP** | One base | A→T | Silent, missense, or stop |
| **Indel** | Small insertion or deletion (< 50 bp) | Insert one base | May shift the reading frame (**frameshift**) |
| **Structural variant (SV)** | Large deletion, duplication, inversion, translocation | Deleting a whole gene | Often severe |
| **Copy-number variant (CNV)** | Gain or loss of a segment | Extra copy of a region | Dosage effects |
| **Mitochondrial / somatic** | Variants outside the nuclear germline | Tumour mutations | Cancer biology, specific diseases |

- **Germline** variants are in every cell and are heritable; **somatic** variants arise later in some cells.

{% hint style="info" %}
**Public health lens.** Almost every person carries thousands of variants that differ from a reference genome - and hundreds that look "damaging" on paper. The vast majority do nothing noticeable. The central challenge of genomic public health is separating signal from the sea of harmless difference, *at scale and without causing harm*.
{% endhint %}

## 2.3 Mendelian, complex, and everything between

| | **Mendelian (monogenic)** | **Complex (polygenic / multifactorial)** |
|---|---|---|
| Causal structure | One gene dominates | Many variants, each small effect, plus environment |
| Examples | Sickle cell disease, cystic fibrosis, Huntington disease, familial hypercholesterolaemia | Type 2 diabetes, hypertension, coronary disease, most cancers |
| Inheritance | Recognisable patterns in families | Weak familial clustering |
| Risk prediction | Sometimes very strong, but **penetrance** may be incomplete | Individually weak; combined as **polygenic scores** (Week 9) |
| Public-health tools | Newborn screening, carrier screening, cascade testing | Risk stratification, lifestyle and treatment decisions |

**Penetrance** and **expressivity** matter: a variant may raise risk but not guarantee disease, and severity can vary. Many variants first described in clinically referred families have lower penetrance when studied in the general population - a lesson with big consequences for population screening.

**Gene-environment interplay.** Sickle cell *trait* (one copy of the HbS allele) protects against severe malaria; where malaria is common the allele is frequent (a classic example of natural selection; Week 4). A disease can be "genetic" and "environmental" at once - and public health acts on the environmental part even when the genetic part is fixed.

## 2.4 Heritability and the attributable-risk fallacy

**Heritability (h²)** is the fraction of variation in a trait *in a given population and environment* that is attributable to genetic differences. It is not a statement about an individual, and it is not fixed: change the environment (e.g. improve nutrition) and heritability of height changes because environmental variance changes.

- Height has high heritability (commonly cited 0.7-0.8 in well-nourished populations), yet average height rose by many centimetres in a few generations as nutrition improved.
- High heritability does **not** mean "unchangeable" and low heritability does **not** mean "preventable".

**Population attributable fraction (PAF).** What fraction of cases would be avoided if an exposure (or risk genotype) were removed? A genotype with a large relative risk but rare in the population may have a smaller PAF than a common, modest one. For public health, *how common* a variant is matters as much as *how strong* it is.

**Misconception box**

| Claim | Why it is wrong |
|---|---|
| "Genetic means untreatable." | PKU is genetic and is prevented by diet from the newborn period; sickle cell outcomes improve with simple care. |
| "Common diseases are mostly 'in the genes' because heritability is high." | Heritability is about variance within populations; prevention targets modifiable exposures. |
| "A genetic test is definitive." | Every test has error, and the *meaning* of a result depends on prevalence, penetrance and interpretation rules. |

## 2.5 The genomic data life cycle

Every analysis in this course follows the same chain. Learning it now gives you a map for the next 11 weeks.

```
 Sample ─► Sequencing ─► Reads (FASTQ) ─► QC ─► Alignment (BAM) ─► Variant calls (VCF)
   W5          W5              W5          W5         W6                  W6
                                                                           │
          ┌────────────────────────────────────────────────────────────────┘
          ▼
   Annotation & interpretation (W7)
          │
          ├─► Population analyses: structure, GWAS, risk scores (W4, W8, W9)
          ├─► Pathogen analyses: distances, trees, clusters, resistance (W10)
          └─► Decisions: screening, surveillance, programmes (W1, W9, W11)
   ───────────────────────────────────────────────────────────────────────
   Underpinning everything: Linux (W2), R (W3), reproducibility, ethics and governance (W11)
```

## 2.6 Evidence standards for genomic applications

Public health acts on **evidence**, and genomic tests need more than a lab result.

### The ACCE framework

Developed by the US Centers for Disease Control and Prevention to evaluate genetic tests. Four components:

| Component | Question |
|---|---|
| **A**nalytic validity | Does the test accurately and reliably measure the genotype (or sequence)? |
| **C**linical validity | Does the result accurately predict the presence or risk of the disease? |
| **C**linical utility | Does using the test lead to improved health outcomes (compared with not using it)? |
| **E**thical, legal and social implications | What are the consequences for individuals, families and society? |

Many tests have excellent analytic validity but modest clinical validity (the variant is a weak predictor), and utility is often unknown.

### The CDC tiered evidence approach

Genomic applications are sometimes grouped by strength of evidence. *Tier 1* applications have strong evidence and guidelines supporting population use - in the US this has included hereditary breast and ovarian cancer (BRCA1/2), Lynch syndrome, and familial hypercholesterolaemia. *Tier 2* have some supporting evidence; *Tier 3* have little or none. The tiers are a useful way to prioritise and communicate, and they change with evidence - check current CDC material.

### Wilson-Jungner principles (1968)

Written for the World Health Organization, these remain the foundation for deciding whether a condition suits population screening. In paraphrase:

1. The condition is an **important health problem**.
2. There is an **accepted treatment** for patients with recognised disease.
3. **Facilities for diagnosis and treatment** are available.
4. There is a **recognisable latent or early symptomatic stage**.
5. There is a **suitable test or examination**.
6. The test is **acceptable to the population**.
7. The **natural history** of the condition is adequately understood.
8. There is an **agreed policy on whom to treat** as patients.
9. The **cost** of case-finding is economically balanced against possible expenditure on medical care as a whole.
10. Case-finding is a **continuing process**, not a "once and for all" project.

Modern criteria (for example those used by national screening committees) add attention to quality assurance, informed choice, evidence from randomised trials where possible, and equity. The ten principles are a checklist for conversation, not a score.

### Sensitivity, specificity and the base-rate trap

For a test applied to *N* people with prevalence *P*:

| | Condition present | Condition absent |
|---|---|---|
| **Test positive** | TP = Sens × P × N | FP = (1 − Spec) × (1 − P) × N |
| **Test negative** | FN = (1 − Sens) × P × N | TN = Spec × (1 − P) × N |

PPV = TP / (TP + FP). NPV = TN / (TN + FN).

**Worked example.** Sens = Spec = 99%, N = 100,000:

| Prevalence | True positives | False positives | PPV | NPV |
|---|---|---|---|---|
| 0.1% (1 in 1,000) | 99 | 999 | **9.0%** | 99.999% |
| 1% | 990 | 990 | **50.0%** | 99.990% |
| 10% | 9,900 | 900 | **91.7%** | 99.888% |

A "99% accurate" test is wrong in most positive results when the condition is rare. This is why population screening requires either a more specific test, a second confirmatory test, or targeting a higher-prevalence group - and why genomic tests for rare conditions are best used with confirmatory pathways.

{% hint style="warning" %}
**Simplification:** Real tests do not have a single sensitivity and specificity: they vary with the variants tested, sample quality and population. Public health appraisal should use performance estimates from populations like the one you will screen.
{% endhint %}

## 2.7 Where genomics fits in public health practice

| Core function | Genomic examples |
|---|---|
| **Assessment** | Genomic surveillance; estimating carrier frequencies; mapping resistance |
| **Policy development** | Deciding which tests to offer; setting data-governance rules; funding priorities |
| **Assurance** | Laboratory quality systems; workforce training; equitable access; evaluation |

And three themes run through the course:

- **Equity.** Most genomic reference data come from people of European ancestry. Tools and risk estimates can be less accurate for others, and benefits may flow unevenly. African populations hold the greatest human genetic diversity yet are markedly underrepresented in many reference datasets - a scientific as well as a fairness problem.
- **Scale and speed.** Pathogen sequencing turns around in days; human programmes unfold over years. Both need decisions under uncertainty.
- **Trust.** Genomic data are personal, family-relevant and permanent. A programme that loses public trust loses its public.

## 2.8 Reading genomic notation

Three ways to name one variant (we will use all three in the lab):

| Notation | Example | Meaning |
|---|---|---|
| **Genomic position** (VCF-style) | `chrToy 1301 A C` | On chromosome `chrToy`, position 1301, reference A, alternate C |
| **HGVS** | `c.301A>C` and `p.Lys101Gln` | Coding-DNA position 301 changes A to C; at the protein level, amino acid 101 changes from lysine (Lys) to glutamine (Gln) |
| **rsID** | `rs334` | A database identifier for a known variant (rs334 is the classic sickle-cell HbS variant) |

Positions in `c.` notation count from the **A of the start codon (ATG)** of the transcript; that is why `c.301` is not the same as genomic position 1301. Always state which **reference genome build** and **transcript** a name refers to: the same variant can have different coordinates in different builds.

{% endtab %}

{% tab title="3 · Conversation" %}

*Zainab is a district health officer. Tunde is a laboratory scientist. Dr. Mensah is their mentor. They are in the district laboratory's small meeting room; a kettle is working very hard in the background.*

**Zainab:** Let me say it plainly. The Ministry has asked me whether our district should "adopt genomics". I don't know what that means. Is it a machine? A department? A budget line?

**Dr. Mensah:** (smiling) Excellent start. If you cannot say what it is, you are the right person to decide. Let me ask you something you already know. When you decide whether to start a screening programme for, say, hypertension, what do you ask?

**Zainab:** How common is it, can we treat it, do we have clinics that can follow up, can we afford it…

**Dr. Mensah:** You've just recited Wilson and Jungner, from memory, without knowing it. Genomics changes the *test*; it does not change the questions.

**Tunde:** Careful, though. The test changes a lot. Genome sequencing doesn't give a yes/no. It gives millions of positions, and most are meaningless.

**Zainab:** Then why is everyone so excited?

**Tunde:** Because when you know *what* to look for, it is cheap and precise. Sickle cell disease is one letter. One change in the β-globin gene: a glutamic acid becomes a valine. We can detect it from a dried blood spot.

**Zainab:** Then the answer is obvious - test every newborn!

**Dr. Mensah:** Is it? Try the next question on the list.

**Zainab:** …can we treat it. Well, we can give penicillin and vaccines, and educate families. And hydroxyurea - if we have it.

**Tunde:** If the clinic has it. If the family can reach the clinic. If the child is *followed up*, not just flagged.

**Zainab:** So the test is easy, the programme is hard.

**Dr. Mensah:** That is the whole discipline in one sentence. Write it down. Now let's try something more slippery. Tunde, you have a new assay for a variant in a gene linked to a rare condition. Sensitivity and specificity are both ninety-nine percent. Zainab, would you buy it?

**Zainab:** Ninety-nine percent! Of course.

**Tunde:** (grinning) Take a pencil.

**Zainab:** Fine. One in a thousand people have the condition. I screen a hundred thousand. So a hundred people have it, and I find ninety-nine of them. Good.

**Dr. Mensah:** And among the other ninety-nine thousand nine hundred?

**Zainab:** One percent are wrongly flagged… that is… (counting) nine hundred and ninety-nine. So I have nearly a thousand false positives, and ninety-nine true ones. That's… less than ten percent of my positives are real.

**Tunde:** And each of those false positives is a frightened family, a repeat test, a follow-up visit.

**Zainab:** I made a mistake. I thought "99% accurate" was a property of the test, like its weight.

**Dr. Mensah:** It is a property of the test *and* the population. The mistake is universal - clinicians make it, politicians make it, newspapers make it. What would you do?

**Zainab:** A second test to confirm positives. Or test only people at higher risk - those with a family history, say.

**Tunde:** Both work, and both are used. Notice you solved a *public health* problem with *public health* logic, not genetics.

**Zainab:** All right. But Tunde, your lab keeps saying "variant". Is a variant a disease?

**Tunde:** No. A variant is a *difference*. Everyone differs from the reference genome in millions of places. Most differences are harmless. Some are protective. A few are harmful, and of those, most only raise risk.

**Zainab:** So if I sequence a hundred people from my district and find a variant that the textbook says causes a disease, what do I tell them?

**Dr. Mensah:** What do *you* think?

**Zainab:** I'd… tell them? They might be in danger!

**Dr. Mensah:** Possibly. But think: textbooks were mostly written from families who came to clinics *because* they were ill. That inflates how dangerous variants look. In the general population, a "disease variant" often has much lower penetrance. And who consented to be told what?

**Tunde:** Consent, return of results, what we do with incidental findings - we'll spend a whole week on it. The point for now is that "we found a variant" is the *beginning* of a hard conversation, not the end.

**Zainab:** (sighing) Then what is the use of sequencing the *pathogen*? At least a bacterium has no feelings.

**Tunde:** (laughs) No, but its genome tells us who infected whom. If two patients' isolates differ by two letters out of five million, they probably share a recent source. If they differ by two thousand, they are unrelated.

**Zainab:** So I could show that the hospital ward cases and the market cases are one outbreak, or two.

**Dr. Mensah:** And that is where the Omicron story began - careful laboratories noticing a pattern, and saying so openly. It required three things: sequencing capacity, good metadata - dates, places - and the willingness to share. Technology was the *smallest* of the three.

**Zainab:** (writing) Capacity, metadata, willingness. And for humans: test, follow-up, consent. Hmm. Is there a danger that we only look where it is easy? Our sequencer is in the capital; the far-flung districts send fewer samples.

**Dr. Mensah:** Oh, you've found the sharpest problem in the field. If you map only the places that send samples, your map shows where *samples come from*, not where *disease is*. We will draw that bias on real data in Week 10.

**Zainab:** Then my first question to the Ministry is: not "should we adopt genomics?" but "which public-health question will genomics help us answer better than what we have?"

**Dr. Mensah:** (raising the kettle triumphantly) Then you have done Week 1.

### Talking points for the forum

1. Think of a condition in your setting. Walk through Wilson-Jungner: which of the ten principles are *not* met, and what would it take to meet them?
2. You are told a new genetic test is "99% accurate." What three questions do you ask before believing it is useful for your population?
3. Whose genomes are in the reference datasets you can access? Who might be missing, and why does it matter for the programme you are imagining?

{% endtab %}

{% tab title="4 · Hands-on lab" %}

{% hint style="success" %}
**Lab goal.** Look at the real file formats you will use all course, appraise a screening programme with numbers, and decode one variant three ways. You only need a terminal. Every command below was run on the course data. All commands start **from the repository root** (the folder containing `README.md`).
{% endhint %}

## Part A - Meet the files (30 min)

### Step 1. Where am I, and what is here?

```bash
pwd
ls
ls data/seq data/seq/ref
```

You should see the top-level folders (`data`, `weeks`, `scripts`, ...) and inside `data/seq/ref`:

```text
adapters.fa
toy_cds_toyR1.fa
toy_ref.fa
toy_ref.gff3
```

### Step 2. Read a reference sequence (FASTA)

```bash
head -n 3 data/seq/ref/toy_ref.fa
```

```text
>chrToy synthetic 6 kb reference (course toy data)
CCATTCAGTAGATTGACAGGGCGAGTAGAGCCTCCAAGCTGAAACGGACAATATGGTTTT
CTCTGCCACTTTGTGCTTATCCTCTGGATGAGCGGTACTCTCAGACAGAGATTCTGTCTG
```

A **FASTA** file has a header line starting with `>` followed by sequence lines. This synthetic "genome" is 6,000 letters long.

### Step 3. Read a gene annotation (GFF3)

```bash
grep -v '^##' data/seq/ref/toy_ref.gff3 | cut -f1-8
```

```text
chrToy	toysim	gene	1001	1900	.	+	.
chrToy	toysim	mRNA	1001	1900	.	+	.
chrToy	toysim	exon	1001	1900	.	+	.
chrToy	toysim	CDS	1001	1900	.	+	0
chrToy	toysim	gene	3501	4199	.	-	.
chrToy	toysim	mRNA	3501	4199	.	-	.
chrToy	toysim	exon	3501	4199	.	-	.
chrToy	toysim	CDS	3501	4199	.	-	0
```

**Stop and check:** there are **two genes**. The first runs 1001-1900 on the `+` strand; the second runs 3501-4199 on the `-` strand. How long is each? (Answer: 900 and 699 bases. 900 / 3 = 300 codons.)

### Step 4. Read some sequencing reads (FASTQ)

```bash
zcat data/seq/reads/sampleA_R1.fastq.gz | head -n 4
```

```text
@VL00123:45:AAAXYZ123:1:1104:1865:11236 1:N:0:ACGTAC
AGATTAGCGATGAGTTCGATATGGAGGTTTCTTATAGAAACATCAACCAATCAACTTAAATGCTGACGCGACATAACTACTTTTAGGCTCGACTTGCAGA
+
CCEGGBFFDHDCBEHGDCGFEECDCBGFDBGDFD?HDCE@@GEEDFGCECDFBDBEADBBBCGEBB>CCEG?C@BCFCFBA@AD??CBCB?ADA?CCBBC
```

A **FASTQ** record has four lines: an identifier, the bases, a `+`, and one quality character per base (decoded in Week 5). Do not worry about the details yet; notice that the sequence line and quality line have the same length (100).

### Step 5. A line list of isolates

```bash
head -n 4 data/outbreak/outbreak_metadata.tsv
tail -n +2 data/outbreak/outbreak_metadata.tsv | wc -l
```

```text
isolate_id	collection_date	district	facility	age	sex	outcome	ciprofloxacin
ISO-001	2026-04-11	A	hospital	36	M	recovered	S
ISO-002	2026-02-09	A	community	32	M	recovered	S
ISO-003	2026-03-15	E	clinic	65	F	recovered	S
74
```

`tail -n +2` skips the header; `wc -l` counts lines. There are **74 data rows** but the alignment holds only 73 isolates - check:

```bash
grep -c '>' data/outbreak/outbreak_alignment.fasta
```

```text
73
```

**Stop and check:** you have found a data-quality problem on Day 1 (one duplicated row). You will find it properly in Week 10. Real genomic projects always start with checking that the counts agree.

### Step 6. Count by district

```bash
tail -n +2 data/outbreak/outbreak_metadata.tsv | cut -f3 | sort | uniq -c
```

```text
     26 A
     10 B
     17 C
     15 D
      6 E
```

Which district has the most isolates? Does that mean it has the most *disease*? Keep that question - Week 10 returns to it.

## Part B - Appraise a screening programme (60 min)

**Scenario.** A regional health authority is considering offering **sickle cell disease screening to all newborns** using a dried blood spot test. Below are planning assumptions for a pilot of 100,000 births (fictional numbers for teaching):

| Assumption | Value |
|---|---|
| Birth cohort | 100,000 |
| Prevalence of sickle cell disease at birth | 1.5% (1 in 67) |
| Screening test sensitivity | 98% |
| Screening test specificity | 99.5% |
| Confirmatory test | Assumed 100% accurate |
| Cost per screening test | 3 USD |
| Cost per confirmatory test | 15 USD |

### Step 1. Build the 2×2 table

Fill in (use a calculator, spreadsheet, or the Python snippet below):

| | Disease | No disease | Total |
|---|---|---|---|
| Screen positive | TP | FP | |
| Screen negative | FN | TN | |
| Total | 1,500 | 98,500 | 100,000 |

```bash
python3 - <<'EOF'
N, prev, sens, spec = 100000, 0.015, 0.98, 0.995
tp = sens*prev*N;  fn = (1-sens)*prev*N
fp = (1-spec)*(1-prev)*N;  tn = spec*(1-prev)*N
print(f"TP={tp:.0f} FN={fn:.0f} FP={fp:.0f} TN={tn:.0f}")
print(f"PPV={tp/(tp+fp):.3f}  NPV={tn/(tn+fn):.5f}")
print(f"cost = screening {3*N:,.0f} + confirmatory {15*(tp+fp):,.0f} USD")
EOF
```

```text
TP=1470 FN=30 FP=493 TN=98008
PPV=0.749  NPV=0.99969
cost = screening 300,000 + confirmatory 29,438 USD
```

**Stop and check:** you should find **1,470 true positives, 30 missed cases, 493 false positives**, and a PPV of about **75%**. About one in four positive screens will turn out *not* to be sickle cell disease after confirmation.

### Step 2. Prevalence matters

Re-run with prevalence 0.1% (a rare condition) and 10% (a high-risk group) and fill in:

| Prevalence | TP | FP | PPV |
|---|---|---|---|
| 0.1% | | | |
| 1.5% | 1,470 | 493 | 74.9% |
| 10% | | | |

(Answers in the Practice tab.) Copy the Python snippet and change `prev`.

### Step 3. Appraise against Wilson-Jungner and ACCE

Copy this template into `results/week01/appraisal.md` (create the folder with `mkdir -p results/week01`) and complete it in 8-12 lines. Use *your* setting for the facts.

```markdown
# Appraisal: newborn screening for sickle cell disease in <region>

| Wilson-Jungner principle | Met? (yes / partly / no / unknown) | Evidence or gap |
|---|---|---|
| 1 Important health problem | | |
| 2 Accepted treatment | | |
| 3 Facilities for diagnosis and treatment | | |
| 4 Recognisable early stage | | |
| 5 Suitable test | | |
| 6 Acceptable to the population | | |
| 7 Natural history understood | | |
| 8 Agreed policy on whom to treat | | |
| 9 Cost balanced | | |
| 10 Continuing process | | |

| ACCE | Judgement | Note |
|---|---|---|
| Analytic validity | | |
| Clinical validity | | |
| Clinical utility | | |
| Ethical, legal, social | | |

**Recommendation (3 lines):** ...
**Biggest uncertainty:** ...
```

## Part C - Decode a variant three ways (45 min)

Here is a VCF-style line you will actually produce in Week 6 (a **VCF** records one variant per line; Week 6 covers the columns):

```text
chrToy  1301  .  A  C  225.4  .  DP=51  GT:AD  1:0,51
```

Task: **trace this variant from genome position to protein change.**

### Step 1. Locate it in the genome

Position **1301** lies between 1001 and 1900, so it is inside gene **toyR1** (`+` strand).

### Step 2. Convert to coding-sequence position

The coding sequence starts at genomic position 1001. So `c.` position = 1301 − 1001 + 1 = **301**. Position 301 is the **first base of codon 101** (codon number = ⌈301 / 3⌉ = 101, base 1 of 3).

### Step 3. Read the codon from the data

```bash
python3 - <<'EOF'
cds = "".join(l.strip() for l in open("data/seq/ref/toy_cds_toyR1.fa") if not l.startswith(">"))
print("CDS length:", len(cds), "bases =", len(cds)//3, "codons")
print("c.301 base:", cds[300])
print("codon 101:", cds[300:303])
EOF
```

```text
CDS length: 900 bases = 300 codons
c.301 base: A
codon 101: AAA
```

The reference codon is **AAA**, which codes for **lysine (Lys, K)**. The variant changes the first base A → C, so the new codon is **CAA**, which codes for **glutamine (Gln, Q)**.

### Step 4. Write the names

| Notation | Result |
|---|---|
| Genomic (VCF) | `chrToy:1301 A>C` |
| HGVS coding | `toyR1.1:c.301A>C` |
| HGVS protein | `p.Lys101Gln` (one-letter: `p.K101Q`) |
| Consequence | **missense** (changes an amino acid) |

**Stop and check:** you have just done by hand what annotation software does in Week 7.

### Step 5 (stretch). Use the genetic code table

Find a codon table (any textbook, or your notes) and answer: which single-base changes to codon AAA would be **synonymous** (no amino-acid change)? Which would create a **stop**? (Answer in the Practice tab.)

## Part D - Map the course to your work (15 min)

In `results/week01/my_goals.md`, write three sentences: (1) the public-health question you most want genomics to help with, (2) which of the 12 weeks matter most for it, (3) the biggest obstacle in your setting.

## If it breaks

| Symptom | Likely cause | Fix |
|---|---|---|
| `No such file or directory` | You are not at the repository root | `cd` to the folder with `README.md`; check with `ls` |
| `zcat: command not found` (macOS) | macOS uses `gzcat` | Use `gzcat`, or `gunzip -c file.gz \| head` |
| `python3: command not found` | Python not installed | See [setup](../start-here/setup.md) |
| Output looks different from the page | Different tool version or typed command | Re-read the command; check for a missing quote |

## Stretch challenge

Compute PPV for the 0.1% case when a **confirmatory second test** (sensitivity 95%, specificity 99.9%) is applied only to screen-positives. Does the combined programme fit the Wilson-Jungner "cost balance" principle better or worse than screening alone?

{% endtab %}

{% tab title="5 · Practice" %}

## Exercises

### Basic

**Exercise 1.** Define, in one sentence each: genome, gene, variant, genotype, phenotype, penetrance.

**Exercise 2.** Classify each as germline or somatic: (a) a BRCA1 variant found in a blood sample from a healthy woman and her mother; (b) a KRAS mutation found only in a tumour biopsy.

**Exercise 3.** Complete the prevalence table from the lab (Part B, Step 2) for prevalence 0.1% and 10%.

<details>

<summary>Show answers (1-3)</summary>

1. *Genome:* all of an organism's DNA/RNA. *Gene:* a heritable unit, often encoding a protein. *Variant:* a position where individuals differ. *Genotype:* the alleles a person carries at a position. *Phenotype:* the observable trait or disease. *Penetrance:* probability that carriers of a genotype develop the trait.
2. (a) germline; (b) somatic.
3. Using sens 98%, spec 99.5%, N = 100,000:
   - 0.1%: TP = 98, FN = 2, FP = 0.005 × 99,900 ≈ **500**, PPV = 98 / (98 + 500) ≈ **16.4%**.
   - 10%: TP = 9,800, FP = 0.005 × 90,000 = **450**, PPV = 9,800 / 10,250 ≈ **95.6%**.
   Lesson: with the same test, PPV rises from 16% to 96% purely because prevalence rises.

</details>

### Intermediate

**Exercise 4.** A district has 40,000 births a year. Carrier screening for a recessive condition costs 5 USD per person. The carrier frequency is 1 in 10. Explain why the prevalence of *affected births* is *not* 1 in 10, and calculate it assuming random mating (Hardy-Weinberg; Week 4): carrier frequency 2pq ≈ 0.10.

**Exercise 5.** A genetic test has analytic validity 99.9% and clinical validity of 40% (PPV for disease within 5 years). A colleague says "99.9% accurate, so we should screen." Write a two-sentence response using ACCE.

**Exercise 6.** Which Wilson-Jungner principle is most likely violated if a country introduces newborn sickle cell screening but has no paediatric haematology service? What would you recommend?

<details>

<summary>Show answers (4-6)</summary>

4. Affected births require **two** carrier parents each transmitting the allele. If allele frequency q satisfies 2q(1−q) ≈ 0.10, then q ≈ 0.053 and affected genotype frequency q² ≈ **0.0028 (about 1 in 360)**, i.e. ≈ 112 affected births per year among 40,000. The carrier frequency is a poor proxy for disease burden.
5. "Analytic validity tells us the lab result is accurate, not that the result predicts disease; with a clinical-validity PPV of 40%, most positives would not develop the disease within five years. Before screening we also need evidence of **clinical utility** - that acting on the result improves outcomes - and an assessment of the ethical and social consequences."
6. Principles **2 and 3** (accepted treatment and facilities for diagnosis and treatment). Recommend building referral and treatment capacity *before* or alongside screening, or beginning with a pilot linked to existing clinics.

</details>

### Challenge

**Exercise 7.** Sketch (words and arrows) a "genomic surveillance for cholera" workflow: which steps happen in the field, the laboratory, the analysis team and the public health decision makers? Identify two points where metadata could be lost or biased.

**Exercise 8.** In the lab Part C, which single-base changes to codon AAA (Lys) are synonymous? Which create a stop codon? (Use the standard genetic code.)

<details>

<summary>Show answers (7-8)</summary>

7. A good answer includes: clinical case detection and stool sample collection (field) → transport and culture or direct sequencing (laboratory) → quality control, assembly, lineage assignment, comparison to previous genomes (analysis) → report to the national epidemiology team (decision makers). Metadata loss points: *date and location* recorded after the fact or at the wrong resolution; *sampling bias* (only severe or hospitalised cases sequenced); mismatched sample IDs between clinic and lab.
8. AAA = Lys. Changing the **third** base: AAG is also Lys (**synonymous**). Changing the first base: CAA = Gln, GAA = Glu, TAA = **stop**. Changing the second base: ACA = Thr, AGA = Arg, ATA = Ile. So the only synonymous change is AAA→AAG, and the only single-base change to a stop codon is AAA→**TAA**.

</details>

## Self-test (8 questions)

1. Which is *not* part of ACCE? (a) Analytic validity (b) Clinical validity (c) Cost-effectiveness (d) Clinical utility
2. A test has sensitivity 90% and specificity 95%. In a population with prevalence 2%, the PPV is closest to: (a) 27% (b) 50% (c) 90% (d) 95%
3. A high-penetrance variant observed in affected families is observed in the general population. Compared with the family estimate, the apparent penetrance is likely to be: (a) higher (b) lower (c) identical (d) unmeasurable
4. "Heritability of 0.6" means: (a) 60% of an individual's trait is genetic (b) 60% of the variance in the population is attributable to genetic variance (c) 60% of relatives share the trait (d) the trait cannot be changed by environment
5. A VCF line says `chrToy 1301 . A C`. The "1301" is a: (a) coding position (b) genomic position (c) codon number (d) read depth
6. Which Wilson-Jungner principle concerns follow-up and continuing review? (a) 1 (b) 5 (c) 8 (d) 10
7. Pathogen genomic surveillance is most vulnerable to which bias? (a) sampling bias (b) recall bias (c) lead-time bias (d) none of these
8. Which statement about sickle cell trait is correct? (a) Carriers always have disease (b) It confers some protection against severe malaria (c) It is caused by a deletion of the whole β-globin gene (d) It is somatic

<details>

<summary>Show answers and reasons</summary>

1. **(c)** Cost-effectiveness is not a component of ACCE (the E is *Ethical, legal and social implications*), although economic evaluation is often added.
2. **(a)** per 100,000: 2,000 diseased → 1,800 TP; 98,000 healthy → 4,900 FP; PPV = 1,800 / 6,700 ≈ 27%.
3. **(b)** Families are ascertained *because* of disease, which inflates penetrance (ascertainment bias).
4. **(b)** Heritability is about variance in a population, not an individual.
5. **(b)** The VCF position is a genomic coordinate.
6. **(d)** Principle 10: case-finding is a continuing process.
7. **(a)** Sampling bias (who gets sequenced) - recall bias and lead-time bias are other problems.
8. **(b)** Trait (one HbS allele) is generally asymptomatic and protective against severe malaria; disease needs two abnormal β-globin alleles.

</details>

## Reflection prompt (150-250 words)

*Describe a public health problem in your setting where genomics might help, and one reason it might not.* Keep it in your portfolio folder (`results/week01/reflection.md`).

## Portfolio mini-deliverable

A single page, `results/week01/portfolio_week01.md`, containing: (1) your completed appraisal table, (2) the PPV table for three prevalences, (3) the three-notation decoding of the variant at 1301, and (4) your three-sentence goals note.

{% endtab %}

{% tab title="6 · Go deeper" %}

Only stable, widely used sources are listed with links. Search each site for the named guideline or lesson. Titles of papers are given so you can find them yourself; always check you have the current version of any guideline.

## Core reading

- **Wilson JMG, Jungner G.** *Principles and practice of screening for disease.* WHO Public Health Papers 34 (1968). The ten principles in the original. Search the WHO website or library catalogue by title.
- **CDC - Genomics and Precision Health** ([cdc.gov](https://www.cdc.gov/genomics-and-health/)): the tiered-evidence approach and the ACCE model's origins; read the section on *tiered genomic applications*.
- **PHG Foundation** ([phgfoundation.org](https://www.phgfoundation.org)): policy-oriented analyses of how genomics is used in health systems; start with introductory explainers.
- **NHGRI** ([genome.gov](https://www.genome.gov)): the *Talking Glossary* and fact sheets are excellent for terms in this week.

## Free courses and videos

- **EMBL-EBI online training** ([ebi.ac.uk/training](https://www.ebi.ac.uk/training)): short free courses on genomics and variation; choose an introductory one.
- **Galaxy Training Network** ([training.galaxyproject.org](https://training.galaxyproject.org)): look for introductory *Genomics* material.

## Guidelines and standards

- **WHO** ([who.int](https://www.who.int)): search for the *Global Genomic Surveillance Strategy* and for guidance on newborn screening and sickle cell disease.
- **GA4GH** ([ga4gh.org](https://www.ga4gh.org)): policy frameworks on responsible genomic data sharing (we revisit them in Week 11).

## Africa-focused

- **H3Africa** ([h3africa.org](https://h3africa.org)): the Human Heredity and Health in Africa initiative: capacity building, ethics and governance resources.
- **Africa CDC** ([africacdc.org](https://africacdc.org)): the Pathogen Genomics Initiative and continental surveillance.

## Datasets and databases to browse

- **ClinVar** ([ncbi.nlm.nih.gov/clinvar](https://www.ncbi.nlm.nih.gov/clinvar/)): search `HBB` and look at how variants are classified; we use it in Week 7.
- **dbSNP / rsIDs**: search `rs334` at NCBI to see how a single variant is described.

{% endtab %}

{% tab title="7 · Contribute" %}

You can help improve this week. Open an issue with the label **`week-01`** or make the edit directly - see [How to contribute](../contribute/README.md).

## Ideas for experts

1. **Local case study:** replace the sickle cell scenario's fictional numbers with figures from a published or national source for your country (cite them).
2. **Another hook:** add a short case on a different programme (e.g. familial hypercholesterolaemia, hereditary cancer cascade testing, a pathogen outbreak).
3. **Translation:** translate the *Start here* tab and glossary entries into another language (label `translation`).
4. **Exercise:** add a Challenge exercise on number-needed-to-screen or on a decision-curve intuition.
5. **Equity lens:** extend the "Evidence standards" section with an equity checklist used by a screening committee.
6. **Accuracy review:** check the heritability and PAF explanations against a textbook you trust and improve the wording.
7. **Accessibility:** propose plain-language or screen-reader-friendly improvements.

## Three-line "how to suggest a change"

1. Open an **issue** (*Suggest a change to a lesson*) for anything that is wrong or unclear.
2. Or click the **pencil** on this file on GitHub to edit it and open a pull request.
3. A reviewer from the *foundations* team will respond; see [How to contribute](../contribute/README.md).

**Version notes:** commands tested with GNU coreutils, Python 3.13 and the course data generated with seed 20261015 (October 2026).

{% endtab %}

{% endtabs %}
