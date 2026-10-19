#!/usr/bin/env python3
"""Pins tools/audit_deposits.py (MAINT t-20261014-e427).

    python3 tests/test_audit_deposits.py

Checks: the current tree audits clean; a deposit dir with no INDEX row is a
named violation (exit 1); suffix dirs match; several rows may cover one dir;
the longest agent prefix wins; rows without dirs warn but do not fail;
malformed dirnames are violations. Fixture trees are built in temp dirs.
"""
from __future__ import annotations

import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import audit_deposits as ad  # noqa: E402

HEADER = """# Data index — one line per deposit

| date | project | agent | what | PR |
|---|---|---|---|---|
"""


def build_tree(tmp: Path, dirs: list[str], rows: list[tuple[str, str, str]]) -> Path:
    (tmp / "data").mkdir()
    (tmp / "data" / "INDEX.md").write_text(
        HEADER + "".join(f"| {d} | {p} | {a} | fixture | - |\n" for d, p, a in rows)
    )
    for rel in dirs:
        (tmp / "data" / rel).mkdir(parents=True)
        (tmp / "data" / rel / "README.md").write_text("fixture\n")
    return tmp


def run_main(root: Path) -> tuple[int, str, dict | None]:
    out, err = io.StringIO(), io.StringIO()
    payload = None
    with redirect_stdout(out), redirect_stderr(err):
        rc = ad.main(["--root", str(root), "--json"])
    text = out.getvalue()
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        pass
    return rc, err.getvalue(), payload


class TestAuditDeposits(unittest.TestCase):
    def test_current_tree_is_clean(self):
        # the deliverable's own evidence: today's tree has no missing rows
        rc, err, payload = run_main(ROOT)
        self.assertEqual(rc, 0, f"current tree must audit clean: {err}")
        self.assertEqual(payload["violations"], [])
        self.assertGreaterEqual(payload["deposits"], 5)

    def test_missing_row_is_named_violation(self):
        with tempfile.TemporaryDirectory() as td:
            root = build_tree(Path(td),
                              dirs=["superocr/2026-10-14-alice", "superocr/2026-10-14-bob"],
                              rows=[("2026-10-14", "superocr", "alice")])
            rc, err, payload = run_main(root)
            self.assertEqual(rc, 1)
            self.assertIn("FAIL", err)
            self.assertEqual([v["dir"] for v in payload["violations"]],
                             ["data/superocr/2026-10-14-bob"])

    def test_suffix_dir_matches_agent_row(self):
        with tempfile.TemporaryDirectory() as td:
            root = build_tree(Path(td),
                              dirs=["superocr/2026-10-14-vesta-ci-fix"],
                              rows=[("2026-10-14", "superocr", "vesta")])
            rc, _, payload = run_main(root)
            self.assertEqual(rc, 0)
            self.assertEqual(len(payload["matched"]), 1)

    def test_several_rows_may_cover_one_dir(self):
        with tempfile.TemporaryDirectory() as td:
            root = build_tree(Path(td),
                              dirs=["superocr/2026-10-14-odysseus"],
                              rows=[("2026-10-14", "superocr", "odysseus"),
                                    ("2026-10-14", "superocr", "odysseus")])
            rc, _, payload = run_main(root)
            self.assertEqual(rc, 0)
            # both rows prefix-match the same dir, so both count as covered
            self.assertEqual(len(payload["rows_without_dir"]), 0)

    def test_longest_agent_prefix_wins(self):
        with tempfile.TemporaryDirectory() as td:
            root = build_tree(Path(td),
                              dirs=["chatcode/2026-10-14-marcus-aurelius-notes"],
                              rows=[("2026-10-14", "chatcode", "marcus"),
                                    ("2026-10-14", "chatcode", "marcus-aurelius")])
            rc, _, payload = run_main(root)
            self.assertEqual(rc, 0)
            self.assertIn("marcus-aurelius", payload["matched"][0]["note"])

    def test_row_without_dir_warns_but_passes(self):
        with tempfile.TemporaryDirectory() as td:
            root = build_tree(Path(td),
                              dirs=[],
                              rows=[("2026-10-14", "superocr", "ghost")])
            rc, _, payload = run_main(root)
            self.assertEqual(rc, 0)
            self.assertEqual(len(payload["rows_without_dir"]), 1)

    def test_malformed_dirname_is_violation(self):
        with tempfile.TemporaryDirectory() as td:
            root = build_tree(Path(td),
                              dirs=["superocr/not-a-date-dir"],
                              rows=[("2026-10-14", "superocr", "alice")])
            rc, _, payload = run_main(root)
            self.assertEqual(rc, 1)
            self.assertIn("not <YYYY-MM-DD>", payload["violations"][0]["note"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
