#!/usr/bin/env python3
"""Tests for tools/check_pushes.py (MAINT t-20261014-83b5).

Covers the deliverable evidence: pass on a valid ledger, and a fixture
row with 4 columns fails naming its row number — plus one fixture per
rule (date, agent, repo, self-locating where, empty what, escaped pipe)
and an integration pass on the repo's own PUSHES.md.

Run: python3 tests/test_check_pushes.py
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from check_pushes import lint  # noqa: E402

HEADER = (
    "# PUSHES — one row per push\n\n"
    "| date (UTC) | agent | repo | branch @ SHA / PR | what + result | next |\n"
    "|---|---|---|---|---|---|\n")
GOOD = HEADER + (
    "| 2026-10-14 | odysseus | superocr | agent/o/t-x @8a8010d | shipped. | — |\n"
    "| 2026-10-14 | vesta | storage + workspace | main (this row) | logged. | — |\n"
    "| 2026-10-15 | cormac | superocr | main — 6 merges | merged **#84** f8fbb211. | — |\n"
    "| 2026-10-15 | argus | storagecode | main @1a2b3c4 + @5d6e7f8 (bot) | rows. | — |\n"
    "| 2026-10-15 | leonidas | superocr | reviews, no pushes | Balloted PR #70. | — |\n"
    "| 2026-10-15 | scipio | chatcode | main (this commit) | plain\\|lex escaped pipe. | — |\n"
    "| 2026-10-15 | vesta | vigil | main @bb689a7 + @51bf58f | VIGIL created. | — |\n"
    "| 2026-10-15 | vesta | chatcode | bus ballots (3) | three verifications cast. | — |\n"
    "| 2026-10-15 | cormac | superocr | review ballot, no push | Balloted t-x PR #89 @d27a65e. | — |\n"
    "| 2026-10-15 | scipio | storagecode | agent/scipio/t-20261014-e427 | auditor, details in what-cell incl. storagecode#1. | — |\n")


def _with(rows: str) -> str:
    """Append fixture rows after the valid rows; they land on known lines."""
    return GOOD + rows


FIXTURE_LINE = len(GOOD.splitlines()) + 1  # 1-based line of an appended row


class LintFixtures(unittest.TestCase):
    def _lint(self, text: str) -> tuple[list[str], int]:
        with tempfile.NamedTemporaryFile(
                "w", suffix=".md", delete=False) as f:
            f.write(text)
            f.flush()  # lint() re-opens the file in this process
            return lint(Path(f.name))

    def test_valid_ledger_passes(self):
        errors, n = self._lint(GOOD)
        self.assertEqual(errors, [])
        self.assertEqual(n, 10)

    def test_deliverable_evidence_4_column_row_fails_with_row_number(self):
        fixture = _with("| 2026-10-14 | bob | chatcode | half a row |\n")
        errors, _ = self._lint(fixture)
        self.assertTrue(any("columns, expected 6" in e
                            and f"row {FIXTURE_LINE}" in e
                            for e in errors), errors)

    def test_bad_date_fails(self):
        fixture = _with("| 14/10/2026 | bob | chatcode | main @abc1234 | x. | — |\n")
        errors, _ = self._lint(fixture)
        self.assertTrue(any("not YYYY-MM-DD" in e for e in errors), errors)

    def test_bad_agent_fails(self):
        fixture = _with("| 2026-10-14 | Bob K | chatcode | main @abc1234 | x. | — |\n")
        errors, _ = self._lint(fixture)
        self.assertTrue(any("not a lowercase token" in e for e in errors), errors)

    def test_unknown_repo_fails(self):
        fixture = _with("| 2026-10-14 | bob | moonbase | main @abc1234 | x. | — |\n")
        errors, _ = self._lint(fixture)
        self.assertTrue(any("names no known repo" in e for e in errors), errors)

    def test_bare_main_where_fails(self):
        fixture = _with("| 2026-10-14 | bob | chatcode | main | x. | — |\n")
        errors, _ = self._lint(fixture)
        self.assertTrue(any("not self-locating" in e for e in errors), errors)

    def test_empty_what_fails(self):
        fixture = _with("| 2026-10-14 | bob | chatcode | main @abc1234 |  | — |\n")
        errors, _ = self._lint(fixture)
        self.assertTrue(any("what column is empty" in e for e in errors), errors)

    def test_unescaped_pipe_breaks_columns_and_fails(self):
        # the real-world case fixed in the 2026-10-15 ledger: plain|lex
        fixture = _with("| 2026-10-15 | bob | superocr | main @abc1234 | plain|lex routes. | — |\n")
        errors, _ = self._lint(fixture)
        self.assertTrue(any("columns, expected 6" in e for e in errors), errors)


class RepoIntegration(unittest.TestCase):
    def test_current_pushes_md_lints_green(self):
        out = subprocess.run(
            [sys.executable, str(ROOT / "tools/check_pushes.py")],
            capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("row(s) OK", out.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
