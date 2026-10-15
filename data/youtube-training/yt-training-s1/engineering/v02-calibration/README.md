# V02 calibration run A — receipt (t-20261015-fec3, scipio)

**Labeled engineering fixture. Does NOT count among the ten editorial films.**

| fact | value (independently re-measured, not quoted from the run's own log) |
|---|---|
| final file | calib-300a-final.mp4 (not uploaded — reproducible from the committed spec) |
| sha256 | `ebe4cd54cffc7a227fde0dcc2b16952d6203a0959396f1b4952af716241e1d5e` (verified with sha256sum) |
| video | h264, 1920x1080, yuv420p, 30/1 fps, 9000 frames, 300.000000 s, 48,148,791 B |
| full-file decode | ffmpeg -xerror -f null — exit 0 |
| structure | 12 shots x 25 s, concat demuxer, no re-encode; total == sum of shots |
| wall time | 585.3 s on 2 vCPU / 2 GB (render 544.6 s + concat 0.6 s + QC 40 s) |
| shot caps | preserved — every shot passed the engine's own <=30 s / <=900-frame validateConfig |

## Interruption + resume (part of this run, by accident and then by design)

The run started on /tmp, which turned out to be a 992 MB tmpfs — a real risk of
ENOSPC mid-film. It was stopped during shot 7, the content-hash cache was moved
to the persistent disk, and the build relaunched: shots 1-6 came back as cache
hits (verified in `run-a-film-manifest.json` → `cache: hit`), shot 7's partial
directory was refused (manifest status != structural-pass) and re-rendered,
shots 8-12 rendered fresh. No lost or duplicated shots: the concat duration
equals the sum of the shots exactly.

## What run A exposed (and why the rig changed after it)

All twelve shots were byte-identical (one distinct sha256 across shots): same
scene, same config, same cache key. Timing, stitching, decode and resume all
passed on what was content-wise a loop. ACCEPTANCE forbids exactly that
padding, so a filler/loop guard was added to the orchestrator: any two
byte-identical shots now fail closed unless a recorded
`spec.allowRepeatedShots.reason` explains them (chatcode
agent/scipio/t-20261015-fec3 @f4df804d). Run A's receipt stands as the negative
test for that guard; run B (distinct per-shot content + audio track) is the
clean calibration run.

## Reproduce

```
cd projects/motion-studio   # chatcode, branch agent/scipio/t-20261015-fec3
node longform/build.mjs --spec longform/calib-300a.spec.json --work <dir> --cache <dir>
```

---

# V02 calibration run B — receipt (the clean run)

| fact | value (independently re-measured) |
|---|---|
| final file | calib-300b-final.mp4 (not uploaded — reproducible from the committed spec) |
| sha256 | `6acb039d87a68735c53e61379c76fc89c22eb17d14f8e2968b76e0734de06055` (sha256sum) |
| video | h264, 1920x1080, yuv420p, 30/1 fps, 9000 frames |
| audio | aac, 48000 Hz (muxed 300 s calibration bed; drift measured 0.000 s) |
| duration | 300.000000 s |
| full-file decode | exit 0 |
| loudness | integrated -15.9 LUFS (target -16 +/-1.5), true peak -11.8 dBFS (limit -1) |
| shots | 12/12 DISTINCT shot hashes — the filler/loop guard had real content to pass |
| black/freeze | 0 unexplained segments |
| wall time | 982.7 s on 2 vCPU / 2 GB, fresh cache (nothing reused from run A) |

The audio track is a labeled engineering bed (196 Hz tone at -16 LUFS), not
narration: run B's job is the mux/drift/loudness path at five-minute scale.
Real narration goes through projects/youtube-training/tools/narrate.py (V03,
chatcode PR #73), whose live TTS proof and tests are on that card.

First launch attempt fail-closed on frame 2 (notDead): the fixture scene's sweep
moved ~0.12 deg/frame — the grader was right, the scene was fixed, no threshold
was weakened (chatcode @745f7e1f). Kept here as evidence the gate bites.

## Reproduce

```
cd projects/motion-studio   # chatcode, branch agent/scipio/t-20261015-fec3
node longform/build.mjs --spec longform/calib-300b.spec.json --work <disk-dir> --cache <disk-dir>
# add narration: runtime spec copy with "narration": "<path>.wav" (see run-b)
```
