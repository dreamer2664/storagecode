# wire/ — the durable archive of the formalcode wire

ntfy keeps messages for a limited time. This directory keeps them forever.

`wire/YYYY-MM-DD.jsonl` — one raw ntfy message object per line (`id`,
`time`, `topic`, `message`, `title`, …), UTC days, append-only.

- Written by `.github/workflows/wire-archive.yml` (runs every 30 minutes,
  pulls the last 48h, dedupes by ntfy message id). Never edited by hand.
- The live wire: <https://ntfy.sh/formalcode> (public topic).
- Downstream pushes to this repo that are the archive job itself are marked
  `[skip ci]` and are skipped by the recorder — the archive of the record is
  not itself an event.

To read a day as prose:

```bash
python3 - wire/2026-10-14.jsonl <<'PY'
import json, sys
for line in open(sys.argv[1], encoding="utf-8"):
    line = line.strip()
    if line:
        print(json.loads(line)["message"])
PY
```
