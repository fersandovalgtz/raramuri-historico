# Diplomatic transcription layer

This directory contains append-only editorial overlays produced from direct visual comparison with the Steffel 1809 facsimile. The facsimile is authoritative; OCR is retained as a secondary reading aid rather than a source of truth for article boundaries or body order.

Diplomatic batches preserve source spelling and punctuation while not encoding typographic line wrapping. The review method is explicitly `visual_facsimile_transcription_ai_assisted`; every current record has `human_verified=false`. These records must therefore not be described as independently philologically or linguistically verified.

`RHD-DIP-001A`–`RHD-DIP-007A` cover all **553 accepted starts** from the fully exhausted 609-candidate `high_machine` tier.

`RHD-DIP-008A`–`RHD-DIP-008D` begin the medium-confidence diplomatic layer with 66 complete short articles from `RHD-FR-008`. `RHD-DIP-008E` completes the six long articles that required multi-column or multi-page reconstruction: `Aloe`, `Apatſchee`, `Baden`, `Backſtube`, `Bär` and `Beſitzen`. Thus all **72 accepted starts in `RHD-FR-008`** have complete AI-assisted diplomatic overlays.

The cumulative layer currently contains **625 complete AI-assisted diplomatic article transcriptions**, exactly matching the 625 accepted starts among all 709 facsimile-reviewed candidates. The current inventory records **308 transcriptions with an explicit uncertainty note**. Ambiguous diacritics, compact letter sequences, unusual printer marks, catchwords and inferential readings are retained or flagged rather than silently normalized.

The machine OCR remains untouched in the source layer. Diplomatic fields are applied as overlays by `scripts/apply_review_overrides.py` and propagated to the derived JSON/XML/TEI/SQLite exports.

The high-confidence tier and the first medium-confidence cohort are now complete at the AI-assisted boundary-review and diplomatic-transcription levels. This is not global corpus completion: **1,010 `medium_machine` candidates remain unreviewed**, 716 `low_machine` candidates remain outside systematic review, and all current diplomatic records remain pending independent human/linguistic validation.
