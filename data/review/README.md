# Facsimile review

This directory stores append-only editorial review batches applied on top of the coverage-first OCR segmentation. Review batches preserve persistent record IDs: false-positive machine boundaries are rejected but never recycled, and accepted candidates remain explicitly distinct from human/philological verification.

## Reviewed high-confidence cohorts

`RHD-FR-001` reviews the first 100 `high_machine` candidates on printed pp. 301–317: 86 accepted starts, 14 rejected false boundaries and 4 clear headword corrections.

`RHD-FR-002` reviews the next 100 on pp. 318–339: 85 accepted, 15 rejected and 10 corrections.

`RHD-FR-003` reviews the next 100 and crosses the German→Rarámuri / Rarámuri→German transition on p. 353: 89 accepted, 11 rejected and 33 corrections.

`RHD-FR-004` reviews the fourth 100 on pp. 357–361: 90 accepted, 10 rejected and 62 corrections.

`RHD-FR-005` reviews the fifth 100 on pp. 361–365: 96 accepted, 4 rejected and 90 corrections.

`RHD-FR-006` reviews the sixth 100 on pp. 365–368: 98 accepted, 2 rejected and 91 corrections. It rejects German gloss fragments (`Hinweg`, `Immer`) and restores genuine Rarámuri starts lost by linear OCR, including `Tápoa`.

`RHD-FR-007` reviews the final nine `high_machine` candidates. All nine are accepted on printed p. 368 and eight headwords receive clear facsimile corrections. Several had been assigned mechanically to p. 369; direct collation shows that p. 369 is already the appendix and that the dictionary entries belong to p. 368.

Cumulative status for the **entire high-confidence machine tier**: **609 candidates reviewed, 553 starts accepted, 56 false boundaries rejected and 298 clear headword corrections**. Every accepted high-confidence start has a complete AI-assisted diplomatic overlay, and the corpus retains **2,439 active provisional candidates** out of the 2,495-candidate coverage layer.

The scope of review batches is headword presence, article-start boundary and exact page placement. Accepted records move to `facsimile_checked_headword_ai_assisted` unless a diplomatic overlay supersedes that status. Rejected IDs are retained with `rejected_false_positive`. Diplomatic overlays use `diplomatic_transcription_ai_assisted`. None of these statuses should be interpreted as `diplomatic_verified` or as human linguistic validation.

The `high_machine` tier is exhausted. The machine inventory still contains 1,110 `medium_machine` and 716 `low_machine` candidates, in addition to the 60 curated anchors.
