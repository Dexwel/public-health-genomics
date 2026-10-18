---
description: Copy this file to start a new week page; it already passes the structure checks.
---

# Week template

Copy the block below into `weeks/week-NN-short-name.md`, replace the placeholders, then add the page to `SUMMARY.md`.

````markdown
---
description: One sentence saying what a learner will be able to do after this week.
---

# Week NN — Title

{% hint style="info" %}
**At a glance** · **Time:** ~6-8 h (2 h concepts, 3-4 h lab, 1-2 h practice) · **Prerequisites:** Week N-1 · **You will produce:** a one-line description · **Tools:** list
{% endhint %}

{% tabs %}

{% tab title="1 · Start here" %}

## Why this matters
(One real-world hook.)

## Learning objectives
By the end of this week you will be able to:
1. ...

## Roadmap
| Step | Time | Tab |
|---|---|---|
| Read the concepts | 2 h | 2 · Concepts |

## Key terms
| Term | Meaning |
|---|---|

## Pre-check
(3-5 questions with answers in `<details>`.)

{% endtab %}

{% tab title="2 · Concepts" %}

(Lecture-quality notes. Worked examples. Misconceptions. "Public health lens" call-outs.)

{% endtab %}

{% tab title="3 · Conversation" %}

**Zainab:** ...

**Tunde:** ...

**Dr. Mensah:** ...

### Talking points for the forum
1. ...

{% endtab %}

{% tab title="4 · Hands-on lab" %}

(Numbered steps. Commands. "What you should see". Stop-and-check. Troubleshooting table. Stretch challenge.)

{% endtab %}

{% tab title="5 · Practice" %}

(6-10 exercises with answers in `<details>`; 8-question self-test; a reflection prompt; a portfolio mini-deliverable.)

{% endtab %}

{% tab title="6 · Go deeper" %}

(Annotated, verified resources: core reading, courses, tool docs, datasets, guidelines, Africa-focused resources.)

{% endtab %}

{% tab title="7 · Contribute" %}

(Week-specific ideas for experts; label `week-NN`; version notes; pointer to `../contribute/README.md`.)

{% endtab %}

{% endtabs %}
````

After saving, run `python scripts/lint_course.py`.
