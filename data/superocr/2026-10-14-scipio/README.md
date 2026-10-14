# S57 replay deposit — t-20261014-713e (scipio, 2026-10-14)

Independent 3× replay of the S55 bench movement on a second machine.

- `replay-summary.json` — counts, hashes, machine spec, verdict (all_runs_identical: true)
- `diff-seed1.json` / `diff-seed2.json` — per-item (id, got) diffs vs the committed
  receipts `superocr:reports/s55-bench-seed{1,2}-3x/`: 1200 items compared, 0 mismatches

The six bench receipts themselves live in superocr (canonical location, PR #89):
`reports/replay-s55/2026-10-14/{seed1-3x,seed2-3x}/`. Numbers: seed-1 75/25 ×3,
seed-2 75/29 ×3; suites canonical (full-sha match vs tools/s38_compare.HASHES);
all receipts pass validate_report.py. Bars 98/95 untouched — every run FAIL vs
the wall, as in every reader_lex receipt.

PR: https://github.com/dreamer2664/superocr/pull/89
