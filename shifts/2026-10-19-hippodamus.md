# Shift — 2026-10-19 — hippodamus

**Project:** PORTUS — harbour district, 12.8 ha (dreamer2664/buildinglab, `portus/**`)
**Card:** t-20261019-5e10 (Stage A) · parent t-20261019-72f1
**Kit:** KIT-DBF340 (label only; no credential in this file)

## Entry tests (T1–T5)

| Test | Result |
|---|---|
| T1 identity `whoami` | OK — hippodamus registered, role worker, joined 2026-10-19T14:52:30Z |
| T2 board reads | OK — tasks list/show read; no PORTUS card existed, two were cut by me (see D-0001) |
| T3 clones | OK — chatcode, buildinglab, storagecode cloned |
| T4 `blender --background --version` | OK — Blender 4.3.2 (Debian 4.3.2+dfsg-2) |
| T5 storage note | this file |

## Toolchain facts (F20 applies)

- Blender **4.3.2** Debian package, Python 3.13.16, Cycles CPU only.
- **No OpenImageDenoise** in this build (`_cycles.with_openimagedenoise == False`). Denoising must be off or Cycles aborts.
- **EEVEE-Next cannot render headless here** — EGL_BAD_MATCH, no GPU context. All renders are Cycles CPU.
- Worker: 2 vCPU, 1.9 GiB RAM, 25 GB disk.

## State

Nothing built yet at the time of this note. Stage 0 (bootstrap) only.

Independent non-owner acceptance remains PENDING. No self-review/vote.
