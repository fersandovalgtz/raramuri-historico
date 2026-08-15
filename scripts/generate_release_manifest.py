#!/usr/bin/env python3
"""Generate deterministic integrity manifest for the RHD machine-only prerelease.

Canonical IIIF publication is an independent gate. The prerelease must nevertheless
hash the exact-witness IIIF preparation evidence and publication inventory so the
98% state is self-contained and auditable without falsely claiming public hosting.
"""
from pathlib import Path
import hashlib, json

ROOT=Path(__file__).resolve().parents[1]
OUT_DIR=ROOT/"dist"; OUT=OUT_DIR/"rhd-steffel-release-manifest.json"
REQUIRED=[
 ("citation","CITATION.cff"),("changelog","CHANGELOG.md"),("data_license","DATA_LICENSE.md"),("provenance","PROVENANCE.md"),
 ("source_ocr","sources/steffel-1809-ocr-source.txt"),("source_checksums","sources/checksums.json"),
 ("witness_registry","sources/external-references.json"),
 ("iiif_local_page_fingerprints","data/iiif/steffel-1809-local-page-fingerprints.json"),
 ("iiif_all84_page_fingerprints","data/iiif/steffel-1809-all84-page-fingerprints.json"),
 ("iiif_canonical_canvas_dimensions","data/iiif/steffel-1809-canonical-canvas-dimensions.json"),
 ("iiif_publication_asset_inventory","data/iiif/steffel-1809-published-png72-assets.json"),
 ("iiif_readiness","docs/IIIF_READINESS.md"),("iiif_publication_runbook","docs/IIIF_PUBLICATION_GITHUB_PAGES.md"),
 ("master_entries","data/entries.csv"),("corpus_inventory","data/corpus_inventory.json"),
 ("canonical_jsonl","data/canonical/steffel-1809.entries.jsonl"),("canonical_appendices","data/canonical/steffel-1809.appendices.json"),
 ("diachronic_machine_scores","data/research/diachronic_machine_scores.json"),
 ("diachronic_machine_calibration","data/research/diachronic_machine_calibration.json"),
 ("tei_rich","data/tei/rhd-steffel-1809-tei.xml"),("tei_lex0","data/tei/rhd-steffel-1809-lex0.xml"),("tei_appendices","data/tei/rhd-steffel-1809-appendices-tei.xml"),
 ("appendix_numeration_ocr","data/appendices/numeration_ocr_candidates.json"),("appendix_numeration_visual","data/appendices/numeration_visual_structure_ai.json"),
 ("appendix_trilingual_ocr","data/appendices/trilingual_sample_ocr_candidates.json"),("appendix_trilingual_visual_alignment","data/appendices/trilingual_visual_alignment_ai.json"),
 ("appendix_prayer_visual","data/appendices/prayer_visual_transcription_ai.json"),("appendix_facsimile_map","data/appendices/facsimile_page_map.json"),
 ("appendix_terminal_uncertainty","data/appendices/terminal_uncertainty_register.json"),
 ("canonical_schema","schemas/rhd-entry-1.0.schema.json"),("steffel_source_profile","source_profiles/steffel-1809.source.json"),
 ("reusable_source_profile_template","source_profiles/_template.source.json"),("second_source_pilot_profile","source_profiles/tellechea-1826.pilot-candidate.json"),
 ("second_source_witness_identity","sources/tellechea-1826-witness.json"),("second_source_pilot_plan","docs/SECOND_SOURCE_PILOT_TELLECHEA_1826.md"),
 ("second_source_minimal_canonical","data/pilot/tellechea-1826.minimal-pilot.jsonl"),("second_source_minimal_tei","data/pilot/tellechea-1826.minimal-pilot.tei.xml"),
 ("second_source_minimal_diagnostics","data/pilot/tellechea-1826.minimal-pilot.diagnostics.json"),("second_source_full_canonical","data/pilot/tellechea-1826.full-witness.jsonl"),
 ("second_source_full_tei","data/pilot/tellechea-1826.full-witness.tei.xml"),("second_source_full_diagnostics","data/pilot/tellechea-1826.full-witness.diagnostics.json"),
 ("machine_only_policy","docs/MACHINE_ONLY_SCIENTIFIC_POLICY.md"),("machine_only_conformity","docs/RHD_1_0_MACHINE_ONLY_CONFORMITY.md"),
 ("completion_matrix","docs/MACHINE_ONLY_COMPLETION_MATRIX.md"),("completion_model","project/completion-model-machine-only.json"),
 ("release_readiness","docs/RELEASE_READINESS_RHD_1_0.md")]
OPTIONAL_IIIF=[
 ("prepared_iiif_manifest","public/iiif/steffel-1809/manifest.json"),
 ("prepared_iiif_canvas_map","public/iiif/steffel-1809/canvas-map.json"),
 ("prepared_iiif_record_map","data/canonical/steffel-1809.iiif-record-map.jsonl"),
 ("prepared_iiif_summary","data/canonical/steffel-1809.iiif-preparation-summary.json")]

