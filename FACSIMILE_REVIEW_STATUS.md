# Facsimile collation and diplomatic transcription status

Rarámuri Histórico Digital now maintains three append-only boundary-review batches spanning both dictionary directions, plus a separate diplomatic-transcription layer. AI-assisted visual collation is always distinguished from independent human/philological and linguistic verification.

## Boundary-review results

| Batch | Machine candidates reviewed | Accepted article starts | Rejected false boundaries | Clear headword corrections | Printed-page span |
|---|---:|---:|---:|---:|---|
| `RHD-FR-001` | 100 | 86 | 14 | 4 | 301–317 |
| `RHD-FR-002` | 100 | 85 | 15 | 10 | 318–339 |
| `RHD-FR-003` | 100 | 89 | 11 | 33 | 340–357 |
| **Cumulative** | **300** | **260** | **40** | **47** | **301–357** |

The coverage-first machine layer remains 2,495 candidates. After the 40 visually rejected false boundaries, 2,455 candidates remain active provisionally. Candidate count is not asserted as the definitive number of printed lexicographic entries.

Boundary review validates headword presence, article-start boundary and exact page placement. It does not by itself validate a complete article body or linguistic interpretation.

## Page-layout reconstruction

Printed pages 301–357 are modeled explicitly as 57 two-column pages. Layout files `data/facsimile/page_layout_301_317.csv`, `data/facsimile/page_layout_318_339.csv` and `data/facsimile/page_layout_340_357.csv` preserve left/right reading order separately from OCR line order.

Printed p. 353 is a structural transition page: the German→Rarámuri dictionary concludes and the Rarámuri→German dictionary begins. `RHD-FR-003` therefore crosses dictionary direction while retaining persistent record IDs and exact facsimile page coordinates.

The supplied OCR does not consistently preserve the reading order of Steffel's two-column pages. Genuine headwords can inherit text from neighboring articles or columns, and OCR-derived page interpolation can drift locally. Exact page placement in reviewed records is consequently taken from the facsimile review overlay.

## Diplomatic transcription

`RHD-DIP-001A`–`RHD-DIP-001E` provide complete AI-assisted diplomatic transcriptions for all **86 accepted starts in RHD-FR-001**. `RHD-DIP-002A` and `RHD-DIP-002B` provide the same coverage for all **85 accepted starts in RHD-FR-002**.

Within `RHD-FR-003`, `RHD-DIP-003A` adds 14 complete articles from printed p. 357, `RHD-DIP-003B` adds 23 clearly bounded articles from p. 356, and `RHD-DIP-003C` adds 18 from p. 355. One accepted p. 356 record (`Cuviruſi`) remains deliberately deferred because its printed cross-reference is visually truncated/ambiguous. The cumulative diplomatic layer now contains **226 complete AI-assisted article transcriptions**. Ninety-eight records carry an explicit uncertainty note.

All current diplomatic records remain `human_verified=false`. Completion of the AI-assisted transcription layer must not be described as independent philological or linguistic verification.

## Next editorial stage

`RHD-FR-003` has **34 accepted starts still awaiting diplomatic reconstruction**. The next stage is to resolve the remaining inverse-dictionary material on pp. 353–354 and the deferred p. 356 record conservatively, then transcribe the accepted German→Rarámuri articles on pp. 340–352. Structurally questionable candidates are not promoted merely to increase coverage.
