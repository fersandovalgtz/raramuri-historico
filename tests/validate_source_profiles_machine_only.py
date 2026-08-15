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
if tellechea.get("project_role") != "second_source_replicability_pilot":
    errors.append("Tellechea profile must have second_source_replicability_pilot role")
credit = tellechea.get("completion_credit", {})
if credit.get("counts_toward_second_source_end_to_end_gate") is not True:
    errors.append("Tellechea full traversal must count toward second-source progress")
if credit.get("completes_second_source_end_to_end_gate") is not True:
    errors.append("Tellechea 205-page traversal must close the second-source industrialization gate")
if tellechea.get("pilot_status") != "full_witness_documentary_traversal_complete":
    errors.append("Tellechea pilot status must record complete full-witness documentary traversal")
witness = tellechea.get("witness", {})
if witness.get("identity_status") != "checksum_fixed_public_witness":
    errors.append("Tellechea witness must be checksum-fixed")
if witness.get("sha256") != "c67b7942090613c494d8057be8aff59ea13a11519c29eae469afad8a85c30dfc":
    errors.append("Tellechea witness SHA-256 differs from the fixed DGB binary")
if witness.get("facsimile_pages") != 205 or witness.get("bytes") != 95088307:
    errors.append("Tellechea fixed witness page/byte identity changed")
if witness.get("checksums_manifest") != "sources/tellechea-1826-witness.json":
    errors.append("Tellechea profile must point to the machine witness manifest")

minimal = tellechea.get("minimal_pilot_outputs", {})
if minimal.get("record_count") != 2:
    errors.append("Tellechea profile must preserve two minimal pilot records")
for key in ("canonical_jsonl", "tei", "diagnostics"):
    rel = minimal.get(key)
    if not rel or not (ROOT / rel).exists():
        errors.append(f"Tellechea minimal pilot output missing: {key}={rel}")
if minimal.get("human_validation_claimed") is not False:
    errors.append("Tellechea minimal pilot outputs must explicitly deny human validation")

full = tellechea.get("full_witness_pilot_outputs", {})
if full.get("record_count") != 205 or full.get("coverage") != "205_of_205_pdf_pages":
    errors.append("Tellechea full pilot metadata must register 205/205 documentary units")
if full.get("generated_in_ci") is not True:
    errors.append("Tellechea full outputs must be declared reproducible CI-derived artifacts")
if full.get("generator") != "scripts/generate_tellechea_full_pilot.py" or full.get("validator") != "tests/validate_tellechea_full_pilot.py":
    errors.append("Tellechea full pilot generator/validator metadata changed")
if full.get("artifact_name") != "tellechea-1826-full-witness-rhd-pilot":
    errors.append("Tellechea full pilot artifact name changed")
if full.get("rhd_core_changes_required") != 0:
    errors.append("Tellechea full pilot must record zero universal-core redesign")
if full.get("lex0_entries_generated") != 0:
    errors.append("Tellechea full pilot must record zero fabricated Lex-0 entries")
if full.get("human_validation_claimed") is not False:
    errors.append("Tellechea full pilot must explicitly deny human validation")

manifest_path = ROOT / "sources/tellechea-1826-witness.json"
if not manifest_path.exists():
    errors.append("missing Tellechea witness identity manifest")
else:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    identity = manifest.get("identity", {})
    if manifest.get("status") != "checksum_fixed_public_witness":
        errors.append("Tellechea witness manifest lost checksum-fixed status")
    if identity.get("sha256") != witness.get("sha256"):
        errors.append("Tellechea profile/witness-manifest SHA-256 mismatch")
    if identity.get("bytes") != witness.get("bytes") or identity.get("pdf_pages") != witness.get("facsimile_pages"):
        errors.append("Tellechea profile/witness-manifest size or page-count mismatch")
    if manifest.get("human_validation_claimed") is not False:
        errors.append("Tellechea witness manifest must explicitly deny human validation")

if errors:
    print("\n".join("ERROR: " + e for e in errors))
    sys.exit(1)
print("OK: reusable template and Steffel/Tellechea profiles enforce zero-required-human-adjudication; Tellechea has a checksum-fixed 205-page witness and the full documentary industrialization gate is closed with zero core redesign, zero Lex-0 fabrication and zero human-validation claim")
