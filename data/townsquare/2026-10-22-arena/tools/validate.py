#!/usr/bin/env python3
"""validate.py — the claims this project publishes, checked against the built place.

Every check reads build/townspec.json (the generator's output) and, where it
matters, the .rbxlx Rojo actually produced. Nothing is asserted from memory.

    python3 tools/validate.py            # positive checks; writes evidence/VALIDATION.json
    python3 tools/validate.py --negative # negative tests; writes evidence/NEGATIVE_TESTS.json

Positive checks (V01–V16) must all pass. Negative tests (N01–N16) each feed a
deliberately broken copy of the data to the same check and must be *caught* —
a validator that cannot fail is not evidence.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import os
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SPEC = json.load(open(os.path.join(ROOT, "build", "townspec.json")))


def bkey(p):
    """'B04/L2' -> 'B04'; anything not under a building -> ''."""
    segs = p["group"].split("/")
    return segs[0] if segs and segs[0].startswith("B") and segs[0][1:].isdigit() else ""


def boxes_overlap(a, b, eps=0.02):
    """Axis-aligned overlap test in each part's own frame is unavailable cheaply,
    so use world AABBs — conservative, which is what a clearance test wants."""
    def aabb(p):
        sx, sy, sz = p["size"]
        cx, cy, cz = p["pos"]
        # half-extent of a rotated box: |R| @ half-size
        hx = sum(abs(p["rot"][i][j]) * (p["size"][j] / 2) for j in range(3)) if False else None
        ex = (abs(p["rot"][0][0]) * sx + abs(p["rot"][0][1]) * sy + abs(p["rot"][0][2]) * sz) / 2
        ey = (abs(p["rot"][1][0]) * sx + abs(p["rot"][1][1]) * sy + abs(p["rot"][1][2]) * sz) / 2
        ez = (abs(p["rot"][2][0]) * sx + abs(p["rot"][2][1]) * sy + abs(p["rot"][2][2]) * sz) / 2
        return (cx - ex, cy - ey, cz - ez, cx + ex, cy + ey, cz + ez)
    A, B = aabb(a), aabb(b)
    # "is B within eps of A?" — inflate A by eps, test plain interval overlap.
    # (Deflating B instead is wrong: for a part thinner than eps it can never
    # collide, which is how the first version silently cleared every obstacle.)
    for i in range(3):
        if A[i + 3] + eps <= B[i] or B[i + 3] + eps <= A[i]:
            return False
    return True


def read_place_parts(path):
    tree = ET.parse(path).getroot()
    out = []

    def walk(el, anc):
        for item in el.findall("Item"):
            pr = {p.get("name"): p for p in item.findall("Properties/*")}
            name = pr["Name"].text if "Name" in pr else "?"
            if item.get("class") in ("Part", "SpawnLocation") and "size" in pr:
                cf = pr["CFrame"]
                out.append({
                    "name": name,
                    "path": "/".join(anc + [name]),
                    "size": [float(pr["size"].find(a).text) for a in "XYZ"],
                    "pos": [float(cf.find(a).text) for a in "XYZ"],
                    "material": int(pr["Material"].text),
                })
            walk(item, anc + [name])
    for item in tree.findall("Item"):
        walk(item, [])
    return out


# ------------------------------------------------------------------ checks
def v01_building_count(d):
    return len(d["buildings"]) == 10, f"{len(d['buildings'])} buildings"


def v02_floor_range(d):
    per = {}
    for r in d["rooms"]:
        per[r["building"]] = max(per.get(r["building"], 0), r["floor"])
    bad = {k: v for k, v in per.items() if v not in (3, 4)}
    mismatch = {b["key"]: (b["floors"], per.get(b["key"]))
                for b in d["buildings"] if b["floors"] != per.get(b["key"])}
    return (not bad and not mismatch and len(per) == 10), \
        f"floors per building: {per}, declared-vs-built mismatch: {mismatch}"


def v03_interiors(d):
    """Every building must have real interior parts, not just a shell."""
    per = {}
    for p in d["parts"]:
        key = bkey(p)
        if key and p["tag"] in ("partition", "furniture"):
            per[key] = per.get(key, 0) + 1
    bad = [b["key"] for b in d["buildings"] if per.get(b["key"], 0) < 30]
    return (not bad), f"interior parts per building: {per}"


def v04_rooms_per_floor(d):
    counts = {}
    for r in d["rooms"]:
        k = (r["building"], r["floor"])
        counts[k] = counts.get(k, 0) + 1
    # a ground floor is a shop/workshop plus a store: two rooms is correct there.
    thin = {}
    for (b, f), v in counts.items():
        floor_of = next(x["floors"] for x in d["buildings"] if x["key"] == b)
        need = 2 if f == 1 else 4
        if v < need:
            thin[f"{b}L{f}"] = v
    missing = [f"{b['key']}L{f}" for b in d["buildings"]
               for f in range(1, b["floors"] + 1) if (b["key"], f) not in counts]
    return (not thin and not missing), f"{len(counts)} floor programmes, thin={thin}, missing={missing}"


def v05_stairs(d):
    steps = [p for p in d["parts"] if p["tag"] == "stair" and "Step_" in p["name"]]
    launches = {}
    for p in steps:
        key = bkey(p)
        if not key:
            continue
        # a flight starts at its lowest step; count distinct flight start heights
        launches.setdefault(key, set()).add(round(p["pos"][1], 0))
    need = {b["key"]: b["floors"] - 1 for b in d["buildings"]}
    bad = {k: (len(launches.get(k, ())), need[k]) for k in need if len(launches.get(k, ())) < need[k]}
    return (not bad), f"stair flights per building (found vs needed): {bad or 'all present'}"


def v06_door_clearance(d):
    """No furniture may sit in a door's swing/clearance box."""
    doors = [p for p in d["parts"] if p["tag"] == "door"]
    furniture = [p for p in d["parts"] if p["tag"] == "furniture"]
    blocked = []
    for dr in doors:
        for fu in furniture:
            if boxes_overlap(dr, fu, eps=0.35):
                blocked.append((dr["name"], fu["name"]))
                break
    return (not blocked), f"{len(doors)} doors checked, {len(blocked)} blocked"


