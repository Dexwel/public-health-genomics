---
description: Learn to move around Linux, read and summarise genomic text files, write a safe shell script, and use Git to keep your work.
---

# Week 2 — Linux and the command line for genomics

{% hint style="info" %}
**At a glance** · **Time:** ~6-8 h (2 h concepts, 3-4 h lab, 1-2 h practice) · **Prerequisites:** [Set up your computer](../start-here/setup.md) done, `bash scripts/check_setup.sh` passes · **You will produce:** a reusable shell script, a read-count table and a Git history of your notes · **Tools:** bash, grep, cut, sort, uniq, awk, zcat, git
{% endhint %}

{% tabs %}

{% tab title="1 · Start here" %}

## Why this matters

Almost every genomic tool - aligners, variant callers, QC programs, phylogenetics - is a **command-line program** that runs on Linux. National sequencing centres, cloud platforms and high-performance computing clusters are all Linux machines. A point-and-click program cannot be run on 500 samples at 2 a.m. while you sleep; a **script** can. And a script is also the best lab notebook there is: it records exactly what you did, so someone else (or you, in six months) can repeat it.

Many public health professionals find the terminal frightening: a blinking cursor, no buttons, and the folklore that one wrong command "deletes everything". This week we make the terminal an ally. You will learn about 30 commands. They are enough to do most of what you need in genomics, and they combine like building blocks.

## Learning objectives

By the end of this week you will be able to:

1. **Navigate** the Linux file system with absolute and relative paths.
2. **Create, copy, move and (carefully) remove** files and folders, and use wildcards.
3. **Inspect** large text and compressed files without opening them (`head`, `tail`, `less`, `wc`, `zcat`).
4. **Combine** commands with pipes and redirection to summarise a file (`grep`, `cut`, `sort`, `uniq`, `awk`).
5. **Handle** file names with spaces and special characters using quotes.
6. **Write** a bash script with variables, arguments, a loop, and safe settings (`set -euo pipefail`).
7. **Explain** file permissions and why a script may say "Permission denied".
8. **Use** Git to save, review and share your work (`init`, `add`, `commit`, `branch`, `log`).

## Roadmap

| Step | Time | Tab |
|---|---|---|
| Pre-check | 10 min | 1 · Start here |
| Read concepts, typing the examples as you go | 90-120 min | 2 · Concepts |
| Read the conversation | 20 min | 3 · Conversation |
| Lab (A-F) | 3-4 h | 4 · Hands-on lab |
| Exercises and self-test | 60-90 min | 5 · Practice |

## Key terms

| Term | Plain meaning |
|---|---|
| **Terminal** | The window where you type commands |
| **Shell (bash)** | The program that reads your commands and runs them |
| **Command** | A program you run by name, e.g. `ls` |
| **Argument / option (flag)** | What you give a command: `ls -l data` (option `-l`, argument `data`) |
| **Path** | The address of a file, e.g. `data/seq/ref/toy_ref.fa` |
| **Working directory** | The folder you are "in" right now (`pwd` prints it) |
| **Pipe (`\|`)** | Sends the output of one command into the next |
| **Script** | A text file of commands that bash runs in order |
| **Stdout / stderr** | The normal output stream / the error message stream |
| **Repository (repo)** | A folder whose history Git tracks |

## Pre-check (answers below)

1. What does `cd ..` do?
2. What is the difference between `>` and `>>`?
3. Why might `rm *.txt` be dangerous?
4. In `grep -c ERROR run.log`, what is `-c`?
5. Which is safer to use for a file named `My Results.csv`: `cat My Results.csv` or `cat "My Results.csv"`?

<details>

<summary>Show answers</summary>

1. Moves one level **up** to the parent folder.
2. `>` writes to a file, replacing anything already there; `>>` **appends** to the end.
3. It deletes every `.txt` file in the current folder immediately, with **no recycle bin**.
4. An **option**: print the **count** of matching lines instead of the lines.
5. `cat "My Results.csv"` - without quotes the shell treats `My` and `Results.csv` as two different files.

</details>

{% endtab %}

{% tab title="2 · Concepts" %}

## 2.1 Terminal, shell, Linux: three words, three things

- **Linux** is an operating system (like Windows or macOS). Most servers and scientific computers run it. macOS is also Unix-based, so these skills transfer.
- The **terminal** is the window. The **shell** is the program inside it that interprets what you type. The most common shell is **bash**.
- A typical prompt looks like this:

```text
user@computer:~/phg-course$ 
```

`user` is who you are, `computer` is the machine, `~/phg-course` is the folder you are in (`~` means your home folder), and `$` says "ready for your command". In this course we write commands **without** the prompt; you type only the command.

{% hint style="info" %}
**Public health lens.** Reproducibility is a public health value: a surveillance analysis that cannot be re-run cannot be audited. A script is a transparent, shareable, checkable record - far better than "I clicked here and there".
{% endhint %}

## 2.2 The file system is a tree

```text
/                          ← the root of everything
├── home/
│   └── amina/             ← "~" (home folder) of user "amina"
│       └── phg-course/    ← the course repository
│           ├── data/
│           │   ├── seq/
│           │   └── linux/
│           ├── weeks/
│           └── results/
└── usr/
    └── bin/               ← where many programs live
```

**Paths** tell the computer where something is.

| Path type | Starts with | Example | Meaning |
|---|---|---|---|
| **Absolute** | `/` | `/home/amina/phg-course/data` | From the root; works from anywhere |
| **Relative** | anything else | `data/seq` | From where you are now |
| **Home** | `~` | `~/phg-course` | Your home folder |
| **Here** | `.` | `./script.sh` | The current folder |
| **Parent** | `..` | `../data` | One level up |

