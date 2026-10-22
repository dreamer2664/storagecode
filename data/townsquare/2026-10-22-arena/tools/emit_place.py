#!/usr/bin/env python3
"""emit_place.py — turn build/townspec.json into (a) the .rbxmx Rojo compiles into
TownSquare.rbxl and (b) src/ReplicatedStorage/TownData.luau for the runtime.

Design notes learned the hard way, verified by tools/verify_place.py:

  * Color3uint8 in a place file is packed 0xRRGGBB. The high byte is NOT alpha;
    writing 0xFFRRGGBB silently loses the red channel after a round-trip.
  * Part.Shape does not survive Rojo's serialisation, so there are no cylinders
    in this town: every part is a Block, and round-ish things are built from
    faceted blocks.
  * A lone Part as the root of an .rbxmx gets renamed, so everything is nested
    under Model/Folder nodes.

    python3 tools/emit_place.py
"""
from __future__ import annotations

import json
import os
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SPEC = json.load(open(os.path.join(ROOT, "build", "townspec.json")))


def tree_of(parts):
    """group path ('B01/L2') -> nested dict of {name: [parts...]}"""
    root: dict = {}
    for p in parts:
        segs = p["group"].split("/")
        if segs[0].startswith("B"):
            segs = ["Buildings"] + segs
        node = root
        for s in segs:
            node = node.setdefault(s, {})
        node.setdefault("__parts__", []).append(p)
    return root


def serialise_rotation(rot):
    return "".join(
        f"<R{i}{j}>{rot[i][j]:.6f}</R{i}{j}>" for i in range(3) for j in range(3)
    )


def clean_name(n: str) -> str:
    return n.rsplit("/", 1)[-1]


def part_xml(p, ref, seen_names, indent):
    name = clean_name(p["name"])
    if name in seen_names:
        seen_names[name] += 1
        name = f"{name}_{seen_names[name]}"
    else:
        seen_names[name] = 1
    r, g, b = p["colour"]
    packed = (r << 16) | (g << 8) | b          # 0xRRGGBB, never 0xAARRGGBB
    x, y, z = p["pos"]
    sx, sy, sz = p["size"]
    cls = p["cls"]
    pad = " " * indent
    props = [
        f'<string name="Name">{escape(name)}</string>',
        f'<CoordinateFrame name="CFrame"><X>{x:.4f}</X><Y>{y:.4f}</Y><Z>{z:.4f}</Z>'
        f'{serialise_rotation(p["rot"])}</CoordinateFrame>',
        f'<Vector3 name="size"><X>{sx:.4f}</X><Y>{sy:.4f}</Y><Z>{sz:.4f}</Z></Vector3>',
        f'<Color3uint8 name="Color3uint8">{packed}</Color3uint8>',
        f'<token name="Material">{p["material_token"]}</token>',
        f'<bool name="Anchored">true</bool>',
        f'<bool name="CanCollide">{"true" if p["collide"] else "false"}</bool>',
        f'<bool name="CastShadow">{"true" if p["shadow"] else "false"}</bool>',
        f'<float name="Transparency">{p["transp"]:.3f}</float>',
    ]
    if cls == "SpawnLocation":
        props.append('<bool name="Neutral">true</bool>')
    out = [f'{pad}<Item class="{cls}" referent="RBX{ref}">', f"{pad} <Properties>"]
    out += [f"{pad}  {pr}" for pr in props]
    out.append(f"{pad} </Properties>")
    out.append(f"{pad}</Item>")
    return "\n".join(out)


def emit_node(node, cls, name, ref, indent, seen_names, out):
    pad = " " * indent
    out.append(f'{pad}<Item class="{cls}" referent="RBX{ref[0]}">')
    ref[0] += 1
    out.append(f"{pad} <Properties><string name=\"Name\">{escape(name)}</string></Properties>")
    local_seen: dict = {}
    for p in node.get("__parts__", []):
        out.append(part_xml(p, ref[0], local_seen, indent + 1))
        ref[0] += 1
    for key, child in node.items():
        if key == "__parts__":
            continue
        child_cls = "Folder" if key in ("Buildings", "Square") or key.startswith("L") else "Model"
        if key.startswith("Square"):
            child_cls = "Folder"
        emit_node(child, child_cls, key, ref, indent + 1, seen_names, out)
    out.append(f"{pad}</Item>")


def build_rbxmx():
    parts = SPEC["parts"]
    tree = tree_of(parts)
    ref = [1]
    out = ['<roblox version="4">', " <External>null</External>", " <External>nil</External>"]
    seen: dict = {}
    emit_node(tree, "Model", "Town", ref, 1, seen, out)
    out.append("</roblox>")
    path = os.path.join(ROOT, "src", "Workspace", "Town.rbxmx")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write("\n".join(out) + "\n")
    return path


def luau_value(v, indent=0):
    pad = "  " * indent
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return f"{v}"
    if isinstance(v, str):
        return '"' + v.replace('\\', '\\\\').replace('"', '\\"') + '"'
    if isinstance(v, list):
        inner = ", ".join(luau_value(x, indent) for x in v)
        return "{ " + inner + " }"
    if isinstance(v, dict):
        items = []
        for k, val in v.items():
            key = k if k.replace("_", "").isalnum() and not k[0].isdigit() else f'["{k}"]'
            items.append(f"{pad}  {key} = {luau_value(val, indent + 1)},")
        return "{\n" + "\n".join(items) + "\n" + pad + "}"
    return "nil"


def build_towndata():
    rooms = []
    for r in SPEC["rooms"]:
        rooms.append({
            "building": r["building"], "floor": r["floor"], "kind": r["kind"],
            "label": r["label"], "centre": [round(c, 3) for c in r["centre"]],
        })
    data = {
        "meta": SPEC["meta"],
        "buildings": [{k: b[k] for k in ("key", "name", "programme", "floors", "width", "depth")}
                      for b in SPEC["buildings"]],
        "rooms": rooms,
        "doors": SPEC["doors"],
        "npcs": [{k: n[k] for k in ("id", "name", "role", "workplace", "home_building",
                                    "home_floor", "home_room", "bed", "shirt", "trousers",
                                    "skin", "post", "hat", "height")}
                 for n in SPEC["npcs"]],
        "beds": SPEC["beds"],
        "posts": SPEC["posts"],
    }
    body = luau_value(data, 0)
    src = (
        "--!nonstrict\n"
        "-- TownData — generated by tools/emit_place.py from tools/townspec.py.\n"
        "-- Do not hand-edit: regenerate instead, so the place, the renders and the\n"
        "-- validators all keep reading the same town.\n"
        "-- 10 buildings, 35 floors, 176 rooms, 64 residents, 10 hinged doors.\n\n"
        "return " + body + "\n"
    )
    path = os.path.join(ROOT, "src", "ReplicatedStorage", "TownData.luau")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(src)
    return path, len(src)


if __name__ == "__main__":
    p1 = build_rbxmx()
    p2, n2 = build_towndata()
    print(f"wrote {p1} ({os.path.getsize(p1)/1e6:.2f} MB)")
    print(f"wrote {p2} ({n2/1024:.0f} KB)")
