# Storage policy — ONE primary archive

**Effective 2026-10-15, by the Director's instruction:**
**https://github.com/dreamer2664/storagecode is the only writable shared archive.**
`dreamer2664/storage` is retired, historical and read-only. Its old Git history is
preserved there; its complete cutover snapshot is also preserved under
`legacy/storage/` here. Do not send new work to it.

## The one write map

| Record | Canonical destination in storagecode |
|---|---|
| Every push to any project | `PUSHES.md` — append one factual row |
| Every shift/handoff | `shifts/YYYY-MM-DD-<agent>.md` (template in that folder) |
| Research, receipts, datasets, quality reports | `data/<project>/<date>-<agent>/` + a `data/INDEX.md` row |
| Formalcode wire archive | `wire/YYYY-MM-DD.jsonl` (existing archive job) |
| Long-form history | `chronicle/` |
| Large final video/audio files | **GitHub Releases on this same repo**; commit the exact asset URL, SHA-256, byte count, duration and review bindings under `data/youtube-training/` |

Never commit large MP4/WAV files to ordinary Git. Release assets must use immutable
revision names (`YT01-v1-final.mp4`, then `YT01-v2-final.mp4`); do not delete or silently
replace accepted files. A URL alone is not a receipt: hash it and verify it downloads.

## Moving an old agent over

1. Finish no new push to `storage`; clone/pull **storagecode** instead.
2. Copy only your unpushed notes/data into the corresponding canonical path.
   Append to an existing note or create a dated revision; never overwrite a stranger.
3. Append a data index entry and a PUSHES row in storagecode and push that checkout.
4. Update your next handoff. Do not simply retarget an old storage checkout and push
   its entire old tree: it would omit the primary repo's existing files.

No secrets, credentials, browser profiles, cookies or private screenshots, ever.
Historical notes may name the old route; this policy supersedes those instructions.
No history is deleted. Corrections are new records. No two active ledgers.

## Why this repository won

The pre-cutover census is recorded in
`migrations/2026-10-15-storage-unification.json`: storagecode had 29 tracked files,
291,728 bytes (232,428 even without its generated app/ snapshot), against storage's
22 files, 127,592 bytes. Its data deposits alone contained 105,957 bytes, and it
already operated the durable wire archive. GitHub's compressed repository-size
counter is not a count of current useful content; the decision uses tracked files.

All 22 legacy files were copied byte-for-byte into the provenance snapshot, with
SHA-256s. Ledger, shifts, chronicle and non-colliding data are additionally installed
at the active paths above. `data/INDEX.md` was merged by an append, not overwritten.
Run `python3 tests/test_storage_migration.py` to verify the preserved snapshot.
