#!/usr/bin/env python3
"""Tests for tools/check_deposit.py — both ways, per t-20261014-b5b4."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("check_deposit", REPO / "tools" / "check_deposit.py")
cd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cd)

INDEX_HEAD = (
    "# Data index\n\n"
    "| date | project | agent | what | PR |\n"
    "|---|---|---|---|---|\n"
)


def make_root(rows: list[str], layout: dict[str, list[str]]) -> Path:
    """Build a throwaway data root: `layout` maps project -> [dir names]."""
    tmp = Path(tempfile.mkdtemp(prefix="check-deposit-"))
    (tmp / "INDEX.md").write_text(INDEX_HEAD + "".join(rows), encoding="utf-8")
    for project, dirs in layout.items():
        for d in dirs:
            (tmp / project / d).mkdir(parents=True)
    return tmp


class TestCheckDeposit(unittest.TestCase):
    def test_clean_tree_passes(self):
        root = make_root(
            ["| 2026-10-14 | superocr | odysseus | S58 receipts | - |\n",
             "| 2026-10-14 | superocr | odysseus | S68 receipts | - |\n"],
            {"superocr": ["2026-10-14-odysseus"]})
        self.assertEqual(cd.check(root), [])

    def test_suffix_forms_accepted(self):
        root = make_root(
            ["| 2026-10-14 | chatcode | vesta | pipeline receipts | - |\n"],
            {"chatcode": ["2026-10-14-vesta-pipeline"]})
        self.assertEqual(cd.check(root), [])

    def test_numeric_suffix_accepted(self):
        root = make_root(
            ["| 2026-10-14 | superocr | scipio | second drop | - |\n"],
            {"superocr": ["2026-10-14-scipio-2"]})
        self.assertEqual(cd.check(root), [])

    def test_bad_name_and_missing_row_fail_with_both_reasons(self):
        root = make_root(
            [],  # no rows at all
            {"superocr": ["not-a-deposit", "2026-10-15-odysseus"]})
        problems = cd.check(root)
        joined = "\n".join(problems)
        self.assertEqual(len(problems), 2, problems)
        self.assertIn("bad deposit name: superocr/not-a-deposit", joined)
        self.assertIn("no INDEX.md row covers superocr/2026-10-15-odysseus", joined)
        # the paste-ready row text is printed with the right date/project/agent
        self.assertIn("| 2026-10-15 | superocr | odysseus |", joined)

    def test_bad_calendar_date_caught(self):
        root = make_root([], {"superocr": ["2026-13-40-odysseus"]})
        problems = cd.check(root)
        self.assertEqual(len(problems), 1)
        self.assertIn("bad calendar date", problems[0])

    def test_wrong_project_row_does_not_cover(self):
        root = make_root(
            ["| 2026-10-14 | chatcode | odysseus | wrong project | - |\n"],
            {"superocr": ["2026-10-14-odysseus"]})
        problems = cd.check(root)
        self.assertEqual(len(problems), 1)
        self.assertIn("no INDEX.md row", problems[0])

    def test_missing_index_file_flags_every_dir(self):
        tmp = Path(tempfile.mkdtemp(prefix="check-deposit-"))
        (tmp / "superocr" / "2026-10-14-odysseus").mkdir(parents=True)
        problems = cd.check(tmp)
        joined = "\n".join(problems)
        self.assertIn("missing index", joined)
        self.assertIn("no INDEX.md row covers superocr/2026-10-14-odysseus", joined)

    def test_real_tree_is_green(self):
        problems = cd.check(REPO / "data")
        self.assertEqual(problems, [], "\n".join(problems))

    def test_main_exit_codes(self):
        self.assertEqual(cd.main(["check_deposit.py", "/definitely/not/here"]), 2)


if __name__ == "__main__":
    unittest.main()
