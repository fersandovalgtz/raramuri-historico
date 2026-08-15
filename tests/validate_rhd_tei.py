#!/usr/bin/env python3
from pathlib import Path
import json
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data" / "canonical" / "steffel-1809.entries.jsonl"
RICH_PATH = ROOT / "data" / "tei" / "rhd-steffel-1809-tei.xml"
LEX0_PATH = ROOT / "data" / "tei" / "rhd-steffel-1809-lex0.xml"
TEI = "http://www.tei-c.org/ns/1.0"
XML = "http://www.w3.org/XML/1998/namespace"
Q = lambda n: f"{{{TEI}}}{n}"
errors = []

for required in (CANONICAL, RICH_PATH, LEX0_PATH):
    if not required.exists():
        errors.append(f"missing {required.relative_to(ROOT)}")
if errors:
    print("\n".join("ERROR: " + e for e in errors)); sys.exit(1)

canonical = [json.loads(line) for line in CANONICAL.read_text(encoding="utf-8").splitlines() if line.strip()]
active = [x for x in canonical if x.get("status") == "active"]
active_ids = {x["record_id"] for x in active}
expected_phil = sum(len(x.get("validation", [])) for x in active)
expected_relations = sum(len(x.get("historical_relations", [])) for x in active)
expected_translations = sum(
    1
    for x in active
    for sense in x.get("lexical", {}).get("senses", [])
    if sense.get("editorial_translation")
)


def validate_header(root, label, expected_root_type):
    if root.tag != Q("TEI"):
        errors.append(f"{label}: root is not TEI namespace TEI")
    if root.get("type") != expected_root_type:
        errors.append(f"{label}: root type {root.get('type')} != {expected_root_type}")
    licence = root.find(f"./{Q('teiHeader')}/{Q('fileDesc')}/{Q('publicationStmt')}/{Q('availability')}/{Q('licence')}")
    if licence is None or not licence.get("target"):
        errors.append(f"{label}: publicationStmt/availability/licence missing")
    list_bibl = root.find(f"./{Q('teiHeader')}/{Q('fileDesc')}/{Q('sourceDesc')}/{Q('listBibl')}")
    if list_bibl is None or list_bibl.get("type") != "dictionaries":
        errors.append(f"{label}: sourceDesc must use listBibl type=dictionaries")
    elif list_bibl.find(Q("biblStruct")) is None:
        errors.append(f"{label}: sourceDesc listBibl lacks biblStruct")
    lang_usage = root.find(f"./{Q('teiHeader')}/{Q('profileDesc')}/{Q('langUsage')}")
    if lang_usage is None:
        errors.append(f"{label}: profileDesc/langUsage missing")
    else:
        languages = {(el.get("ident"), el.get("role")) for el in lang_usage.findall(Q("language"))}
        required_languages = {
            ("und", "objectLanguage"),
            ("de", "objectLanguage"),
            ("es", "workingLanguage"),
        }
        if not required_languages.issubset(languages):
            errors.append(f"{label}: language profile incomplete: {sorted(languages)}")


rich = ET.parse(RICH_PATH).getroot()
validate_header(rich, "rich", "dictionary")
rich_entries = rich.findall(f".//{Q('entry')}")
rich_ids = [e.get(f"{{{XML}}}id") for e in rich_entries]
if len(rich_entries) != len(active) or set(rich_ids) != active_ids:
    errors.append("rich: entry universe differs from active canonical records")
if len(rich_ids) != len(set(rich_ids)):
    errors.append("rich: duplicate xml:id")
if rich.findall(f".//{Q('def')}"):
    errors.append("rich: unparsed source material was auto-promoted to <def>")
for entry in rich_entries:
    if entry.get("type") != "mainEntry" or entry.get(f"{{{XML}}}lang") not in {"de", "und"}:
        errors.append(f"rich: {entry.get(f'{{{XML}}}id')} missing required lexical identity attributes")
    location = next((n for n in entry.findall(Q("note")) if n.get("type") == "sourceLocation"), None)
    if location is None or "printed p." not in (location.text or ""):
        errors.append(f"rich: {entry.get(f'{{{XML}}}id')} missing sourceLocation")

validation_notes = [n for n in rich.findall(f".//{Q('note')}") if n.get("type") == "validation"]
if len(validation_notes) != expected_phil:
    errors.append(f"rich: PHIL note count {len(validation_notes)} != {expected_phil}")
relation_notes = [n for n in rich.findall(f".//{Q('note')}") if n.get("type") == "diachronicCandidate"]
if len(relation_notes) != expected_relations:
    errors.append(f"rich: diachronic candidate count {len(relation_notes)} != {expected_relations}")
for note in relation_notes:
    if note.get("ana") != "#machineCandidate":
        errors.append("rich: diachronic candidate lost machineCandidate annotation")
    if not (note.get("corresp") or "").startswith("urn:raramuri-digital:RD-"):
        errors.append("rich: diachronic candidate target is not explicit Rarámuri Digital URN")
translations = [cit for cit in rich.findall(f".//{Q('cit')}") if cit.get("type") == "translation"]
if len(translations) != expected_translations:
    errors.append(f"rich: translation citation count {len(translations)} != {expected_translations}")

lex0 = ET.parse(LEX0_PATH).getroot()
validate_header(lex0, "lex0", "lex-0")
lex0_entries = lex0.findall(f".//{Q('entry')}")
lex0_ids = [e.get(f"{{{XML}}}id") for e in lex0_entries]
if len(lex0_entries) != len(active) or set(lex0_ids) != active_ids:
    errors.append("lex0: entry universe differs from active canonical records")
if len(lex0_ids) != len(set(lex0_ids)):
    errors.append("lex0: duplicate xml:id")
if lex0.findall(f".//{Q('def')}"):
    errors.append("lex0: contains synthetic <def>")
if [n for n in lex0.findall(f".//{Q('note')}") if n.get("type") in {"validation", "diachronicCandidate", "diplomaticTranscription"}]:
    errors.append("lex0: RHD-specific documentary/validation layers leaked into strict projection")
for entry in lex0_entries:
    rid = entry.get(f"{{{XML}}}id")
    if entry.get("type") != "mainEntry":
        errors.append(f"lex0: {rid} missing type=mainEntry")
    if entry.get(f"{{{XML}}}lang") not in {"de", "und"}:
        errors.append(f"lex0: {rid} missing explicit entry xml:lang")
    if entry.get("source") != "#steffel1809":
        errors.append(f"lex0: {rid} missing source pointer")
    forms = entry.findall(Q("form"))
    if len(forms) != 1 or forms[0].get("type") != "lemma" or forms[0].find(Q("orth")) is None:
        errors.append(f"lex0: {rid} must contain exactly one lemma form")

if errors:
    print("\n".join("ERROR: " + e for e in errors)); sys.exit(1)
print(
    f"OK: rich RHD TEI preserves {len(rich_entries)} entries, {len(validation_notes)} PHIL notes and "
    f"{len(relation_notes)} diachronic candidates; strict Lex-0 projection preserves {len(lex0_entries)} lexical entries without RHD-specific assertion leakage"
)
