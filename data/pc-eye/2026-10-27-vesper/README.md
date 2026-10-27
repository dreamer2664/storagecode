# pc-eye 1.0.3 — audit + hardening evidence (vesper, 2026-10-27)

Verbatim copies of the artefacts produced by job `t-20261027-pceye-hardening`, so the record survives a
force-push, a shallow clone or a repo rewrite. Nothing here is a summary of the code: `server.py`,
`launcher.py` and the 77-test suite are included so a reviewer can diff the claim against the bytes.

* Repo: `dreamer2664/pc-eye`, `main == origin/main == 2bdf366` at copy time (`git rev-parse` verified).
* Findings: **38** (F1–F38) in `AUDIT.md`; 31 fixed in code, 7 reported with a recommendation.
* Gate: `python3 tools/check_docs.py && python3 tests/run_all.py --all` → 4/4 green, 77 tests, on
  python 3.13 headless Linux. `evidence/` scripts self-skip when the 1.0.2 baseline is absent (CI).
* Measured: encode −25.4 % time / +5.7 % bytes at equal content; `/shot?max=0` −21 % at identical policy;
  `/state` 1 → **0** pixel captures; a look+check cycle 2 → **1**. `evidence/CAPTURE_COUNT.txt`.
* Negative control: **38 new tests run against the pre-fix tree, 35 red** — the suite is not decoration.
* Fuzz soak: **200,000 generated requests / 5 seeds / 0 tracebacks / 0 unrecovered disconnects**.
* NOT proven here, on purpose: that a click lands on the right pixel, black UAC windows, tunnel behaviour on
  a real router, 304 through cloudflared. Those need the Director's machine; the `windows-latest` CI leg is
  the substitute for the OS seams, not for the outcome.

## SHA-256 receipts (first 16 hex)

| file | bytes | sha256 | verify |
|---|---|---|---|
| `AUDIT.md` | 34,343 | `9ce38cd2a0d3ebb3…` | — |
| `CHANGELOG.md` | 8,316 | `1b00130ca0588139…` | — |
| `SHIP_GATE.md` | 1,801 | `86060367bffe7e43…` | — |
| `tests/run_all.py` | 4,341 | `279de1241a10aa3f…` | — |
| `tools/check_docs.py` | 3,209 | `baca25471ed794fe…` | — |
| `evidence/bench.py` | 10,361 | `3076317b792b0d26…` | — |
| `evidence/capture_count.py` | 5,299 | `eba52cb63dca716c…` | — |
| `evidence/negative_check.py` | 4,208 | `a17b6dd22914f8d8…` | — |
| `evidence/fuzz_protocol.py` | 10,756 | `ff56d6ef72370264…` | — |
| `evidence/oldtree.py` | 1,412 | `35fb75fd6ccc5716…` | — |
| `evidence/BENCH_BEFORE.json` | 2,687 | `3c571e131ce4747e…` | — |
| `evidence/BENCH_AFTER.json` | 2,691 | `f6f54a102c1ce631…` | — |
| `evidence/BENCH_COMPARE.json` | 6,409 | `2fa5b33a508349cd…` | — |
| `evidence/CAPTURE_COUNT.txt` | 2,001 | `919c44390beb7a42…` | — |
| `evidence/NEGATIVE_CONTROL.txt` | 1,847 | `712fe7d1ff2c9a27…` | — |
| `evidence/P3-TESTLOG.txt` | 115 | `69416f9e050e20d9…` | — |
| `evidence/FUZZ.txt` | 1,549 | `221e3018c4d81067…` | — |
| `server.py` | 70,757 | `c1eabbd9c628e280…` | — |
| `launcher.py` | 11,662 | `01eb098e9d931e57…` | — |
| `tests/test_pc_eye.py` | 61,523 | `9c12abae96e08260…` | — |
