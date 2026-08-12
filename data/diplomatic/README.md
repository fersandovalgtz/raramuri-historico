# Diplomatic transcription layer

This directory contains editorial overlays produced from direct visual comparison with the Steffel 1809 facsimile. Source spelling and punctuation are retained; typographic line wrapping is generally not encoded.

The review method is explicitly `visual_facsimile_transcription_ai_assisted`. Every current manifest has `human_verified=false`. These records must therefore not be described as independently philologically or linguistically verified. They form a reproducible intermediate documentary layer designed for subsequent specialist checking.

The machine OCR remains untouched in the source layer. Diplomatic fields are applied as overlays by `scripts/apply_review_overrides.py`, then propagated to the structured exports and public projection.

## Current batches

`RHD-DIP-001A`–`RHD-DIP-001E` cover all 86 accepted starts from `RHD-FR-001`. `RHD-DIP-002A` and `RHD-DIP-002B` cover all 85 accepted starts from `RHD-FR-002`.

`RHD-DIP-003A`–`RHD-DIP-003E` now cover all 89 accepted starts from `RHD-FR-003`. The final `003D` batch completes the remaining German→Rarámuri articles, including the long `Seitenſtechen` entry reconstructed across pp. 340–341. `003E` completes the remaining Rarámuri→German articles around the p. 353 dictionary-direction transition and pp. 354–356.

The cumulative layer contains **260 complete AI-assisted diplomatic article transcriptions**, matching the 260 accepted starts among the first 300 facsimile-reviewed machine candidates. Readings with uncertain diacritics, compact Fraktur forms, multi-column continuations, or structurally inferred cross-references retain explicit `uncertainty_note` metadata.

One notable case is `Cuviruſi, ſ. Gries.` on p. 356. The terminal cross-reference is difficult in the scan; the reading `Gries` is supported by the visible letters and the source's internal German→Rarámuri `Gries` article. It is intentionally recorded as an AI-assisted inference pending human confirmation, not as a settled philological emendation.
