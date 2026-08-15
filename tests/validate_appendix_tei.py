#!/usr/bin/env python3
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data/tei/rhd-steffel-1809-appendices-tei.xml"
TEI = "http://www.tei-c.org/ns/1.0"
XML = "http://www.w3.org/XML/1998/namespace"
Q = lambda n: f"{{{TEI}}}{n}"
errors = []

if not PATH.exists():
    print("ERROR: appendix TEI supplement missing")
    sys.exit(1)

root = ET.parse(PATH).getroot()
if root.tag != Q("TEI") or root.get("type") != "appendix":
    errors.append("appendix TEI root/type invalid")
collection = next((d for d in root.findall(f".//{Q('div')}") if d.get("type") == "appendixCollection"), None)
if collection is None:
    errors.append("appendixCollection missing")
    divs = []
else:
    divs = [d for d in collection.findall(Q("div")) if d.get(f"{{{XML}}}id")]
if len(divs) != 24:
    errors.append(f"expected 24 appendix divs, got {len(divs)}")
formulas = [d for d in divs if d.get("type") == "parallel_formula"]
if len(formulas) != 22:
    errors.append(f"expected 22 parallel formula divs, got {len(formulas)}")
if [int(d.get("n")) for d in formulas] != list(range(1, 23)):
    errors.append("formula order is not 1..22")

parallel = [ab for ab in root.findall(f".//{Q('ab')}") if ab.get("type") == "parallelText"]
if len(parallel) != 66:
    errors.append(f"expected 66 aligned language blocks, got {len(parallel)}")
lang_counts = {lang: 0 for lang in ("la", "de", "und")}
for ab in parallel:
    lang = ab.get(f"{{{XML}}}lang")
    if lang not in lang_counts:
        errors.append(f"unexpected parallel language: {lang}")
        continue
    lang_counts[lang] += 1
    if ab.get("cert") not in {"high", "medium", "low"}:
        errors.append(f"invalid cert on {lang} parallel block")
    if ab.get("resp") != "#aiVisualAlignment":
        errors.append("parallel block missing AI responsibility pointer")
    if not (ab.text or "").strip():
        errors.append("empty parallel block")
if any(v != 22 for v in lang_counts.values()):
    errors.append(f"language block counts differ from 22: {lang_counts}")

low_und = [ab for ab in parallel if ab.get(f"{{{XML}}}lang") == "und" and ab.get("cert") == "low"]
if len(low_und) != 2:
    errors.append(f"expected two low-confidence Tarahumara blocks, got {len(low_und)}")
uncertainty_notes = [n for n in root.findall(f".//{Q('note')}") if n.get("type") == "uncertainty"]
if len(uncertainty_notes) < 2:
    errors.append("uncertainty notes missing")

agent = root.find(f"./{Q('standOff')}/{Q('listPerson')}/{Q('person')}[@{{{XML}}}id='aiVisualAlignment']")
if agent is None:
    errors.append("AI responsibility declaration missing")
else:
    note = agent.find(Q("note"))
    if note is None or "Non-human" not in (note.text or ""):
        errors.append("AI responsibility declaration does not explicitly deny human status")

if errors:
    print("\n".join("ERROR: " + e for e in errors))
    sys.exit(1)
print("OK: appendix TEI has 24 objects, 22 formula triples / 66 language blocks, confidence and explicit non-human responsibility")
