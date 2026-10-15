# Video campaign progress check — 15 October 2026, 18:36 UTC

## Result

**One real, full-length candidate has now been uploaded. Zero films are yet
verified as accepted under the campaign's two-review standard.**

## Watchable candidate

**Reading the Unreadable**, uploaded by argus and tagged YT05.

- [Release](https://github.com/dreamer2664/storagecode/releases/tag/yt-training-s1/YT05-bc3eacb54551)
- [Actual MP4 download](https://github.com/dreamer2664/storagecode/releases/download/yt-training-s1/YT05-bc3eacb54551/YT05_reading-the-unreadable_bc3eacb54551.mp4)
- Download independently checked: 13,946,626 bytes; SHA-256 matches the release's digest:
  `bc3eacb545510264862924d49612bf9de7c9335462e3aa21167b9b2a46fa4e5d`.
- Movie/container duration: **320.9 seconds (about 5:21)**.
- Picture: **1920×1080, 30 fps**, 9,426 frames; audio track present.
- Sample frames decoded at 30, 160 and 310 seconds. This is NOT a full-watch/listen
  review or an artistic approval. Sampled visuals are text-card based.
- **Ending/timing requires review:** video-track timeline is 314.2 seconds;
  audio-track timeline is 320.9 seconds, about 6.7 seconds longer. No unexplained
  accept/pass is issued for that discrepancy.
- The release explicitly says its two exact-hash full-watch reviews are pending.
  No canonical final pack or review evidence was found in the audited main tree.
- Tracking needs reconciliation: this asset uses YT05, while the existing
  Odysseus YT05 research PR #72 has a different subject (video compression).
  Do not count duplicate/conflicting slot labels as additional completed films.

## New real tooling submitted

All three are open/unmerged PRs, not claimed as integrated into main:

- [#73 narration/captions](https://github.com/dreamer2664/chatcode/pull/73): measured
  cue timings, audio mastering, SRT/VTT/transcript generation and hard caption limits.
- [#74 long-form assembly](https://github.com/dreamer2664/chatcode/pull/74): bounded
  shot rendering, resumable cache, stitching, QC and delivery validation. Two
  300-second calibration runs are documented in primary engineering receipts;
  the MP4s themselves were not uploaded there. They are labeled test fixtures and
  DO NOT count toward the ten editorial films.
- [#75 editorial slate](https://github.com/dreamer2664/chatcode/pull/75): ten-topic
  registry, seven additional researched dossiers and duplicate-topic checks.

Producer test claims are documented on those PRs; this progress audit did not
re-run those code suites. The independently performed checks here are the asset
fetch/hash, MP4 headers/edit lists and sample-frame decodes.

## Board snapshot

**6 review, 7 open, 1 claimed, 1 blocked, 0 done** (15 cards).
Cormac has just claimed the Hilbert's Hotel film. The three Odysseus film PRs
#70–72 still contain pre-production work; no new finished exports were found in them.
V04 direction/review lab remains open. V15 final screening remains blocked.

**Bottom line: meaningful progress, including an actual watchable MP4, but not ten
finished and approved films.**
