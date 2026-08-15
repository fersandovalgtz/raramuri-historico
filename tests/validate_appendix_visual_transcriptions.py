#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
PRAYER = ROOT / "data/appendices/prayer_visual_transcription_ai.json"
NUM = ROOT / "data/appendices/numeration_visual_structure_ai.json"
errors = []

for path in (PRAYER, NUM):
    if not path.exists():
        errors.append(f"missing {path.relative_to(ROOT)}")
if errors:
    print("\n".join("ERROR: " + e for e in errors)); sys.exit(1)

prayer = json.loads(PRAYER.read_text(encoding="utf-8"))
if prayer.get("record_id") != "RHD-S1809-PRAYER-01":
    errors.append("prayer record id mismatch")
if prayer.get("human_verified") is not False:
    errors.append("prayer fabricates human verification")
if prayer.get("status") != "ai_visual_transcription_candidate":
    errors.append("prayer status invalid")
if prayer.get("confidence") not in {"high", "medium", "low"}:
    errors.append("prayer confidence missing")
if not (prayer.get("text") or "").strip().endswith("Amen."):
    errors.append("prayer transcription is empty or does not reach Amen")
if not prayer.get("uncertain_segments"):
    errors.append("prayer must preserve explicit uncertain segments")

num = json.loads(NUM.read_text(encoding="utf-8"))
if num.get("human_verified") is not False:
    errors.append("numeration layer fabricates human verification")
if num.get("status") != "machine_structured_candidate":
    errors.append("numeration status invalid")
cardinals = num.get("primary_cardinals", [])
if len(cardinals) < 30:
    errors.append(f"too few primary cardinal examples: {len(cardinals)}")
values = {x.get("value") for x in cardinals}
for required in (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,30,40,50,60,70,80,90,100,1000):
    if required not in values:
        errors.append(f"numeration primary inventory missing value {required}")
mult = num.get("multiplicatives", [])
if [x.get("times") for x in mult] != list(range(1,11)):
    errors.append("multiplicative sequence is not 1..10")
ordinals = num.get("ordinals", [])
if [x.get("ordinal") for x in ordinals] != [1,2,3,4,5]:
    errors.append("ordinal sequence is not 1..5")
obs = num.get("source_observations", {})
if obs.get("counting_systems_declared_by_source") != 4:
    errors.append("source counting-system count must remain 4")
if obs.get("machine_linguistic_inference_performed") is not False:
    errors.append("numeration layer fabricates linguistic inference")
for collection_name in ("primary_cardinals","secondary_counting_system_examples","third_counting_system_examples","fourth_counting_system_examples","multiplicatives","other_number_words","ordinals"):
    for item in num.get(collection_name, []):
        if item.get("confidence") not in {"high", "medium", "low"}:
            errors.append(f"{collection_name}: invalid confidence")
        if item.get("confidence") == "low" and "?" in (item.get("form") or "") and not item.get("uncertainty"):
            errors.append(f"{collection_name}: question-mark candidate lacks uncertainty explanation")

if errors:
    print("\n".join("ERROR: " + e for e in errors)); sys.exit(1)
print(f"OK: prayer visual transcription preserves uncertainty; numeration structure contains {len(cardinals)} primary examples, 10 multiplicatives, 5 ordinals and four declared counting systems")
