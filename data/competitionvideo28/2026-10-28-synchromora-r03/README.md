# synchromora r03 — corrected partial Shorts delivery

**2026-10-28 · 15/18 clips · still blocked on source 1**

- Canonical organized release: <https://github.com/dreamer2664/competitionvideo28/releases/tag/synchromora-clips-20261028-r03> (prerelease).
- Redundant media archive: <https://github.com/dreamer2664/storagecode/releases/tag/competitionvideo28-synchromora-r03-backup> (two ZIPs, prerelease).
- Production project: <https://github.com/dreamer2664/competitionvideo28/tree/main/synchromora> at `c946e5a` for this receipt. The earlier r02 release remains intact but is labeled superseded.
- `RELEASE.json` records exact live URLs, IDs, byte counts and hashes for all 17 release assets and both mirrors. `PLAN.json` records source cuts; `QC.{md,json}` gives the 15 individual durations, measurements and checksums. `CAPTION_REVIEW.md` explains the revision.

| Asset | Bytes | SHA-256 |
|---|---:|---|
| `00_ALL_AVAILABLE_CLIPS_AND_SRT_r03.zip` | 67,066,102 | `b60bf46939adbd573581882bc017fe8bab3cc12079a0ff6f77f98a2b4c81bc64` |
| `99_REBUILD_KIT_PARTIAL_r03.zip` | 73,197,014 | `59b207855bb000a4156b4abc0109c28586291b81b1c9d955adbdc6b79fb59865` |

**Revision:** an SRT spot-check of r02 found that the standalone Jokers cannonball clip dropped `A` before `CANNONBALL`, owing to an equal-timestamp substring deduplication bug. The code and source token order were corrected, with three regression tests; the affected MP4 and SRT were rerendered. We initially thought the ranking was affected too, but its source range begins later. Its rerender and 13 other MP4s are byte-identical to r02. The corrected burn-in was visually spot-checked.

The delivery ZIP contains 15 MP4s and 15 SRTs, source/cut index, QC, and checksums; its 39 internal SHA-256 records and both ZIP CRCs passed. All 17 canonical assets were downloaded and hash-verified; both archive ZIPs were independently downloaded and hash-verified. All 15 videos fully decoded and passed SRT timing, 720×1280 format, loudness and true-peak checks. A recovery-map rerender of the corrected clip matched six sampled frames and its SRT; audio is lossy, not bit-identical.

**Blocker:** `FDRUMXwb4mg` requires age-verified access; its two normal Shorts and one ranking have not been made. An authorized copy of that exact video is needed; no substitute was used. Captions are machine-generated, not checked by a person listening, and third-party footage/music rights have not been verified. Correct captions and secure rights before posting.

The `theagency` correction was sent and verified as `zv1RGQRf8frH`. User-facing progress and all missing work are explicit; 15/18 is not a full delivery.
