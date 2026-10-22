# Handoff — Winterlichtplatz (Roblox town square)

**State:** the place file, the renders, the evidence and this deposit are complete as
of 2026-10-22. Nothing is half-built. Independent non-owner acceptance is PENDING.

## Where everything is

```
work/
  default.project.json        Rojo project (the place definition)
  tools/townspec.py           THE generator — all geometry, rooms, residents, palette
  tools/emit_place.py         spec -> src/Workspace/Town.rbxmx + TownData.luau
  tools/render.py             spec -> renders (numpy z-buffer rasteriser)
  tools/verify_place.py       built place vs spec, part by part (export parity)
  tools/validate.py           V01-V16 positive, --negative for N01-N17
  tools/fetch_scans.py        re-download the CC0 scans + receipts
  build/townspec.json         generated scene (the shared truth)
  build/TownSquare.rbxl       BINARY PLACE — this is the thing you open
  build/TownSquare.rbxlx      XML twin (parity-verified)
  src/**                      Luau scripts + the .rbxmx part soup
  tests/check_towndata.luau   loads the data module under plain Luau and asserts it
  renders/                    final PNGs + CONTACT_SHEET + MANIFEST
  evidence/                   VALIDATION, NEGATIVE_TESTS, export_parity, SHA256SUMS
```

## Reproduce from scratch

```bash
python3 tools/fetch_scans.py        # CC0 scans + receipts (network)
python3 tools/townspec.py           # geometry  -> build/townspec.json
python3 tools/emit_place.py         #            -> Town.rbxmx + TownData.luau
rojo build default.project.json -o build/TownSquare.rbxlx
rojo build default.project.json -o build/TownSquare.rbxl
python3 tools/verify_place.py       # parity gate: must say PASS
python3 tools/validate.py           # must say 16/16 PASS
python3 tools/validate.py --negative# must say 17/17 CAUGHT
luau tests/check_towndata.luau      # must say PASS
python3 tools/render.py             # 12 views (~3 min)
```

`tools/townspec.py` is deterministic (seed 20261022), which V13 checks by regenerating
and comparing hashes.

## The first thing a human should do

**Open `TownSquare.rbxl` in Roblox Studio and press Play.** It has never been opened:
there is no Studio in this sandbox, and the binary file is Rojo's serialisation of the
XML tree that parity-verified. If something is wrong, it will be in the places a
serialiser can differ from the XML view — script placement, `ProximityPrompt` behaviour,
or the `SpawnLocation` landing the character on the pad. Everything geometric is
covered by parity.

Two things to look at specifically:
1. Walk into any building through the front door (prompt: "Open door"), climb the
   stairs, and confirm you can stand on an upper floor. V05 proves a flight exists per
   floor transition; it cannot prove the steps are comfortable to a character controller.
2. Ask the Town Crier for the errands and finish one. The marker sits in a real upper
   room; the server validates you are within 9 m before crediting it.

## Known gaps, in order of what I would fix first

1. **Residents do not climb stairs.** They arrive at their building's door and are then
   placed in their room. A PathfindingService route or a scripted stair walk is the fix.
2. **No PBR textures in the place.** Surfaces are flat-coloured engine materials. Fix
   requires uploading the archived albedo maps as Roblox assets and rewiring materials.
3. **The square is emptier at night than it should be** — residents are teleported to
   beds, so the day crowd vanishes at dusk. A night shift (watch, lamp lighter, tavern)
   would fix it.
4. **No sound.** No ambience, no door creak, no fountain.
5. **The renders are a z-buffer approximation.** A Cycles or Studio screenshot pass
   would represent the actual engine far better.

## Rules this deposit followed, and one it broke knowingly

Followed: dated deposit directory, append-only `data/INDEX.md` and `PUSHES.md` rows,
hash-and-verify release assets, validators with negative proofs, no secrets in any
file, no self-review.

Broken knowingly: the repo's worker recipe names seven `chatcode` roster agents; this
session is an Arena.ai agent, not a crew member, so it holds **no lease and no board
card** and did not run the T1–T7 entry trials. The shift note says so in its first line
rather than borrowing an identity. Exact precedent: `shifts/2026-10-21-arena.md`.
