#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data/appendices/trilingual_visual_alignment_ai.json"
errors = []

if not PATH.exists():
    print("ERROR: trilingual visual alignment missing")
    sys.exit(1)

data = json.loads(PATH.read_text(encoding="utf-8"))
if data.get("human_verified") is not False:
    errors.append("visual alignment must not claim human verification")
if data.get("language_order") != ["la", "de", "und"]:
    errors.append("language order must be la/de/und")
formulas = data.get("formulas", [])
if len(formulas) != 22:
    errors.append(f"expected 22 formulas, got {len(formulas)}")
if [f.get("formula") for f in formulas] != list(range(1, 23)):
    errors.append("formula sequence is not 1..22")

for item in formulas:
    n = item.get("formula")
    expected_pp = 371 if n <= 4 else 372 if n <= 11 else 373 if n <= 18 else 374
    if item.get("printed_page") != expected_pp or item.get("pdf_page") != expected_pp - 290:
        errors.append(f"formula {n}: facsimile mapping mismatch")
    for field in ("latin", "german", "tarahumara"):
        if not isinstance(item.get(field), str) or not item[field].strip():
            errors.append(f"formula {n}: missing {field}")
    confidence = item.get("confidence", {})
    if set(confidence) != {"la", "de", "und"}:
        errors.append(f"formula {n}: incomplete confidence fields")
    if any(v not in {"high", "medium", "low"} for v in confidence.values()):
        errors.append(f"formula {n}: invalid confidence label")
    if confidence.get("und") == "low" and not item.get("uncertain_segments"):
        errors.append(f"formula {n}: low-confidence Tarahumara lacks explicit uncertainty note")

summary = data.get("summary", {})
if summary.get("formula_count") != 22 or summary.get("formula_alignment_complete") is not True:
    errors.append("summary does not declare complete 22-formula alignment")
if summary.get("human_validation_claimed") is not False:
    errors.append("summary fabricates human validation")
if summary.get("tarahumara_low_confidence_formulas") != [13, 21]:
    errors.append("low-confidence formula inventory differs from records")

if errors:
    print("\n".join("ERROR: " + e for e in errors))
    sys.exit(1)
print("OK: 22 formulas have la/de/und AI visual alignment, exact page mapping, confidence fields and explicit low-confidence uncertainty")
