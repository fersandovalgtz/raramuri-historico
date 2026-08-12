# Facsimile collation and diplomatic transcription status

Rarámuri Histórico Digital maintains three append-only boundary-review batches spanning both dictionary directions, plus a separate diplomatic-transcription layer. AI-assisted visual collation is always distinguished from independent human/philological and linguistic verification.

## Boundary-review results

| Batch | Machine candidates reviewed | Accepted article starts | Rejected false boundaries | Clear headword corrections | Printed-page span |
|---|---:|---:|---:|---:|---|
| `RHD-FR-001` | 100 | 86 | 14 | 4 | 301–317 |
| `RHD-FR-002` | 100 | 85 | 15 | 10 | 318–339 |
| `RHD-FR-003` | 100 | 89 | 11 | 33 | 339–357 |
| **Cumulative** | **300** | **260** | **40** | **47** | **301–357** |

The coverage-first machine layer remains 2,495 candidates. After the 40 visually rejected false boundaries, 2,455 candidates remain active provisionally. Candidate count is not asserted as the definitive number of printed lexicographic entries.

Boundary review validates headword presence, article-start boundary and exact page placement. It does not by itself validate a complete article body or linguistic interpretation.

A direct facsimile recheck during diplomatic completion corrected `RHD-S1809-01137` (`Schöpfen`) from printed p. 340 to printed p. 339 / PDF 49. The correction is stored in the review manifest rather than hidden in downstream exports.

## Page-layout reconstruction

Printed pages 301–357 are modeled explicitly as 57 two-column pages. Layout files `data/facsimile/page_layout_301_317.csv`, `data/facsimile/page_layout_318_339.csv` and `data/facsimile/page_layout_340_357.csv` preserve left/right reading order separately from OCR line order.

Printed p. 353 is a structural transition page: the German→Rarámuri dictionary concludes and the Rarámuri→German dictionary begins. `RHD-FR-003` therefore crosses dictionary direction while retaining persistent record IDs and exact facsimile page coordinates.

The supplied OCR does not consistently preserve the reading order of Steffel's two-column pages. Genuine headwords can inherit text from neighboring articles or columns, and OCR-derived page interpolation can drift locally. Exact page placement in reviewed records is consequently taken from the facsimile review overlay.

## Diplomatic transcription

`RHD-DIP-001A`–`RHD-DIP-001E` provide complete AI-assisted diplomatic transcriptions for all **86 accepted starts in RHD-FR-001**. `RHD-DIP-002A` and `RHD-DIP-002B` provide the same coverage for all **85 accepted starts in RHD-FR-002**.

`RHD-FR-003` is now also complete at the AI-assisted diplomatic level. `RHD-DIP-003A` adds 14 articles from p. 357; `RHD-DIP-003B` adds 23 from p. 356; `RHD-DIP-003C` adds 18 from p. 355; `RHD-DIP-003D` adds the 15 remaining German→Rarámuri articles on pp. 339, 340, 346 and 350; and `RHD-DIP-003E` adds the 19 remaining Rarámuri→German articles on pp. 353–356. The cumulative diplomatic layer therefore contains **260 complete AI-assisted article transcriptions**, exactly matching the 260 accepted starts among the first 300 reviewed candidates.

The previously deferred `Cuviruſi` cross-reference on p. 356 is transcribed as `Cuviruſi, ſ. Gries.`. The terminal cross-reference is difficult in the scan, so this resolution is explicitly documented as an inference supported by the visible facsimile string plus the internal German→Rarámuri `Gries` article, and remains pending independent human confirmation.

All current diplomatic records remain `human_verified=false`. Completion of the AI-assisted transcription layer must not be described as independent philological or linguistic verification.

## Next editorial stage

The first three boundary-review cohorts are internally complete at the AI-assisted diplomatic level: 300 candidates reviewed, 260 accepted starts, and 260 complete diplomatic overlays. The next systematic stage is `RHD-FR-004`: review the next unreviewed high-confidence candidates against the facsimile, extend page-layout coverage beyond p. 357 as necessary, reject false boundaries without recycling IDs, correct clear OCR headword errors, and then build the corresponding diplomatic transcription batches.
