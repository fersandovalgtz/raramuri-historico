# Facsimile collation and diplomatic transcription status

Rarámuri Histórico Digital maintains eight append-only boundary-review batches spanning both dictionary directions and two machine-confidence tiers, plus a separate diplomatic-transcription layer. AI-assisted visual collation is always distinguished from independent human/philological and linguistic verification.

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
| **High-confidence tier** | **609** | **553** | **56** | **298** | **301–368** |
| `RHD-FR-008` · first `medium_machine` cohort | 100 | 72 | 28 | 9 | 301–308 |
| **Cumulative reviewed corpus** | **709** | **625** | **84** | **307** | **301–368** |

The coverage-first machine layer remains 2,495 candidates. All 609 `high_machine` candidates have been resolved at the boundary-review level. `RHD-FR-008` opens systematic review of the 1,110-candidate `medium_machine` tier and confirms the expected change in error profile: 28 of its first 100 machine candidates are wrapped glosses, Rarámuri forms, running prose, OCR fragments or page-transition carry-over rather than independent article starts. Rejected IDs remain persistent and are never recycled, leaving **2,411 active provisional candidates** across all confidence tiers.

A refined facsimile re-check withdrew one initially proposed correction: `RHD-S1809-00107` is printed as `Apatſchee`; the immediately following `Apatſche.` belongs to the article body. The persistent ID is unchanged and the correction count is therefore 9 for `RHD-FR-008`, 307 cumulatively.

Boundary review validates headword presence, article-start boundary and exact page placement. It does not by itself constitute independent linguistic or philological validation.

## Page-layout reconstruction

Printed pages 301–368 are modeled explicitly as 68 two-column dictionary pages. Layout files `data/facsimile/page_layout_301_317.csv`, `data/facsimile/page_layout_318_339.csv`, `data/facsimile/page_layout_340_357.csv`, `data/facsimile/page_layout_358_361.csv`, `data/facsimile/page_layout_362_365.csv` and `data/facsimile/page_layout_366_368.csv` preserve left/right reading order separately from OCR line order.

Printed p. 353 is the structural transition page where the German→Rarámuri dictionary concludes and the Rarámuri→German dictionary begins. Printed p. 369 begins the appendix and is therefore not part of the two-column dictionary-layout layer. `RHD-FR-008` returns to early German→Rarámuri pages 301–308 and reuses the already established layout model.

## Diplomatic transcription

`RHD-DIP-001A`–`RHD-DIP-007A` provide complete AI-assisted diplomatic coverage for all **553 accepted starts in the exhausted `high_machine` tier**.

`RHD-DIP-008A`–`RHD-DIP-008D` add 66 complete short-article transcriptions from `RHD-FR-008`. `RHD-DIP-008E` completes the six long articles that required multi-column or multi-page reconstruction: `Aloe`, `Apatſchee`, `Baden`, `Backſtube`, `Bär` and `Beſitzen`. `RHD-FR-008` is therefore now **72/72 complete at the AI-assisted diplomatic level**.

The cumulative diplomatic layer contains **625 complete AI-assisted article transcriptions**, exactly matching the **625 accepted starts among the 709 candidates reviewed to date**. The inventory records **308 records with an explicit uncertainty note**. All current diplomatic records remain `human_verified=false`; none should be described as independently philologically or linguistically verified.

## Next editorial stage

The next systematic stage is `RHD-FR-009`: review the next 100 unreviewed `medium_machine` candidates in source order, applying the same facsimile-first boundary, page, column and diplomatic-transcription protocol. Global `full_diplomatic_transcription_completed` remains `false`.
