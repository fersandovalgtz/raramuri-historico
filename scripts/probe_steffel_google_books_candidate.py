#!/usr/bin/env python3
"""Probe the free Google Books 1809 volume for the canonical Steffel scan sequence.

This script is diagnostic and non-adjudicative. It retrieves Google Books metadata for
volume M2s6AAAAcAAJ, follows a public PDF download link when the API exposes one, renders
the candidate at the exact same recipe used for the fixed 84-page RHD fingerprints,
and searches every contiguous 84-page window. It never promotes a candidate by itself.
"""
from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib, json, re, subprocess, sys, urllib.parse, urllib.request
from PIL import Image
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
VOLUME_ID="M2s6AAAAcAAJ"
API=f"https://www.googleapis.com/books/v1/volumes/{VOLUME_ID}"
FINGERPRINTS=ROOT/"data/iiif/steffel-1809-all84-page-fingerprints.json"
PDF=Path("/tmp/steffel-google-books-candidate.pdf")
REPORT=Path("/tmp/steffel-google-books-candidate.json")
UA="Raramuri-Historico-Digital/1.0 google-books-witness-probe"


def fetch_json(url):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=60) as r: return json.loads(r.read().decode("utf-8"))

def fetch_bytes(url):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/pdf,*/*;q=0.8"})
    with urllib.request.urlopen(req,timeout=180) as r: return r.read(),r.geturl(),r.headers.get("Content-Type","")

def nkey(path):
    m=re.search(r"(\d+)$",path.stem); return int(m.group(1)) if m else 0

def dhash256(path):
    with Image.open(path) as image:
        g=image.convert("L"); mask=g.point(lambda p:255 if p<245 else 0); bbox=mask.getbbox()
        if bbox:
            x0,y0,x1,y1=bbox; px=max(2,int((x1-x0)*.02)); py=max(2,int((y1-y0)*.02))
            g=g.crop((max(0,x0-px),max(0,y0-py),min(g.width,x1+px),min(g.height,y1+py)))
        small=g.resize((17,16),Image.Resampling.LANCZOS); pixels=list(small.getdata()); value=0
        for y in range(16):
            row=y*17
            for x in range(16): value=(value<<1)|int(pixels[row+x+1]>pixels[row+x])
        return f"{value:064x}"

def hamming(a,b): return (int(a,16)^int(b,16)).bit_count()
def percentile(values,p):
    ordered=sorted(values); idx=min(len(ordered)-1,max(0,int(round((len(ordered)-1)*p))))
    return ordered[idx]

def render_hashes(pdf):
    with TemporaryDirectory(prefix="rhd-gbooks-steffel-") as td:
        prefix=Path(td)/"page"
        subprocess.run(["pdftoppm","-r","72","-gray","-png",str(pdf),str(prefix)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        imgs=sorted(Path(td).glob("page-*.png"),key=nkey)
        return [dhash256(p) for p in imgs]

def candidates_from_metadata(meta):
    access=meta.get("accessInfo",{}); pdf=access.get("pdf") or {}
    urls=[]
    for key in ("downloadLink","acsTokenLink"):
        u=pdf.get(key)
        if isinstance(u,str) and u.startswith("http"): urls.append({"kind":f"accessInfo.pdf.{key}","url":u})
    # Some public-domain Google Books volumes expose a classic download route even when
    # the API omits downloadLink. Keep it as a fallback candidate and let PDF validation decide.
    urls.extend([
        {"kind":"classic_output_pdf","url":f"https://books.google.com/books/download?id={VOLUME_ID}&output=pdf"},
        {"kind":"classic_jscmd_download","url":f"https://books.google.com/books?jscmd=SearchWithinVolume2&q=&vid={VOLUME_ID}"},
    ])
    seen=set(); out=[]
    for x in urls:
        if x["url"] not in seen: seen.add(x["url"]); out.append(x)
    return out

def main():
    meta=fetch_json(API)
    fp=json.loads(FINGERPRINTS.read_text(encoding="utf-8")); canonical=fp.get("hashes_by_pdf_page_1_based",[])
    if len(canonical)!=84: raise SystemExit("ERROR: canonical fingerprint set must contain 84 hashes")
    attempts=[]; downloaded=None
    for cand in candidates_from_metadata(meta):
        try:
            raw,final_url,ctype=fetch_bytes(cand["url"])
            is_pdf=raw.startswith(b"%PDF-")
            attempt={"kind":cand["kind"],"requested_url":cand["url"],"resolved_url":final_url,"content_type":ctype,"bytes":len(raw),"is_pdf":is_pdf,"first_bytes":raw[:16].decode("latin-1",errors="replace")}
            attempts.append(attempt)
            if is_pdf:
                PDF.write_bytes(raw); downloaded=attempt; break
        except Exception as exc:
            attempts.append({"kind":cand["kind"],"requested_url":cand["url"],"error":f"{type(exc).__name__}: {exc}"})
    if downloaded is None:
        result={"probe_id":"RHD-STEFFEL-GOOGLE-BOOKS-PROBE-1","volume_id":VOLUME_ID,"api":API,"title":meta.get("volumeInfo",{}).get("title"),"page_count_metadata":meta.get("volumeInfo",{}).get("pageCount"),"access_viewability":meta.get("accessInfo",{}).get("viewability"),"public_domain":meta.get("accessInfo",{}).get("publicDomain"),"pdf_available":False,"attempts":attempts,"whole_witness_sequence":None,"canonical_for_rhd":False,"human_validation_claimed":False}
        REPORT.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        print("RHD_STEFFEL_GOOGLE_BOOKS="+json.dumps(result,ensure_ascii=False,sort_keys=True)); sys.exit(0)
    reader=PdfReader(str(PDF),strict=False); public_hashes=render_hashes(PDF); best=None
    if len(public_hashes)>=84:
        for start in range(len(public_hashes)-83):
            distances=[hamming(canonical[j],public_hashes[start+j]) for j in range(84)]
            exact=sum(d==0 for d in distances); le8=sum(d<=8 for d in distances); le16=sum(d<=16 for d in distances)
            score=(sum(distances)/84,percentile(distances,.90),max(distances),-exact,-le8,-le16)
            if best is None or score<best[0]: best=(score,start,distances,exact,le8,le16)
    sequence=None
    if best:
        score,start,distances,exact,le8,le16=best
        sequence={"candidate_pdf_page_start_1_based":start+1,"candidate_pdf_page_end_1_based":start+84,"mean_hamming":round(sum(distances)/84,4),"median_hamming":percentile(distances,.50),"p90_hamming":percentile(distances,.90),"max_hamming":max(distances),"exact_page_hashes":exact,"pages_hamming_le_8":le8,"pages_hamming_le_16":le16,"distances_by_canonical_page":distances}
    raw=PDF.read_bytes(); result={"probe_id":"RHD-STEFFEL-GOOGLE-BOOKS-PROBE-1","volume_id":VOLUME_ID,"api":API,"title":meta.get("volumeInfo",{}).get("title"),"page_count_metadata":meta.get("volumeInfo",{}).get("pageCount"),"access_viewability":meta.get("accessInfo",{}).get("viewability"),"public_domain":meta.get("accessInfo",{}).get("publicDomain"),"pdf_available":True,"download":downloaded,"downloaded_pdf_pages":len(reader.pages),"downloaded_pdf_bytes":len(raw),"downloaded_pdf_sha256":hashlib.sha256(raw).hexdigest(),"attempts":attempts,"whole_witness_sequence":sequence,"canonical_for_rhd":False,"human_validation_claimed":False}
    REPORT.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("RHD_STEFFEL_GOOGLE_BOOKS="+json.dumps(result,ensure_ascii=False,sort_keys=True))
    if sequence: print(f"INFO: Google Books best 84-page sequence {sequence['candidate_pdf_page_start_1_based']}-{sequence['candidate_pdf_page_end_1_based']}; mean={sequence['mean_hamming']}; p90={sequence['p90_hamming']}; max={sequence['max_hamming']}; exact={sequence['exact_page_hashes']}/84; <=8={sequence['pages_hamming_le_8']}/84; <=16={sequence['pages_hamming_le_16']}/84")

if __name__=="__main__": main()
