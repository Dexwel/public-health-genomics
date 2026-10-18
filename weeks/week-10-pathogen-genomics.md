---
description: Turn pathogen sequences into outbreak intelligence - SNP distances, clusters, trees, resistance mutations and the epidemiology to interpret them - and learn the biases that can mislead.
---

# Week 10 — Pathogen genomics and surveillance

{% hint style="info" %}
**At a glance** · **Time:** ~8-10 h · **Prerequisites:** Weeks 3, 6, 7 · **You will produce:** a cleaned metadata table, a SNP-distance matrix, clusters, a neighbour-joining tree, a resistance analysis, an epidemic curve by cluster and a short outbreak briefing · **Tools:** R (ape, dplyr, readr), optionally IQ-TREE 2 · **Data:** `data/outbreak` (73 bacterial isolates, 4,000-site alignment)
{% endhint %}

{% tabs %}

{% tab title="1 · Start here" %}

## Why this matters

Pathogen genomics is where public health genomics has had its greatest operational impact. Sequencing every isolate from an outbreak shows which cases belong together, whether a new introduction has occurred, whether transmission is happening inside a hospital, and whether a drug-resistance mutation is spreading. During the COVID-19 pandemic, sequencing networks and open platforms such as Nextstrain changed how outbreaks are tracked, and African laboratories built substantial capacity through the Africa CDC Pathogen Genomics Initiative.

Genomic data alone do not tell the story. They must be joined to **who, where and when**, and read with an awareness of **who was sampled**. This week you analyse a synthetic outbreak of a bacterial pathogen, find clusters, link them to places and dates, track a resistance mutation, and identify the data problems that would mislead a naive analyst.

## Learning objectives

By the end of this week you will be able to:

1. **Explain** how SNP distance reflects relatedness and **why** thresholds are pathogen-specific.
2. **Validate** an alignment and its metadata: ambiguous bases, duplicates, impossible dates.
3. **Compute** a pairwise SNP-distance matrix and **cluster** isolates at several thresholds.
4. **Build and read** a neighbour-joining tree.
5. **Link** genomic clusters to district, facility and time, and **recognise** a hospital transmission cluster.
6. **Analyse** a resistance mutation: association with phenotype, discordant isolates and convergent evolution.
7. **Describe** sampling bias, and write an honest genomic briefing.

## Roadmap

| Step | Time | Tab |
|---|---|---|
| Pre-check | 10 min | 1 · Start here |
| Concepts | 90 min | 2 · Concepts |
| Conversation | 20 min | 3 · Conversation |
| Lab | 4-5 h | 4 · Hands-on lab |
| Practice | 90 min | 5 · Practice |

## Key terms

| Term | Plain meaning |
|---|---|
| **Isolate** | A pure culture of the pathogen from one patient or sample |
| **Alignment** | Sequences lined up so each column is one genome position |
| **SNP distance** | Number of positions at which two isolates differ |
| **Cluster** | Group of isolates close enough to suggest recent shared transmission |
| **Phylogeny / tree** | Diagram of relatedness |
| **Lineage** | A larger group sharing a common ancestor |
| **Convergence** | The same mutation arising independently in unrelated isolates |
| **Genotype-phenotype discordance** | A mutation without the expected resistance, or vice versa |

## Pre-check

1. Two isolates differ at 0 positions out of 4,000. Does that prove one patient infected the other?
2. A resistance mutation appears in 17 isolates. Are they necessarily related?
3. Why can a sequence with 12% ambiguous bases distort a cluster analysis?
4. If 80% of the genomes come from one hospital, what can you not say about the outbreak?

<details>

<summary>Show answers</summary>

1. No. Identical genomes are *compatible* with direct transmission but also with a common source or with slow evolution; epidemiological evidence is needed.
2. No. Mutations can arise independently (convergence) under drug pressure.
3. Ambiguous bases are ignored or treated as differences depending on the method, producing spurious distances or hiding true ones.
4. You cannot say how common the strain is elsewhere: the sample over-represents one place.

</details>

{% endtab %}

{% tab title="2 · Concepts" %}

## 2.1 What a pathogen genome tells you

Pathogens mutate at a roughly constant rate, so the number of differences between two isolates grows with time since they shared an ancestor. For a bacterium such as *Mycobacterium tuberculosis* a few SNPs per year are typical; for SARS-CoV-2, tens per year; each organism needs its own thresholds. Genomic data can:

| Question | How genomes help |
|---|---|
| Are these cases linked? | Clusters of near-identical genomes |
| Where did it come from? | Placement in a global tree |
| Is it spreading in a hospital or the community? | Cluster membership vs facility |
| Is there a new variant or resistance? | Mutation analysis |
| Has the outbreak ended? | Absence of new members of the cluster |

