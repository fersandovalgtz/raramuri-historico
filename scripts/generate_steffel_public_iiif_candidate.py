#!/usr/bin/env python3
"""Generate the exact-witness Steffel IIIF package intended for GitHub Pages.

The package uses the lightweight PNG72 publication asset inventory. Generation is
offline and does NOT claim that the URLs are reachable; `verify_published_steffel_iiif.py`
is the separate network gate that closes publication only after deployment.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import csv
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "data/iiif/steffel-1809-published-png72-assets.json"
ENTRIES = ROOT / "data/entries.csv"
EXPECTED_SHA = "4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f"
EXPECTED_PAGES = 84
EXPECTED_ACTIVE = 1965
DEFAULT_BASE = "https://fersandovalgtz.github.io/raramuri-historico/iiif/steffel-1809"
DEFAULT_OUT = ROOT / "dist/iiif-public-candidate/steffel-1809"


def language_map(text: str) -> dict:
    return {"none": [text]}


def parse_int(value):
    value = (value or "").strip()
    return int(value) if re.fullmatch(r"\d+", value) else None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=DEFAULT_BASE)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUT))
    args = parser.parse_args()
    base = args.base_url.rstrip("/")
    if not base.startswith("https://"):
        raise SystemExit("ERROR: public IIIF base URL must use HTTPS")
    if ".invalid" in base:
        raise SystemExit("ERROR: public IIIF candidate cannot use reserved .invalid host")

    inventory = json.loads(ASSETS.read_text(encoding="utf-8"))
    if inventory.get("source_pdf_sha256") != EXPECTED_SHA:
        raise SystemExit("ERROR: publication inventory not tied to canonical Steffel checksum")
    assets = inventory.get("assets") or []
    if inventory.get("asset_count") != EXPECTED_PAGES or len(assets) != EXPECTED_PAGES:
        raise SystemExit("ERROR: publication inventory must contain exactly 84 page assets")
    if inventory.get("format") != "image/png":
        raise SystemExit("ERROR: expected PNG72 publication inventory")

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    canvases = []
    pages = []
    for expected_page, asset in enumerate(assets, 1):
        if asset.get("pdf_page") != expected_page:
            raise SystemExit(f"ERROR: publication inventory page order mismatch at {expected_page}")
        filename = asset.get("filename")
        width, height = asset.get("width"), asset.get("height")
        if filename != f"{expected_page:03d}.png" or not isinstance(width, int) or not isinstance(height, int):
            raise SystemExit(f"ERROR: malformed publication asset at page {expected_page}")
        canvas_id = f"{base}/canvas/p{expected_page:03d}"
        image_id = f"{base}/pages/{filename}"
        annotation_page_id = f"{base}/page/p{expected_page:03d}/painting"
        annotation_id = f"{base}/annotation/p{expected_page:03d}-image"
        canvases.append({
            "id": canvas_id,
            "type": "Canvas",
            "label": language_map(f"PDF page {expected_page}"),
            "width": width,
            "height": height,
            "items": [{
                "id": annotation_page_id,
                "type": "AnnotationPage",
                "items": [{
                    "id": annotation_id,
                    "type": "Annotation",
                    "motivation": "painting",
                    "body": {
                        "id": image_id,
                        "type": "Image",
                        "format": "image/png",
                        "width": width,
                        "height": height,
                    },
                    "target": canvas_id,
                }],
            }],
        })
        pages.append({
            "pdf_page": expected_page,
            "canvas_id": canvas_id,
            "image_id": image_id,
            "image_filename": filename,
            "width": width,
            "height": height,
            "bytes": asset.get("bytes"),
            "sha256": asset.get("sha256"),
            "region_target_available": False,
        })

    manifest = {
        "@context": "http://iiif.io/api/presentation/3/context.json",
        "id": f"{base}/manifest.json",
        "type": "Manifest",
        "label": {
            "de": ["Steffel 1809 - Tarahumarisches Wörterbuch"],
            "es": ["Steffel 1809 - testimonio canónico RHD"],
        },
        "summary": language_map(
            "RHD machine-only IIIF publication candidate derived from the exact checksum-fixed 84-page Steffel witness."
        ),
        "metadata": [
            {"label": language_map("RHD witness SHA-256"), "value": language_map(EXPECTED_SHA)},
            {"label": language_map("PDF pages"), "value": language_map("84")},
            {"label": language_map("Publication asset profile"), "value": language_map(inventory.get("asset_manifest_id", ""))},
            {"label": language_map("Human validation claimed"), "value": language_map("false")},
        ],
        "requiredStatement": {
            "label": language_map("Attribution / provenance"),
            "value": language_map(
                "Rarámuri Histórico Digital; all painting images derive from canonical Steffel PDF SHA-256 " + EXPECTED_SHA
            ),
        },
        "items": canvases,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    canvas_map = {
        "map_id": "RHD-S1809-IIIF-PUBLIC-CANVAS-MAP-01",
        "source_pdf_sha256": EXPECTED_SHA,
        "source_pdf_pages": EXPECTED_PAGES,
        "asset_manifest_id": inventory.get("asset_manifest_id"),
        "iiif_presentation_version": 3,
        "base_url": base,
        "publication_status": "candidate_not_network_verified",
        "public_image_host_verified": False,
        "human_validation_claimed": False,
        "pages": pages,
    }
    (out / "canvas-map.json").write_text(json.dumps(canvas_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lookup = {p["pdf_page"]: p for p in pages}
    record_map = []
    with ENTRIES.open("r", encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            if row.get("status") == "rejected_false_positive":
                continue
            record_id = (row.get("record_id") or "").strip()
            page = parse_int(row.get("pdf_page"))
            if not record_id or page not in lookup:
                raise SystemExit(f"ERROR: active record lacks valid canonical page: {record_id!r} / {page!r}")
            record_map.append({
                "record_id": record_id,
                "pdf_page": page,
                "printed_page": parse_int(row.get("printed_page")),
                "iiif_canvas": lookup[page]["canvas_id"],
                "iiif_target": None,
                "linkage_level": "page_canvas_only",
                "region_coordinates_available": False,
                "source_pdf_sha256": EXPECTED_SHA,
                "human_validation_claimed": False,
            })
    if len(record_map) != EXPECTED_ACTIVE or len({x["record_id"] for x in record_map}) != EXPECTED_ACTIVE:
        raise SystemExit(f"ERROR: expected {EXPECTED_ACTIVE} unique active record links")
    (out / "record-map.jsonl").write_text(
        "".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n" for x in record_map), encoding="utf-8"
    )
    summary = {
        "candidate_id": "RHD-S1809-IIIF-PUBLIC-CANDIDATE-01",
        "source_pdf_sha256": EXPECTED_SHA,
        "asset_manifest_id": inventory.get("asset_manifest_id"),
        "canvases": len(canvases),
        "page_assets_expected": len(assets),
        "active_records_canvas_mapped": len(record_map),
        "region_targets_generated": 0,
        "public_image_host_verified": False,
        "canonical_iiif_publication_gate_closed": False,
        "human_validation_claimed": False,
        "network_gate": "Run scripts/verify_published_steffel_iiif.py after deployment; only a green network verification closes publication.",
    }
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("generated GitHub Pages IIIF publication candidate: 84 PNG Canvases, 1965 page-level links, 0 xywh regions; network gate remains open")


if __name__ == "__main__":
    main()
