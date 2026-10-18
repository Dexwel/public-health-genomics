---
description: A launch plan, a pilot-cohort plan, and a routine that keeps the course trustworthy over time.
---

# Launch and maintenance

## Before you announce

- [ ] All 12 weeks present; `python scripts/lint_course.py` passes.
- [ ] A **pilot** learner (not the author) completed Weeks 1-3 on a fresh computer or in a Codespace using only the page instructions. Fix everything they stumbled on.
- [ ] `bash scripts/check_setup.sh` passes on Linux/WSL, macOS and Codespaces.
- [ ] Placeholders removed (`YOUR-ORG`, `YOUR-REPO`, `<your-org>`).
- [ ] Repository public, with README, CONTRIBUTING, CODE_OF_CONDUCT, LICENSE.
- [ ] GitBook site published; Week 2 shows seven tabs; links in `README.md` point to the live site.
- [ ] At least two maintainers with admin rights on GitHub **and** GitBook.
- [ ] Reviewer teams exist with at least one named person each (even if the same people overlap).
- [ ] Release `v1.0` tagged.

## Suggested rollout

| Phase | Duration | Goal |
|---|---|---|
| **Alpha** | 2 weeks | 3-5 friendly learners and reviewers; collect issues; fix labs |
| **Pilot cohort** | 12 weeks | 15-30 learners with weekly live sessions; gather feedback; recruit reviewers from the best contributors |
| **Open launch** | ongoing | Announce on professional networks, mailing lists, and to partner institutions |

## Running a cohort (optional)

- **Weekly rhythm:** Monday release of the week; mid-week live help session (45 min) around the lab; Friday discussion thread on the three *talking points*.
- **Assessment:** the Practice tab self-tests (formative), the capstone (summative) and a structured peer review.
- **Roles:** facilitator, a "lab buddy" per five learners, and a subject-matter reviewer on call.
- **Pin the cohort** to a release tag so numbers do not change under their feet.

## Growing the reviewer community

1. Add a standing **"Help wanted"** issue per week listing the contribution ideas from each week's *7 · Contribute* tab.
2. Thank publicly; credit in `CONTRIBUTORS.md` and on the page.
3. Offer a clear ladder: contributor → reviewer for a week → theme lead → maintainer.
4. Invite subject experts for a **single-week review sprint** (two hours) rather than open-ended commitment.
5. Report impact (visits, completions, contributions) back to contributors every quarter.

## Metrics that matter

| Metric | Why |
|---|---|
| Learners who finish Week 3 (the Linux + R hurdle) | Reveals onboarding problems |
| Median time from issue to fix | Reviewer capacity |
| Share of contributions from outside the founding team | Community health |
| Number of languages / local case studies added | Relevance beyond the founders |
| Lab failure reports per week | Reproducibility |

## Maintenance calendar

| When | Task |
|---|---|
| Weekly | Triage; merge approved pull requests |
| Monthly | Re-run `scripts/check_setup.sh` on a fresh Codespace; review open `lab-bug` issues |
| Quarterly | Health check in the [maintainer handbook](../contribute/maintainers.md) (tools, links, guidelines) |
| Yearly | Review the syllabus against the field: new guidelines, tools and resources; retire what is obsolete; tag a major release |

## Backing up and leaving GitBook (portability)

Because every page is plain Markdown in GitHub, the course is never trapped: GitHub renders the pages (tabs appear as plain tag text), and the content can be built with other documentation generators if you ever need to. Keep the repository the source of truth and you keep control.
