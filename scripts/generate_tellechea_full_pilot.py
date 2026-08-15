#!/usr/bin/env python3
"""Traverse the complete checksum-fixed Tellechea 1826 witness through RHD.

This is the strong industrialization pilot, not a claim that Tellechea has become a
fully adjudicated critical edition. Every one of the 205 PDF pages becomes a stable
RHD documentary unit. The embedded PDF text is preserved as a source extraction.
Pages with little/no embedded text receive a separate visual OCR fallback from a
rendered facsimile. Major section headings are detected conservatively and kept as
machine candidates. The complete witness is exported to documentary TEI; nothing is
coerced into Lex-0 or promoted to human validation.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/tellechea-1826-dgb.pdf")
OUT_DIR = ROOT / "data/pilot"
JSONL = OUT_DIR / "tellechea-1826.full-witness.jsonl"
TEI = OUT_DIR / "tellechea-1826.full-witness.tei.xml"
DIAG = OUT_DIR / "tellechea-1826.full-witness.diagnostics.json"
EXPECTED_SHA256 = "c67b7942090613c494d8057be8aff59ea13a11519c29eae469afad8a85c30dfc"
EXPECTED_PAGES = 205
WITNESS_ID = "RHD-WIT-TELLECHEA-1826-DGB"
SOURCE_ID = "RHD-SRC-TELLECHEA-1826"

NS = "http://www.tei-c.org/ns/1.0"
XML_NS = "http://www.w3.org/XML/1998/namespace"
ET.register_namespace("", NS)

MAJOR_HEADINGS = [
    ("preface", ("prefacion", "prefacio")),
    ("book_1", ("libro primero",)),
    ("book_2", ("libro segundo",)),
    ("book_3", ("libro tercero",)),
    ("book_4", ("libro cuarto",)),
    ("doctrinal_material", ("doctrina christiana", "doctrina cristiana")),
    ("prayers_or_sacramental_material", ("oraciones", "sacramentos")),
]


def q(tag: str) -> str:
    return f"{{{NS}}}{tag}"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def norm(text: str) -> str:
    text = (text or "").lower()
    text = (
        text.replace("á", "a").replace("é", "e").replace("í", "i")
        .replace("ó", "o").replace("ú", "u").replace("ü", "u")
    )
    return re.sub(r"[^a-z0-9]+", " ", text)


def printed_number(text: str):
    head = (text or "")[:300]
    m = re.search(r"\(\s*([0-9]{1,3})\s*\)", head)
    return int(m.group(1)) if m else None


def detect_major_heading(text: str):
    # Restrict detection to the beginning of a page so occurrences inside prose do not
    # silently create structural boundaries.
    head = norm((text or "")[:900])
    for section_type, variants in MAJOR_HEADINGS:
        for variant in variants:
            if variant in head:
                return section_type, variant
    return None, None


def detect_chapter_heading(text: str):
    head = norm((text or "")[:700])
    m = re.search(r"\bcap(?:itulo|itvlo|\.)?\s+([ivxlcdm0-9]+)\b", head)
    return m.group(0) if m else None


def render_and_ocr(pdf_page_1based: int, work: Path) -> str:
    prefix = work / f"p{pdf_page_1based:03d}"
    subprocess.run(
        [
            "pdftoppm", "-f", str(pdf_page_1based), "-singlefile", "-r", "150",
            "-gray", "-png", str(PDF), str(prefix),
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    image = prefix.with_suffix(".png")
    proc = subprocess.run(
        ["tesseract", str(image), "stdout", "-l", "spa", "--psm", "6"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        image.unlink()
    except FileNotFoundError:
        pass
    return proc.stdout.strip()


def layer(text: str, status: str, method: str, activity_id: str, confidence: str):
    return {
        "text": text,
        "headword": None,
        "status": status,
        "method": method,
        "activity_id": activity_id,
        "responsibility": "machine",
        "confidence": confidence,
        "derived_from": [WITNESS_ID],
    }


def extraction_provenance(record_id: str, page: int, fallback_activity: str | None):
    items = [
        {
            "activity_id": f"RHD-ACT-T1826-FULL-EMBED-{page:03d}",
            "activity_type": "embedded_text_extraction",
            "generated_entity": f"{record_id}#ocr_raw",
            "used_entities": [WITNESS_ID],
            "agent_id": "pypdf",
            "agent_type": "software",
            "method": "extract_text from checksum-fixed PDF",
            "timestamp": None,
            "software_version": None,
        }
    ]
    if fallback_activity:
        items.append(
            {
                "activity_id": fallback_activity,
                "activity_type": "machine_visual_ocr",
                "generated_entity": f"{record_id}#diplomatic",
                "used_entities": [WITNESS_ID],
                "agent_id": "tesseract-spa",
                "agent_type": "software",
                "method": "150dpi grayscale facsimile render followed by Tesseract OCR fallback; unadjudicated",
                "timestamp": None,
                "software_version": None,
            }
        )
    return items


def main():
    if not PDF.exists():
        raise SystemExit(f"ERROR: checksum-fixed Tellechea PDF not found: {PDF}")
    digest = sha256(PDF)
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"ERROR: refusing non-pinned Tellechea binary: {digest}")

    reader = PdfReader(str(PDF), strict=False)
    if len(reader.pages) != EXPECTED_PAGES:
        raise SystemExit(f"ERROR: expected {EXPECTED_PAGES} pages, got {len(reader.pages)}")

    embedded = []
    for page in reader.pages:
        try:
            embedded.append((page.extract_text() or "").strip())
        except Exception:
            embedded.append("")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    records = []
    transitions = []
    current_section = "front_matter"
    current_section_id = "T1826-SEC-001"
    section_counter = 1
    fallback_pages = []
    blank_pages = []
    chapter_pages = []

    with tempfile.TemporaryDirectory(prefix="rhd-tellechea-full-") as td:
        work = Path(td)
        for idx, source_text in enumerate(embedded):
            pdf_page = idx + 1
            heading_type, heading_match = detect_major_heading(source_text)
            if heading_type and (heading_type != current_section or pdf_page == 1):
                section_counter += 1
                current_section = heading_type
                current_section_id = f"T1826-SEC-{section_counter:03d}"
                transitions.append(
                    {
                        "section_id": current_section_id,
                        "section_type": heading_type,
                        "pdf_page": pdf_page,
                        "printed_page": printed_number(source_text),
                        "heading_match_normalized": heading_match,
                        "status": "machine_candidate",
                    }
                )

            chapter = detect_chapter_heading(source_text)
            if chapter:
                chapter_pages.append({"pdf_page": pdf_page, "heading_normalized": chapter})

            visual_text = ""
            fallback_activity = None
            # The PDF contains a substantial embedded source-text layer. Independent visual
            # OCR is therefore used only where that layer is missing/sparse; representative
            # visual anchors are separately exercised by the minimal pilot.
            if len(source_text) < 80:
                try:
                    visual_text = render_and_ocr(pdf_page, work)
                except subprocess.CalledProcessError as exc:
                    visual_text = ""
                fallback_activity = f"RHD-ACT-T1826-FULL-VIS-{pdf_page:03d}"
                fallback_pages.append(pdf_page)

            if not source_text and not visual_text:
                blank_pages.append(pdf_page)

            record_id = f"RHD-T1826-{10000 + pdf_page:05d}"
            diplomatic = None
            if fallback_activity:
                diplomatic = layer(
                    visual_text,
                    "machine_visual_ocr_unadjudicated" if visual_text else "machine_visual_blank_or_nontextual_observation",
                    "tesseract_5_spa_from_150dpi_facsimile_fallback",
                    fallback_activity,
                    "medium" if visual_text else "low",
                )

            record = {
                "record_id": record_id,
                "source_id": SOURCE_ID,
                "witness_id": WITNESS_ID,
                "direction": None,
                "status": "active",
                "locators": {
                    "printed_page": printed_number(source_text),
                    "digital_page": pdf_page,
                    "column": None,
                    "region": None,
                    "iiif_canvas": None,
                    "iiif_target": None,
                    "ocr_line_start": None,
                    "ocr_line_end": None,
                },
                "layers": {
                    "ocr_raw": layer(
                        source_text,
                        "source_embedded_text_preserved" if source_text else "source_embedded_text_empty",
                        "pypdf_embedded_text_extraction",
                        f"RHD-ACT-T1826-FULL-EMBED-{pdf_page:03d}",
                        "unknown",
                    ),
                    "segmentation": {
                        "method": "pdf_page_boundary_plus_conservative_major_heading_state",
                        "score": None,
                        "confidence": "high",
                        "decision": "accepted",
                        "decision_event_id": f"RHD-ACT-T1826-FULL-SEG-{pdf_page:03d}",
                    },
                    "diplomatic": diplomatic,
                    "critical": None,
                    "normalized": None,
                },
                "lexical": None,
                "validation": [
                    {
                        "event_id": f"RHD-VAL-T1826-FULL-{pdf_page:03d}",
                        "scope": "documentary",
                        "decision": "machine_documentary_page_traversal_without_human_adjudication",
                        "reviewer_type": "machine",
                        "agent_id": "rhd-tellechea-full-pilot",
                        "date": None,
                        "evidence": [WITNESS_ID, f"PDF:{pdf_page}"],
                        "justification": "Page represented from checksum-fixed witness; source extraction is preserved and sparse pages receive separate visual OCR fallback.",
                        "confidence": "high" if source_text else "medium" if visual_text else "low",
                    }
                ],
                "historical_relations": [],
                "provenance": extraction_provenance(record_id, pdf_page, fallback_activity),
                "notes": [
                    {
                        "type": "document_section",
                        "text": json.dumps(
                            {
                                "section_id": current_section_id,
                                "section_type": current_section,
                                "major_heading_detected_here": heading_type,
                                "chapter_heading_candidate": chapter,
                            },
                            ensure_ascii=False,
                            sort_keys=True,
                        ),
                        "status": "machine_candidate",
                        "responsibility": "machine",
                    }
                ],
            }
            records.append(record)

    JSONL.write_text(
        "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in records),
        encoding="utf-8",
    )

    # Documentary TEI grouped by the machine-detected section state.
    tei = ET.Element(q("TEI"))
    header = ET.SubElement(tei, q("teiHeader"))
    file_desc = ET.SubElement(header, q("fileDesc"))
    title_stmt = ET.SubElement(file_desc, q("titleStmt"))
    ET.SubElement(title_stmt, q("title")).text = "Tellechea 1826 — RHD full-witness machine-only industrialization pilot"
    pub_stmt = ET.SubElement(file_desc, q("publicationStmt"))
    ET.SubElement(pub_stmt, q("p")).text = "Machine-only derived pilot; no human validation claimed."
    source_desc = ET.SubElement(file_desc, q("sourceDesc"))
    ET.SubElement(source_desc, q("p")).text = (
        f"Checksum-fixed witness {WITNESS_ID}; SHA-256 {EXPECTED_SHA256}; {EXPECTED_PAGES} PDF pages."
    )
    text_el = ET.SubElement(tei, q("text"))
    body = ET.SubElement(text_el, q("body"))

    section_div = None
    last_section = None
    for record in records:
        note_data = json.loads(record["notes"][0]["text"])
        section_id = note_data["section_id"]
        if section_id != last_section:
            section_div = ET.SubElement(
                body,
                q("div"),
                {"type": "source-section", "subtype": note_data["section_type"], "n": section_id},
            )
            last_section = section_id
        unit = ET.SubElement(
            section_div,
            q("div"),
            {"type": "documentary-unit", f"{{{XML_NS}}}id": record["record_id"]},
        )
        loc = record["locators"]
        pb_attrs = {"n": str(loc["digital_page"])}
        if loc["printed_page"] is not None:
            pb_attrs["facs"] = f"printed:{loc['printed_page']}"
        ET.SubElement(unit, q("pb"), pb_attrs)
        ET.SubElement(unit, q("ab"), {"type": "source-embedded-text"}).text = record["layers"]["ocr_raw"]["text"]
        diplomatic = record["layers"].get("diplomatic")
        if diplomatic is not None:
            ET.SubElement(unit, q("ab"), {"type": "machine-visual-ocr-fallback"}).text = diplomatic.get("text") or ""
        if not record["layers"]["ocr_raw"]["text"] and not (diplomatic or {}).get("text"):
            ET.SubElement(unit, q("gap"), {"reason": "blank-or-nontextual-machine-observation", "unit": "page"})

    ET.indent(tei, space="  ")
    ET.ElementTree(tei).write(TEI, encoding="utf-8", xml_declaration=True)

    diagnostics = {
        "pilot_id": "RHD-TELLECHEA-1826-FULL-WITNESS-PILOT-1",
        "source_id": SOURCE_ID,
        "witness_id": WITNESS_ID,
        "witness_sha256": digest,
        "pdf_pages": EXPECTED_PAGES,
        "canonical_records": len(records),
        "embedded_text_pages": sum(1 for t in embedded if t),
        "embedded_text_characters": sum(len(t) for t in embedded),
        "visual_ocr_fallback_pages": fallback_pages,
        "visual_ocr_fallback_count": len(fallback_pages),
        "blank_or_nontextual_pages_after_fallback": blank_pages,
        "major_section_transitions": transitions,
        "chapter_heading_candidates": chapter_pages,
        "minimal_visual_anchor_pages": [32, 75],
        "grammar_anchor": {"pdf_page": 32, "printed_page": 6},
        "parallel_layout_anchor": {"pdf_page": 75, "printed_page": 49},
        "rhd_core_changes_required": [],
        "source_specific_rules_location": "source_profile_or_adapter_only",
        "lex0_entries_generated": 0,
        "human_validation_claimed": False,
        "scope": "complete 205-page documentary traversal for RHD industrialization; not a human-adjudicated critical edition",
    }
    DIAG.write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(
        "RHD_TELLECHEA_FULL_PILOT="
        + json.dumps(
            {
                "records": len(records),
                "embedded_text_pages": diagnostics["embedded_text_pages"],
                "visual_fallback_pages": len(fallback_pages),
                "blank_pages": len(blank_pages),
                "major_sections": len(transitions),
                "rhd_core_changes_required": 0,
                "human_validation_claimed": False,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
