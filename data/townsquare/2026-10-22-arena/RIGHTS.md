# Rights and provenance — Winterlichtplatz

## What ships here, and under what terms

| Item | Origin | Terms |
|---|---|---|
| `TownSquare.rbxl`, `.rbxlx`, `src/**` (Luau), `tools/**` | authored for this deposit | original work by this session; no third-party code copied |
| Rojo 7.5.1 (build tool, not redistributed) | github.com/rojo-rbx/rojo | MPL-2.0 — used as a binary, not linked or vendored |
| Roblox API enum dump (`assets/enums/Material.json`) | Roblox-Client-Tracker API-Dump | reference data; used to prove material tokens are valid, not redistributed as art |
| 12 photogrammetry scans (`assets/scans/*`) | ambientCG | **CC0 1.0 Universal** — public domain dedication |
| Roblox engine | Roblox Corporation | the place is a Roblox experience; Roblox's own terms govern play |

## The scans, itemised

All twelve are ambientCG materials whose `creationMethod` is `PBRPhotogrammetry` —
captured scans, not procedural textures. Each receipt records the asset id, source
URL, license, zip bytes, zip SHA-256, archived image bytes, archived image SHA-256 and
the measured mean albedo used to colour the place.

| asset | role | mean albedo |
|---|---|---|
| PavingStones151 | square paving | #7b7266 |
| PavingStones141 | cobblestone paving | #927a58 |
| Bricks075A | brick wall A | #8f8570 |
| Bricks094 | brick wall B | #8a7059 |
| Plaster007 | lime plaster render | #bfbeb7 |
| Wood092 | weathered timber | #b0733f |
| Planks039 | plank flooring | #bb9b6b |
| Concrete048 | concrete / kerb | #a29887 |
| Gravel043 | gravel path | #6d6e6a |
| Rock064 | wall stone | #78704d |
| Tiles138 | clay floor tiles | #373737 |
| Bark014 | tree bark | #7b6853 |

Retrieval URL pattern: `https://ambientcg.com/get?file=<ASSET>_1K-JPG.zip`.
License text: <https://docs.ambientcg.com/license/>.

**What is NOT here:** no uploaded Roblox assets, no marketplace models, no reused
screenshots, no third-party textures beyond the CC0 scans above. The renders are
produced from the deposit's own geometry by `tools/render.py`.

## Honest limits on the licence claim

The scans are CC0, so the derived albedo values and archived 512 px colour maps carry
no attribution requirement. This deposit still records them, because a future reader
needs to know where a colour came from. The town's layout, names and residents are
original and invented for this build; any resemblance to a real place is coincidental.
