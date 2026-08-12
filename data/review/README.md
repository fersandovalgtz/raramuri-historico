# Facsimile review

This directory stores append-only editorial review batches applied on top of the coverage-first OCR segmentation. Review batches preserve persistent record IDs: false-positive machine boundaries are rejected but never recycled, and accepted candidates remain explicitly distinct from human/philological verification.

## RHD-FR-001

`RHD-FR-001` reviews the first 100 candidates classified `high_machine`, in source order, against the scanned facsimile. It covers printed pages 301–317. Results: 100 candidates inspected, 86 article starts accepted, 14 false boundaries rejected, and 4 headwords corrected from clear OCR errors (`Allmächtig`, `Eingraben`, `Faſttag`, `Fledermaus`). All 86 accepted starts subsequently received complete AI-assisted diplomatic article transcriptions in `RHD-DIP-001A`–`RHD-DIP-001E`.

## RHD-FR-002

`RHD-FR-002` reviews the next 100 `high_machine` candidates in source order. The reviewed records occur on printed pages 318–339. Results: 100 candidates inspected, 85 article starts accepted, 15 false boundaries rejected, and 10 headwords corrected from clear OCR/layout errors. The review also corrected several exact printed-page assignments where linear OCR and interpolated page anchors had drifted from the facsimile.

Cumulative facsimile-boundary status after the two batches: **200 candidates reviewed, 171 starts accepted, 29 false boundaries rejected, 14 clear headword corrections, and 2,466 active provisional candidates** out of the 2,495-candidate coverage layer.

The scope of both review batches is limited to headword presence, article-start boundary and exact page placement. Accepted records move to `facsimile_checked_headword_ai_assisted` unless a diplomatic overlay supersedes that status. Rejected IDs are retained with `rejected_false_positive`. Neither status should be interpreted as `diplomatic_verified` or as human linguistic validation.
