#!/usr/bin/env python3
"""Build the 84 static IIIF JPEG page assets from the exact canonical Steffel PDF.

Usage:
  python scripts/build_steffel_iiif_images.py /path/to/steffel.pdf /output/pages

The script refuses any source whose SHA-256, byte size, or page count differs from the
canonical RHD witness. It renders with the parameters used to measure the versioned
Canvas dimensions and verifies all 84 output dimensions. It does not publish files.
"""
from pathlib import Path
import hashlib, json, shutil, subprocess, sys, tempfile
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
DIMS=ROOT/"data/iiif/steffel-1809-canonical-canvas-dimensions.json"
EXPECTED_SHA="4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f"
EXPECTED_BYTES=6251443
EXPECTED_PAGES=84

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def main():
    if len(sys.argv)!=3: raise SystemExit("usage: build_steffel_iiif_images.py SOURCE.pdf OUTPUT_DIR")
    source=Path(sys.argv[1]); out=Path(sys.argv[2])
    if not source.exists(): raise SystemExit(f"ERROR: source PDF missing: {source}")
    if source.stat().st_size!=EXPECTED_BYTES or sha256(source)!=EXPECTED_SHA:
        raise SystemExit("ERROR: refusing noncanonical Steffel binary")
    info=subprocess.run(["pdfinfo",str(source)],check=True,text=True,stdout=subprocess.PIPE).stdout
    page_line=next((x for x in info.splitlines() if x.startswith("Pages:")),"")
    pages=int(page_line.split(":",1)[1].strip()) if page_line else -1
    if pages!=EXPECTED_PAGES: raise SystemExit(f"ERROR: expected 84 pages, got {pages}")
    dims=json.loads(DIMS.read_text(encoding="utf-8"))["dimensions_by_pdf_page_1_based"]
    if len(dims)!=84: raise SystemExit("ERROR: invalid dimension inventory")
    out.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="rhd-steffel-iiif-") as td:
        prefix=Path(td)/"page"
        subprocess.run(["pdftoppm","-jpeg","-jpegopt","quality=80","-r","120",str(source),str(prefix)],check=True)
        rendered=sorted(Path(td).glob("page-*.jpg"))
        if len(rendered)!=84: raise SystemExit(f"ERROR: renderer produced {len(rendered)} pages")
        assets=[]
        for i,(src,expected) in enumerate(zip(rendered,dims),1):
            with Image.open(src) as im:
                actual=list(im.size)
            if actual!=expected: raise SystemExit(f"ERROR: page {i} dimensions {actual} != expected {expected}")
            dst=out/f"{i:03d}.jpg"; shutil.copyfile(src,dst)
            assets.append({"pdf_page":i,"filename":dst.name,"width":actual[0],"height":actual[1],"bytes":dst.stat().st_size,"sha256":sha256(dst)})
    manifest={
        "asset_manifest_id":"RHD-S1809-IIIF-STATIC-JPEG-ASSETS-120DPI-01",
        "source_pdf_sha256":EXPECTED_SHA,"source_pdf_bytes":EXPECTED_BYTES,"source_pdf_pages":EXPECTED_PAGES,
        "render":"pdftoppm -jpeg -jpegopt quality=80 -r 120","asset_count":len(assets),
        "publication_status":"built_locally_not_published","human_validation_claimed":False,"assets":assets,
    }
    (out.parent/"page-assets.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"OK: built {len(assets)} exact-witness IIIF JPEG assets in {out}; publication remains a separate gate")

if __name__=="__main__": main()
