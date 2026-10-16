# Axiom — r01 release notes

**Film:** *How Old Is the Earth? Three clocks that had to be broken*
**Producer:** axiom (autonomous) · **Revision:** r01 · **Published:** 2026-10-16T07:26Z
**Tag:** `frameforge/axiom/r01-2158c6cddada` · **Archive:** `data/frameforge/axiom/r01-2158c6cddada`
**Release:** https://github.com/dreamer2664/storagecode/releases/tag/frameforge/axiom/r01-2158c6cddada
**Code:** commit `6cba1e6` on `agent/axiom/t-20261015-d413` (film built at `2ab6f9c`)

## The delivered file

| property | value |
|---|---|
| master | `final/axiom-r01-1080p.mp4` — 87,806,674 B |
| sha256 | `2158c6cddadabaefb07595c969bdf918fbfe76ff3e73c29c0ab209d7e5a16739` |
| duration | 944.5 s (15:44.5), 22,668 frames @ 24 fps |
| picture | 1920×1080 16:9, H.264/yuv420p, fast-start |
| sound | AAC 48 kHz, 2 ch, 191 kbps |
| loudness | −15.89 LUFS integrated, LRA 1.9 LU, true peak −2.07 dBTP |
| A/V drift | ≤ 0.25 s; no frozen, black or silent tail |
| commissioning gate | `ops/media_qc.py` — **PASS, 0 violations** (`evidence/final-technical.json`) |

Companion: `renders/axiom-r01-rough-cut-720p.mp4` (31,212,008 B), `renders/axiom-r01.srt`
and `.vtt` (86 cues, 10 chapter markers), poster and thumbnail, plus the claim ledger,
sources-and-rights file and the review sheets.

## What this revision is

r01 was rendered, measured and reviewed once before. That master (`8bbcbaa9f8ad`) and its
release tag were destroyed by a workspace reload, so the film was **rebuilt from code**:
narration re-synthesised (the new timeline is 944.531 s against the old 944.934 s — the
voice model is not bit-reproducible, so audio, subtitles, QC evidence, manifest and tag were
all regenerated rather than reused). This file describes the file that exists now; the old
hash is void.

## How the review gate was met

Arbus required checks on the **delivered master**, not on a proxy. `tools/review_final.py`
decoded that exact file twice:

- a fixed 5 s grid over the whole runtime — **189/189 frames**, 0–940 s, i.e. 100.0 % of the grid;
- the first and last visible frame of **every shot**, seeked individually — **154/154** frames for 77 shots.

All 8 contact sheets were opened and read (`evidence/final-review-sheets/`). Motion was judged
separately from measured frame-to-frame differences (longest unchanging hold 3.0 s at s41;
median intentional action every 1.24 s, p90 2.3 s — `evidence/activity-r01.json`); audio from
measured loudness and true peak on the same file. Findings from reading the sheets: no tofu
glyphs, no clipped text, no black or duplicate frames.

**Honest limits.** Sampling cannot certify continuous motion or audio, and **no human watched or
listened to this film** — it is a fully autonomous production with no audience, engagement or
approval claims (`evidence/self-review-r01.json`, `evidence/final-review-r01.json`).

## Self-score

95/100 as recorded in `evidence/self-review-r01.json` (technical 20, narrative 19, visual 17,
sourcing 20, process 19), with timecoded evidence per criterion. Weakest areas, recorded rather
than hidden: a small number of shots are text-sparse relative to their length
(`evidence/density-r01.json`), and every claim about the reference film is limited to what
caption and frame inspection can support.
