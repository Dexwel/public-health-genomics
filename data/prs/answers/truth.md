# PRS toy data - answer key

- Trait is continuous; heritability set to 0.40 in G1.
- Causal variants are **hidden** (not on the array): 114 blocks carry one. SNPs on the array only *tag* them.
- Base GWAS: 10,000 people of G1-like ancestry, autosomes only (no X SNPs in the file).
- Target: 400 people from G1 (same ancestry as the base GWAS) and 400 from G2 (a distant ancestry with different allele frequencies and LD). The score is built from G1-ancestry effect sizes, so expect it to predict worse in G2 - portability is the point.
- `harmonisation_traps.tsv` lists the SNPs whose labels were deliberately altered in the base file.
