# Facsimile collation and diplomatic transcription status

Rarámuri Histórico Digital maintains fifteen append-only boundary-review batches spanning both dictionary directions and two machine-confidence tiers, plus a separate diplomatic-transcription layer. AI-assisted visual collation is always distinguished from independent human/philological and linguistic verification.

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
| `RHD-FR-013` · sixth `medium_machine` cohort | 100 | 83 | 17 | 9 | 338–344 |
| `RHD-FR-014` · seventh `medium_machine` cohort | 100 | 81 | 19 | 6 | 345–350 |
| `RHD-FR-015` · eighth `medium_machine` cohort | 100 | 84 | 16 | 37 | 350–356 |
| **Cumulative reviewed corpus** | **1,409** | **1,184** | **225** | **396** | **301–368** |

The coverage-first machine layer remains 2,495 candidates. All 609 `high_machine` candidates have been resolved. The first 800 of 1,110 `medium_machine` candidates have also been reviewed: **631 accepted starts and 169 false boundaries**. Rejected IDs remain persistent and are never recycled, leaving **2,270 active provisional candidates** across all confidence tiers.

`RHD-FR-015` is the first systematic medium-confidence batch to cross the documentary change of dictionary direction. Direct facsimile collation showed that the cohort begins on printed p. 350, not p. 351 as estimated by the OCR-derived queue, and that German→Rarámuri ends and Rarámuri→German begins within printed p. 353. This confirms that page placement and direction must be established from documentary geometry rather than linear OCR order.

The batch rejects 16 false boundaries, including a p. 351 `Zaum` catchword, cross-references, German glosses misread as inverse headwords, grammatical prose and the letter-D explanatory paragraph. It makes **37 clear headword corrections**, reflecting the much heavier OCR degradation once the Rarámuri→German section begins. Corrected readings include `Wohin`, `Zuſchließen`, `Zwanzig`, `Ali oder ari`, `Baſſará`, `Bucú`, `Cachcánali`, `Caú`, `Cocotſchi`, `Corilícu`, `Cotſchimé`, `Echſámela` and `Echtſchiruc`.

Boundary review validates headword presence, article-start boundary, exact page placement and documentary direction. It does not constitute independent linguistic or philological validation.

## Deterministic review queue

`scripts/generate_review_queue.py` selects the first 100 unreviewed records in source order, exhausting `medium_machine` before entering `low_machine`, and excludes every persistent ID already represented in append-only review manifests. The generated projections make cohort selection reproducible; facsimile review still remains authoritative for exact page, column, direction and lemma reading.

## Page-layout reconstruction

Printed pages 301–368 remain modeled explicitly as 68 two-column dictionary pages. Printed p. 353 is a transition page: German→Rarámuri concludes above the section break and Rarámuri→German begins below it. `RHD-FR-015` demonstrates why both column geometry and section geometry must be retained in the editorial model.

## Diplomatic transcription

`RHD-DIP-001A`–`RHD-DIP-007A` provide complete AI-assisted diplomatic coverage for all **553 accepted starts in the exhausted `high_machine` tier**. Subsequent diplomatic series cover every accepted start in `RHD-FR-008` through `RHD-FR-015`.

For `RHD-FR-015`, `RHD-DIP-015A`–`RHD-DIP-015E` provide **84 complete article transcriptions** across printed pp. 350–356. `RHD-DIP-015B` explicitly spans the p. 353 direction change; later subbatches belong to the inverse Rarámuri→German section. Historical spelling and punctuation are preserved, while uncertain Rarámuri forms and morphological readings are flagged rather than normalized.

The cumulative diplomatic layer contains **1,184 complete AI-assisted article transcriptions**, exactly matching the **1,184 accepted starts among the 1,409 candidates reviewed to date**. The inventory records **509 records with an explicit uncertainty note**. All current diplomatic records remain `human_verified=false`.

## Next editorial stage

The next systematic stage is **`RHD-FR-016`**. Its deterministic queue contains the next 100 `medium_machine` candidates, from `RHD-S1809-01778` to `RHD-S1809-01988`, entirely within the Rarámuri→German section and estimated automatically around pp. 356–360. **310 `medium_machine` candidates remain unreviewed**, followed by 716 `low_machine` candidates. Global `full_diplomatic_transcription_completed` remains `false`.