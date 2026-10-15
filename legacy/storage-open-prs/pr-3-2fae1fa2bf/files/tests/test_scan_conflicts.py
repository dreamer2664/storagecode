#!/usr/bin/env python3
"""Tests for tools/scan_conflicts.py (MAINT t-20261014-1d47).

Evidence per the card: a clean tree exits 0; a fixture file with markers
exits 1 naming the file. Plus: markers are line-anchored (a mid-line
token is not flagged), .git is ignored, missing path exits 2, and the
repo's own tree is clean. Fixtures construct markers like the scanner
does ("<"*7) so no literal marker ever sits in this file.

Run: python3 tests/test_scan_conflicts.py
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import scan_conflicts  # noqa: E402

LT, EQ, GT = "<" * 7, "=" * 7, ">" * 7


def write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


class ScanFixtures(unittest.TestCase):
    def setUp(self):
        self.td = Path(tempfile.mkdtemp(prefix="scan-conflicts-"))

    def test_clean_tree_exits_0(self):
        write(self.td / "a.md", "hello\nnot a marker: <<< three only\n")
        self.assertEqual(scan_conflicts.scan([self.td]), {})

    def test_marked_file_fails_and_names_file_and_lines(self):
        write(self.td / "b.md",
              f"top\n{LT} HEAD\nmine\n{EQ}\ntheirs\n{GT} origin\n")
        found = scan_conflicts.scan([self.td])
        self.assertEqual(len(found), 1)
        f = next(iter(found))
        self.assertTrue(f.endswith("b.md"))
        self.assertEqual(found[f], [2, 4, 6])

    def test_line_anchoring_only(self):
        write(self.td / "c.txt",
              f"indented {LT} not a conflict\nplain text {EQ} mid-line\n")
        self.assertEqual(scan_conflicts.scan([self.td]), {})

    def test_git_dir_is_ignored(self):
        write(self.td / ".git" / "MERGE_MSG", f"{LT} junk\n{EQ}\n")
        self.assertEqual(scan_conflicts.scan([self.td]), {})

    def test_binary_is_skipped(self):
        write(self.td / "d.bin", "")
        (self.td / "d.bin").write_bytes(b"\x00\xff" + LT.encode() + b"\xfe")
        self.assertEqual(scan_conflicts.scan([self.td]), {})


class CliEndToEnd(unittest.TestCase):
    def _run(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(ROOT / "tools/scan_conflicts.py"), *args],
            capture_output=True, text=True)

    def test_missing_path_exits_2(self):
        r = self._run("/definitely/not/here")
        self.assertEqual(r.returncode, 2, r.stderr)

    def test_cli_clean_repo_tree_exits_0(self):
        r = self._run()  # default root = this repo
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("clean", r.stdout)

    def test_cli_marked_fixture_exits_1_naming_file(self):
        td = Path(tempfile.mkdtemp(prefix="scan-conflicts-cli-"))
        write(td / "PUSHES.md", f"| a | b |\n{LT} HEAD\nx\n{EQ}\ny\n{GT} o\n")
        r = self._run(str(td))
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("PUSHES.md", r.stderr)
        self.assertIn("line(s) 2, 4, 6", r.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
