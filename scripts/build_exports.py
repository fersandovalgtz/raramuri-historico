#!/usr/bin/env python3
"""Regenera las serializaciones públicas a partir del CSV canónico."""
from pathlib import Path
import csv, json, sqlite3
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "entries_curated.csv"

with CSV_PATH.open(encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

for row in rows:
    for key in ("printed_page", "pdf_page", "source_ocr_line"):
        row[key] = int(row[key])

# JSON completo
json_dir = ROOT / "data" / "json"
json_dir.mkdir(parents=True, exist_ok=True)
(json_dir / "entries_curated.json").write_text(
    json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

# XML documental sencillo
xml_dir = ROOT / "data" / "xml"
xml_dir.mkdir(parents=True, exist_ok=True)
root = ET.Element("raramuriHistorico", {"version": "0.1.0-mvp", "source": "STEFFEL-1809"})
for row in rows:
    e = ET.SubElement(root, "entry", {"id": row["record_id"], "direction": row["direction"]})
    for key in ("headword_raw", "headword_search", "gloss_de_raw", "translation_es_editorial", "printed_page", "pdf_page", "source_ocr_line", "editorial_note", "status", "validation"):
        child = ET.SubElement(e, key)
        child.text = str(row[key])
ET.indent(root)
ET.ElementTree(root).write(xml_dir / "entries_curated.xml", encoding="utf-8", xml_declaration=True)

# Borrador TEI. No se declara aún como TEI Lex-0 validado.
TEI_NS = "http://www.tei-c.org/ns/1.0"
XML_NS = "http://www.w3.org/XML/1998/namespace"
ET.register_namespace("", TEI_NS)
tei = ET.Element(f"{{{TEI_NS}}}TEI")
header = ET.SubElement(tei, f"{{{TEI_NS}}}teiHeader")
file_desc = ET.SubElement(header, f"{{{TEI_NS}}}fileDesc")
title_stmt = ET.SubElement(file_desc, f"{{{TEI_NS}}}titleStmt")
ET.SubElement(title_stmt, f"{{{TEI_NS}}}title").text = "Rarámuri Histórico Digital — Corpus Steffel 1791/1809"
pub_stmt = ET.SubElement(file_desc, f"{{{TEI_NS}}}publicationStmt")
ET.SubElement(pub_stmt, f"{{{TEI_NS}}}p").text = "MVP de investigación; validación lingüística pendiente."
source_desc = ET.SubElement(file_desc, f"{{{TEI_NS}}}sourceDesc")
ET.SubElement(source_desc, f"{{{TEI_NS}}}p").text = "Matthäus Steffel, Tarahumarisches Wörterbuch, edición de 1809."
text = ET.SubElement(tei, f"{{{TEI_NS}}}text")
body = ET.SubElement(text, f"{{{TEI_NS}}}body")
for row in rows:
    entry = ET.SubElement(body, f"{{{TEI_NS}}}entry", {f"{{{XML_NS}}}id": row["record_id"]})
    form = ET.SubElement(entry, f"{{{TEI_NS}}}form", {"type": "lemma"})
    ET.SubElement(form, f"{{{TEI_NS}}}orth").text = row["headword_raw"]
    sense = ET.SubElement(entry, f"{{{TEI_NS}}}sense")
    definition = ET.SubElement(sense, f"{{{TEI_NS}}}def", {f"{{{XML_NS}}}lang": "de"})
    definition.text = row["gloss_de_raw"]
    note = ET.SubElement(sense, f"{{{TEI_NS}}}note", {"type": "editorial-translation", f"{{{XML_NS}}}lang": "es"})
    note.text = row["translation_es_editorial"]
    ET.SubElement(entry, f"{{{TEI_NS}}}bibl").text = f"Steffel 1809, p. {row['printed_page']}"
    ET.SubElement(entry, f"{{{TEI_NS}}}note", {"type": "status"}).text = row["validation"]
ET.indent(tei)
ET.ElementTree(tei).write(xml_dir / "steffel-1809-tei-draft.xml", encoding="utf-8", xml_declaration=True)

# SQLite reproducible
sql_path = ROOT / "data" / "raramuri_historico.sqlite"
if sql_path.exists():
    sql_path.unlink()
con = sqlite3.connect(sql_path)
con.execute("""CREATE TABLE entries (
record_id TEXT PRIMARY KEY, source_code TEXT NOT NULL, direction TEXT NOT NULL,
headword_raw TEXT NOT NULL, headword_search TEXT NOT NULL, gloss_de_raw TEXT,
translation_es_editorial TEXT, printed_page INTEGER, pdf_page INTEGER,
source_ocr_line INTEGER, editorial_note TEXT, status TEXT, validation TEXT)""")
fields = ["record_id","source_code","direction","headword_raw","headword_search","gloss_de_raw","translation_es_editorial","printed_page","pdf_page","source_ocr_line","editorial_note","status","validation"]
con.executemany(
    f"INSERT INTO entries ({','.join(fields)}) VALUES ({','.join('?' for _ in fields)})",
    [[row[k] for k in fields] for row in rows],
)
con.commit(); con.close()

# Proyección ligera para la interfaz pública
public_dir = ROOT / "public" / "data"
public_dir.mkdir(parents=True, exist_ok=True)
projection_fields = ["record_id", "direction", "headword_raw", "gloss_de_raw", "translation_es_editorial", "printed_page"]
projection = [{k: row[k] for k in projection_fields} for row in rows]
(public_dir / "entries.json").write_text(
    json.dumps(projection, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8"
)

print(f"Generated JSON/XML/TEI/SQLite/public projection from {len(rows)} canonical entries")
