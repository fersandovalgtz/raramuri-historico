# Facsimile collation and diplomatic transcription status

Rarámuri Histórico Digital now maintains two append-only boundary-review batches over the German→Rarámuri dictionary and a separate diplomatic-transcription layer. AI-assisted visual collation is always distinguished from independent human/philological and linguistic verification.

## Boundary-review results

| Batch | Machine candidates reviewed | Accepted article starts | Rejected false boundaries | Clear headword corrections | Printed-page span |
|---|---:|---:|---:|---:|---|
| `RHD-FR-001` | 100 | 86 | 14 | 4 | 301–317 |
| `RHD-FR-002` | 100 | 85 | 15 | 10 | 318–339 |
| **Cumulative** | **200** | **171** | **29** | **14** | **301–339** |

The coverage-first machine layer remains 2,495 candidates. After the 29 visually rejected false boundaries, 2,466 candidates remain active provisionally. Candidate count is not asserted as the definitive number of printed lexicographic entries.

Boundary review validates headword presence, article-start boundary and exact page placement. It does not by itself validate a complete article body or linguistic interpretation.

## Page-layout reconstruction

Printed pages 301–339 are modeled explicitly as 39 two-column pages. Layout files `data/facsimile/page_layout_301_317.csv` and `data/facsimile/page_layout_318_339.csv` preserve left/right reading order separately from OCR line order.

This addresses a central methodological finding: the supplied OCR does not consistently preserve the reading order of Steffel's two-column pages. Genuine headwords can therefore inherit text from neighboring articles or columns, and OCR-derived page interpolation can drift locally. Exact page placement in reviewed records is consequently taken from the facsimile review overlay.

## Diplomatic transcription

`RHD-DIP-001A`–`RHD-DIP-001E` provide complete AI-assisted diplomatic transcriptions for all **86 accepted starts in RHD-FR-001**. `RHD-DIP-002A` and `RHD-DIP-002B` now provide the same coverage for all **85 accepted starts in RHD-FR-002**.

The cumulative diplomatic layer therefore contains **171 complete AI-assisted article transcriptions**, exactly matching the 171 accepted boundaries among the first 200 reviewed candidates. Sixty-seven records carry an explicit uncertainty note. Source spelling and punctuation are retained; typographic line wrapping is generally not encoded. Long entries such as `Gebirg` and `Kukuck` were reconstructed from the facsimile across column/page boundaries rather than from linear OCR order.

All current diplomatic records remain `human_verified=false`. Completion of the AI-assisted transcription layer must not be described as independent philological or linguistic verification.

## Next editorial stage

The first two boundary-review cohorts are now internally complete at the AI-assisted diplomatic level. The next systematic stage is `RHD-FR-003`: review the next 100 unreviewed `high_machine` candidates against the facsimile, extend explicit page-layout coverage where needed, reject false boundaries without recycling IDs, correct clear OCR headword errors, and then build the corresponding diplomatic transcription batch.
