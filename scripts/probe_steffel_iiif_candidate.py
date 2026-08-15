#!/usr/bin/env python3
"""Compare an external Steffel IIIF candidate with local appendix fingerprints.

A mismatch is a valid diagnostic result, not a CI failure. Only malformed/unreachable IIIF
is treated as an error. A low distance is a candidate identity signal, not final proof.
"""

from io import BytesIO
from pathlib import Path
import json
import sys
import urllib.request

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FINGERPRINTS = ROOT / "data/iiif/steffel-1809-local-page-fingerprints.json"
MANIFEST_URL = sys.argv[1] if len(sys.argv) > 1 else "https://iiif.archive.org/iiif/gri_000133125012248650/manifest.json"


def label_text(canvas):
    label = canvas.get("label") or {}
    if isinstance(label, str):
        return label
    vals = []
    for v in label.values() if isinstance(label, dict) else []:
        vals.extend(v if isinstance(v, list) else [v])
    return " | ".join(str(x) for x in vals)


def image_url(canvas):
    try:
        body = canvas["items"][0]["items"][0]["body"]
        if isinstance(body, list):
            body = body[0]
        services = body.get("service", []) if isinstance(body, dict) else []
        if isinstance(services, dict):
            services = [services]
        for service in services:
            sid = service.get("id") or service.get("@id")
            if sid:
                return sid.removesuffix("/info.json").rstrip("/") + "/full/800,/0/default.jpg"
        return body.get("id") if isinstance(body, dict) else None
    except (KeyError, IndexError, TypeError):
        return None


def dhash256(image):
    g = image.convert("L")
    mask = g.point(lambda p: 255 if p < 245 else 0)
    bbox = mask.getbbox()
    if bbox:
        x0, y0, x1, y1 = bbox
        px = max(2, int((x1 - x0) * 0.02))
        py = max(2, int((y1 - y0) * 0.02))
        g = g.crop((max(0, x0-px), max(0, y0-py), min(g.width, x1+px), min(g.height, y1+py)))
    small = g.resize((17, 16), Image.Resampling.LANCZOS)
    pixels = list(small.getdata())
    value = 0
    for y in range(16):
        for x in range(16):
            value = (value << 1) | int(pixels[y*17+x+1] > pixels[y*17+x])
    return f"{value:064x}"


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Raramuri-Historico-Digital/1.0 iiif-probe"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.loads(r.read().decode("utf-8"))


def fetch_hash(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Raramuri-Historico-Digital/1.0 iiif-probe"})
    with urllib.request.urlopen(req, timeout=45) as r:
        raw = r.read()
    with Image.open(BytesIO(raw)) as image:
        return dhash256(image)


def hamming(a, b):
    return (int(a, 16) ^ int(b, 16)).bit_count()


def main():
    manifest = fetch_json(MANIFEST_URL)
    context = str(manifest.get("@context", ""))
    canvases = manifest.get("items", [])
    if manifest.get("type") != "Manifest" or "presentation/3" not in context or not canvases:
        raise SystemExit("ERROR: candidate is not a usable IIIF Presentation 3 Manifest")

    expected = json.loads(FINGERPRINTS.read_text(encoding="utf-8"))["pages"]
    # Printed 369–374 must be near the end of this volume, but full-volume scans include
    # covers/back matter. Search the final 120 canvases without assuming an offset.
    start = max(0, len(canvases) - 120)
    hashes = []
    usable = []
    for idx in range(start, len(canvases)):
        url = image_url(canvases[idx])
        if not url:
            continue
        hashes.append(fetch_hash(url))
        usable.append(idx)

    best = None
    for j in range(0, len(hashes) - 5):
        if usable[j+5] - usable[j] != 5:
            continue
        distances = [hamming(expected[k]["dhash256"], hashes[j+k]) for k in range(6)]
        score = (sum(distances), max(distances))
        if best is None or score < best[0]:
            best = (score, j, distances)
    if best is None:
        raise SystemExit("ERROR: no consecutive six-Canvas window could be compared")

    (_, max_distance), j, distances = best
    seq_start = usable[j]
    mean_distance = sum(distances) / 6
    if max_distance <= 72 and mean_distance <= 48:
        classification = "strong_visual_identity_candidate_requires_multi_anchor_confirmation"
    elif mean_distance <= 80:
        classification = "ambiguous_visual_similarity_not_canonical"
    else:
        classification = "strong_mismatch_not_same_scan"

    result = {
        "manifest_url": MANIFEST_URL,
        "manifest_id": manifest.get("id"),
        "canvas_count": len(canvases),
        "best_window_indexes": [seq_start, seq_start + 5],
        "best_window_labels": [label_text(c) for c in canvases[seq_start:seq_start+6]],
        "dhash_distances": distances,
        "mean_distance": round(mean_distance, 2),
        "max_distance": max_distance,
        "classification": classification,
        "canonical_for_rhd": False,
        "human_validation_claimed": False,
    }
    print("RHD_STEFFEL_IIIF_CANDIDATE=" + json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
