#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, re, sys

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"dist/rhd-steffel-release-manifest.json"
errors=[]
if not MANIFEST.exists(): print("ERROR: release manifest missing"); sys.exit(1)
manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
if manifest.get("human_validation_claimed") is not False: errors.append("manifest must explicitly deny human-validation claim")
if "machine-only" not in (manifest.get("release_scope") or ""): errors.append("release scope does not declare machine-only edition")
files=manifest.get("files",[])
if len(files)<34: errors.append(f"too few release artifacts: {len(files)}")
paths=[x.get("path") for x in files]
if len(paths)!=len(set(paths)): errors.append("duplicate path in release manifest")
required=(
 "sources/external-references.json","sources/tellechea-1826-witness.json","data/iiif/steffel-1809-local-page-fingerprints.json",
 "data/research/diachronic_machine_scores.json","data/appendices/numeration_visual_structure_ai.json",
 "data/appendices/trilingual_visual_alignment_ai.json","data/appendices/prayer_visual_transcription_ai.json",
 "data/tei/rhd-steffel-1809-appendices-tei.xml","source_profiles/_template.source.json",
 "source_profiles/tellechea-1826.pilot-candidate.json","data/pilot/tellechea-1826.minimal-pilot.jsonl",
 "data/pilot/tellechea-1826.minimal-pilot.tei.xml","data/pilot/tellechea-1826.minimal-pilot.diagnostics.json",
 "data/pilot/tellechea-1826.full-witness.jsonl","data/pilot/tellechea-1826.full-witness.tei.xml",
 "data/pilot/tellechea-1826.full-witness.diagnostics.json","docs/SECOND_SOURCE_PILOT_TELLECHEA_1826.md",
 "docs/RHD_1_0_MACHINE_ONLY_CONFORMITY.md","docs/MACHINE_ONLY_COMPLETION_MATRIX.md")
for p in required:
    if p not in paths: errors.append(f"required release artifact absent: {p}")
for item in files:
    rel=item.get("path"); path=ROOT/str(rel)
    if not path.exists(): errors.append(f"manifest path missing: {rel}"); continue
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    if digest!=item.get("sha256"): errors.append(f"sha256 mismatch: {rel}")
    if not re.fullmatch(r"[0-9a-f]{64}",item.get("sha256") or ""): errors.append(f"invalid sha256 format: {rel}")
    if path.stat().st_size!=item.get("bytes"): errors.append(f"byte count mismatch: {rel}")

counts=manifest.get("counts",{})
canonical_count=sum(1 for line in (ROOT/"data/canonical/steffel-1809.entries.jsonl").read_text(encoding="utf-8").splitlines() if line.strip())
appendix=json.loads((ROOT/"data/canonical/steffel-1809.appendices.json").read_text(encoding="utf-8")); appendix_count=len(appendix.get("objects",[]))
checks={
 "canonical_lexical_records":canonical_count,"canonical_appendix_objects":24,"trilingual_formula_blocks":22,
 "trilingual_formula_blocks_machine_aligned":22,"prayer_visual_transcriptions":1,"appendix_facsimile_pages_mapped":6,
 "diachronic_documentary_candidates_scored":298,"canonical_working_witnesses":1,
 "second_source_pilot_witnesses_checksum_fixed":1,"second_source_minimal_pilots_complete":1,
 "second_source_minimal_canonical_records":2,"second_source_pilots_full_witness_end_to_end_complete":1,
 "second_source_full_witness_canonical_records":205}
for key,val in checks.items():
    if counts.get(key)!=val: errors.append(f"release manifest count mismatch {key}: expected {val}, got {counts.get(key)}")
if appendix_count!=24: errors.append(f"canonical appendix object count changed: {appendix_count}")
if not isinstance(counts.get("structured_primary_numeral_examples"),int) or counts.get("structured_primary_numeral_examples")<30: errors.append("release manifest must report at least 30 structured primary numeral examples")
if counts.get("registered_noncanonical_external_witnesses",0)<1: errors.append("release manifest must report at least one explicitly noncanonical external witness")

