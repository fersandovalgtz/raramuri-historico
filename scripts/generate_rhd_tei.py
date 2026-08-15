#!/usr/bin/env python3
"""Generate two TEI projections from the RHD 1.0 canonical layer.

1. `rhd-steffel-1809-tei.xml` is the rich RHD TEI P5 research edition. It keeps
   documentary transcription, PHIL status, diachronic candidates and canonical
   appendix objects visible.
2. `rhd-steffel-1809-lex0.xml` is a deliberately narrow TEI Lex-0 interoperability
   projection. It contains only claims that can be expressed honestly inside Lex-0
   without coercing RHD-specific documentary or epistemic layers into lexicographic
   constructs.

Neither output promotes unparsed `definition_raw` to `<def>`.
"""

from pathlib import Path
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data" / "canonical" / "steffel-1809.entries.jsonl"
CANONICAL_APPENDICES = ROOT / "data" / "canonical" / "steffel-1809.appendices.json"
OUT_DIR = ROOT / "data" / "tei"
RICH_OUT = OUT_DIR / "rhd-steffel-1809-tei.xml"
LEX0_OUT = OUT_DIR / "rhd-steffel-1809-lex0.xml"

TEI = "http://www.tei-c.org/ns/1.0"
XML = "http://www.w3.org/XML/1998/namespace"
ET.register_namespace("", TEI)


def q(name):
    return f"{{{TEI}}}{name}"


