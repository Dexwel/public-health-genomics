---
description: Tone, structure and the GitBook-safe Markdown syntax every page must follow.
---

# Style guide

## Voice

- **Plain and warm.** Write for a smart colleague who is new to this topic. Prefer "we" and "you".
- **Concept first, command second.** Explain *why* before *how*. A learner who understands the idea can recover from a failed command; one who only copied it cannot.
- **Define on first use.** Write the full term and the acronym once: "single-nucleotide polymorphism (SNP)".
- **Show uncertainty.** Say "usually", "in most studies", "as of 2026". Mark simplifications with **Simplification:**.
- **Be precise about people.** Use *ancestry* (genetic similarity to reference groups) or *geographic region* when that is what you mean. Do not use race as a biological category. Do not use "Caucasian". Avoid "normal" for genotypes; use "reference" or "common".
- **No medical advice.** Educational examples are not clinical guidance. Toy genes and variants in the data are synthetic.

## Page structure (week pages)

Every week page has front matter, one H1, an at-a-glance hint, and exactly seven tabs in this order:

`1 · Start here` · `2 · Concepts` · `3 · Conversation` · `4 · Hands-on lab` · `5 · Practice` · `6 · Go deeper` · `7 · Contribute`

`scripts/lint_course.py` enforces this. Use [week-template.md](week-template.md) as your starting point.

## Syntax that survives GitBook (and Git Sync)

GitBook reads standard Markdown plus a few block tags. Stick to this list.

````markdown
{% hint style="info" %}   <!-- info | warning | danger | success -->
A call-out. Leave blank lines inside if you add lists.
{% endhint %}

{% tabs %}

{% tab title="1 · Start here" %}

Content (any blocks: headings, code, tables, hints).

{% endtab %}

{% tab title="2 · Concepts" %}

More content.

{% endtab %}

{% endtabs %}

<details>

<summary>Show the answer</summary>

Hidden text, code, tables.

</details>
````

Rules:

1. Put a **blank line** after every opening tag and before every closing tag.
2. Do **not** nest tabs inside tabs.
3. Always give code fences a language (`bash`, `r`, `python`, `text`, `yaml`).
4. Use relative links between pages (`[Week 2](../weeks/week-02-linux.md)`) so they work on GitHub and on the site.
5. Tables must have a header row. Keep cells short; move long text below the table.
6. No raw HTML other than `<details>/<summary>`. No images are required; if you add one, store it under `assets/` (≤ 500 KB) and write alt text.
7. Do not rename a page after publication unless you also add a redirect in `.gitbook.yaml` (see the hosting guide).

## Labs

- All commands run **from the repository root**; write results to `results/weekNN/` (git-ignored).
- Every command was **run by the author**. Paste real output (trim long output with `...`).
- State tool versions in the page ("Version notes").
- Put checks of understanding in the lab: "**Stop and check:** you should see 2,724 mapped reads."
- Keep answer keys out of sight until the "check your answer" step; they live in `data/**/answers/`.

## Conversations

The *Conversation* tab uses three fictional recurring characters, so learners meet them week after week:

| Character | Role | Brings |
|---|---|---|
| **Zainab** | District health officer | The public-health question, scepticism, real constraints |
| **Tunde** | Laboratory scientist | Bench and bioinformatics realities |
| **Dr. Mensah** | Mentor | Socratic questions, gentle humour, correction without condescension |

Dialogues must teach (not summarise), include one honest mistake that gets corrected, and end with **three talking points** for the discussion forum.

## Citations and links

- Cite what you read. Prefer DOIs, official guideline pages and publisher pages.
- **Never invent** a paper, author, DOI or URL. If you cannot verify it, name the resource without a link or leave it out.
- Check each link opens. Prefer stable landing pages over deep links that move.
- Free-to-access resources first; flag paywalls.

## Accessibility

- Descriptive link text ("the ACMG/AMP guideline"), not "click here".
- Do not rely on colour alone to convey meaning in any plot you ask learners to make.
- Keep sentences short; expand abbreviations; avoid idioms that do not translate.
