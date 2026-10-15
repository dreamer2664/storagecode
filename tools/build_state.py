#!/usr/bin/env python3
"""Vigil state compiler — the production tool behind CONTRACT.md §2 (schema v1).

    python3 tools/build_state.py --out app/state.json

Run from a storagecode checkout with the empire as siblings (the workflow
arranges that):  ./src/chatcode  ./src/superocr  ./src/storage  [./src/vigil]

What it does, exactly (CONTRACT.md §2, nothing invented):
  * reads LOCAL checkouts only — no network, no GitHub API, no token, ever
  * board/tasks/*.json + agents/*.json + bus/*.jsonl           <- src/chatcode
  * PUSHES.md + shifts/*.md                                    <- src/storage
  * PUSHES.md again for last_push fallback                     <- src/storage
  * wire/*.jsonl                                               <- THIS repo
  * S55 bench receipts (walls)                                 <- src/superocr
  * writes ONE file, deterministic for a pinned --now

Contract with its readers:
  * every list capped; order deterministic (ties broken by id/file)
  * any missing source -> that key is null once + one line in warnings
  * exit 0 when a state file was written (even degraded), 1 otherwise
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SCHEMA = 1
WINDOW_MIN = 45

CAPS = {"open": 100, "claimed": 50, "review": 50, "blocked": 50,
        "chat_tail": 40, "pushes": 30, "wire": 30, "shifts": 10, "epics": 12}

STATUSES = ("open", "claimed", "review", "blocked", "done", "dropped")
GROUP_KEYS = ("superocr", "chatcode", "storage", "storagecode", "vigil", "empire")
DEFAULT_GROUP = "chatcode"

# last_push sources: group -> repo dir under src/ (exact git HEAD committer date)
GROUP_REPO = {"superocr": "superocr", "chatcode": "chatcode",
              "storage": "storage", "storagecode": None,  # None = this repo
              "vigil": "vigil", "empire": None}

OCR_WORDS = ("OCR", "captcha", "reader", "glyph", "corrosion", "snow", "spiderweb",
             "strippy", "collage", "darts", "stitch", "split", "dark-on-dark",
             "obstruction", "deskew", "lexicon", "bench", "v7b", "recognition",
             "reader_lex")
TITLE_S = re.compile(r"\bS\d{1,2}\b|\bW[12]\b", re.I)
TITLE_OCR = re.compile(r"\b(" + "|".join(re.escape(w) for w in OCR_WORDS) + r")\b", re.I)

LAST_KNOWN_WALLS = {"easy_best": 75, "hard_best": 29, "easy_target": 98, "hard_target": 95,
                    "source": "S55 bench receipts (seed-1 75/25 x3, seed-2 75/29 x3); bars 98/95"}


# ---------------------------------------------------------------- helpers ---
def err(warnings: list, msg: str) -> None:
    warnings.append(msg)


def iso_z(t: dt.datetime) -> str:
    return t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_ts(s):
    if not isinstance(s, str) or not s:
        return None
    try:
        return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def now_from_args(args) -> dt.datetime:
    if args.now:
        t = parse_ts(args.now if args.now.endswith("Z") or "+" in args.now else args.now + "Z")
        if t is None:
            sys.stderr.write(f"bad --now {args.now!r}\n")
            sys.exit(1)
        return t
    return dt.datetime.now(dt.timezone.utc)


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def git_sha10(repo: Path):
    try:
        out = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                             capture_output=True, text=True, timeout=15, check=True)
        return out.stdout.strip()[:10] or None
    except Exception:
        return None


def git_head_iso(repo: Path):
    try:
        out = subprocess.run(["git", "-C", str(repo), "log", "-1", "--format=%cI"],
                             capture_output=True, text=True, timeout=15, check=True)
        return iso_z(parse_ts(out.stdout.strip())) if parse_ts(out.stdout.strip()) else None
    except Exception:
        return None


def clip(s, n):
    s = "" if s is None else str(s)
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 1] + "\u2026"


# ------------------------------------------------------------------ board ---
def load_cards(cc: Path, warnings):
    cards = {}
    tdir = cc / "board" / "tasks"
    if not tdir.is_dir():
        err(warnings, "chatcode board/tasks missing: board section degraded")
        return cards
    bad = 0
    for f in sorted(tdir.glob("*.json")):
        try:
            d = load_json(f)
            if isinstance(d, dict) and d.get("id"):
                cards[d["id"]] = d
        except Exception:
            bad += 1
    if bad:
        err(warnings, f"board: {bad} unparseable task file(s) skipped")
    return cards


def group_of(card: dict, cards: dict) -> str:
    tags = card.get("tags") or []
    for t in tags:
        if t in GROUP_KEYS:
            return t
    cur, seen = card, set()
    for _ in range(6):
        pid = cur.get("parent")
        if not pid or pid in seen or pid not in cards:
            break
        seen.add(pid)
        cur = cards[pid]
        for t in (cur.get("tags") or []):
            if t in GROUP_KEYS:
                return t
    title = card.get("title") or ""
    if TITLE_S.search(title) or TITLE_OCR.search(title):
        return "superocr"
    return DEFAULT_GROUP


def build_board(cards: dict, now: dt.datetime, warnings):
    counts = {s: 0 for s in STATUSES}
    unknown = set()
    for c in cards.values():
        s = c.get("status")
        if s in counts:
            counts[s] += 1
        else:
            unknown.add(str(s))
    if unknown:
        err(warnings, "board: unknown status(es) not counted: " + ", ".join(sorted(unknown)))

    def age_h(ts):
        t = parse_ts(ts)
        return round((now - t).total_seconds() / 3600, 1) if t else None

    opens, claimed, review, blocked = [], [], [], []
    for cid in sorted(cards):
        c = cards[cid]
        s = c.get("status")
        if s == "open":
            opens.append({"id": cid, "title": c.get("title", ""), "priority": c.get("priority"),
                          "tags": c.get("tags") or [], "owner": c.get("owner"),
                          "age_h": age_h(c.get("created_ts"))})
        elif s == "claimed":
            lease = c.get("lease") or {}
            claimed.append({"id": cid, "title": c.get("title", ""), "priority": c.get("priority"),
                            "owner": c.get("owner") or lease.get("agent"),
                            "lease_expires": lease.get("expires"),
                            "checkpoint": clip(lease.get("checkpoint") or c.get("checkpoint"), 240) or None})
        elif s == "review":
            review.append({"id": cid, "title": c.get("title", ""), "owner": c.get("owner"),
                           "pr": c.get("pr"), "age_h": age_h(c.get("updated_ts"))})
        elif s == "blocked":
            note = ""
            hist = c.get("history") or []
            if hist and isinstance(hist[-1], dict):
                note = hist[-1].get("note") or hist[-1].get("action") or ""
            blocked.append({"id": cid, "title": c.get("title", ""), "owner": c.get("owner"),
                            "note": clip(note, 240)})

    opens.sort(key=lambda o: (o["priority"] if o["priority"] is not None else 99,
                              -o["age_h"] if o["age_h"] is not None else 0, o["id"]))
    claimed.sort(key=lambda o: (o["priority"] if o["priority"] is not None else 99, o["id"]))
    review.sort(key=lambda o: (o["age_h"] is None, -(o["age_h"] or 0), o["id"]))
    blocked.sort(key=lambda o: o["id"])

    return ({"counts": counts,
             "open": opens[: CAPS["open"]],
             "claimed": claimed[: CAPS["claimed"]],
             "review": review[: CAPS["review"]],
             "blocked": blocked[: CAPS["blocked"]]},
            opens, review)


# ------------------------------------------------------------------- team ---
def bus_messages(cc: Path, warnings):
    msgs = []
    bdir = cc / "bus"
    if not bdir.is_dir():
        err(warnings, "chatcode bus/ missing: team last_seen falls back to roster only")
        return msgs
    files = sorted(p for p in bdir.glob("*.jsonl"))
    bad = 0
    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        m = json.loads(line)
                        if isinstance(m, dict) and m.get("ts") and m.get("from"):
                            msgs.append(m)
                    except Exception:
                        bad += 1
        except Exception:
            bad += 1
    if bad:
        err(warnings, f"bus: {bad} unparseable line(s) skipped")
    return msgs


def build_team(cc: Path, cards: dict, msgs: list, now: dt.datetime, warnings):
    adir = cc / "agents"
    agents = []
    if not adir.is_dir():
        err(warnings, "chatcode agents/ missing: team section degraded")
        return {"window_min": WINDOW_MIN, "awake": 0, "total": 0, "agents": []}, []
    last_bus = {}
    for m in msgs:
        t = parse_ts(m.get("ts"))
        name = m.get("from")
        if t and (name not in last_bus or t > last_bus[name]):
            last_bus[name] = t
    for f in sorted(adir.glob("*.json")):
        try:
            a = load_json(f)
        except Exception:
            err(warnings, f"agent file unparseable: {f.name}")
            continue
        name = a.get("name") or f.stem
        seen = parse_ts(a.get("last_seen"))
        if name in last_bus and (seen is None or last_bus[name] > seen):
            seen = last_bus[name]
        silent = round((now - seen).total_seconds() / 60) if seen else None
        leases = sum(1 for c in cards.values()
                     if c.get("owner") == name and c.get("status") in ("claimed", "blocked"))
        agents.append({"name": name, "role": a.get("role") or "worker",
                       "kind": a.get("kind") or "ai",
                       "last_seen": iso_z(seen) if seen else None,
                       "silent_min": silent,
                       "alive": bool(silent is not None and silent <= WINDOW_MIN),
                       "leases": leases})
    agents.sort(key=lambda a: (not a["alive"], a["name"]))
    section = {"window_min": WINDOW_MIN,
               "awake": sum(1 for a in agents if a["alive"]),
               "total": len(agents), "agents": agents}
    return section, [a["name"] for a in agents if not a["alive"]]


# ------------------------------------------------------------------- chat ---
def build_chat(cc: Path, msgs: list, now: dt.datetime):
    # channel lives in the file name, not the record — read the channels directly
    chat_msgs = []
    bdir = cc / "bus"
    if bdir.is_dir():
        for f in sorted(bdir.glob("*.jsonl")):
            stem = f.stem
            if stem.startswith("dm-") or not (stem == "general" or stem.startswith("human-")):
                continue
            try:
                with open(f, "r", encoding="utf-8") as fh:
                    for line in fh:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            m = json.loads(line)
                        except Exception:
                            continue
                        if isinstance(m, dict) and m.get("ts") and m.get("from"):
                            m["channel"] = stem
                            chat_msgs.append(m)
            except Exception:
                continue
    fresh = [m for m in chat_msgs if (parse_ts(m["ts"]) and
                                      (now - parse_ts(m["ts"])).total_seconds() <= 86400)]
    chat_msgs.sort(key=lambda m: (m["ts"], m.get("id") or ""))
    tail = [{"id": m.get("id") or "", "ts": m["ts"], "from": m.get("from") or "",
             "type": m.get("type") or "say", "text": clip(m.get("text"), 280)}
            for m in chat_msgs[-CAPS["chat_tail"]:]]
    return {"count_24h": len(fresh), "tail": tail}


# ---------------------------------------------------------------- records ---
def parse_pushes(st: Path, warnings):
    f = st / "PUSHES.md"
    if not f.is_file():
        err(warnings, "storage PUSHES.md missing: records.pushes empty")
        return []
    rows = []
    try:
        lines = f.read_text(encoding="utf-8").splitlines()
    except Exception:
        err(warnings, "storage PUSHES.md unreadable: records.pushes empty")
        return []
    for ln in lines:
        ln = ln.strip()
        if not ln.startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip("|").split("|")]
        if len(cells) < 5 or not re.match(r"^\d{4}-\d{2}-\d{2}$", cells[0]):
            continue
        rows.append({"date": cells[0], "agent": cells[1], "repo": cells[2],
                     "what": clip(cells[4], 280)})
    rows.reverse()  # file is chronological; newest first
    return rows


def build_records(st: Path, self_root: Path, cards: dict, now: dt.datetime, warnings):
    pushes = parse_pushes(st, warnings)
    wire = []
    wdir = self_root / "wire"
    if wdir.is_dir():
        files = sorted(wdir.glob("*.jsonl"), key=lambda p: p.name, reverse=True)[:2]
        for f in files:
            try:
                with open(f, "r", encoding="utf-8") as fh:
                    for line in fh:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            m = json.loads(line)
                        except Exception:
                            continue
                        if isinstance(m, dict) and m.get("id") and m.get("time"):
                            wire.append({"id": m["id"], "ts": m["time"],
                                         "topic": m.get("topic") or "",
                                         "message": clip(m.get("message") or m.get("title"), 200)})
            except Exception:
                err(warnings, f"wire unreadable: {f.name}")
    else:
        err(warnings, "wire/ missing: records.wire empty")
    wire.sort(key=lambda w: (w["ts"], w["id"]))
    wire = wire[-CAPS["wire"]:]
    shifts = []
    sdir = st / "shifts"
    if sdir.is_dir():
        for f in sorted(sdir.glob("*.md")):
            m = re.match(r"^(\d{4}-\d{2}-\d{2})-(.+)\.md$", f.name)
            if m and f.name != "TEMPLATE.md":
                shifts.append({"date": m.group(1), "agent": m.group(2),
                               "file": f"shifts/{f.name}"})
    shifts.sort(key=lambda s: (s["date"], s["agent"]), reverse=True)
    return {"pushes": pushes[: CAPS["pushes"]], "wire": wire,
            "shifts": shifts[: CAPS["shifts"]]}, pushes


# --------------------------------------------------------------- projects ---
def build_projects(cards: dict, now: dt.datetime, repo_pushed: dict):
    groups = {k: [] for k in GROUP_KEYS}
    for cid in sorted(cards):
        groups[group_of(cards[cid], cards)].append(cid)

    children = {}
    for cid, c in cards.items():
        pid = c.get("parent")
        if pid in cards:
            children.setdefault(pid, []).append(cid)

    projects = []
    for key in GROUP_KEYS:
        ids = groups[key]
        if not ids:
            continue
        cnt = {s: 0 for s in STATUSES}
        for cid in ids:
            s = cards[cid].get("status")
            if s in cnt:
                cnt[s] += 1
        total = len(ids)
        done = cnt["done"]
        epics = []
        for cid in ids:
            kids = children.get(cid, [])
            if not kids:
                continue
            kdone = sum(1 for k in kids if cards[k].get("status") == "done")
            epics.append({"id": cid, "title": clip(cards[cid].get("title"), 120),
                          "done": kdone, "total": len(kids)})
        epics.sort(key=lambda e: (-e["total"], e["id"]))
        last_push = repo_pushed.get(key)
        if key == "empire":
            last_push = max((v for v in repo_pushed.values() if v), default=None)
        elif last_push is None and key == "vigil":
            pass  # filled by caller from pushes dates when src/vigil is absent
        projects.append({"key": key,
                         "title": {"superocr": "SUPEROCR \u2014 the OCR war",
                                   "chatcode": "CHATCODE \u2014 the room",
                                   "storage": "STORAGE \u2014 the ledger",
                                   "storagecode": "STORAGECODE \u2014 the vaults",
                                   "vigil": "VIGIL \u2014 the watchtower",
                                   "empire": "EMPIRE \u2014 maintenance & cross-cutting"}[key],
                         "open": cnt["open"], "claimed": cnt["claimed"], "review": cnt["review"],
                         "done": done, "total": total,
                         "progress": round(done / total, 3) if total else 0.0,
                         "epics": epics[: CAPS["epics"]],
                         "last_push": last_push})
    projects.sort(key=lambda p: (-p["total"], p["key"]))
    return projects


# ------------------------------------------------------------------ walls ---
def build_walls(sp: Path, warnings):
    receipts = []
    rdir = sp / "reports"
    if rdir.is_dir():
        for f in sorted(rdir.glob("s55-bench-*/*.json")):
            try:
                d = load_json(f)
            except Exception:
                continue
            suites = d.get("suites") if isinstance(d, dict) else None
            if isinstance(suites, dict) and isinstance(suites.get("easy"), dict) and \
               isinstance(suites.get("hard"), dict):
                receipts.append((d.get("finished_ts") or "", f, d))
    if not receipts:
        err(warnings, "walls: no S55 bench receipts found; kept last known values")
        return dict(LAST_KNOWN_WALLS)
    easy = max(d["suites"]["easy"].get("correct") or 0 for _, _, d in receipts)
    hard = max(d["suites"]["hard"].get("correct") or 0 for _, _, d in receipts)
    bars = (receipts[-1][2].get("bars") or {})
    fams = sorted({f.parent.name for _, f, _ in receipts})
    return {"easy_best": easy, "hard_best": hard,
            "easy_target": bars.get("easy", LAST_KNOWN_WALLS["easy_target"]),
            "hard_target": bars.get("hard", LAST_KNOWN_WALLS["hard_target"]),
            "source": f"{', '.join(fams)} (max over all runs; bars from the newest receipt)"}


# ------------------------------------------------------------------- main ---
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Vigil state compiler (CONTRACT.md schema v1)")
    ap.add_argument("--out", required=True, help="output path, e.g. app/state.json")
    ap.add_argument("--src-root", default="src", help="dir holding chatcode/superocr/storage[/vigil] (default ./src)")
    ap.add_argument("--self-root", default=None, help="storagecode checkout root (default: two levels above this file)")
    ap.add_argument("--now", default=None, help="pin the clock (ISO) for byte-identical reruns")
    args = ap.parse_args(argv)

    now = now_from_args(args)
    src = Path(args.src_root).resolve()
    self_root = Path(args.self_root).resolve() if args.self_root else Path(__file__).resolve().parents[1]
    cc, sp, st = src / "chatcode", src / "superocr", src / "storage"

    warnings = []
    for name, p in (("chatcode", cc), ("superocr", sp), ("storage", st)):
        if not p.is_dir():
            err(warnings, f"{name} checkout missing at {p}: dependent sections degraded")

    git = {}
    for repo, p in (("chatcode", cc), ("superocr", sp), ("storage", st)):
        git[repo] = git_sha10(p) if p.is_dir() else None
    git["storagecode"] = git_sha10(self_root)

    cards = load_cards(cc, warnings)
    board, open_cards, review_cards = build_board(cards, now, warnings)

    msgs = bus_messages(cc, warnings)
    team, silent = build_team(cc, cards, msgs, now, warnings)

    chat = build_chat(cc, msgs, now)

    records, pushes = build_records(st, self_root, cards, now, warnings)

    repo_pushed = {}
    for key, repo in GROUP_REPO.items():
        if repo is None:
            repo_pushed[key] = git_head_iso(self_root) if key == "storagecode" else None
        else:
            p = src / repo
            repo_pushed[key] = git_head_iso(p) if p.is_dir() else None
    # vigil fallback: newest PUSHES.md date for repo 'vigil'
    if not (src / "vigil").is_dir():
        vd = next((r["date"] for r in pushes if r["repo"] == "vigil"), None)
        repo_pushed["vigil"] = f"{vd}T00:00:00Z" if vd else None
    projects = build_projects(cards, now, repo_pushed)

    walls = build_walls(sp, warnings)

    ids = set(cards)
    flags = {"silent_agents": silent,
             "review_stuck": [r["id"] for r in review_cards if (r["age_h"] or 0) > 24],
             "blocked_over_24h": [b["id"] for b in board["blocked"]
                                  if b["id"] in ids and
                                  (lambda t: t and (now - t).total_seconds() > 86400)(
                                      parse_ts(cards[b["id"]].get("updated_ts")))]}

    state = {"schema": SCHEMA, "generated_ts": iso_z(now), "warnings": warnings,
             "git": git, "board": board, "team": team, "chat": chat,
             "records": records, "projects": projects, "walls": walls, "flags": flags}

    out = Path(args.out)
    try:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(state, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    except Exception as exc:  # catastrophic
        sys.stderr.write(f"build_state: cannot write {out}: {exc}\n")
        return 1
    sys.stderr.write(f"build_state: wrote {out} ({out.stat().st_size} bytes, "
                     f"{len(cards)} cards, {team['total']} agents, "
                     f"{len(warnings)} warning(s))\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
