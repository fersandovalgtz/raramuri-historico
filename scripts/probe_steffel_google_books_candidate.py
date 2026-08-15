#!/usr/bin/env python3
"""Probe Google Books volume M2s6AAAAcAAJ for the complete canonical Steffel scan.

Google's JSON API is useful metadata but not a gate: if it rate-limits the runner, the
probe continues against classic public book/download/search routes. Any retrieved PDF
is compared as a complete 84-page image sequence against fixed RHD fingerprints.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib,json,re,subprocess,urllib.parse,urllib.request
from PIL import Image
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]; VID="M2s6AAAAcAAJ"
API=f"https://www.googleapis.com/books/v1/volumes/{VID}"
FP=ROOT/"data/iiif/steffel-1809-all84-page-fingerprints.json"
PDF=Path("/tmp/steffel-google-books-candidate.pdf"); REPORT=Path("/tmp/steffel-google-books-candidate.json")
UA="Mozilla/5.0 Raramuri-Historico-Digital/1.0"
TITLE="Nachrichten von verschiedenen Ländern des Spanischen Amerika"

def get(url,accept="*/*",timeout=180):
 req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":accept,"Accept-Language":"en-US,en;q=0.8"})
 with urllib.request.urlopen(req,timeout=timeout) as r: return r.read(),r.geturl(),r.headers.get("Content-Type","")
def get_json(url):
 raw,_,_=get(url,"application/json",60); return json.loads(raw.decode("utf-8"))
def nkey(p):
 m=re.search(r"(\d+)$",p.stem); return int(m.group(1)) if m else 0
def dhash(path):
 with Image.open(path) as im:
  g=im.convert("L"); mask=g.point(lambda p:255 if p<245 else 0); bbox=mask.getbbox()
  if bbox:
   x0,y0,x1,y1=bbox; px=max(2,int((x1-x0)*.02)); py=max(2,int((y1-y0)*.02)); g=g.crop((max(0,x0-px),max(0,y0-py),min(g.width,x1+px),min(g.height,y1+py)))
  s=g.resize((17,16),Image.Resampling.LANCZOS); px=list(s.getdata()); v=0
  for y in range(16):
   for x in range(16): v=(v<<1)|int(px[y*17+x+1]>px[y*17+x])
  return f"{v:064x}"
def ham(a,b): return (int(a,16)^int(b,16)).bit_count()
def pct(v,p):
 o=sorted(v); return o[min(len(o)-1,max(0,int(round((len(o)-1)*p))))]
def render_hashes(pdf):
 with TemporaryDirectory(prefix="rhd-gbooks-") as td:
  pref=Path(td)/"p"; subprocess.run(["pdftoppm","-r","72","-gray","-png",str(pdf),str(pref)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  return [dhash(p) for p in sorted(Path(td).glob("p-*.png"),key=nkey)]
def download_candidates(meta):
 out=[]; pdf=((meta or {}).get("accessInfo",{}).get("pdf") or {})
 for k in ("downloadLink","acsTokenLink"):
  u=pdf.get(k)
  if isinstance(u,str) and u.startswith("http"): out.append((f"api_{k}",u))
 slug=urllib.parse.quote("Nachrichten_von_verschiedenen_Laendern_des_Spanischen_Amerika")
 out += [
  ("books_download_plain",f"https://books.google.com/books/download?id={VID}&output=pdf"),
  ("books_download_slug",f"https://books.google.com/books/download/{slug}.pdf?id={VID}&output=pdf"),
  ("play_download_plain",f"https://play.google.com/books/download?id={VID}&output=pdf"),
  ("play_download_slug",f"https://play.google.com/books/download/{slug}.pdf?id={VID}&output=pdf"),
 ]
 seen=set(); return [(k,u) for k,u in out if not (u in seen or seen.add(u))]
def probe_search_endpoint():
 urls=[
  f"https://books.google.com/books?jscmd=SearchWithinVolume2&q=Tarahumarisches&vid={VID}",
  f"https://books.google.com/books?jscmd=SearchWithinVolume2&q=Steffel&vid={VID}",
 ]
 reports=[]
 for u in urls:
  try:
   raw,final,ctype=get(u,"application/json,text/plain,*/*",60)
   reports.append({"url":u,"resolved_url":final,"content_type":ctype,"bytes":len(raw),"sample":raw[:1200].decode("utf-8",errors="replace")})
  except Exception as e: reports.append({"url":u,"error":f"{type(e).__name__}: {e}"})
 return reports

def main():
 meta={}; meta_error=None
 try: meta=get_json(API)
 except Exception as e: meta_error=f"{type(e).__name__}: {e}"
 canonical=json.loads(FP.read_text(encoding="utf-8")).get("hashes_by_pdf_page_1_based",[])
 if len(canonical)!=84: raise SystemExit("ERROR: canonical fingerprint set must contain exactly 84 hashes")
 attempts=[]; chosen=None
 for kind,url in download_candidates(meta):
  try:
   raw,final,ctype=get(url,"application/pdf,*/*;q=0.8",180); is_pdf=raw.startswith(b"%PDF-")
   attempts.append({"kind":kind,"requested_url":url,"resolved_url":final,"content_type":ctype,"bytes":len(raw),"is_pdf":is_pdf,"first_bytes":raw[:16].decode("latin-1",errors="replace")})
   if is_pdf: PDF.write_bytes(raw); chosen=attempts[-1]; break
  except Exception as e: attempts.append({"kind":kind,"requested_url":url,"error":f"{type(e).__name__}: {e}"})
 search_reports=probe_search_endpoint()
 sequence=None; pdf_meta=None
 if chosen:
  reader=PdfReader(str(PDF),strict=False); hashes=render_hashes(PDF); best=None
  for start in range(max(0,len(hashes)-83)):
   ds=[ham(canonical[j],hashes[start+j]) for j in range(84)]; exact=sum(d==0 for d in ds); le8=sum(d<=8 for d in ds); le16=sum(d<=16 for d in ds)
   score=(sum(ds)/84,pct(ds,.90),max(ds),-exact,-le8,-le16)
   if best is None or score<best[0]: best=(score,start,ds,exact,le8,le16)
  if best:
   _,start,ds,exact,le8,le16=best; sequence={"candidate_pdf_page_start_1_based":start+1,"candidate_pdf_page_end_1_based":start+84,"mean_hamming":round(sum(ds)/84,4),"median_hamming":pct(ds,.5),"p90_hamming":pct(ds,.9),"max_hamming":max(ds),"exact_page_hashes":exact,"pages_hamming_le_8":le8,"pages_hamming_le_16":le16,"distances_by_canonical_page":ds}
  raw=PDF.read_bytes(); pdf_meta={"pages":len(reader.pages),"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
 result={"probe_id":"RHD-STEFFEL-GOOGLE-BOOKS-PROBE-2","volume_id":VID,"title":((meta.get("volumeInfo") or {}).get("title") if meta else TITLE),"api_metadata_available":bool(meta),"api_error":meta_error,"api_public_domain":((meta.get("accessInfo") or {}).get("publicDomain") if meta else None),"api_viewability":((meta.get("accessInfo") or {}).get("viewability") if meta else None),"pdf_available":bool(chosen),"download":chosen,"downloaded_pdf":pdf_meta,"attempts":attempts,"search_within_volume":search_reports,"whole_witness_sequence":sequence,"canonical_for_rhd":False,"human_validation_claimed":False}
 REPORT.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
 print("RHD_STEFFEL_GOOGLE_BOOKS="+json.dumps(result,ensure_ascii=False,sort_keys=True))
 if sequence: print(f"INFO: Google Books best 84-page sequence {sequence['candidate_pdf_page_start_1_based']}-{sequence['candidate_pdf_page_end_1_based']}; mean={sequence['mean_hamming']}; p90={sequence['p90_hamming']}; max={sequence['max_hamming']}; exact={sequence['exact_page_hashes']}/84; <=8={sequence['pages_hamming_le_8']}/84; <=16={sequence['pages_hamming_le_16']}/84")
 elif not chosen: print("INFO: no unauthenticated public PDF route returned a PDF; SearchWithinVolume diagnostics were preserved for page-image discovery")

if __name__=="__main__": main()