Essential navigation:

| Command | What it does |
|---|---|
| `pwd` | **p**rint **w**orking **d**irectory: where am I? |
| `ls` | **l**i**s**t files. `ls -l` (long: sizes, dates, permissions), `ls -a` (include hidden files starting with `.`), `ls -lh` (human-readable sizes) |
| `cd folder` | **c**hange **d**irectory. `cd` alone goes home; `cd -` goes back to where you were |
| `tree` | Show a tree (not always installed) |

**Tab completion** is the best habit you can build: type the first letters of a name and press **Tab**; the shell completes it (press Tab twice to see options). It saves typing and prevents typos.

## 2.3 Making, copying, moving, deleting

| Command | What it does | Example |
|---|---|---|
| `mkdir` | make a folder (`-p` makes parents too) | `mkdir -p results/week02` |
| `touch` | create an empty file (or update its date) | `touch notes.txt` |
| `cp` | copy (`-r` for folders) | `cp -r data/linux/messy_project results/week02/` |
| `mv` | move **or rename** | `mv old.txt new.txt` |
| `rm` | remove (`-r` folders). **No undo.** | `rm results/tmp.txt` |
| `rmdir` | remove an empty folder | `rmdir empty_folder` |

{% hint style="danger" %}
**There is no recycle bin.** `rm` deletes permanently. Safe habits: (1) run `ls pattern` first to see what a wildcard will match, *then* replace `ls` with `rm`; (2) use `rm -i` (asks first) while you are learning; (3) never run `rm -rf` with a variable or path you did not read twice; (4) practise on copies, not on the original data.
{% endhint %}

### Wildcards (globbing)

The shell expands these *before* running the command:

| Pattern | Matches | Example |
|---|---|---|
| `*` | any characters (including none) | `ls *.fastq.gz` |
| `?` | exactly one character | `ls sample?_R1.fastq.gz` |
| `[ABC]` | one character from the set | `ls sample[AB]_R1.fastq.gz` |
| `{a,b}` | either text (brace expansion) | `ls sample{A,B}_R{1,2}.fastq.gz` |

{% hint style="warning" %}
**Gotcha:** if a pattern matches **nothing**, bash passes it through **unchanged**. So `zcat data/nope/*_R1.fastq.gz` tries to open a file literally called `*_R1.fastq.gz`. You will see this in the lab.
{% endhint %}

## 2.4 Looking inside files

| Command | Shows | Notes |
|---|---|---|
| `head -n 5 file` | first 5 lines | default is 10 |
| `tail -n 5 file` | last 5 lines | `tail -n +2 file` = everything **from** line 2 (skip a header) |
| `less file` | scroll through | `Space` next page, `/word` search, `q` quit |
| `cat file` | the whole file | careful with huge files |
| `wc -l file` | number of lines | `wc` also gives words and bytes |
| `file name` | what kind of file it is | |
| `zcat file.gz` | decompress to the screen | for `.gz` files, no need to unzip |

Genomic files are often *huge*. Never `cat` a 50 GB FASTQ: use `head`, or `zcat file.gz | head`.

## 2.5 Streams, redirection and pipes

Every command has three channels:

| Channel | Number | Default | Example |
|---|---|---|---|
| **stdin** | 0 | keyboard | |
| **stdout** | 1 | screen | normal results |
| **stderr** | 2 | screen | warnings and errors |

Redirection and pipes:

| Syntax | Meaning |
|---|---|
| `cmd > file` | send stdout to a file (**replaces** it) |
| `cmd >> file` | **append** stdout to a file |
| `cmd 2> errors.txt` | send **errors** to a file |
| `cmd > out.txt 2>&1` | send both to a file |
| `cmd1 \| cmd2` | **pipe**: stdout of cmd1 becomes stdin of cmd2 |
| `cmd \| tee out.txt` | show on screen **and** save |

A pipeline is like a production line: each command does one small job.

```text
sequencing_run.log ─► grep ERROR ─► wc -l ─► 13
```

## 2.6 The text-wrangling toolbox

Genomic files are mostly *text tables*. Six tools handle most questions:

| Tool | Job | Example |
|---|---|---|
| `grep` | find lines that match | `grep ERROR run.log` |
| `cut` | take columns | `cut -d, -f6 sheet.csv` (comma-separated, column 6) |
| `sort` | order lines | `sort -n` numeric, `-r` reverse, `-t, -k7,7n` by column 7 |
| `uniq -c` | count repeated lines (**input must be sorted**) | `sort \| uniq -c` |
| `tr` | translate/delete characters | `tr ',' '\t'` |
| `awk` | programmable column logic | `awk -F, 'NR>1 {s+=$7} END {print s}' sheet.csv` |

Useful `grep` options: `-c` count, `-v` invert (lines **without** the match), `-i` ignore case, `-n` show line numbers, `-o` print only the matched part, `-E` extended regular expressions (`grep -E 'WARN|ERROR'`).

**`awk` in one minute.** It reads a file line by line. `$1`, `$2`... are columns; `NR` is the line number; `-F,` sets the separator. A program looks like `condition { action }`. `BEGIN {...}` runs before the first line and `END {...}` after the last.

```bash
awk -F, 'NR>1 {sum[$6]+=$7} END {for (r in sum) print r, sum[r]}' sample_sheet.csv
```

means: skip the header (`NR>1`), add column 7 into a bucket named by column 6, and at the end print each bucket - a group-by in one line.

### Why `sort | uniq -c`?

`uniq` only collapses *adjacent* identical lines, so `sort` first. The pattern `cut | sort | uniq -c` counts how often each value occurs - you will use it every week.

## 2.7 Compressed files

Sequencing data are stored compressed: `.gz` (gzip). You can read them without unpacking:

