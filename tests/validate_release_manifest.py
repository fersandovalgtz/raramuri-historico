#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "dist/rhd-steffel-release-manifest.json"
errors = []

if not MANIFEST.exists():
    print("ERROR: release manifest missing")
    sys.exit(1)

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
if manifest.get("human_validation_claimed") is not False:
    errors.append("manifest must explicitly deny human-validation claim")
if "machine-only" not in (manifest.get("release_scope") or ""):
    errors.append("release scope does not declare machine-only edition")
files = manifest.get("files", [])
if len(files) < 31:
    errors.append(f"too few release artifacts: {len(files)}")
paths = [x.get("path") for x in files]
if len(paths) != len(set(paths)):
    errors.append("duplicate path in release manifest")
for required_path in (
    "sources/external-references.json",
    "sources/tellechea-1826-witness.json",
    "data/iiif/steffel-1809-local-page-fingerprints.json",
    "data/research/diachronic_machine_scores.json",
    "data/appendices/numeration_visual_structure_ai.json",
    "data/appendices/trilingual_visual_alignment_ai.json",
    "data/appendices/prayer_visual_transcription_ai.json",
    "data/tei/rhd-steffel-1809-appendices-tei.xml",
    "source_profiles/_template.source.json",
    "source_profiles/tellechea-1826.pilot-candidate.json",
    "data/pilot/tellechea-1826.minimal-pilot.jsonl",
    "data/pilot/tellechea-1826.minimal-pilot.tei.xml",
    "data/pilot/tellechea-1826.minimal-pilot.diagnostics.json",
    "docs/SECOND_SOURCE_PILOT_TELLECHEA_1826.md",
    "docs/RHD_1_0_MACHINE_ONLY_CONFORMITY.md",
    "docs/MACHINE_ONLY_COMPLETION_MATRIX.md",
):
    if required_path not in paths:
        errors.append(f"required release artifact absent: {required_path}")

for item in files:
    rel = item.get("path")
    path = ROOT / str(rel)
    if not path.exists():
        errors.append(f"manifest path missing: {rel}")
        continue
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != item.get("sha256"):
        errors.append(f"sha256 mismatch: {rel}")
    if not re.fullmatch(r"[0-9a-f]{64}", item.get("sha256") or ""):
        errors.append(f"invalid sha256 format: {rel}")
    if path.stat().st_size != item.get("bytes"):
        errors.append(f"byte count mismatch: {rel}")

counts = manifest.get("counts", {})
canonical = ROOT / "data/canonical/steffel-1809.entries.jsonl"
canonical_count = sum(1 for line in canonical.read_text(encoding="utf-8").splitlines() if line.strip())
appendix = json.loads((ROOT / "data/canonical/steffel-1809.appendices.json").read_text(encoding="utf-8"))
appendix_count = len(appendix.get("objects", []))
if counts.get("canonical_lexical_records") != canonical_count:
    errors.append("canonical lexical record count mismatch")
if counts.get("canonical_appendix_objects") != appendix_count or appendix_count != 24:
    errors.append(f"canonical appendix object count mismatch: manifest={counts.get('canonical_appendix_objects')} actual={appendix_count}")
if counts.get("trilingual_formula_blocks") != 22:
    errors.append("release manifest must report 22 trilingual formula blocks")
if counts.get("trilingual_formula_blocks_machine_aligned") != 22:
    errors.append("release manifest must report 22 machine-aligned trilingual formula blocks")
if not isinstance(counts.get("structured_primary_numeral_examples"), int) or counts.get("structured_primary_numeral_examples") < 30:
    errors.append("release manifest must report at least 30 structured primary numeral examples")
if counts.get("prayer_visual_transcriptions") != 1:
    errors.append("release manifest must report one AI visual prayer transcription")
if counts.get("appendix_facsimile_pages_mapped") != 6:
    errors.append("release manifest must report six mapped appendix facsimile pages")
if counts.get("diachronic_documentary_candidates_scored") != 298:
    errors.append("release manifest must report 298 documentary-scored diachronic candidates")
if counts.get("canonical_working_witnesses") != 1:
    errors.append("release manifest must report exactly one checksum-fixed canonical working witness")