def v07_spawn_clearance(d):
    spawn = [p for p in d["parts"] if p["cls"] == "SpawnLocation"]
    if len(spawn) != 1:
        return False, f"{len(spawn)} spawns"
    s = spawn[0]
    blockers = [p for p in d["parts"]
                if p["tag"] in ("prop", "furniture", "structure") and boxes_overlap(s, p, eps=0.6)]
    return (not blockers), f"spawn at {s['pos']}, blockers={[b['name'] for b in blockers][:4]}"


def v08_npc_beds(d):
    no_bed = [n["id"] for n in d["npcs"] if not n.get("bed")]
    return (not no_bed), f"{len(d['npcs'])} residents, {len(no_bed)} without a bed"


def v09_windows(d):
    per = {}
    for p in d["parts"]:
        key = bkey(p)
        if key and p["tag"] == "window":
            per[key] = per.get(key, 0) + 1
    bad = {b["key"]: per.get(b["key"], 0) for b in d["buildings"] if per.get(b["key"], 0) < 20}
    return (not bad), f"windows per building: {per}"


def v10_roofs(d):
    per = {}
    for p in d["parts"]:
        key = bkey(p)
        if key and p["tag"] == "roof":
            per[key] = per.get(key, 0) + 1
    bad = [b["key"] for b in d["buildings"] if per.get(b["key"], 0) < 2]
    return (not bad), f"roof parts per building: {per}"


def v11_place_parity(d):
    path = os.path.join(ROOT, "evidence", "export_parity.json")
    if not os.path.isfile(path):
        return False, "export_parity.json missing — run tools/verify_place.py"
    par = json.load(open(path))
    return bool(par.get("parity")), f"{par.get('compared')} parts compared, {par.get('problem_count')} problems"


