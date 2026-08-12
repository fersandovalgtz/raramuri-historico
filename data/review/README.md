# Facsimile review

This directory stores append-only editorial review batches applied on top of the coverage-first OCR segmentation. Review batches preserve persistent record IDs: false-positive machine boundaries are rejected but never recycled, and accepted candidates remain explicitly distinct from human/philological verification.

## Exhausted high-confidence tier

`RHD-FR-001` through `RHD-FR-007` exhaust all **609 `high_machine` candidates**. Across those seven cohorts, 553 article starts were accepted, 56 false boundaries rejected and 298 clear headword corrections recorded. Every accepted high-confidence start has a complete AI-assisted diplomatic overlay.

The final high-confidence cohort also corrected an OCR page drift at the end of the dictionary: several candidates assigned mechanically to p. 369 actually occur on printed p. 368, while p. 369 begins the appendix.

## Medium-confidence review

`RHD-FR-008` opens the systematic `medium_machine` tier with its first 100 candidates in source order, on printed pp. 301–308 of the German→Rarámuri dictionary. Direct facsimile collation accepts **72 article starts**, rejects **28 false boundaries** and records **10 clear headword corrections**.

The higher false-positive rate is methodologically informative. Rejections include wrapped Rarámuri equivalents, repeated forms inside long articles, German running prose, OCR fragments and page-transition carry-over. Examples include `Hulirúgameke` inside `Abſchicken`, `Graſe bedecket` inside `Aloe`, `Reductionen ein` and `Piſtolen` inside `Apatſche`, prose fragments inside `Baden`, `Backſtube` and `Bär`, and `Iki` inside `Beißen`.

`RHD-DIP-008A`–`RHD-DIP-008D` currently provide complete diplomatic text for **66 of the 72 accepted `RHD-FR-008` starts**. Six long articles are intentionally deferred for separate complete reconstruction: `Aloe`, `Apatſche`, `Baden`, `Backſtube`, `Bär` and `Beſitzen`.

Cumulative status after `RHD-FR-008`: **709 candidates reviewed, 625 starts accepted, 84 false boundaries rejected, 308 clear headword corrections, 619 complete AI-assisted diplomatic articles and 2,411 active provisional candidates** out of the 2,495-candidate coverage layer.

The scope of review batches is headword presence, article-start boundary and exact page placement. Accepted records move to `facsimile_checked_headword_ai_assisted` unless a diplomatic overlay supersedes that status. Rejected IDs are retained with `rejected_false_positive`. Diplomatic overlays use `diplomatic_transcription_ai_assisted`. None of these statuses should be interpreted as `diplomatic_verified` or as human linguistic validation.

The machine inventory still contains 1,010 unreviewed `medium_machine` candidates and 716 `low_machine` candidates. The next conservative step is to finish the six deferred long articles before opening another medium-confidence review cohort.
