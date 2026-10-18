---
description: Learn R from scratch by cleaning a messy surveillance line list, drawing an epidemic curve, and uncovering sequencing bias.
---

# Week 3 — R for genomic and surveillance data

{% hint style="info" %}
**At a glance** · **Time:** ~6-8 h (2 h concepts, 3-4 h lab, 1-2 h practice) · **Prerequisites:** Week 2 (terminal, scripts) · **You will produce:** a reusable cleaning script, a clean line list, an epidemic curve and a sequencing-coverage chart · **Tools:** R 4.3, readr, dplyr, tidyr, ggplot2
{% endhint %}

{% tabs %}

{% tab title="1 · Start here" %}

## Why this matters

R is the working language of public health data science. Nearly every genomic result you produce in this course - an allele-frequency table, a Manhattan plot, a phylogenetic tree - will be tabulated, tested and drawn in R. But before any of that, every real data project begins with the same unglamorous task: **cleaning**. Surveillance data arrive with dates written three ways, ages typed as "34 yrs", impossible codes like 999, and districts spelled inconsistently. A model fitted to uncleaned data produces confident nonsense.

This week you will clean a realistic (synthetic) line list of 600 cases, and then ask a genomic-surveillance question of it: *Who actually gets sequenced?* The answer - a striking inequality between districts - is the first lesson in **surveillance bias**.

You will also meet two bugs that the author of this lab introduced by accident, and that a careful check caught. Learning to *check your own work* is more important than learning any function.

## Learning objectives

By the end of this week you will be able to:

1. **Navigate** R and RStudio (or the R terminal): the console, scripts, working directory, projects.
2. **Create and manipulate** vectors, data frames and missing values (`NA`).
3. **Import** a CSV with `readr` and **inspect** each column before changing it.
4. **Transform** data with the dplyr verbs `filter`, `mutate`, `group_by`, `summarise`, `count`, `arrange`, `select`, and joins.
5. **Clean** inconsistent dates, numbers and categories safely, and **verify** the result.
6. **Draw** an epidemic curve and a bar chart with ggplot2.
7. **Write** a script that anyone can re-run, and record your R and package versions.

## Roadmap

| Step | Time | Tab |
|---|---|---|
| Pre-check | 10 min | 1 · Start here |
| Concepts (type the examples!) | 90-120 min | 2 · Concepts |
| Conversation | 20 min | 3 · Conversation |
| Lab | 3-4 h | 4 · Hands-on lab |
| Practice | 60-90 min | 5 · Practice |

## Key terms

| Term | Plain meaning |
|---|---|
| **Console / script** | Where you type one command at a time / a saved file of commands |
| **Object** | A named thing you store, e.g. `ages <- c(34, 7)` |
| **Vector** | An ordered set of values of one type |
| **Data frame / tibble** | A table: rows are records, columns are variables |
| **Package** | An add-on that gives R new functions (`library(dplyr)`) |
| **Pipe (`%>%` or `\|>`)** | Passes the result of one step into the next |
| **`NA`** | R's "missing value" |
| **Tidy data** | One variable per column, one observation per row |
| **Line list** | A surveillance table with one row per case |

## Pre-check

1. In R, what does `x <- c(2, 4, 6)` do?
2. What is `mean(c(34, 7, NA))`?
3. What does a pipe do?
4. If a column contains `"30.4"`, `"ND"` and `""`, what type is it in R, and why?
5. Why is `03/02/2026` dangerous in surveillance data?

<details>

<summary>Show answers</summary>

1. Creates a vector of three numbers and stores it in an object called `x`.
2. `NA` - one missing value makes the mean missing unless you say `na.rm = TRUE`.
3. It feeds the output of the left-hand step as the first input to the right-hand step, so you can read code as a sequence.
4. **Character (text)** - the non-numeric `"ND"` forces the whole column to be text; you must convert deliberately.
5. It can mean 3 February (day first) or 2 March (month first). Always know the format and write dates as `YYYY-MM-DD`.

</details>

{% endtab %}

{% tab title="2 · Concepts" %}

## 2.1 R, RStudio and the working directory

**R** is the language and engine. **RStudio** (now Posit Desktop/Workbench) is a comfortable window around it, with a console, a script editor, a file browser and a plot pane. You can also run R in a terminal (`R`) or run a script with `Rscript script.R`, which is what we do in the lab so that results are reproducible.

The **working directory** is the folder R treats as "here". In this course it is always the **repository root**. Check with `getwd()`; change with `setwd("path")` (or, better, open a *project* in that folder so you never need to).

{% hint style="info" %}
**Public health lens.** "Point-and-click" analysis cannot be audited. A script is a complete, rerunnable record of how every number in a report was produced. In an outbreak, that is the difference between "trust me" and "check me".
{% endhint %}

## 2.2 Objects, vectors and missing values

```r
ages <- c(34, 7, 61, NA, 19)   # c() combines values into a vector; NA = missing
mean(ages)                      # NA   (one missing value makes the answer unknown)
mean(ages, na.rm = TRUE)        # 30.25
ages[ages > 18 & !is.na(ages)]  # 34 61 19   (keep the elements where the test is TRUE)
```

Real output:

```text
[1] NA
[1] 30.25
[1] 34 61 19
```

Key ideas:

| Idea | Example | Note |
|---|---|---|
| Assignment | `x <- 5` | `<-` stores a value; `=` also works but `<-` is conventional |
| Types | numeric `3.5`, integer `3L`, character `"A"`, logical `TRUE`, `Date` | Every vector has **one** type |
| Comparison | `==`, `!=`, `<`, `>=` | `=` is assignment; `==` tests equality |
| Logic | `&` (and), `\|` (or), `!` (not) | |
| Missing | `NA`, `is.na(x)` | Never test `x == NA`; use `is.na(x)` |
| Indexing | `x[2]`, `x[x > 5]` | 1-based |
| Sets | `x %in% c("a","b")` | TRUE where `x` is one of the values |

