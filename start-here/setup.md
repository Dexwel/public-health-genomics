---
description: Get a working computer for the course on Windows, macOS, Linux, or in your browser.
---

# Set up your computer

You need a Unix-like command line, R, and a handful of bioinformatics tools. Pick **one** of four routes. All four end with the same check: `bash scripts/check_setup.sh` prints "You are ready for Week 1".

| Route | Best for | Needs | Effort |
|---|---|---|---|
| **A. GitHub Codespaces** | Anyone with a browser and a GitHub account; shared or locked-down computers | Internet; a free GitHub account | 5 min |
| **B. Windows + WSL2** | Windows 10/11 users | Admin rights once; 15 GB disk | 30 min |
| **C. macOS or Linux + conda** | Mac and Linux users | 10 GB disk | 20 min |
| **D. Ubuntu/Debian with apt** | Ubuntu users who prefer system packages | `sudo` | 15 min |

{% tabs %}

{% tab title="A · Codespaces (browser)" %}

1. Create a free GitHub account at github.com if you do not have one.
2. Open the course repository, click the green **Code** button → **Codespaces** → **Create codespace on main**.
3. Wait a few minutes while the environment builds (it installs the tools using `.devcontainer/devcontainer.json`).
4. A VS Code editor opens in your browser with a terminal at the bottom. Continue at **Check your setup** below.

Notes: free accounts have a monthly allowance of Codespaces hours (check GitHub's current limits). **Stop** the codespace when you finish (Codespaces menu → *Stop codespace*), or it keeps using your allowance.

{% endtab %}

{% tab title="B · Windows (WSL2)" %}

WSL2 (Windows Subsystem for Linux) runs a real Ubuntu inside Windows.

1. Open **PowerShell as Administrator** (Start menu → type *PowerShell* → right-click → *Run as administrator*).
2. Run:

   ```powershell
   wsl --install -d Ubuntu
   ```

3. Restart when asked. Ubuntu opens and asks you to choose a **username and password** (the password is invisible as you type - that is normal).
4. In the Ubuntu window, follow **Route D (apt)** below.
5. Keep the course folder **inside** the Linux file system (for example `~/phg-course`), not under `/mnt/c/...`; it is much faster and avoids permission problems.

If `wsl --install` is not recognised, update Windows, or use Route A (Codespaces).

{% endtab %}

{% tab title="C · macOS / Linux (conda)" %}

1. Install **Miniforge** (a minimal conda that uses the community `conda-forge` channel): follow the instructions at conda-forge.org/download (choose your operating system and chip).
2. Open a new terminal, then:

   ```bash
   git clone https://github.com/YOUR-ORG/YOUR-REPO.git phg-course
   cd phg-course
   mamba env create -f environment.yml      # use "conda" if "mamba" is not found
   conda activate phg
   bash scripts/check_setup.sh
   ```

3. Every time you open a new terminal for the course: `cd phg-course && conda activate phg`.

Apple-silicon Macs: some bioinformatics packages are only built for Intel; conda can run them through Rosetta. If a package fails to install, use Route A and tell us (open a *lab problem* issue).

{% endtab %}

{% tab title="D · Ubuntu / Debian (apt)" %}

These package names and versions are the ones the labs were tested with (Ubuntu 24.04):

```bash
sudo apt-get update
sudo apt-get install -y git r-base-core r-cran-ggplot2 r-cran-dplyr r-cran-readr \
    r-cran-tidyr r-cran-ape r-cran-data.table plink1.9 samtools bcftools tabix \
    bwa fastp fastqc seqtk python3-numpy
sudo ln -sf /usr/bin/plink1.9 /usr/local/bin/plink     # the course calls it "plink"

git clone https://github.com/YOUR-ORG/YOUR-REPO.git phg-course
cd phg-course
bash scripts/check_setup.sh
```

Tested versions: R 4.3.3, PLINK 1.90b7.2, samtools 1.19.2, bcftools 1.19, bwa 0.7.17, fastp 0.23.4, FastQC 0.12.1. Newer versions usually work; if a number in a lab differs slightly, the lab says how much variation is normal.

{% endtab %}

{% endtabs %}

## Check your setup

From the repository root:

```bash
bash scripts/check_setup.sh
```

Expected: every line shows `[ ok ]` and ends with `You are ready for Week 1.` If something fails, read the line: it names the missing tool. The data line compares every data file with `data/CHECKSUMS.sha256`; if it fails, regenerate the data with `python3 scripts/make_toy_data.py` (needs `numpy`).

## Common problems

| Symptom | Cause | Fix |
|---|---|---|
| `command not found: plink` | Ubuntu names it `plink1.9` | `sudo ln -sf /usr/bin/plink1.9 /usr/local/bin/plink` |
| `Permission denied` on a script | Missing execute bit | Run it with `bash script.sh` |
| `There is no package called 'ape'` | R package missing | `sudo apt-get install r-cran-ape` (apt) or `conda install r-ape` |
| WSL very slow | Working under `/mnt/c` | Move the folder into your Linux home (`~/`) |
| Codespace out of hours | Free allowance used | Wait for the monthly reset, or use Route B/C/D locally |
| Data checksum mismatch | A data file was edited | Re-run `python3 scripts/make_toy_data.py` |

## Optional but helpful

- A text editor with Markdown and R support (VS Code, RStudio/Posit Desktop).
- A GitHub account (for the contribution workflow and Codespaces).
- A notes file for your lab notebook.
- IQ-TREE 2 (`sudo apt-get install iqtree`, which provides `iqtree2`) for the optional maximum-likelihood tree in Week 10.
