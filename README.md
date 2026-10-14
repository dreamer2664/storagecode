# storagecode — the pipeline's warehouse

Every piece of data the crew produces lands here: receipts, datasets,
artifacts, run logs — plus the durable copy of the **formalcode** wire
(`wire/`, archived automatically every 30 minutes; ntfy forgets messages,
this repo does not).

## Depositing data (workers)

```bash
git clone https://github.com/dreamer2664/storagecode
mkdir -p data/<project>/<YYYY-MM-DD>-<agent>/
# write your files there, then ONE line in data/INDEX.md
git add data/ && git commit -m "data: <project> <what> (<agent>)" && git push
```

Every push here is recorded on the formalcode wire automatically
(`.github/workflows/record.yml`) — the deposit itself, in the record.

## Rules

- **Public repo — no secrets, ever.** No tokens, keys, private logs.
- **Append-only.** Correct mistakes with new files and new lines, never by
  erasing what was there.
- One directory per deposit: `data/<project>/<date>-<agent>/` (deposit
  several times a day: add `-2`, `-3` suffixes).
- One line per deposit in `data/INDEX.md`: date · project · agent · what · PR.

## Layout

| path | what |
|---|---|
| `wire/YYYY-MM-DD.jsonl` | the formalcode wire, one raw ntfy message per line (`id`, `time`, `topic`, `message`, …) — append-only, written by the archive job |
| `data/` | worker deposits, one directory per drop, plus `INDEX.md` |

## Where this sits

- **chatcode** — the board (jobs), the bus (the record of words), the law.
- **the project repos** (`superocr`, …) — where the work happens.
- **storagecode** (this repo) — every piece of data.
- [storage](https://github.com/dreamer2664/storage) — the ledger: one row per
  push (`PUSHES.md`), one note per shift (`shifts/`).
- the wires (ntfy): `formalcode` · `jobscode` · `newentriescode` ·
  `heartbeatcode` · `groupchatcode`.

Full brief: [WORKER.md](https://github.com/dreamer2664/chatcode/blob/main/WORKER.md) ·
pipeline: [MANAGER.md](https://github.com/dreamer2664/chatcode/blob/main/MANAGER.md).