## 2.3 Data frames and tibbles

A **data frame** is a table of equal-length columns.

```r
df <- data.frame(id = c("C1", "C2", "C3"),
                 age = c(34, 7, 61),
                 district = c("A", "B", "A"))
str(df)               # structure: types of each column
df[df$age > 10, ]     # rows where age > 10
```

```text
'data.frame':	3 obs. of  3 variables:
 $ id      : chr  "C1" "C2" "C3"
 $ age     : num  34 7 61
 $ district: chr  "A" "B" "A"
  id age district
1 C1  34        A
3 C3  61        A
```

**Tibbles** (from the tidyverse) are modern data frames that print neatly. We use `readr` to read files into tibbles.

## 2.4 Packages

```r
library(dplyr)          # load a package for this session
# install.packages("dplyr")   # install once (already done by the setup)
```

Packages used here: **readr** (read files), **dplyr** (transform), **tidyr** (reshape), **ggplot2** (plot). Together they are the core of the "tidyverse". We load each explicitly, so scripts show exactly what they depend on.

## 2.5 Importing data: read everything as text first

```r
raw <- read_csv("data/linelist/linelist_messy.csv",
                col_types = cols(.default = col_character()))
```

Why read as text? R's automatic guess turns a column that *looks* numeric into numbers and silently converts anything odd to `NA`. Reading as text keeps every original value so *you* decide how to convert it, and you can look at what was there. This one habit prevents many silent data losses.

## 2.6 The dplyr verbs

| Verb | Job | Example |
|---|---|---|
| `filter()` | keep rows | `filter(age > 10)` |
| `select()` | keep/rename columns | `select(case_id, age)` |
| `mutate()` | create or change columns | `mutate(age_group = ...)` |
| `arrange()` | sort rows | `arrange(desc(age))` |
| `group_by()` + `summarise()` | per-group summaries | `group_by(district) %>% summarise(n = n())` |
| `count()` | shortcut: group and count | `count(district, sex)` |
| `distinct()` | remove duplicate rows | `distinct(df)` |
| `left_join()` / `inner_join()` | combine tables by a key | `inner_join(a, b, by = "case_id")` |

The **pipe** passes the left result to the next step:

```r
df %>%
  filter(age > 10) %>%
  group_by(district) %>%
  summarise(n = n(), mean_age = mean(age))
```

```text
# A tibble: 1 x 3
  district     n mean_age
  <chr>    <int>    <dbl>
1 A            2     47.5
```

(`%>%` comes with dplyr; R 4.1+ also has a built-in pipe `|>` that works the same way for our purposes.)

### `case_when()`: recoding categories

```r
case_when(x %in% c("f", "female") ~ "F",
          x %in% c("m", "male")   ~ "M",
          TRUE                    ~ NA_character_)
```

Reads like a list of rules; the first match wins; `TRUE ~` catches everything else.

### Pitfall: a column you just made hides the old one

Inside one `summarise()`, a name you create is immediately visible to later arguments, and it *hides* the original. Look:

```r
d <- data.frame(g = c("a","a","b"), s = c(TRUE, FALSE, TRUE))
d %>% group_by(g) %>% summarise(n = n(), s = sum(s), pct = 100 * mean(s))
```

```text
  g         n     s   pct
1 a         2     1   100      # WRONG: mean(s) used the new sum (1), not the logical column
2 b         1     1   100
```

The fix is to give the new column a different name:

```r
d %>% group_by(g) %>% summarise(n = n(), n_s = sum(s), pct = 100 * n_s / n)
```

```text
  g         n   n_s   pct
1 a         2     1    50
2 b         1     1   100
```

This exact bug appeared when the author first wrote this week's lab (every district showed absurd percentages like 12,100%). The lesson: **always sanity-check results against common sense**.

## 2.7 Tidy data and reshaping

**Tidy** data have one variable per column and one observation per row. Wide tables (one column per week) are convenient for humans; long tables are what ggplot2 and statistics need.

```r
wide <- data.frame(district = c("A","B"), wk1 = c(3, 5), wk2 = c(4, 2))
pivot_longer(wide, cols = c(wk1, wk2), names_to = "week", values_to = "cases")
```

```text
  district week  cases
  A        wk1       3
  A        wk2       4
  B        wk1       5
  B        wk2       2
```

`pivot_wider()` does the reverse (for example, cases by district and sex as two columns).

## 2.8 Dates and the ambiguity problem

R's `Date` type stores a date as a number of days. Convert text with an explicit **format**:

| Code | Meaning |
|---|---|
| `%Y` | 4-digit year |
| `%m` | month number |
| `%d` | day of month |
| `%b` | abbreviated month name (`Feb`) |
| `%A` | weekday name |

```r
as.Date("03/02/2026", format = "%d/%m/%Y")   # 2026-02-03  (3 February)
as.Date("03/02/2026", format = "%m/%d/%Y")   # 2026-03-02  (2 March!)
as.Date("3 Feb 2026", format = "%d %b %Y")   # 2026-02-03
format(as.Date("2026-02-03"), "%A %d %B %Y") # "Tuesday 03 February 2026"
```

**The same text gives two different dates** depending on the format you assume. You must *know* (ask the data owner) which convention each source used. Month names like `Feb` depend on the computer's language; `Sys.setlocale("LC_TIME", "C")` forces English names so scripts behave the same everywhere.

## 2.9 Factors

A **factor** is a categorical variable with a fixed set of **levels** (and an order). Useful for plots and models:

