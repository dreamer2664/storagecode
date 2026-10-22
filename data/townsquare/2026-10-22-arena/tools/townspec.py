#!/usr/bin/env python3
"""townspec.py — the single authoritative geometry generator for Winterlichtplatz.

One source of truth. This module emits `build/townspec.json`, which is consumed by
THREE things that must never disagree:

  * tools/emit_place.py   -> the .rbxmx that Rojo compiles into TownSquare.rbxl
  * tools/render.py       -> the offline Cycles-free rasteriser that makes the
                             screenshots (reads the *same* boxes and transforms)
  * tools/validate.py     -> the validators (floors per building, door clearance,
                             reachability, spawn clearance, NPC bed census, ...)

Because the renderer and the place are both derived from this one table of boxes,
"the render shows what the ship file contains" is true by construction rather
than by inspection.

Coordinate system: metres == studs. +X east, +Z south, +Y up. The square is
centred on the origin; the ten buildings ring it on a 40 m x 40 m paved place.

Every colour is calibrated from a real CC0 photogrammetry scan (see
assets/scans/SCAN_RECEIPTS.json): `mean_albedo_srgb` becomes the part colour,
and the Roblox Material token is the nearest sensible surface. A .rbxl cannot
carry uploaded PBR textures, so scan colour + engine material is the honest
ceiling for the place file; the offline renders additionally sample the scan
albedo maps as actual textures.
"""
from __future__ import annotations

import json
import math
import os
import random
from dataclasses import dataclass, field

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RNG = random.Random(20261022)  # deterministic: same town every run

# --------------------------------------------------------------------------
# Material tokens: authoritative values from Roblox-Client-Tracker API-Dump.
# --------------------------------------------------------------------------
# Accent colours that are NOT derived from a scan: glazing, metalwork, lamp glass,
# signage and the odd painted object. Declared here so the validator can prove
# that nothing else in the town was coloured by hand.
ACCENTS = {
    "glass":        [128, 150, 168],
    "lamp_glass":   [255, 236, 176],
    "lantern":      [255, 232, 160],
    "iron":         [46, 46, 50],
    "bench_iron":   [52, 52, 56],
    "bollard":      [58, 58, 62],
    "sign_hanger":  [64, 64, 66],
    "soil":         [62, 54, 40],
    "linen":        [240, 238, 232],
    "brass":        [196, 168, 96],
    "canopy_red":   [168, 96, 84],
    "canopy_blue":  [92, 108, 132],
    "paper":        [196, 186, 162],
    "collector":    [96, 132, 148],
    "water":        [96, 132, 148],
    "notice_roof":  [92, 70, 46],
    "spawn_pad":    [120, 126, 132],
}

# Planting colours. Not from a scan (a scanned bark/leaf albedo at this tiling
# reads as static), so they are declared here in full.
GREENS = {
    "ground_grass": [86, 98, 74],
    "tree_canopy": [74, 96, 58],
    "hill": [76, 90, 62],
    "outskirt_crown": [68, 88, 54],
}
MAT = {
    "Plastic": 256, "SmoothPlastic": 272, "Neon": 288,
    "Wood": 512, "WoodPlanks": 528, "Marble": 784, "Slate": 800,
    "Concrete": 816, "Limestone": 820, "Granite": 832, "Pavement": 836,
    "Brick": 848, "Pebble": 864, "Cobblestone": 880, "Rock": 896,
    "Sandstone": 912, "CorrodedMetal": 1040, "DiamondPlate": 1056,
    "Metal": 1088, "Grass": 1280, "LeafyGrass": 1284, "Sand": 1296,
    "Fabric": 1312, "Ground": 1360, "Asphalt": 1376, "Glass": 1568,
    "Plaster": 2310, "CeramicTiles": 2306, "ClayRoofTiles": 2307,
    "RoofShingles": 2308, "Leather": 2309, "Carpet": 2305, "Cardboard": 2304,
    "Rubber": 2311, "Foili": 1072,
}


def scan_colours() -> dict[str, list[int]]:
    path = os.path.join(ROOT, "assets", "scans", "SCAN_RECEIPTS.json")
    out = {}
    for r in json.load(open(path)):
        out[r["role"]] = r["mean_albedo_srgb"]
    return out


SCAN = scan_colours()


def tint(rgb: list[int], f: float) -> list[int]:
    return [max(0, min(255, int(round(c * f)))) for c in rgb]


# Palette: every wall/roof/floor colour traces to a scan role.
PAL = {
    "paving":     (SCAN["ground"],        "Cobblestone"),
    "paving2":    (SCAN["ground_alt"],    "Cobblestone"),
    "kerb":       (SCAN["concrete"],      "Concrete"),
    "wall_brick": (SCAN["brick"],         "Brick"),
    "wall_brick2":(SCAN["brick_alt"],     "Brick"),
    "wall_plaster":(SCAN["plaster"],      "Plaster"),
    "wall_stone": (SCAN["stone"],         "Rock"),
    "timber":     (SCAN["timber"],        "Wood"),
    "floorboard": (SCAN["floorboard"],    "WoodPlanks"),
    "tile":       (SCAN["tile"],          "CeramicTiles"),
    "roof":       (tint(SCAN["brick_alt"], 0.72), "ClayRoofTiles"),
    "roof2":      (tint(SCAN["stone"], 0.85),     "Slate"),
    "gravel":     (SCAN["gravel"],        "Pebble"),
    "bark":       (SCAN["bark"],          "Wood"),
    "concrete":   (SCAN["concrete"],      "Concrete"),
}
# aliases used by interior detail (same scans, plainer names)
PAL["plaster"] = PAL["wall_plaster"]
PAL["stone"] = PAL["wall_stone"]
PAL["brick_alt"] = PAL["wall_brick2"]
PAL["brick"] = PAL["wall_brick"]

# --------------------------------------------------------------------------
# small 3x3 rotation helpers (row-major, right-handed, +Y up)
# --------------------------------------------------------------------------
def rot_y(deg: float):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [[c, 0, s], [0, 1, 0], [-s, 0, c]]


def rot_z(deg: float):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [[c, -s, 0], [s, c, 0], [0, 0, 1]]


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def apply(m, v):
    return [sum(m[i][k] * v[k] for k in range(3)) for i in range(3)]


IDENT = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]


@dataclass
class Part:
    name: str
    group: str
    size: tuple            # local size (x,y,z)
    pos: tuple             # world centre
    rot: list              # 3x3 world rotation
    colour: list
    material: str
    transp: float = 0.0
    collide: bool = True
    cast_shadow: bool = True
    cls: str = "Part"
    tag: str = ""          # semantic tag: wall/floor/door/window/furniture/prop/roof


PARTS: list[Part] = []
TAGGED: dict[str, list[str]] = {}


