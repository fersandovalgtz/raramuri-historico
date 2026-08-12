# Facsimile collation and diplomatic transcription status

Rarámuri Histórico Digital maintains four append-only boundary-review batches spanning both dictionary directions, plus a separate diplomatic-transcription layer. AI-assisted visual collation is always distinguished from independent human/philological and linguistic verification.

## Boundary-review results

| Batch | Machine candidates reviewed | Accepted article starts | Rejected false boundaries | Clear headword corrections | Printed-page span |
|---|---:|---:|---:|---:|---|
| `RHD-FR-001` | 100 | 86 | 14 | 4 | 301–317 |
| `RHD-FR-002` | 100 | 85 | 15 | 10 | 318–339 |
| `RHD-FR-003` | 100 | 89 | 11 | 33 | 339–357 |
| `RHD-FR-004` | 100 | 90 | 10 | 62 | 357–361 |
| **Cumulative** | **400** | **350** | **50** | **109** | **301–361** |

The coverage-first machine layer remains 2,495 candidates. After the 50 visually rejected false boundaries, 2,445 candidates remain active provisionally. Candidate count is not asserted as the definitive number of printed lexicographic entries.

Boundary review validates headword presence, article-start boundary and exact page placement. It does not by itself validate a complete article body or linguistic interpretation.

Direct facsimile review continues to correct local OCR page interpolation. `RHD-FR-004` established that several late G/H candidates mechanically assigned to p. 358 begin on p. 357, late H/I material assigned to p. 359 occurs on p. 358, the J/K block assigned to p. 360 occurs on p. 359, several M entries assigned to p. 360 occur on p. 361, and the final reviewed `Mutſcha` candidate assigned mechanically to p. 362 actually begins on p. 361. These corrections are stored in the review manifest rather than hidden in downstream exports.

## Page-layout reconstruction

Printed pages 301–361 are modeled explicitly as 61 two-column pages. Layout files `data/facsimile/page_layout_301_317.csv`, `data/facsimile/page_layout_318_339.csv`, `data/facsimile/page_layout_340_357.csv` and `data/facsimile/page_layout_358_361.csv` preserve left/right reading order separately from OCR line order.

Printed p. 353 is a structural transition page: the German→Rarámuri dictionary concludes and the Rarámuri→German dictionary begins. `RHD-FR-004` lies wholly in the Rarámuri→German dictionary.

The supplied OCR does not consistently preserve the reading order of Steffel's two-column pages. Genuine headwords can inherit text from neighboring articles or columns, and OCR-derived page interpolation can drift locally. Exact page placement in reviewed records is consequently taken from the facsimile review overlay.

## Diplomatic transcription

`RHD-DIP-001A`–`RHD-DIP-001E` provide complete AI-assisted diplomatic transcriptions for all **86 accepted starts in RHD-FR-001**. `RHD-DIP-002A` and `RHD-DIP-002B` provide the same coverage for all **85 accepted starts in RHD-FR-002**. `RHD-DIP-003A`–`RHD-DIP-003E` provide complete coverage for all **89 accepted starts in RHD-FR-003**.

`RHD-FR-004` is also complete at the AI-assisted diplomatic level. `RHD-DIP-004A` adds 13 articles from p. 357; `RHD-DIP-004B` adds 27 from p. 358; `RHD-DIP-004C` adds 29 from p. 359; `RHD-DIP-004D` adds 2 from p. 360; and `RHD-DIP-004E` adds 19 from p. 361. The cumulative diplomatic layer therefore contains **350 complete AI-assisted article transcriptions**, exactly matching the 350 accepted starts among the first 400 reviewed high-confidence candidates.

`RHD-FR-004` also rejects ten machine boundaries that proved to be running prose, German glosses, grammatical examples or OCR noise. Examples include `Geſchlecht anzudeuten` and `Cambalátſchi hoguila` inside the `Hoguila` article, `Hohl` inside `Hóuke`, `Stempel` inside `Muliki`, and `Menſch` inside the grammatical example in `Mumugi`. Persistent IDs are retained and never recycled.

All current diplomatic records remain `human_verified=false`. Completion of the AI-assisted transcription layer must not be described as independent philological or linguistic verification.

## Next editorial stage

The first four boundary-review cohorts are internally complete at the AI-assisted diplomatic level: 400 candidates reviewed, 350 accepted starts, and 350 complete diplomatic overlays. The next systematic stage is `RHD-FR-005`: review the next unreviewed high-confidence candidates against the facsimile, extend page-layout coverage beyond p. 361 as necessary, reject false boundaries without recycling IDs, correct clear OCR headword errors, and then build the corresponding diplomatic transcription batches.
