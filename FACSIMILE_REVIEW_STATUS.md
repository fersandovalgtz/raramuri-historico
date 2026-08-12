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

Printed pages 301–339 are now modeled explicitly as 39 two-column pages. Layout files `data/facsimile/page_layout_301_317.csv` and `data/facsimile/page_layout_318_339.csv` preserve left/right reading order separately from OCR line order.

This addresses a central methodological finding: the supplied OCR does not consistently preserve the reading order of Steffel's two-column pages. Genuine headwords can therefore inherit text from neighboring articles or columns, and OCR-derived page interpolation can drift locally. Exact page placement in reviewed records is consequently taken from the facsimile review overlay.

## Diplomatic transcription

The first boundary batch has been taken through article-text reconstruction. `RHD-DIP-001A`–`RHD-DIP-001E` provide complete AI-assisted diplomatic transcriptions for all **86 accepted starts in RHD-FR-001**. Source spelling and punctuation are retained; typographic line wrapping is generally not encoded. Twenty-seven of those records carry an explicit uncertainty note.

All current diplomatic records remain `human_verified=false`. Completion of the AI-assisted transcription layer must not be described as independent philological or linguistic verification.

`RHD-FR-002` has completed its boundary/page review: **85 accepted starts are now ready for page-layout-based diplomatic reconstruction**. The next editorial stage is to transcribe those accepted articles conservatively, beginning with short, clearly bounded entries, before moving to further boundary-review batches.