| Command | Meaning |
|---|---|
| `zcat file.gz` | print the decompressed content |
| `gzip file` / `gunzip file.gz` | compress / decompress (replaces the file) |
| `tar -czf out.tar.gz folder/` | pack a folder into one compressed archive |
| `tar -xzf archive.tar.gz` | unpack |

A FASTQ record is **4 lines**, so the number of reads is `lines / 4`: `zcat reads.fastq.gz | wc -l` then divide by 4.

## 2.8 Variables, quotes and spaces

```bash
sample="sampleA"                 # no spaces around "="
echo "$sample"                   # → sampleA     (use $ to read it)
echo "${sample}_R1.fastq.gz"     # braces mark where the name ends
n=$(zcat file.gz | wc -l)        # $(...) runs a command and captures its output
echo $(( n / 4 ))                # $(( ... )) does integer arithmetic
```

**Quoting rules**

| Quotes | Effect | Use when |
|---|---|---|
| `"double"` | variables and `$(...)` expand; spaces are kept together | almost always |
| `'single'` | nothing expands; completely literal | `awk` programs, regular expressions |
| none | the shell splits on spaces and expands wildcards | rarely what you want |

**The spaces problem.** If a file is called `Sample A final FINAL v2.txt`, then `cat Sample A final FINAL v2.txt` means *five* different files. Always quote: `cat "Sample A final FINAL v2.txt"`, or press Tab to auto-escape. Better: **avoid spaces in names** (use `_` or `-`), use lower-case, and keep dates in `YYYY-MM-DD`.

**Environment variables and PATH.** `echo $HOME` prints your home folder. `PATH` is a list of folders where the shell looks for programs; if a tool is "not found", it is either not installed or not in `PATH` (`which tool` shows where the shell finds it).

## 2.9 Permissions

`ls -l` shows ten characters at the start of each line:

```text
-rwxr-xr--  1 amina team  1180 Mar 30 10:02 script.sh
│└┬┘└┬┘└┬┘
│ │  │  └─ other users: r-- (read only)
│ │  └──── group:       r-x (read and execute)
│ └─────── owner:       rwx (read, write, execute)
└───────── type: - file, d directory
```

`chmod +x script.sh` gives permission to **execute** a script (so you can run `./script.sh`). If you only want to run it once you can always say `bash script.sh`, which needs no execute bit. "Permission denied" usually means you lack read/write/execute permission, or you are trying to write somewhere you do not own.

## 2.10 Scripts: from typing to reproducing

A **bash script** is a text file of commands. A good first line is the **shebang**, `#!/usr/bin/env bash`, which tells the system which interpreter to use. Then a safety line:

```bash
set -euo pipefail
```

| Flag | Meaning |
|---|---|
| `-e` | stop at the first command that fails |
| `-u` | treat use of an unset variable as an error |
| `-o pipefail` | a pipeline fails if **any** step fails (not just the last) |

Together they turn silent corruption into a loud, early failure - the right behaviour for science.

**Arguments and defaults**

```bash
reads_dir="${1:-data/seq/reads}"    # first argument, or a default if none given
```

**Loops**

```bash
for r1 in data/seq/reads/*_R1.fastq.gz; do
  sample=$(basename "$r1" _R1.fastq.gz)   # strip folder and suffix
  echo "$sample"
done
```

**If**

```bash
if [ -f "$file" ]; then echo "found"; else echo "missing"; fi
```

**Exit codes.** Every command returns a number: `0` = success, anything else = failure. `echo $?` shows the last one.

**Good scripting habits**

1. Put a comment block at the top: what it does, how to run it.
2. Never hard-code a path that exists only on your computer; use arguments.
3. Write results to a *new* folder; never overwrite raw data.
4. Print progress to the screen (stderr) and save outputs to files.
5. Record versions: `samtools --version | head -n 1`.
6. Keep scripts in Git.

## 2.11 Getting software

| Method | What | When |
|---|---|---|
| **apt** | The Ubuntu/Debian package manager (`sudo apt-get install`) | Standard Ubuntu systems |
| **conda / mamba (Bioconda)** | Isolated environments with versions you choose | Most bioinformatics work; reproducible with `environment.yml` |
| **Containers** (Docker, Apptainer/Singularity) | A whole pre-built system in a box | Pipelines, clusters, long-term reproducibility |
| **Compiling from source** | Last resort | Rare tools |

On a cluster you rarely run big jobs on the login computer; you submit them to a **scheduler** (for example Slurm) with a script. Everything you learn this week carries straight over.

## 2.12 Git in ten minutes

**Git** records snapshots (**commits**) of a folder, so you can see what changed, undo mistakes and collaborate without overwriting each other. GitHub is a website that hosts Git repositories.

| Command | Meaning |
|---|---|
| `git init -b main` | start tracking this folder |
| `git status` | what has changed? |
| `git add file` | stage a change for the next snapshot |
| `git commit -m "message"` | save the snapshot |
| `git log --oneline` | the history |
| `git diff` | show unsaved changes |
| `git switch -c name` | create and move to a new **branch** (a parallel line of work) |
| `git clone URL` | copy a repository |
| `git pull` / `git push` | get / send changes from / to a remote |

Write commit messages that say *why*: "Week 2: count reads per sample" beats "update".

{% endtab %}

{% tab title="3 · Conversation" %}

*The laboratory's computer room. Tunde has a terminal open. Zainab is holding a mug and looking at the screen the way a person looks at a snake.*

**Zainab:** I want it on record that I am only here because the Ministry wants a "data-literate district team". I clicked on my first computer's spreadsheet icon, not on a black window.

**Dr. Mensah:** (from the doorway) Noted, and welcome. Sit down. Tunde, let her drive.

