---
description: How anyone can suggest, write and merge improvements to this course - with or without Git.
---

# How to contribute

This course is a **starting point**. Its value grows as experts add local case studies, corrections, translations, new exercises and fresh tool versions. This page explains how a change travels from your idea to the live site, and how we keep that journey smooth for you and safe for learners.

{% hint style="success" %}
**You do not need to know Git to help.** The first path below takes two minutes and needs only a free GitHub account.
{% endhint %}

## The big picture

```
 You suggest or edit ──► GitHub (source of truth) ──► automatic checks ──► expert review ──► merge ──► GitBook publishes
        │                      ▲                                                                       │
        └── 3 paths below      └────────── edits made inside GitBook are committed back ◄──────────────┘
```

Three ideas keep this seamless:

1. **One source of truth.** Every page is a plain Markdown file in one GitHub repository. GitBook mirrors it using *Git Sync*, so a merge on GitHub appears on the published site automatically, and nobody has to copy and paste between systems.
2. **Robots check the boring things.** Every proposed change is run through `scripts/lint_course.py` and the data/tool checks in `.github/workflows/checks.yml`. Broken tabs, missing pages and dead links are caught before a human spends time.
3. **Humans check the science.** `.github/CODEOWNERS` automatically asks the right subject-matter reviewers (for example the pathogen-genomics reviewers for Week 10). Nothing reaches learners without at least one approval.

## Choose your path

| Path | Best for | Skills needed | Time |
|---|---|---|---|
| **1. Open an issue** | Spotted a typo, an error, an outdated link, or have an idea | A GitHub account | 2 min |
| **2. Edit on GitHub** | Fixing wording, adding a resource, a small exercise | A GitHub account; Markdown basics | 10-30 min |
| **3. Fork and pull request** | New sections, new datasets, scripts, translations | Git; Markdown; a local setup | 1 h+ |
| **4. GitBook change request** | Invited reviewers and editors who prefer a visual editor | An invitation to the GitBook organisation | 10-30 min |

### Path 1 - Open an issue (no editing)

1. Go to the repository's **Issues** tab and choose **New issue**.
2. Pick a form: *Suggest a change to a lesson*, *A lab command did not work* or *Propose a resource, case study or dataset*.
3. Say which week and tab, what is wrong or missing, and (for factual corrections) give a source.

A maintainer triages it within a week, labels it (`week-08`, `lab-bug`, `needs-expert`) and either fixes it or invites you to.

### Path 2 - Edit on GitHub (no installs)

1. Open the page's file on GitHub (for example `weeks/week-08-gwas.md`) and click the **pencil icon** (*Edit this file*).
2. GitHub creates your personal copy (a *fork*) automatically if you cannot write to the repository directly.
3. Make your change. Keep to the [style guide](style-guide.md).
4. Click **Commit changes...**, choose *Create a new branch for this commit and start a pull request*, and write a one-line summary.
5. In the pull request form, tick the checklist. The checks run by themselves; a green tick means the structure is sound.
6. A reviewer will comment or approve. Answer comments by pushing more edits to the same branch, or ask for help.

### Path 3 - Fork and pull request (full control)

```bash
# one time
git clone https://github.com/<you>/<repo>.git        # your fork
cd <repo>
git remote add upstream https://github.com/<org>/<repo>.git

# for each change
git switch main && git pull upstream main            # start from the latest course
git switch -c week08-fix-lambda-wording              # one topic per branch
# ... edit files, then check your work:
python scripts/lint_course.py
bash scripts/check_setup.sh                          # if you touched labs, run them too
git add -p                                           # review what you are adding
git commit -m "Week 8: clarify lambda GC wording"
git push -u origin week08-fix-lambda-wording
# open the pull request on GitHub
```

Branch names: `week08-short-description`, `data-...`, `docs-...`, `translate-fr-week01`.

If a commit would change data, regenerate and commit `data/CHECKSUMS.sha256` (see [data policy](data-policy.md)).

### Path 4 - GitBook change requests

If you were invited to the GitBook organisation as an editor, you can click **Edit** on any page, which opens a *change request* (GitBook's version of a branch). Edit visually, request review, and a maintainer merges it. With Git Sync enabled, a merged change request is committed to GitHub with a message like `GITBOOK-14: Improve the Week 3 cleaning example`. See [How changes flow](../hosting/how-changes-flow.md) for the rules that stop the two systems from fighting each other.

{% hint style="info" %}
GitBook seats for editors are limited by the organisation's plan. That is why Paths 1-3 (GitHub) are the default for everyone, and Path 4 is for a small group of regular reviewers.
{% endhint %}

## What happens to your pull request

| Step | Who | What | Typical time |
|---|---|---|---|
| 1. Automatic checks | GitHub Actions | Page structure, tabs, links, front matter, data checksums, tool smoke test | 2-5 min |
| 2. Preview | GitBook (if enabled) | A preview link for the pull request so reviewers see the real page | automatic |
| 3. Triage | Maintainer | Labels, assigns reviewers, may ask you to split a big change | ≤ 7 days |
| 4. Expert review | CODEOWNERS reviewers | Accuracy, tone, inclusivity, "did you run the command?" | ≤ 14 days |
| 5. Merge | Maintainer | *Squash and merge* with a clear title | same day as approval |
| 6. Publish | GitBook Git Sync | The site updates from `main` | minutes |

## Review standards (what reviewers look for)

1. **Correct.** Facts match a cited guideline, paper or official documentation. No invented references.
2. **Reproducible.** Commands were run by the contributor and the printed output is real. Version numbers are stated.
3. **Inclusive.** Examples reflect the global audience, avoid stereotypes, and use ancestry/race language carefully (see the style guide).
4. **Safe.** No real patient data. No clinical advice presented as such. Toy variants are never framed as real genes.
5. **Teachable.** Concepts come before commands. New terms are defined. Jargon is explained.
6. **Small.** One idea per pull request is easiest to review and fastest to merge.

## Recognition

Everyone who contributes is credited in [CONTRIBUTORS](CONTRIBUTORS.md), and substantial contributors of a section are listed as *contributing authors* on the page they improved (add a line under the title: `Contributing author: Name, Institution`). Contributions are licensed as described in [LICENSE](../LICENSE.md).

## Where to go next

- [Style guide](style-guide.md) - tone, structure, syntax that survives GitBook.
- [Week page template](week-template.md) - copy this to start or restructure a week.
- [Data policy](data-policy.md) - what data may and may not be added.
- [Maintainer handbook](maintainers.md) - triage, review, merge and release routines.
- [Code of conduct](../CODE_OF_CONDUCT.md) - how we treat each other.