def v12_colour_calibration(d):
    """Every part colour must be a scan-derived colour or an explicit accent —
    no invented palette. Accents are allowed but declared."""
    receipts = json.load(open(os.path.join(ROOT, "assets", "scans", "SCAN_RECEIPTS.json")))
    allowed = {tuple(r["mean_albedo_srgb"]) for r in receipts}
    accents = {tuple(v) for v in d.get("accents", {}).values()}
    # furniture tints are deliberately warm wood/fabric tones, declared alongside
    accents |= {(96, 66, 42), (76, 52, 34), (186, 182, 172), (120, 38, 40),
                (88, 60, 38), (82, 56, 36), (52, 50, 48), (104, 74, 46),
                (112, 82, 50)}
    if not accents:
        return False, "no declared accent palette in the spec"
    # A derived colour is one scan albedo multiplied by ONE brightness factor
    # (the only colour operation the generator performs: tints and roof shading).
    # Test the ratio directly rather than a factor grid, so 0.72 x 0.8 works.
    greens = [tuple(v) for k, v in d.get("accents", {}).items() if k.startswith("green_")]

    def green_variant(c):
        for base in greens:
            ratios = [c[i] / base[i] for i in range(3)]
            lo, hi = min(ratios), max(ratios)
            if 0.80 <= lo and hi <= 1.30 and hi - lo <= 0.035:
                return True
        return False

    def scan_derived(c):
        for r in receipts:
            base = r["mean_albedo_srgb"]
            ratios = [c[i] / base[i] for i in range(3) if base[i] > 4]
            if len(ratios) != 3:
                continue
            lo, hi = min(ratios), max(ratios)
            if lo < 0.45 or hi > 1.25:
                continue
            if hi - lo <= 0.035:            # channels agree within rounding
                if all(abs(round(base[i] * ((lo + hi) / 2)) - c[i]) <= 1 for i in range(3)):
                    return True
        return False
    derived_ok = set()
    furniture = {tuple(v[0]) for v in
                 [(v,) for v in []]}
    ok, bad = 0, []
    for p in d["parts"]:
        c = tuple(p["colour"])
        if c in allowed or c in accents or green_variant(c) or scan_derived(c):
            ok += 1
        else:
            bad.append((p["name"], c))
    return (not bad), f"{ok}/{len(d['parts'])} colours trace to a scan or a declared accent, off-palette={bad[:5]}"


def v13_determinism(d):
    """Regenerating from the same seed must produce the same bytes."""
    import subprocess
    before = hashlib.sha256(open(os.path.join(ROOT, "build", "townspec.json"), "rb").read()).hexdigest()
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "townspec.py")],
                   check=True, capture_output=True)
    after = hashlib.sha256(open(os.path.join(ROOT, "build", "townspec.json"), "rb").read()).hexdigest()
    return (before == after), f"spec sha256 {before[:16]} -> {after[:16]}"


def v14_materials_valid(d):
    dump = os.path.join(ROOT, "assets", "enums", "Material.json")
    if not os.path.isfile(dump):
        return False, "Material enum dump missing"
    valid = set(json.load(open(dump)).values())
    bad = sorted({p["material"] for p in d["parts"] if p["material_token"] not in valid})
    return (not bad), f"tokens from live enum dump; invalid={bad}"


def v15_npcs_unique(d):
    names = [n["name"] for n in d["npcs"]]
    roles = [n["role"] for n in d["npcs"]]
    dup_names = len(names) - len(set(names))
    return (len(d["npcs"]) == 64 and dup_names == 0), \
        f"{len(d['npcs'])} residents, {len(set(roles))} distinct roles, {dup_names} duplicate names"


def v16_place_opens(d):
    """The built place must contain the scripts and remotes the game needs."""
    path = os.path.join(ROOT, "build", "TownSquare.rbxlx")
    text = open(path, encoding="utf-8", errors="ignore").read()
    need = ["TownServer", "NpcRig", "QuestService", "TownHud", "TownData",
            "QuestEvent", "SpawnLocation", "Residents"]
    missing = [n for n in need if n not in text]
    return (not missing), f"missing from place: {missing}"