if counts.get("registered_noncanonical_external_witnesses") < 1:
    errors.append("release manifest must report at least one explicitly noncanonical external witness")
if counts.get("second_source_pilot_witnesses_checksum_fixed") != 1:
    errors.append("release manifest must report exactly one checksum-fixed second-source pilot witness")
if counts.get("second_source_minimal_pilots_complete") != 1:
    errors.append("release manifest must report one real completed minimal second-source pipeline")
if counts.get("second_source_minimal_canonical_records") != 2:
    errors.append("Tellechea minimal pilot must contribute exactly two canonical documentary records")
if counts.get("second_source_pilots_full_witness_end_to_end_complete") != 0:
    errors.append("minimal Tellechea pilot must not be confused with full-witness industrialization")

registry = json.loads((ROOT / "sources/external-references.json").read_text(encoding="utf-8"))
ia = next((w for w in registry.get("witnesses", []) if w.get("witness_id") == "IA-tarahumarischesw00stef"), None)
if ia is None or ia.get("canonical_for_rhd") is not False:
    errors.append("Internet Archive parallel witness must remain explicitly noncanonical")
if ia and ((ia.get("identity_comparison") or {}).get("result") != "strong_mismatch_not_verified_as_same_scan"):
    errors.append("Internet Archive witness registry lost the machine fingerprint mismatch result")

pilot = json.loads((ROOT / "source_profiles/tellechea-1826.pilot-candidate.json").read_text(encoding="utf-8"))
pilot_witness = json.loads((ROOT / "sources/tellechea-1826-witness.json").read_text(encoding="utf-8"))
credit = pilot.get("completion_credit", {})
if credit.get("counts_toward_second_source_end_to_end_gate") is not True:
    errors.append("Tellechea real minimal pilot must count toward second-source progress")
if credit.get("completes_second_source_end_to_end_gate") is not False:
    errors.append("Tellechea minimal pilot must not close the full-witness gate")
if pilot.get("witness", {}).get("sha256") != "c67b7942090613c494d8057be8aff59ea13a11519c29eae469afad8a85c30dfc":
    errors.append("Tellechea profile lost fixed witness SHA-256")
if pilot_witness.get("identity", {}).get("sha256") != pilot.get("witness", {}).get("sha256"):
    errors.append("Tellechea profile and witness manifest disagree on checksum")
second = manifest.get("second_source_pilot", {})
if second.get("witness_sha256") != pilot.get("witness", {}).get("sha256"):
    errors.append("release manifest second-source witness checksum mismatch")
if second.get("minimal_end_to_end_completion_credit") is not True:
    errors.append("release manifest must record successful minimal Tellechea pipeline traversal")
if second.get("full_witness_end_to_end_completion_credit") is not False:
    errors.append("release manifest must keep full-witness Tellechea gate open")
if second.get("canonical_records") != 2:
    errors.append("release manifest Tellechea canonical-record count mismatch")

completion = json.loads((ROOT / "project/completion-model-machine-only.json").read_text(encoding="utf-8"))
if manifest.get("completion", {}).get("weighted_completion_percent") != completion.get("weighted_completion_percent"):
    errors.append("completion percentage differs from machine-only completion model")
if manifest.get("completion", {}).get("weighted_remaining_percent") != completion.get("weighted_remaining_percent"):
    errors.append("remaining percentage differs from machine-only completion model")

if errors:
    print("\n".join("ERROR: " + e for e in errors))
    sys.exit(1)
print(
    f"OK: release manifest verifies {len(files)} artifacts, {canonical_count} Steffel lexical records, "
    f"{appendix_count} canonical appendix objects, 22 machine-aligned formula triples, "
    f"{counts.get('structured_primary_numeral_examples')} structured numeral examples, one prayer transcription, "
    f"six facsimile page mappings, 298 documentary-scored diachronic candidates, one canonical Steffel witness, "
    f"{counts.get('registered_noncanonical_external_witnesses')} noncanonical Steffel witness(es), and a real two-record "
    "Tellechea minimal end-to-end pipeline while full-witness industrialization remains open"
)
