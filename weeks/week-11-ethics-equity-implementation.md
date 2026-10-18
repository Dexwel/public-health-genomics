---
description: Ethics, equity, governance and implementation of genomics in public health - consent, re-identification risk (measured on real course data), data sharing principles, benefit sharing, and how to move from a pilot to a programme.
---

# Week 11 — Ethics, equity and implementation

{% hint style="info" %}
**At a glance** · **Time:** ~6-8 h · **Prerequisites:** Weeks 1, 3, 9, 10 (the Week 3 clean line list is used in the lab) · **You will produce:** a re-identification risk table, a data-sharing decision, a short governance policy and an implementation roadmap · **Tools:** R · **Data:** your Week 3 output
{% endhint %}

{% tabs %}

{% tab title="1 · Start here" %}

## Why this matters

Genomic data are unlike most health data. They are **identifying** (nobody else has your genome), **familial** (your result says something about your relatives), **persistent** (it does not change when you move or change your name) and **shared across populations** (a finding about one community can affect others). The technical skills of Weeks 2-10 are only useful if the data are collected with trust and used fairly.

History shows what goes wrong: samples taken for one purpose used for another; communities studied but left without benefit; sequence data from one country used in ways its people did not anticipate. A public health genomics programme earns its legitimacy by getting governance right *before* the first sample is sequenced.

This week combines discussion with one hands-on measurement: you will calculate how identifiable the cases in your own cleaned line list are, using only district, age, sex and dates, and see why "we removed the names" is not enough.

## Learning objectives

By the end of this week you will be able to:

1. **Explain** why genomic data raise special privacy, consent and group-harm issues.
2. **Compare** consent models (specific, broad, dynamic, community) and **apply** them to a scenario.
3. **Measure** re-identification risk with k-anonymity and **reduce** it by generalising.
4. **Use** the FAIR and CARE principles together, and **describe** what responsible data sharing looks like.
5. **Identify** equity concerns in genomic research, access to benefits, and data representation.
6. **Draft** a governance policy and an implementation roadmap for a small genomic surveillance programme.

## Roadmap

| Step | Time | Tab |
|---|---|---|
| Pre-check | 10 min | 1 · Start here |
| Concepts | 90 min | 2 · Concepts |
| Conversation | 20 min | 3 · Conversation |
| Lab | 2-3 h | 4 · Hands-on lab |
| Practice | 90 min | 5 · Practice |

## Key terms

| Term | Plain meaning |
|---|---|
| **Informed consent** | A person's voluntary agreement based on understanding |
| **Broad consent** | Agreement to future, unspecified research within defined limits |
| **De-identification** | Removing direct identifiers (name, ID number) |
| **Re-identification** | Working out who a "de-identified" record belongs to |
| **k-anonymity** | Each record shares its key attributes with at least k−1 others |
| **FAIR** | Findable, Accessible, Interoperable, Reusable (about data) |
| **CARE** | Collective benefit, Authority to control, Responsibility, Ethics (about people) |
| **Benefit sharing** | Returning value (results, capacity, access) to those who contributed |

## Pre-check

1. Name three things that make genomic data different from, say, a blood-pressure reading.
2. A dataset has no names, but each row has exact date of birth, district and sex. Can people be identified?
3. A study finds a gene variant that is more common in one community. What harms (beyond individual privacy) could follow?
4. Who owns a genomic sequence from a person?

<details>

<summary>Show answers</summary>

1. It is unique to the individual, it reveals information about relatives, and it is permanent (and can be re-analysed for purposes unknown at collection).
2. Very probably yes: those three attributes are enough to single out many people, and can be linked to other data (such as voter or school records).
3. Stigma, discrimination (insurance, employment, marriage), misuse of "ancestry" claims, or loss of trust - group harms.
4. "Ownership" is the wrong frame in many legal systems; what exists is a bundle of rights and duties (consent, control, access, use) set by law, the data-protection regime, and the agreements with the contributors and community. Check your jurisdiction.