```r
x <- factor(c("low","high","mid","low"), levels = c("low","mid","high"))
table(x)
```

```text
x
 low  mid high 
   2    1    1 
```

## 2.10 Plotting with ggplot2: a grammar

A plot is built from **data**, **aesthetics** (what maps to x, y, colour) and **geometries** (how to draw):

```r
ggplot(weekly, aes(week_start, n)) +     # data and mapping
  geom_col(fill = "#2b6cb0") +           # bars
  labs(title = "Cases by week", x = "Week starting (Monday)", y = "Cases") +
  theme_minimal()
```

Common geoms: `geom_col` (bars of values), `geom_histogram`, `geom_point`, `geom_line`, `geom_boxplot`. `facet_wrap(~ district)` makes one panel per group. Colours must not be the only carrier of meaning (colour-blind readers): add shapes, labels or direct annotations.

## 2.11 Cleaning principles

1. **Never edit the raw file.** Read it; write a *new* cleaned file.
2. **Look before you change.** Print `table()` of each categorical column; list the odd values.
3. **One rule per problem**, written as a small function you can test.
4. **Do not invent.** Unknown stays `NA` - "unknown" and blank both become missing.
5. **Check after cleaning:** counts, ranges, cross-tabulate raw vs clean values for the unusual codes.
6. **Document assumptions** in comments (for example "dd/mm/yyyy, confirmed with the data owner").

## 2.12 Reproducibility toolkit

| Practice | Why |
|---|---|
| Scripts, not console clicks | Rerunnable |
| `set.seed(123)` before random steps | Same random numbers |
| `sessionInfo()` or `R.version.string`, `packageVersion("dplyr")` | Record versions |
| Relative paths from the project root | Works on anyone's computer |
| **Quarto / R Markdown** | Mix text, code and results in one report that regenerates itself |
| Git | History of your scripts |

{% endtab %}

{% tab title="3 · Conversation" %}

*Zainab has a spreadsheet printed on four sheets of paper, annotated in three colours of pen. Tunde looks at it as one looks at a patient with a worrying X-ray.*

**Zainab:** This is my district's line list for the outbreak. Six hundred cases. I cleaned it myself: I sorted it, I fixed the typos, I deleted the duplicates by hand.

**Tunde:** And if I ask you tomorrow, *exactly* what you changed?

**Zainab:** (pause) I… fixed it. Mostly. I'd have to look.

**Dr. Mensah:** That is the difference between cleaning and *scripting* the cleaning. Zainab, imagine the Ministry sends you the next week's file with another three hundred rows. What do you do?

**Zainab:** Start again. Sort, fix, delete.

**Tunde:** With R you write the rules once. Rerun, done, and the rules *are* the documentation.

**Zainab:** Fine. Show me. I've heard R is for statisticians.

**Tunde:** R is a calculator that remembers. Type `ages <- c(34, 7, 61, NA, 19)`. Now `mean(ages)`.

**Zainab:** It says `NA`. Is it broken?

**Tunde:** No - it is *honest*. One value is missing, so the mean is unknown. Tell it to ignore the missing one: `mean(ages, na.rm = TRUE)`.

**Zainab:** Thirty point two five. I'd prefer it said that automatically.

**Dr. Mensah:** Many people would. But a program that quietly ignores missing values is a program that quietly lies. In surveillance, "we do not know" is information.

**Zainab:** I'll accept that. Now, the dates. In my file, some are `2026-02-03`, some are `03/02/2026` and some are `3 Feb 2026`. How does R know which is which?

**Tunde:** It doesn't. *You* tell it, one pattern at a time. And be careful with the middle one. Is `03/02/2026` the third of February, or the second of March?

**Zainab:** In my country it's the third of February.

**Tunde:** In another country it's the second of March. If you guess wrong, an outbreak that peaked in February looks like it peaked in March.

**Zainab:** That would change the response!

**Dr. Mensah:** And the dangerous part: for dates like `13/02/2026` the wrong guess fails loudly - there is no thirteenth month. But for the third of February, both readings are valid and *nothing warns you*. Silent errors are the expensive ones.

**Zainab:** So I ask the data owner which convention they used.

**Dr. Mensah:** Always. And write it in the script as a comment, so the next person doesn't have to ask again.

**Tunde:** Let me show you the next one, because it bit me last night when I tested the lab. The ages: some are `34`, some are `19 yrs`, and some are `-1` and `999` - those are codes for "unknown". I wrote one line to strip everything that isn't a digit.

**Zainab:** And?

**Tunde:** It turned `-1` into `1`. Because the minus sign isn't a digit.

**Zainab:** (aghast) So eleven people suddenly became one-year-old babies. In a *cleaned* file.

**Tunde:** And nothing complained. I only found it because the course has an answer key and I compared my result to it. In real life there is no answer key.

**Dr. Mensah:** So what do we do when there is no answer key?

**Zainab:** Look at the strange values before and after. Make a table of raw age `-1` and see what it became.

**Dr. Mensah:** Exactly. Cross-tabulate the unusual raw values against the cleaned ones. Check ranges: is anyone younger than zero or older than a hundred and ten? Count the missing values and ask if the number is plausible. Cleaning is not finished until you have *tried to break your own result*.

**Zainab:** All right, but I want the result I came for. Which district has the most sequenced cases?

**Tunde:** Careful with that question. Run it.

**Zainab:** (typing) Coastal Hub: one hundred and twenty-one of one hundred and forty-eight cases have a genome sequence. Highland: five of forty-nine. So… Coastal Hub is where the outbreak is spreading fastest?

**Dr. Mensah:** Why do you think that?

**Zainab:** Because it has the most sequences.

**Dr. Mensah:** What does that column actually measure?

