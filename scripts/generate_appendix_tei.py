#!/usr/bin/env python3
"""Generate a TEI P5 supplement for Steffel's machine-aligned appendices.

This file is intentionally separate from the strict Lex-0 dictionary projection.
Formula-level Latin/German/Tarahumara alignment is AI-assisted, line-break normalized,
and carries explicit confidence/uncertainty. No human verification is claimed.
"""

from pathlib import Path
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data/canonical/steffel-1809.appendices.json"
OUT_DIR = ROOT / "data/tei"
OUT = OUT_DIR / "rhd-steffel-1809-appendices-tei.xml"
TEI = "http://www.tei-c.org/ns/1.0"
XML = "http://www.w3.org/XML/1998/namespace"
ET.register_namespace("", TEI)


def q(name):
    return f"{{{TEI}}}{name}"


def sub(parent, name, text=None, attrs=None):
    el = ET.SubElement(parent, q(name), attrs or {})
    if text is not None:
        el.text = str(text)
    return el


def main():
    data = json.loads(CANONICAL.read_text(encoding="utf-8"))
    root = ET.Element(q("TEI"), {"type": "appendix"})
    header = sub(root, "teiHeader")
    file_desc = sub(header, "fileDesc")
    title_stmt = sub(file_desc, "titleStmt")
    sub(title_stmt, "title", "Rarámuri Histórico Digital — Steffel 1809 appendices — machine-aligned TEI supplement")
    resp = sub(title_stmt, "respStmt")
    sub(resp, "resp", "Academic and technical coordination")
    sub(resp, "name", "Dr. Fernando Sandoval Gutierrez")
    publication = sub(file_desc, "publicationStmt")
    sub(publication, "publisher", "Rarámuri Histórico Digital")
    availability = sub(publication, "availability")
    sub(availability, "p", "Machine-only scholarly supplement; no human validation is claimed.")
    source_desc = sub(file_desc, "sourceDesc")
    bibl = sub(source_desc, "bibl")
    bibl.text = "Matthäus Steffel, Tarahumarisches Wörterbuch, 1809, printed pp. 369–374."

    encoding = sub(header, "encodingDesc")
    project = sub(encoding, "projectDesc")
    sub(
        project,
        "p",
        "Generated from the canonical RHD appendix layer. Formula alignment was produced by AI visual transcription from the project facsimile. Line breaks are normalized; confidence and uncertainty remain explicit.",
    )
    profile = sub(header, "profileDesc")
    lang_usage = sub(profile, "langUsage")
    sub(lang_usage, "language", "Latin", {"ident": "la"})
    sub(lang_usage, "language", "German", {"ident": "de"})
    sub(lang_usage, "language", "Historical Tarahumara/Rarámuri as documented by Steffel", {"ident": "und"})
    revision = sub(header, "revisionDesc")
    sub(revision, "change", "Initial machine-aligned appendix TEI supplement.", {"when": "2026-08-15"})

    text = sub(root, "text")
    body = sub(text, "body")
    collection = sub(body, "div", attrs={"type": "appendixCollection", "n": "Steffel-1809"})
    sub(collection, "head", "Tarahumarische Sprachprobe and associated appendices")

    for obj in data.get("objects", []):
        otype = obj.get("object_type")
        div = sub(
            collection,
            "div",
            attrs={
                f"{{{XML}}}id": obj["object_id"],
                "type": otype,
                **({"n": str(obj["sequence"])} if obj.get("sequence") is not None else {}),
            },
        )
        if obj.get("title_source_ocr"):
            sub(div, "head", obj["title_source_ocr"])
        pp = obj.get("printed_page")
        pdf = obj.get("pdf_page")
        if obj.get("printed_pages"):
            pp = "–".join(str(x) for x in obj["printed_pages"])
        if obj.get("pdf_pages"):
            pdf = "–".join(str(x) for x in obj["pdf_pages"])
        sub(div, "note", f"Steffel 1809, printed p. {pp}; PDF page {pdf}", {"type": "sourceLocation"})

        if otype == "parallel_formula":
            alignment = obj.get("layers", {}).get("parallel_alignment", {})
            texts = alignment.get("texts", {})
            confidence = alignment.get("confidence", {})
            for lang in ("la", "de", "und"):
                ab = sub(
                    div,
                    "ab",
                    texts.get(lang, ""),
                    {
                        "type": "parallelText",
                        f"{{{XML}}}lang": lang,
                        "cert": confidence.get(lang, "unknown"),
                    },
                )
                ab.set("resp", "#aiVisualAlignment")
            for uncertainty in alignment.get("uncertain_segments", []):
                sub(div, "note", uncertainty, {"type": "uncertainty", "resp": "#aiVisualAlignment"})
            sub(
                div,
                "note",
                "Formula-level language alignment is AI-assisted and not human verified.",
                {"type": "epistemicStatus"},
            )
        else:
            ocr = obj.get("layers", {}).get("ocr", {})
            if ocr.get("text"):
                sub(div, "ab", ocr["text"], {"type": "ocrCandidate"})
            sub(div, "note", "This appendix object remains an OCR/AI documentary candidate.", {"type": "epistemicStatus"})

    # Responsibility declaration referenced by @resp values.
    stand_off = sub(root, "standOff")
    list_person = sub(stand_off, "listPerson")
    person = sub(list_person, "person", attrs={f"{{{XML}}}id": "aiVisualAlignment"})
    sub(person, "persName", "AI-assisted visual alignment process")
    sub(person, "note", "Non-human computational agent/process; no human verification implied.")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ET.indent(root)
    ET.ElementTree(root).write(OUT, encoding="utf-8", xml_declaration=True)
    print(f"generated appendix TEI supplement for {len(data.get('objects', []))} objects -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
