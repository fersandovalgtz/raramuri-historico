#!/usr/bin/env python3
"""Verify whether the public Repositorio de Lenguas/Dropbox Steffel PDF is the exact RHD witness.

The public bibliography page links an 84-page Steffel PDF hosted on Dropbox. RHD must
not infer identity from title/page count alone: this probe downloads the linked binary
and compares SHA-256, byte size and PDF page count with the checksum-fixed project
facsimile. Exact binary identity is required before the URL can be used as a canonical
retrieval source or as the build input for a project-controlled IIIF publication.
"""

from pathlib import Path
import hashlib
import json
import sys
import urllib.request

from pypdf import PdfReader

URL = "https://www.dropbox.com/scl/fi/gda4acwz8ou0m68s4wwlr/1809_STEFFEL-Tarahumarisches-Worterbuch_libro.pdf?rlkey=n1kz2hoa4lfq6gq0me6rxsmgu&dl=1"
EXPECTED_SHA256 = "4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f"
EXPECTED_BYTES = 6251443
EXPECTED_PAGES = 84
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/steffel-public-source.pdf")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    req = urllib.request.Request(
        URL,
        headers={"User-Agent": "Raramuri-Historico-Digital/1.0 canonical-witness-source-probe"},
    )
    with urllib.request.urlopen(req, timeout=90) as response:
        raw = response.read()
        final_url = response.geturl()
        content_type = response.headers.get("Content-Type", "")

    if not raw.startswith(b"%PDF-"):
        raise SystemExit(
            "ERROR: public Steffel source did not return PDF; "
            f"content_type={content_type!r}; first_bytes={raw[:20]!r}; final_url={final_url!r}"
        )
    OUT.write_bytes(raw)
    digest = sha256(OUT)
    pages = len(PdfReader(str(OUT), strict=False).pages)
    exact = digest == EXPECTED_SHA256 and len(raw) == EXPECTED_BYTES and pages == EXPECTED_PAGES
    result = {
        "probe_id": "RHD-STEFFEL-PUBLIC-SOURCE-PROBE-1",
        "requested_url": URL,
        "resolved_url": final_url,
        "content_type": content_type,
        "sha256": digest,
        "bytes": len(raw),
        "pdf_pages": pages,
        "expected_sha256": EXPECTED_SHA256,
        "expected_bytes": EXPECTED_BYTES,
        "expected_pdf_pages": EXPECTED_PAGES,
        "exact_binary_identity": exact,
        "canonical_for_rhd_if_exact": exact,
        "human_validation_claimed": False,
    }
    print("RHD_STEFFEL_PUBLIC_SOURCE=" + json.dumps(result, ensure_ascii=False, sort_keys=True))
    if not exact:
        raise SystemExit(
            "ERROR: linked public Steffel PDF is not the checksum-fixed RHD facsimile; "
            f"sha256={digest}; bytes={len(raw)}; pages={pages}"
        )
    print("OK: public Steffel PDF is bit-identical to the checksum-fixed RHD canonical facsimile")


if __name__ == "__main__":
    main()