**Tunde:** Type `pwd`.

**Zainab:** `pwd`. It says `/home/zainab/phg-course`. Is that… where I am?

**Tunde:** Yes: it means **print working directory**. Now `ls`.

**Zainab:** It lists folders: `data`, `weeks`, `scripts`… Lovely. So it's just a filing cabinet with no pictures.

**Dr. Mensah:** Exactly. And now the one habit that will save you hours. Type `cd da` and press the Tab key.

**Zainab:** (pressing) It completed to `data/`. Magic.

**Dr. Mensah:** It is not magic; it is saving your fingers from typos. The most common errors in this field are typos in file names. Tab never typos.

**Zainab:** Fine. Let me look at a file. `cat sample_sheet.csv`. (A wall of text appears.) Too much! How do I read it?

**Tunde:** Don't `cat` unless the file is small. Use `head -n 5` to see the first five lines. Imagine this was a FASTQ file of fifty gigabytes.

**Zainab:** I would have frozen my computer.

**Tunde:** You would have waited a long time and learned a lesson.

**Zainab:** (typing) Good. Now, I want to know how many samples came from each region. In a spreadsheet I'd make a pivot table.

**Dr. Mensah:** Try this. `cut -d, -f6 sample_sheet.csv`. Then think: what did `-d,` mean?

**Zainab:** The delimiter is a comma, and `-f6` is field six. The region column. But it prints the header too.

**Tunde:** Pipe it. `tail -n +2` throws away the header. Then `sort`, then `uniq -c`.

**Zainab:** (typing) `cut -d, -f6 sample_sheet.csv | tail -n +2 | sort | uniq -c`. It says: East 3, North 9, South 6, West 6. A pivot table in one line! Why do I need `sort`?

**Dr. Mensah:** What does `uniq` do?

**Zainab:** Collapses repeats?

**Dr. Mensah:** Only *neighbouring* repeats. If North, South, North appear in that order, `uniq` sees three separate runs. So sort first.

**Zainab:** I can see why people like this. It's like building with Lego.

**Tunde:** Now the dangerous bit. I'll show you my "messy project" folder. Type `ls`.

**Zainab:** `Sample A final FINAL v2.txt`… `results (old).csv`… `Results_NEW.csv`… Tunde, this is an archaeological site.

**Tunde:** (sheepishly) Every lab has one. Try to open the first file. `cat Sample A final FINAL v2.txt`.

**Zainab:** `No such file or directory`. Five times. It's complaining about `Sample`, `A`, `final`, `FINAL` and `v2.txt`.

**Dr. Mensah:** What is the shell doing?

**Zainab:** Treating the spaces as separators, so it thinks I gave it five different files.

**Dr. Mensah:** Exactly. Use quotes: `cat "Sample A final FINAL v2.txt"`. Or avoid spaces forever. A good rule: lower case, underscores, dates as year-month-day.

**Zainab:** Can I just delete the ugly ones? `rm *`…

**Tunde:** (leaping up) STOP. What do you think `rm *` does?

**Zainab:** Removes everything?

**Tunde:** In *this folder*. Permanently. There is no recycle bin. Last year a postdoc lost two weeks of results with `rm *.txt` in the wrong folder.

**Dr. Mensah:** The safe pattern: first type `ls *.txt`. If the list is exactly what you want to delete, press the up arrow and change `ls` to `rm`. Better still: work on a *copy*. Never practise on raw data.

**Zainab:** I made the mistake before I made it. That counts, right?

**Dr. Mensah:** Prevented mistakes count double. Now, the part that turns this from tinkering into science: writing it down. Tunde, show her the script.

**Tunde:** Here. The script counts read pairs in every sample. First line: `set -euo pipefail`.

**Zainab:** What does that do?

**Tunde:** It makes the script *stop* the moment anything goes wrong. Without it, if the file is missing, the script carries on and writes a table saying "0 reads" - and nobody notices.

**Zainab:** A silent zero. Like a district that stops reporting and the dashboard shows no cases.

**Dr. Mensah:** That is exactly the kind of failure we fear in surveillance. Loud failures are friends. Run it.

**Zainab:** (running `bash count_reads.sh`) It says sampleA 1400, sampleB 1200, sampleC 280. And what if I point it at a folder that doesn't exist?

**Tunde:** Try.

**Zainab:** It says `gzip: data/nope/*_R1.fastq.gz: No such file or directory` and stops. Oh, look at that file name: it's the pattern itself, with the star.

**Tunde:** Because when a wildcard matches nothing, bash hands you the pattern untouched. A famous trap. Our script stopped because of `set -e`; without it you might never have noticed.

**Zainab:** A tool that fails loudly is a tool I can trust. I think I just changed my mind about the black window.

**Dr. Mensah:** Don't flatter it too soon. Last thing. Where do these scripts live?

**Zainab:** In a folder on this computer?

**Dr. Mensah:** And if the computer dies? Or you change something and break it? That is what Git is for: a history of every change. One more command: `git commit`. It is a save point you can always return to.

**Zainab:** So I can try things without fear.

**Dr. Mensah:** That is the whole secret of working confidently: make it cheap to undo.

### Talking points for the forum

1. Describe a time a "silent failure" (a blank or zero where an error should have appeared) caused trouble in a data system you know. How would `set -euo pipefail` style thinking help?
2. Why are spaces in file names such a persistent problem, and what naming convention would your team adopt?
3. What would you want recorded in a script or Git history so that someone could re-run a surveillance report you made last year?

{% endtab %}

{% tab title="4 · Hands-on lab" %}

