# Facsimile review

This directory stores append-only editorial review batches applied on top of the coverage-first OCR segmentation. Review batches preserve persistent record IDs: false-positive machine boundaries are rejected but never recycled, and accepted candidates remain explicitly distinct from human/philological verification.

## Exhausted high-confidence tier

`RHD-FR-001` through `RHD-FR-007` exhaust all **609 `high_machine` candidates**. Across those seven cohorts, 553 article starts were accepted, 56 false boundaries rejected and 298 clear headword corrections recorded. Every accepted high-confidence start has a complete AI-assisted diplomatic overlay.

## Medium-confidence review

`RHD-FR-008` reviews the first 100 `medium_machine` candidates on printed pp. 301–308: **72 accepted, 28 rejected and 9 corrections**. `RHD-FR-009` reviews the second 100 on printed pp. 308–315: **70 accepted, 30 rejected and 7 corrections**.

`RHD-FR-010` reviews the third 100 on printed pp. 315–322: **79 accepted, 21 rejected and 13 corrections**. `RHD-FR-011` reviews the fourth 100 on printed pp. 322–327: **81 accepted, 19 rejected and 5 corrections**.

`RHD-FR-012` reviews the fifth 100 `medium_machine` candidates in source order across printed pp. 328–338: **81 accepted article starts, 19 rejected false boundaries and 12 clear headword corrections**.

`RHD-FR-013` reviews the sixth 100 `medium_machine` candidates in deterministic source order across printed pp. 338–344: **83 accepted article starts, 17 rejected false boundaries and 9 clear headword corrections**. Rejections include Rarámuri forms mistaken for German lemmas, the `Sollen` page-bottom catchword, cross-reference continuations and fragments of explanatory prose embedded in `Seitenſtechen`, `Spiel`, `Spielplatz` and `Staar`. The nine corrected headwords are `Schaf`, `Trinkſchale`, `Schalf`, `Schlüſſel`, `Schwißſtube`, `Selbſt`, `Singen`, `Spielplatz` and `Steigen`.

`RHD-DIP-013A`–`RHD-DIP-013E` provide complete diplomatic overlays for **all 83 accepted `RHD-FR-013` starts**. Long records such as `Spiel`, `Spielplatz`, `Staar`, `Stein`, `Sterben` and `Sterblich` are reconstructed from documentary column/page order rather than linear OCR. Ambiguous readings are flagged instead of silently normalized.

Cumulative status after `RHD-FR-013`: **1,209 candidates reviewed, 1,019 starts accepted, 190 false boundaries rejected, 353 clear headword corrections, 1,019 complete AI-assisted diplomatic articles and 2,305 active provisional candidates** out of the 2,495-candidate coverage layer.

The scope of review batches is headword presence, article-start boundary and exact page placement. Accepted records move to `facsimile_checked_headword_ai_assisted` unless a diplomatic overlay supersedes that status. Rejected IDs are retained with `rejected_false_positive`. Diplomatic overlays use `diplomatic_transcription_ai_assisted`. None of these statuses should be interpreted as independently verified or as human linguistic validation.

## Deterministic next cohort

`scripts/generate_review_queue.py` generates `next_review_queue.json` and `next_review_queue_compact.json` from the regenerated coverage layer plus all append-only review manifests. It selects the first 100 unreviewed records in source order, exhausting `medium_machine` before `low_machine`; this prevents manual cohort drift or identifier reuse.

The machine inventory now contains **510 unreviewed `medium_machine` candidates** and 716 `low_machine` candidates. The next systematic review cohort is `RHD-FR-014`.
