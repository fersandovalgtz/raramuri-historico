# Diplomatic transcription layer

This directory contains append-only editorial overlays produced from direct visual comparison with the Steffel 1809 facsimile. The facsimile is authoritative; OCR is retained as a secondary reading aid rather than a source of truth for article boundaries or body order.

Diplomatic batches preserve source spelling and punctuation while not encoding typographic line wrapping. The review method is explicitly `visual_facsimile_transcription_ai_assisted`; every current record has `human_verified=false`. These records must therefore not be described as independently philologically or linguistically verified.

`RHD-DIP-001A`–`RHD-DIP-007A` cover all **553 accepted starts** from the fully exhausted 609-candidate `high_machine` tier. Subsequent diplomatic series provide complete coverage for every accepted start in the systematically reviewed `medium_machine` cohorts.

`RHD-DIP-012A`–`RHD-DIP-012D` contain the 81 complete articles accepted in `RHD-FR-012` across printed pp. 328–338.

`RHD-DIP-013A`–`RHD-DIP-013E` add **83 complete articles** from `RHD-FR-013` across printed pp. 338–344. The set includes short lexical records as well as extended articles `Spiel`, `Spielplatz`, `Staar`, `Stein`, `Sterben` and `Sterblich`, reconstructed in documentary reading order where text crosses columns or pages. Difficult glyphs, Rarámuri forms, diacritics and compact letter sequences are retained or explicitly flagged rather than normalized without evidence.

The cumulative layer currently contains **1,019 complete AI-assisted diplomatic article transcriptions**, exactly matching the 1,019 accepted starts among all 1,209 facsimile-reviewed candidates. The current inventory records **452 transcriptions with an explicit uncertainty note**. All current records remain `human_verified=false` and pending independent human/philological and linguistic validation.

The machine OCR remains untouched in the source layer. Diplomatic fields are applied as overlays by `scripts/apply_review_overrides.py` and propagated to the derived JSON/XML/TEI/SQLite exports.

The high-confidence tier and the first six medium-confidence cohorts are complete at the AI-assisted boundary-review and diplomatic-transcription levels. This is not global corpus completion: **510 `medium_machine` candidates remain unreviewed**, 716 `low_machine` candidates remain outside systematic review, and all current diplomatic records remain pending independent human/linguistic validation.