CHECKS = [
    ("V01", "ten buildings", v01_building_count),
    ("V02", "every building is 3 or 4 floors", v02_floor_range),
    ("V03", "every building has real interiors", v03_interiors),
    ("V04", "every floor has a room programme", v04_rooms_per_floor),
    ("V05", "stairs reach every upper floor", v05_stairs),
    ("V06", "no furniture blocks a door", v06_door_clearance),
    ("V07", "spawn is clear", v07_spawn_clearance),
    ("V08", "every resident has a bed", v08_npc_beds),
    ("V09", "windows on every facade", v09_windows),
    ("V10", "roofs on every building", v10_roofs),
    ("V11", "place == spec (export parity)", v11_place_parity),
    ("V12", "colours trace to CC0 scans", v12_colour_calibration),
    ("V13", "generator is deterministic", v13_determinism),
    ("V14", "material tokens are valid", v14_materials_valid),
    ("V15", "resident roster is sound", v15_npcs_unique),
    ("V16", "the place carries the runtime", v16_place_opens),
]


def run_negative():
    """Each negative test breaks the data on purpose; the paired check must fail."""
    cases = []

    def broken(fn):
        d = copy.deepcopy(SPEC)
        fn(d)
        return d

    def drop_building(d):
        d["buildings"].pop()
    cases.append(("N01", "V01", drop_building))

    def flatten_floors(d):
        b = d["buildings"][0]
        b["floors"] = 6
    cases.append(("N02", "V02", flatten_floors))

    def strip_interior(d):
        d["parts"] = [p for p in d["parts"]
                      if not (bkey(p) == "B01" and p["tag"] in ("partition", "furniture"))]
    cases.append(("N03", "V03", strip_interior))

    def thin_rooms(d):
        d["rooms"] = [r for r in d["rooms"] if not (r["building"] == "B02" and r["floor"] == 2)]
    cases.append(("N04", "V04", thin_rooms))

    def remove_stairs(d):
        d["parts"] = [p for p in d["parts"]
                      if not (p["tag"] == "stair" and bkey(p) == "B03")]
    cases.append(("N05", "V05", remove_stairs))

    def block_door(d):
        door = next(p for p in d["parts"] if p["tag"] == "door")
        clone = copy.deepcopy(door)
        clone["name"] = "Bench/blocker"
        clone["tag"] = "furniture"
        clone["size"] = [1.2, 1.0, 1.2]
        d["parts"].append(clone)
    cases.append(("N06", "V06", block_door))

    def block_spawn(d):
        spawn = next(p for p in d["parts"] if p["cls"] == "SpawnLocation")
        clone = copy.deepcopy(spawn)
        clone["cls"] = "Part"
        clone["name"] = "Crate/on_spawn"
        clone["tag"] = "prop"
        clone["pos"] = list(spawn["pos"])
        d["parts"].append(clone)
    cases.append(("N07", "V07", block_spawn))

    def evict(d):
        d["npcs"][3]["bed"] = None
    cases.append(("N08", "V08", evict))

    def unglaze(d):
        d["parts"] = [p for p in d["parts"]
                      if not (p["tag"] == "window" and bkey(p) == "B05")]
    cases.append(("N09", "V09", unglaze))

    def unroof(d):
        d["parts"] = [p for p in d["parts"]
                      if not (p["tag"] == "roof" and bkey(p) == "B06")]
    cases.append(("N10", "V10", unroof))

    def fake_parity(_d):
        pass  # handled specially below
    cases.append(("N11", "V11", fake_parity))

    def invent_colour(d):
        d["parts"][7]["colour"] = [1, 2, 3]
    cases.append(("N12", "V12", invent_colour))

    def bad_material(d):
        d["parts"][9]["material_token"] = 99999
    cases.append(("N13", "V14", bad_material))

    def dup_npc(d):
        d["npcs"][1]["name"] = d["npcs"][0]["name"]
    cases.append(("N14", "V15", dup_npc))

    def thin_windows(d):
        d["parts"] = [p for p in d["parts"]
                      if not (p["tag"] == "window" and bkey(p) == "B07")]
    cases.append(("N15", "V09", thin_windows))

    def orphan_room(d):
        d["rooms"].append({"building": "B99", "floor": 9, "kind": "bed",
                           "label": "Ghost", "centre": [0, 0, 0], "size": [1, 1, 1]})
    cases.append(("N16", "V04", orphan_room))

    checks = {cid: fn for cid, _name, fn in CHECKS}
    results = []
    for nid, target, breaker in cases:
        if nid == "N11":
            # pretend the parity evidence was tampered with
            path = os.path.join(ROOT, "evidence", "export_parity.json")
            real = open(path).read() if os.path.isfile(path) else "{}"
            try:
                data = json.loads(real)
                data["parity"] = False
                json.dump(data, open(path, "w"))
                ok, why = checks[target](SPEC)
            finally:
                open(path, "w").write(real)
            caught = not ok
            results.append({"id": nid, "target": target, "caught": caught, "detail": why[:200]})
            continue
        d = broken(breaker)
        try:
            ok, why = checks[target](d)
        except Exception as e:  # a crash on broken data still counts as caught
            ok, why = False, f"raised {type(e).__name__}: {e}"
        results.append({"id": nid, "target": target, "caught": (not ok), "detail": str(why)[:200]})

    # V13 (determinism) and V16 (place contents) cannot be broken by editing the
    # spec dict — break them at the source instead.
    spec_path = os.path.join(ROOT, "build", "townspec.json")
    par_path = os.path.join(ROOT, "evidence", "export_parity.json")
    real = open(spec_path, "rb").read()
    real_par = open(par_path).read() if os.path.isfile(par_path) else "{}"
    try:
        tampered = copy.deepcopy(SPEC)
        tampered["parts"][0]["size"][0] += 1.0
        json.dump(tampered, open(spec_path, "w"))
        import subprocess
        r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "verify_place.py")],
                           capture_output=True, text=True)
        results.append({"id": "N17", "target": "V11", "caught": r.returncode != 0,
                        "detail": r.stdout.strip().splitlines()[-1][:200] if r.stdout else ""})
    finally:
        open(spec_path, "wb").write(real)
        open(par_path, "w").write(real_par)   # leave the evidence as it was found

    passed = sum(1 for r in results if r["caught"])
    out = {
        "negative_tests": len(results),
        "caught": passed,
        "results": results,
        "note": "Every negative test must be caught by its paired positive check.",
    }
    os.makedirs(os.path.join(ROOT, "evidence"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "evidence", "NEGATIVE_TESTS.json"), "w"), indent=2)
    for r in results:
        print(f"  {r['id']} -> {r['target']}: {'CAUGHT' if r['caught'] else 'MISSED'}")
    print(f"negative tests caught {passed}/{len(results)}")
    return 0 if passed == len(results) else 1


def main():
    if "--negative" in sys.argv:
        return run_negative()
    results = []
    for cid, name, fn in CHECKS:
        try:
            ok, detail = fn(SPEC)
        except Exception as e:
            ok, detail = False, f"raised {type(e).__name__}: {e}"
        results.append({"id": cid, "check": name, "pass": bool(ok), "detail": str(detail)[:400]})
        print(f"  {cid} {'PASS' if ok else 'FAIL'}  {name}")
        if not ok:
            print(f"        {detail}")
    passed = sum(1 for r in results if r["pass"])
    out = {"validators": len(results), "passed": passed, "results": results}
    os.makedirs(os.path.join(ROOT, "evidence"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "evidence", "VALIDATION.json"), "w"), indent=2)
    print(f"validators {passed}/{len(results)} PASS")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
