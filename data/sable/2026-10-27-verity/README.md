# sable — chess eye audit (verity, 2026-10-27)

Audit and repair of `dreamer2664/sable`, the lichess bot that plays chess through
[pc-eye](https://github.com/dreamer2664/pc-eye). Written by **verity** for **caissa**,
who owns the project. The full note, including the revert instructions I actually ran,
is `HANDOFF-verity.md` on branch `agent/verity/chess-eye-audit`.

**Branch:** `agent/verity/chess-eye-audit` — 6 commits on top of caissa's `1c08a2a`.
`master` untouched, nothing force-pushed, nothing sealed.

## Evidence in this folder

| file | what it proves |
|---|---|
| `geometry_census.txt` | `find_board` over **all 282** recorded frames, by category, with the reason for every refusal |
| `replay_255_positions.json` | 255 replayed positions from the ten recorded games: 255/255 exact, 16320/16320 squares |
| `replay_stdout.txt` | the same run, per game |
| `make_test.txt` | `make test` → 45 tests, OK, exit 0 |
| `uci_test.txt` | `tools/uci_test.py` → 28/28 |
| `perft.txt` | `bash tests/perft.sh` → 26/26 (unchanged by me) |

## The numbers that matter

| | before | after |
|---|---|---|
| Board located, game frames | 143/238 (60%) | **247/247 (100%)** |
| Board location cost | ~145 ms/frame | ~38 ms, 0 ms cached |
| Reads checked before being believed | never | every read (kings, confidence, legality) |
| Own moves verified on screen | no | yes, one retry |
| Recogniser | 640/640 squares | 640/640 (unchanged) |
| Replayed positions | not measurable | **255/255 exact, 16320/16320 squares** |
| Engine per move | 578 ms | **201 ms** |
| Screenshot payload per move | 123 KB | **43 KB** (−65%) |
| `make test` | broken (EACCES, missing `pceye` module) | **45/45 in ~45 s, no PC needed** |

## The four flaws that were actually costing games

1. **The eye could not tell a good read from a bad one.** `lichess_bot.plausible()`
   existed and was never called; `play_game` adopted whatever came back. A half-drawn
   piece read as "a pawn" and stalled the game.
2. **Geometry failed 40% of the time.** Edge refinement demanded a pixel column be
   >97% board colour — impossible across a rank of pieces — and threw away a coarse box
   that was already correct.
3. **A modal made the board unfindable.** Lichess dims the whole page behind the
   promotion picker. The square colours drop to `(96,88,72)/(80,64,56)`, a dark UI panel
   outranks the board, and detection refused a board that was on screen. This is exactly
   where `g_L8_1` died: `own_move_verified g7h8` → `click_failed g7h8q`, one square from
   promoting.
4. **The harness could not start on a clean machine.** Every tool imported a `pceye`
   module from `../pceye` that the repo does not contain; `ladder.py` shelled out to
   `../../pceye/pceye.py`, also absent; every `.sh` shipped `100644` so `make test`
   died with EACCES.

Also found: `learn.py` pointed at a Stockfish (`../../bin/sf`) that never existed, so
the avoid-list silently stayed empty; and the opening book had no quality gate — it
wrote the opponent's moves and accepted any game that was not lost.

## What was added

`tools/boardvision.py` (geometry + recognition + gates, replacing three pasted copies),
`tools/pceye_client.py` (the missing client), `tools/replay_shots.py` (headless replay),
`tests/virtualscreen.py` (a virtual lichess board that answers pc-eye's HTTP calls, so
`play_game()` runs end to end with no PC), `tests/{stub_engine,test_loop,test_boardvision,
test_learn,test_pceye_contract}.py`, `Makefile`, `requirements.txt`.

## Honest limits

- **Nothing was run against lichess.** Every number comes from the 282 frames caissa
  already recorded, or from synthetic frames rendered from them.
- **The promotion picker path is the least-tested thing in the branch.** The virtual
  screen auto-queens instead of drawing a picker, so loop tests stay short of promotion.
  That is precisely where a real game died.
- **34 of the 282 frames are refused, correctly** — they are Game-setup screens with no
  board on screen. Checked by eye; see `geometry_census.txt`.
- `recogniser_accuracy.py` still drives a live analysis board; I fixed its imports and
  made `SCALE` overridable but could not run it. `replay_shots.py` is the offline
  replacement.
- **pc-eye was read and its suite run (32/32 headless) but NOT modified.**

## Revert

```bash
git revert --no-edit 1c08a2a..HEAD   # verified: the tree returns to exactly 1c08a2a
```

Tested in a scratch worktree; the diff against `1c08a2a` came back empty. Per-commit and
"keep the new modules, restore my drivers" options are in `HANDOFF-verity.md` §9.
