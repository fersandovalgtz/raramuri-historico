# Diplomatic transcription layer

This directory contains append-only editorial overlays produced from direct visual comparison with the Steffel 1809 facsimile. The facsimile is authoritative; OCR is retained as a secondary reading aid rather than a source of truth for article boundaries or body order.

Diplomatic batches preserve source spelling and punctuation while not encoding typographic line wrapping. The review method is explicitly `visual_facsimile_transcription_ai_assisted`; every current record has `human_verified=false`. These records must therefore not be described as independently philologically or linguistically verified.

`RHD-DIP-001A`–`RHD-DIP-001E` cover all 86 accepted starts of `RHD-FR-001`. `RHD-DIP-002A`–`RHD-DIP-002B` cover all 85 accepted starts of `RHD-FR-002`. `RHD-DIP-003A`–`RHD-DIP-003E` cover all 89 accepted starts of `RHD-FR-003`. `RHD-DIP-004A`–`RHD-DIP-004E` cover all 90 accepted starts of `RHD-FR-004`. `RHD-DIP-005A`–`RHD-DIP-005F` cover all 96 accepted starts of `RHD-FR-005` across printed pp. 361–365.

The cumulative layer currently contains **446 complete AI-assisted diplomatic article transcriptions**, exactly matching the 446 accepted article starts among the first 500 facsimile-reviewed high-confidence candidates. The current inventory records **229 transcriptions with an explicit uncertainty note**. Ambiguous diacritics, compact letter sequences, unusual printer marks, catchwords and inferential readings are retained or flagged rather than silently normalized.

The machine OCR remains untouched in the source layer. Diplomatic fields are applied as overlays by `scripts/apply_review_overrides.py` and propagated to the derived JSON/XML/TEI/SQLite exports.
