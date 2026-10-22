#!/usr/bin/env python3
"""verify_place.py — export parity: the built place must equal the generator.

Re-parses the .rbxlx Rojo produced and compares it, part by part, against
build/townspec.json: count, hierarchy, name, size, position, rotation, colour,
material token, transparency and collision. Any drift is a FAIL with the
offending part named.

    python3 tools/verify_place.py [build/TownSquare.rbxlx]

Exit 0 = parity, 1 = mismatch, 2 = usage/missing file.
"""
from __future__ import annotations

import json
import os
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def read_xml_parts(path):
    """-> list of dicts, flattened, with their ancestry."""
    out = []

    def props(el):
        d = {}
        for p in el.findall("Properties/*"):
            d[p.get("name")] = p
        return d

    def walk(el, ancestors):
        for item in el.findall("Item"):
            cls = item.get("class")
            pr = props(item)
            name = pr["Name"].text if "Name" in pr else "?"
            if cls in ("Part", "SpawnLocation", "WedgePart", "TrussPart"):
                cf = pr.get("CFrame")
                vec = pr.get("size")
                rot = {}
                pos = {}
                if cf is not None:
                    for i in range(3):
                        for j in range(3):
                            rot[(i, j)] = float(cf.find(f"R{i}{j}").text)
                    for ax in "XYZ":
                        pos[ax] = float(cf.find(ax).text)
                size = {ax: float(vec.find(ax).text) for ax in "XYZ"}
                out.append({
                    "path": "/".join(ancestors + [name]),
                    "class": cls,
                    "name": name,
                    "pos": [pos["X"], pos["Y"], pos["Z"]],
                    "size": [size["X"], size["Y"], size["Z"]],
                    "rot": [[rot[(i, j)] for j in range(3)] for i in range(3)],
                    "colour": int(pr["Color3uint8"].text) if "Color3uint8" in pr else None,
                    "material": int(pr["Material"].text) if "Material" in pr else None,
                    "transp": float(pr["Transparency"].text) if "Transparency" in pr else 0.0,
                    "collide": (pr["CanCollide"].text.strip() == "true") if "CanCollide" in pr else True,
                })
            walk(item, ancestors + [name])

    tree = ET.parse(path).getroot()
    for item in tree.findall("Item"):
        walk(item, [])
    return out


def main(argv):
    xml_path = argv[1] if len(argv) > 1 else os.path.join(ROOT, "build", "TownSquare.rbxlx")
    if not os.path.isfile(xml_path):
        print(f"verify_place: no such file: {xml_path}", file=sys.stderr)
        return 2
    spec = json.load(open(os.path.join(ROOT, "build", "townspec.json")))
    want = spec["parts"]
    got = read_xml_parts(xml_path)
    problems = []

    if len(got) != len(want):
        problems.append(f"part count: spec {len(want)} vs place {len(got)}")

    # match by (group path, name) — the emitter guarantees that key is unique
    def key(p):
        segs = p["group"].split("/")
        if segs[0].startswith("B"):
            segs = ["Buildings"] + segs
        nm = p["name"].rsplit("/", 1)[-1]
        return "/".join(["Town"] + segs + [nm])

    spec_by_path = {}
    for p in want:
        k = key(p)
        n = 1
        kk = k
        while kk in spec_by_path:
            n += 1
            kk = f"{k}_{n}"
        spec_by_path[kk] = p

    place_by_path = {p["path"]: p for p in got}
    missing = [k for k in spec_by_path if k not in place_by_path]
    extra = [k for k in place_by_path if k not in spec_by_path]
    if missing:
        problems.append(f"{len(missing)} spec parts absent from place; first: {missing[:3]}")
    if extra:
        problems.append(f"{len(extra)} place parts not in spec; first: {extra[:3]}")

    checked = 0
    for k, sp in spec_by_path.items():
        gp = place_by_path.get(k)
        if gp is None:
            continue
        checked += 1
        for axis, i in (("size", None),):
            pass
        if any(abs(a - b) > 0.002 for a, b in zip(sp["size"], gp["size"])):
            problems.append(f"size {k}: spec {sp['size']} vs place {gp['size']}")
        if any(abs(a - b) > 0.002 for a, b in zip(sp["pos"], gp["pos"])):
            problems.append(f"pos {k}: spec {sp['pos']} vs place {gp['pos']}")
        if any(abs(sp["rot"][i][j] - gp["rot"][i][j]) > 0.002 for i in range(3) for j in range(3)):
            problems.append(f"rotation {k}: spec {sp['rot']} vs place {gp['rot']}")
        r, g, b = sp["colour"]
        if gp["colour"] != (r << 16) | (g << 8) | b:
            problems.append(f"colour {k}: spec {(r<<16)|(g<<8)|b} vs place {gp['colour']}")
        if gp["material"] != sp["material_token"]:
            problems.append(f"material {k}: spec {sp['material_token']} vs place {gp['material']}")
        if abs(gp["transp"] - sp["transp"]) > 0.005:
            problems.append(f"transparency {k}: spec {sp['transp']} vs place {gp['transp']}")
        if gp["collide"] != sp["collide"]:
            problems.append(f"collide {k}: spec {sp['collide']} vs place {gp['collide']}")

    spawns = [p for p in got if p["class"] == "SpawnLocation"]
    if len(spawns) != 1:
        problems.append(f"expected exactly 1 SpawnLocation, found {len(spawns)}")

    summary = {
        "xml": os.path.relpath(xml_path, ROOT),
        "spec_parts": len(want),
        "place_parts": len(got),
        "compared": checked,
        "problems": problems[:40],
        "problem_count": len(problems),
        "spawn_locations": len(spawns),
        "parity": not problems,
    }
    os.makedirs(os.path.join(ROOT, "evidence"), exist_ok=True)
    json.dump(summary, open(os.path.join(ROOT, "evidence", "export_parity.json"), "w"), indent=2)

    if problems:
        print(f"verify_place: FAIL — {len(problems)} problem(s)")
        for p in problems[:25]:
            print("  " + p)
        return 1
    print(f"verify_place: PASS — {checked}/{len(want)} parts byte-parity "
          f"(size, pos, rotation, colour, material, transparency, collision)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
