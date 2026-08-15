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

num_div = next((d for d in divs if d.get("type") == "appendix_numeration"), None)
if num_div is None:
    errors.append("numeration div missing")
else:
    primary = next((lst for lst in num_div.findall(Q("list")) if lst.get("type") == "primaryCardinals"), None)
    mult = next((lst for lst in num_div.findall(Q("list")) if lst.get("type") == "multiplicatives"), None)
    ords = next((lst for lst in num_div.findall(Q("list")) if lst.get("type") == "ordinals"), None)
    if primary is None or len(primary.findall(Q("item"))) < 30:
        errors.append("TEI numeration primaryCardinals inventory incomplete")
    if mult is None or len(mult.findall(Q("item"))) != 10:
        errors.append("TEI numeration multiplicatives inventory incomplete")
    if ords is None or len(ords.findall(Q("item"))) != 5:
        errors.append("TEI numeration ordinals inventory incomplete")
    for lst in num_div.findall(Q("list")):
        if lst.get("resp") != "#aiVisualAlignment":
            errors.append("numeration list lacks AI responsibility pointer")

prayer_div = next((d for d in divs if d.get("type") == "prayer_text"), None)
if prayer_div is None:
    errors.append("prayer div missing")
else:
    prayer = next((ab for ab in prayer_div.findall(Q("ab")) if ab.get("type") == "visualTranscription"), None)
    if prayer is None:
        errors.append("prayer visualTranscription block missing")
    else:
        if prayer.get(f"{{{XML}}}lang") != "und" or prayer.get("resp") != "#aiVisualAlignment":
            errors.append("prayer transcription language/responsibility invalid")
        if prayer.get("cert") not in {"high", "medium", "low"}:
            errors.append("prayer transcription confidence invalid")
        if not (prayer.text or "").strip().endswith("Amen."):
            errors.append("prayer transcription incomplete")

uncertainty_notes = [n for n in root.findall(f".//{Q('note')}") if n.get("type") == "uncertainty"]
if len(uncertainty_notes) < 6:
    errors.append(f"too few explicit uncertainty notes: {len(uncertainty_notes)}")

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
print("OK: appendix TEI has structured numeration, 22 formula triples / 66 language blocks, AI-transcribed prayer, uncertainty and explicit non-human responsibility")
