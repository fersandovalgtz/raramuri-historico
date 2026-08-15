#!/usr/bin/env python3
"""Generate a static IIIF Presentation 3 package for the canonical Steffel witness.

This generator deliberately separates *prepared IIIF semantics* from *public image
publication*. It can run in CI without the source PDF because the dimensions were
measured from the checksum-fixed 84-page witness and are versioned in
`data/iiif/steffel-1809-canonical-canvas-dimensions.json`.

By default the IDs use the reserved `.invalid` domain. Therefore the generated
Manifest/Canvas map prove deterministic structure and RHD page linkage but do not
claim that page images are already publicly hosted. At publication time, rerun with
`--base-url https://<stable-host>/...` after deploying the exact-binary-derived JPEGs.
No xywh regions are fabricated.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import csv
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DIMENSIONS = ROOT / "data/iiif/steffel-1809-canonical-canvas-dimensions.json"
ENTRIES = ROOT / "data/entries.csv"
MANIFEST = ROOT / "public/iiif/steffel-1809/manifest.json"
CANVAS_MAP = ROOT / "public/iiif/steffel-1809/canvas-map.json"
RECORD_MAP = ROOT / "data/canonical/steffel-1809.iiif-record-map.jsonl"
SUMMARY = ROOT / "data/canonical/steffel-1809.iiif-linkage-summary.json"
EXPECTED_SHA = "4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f"
EXPECTED_PAGES = 84
EXPECTED_ACTIVE = 1965
DEFAULT_BASE = "https://rhd.invalid/iiif/steffel-1809"


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--base-url", default=DEFAULT_BASE)
    return p.parse_args()


def language_map(text):
    return {"none": [text]}


def parse_int(value):
    value = (value or "").strip()
    return int(value) if re.fullmatch(r"\d+", value) else None


def main():
    args = parse_args()
    base = args.base_url.rstrip("/")
    if not re.match(r"^https?://", base):
        raise SystemExit("ERROR: IIIF base URL must be absolute HTTP(S)")

    dims = json.loads(DIMENSIONS.read_text(encoding="utf-8"))
    if dims.get("source_sha256") != EXPECTED_SHA:
        raise SystemExit("ERROR: canvas dimensions are not tied to the canonical Steffel checksum")
    if dims.get("source_pdf_pages") != EXPECTED_PAGES:
        raise SystemExit("ERROR: expected 84-page canonical witness")
    page_dims = dims.get("dimensions_by_pdf_page_1_based", [])
    if len(page_dims) != EXPECTED_PAGES:
        raise SystemExit(f"ERROR: expected 84 page dimensions, got {len(page_dims)}")

    prepared_not_public = base.endswith(".invalid") or ".invalid/" in base
    pages = []
    canvases = []
    for page, wh in enumerate(page_dims, 1):
        width, height = wh
        canvas_id = f"{base}/canvas/p{page:03d}"
        image_id = f"{base}/pages/{page:03d}.jpg"
        annotation_page_id = f"{base}/page/p{page:03d}/painting"
        annotation_id = f"{base}/annotation/p{page:03d}-image"
        pages.append({
            "pdf_page": page,
            "canvas_id": canvas_id,
            "image_id": image_id,
            "width": width,
            "height": height,
            "image_filename": f"{page:03d}.jpg",
            "region_target_available": False,
        })
        canvases.append({
            "id": canvas_id,
            "type": "Canvas",
            "label": language_map(f"PDF page {page}"),
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
                        "format": "image/jpeg",
                        "width": width,
                        "height": height,
                    },
                    "target": canvas_id,
                }],
            }],
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
            "RHD machine-only static IIIF preparation derived from the checksum-fixed 84-page Steffel witness."
        ),
        "metadata": [
            {"label": language_map("RHD witness SHA-256"), "value": language_map(EXPECTED_SHA)},
            {"label": language_map("PDF pages"), "value": language_map(str(EXPECTED_PAGES))},
            {"label": language_map("Publication status"), "value": language_map(
                "prepared-not-public" if prepared_not_public else "publication-base-url-declared-not-probed-by-this-generator"
            )},
            {"label": language_map("Human validation claimed"), "value": language_map("false")},
        ],
        "requiredStatement": {
            "label": language_map("Attribution / provenance"),
            "value": language_map(
                "Rarámuri Histórico Digital; page assets must be generated only from the canonical Steffel PDF with SHA-256 " + EXPECTED_SHA
            ),
        },
        "items": canvases,
    }

    CANVAS_MAP.parent.mkdir(parents=True, exist_ok=True)
    RECORD_MAP.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    canvas_payload = {
        "map_id": "RHD-S1809-IIIF-CANVAS-MAP-01",
        "source_pdf_sha256": EXPECTED_SHA,
        "source_pdf_pages": EXPECTED_PAGES,
        "iiif_presentation_version": 3,
        "base_url": base,
        "publication_status": "prepared_not_public" if prepared_not_public else "base_url_declared_unverified",
        "public_image_host_verified": False,
        "human_validation_claimed": False,
        "pages": pages,
    }
    CANVAS_MAP.write_text(json.dumps(canvas_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    page_lookup = {p["pdf_page"]: p for p in pages}
    mapped = []
    with ENTRIES.open("r", encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            if row.get("status") == "rejected_false_positive":
                continue
            record_id = (row.get("record_id") or "").strip()
            page = parse_int(row.get("pdf_page"))
            if not record_id or page not in page_lookup:
                raise SystemExit(f"ERROR: active record without valid page locator: {record_id!r} page={page!r}")
            item = page_lookup[page]
            mapped.append({
                "record_id": record_id,
                "pdf_page": page,
                "printed_page": parse_int(row.get("printed_page")),
                "iiif_canvas": item["canvas_id"],
                "iiif_target": None,
                "linkage_level": "page_canvas_only",
                "region_coordinates_available": False,
                "source_pdf_sha256": EXPECTED_SHA,
                "human_validation_claimed": False,
            })

    if len(mapped) != EXPECTED_ACTIVE:
        raise SystemExit(f"ERROR: expected {EXPECTED_ACTIVE} active Steffel records, mapped {len(mapped)}")
    if len({m['record_id'] for m in mapped}) != EXPECTED_ACTIVE:
        raise SystemExit("ERROR: duplicate record IDs in IIIF linkage")

    RECORD_MAP.write_text(
        "".join(json.dumps(m, ensure_ascii=False, sort_keys=True) + "\n" for m in mapped),
        encoding="utf-8",
    )
    summary = {
        "linkage_id": "RHD-S1809-IIIF-PAGE-LINKAGE-01",
        "source_pdf_sha256": EXPECTED_SHA,
        "active_records_expected": EXPECTED_ACTIVE,
        "active_records_canvas_mapped": len(mapped),
        "active_record_page_linkage_prepared": True,
        "active_record_canvas_linkage_complete_for_prepared_manifest": True,
        "public_image_host_verified": False,
        "canonical_iiif_publication_gate_closed": False,
        "linkage_level": "page_canvas_only",
        "region_targets_generated": 0,
        "region_coordinates_available": False,
        "base_url": base,
        "publication_status": "prepared_not_public" if prepared_not_public else "base_url_declared_unverified",
        "human_validation_claimed": False,
        "non_claim": "No xywh region is inferred. Page-level Canvas linkage is prepared, but public IIIF is not complete until exact-binary-derived images are stably hosted and probed.",
    }
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"prepared IIIF Presentation 3 structure: 84 canvases, {len(mapped)} active record->Canvas links, "
        f"0 region targets; public publication gate remains open"
    )


if __name__ == "__main__":
    main()
