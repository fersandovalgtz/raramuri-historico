# Facsimile collation and diplomatic transcription status

Rarámuri Histórico Digital maintains seven append-only boundary-review batches spanning both dictionary directions, plus a separate diplomatic-transcription layer. AI-assisted visual collation is always distinguished from independent human/philological and linguistic verification.

## Boundary-review results

| Batch | Machine candidates reviewed | Accepted article starts | Rejected false boundaries | Clear headword corrections | Printed-page span |
|---|---:|---:|---:|---:|---|
| `RHD-FR-001` | 100 | 86 | 14 | 4 | 301–317 |
| `RHD-FR-002` | 100 | 85 | 15 | 10 | 318–339 |
| `RHD-FR-003` | 100 | 89 | 11 | 33 | 339–357 |
| `RHD-FR-004` | 100 | 90 | 10 | 62 | 357–361 |
| `RHD-FR-005` | 100 | 96 | 4 | 90 | 361–365 |
| `RHD-FR-006` | 100 | 98 | 2 | 91 | 365–368 |
| `RHD-FR-007` | 9 | 9 | 0 | 8 | 368 |
| **Cumulative high-confidence tier** | **609** | **553** | **56** | **298** | **301–368** |

The coverage-first machine layer remains 2,495 candidates. All **609 candidates classified `high_machine` have now been visually collated against the facsimile**. Of these, 553 are accepted article starts and 56 are rejected false boundaries. Because rejected IDs remain persistent and are never recycled, 2,439 candidates remain active provisionally across all confidence tiers. Candidate count is not asserted as the definitive number of printed lexicographic entries.

Boundary review validates headword presence, article-start boundary and exact page placement. It does not by itself constitute independent linguistic or philological validation.

`RHD-FR-006` and `RHD-FR-007` lie wholly in the Rarámuri→German dictionary. The final small cohort corrects a consequential OCR page drift: several candidates assigned mechanically to p. 369 actually occur on p. 368, while printed p. 369 begins the appendix. All nine final high-confidence candidates are genuine starts on p. 368.

## Page-layout reconstruction

Printed pages 301–368 are modeled explicitly as 68 two-column dictionary pages. Layout files `data/facsimile/page_layout_301_317.csv`, `data/facsimile/page_layout_318_339.csv`, `data/facsimile/page_layout_340_357.csv`, `data/facsimile/page_layout_358_361.csv`, `data/facsimile/page_layout_362_365.csv` and `data/facsimile/page_layout_366_368.csv` preserve left/right reading order separately from OCR line order.

Printed p. 353 is the structural transition page where the German→Rarámuri dictionary concludes and the Rarámuri→German dictionary begins. Printed p. 369 begins the appendix and is therefore not added to the two-column dictionary-layout layer.

## Diplomatic transcription

`RHD-DIP-001A`–`RHD-DIP-001E` cover all 86 accepted starts of `RHD-FR-001`; `RHD-DIP-002A`–`RHD-DIP-002B` cover all 85 of `RHD-FR-002`; `RHD-DIP-003A`–`RHD-DIP-003E` cover all 89 of `RHD-FR-003`; `RHD-DIP-004A`–`RHD-DIP-004E` cover all 90 of `RHD-FR-004`; `RHD-DIP-005A`–`RHD-DIP-005F` cover all 96 of `RHD-FR-005`; and `RHD-DIP-006A`–`RHD-DIP-006D` cover all 98 of `RHD-FR-006`.

`RHD-DIP-007A` covers the nine accepted starts in the final high-confidence cohort on p. 368. The cumulative diplomatic layer therefore contains **553 complete AI-assisted article transcriptions**, exactly matching every accepted start among all 609 `high_machine` candidates. The inventory currently records **284 records with an explicit uncertainty note**.

Ambiguous diacritics and compact historical letter sequences are retained or flagged instead of silently normalized. All current diplomatic records remain `human_verified=false`; completion of the high-confidence AI-assisted layer must not be described as independent philological or linguistic verification.

## Next editorial stage

The `high_machine` tier is now exhausted at the AI-assisted facsimile and diplomatic levels. The next editorial decision is whether to begin systematic review of the **1,110 `medium_machine` candidates** or first establish an independent human/linguistic validation sample over the 553 accepted high-confidence articles. In either route, `full_diplomatic_transcription_completed` remains `false` because the complete 2,495-candidate machine layer has not been diplomatically resolved.
