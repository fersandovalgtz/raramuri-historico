#!/usr/bin/env python3
"""Build the canonical Steffel IIIF Presentation 3 package from the exact public PDF.

The input is accepted only when it is bit-identical to the checksum-fixed RHD witness.
No external scan is substituted. The output is a static IIIF Presentation 3 Manifest
plus 84 JPEG page resources suitable for GitHub Pages. The project intentionally does
not claim a IIIF Image API service; image bodies are stable static JPEG resources.
"""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import urllib.request

from PIL import Image
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "public"
BASE_URL = "https://fersandovalgtz.github.io/raramuri-historico/iiif/steffel-1809"
SOURCE_URL = "https://www.dropbox.com/scl/fi/gda4acwz8ou0m68s4wwlr/1809_STEFFEL-Tarahumarisches-Worterbuch_libro.pdf?rlkey=n1kz2hoa4lfq6gq0me6rxsmgu&dl=1"
EXPECTED_SHA256 = "4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f"
EXPECTED_BYTES = 6251443
EXPECTED_PAGES = 84
PDF = Path("/tmp/rhd-steffel-canonical.pdf")
IIIF_DIR = PUBLIC_ROOT / "iiif" / "steffel-1809"
PAGES_DIR = IIIF_DIR / "pages"
MANIFEST = IIIF_DIR / "manifest.json"
MAP = IIIF_DIR / "canvas-map.json"
APPENDIX_MAP = ROOT / "data/appendices/facsimile_page_map.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_pdf() -> dict:
    req = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "Raramuri-Historico-Digital/1.0 canonical-iiif-builder"})
    with urllib.request.urlopen(req, timeout=120) as response:
        raw = response.read()
        final_url = response.geturl()
        content_type = response.headers.get("Content-Type", "")
    if not raw.startswith(b"%PDF-"):
        raise SystemExit(f"ERROR: canonical source URL did not return PDF: content_type={content_type!r}, final_url={final_url!r}")
    PDF.write_bytes(raw)
    digest = sha256(PDF)
    pages = len(PdfReader(str(PDF), strict=False).pages)
    if digest != EXPECTED_SHA256 or len(raw) != EXPECTED_BYTES or pages != EXPECTED_PAGES:
        raise SystemExit(
            "ERROR: refusing to build canonical IIIF from non-identical binary; "
            f"sha256={digest}, bytes={len(raw)}, pages={pages}"
        )
    return {"resolved_url": final_url, "content_type": content_type, "sha256": digest, "bytes": len(raw), "pdf_pages": pages}


