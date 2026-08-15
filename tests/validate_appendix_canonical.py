#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data/canonical/steffel-1809.appendices.json"
errors = []

if not PATH.exists():
    print("ERROR: canonical appendix layer missing")
    sys.exit(1)

data = json.loads(PATH.read_text(encoding="utf-8"))
if data.get("schema_id") != "RHD-APPENDIX-CANONICAL-1.0":
    errors.append("schema_id mismatch")
if data.get("human_validation_claimed") is not False:
    errors.append("canonical appendices must not claim human validation")
objects = data.get("objects", [])
if len(objects) != 24:
    errors.append(f"expected 24 appendix objects, got {len(objects)}")
ids = [x.get("object_id") for x in objects]
if len(ids) != len(set(ids)):
    errors.append("duplicate appendix object_id")

numeration = [x for x in objects if x.get("object_type") == "appendix_numeration"]
formulas = [x for x in objects if x.get("object_type") == "parallel_formula"]
prayers = [x for x in objects if x.get("object_type") == "prayer_text"]
if len(numeration) != 1 or len(formulas) != 22 or len(prayers) != 1:
    errors.append(f"object type counts wrong: numeration={len(numeration)}, formulas={len(formulas)}, prayers={len(prayers)}")
if [x.get("sequence") for x in formulas] != list(range(1, 23)):
    errors.append("formula sequence is not exactly 1..22")

expected_page = {}
for i in range(1, 23):
    expected_page[i] = 371 if i <= 4 else 372 if i <= 11 else 373 if i <= 18 else 374
for item in formulas:
    n = item["sequence"]
    pp = item.get("printed_page")
    pdf = item.get("pdf_page")
    if pp != expected_page[n]:
        errors.append(f"formula {n}: printed page {pp} != {expected_page[n]}")
    if pdf != pp - 290:
        errors.append(f"formula {n}: pdf/printed page mapping inconsistent")
    if item.get("language_alignment_verified") is not False:
        errors.append(f"formula {n}: language alignment prematurely verified")
    if item.get("human_verified") is not False:
        errors.append(f"formula {n}: human verification fabricated")
    visual = item.get("layers", {}).get("visual_collation", {})
    if visual.get("status") != "confirmed_ai_assisted" or visual.get("human_verified") is not False:
        errors.append(f"formula {n}: visual collation status invalid")

mapping = data.get("facsimile_mapping", {}).get("mapping", [])
expected_mapping = [(79,369),(80,370),(81,371),(82,372),(83,373),(84,374)]
if [(x.get("pdf_page"), x.get("printed_page")) for x in mapping] != expected_mapping:
    errors.append("facsimile page mapping differs from verified 79–84 / 369–374 sequence")

if errors:
    print("\n".join("ERROR: " + e for e in errors))
    sys.exit(1)
print("OK: canonical appendix layer has 24 machine-only objects, 22 ordered formulas and exact facsimile page mapping")
