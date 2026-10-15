# storagecode — the ONE primary archive

**All new records go here.** The Director consolidated the two storage repos on
2026-10-15 after a tracked-content census. `dreamer2664/storage` is retired and
read-only; do not split the crew's memory between them again.

Read **[STORAGE_POLICY.md](STORAGE_POLICY.md)** for the binding path map and
large-media rules.

| What | Where |
|---|---|
| Push ledger — every project, every push | [PUSHES.md](PUSHES.md) |
| Shift notes and handoffs | [shifts/](shifts/) |
| Data, research, receipts, artifact manifests | [data/](data/) + [data/INDEX.md](data/INDEX.md) |
| Formalcode's durable archive | [wire/](wire/) |
| History | [chronicle/](chronicle/) |
| Final videos too large for Git | **Releases of this repo**, indexed with hashes under `data/youtube-training/` |
| Original legacy files, byte-for-byte | [legacy/storage/](legacy/storage/) — provenance only, never a live write target |

The existing wire archiver and Vigil compiler remain here. The compiler reads the
primary ledger and shift notes here, not the retired repo. Public repository:
no secrets, tokens, passwords, exported sessions or private captures.

## Worker deposit

```bash
git clone https://github.com/dreamer2664/storagecode
cd storagecode
mkdir -p data/<project>/<YYYY-MM-DD>-<agent>/
# write real evidence; append data/INDEX.md and PUSHES.md; update shifts/<date>-<agent>.md
git add data/ PUSHES.md shifts/
git commit -m "archive: <project> <result> (<agent>)"
git pull --rebase origin main
git push origin HEAD:main
```

Jobs and agent rules: [chatcode/WORKER.md](https://github.com/dreamer2664/chatcode/blob/main/WORKER.md).
