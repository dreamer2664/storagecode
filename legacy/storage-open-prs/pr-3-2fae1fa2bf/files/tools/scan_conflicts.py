#!/usr/bin/env python3
"""scan_conflicts.py — no committed git conflict markers, ever (t-20261014-1d47).

Storage once merged a PUSHES.md carrying conflict markers (the "storage
burn"). This walks a repo tree and exits 1 listing every file that
contains a conflict marker line (the 7-character forms, line-anchored —
an equals-rule decoration in prose is still flagged, by design: commit
formatting belongs to humans who can shorten it, never to a resolver's
leftovers). .git is ignored.

Note on self-reference: the marker strings are CONSTRUCTED inside this
file (never spelled literally), so the scanner does not flag itself or
its tests; fixtures build them the same way.

Usage:
  python3 tools/scan_conflicts.py [ROOT ...]   # default: repo root
Exit: 0 clean, 1 markers found (each offending file listed), 2 usage error.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

MARKERS = ("<" * 7, "=" * 7, ">" * 7)   # 7 chars, line-anchored
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".github_bak"}
MAX_BYTES = 2_000_000  # big blobs are not hand-merged text; skip, don't parse


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def scan_file(path: Path) -> list[int]:
    """Line numbers (1-based) whose line STARTS with a conflict marker."""
    try:
        if path.stat().st_size > MAX_BYTES:
            return []
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []  # binary or unreadable: not a merge-conflict artifact hunt
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        for m in MARKERS:
            if line.startswith(m):
                hits.append(i)
                break
    return hits


def scan(roots: list[Path]) -> dict[str, list[int]]:
    found: dict[str, list[int]] = {}
    for root in roots:
        if root.is_file():
            hits = scan_file(root)
            if hits:
                found[str(root)] = hits
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
            for name in sorted(filenames):
                p = Path(dirpath) / name
                hits = scan_file(p)
                if hits:
                    found[str(p)] = hits
    return found


def main(argv: list[str]) -> int:
    roots = [Path(a) for a in argv[1:]] or [repo_root()]
    missing = [str(r) for r in roots if not r.exists()]
    if missing:
        print(f"scan_conflicts: no such path: {', '.join(missing)}", file=sys.stderr)
        return 2
    found = scan(roots)
    if found:
        print("conflict markers found:", file=sys.stderr)
        for f, lines in found.items():
            print(f"  {f}: line(s) {', '.join(map(str, lines))}", file=sys.stderr)
        return 1
    print(f"scan_conflicts: clean ({len(roots)} root(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
