#!/usr/bin/env python3
"""Freeze the first 50 open-validation records as the next philological work batch."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
VALIDATION = ROOT / "data" / "validation"
queue = json.load((VALIDATION / "uncertainty_queue.json").open(encoding="utf-8"))
records = queue.get("records", [])[:50]
out = {
    "batch_id": "RHD-PHIL-001",
    "stage": "ai_assisted_philological_recollation",
    "selection_rule": "first 50 records from deterministic open-validation queue",
    "count": len(records),
    "human_verified": False,
    "records": records,
}
(VALIDATION / "next_philological_batch.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(f"Generated RHD-PHIL-001 working batch with {len(records)} records")
