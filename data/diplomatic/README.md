# Diplomatic transcription layer

This directory contains append-only editorial overlays produced from direct visual comparison with the Steffel 1809 facsimile. The facsimile is authoritative; OCR is retained as a secondary reading aid rather than a source of truth for article boundaries, page placement or body order.

Diplomatic batches preserve source wording and punctuation while not encoding typographic line wrapping. The review method is `visual_facsimile_transcription_ai_assisted`; every current record has `human_verified=false`. These records must therefore not be described as independently philologically or linguistically verified.

`RHD-DIP-001A`–`RHD-DIP-007A` cover all **553 accepted starts** from the fully exhausted 609-candidate `high_machine` tier. Subsequent diplomatic series provide complete coverage for every accepted start in the systematically reviewed `medium_machine` cohorts.

`RHD-DIP-016A`–`RHD-DIP-016I` add **90 complete articles** from `RHD-FR-016` across printed pp. **356–360**, entirely inside the Rarámuri→German section. The series was split into smaller append-only subbatches after a connector-size limitation during writing; this implementation detail does not alter editorial scope or record identity.

The set includes compact lexical articles and the longer `Haleséatschic, oder Hareséatschic` place-name article. Representative recovered forms include `Etschaguóameke`, `Galá tá símega`, `Guarátscha`, `Guechtschíc`, `Jachcála`, `Jumánamatschígameke`, `Kauguáca`, `Kuepútsela, oder Kepútschela` and `Kubírusi, oder Gubírusi`. Two new records carry explicit uncertainty notes for a long toponymic passage and a difficult variant pair.

The facsimile remains authoritative. The 2020 Universidad de Sonora transcription (Merrill et al., DOI `10.47807/UNISON.8`) was used only as a secondary collation aid for difficult Rarámuri glyphs and diacritics; it does not replace direct facsimile evidence.

The cumulative layer currently contains **1,274 complete AI-assisted diplomatic article transcriptions**, exactly matching the **1,274 accepted starts among all 1,509 facsimile-reviewed candidates**. The current inventory records **511 transcriptions with an explicit uncertainty note**. All current records remain `human_verified=false` and pending independent human/philological and linguistic validation.

The machine OCR remains untouched in the source layer. Diplomatic fields are applied as overlays by `scripts/apply_review_overrides.py` and propagated to the derived JSON/XML/TEI/SQLite exports.

The high-confidence tier and the first nine medium-confidence cohorts are complete at the AI-assisted boundary-review and diplomatic-transcription levels. This is not global corpus completion: **210 `medium_machine` candidates remain unreviewed**, 716 `low_machine` candidates remain outside systematic review, and all current diplomatic records remain pending independent human/linguistic validation.

The next cohort is **`RHD-FR-017`**, wholly within Rarámuri→German, automatically estimated around printed pp. **360–365**. Its queue again contains many heavily corrupted Rarámuri candidates, so exact headword, page and column must be established from the facsimile.