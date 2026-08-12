# Facsimile review

This directory stores append-only editorial review batches applied on top of the coverage-first OCR segmentation. Review batches preserve persistent record IDs: false-positive machine boundaries are rejected but never recycled, and accepted candidates remain explicitly distinct from human/philological verification.

## Exhausted high-confidence tier

`RHD-FR-001` through `RHD-FR-007` exhaust all **609 `high_machine` candidates**. Across those seven cohorts, 553 article starts were accepted, 56 false boundaries rejected and 298 clear headword corrections recorded. Every accepted high-confidence start has a complete AI-assisted diplomatic overlay.

## Medium-confidence review

`RHD-FR-008` reviews the first 100 `medium_machine` candidates on printed pp. 301–308: **72 accepted, 28 rejected and 9 corrections**. `RHD-FR-009` reviews the second 100 on printed pp. 308–315: **70 accepted, 30 rejected and 7 corrections**. Both cohorts have complete AI-assisted diplomatic coverage.

`RHD-FR-010` reviews the third 100 `medium_machine` candidates in source order, directly collated on printed pp. 315–322. It yields **79 accepted article starts, 21 rejected false boundaries and 13 clear headword corrections**. Rejections include cross-references such as `Aufwecken`, Rarámuri equivalents such as `Sami`, the page catchword `Eule`, OCR fragments and running prose inside long entries including `Feige indianiſche`, `Fiſchen`, `Fliege`, `Gebirg` and `Getränk`.

`RHD-DIP-010A`–`RHD-DIP-010C` transcribe 75 accepted short/medium articles; `RHD-DIP-010D` completes the four longer articles `Feige indianiſche`, `Fragen`, `Geige` and `Getränk`. Thus **all 79 accepted `RHD-FR-010` starts have complete AI-assisted diplomatic overlays**.

Cumulative status after `RHD-FR-010`: **909 candidates reviewed, 774 starts accepted, 135 false boundaries rejected, 327 clear headword corrections, 774 complete AI-assisted diplomatic articles and 2,360 active provisional candidates** out of the 2,495-candidate coverage layer.

The scope of review batches is headword presence, article-start boundary and exact page placement. Accepted records move to `facsimile_checked_headword_ai_assisted` unless a diplomatic overlay supersedes that status. Rejected IDs are retained with `rejected_false_positive`. Diplomatic overlays use `diplomatic_transcription_ai_assisted`. None of these statuses should be interpreted as independently verified or as human linguistic validation.

The machine inventory now contains **810 unreviewed `medium_machine` candidates** and 716 `low_machine` candidates. The next systematic review cohort is `RHD-FR-011`.