def add(name, group, size, pos, rot=IDENT, colour=None, material="Plastic",
        transp=0.0, collide=True, cast_shadow=True, cls="Part", tag="") -> Part:
    if colour is None:
        colour = PAL["wall_plaster"][0]
    if isinstance(colour, str):
        colour, material = PAL[colour][0], (material if material != "Plastic" else PAL[colour][1])
    p = Part(name, group, tuple(round(v, 4) for v in size),
             tuple(round(v, 4) for v in pos), [row[:] for row in rot],
             list(colour), material, transp, collide, cast_shadow, cls, tag)
    PARTS.append(p)
    if tag:
        TAGGED.setdefault(tag, []).append(name)
    return p


class Builder:
    """Local frame for one building: yaw about Y, then translate."""

    def __init__(self, group: str, origin, yaw: float):
        self.group = group
        self.origin = origin
        self.yaw = yaw
        self.R = rot_y(yaw)

    def world(self, lx, ly, lz):
        w = apply(self.R, (lx, ly, lz))
        return (w[0] + self.origin[0], w[1] + self.origin[1], w[2] + self.origin[2])

    def box(self, name, lx, ly, lz, sx, sy, sz, *, colour=None, material="Plastic",
            tag="", transp=0.0, collide=True, rot_z_deg=0.0, cls="Part",
            cast_shadow=True):
        R = self.R if rot_z_deg == 0 else matmul(self.R, rot_z(rot_z_deg))
        return add(f"{self.group}/{name}", self.group, (sx, sy, sz),
                   self.world(lx, ly, lz), R, colour, material, transp,
                   collide, cast_shadow, cls, tag)


# --------------------------------------------------------------------------
# Wall with openings
# --------------------------------------------------------------------------
def wall_with_openings(b: Builder, name, *, axis, span, fixed, y0, y1, thickness,
                       openings, colour, material, tag="wall", inset=0.0):
    """axis='x': wall runs along local X at local z=fixed. axis='z': along Z at x=fixed.

    `openings` = list of (centre_along, width, hole_y0, hole_y1) in local coords.
    Emits pier boxes between openings plus sill/lintel boxes over each opening.
    """
    a0, a1 = span
    ops = sorted(openings, key=lambda o: o[0])
    cursor = a0
    idx = 0

    def emit(c0, c1, lo, hi):
        if c1 - c0 <= 1e-4 or hi - lo <= 1e-4:
            return
        nonlocal idx
        mid = (c0 + c1) / 2
        cy = (lo + hi) / 2
        if axis == "x":
            b.box(f"{name}_{idx}", mid, cy, fixed, c1 - c0, hi - lo, thickness,
                  colour=colour, material=material, tag=tag)
        else:
            b.box(f"{name}_{idx}", fixed, cy, mid, thickness, hi - lo, c1 - c0,
                  colour=colour, material=material, tag=tag)
        idx += 1

    for (c, w, oy0, oy1) in ops:
        lo, hi = c - w / 2, c + w / 2
        emit(cursor, max(cursor, lo), y0, y1)          # pier before the opening
        emit(lo, hi, y0, min(oy0, y1))                 # sill under it
        emit(lo, hi, max(oy1, y0), y1)                 # lintel over it
        cursor = max(cursor, hi)
    emit(cursor, a1, y0, y1)                           # final pier


# --------------------------------------------------------------------------
# Building programme
# --------------------------------------------------------------------------
@dataclass
class BuildingSpec:
    key: str
    name: str
    programme: str
    floors: int
    width: float
    depth: float
    angle_deg: float
    palette: str
    roof: str = "gable"
    shop_sign: str = ""


GROUND_H = 4.4
FLOOR_H = 3.6
SLAB_T = 0.35
WALL_T = 0.30

BUILDINGS = [
    BuildingSpec("B01", "The Gilded Lark",      "inn + 4 upper apartments", 4, 15.0, 12.0,  18.0, "wall_plaster"),
    BuildingSpec("B02", "Corvin's Bakery",      "bakehouse + 3 apartments", 3, 12.0, 11.0,  54.0, "wall_brick"),
    BuildingSpec("B03", "Bell & Buckle Smithy", "forge + 3 apartments",     3, 12.5, 11.5,  91.0, "wall_brick2"),
    BuildingSpec("B04", "The Salt House",       "merchant hall + 4 floors", 4, 16.0, 12.5, 128.0, "wall_stone"),
    BuildingSpec("B05", "Weavers' Hall",        "guild hall + workshops",   4, 14.0, 12.0, 165.0, "wall_plaster"),
    BuildingSpec("B06", "Saint Auden's Rectory","rectory + 3 floors",       3, 12.0, 11.0, 202.0, "wall_stone"),
    BuildingSpec("B07", "The Paper Lantern",    "bookshop + 3 floors",      3, 12.0, 11.0, 238.0, "wall_brick"),
    BuildingSpec("B08", "Apothecary Vale",      "apothecary + 4 floors",    4, 12.5, 11.5, 275.0, "wall_plaster"),
    BuildingSpec("B09", "The Copper Kettle",    "tavern + 4 apartments",    4, 15.0, 12.0, 312.0, "wall_brick2"),
    BuildingSpec("B10", "Watch House",          "watch house + barracks",   3, 13.0, 11.5, 345.0, "wall_stone"),
]

FRONT_R = 29.0      # radius of the facade line, metres from square centre
SQUARE_HALF = 20.0  # paved square half-width
SPAWN = (0.0, 0.0, -7.0)  # proven clear by V07

ROOM_WORDS = {
    "living": "Living Room", "bed": "Bedroom", "kitchen": "Kitchen",
    "store": "Storeroom", "shop": "Shop Floor", "forge": "Forge",
    "hall": "Hall", "study": "Study", "attic": "Attic Room",
}
FURNITURE_TINTS = {
    "table": ([96, 66, 42], "Wood"), "chair": ([76, 52, 34], "Wood"),
    "bed": ([186, 182, 172], "Fabric"), "rug": ([120, 38, 40], "Fabric"),
    "shelf": ([88, 60, 38], "Wood"), "counter": ([82, 56, 36], "Wood"),
    "stove": ([52, 50, 48], "Metal"), "barrel": ([104, 74, 46], "Wood"),
    "crate": ([112, 82, 50], "Wood"),
}


