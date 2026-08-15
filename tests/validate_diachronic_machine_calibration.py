#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data/research/diachronic_machine_calibration.json"
errors = []
if not PATH.exists():
    print("ERROR: diachronic machine calibration missing"); sys.exit(1)

data = json.loads(PATH.read_text(encoding="utf-8"))
if data.get("candidate_count") != 298:
    errors.append(f"expected 298 candidates, got {data.get('candidate_count')}")
if data.get("null_pair_count") != 298 * 17:
    errors.append(f"expected {298*17} null pairs, got {data.get('null_pair_count')}")
if len(data.get("records", [])) != 298:
    errors.append("calibration record count differs from candidate universe")
if len(data.get("null_by_shift", [])) != 17:
    errors.append("calibration must contain 17 deterministic null shifts")
if data.get("scope") != "graphemic_retrieval_specificity_only":
    errors.append("calibration scope is not explicitly graphemic-only")
for key in ("automatic_semantic_judgment", "automatic_cognacy_judgment", "automatic_etymological_judgment", "automatic_historical_continuity_judgment", "human_reviewed"):
    if data.get(key) is not False:
        errors.append(f"top-level forbidden promotion: {key}")

summary = data.get("summary", {})
obs = summary.get("observed_mean_sequence_ratio")
null = summary.get("null_mean_sequence_ratio")
if not isinstance(obs, (int, float)) or not isinstance(null, (int, float)):
    errors.append("missing observed/null mean calibration statistics")
if isinstance(obs, (int, float)) and isinstance(null, (int, float)):
    if abs(summary.get("mean_ratio_lift_over_null", 999) - (obs-null)) > 0.00001:
        errors.append("reported mean ratio lift is inconsistent")

allowed_buckets = {
    "very_high_graphemic_specificity", "high_graphemic_specificity",
    "moderate_graphemic_specificity", "low_graphemic_specificity"
}
for r in data.get("records", []):
    if r.get("relation_status") != "candidate":
        errors.append(f"{r.get('semantic_context_id')}: relation promoted beyond candidate")
    if r.get("calibration_scope") != "graphemic_retrieval_specificity_only":
        errors.append(f"{r.get('semantic_context_id')}: scope changed")
    if r.get("graphemic_specificity_bucket") not in allowed_buckets:
        errors.append(f"{r.get('semantic_context_id')}: invalid specificity bucket")
    p = r.get("null_empirical_percentile")
    tail = r.get("null_empirical_upper_tail")
    if not isinstance(p, (int, float)) or not 0 <= p <= 1:
        errors.append(f"{r.get('semantic_context_id')}: bad empirical percentile")
    if not isinstance(tail, (int, float)) or not 0 < tail <= 1:
        errors.append(f"{r.get('semantic_context_id')}: bad empirical upper tail")
    for key in ("semantic_probability", "cognacy_probability", "etymological_probability", "historical_continuity_probability"):
        if r.get(key) is not None:
            errors.append(f"{r.get('semantic_context_id')}: fabricated {key}")
    if r.get("human_reviewed") is not False:
        errors.append(f"{r.get('semantic_context_id')}: fabricated human review")

serialized = PATH.read_text(encoding="utf-8").lower()
for forbidden in ("cognacy confirmed", "etymology confirmed", "semantic identity confirmed", "sound law confirmed"):
    if forbidden in serialized:
        errors.append(f"forbidden claim in calibration: {forbidden}")

if errors:
    print("\n".join("ERROR: " + e for e in errors)); sys.exit(1)
print(
    f"OK: 298 candidates calibrated against {data.get('null_pair_count')} deterministic broken-pair controls; "
    f"observed mean={obs}, null mean={null}; all relations remain candidate and all semantic/etymological probabilities remain null"
)
