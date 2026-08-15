#!/usr/bin/env python3
"""Validate the first Steffel -> RHD 1.0 canonical projection.

Uses only the Python standard library. If jsonschema is installed, full schema
validation is also performed; otherwise structural and corpus invariants remain mandatory.
"""

from pathlib import Path
import csv
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = ROOT / "data" / "entries.csv"
CANONICAL = ROOT / "data" / "canonical" / "steffel-1809.entries.jsonl"
SUMMARY = ROOT / "data" / "canonical" / "steffel-1809.summary.json"
SCHEMA_PATH = ROOT / "schemas" / "rhd-entry-1.0.schema.json"
PROFILE_PATH = ROOT / "source_profiles" / "steffel-1809.source.json"
INVENTORY_PATH = ROOT / "data" / "corpus_inventory.json"

errors = []


def load_jsonl(path):
    result = []
    with path.open(encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                result.append(json.loads(line))
            except json.JSONDecodeError as exc:
                errors.append(f"bad JSONL line {lineno}: {exc}")
    return result


for required in (SOURCE_CSV, CANONICAL, SUMMARY, SCHEMA_PATH, PROFILE_PATH, INVENTORY_PATH):
    if not required.exists():
        errors.append(f"missing required file: {required.relative_to(ROOT)}")

if errors:
    print("\n".join("ERROR: " + e for e in errors))
    sys.exit(1)

source_rows = list(csv.DictReader(SOURCE_CSV.open(encoding="utf-8")))
source_by_id = {r["record_id"]: r for r in source_rows}
canonical = load_jsonl(CANONICAL)
canonical_by_id = {r.get("record_id"): r for r in canonical}
summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))

if len(canonical) != len(source_rows):
    errors.append(f"canonical count {len(canonical)} != source count {len(source_rows)}")
if len(canonical_by_id) != len(canonical):
    errors.append("duplicate record_id in canonical output")
if set(canonical_by_id) != set(source_by_id):
    errors.append("canonical record_id set differs from operational source")
if len(source_rows) != inventory["candidate_entries_total"]:
    errors.append("operational source differs from corpus inventory")

expected_rejected = sum(r.get("status") == "rejected_false_positive" for r in source_rows)
expected_active = len(source_rows) - expected_rejected
expected_open = sum(
    r.get("status") != "rejected_false_positive"
    and r.get("diplomatic_note_state") == "open_validation"
    for r in source_rows
)

actual_rejected = sum(r.get("status") == "rejected_boundary" for r in canonical)
actual_active = sum(r.get("status") == "active" for r in canonical)
actual_open = sum(
    any(n.get("status") == "open_validation" for n in r.get("notes", []))
    for r in canonical
)

if actual_rejected != expected_rejected:
    errors.append(f"rejected count {actual_rejected} != {expected_rejected}")
if actual_active != expected_active:
    errors.append(f"active count {actual_active} != {expected_active}")
if actual_open != expected_open:
    errors.append(f"open-validation note count {actual_open} != {expected_open}")

if expected_active != inventory["facsimile_review"]["active_candidates_after_review"]:
    errors.append("active source count differs from inventory")
if expected_rejected != inventory["facsimile_review"]["rejected_false_positive_boundaries"]:
    errors.append("rejected source count differs from inventory")

required_top = {
    "record_id",
    "source_id",
    "witness_id",
    "status",
    "locators",
    "layers",
    "provenance",
}

for item in canonical:
    rid = item.get("record_id")
    src = source_by_id.get(rid, {})

    missing = required_top - set(item)
    if missing:
        errors.append(f"{rid}: missing canonical keys {sorted(missing)}")
        continue

    if not re.fullmatch(r"RHD-S1809-\d{5}", rid or ""):
        errors.append(f"{rid}: bad canonical record_id")
    if item["source_id"] != profile["source_id"]:
        errors.append(f"{rid}: source_id differs from profile")
    if item["witness_id"] != profile["witness"]["witness_id"]:
        errors.append(f"{rid}: witness_id differs from profile")
    if item.get("direction") != src.get("direction"):
        errors.append(f"{rid}: direction changed during projection")
    if str(item["locators"].get("printed_page")) != str(src.get("printed_page")):
        errors.append(f"{rid}: printed page changed during projection")
    if str(item["locators"].get("ocr_line_start")) != str(src.get("source_ocr_line_start")):
        errors.append(f"{rid}: OCR start line changed")
    if str(item["locators"].get("ocr_line_end")) != str(src.get("source_ocr_line_end")):
        errors.append(f"{rid}: OCR end line changed")

    rejected = src.get("status") == "rejected_false_positive"
    expected_status = "rejected_boundary" if rejected else "active"
    if item["status"] != expected_status:
        errors.append(f"{rid}: canonical status {item['status']} != {expected_status}")

    segmentation = item["layers"].get("segmentation", {})
    if segmentation.get("confidence") != src.get("segmentation_confidence"):
        errors.append(f"{rid}: segmentation confidence changed")
    if rejected and segmentation.get("decision") != "rejected":
        errors.append(f"{rid}: rejected source boundary not preserved as rejected")
    if not rejected and segmentation.get("decision") != "accepted":
        errors.append(f"{rid}: accepted source boundary not preserved as accepted")

    diplomatic = item["layers"].get("diplomatic", {})
    if rejected:
        if diplomatic.get("text"):
            errors.append(f"{rid}: rejected boundary unexpectedly has diplomatic text")
    else:
        if diplomatic.get("text") != (src.get("article_diplomatic") or "").strip():
            errors.append(f"{rid}: diplomatic article changed")
        expected_head = (src.get("headword_diplomatic") or "").strip() or None
        if diplomatic.get("headword") != expected_head:
            errors.append(f"{rid}: diplomatic headword changed")

    # RHD 1.0 safeguard: no synthetic human event may be fabricated by this adapter.
    for event in item.get("validation", []):
        if event.get("reviewer_type") == "human":
            errors.append(f"{rid}: adapter fabricated a human validation event")

    for event in item.get("provenance", []):
        if event.get("agent_type") == "ai_system" and event.get("activity_type") == "diplomatic_transcription":
            if rejected:
                errors.append(f"{rid}: rejected boundary has diplomatic AI provenance")

# Summary must be calculable from the records, not manually asserted.
expected_summary = {
    "records_total": len(canonical),
    "active": actual_active,
    "rejected_boundary": actual_rejected,
    "candidate": sum(r.get("status") == "candidate" for r in canonical),
    "open_validation_notes": actual_open,
    "human_validation_events": 0,
}
for key, expected in expected_summary.items():
    if summary.get(key) != expected:
        errors.append(f"summary {key}={summary.get(key)} != {expected}")

# Optional full JSON Schema validation if the environment already provides jsonschema.
try:
    import jsonschema  # type: ignore
except ImportError:
    jsonschema = None

if jsonschema is not None:
    validator = jsonschema.Draft202012Validator(schema)
    for item in canonical:
        for err in validator.iter_errors(item):
            path = ".".join(str(p) for p in err.absolute_path)
            errors.append(f"{item.get('record_id')}: schema {path}: {err.message}")

if errors:
    print("\n".join("ERROR: " + e for e in errors))
    sys.exit(1)

print(
    f"OK: {len(canonical)} canonical records; {actual_active} active; "
    f"{actual_rejected} rejected boundaries; {actual_open} open-validation notes; "
    "no synthetic human validation events"
)
