#!/usr/bin/env python3
from pathlib import Path
import json
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data" / "canonical" / "steffel-1809.entries.jsonl"
TEI_PATH = ROOT / "data" / "tei" / "rhd-steffel-1809-tei.xml"
TEI = "http://www.tei-c.org/ns/1.0"
XML = "http://www.w3.org/XML/1998/namespace"
Q = lambda n: f"{{{TEI}}}{n}"
errors = []

if not CANONICAL.exists():
    errors.append("canonical JSONL missing")
if not TEI_PATH.exists():
    errors.append("TEI projection missing")
if errors:
    print("\n".join("ERROR: " + e for e in errors)); sys.exit(1)

canonical = [json.loads(line) for line in CANONICAL.read_text(encoding="utf-8").splitlines() if line.strip()]
active = [x for x in canonical if x.get("status") == "active"]
expected_phil = sum(len(x.get("validation", [])) for x in active)
expected_relations = sum(len(x.get("historical_relations", [])) for x in active)
expected_translations = sum(
    1
    for x in active
    for sense in x.get("lexical", {}).get("senses", [])
    if sense.get("editorial_translation")
)

root = ET.parse(TEI_PATH).getroot()
if root.tag != Q("TEI"):
    errors.append("root is not TEI namespace TEI")
if root.get("type") != "dictionary":
    errors.append("TEI root must carry type=dictionary")

# Known Lex-0 0.9.5 header constraints we can enforce without the external schema.
licence = root.find(f"./{Q('teiHeader')}/{Q('fileDesc')}/{Q('publicationStmt')}/{Q('availability')}/{Q('licence')}")
if licence is None or not licence.get("target"):
    errors.append("publicationStmt/availability/licence missing")
list_bibl = root.find(f"./{Q('teiHeader')}/{Q('fileDesc')}/{Q('sourceDesc')}/{Q('listBibl')}")
if list_bibl is None or list_bibl.get("type") != "dictionaries":
    errors.append("sourceDesc must use listBibl type=dictionaries")
if list_bibl is not None and list_bibl.find(Q("biblStruct")) is None:
    errors.append("sourceDesc listBibl lacks biblStruct")
lang_usage = root.find(f"./{Q('teiHeader')}/{Q('profileDesc')}/{Q('langUsage')}")
if lang_usage is None:
    errors.append("profileDesc/langUsage missing")
else:
    languages = {(el.get("ident"), el.get("role")) for el in lang_usage.findall(Q("language"))}
    required_languages = {
        ("und", "objectLanguage"),
        ("de", "workingLanguage"),
        ("es", "workingLanguage"),
    }
    if not required_languages.issubset(languages):
        errors.append(f"language profile incomplete: {sorted(languages)}")
cat_desc = root.find(f".//{Q('category')}[@{{{XML}}}id='machineCandidate']/{Q('catDesc')}")
if cat_desc is None or cat_desc.find(Q("term")) is None:
    errors.append("machineCandidate catDesc must contain term")

entries = root.findall(f".//{Q('entry')}")
if len(entries) != len(active):
    errors.append(f"TEI entry count {len(entries)} != active canonical {len(active)}")
ids = [e.get(f"{{{XML}}}id") for e in entries]
if len(ids) != len(set(ids)):
    errors.append("duplicate xml:id in TEI entries")
if set(ids) != {x["record_id"] for x in active}:
    errors.append("TEI entry IDs differ from active canonical IDs")

# Critical safety rule: the conservative projection must not manufacture definitions.
if root.findall(f".//{Q('def')}"):
    errors.append("TEI projection contains <def>; unparsed source material must not be auto-promoted")

validation_notes = [
    n for n in root.findall(f".//{Q('note')}") if n.get("type") == "validation"
]
if len(validation_notes) != expected_phil:
    errors.append(f"TEI PHIL note count {len(validation_notes)} != {expected_phil}")

relations = [xr for xr in root.findall(f".//{Q('xr')}") if xr.get("type") == "diachronic-candidate"]
if len(relations) != expected_relations:
    errors.append(f"TEI diachronic relation count {len(relations)} != {expected_relations}")
for xr in relations:
    if xr.get("ana") != "#machineCandidate":
        errors.append("diachronic candidate lost machineCandidate annotation")
    if not (xr.get("corresp") or "").startswith("urn:raramuri-digital:RD-"):
        errors.append("diachronic candidate target is not an explicit Rarámuri Digital URN")

translations = [cit for cit in root.findall(f".//{Q('cit')}") if cit.get("type") == "translation"]
if len(translations) != expected_translations:
    errors.append(f"translation citation count {len(translations)} != {expected_translations}")
for cit in translations:
    if cit.get(f"{{{XML}}}lang") != "es":
        errors.append("editorial Spanish translation missing xml:lang=es")

for entry in entries:
    bibl = entry.find(Q("bibl"))
    if bibl is None or "printed p." not in (bibl.text or ""):
        errors.append(f"{entry.get(f'{{{XML}}}id')}: missing printed-page bibl")

if errors:
    print("\n".join("ERROR: " + e for e in errors)); sys.exit(1)
print(
    f"OK: TEI projection has Lex-0-ready header invariants, {len(entries)} active entries, "
    f"{len(validation_notes)} PHIL notes, {len(relations)} machine diachronic candidates, "
    f"{len(translations)} editorial translations, and no synthetic <def> elements"
)
