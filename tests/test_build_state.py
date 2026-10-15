#!/usr/bin/env python3
"""Evidence for V-STATE (t-20261015-c39d), CONTRACT.md §2:

    python3 tests/test_build_state.py

Runs tools/build_state.py the way the workflow does and checks the contract:
every §2 key, exact item shapes, caps, deterministic order, and — with a
pinned clock — byte-identical reruns. Needs the empire as siblings of this
repo (VIGIL_SRC overrides; default ../../ which is src/ in the workflow and
in a local mirror).
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(os.environ.get("VIGIL_SRC", ROOT.parents[0]))
TOOL = ROOT / "tools" / "build_state.py"
NOW = "2026-10-15T09:00:00Z"

TOP_KEYS = {"schema", "generated_ts", "warnings", "git", "board", "team",
            "chat", "records", "projects", "walls", "flags"}
ITEM_KEYS = {
    ("board", "open"): {"id", "title", "priority", "tags", "owner", "age_h"},
    ("board", "claimed"): {"id", "title", "priority", "owner", "lease_expires", "checkpoint"},
    ("board", "review"): {"id", "title", "owner", "pr", "age_h"},
    ("board", "blocked"): {"id", "title", "owner", "note"},
    ("chat", "tail"): {"id", "ts", "from", "type", "text"},
    ("records", "pushes"): {"date", "agent", "repo", "what"},
    ("records", "wire"): {"id", "ts", "topic", "message"},
    ("records", "shifts"): {"date", "agent", "file"},
}
CAPS = {"open": 100, "claimed": 50, "review": 50, "blocked": 50,
        "chat_tail": 40, "pushes": 30, "wire": 30, "shifts": 10, "epics": 12}


def build(out: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TOOL), "--out", str(out), "--src-root", str(SRC), "--now", NOW],
        capture_output=True, text=True)


@unittest.skipUnless((SRC / "chatcode" / "board" / "tasks").is_dir(),
                     f"empire checkouts not found under {SRC} (set VIGIL_SRC)")
class BuildState(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out1 = Path(cls.tmp.name) / "s1.json"
        cls.out2 = Path(cls.tmp.name) / "s2.json"
        cls.r1 = build(cls.out1)
        cls.r2 = build(cls.out2)
        cls.state = json.loads(cls.out1.read_text()) if cls.out1.exists() else {}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_exit_zero_and_writes(self):
        self.assertEqual(self.r1.returncode, 0, self.r1.stderr)
        self.assertTrue(self.out1.is_file())

    def test_every_contract_key(self):
        self.assertEqual(set(self.state), TOP_KEYS)
        self.assertEqual(self.state["schema"], 1)
        self.assertRegex(self.state["generated_ts"], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
        for coll in ("open", "claimed", "review", "blocked"):
            self.assertIsInstance(self.state["board"][coll], list)
        for k in ("counts", "window_min", "awake", "total", "agents", "count_24h", "tail",
                  "pushes", "wire", "shifts", "epics"):
            self.assertIn(k, json.dumps(self.state))  # present somewhere per schema

    def test_counts_match_the_board(self):
        tasks = list((SRC / "chatcode" / "board" / "tasks").glob("*.json"))
        statuses = {}
        for f in tasks:
            s = json.loads(f.read_text()).get("status")
            statuses[s] = statuses.get(s, 0) + 1
        for s in ("open", "claimed", "review", "blocked", "done", "dropped"):
            self.assertEqual(self.state["board"]["counts"].get(s), statuses.get(s, 0),
                             f"status {s}")

    def test_item_shapes_exact(self):
        for (sec, coll), keys in ITEM_KEYS.items():
            for item in self.state[sec][coll]:
                self.assertEqual(set(item), keys, f"{sec}.{coll} item {item}")

    def test_caps_respected(self):
        b, c, r = self.state["board"], self.state["chat"], self.state["records"]
        self.assertLessEqual(len(b["open"]), CAPS["open"])
        self.assertLessEqual(len(b["claimed"]), CAPS["claimed"])
        self.assertLessEqual(len(b["review"]), CAPS["review"])
        self.assertLessEqual(len(b["blocked"]), CAPS["blocked"])
        self.assertLessEqual(len(c["tail"]), CAPS["chat_tail"])
        self.assertLessEqual(len(r["pushes"]), CAPS["pushes"])
        self.assertLessEqual(len(r["wire"]), CAPS["wire"])
        self.assertLessEqual(len(r["shifts"]), CAPS["shifts"])
        for p in self.state["projects"]:
            self.assertLessEqual(len(p["epics"]), CAPS["epics"])

    def test_deterministic_bytes_with_pinned_clock(self):
        self.assertEqual(self.r2.returncode, 0, self.r2.stderr)
        self.assertEqual(self.out1.read_bytes(), self.out2.read_bytes(),
                         "two runs with the same inputs and --now must be byte-identical")

    def test_walls_and_flags_are_honest(self):
        w = self.state["walls"]
        self.assertIsInstance(w.get("easy_best"), int)
        self.assertLess(w["easy_target"], 100)  # the bars exist and are not claimed met
        self.assertLessEqual(w["easy_best"], 100)
        self.assertTrue(w.get("source"))
        for name in self.state["flags"]["silent_agents"]:
            agent = next(a for a in self.state["team"]["agents"] if a["name"] == name)
            self.assertFalse(agent["alive"])

    def test_no_missing_source_warnings_when_complete(self):
        missing = [w for w in self.state["warnings"] if "missing" in w or "degraded" in w]
        self.assertEqual(missing, [], f"warnings should be clean with all checkouts present: {missing}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
