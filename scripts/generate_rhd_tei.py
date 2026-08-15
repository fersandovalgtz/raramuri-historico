#!/usr/bin/env python3
"""Generate the RHD Steffel TEI P5 research projection from canonical JSONL.

The output is intentionally conservative: it does not reinterpret unparsed source
article material as <def>. Editorial Spanish translations are encoded as translation
citations. Machine diachronic candidates remain explicitly non-adjudicated.

The header follows known TEI Lex-0 0.9.5 requirements (TEI @type, availability/licence,
listBibl/biblStruct source description, and language profile). Full Lex-0 schema
validation remains a separate release gate because the documentary transcription layer
contains project-specific structures that may require a dedicated TEI customization.
"""

from pathlib import Path
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data" / "canonical" / "steffel-1809.entries.jsonl"
OUT_DIR = ROOT / "data" / "tei"
OUT = OUT_DIR / "rhd-steffel-1809-tei.xml"

TEI = "http://www.tei-c.org/ns/1.0"
XML = "http://www.w3.org/XML/1998/namespace"
ET.register_namespace("", TEI)


def q(name):
    return f"{{{TEI}}}{name}"


def load_jsonl(path):
    with path.open(encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def sub(parent, name, text=None, attrs=None):
    el = ET.SubElement(parent, q(name), attrs or {})
    if text is not None:
        el.text = str(text)
    return el


def add_header(root):
    header = sub(root, "teiHeader")
    file_desc = sub(header, "fileDesc")
    title_stmt = sub(file_desc, "titleStmt")
    sub(title_stmt, "title", "Rarámuri Histórico Digital — Corpus Steffel 1791/1809")
    resp = sub(title_stmt, "respStmt")
    sub(resp, "resp", "Academic and technical coordination")
    sub(resp, "name", "Dr. Fernando Sandoval Gutierrez")

    publication = sub(file_desc, "publicationStmt")
    sub(publication, "publisher", "Rarámuri Histórico Digital")
    availability = sub(publication, "availability")
    sub(
        availability,
        "licence",
        "Editorial and derived data layers are released under CC BY 4.0; source facsimile rights and provenance are documented separately.",
        {"target": "https://creativecommons.org/licenses/by/4.0/"},
    )

    source_desc = sub(file_desc, "sourceDesc")
    list_bibl = sub(source_desc, "listBibl", attrs={"type": "dictionaries"})
    bibl_struct = sub(list_bibl, "biblStruct", attrs={f"{{{XML}}}id": "steffel1809"})
    monogr = sub(bibl_struct, "monogr")
    author = sub(monogr, "author")
    pers = sub(author, "persName")
    sub(pers, "forename", "Matthäus")
    sub(pers, "surname", "Steffel")
    sub(monogr, "title", "Tarahumarisches Wörterbuch")
    imprint = sub(monogr, "imprint")
    sub(imprint, "date", "1809", {"when": "1809"})
    note = sub(bibl_struct, "note")
    note.text = "Compiled/dated 1791; project working facsimile and preserved OCR are the documentary basis of this projection."

    encoding = sub(header, "encodingDesc")
    project = sub(encoding, "projectDesc")
    sub(
        project,
        "p",
        "Generated from the RHD 1.0 canonical layer. Facsimile, OCR, diplomatic transcription, AI-assisted recollation, human validation and diachronic relations remain epistemically separate.",
    )
    editorial = sub(encoding, "editorialDecl")
    sub(
        editorial,
        "p",
        "No unparsed OCR or diplomatic article text is automatically promoted to a lexical definition or semantic sense. Normalization and historical correspondence remain derived layers with explicit provenance.",
    )
    class_decl = sub(encoding, "classDecl")
    taxonomy = sub(class_decl, "taxonomy", attrs={f"{{{XML}}}id": "rhd-status"})
    cat = sub(taxonomy, "category", attrs={f"{{{XML}}}id": "machineCandidate"})
    cat_desc = sub(cat, "catDesc")
    sub(cat_desc, "term", "machine diachronic candidate")
    sub(
        cat_desc,
        "note",
        "No semantic, etymological or historical-continuity judgment is implied.",
    )

    profile = sub(header, "profileDesc")
    lang_usage = sub(profile, "langUsage")
    sub(
        lang_usage,
        "language",
        "Historical Tarahumara/Rarámuri as documented by Steffel; no modern ISO variety is assigned by RHD without independent linguistic adjudication.",
        {"ident": "und", "role": "objectLanguage"},
    )
    sub(
        lang_usage,
        "language",
        "German documentary metalanguage and historical dictionary language.",
        {"ident": "de", "role": "workingLanguage"},
    )
    sub(
        lang_usage,
        "language",
        "Spanish modern editorial translation and project documentation.",
        {"ident": "es", "role": "workingLanguage"},
    )

    revision = sub(header, "revisionDesc")
    change = sub(revision, "change", attrs={"when": "2026-08-15"})
    change.text = "RHD 1.0 canonical TEI projection introduced and header aligned to known TEI Lex-0 0.9.5 constraints; full Lex-0 schema validation remains a release gate."


def add_entry(div, item):
    rid = item["record_id"]
    attrs = {f"{{{XML}}}id": rid, "n": item.get("direction") or ""}
    entry = sub(div, "entry", attrs=attrs)

    forms = item.get("lexical", {}).get("forms", [])
    lemma = next((f for f in forms if f.get("type") == "lemma"), None)
    if lemma:
        form = sub(entry, "form", attrs={"type": "lemma"})
        orth_attrs = {}
        if lemma.get("language"):
            orth_attrs[f"{{{XML}}}lang"] = lemma["language"]
        sub(form, "orth", lemma.get("orth", ""), orth_attrs)

    diplomatic = item.get("layers", {}).get("diplomatic", {})
    if diplomatic.get("text"):
        cit = sub(entry, "cit", attrs={"type": "diplomatic-transcription"})
        sub(cit, "quote", diplomatic["text"])
        sub(
            cit,
            "note",
            "AI-assisted visual transcription; it is documentary evidence, not independent human verification.",
            {"type": "status"},
        )

    for sense in item.get("lexical", {}).get("senses", []):
        sense_attrs = {f"{{{XML}}}id": sense.get("sense_id")}
        sense_el = sub(entry, "sense", attrs=sense_attrs)
        if sense.get("editorial_translation"):
            cit = sub(sense_el, "cit", attrs={"type": "translation", f"{{{XML}}}lang": "es"})
            sub(cit, "quote", sense["editorial_translation"])
            sub(cit, "note", "Modern editorial translation; not attributed to Steffel.", {"type": "responsibility"})

    loc = item.get("locators", {})
    bibl_text = f"Steffel 1809, printed p. {loc.get('printed_page')}"
    if loc.get("column"):
        bibl_text += f", {loc['column']} column"
    if loc.get("digital_page") is not None:
        bibl_text += f"; digital page {loc['digital_page']}"
    sub(entry, "bibl", bibl_text)

    for event in item.get("validation", []):
        if event.get("reviewer_type") != "ai_assisted":
            continue
        attrs = {"type": "validation", "subtype": event.get("scope", "general")}
        note = sub(entry, "note", attrs=attrs)
        note.text = f"{event.get('event_id')}: {event.get('decision')}"
        if event.get("justification"):
            note.text += f" — {event['justification']}"

    for relation in item.get("historical_relations", []):
        xr = sub(
            entry,
            "xr",
            attrs={
                "type": "diachronic-candidate",
                "ana": "#machineCandidate",
                "corresp": f"urn:raramuri-digital:{relation['target_id']}",
            },
        )
        ref = sub(xr, "ref", attrs={"target": f"urn:raramuri-digital:{relation['target_id']}"})
        ref.text = relation["target_id"]
        sub(
            xr,
            "note",
            f"Candidate only; retrieval signal={relation.get('method')}; human_reviewed={str(relation.get('human_reviewed')).lower()}.",
            {"type": "status"},
        )


def main():
    items = load_jsonl(CANONICAL)
    root = ET.Element(q("TEI"), {"type": "dictionary"})
    add_header(root)
    text_el = sub(root, "text")
    body = sub(text_el, "body")

    active = [x for x in items if x.get("status") == "active"]
    for direction in ("DE-RAR", "RAR-DE"):
        div = sub(body, "div", attrs={"type": "dictionary", "n": direction})
        for item in active:
            if item.get("direction") == direction:
                add_entry(div, item)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ET.indent(root)
    ET.ElementTree(root).write(OUT, encoding="utf-8", xml_declaration=True)
    print(f"generated TEI P5 research projection for {len(active)} active entries -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
