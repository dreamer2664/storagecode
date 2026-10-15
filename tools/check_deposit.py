#!/usr/bin/env python3
"""Deposit validator for the warehouse (task t-20261014-b5b4).

    python3 tools/check_deposit.py [data-root]      # default: <repo>/data

Rules, exactly as the warehouse keeps them:

  1. every directory under ``data/<project>/`` is a deposit dir named
     ``<date>-<agent>`` with an optional ``-<suffix>`` tail, i.e.
     ``YYYY-MM-DD`` + ``-`` + kebab segments (agent first, then any
     discriminator such as ``-2`` or ``-pipeline``);
  2. every deposit dir is covered by at least one row in
     ``data/INDEX.md`` whose date, project and agent cells all match the
     dir (several rows may map to one dir when deposits stack the same day);
  3. when coverage is absent the validator prints a paste-ready INDEX row
     so the fix is mechanical.

Exit codes: 0 = clean, 1 = validation failures (every reason printed),
2 = usage error (missing root etc.). Reads each file once; never writes.
"""

from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

DIR_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)$")


def fail(msg: str) -> None:
    print(f"  {msg}")


def parse_index(index_path: Path) -> set[tuple[str, str, str]]:
    """(date, project, agent) triples covered by data/INDEX.md rows."""
    covered: set[tuple[str, str, str]] = set()
    if not index_path.is_file():
        return covered
    for line in index_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3 or cells[0] in ("date", "---", ":---"):
            continue
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", cells[0]):
            continue
        covered.add((cells[0], cells[1], cells[2]))
    return covered


def check(root: Path) -> list[str]:
    problems: list[str] = []
    index = root / "INDEX.md"
    covered = parse_index(index)
    if not index.is_file():
        problems.append(f"missing index: {index} — no deposit can be covered")
    projects = sorted(p for p in root.iterdir() if p.is_dir()) if root.is_dir() else []
    for project in projects:
        for dep in sorted(p for p in project.iterdir() if p.is_dir()):
            m = DIR_RE.match(dep.name)
            if not m:
                problems.append(
                    f"bad deposit name: {project.name}/{dep.name} — expected "
                    "<YYYY-MM-DD>-<agent>(-<suffix>)")
                continue
            y, mo, d, rest = m.groups()
            try:
                dt.date(int(y), int(mo), int(d))
            except ValueError:
                problems.append(f"bad calendar date in dir name: {project.name}/{dep.name}")
                continue
            date_s = f"{y}-{mo}-{d}"
            agent = rest.split("-")[0]
            key = (date_s, project.name, agent)
            if key not in covered:
                problems.append(
                    f"no INDEX.md row covers {project.name}/{dep.name} — paste-ready row:\n"
                    f"    | {date_s} | {project.name} | {agent} | <what was deposited> | - |")
    return problems


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parents[1] / "data"
    if not root.is_dir():
        print(f"check_deposit: no such data root: {root}", file=sys.stderr)
        return 2
    problems = check(root)
    if problems:
        print(f"check_deposit: FAIL ({len(problems)} problem(s)):")
        for p in problems:
            print(f"  {p}")
        return 1
    print(f"check_deposit: OK ({root})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
