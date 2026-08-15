#!/usr/bin/env python3
"""Build the 84 lightweight PNG72 publication derivatives from canonical Steffel.

The PDF is the identity authority. The script refuses any other binary, renders at
72 dpi grayscale with pdftoppm, converts each page to a one-bit image using the
versioned threshold rule, and can verify the resulting distribution bytes against
`data/iiif/steffel-1809-published-png72-assets.json`.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile

from PIL import Image
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
INVENTORY=ROOT/"data/iiif/steffel-1809-published-png72-assets.json"
EXPECTED_SHA="4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f"
EXPECTED_BYTES=6251443
EXPECTED_PAGES=84


def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda:fh.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("pdf",help="checksum-fixed canonical Steffel PDF")
    ap.add_argument("output_dir")
    ap.add_argument("--verify-inventory",action="store_true")
    args=ap.parse_args()
    pdf=Path(args.pdf); out=Path(args.output_dir)
    if not pdf.exists(): raise SystemExit("ERROR: source PDF missing")
    if pdf.stat().st_size!=EXPECTED_BYTES: raise SystemExit(f"ERROR: source bytes mismatch: {pdf.stat().st_size}")
    digest=sha256(pdf)
    if digest!=EXPECTED_SHA: raise SystemExit(f"ERROR: source SHA-256 mismatch: {digest}")
    pages=len(PdfReader(str(pdf)).pages)
    if pages!=EXPECTED_PAGES: raise SystemExit(f"ERROR: source page count mismatch: {pages}")
    if shutil.which("pdftoppm") is None: raise SystemExit("ERROR: pdftoppm unavailable")

    inventory=json.loads(INVENTORY.read_text(encoding="utf-8"))
    expected=inventory.get("assets",[])
    if inventory.get("source_pdf_sha256")!=EXPECTED_SHA or inventory.get("asset_count")!=84 or len(expected)!=84:
        raise SystemExit("ERROR: publication inventory does not match canonical witness / 84-page contract")

    out.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="rhd-steffel-png72-") as td:
        prefix=Path(td)/"page"
        subprocess.run(["pdftoppm","-r","72","-gray","-png",str(pdf),str(prefix)],check=True,stdout=subprocess.DEVNULL)
        raws=sorted(Path(td).glob("page-*.png"),key=lambda p:int(p.stem.split("-")[-1]))
        if len(raws)!=84: raise SystemExit(f"ERROR: pdftoppm produced {len(raws)} pages, expected 84")
        produced=[]
        for i,src in enumerate(raws,1):
            with Image.open(src) as original:
                gray=original.convert("L")
                # Versioned rule: values > 204 become white; values <= 204 become black.
                # mode='1' yields the explicit one-bit distribution representation.
                bw=gray.point(lambda x:255 if x>204 else 0,mode="1")
                dest=out/f"{i:03d}.png"
                bw.save(dest,format="PNG",optimize=False,compress_level=9)
                produced.append({"pdf_page":i,"filename":dest.name,"width":bw.width,"height":bw.height,"bytes":dest.stat().st_size,"sha256":sha256(dest)})

    if args.verify_inventory:
        mismatches=[]
        for got,want in zip(produced,expected,strict=True):
            for key in ("pdf_page","filename","width","height","bytes","sha256"):
                if got.get(key)!=want.get(key): mismatches.append(f"page {got['pdf_page']} {key}: got={got.get(key)} expected={want.get(key)}")
        if mismatches:
            raise SystemExit("ERROR: generated PNG72 bytes differ from versioned publication inventory:\n"+"\n".join(mismatches[:30]))
    print(json.dumps({"source_sha256":digest,"source_bytes":EXPECTED_BYTES,"source_pages":pages,"png_pages":len(produced),"total_png_bytes":sum(x["bytes"] for x in produced),"inventory_byte_verified":bool(args.verify_inventory),"human_validation_claimed":False},ensure_ascii=False,indent=2))

if __name__=="__main__": main()
