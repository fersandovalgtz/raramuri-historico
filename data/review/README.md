# Facsimile review

This directory stores append-only editorial review batches applied on top of the coverage-first OCR segmentation. Review batches preserve persistent record IDs: false-positive machine boundaries are rejected but never recycled, and accepted candidates remain explicitly distinct from human/philological verification.

## Exhausted high-confidence tier

`RHD-FR-001` through `RHD-FR-007` exhaust all **609 `high_machine` candidates**. Across those cohorts, 553 article starts were accepted, 56 false boundaries rejected and 298 clear headword corrections recorded. Every accepted high-confidence start has a complete AI-assisted diplomatic overlay.

## Medium-confidence review

`RHD-FR-008` through `RHD-FR-015` cover the first eight systematic 100-record `medium_machine` cohorts. `RHD-FR-016` reviews the ninth cohort, entirely within Rarámuri→German.

`RHD-FR-016` contains **100 reviewed candidates, 90 accepted article starts, 10 rejected false boundaries and 87 clear headword corrections**. Direct facsimile collation places the accepted/rejected evidence across printed pp. **356–360** and corrects the machine page assignment for **32 records**.

The rejected candidates are German glosses, cross-references or prose fragments misidentified as Rarámuri headwords: `Ja`, `Bart hat`, `Seyn`, `Arm`, `Tichic`, `Mörtel`, `Ichic Kunofiein`, `Aufmunterung`, `Frisch` and `Ganz`. Representative recovered headwords include `Etschaguóameke`, `Guarátscha`, `Guechtschíc`, `Haleséatschic, oder Hareséatschic`, `Jachcála`, `Jumánamatschígameke`, `Kauguáca` and `Kuepútsela, oder Kepútschela`.

The high correction rate is evidence of OCR degradation in the inverse dictionary rather than a claim of new normalized orthography. The facsimile is authoritative. The 2020 Universidad de Sonora transcription by Merrill et al. is documented as a secondary collation aid only.

`RHD-DIP-016A`–`RHD-DIP-016I` provide complete diplomatic overlays for **all 90 accepted `RHD-FR-016` starts**. Ambiguous readings remain flaggable through `uncertainty_note`; every record remains `human_verified=false`.

Cumulative status after `RHD-FR-016`: **1,509 candidates reviewed, 1,274 starts accepted, 235 false boundaries rejected, 483 clear headword corrections, 1,274 complete AI-assisted diplomatic articles and 2,260 active provisional candidates** out of the 2,495-candidate coverage layer.

The scope of review batches is headword presence, article-start boundary, exact page placement and documentary direction. Accepted records move to `facsimile_checked_headword_ai_assisted` unless a diplomatic overlay supersedes that status. Rejected IDs are retained with `rejected_false_positive`. Diplomatic overlays use `diplomatic_transcription_ai_assisted`. None of these statuses should be interpreted as independently verified linguistic or philological readings.

## Deterministic next cohort

`scripts/generate_review_queue.py` generates `next_review_queue.json` and `next_review_queue_compact.json` from the regenerated coverage layer plus all append-only review manifests. It selects the first 100 unreviewed records in source order, exhausting `medium_machine` before `low_machine`.

The machine inventory now contains **210 unreviewed `medium_machine` candidates** and 716 `low_machine` candidates. The next systematic cohort is **`RHD-FR-017`**, from `RHD-S1809-01989` (`Lala`) through `RHD-S1809-02233` (`Rnsra`), within Rarámuri→German and automatically estimated around printed pp. **360–365**. Exact pagination and readings remain subject to facsimile collation.