{% hint style="success" %}
**Lab goal.** Use the shell to summarise a sample sheet and a sequencing-run log, count reads in compressed FASTQ files, tame a messy folder safely, write a script, and keep your work in Git. Every command was run on the course data. Always start **from the repository root**, and write outputs to `results/week02/`.
{% endhint %}

```bash
mkdir -p results/week02
```

## Part A - Orientation (15 min)

### Step 1. Where am I?

```bash
pwd
ls
ls -l data/linux
```

`ls -l` shows type and permissions, size, date and name. You should see two folders (`fastq_mini`, `messy_project`) and two files (`sample_sheet.csv` of about 1.2 KB and `sequencing_run.log` of about 16 KB).

### Step 2. Practise Tab completion

Type `ls data/li` then press **Tab**. It should become `ls data/linux/`. Press Tab again after `data/linux/s` to see the choices.

## Part B - Summarise a table and a log (60 min)

### Step 3. Look at the sample sheet

```bash
head -n 4 data/linux/sample_sheet.csv
wc -l data/linux/sample_sheet.csv
```

```text
sample_id,run,lane,barcode,collection_date,region,read_pairs
S001,RUN_0412,1,ACGTAC,2026-03-11,South,837218
S002,RUN_0412,3,ACGTAC,2026-03-15,West,610846
S003,RUN_0412,1,ACGTAC,2026-03-05,North,842966
25 data/linux/sample_sheet.csv
```

That is 24 samples plus a header line.

### Step 4. Count samples per region

```bash
cut -d, -f6 data/linux/sample_sheet.csv | tail -n +2 | sort | uniq -c
```

```text
      3 East
      9 North
      6 South
      6 West
```

**Stop and check:** the counts add up to 24.

### Step 5. Total read pairs per region (awk)

```bash
awk -F, 'NR>1 {sum[$6]+=$7} END {for (r in sum) print r, sum[r]}' data/linux/sample_sheet.csv | sort
```

```text
East 1775642
North 6327075
South 2589882
West 3257631
```

### Step 6. Which samples have the most (and fewest) reads?

```bash
tail -n +2 data/linux/sample_sheet.csv | sort -t, -k7,7nr | head -n 3 | cut -d, -f1,6,7
tail -n +2 data/linux/sample_sheet.csv | sort -t, -k7,7n  | head -n 1 | cut -d, -f1,7
```

```text
S011,North,886642
S003,North,842966
S001,South,837218
S006,167971
```

`-t,` sets the separator, `-k7,7` sorts on column 7, `n` means numeric, `r` reverse.

### Step 7. Read the sequencing-run log

```bash
head -n 3 data/linux/sequencing_run.log
awk '{print $3}' data/linux/sequencing_run.log | sort | uniq -c
```

```text
2026-03-30 09:00:33 INFO  [lane4] lane 4 Q30 83%
2026-03-30 09:01:45 INFO  [lane2] lane 2 Q30 82%
2026-03-30 09:02:36 INFO  [lane1] lane 1 Q30 94%
     13 ERROR
    260 INFO
     27 WARN
```

(Column 3 of each line is the severity.) Now look at the errors and which lanes produce the warnings:

```bash
grep ERROR data/linux/sequencing_run.log | head -n 3
grep WARN data/linux/sequencing_run.log | grep -o 'lane[0-9]' | sort | uniq -c
```

```text
2026-03-30 09:40:25 ERROR [lane2] tile 1177 failed focus check
2026-03-30 09:56:36 ERROR [lane3] tile 1218 failed focus check
2026-03-30 10:10:20 ERROR [lane4] tile 1217 failed focus check
     11 lane1
      4 lane2
      2 lane3
     10 lane4
```

**Stop and check:** lanes 1 and 4 have the most warnings (low-quality Q30 messages). In a real run you would tell the sequencing core.

### Step 8. Save a summary

```bash
{
  echo "Severity counts"
  awk '{print $3}' data/linux/sequencing_run.log | sort | uniq -c
  echo
  echo "Warnings per lane"
  grep WARN data/linux/sequencing_run.log | grep -o 'lane[0-9]' | sort | uniq -c
} > results/week02/run_summary.txt
cat results/week02/run_summary.txt
```

The braces group several commands so one `>` redirects all their output.

## Part C - Count reads in FASTQ files (30 min)

### Step 9. Reads per sample

A FASTQ record has 4 lines, so reads = lines ÷ 4.

```bash
for f in data/seq/reads/sample*_R1.fastq.gz; do
  echo "$f $(( $(zcat "$f" | wc -l) / 4 ))"
done
```

```text
data/seq/reads/sampleA_R1.fastq.gz 1400
data/seq/reads/sampleB_R1.fastq.gz 1200
data/seq/reads/sampleC_R1.fastq.gz 280
```

### Step 10. Check read length

```bash
zcat data/seq/reads/sampleA_R1.fastq.gz | awk 'NR%4==2 {print length($0)}' | sort -n | uniq -c
```

```text
   1400 100
```

(`NR%4==2` selects line 2, 6, 10... - the sequence lines.) All 1,400 reads are 100 bases.

### Step 11. A famous trap: counting `@`

A FASTQ read name starts with `@`. Count lines starting with `@` in a small file:

```bash
wc -l data/linux/fastq_mini/sampleA_mini_R1.fastq
grep -c '^@' data/linux/fastq_mini/sampleA_mini_R1.fastq
```

```text
100 data/linux/fastq_mini/sampleA_mini_R1.fastq
26
```

100 lines means **25 reads**, but `grep` found **26** lines beginning with `@`. Why? A **quality line** can also begin with `@` (the character `@` is a valid quality score, Q31). So counting `@` is unreliable; counting lines ÷ 4 is safe. Find the culprit:

