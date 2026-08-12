# Facsimile review

This directory stores append-only editorial review batches applied on top of the coverage-first OCR segmentation. Review batches preserve persistent record IDs: false-positive machine boundaries are rejected but never recycled, and accepted candidates remain explicitly distinct from human/philological verification.

## Exhausted high-confidence tier

`RHD-FR-001` through `RHD-FR-007` exhaust all **609 `high_machine` candidates**. Across those seven cohorts, 553 article starts were accepted, 56 false boundaries rejected and 298 clear headword corrections recorded. Every accepted high-confidence start has a complete AI-assisted diplomatic overlay.

## Medium-confidence review

`RHD-FR-008` reviews the first 100 `medium_machine` candidates on printed pp. 301–308: **72 accepted, 28 rejected and 9 corrections**. `RHD-DIP-008A`–`RHD-DIP-008E` provide complete diplomatic coverage for all 72 accepted starts, including the long articles `Aloe`, `Apatſchee`, `Baden`, `Backſtube`, `Bär` and `Beſitzen`.

`RHD-FR-009` reviews the second 100 `medium_machine` candidates. Direct facsimile collation places them on printed pp. 308–315 and yields **70 accepted starts, 30 rejected false boundaries and 7 clear headword corrections**. Rejections again include wrapped Rarámuri equivalents and running prose inside long entries such as `Beſitzen`, `Bock`, `Brod`, `Da`, `Dieb` and `Ente`. The manifest also corrects local OCR page interpolation: `Bley`–`Blitzen` belong to p. 309, while `Einbilden, ſich`, `Eingebohrner` and `Eingedenk ſeyn` belong to p. 313.

`RHD-DIP-009A`–`RHD-DIP-009E` cover 65 short accepted articles. `RHD-DIP-009F` completes the five longer records `Da`, `Dieb`, `Dorfrichter`, `Dürfen` and `Ente`. Thus **all 70 accepted `RHD-FR-009` starts have complete AI-assisted diplomatic overlays**.

Cumulative status after `RHD-FR-009`: **809 candidates reviewed, 695 starts accepted, 114 false boundaries rejected, 314 clear headword corrections, 695 complete AI-assisted diplomatic articles and 2,381 active provisional candidates** out of the 2,495-candidate coverage layer.

The scope of review batches is headword presence, article-start boundary and exact page placement. Accepted records move to `facsimile_checked_headword_ai_assisted` unless a diplomatic overlay supersedes that status. Rejected IDs are retained with `rejected_false_positive`. Diplomatic overlays use `diplomatic_transcription_ai_assisted`. None of these statuses should be interpreted as independently verified or as human linguistic validation.

The machine inventory now contains **910 unreviewed `medium_machine` candidates** and 716 `low_machine` candidates. The next systematic review cohort is `RHD-FR-010`.
