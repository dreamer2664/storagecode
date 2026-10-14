The fix, verbatim (superocr 9ab638a1, apps/captcha-studio/engine.py):

-# Preserve the canonical face order, but supply our own verified font assets.
-FONT_NAMES = tuple(Path(p).name for p in G._FONT_CANDIDATES)
+# Preserve the canonical face order, but supply our own verified font assets.
+# W2 (aba01082): generator._FONT_CANDIDATES now carries the system eight PLUS
+# the bundled-eight fallback, so the face list must be deduped by basename —
+# otherwise /api/health reports 16 fonts and the eight-face invariant breaks.
+FONT_NAMES = tuple(dict.fromkeys(Path(p).name for p in G._FONT_CANDIDATES))