```bash
awk 'NR%4==0 && /^@/ {print NR": "substr($0,1,30)}' data/linux/fastq_mini/sampleA_mini_R1.fastq
```

**Stop and check:** you should see exactly one line number that is a multiple of 4 (a quality line starting with `@`).

## Part D - Tame the messy folder (30 min)

### Step 12. See why quoting matters

```bash
ls -1 data/linux/messy_project
cat data/linux/messy_project/Sample A final FINAL v2.txt
```

The second command fails (five separate arguments). Now quote it:

```bash
cat "data/linux/messy_project/Sample A final FINAL v2.txt"
```

```text
placeholder for Sample A final FINAL v2.txt
```

### Step 13. Work on a **copy**, never the original

```bash
rm -rf results/week02/messy_project          # safe: it is in results/ and we made it
cp -r data/linux/messy_project results/week02/messy_project
```

### Step 14. Rename safely with a loop

```bash
cd results/week02/messy_project
find . -type f -print0 | while IFS= read -r -d '' f; do
  dir=$(dirname "$f"); base=$(basename "$f")
  new=$(printf '%s' "$base" | tr '[:upper:] ' '[:lower:]_' | tr -d '()')
  if [ "$base" != "$new" ]; then
    mv -n -- "$f" "$dir/$new"          # -n: never overwrite
    echo "renamed: $base -> $new"
  fi
done
cd ../../..                              # back to the repository root
```

```text
renamed: Sample A final FINAL v2.txt -> sample_a_final_final_v2.txt
renamed: sample_b notes.TXT -> sample_b_notes.txt
renamed: lane1 reads.fq -> lane1_reads.fq
renamed: Results_NEW.csv -> results_new.csv
renamed: README -> readme
renamed: fig1 - draft.png.txt -> fig1_-_draft.png.txt
renamed: results (old).csv -> results_old.csv
```

(The order may differ on your computer.) What the loop does: `find ... -print0` lists files separated by NUL characters (safe with spaces), `read -d ''` reads them one by one, `tr` lower-cases and swaps spaces for `_`, `tr -d '()'` removes brackets, and `mv -n` refuses to overwrite.

**Stop and check:** `find results/week02/messy_project -type f | sort` should list ten files, none of them containing a space *except* the folder `Run 3` (we renamed files, not folders). That is a deliberate reminder to quote paths. The rename of `README` to `readme` also reminds you that automatic rules can be too eager: always review what a script did.

## Part E - Your first script (45 min)

### Step 15. Create the script

Open a text editor (`nano results/week02/count_reads.sh`) and type, or use this command to create it:

```bash
cat > results/week02/count_reads.sh <<'EOF'
#!/usr/bin/env bash
# count_reads.sh - count read pairs in every R1 FASTQ file of a folder.
# Usage: bash results/week02/count_reads.sh [reads_folder] [output_file]
set -euo pipefail                      # stop on errors, unset variables and failed pipes

reads_dir="${1:-data/seq/reads}"       # first argument, or a default
out="${2:-results/week02/read_counts.tsv}"

mkdir -p "$(dirname "$out")"
printf 'sample\tread_pairs\n' > "$out"

for r1 in "$reads_dir"/*_R1.fastq.gz; do
  sample=$(basename "$r1" _R1.fastq.gz)
  lines=$(zcat "$r1" | wc -l)
  printf '%s\t%d\n' "$sample" $(( lines / 4 )) >> "$out"
  echo "counted $sample" >&2           # progress goes to the screen (stderr)
done
cat "$out"
EOF
```

(The `<<'EOF'` ... `EOF` form is a *here-document*: everything between is written to the file exactly as typed.)

### Step 16. Run it

```bash
bash results/week02/count_reads.sh
```

```text
counted sampleA
counted sampleB
counted sampleC
sample	read_pairs
sampleA	1400
sampleB	1200
sampleC	280
```

**Stop and check:** `cat results/week02/read_counts.tsv` shows the same table, and `echo $?` after the script prints `0`.

### Step 17. Break it on purpose

```bash
bash results/week02/count_reads.sh data/nope
echo "exit code: $?"
```

```text
gzip: data/nope/*_R1.fastq.gz: No such file or directory
exit code: 1
```

The script stopped with a non-zero exit code, because of `set -euo pipefail`. Notice the file name in the error is the *unexpanded pattern*: no files matched. Real scripts often add `shopt -s nullglob` or an explicit check (`ls "$reads_dir"/*_R1.fastq.gz > /dev/null`) to give a friendlier message.

### Step 18. Make it executable and log it

```bash
chmod +x results/week02/count_reads.sh
./results/week02/count_reads.sh 2>&1 | tee results/week02/count_reads.log
ls -l results/week02/count_reads.sh
```

The `-rwx...` at the start shows it is now executable. `tee` shows the output *and* saves it.

## Part F - Version control with Git (30 min)

Practise in a scratch folder so you cannot harm the course repository.

```bash
mkdir -p results/week02/git_practice && cd results/week02/git_practice
git init -b main
git config user.name  "Your Name"
git config user.email "you@example.org"
echo "# My lab notebook" > notebook.md
git status --short
git add notebook.md
git commit -m "Start notebook"
git switch -c week02-notes
echo "Learned pipes and awk" >> notebook.md
git diff --stat
git commit -am "Add notes on pipes and awk"
git log --oneline --graph --all
cd ../../..
```

You should see two commits, the newest on branch `week02-notes`. Commit messages and hashes will differ from anyone else's.

**Stop and check:** `git log --oneline` lists both commits; `git status` says the working tree is clean.

## If it breaks

