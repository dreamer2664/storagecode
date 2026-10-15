#!/usr/bin/env python3
"""Audit deposit directories against data/INDEX.md — one line per deposit.

The warehouse law (README): every deposit lives at
    data/<project>/<YYYY-MM-DD>-<agent>[-<suffix>]/
and gets ONE line in data/INDEX.md (date · project · agent · what · PR).
Deposits without a line are invisible to the index — this tool finds them.

    python3 tools/audit_deposits.py            # audit the repo
    python3 tools/audit_deposits.py --root DIR # audit a fixture/other tree
    python3 tools/audit_deposits.py --json     # machine-readable findings

Matching (documented because names are ambiguous):
- a dir `data/<project>/<date>-<rest>` matches a row when row.date == date,
  row.project == project, and rest == agent or rest startswith agent + "-"
  (deposits may carry a suffix, e.g. 2026-10-14-vesta-ci-fix);
- when several agents prefix-match (e.g. rest "marcus-aurelius-x" matches
  both "marcus" and "marcus-aurelius"), the LONGEST agent wins;
- one dir may be covered by several rows (same agent, same day, several
  deposits into one dir) — at least one row is enough;
- rows whose (date, project, agent) has no dir are reported as warnings,
  not violations: the deliverable is dirs-without-rows (exit 1 on those).

Exit: 0 = every deposit dir has a matching row · 1 = at least one missing ·
2 = INDEX.md unreadable / no data dir. Stdlib only.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

DIR_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)$")


def parse_index(index_path: Path) -> list[dict]:
    """Parse INDEX.md table rows into {date, project, agent, what, pr, line_no}."""
    rows: list[dict] = []
    for i, line in enumerate(index_path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3 or cells[0] in ("date", "") or set(cells[0]) <= {"-", ":"}:
            continue  # header / separator
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", cells[0]):
            continue  # not a data row
        rows.append({"date": cells[0], "project": cells[1], "agent": cells[2],
                     "what": cells[3] if len(cells) > 3 else "",
                     "pr": cells[4] if len(cells) > 4 else "", "line_no": i})
    return rows


def deposit_dirs(data_root: Path) -> list[Path]:
    """Every data/<project>/<dir> — the deposit directories."""
    out = []
    for project in sorted(p for p in data_root.iterdir() if p.is_dir()):
        for d in sorted(project.iterdir()):
            if d.is_dir():
                out.append(d)
    return out


def match_rows(dirname: str, project: str, rows: list[dict]) -> tuple[list[dict], str]:
    """Return (matching rows, note) for a deposit dir; [] => unmatched.

    Every row that prefix-matches counts as covering the dir (one dir may
    legitimately carry several same-day deposits); the longest agent is the
    reported best match.
    """
    m = DIR_RE.match(dirname)
    if not m:
        return [], "dirname is not <YYYY-MM-DD>-<agent>[-suffix]"
    date, rest = m.group(1), m.group(2)
    candidates = [r for r in rows
                  if r["date"] == date and r["project"] == project
                  and (rest == r["agent"] or rest.startswith(r["agent"] + "-"))]
    if not candidates:
        return [], f"no INDEX row for date={date} project={project} agent~{rest}"
    best = max(candidates, key=lambda r: len(r["agent"]))
    note = f"matched line {best['line_no']} (agent {best['agent']}"
    if len(candidates) > 1:
        note += f", {len(candidates)} rows cover this dir"
    note += ")"
    return candidates, note


def audit(root: Path) -> dict:
    data_root = root / "data"
    index_path = data_root / "INDEX.md"
    if not data_root.is_dir():
        raise SystemExit(f"no data/ directory under {root}")
    if not index_path.is_file():
        raise SystemExit(f"no data/INDEX.md under {root}")
    rows = parse_index(index_path)
    dirs = deposit_dirs(data_root)

    matched, violations = [], []
    covered_rows: set[int] = set()
    for d in dirs:
        hits, note = match_rows(d.name, d.parent.name, rows)
        entry = {"dir": f"data/{d.parent.name}/{d.name}", "note": note}
        if not hits:
            violations.append(entry)
        else:
            # every prefix-matching row counts as covering this dir: one dir
            # may carry several same-day deposits from the same agent
            covered_rows.update(r["line_no"] for r in hits)
            matched.append(entry)
    orphan_rows = [r for r in rows if r["line_no"] not in covered_rows]
    return {"deposits": len(dirs), "index_rows": len(rows),
            "matched": matched, "violations": violations,
            "rows_without_dir": [
                {"line_no": r["line_no"], "date": r["date"],
                 "project": r["project"], "agent": r["agent"]}
                for r in orphan_rows]}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]),
                    help="repo root holding data/ (default: this repo)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)

    result = audit(Path(args.root))
    result["ok"] = not result["violations"]
    if args.json:
        # stdout stays pure JSON in this mode; the verdict line goes to stderr
        print(json.dumps(result, indent=2))
    else:
        print(f"deposits: {result['deposits']} · index rows: {result['index_rows']}")
        for m in result["matched"]:
            print(f"  ok        {m['dir']} — {m['note']}")
        for v in result["violations"]:
            print(f"  MISSING   {v['dir']} — {v['note']}")
        for o in result["rows_without_dir"]:
            print(f"  warning   INDEX line {o['line_no']} ({o['date']} {o['project']}/{o['agent']}) has no deposit dir")
    verdict_out = sys.stderr if args.json else sys.stdout
    if result["violations"]:
        n = len(result["violations"])
        print(f"FAIL: {n} deposit dir(s) without an INDEX row", file=sys.stderr)
        return 1
    print("OK: every deposit dir has a matching INDEX row", file=verdict_out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
