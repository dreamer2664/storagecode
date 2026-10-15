# Data index — one line per deposit

Append-only. Format: `date · project · agent · what · PR` (or `-` when there
is no PR). Newest at the bottom.

| date | project | agent | what | PR |
|---|---|---|---|---|
| 2026-10-14 | chatcode | vesta | pipeline build receipts — validate 0 errors after repair chain, first automatic formalcode lines, CI green on 2cea75af/f3750d64 | - |
| 2026-10-14 | superocr | vesta | main CI regression since #82 + fix — red log extract, verbatim diff, local 24/24; CI on 9ab638a1 noted in dir | - |
| 2026-10-14 | superocr | odysseus | S58 t-20261014-d325 replay receipts — live 100-item seed-1 hard pass (floor/final/route-pieces jsonl) + census json; tool+report on branch agent/odysseus/t-20261014-d325, gates G1-G5 PASS, 32/32 tests | - |
| 2026-10-14 | superocr | odysseus | S68 t-20261014-8ff6 easy-residue census receipts — live 100-item seed-1 easy pass (floor/final/route-pieces jsonl) + census json; 25 misses (13 case / 8 seg / 4 glyph), gates G1-G3 PASS | - |
| 2026-10-14 | superocr | scipio | S57 replay receipts (t-20261014-713e): seed-1 75/25 ×3 + seed-2 75/29 ×3 on canonical suites, per-item diff 0/1200 mismatches, validate_report ×6 VALID — summary + diffs; receipts in superocr PR #89 | superocr#89 |
| 2026-10-15 | superocr | odysseus | S65 t-20261014-138a darts fresh-corpus receipts — seed-900 40-item reads jsonl + census json (0/40 floor, 0/40 shipping, 40/40 segmentation stage; manifest sha256 3fc6ae4d) | - |
| 2026-10-15 | storage-migration | vesta | Legacy storage ledger, shifts, chronicle and data imported without loss; original data index: [legacy/storage/data/INDEX.md](../legacy/storage/data/INDEX.md); checksum map: migrations/2026-10-15-storage-unification.json | storage@c0e46a8204 |
| 2026-10-15 | youtube-training | vesta | yt-training-s1 launch: ten reserved final-film slots; 0 completed at launch; viewing index data/youtube-training/INDEX.md; production/review requirements in chatcode projects/youtube-training | - |
| 2026-10-15 | storage-migration | vesta | Server-side legacy archive frozen @aa18c8656b; late PUSHES rows reconciled; 3 unmerged maintenance PRs preserved with immutable source/patch hashes under legacy/storage-open-prs/ (not accepted) | - |
