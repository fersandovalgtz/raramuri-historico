# Facsimile collation and diplomatic transcription status

Rarámuri Histórico Digital maintains eleven append-only boundary-review batches spanning both dictionary directions and two machine-confidence tiers, plus a separate diplomatic-transcription layer. AI-assisted visual collation is always distinguished from independent human/philological and linguistic verification.

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
| `RHD-FR-009` · second `medium_machine` cohort | 100 | 70 | 30 | 7 | 308–315 |
| `RHD-FR-010` · third `medium_machine` cohort | 100 | 79 | 21 | 13 | 315–322 |
| `RHD-FR-011` · fourth `medium_machine` cohort | 100 | 81 | 19 | 5 | 322–327 |
| **Cumulative reviewed corpus** | **1,009** | **855** | **154** | **332** | **301–368** |

The coverage-first machine layer remains 2,495 candidates. All 609 `high_machine` candidates have been resolved. The first 400 of 1,110 `medium_machine` candidates have now also been reviewed: 302 accepted starts and 98 false boundaries. `RHD-FR-011` covers printed pp. 322–327. Its rejected candidates again demonstrate the need for facsimile-first review: they include cross-references, Rarámuri equivalents, OCR fragments and running prose embedded within longer articles. Rejected IDs remain persistent and are never recycled, leaving **2,341 active provisional candidates** across all confidence tiers.

Boundary review validates headword presence, article-start boundary and exact page placement. It does not by itself constitute independent linguistic or philological validation.

## Page-layout reconstruction

Printed pages 301–368 remain modeled explicitly as 68 two-column dictionary pages. `RHD-FR-011` revisits pp. 322–327 and therefore reuses the existing layout layer. Printed p. 353 is the German→Rarámuri / Rarámuri→German transition; printed p. 369 begins the appendix.

## Diplomatic transcription

`RHD-DIP-001A`–`RHD-DIP-007A` provide complete AI-assisted diplomatic coverage for all **553 accepted starts in the exhausted `high_machine` tier**. `RHD-DIP-008A`–`RHD-DIP-008E` cover all 72 accepted starts in `RHD-FR-008`, and `RHD-DIP-009A`–`RHD-DIP-009F` cover all 70 accepted starts in `RHD-FR-009`.

For `RHD-FR-010`, `RHD-DIP-010A`–`RHD-DIP-010C` contain 75 complete short/medium articles and `RHD-DIP-010D` completes the four longer records `Feige indianiſche`, `Fragen`, `Geige` and `Getränk`.

For `RHD-FR-011`, `RHD-DIP-011A`–`RHD-DIP-011C` contain **72 complete short/medium articles**. `RHD-DIP-011D` completes the nine longer records `Gras`, `Gries`, `Hart`, `Herr`, `Hinaus`, `Ja`, `Jahr`, `Kochen` and `Kranich`. Thus **all 81 accepted starts in `RHD-FR-011` are complete at the AI-assisted diplomatic level**.

The cumulative diplomatic layer contains **855 complete AI-assisted article transcriptions**, exactly matching the **855 accepted starts among the 1,009 candidates reviewed to date**. The inventory records **390 records with an explicit uncertainty note**. All current diplomatic records remain `human_verified=false`; none should be described as independently philologically or linguistically verified.

## Next editorial stage

The next systematic stage is `RHD-FR-012`: review the next 100 unreviewed `medium_machine` candidates in source order, applying the same facsimile-first boundary, page, column and diplomatic-transcription protocol. **710 `medium_machine` candidates remain unreviewed**, followed by 716 `low_machine` candidates. Global `full_diplomatic_transcription_completed` remains `false`.
