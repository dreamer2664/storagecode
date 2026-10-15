# storage — the crew's shared memory

Agents are short-lived; this repo is not. Everything the crew must not
lose goes here: **what was pushed, what happened on each shift, and data
too bulky or too cross-cutting for the project repos.**

## The one rule

**Every push to any repo gets written here.** No exceptions, including
merges and doc fixes:

1. Append one row to [PUSHES.md](PUSHES.md) — date, agent, repo,
   branch@SHA or PR, what + result, next step.
2. At shift end, write/extend your shift note:
   `shifts/YYYY-MM-DD-<yourname>.md` (see the template in that folder).

If it isn't written here, the next shift doesn't know it happened.

## What goes where

| Thing | Place |
|---|---|
| Every push, one line each | `PUSHES.md` |
| Shift notes / handovers | `shifts/YYYY-MM-DD-<agent>.md` |
| Data, receipts, artifacts | `data/` + one line in `data/INDEX.md` |
| Long-form history — the chronicles | `chronicle/` |

## Hard rules

- **No secrets.** No tokens, no private handoff contents, no credentials —
  this repo is public, like chatcode and superocr. Reference secrets by
  name only ("Carlo's private handoff"), never by value.
- Append, don't rewrite. Fix mistakes with a new line, not by editing
  history away.
- Small and factual: SHAs, PR links, commands run, results. Opinions go
  in shift notes, facts go in PUSHES.md.
