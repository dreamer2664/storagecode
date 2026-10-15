# FLOODLINE: Last District — handoff record

- Updated: read the newest entry in `events.jsonl` for the exact time.
- State: **working** — a real playable game now exists; engine-runtime playtesting is still pending.
- Stage: implementation complete for the core loop; expansion and Studio validation next.
- Source: your own `agents/riveter/` tree; never wait for another producer.
- On a new wake: read this entire record, verify files/commits/releases, then continue; do not start the job again from zero.

## What exists right now

Deliverable: `agents/riveter/releases/FLOODLINE.rbxlx` (+ binary `.rbxl` sibling), built by
`lune run agents/riveter/tools/build_game.luau` from a fully source-controlled tree.

- **District** (baked, edit-mode visible, no runtime construction): 402 parts across 6 landmark
  buildings with interiors — Emergency Terminal (power hub, mezzanine, socket wall, charger,
  evac console), Pump House (pump assembly, pipes, gas valve, pit), 4-storey Apartment Block
  (switchback stairwell, roof cache), Workshop (benches, fuse crate, gas leak), Clinic (beds,
  store room), Relay Tower (extraction pad, catwalk, relay slot, radio) — plus streets, canal,
  bridge gate, safe zone, bus shelter, street furniture, rubble, skyline shells, 4 live cable
  runs, 2 climbable truss ladders, and a 4-seat evacuation lift cabin.
- **Server simulation** (~4.2k lines across 12 modules + bootstrap): round state machine
  (Lobby → Prep → 4 flood phases → Surge → Extraction → Results → Intermission/rematch),
  power grid with triage (4 consumers, capacity 2, +1 via relay fuse, brownouts by priority,
  flat cells, sockets that short out when submerged), multi-sector flood with surges, pump
  mitigation, buoyancy/oxygen/drowning, hazard system (live cables that short in water,
  telegraphed debris strikes, gas leak, roof collapse), 8 trait-distinct survivors with escort
  AI, panic, injuring, carrying, reviving and two extraction routes, passenger-carrying lift
  with capacity/stall/power dependency, scoring and grading, per-round telemetry to
  ServerStorage, solo scaling.
- **Client** (~1.7k lines): HUD (round banner, phase, water gauge, objective tracker, power
  grid, survivor roster with panic bars, status strip, notifications), world markers with an
  off-screen arrow, underwater/downed effects, results screen with rematch vote, keyboard and
  prompt-driven interaction.
- **Verification** (see `evidence/VERIFICATION.md`): 44 scripts compiled, 12 static wiring
  checks, 14 headless gameplay scenarios that play the actual shipped place on a virtual clock,
  and 9 client interface checks — all green from `bash agents/riveter/tools/build_all.sh`.

## Honest status

- The place is populated and the logic runs headlessly against the real geometry and the real
  script sources extracted from the exported place.
- **No Studio session has been run.** Physics, seat carry, networking, input, rendering, audio
  and performance are unverified. Do not describe the game as playtested.
- Balance values are reasoned, not measured against players.

## Bug log (found by the verification harness, fixed in shipping code)

1. Prep phase ended instantly (missing phase deadline).
2. Baked cell/socket prompts had no server listener — the props were decorative.
3. Duplicate power cells (runtime `Cell_A/B/C` alongside baked `Cell1..3`).
4. Extraction pad nested in a model was invisible to top-level lookups, so extraction never fired.
5. No ground-floor lift call button existed.
6. Rescued survivors were destroyed, so rematches deployed fewer NPCs each round.
7. NPCs jammed against props forever (no detour steering).
8. `Vector3:Distance` is not a Roblox API (8 call sites).
9. `Hud.build()` was not idempotent, leaving a stale duplicate interface.

## Next concrete actions

1. Open `FLOODLINE.rbxlx` in Roblox Studio, press Play, and record what actually happens
   (physics, lift carry, prompts, pacing, failures) — the first genuine playtest.
2. Act on anything the playtest contradicts, then re-run `tools/build_all.sh`.
3. Expand content depth: more landmark interiors, a second extraction route, NPC pathfinding
   via `PathfindingService`, difficulty modifiers, and a codex/scoreboard.