| Symptom | Likely cause | Fix |
|---|---|---|
| `No such file or directory` | Wrong folder or path typo | `pwd`, `ls`, use Tab completion |
| `Permission denied` running a script | Not executable | `bash script.sh` or `chmod +x script.sh` |
| `zcat: command not found` (macOS) | macOS calls it `gzcat` | Use `gzcat`, or `gunzip -c file \| ...` |
| Output scrolls past | Too long | Add `\| less` or `\| head` |
| `uniq -c` gives odd counts | Input not sorted | Add `sort` before `uniq -c` |
| `awk: syntax error` | Quote mismatch | Use **single** quotes around the program |
| Git asks for identity | Not configured | `git config user.name` and `user.email` |
| Prompt shows `>` and nothing runs | An unclosed quote | Press `Ctrl+C`, retype |

## Stretch challenge

Write `results/week02/log_summary.sh` that takes a log file as argument and prints (1) the number of lines at each severity, (2) the lane with the most ERROR lines, and (3) the time of the first and last line. Test it on `data/linux/sequencing_run.log` and on a file that does not exist (it should fail loudly with a helpful message).

{% endtab %}

{% tab title="5 · Practice" %}

## Exercises

### Basic

**Exercise 1.** Which command prints the last 5 lines of `data/linux/sequencing_run.log`?

**Exercise 2.** What does `ls data/seq/reads/sample[AB]_R1.fastq.gz` print?

**Exercise 3.** Write one command that counts the number of `WARN` lines in the run log.

**Exercise 4.** Explain what `cmd1 > file` and `cmd1 | cmd2` each do.

<details>

<summary>Show answers (1-4)</summary>

1. `tail -n 5 data/linux/sequencing_run.log`
2. `data/seq/reads/sampleA_R1.fastq.gz` and `data/seq/reads/sampleB_R1.fastq.gz` (the `[AB]` matches one of A or B; sampleC is excluded).
3. `grep -c WARN data/linux/sequencing_run.log` → **27**.
4. `>` writes the command's output into a file (replacing it); `|` feeds the output directly as the input of the next command.

</details>

### Intermediate

**Exercise 5.** How many `WARN` lines are for lane 4? And how many `ERROR` lines per lane? Use one pipeline for each.

**Exercise 6.** What is the mean number of read pairs per sample in the sample sheet (rounded to the nearest whole number)? Use `awk`.

**Exercise 7.** The file `data/linux/sample_sheet.csv` has samples collected in which months? (Hint: `cut -c1-7`.)

<details>

<summary>Show answers (5-7)</summary>

5. `grep WARN data/linux/sequencing_run.log | grep -c lane4` → **10**.
   `grep ERROR data/linux/sequencing_run.log | grep -o 'lane[0-9]' | sort | uniq -c` → lane1 1, lane2 4, lane3 5, lane4 3 (total 13).
6. `awk -F, 'NR>1{s+=$7;n++} END{printf "%d samples, mean %.0f\n", n, s/n}' data/linux/sample_sheet.csv` → `24 samples, mean 581260`.
7. `cut -d, -f5 data/linux/sample_sheet.csv | tail -n +2 | cut -c1-7 | sort | uniq -c` → all 24 in `2026-03`.

</details>

**Exercise 8.** A colleague's script runs `rm -rf $output_dir/*`. The variable `output_dir` is accidentally empty. What command does the shell run? How could `set -u` and a check protect you?

<details>

<summary>Show answer (8)</summary>

With an empty variable the command becomes `rm -rf /*` - an attempt to delete everything the user may delete. `set -u` makes the script **stop** when an unset variable is used (an *empty but set* variable needs an explicit check, e.g. `[ -n "$output_dir" ] || { echo "output_dir is empty" >&2; exit 1; }`), and using `"${output_dir:?output_dir is not set}"` aborts with a message when it is unset or empty.

</details>

### Challenge

**Exercise 9.** Write a loop that, for every FASTQ in `data/seq/reads/`, prints the file name and the **average read length** of the first 100 reads (hint: `zcat | head -n 400 | awk 'NR%4==2{s+=length($0);n++} END{print s/n}'`).

**Exercise 10.** Explain why `grep -c '^@' file.fastq` can over-count reads, and give a correct way.

<details>

<summary>Show answers (9-10)</summary>

9.
   ```bash
   for f in data/seq/reads/*.fastq.gz; do
     avg=$(zcat "$f" | head -n 400 | awk 'NR%4==2{s+=length($0);n++} END{print s/n}')
     echo "$f $avg"
   done
   ```
   All files print 100 (all reads are 100 bases).
10. A quality line may begin with `@`, which is also a valid quality character. The robust method is `lines / 4` (`zcat f \| wc -l`), or an `awk` that checks `NR%4==1`.

</details>

## Command cheat sheet

| Goal | Command |
|---|---|
| Where am I? | `pwd` |
| List with details | `ls -lh` |
| Go to folder / up / home | `cd dir` / `cd ..` / `cd` |
| First / last lines | `head -n 5 f` / `tail -n 5 f` |
| Skip header | `tail -n +2 f` |
| Count lines | `wc -l f` |
| Read gzip | `zcat f.gz \| head` |
| Search | `grep -c pat f`, `grep -v pat f`, `grep -E 'a\|b' f` |
| Columns | `cut -d, -f1,3 f` |
| Count categories | `... \| sort \| uniq -c` |
| Sort numerically (by column) | `sort -t, -k7,7n` |
| Sum a column | `awk -F, 'NR>1{s+=$7} END{print s}' f` |
| Save and show output | `cmd \| tee out.txt` |
| Make executable | `chmod +x script.sh` |
| Save a snapshot | `git add f && git commit -m "why"` |

## Common mistakes

