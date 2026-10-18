---
description: Step-by-step GitBook setup - account, site, Git Sync, publishing, custom domain and the free community plan.
---

# Step 3 to 6: Set up GitBook

Do [GitHub setup](github-setup.md) first. Everything here was checked against GitBook's public documentation (October 2026).

## Part A - Account and organisation

1. Go to **app.gitbook.com** and sign up (signing in *with GitHub* is the easiest, because you will connect GitHub anyway).
2. Create an **organisation** when asked (for example "Public Health Genomics Course"). Organisations own sites and decide who can edit.

## Part B - Create the site

GitBook calls the published book a **site**; the editable content lives in a **space** (a section of the site).

1. From your organisation **Home**, click the **+** next to **Sites**.
2. Enter a name visitors will recognise (for example *Public Health Genomics*) and click **Create**.
3. When asked for a starting point, choose **Git Sync** (the options also include templates, imports and a blank section).

{% hint style="info" %}
If you picked a blank section by mistake you can connect Git Sync later: on a space, click **Set up** next to **Git Sync** in the space header and choose **GitHub Sync**.
{% endhint %}

## Part C - Connect GitHub with Git Sync

Only organisation **administrators and creators** can enable Git Sync.

1. Open **Git Sync** from the site sidebar (or the space header, as above) and choose **GitHub Sync**.
2. **Connect GitHub.** Authorise your GitHub account, then **install the GitBook GitHub app** on the account or organisation that owns the repository. Grant it access to **only the course repository**.
   - If you see **"Potential duplicated accounts"**, the GitHub account is already linked to another GitBook user. Log out, sign in with GitHub, and follow GitBook's troubleshooting page.
   - GitHub Enterprise Server instances are not supported; github.com is.
