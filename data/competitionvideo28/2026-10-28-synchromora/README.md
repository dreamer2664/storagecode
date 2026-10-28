# synchromora — six-source clipping commission, partial handoff

**2026-10-28 · 15/18 delivered · 3 blocked**

- Canonical, organized user-facing release: <https://github.com/dreamer2664/competitionvideo28/releases/tag/synchromora-clips-20261028-r02> (prerelease).
- Redundant media archive: <https://github.com/dreamer2664/storagecode/releases/tag/competitionvideo28-synchromora-r02-backup> (two ZIPs, prerelease).
- Production code, editable caption data, notes and visual samples: <https://github.com/dreamer2664/competitionvideo28/tree/main/synchromora> (checkpoint `72923a0`).
- `RELEASE.json` records exact URLs, asset IDs, byte counts, SHA-256, and mirror bindings. `QC.{json,md}` records every clip's duration, measured loudness, hashes and mechanical QA. `PLAN.json` records each source interval and rank; `SOURCES.json` credits the supplied uploaders.

| Archive asset | Bytes | SHA-256 |
|---|---:|---|
| `00_ALL_AVAILABLE_CLIPS_AND_SRT_r02.zip` | 67,061,280 | `7c0c6a35a5e6b3855a170e11dd4ee5a862797c7174c5971d0c71140e83be2d42` |
| `99_REBUILD_KIT_PARTIAL_r02.zip` | 73,145,320 | `b6339d2f18e4c65260ab758ca72ffda443bdf4c4614370ec1966f6566b136b72` |

The first ZIP has **15 vertical H.264/AAC MP4s, 15 SRTs**, a missing-source notice, source/cut index and checksums. The separate recovery ZIP contains the used source windows and project data. The 15 individual MP4s and both ZIPs were actually downloaded from the competition release and matched SHA-256; both ZIPs were downloaded and matched again from the storagecode mirror. The delivery ZIP's 39 internal checksum records and both ZIP CRCs passed. All 15 MP4s fully decoded; final post-encode loudness is −16.90 to −15.27 LUFS, highest measured true peak −1.89 dBTP. Representative screenshots were visually inspected, not an end-to-end human watch.

**Blocker:** source `FDRUMXwb4mg` is age-restricted; its two normal Shorts and one ranking have not been made. An authorized file of that exact source is needed; no replacement was substituted. Captions are machine-generated and have not been verified by a person listening. Third-party footage and embedded music rights are not verified; attribution does not grant permission. Correct captions and secure rights before public posting.

**Recovery:** download/extract the rebuild ZIP, install FFmpeg, Python 3 and NumPy, then from its `synchromora/` directory run `python3 src/render_clips.py --recovery-map ../inputs/input-map.json --output-dir work/unmastered` followed by `python3 src/master_audio.py --input-dir work/unmastered --output-dir work/deliverables`. A recovery-based sample passed rendering; sampled frames matched, but lossy audio need not be byte-identical. The missing source is not included.
