#!/usr/bin/env python3
"""Probe the mutable public Steffel PDF against the fixed RHD witness.

This diagnostic is intentionally cheap. The external provider is mutable and therefore
cannot be a canonical dependency. We test binary identity (SHA-256, bytes, page count)
and record drift. We do NOT render hundreds of pages merely to reconfirm that a changed
external wrapper is noncanonical; perceptual comparison belongs to dedicated candidate-
witness probes.
"""
from pathlib import Path
import hashlib, json, sys, urllib.request
from pypdf import PdfReader

URL="https://www.dropbox.com/scl/fi/gda4acwz8ou0m68s4wwlr/1809_STEFFEL-Tarahumarisches-Worterbuch_libro.pdf?rlkey=n1kz2hoa4lfq6gq0me6rxsmgu&dl=1"
EXPECTED_SHA256="4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f"
EXPECTED_BYTES=6251443
EXPECTED_PAGES=84
OUT=Path(sys.argv[1]) if len(sys.argv)>1 else Path("/tmp/steffel-public-source.pdf")
REPORT=Path(sys.argv[2]) if len(sys.argv)>2 else Path("/tmp/steffel-public-source-probe.json")


def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda:fh.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    req=urllib.request.Request(URL,headers={"User-Agent":"Raramuri-Historico-Digital/1.0 checksum-first-public-source-probe"})
    with urllib.request.urlopen(req,timeout=120) as response:
        raw=response.read()
        final_url=response.geturl()
        content_type=response.headers.get("Content-Type","")
    if not raw.startswith(b"%PDF-"):
        raise SystemExit(f"ERROR: public source did not return PDF; content_type={content_type!r}; final_url={final_url!r}")
    OUT.write_bytes(raw)
    digest=sha256(OUT)
    pages=len(PdfReader(str(OUT),strict=False).pages)
    exact=(digest==EXPECTED_SHA256 and len(raw)==EXPECTED_BYTES and pages==EXPECTED_PAGES)
    result={
        "probe_id":"RHD-STEFFEL-PUBLIC-SOURCE-PROBE-3",
        "requested_url":URL,
        "resolved_url":final_url,
        "content_type":content_type,
        "sha256":digest,
        "bytes":len(raw),
        "pdf_pages":pages,
        "expected_sha256":EXPECTED_SHA256,
        "expected_bytes":EXPECTED_BYTES,
        "expected_pdf_pages":EXPECTED_PAGES,
        "exact_binary_identity":exact,
        "binary_identity_status":"exact" if exact else "external_provider_drift",
        "canonical_for_rhd":exact,
        "perceptual_comparison_performed":False,
        "perceptual_comparison_policy":"not performed for mutable provider drift; use dedicated candidate-witness probes if identity investigation is scientifically warranted",
        "human_validation_claimed":False,
    }
    REPORT.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("RHD_STEFFEL_PUBLIC_SOURCE="+json.dumps(result,ensure_ascii=False,sort_keys=True))
    if exact:
        print("OK: mutable public URL currently serves the bit-identical canonical witness")
    else:
        print(f"INFO: mutable provider drift: pages={pages}, bytes={len(raw)}, sha256={digest}; canonical witness remains {EXPECTED_PAGES} pages / {EXPECTED_BYTES} bytes / {EXPECTED_SHA256}")

if __name__=="__main__":
    main()
