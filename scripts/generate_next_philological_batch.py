#!/usr/bin/env python3
"""Generate the next AI recollation batch and a separate human-review queue."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
VALIDATION = ROOT / "data" / "validation"
REVIEW = VALIDATION / "review"
queue = json.load((VALIDATION / "uncertainty_queue.json").open(encoding="utf-8"))
all_records = queue.get("records", [])

reviewed_ids = set()
human_items = []
completed_batches = []
for path in sorted(REVIEW.glob("philological_review_batch_*.json")):
    manifest = json.load(path.open(encoding="utf-8"))
    completed_batches.append(manifest.get("batch_id", path.stem))
    for item in manifest.get("records", []):
        rid = item["record_id"]
        reviewed_ids.add(rid)
        route = item.get("residual_route", "")
        if route:
            human_items.append({
                "record_id": rid,
                "source_batch": manifest.get("batch_id", ""),
                "printed_page": item.get("printed_page"),
                "ai_recollation_disposition": item.get("disposition", ""),
                "residual_route": route,
                "ai_recollation_note": item.get("note", ""),
                "human_verified": False,
                "philologically_verified_by_human": False,
                "linguistically_verified": False,
            })

remaining = [x for x in all_records if x.get("record_id") not in reviewed_ids]
next_number = len(completed_batches) + 1
next_id = f"RHD-PHIL-{next_number:03d}"
next_records = remaining[:50]
next_batch = {
    "batch_id": next_id,
    "stage": "ai_assisted_philological_recollation",
    "selection_rule": "first 50 open-validation records not present in philological_review_batch_*.json",
    "remaining_before_batch": len(remaining),
    "count": len(next_records),
    "human_verified": False,
    "records": next_records,
}
(VALIDATION / "next_philological_batch.json").write_text(
    json.dumps(next_batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
compact = {
    "batch_id": next_id,
    "remaining_before_batch": len(remaining),
    "count": len(next_records),
    "records": [
        [x["record_id"], x["printed_page"], x.get("facsimile_column", ""), x.get("headword_diplomatic", "")]
        for x in next_records
    ],
}
(VALIDATION / "next_philological_batch_compact.json").write_text(
    json.dumps(compact, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8"
)

# Human queue prioritizes records still unresolved after AI recollation, then
# records whose graphic reading is stable but whose linguistic/semantic judgment
# remains outside the AI recollation claim.
rank = {"unresolved_after_ai_recollation": 1, "corrected_ai_assisted": 2, "confirmed_ai_assisted": 3}
human_items.sort(key=lambda x: (rank.get(x["ai_recollation_disposition"], 9), x.get("printed_page") or 999, x["record_id"]))
human_queue = {
    "stage": "independent_human_review",
    "selection_rule": "records already AI-recollated that retain an explicit residual human/linguistic route",
    "count": len(human_items),
    "human_verified": False,
    "records": human_items,
}
(VALIDATION / "human_review_queue.json").write_text(
    json.dumps(human_queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

status = {
    "open_validation_records_total": len(all_records),
    "ai_philological_recollation_reviewed": len(reviewed_ids),
    "ai_philological_recollation_remaining": len(remaining),
    "completed_ai_recollation_batches": completed_batches,
    "next_ai_recollation_batch": next_id if next_records else None,
    "next_ai_recollation_batch_size": len(next_records),
    "human_review_queue_count": len(human_items),
    "human_verified_records": 0,
    "philologically_verified_by_human_records": 0,
    "linguistically_verified_records": 0,
}
(VALIDATION / "validation_progress.json").write_text(
    json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(
    f"Reviewed by AI recollation={len(reviewed_ids)}; remaining={len(remaining)}; "
    f"next={next_id} ({len(next_records)}); human queue={len(human_items)}"
)