3. Under **Source repository**, select the repository and the **branch** to sync: `main`.
4. **Choose the initial sync direction - this is the step people get wrong.**
   - The default is **GitBook → GitHub** (GitBook's content is the source of truth).
   - Because the course already lives on GitHub, click **Swap direction** so it reads **GitHub → GitBook**.
   - **Warning from GitBook:** the direction you choose replaces the destination. If you accidentally sync an empty GitBook space *to* GitHub, or an empty repository *to* GitBook, you can overwrite real content. Double-check the repository, branch and direction before clicking Sync.
5. **Project directory:** leave empty (the course is at the repository root).
6. **Content mapping:** map the space to `./` (the repository root; the configuration file `.gitbook.yaml` tells GitBook where to read).
7. **Advanced options (optional):**
   - *Commit message template* - GitBook's default produces messages like `GITBOOK-14: Improve documentation about users management`. You can customise it with the placeholders `{change_request_number}` and `{change_request_subject}`.
   - *Fork previews* - see "Pull-request previews" below. Leave **off** unless you have read the security note.
8. Click **Sync**. The pages should appear in GitBook within a minute or two, in the order set by `SUMMARY.md`.

### What `.gitbook.yaml` and `SUMMARY.md` do

The course already includes them.

`.gitbook.yaml` (repository root):

```yaml
root: ./

structure:
  readme: README.md
  summary: SUMMARY.md
```

| Option | Meaning |
|---|---|
| `root` | The folder GitBook reads (default `./`). All other paths are relative to it. |
| `structure.readme` | The landing page. |
| `structure.summary` | The file that defines the sidebar. |
| `redirects` | (Optional) maps an old path to a new one, so renamed pages do not break old links. |

If you ever rename `weeks/week-08-gwas.md`, add:

```yaml
redirects:
  weeks/week-08-gwas-old-name: weeks/week-08-gwas.md
```

`SUMMARY.md` rules (from GitBook's documentation): `##` headings group pages; top-level bullet links are pages; indented bullets are child pages; each file may appear **once**; a quoted title after the path sets a different sidebar label. If a page is missing from `SUMMARY.md` it will not be in the navigation - `scripts/lint_course.py` warns you.

### Check the import

Open **Week 2 · Linux** on the site. You should see **seven tabs** across the top of the content. If you see raw `{% tab %}` text instead, the file did not sync as GitBook-flavoured Markdown: confirm the branch is `main` and run `python scripts/lint_course.py` locally.

## Part D - Publish

1. Open the site from your organisation **Home**.
2. Click **Preview** in the site header to check how it looks.
3. Click **Publish** in the site header.
4. Visibility: sites are **Public** by default. You can review it under **Settings → Audience** (other options: private share links, and sign-in protected "Authenticated Access" - not what we want for an open course).

GitBook gives the published site a default address on its own domain; the exact form is shown after publishing - copy it into the repository `README.md` and the repository description.

## Part E - (Optional) Use your own domain

For example `genomics.yourorganisation.org`.

1. Choose a **subdomain** (`learn.`, `genomics.`, `www.`).
2. In the site **Settings**, click **Set up a custom domain**, enter the domain and click **Next**.
3. GitBook shows a **CNAME record** with a *Type*, *Name* and *Target*. In your domain registrar's DNS settings, add it exactly. Use a **CNAME**, not an A record.
4. Wait **at least one hour** before pressing **Next** (propagation can take up to 48 hours).
5. GitBook verifies the record, issues the **SSL certificate** automatically, and notifies you. Click **Finish**.

Custom domains are not part of every plan; check the plan you are on (see Part F).

## Part F - Get the right plan (free options)

Plan names, limits and eligibility change. As of October 2026, GitBook's public documentation says:

| Plan | What it gives | Good for |
|---|---|---|
| **Free** | One user; GitBook editor; Git Sync with GitHub/GitLab; preview deployments | Starting alone, or when every collaborator works through GitHub |
| **Community** | Free for eligible **non-profit, open-source and education-related groups**; includes all features of the top (Ultimate) plan except SAML single sign-on | A multi-person team with GitBook editors, custom domain and branding |
| **Sponsored site** (for open-source projects on the Community plan) | Premium site features (such as custom domain and branding) at no cost, in exchange for one small, privacy-respecting ad per page, which can earn the project money | Open-source courses that accept a small ad |

**Eligibility highlights for Community:**

- *Open source:* a **public** GitHub/GitLab repository, not tied to a for-profit or venture-backed company, with `README.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` and a valid open-source `LICENSE` - this repository includes all four.
- *Education:* whole schools and universities do not qualify, but **small course, lab or student groups** can; each member needs a GitBook account created with an institutional email and an invitation to the organisation.
- *Non-profits:* official non-profit status (for example 501(c) or equivalent) and documentation.

**How to apply** (from GitBook's documentation):

1. Sign in to GitBook and choose or create the organisation.
2. Copy the organisation URL (it looks like `app.gitbook.com/o/<string>/home`).
3. Contact GitBook through the website contact form (*Contact Support → pricing question → apply to Community plan*) or email **support@gitbook.com**, including: the project's purpose, the public repository link and the organisation link (and for non-profits, your public website and registration documents).

**Sponsored site plan**: publish the site publicly, wait seven days, then go to site settings → **Ads and sponsorship**, review the checklist and submit; review takes about a week. Projects are rejected for being not open-source / not-for-profit, crypto-related, written primarily in a language other than English, low-quality content, or not reaching a minimum number of page views. If you do not submit within a month the site reverts to the free plan and premium features switch off.

{% hint style="warning" %}
Read GitBook's current **plans** and **pricing** pages before relying on any of this; the plan descriptions above summarise documentation that GitBook may update.
{% endhint %}

## Part G - Pull-request previews (very useful for reviewers)

GitBook can build a preview of your documentation for each GitHub pull request, so reviewers see the real tabs and layout before merging.

- Requirement: give the **GitBook GitHub app read-only permission for pull requests** (the app asks during installation). Each pull request then gets a status check with a **Details** link to a unique preview.
- The site must be **published**, and not behind authenticated access.
- Preview links are only accessible to people who have a GitBook account.
- **Pull requests from forks do not get previews by default.** GitBook explains why: previews are served under *your* domain, so a malicious fork of a public repository could publish unwanted content there. You can enable **fork previews** in the Git Sync settings. If you enable it, restrict who can approve workflow runs and always read what a fork changes before opening its preview link.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Site is blank after first sync | Direction was GitBook → GitHub with an empty space | Check the repository still has its files (look at the commit history); fix direction (GitHub → GitBook) and sync again |
| Raw `{% tabs %}` text shown | File not parsed as GitBook Markdown, or tag typo | Run the linter; confirm the file is listed in `SUMMARY.md` |
| A page is missing from the sidebar | Not listed in `SUMMARY.md` | Add it (once) and merge |
| Sync stopped | GitHub app uninstalled or lost access, or the branch was renamed/deleted | Reinstall the app for the repository; reselect the branch in Git Sync settings |
| GitBook says it cannot push | Branch protection blocks the GitBook app | See "Model A / Model B" in [How changes flow](how-changes-flow.md) |
| Custom domain stuck on "pending" | CNAME not yet propagated or wrong target | Re-copy the record, wait, check with an online DNS lookup tool |
| Renamed page gives 404 | Old URL not redirected | Add a `redirects:` entry in `.gitbook.yaml` |
