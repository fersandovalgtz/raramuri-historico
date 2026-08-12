# Facsimile collation and diplomatic transcription status

Rarámuri Histórico Digital maintains six append-only boundary-review batches spanning both dictionary directions, plus a separate diplomatic-transcription layer. AI-assisted visual collation is always distinguished from independent human/philological and linguistic verification.

## Boundary-review results

| Batch | Machine candidates reviewed | Accepted article starts | Rejected false boundaries | Clear headword corrections | Printed-page span |
|---|---:|---:|---:|---:|---|
| `RHD-FR-001` | 100 | 86 | 14 | 4 | 301–317 |
| `RHD-FR-002` | 100 | 85 | 15 | 10 | 318–339 |
| `RHD-FR-003` | 100 | 89 | 11 | 33 | 339–357 |
| `RHD-FR-004` | 100 | 90 | 10 | 62 | 357–361 |
| `RHD-FR-005` | 100 | 96 | 4 | 90 | 361–365 |
| `RHD-FR-006` | 100 | 98 | 2 | 91 | 365–368 |
| **Cumulative** | **600** | **544** | **56** | **290** | **301–368** |

The coverage-first machine layer remains 2,495 candidates. After 56 visually rejected false boundaries, 2,439 candidates remain active provisionally. Candidate count is not asserted as the definitive number of printed lexicographic entries.

Boundary review validates headword presence, article-start boundary and exact page placement. It does not by itself validate a complete article body or linguistic interpretation.

`RHD-FR-006` lies wholly in the Rarámuri→German dictionary. Direct facsimile collation corrected substantial OCR distortion in the late R–T sequence and rejected two German gloss fragments that had been promoted mechanically to candidate boundaries: `Hinweg` inside `Segui` and `Immer` inside `Sinévi`. It also restored genuine Rarámuri headwords that disappeared in linear OCR, including `Tápoa` before the German gloss “Aufſpielen, Muſik machen.” Persistent IDs are retained and never recycled.

## Page-layout reconstruction

Printed pages 301–368 are modeled explicitly as 68 two-column pages. Layout files `data/facsimile/page_layout_301_317.csv`, `data/facsimile/page_layout_318_339.csv`, `data/facsimile/page_layout_340_357.csv`, `data/facsimile/page_layout_358_361.csv`, `data/facsimile/page_layout_362_365.csv` and `data/facsimile/page_layout_366_368.csv` preserve left/right reading order separately from OCR line order.

Printed p. 353 is the structural transition page where the German→Rarámuri dictionary concludes and the Rarámuri→German dictionary begins. The supplied OCR does not consistently preserve two-column reading order and can drift in page assignment; exact page placement in reviewed records therefore comes from the facsimile overlay.

## Diplomatic transcription

`RHD-DIP-001A`–`RHD-DIP-001E` cover all 86 accepted starts of `RHD-FR-001`; `RHD-DIP-002A`–`RHD-DIP-002B` cover all 85 of `RHD-FR-002`; `RHD-DIP-003A`–`RHD-DIP-003E` cover all 89 of `RHD-FR-003`; `RHD-DIP-004A`–`RHD-DIP-004E` cover all 90 of `RHD-FR-004`; and `RHD-DIP-005A`–`RHD-DIP-005F` cover all 96 of `RHD-FR-005`.

`RHD-FR-006` is also complete at the AI-assisted diplomatic level. `RHD-DIP-006A`–`RHD-DIP-006D` add 98 complete article transcriptions across printed pp. 365–368. The cumulative diplomatic layer therefore contains **544 complete AI-assisted article transcriptions**, exactly matching the 544 accepted starts among the first 600 reviewed high-confidence candidates. The inventory currently records **276 records with an explicit uncertainty note**.

Ambiguous diacritics and compact historical letter sequences are retained or flagged instead of silently normalized. All current diplomatic records remain `human_verified=false`; completion of this layer must not be described as independent philological or linguistic verification.

## Next editorial stage

The first six boundary-review cohorts are internally complete at the AI-assisted diplomatic level: 600 candidates reviewed, 544 accepted starts and 544 complete diplomatic overlays. The machine layer contains 609 `high_machine` candidates in total, so only **nine high-confidence candidates remain**. The next systematic stage is a final small cohort, `RHD-FR-007`, to exhaust that confidence tier before the project turns to the medium-confidence layer or independent human/linguistic validation.
