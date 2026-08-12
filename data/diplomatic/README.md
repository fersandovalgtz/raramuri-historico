# Diplomatic transcription layer

This directory contains append-only editorial overlays produced from direct visual comparison with the Steffel 1809 facsimile. The facsimile is authoritative; OCR is retained as a secondary reading aid rather than a source of truth for article boundaries or body order.

Diplomatic batches preserve source spelling and punctuation while not encoding typographic line wrapping. The review method is explicitly `visual_facsimile_transcription_ai_assisted`; every current record has `human_verified=false`. These records must therefore not be described as independently philologically or linguistically verified.

`RHD-DIP-001A`–`RHD-DIP-001E` cover all 86 accepted starts of `RHD-FR-001`. `RHD-DIP-002A`–`RHD-DIP-002B` cover all 85 accepted starts of `RHD-FR-002`. `RHD-DIP-003A`–`RHD-DIP-003E` cover all 89 accepted starts of `RHD-FR-003`. `RHD-DIP-004A`–`RHD-DIP-004E` cover all 90 accepted starts of `RHD-FR-004`. `RHD-DIP-005A`–`RHD-DIP-005F` cover all 96 accepted starts of `RHD-FR-005`. `RHD-DIP-006A`–`RHD-DIP-006D` cover all 98 accepted starts of `RHD-FR-006`. `RHD-DIP-007A` covers all nine accepted starts in the final `high_machine` cohort on printed p. 368.

The cumulative layer contains **553 complete AI-assisted diplomatic article transcriptions**, exactly matching every accepted article start among all **609 facsimile-reviewed `high_machine` candidates**. The current inventory records **284 transcriptions with an explicit uncertainty note**. Ambiguous diacritics, compact letter sequences, unusual printer marks, catchwords and inferential readings are retained or flagged rather than silently normalized.

The machine OCR remains untouched in the source layer. Diplomatic fields are applied as overlays by `scripts/apply_review_overrides.py` and propagated to the derived JSON/XML/TEI/SQLite exports.

The high-confidence machine tier is now fully resolved at the AI-assisted boundary-review and diplomatic-transcription levels. This is not global corpus completion: 1,110 `medium_machine` and 716 `low_machine` candidates remain outside systematic facsimile review, and all current diplomatic records remain pending independent human/linguistic validation.
