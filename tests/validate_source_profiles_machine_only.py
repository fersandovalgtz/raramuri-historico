#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT / "source_profiles/_template.source.json",
    ROOT / "source_profiles/steffel-1809.source.json",
    ROOT / "source_profiles/tellechea-1826.pilot-candidate.json",
]
errors = []

for path in FILES:
    if not path.exists():
        errors.append(f"missing source profile: {path.relative_to(ROOT)}")
        continue
    data = json.loads(path.read_text(encoding="utf-8"))
    label = str(path.relative_to(ROOT))
    if data.get("edition_scope") != "machine_only_scholarly_edition":
        errors.append(f"{label}: edition_scope is not machine_only_scholarly_edition")
    if data.get("human_adjudication_required") is not False:
        errors.append(f"{label}: human_adjudication_required must be false")
    validation = data.get("validation", {})
    if validation.get("policy") != "machine_only":
        errors.append(f"{label}: validation policy is not machine_only")
    if validation.get("human_review_required") is not False:
        errors.append(f"{label}: human_review_required must be false")

    serialized = json.dumps(data, ensure_ascii=False).lower()
    forbidden_requirements = [
        "declared human-review target has been independently adjudicated",
        "human review required",
        '"human_review_required": true',
        '"human_adjudication_required": true',
    ]
    for phrase in forbidden_requirements:
        if phrase in serialized:
            errors.append(f"{label}: contains forbidden human-required completion language: {phrase}")

    coverage = data.get("coverage_definition", {})
    if "critical_edition_complete_when" in coverage:
        errors.append(f"{label}: legacy human-critical completion gate remains")

steffel = json.loads(FILES[1].read_text(encoding="utf-8")) if FILES[1].exists() else {}
if steffel.get("project_role") != "reference_implementation":
    errors.append("Steffel profile lost reference_implementation role")
if steffel.get("current_documentary_state", {}).get("human_validation_claimed") is not False:
    errors.append("Steffel profile must explicitly deny human-validation claim")
if steffel.get("current_documentary_state", {}).get("confirmed_ai_assisted") != 284:
    errors.append("Steffel profile machine-state count changed: confirmed_ai_assisted")
if steffel.get("current_documentary_state", {}).get("corrected_ai_assisted") != 152:
    errors.append("Steffel profile machine-state count changed: corrected_ai_assisted")
if steffel.get("current_documentary_state", {}).get("unresolved_after_ai_recollation") != 46:
    errors.append("Steffel profile machine-state count changed: unresolved_after_ai_recollation")

tellechea = json.loads(FILES[2].read_text(encoding="utf-8")) if FILES[2].exists() else {}
if tellechea.get("project_role") != "second_source_replicability_pilot_candidate":
    errors.append("Tellechea profile lost pilot-candidate role")
if tellechea.get("completion_credit", {}).get("counts_toward_second_source_end_to_end_gate") is not False:
    errors.append("Tellechea candidate profile must not receive end-to-end completion credit before ingestion")
if tellechea.get("pilot_status") != "candidate_selected_binary_not_yet_ingested":
    errors.append("Tellechea pilot status must remain binary-not-yet-ingested until witness acquisition")

if errors:
    print("\n".join("ERROR: " + e for e in errors))
    sys.exit(1)
print("OK: reusable template, Steffel reference profile and Tellechea pilot profile all enforce zero-required-human-adjudication; pilot receives no premature replication credit")
