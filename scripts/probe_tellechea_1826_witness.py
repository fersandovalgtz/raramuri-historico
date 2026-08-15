#!/usr/bin/env python3
"""Verify the checksum-fixed public DGB witness for Tellechea 1826.

This is a binary-identity gate only. It does not perform textual, linguistic or human
adjudication. Any provider-side change to the PDF must be surfaced rather than silently
accepted as the same RHD witness.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import json
import sys
import urllib.request

from pypdf import PdfReader

URL = "https://dgb.cultura.gob.mx/recursos/documentos/lenguasindigenas/Compendiogramaticalpara.pdf"
EXPECTED_SHA256 = "c67b7942090613c494d8057be8aff59ea13a11519c29eae469afad8a85c30dfc"
EXPECTED_BYTES = 95088307
EXPECTED_PAGES = 205
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
        headers={"User-Agent": "Raramuri-Historico-Digital/1.0 witness-verifier"},
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
    digest = sha256(OUT)
    reader = PdfReader(str(OUT), strict=False)
    page_count = len(reader.pages)

    errors = []
    if digest != EXPECTED_SHA256:
        errors.append(f"sha256 changed: expected={EXPECTED_SHA256} actual={digest}")
    if len(raw) != EXPECTED_BYTES:
        errors.append(f"byte size changed: expected={EXPECTED_BYTES} actual={len(raw)}")
    if page_count != EXPECTED_PAGES:
        errors.append(f"page count changed: expected={EXPECTED_PAGES} actual={page_count}")
    if errors:
        raise SystemExit("ERROR: checksum-fixed Tellechea witness changed; " + "; ".join(errors))

    metadata = {
        "witness_id": "RHD-WIT-TELLECHEA-1826-DGB",
        "source_id": "RHD-SRC-TELLECHEA-1826",
        "provider": "Dirección General de Bibliotecas, Secretaría de Cultura, México",
        "requested_url": URL,
        "resolved_url": final_url,
        "content_type": content_type,
        "bytes": len(raw),
        "sha256": digest,
        "pdf_pages": page_count,
        "pdf_header": raw[:8].decode("latin-1", errors="replace"),
        "human_validation_claimed": False,
        "identity_status": "checksum_fixed_public_witness_verified",
        "scope": "binary identity verification only; no textual or linguistic adjudication",
    }
    print("OK: checksum-fixed Tellechea 1826 witness verified")
    print("RHD_TELLECHEA_WITNESS=" + json.dumps(metadata, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
