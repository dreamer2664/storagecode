#!/usr/bin/env python3
"""Append the formalcode wire stream to wire/<date>.jsonl — dedup by ntfy id.

Reads NDJSON from ntfy (poll output, one message object per line), drops
non-message events (open/keepalive), skips ids already archived anywhere in
wire/, and appends the rest to the file of each message's UTC day. Append-only
and idempotent: running it twice writes nothing the second time.

    python3 tools/append_wire.py /tmp/formalcode.jsonl

Stdlib only — runs from .github/workflows/wire-archive.yml every 30 minutes.
"""
from __future__ import annotations

import datetime as dt
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WIRE = os.path.join(os.path.dirname(HERE), "wire")


def archived_ids() -> set[str]:
    seen: set[str] = set()
    for path in glob.glob(os.path.join(WIRE, "*.jsonl")):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    mid = json.loads(line).get("id")
                except json.JSONDecodeError:
                    continue
                if mid:
                    seen.add(mid)
    return seen


def main() -> int:
    src = sys.argv[1] if len(sys.argv) > 1 else "/tmp/formalcode.jsonl"
    seen = archived_ids()
    fresh: dict[str, dict] = {}
    dupes = 0
    if os.path.exists(src):
        with open(src, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    m = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if m.get("event") != "message":
                    continue
                mid = m.get("id")
                if not mid or not m.get("time"):
                    continue
                if mid in seen or mid in fresh:
                    dupes += 1
                    continue
                fresh[mid] = m
    if not fresh:
        print(f"wire: nothing new ({dupes} already archived)")
        return 0

    by_day: dict[str, list[dict]] = {}
    for m in sorted(fresh.values(), key=lambda x: x["time"]):
        day = dt.datetime.fromtimestamp(m["time"], dt.timezone.utc).date().isoformat()
        by_day.setdefault(day, []).append(m)
    for day, msgs in sorted(by_day.items()):
        path = os.path.join(WIRE, f"{day}.jsonl")
        with open(path, "a", encoding="utf-8") as f:
            for m in msgs:
                f.write(json.dumps(m, ensure_ascii=False, sort_keys=True) + "\n")
    days = ", ".join(f"{d} (+{len(by_day[d])})" for d in sorted(by_day))
    print(f"wire: archived {len(fresh)} new message(s) — {days}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
