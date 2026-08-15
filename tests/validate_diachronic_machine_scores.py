#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data/research/diachronic_machine_scores.json"
QUEUE = ROOT / "data/research/diachronic_semantic_context_queue.json"
errors = []

if not PATH.exists():
    print("ERROR: diachronic machine score layer missing")
    sys.exit(1)

data = json.loads(PATH.read_text(encoding="utf-8"))
queue = json.loads(QUEUE.read_text(encoding="utf-8"))
records = data.get("records", [])
if data.get("count") != 298 or len(records) != 298:
    errors.append(f"expected 298 scored candidates, got declared={data.get('count')} actual={len(records)}")
if len(queue.get("records", [])) != len(records):
    errors.append("score layer does not cover source queue exactly")
for key in (
    "automatic_semantic_judgment",
    "automatic_cognacy_judgment",
    "automatic_etymological_judgment",
    "automatic_historical_continuity_judgment",
    "human_reviewed",
):
    if data.get(key) is not False:
        errors.append(f"top-level safeguard {key} must be false")

ids = [x.get("semantic_context_id") for x in records]
if len(ids) != len(set(ids)):
    errors.append("duplicate semantic_context_id in score layer")
source_ids = {x.get("semantic_context_id") for x in queue.get("records", [])}
if set(ids) != source_ids:
    errors.append("score layer IDs differ from source queue")

allowed_buckets = {"high_documentary_support", "medium_documentary_support", "low_documentary_support"}
for item in records:
    rid = item.get("semantic_context_id")
    score = item.get("documentary_support_score")
    if not isinstance(score, (int, float)) or not 0 <= score <= 0.99:
        errors.append(f"{rid}: invalid score {score}")
    if item.get("support_bucket") not in allowed_buckets:
        errors.append(f"{rid}: invalid support bucket")
    if item.get("relation_status") != "candidate":
        errors.append(f"{rid}: relation promoted beyond candidate")
    if item.get("score_scope") != "documentary_retrieval_support_only":
        errors.append(f"{rid}: score scope changed")
    for field in (
        "semantic_probability",
        "cognacy_probability",
        "etymological_probability",
        "historical_continuity_probability",
    ):
        if item.get(field) is not None:
            errors.append(f"{rid}: fabricated {field}")
    if item.get("human_reviewed") is not False:
        errors.append(f"{rid}: fabricated human review")

bucket_total = sum(data.get("summary", {}).get("support_buckets", {}).values())
if bucket_total != 298:
    errors.append(f"support bucket total {bucket_total} != 298")

if errors:
    print("\n".join("ERROR: " + e for e in errors))
    sys.exit(1)
print(f"OK: 298 diachronic candidates scored for documentary retrieval support only; all remain candidate with zero semantic/cognacy/continuity claims")
