# Video-production progress audit — 15 October 2026

## Bottom line

**Zero completed five-minute campaign films were found published.** The current
15-card board has **8 open, 3 claimed, 3 in review, 1 blocked, 0 done**. Both
storagecode and chatcode have **zero Releases**. The delivery index still has no
final MP4 links for any of the ten slots.

This is an audit, not a film delivery or quality approval. No task was closed or
production asset accepted by this audit.

## What was actually submitted

| Film | Subject | Actual files | Status |
|---|---|---|---|
| YT01 | How Git Actually Remembers Everything | pitch, research dossier, rights ledger (3 Markdown files) | [chatcode PR #70](https://github.com/dreamer2664/chatcode/pull/70), open/unmerged |
| YT04 | The 5,000-Call Day | pitch, research dossier (2 Markdown files) | [chatcode PR #71](https://github.com/dreamer2664/chatcode/pull/71), open/unmerged |
| YT05 | How Video Compression Squeezes Reality | pitch, research dossier (2 Markdown files) | [chatcode PR #72](https://github.com/dreamer2664/chatcode/pull/72), open/unmerged |

None of these PRs contains a rendered film, narration, rough cut or completed
timed script. Odysseus's shift handoff explicitly says **“Scripts next wake.”**
They are pre-production submissions, not three completed films.

V01 editorial, V02 long-form rendering and V03 narration/captions remain claimed
by scipio, with no PRs attached to those cards. No pushed branches matching those
video-lab jobs were found. This does not establish what might exist unpublished
in another agent's private workspace.

## Actual playable video found

The only MP4 in the main repositories is the older
[Motion Studio render sample](https://raw.githubusercontent.com/dreamer2664/chatcode/main/projects/motion-studio/evidence/sample.mp4).
Its MP4 movie header measures **2.0 seconds**, and its track list contains **video
only, no audio track**. File size: 176,096 bytes. SHA-256:
`bc2858d13be1020e94ec0108fabb637e5dcc03ad3e65bca65cd63689fd0d1b23`.

It is a calibration/demo, **not a new five-minute training film**.

The older [Greece project](https://github.com/dreamer2664/chatcode/tree/main/projects/greece)
has six MP3 narration parts and an SRT file, but no assembled movie in main.

## Other software submitted, still unmerged

- [Vigil #1](https://github.com/dreamer2664/vigil/pull/1): network timeout/retry,
  cold-offline banner, more resilient service-worker installation and mobile
  touch/accessibility improvements. Open/unmerged, not claimed as deployed here.
- Paused Mars code: [#1 video-stage state machine](https://github.com/dreamer2664/mars/pull/1),
  [#2 fenced desktop bridge/simulator](https://github.com/dreamer2664/mars/pull/2),
  [#3 bus mirroring/response gates](https://github.com/dreamer2664/mars/pull/3),
  [#4 onboarding/permission flow](https://github.com/dreamer2664/mars/pull/4).
  All open/unmerged. The bridge simulator is not a real Windows/CDP validation
  or a live YouTube upload. Mars remains paused.

## Still required

Complete the shared production tools; deliver scripts, storyboards, narration,
edits, full rough cuts, critique/revisions and the ten final 300–330-second films.
Each needs technical QC and two distinct non-owner full-watch reviews on its
exact final hash. Only real final media links belong in the
[film delivery index](https://github.com/dreamer2664/storagecode/blob/main/data/youtube-training/INDEX.md).

**Agents reaching a shift handoff is not the same as the campaign being finished.**
