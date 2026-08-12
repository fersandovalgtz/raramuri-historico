# Diplomatic transcription layer

This directory contains append-only editorial overlays produced from direct visual comparison with the Steffel 1809 facsimile. The facsimile is authoritative; OCR is retained as a secondary reading aid rather than a source of truth for article boundaries, page placement or body order.

Diplomatic batches preserve source spelling and punctuation while not encoding typographic line wrapping. The review method is `visual_facsimile_transcription_ai_assisted`; every current record has `human_verified=false`. These records must therefore not be described as independently philologically or linguistically verified.

`RHD-DIP-001A`–`RHD-DIP-007A` cover all **553 accepted starts** from the fully exhausted 609-candidate `high_machine` tier. Subsequent diplomatic series provide complete coverage for every accepted start in the systematically reviewed `medium_machine` cohorts.

`RHD-DIP-015A`–`RHD-DIP-015E` add **84 complete articles** from `RHD-FR-015` across printed pp. **350–356**. This is the first diplomatic cohort to cross the documentary direction change on p. 353. `RHD-DIP-015A` remains German→Rarámuri; `RHD-DIP-015B` contains the transition; subsequent records are Rarámuri→German.

The set includes long grammatical or cultural articles such as `Wolf`, `Wollen`, `Zugehören`, `Baláliruc`, `Baſſirúgameke`, `Batſabe` and `Có oder gö`, as well as many inverse-dictionary forms whose OCR headwords required direct facsimile recovery. Historical spelling and punctuation are retained; difficult diacritics, Rarámuri forms and morphological interpretations are explicitly flagged rather than normalized without evidence.

The cumulative layer currently contains **1,184 complete AI-assisted diplomatic article transcriptions**, exactly matching the **1,184 accepted starts among all 1,409 facsimile-reviewed candidates**. The current inventory records **509 transcriptions with an explicit uncertainty note**. All current records remain `human_verified=false` and pending independent human/philological and linguistic validation.

The machine OCR remains untouched in the source layer. Diplomatic fields are applied as overlays by `scripts/apply_review_overrides.py` and propagated to the derived JSON/XML/TEI/SQLite exports.

The high-confidence tier and the first eight medium-confidence cohorts are complete at the AI-assisted boundary-review and diplomatic-transcription levels. This is not global corpus completion: **310 `medium_machine` candidates remain unreviewed**, 716 `low_machine` candidates remain outside systematic review, and all current diplomatic records remain pending independent human/linguistic validation.

The next cohort is **`RHD-FR-016`**, wholly within the Rarámuri→German section. Its OCR-derived queue spans approximately printed pp. 356–360 and contains many heavily corrupted Rarámuri candidates, so the same facsimile-first, column-aware protocol remains necessary.