#!/usr/bin/env python3
"""Generate deterministic priority views for independent human review.

This script does not perform or claim human validation. It only orders the
already AI-recollated human_review_queue so independent reviewers can address
residual uncertainty systematically. It then generates reviewer-ready evidence
packets for the priority-1 unresolved cohort.
"""
from pathlib import Path
import json
import runpy

ROOT = Path(__file__).resolve().parents[1]
V = ROOT / "data" / "validation"
SOURCE = V / "human_review_queue.json"
OUT = V / "human_review_priority.json"
COMPACT = V / "human_review_priority_compact.json"

human = json.load(SOURCE.open(encoding="utf-8"))
records = human.get("records", [])

rank = {
    "unresolved_after_ai_recollation": 1,
    "corrected_ai_assisted": 2,
    "confirmed_ai_assisted": 3,
}
labels = {
    1: "unresolved_after_ai_recollation",
    2: "corrected_ai_assisted",
    3: "confirmed_ai_assisted",
}

ordered = sorted(
    records,
    key=lambda x: (
        rank.get(x.get("ai_recollation_disposition"), 99),
        int(x.get("printed_page", 9999)),
        x.get("record_id", ""),
    ),
)

priority_counts = {labels[i]: 0 for i in (1, 2, 3)}
full_records = []
compact_records = []
for x in ordered:
    disposition = x.get("ai_recollation_disposition")
    priority_rank = rank.get(disposition, 99)
    if disposition in priority_counts:
        priority_counts[disposition] += 1
    item = {
        "priority_rank": priority_rank,
        "priority_reason": (
            "AI recollation did not close the documentary problem"
            if priority_rank == 1 else
            "AI recollation proposed a documentary correction requiring adjudication"
            if priority_rank == 2 else
            "AI recollation confirmed the reading but residual linguistic/semantic/disciplinary review remains"
        ),
        "record_id": x.get("record_id"),
        "source_batch": x.get("source_batch"),
        "printed_page": x.get("printed_page"),
        "ai_recollation_disposition": disposition,
        "residual_route": x.get("residual_route"),
        "ai_recollation_note": x.get("ai_recollation_note", ""),
        "human_verified": False,
        "philologically_verified_by_human": False,
        "linguistically_verified": False,
    }
    full_records.append(item)
    compact_records.append([
        priority_rank,
        x.get("record_id"),
        x.get("printed_page"),
        disposition,
        x.get("residual_route"),
    ])

payload = {
    "stage": "independent_human_review_priority",
    "generated_from": "data/validation/human_review_queue.json",
    "selection_rule": "priority 1 unresolved_after_ai_recollation; priority 2 corrected_ai_assisted; priority 3 confirmed_ai_assisted; then printed page and persistent record_id",
    "count": len(full_records),
    "priority_counts": priority_counts,
    "human_verified": False,
    "records": full_records,
}
compact = {
    "stage": "independent_human_review_priority",
    "count": len(compact_records),
    "priority_counts": priority_counts,
    "records": compact_records,
}

OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
COMPACT.write_text(json.dumps(compact, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
print(f"Generated human review priority: {len(full_records)} records; {priority_counts}")

# Generate review packets only after the priority artifacts exist. The called
# script is also non-adjudicative and leaves every verification flag false.
runpy.run_path(str(ROOT / "scripts" / "generate_priority1_review_dossiers.py"), run_name="__main__")

# Keep project metadata synchronized with the generated priority layer.
meta_path = ROOT / "project-metadata.json"
if meta_path.exists():
    meta = json.load(meta_path.open(encoding="utf-8"))
    scope = meta.setdefault("scope", {})
    pipeline = meta.setdefault("editorial_pipeline", {})
    unresolved = priority_counts["unresolved_after_ai_recollation"]
    corrected = priority_counts["corrected_ai_assisted"]
    confirmed = priority_counts["confirmed_ai_assisted"]
    scope["human_review_priority_counts"] = {
        "unresolved_after_ai_recollation": unresolved,
        "corrected_ai_assisted": corrected,
        "confirmed_ai_assisted": confirmed,
    }
    scope["priority1_review_dossiers"] = unresolved
    scope["status"] = (
        "Complete AI-assisted documentary phase: all 2,495 segmented candidates reviewed against facsimile; "
        "1,965 provisional article starts accepted and diplomatically transcribed; 530 false boundaries rejected; "
        "781 headwords corrected. Scientific note audit identified 482 explicit open-validation records and "
        "RHD-PHIL-001–010 re-collated all 482 at high resolution. The independent human queue is prioritized as "
        f"{unresolved} unresolved, {corrected} proposed corrections and {confirmed} AI-confirmed records with residual "
        f"review routes. {unresolved} reviewer-ready priority-1 evidence dossiers are generated. Human/philological "
        "and linguistic verification remains 0/482."
    )
    pipeline["priority1_review_dossiers"] = "data/validation/priority1_review_dossiers.json"
    pipeline["priority1_review_dossiers_compact"] = "data/validation/priority1_review_dossiers_compact.json"
    pipeline["priority1_review_index"] = "data/validation/PRIORITY1_REVIEW_INDEX.md"
    pipeline["priority1_review_dossier_directory"] = "data/validation/dossiers/priority1/"
    pipeline["priority1_review_dossier_generator"] = "scripts/generate_priority1_review_dossiers.py"
    pipeline["priority1_review_dossier_count"] = unresolved
    pipeline["human_review_priority_counts"] = {
        "priority_1_unresolved": unresolved,
        "priority_2_corrected_ai_assisted": corrected,
        "priority_3_confirmed_ai_assisted": confirmed,
    }
    pipeline["next_stage_priority"] = (
        f"Begin with the {unresolved} reviewer-ready priority-1 unresolved dossiers, then adjudicate the "
        f"{corrected} corrected_ai_assisted proposals, then complete residual linguistic, semantic, historical and "
        f"disciplinary review of the {confirmed} confirmed_ai_assisted records. Use HUMAN_REVIEW_PROTOCOL.md and "
        "human_review_template.json; no verification flag may be set without explicit independent reviewer evidence."
    )
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Synchronized project-metadata.json human-review counts and dossier references")
