---
description: The routines maintainers follow - triage, review, merge, release and keeping content fresh.
---

# Maintainer handbook

## Roles

| Role | Can | Typical people |
|---|---|---|
| **Maintainer** | Triage, merge, change CI/data/structure, manage access | 2-3 course leads (never just one - avoid a single point of failure) |
| **Reviewer** | Approve changes in their theme (CODEOWNERS) | Subject-matter experts: a bioinformatician, a clinical geneticist, an epidemiologist, an ethicist |
| **Contributor** | Open issues and pull requests | Anyone |

Aim for **two reviewers per theme** so leave and travel do not stall the queue.

## Weekly routine (30 minutes)

1. **Triage new issues:** add labels `week-NN`, `lab-bug` / `suggestion` / `resource`, and `needs-expert` if a reviewer is required. Remove `needs-triage`.
2. **Nudge reviews** older than 7 days (ask the CODEOWNERS team, or reassign).
3. **Merge approved pull requests** (see below).
4. Skim GitHub Discussions for questions that reveal a confusing explanation - turn them into issues.

## Merging a pull request

Merge only when **all** are true:

- [ ] Checks are green (structure, data, tool smoke test).
- [ ] At least one approval from a CODEOWNER of every changed path (two for data or script changes).
- [ ] Claims and numbers are supported; commands were run; no invented references.
- [ ] No real data; no files over 5 MB.
- [ ] The PR title is a clear sentence: *"Week 8: explain PI_HAT inflation under population structure"*.

Use **Squash and merge** so `main` has one readable commit per contribution. Thank the contributor in the comment, and add them to `CONTRIBUTORS.md` if they have not been listed.

## Keeping the two systems in sync

Read [How changes flow](../hosting/how-changes-flow.md). The short version:

- GitHub `main` is the source of truth.
- Merging to `main` publishes the site (Git Sync).
- Never edit the same page in GitBook and GitHub at the same time; if a change request is open in GitBook for a page, tell contributors before merging a PR for the same page.

## Releases

Tag a release (`v1.0`, `v1.1`...) when something learners will notice has changed: a new week, a changed dataset, or a tool upgrade. Release notes list the pages changed and *whether learners mid-course need to re-download the data*. For cohort-based teaching, freeze a copy per cohort (a tag) so numbers stay stable while the course continues to improve.

## Quarterly health check

| Task | How |
|---|---|
| Tool versions | Run labs on the latest apt/conda versions; update "Version notes" if outputs change |
| Links | Open every link in the *Go deeper* tabs (or use a link checker); fix or remove dead ones |
| Guidelines | Check for updates to ACMG/AMP, WHO, Wilson-Jungner-derived criteria and data-protection laws cited in Weeks 7, 9, 10 and 11 |
| Accessibility and language | Ask a new learner to read one week and report confusing passages |
| Access | Remove inactive reviewers; confirm at least two maintainers have admin |

## Handling difficult situations

- **A contributor disagrees with a reviewer:** invite a second expert; decide on evidence, not seniority.
- **Possible personal data in a PR:** do not merge. Ask the contributor to remove it, and if it was pushed, contact a maintainer immediately - the data must be purged from history, not merely deleted.
- **Content disputes (sensitive topics):** the Code of Conduct applies; maintainers may close threads.
