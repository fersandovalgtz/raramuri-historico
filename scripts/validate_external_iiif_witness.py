#!/usr/bin/env python3
"""Validate and machine-map the external Internet Archive IIIF Steffel witness.

Internet Archive labels Canvases by scan number rather than printed pagination for this
item. Therefore RHD does not infer a numeric offset. Instead it compares a consecutive
window of external Canvas images against perceptual dHash fingerprints computed from
the independently AI-collated local project PDF pages 79–84 (= printed 369–374).

This is an identity/reproducibility test, not textual or human validation.
"""

from pathlib import Path
from io import BytesIO
import json
import sys
import urllib.request

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/steffel-iiif-manifest.json")
LOCAL_MAP = ROOT / "data/appendices/facsimile_page_map.json"
FINGERPRINTS = ROOT / "data/iiif/steffel-1809-local-page-fingerprints.json"
errors = []

if not MANIFEST.exists():
    print(f"ERROR: downloaded manifest missing: {MANIFEST}")
    sys.exit(1)

data = json.loads(MANIFEST.read_text(encoding="utf-8"))
context = data.get("@context")
context_text = " ".join(str(x) for x in context) if isinstance(context, list) else str(context or "")
if "presentation/3" not in context_text:
    errors.append(f"manifest is not IIIF Presentation 3.x: context={context!r}")
if data.get("type") != "Manifest":
    errors.append(f"manifest type is {data.get('type')!r}, expected 'Manifest'")
manifest_id = data.get("id") or ""
if "tarahumarischesw00stef" not in manifest_id:
    errors.append(f"manifest id does not identify Steffel Internet Archive item: {manifest_id}")
canvases = data.get("items")
if not isinstance(canvases, list) or not canvases:
    errors.append("Presentation 3 Manifest has no Canvas items")
    canvases = []
if len(canvases) < 80:
    errors.append(f"implausibly small Canvas count: {len(canvases)}")

local = json.loads(LOCAL_MAP.read_text(encoding="utf-8"))
local_printed = [x.get("printed_page") for x in local.get("mapping", [])]
if local_printed != [369, 370, 371, 372, 373, 374]:
    errors.append(f"local appendix map changed unexpectedly: {local_printed}")
fingerprint_data = json.loads(FINGERPRINTS.read_text(encoding="utf-8"))
expected = fingerprint_data.get("pages", [])
if [(x.get("pdf_page"), x.get("printed_page")) for x in expected] != [
    (79, 369), (80, 370), (81, 371), (82, 372), (83, 373), (84, 374)
]:
    errors.append("local fingerprint sequence differs from independently collated appendix mapping")


def label_text(canvas):
    label = canvas.get("label")
    if isinstance(label, str):
        return label
    if isinstance(label, dict):
        parts = []
        for values in label.values():
            if isinstance(values, list):
                parts.extend(str(v) for v in values)
            elif values is not None:
                parts.append(str(values))
        return " | ".join(parts)
    return ""


def image_url(canvas):
    try:
        annotation_page = canvas["items"][0]
        annotation = annotation_page["items"][0]
        body = annotation["body"]
        if isinstance(body, list):
            body = body[0]
        service = body.get("service") if isinstance(body, dict) else None
        if isinstance(service, dict):
            service = [service]
        if isinstance(service, list):
            for srv in service:
                sid = (srv or {}).get("id") or (srv or {}).get("@id")
                if sid and sid.startswith("http"):
                    sid = sid.removesuffix("/info.json").rstrip("/")
                    return sid + "/full/800,/0/default.jpg"
        bid = (body or {}).get("id") if isinstance(body, dict) else None
        if bid and bid.startswith("http"):
            return bid
    except (KeyError, IndexError, TypeError):
        return None
    return None