def sha256(path):
 h=hashlib.sha256()
 with path.open("rb") as fh:
  for chunk in iter(lambda:fh.read(1024*1024),b""): h.update(chunk)
 return h.hexdigest()
def read_json(path): return json.loads(path.read_text(encoding="utf-8"))
def jsonl_count(path): return sum(1 for x in path.read_text(encoding="utf-8").splitlines() if x.strip())
def artifact(role,rel):
 p=ROOT/rel
 return {"role":role,"path":rel,"bytes":p.stat().st_size,"sha256":sha256(p)}

def main():
 missing=[rel for _,rel in REQUIRED if not (ROOT/rel).exists()]
 if missing: raise SystemExit("release manifest cannot be generated; missing required artifacts: "+", ".join(missing))
 records=[artifact(role,rel) for role,rel in REQUIRED]
 optional_present=[]
 for role,rel in OPTIONAL_IIIF:
  if (ROOT/rel).exists(): records.append(artifact(role,rel)); optional_present.append(rel)

 canonical_count=jsonl_count(ROOT/"data/canonical/steffel-1809.entries.jsonl")
 appendix_source=read_json(ROOT/"data/appendices/trilingual_sample_ocr_candidates.json"); appendix_alignment=read_json(ROOT/"data/appendices/trilingual_visual_alignment_ai.json")
 appendix_canonical=read_json(ROOT/"data/canonical/steffel-1809.appendices.json"); numeration_visual=read_json(ROOT/"data/appendices/numeration_visual_structure_ai.json")
 prayer_visual=read_json(ROOT/"data/appendices/prayer_visual_transcription_ai.json"); uncertainty=read_json(ROOT/"data/appendices/terminal_uncertainty_register.json")
 diachronic=read_json(ROOT/"data/research/diachronic_machine_scores.json"); calibration=read_json(ROOT/"data/research/diachronic_machine_calibration.json")
 completion=read_json(ROOT/"project/completion-model-machine-only.json"); page_map=read_json(ROOT/"data/appendices/facsimile_page_map.json")
 witness_registry=read_json(ROOT/"sources/external-references.json"); pilot_profile=read_json(ROOT/"source_profiles/tellechea-1826.pilot-candidate.json")
 pilot_witness=read_json(ROOT/"sources/tellechea-1826-witness.json"); minimal_diag=read_json(ROOT/"data/pilot/tellechea-1826.minimal-pilot.diagnostics.json")
 full_diag=read_json(ROOT/"data/pilot/tellechea-1826.full-witness.diagnostics.json"); minimal_count=jsonl_count(ROOT/"data/pilot/tellechea-1826.minimal-pilot.jsonl")
 full_count=jsonl_count(ROOT/"data/pilot/tellechea-1826.full-witness.jsonl")
 iiif_assets=read_json(ROOT/"data/iiif/steffel-1809-published-png72-assets.json")
 iiif_dims=read_json(ROOT/"data/iiif/steffel-1809-canonical-canvas-dimensions.json")
 canonical_witnesses=[w for w in witness_registry.get("witnesses",[]) if w.get("canonical_for_rhd") is not False and w.get("role")=="canonical_working_facsimile"]
 parallel_witnesses=[w for w in witness_registry.get("witnesses",[]) if w.get("canonical_for_rhd") is False]
 credit=pilot_profile.get("completion_credit",{}); fixed=(pilot_profile.get("witness",{}).get("identity_status")=="checksum_fixed_public_witness" and pilot_witness.get("status")=="checksum_fixed_public_witness")
 minimal_complete=(minimal_count==2 and minimal_diag.get("pilot_id")=="RHD-TELLECHEA-1826-MINIMAL-PILOT-1" and minimal_diag.get("human_validation_claimed") is False)
 full_complete=(full_count==205 and full_diag.get("pilot_id")=="RHD-TELLECHEA-1826-FULL-WITNESS-PILOT-1" and full_diag.get("pdf_pages")==205 and full_diag.get("canonical_records")==205 and full_diag.get("rhd_core_changes_required")==[] and full_diag.get("lex0_entries_generated")==0 and full_diag.get("human_validation_claimed") is False and credit.get("completes_second_source_end_to_end_gate") is True)

 # Publication remains open until network verification succeeds. Prepared files are
 # hashed as evidence but never promoted to a public IIIF completion claim here.
 prepared_manifest=ROOT/"public/iiif/steffel-1809/manifest.json"; prepared_map=ROOT/"public/iiif/steffel-1809/canvas-map.json"; prepared_summary=ROOT/"data/canonical/steffel-1809.iiif-preparation-summary.json"
 prepared_canvases=0; prepared_links=0
 if prepared_manifest.exists(): prepared_canvases=len(read_json(prepared_manifest).get("items",[]))
 if prepared_summary.exists(): prepared_links=read_json(prepared_summary).get("active_records_canvas_mapped",0)
 canonical_iiif_complete=False
 iiif_meta={
  "status":"prepared_exact_witness_publication_not_network_verified",
  "presentation_version":3,
  "source_pdf_sha256":"4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f",
  "prepared_canvases":prepared_canvases,
  "prepared_active_record_canvas_links":prepared_links,
  "publication_asset_profile":iiif_assets.get("asset_manifest_id"),
  "publication_assets_inventoried":iiif_assets.get("asset_count",0),
  "canonical_canvas_dimensions_inventoried":len(iiif_dims.get("dimensions_by_pdf_page_1_based",[])),
  "public_manifest_url":"https://fersandovalgtz.github.io/raramuri-historico/iiif/steffel-1809/manifest.json",
  "public_network_verified":False,
  "generated_from_exact_binary":False,
  "active_record_canvas_linkage_complete":False,
  "active_records_canvas_linked":0,
  "region_targets_generated":0}

 manifest={"manifest_id":"RHD-STEFFEL-MACHINE-ONLY-RELEASE-MANIFEST-1","generated_from":"repository working tree plus deterministic CI-derived pilot outputs","release_scope":"machine-only historical-digital scholarly edition; zero required human adjudication","human_validation_claimed":False,
  "gates":{"canonical_iiif_complete":False,"second_source_industrialization_complete":bool(full_complete),"appendix_uncertainty_terminalized":uncertainty.get("all_items_terminal") is True,"diachronic_null_calibration_complete":calibration.get("candidate_count")==298 and calibration.get("null_pair_count")==5066},
  "counts":{"canonical_lexical_records":canonical_count,"canonical_appendix_objects":len(appendix_canonical.get("objects",[])),"trilingual_formula_blocks":appendix_source.get("formula_count"),"trilingual_formula_blocks_machine_aligned":len(appendix_alignment.get("formulas",[])),"structured_primary_numeral_examples":len(numeration_visual.get("primary_cardinals",[])),"prayer_visual_transcriptions":1 if prayer_visual.get("text") else 0,"appendix_facsimile_pages_mapped":len(page_map.get("mapping",[])),"appendix_terminal_uncertainties":uncertainty.get("summary",{}).get("count"),"diachronic_documentary_candidates_scored":diachronic.get("count"),"diachronic_candidates_null_calibrated":calibration.get("candidate_count"),"diachronic_null_control_pairs":calibration.get("null_pair_count"),"canonical_working_witnesses":len(canonical_witnesses),"registered_noncanonical_external_witnesses":len(parallel_witnesses),"canonical_iiif_manifests_generated":0,"canonical_iiif_canvases":0,"canonical_iiif_static_page_images":0,"active_records_canvas_linked":0,"prepared_iiif_canvases":prepared_canvases,"prepared_iiif_active_record_canvas_links":prepared_links,"iiif_publication_assets_inventoried":iiif_assets.get("asset_count",0),"second_source_pilot_witnesses_checksum_fixed":1 if fixed else 0,"second_source_minimal_pilots_complete":1 if minimal_complete else 0,"second_source_minimal_canonical_records":minimal_count,"second_source_pilots_full_witness_end_to_end_complete":1 if full_complete else 0,"second_source_full_witness_canonical_records":full_count},
  "canonical_iiif":iiif_meta,
  "second_source_pilot":{"source_id":pilot_profile.get("source_id"),"pilot_status":pilot_profile.get("pilot_status"),"witness_id":pilot_profile.get("witness",{}).get("witness_id"),"witness_sha256":pilot_profile.get("witness",{}).get("sha256"),"minimal_end_to_end_completion_credit":bool(minimal_complete),"full_witness_end_to_end_completion_credit":bool(full_complete),"minimal_canonical_records":minimal_count,"full_witness_canonical_records":full_count,"full_witness_pdf_pages":full_diag.get("pdf_pages"),"full_witness_rhd_core_changes_required":len(full_diag.get("rhd_core_changes_required",[])),"full_witness_lex0_entries_generated":full_diag.get("lex0_entries_generated")},
  "completion":{"weighted_completion_percent":completion.get("weighted_completion_percent"),"weighted_remaining_percent":completion.get("weighted_remaining_percent")},"optional_artifacts_present":optional_present,"files":records}
 OUT_DIR.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
 print(f"generated release manifest with {len(records)} hashed artifacts; IIIF prepared={prepared_canvases}/84 canvases and {prepared_links}/1965 links, public gate=open; appendix terminal uncertainty={manifest['gates']['appendix_uncertainty_terminalized']}; diachronic null calibration={manifest['gates']['diachronic_null_calibration_complete']}; Tellechea full gate={'closed' if full_complete else 'open'}")
if __name__=="__main__": main()
