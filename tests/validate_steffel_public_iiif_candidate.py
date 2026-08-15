#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT=Path(__file__).resolve().parents[1]
BASE="https://fersandovalgtz.github.io/raramuri-historico/iiif/steffel-1809"
OUT=ROOT/"dist/iiif-public-candidate/steffel-1809"
ASSETS=ROOT/"data/iiif/steffel-1809-published-png72-assets.json"
SHA="4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f"
errors=[]

for p in (OUT/"manifest.json", OUT/"canvas-map.json", OUT/"record-map.jsonl", OUT/"summary.json", ASSETS):
    if not p.exists(): errors.append(f"missing public IIIF candidate artifact: {p.relative_to(ROOT)}")
if errors:
    print("\n".join("ERROR: "+e for e in errors)); sys.exit(1)

manifest=json.loads((OUT/"manifest.json").read_text(encoding="utf-8"))
cmap=json.loads((OUT/"canvas-map.json").read_text(encoding="utf-8"))
summary=json.loads((OUT/"summary.json").read_text(encoding="utf-8"))
assets=json.loads(ASSETS.read_text(encoding="utf-8"))
records=[json.loads(x) for x in (OUT/"record-map.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]

if assets.get("source_pdf_sha256")!=SHA or assets.get("asset_count")!=84 or assets.get("format")!="image/png": errors.append("publication asset inventory identity/format mismatch")
asset_rows=assets.get("assets",[])
if len(asset_rows)!=84: errors.append("publication asset inventory does not contain 84 rows")

if manifest.get("@context")!="http://iiif.io/api/presentation/3/context.json" or manifest.get("type")!="Manifest": errors.append("candidate is not IIIF Presentation 3 Manifest")
if manifest.get("id")!=BASE+"/manifest.json": errors.append("candidate Manifest id is not canonical GitHub Pages URL")
items=manifest.get("items",[])
if len(items)!=84: errors.append(f"candidate must contain 84 Canvases, got {len(items)}")

for i,(canvas,asset) in enumerate(zip(items,asset_rows),1):
    if asset.get("pdf_page")!=i or asset.get("filename")!=f"{i:03d}.png": errors.append(f"page {i}: malformed publication inventory")
    expected_wh=[asset.get("width"),asset.get("height")]
    if canvas.get("type")!="Canvas" or [canvas.get("width"),canvas.get("height")]!=expected_wh: errors.append(f"page {i}: Canvas dimensions mismatch")
    try:
        ann=canvas["items"][0]["items"][0]; body=ann["body"]
    except Exception:
        errors.append(f"page {i}: missing painting annotation"); continue
    if ann.get("motivation")!="painting" or ann.get("target")!=canvas.get("id"): errors.append(f"page {i}: painting annotation invalid")
    if body.get("type")!="Image" or body.get("format")!="image/png": errors.append(f"page {i}: painting body must be PNG")
    if body.get("id")!=BASE+f"/pages/{i:03d}.png": errors.append(f"page {i}: public image URL mismatch")
    if [body.get("width"),body.get("height")]!=expected_wh: errors.append(f"page {i}: painting dimensions mismatch")
    serialized=json.dumps(canvas,ensure_ascii=False).lower()
    if "xywh=" in serialized: errors.append(f"page {i}: candidate fabricates xywh region")

pages=cmap.get("pages",[])
if cmap.get("source_pdf_sha256")!=SHA or cmap.get("base_url")!=BASE or len(pages)!=84: errors.append("public canvas map identity/count mismatch")
if cmap.get("public_image_host_verified") is not False or cmap.get("publication_status")!="candidate_not_network_verified": errors.append("offline candidate falsely claims publication verification")
for i,p in enumerate(pages,1):
    asset=asset_rows[i-1]
    if p.get("pdf_page")!=i or p.get("image_filename")!=asset.get("filename") or p.get("sha256")!=asset.get("sha256") or p.get("bytes")!=asset.get("bytes"): errors.append(f"page {i}: canvas map asset integrity mismatch")
    if p.get("region_target_available") is not False: errors.append(f"page {i}: region target fabricated")

if len(records)!=1965 or len({r.get("record_id") for r in records})!=1965: errors.append("public record map must contain exactly 1965 unique active records")
for r in records:
    page=r.get("pdf_page")
    if not isinstance(page,int) or not 1<=page<=84: errors.append(f"{r.get('record_id')}: invalid pdf page"); continue
    if r.get("iiif_canvas")!=BASE+f"/canvas/p{page:03d}": errors.append(f"{r.get('record_id')}: public Canvas URL mismatch")
    if r.get("iiif_target") is not None or r.get("region_coordinates_available") is not False: errors.append(f"{r.get('record_id')}: fabricated region")
    if r.get("human_validation_claimed") is not False: errors.append(f"{r.get('record_id')}: fabricated human validation")

if summary.get("canvases")!=84 or summary.get("page_assets_expected")!=84 or summary.get("active_records_canvas_mapped")!=1965: errors.append("public candidate summary coverage mismatch")
if summary.get("region_targets_generated")!=0 or summary.get("public_image_host_verified") is not False or summary.get("canonical_iiif_publication_gate_closed") is not False: errors.append("public candidate summary prematurely closes publication gate")
if summary.get("human_validation_claimed") is not False: errors.append("public candidate summary fabricates human validation")

if errors:
    print("\n".join("ERROR: "+e for e in errors)); sys.exit(1)
print("OK: GitHub Pages IIIF candidate has 84 exact-inventory PNG Canvases and 1965 public page-level links; network publication gate remains explicitly open")