**Zainab:** (slowly) How many cases were sequenced. Not how many cases there *were*. (pause) Oh. Coastal Hub is where the sequencer is.

**Tunde:** The reference lab is there. Samples from Highland have to travel for two days on a bad road.

**Zainab:** So if I draw a map from the *sequenced* cases only, Highland looks quiet. It's not quiet. It's invisible.

**Dr. Mensah:** And that is why a denominator matters: sequenced cases out of *all* cases. Eighty-two percent in one district, ten percent in another, and an analyst who forgets that will draw conclusions about the geography of the lab, not of the disease.

**Zainab:** I want a chart that shows this. A bar chart of the percentage sequenced, by district.

**Tunde:** Ten lines of ggplot. But notice something first. You made that chart *because you asked a suspicious question of your own data*. That habit is worth more than any function.

**Zainab:** (writing on her printout) "Ask: who is missing?"

**Dr. Mensah:** Write it in red. We will meet it again in Week 10.

### Talking points for the forum

1. Describe a time a date format caused confusion in your work. What agreement about data formats would prevent it?
2. After cleaning a dataset, what *three* checks would you do to try to break your own result?
3. Where is your country's genomic sequencing capacity, and which populations might be systematically under-represented in sequence data as a result?

{% endtab %}

{% tab title="4 · Hands-on lab" %}

{% hint style="success" %}
**Lab goal.** Build a script that cleans `data/linelist/linelist_messy.csv`, check it against the answer key, and draw two charts. Everything below was run on the course data with R 4.3.3, dplyr 1.1.4, ggplot2 3.4.4 and readr 2.1.5. Work **from the repository root**. If you use RStudio, open a *project* in that folder or run `setwd()` to it first; a script run with `Rscript` from the terminal needs no setup.
{% endhint %}

```bash
mkdir -p results/week03
```

## Part A - Inspect before you clean (45 min)

Start an R session (type `R` in the terminal, or use the RStudio console). Type these lines one at a time.

### Step 1. Read as text and look

```r
library(readr); library(dplyr)
raw <- read_csv("data/linelist/linelist_messy.csv",
                col_types = cols(.default = col_character()))
nrow(raw)
head(raw, 3)
```

```text
[1] 601
```

601 rows (header excluded). Now tabulate every categorical column:

```r
table(raw$sex, useNA = "ifany")
table(raw$outcome, useNA = "ifany")
table(raw$sequenced, useNA = "ifany")
```

```text
      F  Female       M       f       m    male unknown    <NA> 
    203      39     195      28      31      41      24      40 

    ALIVE     Alive      DIED      Died     alive      dead      died recovered 
       47        94         2         3       347         2        10        65 
     <NA> 
       31 

    0     1 FALSE     N  TRUE     Y    no   yes 
   76    68    67    83    75    70    90    72 
```

**Stop and check:** write down (in your notebook) the groups you would merge: `F/f/Female`, `M/m/male`, `unknown`/blank → missing; `alive/Alive/ALIVE/recovered`; `died/DIED/Died/dead`; and the eight spellings of yes/no.

### Step 2. The districts

```r
table(raw$district, useNA = "ifany")
```

You should see **20 distinct spellings** of six real districts: upper case, lower case, extra spaces, and `Savana` with one "n". (The first lines of the output are `COASTAL HUB 13, Coastal Hub 124, DELTA EAST 11, ...`.)

### Step 3. The dates

```r
patterns <- ifelse(grepl("^\\d{4}-\\d{2}-\\d{2}$", raw$date_onset), "iso",
            ifelse(grepl("^\\d{2}/\\d{2}/\\d{4}$", raw$date_onset), "dmy",
            ifelse(grepl("^\\d{1,2} [A-Za-z]{3} \\d{4}$", raw$date_onset), "long",
            ifelse(is.na(raw$date_onset), "blank", "other"))))
table(patterns)
```

```text
patterns
blank   dmy   iso  long 
   27   118   408    48 
```

Three formats and 27 blanks; no unrecognised pattern. (`\\d` means "a digit"; `^` and `$` anchor the start and end.)

### Step 4. Ages and ct values

```r
unique(raw$age[is.na(suppressWarnings(as.numeric(raw$age)))])[1:6]
table(raw$age[raw$age %in% c("-1", "999")])
table(raw$ct_value[is.na(suppressWarnings(as.numeric(raw$ct_value)))], useNA = "ifany")
sum(duplicated(raw))
```

```text
[1] NA       "19 yrs" "20 yrs" "52 yrs" "34 yrs" "23 yrs"

 -1 999 
 11  18 

  ND <NA> 
  37   73 

[1] 1
```

Ages come as plain numbers, as `"34 yrs"`, as codes `-1` (11 cases) and `999` (18 cases), and blanks (19). `ct_value` (a measure of how much virus was in the sample) has `ND` ("not detected") and blanks. There is **one duplicate row**.

## Part B - The cleaning script (60 min)

Save the following as `results/week03/clean_linelist.R` (copy the whole block). Read each section, comparing it with what you found in Part A.