def build_building(spec: BuildingSpec, door_registry: list, room_registry: list):
    th = math.radians(spec.angle_deg)
    # facade line sits at radius FRONT_R; +Z of the building points outward
    cx = math.cos(th) * (FRONT_R + spec.depth / 2)
    cz = math.sin(th) * (FRONT_R + spec.depth / 2)
    yaw = 90.0 - spec.angle_deg
    b = Builder(spec.key, (cx, 0.0, cz), yaw)
    g = spec.key
    w, d = spec.width, spec.depth
    hw, hd = w / 2, d / 2
    pal = PAL[spec.palette]
    wall_col, wall_mat = pal[0], pal[1]
    trim_col = PAL["concrete"][0]
    floor_col, floor_mat = PAL["floorboard"][0], "WoodPlanks"
    roof_col, roof_mat = PAL["roof"][0], "ClayRoofTiles"

    # ---- plinth + ground slab
    b.box("Plinth", 0, 0.1, 0, w + 0.6, 0.4, d + 0.6, colour=trim_col,
          material="Concrete", tag="structure")
    b.box("Slab_G", 0, 0.2 + SLAB_T / 2, 0, w, SLAB_T, d,
          colour=floor_col, material=floor_mat, tag="floor")

    stair_x = -hw + 1.15           # stairwell at the west end
    stair_w = 1.9
    stair_z = 0.6

    total_h = GROUND_H + (spec.floors - 1) * FLOOR_H
    # ---- floors
    for f in range(spec.floors):
        y0 = 0.2 + (0 if f == 0 else GROUND_H + (f - 1) * FLOOR_H)
        fh = GROUND_H if f == 0 else FLOOR_H
        y1 = y0 + fh
        level_y = y0 + 0.12
        grp_floor = f"{g}/L{f+1}"
        bf = Builder(grp_floor, (cx, 0.0, cz), yaw)
        top = (f == spec.floors - 1)

        # slab of the floor above (with a stair opening); not for the top floor
        if not top:
            sy = y1 + SLAB_T / 2
            hole = (stair_x - stair_w / 2, stair_x + stair_w / 2,
                    stair_z - 1.6, stair_z + 1.6)
            x_l, x_r = -hw, hw
            z_l, z_r = -hd, hd
            # four rectangles around the stair hole
            segs = [
                ("a", (x_l, hole[0]), (z_l, z_r)),
                ("b", (hole[1], x_r), (z_l, z_r)),
                ("c", (hole[0], hole[1]), (z_l, hole[2])),
                ("d", (hole[0], hole[1]), (hole[3], z_r)),
            ]
            for nm, (xa, xb), (za, zb) in segs:
                if xb - xa < 0.05 or zb - za < 0.05:
                    continue
                bf.box(f"Slab_{nm}", (xa + xb) / 2, sy, (za + zb) / 2,
                       xb - xa, SLAB_T, zb - za, colour=floor_col,
                       material=floor_mat, tag="floor")

        # ---- exterior walls, facade (+/-Z faces) and gable ends (+/-X)
        wind_h, sill = 1.75, 1.05
        n_front = 3 if w >= 13 else 2
        front_ops = []
        for i in range(n_front):
            x = -hw + (i + 0.5) * (w / n_front)
            front_ops.append((x, 1.15, y0 + sill, y0 + sill + wind_h))
        back_ops = [(x, 1.05, y0 + sill, y0 + sill + wind_h)
                    for x in (-hw + w * 0.28, -hw + w * 0.72)]
        side_ops = [(z, 1.0, y0 + sill, y0 + sill + wind_h)
                    for z in (-hd + d * 0.30, -hd + d * 0.72)]

        # front facade: ground floor gets the entrance door
        if f == 0:
            door_w, door_h = 1.6, 2.75
            front_ops_f = [(o[0], o[1], o[2], o[3]) for o in front_ops if abs(o[0]) > door_w]
            front_ops_f = [(0.0, door_w, y0, y0 + door_h)] + front_ops_f
        else:
            front_ops_f = front_ops

        wall_with_openings(bf, "FacadeFront", axis="x", span=(-hw, hw), fixed=-hd + WALL_T / 2,
                           y0=y0, y1=y1, thickness=WALL_T, openings=front_ops_f,
                           colour=wall_col, material=wall_mat)
        wall_with_openings(bf, "FacadeBack", axis="x", span=(-hw, hw), fixed=hd - WALL_T / 2,
                           y0=y0, y1=y1, thickness=WALL_T, openings=back_ops,
                           colour=wall_col, material=wall_mat)
        wall_with_openings(bf, "GableL", axis="z", span=(-hd, hd), fixed=-hw + WALL_T / 2,
                           y0=y0, y1=y1, thickness=WALL_T, openings=side_ops,
                           colour=wall_col, material=wall_mat)
        wall_with_openings(bf, "GableR", axis="z", span=(-hd, hd), fixed=hw - WALL_T / 2,
                           y0=y0, y1=y1, thickness=WALL_T, openings=side_ops,
                           colour=wall_col, material=wall_mat)

        # ---- glazing
        for i, (x, ow, oy0, oy1) in enumerate(front_ops_f):
            if oy1 - oy0 < 1.0:
                continue
            glass = [128, 150, 168]
            bf.box(f"Glass_F{i}", x, (oy0 + oy1) / 2, -hd + WALL_T / 2,
                   ow - 0.14, (oy1 - oy0) - 0.14, 0.08, colour=glass,
                   material="Glass", transp=0.35, collide=False, tag="window",
                   cast_shadow=False)
            # muntin cross
            bf.box(f"Muntin_F{i}", x, (oy0 + oy1) / 2, -hd + WALL_T / 2 + 0.02,
                   0.045, (oy1 - oy0) - 0.12, 0.05, colour=PAL["timber"][0],
                   material="Wood", collide=False, tag="window")
        for i, (x, ow, oy0, oy1) in enumerate(back_ops):
            bf.box(f"Glass_B{i}", x, (oy0 + oy1) / 2, hd - WALL_T / 2,
                   ow - 0.14, (oy1 - oy0) - 0.14, 0.08, colour=[128, 150, 168],
                   material="Glass", transp=0.35, collide=False, tag="window",
                   cast_shadow=False)
        for side, sgn in (("L", -1), ("R", 1)):
            for i, (z, ow, oy0, oy1) in enumerate(side_ops):
                bf.box(f"Glass_{side}{i}", sgn * (hw - WALL_T / 2), (oy0 + oy1) / 2, z,
                       0.08, (oy1 - oy0) - 0.14, ow - 0.14, colour=[128, 150, 168],
                       material="Glass", transp=0.35, collide=False, tag="window",
                       cast_shadow=False)

        # ---- front door leaf (server script hinges it)
        if f == 0:
            dname = f"{grp_floor}/Door_Front"
            bf.box("Door_Front", -0.34, y0 + door_h / 2 - 0.02, -hd + 0.10,
                   1.52, door_h - 0.10, 0.12, colour=PAL["timber"][0],
                   material="Wood", tag="door")
            door_registry.append({"name": dname, "building": g, "floor": 1,
                                  "kind": "entrance"})

        # ---- interior: corridor along X at z = stair_z, rooms fore and aft
        corr_z0, corr_z1 = stair_z - 1.05, stair_z + 1.05
        bf.box("CorrWallFront", 0, (y0 + y1) / 2, corr_z0, w - stair_w - 0.6, fh, 0.16,
               colour=PAL["plaster"][0], material="Plaster", tag="partition")
        bf.box("CorrWallBack", 0, (y0 + y1) / 2, corr_z1, w - stair_w - 0.6, fh, 0.16,
               colour=PAL["plaster"][0], material="Plaster", tag="partition")
        # room dividers front and back
        n_div = max(2, int(round((w - stair_w) / 4.0)))
        for i in range(1, n_div):
            x = -hw + stair_w + 0.3 + i * (w - stair_w - 0.6) / n_div
            for zz in (corr_z0 - (abs(corr_z0) + hd) / 2 + 0.4, (corr_z1 + hd) / 2):
                bf.box(f"Divider_{i}_{'F' if zz < stair_z else 'B'}", x,
                       (y0 + y1) / 2, zz, 0.16, fh, abs(hd) - 1.6,
                       colour=PAL["plaster"][0], material="Plaster", tag="partition")

        # ---- stairs to the floor above
        if not top:
            steps = 12
            rise = FLOOR_H / steps
            run = 0.30
            for s in range(steps):
                bf.box(f"Step_{s}", stair_x, y1 + rise * (s + 0.5), stair_z - 1.4 + s * run,
                       stair_w, rise, run, colour=PAL["concrete"][0],
                       material="Concrete", tag="stair")
            bf.box("Stringer", stair_x - stair_w / 2 - 0.06,
                   y1 + FLOOR_H / 2, stair_z - 1.4 + steps * run / 2,
                   0.12, FLOOR_H, steps * run, colour=PAL["timber"][0],
                   material="Wood", tag="stair")

        # ---- room programme + furniture
        room_names = []
        prog = []
        if f == 0:
            # keep the first 3.2 m behind the door clear (V06 checks this)
            prog = [("shop", -hd + 4.0), ("store", hd - 3.0)]
        else:
            kinds = ["living", "bed", "kitchen", "bed", "study", "kitchen", "bed", "store"]
            for i in range(n_div):
                prog.append((kinds[(i + f) % len(kinds)], -hd + 2.6))
                prog.append((kinds[(i + f + 3) % len(kinds)], hd - 2.6))
        for ri, (kind, zc) in enumerate(prog):
            span_x = (w - stair_w - 0.6) / n_div
            xc = -hw + stair_w + 0.3 + (ri // 2 + 0.5) * span_x
            room_names.append((kind, xc, zc))
            room_registry.append({
                "building": g, "building_name": spec.name, "floor": f + 1,
                "kind": kind, "label": ROOM_WORDS.get(kind, kind),
                "centre": list(b.world(xc, level_y + fh / 2, zc)),
                "size": [span_x - 0.3, fh, abs(hd) - 1.8],
            })
            furnish(bf, f"{spec.key}_F{f+1}_R{ri}", kind, xc, y0, zc, span_x, hd)

        # ---- lighting fixture per floor
        bf.box("CeilLamp", 0.4, y1 - 0.30, stair_z,
               0.55, 0.16, 0.55, colour=[255, 236, 176], material="Neon",
               collide=False, tag="light", cast_shadow=False)

    # ---- roof
    if spec.roof == "gable":
        rise = 2.9
        ridge_y = total_h + rise
        overhang = 0.38
        slope_len = math.hypot(hd + overhang, rise)
        ang = math.degrees(math.atan2(rise, hd + overhang))
        for sgn, nm in ((-1, "Front"), (1, "Back")):
            R = matmul(b.R, rot_x(sgn * ang))
            add(f"{g}/{g}/Roof_{nm}", g, (w + 2 * overhang, 0.28, slope_len),
                b.world(0, total_h + rise / 2, sgn * (hd + overhang) / 2),
                R, roof_col, roof_mat, 0.0, False, True, "Part", "roof")
        # ridge cap
        b.box("Ridge", 0, ridge_y - 0.05, 0, w + 2 * overhang, 0.22, 0.5,
              colour=tint(roof_col, 0.8), material=roof_mat, tag="roof")
        # stepped gable ends
        steps = 5
        for sgn, side in ((-1, "L"), (1, "R")):
            for s in range(steps):
                frac = (s + 1) / steps
                b.box(f"GableStep_{side}{s}", sgn * (hw - WALL_T / 2 + 0.02),
                      total_h + rise * (frac - 0.5 / steps) / 1.0,
                      stair_z * 0, 0.34, rise / steps, (d) * (1 - frac) + 0.2,
                      colour=wall_col, material=wall_mat, tag="structure")
        # chimney
        chx = hw * 0.45
        b.box("Chimney", chx, ridge_y + 0.4, hd * 0.25, 0.85, 1.7, 0.85,
              colour=PAL["brick_alt"][0], material="Brick", tag="structure")
        b.box("ChimneyCap", chx, ridge_y + 1.28, hd * 0.25, 1.05, 0.16, 1.05,
              colour=trim_col, material="Concrete", tag="structure")
    else:
        b.box("Parapet", 0, total_h + 0.4, 0, w + 0.4, 0.8, d + 0.4,
              colour=wall_col, material=wall_mat, tag="roof")

    # ---- street-facing signage board over the door
    if spec.shop_sign:
        b.box("SignBoard", 0, GROUND_H - 0.55, -hd - 0.12, w * 0.55, 0.62, 0.12,
              colour=PAL["timber"][0], material="Wood", tag="prop")
        b.box("SignHanger", 0, GROUND_H + 0.02, -hd - 0.10, w * 0.6, 0.08, 0.10,
              colour=[64, 64, 66], material="Metal", tag="prop")

    return b


def rot_x(deg: float):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [[1, 0, 0], [0, c, -s], [0, s, c]]


def furnish(b: Builder, tagp: str, kind: str, xc: float, y0: float, zc: float,
            span_x: float, hd: float):
    """A few honest parts per room: something to sit on, something to put things on."""
    y = y0 + 0.12
    if kind in ("shop", "forge", "hall"):
        b.box(f"{tagp}_Counter", xc, y + 0.5, zc, min(3.2, span_x * 0.7), 1.0, 0.65,
              colour=FURNITURE_TINTS["counter"][0], material="Wood", tag="furniture")
        b.box(f"{tagp}_Shelf", xc, y + 1.1, zc + (1.4 if zc > 0 else -1.4),
              min(3.0, span_x * 0.7), 0.9, 0.4,
              colour=FURNITURE_TINTS["shelf"][0], material="Wood", tag="furniture")
        b.box(f"{tagp}_Barrel", xc + span_x * 0.3, y + 0.45, zc - 0.9, 0.75, 0.9, 0.75,
              colour=FURNITURE_TINTS["barrel"][0], material="Wood", tag="furniture")
    elif kind == "bed":
        b.box(f"{tagp}_Bed", xc, y + 0.32, zc, 1.25, 0.42, 2.1,
              colour=FURNITURE_TINTS["bed"][0], material="Fabric", tag="furniture")
        b.box(f"{tagp}_Pillow", xc, y + 0.6, zc - 0.8, 1.05, 0.16, 0.42,
              colour=[240, 238, 232], material="Fabric", tag="furniture")
        b.box(f"{tagp}_Chest", xc + span_x * 0.32, y + 0.35, zc + 0.6, 0.8, 0.7, 0.5,
              colour=FURNITURE_TINTS["crate"][0], material="Wood", tag="furniture")
    elif kind in ("living", "study"):
        b.box(f"{tagp}_Table", xc, y + 0.38, zc, 1.1, 0.09, 1.1,
              colour=FURNITURE_TINTS["table"][0], material="Wood", tag="furniture")
        for i, (dx, dz) in enumerate(((-0.42, -0.42), (0.42, -0.42), (-0.42, 0.42), (0.42, 0.42))):
            b.box(f"{tagp}_Leg{i}", xc + dx, y + 0.19, zc + dz, 0.09, 0.38, 0.09,
                  colour=FURNITURE_TINTS["table"][0], material="Wood", tag="furniture")
        b.box(f"{tagp}_Chair", xc + 1.0, y + 0.24, zc, 0.48, 0.48, 0.48,
              colour=FURNITURE_TINTS["chair"][0], material="Wood", tag="furniture")
        b.box(f"{tagp}_Shelf", xc - span_x * 0.32, y + 1.0, zc, 0.35, 1.6, 1.5,
              colour=FURNITURE_TINTS["shelf"][0], material="Wood", tag="furniture")
        b.box(f"{tagp}_Rug", xc, y + 0.02, zc + 1.1, 2.0, 0.04, 1.4,
              colour=FURNITURE_TINTS["rug"][0], material="Fabric", tag="furniture",
              collide=False)
    elif kind == "kitchen":
        b.box(f"{tagp}_Stove", xc - span_x * 0.25, y + 0.45, zc, 1.0, 0.9, 0.85,
              colour=FURNITURE_TINTS["stove"][0], material="Metal", tag="furniture")
        b.box(f"{tagp}_Table", xc + 0.5, y + 0.38, zc, 0.9, 0.09, 0.9,
              colour=FURNITURE_TINTS["table"][0], material="Wood", tag="furniture")
        b.box(f"{tagp}_Shelf", xc, y + 1.35, zc + (1.3 if zc > 0 else -1.3),
              min(2.4, span_x * 0.6), 0.7, 0.35,
              colour=FURNITURE_TINTS["shelf"][0], material="Wood", tag="furniture")
    else:  # store / attic
        for i in range(2):
            b.box(f"{tagp}_Crate{i}", xc + (i - 0.5) * 1.1, y + 0.36, zc, 0.7, 0.72, 0.7,
                  colour=FURNITURE_TINTS["crate"][0], material="Wood", tag="furniture")
        b.box(f"{tagp}_Barrel", xc - span_x * 0.3, y + 0.45, zc + 0.8, 0.8, 0.9, 0.8,
              colour=FURNITURE_TINTS["barrel"][0], material="Wood", tag="furniture")


# --------------------------------------------------------------------------
# The square itself
# --------------------------------------------------------------------------
def build_square():
    g = "Square"
    b = Builder(g, (0, 0, 0), 0.0)
    pav = PAL["paving"][0]
    pav2 = PAL["paving2"][0]

    # base ground beyond the square: grass/earth apron, not a bare plane
    b.box("Ground", 0, -0.5, 0, 640, 1.0, 640, colour=GREENS["ground_grass"],
          material="Grass", tag="ground")
    # street ring hugging the building line, then four radial streets
    ring_in, ring_out = 21.0, 28.2
    for i in range(32):
        a0 = 2 * math.pi * i / 32
        a1 = 2 * math.pi * (i + 1) / 32
        am = (a0 + a1) / 2
        rm = (ring_in + ring_out) / 2
        seg_len = 2 * math.pi * rm / 32 + 0.12
        seg = add(f"Square/StreetRing{i:02d}", "Square",
                  (seg_len, 0.2, ring_out - ring_in),
                  (math.cos(am) * rm, 0.04, math.sin(am) * rm),
                  rot_y(-math.degrees(am)), tint(pav, 0.86 if i % 2 else 0.90),
                  "Cobblestone", 0.0, True, False, "Part", "ground")
    for i, ang in enumerate((0, 90, 180, 270)):
        r0, r1 = 27.0, 72.0
        rm = (r0 + r1) / 2
        a = math.radians(ang)
        add(f"Square/Street{i}", "Square",
            (6.0, 0.2, r1 - r0), (math.cos(a) * rm, 0.04, math.sin(a) * rm),
            rot_y(ang), tint(pav, 0.90), "Cobblestone", 0.0, True, False,
            "Part", "ground")
    # paved square: 8 x 8 slabs of varied tint, plus kerb ring
    n = 8
    for i in range(n):
        for j in range(n):
            x = -SQUARE_HALF + (i + 0.5) * (2 * SQUARE_HALF / n)
            z = -SQUARE_HALF + (j + 0.5) * (2 * SQUARE_HALF / n)
            col = tint(pav, 1.0 if (i + j) % 2 == 0 else 0.94)
            b.box(f"Pave_{i}_{j}", x, 0.05, z, 2 * SQUARE_HALF / n - 0.04, 0.2,
                  2 * SQUARE_HALF / n - 0.04, colour=col, material="Cobblestone",
                  tag="ground", cast_shadow=False)
    # kerb ring around the square
    for sgn in (-1, 1):
        b.box(f"Kerb_X{sgn}", 0, 0.16, sgn * (SQUARE_HALF + 0.3), 2 * SQUARE_HALF + 1.2, 0.3, 0.6,
              colour=PAL["kerb"][0], material="Concrete", tag="ground")
        b.box(f"Kerb_Z{sgn}", sgn * (SQUARE_HALF + 0.3), 0.16, 0, 0.6, 0.3, 2 * SQUARE_HALF + 1.2,
              colour=PAL["kerb"][0], material="Concrete", tag="ground")
    # radial inlay bands in the scan's lighter paving
    for sgn in (-1, 1):
        b.box(f"Inlay_{sgn}", sgn * 9.5, 0.13, 0, 1.1, 0.06, 2 * SQUARE_HALF - 4,
              colour=pav2, material="Cobblestone", tag="ground", collide=False,
              cast_shadow=False)

    # ---- fountain at the centre
    segs = 16
    for i in range(segs):
        a = 2 * math.pi * i / segs
        b.box(f"Basin_{i}", math.cos(a) * 3.1, 0.55, math.sin(a) * 3.1,
              1.35, 1.1, 0.34, colour=PAL["stone"][0], material="Rock", tag="prop",
              rot_z_deg=0.0)
        # orient each basin segment tangentially (rotate about Y instead)
        PARTS[-1].rot = rot_y(-math.degrees(a))
    b.box("BasinWater", 0, 0.72, 0, 5.6, 0.12, 5.6, colour=[96, 132, 148],
          material="Glass", transp=0.25, tag="prop", collide=False, cast_shadow=False)
    b.box("FountainPlinth", 0, 0.4, 0, 4.4, 0.8, 4.4, colour=PAL["stone"][0],
          material="Rock", tag="prop")
    b.box("FountainColumn", 0, 1.5, 0, 0.75, 2.2, 0.75, colour=PAL["stone"][0],
          material="Rock", tag="prop")
    b.box("FountainBowl", 0, 2.75, 0, 2.0, 0.28, 2.0, colour=PAL["stone"][0],
          material="Rock", tag="prop")
    b.box("FountainFinial", 0, 3.25, 0, 0.5, 0.9, 0.5, colour=[196, 168, 96],
          material="CorrodedMetal", tag="prop")

    # ---- lamps around the square
    lamp_positions = [(14, 14), (-14, 14), (14, -14), (-14, -14),
                      (17, 0), (-17, 0), (0, 17), (0, -17)]
    for i, (x, z) in enumerate(lamp_positions):
        b.box(f"Lamp_{i}_Post", x, 2.3, z, 0.24, 4.6, 0.24, colour=[46, 46, 50],
              material="Metal", tag="prop")
        b.box(f"Lamp_{i}_Base", x, 0.2, z, 0.55, 0.4, 0.55, colour=[46, 46, 50],
              material="Metal", tag="prop")
        b.box(f"Lamp_{i}_Arm", x, 4.7, z, 0.9, 0.12, 0.12, colour=[46, 46, 50],
              material="Metal", tag="prop")
        b.box(f"Lamp_{i}_Lantern", x + 0.45, 4.35, z, 0.42, 0.6, 0.42,
              colour=[255, 232, 160], material="Neon", tag="light", collide=False,
              cast_shadow=False)

    # ---- benches
    for i, (x, z, rot) in enumerate([(10, 10, 45), (-10, 10, -45), (10, -10, 135),
                                     (-10, -10, -135), (0, 12, 0), (0, -12, 180)]):
        bb = Builder("Square", (x, 0, z), rot)
        bb.box(f"Bench_{i}_Seat", 0, 0.55, 0, 2.2, 0.14, 0.62,
               colour=PAL["timber"][0], material="Wood", tag="prop")
        bb.box(f"Bench_{i}_Back", 0, 0.92, 0.28, 2.2, 0.5, 0.12,
               colour=PAL["timber"][0], material="Wood", tag="prop")
        for s in (-1, 1):
            bb.box(f"Bench_{i}_Leg{s}", s * 0.85, 0.26, 0, 0.14, 0.52, 0.5,
                   colour=[52, 52, 56], material="Metal", tag="prop")

    # ---- market stalls
    for i, (x, z) in enumerate([(-11, 3), (-11, -3), (11, 3), (11, -3)]):
        b.box(f"Stall_{i}_PostA", x - 1.1, 1.1, z - 1.0, 0.16, 2.2, 0.16,
              colour=PAL["timber"][0], material="Wood", tag="prop")
        b.box(f"Stall_{i}_PostB", x + 1.1, 1.1, z - 1.0, 0.16, 2.2, 0.16,
              colour=PAL["timber"][0], material="Wood", tag="prop")
        b.box(f"Stall_{i}_PostC", x - 1.1, 1.1, z + 1.0, 0.16, 2.2, 0.16,
              colour=PAL["timber"][0], material="Wood", tag="prop")
        b.box(f"Stall_{i}_PostD", x + 1.1, 1.1, z + 1.0, 0.16, 2.2, 0.16,
              colour=PAL["timber"][0], material="Wood", tag="prop")
        b.box(f"Stall_{i}_Canopy", x, 2.32, z, 2.7, 0.12, 2.6,
              colour=[168, 96, 84] if i % 2 == 0 else [92, 108, 132],
              material="Fabric", tag="prop")
        b.box(f"Stall_{i}_Table", x, 0.85, z, 2.2, 0.12, 1.3,
              colour=PAL["timber"][0], material="Wood", tag="prop")

    # ---- trees
    for i, (x, z) in enumerate([(-16, 6), (-16, -6), (16, 6), (16, -6),
                                (6, -16), (-6, -16), (6, 16), (-6, 16)]):
        b.box(f"Tree_{i}_Trunk", x, 1.7, z, 0.55, 3.4, 0.55, colour=PAL["bark"][0],
              material="Wood", tag="prop")
        for c, (dx, dy, dz, s, rz) in enumerate([(0, 4.2, 0, 2.5, 8),
                                                 (1.0, 3.7, 0.7, 1.8, -14),
                                                 (-0.9, 3.9, -0.6, 1.9, 22),
                                                 (0.2, 5.1, -0.3, 1.7, -6),
                                                 (-0.3, 3.4, 0.9, 1.5, 30)]):
            b.box(f"Tree_{i}_Canopy{c}", x + dx, dy, z + dz, s, s * 0.72, s,
                  colour=tint(GREENS["tree_canopy"], 1.0 + 0.06 * c), material="LeafyGrass",
                  tag="prop", rot_z_deg=rz)

    # ---- notice board, well, bollards
    b.box("NoticePostL", -6.4, 1.05, 8.4, 0.18, 2.1, 0.18, colour=PAL["timber"][0],
          material="Wood", tag="prop")
    b.box("NoticePostR", -5.0, 1.05, 8.4, 0.18, 2.1, 0.18, colour=PAL["timber"][0],
          material="Wood", tag="prop")
    b.box("NoticeBoard", -5.7, 1.75, 8.4, 1.7, 1.0, 0.1, colour=[196, 186, 162],
          material="Cardboard", tag="prop")
    b.box("NoticeRoof", -5.7, 2.35, 8.4, 2.0, 0.12, 0.5, colour=ACCENTS["notice_roof"],
          material="Wood", tag="prop")
    for i, (x, z) in enumerate([(4.4, 8.4), (2.2, 8.4), (-2.2, 8.4), (-4.4, 8.4)]):
        b.box(f"Bollard_{i}", x, 0.45, z, 0.22, 0.9, 0.22, colour=[58, 58, 62],
              material="Metal", tag="prop")
    # planters
    for i, (x, z) in enumerate([(13, 8), (-13, 8), (13, -8), (-13, -8)]):
        b.box(f"Planter_{i}", x, 0.4, z, 1.6, 0.7, 1.6, colour=PAL["stone"][0],
              material="Rock", tag="prop")
        b.box(f"Planter_{i}_Soil", x, 0.78, z, 1.35, 0.1, 1.35, colour=[62, 54, 40],
              material="Ground", tag="prop", collide=False)

    # spawn
    # Spawn pad: placed where tools/validate.py proves 1.2 m of clearance from
    # every prop. It used to sit on a bench, which V07 caught.
    b.box("SpawnPad", 0, 0.12, SPAWN[2], 6.0, 0.1, 4.0, colour=PAL["kerb"][0],
          material="Concrete", tag="spawnpad", collide=False, cast_shadow=False)
    add("Square/Spawn", "Square", (6.0, 0.4, 4.0), (SPAWN[0], 0.35, SPAWN[2]), IDENT,
        ACCENTS["spawn_pad"], "Concrete", 0, True, True, cls="SpawnLocation", tag="spawn")


# --------------------------------------------------------------------------
# Outskirts: the streets around the square. In the place file as well as in the
# renders, so nothing in a screenshot is scenery that the .rbxl lacks.
# --------------------------------------------------------------------------
def build_outskirts():
    b = Builder("Outskirts", (0, 0, 0), 0.0)
    rng = random.Random(7717)
    wall_tints = [PAL["wall_plaster"], PAL["wall_brick"], PAL["wall_stone"],
                  PAL["wall_brick2"]]
    roof_tints = [PAL["roof"], PAL["roof2"]]

    # sixteen outlying houses on two loose rings
    for i in range(16):
        ang = 2 * math.pi * (i + 0.5) / 16 + 0.14
        radius = 54.0 + (i % 3) * 7.0
        hx = math.cos(ang) * radius
        hz = math.sin(ang) * radius
        hw = rng.uniform(7.0, 12.0)
        hd = rng.uniform(6.0, 9.5)
        h = rng.uniform(7.0, 12.5)
        yaw = -math.degrees(ang) + 90 + rng.uniform(-14, 14)
        bb = Builder(f"Outskirts/H{i:02d}", (hx, 0, hz), yaw)
        wcol, wmat = wall_tints[i % len(wall_tints)]
        rcol, rmat = roof_tints[i % len(roof_tints)]
        bb.box("Body", 0, h / 2, 0, hw, h, hd, colour=wcol, material=wmat, tag="outskirt")
        # two roof slabs
        rise = hd * 0.42
        ang_r = math.degrees(math.atan2(rise, hd / 2 + 0.4))
        for sgn in (-1, 1):
            R = matmul(bb.R, rot_x(sgn * ang_r))
            add(f"Outskirts/H{i:02d}/Roof{sgn}", "Outskirts",
                (hw + 0.9, 0.26, math.hypot(hd / 2 + 0.4, rise)),
                bb.world(0, h + rise / 2, sgn * (hd / 2 + 0.4) / 2),
                R, rcol, rmat, 0.0, False, True, "Part", "outskirt")
        # a few windows so they do not read as blank slabs
        for w in range(2):
            for fl in range(max(2, int(h / 3.4))):
                wy = 1.8 + fl * 3.2
                if wy + 0.9 > h - 0.6:
                    break
                bb.box(f"Win{w}{fl}", -hw / 2 + w * hw, wy, -hd / 2 - 0.04,
                       0.95, 1.25, 0.08, colour=ACCENTS["glass"], material="Glass",
                       transp=0.35, collide=False, tag="window", cast_shadow=False)

    # a treeline and distant hills, so the horizon is not a bare plane
    for i in range(26):
        ang = 2 * math.pi * i / 26 + 0.05
        radius = 78.0 + (i % 5) * 4.0
        tx = math.cos(ang) * radius
        tz = math.sin(ang) * radius
        h = rng.uniform(6.5, 10.5)
        b.box(f"OutTree{i}_Trunk", tx, h * 0.22, tz, 0.6, h * 0.45, 0.6,
              colour=PAL["bark"][0], material="Wood", tag="outskirt")
        b.box(f"OutTree{i}_Crown", tx, h * 0.62, tz, h * 0.46, h * 0.52, h * 0.46,
              colour=tint(GREENS["outskirt_crown"], 0.9 + 0.05 * (i % 4)), material="LeafyGrass",
              tag="outskirt")
    # a continuous ridge, not nine isolated lumps: adjacent hills overlap so the
    # horizon is closed and no sky shows between them
    for i in range(20):
        ang = 2 * math.pi * i / 20
        radius = 138.0
        b.box(f"Hill{i}", math.cos(ang) * radius, 9.0, math.sin(ang) * radius,
              104.0, 17.0 + (i % 3) * 9.0, 48.0,
              colour=tint(GREENS["hill"], 0.92 + 0.05 * (i % 3)), material="Grass",
              tag="outskirt", collide=False, cast_shadow=False, rot_z_deg=0.0)


# --------------------------------------------------------------------------
# People: 64 residents, each with a home, a workplace and a post in the square
# --------------------------------------------------------------------------
FAMILY = ["Ash", "Bell", "Corvin", "Dunmore", "Ellery", "Fen", "Garrick", "Hollis",
          "Ivo", "Jory", "Kell", "Linden", "Marek", "Nell", "Oswin", "Pike",
          "Quill", "Renn", "Sable", "Thorne", "Ulric", "Vale", "Wren", "Yarrow",
          "Zell", "Bram", "Cis", "Dov", "Edda", "Foss", "Greta", "Hask",
          "Ingrid", "Joss", "Kira", "Lars", "Mira", "Noor", "Olek", "Petra",
          "Rurik", "Sig", "Tova", "Ulla", "Vidar", "Wilm", "Yara", "Ansel",
          "Berta", "Cato", "Dagne", "Emil", "Freya", "Gunnar", "Hedda", "Isak",
          "Juna", "Kasper", "Liv", "Milo", "Nadia", "Otto", "Pia", "Rolf"]
GIVEN = ["Ada", "Bram", "Cato", "Dora", "Elin", "Falk", "Gesa", "Hugo", "Ida",
         "Jonas", "Kurt", "Lena", "Milo", "Nora", "Otto", "Pim", "Roos", "Sven",
         "Tess", "Udo", "Vera", "Wim", "Yvo", "Zeno", "Bert", "Cilla", "Dirk",
         "Ebba", "Finn", "Gijs", "Hanna", "Ines", "Jens", "Klara", "Lars",
         "Maja", "Nele", "Olav", "Puck", "Rens", "Sanne", "Timo", "Ulla",
         "Vigo", "Wout", "Ines", "Yfke", "Zwaan", "Aagt", "Bo", "Cees", "Dunja",
         "Evert", "Fenna", "Gerd", "Hidde", "Ilse", "Jort", "Kees", "Lotte",
         "Maarten", "Nienke"]
ROLES = [
    ("innkeeper", "B01"), ("cook", "B01"), ("chambermaid", "B01"), ("stablehand", "B01"),
    ("baker", "B02"), ("miller", "B02"), ("apprentice baker", "B02"),
    ("blacksmith", "B03"), ("farrier", "B03"), ("bell founder", "B03"),
    ("salt merchant", "B04"), ("clerk", "B04"), ("warehouse porter", "B04"), ("scribe", "B04"),
    ("weaver", "B05"), ("dyer", "B05"), ("loomwright", "B05"),
    ("verger", "B06"), ("curate", "B06"),
    ("bookseller", "B07"), ("binder", "B07"),
    ("apothecary", "B08"), ("herbalist", "B08"), ("physician's assistant", "B08"),
    ("tavern keeper", "B09"), ("potboy", "B09"), ("fiddler", "B09"),
    ("watch sergeant", "B10"), ("constable", "B10"), ("gaoler", "B10"),
    ("market trader", "Square"), ("flower seller", "Square"), ("fishmonger", "Square"),
    ("cheesemonger", "Square"), ("tinker", "Square"), ("cooper", "Square"),
    ("carter", "Square"), ("water carrier", "Square"), ("lamp lighter", "Square"),
    ("night watchman", "Square"), ("town crier", "Square"), ("pigeon keeper", "Square"),
    ("schoolteacher", "B07"), ("midwife", "B08"), ("sexton", "B06"),
    ("rope maker", "B05"), ("tanner", "B03"), ("pewterer", "B03"),
    ("glassblower", "B08"), ("cartwright", "B04"), ("netter", "B07"),
    ("charcoal burner", "B02"), ("chandler", "B09"), ("brewer", "B09"),
    ("shearer", "B05"), ("goose girl", "Square"), ("orchardman", "Square"),
    ("rat catcher", "B10"), ("town clerk", "B10"), ("stone mason", "B04"),
    ("carpenter", "B02"), ("tiler", "B08"), ("huckster", "Square"),
    ("gleeman", "B09"),
]

CIVIC = ["the market cross", "the fountain", "the notice board", "the well",
         "the north bench", "the west stall", "the lime tree", "the east kerb"]

# Where each civic post physically is. Shared by TownServer (residents walk to
# it) and tools/render.py (screenshots stand the residents at it), so a render
# cannot put a person where the game does not.
POSTS = {
    "the market cross": [0.0, 0.0, 7.0],
    "the fountain": [0.0, 0.0, 5.2],
    "the notice board": [-5.7, 0.0, 7.0],
    "the well": [5.5, 0.0, 6.5],
    "the north bench": [0.0, 0.0, -12.0],
    "the west stall": [-11.0, 0.0, 3.0],
    "the lime tree": [6.0, 0.0, -16.0],
    "the east kerb": [17.0, 0.0, 0.0],
}


def build_people(rooms):
    npcs = []
    for i in range(64):
        role, place = ROLES[i]
        home = BUILDINGS[i % len(BUILDINGS)].key if place == "Square" else place
        home_rooms = [r for r in rooms if r["building"] == home and r["floor"] >= 2]
        if not home_rooms:
            home_rooms = [r for r in rooms if r["building"] == home]
        room = home_rooms[i % len(home_rooms)] if home_rooms else rooms[i % len(rooms)]
        palette = [
            [[128, 96, 78], [64, 72, 96], [96, 84, 64], [72, 88, 72]],
            [[148, 120, 92], [86, 64, 58], [60, 78, 84], [108, 100, 76]],
            [[92, 76, 60], [118, 92, 66], [70, 84, 92], [130, 118, 96]],
        ][i % 3]
        npcs.append({
            "id": f"N{i+1:02d}",
            "name": f"{GIVEN[i % len(GIVEN)]} {FAMILY[i % len(FAMILY)]}",
            "role": role,
            "workplace": place if place != "Square" else "Square",
            "home_building": home,
            "home_floor": room["floor"],
            "home_room": f"{room['building']}L{room['floor']}",
            "bed": None,               # assigned by validate/plan step
            "shirt": palette[0], "trousers": palette[1], "skin": None,
            "post": CIVIC[(i * 5) % len(CIVIC)],
            "hat": i % 3 == 0,
            "height": 1.62 + ((i * 7) % 23) / 100.0,
        })
    skins = [[236, 202, 172], [214, 172, 134], [176, 128, 96], [138, 96, 68],
             [96, 64, 46], [252, 220, 196]]
    for i, n in enumerate(npcs):
        n["skin"] = skins[(i * 3) % len(skins)]
    return npcs


# --------------------------------------------------------------------------
def main():
    rooms: list = []
    doors: list = []
    for spec in BUILDINGS:
        build_building(spec, doors, rooms)
    build_square()
    build_outskirts()
    npcs = build_people(rooms)

    # every resident gets a bed: one per NPC per room, laid out on a grid
    by_room: dict[str, list] = {}
    for n in npcs:
        by_room.setdefault(n["home_room"], []).append(n)
    beds = []
    for room_id, people in by_room.items():
        bld = room_id[:-2]
        fl = int(room_id[-1])
        anchor = next((r for r in rooms if r["building"] == bld and r["floor"] == fl), None)
        if not anchor:
            continue
        for k, person in enumerate(people):
            off = (k - (len(people) - 1) / 2) * 1.5
            pos = [anchor["centre"][0] + off, anchor["centre"][1] - 1.4,
                   anchor["centre"][2]]
            person["bed"] = {"room": room_id, "position": pos}
            beds.append({"npc": person["id"], "room": room_id, "position": pos})

    spec_out = {
        "meta": {
            "generator": "tools/townspec.py",
            "seed": 20261022,
            "units": "metres (studs) — +X east, +Z south, +Y up",
            "buildings": len(BUILDINGS),
            "floors": sum(b.floors for b in BUILDINGS),
            "npcs": len(npcs),
            "rooms": len(rooms),
            "parts": None,
            "square_half_width": SQUARE_HALF,
            "front_radius": FRONT_R,
        },
        "palette": {k: {"colour": v[0], "material": v[1]} for k, v in PAL.items()},
        "accents": {**ACCENTS, **{f"green_{k}": v for k, v in GREENS.items()}},
        "materials": MAT,
        "buildings": [{
            "key": b.key, "name": b.name, "programme": b.programme,
            "floors": b.floors, "width": b.width, "depth": b.depth,
            "angle_deg": b.angle_deg, "palette": b.palette,
        } for b in BUILDINGS],
        "rooms": rooms,
        "doors": doors,
        "npcs": npcs,
        "posts": POSTS,
        "beds": beds,
        "parts": [{
            "name": p.name, "group": p.group,
            "size": list(p.size), "pos": list(p.pos),
            "rot": p.rot,
            "colour": p.colour, "material": p.material,
            "material_token": MAT[p.material],
            "transp": p.transp, "collide": p.collide,
            "shadow": p.cast_shadow, "cls": p.cls, "tag": p.tag,
        } for p in PARTS],
    }
    spec_out["meta"]["parts"] = len(PARTS)
    os.makedirs(os.path.join(ROOT, "build"), exist_ok=True)
    out = os.path.join(ROOT, "build", "townspec.json")
    with open(out, "w") as f:
        json.dump(spec_out, f)
    tags: dict[str, int] = {}
    for p in PARTS:
        tags[p.tag] = tags.get(p.tag, 0) + 1
    print(f"wrote {out}  ({os.path.getsize(out)/1e6:.2f} MB)")
    print(f"parts={len(PARTS)}  buildings={len(BUILDINGS)}  "
          f"floors={sum(b.floors for b in BUILDINGS)}  rooms={len(rooms)}  "
          f"npcs={len(npcs)}  doors={len(doors)}")
    print("by tag:", ", ".join(f"{k}={v}" for k, v in sorted(tags.items(), key=lambda kv: -kv[1])))


if __name__ == "__main__":
    main()
