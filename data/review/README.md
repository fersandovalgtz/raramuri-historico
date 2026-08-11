# Facsimile review

This directory stores append-only editorial review batches applied on top of the coverage-first OCR segmentation.

Batch `RHD-FR-001` reviews the first 100 candidates classified `high_machine`, in source order, against the scanned facsimile. Scope is limited to headword presence and article-start boundary; it is not a full diplomatic transcription or linguistic validation.

Results: 100 candidates inspected, 86 article starts accepted, 14 false boundaries rejected, and 4 headwords corrected from clear OCR errors (`Allmächtig`, `Eingraben`, `Faſttag`, `Fledermaus`). Exact printed/PDF page coordinates are recorded for all 100.

Rejected IDs are retained with status `rejected_false_positive`. Accepted records move to `facsimile_checked_headword_ai_assisted`; this must not be interpreted as `diplomatic_verified`.