def load_jsonl(path):
    with path.open(encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sub(parent, name, text=None, attrs=None):
    el = ET.SubElement(parent, q(name), attrs or {})
    if text is not None:
        el.text = str(text)
    return el


def add_common_header(root, title, project_text, revision_text):
    header = sub(root, "teiHeader")
    file_desc = sub(header, "fileDesc")
    title_stmt = sub(file_desc, "titleStmt")
    sub(title_stmt, "title", title)
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

    encoding = sub(header, "encodingDesc")
    project = sub(encoding, "projectDesc")
    sub(project, "p", project_text)
    editorial = sub(encoding, "editorialDecl")
    sub(
        editorial,
        "p",
        "No unparsed OCR or diplomatic article text is automatically promoted to a lexical definition or semantic sense. Normalization and historical correspondence remain derived layers with explicit provenance. The current scholarly release is machine-only and does not claim human validation.",
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
        "German dictionary language.",
        {"ident": "de", "role": "objectLanguage"},
    )
    sub(
        lang_usage,
        "language",
        "Latin in the trilingual language sample.",
        {"ident": "la", "role": "objectLanguage"},
    )
    sub(
        lang_usage,
        "language",
        "Spanish modern editorial and project language.",
        {"ident": "es", "role": "workingLanguage"},
    )

    revision = sub(header, "revisionDesc")
    change = sub(revision, "change", attrs={"when": "2026-08-15"})
    change.text = revision_text
    return header


def entry_language(item):
    return "de" if item.get("direction") == "DE-RAR" else "und"


def lemma_for(item):
    forms = item.get("lexical", {}).get("forms", [])
    return next((f for f in forms if f.get("type") == "lemma" and f.get("orth")), None)


def add_rich_header(root):
    header = add_common_header(
        root,
        "Rarámuri Histórico Digital — Corpus Steffel 1791/1809 — TEI research edition",
        "Rich RHD TEI P5 projection generated from the RHD 1.0 canonical layers. Facsimile, OCR, diplomatic transcription, AI-assisted recollation, explicit uncertainty, appendices and diachronic relations remain epistemically separate. No human adjudication is required or claimed in the current edition scope.",
        "Rich machine-only RHD TEI P5 projection generated from canonical lexical and appendix layers; it is not asserted to be a strict TEI Lex-0 document.",
    )
    encoding = header.find(q("encodingDesc"))
    class_decl = sub(encoding, "classDecl")
    taxonomy = sub(class_decl, "taxonomy", attrs={f"{{{XML}}}id": "rhd-status"})
    cat = sub(taxonomy, "category", attrs={f"{{{XML}}}id": "machineCandidate"})
    cat_desc = sub(cat, "catDesc")
    sub(cat_desc, "term", "machine candidate")
    sub(cat_desc, "note", "No human validation, semantic identity, etymology or historical-continuity judgment is implied.")


def add_rich_entry(div, item):
    rid = item["record_id"]
    entry = sub(
        div,
        "entry",
        attrs={
            f"{{{XML}}}id": rid,
            f"{{{XML}}}lang": entry_language(item),
            "type": "mainEntry",
            "n": item.get("direction") or "",
        },
    )

    lemma = lemma_for(item)
    if lemma:
        form = sub(entry, "form", attrs={"type": "lemma"})
        sub(form, "orth", lemma["orth"])

    diplomatic = item.get("layers", {}).get("diplomatic", {})
    if diplomatic.get("text"):
        note = sub(entry, "note", attrs={"type": "diplomaticTranscription"})
        note.text = diplomatic["text"]
        sub(
            entry,
            "note",
            "Diplomatic transcription above is AI-assisted documentary evidence; no human verification is claimed.",
            {"type": "epistemicStatus"},
        )

    for sense in item.get("lexical", {}).get("senses", []):
        if sense.get("editorial_translation"):
            cit = sub(entry, "cit", attrs={"type": "translation", f"{{{XML}}}lang": "es"})
            sub(cit, "quote", sense["editorial_translation"])
            sub(cit, "note", "Modern editorial translation; not attributed to Steffel.", {"type": "responsibility"})

    loc = item.get("locators", {})
    location = f"Steffel 1809, printed p. {loc.get('printed_page')}"
    if loc.get("column"):
        location += f", {loc['column']} column"
    if loc.get("digital_page") is not None:
        location += f"; digital page {loc['digital_page']}"
    sub(entry, "note", location, {"type": "sourceLocation"})

    for event in item.get("validation", []):
        if event.get("reviewer_type") != "ai_assisted":
            continue
        note = sub(entry, "note", attrs={"type": "validation", "subtype": event.get("scope", "general")})
        note.text = f"{event.get('event_id')}: {event.get('decision')}"
        if event.get("justification"):
            note.text += f" — {event['justification']}"

    for relation in item.get("historical_relations", []):
        note = sub(
            entry,
            "note",
            attrs={
                "type": "diachronicCandidate",
                "ana": "#machineCandidate",
                "corresp": f"urn:raramuri-digital:{relation['target_id']}",
            },
        )
        note.text = (
            f"Candidate relation to {relation['target_id']}; retrieval signal={relation.get('method')}; "
            f"human_reviewed={str(relation.get('human_reviewed')).lower()}."
        )


def add_rich_appendices(body, appendix_data):
    collection = sub(
        body,
        "div",
        attrs={
            "type": "appendixCollection",
            "n": "Steffel-1809-appendices",
            "ana": "#machineCandidate",
        },
    )
    sub(
        collection,
        "head",
        "Steffel appendices — machine-only canonical projection",
    )
    sub(
        collection,
        "note",
        "Appendix structures combine source OCR with AI visual page/sequence collation. No human validation or language-line alignment is claimed.",
        {"type": "epistemicStatus"},
    )

    for obj in appendix_data.get("objects", []):
        otype = obj.get("object_type")
        attrs = {
            f"{{{XML}}}id": obj["object_id"],
            "type": otype,
            "ana": "#machineCandidate",
        }
        if obj.get("sequence") is not None:
            attrs["n"] = str(obj["sequence"])
        div = sub(collection, "div", attrs=attrs)
        title = obj.get("title_source_ocr")
        if title:
            sub(div, "head", title)

        printed = obj.get("printed_page")
        pdf_page = obj.get("pdf_page")
        if obj.get("printed_pages"):
            printed = "–".join(str(x) for x in obj["printed_pages"])
        if obj.get("pdf_pages"):
            pdf_page = "–".join(str(x) for x in obj["pdf_pages"])
        sub(div, "note", f"Steffel 1809, printed p. {printed}; PDF page {pdf_page}", {"type": "sourceLocation"})

        ocr = obj.get("layers", {}).get("ocr", {})
        if ocr.get("text"):
            sub(div, "ab", ocr["text"], {"type": "ocrCandidate"})
        visual = obj.get("layers", {}).get("visual_collation", {})
        if visual:
            sub(
                div,
                "note",
                visual.get("claim") or "AI visual collation recorded.",
                {"type": "visualCollation", "subtype": visual.get("status", "confirmed_ai_assisted")},
            )
        if otype == "parallel_formula":
            sub(
                div,
                "note",
                "Expected printed language order: Latin, German, Tarahumara. Language-line alignment is not yet asserted in this OCR-level canonical projection.",
                {"type": "parallelTextStatus"},
            )


def generate_rich(active, appendix_data):
    root = ET.Element(q("TEI"), {"type": "dictionary"})
    add_rich_header(root)
    text_el = sub(root, "text")
    body = sub(text_el, "body")
    for direction in ("DE-RAR", "RAR-DE"):
        div = sub(body, "div", attrs={"type": "dictionary", "n": direction})
        for item in active:
            if item.get("direction") == direction:
                add_rich_entry(div, item)
    add_rich_appendices(body, appendix_data)
    ET.indent(root)
    ET.ElementTree(root).write(RICH_OUT, encoding="utf-8", xml_declaration=True)


def generate_lex0(active):
    """Produce a strict, intentionally minimal Lex-0 projection.

    RHD-specific documentary transcription, validation events, appendices, page-level
    notes and diachronic hypotheses stay in the rich TEI/canonical layers. Lex-0
    receives only persistent lexical entries and diplomatic lemmas.
    """
    root = ET.Element(q("TEI"), {"type": "lex-0"})
    add_common_header(
        root,
        "Rarámuri Histórico Digital — Corpus Steffel 1791/1809 — TEI Lex-0 projection",
        "Strict interoperability projection from the RHD 1.0 canonical lexical layer. RHD-specific documentary, appendix and validation layers remain outside this Lex-0 projection and are linked by persistent record identifiers.",
        "Strict TEI Lex-0 interoperability projection generated separately from the rich machine-only RHD TEI research edition.",
    )
    text_el = sub(root, "text")
    body = sub(text_el, "body")

    for item in active:
        lemma = lemma_for(item)
        if not lemma:
            continue
        entry = sub(
            body,
            "entry",
            attrs={
                f"{{{XML}}}id": item["record_id"],
                f"{{{XML}}}lang": entry_language(item),
                "type": "mainEntry",
                "n": item.get("direction") or "",
                "source": "#steffel1809",
            },
        )
        form = sub(entry, "form", attrs={"type": "lemma"})
        sub(form, "orth", lemma["orth"])

    ET.indent(root)
    ET.ElementTree(root).write(LEX0_OUT, encoding="utf-8", xml_declaration=True)


def main():
    items = load_jsonl(CANONICAL)
    active = [x for x in items if x.get("status") == "active"]
    appendices = load_json(CANONICAL_APPENDICES)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    generate_rich(active, appendices)
    generate_lex0(active)
    print(
        f"generated rich RHD TEI for {len(active)} active entries + {len(appendices.get('objects', []))} appendix objects "
        f"and strict Lex-0 projection for {len(active)} lexical entries -> "
        f"{RICH_OUT.relative_to(ROOT)}, {LEX0_OUT.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
