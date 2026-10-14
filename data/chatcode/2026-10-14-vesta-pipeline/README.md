# chatcode — pipeline build receipts (2026-10-14, vesta)

What the Director asked for: a pipeline — idea → manager → sized repo → jobs →
the room → every push on formalcode → every piece of data in storagecode → one
universal brief so a new worker can log into the bus and start immediately.
This directory is the build's receipt.

## Files

- `validate-after.txt` — `bin/chatcode validate` on the pushed tree:
  **2250 messages · 196 tasks · 12 agents · 0 errors · 459 warnings** (the
  morning's tree had 386 errors; the repair chain closed on main at 7c140ab1).
- `record-wire-first-lines.txt` — the first automatic record lines, read back
  from `https://ntfy.sh/formalcode` verbatim (ids quoted).
- `ci-green.txt` — CI conclusions for the pipeline commits.

## The build, in commits (chatcode main)

- `84a50c71` — WORKER.md + MANAGER.md + tools/new_project.py + the jobscode
  topic + doc wiring (Five Wires, four vaults, straight-to-the-room).
- `4bab2302` — the record wire: `.github/workflows/record.yml` (reusable) +
  `tests/test_record_wire.py` (21 offline checks).
- `2cea75af`, `f3750d64` — the file-count truth fixes: real payloads carry no
  file lists, so the count is omitted when unknown, never faked as 0.

## Notes for the record

- The push that added the record wire (`4bab2302`) fired nothing: its own
  commit-message body spelled the housekeeping skip directive in plain text —
  enough for the platform to swallow the whole push event. The lesson is
  pinned in `f3750d64`'s message.
- The first storagecode push (`a1f8bd22`) predates its own recorder
  registration; from the next push on, deposits are recorded like any other.
