# Diplomatic transcription layer

This directory contains append-only editorial overlays produced from direct visual comparison with the Steffel 1809 facsimile. The facsimile is authoritative; OCR is retained as a secondary reading aid rather than a source of truth for article boundaries or body order.

Diplomatic batches preserve source spelling and punctuation while not encoding typographic line wrapping. The review method is explicitly `visual_facsimile_transcription_ai_assisted`; every current record has `human_verified=false`. These records must therefore not be described as independently philologically or linguistically verified.

`RHD-DIP-001A`–`RHD-DIP-007A` cover all **553 accepted starts** from the fully exhausted 609-candidate `high_machine` tier. `RHD-DIP-008A`–`RHD-DIP-008E` cover all 72 accepted starts in the first medium-confidence cohort, and `RHD-DIP-009A`–`RHD-DIP-009F` cover all 70 accepted starts in the second.

`RHD-DIP-010A`–`RHD-DIP-010C` add **75 complete short/medium articles** from `RHD-FR-010` across printed pp. 315–322. `RHD-DIP-010D` completes the four longer articles `Feige indianiſche`, `Fragen`, `Geige` and `Getränk`. Thus all **79 accepted starts in `RHD-FR-010`** have complete AI-assisted diplomatic overlays.

`RHD-DIP-011A`–`RHD-DIP-011C` add **72 complete short/medium articles** from `RHD-FR-011` across printed pp. 322–327. `RHD-DIP-011D` completes the nine longer articles `Gras`, `Gries`, `Hart`, `Herr`, `Hinaus`, `Ja`, `Jahr`, `Kochen` and `Kranich`. Thus all **81 accepted starts in `RHD-FR-011`** have complete AI-assisted diplomatic overlays.

The cumulative layer currently contains **855 complete AI-assisted diplomatic article transcriptions**, exactly matching the 855 accepted starts among all 1,009 facsimile-reviewed candidates. The current inventory records **390 transcriptions with an explicit uncertainty note**. Ambiguous diacritics, compact letter sequences, unusual printer marks, catchwords and inferential readings are retained or flagged rather than silently normalized.

The machine OCR remains untouched in the source layer. Diplomatic fields are applied as overlays by `scripts/apply_review_overrides.py` and propagated to the derived JSON/XML/TEI/SQLite exports.

The high-confidence tier and the first four medium-confidence cohorts are complete at the AI-assisted boundary-review and diplomatic-transcription levels. This is not global corpus completion: **710 `medium_machine` candidates remain unreviewed**, 716 `low_machine` candidates remain outside systematic review, and all current diplomatic records remain pending independent human/linguistic validation.