```r
# clean_linelist.R - clean the messy surveillance line list (Week 3).
# Run from the repository root:  Rscript results/week03/clean_linelist.R
suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(tidyr)
  library(ggplot2)
})
invisible(Sys.setlocale("LC_TIME", "C"))   # make "Feb" mean February whatever the computer language
dir.create("results/week03", showWarnings = FALSE, recursive = TRUE)

# 1. Read everything as text first, so R does not guess (and silently break) anything ----
raw <- read_csv("data/linelist/linelist_messy.csv", col_types = cols(.default = col_character()))
cat("Rows read:", nrow(raw), "\n")

# 2. Remove exact duplicate rows ----------------------------------------------------------
dup_rows <- sum(duplicated(raw))
dat <- distinct(raw)
cat("Exact duplicate rows removed:", dup_rows, "-> rows now:", nrow(dat), "\n")
stopifnot(!anyDuplicated(dat$case_id))

# 3. Helper functions, one per messy column ---------------------------------------------
parse_date <- function(x) {
  x <- trimws(x)
  out <- as.Date(rep(NA_character_, length(x)))
  iso  <- !is.na(x) & grepl("^\\d{4}-\\d{2}-\\d{2}$", x)
  dmy  <- !is.na(x) & grepl("^\\d{2}/\\d{2}/\\d{4}$", x)
  long <- !is.na(x) & grepl("^\\d{1,2} [A-Za-z]{3} \\d{4}$", x)
  out[iso]  <- as.Date(x[iso], format = "%Y-%m-%d")
  out[dmy]  <- as.Date(x[dmy], format = "%d/%m/%Y")      # day first!
  out[long] <- as.Date(x[long], format = "%d %b %Y")
  out
}

parse_age <- function(x) {
  x <- tolower(trimws(x))
  # keep an optional minus sign: stripping every non-digit would turn the code "-1" into 1!
  num <- suppressWarnings(as.numeric(sub("^(-?[0-9.]+).*$", "\\1", x)))
  months <- grepl("month", x)
  num[months] <- num[months] / 12                            # months -> years
  num[!is.na(num) & (num < 0 | num > 110)] <- NA              # -1 and 999 are codes, not ages
  num
}

clean_sex <- function(x) {
  x <- tolower(trimws(x))
  case_when(x %in% c("f", "female") ~ "F",
            x %in% c("m", "male")   ~ "M",
            TRUE                    ~ NA_character_)         # "unknown" and blank -> missing
}

districts <- c("Savanna North", "Savanna South", "Lakeside", "Coastal Hub", "Highland", "Delta East")
clean_district <- function(x) {
  x <- tolower(trimws(x))
  x <- gsub("savana ", "savanna ", x, fixed = TRUE)           # the known misspelling
  districts[match(x, tolower(districts))]                      # NA if still unrecognised
}

clean_outcome <- function(x) {
  x <- tolower(trimws(x))
  case_when(x %in% c("alive", "recovered") ~ "alive",
            x %in% c("died", "dead")       ~ "died",
            TRUE                           ~ NA_character_)
}

clean_yesno <- function(x) {
  x <- tolower(trimws(x))
  case_when(x %in% c("y", "yes", "1", "true")  ~ TRUE,
            x %in% c("n", "no", "0", "false")  ~ FALSE,
            TRUE                               ~ NA)
}

# 4. Apply them ---------------------------------------------------------------------------
clean <- dat %>%
  mutate(date_onset    = parse_date(date_onset),
         age           = parse_age(age),
         sex           = clean_sex(sex),
         district      = clean_district(district),
         facility_type = tolower(trimws(facility_type)),
         outcome       = clean_outcome(outcome),
         sequenced     = clean_yesno(sequenced),
         sequence_id   = na_if(trimws(sequence_id), ""),
         ct_value      = suppressWarnings(as.numeric(ct_value)))   # "ND"/"NA"/blank -> NA

# 5. Logical checks ------------------------------------------------------------------------
cat("\nMissing values after cleaning:\n")
print(colSums(is.na(clean)))
conflict <- clean %>% filter(sequenced == FALSE, !is.na(sequence_id))
cat("\nUnsequenced cases that still have a sequence_id (data conflict):", nrow(conflict), "\n")
cat("Cases with onset date range:", format(min(clean$date_onset, na.rm = TRUE)), "to",
    format(max(clean$date_onset, na.rm = TRUE)), "\n")

write_csv(clean, "results/week03/linelist_clean.csv")

# 6. Compare with the answer key (only now!) ------------------------------------------------
truth <- read_csv("data/linelist/answers/linelist_truth.csv", show_col_types = FALSE) %>%
  mutate(sequenced = as.logical(sequenced))
cmp <- inner_join(clean, truth, by = "case_id", suffix = c("", "_true"))
same <- function(a, b) ifelse(is.na(a) | is.na(b), NA, a == b)    # NA means "we could not tell"
report <- tibble(
  column     = c("date_onset", "age", "sex", "district", "facility_type", "outcome", "sequenced"),
  checked    = c(sum(!is.na(cmp$date_onset)), sum(!is.na(cmp$age)), sum(!is.na(cmp$sex)),
                 sum(!is.na(cmp$district)), sum(!is.na(cmp$facility_type)), sum(!is.na(cmp$outcome)),
                 sum(!is.na(cmp$sequenced))),
  correct    = c(sum(same(cmp$date_onset, cmp$date_onset_true), na.rm = TRUE),
                 sum(same(cmp$age, cmp$age_true), na.rm = TRUE),
                 sum(same(cmp$sex, cmp$sex_true), na.rm = TRUE),
                 sum(same(cmp$district, cmp$district_true), na.rm = TRUE),
                 sum(same(cmp$facility_type, cmp$facility_type_true), na.rm = TRUE),
                 sum(same(cmp$outcome, cmp$outcome_true), na.rm = TRUE),
                 sum(same(cmp$sequenced, cmp$sequenced_true), na.rm = TRUE)))
cat("\nAgreement with the answer key (non-missing values only):\n")
print(as.data.frame(report), row.names = FALSE)

# 7. Plot 1: epidemic curve by week ----------------------------------------------------------
weekly <- clean %>%
  filter(!is.na(date_onset)) %>%
  mutate(week_start = as.Date(cut(date_onset, "week"))) %>%      # weeks start on Monday
  count(week_start)
p1 <- ggplot(weekly, aes(week_start, n)) +
  geom_col(fill = "#2b6cb0") +
  labs(title = "Cases by week of symptom onset", x = "Week starting (Monday)", y = "Cases") +
  theme_minimal(base_size = 12)
ggsave("results/week03/epicurve.png", p1, width = 7, height = 4, dpi = 120)

# 8. Plot 2: who gets sequenced? ---------------------------------------------------------------
seq_by_district <- clean %>%
  filter(!is.na(district), !is.na(sequenced)) %>%
  group_by(district) %>%
  summarise(cases = n(), n_seq = sum(sequenced), pct = 100 * n_seq / cases, .groups = "drop") %>%
  arrange(desc(pct))
cat("\nSequencing coverage by district:\n")
print(as.data.frame(seq_by_district), row.names = FALSE, digits = 3)
p2 <- ggplot(seq_by_district, aes(reorder(district, pct), pct)) +
  geom_col(fill = "#2f855a") + coord_flip() +
  labs(title = "Share of cases with a genome sequence, by district",
       x = NULL, y = "% of cases sequenced") +
  theme_minimal(base_size = 12)
ggsave("results/week03/sequencing_by_district.png", p2, width = 7, height = 4, dpi = 120)

cat("\nSaved: linelist_clean.csv, epicurve.png, sequencing_by_district.png in results/week03/\n")
cat("\nR session:\n"); print(R.version.string)
```