</details>

{% endtab %}

{% tab title="2 · Concepts" %}

## 2.1 What makes genomic data special

| Property | Consequence |
|---|---|
| **Uniquely identifying** | True anonymisation of a whole genome is hard; even short stretches can link to relatives in other databases |
| **Familial** | A person's result implicates relatives who did not consent |
| **Persistent and re-usable** | Today's "no known meaning" variant may be meaningful in ten years |
| **Group-level** | Findings can stigmatise populations, not just individuals |
| **Valuable** | Commercial interest raises issues of ownership and benefit |

## 2.2 Consent models

| Model | What it is | Strength | Weakness |
|---|---|---|---|
| **Specific** | Consent for one named study | Clear | Re-contacting people is costly; data cannot be reused |
| **Broad** | Consent for future research within limits, with oversight | Efficient; supports data sharing | People may not understand "future"; needs strong governance |
| **Tiered** | Individual chooses categories (e.g., cancer research only; sharing with industry yes/no) | Respects preferences | Complex to administer |
| **Dynamic** | Ongoing digital interaction; can change choices | Participatory | Needs infrastructure and literacy |
| **Community** (engagement or consent) | Agreement of community leaders or bodies *in addition to* individual consent | Recognises group interests | Defining "the community" and its legitimate representatives is hard |

Public health surveillance often operates under legal authority *without* individual consent (notifiable disease reporting). That use is typically limited to specified purposes with strong safeguards; **research** uses of the same data usually require ethics review and may require consent. Know which regime applies.

### Return of results

If you find something important (for example an actionable variant), do you tell the person? Frameworks differ. A programme must decide **in advance** what it will and will not return, and whether participants may decline.

## 2.3 Privacy and re-identification

**Direct identifiers** (name, national ID, phone) are removed first. But **quasi-identifiers** - district, age, sex, dates - can be combined and linked with other sources to re-identify someone. **k-anonymity** measures this: a record has *k* if it shares its combination of quasi-identifiers with k−1 others. A record with **k = 1 is unique**. Remedies:

- **Generalise:** exact age → age band; date → week or month; district → region.
- **Suppress:** hide small cells (for example counts below 5) in published tables.
- **Control access:** share detailed data only under agreements, in secure environments.
- **Minimise:** do not collect or release what you do not need.

k-anonymity is a simple measure and not a guarantee (it ignores what an attacker already knows), but it is a very useful first check.

## 2.4 FAIR and CARE

**FAIR** is about making data usable by machines and people: findable (identifiers, metadata), accessible (clear access conditions - not necessarily "open"), interoperable (standard formats and vocabularies), reusable (provenance, licence). **CARE** (from the Global Indigenous Data Alliance) is about people: **C**ollective benefit, **A**uthority to control, **R**esponsibility, **E**thics. FAIR alone says nothing about whether sharing is fair or consented; CARE keeps the data tied to the interests of the people they come from. Use both: "**as open as possible, as closed as necessary**".

## 2.5 Governance building blocks

