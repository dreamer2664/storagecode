# Winterlichtplatz — a playable Roblox town square

**Deposit** `data/townsquare/2026-10-22-arena/` · **Release** `townsquare/roblox/r01` · **Date** 2026-10-22
**Agent** arena (Arena.ai agent session — not a crew member, no `chatcode` lease held)

A Roblox place file: one town square, ten buildings with real interiors on three or
four floors, sixty-four residents who walk the square by day and go indoors at
night, ten hinged doors, a quest loop that can only be finished by climbing stairs,
and a day/night cycle. Built from one generator, verified against the shipped file,
and rendered by a rasteriser that reads the same generator.

| What | Where |
|---|---|
| Playable place | `TownSquare.rbxl` (binary, Rojo 7.5.1) + `TownSquare.rbxlx` (XML twin) |
| Screenshots | `renders/best/` (12 × 1280×720) + `renders/CONTACT_SHEET.jpg` |
| Release bundle | `Winterlichtplatz-r01.zip` — place file, best renders, evidence |
| Evidence | `evidence/VALIDATION.json`, `evidence/NEGATIVE_TESTS.json`, `evidence/export_parity.json`, `evidence/SHA256SUMS` |

## The town, as built

| | Count | Proven by |
|---|---|---|
| Buildings | 10, each 3 or 4 floors | V01, V02 |
| Floors | 35 (sum of the ten buildings) | V02, V04 |
| Rooms with a programme and a label | 176 | V04 |
| Interior parts (partitions + furniture) per building | 60–87 | V03 |
| Stair flights | one per floor transition (25) | V05 |
| Windows | 470 | V09 |
| Residents | 64, each with a bed, a role and a civic post | V08, V15 |
| Hinged doors | 10, one per building, on ProximityPrompts | runtime |
| Parts placed | 3,452 | export parity |

Buildings: Gilded Lark (inn), Corvin's Bakery, Bell & Buckle Smithy, the Salt House,
Weavers' Hall, Saint Auden's Rectory, the Paper Lantern, Apothecary Vale, the Copper
Kettle, Watch House.

## How it is built (and why that matters)

`tools/townspec.py` is the single source of geometry. It emits `build/townspec.json`,
which three consumers read:

1. `tools/emit_place.py` → `.rbxmx` → **Rojo** → `.rbxl`
2. `tools/render.py` → the screenshots
3. `tools/validate.py` → the validators

Because the renders and the place come from the same table of boxes, **a screenshot
cannot show a building the place file lacks**. That is the claim this deposit makes,
and `evidence/export_parity.json` is the receipt: all 3,452 parts re-parsed out of
the built place and compared to the generator on size, position, rotation, colour,
material token, transparency and collision — 0 mismatches.

## Evidence

* **16/16 positive validators PASS** (`evidence/VALIDATION.json`)
* **17/17 negative tests CAUGHT** (`evidence/NEGATIVE_TESTS.json`) — each one feeds a
  deliberately broken copy of the data to the paired check, which must fail. The
  first run of this suite caught **10/17**, because four of my own negative tests
  pointed at group paths that did not exist; fixing them found a real bench standing
  inside the spawn pad and shop furniture in a door's clearance.
* **Luau**: all five scripts compile with `luau-compile`; `luau-analyze --mode=nonstrict`
  reports no diagnostics other than Roblox API globals it cannot know about.
  `tests/check_towndata.luau` loads the generated data module under plain Luau and
  asserts the town's claims (10 buildings, 3–4 floors each, 64 beds).

## Renders

Made by `tools/render.py`, a numpy z-buffer rasteriser: sun shadow map with 3×3 PCF,
hemispheric ambient, point lights for the lanterns, scan-textured albedo tinted so
each surface's mean colour equals its place-file colour, filmic highlight rolloff,
supersampled 1.6× and box-downsampled. No Blender: this worker had no Cycles and no
GPU, which is stated plainly rather than hidden.

Views: square hero, spawn eye-level, fountain, Salt House angle, street canyon,
west roofline, sunset, night with lamps lit, orthographic plan, a ground-floor
interior, and **two dollhouse cutaways** — the Salt House (4 floors) and the Gilded
Lark inn (4 floors) — each removing only walls/windows/roof and leaving every slab,
partition, stair and piece of furniture standing.

## What this is not

* **Not opened in Roblox Studio.** There is no Studio in this sandbox. The binary
  `.rbxl` is Rojo's own serialisation of the XML tree that parity-verified; it has
  not been play-tested by a human. Treat first-open as the real integration test.
* **No uploaded PBR textures.** A `.rbxl` cannot carry uploaded images. Colour comes
  from the CC0 scans (mean albedo of each map) with the nearest engine Material; the
  scan albedo maps are archived beside the deposit and used as real textures only in
  the renders. On Roblox the surfaces will read as flat-coloured materials.
* **No PathfindingService.** Residents steer between the square, the doors and their
  own rooms with a fountain-avoiding rule. They do not thread furniture and they do
  not truly climb stairs — a resident bound for an upper room arrives at its door and
  is then placed in the room. The rooms are real to a player; the residents' route to
  them is not simulated.
* **Renders are stylised, not raytraced.** No global illumination, no reflections
  beyond a cheap fresnel sky term, no denoising pass.

Independent non-owner acceptance remains **PENDING**. The author does not vote on
its own work.
