# Diplomatic transcription layer

This directory contains append-only editorial overlays produced from direct visual comparison with the Steffel 1809 facsimile. The facsimile is authoritative; OCR is retained as a secondary reading aid rather than a source of truth for article boundaries or body order.

Diplomatic batches preserve source spelling and punctuation while not encoding typographic line wrapping. The review method is explicitly `visual_facsimile_transcription_ai_assisted`; every current record has `human_verified=false`. These records must therefore not be described as independently philologically or linguistically verified.

`RHD-DIP-001A`–`RHD-DIP-007A` cover all **553 accepted starts** from the fully exhausted 609-candidate `high_machine` tier. The subsequent `RHD-DIP-008` through `RHD-DIP-011` series provide complete coverage for every accepted start in the first four `medium_machine` cohorts.

`RHD-DIP-012A`–`RHD-DIP-012D` add **81 complete articles** from `RHD-FR-012` across printed pp. 328–338. The set includes long records such as `Metall`, `Müſſen`, `Pfeil`, `Pflug` and `Reh`, reconstructed in documentary reading order when articles cross columns or printed pages. Difficult readings may be secondarily collated against the 2020 critical edition documented in `SOURCES.md`, while the Steffel 1809 facsimile remains the authoritative source for this layer.

The cumulative layer currently contains **936 complete AI-assisted diplomatic article transcriptions**, exactly matching the 936 accepted starts among all 1,109 facsimile-reviewed candidates. The current inventory records **424 transcriptions with an explicit uncertainty note**. Ambiguous diacritics, compact letter sequences, unusual printer marks, catchwords, source-layout ambiguities and inferential readings are retained or flagged rather than silently normalized.

The machine OCR remains untouched in the source layer. Diplomatic fields are applied as overlays by `scripts/apply_review_overrides.py` and propagated to the derived JSON/XML/TEI/SQLite exports.

The high-confidence tier and the first five medium-confidence cohorts are complete at the AI-assisted boundary-review and diplomatic-transcription levels. This is not global corpus completion: **610 `medium_machine` candidates remain unreviewed**, 716 `low_machine` candidates remain outside systematic review, and all current diplomatic records remain pending independent human/linguistic validation.
