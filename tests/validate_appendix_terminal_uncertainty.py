#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data/appendices/terminal_uncertainty_register.json"
errors = []
if not PATH.exists():
    print("ERROR: terminal appendix uncertainty register missing"); sys.exit(1)

data = json.loads(PATH.read_text(encoding="utf-8"))
items = data.get("items", [])
if data.get("scope") != "machine_only_appendix_terminal_uncertainty":
    errors.append("wrong uncertainty-register scope")
if data.get("human_review_required") is not False or data.get("human_validation_claimed") is not False:
    errors.append("appendix uncertainty register reintroduced human requirement/claim")
if data.get("all_items_terminal") is not True:
    errors.append("not all appendix uncertainties are terminal")
if data.get("summary", {}).get("count") != len(items):
    errors.append("uncertainty summary count mismatch")
if len(items) < 10:
    errors.append(f"implausibly small residual uncertainty inventory: {len(items)}")
if len({x.get('uncertainty_id') for x in items}) != len(items):
    errors.append("duplicate appendix uncertainty ID")

allowed_sources = {
    "trilingual_visual_alignment_ai",
    "numeration_visual_structure_ai",
    "prayer_visual_transcription_ai",
}
for item in items:
    uid = item.get("uncertainty_id")
    if item.get("source_layer") not in allowed_sources:
        errors.append(f"{uid}: unknown source layer")
    if item.get("confidence") not in {"medium", "low"}:
        errors.append(f"{uid}: terminal register should contain only medium/low items")
    if item.get("terminal_status") != "explicit_machine_uncertainty":
        errors.append(f"{uid}: uncertainty not terminalized explicitly")
    if item.get("resolution_required_for_machine_only_completion") is not False:
        errors.append(f"{uid}: incorrectly blocks machine-only completion")
    if item.get("human_review_required") is not False:
        errors.append(f"{uid}: human review requirement fabricated")
    if item.get("normalization_or_repair_performed") is not False:
        errors.append(f"{uid}: speculative repair performed")

if errors:
    print("\n".join("ERROR: " + e for e in errors)); sys.exit(1)
print(f"OK: {len(items)} residual appendix readings are explicitly preserved as terminal machine uncertainty; no repair or human gate is required")
