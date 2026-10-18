---
description: Create the GitHub repository, protect the main branch, switch on checks and reviewers.
---

# Step 1 and 2: Set up GitHub

You need a free GitHub account (github.com). If your team will own the course, create a **GitHub organisation** first (profile menu → *Your organizations* → *New organization*, Free plan) so ownership does not depend on one person's account.

## Part A - Create the repository and upload the course

1. Click **+** (top right) → **New repository**.
2. **Owner:** your organisation (or your account). **Repository name:** for example `public-health-genomics-course`.
3. **Visibility: Public.** (GitBook's open-source and community plans require a public repository, and a public repository lets anyone propose changes.)
4. Leave *Add a README* **unticked** (the course already has one). Click **Create repository**.
5. Put the course in it. Pick one:

{% tabs %}

{% tab title="Command line (recommended)" %}

From the folder that contains `README.md` and `SUMMARY.md`:

```bash
git init -b main
git add .
git commit -m "Initial import of the Public Health Genomics course"
git remote add origin https://github.com/<your-org>/<repo>.git
git push -u origin main
```

Check on GitHub that you see `README.md`, `SUMMARY.md`, `weeks/`, `data/`, and so on.

{% endtab %}

{% tab title="Browser only" %}

1. On the new empty repository page, click **uploading an existing file**.
2. Unzip the course on your computer and drag **the contents** of the folder (not the folder itself) into the page. GitHub's web uploader accepts up to 100 files at a time, so upload in batches (`.github`, `contribute`, `data`, `hosting`, `scripts`, `start-here`, `weeks`, and the top-level files).
3. Write a commit message and click **Commit changes**.

Hidden folders such as `.github` may not appear in your file picker; enable "show hidden files" in your operating system, or use the command-line method.

{% endtab %}

{% endtabs %}

6. Replace the placeholders `YOUR-ORG/YOUR-REPO` in `README.md`, `contribute/` and `.github/` with your real names (use search: *Go to file* → `/` or the repository's search for the text `YOUR-ORG`).
7. Turn on **Discussions** (Settings → General → Features → Discussions). Learners ask questions there instead of in Issues.

## Part B - Protect the `main` branch with a ruleset

A *ruleset* stops anyone (including you by accident) from pushing unreviewed changes to the live course.

1. **Settings → Rules → Rulesets → New ruleset → New branch ruleset.**
2. Name: `Protect main`. Enforcement status: **Active**.
3. **Target branches:** *Add target* → *Include default branch*.
4. Tick:
   - **Require a pull request before merging** → *Required approvals: 1*; tick **Require review from Code Owners**; tick **Dismiss stale pull request approvals when new commits are pushed**.
   - **Require status checks to pass** → add the checks `Structure and links`, `Toy data reproduces`, `Smoke-test the tools`. (They appear in the list after the workflow has run once; open a trivial pull request first to make them appear.)
   - **Block force pushes** and **Restrict deletions**.
5. Click **Create**.

{% hint style="warning" %}
**Git Sync interaction (read this before turning on required reviews).** When GitBook commits to your synced branch (for example when a change request is merged inside GitBook), it needs permission to push. If `main` requires pull requests, those pushes may be refused unless the GitBook app is allowed to bypass the rule. GitBook's documentation we reviewed does not describe this case, so test it (see [How changes flow](how-changes-flow.md), "Choose one editing model") before you invite GitBook editors. The simplest, most robust setup is **Model A: GitHub-only editing**, where nobody merges change requests in GitBook.
{% endhint %}

## Part C - Reviewers with CODEOWNERS

`.github/CODEOWNERS` already maps each week to a reviewer team.

1. Create teams in your organisation (**Teams → New team**): `phg-maintainers`, `phg-reviewers-foundations`, `phg-reviewers-computing`, `phg-reviewers-genetics`, `phg-reviewers-sequencing`, `phg-reviewers-clinical-genomics`, `phg-reviewers-statistical-genetics`, `phg-reviewers-pathogen-genomics`, `phg-reviewers-ethics-policy`.
2. Give each team **Write** access (Settings → Collaborators and teams).
3. Edit `.github/CODEOWNERS`: replace `@YOUR-ORG` with your organisation's name.
4. Start small: if you only have three experts, put each in several teams. You can split later.

{% hint style="info" %}
CODEOWNERS only works for **teams or users with write access**. If you work on a personal account (no organisation), list individual `@usernames` instead of teams.
{% endhint %}

## Part D - Make contributing easy

- **Issue forms** (`.github/ISSUE_TEMPLATE/`) are ready. Open *Issues → New issue* to confirm the three forms appear. In `config.yml` replace the Discussions URL.
- **Labels:** create `week-01` ... `week-12`, `lab-bug`, `suggestion`, `resource`, `needs-expert`, `needs-triage`, `good first issue`, `translation`. (Issues → Labels → New label.)
- **Pull-request template** is in `.github/pull_request_template.md` (nothing to do).
- **Repository description and topics** (cog next to *About*): "Open 12-week Public Health Genomics course (Linux, R, genomics) - contributions welcome", topics `genomics`, `public-health`, `education`, `gitbook`, `open-science`.
- **Pinned issue:** open an issue called *Start here: how to help* linking to `contribute/README.md` and pin it.

## Part E - Verify with a test pull request

1. On GitHub open `contribute/CONTRIBUTORS.md`, click the pencil, add a line, and choose *Create a new branch and start a pull request*.
2. Watch the **Checks** tab: the three checks should turn green.
3. Confirm the right reviewers were requested automatically (right side of the pull request).
4. Approve and **Squash and merge**. Delete the branch.

If a check fails, open it and read the message; `scripts/lint_course.py` prints the file and line.
