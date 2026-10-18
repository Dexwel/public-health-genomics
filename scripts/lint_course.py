#!/usr/bin/env python3
"""
lint_course.py - structural checks that keep the GitBook site from breaking.

Run from the repository root:   python scripts/lint_course.py
Exit code 0 = all good, 1 = problems found (CI fails the pull request).

Checks
  1. SUMMARY.md: every linked file exists; every book page is listed exactly once.
  2. GitBook blocks: {% tabs %}/{% endtabs %}, {% tab %}/{% endtab %}, {% hint %}/{% endhint %},
     <details>/</details> are balanced and not nested wrongly.
  3. Week pages: front matter with `description:`, one H1, and the 7 required tabs in order.
  4. Relative Markdown links resolve to real files (anchors are not checked).
  5. Fenced code blocks are closed.
  6. Hygiene: no tabs-for-indent in code fences? (skipped) / no merge-conflict markers / no files > 5 MB.
Only the Python standard library is used.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK_DIRS = ["start-here", "weeks", "contribute", "hosting", "showcase"]
BOOK_TOP_FILES = ["README.md"]
EXTRA_BOOK_FILES = ["data/README.md"]  # pages outside the usual folders that are part of the book
NOT_PAGES = {"CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "LICENSE.md", "SUMMARY.md"}
WEEK_TABS = ["1 · Start here", "2 · Concepts", "3 · Conversation", "4 · Hands-on lab",
             "5 · Practice", "6 · Go deeper", "7 · Contribute"]

errors: list[str] = []
warnings: list[str] = []


def err(path: Path, msg: str, line: int | None = None) -> None:
    loc = f"{path.relative_to(ROOT)}" + (f":{line}" if line else "")
    errors.append(f"{loc}: {msg}")


def book_pages() -> list[Path]:
    pages = [ROOT / f for f in BOOK_TOP_FILES if (ROOT / f).exists()]
    for d in BOOK_DIRS:
        if (ROOT / d).is_dir():
            pages += sorted(p for p in (ROOT / d).rglob("*.md"))
    pages += [ROOT / f for f in EXTRA_BOOK_FILES if (ROOT / f).exists()]
    return [p for p in pages if p.name not in NOT_PAGES or p.name == "README.md"]


def strip_code(text: str) -> str:
    """Blank out fenced code and inline code so we do not lint examples."""
    out, fence = [], None
    for line in text.split("\n"):
        m = re.match(r"^\s*(`{3,}|~{3,})", line)
        if m:
            tok = m.group(1)[0] * 3
            if fence is None:
                fence = tok
            elif line.strip().startswith(fence):
                fence = None
            out.append("")
            continue
        out.append("" if fence else re.sub(r"`[^`\n]*`", "``", line))
    return "\n".join(out)


def check_summary() -> set[Path]:
    summary = ROOT / "SUMMARY.md"
    if not summary.exists():
        err(summary, "SUMMARY.md is missing")
        return set()
    linked: dict[Path, int] = {}
    for n, line in enumerate(summary.read_text(encoding="utf-8").split("\n"), 1):
        for m in re.finditer(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", line):
            target = m.group(1)
            if re.match(r"^[a-z]+://", target):
                continue
            p = (ROOT / target.split("#")[0]).resolve()
            if not p.exists():
                err(summary, f"links to missing file '{target}'", n)
            linked[p] = linked.get(p, 0) + 1
    for p, count in linked.items():
        if count > 1:
            err(summary, f"'{p.relative_to(ROOT)}' is listed {count} times (GitBook allows a file once)")
    pages = {p.resolve() for p in book_pages()}
    for p in sorted(pages - set(linked)):
        err(summary, f"page '{p.relative_to(ROOT)}' is not listed in SUMMARY.md (it would be missing from the site)")
    return set(linked)


def check_blocks(path: Path, text: str) -> None:
    body = strip_code(text)
    stack: list[tuple[str, int]] = []
    pairs = {"endtabs": "tabs", "endtab": "tab", "endhint": "hint"}
    for n, line in enumerate(body.split("\n"), 1):
        for m in re.finditer(r"\{%\s*(\w+)([^%]*)%\}", line):
            name = m.group(1)
            if name in ("tabs", "tab", "hint", "stepper", "step", "columns", "column", "updates", "embed", "file", "include"):
                if name in ("embed", "file", "include"):
                    continue
                stack.append((name, n))
            elif name in pairs or name in ("endstepper", "endstep", "endcolumns", "endcolumn", "endupdates"):
                want = pairs.get(name, name[3:])
                if not stack or stack[-1][0] != want:
                    top = stack[-1] if stack else None
                    err(path, f"unexpected '{{% {name} %}}' (open block: {top[0] + ' from line ' + str(top[1]) if top else 'none'})", n)
                else:
                    stack.pop()
        opens = len(re.findall(r"<details\b", line))
        closes = len(re.findall(r"</details>", line))
        for _ in range(opens):
            stack.append(("details", n))
        for _ in range(closes):
            if stack and stack[-1][0] == "details":
                stack.pop()
            else:
                err(path, "unexpected </details>", n)
    for name, n in stack:
        err(path, f"'{name}' opened here is never closed", n)
    if "{% tab" in body and "{% tabs" not in body:
        err(path, "uses {% tab %} outside a {% tabs %} block")


def check_fences(path: Path, text: str) -> None:
    fence, start = None, 0
    for n, line in enumerate(text.split("\n"), 1):
        m = re.match(r"^\s*(`{3,}|~{3,})", line)
        if m:
            tok = m.group(1)
            if fence is None:
                fence, start = tok, n
            elif line.strip().startswith(fence[0] * len(fence)):
                fence = None
    if fence:
        err(path, "code fence opened here is never closed", start)


def check_week(path: Path, text: str) -> None:
    if not text.startswith("---\n") or "description:" not in text.split("---", 2)[1]:
        err(path, "week pages need front matter with a one-sentence `description:`")
    h1 = [l for l in strip_code(text).split("\n") if re.match(r"^# [^#]", l)]
    if len(h1) != 1:
        err(path, f"expected exactly one '# ' heading, found {len(h1)}")
    titles = re.findall(r"\{%\s*tab\s+title=\"([^\"]+)\"", text)
    if titles != WEEK_TABS:
        err(path, f"tabs must be exactly {WEEK_TABS}; found {titles}")


def check_links(path: Path, text: str) -> None:
    body = strip_code(text)
    for n, line in enumerate(body.split("\n"), 1):
        for m in re.finditer(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", line):
            target = m.group(1)
            if re.match(r"^([a-z]+:|#|mailto:)", target):
                continue
            rel = target.split("#")[0]
            if not rel:
                continue
            if not (path.parent / rel).resolve().exists():
                err(path, f"broken relative link '{target}'", n)


def check_hygiene() -> None:
    for p in ROOT.rglob("*"):
        if ".git" in p.parts or not p.is_file():
            continue
        if p.stat().st_size > 5 * 1024 * 1024:
            err(p, "file is larger than 5 MB (see contribute/data-policy.md)")
        if p.suffix in {".md", ".yml", ".yaml", ".py", ".sh", ".R", ".tsv", ".csv"}:
            try:
                t = p.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                err(p, "not valid UTF-8")
                continue
            if re.search(r"^(<<<<<<<|>>>>>>>) ", t, re.M):
                err(p, "contains merge-conflict markers")


def main() -> int:
    check_summary()
    for p in book_pages():
        text = p.read_text(encoding="utf-8")
        check_blocks(p, text)
        check_fences(p, text)
        check_links(p, text)
        if p.parent.name == "weeks" and p.name.startswith("week-"):
            check_week(p, text)
    check_hygiene()
    weeks = sorted((ROOT / "weeks").glob("week-*.md"))
    if len(weeks) != 12:
        warnings.append(f"weeks/: found {len(weeks)} week pages (course design has 12)")
    for w in warnings:
        print("WARN ", w)
    if errors:
        print(f"\n{len(errors)} problem(s):")
        for e in errors:
            print("  ✗", e)
        return 1
    print(f"OK - {len(book_pages())} pages checked, no structural problems.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
