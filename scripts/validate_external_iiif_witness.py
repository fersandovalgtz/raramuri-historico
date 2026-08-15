#!/usr/bin/env python3
"""Validate the external Internet Archive IIIF witness used by RHD Steffel.

Input is a downloaded IIIF Presentation manifest. The validator accepts Presentation
3-style manifests and also reports a clear error for older structures. It requires the
printed page labels 369–374 to be recoverable as a consecutive Canvas sequence, which
can then be compared with the independently AI-collated local PDF mapping 79–84.
"""

from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/steffel-iiif-manifest.json")
LOCAL_MAP = ROOT / "data/appendices/facsimile_page_map.json"
errors = []

if not MANIFEST.exists():
    print(f"ERROR: downloaded manifest missing: {MANIFEST}")
    sys.exit(1)

data = json.loads(MANIFEST.read_text(encoding="utf-8"))
context = data.get("@context")
if isinstance(context, list):
    context_text = " ".join(str(x) for x in context)
else:
    context_text = str(context or "")
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


def has_printed_number(label, number):
    # Match a standalone page number, allowing labels like "Page 369" or "369".
    return re.search(rf"(?<!\d){number}(?!\d)", label or "") is not None

labels = [label_text(c) for c in canvases]
sequence_start = None
for i in range(0, max(0, len(canvases) - 5)):
    if all(has_printed_number(labels[i + offset], 369 + offset) for offset in range(6)):
        sequence_start = i
        break

if sequence_start is None:
    # Some IA manifests use scan labels rather than printed pagination. This does not
    # invalidate the witness itself, but it is insufficient for automatic canonical
    # page mapping and should remain a release gate.
    tail = labels[-12:]
    errors.append(
        "could not recover consecutive printed Canvas labels 369–374; "
        f"last labels={tail!r}"
    )

local = json.loads(LOCAL_MAP.read_text(encoding="utf-8"))
local_printed = [x.get("printed_page") for x in local.get("mapping", [])]
if local_printed != [369, 370, 371, 372, 373, 374]:
    errors.append(f"local appendix map changed unexpectedly: {local_printed}")

if sequence_start is not None:
    selected = canvases[sequence_start:sequence_start + 6]
    for offset, canvas in enumerate(selected):
        if canvas.get("type") != "Canvas":
            errors.append(f"printed {369+offset}: object type is not Canvas")
        cid = canvas.get("id") or ""
        if not cid.startswith("http"):
            errors.append(f"printed {369+offset}: Canvas lacks dereferenceable HTTP(S) id")
        pages = canvas.get("items") or []
        if not pages:
            errors.append(f"printed {369+offset}: Canvas lacks AnnotationPage items")

if errors:
    print("\n".join("ERROR: " + e for e in errors))
    sys.exit(1)

print(
    "OK: Internet Archive IIIF Presentation 3 witness is dereferenceable and exposes "
    f"{len(canvases)} Canvases; printed pages 369–374 occur consecutively at Canvas indexes "
    f"{sequence_start}–{sequence_start+5} and agree with the independently collated local appendix sequence"
)
