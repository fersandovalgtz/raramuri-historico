#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, re, sys

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"dist/rhd-steffel-release-manifest.json"; errors=[]
if not MANIFEST.exists(): print("ERROR: release manifest missing"); sys.exit(1)
manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
if manifest.get("human_validation_claimed") is not False: errors.append("manifest must explicitly deny human-validation claim")
if "machine-only" not in (manifest.get("release_scope") or ""): errors.append("release scope does not declare machine-only edition")
files=manifest.get("files",[]); paths=[x.get("path") for x in files]
if len(files)<45: errors.append(f"too few hashed prerelease artifacts: {len(files)}")
if len(paths)!=len(set(paths)): errors.append("duplicate path in release manifest")

required=(
 "CITATION.cff","CHANGELOG.md","DATA_LICENSE.md","PROVENANCE.md",
 "sources/external-references.json","sources/tellechea-1826-witness.json",
 "data/iiif/steffel-1809-local-page-fingerprints.json","data/iiif/steffel-1809-all84-page-fingerprints.json",
 "data/iiif/steffel-1809-canonical-canvas-dimensions.json","data/iiif/steffel-1809-published-png72-assets.json",
 "docs/IIIF_READINESS.md","docs/IIIF_PUBLICATION_GITHUB_PAGES.md","docs/RELEASE_READINESS_RHD_1_0.md",
 "data/research/diachronic_machine_scores.json","data/research/diachronic_machine_calibration.json",
 "data/appendices/numeration_visual_structure_ai.json","data/appendices/trilingual_visual_alignment_ai.json",
 "data/appendices/prayer_visual_transcription_ai.json","data/appendices/terminal_uncertainty_register.json",
 "data/tei/rhd-steffel-1809-appendices-tei.xml","source_profiles/_template.source.json",
 "source_profiles/tellechea-1826.pilot-candidate.json","data/pilot/tellechea-1826.minimal-pilot.jsonl",
 "data/pilot/tellechea-1826.minimal-pilot.tei.xml","data/pilot/tellechea-1826.minimal-pilot.diagnostics.json",
 "data/pilot/tellechea-1826.full-witness.jsonl","data/pilot/tellechea-1826.full-witness.tei.xml",
 "data/pilot/tellechea-1826.full-witness.diagnostics.json","docs/SECOND_SOURCE_PILOT_TELLECHEA_1826.md",
 "docs/RHD_1_0_MACHINE_ONLY_CONFORMITY.md","docs/MACHINE_ONLY_COMPLETION_MATRIX.md")
for p in required:
 if p not in paths: errors.append(f"required prerelease artifact absent: {p}")

for item in files:
 rel=item.get("path"); path=ROOT/str(rel)
 if not path.exists(): errors.append(f"manifest path missing: {rel}"); continue
 dig=hashlib.sha256(path.read_bytes()).hexdigest()
 if dig!=item.get("sha256"): errors.append(f"sha256 mismatch: {rel}")
 if not re.fullmatch(r"[0-9a-f]{64}",item.get("sha256") or ""): errors.append(f"invalid sha256 format: {rel}")
 if path.stat().st_size!=item.get("bytes"): errors.append(f"byte count mismatch: {rel}")

counts=manifest.get("counts",{}); gates=manifest.get("gates",{})
canonical_count=sum(1 for line in (ROOT/"data/canonical/steffel-1809.entries.jsonl").read_text(encoding="utf-8").splitlines() if line.strip())
base_checks={
 "canonical_lexical_records":canonical_count,"canonical_appendix_objects":24,
 "trilingual_formula_blocks":22,"trilingual_formula_blocks_machine_aligned":22,
 "prayer_visual_transcriptions":1,"appendix_facsimile_pages_mapped":6,
 "appendix_terminal_uncertainties":43,
 "diachronic_documentary_candidates_scored":298,"diachronic_candidates_null_calibrated":298,
 "diachronic_null_control_pairs":5066,"canonical_working_witnesses":1,
 "prepared_iiif_canvases":84,"prepared_iiif_active_record_canvas_links":1965,
 "iiif_publication_assets_inventoried":84,
 "second_source_pilot_witnesses_checksum_fixed":1,"second_source_minimal_pilots_complete":1,
 "second_source_minimal_canonical_records":2,"second_source_pilots_full_witness_end_to_end_complete":1,
 "second_source_full_witness_canonical_records":205}
for key,val in base_checks.items():
 if counts.get(key)!=val: errors.append(f"release manifest count mismatch {key}: expected {val}, got {counts.get(key)}")
if not isinstance(counts.get("structured_primary_numeral_examples"),int) or counts.get("structured_primary_numeral_examples")<30: errors.append("expected at least 30 structured primary numeral examples")
if counts.get("registered_noncanonical_external_witnesses",0)<1: errors.append("at least one explicitly noncanonical external witness must remain registered")
if gates.get("second_source_industrialization_complete") is not True: errors.append("Tellechea industrialization gate must remain closed")
if gates.get("appendix_uncertainty_terminalized") is not True: errors.append("appendix uncertainty gate not terminalized")
if gates.get("diachronic_null_calibration_complete") is not True: errors.append("diachronic null calibration gate not complete")

