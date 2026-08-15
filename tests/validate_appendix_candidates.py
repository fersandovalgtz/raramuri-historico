#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
NUM = ROOT / "data" / "appendices" / "numeration_ocr_candidates.json"
SAMPLE = ROOT / "data" / "appendices" / "trilingual_sample_ocr_candidates.json"
errors = []

for path in (NUM, SAMPLE):
    if not path.exists():
        errors.append(f"missing {path.relative_to(ROOT)}")
if errors:
    print("\n".join("ERROR: " + e for e in errors)); sys.exit(1)

num = json.loads(NUM.read_text(encoding="utf-8"))
sample = json.loads(SAMPLE.read_text(encoding="utf-8"))

if num.get("collection_id") != "RHD-S1809-APP-NUMERATION":
    errors.append("numeration collection id mismatch")
if num.get("facsimile_verified") is not False or num.get("human_verified") is not False:
    errors.append("numeration OCR layer prematurely claims verification")
if num.get("normalization_performed") is not False or num.get("linguistic_analysis_performed") is not False:
    errors.append("numeration OCR layer prematurely claims normalization/analysis")
num_candidates = num.get("numbered_expression_candidates", [])
if len(num_candidates) < 20:
    errors.append(f"implausibly small numeration OCR candidate inventory: {len(num_candidates)}")
if len({x.get('candidate_id') for x in num_candidates}) != len(num_candidates):
    errors.append("duplicate numeration candidate id")
for item in num_candidates:
    if item.get("status") != "ocr_structured_candidate":
        errors.append(f"{item.get('candidate_id')}: wrong status")
    if item.get("facsimile_verified") is not False or item.get("human_verified") is not False:
        errors.append(f"{item.get('candidate_id')}: premature verification")

if sample.get("collection_id") != "RHD-S1809-APP-TRILINGUAL-SAMPLE":
    errors.append("sample collection id mismatch")
if sample.get("formula_count") != 22:
    errors.append(f"expected 22 formula blocks, got {sample.get('formula_count')}")
formulas = sample.get("formulas", [])
if len(formulas) != 22:
    errors.append(f"formula array length {len(formulas)} != 22")
expected_ids = [f"RHD-S1809-SAMPLE-{i:02d}" for i in range(1, 23)]
if [x.get("record_id") for x in formulas] != expected_ids:
    errors.append("formula IDs/order differ from 01–22")
last_end = -1
for index, item in enumerate(formulas, 1):
    if item.get("formula_number_editorial") != index:
        errors.append(f"formula {index}: editorial number mismatch")
    if item.get("status") != "ocr_structured_candidate":
        errors.append(f"formula {index}: wrong status")
    if item.get("language_alignment_verified") is not False:
        errors.append(f"formula {index}: language alignment prematurely verified")
    if item.get("facsimile_verified") is not False or item.get("human_verified") is not False:
        errors.append(f"formula {index}: premature verification")
    start = item.get("source_ocr_line_start")
    end = item.get("source_ocr_line_end")
    if not isinstance(start, int) or not isinstance(end, int) or start > end:
        errors.append(f"formula {index}: invalid source range")
    if start <= last_end:
        errors.append(f"formula {index}: overlaps or is out of source order")
    last_end = end

prayer = sample.get("lord_prayer", {})
if prayer.get("record_id") != "RHD-S1809-PRAYER-01":
    errors.append("Lord's Prayer record missing")
if prayer.get("facsimile_verified") is not False or prayer.get("human_verified") is not False:
    errors.append("Lord's Prayer prematurely verified")
if prayer.get("source_ocr_line_start", 0) <= last_end:
    errors.append("Lord's Prayer does not follow formula 22")

if errors:
    print("\n".join("ERROR: " + e for e in errors)); sys.exit(1)
print(
    f"OK: numeration has {len(num_candidates)} OCR-number candidates; trilingual sample has 22 ordered blocks plus separate Lord's Prayer; no facsimile/human verification fabricated"
)
