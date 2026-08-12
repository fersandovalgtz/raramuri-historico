# Facsimile review

This directory stores append-only editorial review batches applied on top of the coverage-first OCR segmentation. Review batches preserve persistent record IDs: false-positive machine boundaries are rejected but never recycled, and accepted candidates remain explicitly distinct from human/philological verification.

## Exhausted high-confidence tier

`RHD-FR-001` through `RHD-FR-007` exhaust all **609 `high_machine` candidates**. Across those cohorts, 553 article starts were accepted, 56 false boundaries rejected and 298 clear headword corrections recorded. Every accepted high-confidence start has a complete AI-assisted diplomatic overlay.

## Medium-confidence review

`RHD-FR-008` through `RHD-FR-014` cover the first seven systematic 100-record `medium_machine` cohorts. `RHD-FR-015` reviews the eighth cohort in deterministic source order and is the first systematic batch to cross the dictionary-direction transition.

`RHD-FR-015` contains **100 reviewed candidates, 84 accepted article starts, 16 rejected false boundaries and 37 clear headword corrections**. Direct facsimile collation places the cohort on printed pp. **350–356**. The first four candidates (`Wenig`, `Werfen`, `Wettlauf`, `Widder`) are actually on p. 350, although the OCR-derived queue estimated p. 351.

Printed p. 353 is directionally mixed: German→Rarámuri concludes in the upper portion and Rarámuri→German begins below the section break. The batch therefore records explicit direction awareness in addition to page and column placement. Rejections include catchwords, cross-references, German glosses mistaken for inverse headwords, grammatical prose and paratext. The 37 corrections include heavily degraded inverse forms such as `Ali oder ari`, `Atſchilélila`, `Bacalátſchi`, `Baſſará`, `Bucú`, `Cachcánali`, `Cocotſchi`, `Corilícu`, `Cotſchimé`, `Echſámela` and `Echtſchiruc`.

`RHD-DIP-015A`–`RHD-DIP-015E` provide complete diplomatic overlays for **all 84 accepted starts**. The transition is preserved explicitly in `RHD-DIP-015B`; later records are in the Rarámuri→German section. Ambiguous diacritics and morphological readings remain flagged rather than silently normalized.

Cumulative status after `RHD-FR-015`: **1,409 candidates reviewed, 1,184 starts accepted, 225 false boundaries rejected, 396 clear headword corrections, 1,184 complete AI-assisted diplomatic articles and 2,270 active provisional candidates** out of the 2,495-candidate coverage layer.

The scope of review batches is headword presence, article-start boundary, exact page placement and documentary direction. Accepted records move to `facsimile_checked_headword_ai_assisted` unless a diplomatic overlay supersedes that status. Rejected IDs are retained with `rejected_false_positive`. Diplomatic overlays use `diplomatic_transcription_ai_assisted`. None of these statuses should be interpreted as independently verified linguistic or philological readings.

## Deterministic next cohort

`scripts/generate_review_queue.py` generates `next_review_queue.json` and `next_review_queue_compact.json` from the regenerated coverage layer plus all append-only review manifests. It selects the first 100 unreviewed records in source order, exhausting `medium_machine` before `low_machine`.

The machine inventory now contains **310 unreviewed `medium_machine` candidates** and 716 `low_machine` candidates. The next systematic cohort is **`RHD-FR-016`**, from `RHD-S1809-01778` to `RHD-S1809-01988`, already within Rarámuri→German and automatically estimated around printed pp. 356–360. Exact pagination and readings remain subject to facsimile collation.