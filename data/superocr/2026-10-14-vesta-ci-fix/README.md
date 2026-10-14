# superocr — main CI regression + fix (2026-10-14, vesta)

## What broke

Main CI went red at `aba01082` (merge of #82, "W2 release custody") and stayed
red through #53/#73/#76: `tests/test_captcha_studio.py::HTTPTests.
test_health_and_static` asserts `build.fonts == 8`, and the app answered 16.

## Why

#82 added the bundled-font fallback: `generator._FONT_CANDIDATES` became the
system eight PLUS the bundled eight, and `apps/captcha-studio/engine.py` mapped
that list 1:1 into `FONT_NAMES` — so `/api/health` counted every face twice.

## The fix — `9ab638a1`

`FONT_NAMES = tuple(dict.fromkeys(Path(p).name for p in G._FONT_CANDIDATES))`
— deduped by basename, canonical order preserved. The app reports, verifies
and ships eight faces again. Local: 24/24 in tests/test_captcha_studio.py;
app-bundle 0 failures; wide-M split ok.

## Files

- `ci-red-extract.txt` — the failing block from run d364f233's log (verbatim).
- `fix.md` — the diff that closed it.
- `ci-after.txt` — CI conclusion on 9ab638a1 (superocr's full suite is slow;
  the number lands here when it finishes).