# IIIF public publication remains a legitimate open gate at 98%. The manifest must
# record the complete preparation/inventory without converting that evidence into a
# false claim that the network endpoint is already published.
iiif=manifest.get("canonical_iiif",{}); iiif_closed=gates.get("canonical_iiif_complete") is True
if iiif_closed: errors.append("prerelease must not close canonical IIIF before network verification is persisted")
if counts.get("canonical_iiif_manifests_generated")!=0 or counts.get("canonical_iiif_canvases")!=0 or counts.get("canonical_iiif_static_page_images")!=0: errors.append("open IIIF gate falsely claims published canonical assets")
if counts.get("active_records_canvas_linked")!=0: errors.append("open IIIF gate falsely claims published active-record links")
if iiif.get("source_pdf_sha256")!="4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f": errors.append("IIIF preparation not tied to canonical Steffel checksum")
if iiif.get("prepared_canvases")!=84 or iiif.get("prepared_active_record_canvas_links")!=1965: errors.append("IIIF preparation coverage missing from manifest")
if iiif.get("publication_assets_inventoried")!=84 or iiif.get("canonical_canvas_dimensions_inventoried")!=84: errors.append("IIIF 84-page publication/dimension inventories missing")
if iiif.get("public_network_verified") is not False or iiif.get("generated_from_exact_binary") is not False or iiif.get("active_record_canvas_linkage_complete") is not False: errors.append("open IIIF gate falsely claims public completion")
if not str(iiif.get("public_manifest_url","")).startswith("https://fersandovalgtz.github.io/raramuri-historico/iiif/steffel-1809/"): errors.append("expected GitHub Pages canonical publication URL absent")
if iiif.get("region_targets_generated")!=0: errors.append("IIIF manifest fabricates region targets")

assets=json.loads((ROOT/"data/iiif/steffel-1809-published-png72-assets.json").read_text(encoding="utf-8"))
if assets.get("source_pdf_sha256")!="4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f" or assets.get("asset_count")!=84 or assets.get("format")!="image/png": errors.append("IIIF publication asset inventory identity/count/format mismatch")
if len(assets.get("assets",[]))!=84: errors.append("IIIF publication asset rows != 84")

dims=json.loads((ROOT/"data/iiif/steffel-1809-canonical-canvas-dimensions.json").read_text(encoding="utf-8"))
if dims.get("source_sha256")!="4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f" or len(dims.get("dimensions_by_pdf_page_1_based",[]))!=84: errors.append("IIIF canonical dimension inventory mismatch")

cal=json.loads((ROOT/"data/research/diachronic_machine_calibration.json").read_text(encoding="utf-8"))
if cal.get("candidate_count")!=298 or cal.get("null_pair_count")!=5066: errors.append("diachronic calibration coverage mismatch")
for k in ("automatic_semantic_judgment","automatic_cognacy_judgment","automatic_etymological_judgment","automatic_historical_continuity_judgment","human_reviewed"):
 if cal.get(k) is not False: errors.append(f"diachronic calibration fabricated {k}")
unc=json.loads((ROOT/"data/appendices/terminal_uncertainty_register.json").read_text(encoding="utf-8"))
if unc.get("all_items_terminal") is not True or unc.get("human_review_required") is not False: errors.append("appendix terminal uncertainty policy changed")

pilot=json.loads((ROOT/"source_profiles/tellechea-1826.pilot-candidate.json").read_text(encoding="utf-8")); fixed_sha="c67b7942090613c494d8057be8aff59ea13a11519c29eae469afad8a85c30dfc"
if pilot.get("witness",{}).get("sha256")!=fixed_sha: errors.append("Tellechea fixed witness checksum mismatch")
full=json.loads((ROOT/"data/pilot/tellechea-1826.full-witness.diagnostics.json").read_text(encoding="utf-8"))
if full.get("canonical_records")!=205 or full.get("pdf_pages")!=205 or full.get("rhd_core_changes_required")!=[] or full.get("lex0_entries_generated")!=0 or full.get("human_validation_claimed") is not False: errors.append("Tellechea 205/205 machine-only proof regressed")

completion=json.loads((ROOT/"project/completion-model-machine-only.json").read_text(encoding="utf-8"))
if completion.get("weighted_completion_percent")!=98.0 or completion.get("weighted_remaining_percent")!=2.0: errors.append("completion model must remain 98/2 until publication gates close")
if manifest.get("completion",{}).get("weighted_completion_percent")!=completion.get("weighted_completion_percent") or manifest.get("completion",{}).get("weighted_remaining_percent")!=completion.get("weighted_remaining_percent"): errors.append("completion percentages differ from model")

if errors: print("\n".join("ERROR: "+e for e in errors)); sys.exit(1)
print(f"OK: prerelease manifest verifies {len(files)} hashed artifacts, {canonical_count} Steffel records, 24 appendices/43 terminal uncertainties, 298 candidates vs 5066 null pairs, Tellechea 205/205, and IIIF preparation 84 canvases + 1965 links + 84 publication assets; public IIIF remains correctly open")
