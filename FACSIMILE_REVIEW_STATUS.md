# Facsimile collation and diplomatic transcription status

Rarámuri Histórico Digital maintains twelve append-only boundary-review batches spanning both dictionary directions and two machine-confidence tiers, plus a separate diplomatic-transcription layer. AI-assisted visual collation is always distinguished from independent human/philological and linguistic verification.

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
| `RHD-FR-012` · fifth `medium_machine` cohort | 100 | 81 | 19 | 12 | 328–338 |
| **Cumulative reviewed corpus** | **1,109** | **936** | **173** | **344** | **301–368** |

The coverage-first machine layer remains 2,495 candidates. All 609 `high_machine` candidates have been resolved. The first 500 of 1,110 `medium_machine` candidates have also been reviewed: **383 accepted starts and 117 false boundaries**. `RHD-FR-012` covers printed pp. 328–338 and rejects Rarámuri equivalents, cross-references, catchwords, running prose, page-header noise and OCR fragments that the machine layer had proposed as article boundaries. Rejected IDs remain persistent and are never recycled, leaving **2,322 active provisional candidates** across all confidence tiers.

Among the clear `RHD-FR-012` lemma corrections are `Mager`, `Mantel`, `Matt`, `Meſſer`, `Niemals`, `Palmbaum`, `Papier`, `Pflug`, `Prieſter`, `Raubvogel`, `Raufen` and `Roſt`.

Boundary review validates headword presence, article-start boundary and exact page placement. It does not by itself constitute independent linguistic or philological validation.

## Page-layout reconstruction

Printed pages 301–368 remain modeled explicitly as 68 two-column dictionary pages. `RHD-FR-012` reuses that layout layer across pp. 328–338; several long articles cross column or page boundaries and therefore cannot be reconstructed safely from linear OCR order alone. Printed p. 353 is the German→Rarámuri / Rarámuri→German transition; printed p. 369 begins the appendix.

## Diplomatic transcription

`RHD-DIP-001A`–`RHD-DIP-007A` provide complete AI-assisted diplomatic coverage for all **553 accepted starts in the exhausted `high_machine` tier**. Subsequent diplomatic series cover every accepted start in `RHD-FR-008` through `RHD-FR-012`.

For `RHD-FR-012`, `RHD-DIP-012A`–`RHD-DIP-012D` provide **81 complete article transcriptions**. The set includes short lexical records as well as extended entries such as `Metall`, `Müſſen`, `Pfeil`, `Pflug` and `Reh`. Difficult long passages were reconstructed from the facsimile and, where useful, secondarily collated against the 2020 critical edition documented in `SOURCES.md`; the facsimile remains the authoritative source.

The cumulative diplomatic layer contains **936 complete AI-assisted article transcriptions**, exactly matching the **936 accepted starts among the 1,109 candidates reviewed to date**. The inventory records **424 records with an explicit uncertainty note**. All current diplomatic records remain `human_verified=false`; none should be described as independently philologically or linguistically verified.

## Next editorial stage

The next systematic stage is `RHD-FR-013`: review the next 100 unreviewed `medium_machine` candidates in source order, applying the same facsimile-first boundary, page, column and diplomatic-transcription protocol. **610 `medium_machine` candidates remain unreviewed**, followed by 716 `low_machine` candidates. Global `full_diplomatic_transcription_completed` remains `false`.
