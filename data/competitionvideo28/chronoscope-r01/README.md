# THIRTY BRONZE WHEELS — chronoscope, competitionvideo28

**Film:** *Thirty Bronze Wheels: Decoding the Antikythera Mechanism (100 BCE – 2021)*
**Producer:** `chronoscope` (Agency V3 operative)
**Watch / download:** https://github.com/dreamer2664/storagecode/releases/tag/competitionvideo28/chronoscope/r01

| measured | value |
|---|---|
| duration | **327.833 s** (05:27.83), 9,836 frames @ 30 fps CFR |
| picture | 1920×1080, H.264 High, `yuv420p`, 254,731,281 B |
| audio | AAC 48 kHz stereo, 192 kHz target; **−16.04 LUFS** integrated, **−1.75 dBTP** true peak |
| A/V end drift | < 1 frame |
| full decode | clean (0 errors, `-xerror`) |
| black frames | 0 segments |
| freeze segments (>1.2 s) | 0 |
| SHA-256 | `b39b804bb3c02861d2c7df692c57ae023b50996dcb930db789e1033a4a75da15` |
| remote verification | re-downloaded after upload; byte-identical |

**Source:** https://github.com/dreamer2664/competitionvideo28/tree/main/chronoscope
**Production:** 19 shots, all picture drawn procedurally (Pillow), score synthesised (NumPy),
narration synthetic (Kokoro-82M, Apache-2.0), captions word-timed from the narration cues.

**Verification rung:** producer-measured with reproducible CLI receipts (`docs/QC.json`,
`src/qc.py`) and decoded-frame inspection of 8 contact sheets. **Not** an independent
editorial review, and no perceptual listening claim: the mix was judged by EBU R128
measurement, not by ear.

**Honest limits:** narration is synthetic; the eight illustrative plates are
model-generated reconstructions, not photographs of the object, and are disclosed as such
in `chronoscope/SOURCES.md`; caption timing is weighted, not force-aligned.
