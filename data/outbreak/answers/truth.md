# Outbreak toy data - answer key

- Alignment: 73 isolates x 4,000 positions (all sites kept, including invariant ones).
- True groups: C1 (30 isolates, districts A/B), C2 (15, districts C/E, carries the ciprofloxacin-resistance mutation at alignment position 2731), C3 (8, hospital H in district D), and 20 sporadic isolates.
- C1 and C3 share a recent common ancestor (a 'lineage'), so they are close but distinct clusters; C2 is a different lineage.
- Two sporadic isolates carry the resistance mutation by independent mutation (convergence): resistance does not imply relatedness.
- Planted data problems: (1) one C1 isolate has its collection year mistyped as 2025; (2) one metadata row is duplicated; (3) two isolates have >10% N bases; (4) one C2 isolate carries the mutation but is phenotypically susceptible.
- The mistyped isolate is ISO-014 (true date 2026-02-14); the discordant isolate is ISO-018; the duplicated row is ISO-011; high-N isolates are ISO-001, ISO-003.
