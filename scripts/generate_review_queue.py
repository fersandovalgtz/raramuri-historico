#!/usr/bin/env python3
"""Generate the next deterministic facsimile-review cohort.

The queue is derived only from the regenerated coverage-first entries layer and
append-only review manifests. It never mutates source OCR or editorial evidence.
"""
from pathlib import Path
import csv, json

ROOT = Path(__file__).resolve().parents[1]
ENTRIES = ROOT / "data" / "entries.csv"
REVIEW_DIR = ROOT / "data" / "review"
OUT = REVIEW_DIR / "next_review_queue.json"
COMPACT = REVIEW_DIR / "next_review_queue_compact.json"

rows = list(csv.DictReader(ENTRIES.open(encoding="utf-8")))
seen = set()
for path in sorted(REVIEW_DIR.glob("facsimile_review_batch_*.json")):
    manifest = json.load(path.open(encoding="utf-8"))
    for rid, _page in manifest.get("records", []):
        if rid in seen:
            raise SystemExit(f"duplicate reviewed record id: {rid}")
        seen.add(rid)

priority = ["medium_machine", "low_machine"]
selected = []
selected_tier = None
for tier in priority:
    pending = [r for r in rows if r.get("segmentation_confidence") == tier and r["record_id"] not in seen]
    if pending:
        selected_tier = tier
        selected = pending[:100]
        remaining_in_tier = len(pending)
        break
else:
    remaining_in_tier = 0

payload = {
    "generated_from": "data/entries.csv + data/review/facsimile_review_batch_*.json",
    "selection_rule": "first 100 unreviewed records in source/record order, medium_machine before low_machine",
    "tier": selected_tier,
    "remaining_before_batch": remaining_in_tier,
    "count": len(selected),
    "records": [
        {
            "record_id": r["record_id"],
            "direction": r.get("direction", ""),
            "headword_raw": r.get("headword_raw", ""),
            "printed_page": int(r["printed_page"]) if r.get("printed_page") else None,
            "pdf_page": int(r["pdf_page"]) if r.get("pdf_page") else None,
            "source_ocr_line_start": int(r["source_ocr_line_start"]) if r.get("source_ocr_line_start") else None,
            "source_ocr_line_end": int(r["source_ocr_line_end"]) if r.get("source_ocr_line_end") else None
        }
        for r in selected
    ]
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
compact = {
    "tier": selected_tier,
    "remaining_before_batch": remaining_in_tier,
    "records": [[r["record_id"], int(r["printed_page"]), r.get("headword_raw", "")] for r in selected]
}
COMPACT.write_text(json.dumps(compact, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
print(f"generated {len(selected)}-record queue for {selected_tier}; {remaining_in_tier} pending before batch")
