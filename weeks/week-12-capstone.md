---
description: Plan, execute, document and peer-review a small public health genomics project that brings together everything from Weeks 1-11, with three tracks, a rubric and a reproducibility check.
---

# Week 12 — Capstone

{% hint style="info" %}
**At a glance** · **Time:** ~10-14 h across the week · **Prerequisites:** Weeks 1-11 (at least the weeks your track needs) · **You will produce:** one reproducible mini-project with a 1,500-word report, a README that lets a stranger rerun it, a peer review of someone else's project, and a short reflection · **Tools:** everything · **Data:** choose a track
{% endhint %}

{% tabs %}

{% tab title="1 · Start here" %}

## Why this matters

You have learned tools one at a time. Public health genomics is practised by combining them to answer a *question* for a *decision-maker* with *honest limits*. The capstone is a small, complete version of that: a question, a reproducible analysis, a clear report, a peer review, and a plan for what you would do next.

Quality matters more than size. A modest project that anyone can rerun and whose limitations are clearly stated beats an ambitious one nobody can reproduce.

## Learning objectives

By the end of this week you will be able to:

1. **Frame** a genomic question for a public health decision and choose the minimal analysis that can answer it.
2. **Execute** a reproducible workflow using the command line and R.
3. **Verify** your own work against known answers and sanity checks, and **report** what you did not verify.
4. **Write** a short report that separates findings, interpretation, limitations and recommendations.
5. **Review** a colleague's project constructively using a rubric.
6. **Reflect** on what you would do differently, and plan how to keep learning and contributing.

## The week at a glance

| Day | Task | Time |
|---|---|---|
| 1 | Choose a track; write a one-page plan (question, data, method, outputs, risks) | 1.5 h |
| 2 | Run the analysis; commit scripts and results | 3 h |
| 3 | Verify (checks, sensitivity), draft the report | 3 h |
| 4 | Finish the README; run `scripts/capstone_check.sh`; submit | 2 h |
| 5 | Peer review (give and receive); respond to reviews | 2.5 h |
| 6-7 | Revise; reflect; optional: contribute an improvement to the course | 2 h |

## Key terms

| Term | Plain meaning |
|---|---|
| **Scope** | What the project will and will not do |
| **Reproducible** | Another person can rerun it and get the same results |
| **Sensitivity analysis** | Checking how conclusions change when choices change |
| **Peer review** | Constructive evaluation by a colleague |
| **Limitations** | Honest statement of what the work cannot support |

## Pre-check

1. In one sentence, what is the *decision* your project will inform?
2. List the three Weeks whose skills your project most depends on.
3. What is the *smallest* analysis that would answer your question?
4. What could make your result misleading?

<details>

<summary>Notes</summary>

There are no single right answers. A good response to (1) names a decision-maker and an action ("whether to open a hospital infection-control investigation"); to (3) resists adding extra analyses; to (4) names a bias or data problem from earlier weeks (ancestry, sampling, missing values, quality).

</details>

{% endtab %}

{% tab title="2 · Concepts" %}

## 2.1 Choose a track

