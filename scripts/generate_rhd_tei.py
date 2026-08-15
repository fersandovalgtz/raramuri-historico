#!/usr/bin/env python3
"""Generate two TEI projections from the RHD 1.0 canonical layer.

1. `rhd-steffel-1809-tei.xml` is the rich RHD TEI P5 research edition. It keeps
   documentary transcription, PHIL status and diachronic candidates visible.
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
        "No unparsed OCR or diplomatic article text is automatically promoted to a lexical definition or semantic sense. Normalization and historical correspondence remain derived layers with explicit provenance.",
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
        "Rich RHD TEI P5 projection generated from the RHD 1.0 canonical layer. Facsimile, OCR, diplomatic transcription, AI-assisted recollation, human validation and diachronic relations remain epistemically separate.",
        "Rich RHD TEI P5 projection generated from the canonical layer; it is not asserted to be a strict TEI Lex-0 document.",
    )
    encoding = header.find(q("encodingDesc"))
    class_decl = sub(encoding, "classDecl")
    taxonomy = sub(class_decl, "taxonomy", attrs={f"{{{XML}}}id": "rhd-status"})
    cat = sub(taxonomy, "category", attrs={f"{{{XML}}}id": "machineCandidate"})
    cat_desc = sub(cat, "catDesc")
    sub(cat_desc, "term", "machine diachronic candidate")
    sub(cat_desc, "note", "No semantic, etymological or historical-continuity judgment is implied.")


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
            "Diplomatic transcription above is AI-assisted documentary evidence, not independent human verification.",
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


def generate_rich(active):
    root = ET.Element(q("TEI"), {"type": "dictionary"})
    add_rich_header(root)
    text_el = sub(root, "text")
    body = sub(text_el, "body")
    for direction in ("DE-RAR", "RAR-DE"):
        div = sub(body, "div", attrs={"type": "dictionary", "n": direction})
        for item in active:
            if item.get("direction") == direction:
                add_rich_entry(div, item)
    ET.indent(root)
    ET.ElementTree(root).write(RICH_OUT, encoding="utf-8", xml_declaration=True)


def generate_lex0(active):
    """Produce a strict, intentionally minimal Lex-0 projection.

    RHD-specific documentary transcription, validation events, page-level notes and
    diachronic hypotheses stay in the rich TEI/canonical layers. Lex-0 receives only
    persistent lexical entries and diplomatic lemmas, with explicit entry language.
    """
    root = ET.Element(q("TEI"), {"type": "dictionary"})
    add_common_header(
        root,
        "Rarámuri Histórico Digital — Corpus Steffel 1791/1809 — TEI Lex-0 projection",
        "Strict interoperability projection from the RHD 1.0 canonical layer. RHD-specific documentary and validation layers remain outside this Lex-0 projection and are linked by persistent record identifiers.",
        "Strict TEI Lex-0 interoperability projection generated separately from the rich RHD TEI research edition.",
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
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    generate_rich(active)
    generate_lex0(active)
    print(
        f"generated rich RHD TEI and strict Lex-0 projection for {len(active)} active entries -> "
        f"{RICH_OUT.relative_to(ROOT)}, {LEX0_OUT.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
