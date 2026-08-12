# Facsimile review

This directory stores append-only editorial review batches applied on top of the coverage-first OCR segmentation. Review batches preserve persistent record IDs: false-positive machine boundaries are rejected but never recycled, and accepted candidates remain explicitly distinct from human/philological verification.

## Reviewed cohorts

`RHD-FR-001` reviews the first 100 `high_machine` candidates on printed pp. 301–317: 86 accepted starts, 14 rejected false boundaries and 4 clear headword corrections. All accepted starts are covered by `RHD-DIP-001A`–`RHD-DIP-001E`.

`RHD-FR-002` reviews the next 100 candidates on pp. 318–339: 85 accepted, 15 rejected and 10 corrections. All accepted starts are covered by `RHD-DIP-002A`–`RHD-DIP-002B`.

`RHD-FR-003` reviews the next 100 and crosses the German→Rarámuri / Rarámuri→German transition on p. 353: 89 accepted, 11 rejected and 33 corrections. All accepted starts are covered by `RHD-DIP-003A`–`RHD-DIP-003E`.

`RHD-FR-004` reviews the fourth 100, wholly in the Rarámuri→German dictionary on pp. 357–361: 90 accepted, 10 rejected and 62 corrections. All accepted starts are covered by `RHD-DIP-004A`–`RHD-DIP-004E`.

`RHD-FR-005` reviews the fifth 100, also wholly Rarámuri→German, spanning the end of p. 361 through p. 365: 96 accepted, 4 rejected and 90 corrections. The rejected candidates are inter-page/header noise, a German gloss continuing a preceding article, Q-section explanatory prose and a page-foot catchword rather than an article start. All 96 accepted starts are covered by `RHD-DIP-005A`–`RHD-DIP-005F`.

Cumulative status after five review batches: **500 candidates reviewed, 446 starts accepted, 54 false boundaries rejected, 199 clear headword corrections, 446 complete AI-assisted diplomatic articles and 2,441 active provisional candidates** out of the 2,495-candidate coverage layer.

The scope of review batches is headword presence, article-start boundary and exact page placement. Accepted records move to `facsimile_checked_headword_ai_assisted` unless a diplomatic overlay supersedes that status. Rejected IDs are retained with `rejected_false_positive`. Diplomatic overlays use `diplomatic_transcription_ai_assisted`. None of these statuses should be interpreted as `diplomatic_verified` or as human linguistic validation.