| Component | What it does |
|---|---|
| **Ethics review** | Independent assessment of research protocols |
| **Data access committee** | Decides who may use controlled-access data, for what |
| **Data sharing agreement / material transfer agreement** | Legal terms: purpose, security, no re-identification, publication, benefit |
| **Data protection law** | Binding rules (examples: the Nigeria Data Protection Act 2023, South Africa's POPIA, the EU GDPR); check the law that applies to you |
| **Community engagement** | Meaningful involvement before, during and after |
| **Standards** | GA4GH frameworks and tools for responsible sharing, e.g. data-use ontologies |

For **pathogens**, access and benefit sharing also arises under international agreements (for example the Nagoya Protocol on genetic resources) and under the principles adopted by the WHO and partners for sharing pathogen data. Policy here is evolving; check current guidance.

## 2.6 Equity

Equity in genomics has three faces:

1. **Representation.** Most participants in large genomic studies are of European ancestry; reference data and tools therefore work less well elsewhere (Weeks 4 and 9).
2. **Access.** Technology, sequencing capacity and the ability to act on results are unevenly distributed.
3. **Benefit and credit.** Local researchers, laboratories and communities should be partners, not only sample sources: authorship, capacity building, shared data and technology transfer. Initiatives such as H3Africa and the Africa CDC Pathogen Genomics Initiative aim to build local capability.

## 2.7 From pilot to programme: implementation

A successful pilot is not a programme. Use an implementation framework (for example **CFIR** to examine context and barriers, **RE-AIM** to plan and evaluate Reach, Effectiveness, Adoption, Implementation, Maintenance). Questions to ask:

| Domain | Questions |
|---|---|
| Need and value | What decision will genomic data change? For whom? |
| Capacity | Laboratory, bioinformatics, supply chain, electricity, internet, workforce |
| Sustainability | Who pays in year 3? What if donor funding ends? |
| Integration | How do results reach the clinician or the programme manager? |
| Quality | Accreditation, external quality assessment, validation (Week 6) |
| Ethics and law | Consent basis, data protection, governance (this week) |
| Evaluation | Which indicators show benefit? Harm? |

{% hint style="info" %}
**Public health lens.** The question is not "can we sequence?" but "should we, for whom, with what safeguards, and what will change because of it?"
{% endhint %}

{% endtab %}

{% tab title="3 · Conversation" %}

*The Ministry's ethics board room. A long table, six chairs. A pile of consent forms. Dr. Mensah chairs; Zainab is presenting for the first time; Tunde, as the data lead, is asked to answer the hard questions.*

**Dr. Mensah:** Zainab, you wish to put the cleaned line list on an open data portal. Tell the board why.

**Zainab:** Transparency. Researchers elsewhere could use it. And the names are already gone: no case IDs beyond a number, no phone numbers, no addresses.

**Dr. Mensah:** Tunde, you ran a check last night.

**Tunde:** I counted how many people are unique in the data using only four things: district, sex, age and the date of onset.

**Zainab:** Those are not identifying. There are six hundred cases and only five districts.

**Tunde:** With the exact onset date, 467 of 471 complete records are unique. Ninety-nine percent.

**Zainab:** That can't be. You could not find *me* from district, age and a date.

**Tunde:** Could a neighbour? A health worker who saw the case? Someone with a school register? If you know a woman aged 34 got sick in Lakeside on the ninth of February, you know exactly which row to read. And the row tells you whether she died.

**Zainab:** (pause) I hadn't thought about "who might already know part of it."

**Dr. Mensah:** That is the question privacy engineers ask. What can you do to reduce the risk?

**Zainab:** Round the age into bands. Report the week, not the day.

**Tunde:** That brings unique records down from 99% to 35%. Use the month instead of the week and it falls to 14%. Drop sex and use only district, age band and month, and it's under 7%.

**Zainab:** So I can lower the risk, but not to zero. And every time I generalise, the data are less useful. The epidemic curve by day is gone.

**Dr. Mensah:** Exactly. There is no "safe" dataset, only a trade-off between risk and utility, and the decision must be taken with the people concerned, not for them. What else would you ask before sharing?

**Zainab:** Who will use it? For what? Whether the patients agreed to it.

**Dr. Mensah:** The patients. Tunde, were these cases asked?

**Tunde:** Notifiable disease reporting is a legal duty. There was no individual consent for research use or publication.

**Zainab:** Then the legal basis for surveillance does not stretch to open release.

**Dr. Mensah:** Good. And what about the *community*? The districts that are over-represented in the sequences will look like hotspots on any map.

**Zainab:** They could be stigmatised. "Lakeside is the outbreak district."

**Tunde:** And Highland barely appears, simply because the samples didn't get here.

**Dr. Mensah:** So a published map could harm the very district that is best at sending samples, and ignore the district that is not. Fairness again. Zainab, give the board your revised proposal.

**Zainab:** A tiered approach. A public summary: counts by district and month, small numbers suppressed. A controlled-access dataset with weekly dates and age bands, released through a data access committee under an agreement that forbids re-identification and requires the district health teams to be told and credited. And the exact data stay in the Ministry.

**Dr. Mensah:** And benefit sharing?

**Zainab:** Training for the district laboratories and a commitment to return results within a week, before anything is published.

**Dr. Mensah:** Does the board agree? (pause) The motion carries. Zainab, you came in to open the data and you have redesigned the policy. That is what governance is for.

### Talking points for the forum

1. A researcher abroad asks for the controlled-access dataset and wants to share it with a company. What conditions would you impose?
2. How should a community be involved *before* a sequencing programme begins? Who speaks for the community?
3. What would "benefit" look like to a district health team that supplies samples? To patients?

{% endtab %}

{% tab title="4 · Hands-on lab" %}

{% hint style="success" %}
**Lab goal.** Measure re-identification risk in the cleaned line list from Week 3, reduce it by generalising, and write a data-sharing decision. Run from the repository root; `results/week03/linelist_clean.csv` must exist (run Week 3's script if it does not).
{% endhint %}

```bash
mkdir -p results/week11 && cd results/week11
ls ../week03/linelist_clean.csv
```

## Part A - Measure k-anonymity (45 min)

Save as `reidentification_risk.R` and run `Rscript reidentification_risk.R`:

```r
# reidentification_risk.R - how identifiable are people in a "de-identified" line list? (Week 11)
suppressPackageStartupMessages({library(readr); library(dplyr)})
ll <- read_csv("../week03/linelist_clean.csv", show_col_types = FALSE) %>%
  mutate(age_exact = age,
         age_band  = cut(age, c(-Inf, 4, 14, 44, 64, Inf), labels = c("0-4", "5-14", "15-44", "45-64", "65+")),
         week      = as.Date(cut(date_onset, "week")),
         month     = format(date_onset, "%Y-%m"))
cat("Rows:", nrow(ll), "\n")
k_report <- function(df, keys, label) {
  d <- df %>% filter(if_all(all_of(keys), ~ !is.na(.))) %>% group_by(across(all_of(keys))) %>% mutate(k = n()) %>% ungroup()
  cat(sprintf("%-46s complete rows %3d | unique (k=1): %3d (%4.1f%%) | k<5: %3d (%4.1f%%) | smallest k = %d\n",
              label, nrow(d), sum(d$k == 1), 100 * mean(d$k == 1), sum(d$k < 5), 100 * mean(d$k < 5), min(d$k)))
  invisible(d)
}
k_report(ll, c("district", "sex", "age_exact", "date_onset"),   "district + sex + exact age + exact onset date")
k_report(ll, c("district", "sex", "age_exact", "week"),         "district + sex + exact age + onset week")
k_report(ll, c("district", "sex", "age_band", "week"),          "district + sex + age band + onset week")
k_report(ll, c("district", "sex", "age_band", "month"),         "district + sex + age band + onset month")
k_report(ll, c("district", "age_band", "month"),                "district + age band + onset month")
k_report(ll, c("district", "month"),                            "district + onset month")
```

```text
Rows: 600
district + sex + exact age + exact onset date  complete rows 471 | unique (k=1): 467 (99.2%) | k<5: 471 (100.0%) | smallest k = 1
district + sex + exact age + onset week        complete rows 471 | unique (k=1): 445 (94.5%) | k<5: 471 (100.0%) | smallest k = 1
district + sex + age band + onset week         complete rows 471 | unique (k=1): 165 (35.0%) | k<5: 402 (85.4%) | smallest k = 1
district + sex + age band + onset month        complete rows 471 | unique (k=1):  67 (14.2%) | k<5: 189 (40.1%) | smallest k = 1
district + age band + onset month              complete rows 526 | unique (k=1):  35 ( 6.7%) | k<5: 127 (24.1%) | smallest k = 1
district + onset month                         complete rows 573 | unique (k=1):   3 ( 0.5%) | k<5:  23 ( 4.0%) | smallest k = 1
```

**How the code works.** For each choice of quasi-identifiers (the "keys") the script keeps rows complete on those keys, counts how many rows share each combination (`k`), and reports the share that is unique (`k = 1`) and the share with `k < 5` (a common minimum cell size for publication). "Complete rows" differ between lines because missing values (Week 3) reduce the number of usable rows.

**Interpret.**

| What is released | Records unique | Records in groups < 5 |
|---|---|---|
| district + sex + exact age + exact date | **99.2%** | 100% |
| ... with onset *week* instead of date | 94.5% | 100% |
| ... with age *band* | 35.0% | 85.4% |
| ... with onset *month* | 14.2% | 40.1% |
| district + age band + month (no sex) | 6.7% | 24.1% |
| district + month only | 0.5% | 4.0% |

Even the coarsest useful release leaves some small groups (4% of rows in cells under 5). Each step towards privacy removes detail: the last row cannot show an age pattern or a sex difference. **There is no free lunch.**

## Part B - What would an attacker add? (30 min)

k-anonymity assumes the attacker knows only the released quasi-identifiers. Think about, and write down, three **linkage** sources in your own setting (for example hospital registers, school lists, social-media posts, funeral announcements) and what each could add. Then answer: *does a case's outcome (died / alive) create an additional harm if the row is identified?* In this dataset, which rows are the most sensitive?

## Part C - Decide and justify (45 min)

Write `results/week11/sharing_decision.md` (≤400 words). Use this template:

```text
DATA-SHARING DECISION
Dataset: Week 3 cleaned line list (600 cases)
Requested use: <who, why>
Legal/ethical basis for original collection: <e.g., statutory surveillance; no individual research consent>
Tier 1 - public: <what exactly: e.g., counts by district and month, cells < 5 suppressed>
Tier 2 - controlled access: <fields; generalisation; risk (k-anonymity numbers from Part A); conditions>
Tier 3 - internal only: <fields>
Conditions: no re-identification; no linkage without approval; no onward sharing; acknowledgement of district teams; results returned before publication
Benefit sharing: <training, capacity, access to results>
Review: <who decides, how often, how a complaint is handled>
Risks accepted and residual: <numbers>
```

## Part D - FAIR and CARE audit (30 min)

Apply this checklist to the course's own data (`data/README.md`) and to your Tier 2 release:

| Question | FAIR | CARE |
|---|---|---|
| Is there a persistent identifier and metadata? | F | |
| Is the access condition stated? | A | A (authority) |
| Do standard formats and vocabularies exist? | I | |
| Is there a licence and provenance? | R | |
| Who benefits and how are they involved? | | C (collective benefit) |
| Who controls secondary use? | | A (authority to control) |
| Who is accountable for harm? | | R (responsibility) |
| Were ethics considered, including group harms? | | E (ethics) |

(The course's data are synthetic, so no real people are involved; use the audit as practice.)

## Part E - An implementation roadmap (60 min)

Write a one-page roadmap (`roadmap.md`) for a 3-year programme to sequence priority pathogens in a country you know: Year 1 (governance, laboratory validation, 2 sentinel sites), Year 2 (expand, link to surveillance reports), Year 3 (sustain, evaluate). For each year list: **people, laboratory, bioinformatics, data governance, funding, indicators**. Include at least three **RE-AIM** indicators (for example proportion of notified cases sequenced by district; median days from sample to report; proportion of reports used in a public health action).

## If it breaks

| Message or symptom | Likely cause | Fix |
|---|---|---|
| `cannot open file '../week03/linelist_clean.csv'` | Week 3 not run | Run Week 3 first, or copy the file from your Week 3 results |
| Different percentages | You changed the cleaning script | Check that the clean list has 600 rows and the age/date columns |
| `could not find function "if_all"` | Old dplyr (< 1.0.4) | Update dplyr |
| `week` column NA | `date_onset` stored as text | Make sure `read_csv` parses dates (check `class(ll$date_onset)`) |

## Stretch challenge

1. Add `facility_type` as a further key. How much does uniqueness rise?
2. Add **suppression**: for the 3-key release (district + age band + month), replace the values in groups with k < 5 by "other" and recompute the shares.
3. Implement `l-diversity` for outcome: among groups with k ≥ 5, how many contain only one outcome value (everyone alive)? Why does that matter?

{% endtab %}

{% tab title="5 · Practice" %}

## Exercises

### Basic

**Exercise 1.** Define quasi-identifier and give three examples from a line list.

**Exercise 2.** What is the difference between FAIR and CARE?

**Exercise 3.** According to Part A, how does coarsening the date from day to week change the share of unique records? From week to month (with age bands and sex)?

<details>

<summary>Show answers (1-3)</summary>

1. An attribute that is not a name or ID but can single someone out when combined with others or linked to other data: district, age, sex, date of onset, facility.
2. FAIR describes properties of data (findable, accessible, interoperable, reusable); CARE describes people-centred obligations (collective benefit, authority to control, responsibility, ethics). Use both.
3. Day → week: 99.2% → 94.5% unique (little change with exact age). Week → month (with age band and sex): 35.0% → 14.2%.

</details>

### Intermediate

**Exercise 4.** You are asked to release the line list to a university team. Which tier of your decision would apply, which fields would you generalise, and what would you require in the agreement?

**Exercise 5.** A district health officer objects: "Our samples built this dataset, but we only found out about the publication afterwards." List four actions that would have prevented this.

**Exercise 6.** In Week 3 you found that 82% of Coastal Hub cases were sequenced against 10% of Highland cases. Explain two equity problems this creates for a public map of "sequenced cases".

<details>

<summary>Show answers (4-6)</summary>

4. Tier 2 (controlled access). Generalise age to bands, dates to week or month, remove or aggregate facility; require a data-use agreement with a purpose limitation, no re-identification or linkage, secure storage, deletion on completion, no onward sharing, acknowledgement of the district teams, and a review of outputs before publication.
5. Involve district teams from the design stage; specify co-authorship or acknowledgement in the agreement; share draft results for comment before publication; agree a publication plan; provide training or capacity in return.
6. Coastal Hub would look like the hotspot (more sequences) and could be stigmatised or over-resourced; Highland would look free of disease despite 49 cases, and be under-served. Conclusions about geography would reflect laboratory access, not disease.

</details>

### Challenge

**Exercise 7.** Draft a one-page *community engagement plan* for a new pathogen sequencing programme, covering who, when, how, and what decisions the community would have a real say in.

**Exercise 8.** Role-play: a pharmaceutical company offers to fund your sequencing programme in exchange for exclusive access to the data. Write the three conditions you would insist on and one you would refuse.

<details>

<summary>Show answers (7-8)</summary>

7. A good plan names representatives chosen by the community (not only officials), starts before sample collection, uses local languages and formats, includes feedback and complaint mechanisms, and states which decisions are shared (for example the data access rules and whether results are published).
8. Example conditions to insist on: public-interest access (data also available to the public-health system and academic users); benefit sharing (capacity building, affordable access to any products); independent governance (data access committee including local members). Refuse: exclusive, permanent control of the data or any right to restrict the programme from publishing and sharing for public health.

</details>

## Self-test (8 questions)

1. A record with k = 1 is: (a) shared by many others (b) unique on the chosen attributes (c) anonymous (d) encrypted
2. Which makes a dataset safer? (a) Exact dates (b) Generalising age into bands (c) Adding more columns (d) Adding sequence data
3. FAIR stands for: (a) Findable, Accessible, Interoperable, Reusable (b) Free, Accessible, Independent, Reliable (c) Fast, Accurate, Integrated, Reproducible (d) none
4. CARE emphasises: (a) speed (b) collective benefit and authority to control (c) file formats (d) cost
5. Statutory disease notification generally: (a) always allows open data release (b) is for surveillance purposes and does not automatically permit other uses (c) needs no safeguards (d) is the same as research consent
6. A group-level harm from a genomic finding is: (a) a lab error (b) stigmatisation of a community (c) a missing value (d) a bad plot
7. Why is whole-genome anonymisation hard? (a) Genomes are large (b) A genome is itself identifying and links to relatives (c) Names are inside (d) Compression
8. The best time to engage a community is: (a) after publication (b) before and throughout the programme (c) never (d) only if funding requires

<details>

<summary>Show answers and reasons</summary>

1. **(b)**
2. **(b)**
3. **(a)**
4. **(b)**
5. **(b)**
6. **(b)**
7. **(b)**
8. **(b)**

</details>

## Reflection prompt (150-250 words)

Describe a research or surveillance project you know in which participants or communities were not fully involved. What would a better process have looked like, and what would it have cost?

## Portfolio mini-deliverable

`results/week11/`: `reidentification_risk.R`, the printed risk table, `sharing_decision.md`, and `roadmap.md`.

{% endtab %}

{% tab title="6 · Go deeper" %}

## Core resources

- **GA4GH** ([ga4gh.org](https://www.ga4gh.org)): the Framework for Responsible Sharing of Genomic and Health-Related Data, data-use ontologies and policy tools; start with the policy section of the site.
- **Global Indigenous Data Alliance - CARE Principles** ([gida-global.org](https://www.gida-global.org)): the principles, with explanations and case studies.
- **GO FAIR** ([go-fair.org](https://www.go-fair.org)): the FAIR principles and implementation guidance.
- **H3Africa** ([h3africa.org](https://h3africa.org)): governance documents, community engagement experience, and data-sharing policies from a large African genomics consortium.
- **WHO** ([who.int](https://www.who.int)): search for WHO guidance on human genome data collection, access, use and sharing, and on pathogen data sharing.
- **PHG Foundation** ([phgfoundation.org](https://www.phgfoundation.org)): policy analysis on genomics and equity in health systems.
- **Africa CDC** ([africacdc.org](https://africacdc.org)): the Pathogen Genomics Initiative and continental policy on data sharing.
- **Nagoya Protocol**: search for "Nagoya Protocol access and benefit-sharing" on the Convention on Biological Diversity website.
- **Data protection law in your country**: search for the national authority (for example, the Nigeria Data Protection Commission) and the current Act.
- **Implementation science:** search for "Consolidated Framework for Implementation Research (CFIR)" and "RE-AIM framework".

## Cases to read about (search by name)

- The Havasupai Tribe and the Arizona Board of Regents (consent and secondary use of samples).
- Henrietta Lacks and the HeLa cell line (consent, ownership and benefit).
- Public debates on sharing pathogen sequence data during the COVID-19 pandemic.

{% endtab %}

{% tab title="7 · Contribute" %}

You can help improve this week. Open an issue with the label **`week-11`** or edit the file directly - see [How to contribute](../contribute/README.md).

## Ideas for experts

1. **Local law boxes:** short, cited summaries of data-protection and research-ethics rules in your country (with the date you checked them).
2. **Consent materials:** translated, user-tested consent and information leaflets (see the [data policy](../contribute/data-policy.md)).
3. **Community case study:** a written case with the community's permission, on engagement in a genomics project.
4. **Differential privacy:** an introduction and a small tested R example, as a comparison with k-anonymity.
5. **Benefit-sharing models:** a comparison of real agreements (with sources).
6. **Costing:** a template for the cost of a genomic surveillance programme.
7. **Translations:** the *Concepts* tab (label `translation`).

**Version notes:** tested with R 4.3.3 and dplyr 1.1.4 on Ubuntu 24.04 (October 2026). Laws and guidance change; always check the current version.

{% endtab %}

{% endtabs %}
