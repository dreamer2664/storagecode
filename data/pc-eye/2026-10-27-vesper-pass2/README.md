# pc-eye 1.0.3 — pass 2 evidence (vesper, 2026-10-27)

The increment on `2026-10-27-vesper/` (pass 1, `2bdf366`): the fuzzing record, the windows-latest leg, and
the process fixes. Copies are byte-for-byte from `pc-eye@b2c2a13`; `sha256sum -c SHA256SUMS` verifies them.
Pass-1 files that did not change (the launcher, the benches, `PC-EYE.md`) are NOT repeated here — they are
already in the sibling directory, and duplicating them would create two copies that can disagree.

* Repo at copy time: `dreamer2664/pc-eye`, `main == origin/main == b2c2a13` (`git rev-parse` verified, not
  inferred from a push line).
* Findings in this increment: **F27–F42** (16 ids), all in `AUDIT.md`. The audit as a whole carries **42**
  distinct finding ids — that number is computed here by `grep -o 'F[0-9]\+' | sort -u | wc -l`, not
  asserted, because a count written into a README is the first thing to go stale (pc-eye F16, agency F27).
* Final CI state: **4/4 green** on `b2c2a13` — `test (ubuntu-latest, 3.10/3.13)` and
  `test (windows-latest, 3.10/3.13)`, read from the run log, not from the badge: the Windows log says
  `PASS  -m unittest discover -s tests -v (11.1s)`, `PASS tools\check_docs.py`,
  `PASS evidence\capture_count.py`, `PASS evidence\negative_check.py`. The Windows leg had been red since
  I added it; three of its four reds were my tests being wrong about Windows, one was a real socket leak.
* Fuzz soak in this copy of `evidence/FUZZ.txt`: 200,000 requests / 5 seeds / 0 tracebacks / 0 hard
  failures, regenerated AFTER F41 with a widened oracle (the previous one could not see bare
  `TypeError`/`NameError`, which is how 33 tracebacks went unreported).
* `tools/git-hooks/pre-commit` + `tools/install_hooks.sh`: the "never commit on main" rule as a machine check,
  because I wrote the rule down and broke it twice the same day (F39/F40). Included so the hook text itself is
  on record — it is the only artefact here whose failure mode is silent.
* Disclosure that belongs in an archive, not only in a chat message: I committed directly to `main` twice and
  undid both with `push --force-with-lease` on my own branch tip. No one else's history was touched. The
  evidence for that claim is the reflog-style record in `AUDIT.md` F39/F40 plus the branch/merge topology:
  every merge into main is a `--no-ff` merge of an `agent/vesper/*` branch.
