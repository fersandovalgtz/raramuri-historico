#!/usr/bin/env python3
from pathlib import Path
import json, sys
import xml.etree.ElementTree as ET
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
JSONL = ROOT / "data/pilot/tellechea-1826.full-witness.jsonl"
TEI = ROOT / "data/pilot/tellechea-1826.full-witness.tei.xml"
DIAG = ROOT / "data/pilot/tellechea-1826.full-witness.diagnostics.json"
SCHEMA = ROOT / "schemas/rhd-entry-1.0.schema.json"
SHA = "c67b7942090613c494d8057be8aff59ea13a11519c29eae469afad8a85c30dfc"
errors = []

for p in (JSONL, TEI, DIAG):
    if not p.exists(): errors.append(f"missing full-witness pilot artifact: {p.relative_to(ROOT)}")
if errors:
    print("\n".join("ERROR: " + e for e in errors)); sys.exit(1)

schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
validator = Draft202012Validator(schema, format_checker=FormatChecker())
records = [json.loads(x) for x in JSONL.read_text(encoding="utf-8").splitlines() if x.strip()]
if len(records) != 205: errors.append(f"full witness must produce 205 canonical page units, got {len(records)}")
if len({r.get('record_id') for r in records}) != len(records): errors.append("full-witness record IDs are not unique")

for i, r in enumerate(records, start=1):
    for e in sorted(validator.iter_errors(r), key=lambda e: list(e.path)):
        errors.append(f"{r.get('record_id')}: JSON Schema: {e.message}")
    if r.get("source_id") != "RHD-SRC-TELLECHEA-1826": errors.append(f"page {i}: wrong source_id")
    if r.get("witness_id") != "RHD-WIT-TELLECHEA-1826-DGB": errors.append(f"page {i}: wrong witness_id")
    if r.get("locators", {}).get("digital_page") != i: errors.append(f"page {i}: digital page sequence broken")
    if r.get("record_id") != f"RHD-T1826-{10000+i:05d}": errors.append(f"page {i}: persistent ID not deterministic")
    if r.get("lexical") is not None: errors.append(f"page {i}: documentary pilot fabricated lexical content")
    if not r.get("provenance"): errors.append(f"page {i}: missing provenance")
    if any(v.get("reviewer_type") == "human" for v in r.get("validation", [])): errors.append(f"page {i}: fabricated human validation")
    layers = r.get("layers", {})
    if layers.get("ocr_raw", {}).get("method") != "pypdf_embedded_text_extraction": errors.append(f"page {i}: source extraction layer lost")
    dip = layers.get("diplomatic", {})
    if not isinstance(dip, dict) or not dip.get("method"): errors.append(f"page {i}: required documentary/diplomatic projection absent")

if len(records) >= 75:
    if records[31].get("locators", {}).get("printed_page") != 6: errors.append("full traversal lost grammar anchor PDF 32 / printed 6")
    if records[74].get("locators", {}).get("printed_page") != 49: errors.append("full traversal lost parallel anchor PDF 75 / printed 49")

diag = json.loads(DIAG.read_text(encoding="utf-8"))
if diag.get("pilot_id") != "RHD-TELLECHEA-1826-FULL-WITNESS-PILOT-1": errors.append("wrong full-witness pilot ID")
if diag.get("witness_sha256") != SHA: errors.append("full pilot not tied to fixed Tellechea witness")
if diag.get("pdf_pages") != 205 or diag.get("canonical_records") != 205: errors.append("full pilot coverage count is not 205/205")
if diag.get("embedded_text_pages", 0) < 190: errors.append("unexpected loss of substantial embedded source-text layer")
if diag.get("embedded_text_characters", 0) < 250000: errors.append("embedded source-text extraction unexpectedly small")
if diag.get("visual_ocr_fallback_count", 0) < 1: errors.append("sparse pages did not exercise visual OCR fallback")
if len(diag.get("major_section_transitions", [])) < 2: errors.append("document hierarchy did not detect enough conservative major-section transitions")
if diag.get("rhd_core_changes_required") != []: errors.append("strong pilot required source-specific changes to universal RHD core")
if diag.get("source_specific_rules_location") != "source_profile_or_adapter_only": errors.append("source-specific rules leaked outside profile/adapter policy")
if diag.get("lex0_entries_generated") != 0: errors.append("non-lexicographic full pilot generated Lex-0 entries")
if diag.get("human_validation_claimed") is not False: errors.append("full pilot must explicitly deny human validation")

try:
    root = ET.parse(TEI).getroot(); ns = {"tei": "http://www.tei-c.org/ns/1.0"}
    units = root.findall(".//tei:div[@type='documentary-unit']", ns)
    sections = root.findall(".//tei:div[@type='source-section']", ns)
    if len(units) != 205: errors.append(f"TEI must contain 205 documentary units, got {len(units)}")
    if len(sections) < 2: errors.append("TEI does not preserve machine-detected document hierarchy")
    if root.findall(".//tei:entry", ns): errors.append("full Tellechea TEI must not contain dictionary entries")
except ET.ParseError as exc:
    errors.append(f"invalid full-witness TEI XML: {exc}")

serialized = (JSONL.read_text(encoding="utf-8") + TEI.read_text(encoding="utf-8") + DIAG.read_text(encoding="utf-8")).lower()
for forbidden in ("human_verified", "expert_verified", "etymology confirmed", "cognate confirmed"):
    if forbidden in serialized: errors.append(f"forbidden scholarly claim in full pilot: {forbidden}")

if errors:
    print("\n".join("ERROR: " + e for e in errors)); sys.exit(1)
print(f"OK: all 205 Tellechea pages traverse checksum-fixed RHD documentary canonicalization and TEI; embedded source text={diag.get('embedded_text_pages')} pages, visual fallback={diag.get('visual_ocr_fallback_count')} pages, core redesign=0, Lex-0 fabrication=0, human validation=0")
