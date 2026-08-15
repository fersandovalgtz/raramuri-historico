#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, sys
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"public/iiif/steffel-1809"
MANIFEST=BASE/"manifest.json"; MAP=BASE/"canvas-map.json"; PAGES=BASE/"pages"
EXPECTED_SHA="4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f"
EXPECTED_WITNESS="RHD-WIT-STEFFEL-1809-PROJECT-FACSIMILE"
BASE_URL="https://fersandovalgtz.github.io/raramuri-historico/iiif/steffel-1809"
errors=[]
for p in (MANIFEST,MAP):
    if not p.exists(): errors.append(f"missing canonical IIIF artifact: {p.relative_to(ROOT)}")
if errors: print("\n".join("ERROR: "+e for e in errors)); sys.exit(1)
manifest=json.loads(MANIFEST.read_text(encoding="utf-8")); cmap=json.loads(MAP.read_text(encoding="utf-8"))
ctx=manifest.get("@context"); ctx_text=" ".join(ctx) if isinstance(ctx,list) else str(ctx or "")
if "presentation/3" not in ctx_text: errors.append("canonical manifest is not IIIF Presentation 3")
if manifest.get("type")!="Manifest": errors.append("canonical IIIF root must be Manifest")
if manifest.get("id")!=f"{BASE_URL}/manifest.json": errors.append("canonical manifest stable ID changed")
items=manifest.get("items",[])
if len(items)!=84: errors.append(f"canonical IIIF must contain exactly 84 Canvases, got {len(items)}")
if cmap.get("witness_id")!=EXPECTED_WITNESS: errors.append("canvas map witness ID differs from Steffel source profile")
if cmap.get("source_pdf_sha256")!=EXPECTED_SHA: errors.append("canvas map lost canonical PDF checksum")
if cmap.get("source_pdf_bytes")!=6251443 or cmap.get("source_pdf_pages")!=84: errors.append("canvas map lost canonical PDF size/page identity")
if cmap.get("canonical_binary_identity_required") is not True: errors.append("canvas map must require exact binary identity")
if cmap.get("human_validation_claimed") is not False: errors.append("canvas map must deny human validation")
pages=cmap.get("pages",[])
if len(pages)!=84: errors.append(f"canvas map must contain 84 pages, got {len(pages)}")

for i in range(1,85):
    expected_canvas=f"{BASE_URL}/canvas/p{i:03d}"; expected_image=f"{BASE_URL}/pages/{i:03d}.jpg"
    if i<=len(items):
        canvas=items[i-1]
        if canvas.get("id")!=expected_canvas: errors.append(f"Canvas {i} ID mismatch")
        if canvas.get("type")!="Canvas": errors.append(f"Canvas {i} type mismatch")
        try:
            ann=canvas["items"][0]["items"][0]
            body=ann["body"]
            if ann.get("motivation")!="painting" or ann.get("target")!=expected_canvas: errors.append(f"Canvas {i} painting annotation mismatch")
            if body.get("id")!=expected_image or body.get("format")!="image/jpeg": errors.append(f"Canvas {i} image body mismatch")
        except (KeyError,IndexError,TypeError): errors.append(f"Canvas {i} missing painting annotation")
    image_path=PAGES/f"{i:03d}.jpg"
    if not image_path.exists(): errors.append(f"missing canonical page image {i:03d}.jpg"); continue
    digest=hashlib.sha256(image_path.read_bytes()).hexdigest()
    if i<=len(pages):
        row=pages[i-1]
        if row.get("pdf_page")!=i: errors.append(f"canvas map page sequence mismatch at {i}")
        if row.get("canvas_id")!=expected_canvas or row.get("image_url")!=expected_image: errors.append(f"canvas map URL mismatch at {i}")
        if row.get("image_sha256")!=digest: errors.append(f"image checksum mismatch at {i}")
        with Image.open(image_path) as image: width,height=image.size
        if row.get("width")!=width or row.get("height")!=height: errors.append(f"image dimensions mismatch at {i}")
        if i<=len(items) and (items[i-1].get("width")!=width or items[i-1].get("height")!=height): errors.append(f"Canvas dimensions mismatch at {i}")

appendix={79:369,80:370,81:371,82:372,83:373,84:374}
for pdf_page,printed_page in appendix.items():
    if len(pages)>=pdf_page and pages[pdf_page-1].get("printed_page")!=printed_page: errors.append(f"appendix page mapping lost: PDF {pdf_page} -> printed {printed_page}")
    if len(items)>=pdf_page:
        label=" ".join(items[pdf_page-1].get("label",{}).get("none",[]))
        if str(printed_page) not in label: errors.append(f"Canvas {pdf_page} label omits printed page {printed_page}")

profile=json.loads((ROOT/"source_profiles/steffel-1809.source.json").read_text(encoding="utf-8"))
if profile.get("witness",{}).get("witness_id")!=EXPECTED_WITNESS: errors.append("validator witness constant differs from source profile")

if errors: print("\n".join("ERROR: "+e for e in errors)); sys.exit(1)
print("OK: canonical Steffel IIIF Presentation 3 package has 84 checksum-derived static image Canvases, stable GitHub Pages IDs, exact appendix mapping and zero human-validation claim")