They cannot, alone, tell **who infected whom** or **the direction** of transmission.

## 2.2 From reads to a comparable alignment

Week 6's pipeline applied to each isolate gives variant calls; for outbreak work these are usually converted to a **whole-genome alignment** (or a core-genome alignment): every isolate's sequence laid out position by position. Quality control comes first: low-coverage or contaminated isolates produce many ambiguous bases (`N`).

{% hint style="warning" %}
**Ambiguous bases are not differences.** Compare isolates only over positions called in both (*pairwise deletion*), and consider excluding isolates with more than about 5% ambiguity.
{% endhint %}

## 2.3 SNP distances and clusters

The **SNP distance** between two isolates is the count of positions where both have a determined base and they differ. A **cluster** is a set linked by distances below a threshold. Two practical points:

1. **Thresholds are organism- and question-specific.** Published examples include a few SNPs for *M. tuberculosis* recent transmission and a handful or fewer for many outbreak-causing bacteria; always check the literature for your pathogen.
2. **The linkage rule matters.** *Single linkage* chains: A joins B, B joins C, so A and C land in one cluster even if they differ more than the threshold. It is sensitive but can merge distinct chains. *Complete linkage* is strict. Report both the threshold and the rule.

## 2.4 Trees

A **neighbour-joining (NJ)** tree is a fast distance-based tree. **Maximum-likelihood** methods (IQ-TREE, RAxML) model the evolution of sequences and give better trees, with confidence values. Reading a tree:

- Tips are isolates; branch lengths are proportional to SNP differences (or time).
- Isolates that share a recent common ancestor sit together; a cluster appears as a tight clade.
- The tree can be **rooted** with an outgroup; unrooted trees do not show direction of time.
- A tree is a *hypothesis* about relatedness, not a transmission tree.

## 2.5 Genotype and phenotype: resistance

A resistance **mutation** (genotype) predicts a resistance **phenotype** (the isolate grows in the presence of the drug), but imperfectly. Reasons for discordance: other resistance mechanisms, heteroresistance (mixed populations), laboratory error, or a compensatory change. Convergent evolution can produce the same mutation in unrelated lineages; **resistance in two isolates does not mean the two are related.**

## 2.6 Metadata is half the data

A genome without date, place and facility is almost useless. Typical metadata problems: duplicated records, mistyped dates, inconsistent place names, mislabelled isolates. A single typo, such as the year 2025 instead of 2026, can move a case a year back and corrupt the epidemic curve.

## 2.7 Sampling bias

