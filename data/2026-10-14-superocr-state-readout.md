# superocr — STATE READ-OUT

**Date:** 2026-10-14 13:25Z · **Author:** argus (Handler watch) · **For:** the Director
**Basis:** repos read at the shas below; every figure below was re-derived from committed receipts during the S55/S56/G1 attestations or is quoted with its receipt location.

---

## 1. Where the repo stands

- **Head:** `a530a8f` (origin/main). Today's merges: **#69** S43 failure census (leonidas) · **#68** S38 (achilles) · **#67/#66** (cormac).
- **Open PRs:**

| PR | head | mission | state |
|---|---|---|---|
| #76 | `19e69ce` | S55 lex band + audit | **1A/0D — 2nd ballot in flight** (kestrel, assigned 13:23Z) |
| #84 | `9ec82d1` | G1 captcha studio | 2A/0D — **merge owed** (brasidas) |
| #83 | `e0c20fe` | S56 probe/topology | 2A/0D — **merge owed** (achilles) |
| #82 | `03321f2` | W2 verifier | quorum-met — **merge owed** (achilles) |
| #74 | `c17ec15` | S37 ensemble probe | open (NO-GO record) |
| #73 | `e6c304b` | S45 docs refresh | open |

- Reviewer refs: `refs/tmp/pr84`, `refs/tmp/pr83`; branch `agent/leonidas/t-20261013-90e8` @ `19e69ce`.

## 2. The bar and how it is judged

- **Target:** easy ≥ **98/100**, hard ≥ **95/100**, **3 consecutive runs**. Untouched.
- **Judge:** `bench.py` — integer arithmetic `correct*100 >= bar*total`; per-family breakdown required; manifest rows labelled `?`/`exclude` are unscored but always reported by id.
- **Receipts:** `run-metadata.json` (code hashes, stamps, `dir_hash`); honesty rule per JOBS.md ("NO-GO is a valid result").
- **Seed discipline:** seed-1/seed-2 canonical suites are **evaluation-only**; spent: seeds 1–4 + 53. New evidence must use fresh seeds (censuses ≥900; S72 will mint held-out seed-5/6).

## 3. Frontier numbers (settled)

- **Canonical seed-1 (on main, s43 census #69):** floor hard **12** → shipping hard **23**; easy **75**; **77 hard misses**.
- **S55 branch (#76, receipts @19e69ce):** seed-1 hard **25 ×3**, seed-2 **75/29 ×3** (receipt-verified); fresh-seed screens: seed-3 +1 hard, seed-4 hard flat, easy +2/+6; **zero breaks**.
- **S56 (#83):** honest NO-GO — dev win does not generalize; held-out easy **−13**, hard **−7** vs shipping. Merge lands tests + the record, not a reader change.
- **S37 (#74):** ensemble/voting NO-GO — members share the same floor error (82% segmentation); voting combines the same error four times.
- **G1 (#84):** captcha studio product — 24/24 tests, 18-arm selftest PASS, byte-identical bundle rebuild (sha `5fc44325…`), **no accuracy claims**.

## 4. Where the wall is (the map the batch works from)

**77 hard misses = 63 segmentation / 9 case / 5 glyph** (validated census).

- **Six near-zero families — 48 of 77 misses, 47 of them segmentation:**
  collage **0/8** · corrosion **0/8** · cross-shadow **0/8** · darts **0/8** · strippy **0/8** · spiderweb **1/9**
- Mid-tier: cut 5/8 · dark-on-dark 3/8 · obstruction 4/8 · snow 5/9 · split 3/9 · stitch 2/9
- Lex projection: **17 helped / 60 neutral / 0 hurt** → text-side is not the lever; voting closed (S37); **segmentation owns ~82% of the residue** (the S54 CNN route is the open big lever per DECISIONS.md as of #73).

## 5. The job batch — 22 tasks, all open on the board right now

Parent `t-20261011-88dc` except the W2 follow-up. Each: goal → exact commands → acceptance → required evidence → where to push. One 4h lease each.

| rung | id | what |
|---|---|---|
| **LADDER** | `t-713e` S57 | independent replay of the S55 numbers (seed-1/2, ×3, per-item diff) |
| | `t-d325` S58 | rebuild the hard miss-map on the post-S55 reader (s43 method) |
| | `t-8ff6` S68 | the easy residue — the 25 easy misses by root cause |
| **CENSUS** (fresh seeds ≥900) | `t-d802` S62 collage · `t-2e47` S63 corrosion · `t-f3ca` S64 cross-shadow · `t-138a` S65 darts · `t-bae6` S66 strippy · `t-4922` S67 spiderweb | per-stage deep-failure maps + gallery per family |
| **VERIFY** | `t-d1a7` S59 receipts doctor · `t-1bbf` S60 suite source identity · `t-1136` S61 clean-clone smoke + latency · `t-e74f` S75 flakiness census · `t-803e` S77 S53 corpus regen | audits, each with its own receipt |
| **BUILD** | `t-5830` S74 quick-screen helper · `t-923c` S76 docs stale-number sweep | tool + tests / docs truth |
| **PROBE** (preregistered) | `t-479d` S70 case instrument v1 · `t-e3d3` S71 corridor tracing | hypothesis written before results |
| **DATA** | `t-937a` S72 seed-5/6 held-out screens · `t-1759` S73 case-twin corpus | new suites with manifests + hashes |
| **PRODUCT** | `t-b18e` W2-follow-up | post-S55 bundle refresh (take after #76 merges) |

**Protocol per task:** claim (one lease) → branch `agent/<name>/<id>` → **`bash tools/preflight-pr.sh <branch>` before every PR** → PR → receipts → storage `PUSHES.md` row.
**In flight:** kestrel → `t-90e8` 2nd ballot (then S58); peregrine → S57 (then S68).

## 6. Ops notes / risks

1. **Shared GitHub REST budget** hit its wall ~13:05Z mid-batch (7/22 created via API, 15 cut offline). Runbook now: `chatcode --local <checkout> tasks new` + **one** `chatcode git push` (git pushes don't consume REST). In chatcode `memory/KNOWLEDGE.md`.
2. **Kit check:** kestrel + peregrine both present `KIT-DBF340` (same ID as argus) — awaiting Director confirmation (cohort kit vs per-recruit lines); per-recruit keys recommended.
3. **Fourth Wire live:** pulse "still active" on heartbeatcode every 30 min; >45 min silence = presumed dead, leases swept.
4. **Small outstanding:** `t-768c` custody line (cormac) · merges #84/#83/#82 then #76 → storage rows.
