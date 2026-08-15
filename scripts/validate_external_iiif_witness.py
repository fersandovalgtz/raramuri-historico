#!/usr/bin/env python3
"""Validate the registered Internet Archive IIIF item as a *parallel* Steffel witness.

The checksum-fixed RHD working facsimile remains canonical. Internet Archive labels this
item by scan number and, more importantly, a six-page perceptual-fingerprint comparison
against locally collated printed pp. 369–374 shows a strong image mismatch. That is
scientifically useful negative evidence: the external item is a valid IIIF 3 reference,
but must not be substituted silently for the canonical working scan.

CI succeeds only if both conditions remain true:
1. the external Manifest is a usable IIIF Presentation 3 Manifest; and
2. the registered noncanonical identity status is still supported by a strong mismatch.

If a future provider changes the item so that it becomes visually close to the local
scan, this test fails and forces the witness registry to be reconsidered explicitly.
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
REGISTRY = ROOT / "sources/external-references.json"
errors = []

if not MANIFEST.exists():
    print(f"ERROR: downloaded manifest missing: {MANIFEST}")
    sys.exit(1)

data = json.loads(MANIFEST.read_text(encoding="utf-8"))
registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
external = next(
    (w for w in registry.get("witnesses", []) if w.get("witness_id") == "IA-tarahumarischesw00stef"),
    None,
)
if external is None:
    errors.append("Internet Archive witness is not registered")
elif external.get("canonical_for_rhd") is not False:
    errors.append("Internet Archive witness must remain explicitly noncanonical")
elif external.get("role") != "parallel_external_witness_candidate":
    errors.append(f"unexpected external witness role: {external.get('role')}")

context = data.get("@context")
context_text = " ".join(str(x) for x in context) if isinstance(context, list) else str(context or "")
if "presentation/3" not in context_text:
    errors.append(f"manifest is not IIIF Presentation 3.x: context={context!r}")
if data.get("type") != "Manifest":
    errors.append(f"manifest type is {data.get('type')!r}, expected 'Manifest'")
manifest_id = data.get("id") or ""
if "tarahumarischesw00stef" not in manifest_id:
    errors.append(f"manifest id does not identify registered Steffel Internet Archive item: {manifest_id}")
canvases = data.get("items")
if not isinstance(canvases, list) or not canvases:
    errors.append("Presentation 3 Manifest has no Canvas items")
    canvases = []
if len(canvases) < 80:
    errors.append(f"implausibly small Canvas count: {len(canvases)}")

local = json.loads(LOCAL_MAP.read_text(encoding="utf-8"))
if [x.get("printed_page") for x in local.get("mapping", [])] != [369, 370, 371, 372, 373, 374]:
    errors.append("local appendix page map changed unexpectedly")
fingerprint_data = json.loads(FINGERPRINTS.read_text(encoding="utf-8"))
expected = fingerprint_data.get("pages", [])
if [(x.get("pdf_page"), x.get("printed_page")) for x in expected] != [
    (79, 369), (80, 370), (81, 371), (82, 372), (83, 373), (84, 374)
]:
    errors.append("local fingerprint sequence differs from collated appendix mapping")


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
        body = canvas["items"][0]["items"][0]["body"]
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

# Search the final twenty Canvases for the most similar six-page consecutive window.
# We do not infer a printed-page offset from Canvas labels.
start_index = max(0, len(canvases) - 20)
candidates = canvases[start_index:]
candidate_hashes = []
for absolute_index, canvas in enumerate(candidates, start=start_index):
    url = image_url(canvas)
    if not url:
        print(f"ERROR: Canvas index {absolute_index} label={label_text(canvas)!r} lacks a recoverable image URL")
        sys.exit(1)
    try:
        candidate_hashes.append(fetch_hash(url))
    except Exception as exc:
        print(f"ERROR: could not fetch/hash Canvas index {absolute_index}: {exc}")
        sys.exit(1)

best = None
for local_start in range(0, len(candidate_hashes) - 5):
    distances = [hamming(expected[offset]["dhash256"], candidate_hashes[local_start + offset]) for offset in range(6)]
    score = (sum(distances), max(distances))
    if best is None or score < best[:2]:
        best = (score[0], score[1], distances, local_start)

if best is None:
    print("ERROR: no six-Canvas window available for fingerprint comparison")
    sys.exit(1)

total_distance, max_distance, distances, local_start = best
sequence_start = start_index + local_start
mean_distance = total_distance / 6
labels = [label_text(c) for c in canvases[sequence_start:sequence_start + 6]]

# Identity threshold used by the earlier attempted canonical mapping. A result above
# both boundaries is positive evidence for the registry's NONCANONICAL status.
is_close_enough_for_identity = max_distance <= 72 and mean_distance <= 48
if is_close_enough_for_identity:
    print(
        "ERROR: external witness is unexpectedly close to the local working scan; "
        "registry says noncanonical, so identity must be reconsidered explicitly. "
        f"indexes={sequence_start}-{sequence_start+5}, labels={labels!r}, distances={distances}, mean={mean_distance:.2f}"
    )
    sys.exit(1)

registered_result = ((external or {}).get("identity_comparison") or {}).get("result")
if registered_result != "strong_mismatch_not_verified_as_same_scan":
    print(f"ERROR: registry identity result is not the expected strong mismatch state: {registered_result!r}")
    sys.exit(1)

print(
    "OK: Internet Archive item is a valid IIIF Presentation 3 parallel witness and remains correctly NONCANONICAL for RHD; "
    f"Canvas count={len(canvases)}; best six-page window indexes={sequence_start}-{sequence_start+5}; "
    f"labels={labels!r}; dHash distances={distances}; mean={mean_distance:.2f}. "
    "No external Canvas is substituted for the checksum-fixed working facsimile."
)
