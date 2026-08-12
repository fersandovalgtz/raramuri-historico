# Facsimile review

This directory stores append-only editorial review batches applied on top of the coverage-first OCR segmentation. Review batches preserve persistent record IDs: false-positive machine boundaries are rejected but never recycled, and accepted candidates remain explicitly distinct from human/philological verification.

## Exhausted high-confidence tier

`RHD-FR-001` through `RHD-FR-007` exhaust all **609 `high_machine` candidates**. Across those seven cohorts, 553 article starts were accepted, 56 false boundaries rejected and 298 clear headword corrections recorded. Every accepted high-confidence start has a complete AI-assisted diplomatic overlay.

## Medium-confidence review

`RHD-FR-008` reviews the first 100 `medium_machine` candidates on printed pp. 301–308: **72 accepted, 28 rejected and 9 corrections**. `RHD-FR-009` reviews the second 100 on printed pp. 308–315: **70 accepted, 30 rejected and 7 corrections**.

`RHD-FR-010` reviews the third 100 on printed pp. 315–322: **79 accepted, 21 rejected and 13 corrections**. `RHD-FR-011` reviews the fourth 100 on printed pp. 322–327: **81 accepted, 19 rejected and 5 corrections**.

`RHD-FR-012` reviews the fifth 100 `medium_machine` candidates in source order across printed pp. 328–338: **81 accepted article starts, 19 rejected false boundaries and 12 clear headword corrections**. Rejections include a page-bottom catchword, Rarámuri equivalents mis-segmented as German lemmas, cross-references, running prose inside long articles, page-header/column noise and OCR fragments. Clear corrected headwords include `Mager`, `Mantel`, `Matt`, `Meſſer`, `Niemals`, `Palmbaum`, `Papier`, `Pflug`, `Prieſter`, `Raubvogel`, `Raufen` and `Roſt`.

`RHD-DIP-012A`–`RHD-DIP-012D` provide complete diplomatic overlays for **all 81 accepted `RHD-FR-012` starts**. Long articles that cross columns or pages are reconstructed from the facsimile rather than from linear OCR order. The 2020 critical edition listed in `SOURCES.md` is used only as a secondary collation aid for difficult passages; the Steffel facsimile remains authoritative.

Cumulative status after `RHD-FR-012`: **1,109 candidates reviewed, 936 starts accepted, 173 false boundaries rejected, 344 clear headword corrections, 936 complete AI-assisted diplomatic articles and 2,322 active provisional candidates** out of the 2,495-candidate coverage layer.

The scope of review batches is headword presence, article-start boundary and exact page placement. Accepted records move to `facsimile_checked_headword_ai_assisted` unless a diplomatic overlay supersedes that status. Rejected IDs are retained with `rejected_false_positive`. Diplomatic overlays use `diplomatic_transcription_ai_assisted`. None of these statuses should be interpreted as independently verified or as human linguistic validation.

The machine inventory now contains **610 unreviewed `medium_machine` candidates** and 716 `low_machine` candidates. The next systematic review cohort is `RHD-FR-013`.
