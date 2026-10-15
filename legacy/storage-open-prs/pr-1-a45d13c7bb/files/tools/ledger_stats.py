#!/usr/bin/env python3
"""Count PUSHES.md rows per day, per agent and per repo.

Usage:
    python3 tools/ledger_stats.py [PUSHES.md] [--json]

A ledger row is a markdown table line whose first cell is an ISO date
(YYYY-MM-DD). Header and separator lines are ignored. Repo cells that
combine repos (e.g. "superocr + workspace") are counted under the full
text, so the counts always sum to the number of rows.
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse_rows(text):
    """Return a list of (date, agent, repo) tuples for each ledger row."""
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|") or not line.endswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3 or not DATE_RE.match(cells[0]):
            continue
        rows.append((cells[0], cells[1], cells[2]))
    return rows


def stats(rows):
    return {
        "total": len(rows),
        "per_day": dict(sorted(Counter(r[0] for r in rows).items())),
        "per_agent": dict(Counter(r[1] for r in rows).most_common()),
        "per_repo": dict(Counter(r[2] for r in rows).most_common()),
    }


def render_table(s):
    out = [f"total rows: {s['total']}"]
    for title, key in (("per day", "per_day"), ("per agent", "per_agent"), ("per repo", "per_repo")):
        out.append("")
        out.append(f"| {title} | rows |")
        out.append("|---|---|")
        for k, v in s[key].items():
            out.append(f"| {k} | {v} |")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?", default=str(Path(__file__).resolve().parent.parent / "PUSHES.md"))
    ap.add_argument("--json", action="store_true", help="print JSON instead of tables")
    args = ap.parse_args(argv)
    s = stats(parse_rows(Path(args.path).read_text(encoding="utf-8")))
    print(json.dumps(s, indent=2) if args.json else render_table(s))
    return 0


if __name__ == "__main__":
    sys.exit(main())