def dhash256(image):
    g = image.convert("L")
    mask = g.point(lambda p: 255 if p < 245 else 0)
    bbox = mask.getbbox()
    if bbox:
        x0, y0, x1, y1 = bbox
        pad_x = max(2, int((x1 - x0) * 0.02))
        pad_y = max(2, int((y1 - y0) * 0.02))
        g = g.crop((max(0, x0 - pad_x), max(0, y0 - pad_y), min(g.width, x1 + pad_x), min(g.height, y1 + pad_y)))
    small = g.resize((17, 16), Image.Resampling.LANCZOS)
    pixels = list(small.getdata())
    value = 0
    for y in range(16):
        row = y * 17
        for x in range(16):
            value = (value << 1) | int(pixels[row + x + 1] > pixels[row + x])
    return f"{value:064x}"


def fetch_hash(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Raramuri-Historico-Digital/1.0 machine-witness-validator"})
    with urllib.request.urlopen(req, timeout=45) as response:
        raw = response.read()
    with Image.open(BytesIO(raw)) as image:
        return dhash256(image)


def hamming(a, b):
    return (int(a, 16) ^ int(b, 16)).bit_count()

if errors:
    print("\n".join("ERROR: " + e for e in errors))
    sys.exit(1)

# The source has only ~90 Canvases. Restrict the network comparison to the final 20,
# where printed pp. 369–374 must occur, but do not assume the scan-number offset.
start_index = max(0, len(canvases) - 20)
candidates = canvases[start_index:]
candidate_hashes = []
for absolute_index, canvas in enumerate(candidates, start=start_index):
    url = image_url(canvas)
    if not url:
        print(f"ERROR: Canvas index {absolute_index} label={label_text(canvas)!r} has no recoverable image/service URL")
        sys.exit(1)
    try:
        digest = fetch_hash(url)
    except Exception as exc:
        print(f"ERROR: could not fetch/hash Canvas index {absolute_index} label={label_text(canvas)!r}: {exc}")
        sys.exit(1)
    candidate_hashes.append(digest)

best = None
for local_start in range(0, len(candidate_hashes) - 5):
    distances = [hamming(expected[offset]["dhash256"], candidate_hashes[local_start + offset]) for offset in range(6)]
    score = (sum(distances), max(distances), distances)
    if best is None or score[:2] < best[:2]:
        best = (score[0], score[1], distances, local_start)

if best is None:
    print("ERROR: no six-Canvas window available for fingerprint comparison")
    sys.exit(1)

total_distance, max_distance, distances, local_start = best
sequence_start = start_index + local_start
mean_distance = total_distance / 6
# 256-bit auto-cropped dHash. These thresholds allow moderate compression/crop changes
# but reject unrelated pages. The sequence constraint further reduces false matches.
if max_distance > 72 or mean_distance > 48:
    labels = [label_text(c) for c in canvases[sequence_start:sequence_start + 6]]
    print(
        "ERROR: best external six-page window is not visually similar enough to local appendix fingerprints; "
        f"Canvas indexes={sequence_start}-{sequence_start+5}, labels={labels!r}, distances={distances}, mean={mean_distance:.2f}"
    )
    sys.exit(1)

selected = canvases[sequence_start:sequence_start + 6]
for offset, canvas in enumerate(selected):
    if canvas.get("type") != "Canvas":
        errors.append(f"printed {369+offset}: selected object type is not Canvas")
    cid = canvas.get("id") or ""
    if not cid.startswith("http"):
        errors.append(f"printed {369+offset}: Canvas lacks dereferenceable HTTP(S) id")
    if not canvas.get("items"):
        errors.append(f"printed {369+offset}: Canvas lacks AnnotationPage items")

if errors:
    print("\n".join("ERROR: " + e for e in errors))
    sys.exit(1)

mapping = [
    {
        "printed_page": 369 + offset,
        "local_pdf_page": 79 + offset,
        "external_canvas_index": sequence_start + offset,
        "external_canvas_label": label_text(canvas),
        "external_canvas_id": canvas.get("id"),
        "dhash_hamming_distance": distances[offset],
    }
    for offset, canvas in enumerate(selected)
]
print(
    "OK: Internet Archive IIIF Presentation 3 witness verified by image fingerprints; "
    f"{len(canvases)} Canvases; matched printed 369–374 to external Canvas indexes "
    f"{sequence_start}–{sequence_start+5}; mean dHash distance={mean_distance:.2f}; mapping={json.dumps(mapping, ensure_ascii=False)}"
)
