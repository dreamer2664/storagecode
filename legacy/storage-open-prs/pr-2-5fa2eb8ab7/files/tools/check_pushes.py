#!/usr/bin/env python3
"""check_pushes.py — lint the PUSHES.md ledger (MAINT t-20261014-83b5).

Validates every data row of the ledger against the contract the room
actually writes (derived from the 60+ production rows on 2026-10-14/15):

  1. exactly 6 columns (`\\|` inside a cell is an escaped pipe, not a
     separator — unescaped pipes split columns);
  2. date column is YYYY-MM-DD;
  3. agent is one lowercase token (hyphens allowed);
  4. repo column names at least one known repo
     (chatcode, superocr, storage, storagecode — composite cells like
     "superocr + workspace" pass on the repo token);
  5. the where-column is self-locating: a `@sha`, a PR reference,
     a task-branch ref (`agent/<agent>/<task-id>`) or a
     `(this commit)`-class marker.
     (`PR #n`, `pull/n`, `**#n**` anywhere in the row), or an explicit
     self-reference the ledger's own conventions use
     (`(this commit)`, `(this row)`, `(initial)`,
     `(watch log vN, this row)`, `no push(es)`, `bus ballots (N)`);
  6. the what-column is not empty.

Every violation is reported with its row number; exit 1 if any.

Usage:
  python3 tools/check_pushes.py            # lint the repo-root PUSHES.md
  python3 tools/check_pushes.py PATH       # lint another ledger (fixtures)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPOS = ("chatcode", "superocr", "storage", "storagecode", "vigil")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
AGENT_RE = re.compile(r"^[a-z][a-z0-9-]*$")
SHA_RE = re.compile(r"@[0-9a-f]{7,40}\b")
PR_RE = re.compile(r"\bPR #\d+\b|pull/\d+|\*\*#\d+\*\*")
# a task-branch ref (agent/<agent>/<task-id>) is resolvable via git fetch —
# weaker than a sha but self-locating (scipio rows, 2026-10-15)
BRANCH_RE = re.compile(r"\bagent/[a-z0-9-]+/t-\d{8}-[0-9a-f]{4}\b")
SELFREF_RE = re.compile(r"\((?:watch log v\d+, )?this (?:commit|row)\)"
                        r"|\(initial\)|\bno pushes?\b|\bbus ballots? \(\d+\)")


def _split_row(line: str) -> list[str]:
    """Split a markdown table row into cells; `\\|` is escaped content."""
    esc = line.replace(r"\|", "\x00")
    cells = [c.replace("\x00", "|").strip() for c in esc.strip().split("|")]
    if cells and cells[0] == "":
        cells = cells[1:]
    if cells and cells[-1] == "":
        cells = cells[:-1]
    return cells


def lint(path: Path) -> tuple[list[str], int]:
    errors: list[str] = []
    rows = path.read_text(encoding="utf-8").splitlines()
    data = 0
    for i, line in enumerate(rows, 1):
        if not line.lstrip().startswith("|"):
            continue
        cells = _split_row(line)
        if cells and "date" in cells[0].lower():
            continue  # header row (+ its separator line has dashes only)
        if cells and all(set(c) <= set("-: ") for c in cells):
            continue  # |---|---| separator
        data += 1
        where = line
        if len(cells) != 6:
            errors.append(f"row {i}: {len(cells)} columns, expected 6")
            continue  # downstream checks need the columns aligned
        date, agent, repo, sha_cell, what, _nxt = cells
        if not DATE_RE.match(date):
            errors.append(f"row {i}: date {date!r} is not YYYY-MM-DD")
        if not AGENT_RE.match(agent):
            errors.append(f"row {i}: agent {agent!r} is not a lowercase token")
        if not any(r in repo for r in REPOS):
            errors.append(f"row {i}: repo {repo!r} names no known repo")
        if not (SHA_RE.search(where) or PR_RE.search(where)
                or BRANCH_RE.search(where)
                or SELFREF_RE.search(sha_cell)):
            errors.append(
                f"row {i}: where {sha_cell!r} is not self-locating "
                "(need @sha, PR ref, or a (this commit)/(this row)/(initial)/"
                "watch-log/no-pushes marker)")
        if not what:
            errors.append(f"row {i}: what column is empty")
    if data == 0:
        errors.append(f"{path}: no data rows found")
    return errors, data


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else (
        Path(__file__).resolve().parent.parent / "PUSHES.md")
    errors, n = lint(path)
    if errors:
        print(f"PUSHES lint FAIL ({path}):", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1
    print(f"PUSHES.md: {n} row(s) OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
