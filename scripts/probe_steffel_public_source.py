#!/usr/bin/env python3
"""Probe the mutable public Steffel PDF against the fixed RHD witness.

Binary identity is tested first. If the provider has replaced the PDF container, the
probe performs a second, non-adjudicative whole-witness image-sequence comparison: it
renders the public PDF with the same 72-dpi grayscale recipe used to fingerprint all
84 canonical pages and searches every contiguous 84-page window. This diagnostic does
NOT itself promote the public source to canonical status; downstream builders must
apply an explicit acceptance gate to the measured distances.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib, json, re, subprocess, sys, urllib.request
from PIL import Image
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
URL="https://www.dropbox.com/scl/fi/gda4acwz8ou0m68s4wwlr/1809_STEFFEL-Tarahumarisches-Worterbuch_libro.pdf?rlkey=n1kz2hoa4lfq6gq0me6rxsmgu&dl=1"
EXPECTED_SHA256="4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f"
EXPECTED_BYTES=6251443; EXPECTED_PAGES=84
FINGERPRINTS=ROOT/"data/iiif/steffel-1809-all84-page-fingerprints.json"
OUT=Path(sys.argv[1]) if len(sys.argv)>1 else Path("/tmp/steffel-public-source.pdf")
REPORT=Path(sys.argv[2]) if len(sys.argv)>2 else Path("/tmp/steffel-public-source-probe.json")

def sha256(path):
 h=hashlib.sha256()
 with path.open("rb") as fh:
  for chunk in iter(lambda:fh.read(1024*1024),b""): h.update(chunk)
 return h.hexdigest()
def nkey(path):
 m=re.search(r"(\d+)$",path.stem); return int(m.group(1)) if m else 0
def dhash256(path):
 with Image.open(path) as image:
  g=image.convert("L"); mask=g.point(lambda p:255 if p<245 else 0); bbox=mask.getbbox()
  if bbox:
   x0,y0,x1,y1=bbox; px=max(2,int((x1-x0)*.02)); py=max(2,int((y1-y0)*.02)); g=g.crop((max(0,x0-px),max(0,y0-py),min(g.width,x1+px),min(g.height,y1+py)))
  small=g.resize((17,16),Image.Resampling.LANCZOS); pixels=list(small.getdata()); value=0
  for y in range(16):
   row=y*17
   for x in range(16): value=(value<<1)|int(pixels[row+x+1]>pixels[row+x])
  return f"{value:064x}"
def hamming(a,b): return (int(a,16)^int(b,16)).bit_count()
def percentile(values,p):
 if not values: return None
 ordered=sorted(values); idx=min(len(ordered)-1,max(0,int(round((len(ordered)-1)*p))))
 return ordered[idx]

def render_hashes(pdf):
 with TemporaryDirectory(prefix="rhd-steffel-public-fp-") as td:
  prefix=Path(td)/"page"
  subprocess.run(["pdftoppm","-r","72","-gray","-png",str(pdf),str(prefix)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  images=sorted(Path(td).glob("page-*.png"),key=nkey)
  return [dhash256(p) for p in images]

def main():
 req=urllib.request.Request(URL,headers={"User-Agent":"Raramuri-Historico-Digital/1.0 public-source-sequence-probe"})
 with urllib.request.urlopen(req,timeout=120) as response:
  raw=response.read(); final_url=response.geturl(); content_type=response.headers.get("Content-Type","")
 if not raw.startswith(b"%PDF-"): raise SystemExit(f"ERROR: public source did not return PDF; content_type={content_type!r}; final_url={final_url!r}")
 OUT.write_bytes(raw); digest=sha256(OUT); pages=len(PdfReader(str(OUT),strict=False).pages)
 exact=(digest==EXPECTED_SHA256 and len(raw)==EXPECTED_BYTES and pages==EXPECTED_PAGES)
 fp=json.loads(FINGERPRINTS.read_text(encoding="utf-8")); canonical=fp.get("hashes_by_pdf_page_1_based",[])
 if len(canonical)!=84 or fp.get("source_sha256")!=EXPECTED_SHA256: raise SystemExit("ERROR: canonical all-84 fingerprint set is invalid")
 public_hashes=render_hashes(OUT)
 best=None
 if len(public_hashes)>=84:
  for start in range(0,len(public_hashes)-83):
   distances=[hamming(canonical[j],public_hashes[start+j]) for j in range(84)]
   mean=sum(distances)/84; p90=percentile(distances,.90); maxd=max(distances); exact_hashes=sum(d==0 for d in distances); within16=sum(d<=16 for d in distances)
   score=(mean,p90,maxd,-exact_hashes,-within16)
   if best is None or score<best[0]: best=(score,start,distances,exact_hashes,within16)
 sequence=None
 if best:
  score,start,distances,exact_hashes,within16=best
  sequence={"public_pdf_page_start_1_based":start+1,"public_pdf_page_end_1_based":start+84,"mean_hamming":round(sum(distances)/84,4),"median_hamming":percentile(distances,.50),"p90_hamming":percentile(distances,.90),"max_hamming":max(distances),"exact_page_hashes":exact_hashes,"pages_hamming_le_16":within16,"distances_by_canonical_page":distances}
 result={"probe_id":"RHD-STEFFEL-PUBLIC-SOURCE-PROBE-2","requested_url":URL,"resolved_url":final_url,"content_type":content_type,"sha256":digest,"bytes":len(raw),"pdf_pages":pages,"expected_sha256":EXPECTED_SHA256,"expected_bytes":EXPECTED_BYTES,"expected_pdf_pages":EXPECTED_PAGES,"exact_binary_identity":exact,"binary_identity_status":"exact" if exact else "changed_public_pdf_container","whole_witness_sequence":sequence,"canonical_for_rhd":exact,"human_validation_claimed":False}
 REPORT.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
 print("RHD_STEFFEL_PUBLIC_SOURCE="+json.dumps(result,ensure_ascii=False,sort_keys=True))
 if exact: print("OK: public PDF is bit-identical to the checksum-fixed RHD witness")
 elif sequence: print(f"INFO: public PDF wrapper differs; best 84-page sequence is public pages {sequence['public_pdf_page_start_1_based']}-{sequence['public_pdf_page_end_1_based']} with mean dHash distance {sequence['mean_hamming']}, p90 {sequence['p90_hamming']}, max {sequence['max_hamming']}, exact hashes {sequence['exact_page_hashes']}/84")
 else: print("INFO: public PDF wrapper differs and contains fewer than 84 renderable pages; no full sequence candidate")

if __name__=="__main__": main()
