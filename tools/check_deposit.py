#!/usr/bin/env python3
"""Deposit validator for the warehouse (task t-20261014-b5b4).

    python3 tools/check_deposit.py [data-root]      # default: <repo>/data

Rules, exactly as the warehouse keeps them:

  1. every directory under ``data/<project>/`` is a deposit dir named
     ``<date>-<agent>`` with an optional ``-<suffix>`` tail, i.e.
     ``YYYY-MM-DD`` + ``-`` + kebab segments (agent first, then any
     discriminator such as ``-2`` or ``-pipeline``);
  2. every deposit dir is covered by at least one row in
     ``data/INDEX.md`` whose date, project and agent cells all match the
     dir (several rows may map to one dir when deposits stack the same day);
  3. when coverage is absent the validator prints a paste-ready INDEX row
     so the fix is mechanical.

Exit codes: 0 = clean, 1 = validation failures (every reason printed),
2 = usage error (missing root etc.). Reads each file once; never writes.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import re
import sys
from pathlib import Path

DIR_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)$")


def fail(msg: str) -> None:
    print(f"  {msg}")


def parse_index(index_path: Path) -> set[tuple[str, str, str]]:
    """(date, project, agent) triples covered by data/INDEX.md rows."""
    covered: set[tuple[str, str, str]] = set()
    if not index_path.is_file():
        return covered
    for line in index_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3 or cells[0] in ("date", "---", ":---"):
            continue
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", cells[0]):
            continue
        covered.add((cells[0], cells[1], cells[2]))
    return covered


# Enforced from the day the rule was written, i.e. it applies to the deposits being made now —
# including mine. A rule that starts tomorrow, protecting nobody's work, is decoration.
POLICY_SINCE = dt.date(2026, 10, 27)


def _deposit_date(dep: Path):
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", dep.name)
    return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


def verify_manifest(dep: Path) -> list[str]:
    """A deposit's SHA256SUMS must cover it exactly, and every digest must match. Found by my own deposit.

    The archive is the ONLY copy that survives a force-push or a repo rewrite (STORAGE_POLICY), so a deposit
    whose `sha256sum -c` fails is not evidence — it is a story about evidence. My pass-2 directory shipped
    broken for eleven minutes because the writer emitted SHA256SUMS before the README, so the manifest hashed
    a file it did not yet contain and `-c` died on the one line a reviewer is sure to run. Order of writes in
    a generator is exactly the kind of thing a machine must check.

    Scoped deliberately, because the tool's own suite is the contract (F15/F20, agency): an EMPTY deposit is
    not this check's business (the fixtures build empty dirs and expect green) and the 16 legacy archives that
    have files but no manifest are a POLICY question for the Director, not a surprise to drop on an already-red
    CI — so a missing manifest on a non-empty deposit is counted and reported separately, never as a problem.
    """
    out: list[str] = []
    man = dep / "SHA256SUMS"
    files = sorted(f for f in dep.rglob("*") if f.is_file() and f.name != "SHA256SUMS")
    enforced = (_deposit_date(dep) or POLICY_SINCE) >= POLICY_SINCE
    if not enforced:
        # Pre-policy deposit: count the gaps for the NOTE, do not fail the gate on them. Its SHA256SUMS may
        # legitimately describe a different tree (nordbahnhof lists 136 files that are not in its own
        # directory) — worth telling a human once, not worth 136 lines that bury the 16 real ones.
        try:
            listed = {l.split("  ", 1)[1] for l in man.read_text(encoding="utf-8").splitlines()
                      if "  " in l} if man.is_file() else set()
        except Exception:
            listed = set()
        on_disk = {f.relative_to(dep).as_posix() for f in files}
        missing = len(listed - on_disk)
        extra = len(on_disk - listed)
        if missing or extra:
            LEGACY_GAPS.append((dep.name, missing, extra))
        return []
    if not man.is_file():
        if not files or not enforced:
            return []
        return [f"{dep.name}: no SHA256SUMS for {len(files)} file(s) — an archive nobody can verify"]
    if not files:
        return []                                            # a placeholder dir; nothing to verify yet
    lines = [l for l in man.read_text(encoding="utf-8").splitlines() if l.strip()]
    listed: dict[str, str] = {}
    for l in lines:
        m = re.match(r"^([0-9a-f]{64})  (.+)$", l)      # exactly the two-space form sha256sum writes
        if not m:
            out.append(f"{dep.name}: SHA256SUMS line not in '<digest>  <path>' form: {l[:70]!r}")
            continue
        if m.group(2) in listed:
            out.append(f"{dep.name}: {m.group(2)} listed twice (which digest is the real one?)")
        listed[m.group(2)] = m.group(1)
    for rel, digest in sorted(listed.items()):
        f = dep / rel
        if not f.is_file():
            out.append(f"{dep.name}: SHA256SUMS lists {rel} but the file is not in the deposit")
        elif hashlib.sha256(f.read_bytes()).hexdigest() != digest:
            out.append(f"{dep.name}: {rel} does not match SHA256SUMS (record corrupted or file rewritten)")
    unlisted = [f.relative_to(dep).as_posix() for f in files if f.relative_to(dep).as_posix() not in listed]
    if unlisted:
        detail = (f"{dep.name}: {rel_missing(unlisted)} in SHA256SUMS (sha256sum -c will not verify "
                  f"{'them' if len(unlisted) > 1 else 'it'}, or worse: the manifest was written before the "
                  f"file)") if enforced else ""
        if enforced:
            out.append(detail)
    return out


LEGACY_UNLISTED: list[tuple] = []        # filled while checking, reported as ONE line, not as 100
LEGACY_GAPS: list[tuple] = []            # (deposit, files listed-but-absent, files present-but-unlisted)


def rel_missing(names: list[str]) -> str:
    return (", ".join(names[:3] + [f"(+{len(names) - 3} more)"] if len(names) > 3 else names)) + " not listed"


def check(root: Path) -> list[str]:
    problems: list[str] = []
    index = root / "INDEX.md"
    covered = parse_index(index)
    if not index.is_file():
        problems.append(f"missing index: {index} — no deposit can be covered")
    LEGACY_UNLISTED.clear()
    projects = sorted(p for p in root.iterdir() if p.is_dir()) if root.is_dir() else []
    for project in projects:
        for dep in sorted(p for p in project.iterdir() if p.is_dir()):
            m = DIR_RE.match(dep.name)
            if not m:
                problems.append(
                    f"bad deposit name: {project.name}/{dep.name} — expected "
                    "<YYYY-MM-DD>-<agent>(-<suffix>)")
                continue
            y, mo, d, rest = m.groups()
            try:
                dt.date(int(y), int(mo), int(d))
            except ValueError:
                problems.append(f"bad calendar date in dir name: {project.name}/{dep.name}")
                continue
            date_s = f"{y}-{mo}-{d}"
            agent = rest.split("-")[0]
            key = (date_s, project.name, agent)
            problems.extend(verify_manifest(dep))
            if key not in covered:  # (manifest problems, if any, are already in `problems`)
                problems.append(
                    f"no INDEX.md row covers {project.name}/{dep.name} — paste-ready row:\n"
                    f"    | {date_s} | {project.name} | {agent} | <what was deposited> | - |")
    if LEGACY_GAPS:
        lm = sum(m for _, m, _ in LEGACY_GAPS)
        le = sum(e for _, _, e in LEGACY_GAPS)
        print(f"check_deposit: NOTE — {len(LEGACY_GAPS)} pre-{POLICY_SINCE} deposit(s) have manifests that "
              f"disagree with their own contents ({lm} listed-but-absent, {le} present-but-unlisted); not "
              f"failed, because the rule starts at {POLICY_SINCE} and 136 lines from one archive would bury "
              f"the real problems. Fixing them is the Director's call: `sha256sum -c` in each directory.")
    if LEGACY_UNLISTED:
        n = sum(c for _, c in LEGACY_UNLISTED)
        print(f"check_deposit: NOTE — {len(LEGACY_UNLISTED)} pre-{POLICY_SINCE} deposit(s) hold {n} file(s) "
              f"their SHA256SUMS does not list, and {LEGACY_COUNT_HINT}; completeness is enforced only for "
              f"deposits dated {POLICY_SINCE} or later, because 100 new failures on an already-red gate gets "
              f"ignored rather than fixed (and the retroactive rule is the Director's to set, not mine)")
    return problems


LEGACY_COUNT_HINT = "see git log -- tools/check_deposit.py for the rule"


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parents[1] / "data"
    if not root.is_dir():
        print(f"check_deposit: no such data root: {root}", file=sys.stderr)
        return 2
    problems = check(root)
    if problems:
        print(f"check_deposit: FAIL ({len(problems)} problem(s)):")
        for p in problems:
            print(f"  {p}")
        return 1
    print(f"check_deposit: OK ({root})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
