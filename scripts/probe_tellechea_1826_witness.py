#!/usr/bin/env python3
"""Fetch and fingerprint the public DGB Tellechea 1826 PDF witness candidate.

This script is intentionally non-adjudicative. Its job is only to establish whether a
reproducible binary exists at the declared public URI and to emit machine-verifiable
identity metadata (SHA-256, byte size, PDF page count, header/trailer sanity).
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import json
import sys
import urllib.request

from pypdf import PdfReader

# DGB's public viewer is called with
#   /recursos/libro_flip/index.php?libro=../documentos/lenguasindigenas/Compendiogramaticalpara.pdf
# Therefore the relative PDF path resolves under /recursos/documentos/, not /documentos/.
URL = "https://dgb.cultura.gob.mx/recursos/documentos/lenguasindigenas/Compendiogramaticalpara.pdf"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/tellechea-1826-dgb.pdf")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    req = urllib.request.Request(
        URL,
        headers={"User-Agent": "Raramuri-Historico-Digital/1.0 witness-probe"},
    )
    with urllib.request.urlopen(req, timeout=90) as response:
        raw = response.read()
        content_type = response.headers.get("Content-Type", "")
        final_url = response.geturl()

    if not raw.startswith(b"%PDF-"):
        raise SystemExit(
            f"ERROR: DGB Tellechea endpoint did not return a PDF; content_type={content_type!r}; "
            f"first_bytes={raw[:20]!r}; final_url={final_url!r}"
        )

    OUT.write_bytes(raw)
    reader = PdfReader(str(OUT), strict=False)
    page_count = len(reader.pages)
    if page_count < 150:
        raise SystemExit(f"ERROR: implausibly short Tellechea PDF: {page_count} pages")

    metadata = {
        "witness_probe_id": "RHD-TELLECHEA-1826-DGB-PROBE-1",
        "source_id": "RHD-SRC-TELLECHEA-1826",
        "provider": "Dirección General de Bibliotecas, Secretaría de Cultura, México",
        "requested_url": URL,
        "resolved_url": final_url,
        "content_type": content_type,
        "bytes": len(raw),
        "sha256": sha256(OUT),
        "pdf_pages": page_count,
        "pdf_header": raw[:8].decode("latin-1", errors="replace"),
        "human_validation_claimed": False,
        "scope": "binary identity probe only; no textual or linguistic adjudication",
    }
    print("RHD_TELLECHEA_WITNESS=" + json.dumps(metadata, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
