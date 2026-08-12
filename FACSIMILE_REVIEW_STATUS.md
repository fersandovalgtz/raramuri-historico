# Facsimile collation and diplomatic transcription status

Rarámuri Histórico Digital maintains nine append-only boundary-review batches spanning both dictionary directions and two machine-confidence tiers, plus a separate diplomatic-transcription layer. AI-assisted visual collation is always distinguished from independent human/philological and linguistic verification.

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
| **Cumulative reviewed corpus** | **809** | **695** | **114** | **314** | **301–368** |

The coverage-first machine layer remains 2,495 candidates. All 609 `high_machine` candidates have been resolved. The first 200 `medium_machine` candidates have now also been reviewed: 142 accepted starts and 58 false boundaries. `RHD-FR-009` again shows the noisier medium-confidence error profile, with wrapped Rarámuri equivalents, prose inside long articles, section/header noise and OCR page-transition material among the rejected candidates. Rejected IDs remain persistent and are never recycled, leaving **2,381 active provisional candidates** across all confidence tiers.

Direct facsimile collation also corrected page interpolation inside `RHD-FR-009`: the `Bley`–`Blitzen` group occurs on printed p. 309 rather than p. 310, while `Einbilden, ſich`, `Eingebohrner` and `Eingedenk ſeyn` occur on p. 313 rather than p. 314. These corrections are stored in the review manifest rather than hidden in downstream exports.

Boundary review validates headword presence, article-start boundary and exact page placement. It does not by itself constitute independent linguistic or philological validation.

## Page-layout reconstruction

Printed pages 301–368 remain modeled explicitly as 68 two-column dictionary pages. `RHD-FR-009` revisits pp. 308–315 and therefore reuses the existing layout layer. Printed p. 353 is the German→Rarámuri / Rarámuri→German transition; printed p. 369 begins the appendix.

## Diplomatic transcription

`RHD-DIP-001A`–`RHD-DIP-007A` provide complete AI-assisted diplomatic coverage for all **553 accepted starts in the exhausted `high_machine` tier**. `RHD-DIP-008A`–`RHD-DIP-008E` cover all **72 accepted starts in `RHD-FR-008`**.

`RHD-DIP-009A`–`RHD-DIP-009E` add 65 short accepted articles from printed pp. 308–315. `RHD-DIP-009F` completes the five longer records `Da`, `Dieb`, `Dorfrichter`, `Dürfen` and the multi-page ethnographic article `Ente`. Thus **all 70 accepted starts in `RHD-FR-009` are complete at the AI-assisted diplomatic level**.

The cumulative diplomatic layer contains **695 complete AI-assisted article transcriptions**, exactly matching the **695 accepted starts among the 809 candidates reviewed to date**. The inventory records **329 records with an explicit uncertainty note**. All current diplomatic records remain `human_verified=false`; none should be described as independently philologically or linguistically verified.

## Next editorial stage

The next systematic stage is `RHD-FR-010`: review the next 100 unreviewed `medium_machine` candidates in source order, applying the same facsimile-first boundary, page, column and diplomatic-transcription protocol. **910 `medium_machine` candidates remain unreviewed**, followed by 716 `low_machine` candidates. Global `full_diplomatic_transcription_completed` remains `false`.