## Part C - Run it and check (30 min)

### Step 5. Run the script

```bash
Rscript results/week03/clean_linelist.R
```

You should see (the agreement table is printed by the script **after** it compares your cleaning with the answer key - a deliberate "check your answer" step):

```text
Rows read: 601 
Exact duplicate rows removed: 1 -> rows now: 600 

Missing values after cleaning:
      case_id    date_onset           age           sex      district 
            0            27            48            64             0 
facility_type       outcome     sequenced   sequence_id      ct_value 
            0            31             0           330           110 

Unsequenced cases that still have a sequence_id (data conflict): 6 
Cases with onset date range: 2026-01-12 to 2026-06-29 

Agreement with the answer key (non-missing values only):
        column checked correct
    date_onset     573     573
           age     552     552
           sex     536     536
      district     600     600
 facility_type     600     600
       outcome     569     569
     sequenced     600     600
```

**Stop and check:** every `correct` equals `checked`. If your numbers differ, find which function disagrees: the first argument of `table()` on the raw vs cleaned values for that column will show it.

### Step 6. Understand the missing values

The 48 missing ages = 19 blanks + 11 codes of `-1` + 18 codes of `999`. The 64 missing sexes = 40 blanks + 24 `"unknown"`. This is a useful habit: *every* `NA` should be explainable.

### Step 7. A bug you can reproduce

In R, compare two ways to extract the number from age text:

```r
raw_ages <- c("34", "19 yrs", "-1", "999")
as.numeric(gsub("[^0-9.]", "", raw_ages))              # the tempting one-liner
as.numeric(sub("^(-?[0-9.]+).*$", "\\1", raw_ages))    # the version in the script
```

```text
[1]  34  19   1 999
[1]  34  19  -1 999
```

The first turns `-1` into `1` (eleven cases would have become infants!) and nothing warns you. **Without the answer key you would only catch this by cross-tabulating the unusual raw codes against the cleaned values.** Do that now for `-1`: `table(raw$age[raw$age == "-1"])` and check that those cases are `NA` in `results/week03/linelist_clean.csv`.

## Part D - Read the results (45 min)

### Step 8. The epidemic curve

