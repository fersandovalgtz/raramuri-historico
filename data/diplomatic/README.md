# Diplomatic transcription layer

This directory contains editorial overlays produced from direct visual comparison with the Steffel 1809 facsimile.

`diplomatic_batch_001.json` (`RHD-DIP-001A`) is the first article-text batch. It contains ten short entries whose complete article text can be delimited clearly on the facsimile. The transcription preserves source spelling and punctuation but does not encode typographic line wrapping.

The review method is explicitly `visual_facsimile_transcription_ai_assisted`. `human_verified` is `false`. These records must therefore not be described as philologically or linguistically verified. They are a reproducible intermediate layer designed for subsequent independent human checking.

The machine OCR remains untouched in the source layer. Diplomatic fields are applied as overlays by `scripts/apply_review_overrides.py`.