def render_pages() -> list[dict]:
    if IIIF_DIR.exists():
        shutil.rmtree(IIIF_DIR)
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    prefix = PAGES_DIR / "page"
    subprocess.run(
        ["pdftoppm", "-jpeg", "-r", "150", "-jpegopt", "quality=86", str(PDF), str(prefix)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    generated = sorted(PAGES_DIR.glob("page-*.jpg"))
    if len(generated) != EXPECTED_PAGES:
        raise SystemExit(f"ERROR: expected {EXPECTED_PAGES} rendered pages, got {len(generated)}")
    pages = []
    for index, src in enumerate(generated, start=1):
        target = PAGES_DIR / f"{index:03d}.jpg"
        src.rename(target)
        with Image.open(target) as image:
            width, height = image.size
        pages.append({
            "pdf_page": index,
            "image_path": target.relative_to(PUBLIC_ROOT).as_posix(),
            "image_url": f"{BASE_URL}/pages/{index:03d}.jpg",
            "width": width,
            "height": height,
            "sha256": sha256(target),
            "bytes": target.stat().st_size,
        })
    return pages


def appendix_printed_pages() -> dict[int, int]:
    data = json.loads(APPENDIX_MAP.read_text(encoding="utf-8"))
    return {int(x["pdf_page"]): int(x["printed_page"]) for x in data.get("mapping", [])}


def build_manifest(source_meta: dict, pages: list[dict]) -> None:
    printed = appendix_printed_pages()
    canvases = []
    mapping = []
    for page in pages:
        n = page["pdf_page"]
        canvas_id = f"{BASE_URL}/canvas/p{n:03d}"
        annotation_page_id = f"{BASE_URL}/page/p{n:03d}/1"
        annotation_id = f"{BASE_URL}/annotation/p{n:03d}-image"
        label = f"PDF page {n}"
        metadata = [{"label": {"en": ["PDF page"]}, "value": {"none": [str(n)]}}]
        if n in printed:
            label += f" / printed {printed[n]}"
            metadata.append({"label": {"en": ["Printed page"]}, "value": {"none": [str(printed[n])]}})
        canvas = {
            "id": canvas_id,
            "type": "Canvas",
            "label": {"none": [label]},
            "height": page["height"],
            "width": page["width"],
            "metadata": metadata,
            "items": [{
                "id": annotation_page_id,
                "type": "AnnotationPage",
                "items": [{
                    "id": annotation_id,
                    "type": "Annotation",
                    "motivation": "painting",
                    "target": canvas_id,
                    "body": {
                        "id": page["image_url"],
                        "type": "Image",
                        "format": "image/jpeg",
                        "height": page["height"],
                        "width": page["width"],
                    },
                }],
            }],
        }
        canvases.append(canvas)
        mapping.append({
            "pdf_page": n,
            "printed_page": printed.get(n),
            "canvas_id": canvas_id,
            "image_url": page["image_url"],
            "image_sha256": page["sha256"],
            "image_bytes": page["bytes"],
            "width": page["width"],
            "height": page["height"],
        })

    manifest = {
        "@context": "http://iiif.io/api/presentation/3/context.json",
        "id": f"{BASE_URL}/manifest.json",
        "type": "Manifest",
        "label": {
            "de": ["Tarahumarisches Wörterbuch"],
            "es": ["Diccionario tarahumara de Matthäus Steffel — witness canónico RHD"],
            "en": ["Matthäus Steffel Tarahumara dictionary — canonical RHD witness"],
        },
        "summary": {
            "es": ["Manifest IIIF Presentation 3 derivado exclusivamente del PDF público bit-idéntico al facsímil canónico checksum-fixed de RHD. No implica validación humana."],
            "en": ["IIIF Presentation 3 Manifest derived exclusively from the public PDF that is bit-identical to the checksum-fixed canonical RHD facsimile. No human validation is implied."],
        },
        "metadata": [
            {"label": {"en": ["RHD witness"]}, "value": {"none": ["RHD-WIT-STEFFEL-1809-WORKING-FACSIMILE"]}},
            {"label": {"en": ["Canonical PDF SHA-256"]}, "value": {"none": [EXPECTED_SHA256]}},
            {"label": {"en": ["Canonical PDF bytes"]}, "value": {"none": [str(EXPECTED_BYTES)]}},
            {"label": {"en": ["PDF pages"]}, "value": {"none": [str(EXPECTED_PAGES)]}},
            {"label": {"en": ["Source identity"]}, "value": {"none": ["Exact binary identity verified before IIIF derivation"]}},
        ],
        "requiredStatement": {
            "label": {"en": ["Attribution"]},
            "value": {"none": ["Rarámuri Histórico Digital (RHD). Images mechanically derived from the checksum-fixed Steffel facsimile; source work published 1809."]},
        },
        "rendering": [{
            "id": SOURCE_URL,
            "type": "Text",
            "label": {"en": ["Canonical source PDF"]},
            "format": "application/pdf",
        }],
        "items": canvases,
    }
    IIIF_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    canvas_map = {
        "map_id": "RHD-STEFFEL-1809-CANONICAL-IIIF-MAP-1",
        "manifest_id": manifest["id"],
        "witness_id": "RHD-WIT-STEFFEL-1809-WORKING-FACSIMILE",
        "source_pdf_sha256": EXPECTED_SHA256,
        "source_pdf_bytes": EXPECTED_BYTES,
        "source_pdf_pages": EXPECTED_PAGES,
        "source_resolved_url": source_meta["resolved_url"],
        "canonical_binary_identity_required": True,
        "human_validation_claimed": False,
        "pages": mapping,
    }
    MAP.write_text(json.dumps(canvas_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    source_meta = fetch_pdf()
    pages = render_pages()
    build_manifest(source_meta, pages)
    print(
        "RHD_CANONICAL_IIIF=" + json.dumps({
            "manifest": f"{BASE_URL}/manifest.json",
            "canvases": len(pages),
            "source_sha256": source_meta["sha256"],
            "source_bytes": source_meta["bytes"],
            "source_pdf_pages": source_meta["pdf_pages"],
            "static_page_images": len(pages),
            "human_validation_claimed": False,
        }, sort_keys=True)
    )


if __name__ == "__main__":
    main()
