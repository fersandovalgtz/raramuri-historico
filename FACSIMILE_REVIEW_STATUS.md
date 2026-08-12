# Facsimile collation and diplomatic transcription status

Rarámuri Histórico Digital maintains sixteen append-only boundary-review batches spanning both dictionary directions and two machine-confidence tiers, plus a separate diplomatic-transcription layer. AI-assisted visual collation is always distinguished from independent human/philological and linguistic verification.

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
| `RHD-FR-008` | 100 | 72 | 28 | 9 | 301–308 |
| `RHD-FR-009` | 100 | 70 | 30 | 7 | 308–315 |
| `RHD-FR-010` | 100 | 79 | 21 | 13 | 315–322 |
| `RHD-FR-011` | 100 | 81 | 19 | 5 | 322–327 |
| `RHD-FR-012` | 100 | 81 | 19 | 12 | 328–338 |
| `RHD-FR-013` | 100 | 83 | 17 | 9 | 338–344 |
| `RHD-FR-014` | 100 | 81 | 19 | 6 | 345–350 |
| `RHD-FR-015` | 100 | 84 | 16 | 37 | 350–356 |
| `RHD-FR-016` | 100 | 90 | 10 | 87 | 356–360 |
| **Cumulative reviewed corpus** | **1,509** | **1,274** | **235** | **483** | **301–368** |

The coverage-first machine layer remains 2,495 candidates. All 609 `high_machine` candidates have been resolved. The first **900 of 1,110 `medium_machine` candidates** have also been reviewed: **721 accepted starts and 179 false boundaries**. Rejected IDs remain persistent and are never recycled, leaving **2,260 active provisional candidates**.

`RHD-FR-016` is wholly within the Rarámuri→German section. It resolves 100 candidates across printed pp. **356–360**, accepting 90 and rejecting 10 German glosses, cross-references or fragments of explanatory prose. The inverse section exhibits severe OCR degradation: **87 of the 90 accepted starts require a clear headword correction**, and **32 candidate page assignments are corrected by direct facsimile collation**.

Representative recovered forms include `Etschaguóameke`, `Ekítschipí`, `Galá tá símega`, `Guarátscha`, `Guechtschíc`, `Haleséatschic, oder Hareséatschic`, `Jachcála`, `Jumánamatschígameke`, `Kauguáca`, `Kuepútsela, oder Kepútschela` and `Kubírusi, oder Gubírusi`. The Steffel facsimile remains authoritative; the Merrill et al. 2020 transcription is used only as a secondary collation aid for difficult glyphs and diacritics.

Boundary review validates headword presence, article-start boundary, exact page placement and documentary direction. It does not constitute independent linguistic or philological validation.

## Deterministic review queue

`scripts/generate_review_queue.py` selects the first 100 unreviewed records in source order, exhausting `medium_machine` before entering `low_machine`, and excludes every persistent ID already represented in append-only review manifests. Facsimile review remains authoritative for exact page, column, direction and lemma reading.

## Page-layout reconstruction

Printed pages 301–368 remain modeled explicitly as 68 two-column dictionary pages. Printed p. 353 is a transition page: German→Rarámuri concludes above the section break and Rarámuri→German begins below it. `RHD-FR-016` further demonstrates that OCR-derived page assignment in the inverse section can drift across page boundaries and therefore must remain an editorial overlay rather than source truth.

## Diplomatic transcription

`RHD-DIP-001A`–`RHD-DIP-007A` provide complete AI-assisted diplomatic coverage for all **553 accepted starts in the exhausted `high_machine` tier**. Subsequent diplomatic series cover every accepted start in `RHD-FR-008` through `RHD-FR-016`.

For `RHD-FR-016`, `RHD-DIP-016A`–`RHD-DIP-016I` provide **90 complete article transcriptions** across pp. 356–360. Two records in this new series carry explicit uncertainty notes for a long place-name article and a difficult variant-form pair.

The cumulative diplomatic layer contains **1,274 complete AI-assisted article transcriptions**, exactly matching the **1,274 accepted starts among the 1,509 candidates reviewed to date**. The inventory records **511 records with an explicit uncertainty note**. All current diplomatic records remain `human_verified=false`.

## Next editorial stage

The next systematic stage is **`RHD-FR-017`**. Its deterministic queue contains the next 100 `medium_machine` candidates, from `RHD-S1809-01989` (`Lala`) through `RHD-S1809-02233` (`Rnsra`), entirely within Rarámuri→German and automatically estimated around printed pp. **360–365**. **210 `medium_machine` candidates remain unreviewed**, followed by 716 `low_machine` candidates. Global `full_diplomatic_transcription_completed` remains `false`.