# Facsimile review

This directory stores append-only editorial review batches applied on top of the coverage-first OCR segmentation. Review batches preserve persistent record IDs: false-positive machine boundaries are rejected but never recycled, and accepted candidates remain explicitly distinct from human/philological verification.

## Reviewed cohorts

`RHD-FR-001` reviews the first 100 `high_machine` candidates on printed pp. 301–317: 86 accepted starts, 14 rejected false boundaries and 4 clear headword corrections. All accepted starts are covered by `RHD-DIP-001A`–`RHD-DIP-001E`.

`RHD-FR-002` reviews the next 100 candidates on pp. 318–339: 85 accepted, 15 rejected and 10 corrections. All accepted starts are covered by `RHD-DIP-002A`–`RHD-DIP-002B`.

`RHD-FR-003` reviews the next 100 and crosses the German→Rarámuri / Rarámuri→German transition on p. 353: 89 accepted, 11 rejected and 33 corrections. All accepted starts are covered by `RHD-DIP-003A`–`RHD-DIP-003E`.

`RHD-FR-004` reviews the fourth 100, wholly in the Rarámuri→German dictionary on pp. 357–361: 90 accepted, 10 rejected and 62 corrections. All accepted starts are covered by `RHD-DIP-004A`–`RHD-DIP-004E`.

`RHD-FR-005` reviews the fifth 100 on pp. 361–365: 96 accepted, 4 rejected and 90 corrections. All accepted starts are covered by `RHD-DIP-005A`–`RHD-DIP-005F`.

`RHD-FR-006` reviews the sixth 100, wholly Rarámuri→German, on pp. 365–368: 98 accepted, 2 rejected and 91 clear headword corrections. The rejected candidates are German gloss fragments (`Hinweg`, `Immer`) rather than Rarámuri article starts. The review also restores genuine headwords lost by linear OCR, such as `Tápoa`. All 98 accepted starts are covered by `RHD-DIP-006A`–`RHD-DIP-006D`.

Cumulative status after six review batches: **600 candidates reviewed, 544 starts accepted, 56 false boundaries rejected, 290 clear headword corrections, 544 complete AI-assisted diplomatic articles and 2,439 active provisional candidates** out of the 2,495-candidate coverage layer.

The scope of review batches is headword presence, article-start boundary and exact page placement. Accepted records move to `facsimile_checked_headword_ai_assisted` unless a diplomatic overlay supersedes that status. Rejected IDs are retained with `rejected_false_positive`. Diplomatic overlays use `diplomatic_transcription_ai_assisted`. None of these statuses should be interpreted as `diplomatic_verified` or as human linguistic validation.

The machine segmentation contains 609 `high_machine` candidates in total. After `RHD-FR-006`, nine remain for the final small high-confidence cohort `RHD-FR-007`.
