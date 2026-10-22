#!/usr/bin/env python3
"""Fetch the CC0 photogrammetry scans this project is calibrated against.

Every entry is creationMethod == PBRPhotogrammetry (a real captured scan, not a
procedural texture). We archive a 512px copy of each Color (albedo) map plus a
receipt: source URL, CC0 dedication, zip + image SHA-256, and the measured mean
albedo, which is what the Roblox build uses as part colour where a texture
upload would be required (a place file cannot carry uploaded PBR assets).

    python3 tools/fetch_scans.py
"""
import hashlib
import io
import json
import os
import subprocess
import zipfile

WANT = [
    ("PavingStones151", "square paving / cobbles",  "ground"),
    ("PavingStones141", "cobblestone paving",       "ground_alt"),
    ("Bricks075A",      "brick wall, course A",     "brick"),
    ("Bricks094",       "brick wall, course B",     "brick_alt"),
    ("Plaster007",      "lime plaster render",      "plaster"),
    ("Wood092",         "weathered timber boards",  "timber"),
    ("Planks039",       "plank flooring",           "floorboard"),
    ("Concrete048",     "concrete / kerb stone",    "concrete"),
    ("Gravel043",       "compacted gravel path",    "gravel"),
    ("Rock064",         "wall stone",               "stone"),
    ("Tiles138",        "clay floor tiles",         "tile"),
    ("Bark014",         "tree bark",                "bark"),
]
API = json.load(open('/tmp/acg.json'))
BY_ID = {a['assetId']: a for a in API['foundAssets']}
OUT = "assets/scans"
os.makedirs(OUT, exist_ok=True)
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"

import numpy as np
from PIL import Image

receipts = []
for aid, desc, role in WANT:
    meta = BY_ID.get(aid, {})
    url = f"https://ambientcg.com/get?file={aid}_1K-JPG.zip"
    tmp = f"/tmp/{aid}.zip"
    r = subprocess.run(["curl", "-sL", "-m", "300", "-A", UA, "-o", tmp, "-w", "%{http_code}", url],
                       capture_output=True, text=True)
    if r.stdout.strip() != "200":
        print(f"FAIL {aid}: http {r.stdout.strip()}")
        continue
    raw = open(tmp, "rb").read()
    z = zipfile.ZipFile(io.BytesIO(raw))
    color = [n for n in z.namelist() if "_Color" in n and n.lower().endswith(".jpg")]
    if not color:
        print(f"NO COLOR {aid}")
        continue
    img = Image.open(io.BytesIO(z.read(color[0]))).convert("RGB").resize((512, 512), Image.LANCZOS)
    fn = f"{aid}_albedo_512.jpg"
    img.save(os.path.join(OUT, fn), quality=88, optimize=True)
    arr = np.asarray(img, dtype=np.float32) / 255.0
    mean_lin = (arr ** 2.2).reshape(-1, 3).mean(axis=0)
    mean_srgb = np.power(mean_lin, 1 / 2.2)
    rgb = [int(round(c * 255)) for c in mean_srgb]
    data = open(os.path.join(OUT, fn), "rb").read()
    receipts.append({
        "asset_id": aid, "role": role, "description": desc,
        "source_url": f"https://ambientcg.com/view?id={aid}",
        "download_url": url,
        "license": "CC0 1.0 Universal (public domain dedication)",
        "license_url": "https://docs.ambientcg.com/license/",
        "creation_method": meta.get("creationMethod"),
        "creation_method_name": meta.get("creationMethodName"),
        "is_real_scan": meta.get("creationMethod") == "PBRPhotogrammetry",
        "archived_color_map": fn,
        "archived_bytes": len(data),
        "archived_sha256": hashlib.sha256(data).hexdigest(),
        "zip_bytes": len(raw),
        "zip_sha256": hashlib.sha256(raw).hexdigest(),
        "mean_albedo_srgb": rgb,
        "mean_albedo_hex": "#%02x%02x%02x" % tuple(rgb),
    })
    print(f"OK {aid:18} {role:12} {rgb}  scan={meta.get('creationMethod')}")

json.dump(receipts, open(os.path.join(OUT, "SCAN_RECEIPTS.json"), "w"), indent=2)
print(f"\n{len(receipts)}/{len(WANT)} archived -> {OUT}")
