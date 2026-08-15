#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
PRIORITY = ROOT / "data" / "validation" / "human_review_priority_compact.json"
PACKETS = ROOT / "data" / "validation" / "human_review_packets"
errors = []

priority = json.loads(PRIORITY.read_text(encoding="utf-8"))
expected = {row[1]: row for row in priority["records"]}
manifest_path = PACKETS / "manifest.json"
if not manifest_path.exists():
    errors.append("human review packet manifest missing")
else:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    seen = {}
    counts = {1: 0, 2: 0, 3: 0}
    for packet_meta in manifest.get("packets", []):
        path = PACKETS / packet_meta["file"]
        if not path.exists():
            errors.append(f"missing packet {packet_meta['file']}")
            continue
        packet = json.loads(path.read_text(encoding="utf-8"))
        if packet.get("human_reviewed") is not False:
            errors.append(f"{path.name}: packet must remain human_reviewed=false before review")
        if packet.get("count") != len(packet.get("records", [])):
            errors.append(f"{path.name}: count mismatch")
        for record in packet.get("records", []):
            rid = record.get("record_id")
            if rid in seen:
                errors.append(f"duplicate packet record {rid}")
            seen[rid] = path.name
            if rid not in expected:
                errors.append(f"unexpected packet record {rid}")
                continue
            exp = expected[rid]
            if record.get("priority") != exp[0] or record.get("printed_page") != exp[2]:
                errors.append(f"{rid}: priority/page changed")
            if record.get("ai_disposition") != exp[3] or record.get("recommended_review_route") != exp[4]:
                errors.append(f"{rid}: review routing changed")
            counts[exp[0]] += 1
            decision = record.get("independent_review", {})
            if decision.get("human_verified") is not False:
                errors.append(f"{rid}: blank review form must not claim human verification")
            if decision.get("reviewer", {}).get("name") is not None:
                errors.append(f"{rid}: reviewer name was prefilled")
            if decision.get("philological_decision") != "not_assessed":
                errors.append(f"{rid}: human philological decision was prefilled")
            if decision.get("linguistic_decision") != "not_assessed":
                errors.append(f"{rid}: human linguistic decision was prefilled")

    if set(seen) != set(expected):
        missing = sorted(set(expected) - set(seen))[:10]
        extra = sorted(set(seen) - set(expected))[:10]
        errors.append(f"packet universe mismatch missing={missing} extra={extra}")
    expected_counts = {1: 46, 2: 152, 3: 284}
    if counts != expected_counts:
        errors.append(f"packet priority counts {counts} != {expected_counts}")
    if manifest.get("priority_counts") != {"1": 46, "2": 152, "3": 284}:
        errors.append("packet manifest priority counts mismatch")

if errors:
    print("\n".join("ERROR: " + e for e in errors)); sys.exit(1)
print("OK: 482 human-review records packaged exactly once (46/152/284), with no human decisions prefilled")
