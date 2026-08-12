# Facsimile review

This directory stores append-only editorial review batches applied on top of the coverage-first OCR segmentation. Review batches preserve persistent record IDs: false-positive machine boundaries are rejected but never recycled, and accepted candidates remain explicitly distinct from human/philological verification.

## Exhausted high-confidence tier

`RHD-FR-001` through `RHD-FR-007` exhaust all **609 `high_machine` candidates**. Across those seven cohorts, 553 article starts were accepted, 56 false boundaries rejected and 298 clear headword corrections recorded. Every accepted high-confidence start has a complete AI-assisted diplomatic overlay.

## Medium-confidence review

`RHD-FR-008` through `RHD-FR-013` cover the first six systematic 100-record `medium_machine` cohorts. After those batches, 600 medium-confidence candidates had been reviewed: 466 accepted starts and 134 false boundaries.

`RHD-FR-014` reviews the seventh 100 `medium_machine` candidates in deterministic source order across printed pp. 345–350: **81 accepted article starts, 19 rejected false boundaries and 6 clear headword corrections**. The rejected boundaries include Rarámuri forms (`Joliki`, `Tóuke`, `Pitichabürameke`), the p. 346 catchword `Um-`, cross-references and prose fragments generated from the long articles `Tanz`, `Vogel`, `Warm` and `Wehe thun`. The six corrected headwords are `Trunk`, `Verehligen`, `Vergänglich`, `Verſucher`, `Voll` and `Wahnſinnig`.

Eighteen `RHD-FR-014` records also received corrected printed-page placement after facsimile collation. These page corrections are editorial overlays and do not mutate the preserved OCR source or recycle persistent IDs.

`RHD-DIP-014A`–`RHD-DIP-014E` provide complete diplomatic overlays for **all 81 accepted `RHD-FR-014` starts**. Extended records including `Taback`, `Verhexen`, `Viel`, `Vogel`, `Weit` and `Waizen` are reconstructed from documentary column/page order rather than linear OCR. Ambiguous readings are flagged instead of silently normalized.

Cumulative status after `RHD-FR-014`: **1,309 candidates reviewed, 1,100 starts accepted, 209 false boundaries rejected, 359 clear headword corrections, 1,100 complete AI-assisted diplomatic articles and 2,286 active provisional candidates** out of the 2,495-candidate coverage layer.

The scope of review batches is headword presence, article-start boundary and exact page placement. Accepted records move to `facsimile_checked_headword_ai_assisted` unless a diplomatic overlay supersedes that status. Rejected IDs are retained with `rejected_false_positive`. Diplomatic overlays use `diplomatic_transcription_ai_assisted`. None of these statuses should be interpreted as independently verified or as human linguistic validation.

## Deterministic next cohort

`scripts/generate_review_queue.py` generates `next_review_queue.json` and `next_review_queue_compact.json` from the regenerated coverage layer plus all append-only review manifests. It selects the first 100 unreviewed records in source order, exhausting `medium_machine` before `low_machine`; this prevents manual cohort drift or identifier reuse.

The machine inventory now contains **410 unreviewed `medium_machine` candidates** and 716 `low_machine` candidates. The next systematic review cohort is `RHD-FR-015`, from `RHD-S1809-01543` (`Wenig`) to `RHD-S1809-01774` (`Eke`), spanning approximately printed pp. 351–356 and crossing the p. 353 German→Rarámuri / Rarámuri→German transition.
