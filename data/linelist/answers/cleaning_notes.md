# Linelist cleaning - what was planted

- `date_onset`: three formats (ISO `2026-02-03`, `03/02/2026` as day/month/year, `3 Feb 2026`) plus ~5% blanks.
- `age`: some like `34 yrs`, some in months (`18 months`), impossible values `999` and `-1`, and blanks.
- `sex`: `M`, `F`, `male`, `Female`, lower-case, blank and `unknown`.
- `district`: upper/lower case, stray spaces, and a misspelling (`Savana North`).
- `outcome`: capitalisation variants, `dead`/`recovered`, blanks.
- `sequenced`: `Y/yes/1/TRUE` vs `N/no/0/FALSE`; ~2% of unsequenced cases still have a `sequence_id` (a data conflict).
- `ct_value`: `ND`, `NA` or blank in ~15% of rows.
- One duplicated row (the row after `C-0300`).
- `linelist_truth.csv` is the clean version for checking your work. Sequencing rate differs strongly by district (bias!).
