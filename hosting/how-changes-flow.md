---
description: How GitHub, automatic checks and GitBook cooperate so that changes merge seamlessly and conflicts are rare.
---

# How changes flow (and how we avoid conflicts)

The goal is that a contributor's improvement becomes visible to learners **without anyone copying and pasting**, and that two people editing at once never silently overwrite each other.

## The life of a change

```
1  Contributor edits (web pencil, fork, or GitBook change request)
2  Pull request opened on GitHub                       ← all models converge here
3  GitHub Actions run: lint_course.py, data check, tool smoke test
4  GitBook posts a preview link on the pull request    (if previews are enabled)
5  CODEOWNERS reviewers are requested automatically
6  Reviewer approves; maintainer clicks "Squash and merge" into main
7  Git Sync imports the new commit into GitBook        → live site updates
```

## Choose one editing model

Pick **one** of these on day one. Mixing them without rules is the main source of trouble.

### Model A - GitHub-only editing (recommended)

- Everyone proposes changes through GitHub (issues, web editor, forks).
- GitBook is a **read-only mirror and publisher**: nobody edits pages or merges change requests inside GitBook.
- Branch protection can be strict (pull requests + reviews + checks) with no exceptions, because only humans via pull requests write to `main`.

Why recommended: one review pipeline, one history, and no risk that GitBook's commits bypass your checks.

### Model B - Hybrid (GitHub + GitBook editors)

- Experts who prefer a visual editor use GitBook **change requests** (GitBook's branches). A merged change request is committed to the synced branch with a message like `GITBOOK-14: <subject>`.
- Everyone else still uses GitHub.
- Requires: GitBook seats for those editors (see plans), and a **tested** way for GitBook's commits to land on a protected `main` (GitHub rulesets can allow a named app to bypass; GitBook's documentation we reviewed does not state how it behaves with required pull requests, so run a test commit before relying on it).
- Rules to prevent conflicts:
  1. **One page, one editor at a time.** Before editing a page in GitBook, check there is no open GitHub pull request touching it (search the PR list for the filename), and write "editing Week N in GitBook" in the Discussions thread.
  2. **Keep change requests short-lived** (hours, not weeks); merge or close them.
  3. **GitBook change request merges cannot be undone**; you fix mistakes with a new change request - or with a revert commit on GitHub.
  4. **Do not use GitBook-only features** that Markdown cannot represent (anything that is not in the [style guide](../contribute/style-guide.md)), or the files will gain unreviewable syntax.

## What "seamless" means in practice

| Concern | How it is handled |
|---|---|
| Two people edit the same file | GitHub shows a conflict in the pull request; the second contributor updates their branch (`git pull upstream main`) or resolves it in the browser. Small, one-topic pull requests make conflicts rare. |
| A change breaks the site | CI fails (unbalanced tabs, page missing from `SUMMARY.md`, broken link). The merge button stays disabled. |
| A change is wrong scientifically | CODEOWNERS routes the page to a subject-matter team; approval is required. |
| A bad change is merged | Revert the commit on GitHub (`Revert` button on the merged pull request); Git Sync republishes the previous text. |
| A page is renamed | Add a redirect in `.gitbook.yaml` in the same pull request. |
| Learners mid-course see content shift | Tag releases; for a cohort, share the tag's link (GitHub *Releases*) so their numbers never change mid-course. |
| A contributor is new to Git | Path 1 (issue) and Path 2 (pencil edit) in [How to contribute](../contribute/README.md). |

## If something goes wrong with sync

1. **Do not panic - the history is in GitHub.** The repository contains every previous version of every page.
2. Check the Git Sync panel in GitBook for the last sync status and error.
3. Confirm the GitBook GitHub app still has access to the repository (GitHub → Settings → Applications).
4. Confirm the synced **branch** still exists and matches the one chosen in Git Sync.
5. If GitBook content and GitHub diverge, decide which is right, then re-sync with the **direction** set to the correct source (reading GitBook's warning: the source replaces the destination).
6. Ask GitBook support; share your organisation URL.

## Security notes

- Keep the GitBook GitHub app limited to this one repository.
- Do not store secrets, tokens or personal data in the repository.
- Treat fork previews as a privilege (see [GitBook setup](gitbook-setup.md), Part G).
- Require two-factor authentication for the GitHub organisation (Settings → Authentication security).
