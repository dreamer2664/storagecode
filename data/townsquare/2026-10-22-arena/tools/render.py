#!/usr/bin/env python3
"""render.py — offline rasteriser for Winterlichtplatz.

No Blender, no GPU: this sandbox has 2 vCPU and no Cycles, so the screenshots are
made by a numpy z-buffer renderer that reads the SAME build/townspec.json the
place file is compiled from. A render therefore cannot show a building the .rbxl
does not contain.

What it does per frame:
  * flat-shaded triangles with a sun shadow map (3x3 PCF), hemispheric ambient,
    and point lights for the neon lanterns (interiors and night shots need them);
  * albedo sampled from the CC0 photogrammetry scans, tiled by world position and
    tinted so that the surface's mean colour equals the part's colour in the place
    file — the render and the .rbxl agree on colour instead of drifting apart;
  * supersampled (SSAA) and box-downsampled, with fog toward the sky colour.

    python3 tools/render.py                # all views
    python3 tools/render.py --only hero --scale 0.5   # quick single test
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SPEC = json.load(open(os.path.join(ROOT, "build", "townspec.json")))

# ---------------------------------------------------------------- texture bank
TEX_BY_MATERIAL = {
    "Cobblestone": "PavingStones151", "Pavement": "PavingStones151",
    "Pebble": "PavingStones151", "Ground": "Gravel043",
    "Brick": "Bricks075A", "Plaster": "Plaster007", "Rock": "Rock064",
    "Concrete": "Concrete048", "Limestone": "Concrete048",
    "Wood": "Wood092", "WoodPlanks": "Planks039", "Cardboard": "Planks039",
    "CeramicTiles": "Tiles138", "ClayRoofTiles": "Tiles138",
    "RoofShingles": "Tiles138", "Slate": "Tiles138", "Marble": "Tiles138",
    "Fabric": "Planks039", "Leather": "Bark014", "Metal": "Concrete048",
    "CorrodedMetal": "Concrete048", "Neon": "Concrete048", "Grass": "Gravel043",
    "LeafyGrass": "Gravel043", "Granite": "Rock064", "Sandstone": "Rock064",
    "SmoothPlastic": "Concrete048", "Plastic": "Concrete048",
}
TILE_METRES = {
    "Cobblestone": 8.0, "Pavement": 8.0, "Pebble": 6.0, "Ground": 14.0,
    "Brick": 4.0, "Plaster": 6.0, "Rock": 5.0, "Concrete": 6.0,
    "Wood": 3.0, "WoodPlanks": 4.0, "Fabric": 2.0, "CeramicTiles": 3.0,
    "ClayRoofTiles": 6.0, "Metal": 5.0, "LeafyGrass": 2.2, "Bark": 2.4,
    "Neon": 3.0, "CorrodedMetal": 3.0, "Limestone": 6.0, "Slate": 5.0,
    "Grass": 10.0, "Cardboard": 3.0, "SmoothPlastic": 4.0, "Plastic": 4.0,
    "Leather": 3.0, "Marble": 4.0, "Granite": 5.0, "Sandstone": 5.0,
    "RoofShingles": 4.0,
}


def load_textures():
    tex = {}
    for role_file in os.listdir(os.path.join(ROOT, "assets", "scans")):
        if not role_file.endswith(".jpg"):
            continue
        path = os.path.join(ROOT, "assets", "scans", role_file)
        img = Image.open(path).convert("RGB").resize((512, 512), Image.LANCZOS)
        a = np.asarray(img, dtype=np.float32) / 255.0
        # de-light the scan: normalise so the mean is 1.0, keep only detail
        mean = a.reshape(-1, 3).mean(axis=0)
        raw = a / np.maximum(mean, 1e-3)
        # pull the detail toward 1.0: a scan's speckle at 6 m tiling reads as
        # static; 55% contrast keeps grain and loses the noise
        tex[role_file] = {"detail": 1.0 + (raw - 1.0) * 0.55, "mean": mean}
    return tex


TEX = load_textures()


def texture_for(asset_id: str):
    for f, v in TEX.items():
        if f.startswith(asset_id):
            return v
    return None


# ---------------------------------------------------------------- scene build
def build_scene(hide=None, only_group=None, include_npcs=True, night=False):
    """-> (tris, meta) with world-space vertices, normals, colours, uv hints."""
    verts = []
    normals = []
    colours = []
    texids = []
    emissive = []
    refl = []
    tiles = []
    corners = np.array([[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
                        [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]], dtype=np.float64)
    faces = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1),
             (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]

    all_parts = list(SPEC["parts"])
    if include_npcs:
        for rp in resident_parts(night=night):
            all_parts.append({
                "group": "Residents", "name": "resident", "size": rp["size"],
                "pos": rp["pos"], "rot": rp["rot"], "colour": [int(round(c * 255)) for c in rp["colour"]],
                "material": rp["material"], "transp": 0.0, "collide": False,
                "tag": "resident", "cls": "Part",
            })
    for p in all_parts:
        if only_group and not p["group"].startswith(only_group):
            continue
        if hide and hide(p):
            continue
        R = np.array(p["rot"], dtype=np.float64)
        size = np.array(p["size"], dtype=np.float64) / 2.0
        pos = np.array(p["pos"], dtype=np.float64)
        local = corners * size
        world = local @ R.T + pos
        col = np.array(p["colour"], dtype=np.float32) / 255.0
        mat = p["material"]
        tex = texture_for(TEX_BY_MATERIAL.get(mat, "Concrete048"))
        if tex is None:
            tex = TEX["Concrete048_albedo_512.jpg"]
        # tint so the textured mean equals the part colour from the place file
        for f in faces:
            idx = list(f)
            for tri in ((idx[0], idx[1], idx[2]), (idx[0], idx[2], idx[3])):
                a, b, c = world[tri[0]], world[tri[1]], world[tri[2]]
                n = np.cross(b - a, c - a)
                ln = np.linalg.norm(n)
                if ln < 1e-9:
                    continue
                verts.append([a, b, c])
                normals.append(n / ln)
                colours.append(col)
                texids.append(tex)
                tiles.append(TILE_METRES.get(mat, 6.0))
                emissive.append(1.0 if mat == "Neon" else 0.0)
                refl.append({"Glass": 0.16, "Metal": 0.22, "CorrodedMetal": 0.18,
                             "DiamondPlate": 0.2, "Marble": 0.12,
                             "CeramicTiles": 0.08}.get(mat, 0.0))
    return {
        "v": np.array(verts, dtype=np.float64),
        "n": np.array(normals, dtype=np.float64),
        "c": np.array(colours, dtype=np.float32),
        "tex": texids,
        "tile": np.array(tiles, dtype=np.float64),
        "emis": np.array(emissive, dtype=np.float32),
        "refl": np.array(refl, dtype=np.float32),
    }


# ---------------------------------------------------------------- camera
class Camera:
    def __init__(self, eye, target, fov=52.0, up=(0, 1, 0), ortho=None):
        self.eye = np.array(eye, dtype=np.float64)
        f = np.array(target, dtype=np.float64) - self.eye
        f = f / np.linalg.norm(f)
        self.forward = f
        upv = np.array(up, dtype=np.float64)
        r = np.cross(f, upv)
        if np.linalg.norm(r) < 1e-6:
            r = np.cross(f, np.array([0.0, 0.0, 1.0]))
        r = r / np.linalg.norm(r)
        u = np.cross(r, f)
        self.right, self.up = r, u
        self.fov = math.radians(fov)
        self.ortho = ortho

    def project(self, pts):
        d = pts - self.eye
        x = d @ self.right
        y = d @ self.up
        z = d @ self.forward
        return x, y, z

    def to_screen(self, x, y, z, W, H):
        if self.ortho is not None:
            sx = (x / self.ortho + 0.5) * W
            sy = (0.5 - y / self.ortho) * H
            return sx, sy, z
        f = (H * 0.5) / math.tan(self.fov * 0.5)
        zz = np.where(np.abs(z) < 1e-6, 1e-6, z)
        return x * f / zz + W * 0.5, H * 0.5 - y * f / zz, z




# ---------------------------------------------------------------- residents
def resident_parts(night=False):
    """Block figures for the 64 residents, at the same positions TownServer uses:
    their civic post by day, their own bed at night. Colours come from TownData."""
    parts = []
    posts = SPEC["posts"]
    beds = {b["npc"]: b for b in SPEC["beds"]}
    for i, n in enumerate(SPEC["npcs"]):
        if night:
            bed = beds.get(n["id"])
            if not bed:
                continue
            bx, by, bz = bed["position"]
            base = (bx, by - 0.55, bz)
            # a person asleep is a shorter stack of blocks
            torso_y, head_y = 0.55, 1.05
        else:
            p = posts.get(n["post"], [0.0, 0.0, 8.0])
            jx = ((i * 37) % 11) - 5
            jz = ((i * 53) % 11) - 5
            base = (p[0] + jx * 1.15, p[1], p[2] + jz * 1.15)
            torso_y, head_y = 1.25, 2.02
        scale = n["height"] / 1.75
        shirt = [c / 255.0 for c in n["shirt"]]
        trousers = [c / 255.0 for c in n["trousers"]]
        skin = [c / 255.0 for c in n["skin"]]
        yaw = (i * 1.7) % 6.283
        parts.append({"size": (0.92 * scale, 1.15 * scale, 0.52 * scale),
                      "pos": (base[0], base[1] + torso_y, base[2]),
                      "colour": shirt, "material": "Fabric", "rot": rot_y(math.degrees(yaw))})
        parts.append({"size": (0.56 * scale, 0.56 * scale, 0.56 * scale),
                      "pos": (base[0], base[1] + head_y, base[2]),
                      "colour": skin, "material": "SmoothPlastic", "rot": rot_y(math.degrees(yaw))})
        if n.get("hat"):
            parts.append({"size": (0.66 * scale, 0.18 * scale, 0.66 * scale),
                          "pos": (base[0], base[1] + head_y + 0.34 * scale, base[2]),
                          "colour": [0.23, 0.19, 0.16], "material": "Wood",
                          "rot": rot_y(math.degrees(yaw))})
        for sgn in (-1, 1):
            off = rot_y(math.degrees(yaw))
            dx, _, dz = apply_np(off, (sgn * 0.19 * scale, 0, 0))
            parts.append({"size": (0.30 * scale, 1.02 * scale, 0.32 * scale),
                          "pos": (base[0] + dx, base[1] + 0.51 * scale, base[2] + dz),
                          "colour": trousers, "material": "Fabric", "rot": off})
            ax, _, az = apply_np(off, (sgn * 0.60 * scale, 0, 0))
            parts.append({"size": (0.26 * scale, 1.02 * scale, 0.28 * scale),
                          "pos": (base[0] + ax, base[1] + 1.28 * scale, base[2] + az),
                          "colour": shirt, "material": "Fabric", "rot": off})
    return parts


def apply_np(m, v):
    return (m[0][0] * v[0] + m[0][1] * v[1] + m[0][2] * v[2],
            m[1][0] * v[0] + m[1][1] * v[1] + m[1][2] * v[2],
            m[2][0] * v[0] + m[2][1] * v[1] + m[2][2] * v[2])


def rot_y(deg):
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    return [[c, 0, sn], [0, 1, 0], [-sn, 0, c]]


# ---------------------------------------------------------------- shadows
def shadow_map(scene, sun_dir, centre, extent, res=1536):
    """Orthographic depth map looking along the sun direction."""
    cam = Camera(centre + sun_dir * extent * 2.0, centre, ortho=extent)
    depth = np.full((res, res), 1e9, dtype=np.float32)
    v = scene["v"]
    x, y, z = cam.project(v.reshape(-1, 3))
    x = x.reshape(-1, 3)
    y = y.reshape(-1, 3)
    z = z.reshape(-1, 3)
    sx, sy, sz = cam.to_screen(x, y, z, res, res)
    for i in range(len(sx)):
        _raster_depth(depth, sx[i], sy[i], sz[i])
    return cam, depth, extent


def _raster_depth(depth, sx, sy, sz):
    res = depth.shape[0]
    minx, maxx = int(max(0, math.floor(sx.min()))), int(min(res - 1, math.ceil(sx.max())))
    miny, maxy = int(max(0, math.floor(sy.min()))), int(min(res - 1, math.ceil(sy.max())))
    if minx >= maxx or miny >= maxy:
        return
    d = (sx[1] - sx[0]) * (sy[2] - sy[0]) - (sx[2] - sx[0]) * (sy[1] - sy[0])
    if abs(d) < 1e-12:
        return
    xs = np.arange(minx, maxx + 1) + 0.5
    ys = np.arange(miny, maxy + 1) + 0.5
    gx, gy = np.meshgrid(xs, ys)
    w0 = ((sx[1] - gx) * (sy[2] - gy) - (sx[2] - gx) * (sy[1] - gy)) / d
    w1 = ((sx[2] - gx) * (sy[0] - gy) - (sx[0] - gx) * (sy[2] - gy)) / d
    w2 = 1.0 - w0 - w1
    inside = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
    if not inside.any():
        return
    zz = w0 * sz[0] + w1 * sz[1] + w2 * sz[2]
    sub = depth[miny:maxy + 1, minx:maxx + 1]
    np.minimum(sub, np.where(inside, zz, 1e9), out=sub)


def sample_shadow(cam, depth, extent, pts, bias=0.06):
    res = depth.shape[0]
    x, y, z = cam.project(pts)
    sx, sy, sz = cam.to_screen(x, y, z, res, res)
    ix = np.clip(sx.astype(np.int32), 0, res - 1)
    iy = np.clip(sy.astype(np.int32), 0, res - 1)
    lit = np.zeros(pts.shape[0], dtype=np.float32)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            jx = np.clip(ix + dx, 0, res - 1)
            jy = np.clip(iy + dy, 0, res - 1)
            stored = depth[jy, jx]
            lit += (sz <= stored + bias).astype(np.float32)
    return lit / 9.0


# ---------------------------------------------------------------- main raster
SKY_TOP = np.array([0.24, 0.42, 0.68], dtype=np.float32)
SKY_HORIZON = np.array([0.62, 0.70, 0.80], dtype=np.float32)


def render(scene, cam, W, H, sun_dir, sun_col, ambient, sky, point_lights=(),
           shadow=(None, None, None), fog=(90.0, 520.0), exposure=1.0, night=False):
    colour = np.zeros((H, W, 3), dtype=np.float32)
    depthb = np.full((H, W), 1e9, dtype=np.float32)

    # sky background with a soft gradient
    yy = (np.arange(H, dtype=np.float32) / H)[:, None]
    grad = (1.0 - yy)[..., None] * SKY_TOP + yy[..., None] * SKY_HORIZON
    colour[:] = grad * (0.35 if night else 1.0)

    v = scene["v"].reshape(-1, 3)
    x, y, z = cam.project(v)
    x = x.reshape(-1, 3)
    y = y.reshape(-1, 3)
    z = z.reshape(-1, 3)

    # crude frustum cull by centroid
    cx, cy, cz = x.mean(axis=1), y.mean(axis=1), z.mean(axis=1)
    if cam.ortho is None:
        lim = math.tan(cam.fov * 0.5) * 1.6
        keep = (cz > 0.25) & (np.abs(cx) < np.abs(cz) * lim + 40) & (np.abs(cy) < np.abs(cz) * lim + 40)
    else:
        keep = (np.abs(cx) < cam.ortho) & (np.abs(cy) < cam.ortho)

    idxs = np.nonzero(keep)[0]
    sx, sy, sz = cam.to_screen(x, y, z, W, H)

    sun_dir = sun_dir / np.linalg.norm(sun_dir)
    shadow_cam, shadow_depth, shadow_extent = shadow

    NEAR = 0.15

    def draw(ax, ay, az, tri_idx):
        _raster_tri(
            colour, depthb, ax, ay, az,
            scene["n"][tri_idx], scene["c"][tri_idx], scene["tex"][tri_idx],
            scene["tile"][tri_idx], scene["emis"][tri_idx], scene["refl"][tri_idx],
            sun_dir, sun_col, ambient, sky, point_lights,
            shadow_cam, shadow_depth, shadow_extent, fog, exposure, cam, night,
        )

    for i in idxs:
        tri = np.stack([x[i], y[i], z[i]], axis=-1)      # camera space, 3 verts
        if cam.ortho is None and tri[:, 2].min() <= NEAR:
            # Clip against the near plane instead of dropping the triangle. Without
            # this, any single triangle large enough to pass behind the camera —
            # notably the 640 m ground plane — vanishes completely, and the sky
            # shows through the holes it leaves.
            poly = list(tri)
            clipped = []
            n = len(poly)
            for k in range(n):
                a = poly[k]
                b = poly[(k + 1) % n]
                ain = a[2] >= NEAR
                bin_ = b[2] >= NEAR
                if ain:
                    clipped.append(a)
                if ain != bin_:
                    t = (NEAR - a[2]) / (b[2] - a[2])
                    clipped.append(a + (b - a) * t)
            if len(clipped) < 3:
                continue
            for k in range(1, len(clipped) - 1):
                fan = np.stack([clipped[0], clipped[k], clipped[k + 1]])
                px, py, pz = cam.to_screen(fan[:, 0], fan[:, 1], fan[:, 2], W, H)
                if np.any(pz <= 0):
                    continue
                draw(px, py, pz, i)
            continue
        if cam.ortho is None and tri[:, 2].max() <= NEAR:
            continue
        draw(sx[i], sy[i], z[i], i)

    # Reinhard-ish shoulder: keeps highlight detail in light plaster and lime
    # wash instead of clipping it to flat white.
    img = colour * 1.06
    img = img / (1.0 + img) * 1.62
    return np.clip(img, 0.0, 1.0)


def _raster_tri(colour, depthb, sx, sy, sz, normal, base_col, tex, tile,
                emis, reflectivity, sun_dir, sun_col, ambient, sky, point_lights,
                shadow_cam, shadow_depth, shadow_extent, fog, exposure, cam, night):
    H, W = depthb.shape
    minx, maxx = int(max(0, math.floor(sx.min()))), int(min(W - 1, math.ceil(sx.max())))
    miny, maxy = int(max(0, math.floor(sy.min()))), int(min(H - 1, math.ceil(sy.max())))
    if minx >= maxx or miny >= maxy:
        return
    if (maxx - minx) * (maxy - miny) > 40_000_000:
        return
    d = (sx[1] - sx[0]) * (sy[2] - sy[0]) - (sx[2] - sx[0]) * (sy[1] - sy[0])
    if abs(d) < 1e-12:
        return
    xs = np.arange(minx, maxx + 1) + 0.5
    ys = np.arange(miny, maxy + 1) + 0.5
    gx, gy = np.meshgrid(xs, ys)
    w0 = ((sx[1] - gx) * (sy[2] - gy) - (sx[2] - gx) * (sy[1] - gy)) / d
    w1 = ((sx[2] - gx) * (sy[0] - gy) - (sx[0] - gx) * (sy[2] - gy)) / d
    w2 = 1.0 - w0 - w1
    inside = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
    if not inside.any():
        return

    # depth: perspective-correct via 1/z, which interpolates linearly in screen space
    iz = 1.0 / np.maximum(sz, 1e-4)
    izp = w0 * iz[0] + w1 * iz[1] + w2 * iz[2]
    zz = 1.0 / np.maximum(izp, 1e-9)

    sub = depthb[miny:maxy + 1, minx:maxx + 1]
    closer = inside & (zz < sub)
    if not closer.any():
        return
    sub[closer] = zz[closer]

    # world position of every covered pixel
    hx = gx[closer]
    hy = gy[closer]
    zc = zz[closer]
    if cam.ortho is not None:
        xc = (hx / W - 0.5) * cam.ortho
        yc = (0.5 - hy / H) * cam.ortho
    else:
        fpx = (H * 0.5) / math.tan(cam.fov * 0.5)
        xc = (hx - W * 0.5) * zc / fpx
        yc = (H * 0.5 - hy) * zc / fpx
    pts = (cam.eye
           + cam.right * xc[:, None]
           + cam.up * yc[:, None]
           + cam.forward * zc[:, None])

    n = normal
    ndl = max(0.0, float(np.dot(n, -sun_dir)))
    if shadow_cam is not None:
        lit = ndl * sample_shadow(shadow_cam, shadow_depth, shadow_extent, pts)
    else:
        lit = np.full(pts.shape[0], ndl, dtype=np.float32)

    hemi = np.clip(n[1] * 0.5 + 0.5, 0.0, 1.0)
    amb = ambient * (0.55 + 0.45 * hemi)

    # world-space planar UV from the dominant normal axis, then tile the scan
    an = np.abs(n)
    if an[1] >= an[0] and an[1] >= an[2]:
        u, vv = pts[:, 0], pts[:, 2]
    elif an[0] >= an[2]:
        u, vv = pts[:, 2], pts[:, 1]
    else:
        u, vv = pts[:, 0], pts[:, 1]
    tu = np.mod(u / tile, 1.0)
    tv = np.mod(vv / tile, 1.0)
    detail = tex["detail"]
    ti = np.clip((tv * 511).astype(np.int32), 0, 511)
    tj = np.clip((tu * 511).astype(np.int32), 0, 511)
    albedo = detail[ti, tj] * base_col[None, :]

    light = sun_col[None, :] * np.asarray(lit, dtype=np.float32)[:, None] + amb
    for (lp, lcol, lint, lrange) in point_lights:
        dvec = lp - pts
        dist2 = np.maximum(np.einsum("ij,ij->i", dvec, dvec), 1e-4)
        fall = np.clip(1.0 - dist2 / (lrange * lrange), 0.0, 1.0) ** 2
        nd = np.clip(np.einsum("ij,j->i", dvec / np.sqrt(dist2)[:, None], n), 0.0, 1.0)
        light = light + lcol[None, :] * (lint * fall * (0.35 + 0.65 * nd))[:, None]

    light = np.clip(light, 0.0, 2.6)   # no single lamp may run away
    shaded = albedo * light
    # reflective surfaces: sky reflection by normal (fresnel-ish) + sun highlight
    if reflectivity > 0.0:
        view = cam.eye - pts
        view = view / np.maximum(np.linalg.norm(view, axis=1)[:, None], 1e-6)
        up_facing = np.clip(n[1] * 0.5 + 0.5, 0.0, 1.0)
        sky_ref = (SKY_HORIZON[None, :] * 0.55 + SKY_TOP[None, :] * 0.45) * (
            0.45 + 0.55 * up_facing)
        cos_v = np.clip(np.abs(np.einsum("ij,j->i", view, n)), 0.0, 1.0)
        fres = (1.0 - cos_v) ** 2.2
        half = (-sun_dir + 1e-6)
        spec_amt = np.clip(np.dot(n, half), 0.0, 1.0) ** 48
        shaded = shaded * (1.0 - reflectivity) + reflectivity * (
            albedo * 0.35
            + sky_ref * (0.35 + 0.65 * fres)[:, None]
            + sun_col[None, :] * (spec_amt * 0.9))
    if emis > 0.5:
        shaded = np.broadcast_to(base_col * (1.55 if night else 1.12), shaded.shape).copy()

    dist = np.linalg.norm(pts - cam.eye, axis=1)
    fog_near, fog_far = fog
    fg = np.clip((dist - fog_near) / max(1e-3, fog_far - fog_near), 0.0, 1.0)[:, None]
    fog_col = SKY_HORIZON * (0.30 if night else 1.0)
    shaded = shaded * (1.0 - fg) + fog_col * fg

    # NB: assign through a boolean mask on the slice view. A slice of an
    # (H,W,3) array is strided, so .reshape(-1,3) would return a COPY and the
    # shading would be thrown away (which is exactly what happened first time).
    region = colour[miny:maxy + 1, minx:maxx + 1]
    region[closer] = (shaded * exposure).astype(np.float32)


# ---------------------------------------------------------------- views
def sun_vector(azimuth_deg, elevation_deg):
    a = math.radians(azimuth_deg)
    e = math.radians(elevation_deg)
    d = np.array([math.cos(e) * math.cos(a), math.sin(e), math.cos(e) * math.sin(a)])
    return -d / np.linalg.norm(d)   # direction *toward* the sun is -d; we return the light travel dir


def gather_lights(intensity=0.62, reach=13.0):
    out = []
    for p in SPEC["parts"]:
        if p["material"] == "Neon":
            out.append((np.array(p["pos"]), np.array([1.0, 0.88, 0.68], dtype=np.float32),
                         intensity, reach))
    return out


VIEWS = [
    # name, eye, target, fov, sun(az, el), ambient, night
    ("01_square_hero",      (5, 34, 48),    (0, 5, -1),    47, (232, 32), 0.90, False),
    ("02_spawn_eye_level",  (9.5, 1.8, 24), (0.0, 6.5, -4), 58, (232, 34), 0.92, False),
    ("03_fountain_low",     (10.5, 1.6, 9.5), (0.0, 2.6, 0.0), 68, (215, 24), 0.86, False),
    ("04_salt_house_angle", (14, 2.4, 20),  (26, 12, -18), 62, (240, 30), 0.86, False),
    ("05_street_canyon",    (-20, 2.0, 17), (-40, 10, -26), 60, (250, 24), 0.94, False),
    ("06_roofline_west",    (24, 20, 30),   (0, 6, 2),     50, (200, 28), 0.86, False),
    ("07_sunset_long",      (58, 15, 52),   (-6, 6, -8),   50, (298, 5),  0.86, False),
    ("08_night_square",     (14, 5.5, 22),  (-2, 5, -3),   58, (300, 40), 0.14, True),
    ("09_plan_ortho",       (0, 150, 0.1),  (0, 0, 0),     40, (180, 78), 1.05, False),
    ("10_interior_shop",    None, None, 66, None, 0.26, False),
    ("11_cutaway_b01",      None, None, 50, (205, 34), 0.86, False),
    ("12_cutaway_b04",      None, None, 50, (225, 32), 0.94, False),
]


def interior_camera(building_key, floor, room_label=None):
    """Stand inside a room the town spec actually schedules."""
    rooms = [r for r in SPEC["rooms"]
             if r["building"] == building_key and r["floor"] == floor]
    if room_label:
        rooms = [r for r in rooms if r["label"] == room_label] or rooms
    room = max(rooms, key=lambda r: r["size"][0] * r["size"][2])
    cx, cy, cz = room["centre"]
    sx, sy, sz = room["size"]
    b = next(b for b in SPEC["buildings"] if b["key"] == building_key)
    ang = math.radians(b["angle_deg"])
    # local +Z of the building points away from the square; sit back, face the front
    yaw = math.radians(90.0 - b["angle_deg"])
    def fwd(x, z):
        return (x * math.cos(yaw) + z * math.sin(yaw), -x * math.sin(yaw) + z * math.cos(yaw))
    # stand just inside the back of the room, look across it at the facade windows
    fx, fz = fwd(0.0, -1.0)          # towards the front (square side)
    bx, bz = fwd(0.0, 1.0)
    side_x, side_z = fwd(1.0, 0.0)
    eye = (cx + bx * sz * 0.30 + side_x * sx * 0.22,
           cy + 0.45,
           cz + bz * sz * 0.30 + side_z * sx * 0.22)
    target = (cx + fx * sz * 0.55 - side_x * sx * 0.18,
              cy - 0.05,
              cz + fz * sz * 0.55 - side_z * sx * 0.18)
    return eye, target


def interior_camera_old(building_key, floor, offset_in_room=0.0):
    """Stand inside a real room: eye at 1.65 m, looking across the room."""
    b = next(b for b in SPEC["buildings"] if b["key"] == building_key)
    ang = math.radians(b["angle_deg"])
    cx = math.cos(ang) * (SPEC["meta"]["front_radius"] + b["depth"] / 2)
    cz = math.sin(ang) * (SPEC["meta"]["front_radius"] + b["depth"] / 2)
    yaw = math.radians(90.0 - b["angle_deg"])
    # local room point, then rotate into world
    def world(lx, ly, lz):
        return (cx + lx * math.cos(yaw) + lz * math.sin(yaw),
                ly,
                cz - lx * math.sin(yaw) + lz * math.cos(yaw))
    eye_y = (4.4 + (floor - 2) * 3.6) + 1.65 if floor > 1 else 1.75
    eye = world(-b["width"] * 0.18, eye_y, b["depth"] * 0.22)
    target = world(b["width"] * 0.25, eye_y - 0.35, -b["depth"] * 0.30)
    return eye, target


def downsample(img, factor):
    if factor <= 1:
        return (np.clip(img, 0, 1) * 255).astype(np.uint8)
    H, W, _ = img.shape
    H2, W2 = H // factor, W // factor
    a = img[:H2 * factor, :W2 * factor].reshape(H2, factor, W2, factor, 3).mean(axis=(1, 3))
    return (np.clip(a, 0, 1) * 255).astype(np.uint8)


def vignette(img):
    H, W, _ = img.shape
    yy, xx = np.mgrid[0:H, 0:W]
    cx, cy = W / 2, H / 2
    r = np.sqrt(((xx - cx) / cx) ** 2 + ((yy - cy) / cy) ** 2)
    v = np.clip(1.15 - 0.28 * r ** 2, 0.0, 1.0)[..., None]
    return img * v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None)
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--ss", type=float, default=1.5, help="supersample factor")
    args = ap.parse_args()

    outdir = os.path.join(ROOT, "renders")
    os.makedirs(outdir, exist_ok=True)
    W = int(1600 * args.scale)
    H = int(900 * args.scale)
    SW, SH = int(W * args.ss), int(H * args.ss)
    lights = gather_lights()
    base_scene = build_scene()
    print(f"scene: {len(base_scene['v'])} triangles")

    for (name, eye, target, fov, sun, amb, night) in VIEWS:
        if args.only and args.only not in name:
            continue
        t0 = time.time()
        scene = base_scene
        point_lights = []
        if "interior" in name:
            if "shop" in name:
                key, floor = "B04", 1
            else:
                best = max((r for r in SPEC["rooms"] if r["floor"] >= 2),
                           key=lambda r: r["size"][0] * r["size"][2])
                key, floor = best["building"], best["floor"]
            eye, target = interior_camera(key, floor)
            fov = 80
            sun = (225, 26)
            near = sorted(lights, key=lambda l: np.linalg.norm(l[0] - np.array(eye)))
            point_lights = near[:2]
            amb = 0.34
        elif "cutaway" in name:
            # Cut B04 open along its own facade plane: hide everything of B04
            # that sits in front of its centre line, so the section shows the
            # floor slabs, partitions, furniture and stairs inside.
            # Dollhouse section: remove B04's walls, windows, roof and doors and
            # leave the slabs, partitions, furniture and stairs standing. What is
            # left is exactly what the place file has inside that building.
            cut_key = "B01" if "b01" in name else "B04"

            def hide(p, _k=cut_key):
                if not (p["group"] == _k or p["group"].startswith(_k + "/")):
                    return False
                return p["tag"] in ("wall", "window", "roof", "structure")
            scene = build_scene(hide=hide)
            cb = next(b for b in SPEC["buildings"] if b["key"] == cut_key)
            a = math.radians(cb["angle_deg"])
            bxc = math.cos(a) * (SPEC["meta"]["front_radius"] + cb["depth"] / 2)
            bzc = math.sin(a) * (SPEC["meta"]["front_radius"] + cb["depth"] / 2)
            eye = (bxc * 0.30, 19.0, bzc * 0.30)
            target = (bxc, 8.0, bzc)
        elif night:
            scene = build_scene(include_npcs=True, night=False)
            bright = gather_lights(intensity=1.35, reach=22.0)
            near = sorted(bright, key=lambda l: np.linalg.norm(l[0] - np.array([14, 5.5, 22])))
            point_lights = near[:9]
            amb = 0.34

        cam = Camera(eye, target, fov=fov, ortho=(84.0 if "plan" in name else None))
        if "plan" in name:
            eye = (0, 120, 0.1)
            cam = Camera(eye, (0, 0, 0), ortho=84.0)
        sd = sun_vector(*sun)
        sun_col = np.array([1.04, 0.98, 0.88], dtype=np.float32)
        global SKY_TOP, SKY_HORIZON
        if "sunset" in name:
            SKY_TOP = np.array([0.20, 0.24, 0.42], dtype=np.float32)
            SKY_HORIZON = np.array([0.92, 0.60, 0.38], dtype=np.float32)
        else:
            SKY_TOP = np.array([0.24, 0.42, 0.68], dtype=np.float32)
            SKY_HORIZON = np.array([0.62, 0.70, 0.80], dtype=np.float32)
        exposure = 1.05
        if "interior" in name:
            exposure = 0.88
        if night:
            sun_col = np.array([0.26, 0.33, 0.46], dtype=np.float32)
            exposure = 1.02
        elif "sunset" in name:
            sun_col = np.array([1.30, 0.86, 0.52], dtype=np.float32)
        if "interior" in name:
            centre = np.array([eye[0], 4.0, eye[2]])
            sh_cam, sh_dep, sh_ext = shadow_map(scene, sd, centre, 34.0, res=1600)
        else:
            centre = np.array([0.0, 6.0, 0.0])
            sh_cam, sh_dep, sh_ext = shadow_map(scene, sd, centre, 74.0, res=1400)

        img = render(scene, cam, SW, SH, sd, sun_col, amb,
                     SKY_HORIZON, point_lights=point_lights,
                     shadow=(sh_cam, sh_dep, sh_ext),
                     fog=(420.0, 2000.0), exposure=exposure, night=night)
        img = vignette(img)
        arr = downsample(img, int(round(args.ss)) if args.ss >= 1 else 1)
        path = os.path.join(outdir, f"{name}.png")
        Image.fromarray(arr).save(path, optimize=True)
        print(f"  {name}: {arr.shape[1]}x{arr.shape[0]} in {time.time()-t0:.1f}s -> {os.path.relpath(path, ROOT)}")


if __name__ == "__main__":
    main()
