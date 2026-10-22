#!/usr/bin/env python3
"""publish_renders.py — best-of set, contact sheet, manifest and checksums."""
import glob, hashlib, json, os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "renders")
BEST = os.path.join(SRC, "best")
os.makedirs(BEST, exist_ok=True)

TITLES = {
    "01_square_hero": "the square from the south, 64 residents at their posts",
    "02_spawn_eye_level": "spawn eye-level, looking north across the cobbles",
    "03_fountain_low": "fountain and market stalls from knee height",
    "04_salt_house_angle": "the Salt House (B04) from the south-east",
    "05_street_canyon": "street canyon between the Paper Lantern and Watch House",
    "06_roofline_west": "roofline from the west, gables and chimneys",
    "07_sunset_long": "the square at sunset",
    "08_night_square": "night, lamps lit, residents indoors",
    "09_plan_ortho": "orthographic plan: square, ring street, ten buildings",
    "10_interior_shop": "ground-floor interior, Salt House",
    "11_interior_upper": "upper-floor interior, the Gilded Lark",
    "12_cutaway_b04": "dollhouse cutaway, the Salt House: every floor, stair and room",
}

files = sorted(f for f in glob.glob(os.path.join(SRC, "*.png")))
manifest = {"views": [], "generator": "tools/render.py",
            "note": "Rendered by the deposit's own numpy rasteriser from build/townspec.json, "
                    "the same table the place file is compiled from."}
thumbs = []
for f in files:
    name = os.path.splitext(os.path.basename(f))[0]
    im = Image.open(f).convert("RGB")
    out = os.path.join(BEST, name + ".jpg")
    im.save(out, quality=90, optimize=True, progressive=True)
    data = open(out, "rb").read()
    manifest["views"].append({
        "view": name, "title": TITLES.get(name, name), "file": os.path.basename(out),
        "width": im.size[0], "height": im.size[1], "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    })
    thumbs.append(im.resize((480, 270), Image.LANCZOS))

cols, rows = 3, (len(thumbs) + 2) // 3
sheet = Image.new("RGB", (480 * cols, 270 * rows), (10, 11, 13))
for i, t in enumerate(thumbs):
    sheet.paste(t, ((i % cols) * 480, (i // cols) * 270))
sheet_path = os.path.join(SRC, "CONTACT_SHEET.jpg")
sheet.save(sheet_path, quality=88, optimize=True)
manifest["contact_sheet"] = {"file": "CONTACT_SHEET.jpg",
                             "sha256": hashlib.sha256(open(sheet_path, "rb").read()).hexdigest(),
                             "bytes": os.path.getsize(sheet_path)}
json.dump(manifest, open(os.path.join(SRC, "MANIFEST.json"), "w"), indent=2)
print(f"{len(manifest['views'])} views -> {BEST}")
print(f"contact sheet {sheet.size[0]}x{sheet.size[1]}")
