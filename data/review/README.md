# Facsimile review

This directory stores append-only editorial review batches applied on top of the coverage-first OCR segmentation. Review batches preserve persistent record IDs: false-positive machine boundaries are rejected but never recycled, and accepted candidates remain explicitly distinct from human/philological verification.

## Exhausted high-confidence tier

`RHD-FR-001` through `RHD-FR-007` exhaust all **609 `high_machine` candidates**. Across those seven cohorts, 553 article starts were accepted, 56 false boundaries rejected and 298 clear headword corrections recorded. Every accepted high-confidence start has a complete AI-assisted diplomatic overlay.

## Medium-confidence review

`RHD-FR-008` reviews the first 100 `medium_machine` candidates on printed pp. 301–308: **72 accepted, 28 rejected and 9 corrections**. `RHD-FR-009` reviews the second 100 on printed pp. 308–315: **70 accepted, 30 rejected and 7 corrections**. Both cohorts have complete AI-assisted diplomatic coverage.

`RHD-FR-010` reviews the third 100 `medium_machine` candidates in source order on printed pp. 315–322: **79 accepted, 21 rejected and 13 corrections**. Its accepted starts all have complete AI-assisted diplomatic overlays in `RHD-DIP-010A`–`RHD-DIP-010D`.

`RHD-FR-011` reviews the fourth 100 `medium_machine` candidates in source order on printed pp. 322–327: **81 accepted article starts, 19 rejected false boundaries and 5 clear headword corrections**. The rejected candidates include cross-references, Rarámuri equivalents, OCR fragments and running prose inside longer articles. The five corrected headwords are `Harnen`, `Hochzeit`, `Hohl`, `Jemand` and `Kamiſol`; the latter corrects an OCR confusion of long `ſ` with `f`.

`RHD-DIP-011A`–`RHD-DIP-011C` transcribe 72 accepted short/medium articles; `RHD-DIP-011D` completes the nine longer articles `Gras`, `Gries`, `Hart`, `Herr`, `Hinaus`, `Ja`, `Jahr`, `Kochen` and `Kranich`. Thus **all 81 accepted `RHD-FR-011` starts have complete AI-assisted diplomatic overlays**.

Cumulative status after `RHD-FR-011`: **1,009 candidates reviewed, 855 starts accepted, 154 false boundaries rejected, 332 clear headword corrections, 855 complete AI-assisted diplomatic articles and 2,341 active provisional candidates** out of the 2,495-candidate coverage layer.

The scope of review batches is headword presence, article-start boundary and exact page placement. Accepted records move to `facsimile_checked_headword_ai_assisted` unless a diplomatic overlay supersedes that status. Rejected IDs are retained with `rejected_false_positive`. Diplomatic overlays use `diplomatic_transcription_ai_assisted`. None of these statuses should be interpreted as independently verified or as human linguistic validation.

The machine inventory now contains **710 unreviewed `medium_machine` candidates** and 716 `low_machine` candidates. The next systematic review cohort is `RHD-FR-012`.
