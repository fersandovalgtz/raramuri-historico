#!/usr/bin/env python3
"""Synchronize root project metadata from generated scientific state.

This script only mirrors counts and workflow state already present in generated
artifacts. It does not perform or imply human verification.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PM = ROOT / "project-metadata.json"
PRIORITY = ROOT / "data" / "validation" / "human_review_priority.json"
PROGRESS = ROOT / "data" / "validation" / "validation_progress.json"
DIACHRONIC = ROOT / "data" / "diachronic" / "exact_graphic_candidates_summary.json"

pm = json.loads(PM.read_text(encoding="utf-8"))
priority = json.loads(PRIORITY.read_text(encoding="utf-8"))
progress = json.loads(PROGRESS.read_text(encoding="utf-8"))
counts = priority.get("priority_counts", {})

unresolved = int(counts.get("unresolved_after_ai_recollation", 0))
corrected = int(counts.get("corrected_ai_assisted", 0))
confirmed = int(counts.get("confirmed_ai_assisted", 0))
human_count = int(priority.get("count", unresolved + corrected + confirmed))

scope = pm.setdefault("scope", {})
pipeline = pm.setdefault("editorial_pipeline", {})

scope["ai_philological_recollation_reviewed"] = int(progress.get("ai_philological_recollation_reviewed", 0))
scope["ai_philological_recollation_remaining"] = int(progress.get("ai_philological_recollation_remaining", 0))
scope["human_review_queue_count"] = human_count
scope["human_review_priority_counts"] = {
    "unresolved_after_ai_recollation": unresolved,
    "corrected_ai_assisted": corrected,
    "confirmed_ai_assisted": confirmed,
}
scope["human_verified_diplomatic_transcriptions"] = int(progress.get("human_verified_records", 0))
scope["philologically_verified_by_human_records"] = int(progress.get("philologically_verified_by_human_records", 0))
scope["linguistically_verified_records"] = int(progress.get("linguistically_verified_records", 0))
scope["all_open_validation_records_ai_recollated"] = int(progress.get("ai_philological_recollation_remaining", 0)) == 0
scope["status"] = (
    "Complete AI-assisted documentary phase: all 2,495 segmented candidates reviewed against facsimile; "
    "1,965 provisional article starts accepted and diplomatically transcribed; 530 false boundaries rejected; "
    "781 headwords corrected. Scientific note audit identified 482 explicit open-validation records and "
    "RHD-PHIL-001–010 re-collated all 482 at high resolution. The independent human queue is prioritized as "
    f"{unresolved} unresolved, {corrected} proposed corrections and {confirmed} AI-confirmed records with residual review routes. "
    "Human/philological and linguistic verification remains 0/482."
)

pipeline["human_review_queue_count"] = human_count
pipeline["human_review_priority_counts"] = {
    "priority_1_unresolved": unresolved,
    "priority_2_corrected_ai_assisted": corrected,
    "priority_3_confirmed_ai_assisted": confirmed,
}
pipeline["human_verified_records"] = int(progress.get("human_verified_records", 0))
pipeline["philologically_verified_by_human_records"] = int(progress.get("philologically_verified_by_human_records", 0))
pipeline["linguistically_verified_records"] = int(progress.get("linguistically_verified_records", 0))
pipeline["next_systematic_stage"] = "independent_human_philological_and_linguistic_validation_plus_diachronic_candidate_adjudication"
pipeline["next_stage_priority"] = (
    f"Begin with the {unresolved} priority-1 unresolved records, then adjudicate the {corrected} "
    f"corrected_ai_assisted proposals, then complete residual linguistic, semantic, historical and disciplinary "
    f"review of the {confirmed} confirmed_ai_assisted records. Diachronic machine candidates remain a separate "
    "derived layer and may not be promoted to validated correspondences without explicit independent review."
)

if DIACHRONIC.exists():
    d = json.loads(DIACHRONIC.read_text(encoding="utf-8"))
    scope["diachronic_exact_graphic_candidates"] = int(d.get("candidate_count", 0))
    scope["diachronic_historical_records_with_candidates"] = int(d.get("historical_records_with_candidates", 0))
    scope["diachronic_modern_records_matched"] = int(d.get("modern_records_matched", 0))
    scope["diachronic_unique_graphic_keys"] = int(d.get("unique_graphic_keys", 0))
    pipeline["diachronic_correspondence_layer"] = "data/diachronic/exact_graphic_candidates.json"
    pipeline["diachronic_correspondence_summary"] = "data/diachronic/exact_graphic_candidates_summary.json"
    pipeline["diachronic_relation_type"] = d.get("relation_type", "exact_normalized_graphic_match")
    pipeline["diachronic_candidate_count"] = int(d.get("candidate_count", 0))
    pipeline["diachronic_modern_source_commit"] = d.get("modern_commit", "")
    pipeline["diachronic_human_reviewed_candidates"] = 0
    pipeline["diachronic_policy"] = (
        "Machine-generated exact graphic matches are documentary comparison candidates only; they do not assert "
        "semantic identity, cognacy, dialect identity or historical lexical continuity."
    )

PM.write_text(json.dumps(pm, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(
    "Synchronized project metadata: "
    f"human priority={unresolved}/{corrected}/{confirmed}; "
    f"diachronic candidates={scope.get('diachronic_exact_graphic_candidates', 0)}"
)
