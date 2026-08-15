#!/usr/bin/env python3
from pathlib import Path
import json, re, sys

ROOT=Path(__file__).resolve().parents[1]
DIMS=ROOT/"data/iiif/steffel-1809-canonical-canvas-dimensions.json"
MANIFEST=ROOT/"public/iiif/steffel-1809/manifest.json"
CANVAS_MAP=ROOT/"public/iiif/steffel-1809/canvas-map.json"
RECORD_MAP=ROOT/"data/canonical/steffel-1809.iiif-record-map.jsonl"
SUMMARY=ROOT/"data/canonical/steffel-1809.iiif-preparation-summary.json"
SHA="4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f"
errors=[]

for p in (DIMS,MANIFEST,CANVAS_MAP,RECORD_MAP,SUMMARY):
    if not p.exists(): errors.append(f"missing prepared IIIF artifact: {p.relative_to(ROOT)}")
if errors:
    print("\n".join("ERROR: "+e for e in errors)); sys.exit(1)

dims=json.loads(DIMS.read_text(encoding="utf-8")); manifest=json.loads(MANIFEST.read_text(encoding="utf-8")); cmap=json.loads(CANVAS_MAP.read_text(encoding="utf-8")); summary=json.loads(SUMMARY.read_text(encoding="utf-8"))
if dims.get("source_sha256")!=SHA or dims.get("source_bytes")!=6251443 or dims.get("source_pdf_pages")!=84: errors.append("dimension set is not tied to exact canonical witness")
wh=dims.get("dimensions_by_pdf_page_1_based",[])
if len(wh)!=84 or any(not isinstance(x,list) or len(x)!=2 or x[0]<=0 or x[1]<=0 for x in wh): errors.append("invalid 84-page canvas dimension inventory")
if dims.get("derived_locally_from_checksum_fixed_witness") is not True or dims.get("public_image_host_verified") is not False: errors.append("dimension set publication/derivation state changed")

if manifest.get("@context")!="http://iiif.io/api/presentation/3/context.json" or manifest.get("type")!="Manifest": errors.append("not IIIF Presentation 3 Manifest")
if not str(manifest.get("id","")).startswith("https://rhd.invalid/"): errors.append("CI preparation must use reserved non-public .invalid IDs")
items=manifest.get("items",[])
if len(items)!=84: errors.append(f"expected 84 Canvases, got {len(items)}")
canvas_ids=[]
for i,(canvas,expected_wh) in enumerate(zip(items,wh),1):
    if canvas.get("type")!="Canvas": errors.append(f"page {i}: non-Canvas item"); continue
    canvas_ids.append(canvas.get("id"))
    if [canvas.get("width"),canvas.get("height")]!=expected_wh: errors.append(f"page {i}: Canvas dimensions differ from exact-witness inventory")
    aps=canvas.get("items",[])
    try:
        ann=aps[0]["items"][0]; body=ann["body"]
    except Exception:
        errors.append(f"page {i}: missing painting Annotation structure"); continue
    if ann.get("motivation")!="painting" or ann.get("target")!=canvas.get("id"): errors.append(f"page {i}: invalid painting Annotation")
    if body.get("type")!="Image" or body.get("format")!="image/jpeg": errors.append(f"page {i}: invalid image body")
    if [body.get("width"),body.get("height")]!=expected_wh: errors.append(f"page {i}: image dimensions differ from Canvas")
    if not str(body.get("id","")).endswith(f"/pages/{i:03d}.jpg"): errors.append(f"page {i}: unstable image naming")
if len(set(canvas_ids))!=84: errors.append("Canvas IDs are not unique")

pages=cmap.get("pages",[])
if cmap.get("source_pdf_sha256")!=SHA or cmap.get("source_pdf_pages")!=84 or len(pages)!=84: errors.append("canvas map witness identity/count mismatch")
if cmap.get("publication_status")!="prepared_not_public" or cmap.get("public_image_host_verified") is not False: errors.append("canvas map falsely claims publication")
for i,p in enumerate(pages,1):
    if p.get("pdf_page")!=i or p.get("canvas_id")!=items[i-1].get("id"): errors.append(f"page {i}: canvas map mismatch")
    if p.get("region_target_available") is not False: errors.append(f"page {i}: fabricated region availability")

records=[json.loads(x) for x in RECORD_MAP.read_text(encoding="utf-8").splitlines() if x.strip()]
if len(records)!=1965 or len({r.get('record_id') for r in records})!=1965: errors.append("record->Canvas map does not contain exactly 1965 unique active records")
for r in records:
    page=r.get("pdf_page")
    if not isinstance(page,int) or not 1<=page<=84: errors.append(f"{r.get('record_id')}: bad pdf_page"); continue
    if r.get("iiif_canvas")!=items[page-1].get("id"): errors.append(f"{r.get('record_id')}: Canvas mismatch")
    if r.get("iiif_target") is not None or r.get("region_coordinates_available") is not False: errors.append(f"{r.get('record_id')}: fabricated region target")
    if r.get("human_validation_claimed") is not False: errors.append(f"{r.get('record_id')}: fabricated human validation")

if summary.get("source_pdf_sha256")!=SHA or summary.get("active_records_canvas_mapped")!=1965: errors.append("IIIF preparation summary coverage mismatch")
if summary.get("active_record_page_linkage_prepared") is not True or summary.get("active_record_canvas_linkage_complete_for_prepared_manifest") is not True: errors.append("prepared page linkage not marked complete")
if summary.get("canonical_iiif_publication_gate_closed") is not False or summary.get("public_image_host_verified") is not False: errors.append("preparation summary falsely closes public IIIF gate")
if summary.get("region_targets_generated")!=0 or summary.get("region_coordinates_available") is not False: errors.append("preparation summary fabricates regions")
if summary.get("human_validation_claimed") is not False: errors.append("preparation summary fabricates human validation")

serialized=(MANIFEST.read_text(encoding="utf-8")+CANVAS_MAP.read_text(encoding="utf-8")+RECORD_MAP.read_text(encoding="utf-8")+SUMMARY.read_text(encoding="utf-8")).lower()
for forbidden in ("human_verified\": true","region_coordinates_available\": true","canonical_iiif_publication_gate_closed\": true"):
    if forbidden in serialized: errors.append(f"forbidden IIIF preparation claim: {forbidden}")

if errors:
    print("\n".join("ERROR: "+e for e in errors)); sys.exit(1)
print("OK: exact-witness IIIF preparation has 84 Canvases and 1965 page-level record links, with 0 fabricated regions and public hosting explicitly still open")
