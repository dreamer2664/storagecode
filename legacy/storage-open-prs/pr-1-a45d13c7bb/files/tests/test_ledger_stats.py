#!/usr/bin/env python3
"""Fixture tests for tools/ledger_stats.py. Run: python3 tests/test_ledger_stats.py"""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import ledger_stats as ls  # noqa: E402

FIXTURE = """# PUSHES — fixture

| date (UTC) | agent | repo | branch @ SHA / PR | what + result | next |
|---|---|---|---|---|---|
| 2026-10-13 | alice | superocr | main @aaa | x | y |
| 2026-10-14 | alice | chatcode | main @bbb | x | y |
| 2026-10-14 | bob | storage | main (this row) | x | — |
| 2026-10-14 | bob | superocr + workspace | agent/bob/t-1 @ccc | x | y |

not a row | at all
| 2026-10-15 | carol | storage | main | x | y
"""


class LedgerStatsTest(unittest.TestCase):
    def test_parse_skips_header_separator_and_prose(self):
        rows = ls.parse_rows(FIXTURE)
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0], ("2026-10-13", "alice", "superocr"))

    def test_counts_per_day_agent_repo(self):
        s = ls.stats(ls.parse_rows(FIXTURE))
        self.assertEqual(s["total"], 4)
        self.assertEqual(s["per_day"], {"2026-10-13": 1, "2026-10-14": 3})
        self.assertEqual(s["per_agent"], {"alice": 2, "bob": 2})
        self.assertEqual(s["per_repo"]["storage"], 1)
        self.assertEqual(s["per_repo"]["superocr + workspace"], 1)
        self.assertEqual(sum(s["per_day"].values()), s["total"])
        self.assertEqual(sum(s["per_agent"].values()), s["total"])
        self.assertEqual(sum(s["per_repo"].values()), s["total"])

    def test_main_on_fixture_file_json_and_table(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "PUSHES.md"
            p.write_text(FIXTURE, encoding="utf-8")
            self.assertEqual(ls.main([str(p), "--json"]), 0)
            self.assertEqual(ls.main([str(p)]), 0)

    def test_real_ledger_has_rows(self):
        s = ls.stats(ls.parse_rows((ROOT / "PUSHES.md").read_text(encoding="utf-8")))
        self.assertGreater(s["total"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
