#!/usr/bin/env python3
"""Verify the checksum-fixed DGB witness for Tellechea 1826 and characterize its text layer.

Binary identity is a hard gate. Embedded-text measurements are diagnostic only and are
never promoted to diplomatic transcription or human validation.
"""

from pathlib import Path
import hashlib
import json
import re
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


def compact(text: str, limit: int = 160) -> str:
    return re.sub(r"\s+", " ", text or "").strip()[:limit]


def main() -> None:
    req = urllib.request.Request(URL, headers={"User-Agent": "Raramuri-Historico-Digital/1.0 witness-verifier"})
    with urllib.request.urlopen(req, timeout=90) as response:
        raw = response.read()
        content_type = response.headers.get("Content-Type", "")
        final_url = response.geturl()

    if not raw.startswith(b"%PDF-"):
        raise SystemExit(f"ERROR: DGB endpoint did not return PDF: {content_type!r} {raw[:20]!r}")

    OUT.write_bytes(raw)
    digest = sha256(OUT)
    reader = PdfReader(str(OUT), strict=False)
    page_count = len(reader.pages)
    errors = []
    if digest != EXPECTED_SHA256:
        errors.append(f"sha256 expected={EXPECTED_SHA256} actual={digest}")
    if len(raw) != EXPECTED_BYTES:
        errors.append(f"bytes expected={EXPECTED_BYTES} actual={len(raw)}")
    if page_count != EXPECTED_PAGES:
        errors.append(f"pages expected={EXPECTED_PAGES} actual={page_count}")
    if errors:
        raise SystemExit("ERROR: checksum-fixed Tellechea witness changed; " + "; ".join(errors))

    total_chars = 0
    pages_with_text = 0
    nonempty_counts = []
    keyword_hits = []
    first_nonempty = []
    keywords = ["tarahumar", "libro primero", "conjug", "padre nuestro", "doctrina", "sacramento"]
    for page_no, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""
        chars = len(text.strip())
        total_chars += chars
        if chars:
            pages_with_text += 1
            nonempty_counts.append(chars)
            if len(first_nonempty) < 6:
                first_nonempty.append({"pdf_page": page_no, "chars": chars, "sample": compact(text)})
        lowered = text.lower()
        hits = [kw for kw in keywords if kw in lowered]
        if hits and len(keyword_hits) < 20:
            keyword_hits.append({"pdf_page": page_no, "hits": hits, "sample": compact(text)})

    median_chars = sorted(nonempty_counts)[len(nonempty_counts) // 2] if nonempty_counts else 0
    if pages_with_text >= 150 and total_chars >= 100000:
        text_class = "substantial_embedded_text_layer"
    elif pages_with_text >= 20 and total_chars >= 10000:
        text_class = "partial_embedded_text_layer"
    else:
        text_class = "image_dominant_or_text_layer_not_useful"

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
        "identity_status": "checksum_fixed_public_witness_verified",
        "text_layer": {
            "classification": text_class,
            "pages_with_extractable_text": pages_with_text,
            "total_extracted_characters": total_chars,
            "median_chars_on_nonempty_page": median_chars,
            "first_nonempty_pages": first_nonempty,
            "keyword_hits": keyword_hits,
            "status": "diagnostic_only_not_diplomatic_transcription"
        },
        "human_validation_claimed": False,
        "scope": "binary identity plus extractability diagnostics; no textual or linguistic adjudication",
    }
    print("OK: checksum-fixed Tellechea 1826 witness verified")
    print("RHD_TELLECHEA_WITNESS=" + json.dumps(metadata, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
