#!/usr/bin/env python3
from pathlib import Path
import json
import sys
import xml.etree.ElementTree as ET

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
JSONL = ROOT / "data/pilot/tellechea-1826.minimal-pilot.jsonl"
TEI = ROOT / "data/pilot/tellechea-1826.minimal-pilot.tei.xml"
DIAG = ROOT / "data/pilot/tellechea-1826.minimal-pilot.diagnostics.json"
SCHEMA = ROOT / "schemas/rhd-entry-1.0.schema.json"
EXPECTED_SHA = "c67b7942090613c494d8057be8aff59ea13a11519c29eae469afad8a85c30dfc"
errors = []

for path in (JSONL, TEI, DIAG):
    if not path.exists():
        errors.append(f"missing generated pilot artifact: {path.relative_to(ROOT)}")

if errors:
    print("\n".join("ERROR: " + e for e in errors))
    sys.exit(1)

schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
validator = Draft202012Validator(schema, format_checker=FormatChecker())
records = [json.loads(line) for line in JSONL.read_text(encoding="utf-8").splitlines() if line.strip()]
if len(records) != 2:
    errors.append(f"expected exactly two minimal pilot records, got {len(records)}")

for record in records:
    validation_errors = sorted(validator.iter_errors(record), key=lambda e: list(e.path))
    for e in validation_errors:
        errors.append(f"{record.get('record_id')}: JSON Schema: {e.message}")
    if record.get("source_id") != "RHD-SRC-TELLECHEA-1826":
        errors.append(f"{record.get('record_id')}: wrong source_id")
    if record.get("witness_id") != "RHD-WIT-TELLECHEA-1826-DGB":
        errors.append(f"{record.get('record_id')}: wrong witness_id")
    if record.get("lexical") is not None:
        errors.append(f"{record.get('record_id')}: non-lexicographic pilot must not fabricate Lex-0 lexical content")
    layers = record.get("layers", {})
    if layers.get("ocr_raw", {}).get("method") != "pypdf_embedded_text_extraction":
        errors.append(f"{record.get('record_id')}: embedded source text method missing")
    diplomatic = layers.get("diplomatic", {})
    if diplomatic.get("status") != "machine_visual_ocr_unadjudicated":
        errors.append(f"{record.get('record_id')}: visual OCR must remain explicitly unadjudicated")
    if "tesseract" not in (diplomatic.get("method") or ""):
        errors.append(f"{record.get('record_id')}: visual OCR method is not Tesseract-based")
    if any(v.get("reviewer_type") == "human" for v in record.get("validation", [])):
        errors.append(f"{record.get('record_id')}: human validation fabricated")
    if not record.get("provenance"):
        errors.append(f"{record.get('record_id')}: missing provenance")

ids = [r.get("record_id") for r in records]
if ids != ["RHD-T1826-00001", "RHD-T1826-00002"]:
    errors.append(f"unexpected persistent IDs/order: {ids}")
if records and records[0].get("locators", {}).get("printed_page") != 6:
    errors.append("grammar anchor must resolve to printed page 6")
if len(records) > 1 and records[1].get("locators", {}).get("printed_page") != 49:
    errors.append("parallel-layout pilot must resolve to printed page 49")
if len(records) > 1 and records[1].get("locators", {}).get("column") != "two-column-layout-candidate":
    errors.append("parallel-layout record lost two-column candidate locator")

diag = json.loads(DIAG.read_text(encoding="utf-8"))
if diag.get("witness_sha256") != EXPECTED_SHA:
    errors.append("pilot diagnostics are not tied to checksum-fixed witness")
if diag.get("human_validation_claimed") is not False:
    errors.append("pilot diagnostics must deny human-validation claim")
if len(diag.get("records", [])) != 2:
    errors.append("pilot diagnostics must describe two records")
for item in diag.get("records", []):
    if item.get("embedded_chars", 0) < 100 or item.get("visual_ocr_chars", 0) < 100:
        errors.append(f"{item.get('record_id')}: insufficient source/visual text for a real pilot")
    sim = item.get("token_jaccard")
    if not isinstance(sim, (int, float)) or sim <= 0:
        errors.append(f"{item.get('record_id')}: no measurable documentary agreement between embedded and visual OCR layers")

try:
    root = ET.parse(TEI).getroot()
    ns = {"tei": "http://www.tei-c.org/ns/1.0"}
    divs = root.findall(".//tei:div[@type='documentary-unit']", ns)
    if len(divs) != 2:
        errors.append(f"TEI must contain two documentary units, got {len(divs)}")
    machine_ocr = root.findall(".//tei:ab[@type='machine-visual-ocr']", ns)
    if len(machine_ocr) != 2:
        errors.append("TEI must preserve two machine visual OCR layers")
    if root.findall(".//tei:entry", ns):
        errors.append("Tellechea documentary pilot must not be coerced into dictionary entries")
except ET.ParseError as exc:
    errors.append(f"invalid TEI XML: {exc}")

serialized = (JSONL.read_text(encoding="utf-8") + TEI.read_text(encoding="utf-8") + DIAG.read_text(encoding="utf-8")).lower()
for forbidden in ("human_verified", "expert_verified", "human validated", "cognate", "etymology confirmed"):
    if forbidden in serialized:
        errors.append(f"forbidden claim in pilot artifacts: {forbidden}")

if errors:
    print("\n".join("ERROR: " + e for e in errors))
    sys.exit(1)
print("OK: Tellechea checksum-fixed witness produced two real non-lexicographic RHD canonical units (grammar + parallel-layout), independent embedded/visual OCR layers and TEI without human or lexical fabrication")