All tracks use only the synthetic course data (so nobody's privacy is at risk) and each can be completed with the tools you already have.

### Track A - Outbreak briefing (pathogen genomics)

**Question:** *What does the genomic data tell the ministry about this outbreak, and what should it do next?*

- **Data:** `data/outbreak`, plus `data/linelist` for case context.
- **Core skills:** Weeks 3, 7 (annotation concepts), 10, 11.
- **Minimum:** validated alignment and metadata; clusters at two thresholds; cluster-by-place-and-time table; resistance analysis; briefing with recommendations and limits.
- **Extensions:** ML tree; a sensitivity analysis on the cluster threshold; sequencing-coverage analysis linking the line list (Week 3) and the genomes.

### Track B - Human risk prediction and equity (GWAS and PRS)

**Question:** *Would a polygenic score based on this discovery study be a fair and useful screening tool for the target population?*

- **Data:** `data/gwas` and `data/prs`.
- **Core skills:** Weeks 4, 8, 9, 11.
- **Minimum:** QC with a logged rationale; the association and one confounding check (naive vs adjusted); the score evaluated in both ancestry groups; screening metrics; an equity assessment and recommendation.
- **Extensions:** tune on a half and test on the other half; a calibration plot; a fairness analysis of thresholds.

### Track C - A validated variant pipeline (sequencing and interpretation)

**Question:** *Is this laboratory's pipeline ready to report variants from these three samples, and under what conditions?*

- **Data:** `data/seq` (three samples).
- **Core skills:** Weeks 2, 5, 6, 7.
- **Minimum:** a single script that runs QC, trimming, alignment, calling and annotation; a truth-set comparison with sensitivity and precision per sample; acceptance criteria; a verdict per sample; a reporting policy for uncertain results.
- **Extensions:** a Snakemake or Nextflow version; a filter sweep on depth and quality; a comparison of two callers.

{% hint style="warning" %}
**One track, finished.** Do not combine tracks. The most common capstone failure is a plan too large to finish.
{% endhint %}

## 2.2 What a good project contains

| Component | What it must do |
|---|---|
| **Question and decision** | One paragraph. Who will use this, and for what? |
| **Methods** | Enough for another analyst to repeat them: tools, versions, parameters, thresholds and reasons |
| **Verification** | At least two independent checks (for example answer key, sanity checks, alternative method) |
| **Results** | Few, clear figures and tables; every figure has a one-sentence caption stating the lesson |
| **Interpretation** | What the results mean for the decision |
| **Limitations** | Biases, missing data, what you did not test |
| **Recommendations** | Actions proportionate to the evidence, including "repeat" or "do not deploy" |
| **Reproducibility** | A README with exact commands and expected outputs; scripts, not manual steps |

## 2.3 The project README (copy this)

````markdown
# <Project title>

**Track:** A / B / C  **Author:** <name>  **Date:** <date>

## Question and decision
One paragraph.

## How to reproduce
1. Requirements: <tools and versions, from `bash scripts/check_setup.sh`>
2. Run from the repository root:
   ```bash
   bash results/week12/run_all.sh
   ```
3. Expected key results: <3-5 numbers a reader can compare with>

## Folder contents
- `run_all.sh` - runs everything in order
- `scripts/` - each script with a header comment saying what it does
- `figures/`, `tables/` - outputs
- `report.md` - the report

## Verification
List your checks and their outcomes.

## Limitations
Bullet list.
````

## 2.4 Verification: trying to break your own result

Use at least two of:

1. **Answer key:** compare with the truth files in `data/*/answers/` *after* finishing the analysis.
2. **Sanity checks:** do counts add up, are ranges plausible, do numbers agree between two routes?
3. **Sensitivity:** change a threshold (cluster distance, p-value, depth) and report whether the conclusion changes.
4. **Negative control:** a case where you expect *nothing* (a sample that should fail, a SNP that should not be associated).
5. **Independent rerun:** run the whole workflow from scratch in a clean folder.

## 2.5 Writing the report

A 1,500-word structure that works:

| Section | Words | Content |
|---|---|---|
| Summary | 150 | Headline, key numbers, recommendation, confidence |
| Background and question | 150 | Decision and context |
| Methods | 300 | Short; link to scripts |
| Results | 400 | Figures and tables, each with a caption |
| Interpretation | 200 | What it means for the decision |
| Limitations | 150 | Honest, specific |
| Recommendations and next steps | 150 | Proportionate actions |

Write for a busy decision-maker: put the conclusion first, number the figures, define each term once, never use a figure you cannot explain.

## 2.6 Giving and receiving peer review

Review the *work*, not the person. Use the rubric below, quote the part you are discussing, say what works before what does not, and suggest a concrete improvement for each issue. Receiving: respond to every comment with *done*, *will not do (because...)*, or *need clarification*. Disagreement is allowed; silence is not.

### Review checklist (one page)

| # | Question | Yes / partly / no | Evidence (quote or line) |
|---|---|---|---|
| 1 | Is the decision and question clear in one paragraph? | | |
| 2 | Could you rerun it from the README alone? | | |
| 3 | Are methods and thresholds justified? | | |
| 4 | Are at least two verification checks reported? | | |
| 5 | Do figures have captions that state the lesson? | | |
| 6 | Do conclusions follow from the results (nothing more)? | | |
| 7 | Are limitations specific, not generic? | | |
| 8 | Are ethics and equity considered where relevant? | | |
| 9 | Are recommendations proportionate? | | |
| 10 | What is the one thing you would change first? | | |

{% hint style="info" %}
**Public health lens.** Peer review is how public health science stays honest. In a real response, an independent colleague checking your cluster call or your risk estimate before it goes to the director is not an insult; it is routine good practice.
{% endhint %}

{% endtab %}

{% tab title="3 · Conversation" %}

*Friday afternoon, the last session. A whiteboard with three coloured columns labelled A, B and C. Zainab is writing in the first one. Tunde has his arms folded. Dr. Mensah is eating groundnuts.*

**Dr. Mensah:** Zainab, which track?

**Zainab:** All three. Outbreak, risk score and pipeline. I've learned all of them, and I'd like to show I can do all of them.

**Tunde:** Seven days?

**Zainab:** I can run the scripts. They already exist.

**Dr. Mensah:** And what do you plan to *write*?

**Zainab:** (pause) Three reports.

**Dr. Mensah:** You would have three half-finished things and no time to check any of them. Choose one.

**Zainab:** Fine. Track A. The outbreak. Because that's what the ministry will ask me about on Monday.

**Tunde:** Good. Now the question. Not "analyse the outbreak". What decision?

**Zainab:** Whether to open an infection-control investigation at Hospital H.

**Dr. Mensah:** And what evidence would change your answer?

**Zainab:** If the eight isolates there were identical and close in time, yes. If they were scattered across the tree, no.

**Tunde:** That is a hypothesis you can test, and a result that could say "no". That is what makes it an analysis rather than a tour of the data.

**Zainab:** I'll also do the resistance mutation, the epidemic curve, the districts, the ML tree, and the sequencing coverage by district.

**Dr. Mensah:** Which of those does the *decision* need?

**Zainab:** (slowly) The clusters. The place and time of the hospital cluster. And whether anything else links to it.

**Tunde:** The resistance mutation?

**Zainab:** Hospital H is K3 and carries no mutation. Resistance belongs to the other cluster. It could be a separate section... or not. I think it's a distraction here.

**Dr. Mensah:** Put it in "next steps". A good report leaves things out on purpose. Now, how will you know you did it correctly?

**Zainab:** I'll compare with the answer key.

**Tunde:** The answer key is one check. It's the *last* check, because real outbreaks don't come with one. What else?

**Zainab:** Change the SNP threshold and see if the cluster changes. That showed up in Week 10: at two SNPs the big cluster split in two. But Hospital H stayed the same at every threshold.

**Dr. Mensah:** That is a *sensitivity analysis*, and it makes your claim stronger. What else?

**Zainab:** A negative control. A hospital where I'd expect no cluster?

**Tunde:** You have one: the sporadic isolates, spread across districts, nearest neighbour thirty-plus SNPs. They shouldn't cluster at any threshold. If they did, your threshold is too loose.

**Zainab:** Good. Then the limitation. Sequencing coverage is unknown. I only see isolates that were sent, so I can't say there are no other cases.

**Dr. Mensah:** What would you recommend?

**Zainab:** Investigate Hospital H, review infection control on the ward, and ask the district teams about unsequenced cases at the same time.

**Tunde:** Notice what you did *not* recommend.

**Zainab:** I did not say who infected whom. I did not say "the outbreak is over". I did not say "the hospital is to blame".

**Dr. Mensah:** And the README, so someone else can run it?

**Zainab:** One command. And the expected key numbers: seventy-one isolates after quality control, clusters of thirty, fifteen and eight.

**Tunde:** And your peer reviewer will run it on a clean folder. If it fails, you fix it. I once handed in a script that only worked on my laptop because it read a file from my desktop.

**Zainab:** What happened?

**Tunde:** The reviewer said: "I assume this is a lovely result. I cannot tell." It cost me a day.

**Dr. Mensah:** Which is the best review you can get. Now, Zainab, say your plan in one breath.

**Zainab:** I will decide whether Hospital H needs an infection-control investigation, by clustering the isolates, testing that the hospital cluster is stable across thresholds, checking that sporadic cases don't cluster, and reporting what the sequencing coverage means for what I can claim. I'll leave resistance for next steps.

**Dr. Mensah:** That is a capstone. And remember: you came in wanting to do three projects. The discipline is the one you will need in the ministry.

### Talking points for the forum

1. Post your one-sentence decision and your *negative control*. Ask your peers to find a hole.
2. What did you decide to *leave out*, and why?
3. What is the first change you would make to this course after finishing it?

{% endtab %}

{% tab title="4 · Hands-on lab" %}

{% hint style="success" %}
**Lab goal.** Plan, run, verify, write up and submit one capstone project. This tab is a work plan with templates and checks; the analysis itself comes from the earlier weeks. Work in `results/week12`.
{% endhint %}

```bash
mkdir -p results/week12/{scripts,figures,tables} && cd results/week12
```

## Part A - Day 1: the plan (90 min)

Write `plan.md` (one page) from this template. Do not start analysing until you have filled in every line.

```text
CAPSTONE PLAN
Track: A / B / C
Decision this will inform (one sentence):
Decision-maker:
Question (answerable, with a result that could say "no"):
Data (files):
Minimum analysis (numbered list, 4-6 steps):
Planned verification (at least 2 from: answer key, sanity checks, sensitivity, negative control, clean rerun):
Planned figures/tables (max 4):
What I will deliberately leave out:
Three things that could make my result misleading:
Time plan (hours per day):
```

Check your plan against the "one track, finished" rule: could you complete the minimum analysis in about 6 hours of compute and coding? If not, cut it.

## Part B - Days 2-3: execute and verify (6 h)

### Step 1. Start from the course scripts

Copy, do not retype, scripts from the earlier weeks into `scripts/`, and keep a header comment stating what each does and its inputs and outputs. Track starting points:

| Track | Scripts to start from |
|---|---|
| A | Week 3 `clean_linelist.R`, Week 10 `outbreak.R` and `outbreak2.R`, Week 11 `reidentification_risk.R` |
| B | Week 8 `run_gwas.sh`, `plot_gwas.R`; Week 9 `prs.R`, `evaluate_prs.R`, `screening.R` |
| C | Week 5 commands (FastQC, fastp), Week 6 commands (bwa, samtools, bcftools), Week 7 `bcftools csq` and `make_report.R` |

### Step 2. One command to run everything

Create `run_all.sh`, which runs your scripts in order and stops on the first error. Example for Track A (adapt the paths to where *you* put your files):

```bash
#!/usr/bin/env bash
# run_all.sh - rerun the whole capstone from the repository root:  bash results/week12/run_all.sh
set -euo pipefail
cd "$(dirname "$0")"                       # work inside results/week12
mkdir -p figures tables
cp ../week10/outbreak.R ../week10/outbreak2.R scripts/ 2>/dev/null || true
cd scripts
Rscript outbreak.R
Rscript outbreak2.R
cd ..
echo "run_all.sh finished OK"
```

`set -euo pipefail` makes the script stop at the first failure instead of silently producing partial results (Week 2). `cd "$(dirname "$0")"` makes the script work wherever it is started. **Adapt the data paths:** scripts that use `../../data/...` assume they run two levels below the repository root, so keep your project at `results/week12/scripts` or adjust the paths.

### Step 3. Verify (at least two checks)

For each check, record *what you did*, *what you expected* and *what you found* in `verification.md`:

```text
CHECK 1: <name>
Expected: <...>
Found:    <...>
Conclusion: <consistent / not consistent / needs follow-up>
```

Suggested checks by track:

| Track | Checks |
|---|---|
| A | Cluster threshold sweep (2, 5, 10, 20 SNPs); negative control (do sporadic isolates cluster?); answer key `clusters_truth.tsv` after finishing |
| B | Naive vs adjusted λ; a SNP known to be neutral (should not be significant); tune on half the target set and test on the other half |
| C | Truth-set TP/FN/FP per sample; a filter sweep (`DP`, `QUAL`); a deliberately failed sample (C) handled by a written criterion |

### Step 4. Quick progress check

```bash
cd ../..                  # back to the repository root
bash scripts/capstone_check.sh
```

This tool reads your `results/` folders and prints PASS, FAIL or SKIP for the key results of Weeks 3-11 (for example, clusters of 30, 15 and 8 in Week 10). It reports on the earlier weeks, not on your capstone; its purpose is to confirm that the foundations are in place. Real output on a complete set of results:

```text
PASS   W3 clean line list has 600 rows
PASS   W4 PCA file has 1000 people
PASS   W5 fastp report for sample C exists
PASS   W6 sample A VCF has 6 variants
PASS   W6 sample B VCF has 5 variants
PASS   W7 annotated VCF has a stop_gained call
PASS   W8 QC leaves 975 people
PASS   W8 top hit is ts06_067
PASS   W9 scores exist for 7 thresholds
PASS   W10 5-SNP clusters of 30, 15 and 8
PASS   W11 re-identification script saved

Summary: 11 passed, 0 failed, 0 skipped
```

If a line says `FAIL`, open the matching week and compare your output with the page. If a line says `SKIP`, that week's results are not in your `results/` folder.

## Part C - Day 3-4: write the report (3 h)

Write `report.md` following the 1,500-word structure from the *Concepts* tab. Rules:

1. **Conclusion first.** The summary must state the recommendation and your confidence.
2. **Every figure has a caption** of the form "Figure 2. <what it shows>: <the lesson>."
3. **Every number traces to a script.** Add the script name in square brackets, e.g. "[outbreak2.R]".
4. **Limitations are specific**, not "more data would help". Name the bias (for example sequencing coverage, ancestry composition, missing values) and what it could do to the conclusion.
5. **Recommendations are proportionate**: "investigate" is different from "declare".

## Part D - Day 4: the README and the clean-folder test (2 h)

Write `README.md` from the template in the *Concepts* tab. Then run the **clean-folder test**: copy your project to a new empty directory, run `run_all.sh` and check that the expected key results match your README. If it fails, you have just found the problem your reviewer would have found.

```bash
T=$(mktemp -d)                              # a new, empty temporary folder
cp -r <path-to-repository>/. "$T"/          # copy the whole repository there
cd "$T" && bash results/week12/run_all.sh   # rerun everything from scratch
```

(Adjust the paths to where your repository is.)

## Part E - Day 5: peer review (2.5 h)

1. Swap projects with a classmate, or post yours to the course forum (see [How it works](../start-here/how-it-works.md)) and review a post from someone else.
2. Use the 10-question review checklist from the *Concepts* tab. **Run their `run_all.sh`.** Record whether it worked.
3. Write the review in four parts: **What works**, **Main concerns** (max 3), **Smaller suggestions**, **One thing to change first**.
4. Receive your review. Respond to every point with *done*, *will not do (because...)* or *need clarification*.

## Part F - Days 6-7: reflect and contribute (2 h)

1. Write `reflection.md` (250 words): what you learned, what was hardest, what you would do differently, what you will practise next.
2. **Give back.** Open an issue or pull request on the course repository with one improvement: a typo, a clearer sentence, a broken link, a new exercise, or an idea from a "Contribute" tab. See [How to contribute](../contribute/README.md). This is how the course improves, and it is the only way an open course stays alive.

## Submission checklist

| ✔ | Item |
|---|---|
| ☐ | `plan.md` written before analysis |
| ☐ | `run_all.sh` runs from a clean folder |
| ☐ | `verification.md` with ≥ 2 checks |
| ☐ | `report.md` (≈1,500 words) with captions and script references |
| ☐ | `README.md` with expected key results |
| ☐ | Peer review given and received, responses recorded |
| ☐ | `reflection.md` |
| ☐ | One contribution proposed to the course |

## If it breaks

| Message or symptom | Likely cause | Fix |
|---|---|---|
| `run_all.sh` works on your computer but not the reviewer's | Absolute paths or files outside the repository | Use relative paths; copy inputs into the project |
| `cannot open file '../../data/...'` | Wrong working directory for the script | Run from the folder the script expects, or fix the path |
| Figures missing | A script failed silently | Use `set -euo pipefail`; read the first error |
| Numbers differ from your report | Report written before the final run | Rerun `run_all.sh`, then update the report |
| Review took too long | Too many concerns | Limit to the three main concerns |
| Out of time | Scope too large | Cut figures, not verification |

{% endtab %}

{% tab title="5 · Practice" %}

## Rubric (self-assessment and reviewer)

Score each row 0-3 (0 absent, 1 partial, 2 good, 3 excellent). A project scoring 20 or more of 30 meets the course standard.

| # | Criterion | Competency | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|---|
| 1 | Question and decision | C1 | None | Vague topic | Clear question | Clear decision-maker, action, and a result that could say no |
| 2 | Reproducibility | C2 | Manual steps | Scripts, some manual | One command works | Works from a clean folder; versions recorded |
| 3 | Data checks | C2, C4 | None | Some | Missing/duplicate/range checks | Checks reported, with decisions logged |
| 4 | Core analysis | C3-C8 | Incorrect | Partly correct | Correct | Correct and appropriately minimal |
| 5 | Verification | C5, C7 | None | One check | Two checks | ≥ 2 checks incl. sensitivity or negative control |
| 6 | Interpretation | C6, C8 | Overclaims | Descriptive only | Sound | Sound, linked to the decision |
| 7 | Limitations | C1, C9 | None | Generic | Specific | Specific, with direction of likely bias |
| 8 | Ethics and equity | C9 | None | Mentioned | Applied to the data | Shapes the recommendations |
| 9 | Communication | C10 | Unclear | Hard to follow | Clear | Conclusion first, captions that state the lesson |
| 10 | Peer review | C10 | None | Cursory | Specific, constructive | Specific, constructive, responses recorded |

## Exercises

**Exercise 1.** Rewrite this vague question into a good capstone question: "Analyse the outbreak data."

**Exercise 2.** You have an excellent result but it only works on your laptop. List three things you would do before submitting.

**Exercise 3.** A reviewer writes: "This is bad." Rewrite the comment so that it is useful.

**Exercise 4.** Give an example of a conclusion your project *cannot* support, and the wording that avoids it.

**Exercise 5.** Choose any figure from Weeks 3-11 and write its caption in the form "Figure N. <what it shows>: <the lesson>."

<details>

<summary>Show suggested answers</summary>

1. "Does the genomic evidence support opening an infection-control investigation at Hospital H, and which other cases should the district teams follow up?" (Names a decision, an action and testable evidence.)
2. Replace absolute paths with relative paths; copy any external files into the project; run from a clean folder; record tool versions; write the expected key numbers in the README.
3. "The negative control is missing, so I cannot tell whether your 5-SNP threshold is too loose. Please add a check that the sporadic isolates do not cluster, and show the result."
4. For Track A: "The eight isolates prove the hospital infected the patients" (unsupported); safer: "The eight isolates are genetically identical and clustered in time in one hospital, which is consistent with healthcare-associated transmission and warrants investigation."
5. Example (Week 3): "Figure 2. Share of cases with a genome sequence by district: Coastal Hub sequences 82% of cases and Highland 10%, so a map of sequences shows where the sequencer is, not only where the disease is."

</details>

## Self-test (8 questions)

1. The best capstone scope is: (a) the largest possible (b) the smallest analysis that answers the question (c) all three tracks (d) no analysis
2. `set -euo pipefail` in a script: (a) hides errors (b) stops it at the first failure (c) speeds it (d) deletes files
3. A negative control is: (a) a case where you expect no effect (b) an error (c) a negative result (d) a placebo only
4. A good caption: (a) repeats the title (b) states what is shown and the lesson (c) lists colours (d) is omitted
5. The answer key should be checked: (a) first (b) after finishing your own analysis (c) never (d) while coding
6. A reviewer's comment should be: (a) general (b) specific, with a suggested improvement (c) personal (d) anonymous only
7. The role of limitations is to: (a) weaken the report (b) state honestly what the work cannot support (c) fill space (d) avoid recommendations
8. A recommendation should be: (a) as strong as possible (b) proportionate to the evidence (c) hidden (d) identical across projects

<details>

<summary>Show answers</summary>

1. **(b)**
2. **(b)**
3. **(a)**
4. **(b)**
5. **(b)**
6. **(b)**
7. **(b)**
8. **(b)**

</details>

## Reflection prompt (250 words)

Look back at the competencies C1-C10 in the [syllabus](../start-here/syllabus.md). Which three are now your strengths, which three do you most want to develop, and what is your plan (resource, project, community) for the next six months?

## Portfolio

Collect your Week 1-12 deliverables into one folder or repository. Add a one-page index describing each piece. This is your public record of the skills you built and can be shared with employers, mentors and collaborators.

{% endtab %}

{% tab title="6 · Go deeper" %}

## Keep learning

- **The Carpentries** ([carpentries.org](https://carpentries.org)): lessons and instructor training; consider becoming a helper at a local workshop.
- **EMBL-EBI Training** ([ebi.ac.uk/training](https://www.ebi.ac.uk/training)): free online courses on genomics, bioinformatics and data resources.
- **Galaxy Training Network** ([training.galaxyproject.org](https://training.galaxyproject.org)): hundreds of tutorials; excellent for areas this course did not cover (RNA-seq, metagenomics, single-cell).
- **Bioconductor** ([bioconductor.org](https://www.bioconductor.org)): R packages and workflows for genomic data.
- **H3ABioNet** (search the name): African bioinformatics network with training, standards and community.
- **Nextstrain** ([nextstrain.org](https://nextstrain.org)): join the community, run a build on public data.
- **Africa CDC** ([africacdc.org](https://africacdc.org)): the Pathogen Genomics Initiative and related training opportunities.
- **WHO** ([who.int](https://www.who.int)): global strategies and guidance on genomics and surveillance.
- **PHG Foundation** ([phgfoundation.org](https://www.phgfoundation.org)): policy and implementation resources for public health genomics.
- **GA4GH** ([ga4gh.org](https://www.ga4gh.org)): standards work; open working groups welcome participation.

## Ideas for what to do next

1. **Rerun a published analysis** from its code and data; write down what was easy and what was hard.
2. **Join an open project:** answer a question on a bioinformatics forum, fix documentation, or add a tutorial.
3. **Learn one tool deeply:** a workflow manager (Snakemake or Nextflow), a mixed-model GWAS tool, or a phylogenetic dating method.
4. **Write it up:** turn your capstone into a short blog post or a preprint-style report with your supervisor's guidance.
5. **Teach it:** run a two-hour session on Week 2 or Week 3 for colleagues. Teaching reveals gaps in understanding.

{% endtab %}

{% tab title="7 · Contribute" %}

You can help improve this week and the course as a whole. Open an issue with the label **`week-12`** or edit the file directly - see [How to contribute](../contribute/README.md).

## Ideas for experts

1. **Capstone exemplars:** a fully worked, openly licensed example project for each track, with a model report and a model peer review.
2. **Autograding:** extend `scripts/capstone_check.sh` into a checker for each track's key outputs (keep the checks about *results*, not code style).
3. **Real-data tracks:** well-documented public datasets (with licences and ethics notes) for learners who have completed the toy data.
4. **Workflow tracks:** a Snakemake or Nextflow capstone for learners who want to scale up.
5. **Assessment:** an expanded rubric with level descriptors, and calibration examples for reviewers.
6. **Community:** a regular open "show and tell" session where graduates present their capstones.

**Version notes:** the check script was tested with bash on Ubuntu 24.04 (October 2026) against a complete set of results from Weeks 3-11.

{% endtab %}

{% endtabs %}
