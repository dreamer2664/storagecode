#!/usr/bin/env python3
"""Pins tools/append_wire.py (MAINT t-20261014-e4e9), the durable formalcode
archive. The workflow runs this every 30 minutes against the live wire; if it
silently dropped messages, double-archived them, or mis-filed the UTC day,
the record would rot without anyone noticing — so the behaviour is pinned:

  1. non-message events (open/keepalive) are skipped
  2. dedup by id — within one input file
  3. dedup by id — against what is already archived in wire/
  4. a second run is idempotent (byte-identical wire, "nothing new")
  5. messages split into files by UTC day of `time`
  6. messages land sorted by time
  7. messages missing id or time are skipped
  8. malformed JSON lines are skipped, not fatal

    python3 tests/test_append_wire.py

Stdlib only. The real wire/ is never touched: the tool's WIRE path is
redirected to a temp dir for every case.
"""
from __future__ import annotations

import datetime as dt
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "append_wire.py"

_spec = importlib.util.spec_from_file_location("append_wire", TOOL)
AW = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(AW)

UTC = dt.timezone.utc


def ts(y, mo, d, h=12, mi=0, s=0) -> int:
    return int(dt.datetime(y, mo, d, h, mi, s, tzinfo=UTC).timestamp())


def msg(mid: str, time: int, message: str = "m") -> dict:
    return {"id": mid, "time": time, "event": "message", "topic": "formalcode",
            "message": message}


class AppendWire(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        root = Path(self._tmp.name)
        self.wire = root / "wire"
        self.wire.mkdir()
        self.src = root / "formalcode.jsonl"
        self._old_wire = AW.WIRE
        AW.WIRE = str(self.wire)

    def tearDown(self):
        AW.WIRE = self._old_wire
        self._tmp.cleanup()

    def run_tool(self) -> tuple[int, str]:
        argv = [str(TOOL), str(self.src)]
        old = sys.argv
        sys.argv = argv
        out = io.StringIO()
        try:
            with redirect_stdout(out):
                rc = AW.main()
        finally:
            sys.argv = old
        return rc, out.getvalue()

    def write_src(self, lines: list) -> None:
        self.src.write_text("".join(json.dumps(x) + "\n" if isinstance(x, dict) else x + "\n"
                                    for x in lines), encoding="utf-8")

    def wire_lines(self, name: str) -> list[dict]:
        p = self.wire / name
        if not p.exists():
            return []
        return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]

    def test_non_message_events_skipped(self):
        self.write_src([{"event": "open"}, {"event": "keepalive"},
                        msg("a1", ts(2026, 10, 14))])
        rc, out = self.run_tool()
        self.assertEqual(rc, 0)
        rows = self.wire_lines("2026-10-14.jsonl")
        self.assertEqual([r["id"] for r in rows], ["a1"])
        self.assertIn("archived 1", out)

    def test_dedup_within_input_file(self):
        self.write_src([msg("dup", ts(2026, 10, 14)), msg("dup", ts(2026, 10, 14))])
        rc, out = self.run_tool()
        self.assertEqual(rc, 0)
        self.assertEqual(len(self.wire_lines("2026-10-14.jsonl")), 1)

    def test_dedup_against_existing_archive(self):
        (self.wire / "2026-10-13.jsonl").write_text(
            json.dumps(msg("old", ts(2026, 10, 13))) + "\n", encoding="utf-8")
        self.write_src([msg("old", ts(2026, 10, 13)), msg("new", ts(2026, 10, 14))])
        rc, out = self.run_tool()
        self.assertEqual(rc, 0)
        self.assertEqual(len(self.wire_lines("2026-10-13.jsonl")), 1)   # untouched
        self.assertEqual([r["id"] for r in self.wire_lines("2026-10-14.jsonl")], ["new"])

    def test_second_run_is_idempotent(self):
        self.write_src([msg("a1", ts(2026, 10, 14)), msg("a2", ts(2026, 10, 14, 13))])
        self.run_tool()
        before = (self.wire / "2026-10-14.jsonl").read_bytes()
        rc, out = self.run_tool()
        self.assertEqual(rc, 0)
        self.assertIn("nothing new", out)
        self.assertEqual((self.wire / "2026-10-14.jsonl").read_bytes(), before)

    def test_day_split_by_utc_date(self):
        self.write_src([
            msg("late", ts(2026, 10, 14, 23, 59, 59)),
            msg("early", ts(2026, 10, 15, 0, 0, 1)),
        ])
        rc, _ = self.run_tool()
        self.assertEqual(rc, 0)
        self.assertEqual([r["id"] for r in self.wire_lines("2026-10-14.jsonl")], ["late"])
        self.assertEqual([r["id"] for r in self.wire_lines("2026-10-15.jsonl")], ["early"])

    def test_messages_sorted_by_time(self):
        self.write_src([
            msg("c", ts(2026, 10, 14, 15)),
            msg("a", ts(2026, 10, 14, 9)),
            msg("b", ts(2026, 10, 14, 12)),
        ])
        rc, _ = self.run_tool()
        self.assertEqual(rc, 0)
        self.assertEqual([r["id"] for r in self.wire_lines("2026-10-14.jsonl")],
                         ["a", "b", "c"])

    def test_missing_id_or_time_skipped(self):
        self.write_src([
            {"event": "message", "time": ts(2026, 10, 14)},                 # no id
            {"event": "message", "id": "notime"},                           # no time
            msg("ok", ts(2026, 10, 14)),
        ])
        rc, _ = self.run_tool()
        self.assertEqual(rc, 0)
        self.assertEqual([r["id"] for r in self.wire_lines("2026-10-14.jsonl")], ["ok"])

    def test_malformed_json_lines_skipped(self):
        self.write_src(["{not json at all", "", json.dumps(msg("ok", ts(2026, 10, 14)))])
        rc, _ = self.run_tool()
        self.assertEqual(rc, 0)
        self.assertEqual([r["id"] for r in self.wire_lines("2026-10-14.jsonl")], ["ok"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