registry=json.loads((ROOT/"sources/external-references.json").read_text(encoding="utf-8"))
ia=next((w for w in registry.get("witnesses",[]) if w.get("witness_id")=="IA-tarahumarischesw00stef"),None)
if ia is None or ia.get("canonical_for_rhd") is not False: errors.append("Internet Archive parallel witness must remain explicitly noncanonical")
if ia and ((ia.get("identity_comparison") or {}).get("result")!="strong_mismatch_not_verified_as_same_scan"): errors.append("Internet Archive witness registry lost strong mismatch result")

pilot=json.loads((ROOT/"source_profiles/tellechea-1826.pilot-candidate.json").read_text(encoding="utf-8"))
pilot_witness=json.loads((ROOT/"sources/tellechea-1826-witness.json").read_text(encoding="utf-8"))
credit=pilot.get("completion_credit",{})
if credit.get("counts_toward_second_source_end_to_end_gate") is not True: errors.append("Tellechea pilot must count toward second-source progress")
if credit.get("completes_second_source_end_to_end_gate") is not True: errors.append("Tellechea complete traversal must close second-source gate")
fixed_sha="c67b7942090613c494d8057be8aff59ea13a11519c29eae469afad8a85c30dfc"
if pilot.get("witness",{}).get("sha256")!=fixed_sha: errors.append("Tellechea profile lost fixed witness SHA-256")
if pilot_witness.get("identity",{}).get("sha256")!=fixed_sha: errors.append("Tellechea witness manifest checksum mismatch")
full_diag=json.loads((ROOT/"data/pilot/tellechea-1826.full-witness.diagnostics.json").read_text(encoding="utf-8"))
if full_diag.get("canonical_records")!=205 or full_diag.get("pdf_pages")!=205: errors.append("Tellechea full diagnostics must prove 205/205 traversal")
if full_diag.get("rhd_core_changes_required")!=[]: errors.append("Tellechea full traversal required universal-core redesign")
if full_diag.get("lex0_entries_generated")!=0: errors.append("Tellechea full traversal fabricated Lex-0 entries")
if full_diag.get("human_validation_claimed") is not False: errors.append("Tellechea full traversal fabricated human validation")

second=manifest.get("second_source_pilot",{})
if second.get("witness_sha256")!=fixed_sha: errors.append("release manifest second-source witness checksum mismatch")
if second.get("minimal_end_to_end_completion_credit") is not True: errors.append("release manifest lost minimal Tellechea proof")
if second.get("full_witness_end_to_end_completion_credit") is not True: errors.append("release manifest must record closed full-witness Tellechea gate")
if second.get("full_witness_canonical_records")!=205 or second.get("full_witness_pdf_pages")!=205: errors.append("release manifest full-witness Tellechea coverage mismatch")
if second.get("full_witness_rhd_core_changes_required")!=0: errors.append("release manifest must report zero RHD core redesign for Tellechea")
if second.get("full_witness_lex0_entries_generated")!=0: errors.append("release manifest must report zero Lex-0 fabrication for Tellechea")

completion=json.loads((ROOT/"project/completion-model-machine-only.json").read_text(encoding="utf-8"))
if manifest.get("completion",{}).get("weighted_completion_percent")!=completion.get("weighted_completion_percent"): errors.append("completion percentage differs from machine-only completion model")
if manifest.get("completion",{}).get("weighted_remaining_percent")!=completion.get("weighted_remaining_percent"): errors.append("remaining percentage differs from machine-only completion model")
if completion.get("weighted_completion_percent")!=93.0 or completion.get("weighted_remaining_percent")!=7.0: errors.append("completion model must be 93/7 after closing second-source gate")

if errors: print("\n".join("ERROR: "+e for e in errors)); sys.exit(1)
print(f"OK: release manifest verifies {len(files)} artifacts, {canonical_count} Steffel lexical records, {appendix_count} appendix objects, 298 documentary-scored diachronic candidates, and complete 205/205 Tellechea industrialization with zero core redesign, zero Lex-0 fabrication and zero human-validation claim; weighted completion=93.0%")