Genomic surveillance observes only the isolates that were *collected, cultured, sent and sequenced*. If one hospital sends all its isolates and a rural clinic sends none, the genomic picture reflects the hospital (Week 3's sequencing-coverage lesson). Always report the sequencing fraction (sequenced / notified) by place and time.

## 2.8 Data sharing and governance

Sequences and metadata are shared through the public archives (the INSDC databases ENA/NCBI/DDBJ) and through platforms such as **GISAID** and **Pathoplexus** with different access models. The same data can be used to trace individuals or stigmatise communities; metadata should be minimised (for example, district rather than address, age bands rather than date of birth) and sharing governed by agreements. Week 11 returns to this.

{% hint style="info" %}
**Public health lens.** A genomic cluster is a prompt for investigation, not a conclusion. The standard sentence is: "These isolates are genetically very close; the epidemiological investigation will determine whether they are linked."
{% endhint %}

{% endtab %}

{% tab title="3 · Conversation" %}

*The Ministry's emergency room. A map of five districts is pinned to the wall; coloured pins mark cases. Zainab has a freshly printed tree. Dr. Mensah is sipping cold tea. Tunde has just arrived, out of breath.*

**Tunde:** The alignment's in. Seventy-three isolates, four thousand sites. Before anything else, two problems with the metadata.

**Zainab:** Seventy-four rows for seventy-three isolates.

**Tunde:** One isolate, ISO-011, is listed twice. Identical rows, so safe to drop. The second problem is worse. Look at the dates.

**Zainab:** The range runs from February 2025 to June 2026. The outbreak started this January. (pause) One isolate, ISO-014, is a year early.

**Tunde:** A typo. Twenty twenty-five instead of twenty twenty-six. If I'd drawn the epidemic curve straight from the file, there would be a lone case a year before everything else, and a headline about "an undetected early introduction".

**Dr. Mensah:** And that is the kind of error that gets into a newspaper. What next?

**Tunde:** Sequence quality. Two isolates, ISO-001 and ISO-003, have more than eleven percent ambiguous bases. I excluded them.

**Zainab:** Isn't that throwing away cases?

**Tunde:** They are still cases in the line list. I just don't trust their distances. Ambiguity makes them look different from everything, or identical to anything.

**Zainab:** All right. Now the tree. There are three tight groups and a lot of long lonely branches.

**Dr. Mensah:** Tell me what you see.

**Zainab:** A blue group of thirty. An orange group of fifteen. A green group of eight. Eighteen isolates sitting alone.

**Tunde:** I clustered with a five-SNP threshold. Green has zero differences between its eight isolates. All eight are from Hospital H, within twelve days.

**Zainab:** That's a hospital outbreak. Identical genomes, one ward, two weeks.

**Dr. Mensah:** Careful with that word. What can you say, and what can't you?

**Zainab:** That the genomes are indistinguishable and the patients share a facility and a time window. It *suggests* transmission inside the hospital. But I can't say who infected whom, or rule out a contaminated device that infected them all separately.

**Dr. Mensah:** Good. Blue?

**Tunde:** Districts A and B, from late January to mid-March. Thirty isolates, within-cluster distances up to fourteen SNPs, but they chain together.

**Zainab:** Up to fourteen? You said the threshold was five.

**Tunde:** Single linkage. Each isolate is within five of *some* other isolate, so the chain holds, even though the two ends differ by fourteen. At a two-SNP threshold blue splits into two groups.

**Zainab:** So the clusters depend on the threshold.

**Dr. Mensah:** They always do. Which is why we state the threshold and the linkage method whenever we report a cluster. Now: resistance.

**Tunde:** There's a mutation at alignment position 2731. Seventeen isolates carry it. Sixteen are resistant to ciprofloxacin, one is not.

**Zainab:** The orange cluster has all fifteen of them.

**Tunde:** Plus two sporadic isolates in other districts.

**Zainab:** So the two sporadic ones are part of the outbreak?

**Tunde:** Their genomes are forty-odd SNPs from anyone else. They are not related to orange. The same mutation arose twice, independently.

**Zainab:** Convergent evolution. Under drug pressure, the bacteria find the same escape.

**Dr. Mensah:** Which has a public-health implication: if you used the resistance mutation as a marker of "the outbreak strain", you would wrongly include those two.

**Zainab:** And the one susceptible isolate with the mutation?

**Tunde:** ISO-018. In the orange cluster. The mutation is there, the phenotype says susceptible.

**Zainab:** A lab error? Or the mutation doesn't always give resistance?

**Dr. Mensah:** It could be either; or the testing method was wrong; or the culture was mixed. What do you do?

**Zainab:** Ask the lab to repeat the susceptibility test and re-sequence.

**Dr. Mensah:** And in your report?

**Zainab:** I flag it. I don't quietly relabel it.

**Dr. Mensah:** Last question. We have thirty-nine cases in two districts and a cluster in a hospital. What do you *not* know?

**Zainab:** How many cases there were that were not sequenced. If a district sends nothing, it doesn't appear in the tree. The picture is only as complete as the sampling.

**Dr. Mensah:** Write that down in red. I told you we'd meet it again.

### Talking points for the forum

1. A cluster of eight identical genomes appears in one hospital. List the investigations you would launch, and the three alternative explanations you must exclude.
2. Your laboratory sequences 80% of cases in the capital and 10% in remote districts. How would you describe the data in a briefing?
3. Who should decide what metadata (for example exact dates, ward, age) is shared publicly when a cluster involves 8 identifiable patients?

{% endtab %}

{% tab title="4 · Hands-on lab" %}

{% hint style="success" %}
**Lab goal.** Go from an alignment and a line list to a cluster-level briefing. Everything below was run with R 4.3.3 and ape 5.7.1. Work in `results/week10` created from the repository root.
{% endhint %}

```bash
mkdir -p results/week10 && cd results/week10
D=../../data/outbreak
head -3 $D/outbreak_metadata.tsv; grep -c ">" $D/outbreak_alignment.fasta
Rscript -e 'for (p in c("ape","dplyr","readr","tidyr")) cat(p, requireNamespace(p, quietly = TRUE), "\n")'
```

All four packages should print `TRUE`. The `ape` package reads alignments and builds trees.

## Part A - Validate the data and cluster (75 min)

Save as `outbreak.R` and run `Rscript outbreak.R`:

```r
# outbreak.R - from alignment to clusters to epidemiology (Week 10). Run from results/week10.
suppressPackageStartupMessages({library(ape); library(dplyr); library(readr)})
D <- "../../data/outbreak"
aln  <- read.dna(file.path(D, "outbreak_alignment.fasta"), format = "fasta", as.character = FALSE)
meta <- read_tsv(file.path(D, "outbreak_metadata.tsv"), show_col_types = FALSE)
cat("Alignment:", nrow(aln), "isolates x", ncol(aln), "positions\n")

# 1. Metadata checks ------------------------------------------------------------------------
cat("Metadata rows:", nrow(meta), " distinct isolates:", n_distinct(meta$isolate_id), "\n")
cat("Duplicated isolate_id:", meta$isolate_id[duplicated(meta$isolate_id)], "\n")
meta <- distinct(meta)
cat("Collection date range:", format(range(as.Date(meta$collection_date))), "\n")
print(as.data.frame(meta %>% filter(as.Date(collection_date) < as.Date("2026-01-01") | as.Date(collection_date) > as.Date("2026-12-31"))))
stopifnot(setequal(rownames(aln), meta$isolate_id))

# 2. Sequence quality: how many ambiguous (N) bases per isolate? -------------------------------
pctN <- apply(as.character(aln), 1, function(x) 100 * mean(!x %in% c("a", "c", "g", "t")))
cat("\nIsolates with >5% ambiguous bases:\n"); print(round(pctN[pctN > 5], 1))
keep <- names(pctN)[pctN <= 5]
aln2 <- aln[keep, ]
cat("Kept:", length(keep), "isolates\n")

# 3. Variable sites and pairwise SNP distances -------------------------------------------------
var_sites <- sum(apply(as.character(aln2), 2, function(x) { x <- x[x %in% c("a","c","g","t")]; length(unique(x)) > 1 }))
cat("Variable sites:", var_sites, "of", ncol(aln2), "\n")
snp <- dist.dna(aln2, model = "N", pairwise.deletion = TRUE, as.matrix = TRUE)   # raw SNP counts
cat("Pairwise SNP distance: min", min(snp[upper.tri(snp)]), " median", median(snp[upper.tri(snp)]),
    " max", max(snp[upper.tri(snp)]), "\n")

# 4. Cluster at a SNP threshold and compare with the truth ---------------------------------------
truth <- read_tsv(file.path(D, "answers/clusters_truth.tsv"), show_col_types = FALSE)
hc <- hclust(as.dist(snp), method = "single")
for (thr in c(2, 5, 10, 20)) {
  cl <- cutree(hc, h = thr)
  cat(sprintf("\nThreshold <= %d SNPs: %d clusters; sizes: %s\n", thr, max(cl), paste(sort(table(cl), decreasing = TRUE), collapse = " ")))
}
write_tsv(tibble(isolate_id = names(cutree(hc, h = 5)), cluster5 = cutree(hc, h = 5)), "clusters_5snp.tsv")
saveRDS(list(aln = aln2, snp = snp), "outbreak_objects.rds")
```

```text
Alignment: 73 isolates x 4000 positions
Metadata rows: 74  distinct isolates: 73
Duplicated isolate_id: ISO-011
Collection date range: 2025-02-14 2026-06-09
  isolate_id collection_date district facility age sex   outcome ciprofloxacin
1    ISO-014      2025-02-14        A hospital  13   M recovered             S

Isolates with >5% ambiguous bases:
ISO-001 ISO-003
   12.7    11.7
Kept: 71 isolates
Variable sites: 702 of 4000
Pairwise SNP distance: min 0  median 53  max 114

Threshold <= 2 SNPs: 22 clusters; sizes: 26 15 8 4 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1

Threshold <= 5 SNPs: 21 clusters; sizes: 30 15 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1

Threshold <= 10 SNPs: 21 clusters; sizes: 30 15 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1

Threshold <= 20 SNPs: 21 clusters; sizes: 30 15 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```

**Interpret.**

1. **Metadata.** One duplicated row (ISO-011) and one impossible date: ISO-014 is dated 14 February **2025**, a year before the outbreak. The collection date is a typo; the answer key says the true date is 2026-02-14.
2. **Sequence quality.** ISO-001 and ISO-003 have 12.7% and 11.7% ambiguous bases and are excluded: 71 isolates remain.
3. **Variable sites.** 702 of 4,000 positions vary; the median pair differs by 53 SNPs, the maximum 114.
4. **Thresholds.** From 5 SNPs upward the result is stable: clusters of 30, 15 and 8 and 18 singletons. At 2 SNPs the 30-isolate cluster splits into 26 and 4: the threshold changes the answer.

## Part B - Compare with the truth and add epidemiology (60 min)

Save as `outbreak2.R` and run `Rscript outbreak2.R`:

```r
# outbreak2.R - clusters vs truth, resistance, tree and epidemiology (Week 10). Run after outbreak.R.
suppressPackageStartupMessages({library(ape); library(dplyr); library(readr); library(tidyr)})
D <- "../../data/outbreak"
o <- readRDS("outbreak_objects.rds"); aln <- o$aln; snp <- o$snp
meta  <- read_tsv(file.path(D, "outbreak_metadata.tsv"), show_col_types = FALSE) %>% distinct()
truth <- read_tsv(file.path(D, "answers/clusters_truth.tsv"), show_col_types = FALSE)
cl <- read_tsv("clusters_5snp.tsv", show_col_types = FALSE)

# 1. Name the clusters by size and compare with the truth -------------------------------------------
sizes <- cl %>% count(cluster5) %>% mutate(label = ifelse(n >= 5, paste0("K", rank(-n, ties.method = "first")), "sporadic"))
cl <- cl %>% left_join(sizes %>% select(cluster5, label), by = "cluster5") %>% rename(found = label)
cmp <- cl %>% inner_join(truth, by = "isolate_id")
cat("Found clusters vs truth:\n"); print(table(found = cmp$found, truth = cmp$true_cluster))

# 2. Epidemiology of each cluster ---------------------------------------------------------------------
m <- meta %>% inner_join(cl %>% select(isolate_id, found), by = "isolate_id") %>% mutate(date = as.Date(collection_date))
m$date[m$isolate_id == "ISO-014"] <- as.Date("2026-02-14")      # corrected from the answer key's note
cat("\nCluster by district:\n"); print(table(m$found, m$district))
cat("\nCluster by facility:\n"); print(table(m$found, m$facility))
cat("\nDates by cluster:\n")
print(as.data.frame(m %>% group_by(found) %>% summarise(n = n(), first = min(date), last = max(date))))

# 3. The resistance mutation at alignment position 2731 --------------------------------------------------
A <- as.character(aln)[, 2731]
cat("\nBase at alignment position 2731:\n"); print(table(A, useNA = "ifany"))
r <- tibble(isolate_id = rownames(aln), base2731 = A) %>% inner_join(m, by = "isolate_id")
cat("\nMutation vs ciprofloxacin phenotype:\n"); print(table(base2731 = r$base2731, cipro = r$ciprofloxacin))
cat("\nMutation by cluster:\n"); print(table(r$found, r$base2731))
cat("\nMutation carriers that are susceptible:\n"); print(as.data.frame(r %>% filter(base2731 != names(which.max(table(base2731))), ciprofloxacin == "S") %>% select(isolate_id, found, district, ciprofloxacin)))

# 4. Neighbour-joining tree --------------------------------------------------------------------------------
tr <- nj(snp); tr <- root(tr, outgroup = names(which.max(rowMeans(snp))), resolve.root = TRUE)
cols <- c(K1 = "#2b6cb0", K2 = "#dd6b20", K3 = "#2f855a", sporadic = "grey60")
tipcol <- cols[cl$found[match(tr$tip.label, cl$isolate_id)]]
png("tree.png", width = 900, height = 1100, res = 110)
plot(tr, tip.color = tipcol, cex = 0.55, no.margin = FALSE, main = "Neighbour-joining tree (SNP distance)")
legend("bottomleft", legend = names(cols), text.col = cols, bty = "n", cex = 0.9)
add.scale.bar()
dev.off()
cat("\nTree saved: tree.png (", Ntip(tr), "tips )\n")

# 5. Epidemic curve by cluster -----------------------------------------------------------------------------------
png("epicurve_clusters.png", width = 900, height = 500, res = 110)
m$week <- as.Date(cut(m$date, "week"))
tab <- table(m$week, factor(m$found, levels = names(cols)))
barplot(t(tab), col = cols, border = NA, las = 2, cex.names = 0.6, legend.text = names(cols),
        args.legend = list(bty = "n"), main = "Isolates by week of collection and cluster", ylab = "Isolates")
dev.off()
```

```text
Found clusters vs truth:
          truth
found      C1 C2 C3 sporadic
  K1       30  0  0        0
  K2        0 15  0        0
  K3        0  0  8        0
  sporadic  0  0  0       18

Cluster by district:

            A  B  C  D  E
  K1       23  7  0  0  0
  K2        0  0 13  0  2
  K3        0  0  0  8  0
  sporadic  2  3  4  6  3

Cluster by facility:

           clinic community hospital hospital_H
  K1           18        11        1          0
  K2            7         6        2          0
  K3            0         0        0          8
  sporadic      3         9        6          0

Dates by cluster:
     found  n      first       last
1       K1 30 2026-01-28 2026-03-16
2       K2 15 2026-03-06 2026-04-18
3       K3  8 2026-04-17 2026-04-29
4 sporadic 18 2026-01-10 2026-06-09

Base at alignment position 2731:
A
 g  t
17 54

Mutation vs ciprofloxacin phenotype:
        cipro
base2731  R  S
       g 16  1
       t  0 54

Mutation by cluster:

            g  t
  K1        0 30
  K2       15  0
  K3        0  8
  sporadic  2 16

Mutation carriers that are susceptible:
  isolate_id found district ciprofloxacin
1    ISO-018    K2        C             S

Tree saved: tree.png ( 71 tips )
```

(The script also saves `tree.png` and `epicurve_clusters.png`; the `null device 1` lines R prints are harmless.) **The 5-SNP clusters reproduce the truth exactly: 30, 15, 8, and 18 sporadic isolates.**

**Interpret each cluster as a public-health analyst.**

| Cluster | n | Where | When | What it suggests |
|---|---|---|---|---|
| **K1** | 30 | Districts A and B (23 + 7), mostly clinics and community | 28 Jan - 16 Mar | Community transmission across two neighbouring districts; the distances within K1 reach 14 SNPs (single linkage chains), consistent with a growing outbreak |
| **K2** | 15 | Districts C (13) and E (2) | 6 Mar - 18 Apr | A separate lineage (≥ 74 SNPs from K1 and K3) carrying the resistance mutation |
| **K3** | 8 | District D, **all in Hospital H** | 17 - 29 Apr | Eight **identical** genomes (0 SNPs) in one hospital within 12 days: a probable healthcare-associated cluster; its nearest cluster is K1 (25 SNPs), suggesting a shared lineage |
| **Sporadic** | 18 | All districts | Whole period | Isolates unrelated to the clusters (nearest neighbour 34-89 SNPs); possible multiple introductions or unsampled transmission |

**Resistance.** The mutation at position 2731 is `g` in 17 isolates and `t` in 54. It predicts ciprofloxacin resistance in 16 of 17 carriers and all 54 non-carriers are susceptible. The mutation is in all 15 K2 isolates **and in two sporadic isolates** that are genomically unrelated to K2 (convergent evolution): resistance is **not** a marker of the outbreak strain. **ISO-018** (K2, district C) carries the mutation but tests susceptible: report it as discordant and request a repeat susceptibility test and re-sequencing.

## Part C - Look at the tree and epidemic curve (30 min)

Open `tree.png`: the three clusters appear as compact groups of coloured tips (blue K1, orange K2, green K3) among long grey branches (sporadic isolates). K3's tips have zero branch length between them. Open `epicurve_clusters.png`: K1 comes first, K2 overlaps its tail, K3 is a short burst in April; sporadic isolates are spread over the whole period.

**Check the date fix.** The script corrected ISO-014 to 2026-02-14 for the epidemic curve. In real life you would not guess: you would ask the source laboratory, record the correction and keep the original value.

## Part D - Optional: a maximum-likelihood tree (30 min)

If IQ-TREE 2 is installed (`which iqtree2`):

```bash
Rscript -e 'suppressMessages(library(ape)); o <- readRDS("outbreak_objects.rds"); write.dna(o$aln, "clean_alignment.fasta", format = "fasta", nbcol = -1, colsep = "")'
iqtree2 -s clean_alignment.fasta -m GTR+G -nt 2 -pre ml -quiet 2>&1 | tail -2
ls ml.*
```

`ml.treefile` is a maximum-likelihood tree in Newick format. Check that each 5-SNP cluster forms a clade (a monophyletic group) in the ML tree:

```bash
Rscript -e 'suppressMessages(library(ape)); t <- read.tree("ml.treefile"); cl <- read.delim("clusters_5snp.tsv")
tab <- table(cl$cluster5)
for (k in names(tab)[tab >= 5]) cat("cluster", k, "n", sum(cl$cluster5 == k), "monophyletic:", is.monophyletic(t, cl$isolate_id[cl$cluster5 == k]), "\n")'
```

```text
cluster 1 n 30 monophyletic: TRUE 
cluster 2 n 15 monophyletic: TRUE 
cluster 5 n 8 monophyletic: TRUE
```

All three clusters are clades in the ML tree too (the cluster labels 1, 2 and 5 are the internal numbers `hclust` assigned; they correspond to K1, K2 and K3). The run takes a few seconds.

## Part E - The briefing (45 min)

Write `results/week10/briefing.md` (≤400 words) for a ministry director:

1. **Headline** (one sentence) and the **confidence** you have.
2. **What the genomes show:** three clusters with size, place, time.
3. **What this means for action:** an investigation of Hospital H; community follow-up in districts A, B, C and E; susceptibility retest for ISO-018.
4. **Resistance:** the mutation is **not** a marker of one outbreak.
5. **Data limits:** 2 isolates excluded for ambiguity; 1 date corrected; **sequencing coverage unknown** - the number of cases that were not sequenced should be stated.
6. **What you are not claiming:** who infected whom.

## If it breaks

| Message or symptom | Likely cause | Fix |
|---|---|---|
| `there is no package called 'ape'` | Package missing | Re-run the setup for your route |
| `cannot open file` | Wrong directory | Run from `results/week10`; check `ls ../../data/outbreak` |
| `stopifnot(setequal(...))` fails | Isolate names differ | Compare `rownames(aln)` and `meta$isolate_id` |
| Different cluster counts | Different threshold or linkage | Check `h = 5` and `method = "single"` |
| `object 'outbreak_objects.rds' not found` | `outbreak.R` not run | Run it first |
| `iqtree2: command not found` | Not installed | Skip Part D (optional) |
| Tree plot cut off | PNG size | Increase `height` in `png()` |

## Stretch challenge

1. Recluster with `method = "complete"` at 5 SNPs. How do K1's members change?
2. Add the date of onset into the cluster table and estimate an **epidemic growth rate** for K1 (cases per week).
3. Simulate **under-sampling**: randomly remove 50% of isolates from district A and recluster. What happens to cluster sizes and to the apparent geography?

{% endtab %}

{% tab title="5 · Practice" %}

## Exercises

### Basic

**Exercise 1.** Define a SNP distance and explain why positions with `N` in one of the two sequences are excluded from the pair.

**Exercise 2.** Why must a collection date outside the outbreak period be checked rather than deleted?

**Exercise 3.** In the output, how many isolates remained after quality control, and why were two removed?

<details>

<summary>Show answers (1-3)</summary>

1. The count of positions where both isolates have a called base and the bases differ. An `N` means "unknown", not "different", so counting it would manufacture differences.
2. It may be a typo (as here), a genuinely early case (important!) or a laboratory error. Check with the source before changing or deleting, and keep a record.
3. 71 of 73; ISO-001 (12.7% ambiguous) and ISO-003 (11.7%) failed the 5% criterion.

</details>

### Intermediate

**Exercise 4.** Calculate the fraction of resistance-mutation carriers that are phenotypically resistant, and the fraction of resistant isolates that carry the mutation.

**Exercise 5.** From the cluster-by-facility table, what proportion of K1 isolates come from hospitals? What would you conclude about where K1 transmission happens?

**Exercise 6.** Explain why single linkage can place two isolates 14 SNPs apart in the same cluster at a 5-SNP threshold. When is that useful and when misleading?

<details>

<summary>Show answers (4-6)</summary>

4. 16 / 17 = 94% of carriers are resistant (the positive predictive value of the mutation); resistant isolates number 16, all of which carry the mutation: 100% (sensitivity of the mutation for resistance in this dataset).
5. 1 of 30 (3%). Transmission of K1 happens mainly outside hospitals, in clinics and the community.
6. Chain A-B-C: A and B within 5, B and C within 5, so A and C join although they may be up to 10 apart; chains can be longer. Useful to capture growing transmission chains; misleading if a bridging isolate links two unrelated groups.

</details>

### Challenge

**Exercise 7.** Two sporadic isolates carry the resistance mutation. Design the analysis to confirm convergent evolution rather than transmission from K2, including what additional data you would collect.

**Exercise 8.** Write a four-sentence press statement about the K3 hospital cluster that is accurate, does not blame any individual, and protects patient privacy.

<details>

<summary>Show answers (7-8)</summary>

7. Show that they lie on different branches of the tree (nearest neighbour is 34+ SNPs from K2 and each other), that the mutation appears on a distinct genetic background, and that the epidemiological links (place, time, contacts) are absent; check the surrounding sequence to see whether the same nucleotide change occurs in different haplotypes; collect travel and treatment histories (drug exposure promoting resistance).
8. Example: "Hospital H has identified eight patients with a bacterial infection caused by a closely related strain between 17 and 29 April. Laboratory sequencing shows the bacteria are almost identical, and infection control measures have been strengthened on the affected ward. There is no evidence of risk to the wider community at this time, and patients and families have been informed directly. Investigations to find the source are continuing, and we will update the public as soon as we know more." (Avoids ward names, ages, or dates for individuals; makes no claim of fault.)

</details>

## Self-test (8 questions)

1. SNP distance counts: (a) all positions (b) differing positions where both have called bases (c) positions with N (d) indels only
2. Identical genomes in 8 patients in one ward within 2 weeks suggest: (a) a probable common source or chain of transmission needing investigation (b) a lab error (c) different strains (d) nothing
3. Convergent evolution means: (a) the same mutation arising independently (b) transmission between patients (c) a typing error (d) lateral transfer
4. The correct way to handle a mistyped collection date is: (a) delete the isolate (b) check with the source, correct and document (c) ignore it (d) guess
5. A rooted tree: (a) shows an outgroup-based direction (b) is always a transmission tree (c) has no branch lengths (d) is a map
6. If most genomes come from one hospital, the genomic picture: (a) represents the nation (b) over-represents that hospital (c) is unbiased (d) is invalid
7. A resistance mutation in two unrelated isolates indicates: (a) they were infected by the same person (b) possibly independent emergence (c) lab contamination only (d) nothing
8. The threshold for a cluster should be: (a) universal (b) chosen and justified for the pathogen and question (c) whatever gives the biggest cluster (d) zero

<details>

<summary>Show answers and reasons</summary>

1. **(b)**
2. **(a)**
3. **(a)**
4. **(b)**
5. **(a)** Rooting gives direction relative to the outgroup; a tree is not a transmission tree.
6. **(b)**
7. **(b)**
8. **(b)**

</details>

## Reflection prompt (150-250 words)

Describe the metadata your national programme would need to make a genomic cluster interpretable, and the metadata you would deliberately **not** share publicly. Who decides?

## Portfolio mini-deliverable

`results/week10/`: `outbreak.R`, `outbreak2.R`, `clusters_5snp.tsv`, `tree.png`, `epicurve_clusters.png`, and `briefing.md`.

{% endtab %}

{% tab title="6 · Go deeper" %}

## Core resources

- **Nextstrain** ([nextstrain.org](https://nextstrain.org)): open-source real-time pathogen tracking; explore the public builds and the documentation on how trees are produced.
- **Africa CDC** ([africacdc.org](https://africacdc.org)): the Pathogen Genomics Initiative and continental surveillance programmes.
- **WHO** ([who.int](https://www.who.int)): search for the "Global genomic surveillance strategy for pathogens with pandemic and epidemic potential" and for guidance on sequencing and data sharing.
- **GISAID** ([gisaid.org](https://www.gisaid.org)) and **Pathoplexus** ([pathoplexus.org](https://pathoplexus.org)): pathogen sequence sharing platforms with different governance models; read their terms before sharing.
- **European Nucleotide Archive** ([ebi.ac.uk/ena](https://www.ebi.ac.uk/ena)) and **NCBI** ([ncbi.nlm.nih.gov](https://www.ncbi.nlm.nih.gov)): open archives where raw reads and assemblies are deposited.
- **Galaxy Training Network** ([training.galaxyproject.org](https://training.galaxyproject.org)): tutorials on pathogen analysis, phylogenetics and genomic epidemiology.
- **EMBL-EBI Training** ([ebi.ac.uk/training](https://www.ebi.ac.uk/training)): courses on phylogenetics and microbial genomics.
- **GA4GH** ([ga4gh.org](https://www.ga4gh.org)): standards for data sharing and consent.

## Tools and methods to search for

- **IQ-TREE** (maximum-likelihood trees), **FastTree**, and **BEAST** (time-scaled trees): search each name with "documentation".
- **TreeTime**, **Augur**, **Auspice**: the Nextstrain toolkit for time-scaled trees and visualisation.
- **ggtree** (Bioconductor) for publication-quality trees in R.
- **Genomic epidemiology** reviews: search for "genomic epidemiology outbreak investigation review" for accessible overviews and threshold discussions per pathogen.

{% endtab %}

{% tab title="7 · Contribute" %}

You can help improve this week. Open an issue with the label **`week-10`** or edit the file directly - see [How to contribute](../contribute/README.md).

## Ideas for experts

1. **Pathogen-specific thresholds:** a cited table of SNP thresholds for specific pathogens (with references you have opened).
2. **Time-scaled tree:** a tested TreeTime or BEAST example using the same data.
3. **ggtree version:** plotting with ggtree, annotated with district and resistance.
4. **Transmission inference:** an exercise on tools that infer who-infected-whom, and their assumptions.
5. **Real public dataset:** a small open Nextstrain build, with its licence.
6. **Wastewater genomics:** a short example and discussion of sampling bias.
7. **Translations:** the *Concepts* tab (label `translation`).

**Version notes:** tested with R 4.3.3, ape 5.7.1, dplyr 1.1.4 and IQ-TREE 2 on Ubuntu 24.04 (October 2026).

{% endtab %}

{% endtabs %}
