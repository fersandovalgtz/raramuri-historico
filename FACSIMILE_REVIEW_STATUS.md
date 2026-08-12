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

`RHD-DIP-003A` starts the diplomatic reconstruction of `RHD-FR-003` with **14 complete articles from printed p. 357**, in the Rarámuri→German section. The cumulative diplomatic layer therefore contains **185 complete AI-assisted article transcriptions**. Seventy-four records carry an explicit uncertainty note. Source spelling and punctuation are retained; typographic line wrapping is generally not encoded.

All current diplomatic records remain `human_verified=false`. Completion of the AI-assisted transcription layer must not be described as independent philological or linguistic verification.

## Next editorial stage

`RHD-FR-003` has **75 accepted starts still awaiting diplomatic reconstruction**. The next stage is to continue backwards through the dense inverse-dictionary pages 356 and 355, then resolve the remaining accepted German→Rarámuri articles on pp. 340–352, preserving explicit uncertainty wherever the facsimile does not support a confident reading.