Open `results/week03/epicurve.png` (in the file browser, or RStudio's Files pane). You should see a rapid rise, a peak, and a long tail. Find the peak week:

```r
library(dplyr); library(readr)
clean <- read_csv("results/week03/linelist_clean.csv", show_col_types = FALSE)
clean %>% filter(!is.na(date_onset)) %>%
  mutate(week_start = as.Date(cut(date_onset, "week"))) %>%
  count(week_start) %>% arrange(desc(n)) %>% head(3)
```

```text
  week_start     n
  2026-02-16    73
  2026-02-09    67
  2026-02-02    60
```

The peak is the week starting **16 February 2026** with 73 cases (cases with a missing onset date, 27 of them, are not plotted - always say so in a caption).

### Step 9. Who gets sequenced? (surveillance bias)

The script printed:

```text
      district cases n_seq  pct
   Coastal Hub   148   121 81.8
 Savanna North   142    79 55.6
 Savanna South    84    39 46.4
      Lakeside    82    24 29.3
    Delta East    95    16 16.8
      Highland    49     5 10.2
```

Open `results/week03/sequencing_by_district.png`. **Interpret:** Coastal Hub sequences 82% of cases, Highland only 10%. If you drew a map from *sequence counts*, Highland would look nearly free of disease; but Highland has 49 cases. Genomic maps show where the **sequencer** reaches, not only where the **disease** is.

### Step 10. Another look: case fatality and facility

```r
clean %>% filter(!is.na(outcome)) %>% group_by(facility_type) %>%
  summarise(n = n(), died = sum(outcome == "died"), cfr_pct = round(100 * died / n, 1))
```

```text
  facility_type     n  died cfr_pct
  clinic          264     8     3  
  community       116     4     3.4
  hospital        189     5     2.6
```

Case fatality is similar by facility (about 3%). Is it fair to compare these? (Think: who is sent to a hospital, and who is missing an outcome?)

## Part E - Save, version, record (20 min)

```bash
cd results/week03 && git init -b main 2>/dev/null; git add clean_linelist.R && git -c user.name=You -c user.email=you@example.org commit -m "Week 3: line-list cleaning script" ; cd ../..
```

(Optional. The `-c` options supply a temporary identity so this works even if Git is not yet configured. If you prefer, put your script in your own project repository.)

In R, record your versions for the portfolio:

```r
R.version.string; packageVersion("dplyr"); packageVersion("ggplot2")
```

```text
[1] "R version 4.3.3 (2024-02-29)"
[1] '1.1.4'
[1] '3.4.4'
```

## If it breaks

| Message or symptom | Likely cause | Fix |
|---|---|---|
| `cannot open file 'data/linelist/...'` | Not at repository root | `getwd()`; `setwd()` to the root |
| `there is no package called 'dplyr'` | Package not installed | Re-run the setup for your route |
| `Error in library(tidyr) ... object not found` | Misspelt name | R is case-sensitive: `library(tidyr)` |
| Dates all `NA` | Different locale or format | Check `Sys.setlocale("LC_TIME","C")` ran; print a few raw dates |
| `could not find function "%>%"` | `dplyr` not loaded | `library(dplyr)` |
| Warning `NAs introduced by coercion` | Text became numbers | Expected for `ND`; wrapped in `suppressWarnings` deliberately |
| Plot not shown | Running with `Rscript` | Plots are saved to PNG files by `ggsave` |
| Numbers differ from this page | Edited data, or a different step | Run `bash scripts/check_setup.sh`; re-read the rule you changed |

## Stretch challenge

1. Add a function `check_ranges(clean)` that stops the script if any age is outside 0-110, any onset date is in the future, or any `ct_value` is outside 10-45.
2. Make a **faceted** epidemic curve (`facet_wrap(~ district)`). Which districts peaked earliest?
3. Compute, per district, the number of cases **with a missing onset date** and discuss whether missingness is evenly spread.

{% endtab %}

{% tab title="5 · Practice" %}

## Exercises

### Basic

**Exercise 1.** Write R code that creates a vector `cts` of the values `22.1, 30.4, NA, 27.7`, and prints the mean ignoring the missing value.

**Exercise 2.** What does `clean %>% count(sex)` produce? Why does one row have `NA`?

**Exercise 3.** What is wrong with `if (x == NA)`? Write the correct test.

<details>

<summary>Show answers (1-3)</summary>

1.
   ```r
   cts <- c(22.1, 30.4, NA, 27.7)
   mean(cts, na.rm = TRUE)    # 26.73333
   ```
2. A table of counts by `sex`: `F`, `M` and `NA`. The `NA` row (64 cases) holds those whose sex was blank or `"unknown"` and was deliberately recoded to missing.
3. Any comparison with `NA` returns `NA`, so the `if` fails. Use `is.na(x)`.

</details>

### Intermediate

**Exercise 4.** Using the cleaned data, compute the median age of cases by sex (ignoring missing).

**Exercise 5.** Make a table of cases by district and whether they were sequenced (`TRUE`/`FALSE`), in wide form with `pivot_wider`.

**Exercise 6.** The district-by-sex counts for the cleaned file are given in the answer below. Without running code, which district has the highest *proportion* of female cases among cases with known sex? (Compute by hand.)

<details>

<summary>Show answers (4-6)</summary>

4.
   ```r
   clean %>% filter(!is.na(sex)) %>% group_by(sex) %>%
     summarise(median_age = median(age, na.rm = TRUE))
   ```
5.
   ```r
   clean %>% count(district, sequenced) %>%
     pivot_wider(names_from = sequenced, values_from = n, names_prefix = "seq_")
   ```
6. Counts (F, M): Coastal Hub 60/68, Delta East 51/38, Highland 20/24, Lakeside 36/38, Savanna North 58/68, Savanna South 44/31. Proportion female: Savanna South 44/75 = **58.7%** (highest), Delta East 51/89 = 57.3%, Highland 45.5%, Lakeside 48.6%, Savanna North 46.0%, Coastal Hub 46.9%. Lesson: compute, don't eyeball.

</details>

**Exercise 7.** Explain the bug in `summarise(n = n(), s = sum(s), pct = 100 * mean(s))` and how you would detect it from the output alone.

<details>

<summary>Show answer (7)</summary>

`mean(s)` uses the *new* column `s` (a count), not the original logical column, so the percentage is wrong - for example 100 when the true share is 50%. It shows up as impossible values (a "percentage" above 100) or as results that disagree with a quick hand check. Fix by naming the new column differently.

</details>

### Challenge

**Exercise 8.** A colleague's file contains the date `04/05/2026`. Describe a process for deciding its format that does not rely on guessing, and what you would write into the script.

**Exercise 9.** Write a function `age_group(age)` returning `"0-4"`, `"5-14"`, `"15-44"`, `"45-64"`, `"65+"` or `NA`, and use it to compare sequencing percentage by age group. Is there a sign that some age groups are sequenced less?

<details>

<summary>Show answers (8-9)</summary>

8. Ask the data owner; look at *other* rows from the same source for a day above 12 (for example `25/05/2026` proves day-first); compare with other date columns (e.g. report date) for plausibility; record the decision as a comment (`# source X uses dd/mm/yyyy, confirmed by <name> on <date>`) and, ideally, ask the source to switch to ISO `YYYY-MM-DD`.
9.
   ```r
   age_group <- function(a) cut(a, breaks = c(-Inf, 4, 14, 44, 64, Inf),
                                labels = c("0-4","5-14","15-44","45-64","65+"))
   clean %>% mutate(ag = age_group(age)) %>% filter(!is.na(ag)) %>%
     group_by(ag) %>% summarise(n = n(), pct_seq = round(100 * mean(sequenced), 1))
   ```
   Interpret the output yourself; discuss whether any pattern reflects access to care.

</details>

## Self-test (8 questions)

1. Which reads a CSV as all text? (a) `read_csv(f)` (b) `read_csv(f, col_types = cols(.default = col_character()))` (c) `read.csv(f)` (d) `readLines(f)` returns a data frame
2. `df %>% filter(age > 10)` returns: (a) a column (b) rows where age > 10 (c) a plot (d) the mean
3. The result of `NA > 5` is: (a) `TRUE` (b) `FALSE` (c) `NA` (d) an error
4. For dates, `%b` means: (a) month number (b) abbreviated month name (c) year (d) weekday
5. In ggplot2, `aes()` maps: (a) data to visual properties (b) packages to scripts (c) colours to hex codes only (d) rows to columns
6. Why `distinct()` before analysis? (a) to sort rows (b) to remove duplicated records (c) to rename columns (d) to join tables
7. A sensible way to treat the age code `999` is: (a) keep it, mean ages are fine (b) convert to `NA` (c) convert to 99 (d) delete the whole file
8. A bar chart of "cases sequenced per district" alone is misleading because: (a) bars are ugly (b) it omits the denominator (cases that could have been sequenced) (c) it uses the wrong colour (d) districts are unordered

<details>

<summary>Show answers and reasons</summary>

1. **(b)** Setting the default column type to character keeps raw values.
2. **(b)** `filter` keeps rows.
3. **(c)** Comparisons with `NA` give `NA`.
4. **(b)** `%b` is the abbreviated month name; `%m` is the number.
5. **(a)** Aesthetics map data to x, y, colour, size and so on.
6. **(b)** `distinct()` removes duplicated rows.
7. **(b)** It is a missing-value code, not a real age.
8. **(b)** Without a denominator the chart shows capacity, not burden.

</details>

## Reflection prompt (150-250 words)

Describe a dataset you use that has the same kinds of problems (mixed formats, codes for "unknown", duplicates). Which three cleaning rules would you write first, and which would you ask someone to confirm before applying?

## Portfolio mini-deliverable

In `results/week03/`: `clean_linelist.R`, `linelist_clean.csv`, both PNG charts, and a 200-word `README.md` that states (1) the cleaning assumptions (date convention, how codes were treated), (2) what you checked, (3) one finding about sequencing bias.

{% endtab %}

{% tab title="6 · Go deeper" %}

## Core reading and lessons

- **R for Data Science (2nd edition)** ([r4ds.hadley.nz](https://r4ds.hadley.nz)): the best free book for importing, tidying, transforming and visualising data. Read *Data transformation*, *Data tidying*, *Data import*, and *Data visualization*.
- **The Carpentries - "R for Reproducible Scientific Analysis"** ([carpentries.org](https://carpentries.org)): a gentle, workshop-style introduction to R and the tidyverse for beginners.
- **Data Carpentry - "Data Analysis and Visualization in R for Ecologists"** ([datacarpentry.org](https://datacarpentry.org)): a similar beginner lesson, with strong coverage of data frames, dplyr and ggplot2.

## Free courses and videos

- **EMBL-EBI Training** ([ebi.ac.uk/training](https://www.ebi.ac.uk/training)): look for introductory R and statistics courses for life scientists.
- **Galaxy Training Network** ([training.galaxyproject.org](https://training.galaxyproject.org)): has an "Introduction to R" style tutorial in the statistics topic.

## Tool documentation

- **tidyverse documentation** (search "tidyverse dplyr reference"): the *dplyr*, *tidyr*, *readr* and *ggplot2* sites each have a cheat sheet and a reference.
- **`?function`** in R opens a function's help page (for example `?case_when`).
- **Bioconductor** ([bioconductor.org](https://www.bioconductor.org)): packages for genomic data in R, which you will meet in later weeks.

## Epidemiology in R

- **The Epidemiologist R Handbook** (search by title): a free, practical handbook for applied epidemiology in R, with chapters on cleaning data, epidemic curves and surveillance dashboards. Many of its examples will feel familiar after this week.
- **R Epidemics Consortium (RECON)** (search by name): packages and training for outbreak analytics.

## Data and bias

- Search for literature on **"genomic surveillance sampling bias"** and "representativeness of sequenced samples" to see how real programmes track coverage; we return to this in Week 10.

## Africa-focused and community

- **H3ABioNet** (search the name): pan-African bioinformatics training and resources, including R training.
- Local R user groups and "R-Ladies" chapters in your region (search for your city).

{% endtab %}

{% tab title="7 · Contribute" %}

You can help improve this week. Open an issue with the label **`week-03`** or edit the file directly - see [How to contribute](../contribute/README.md).

## Ideas for experts

1. **A base-R version:** add an optional version of the cleaning script that uses no tidyverse packages (useful where installing packages is difficult).
2. **`lubridate` alternative:** show a short tested alternative using `lubridate` for those who have it.
3. **More messy realities:** propose new, realistic data problems (for example, Excel serial dates, names with accents, mixed decimal commas) and a matching generator patch (see the data policy).
4. **Quarto:** add a tested Quarto template that renders the cleaning report as HTML.
5. **Local example:** replace the surveillance-bias discussion with a real, cited example of sequencing coverage in a country you know.
6. **Accessibility:** colour-blind-safe palettes and alt text for the charts.
7. **Translation:** translate the *Concepts* tab (label `translation`).

## Three-line "how to suggest a change"

1. Open an **issue** (*Suggest a change to a lesson*), or use *A lab command did not work* if the script fails for you.
2. Or click the **pencil** on this file on GitHub, edit it, and open a pull request.
3. A reviewer from the *computing* team will respond; see [How to contribute](../contribute/README.md).

**Version notes:** tested with R 4.3.3, readr 2.1.5, dplyr 1.1.4, tidyr 1.3.1, ggplot2 3.4.4 on Ubuntu 24.04 (October 2026). Output formatting (for example how tibbles print) may differ slightly in newer versions.

{% endtab %}

{% endtabs %}
