# GWAS toy cohort - answer key

- Cohort: 1000 people, 500 cases / 500 controls, 3160 SNPs on chromosomes 1-22 and X (coded 23).
- Main causal SNP: **ts06_067** (chromosome 6, bp 5079921); allele A1 is the risk allele, simulated odds ratio 2.0 per copy.
- Suggestive SNP: **ts12_048** (chromosome 12); simulated OR 1.6 per copy - expect it to be suggestive, not genome-wide significant.
- Population stratification: POP2 has higher baseline risk and is over-represented among cases, so naive tests are inflated.
- Planted problems: see `planted_problems.tsv`. True ancestry labels: `true_ancestry.tsv`.
- Chromosome 23 = X; males are hemizygous (homozygous calls).
