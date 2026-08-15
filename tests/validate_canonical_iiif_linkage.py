#!/usr/bin/env python3
from pathlib import Path
import json, re, sys

ROOT=Path(__file__).resolve().parents[1]
CANON=ROOT/"data/canonical/steffel-1809.entries.jsonl"
SUMMARY=ROOT/"data/canonical/steffel-1809.iiif-linkage-summary.json"
BASE="https://fersandovalgtz.github.io/raramuri-historico/iiif/steffel-1809/canvas/p"
errors=[]
rows=[json.loads(line) for line in CANON.read_text(encoding="utf-8").splitlines() if line.strip()]
active=[r for r in rows if r.get("status")=="active"]
for r in rows:
    loc=r.get("locators",{}); page=loc.get("digital_page"); cid=loc.get("iiif_canvas"); target=loc.get("iiif_target")
    if isinstance(page,int) and 1<=page<=84:
        expected=f"{BASE}{page:03d}"
        if cid!=expected or target!=expected: errors.append(f"{r.get('record_id')}: page {page} not linked to expected Canvas")
    elif cid is not None or target is not None:
        errors.append(f"{r.get('record_id')}: IIIF locator exists without valid digital page")
if not SUMMARY.exists(): errors.append("IIIF linkage summary missing")
else:
    s=json.loads(SUMMARY.read_text(encoding="utf-8"))
    if s.get("records_total")!=len(rows): errors.append("IIIF linkage summary total mismatch")
    if s.get("active_records")!=len(active): errors.append("IIIF linkage summary active count mismatch")
    if s.get("active_records_canvas_mapped")!=len(active): errors.append(f"not all active records are page-Canvas linked: {s.get('active_records_canvas_mapped')}/{len(active)}")
    if s.get("active_records_without_digital_page")!=[]: errors.append(f"active records lack digital page: {len(s.get('active_records_without_digital_page',[]))}")
    if s.get("invalid_digital_pages")!=[]: errors.append("invalid digital pages found in canonical records")
    if s.get("human_validation_claimed") is not False: errors.append("IIIF linkage must deny human validation")
    if s.get("linkage_level")!="page_canvas" or s.get("region_targets_generated")!=0: errors.append("linkage summary must accurately state page-level Canvas mapping and zero fabricated regions")
if len(active)!=1965: errors.append(f"active-record invariant changed: {len(active)}")
if errors:
    print("\n".join("ERROR: "+e for e in errors)); sys.exit(1)
print(f"OK: all {len(active)} active Steffel records are linked deterministically to their canonical IIIF page Canvases; no fake xywh regions or human validation were introduced")
