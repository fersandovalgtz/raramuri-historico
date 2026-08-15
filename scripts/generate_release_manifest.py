#!/usr/bin/env python3
"""Generate deterministic integrity manifest for the RHD machine-only prerelease.

Canonical IIIF is an optional gate: if exact-binary-derived IIIF files exist they are
hashed and reported; their absence must not invalidate all other checksum-fixed science.
"""
from pathlib import Path
import hashlib, json

ROOT=Path(__file__).resolve().parents[1]
OUT_DIR=ROOT/"dist"; OUT=OUT_DIR/"rhd-steffel-release-manifest.json"
REQUIRED=[
 ("source_ocr","sources/steffel-1809-ocr-source.txt"),("source_checksums","sources/checksums.json"),
 ("witness_registry","sources/external-references.json"),("iiif_local_page_fingerprints","data/iiif/steffel-1809-local-page-fingerprints.json"),
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
 ("completion_matrix","docs/MACHINE_ONLY_COMPLETION_MATRIX.md"),("completion_model","project/completion-model-machine-only.json")]
OPTIONAL_IIIF=[
 ("canonical_iiif_manifest","public/iiif/steffel-1809/manifest.json"),
 ("canonical_iiif_canvas_map","public/iiif/steffel-1809/canvas-map.json"),
 ("canonical_iiif_linkage_summary","data/canonical/steffel-1809.iiif-linkage-summary.json")]

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
 canonical_witnesses=[w for w in witness_registry.get("witnesses",[]) if w.get("canonical_for_rhd") is not False and w.get("role")=="canonical_working_facsimile"]
 parallel_witnesses=[w for w in witness_registry.get("witnesses",[]) if w.get("canonical_for_rhd") is False]
 credit=pilot_profile.get("completion_credit",{}); fixed=(pilot_profile.get("witness",{}).get("identity_status")=="checksum_fixed_public_witness" and pilot_witness.get("status")=="checksum_fixed_public_witness")
 minimal_complete=(minimal_count==2 and minimal_diag.get("pilot_id")=="RHD-TELLECHEA-1826-MINIMAL-PILOT-1" and minimal_diag.get("human_validation_claimed") is False)
 full_complete=(full_count==205 and full_diag.get("pilot_id")=="RHD-TELLECHEA-1826-FULL-WITNESS-PILOT-1" and full_diag.get("pdf_pages")==205 and full_diag.get("canonical_records")==205 and full_diag.get("rhd_core_changes_required")==[] and full_diag.get("lex0_entries_generated")==0 and full_diag.get("human_validation_claimed") is False and credit.get("completes_second_source_end_to_end_gate") is True)

 iiif_manifest_path=ROOT/"public/iiif/steffel-1809/manifest.json"; iiif_map_path=ROOT/"public/iiif/steffel-1809/canvas-map.json"; linkage_path=ROOT/"data/canonical/steffel-1809.iiif-linkage-summary.json"
 canonical_iiif_complete=False; iiif_meta={"status":"open_not_packaged_in_this_working_tree","presentation_version":3,"canvases":0,"static_page_images":0,"generated_from_exact_binary":False,"active_record_canvas_linkage_complete":False,"region_targets_generated":0}
 if iiif_manifest_path.exists() and iiif_map_path.exists() and linkage_path.exists():
  iiif_manifest=read_json(iiif_manifest_path); iiif_map=read_json(iiif_map_path); linkage=read_json(linkage_path); pages=iiif_map.get("pages",[])
  image_count=sum((ROOT/"public/iiif/steffel-1809/pages"/f"{i:03d}.jpg").exists() for i in range(1,85))
  canonical_iiif_complete=(iiif_manifest.get("type")=="Manifest" and len(iiif_manifest.get("items",[]))==84 and len(pages)==84 and image_count==84 and iiif_map.get("source_pdf_sha256")=="4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f" and linkage.get("active_records_canvas_mapped")==1965)
  iiif_meta={"status":"complete_exact_binary_derived" if canonical_iiif_complete else "present_but_incomplete","manifest_id":iiif_manifest.get("id"),"witness_id":iiif_map.get("witness_id"),"source_pdf_sha256":iiif_map.get("source_pdf_sha256"),"presentation_version":3,"canvases":len(iiif_manifest.get("items",[])),"static_page_images":image_count,"generated_from_exact_binary":bool(canonical_iiif_complete),"active_record_canvas_linkage_complete":linkage.get("active_records_canvas_mapped")==1965,"active_records_canvas_linked":linkage.get("active_records_canvas_mapped",0),"linkage_level":linkage.get("linkage_level"),"region_targets_generated":linkage.get("region_targets_generated",0)}

 manifest={"manifest_id":"RHD-STEFFEL-MACHINE-ONLY-RELEASE-MANIFEST-1","generated_from":"repository working tree plus deterministic CI-derived pilot outputs","release_scope":"machine-only historical-digital scholarly edition; zero required human adjudication","human_validation_claimed":False,
  "gates":{"canonical_iiif_complete":bool(canonical_iiif_complete),"second_source_industrialization_complete":bool(full_complete),"appendix_uncertainty_terminalized":uncertainty.get("all_items_terminal") is True,"diachronic_null_calibration_complete":calibration.get("candidate_count")==298 and calibration.get("null_pair_count")==5066},
  "counts":{"canonical_lexical_records":canonical_count,"canonical_appendix_objects":len(appendix_canonical.get("objects",[])),"trilingual_formula_blocks":appendix_source.get("formula_count"),"trilingual_formula_blocks_machine_aligned":len(appendix_alignment.get("formulas",[])),"structured_primary_numeral_examples":len(numeration_visual.get("primary_cardinals",[])),"prayer_visual_transcriptions":1 if prayer_visual.get("text") else 0,"appendix_facsimile_pages_mapped":len(page_map.get("mapping",[])),"appendix_terminal_uncertainties":uncertainty.get("summary",{}).get("count"),"diachronic_documentary_candidates_scored":diachronic.get("count"),"diachronic_candidates_null_calibrated":calibration.get("candidate_count"),"diachronic_null_control_pairs":calibration.get("null_pair_count"),"canonical_working_witnesses":len(canonical_witnesses),"registered_noncanonical_external_witnesses":len(parallel_witnesses),"canonical_iiif_manifests_generated":1 if canonical_iiif_complete else 0,"canonical_iiif_canvases":iiif_meta.get("canvases",0),"canonical_iiif_static_page_images":iiif_meta.get("static_page_images",0),"active_records_canvas_linked":iiif_meta.get("active_records_canvas_linked",0),"second_source_pilot_witnesses_checksum_fixed":1 if fixed else 0,"second_source_minimal_pilots_complete":1 if minimal_complete else 0,"second_source_minimal_canonical_records":minimal_count,"second_source_pilots_full_witness_end_to_end_complete":1 if full_complete else 0,"second_source_full_witness_canonical_records":full_count},
  "canonical_iiif":iiif_meta,
  "second_source_pilot":{"source_id":pilot_profile.get("source_id"),"pilot_status":pilot_profile.get("pilot_status"),"witness_id":pilot_profile.get("witness",{}).get("witness_id"),"witness_sha256":pilot_profile.get("witness",{}).get("sha256"),"minimal_end_to_end_completion_credit":bool(minimal_complete),"full_witness_end_to_end_completion_credit":bool(full_complete),"minimal_canonical_records":minimal_count,"full_witness_canonical_records":full_count,"full_witness_pdf_pages":full_diag.get("pdf_pages"),"full_witness_rhd_core_changes_required":len(full_diag.get("rhd_core_changes_required",[])),"full_witness_lex0_entries_generated":full_diag.get("lex0_entries_generated")},
  "completion":{"weighted_completion_percent":completion.get("weighted_completion_percent"),"weighted_remaining_percent":completion.get("weighted_remaining_percent")},"optional_artifacts_present":optional_present,"files":records}
 OUT_DIR.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
 print(f"generated release manifest with {len(records)} hashed artifacts; canonical IIIF={'closed' if canonical_iiif_complete else 'open'}; appendix terminal uncertainty={manifest['gates']['appendix_uncertainty_terminalized']}; diachronic null calibration={manifest['gates']['diachronic_null_calibration_complete']}; Tellechea full gate={'closed' if full_complete else 'open'}")
if __name__=="__main__": main()
