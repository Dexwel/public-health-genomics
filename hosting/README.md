---
description: The complete path from this folder on your computer to a public, community-maintained GitBook site.
---

# Hosting the course on GitBook

This section takes you from the files you downloaded to a live site that your community can improve. It is written for someone who has **never used GitHub or GitBook**. Allow **about 90 minutes** the first time (plus waiting for DNS if you use your own domain).

## The architecture in one picture

```
 ┌────────────────────┐   pull requests    ┌─────────────────────┐   Git Sync   ┌───────────────────┐
 │ Contributors       │ ─────────────────► │ GitHub repository   │ ◄──────────► │ GitBook site      │
 │ (issues, PRs, web  │                    │ (source of truth)   │              │ (the pretty,      │
 │  editor)           │ ◄───── review ──── │ + automatic checks  │              │  searchable book) │
 └────────────────────┘                    └─────────────────────┘              └───────────────────┘
```

- **GitHub** stores every page as a Markdown file with full history, runs the automatic checks, and is where people propose changes.
- **GitBook** turns those files into a navigable, searchable website with tabs, hints and a table of contents.
- **Git Sync** is GitBook's built-in two-way link between them. A change merged on GitHub appears on the site; a change request merged in GitBook is committed to GitHub.

## Checklist

Follow these in order. Each links to a detailed page.

| # | Step | Where | Time |
|---|---|---|---|
| 1 | Create the GitHub repository and upload the course | [GitHub setup](github-setup.md), part A | 15 min |
| 2 | Protect `main`, turn on checks, assign reviewers | [GitHub setup](github-setup.md), parts B-D | 20 min |
| 3 | Create a GitBook account, organisation and site | [GitBook setup](gitbook-setup.md), parts A-B | 10 min |
| 4 | Connect the repository with Git Sync | [GitBook setup](gitbook-setup.md), part C | 10 min |
| 5 | Publish, check, (optionally) add a custom domain | [GitBook setup](gitbook-setup.md), parts D-E | 15 min + DNS |
| 6 | Apply for the free community or open-source plan | [GitBook setup](gitbook-setup.md), part F | 10 min |
| 7 | Learn the rules that keep the two systems in sync | [How changes flow](how-changes-flow.md) | 15 min |
| 8 | Announce, invite reviewers, run a pilot cohort | [Launch and maintenance](launch-and-maintenance.md) | ongoing |

{% hint style="warning" %}
**Plans, limits and screen labels change.** The steps below were checked against GitBook's public documentation in October 2026. If a button is named differently when you get there, search GitBook's documentation for the same feature name (*Git Sync*, *change requests*, *custom domain*) rather than guessing. Pricing and eligibility rules are on GitBook's pricing and plans pages; read them before you rely on a free tier.
{% endhint %}

## Why this design (and what we deliberately avoided)

| Decision | Reason |
|---|---|
| **GitHub is the source of truth** | Experts already have GitHub accounts, reviews and history are built in, and CI can check every change. GitBook seats are limited by plan; GitHub contributors are free and unlimited. |
| **Plain Markdown + a few GitBook tags** | The content is portable. If you ever leave GitBook, the repository still renders on GitHub and can be built with other tools. |
| **Automatic checks before humans look** | Reviewers' time is the scarcest resource. Robots catch broken tabs and dead links. |
| **CODEOWNERS** | Routes each week to the right experts without anyone remembering who to ask. |
| **Synthetic, reproducible data** | No privacy risk, no big files, and every lab number can be verified by anyone. |