| Mistake | Symptom | Prevention |
|---|---|---|
| Forgetting to quote a path with spaces | "No such file" for each word | Quote, or avoid spaces |
| `uniq -c` without `sort` | Counts of 1 everywhere | Always sort first |
| Using `>` when you meant `>>` | File replaced, data lost | Read the line twice; work on copies |
| Writing results into `data/` | Raw data modified | Write to `results/` |
| Running `rm` with a wildcard | Files deleted | Test with `ls` first |
| Pasting commands you do not understand | Surprise outcomes | Read each line; ask |
| No `set -euo pipefail` | Silent partial results | Start every script with it |

## Self-test (8 questions)

1. `ls ..` lists: (a) the current folder (b) the parent folder (c) the home folder (d) hidden files
2. A pipeline `A | B | C` fails in the *middle* step B but C succeeds. By default bash reports: (a) failure (b) C's exit status (c) B's exit status (d) a warning only
3. Which prints only the *column 6* of a comma-separated file? (a) `cut -f6` (b) `cut -d, -f6` (c) `cut -c6` (d) `awk 6`
4. To append output to a file you use: (a) `>` (b) `>>` (c) `|` (d) `<`
5. `rm *.txt` removes: (a) .txt files in the current folder (b) all folders (c) only one file (d) nothing until confirmed
6. Which line of a FASTQ record holds the base qualities? (a) 1 (b) 2 (c) 3 (d) 4
7. What does `set -e` do? (a) Echo commands (b) Exit on the first error (c) Set an environment variable (d) Enable extended globbing
8. What does `git commit -m "msg"` do? (a) uploads to GitHub (b) saves a snapshot locally (c) deletes a branch (d) shows history

<details>

<summary>Show answers and reasons</summary>

1. **(b)** `..` is the parent folder.
2. **(b)** By default a pipeline returns the **last** command's status, which is why `pipefail` exists.
3. **(b)** `-d,` sets the delimiter and `-f6` picks the field.
4. **(b)** `>>` appends.
5. **(a)** Only `.txt` files in the current folder, immediately.
6. **(d)** Line 4: line 1 header, 2 sequence, 3 `+`, 4 qualities.
7. **(b)** Stop at the first command that fails.
8. **(b)** A local snapshot; `git push` uploads.

</details>

## Reflection prompt (150-250 words)

Think of a repetitive data task in your work (for example compiling a weekly report). Which parts could be a script? What would you need to make it safe and repeatable?

## Portfolio mini-deliverable

A folder `results/week02/` containing: `count_reads.sh`, `read_counts.tsv`, `run_summary.txt`, your Git practice repository, and a short `NOTES.md` listing five commands you learned and one mistake you made.

{% endtab %}

{% tab title="6 · Go deeper" %}

## Core reading and lessons

- **The Carpentries - "The Unix Shell"** ([carpentries.org](https://carpentries.org)): a gentle, widely taught lesson with exercises. Look for the lesson from the Software Carpentry collection (navigation, pipes, loops, scripts).
- **The Carpentries - "Version Control with Git"**: the standard beginner Git lesson.
- **Data Carpentry - Genomics workshop** ([datacarpentry.org](https://datacarpentry.org)): shows these same tools used on real sequencing data, including a shell-genomics introduction.

## Free courses and videos

- **EMBL-EBI Training** ([ebi.ac.uk/training](https://www.ebi.ac.uk/training)): search for introductory bioinformatics and command-line courses.
- **Galaxy Training Network** ([training.galaxyproject.org](https://training.galaxyproject.org)): has a section on *Introduction to Unix and Linux for bioinformatics* style material; search the catalogue.

## Tool documentation

- **GNU coreutils manual** (search for "GNU coreutils" and read the pages on `sort`, `cut`, `uniq`).
- **`man` pages**: type `man grep` in the terminal (press `q` to quit). `grep --help | less` also works.
- **GitHub Docs** ([docs.github.com](https://docs.github.com)): a good "Hello World" and Git cheat sheet pages.

## Practice ideas

- Use the same tools on your own (non-sensitive) spreadsheets exported as CSV: count categories, find duplicates.
- Read other people's scripts: pick one from a public repository and annotate it.

## Africa-focused and community

- **H3ABioNet** (search for "H3ABioNet training"): the pan-African bioinformatics network, which offered introductory bioinformatics and Linux training and resources.
- Local communities: search for Carpentries or bioinformatics meetups in your country.

{% endtab %}

{% tab title="7 · Contribute" %}

You can help improve this week. Open an issue with the label **`week-02`** or edit the file directly - see [How to contribute](../contribute/README.md).

## Ideas for experts

1. **Windows and Mac variations:** add a short "if your terminal behaves differently" box (PowerShell vs WSL2; macOS `zcat` vs `gzcat`).
2. **HPC section:** add a worked example of submitting the script to a Slurm scheduler, with an `sbatch` file (label it as optional).
3. **Better error messages:** extend Step 17 with `shopt -s nullglob` and an explicit "no files found" message; test it.
4. **More awk:** add two more awk recipes from your own work (for example computing a 7-day moving average).
5. **Accessibility:** a screen-reader-friendly version of the file-tree diagrams.
6. **Translation:** translate the Concepts tab into another language (label `translation`).
7. **Security:** a note on safe handling of credentials and sensitive data in scripts.

## Three-line "how to suggest a change"

1. Open an **issue** (*Suggest a change to a lesson*) for anything wrong or unclear.
2. Or click the **pencil** on this file on GitHub, edit it and open a pull request.
3. A reviewer from the *computing* team will respond; see [How to contribute](../contribute/README.md).

**Version notes:** commands tested with GNU bash 5.2, GNU coreutils, gawk/mawk, and Git on Ubuntu 24.04 (October 2026). Outputs shown are from the course data generated with seed 20261015.

{% endtab %}

{% endtabs %}
