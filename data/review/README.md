# Facsimile review

This directory stores append-only editorial review batches applied on top of the coverage-first OCR segmentation. Review batches preserve persistent record IDs: false-positive machine boundaries are rejected but never recycled, and accepted candidates remain explicitly distinct from human/philological verification.

## RHD-FR-001

`RHD-FR-001` reviews the first 100 candidates classified `high_machine`, in source order, against the scanned facsimile. It covers printed pages 301–317. Results: 100 candidates inspected, 86 article starts accepted, 14 false boundaries rejected, and 4 headwords corrected from clear OCR errors. All 86 accepted starts subsequently received complete AI-assisted diplomatic article transcriptions in `RHD-DIP-001A`–`RHD-DIP-001E`.

## RHD-FR-002

`RHD-FR-002` reviews the next 100 `high_machine` candidates in source order. The reviewed records occur on printed pages 318–339. Results: 100 candidates inspected, 85 article starts accepted, 15 false boundaries rejected, and 10 headwords corrected from clear OCR/layout errors. All 85 accepted starts subsequently received complete AI-assisted diplomatic transcriptions in `RHD-DIP-002A` and `RHD-DIP-002B`.

## RHD-FR-003

`RHD-FR-003` reviews the next 100 `high_machine` candidates and crosses the structural transition from German→Rarámuri to Rarámuri→German on printed p. 353. Results: 100 candidates inspected, 89 article starts accepted, 11 false boundaries rejected, and 33 headwords corrected from clear OCR/layout errors. All 89 accepted starts subsequently received complete AI-assisted diplomatic transcriptions in `RHD-DIP-003A`–`RHD-DIP-003E`.

## RHD-FR-004

`RHD-FR-004` reviews the fourth cohort of 100 `high_machine` candidates, wholly in the Rarámuri→German dictionary. Direct facsimile collation places the accepted starts on printed pages 357–361 and corrects several local OCR page-interpolation errors. Results: 100 candidates inspected, 90 article starts accepted, 10 false boundaries rejected, and 62 headwords corrected from clear OCR/layout or diacritic errors. All 90 accepted starts received complete AI-assisted diplomatic transcriptions in `RHD-DIP-004A`–`RHD-DIP-004E`.

Cumulative status after four review batches: **400 candidates reviewed, 350 starts accepted, 50 false boundaries rejected, 109 clear headword corrections, 350 complete AI-assisted diplomatic articles, and 2,445 active provisional candidates** out of the 2,495-candidate coverage layer.

The scope of review batches is headword presence, article-start boundary and exact page placement. Accepted records move to `facsimile_checked_headword_ai_assisted` unless a diplomatic overlay supersedes that status. Rejected IDs are retained with `rejected_false_positive`. Diplomatic overlays use `diplomatic_transcription_ai_assisted`. None of these statuses should be interpreted as `diplomatic_verified` or as human linguistic validation.
