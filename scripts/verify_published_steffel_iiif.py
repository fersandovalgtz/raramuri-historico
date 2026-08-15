#!/usr/bin/env python3
"""Verify the publicly hosted Steffel IIIF package against exact-witness assets.

This is a publication gate, not a structure generator. It fails unless the Manifest
and every one of the 84 page images are actually retrievable over HTTP(S), agree
with the versioned exact-witness asset inventory, and expose no fabricated region
claims. It never treats an external parallel witness as canonical.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSET_MANIFEST = ROOT / "data/iiif/steffel-1809-published-png72-assets.json"
DEFAULT_MANIFEST_URL = (
    "https://fersandovalgtz.github.io/raramuri-historico/iiif/steffel-1809/manifest.json"
)
EXPECTED_SOURCE_SHA = "4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f"
EXPECTED_CANVASES = 84


def fetch_bytes(url: str, timeout: float) -> tuple[bytes, str]:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"non-HTTP(S) publication URL: {url}")
    if parsed.hostname and parsed.hostname.endswith(".invalid"):
        raise ValueError(f"reserved .invalid host cannot close publication gate: {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "RHD-IIIF-publication-verifier/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        status = getattr(response, "status", 200)
        if status != 200:
            raise RuntimeError(f"HTTP {status}: {url}")
        return response.read(), response.headers.get_content_type()


def load_json_url(url: str, timeout: float) -> dict:
    payload, _ = fetch_bytes(url, timeout)
    return json.loads(payload.decode("utf-8"))


def image_body_from_canvas(canvas: dict) -> dict:
    pages = canvas.get("items") or []
    if len(pages) != 1:
        raise ValueError(f"Canvas must contain exactly one painting AnnotationPage: {canvas.get('id')}")
    annotations = pages[0].get("items") or []
    if len(annotations) != 1:
        raise ValueError(f"painting AnnotationPage must contain exactly one Annotation: {canvas.get('id')}")
    annotation = annotations[0]
    if annotation.get("motivation") != "painting":
        raise ValueError(f"non-painting image Annotation: {canvas.get('id')}")
    body = annotation.get("body") or {}
    if body.get("type") != "Image":
        raise ValueError(f"painting body is not Image: {canvas.get('id')}")
    return body


def verify(manifest_url: str, timeout: float) -> dict:
    assets = json.loads(ASSET_MANIFEST.read_text(encoding="utf-8"))
    if assets.get("source_pdf_sha256") != EXPECTED_SOURCE_SHA:
        raise ValueError("versioned publication asset inventory has wrong canonical source checksum")
    if assets.get("asset_count") != EXPECTED_CANVASES or len(assets.get("assets", [])) != EXPECTED_CANVASES:
        raise ValueError("versioned publication asset inventory must contain exactly 84 pages")

    manifest = load_json_url(manifest_url, timeout)
    if manifest.get("@context") != "http://iiif.io/api/presentation/3/context.json":
        raise ValueError("Manifest is not IIIF Presentation API 3")
    if manifest.get("type") != "Manifest":
        raise ValueError("published root resource is not a IIIF Manifest")
    if manifest.get("id") != manifest_url:
        raise ValueError(f"Manifest id is not its published URL: {manifest.get('id')}")

    canvases = manifest.get("items") or []
    if len(canvases) != EXPECTED_CANVASES:
        raise ValueError(f"expected 84 Canvases, got {len(canvases)}")

    checked = []
    for expected, canvas in zip(assets["assets"], canvases, strict=True):
        page = expected["pdf_page"]
        if canvas.get("type") != "Canvas":
            raise ValueError(f"page {page}: item is not Canvas")
        if canvas.get("width") != expected["width"] or canvas.get("height") != expected["height"]:
            raise ValueError(f"page {page}: Canvas dimensions differ from exact-witness inventory")
        canvas_id = canvas.get("id") or ""
        if "#xywh=" in canvas_id or "xywh=" in json.dumps(canvas, ensure_ascii=False):
            raise ValueError(f"page {page}: fabricated/unsupported xywh selector detected")

        body = image_body_from_canvas(canvas)
        image_url = body.get("id") or ""
        if not image_url.endswith("/" + expected["filename"]):
            raise ValueError(f"page {page}: image filename does not match inventory: {image_url}")
        if body.get("format") != "image/png":
            raise ValueError(f"page {page}: expected image/png body")
        if body.get("width") != expected["width"] or body.get("height") != expected["height"]:
            raise ValueError(f"page {page}: image body dimensions differ from inventory")

        raw, content_type = fetch_bytes(image_url, timeout)
        digest = hashlib.sha256(raw).hexdigest()
        if len(raw) != expected["bytes"]:
            raise ValueError(f"page {page}: byte count mismatch")
        if digest != expected["sha256"]:
            raise ValueError(f"page {page}: SHA-256 mismatch")
        if content_type not in {"image/png", "application/octet-stream"}:
            raise ValueError(f"page {page}: unexpected Content-Type {content_type}")
        with Image.open(io.BytesIO(raw)) as im:
            if im.size != (expected["width"], expected["height"]):
                raise ValueError(f"page {page}: decoded image dimensions mismatch")
        checked.append({"pdf_page": page, "canvas": canvas_id, "image": image_url, "sha256": digest})

    serial = json.dumps(manifest, ensure_ascii=False).lower()
    for forbidden in ("human_verified", "expert_verified", "human validated", "human-validated"):
        if forbidden in serial:
            raise ValueError(f"forbidden human-validation claim in published Manifest: {forbidden}")

    return {
        "manifest_url": manifest_url,
        "source_pdf_sha256": EXPECTED_SOURCE_SHA,
        "canvases_verified": len(checked),
        "images_verified": len(checked),
        "all_image_hashes_match": True,
        "fabricated_xywh_regions": 0,
        "human_validation_claimed": False,
        "publication_gate": "closed",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-url", default=DEFAULT_MANIFEST_URL)
    parser.add_argument("--timeout", type=float, default=20.0)
    args = parser.parse_args()
    try:
        result = verify(args.manifest_url, args.timeout)
    except (ValueError, RuntimeError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"ERROR: canonical IIIF publication gate remains open: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
