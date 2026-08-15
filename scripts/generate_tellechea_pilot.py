#!/usr/bin/env python3
"""Generate a minimal end-to-end RHD pilot from checksum-fixed Tellechea 1826.

The pilot deliberately exercises two non-lexicographic documentary forms:
1) a grammar page anchored by LIBRO PRIMERO / CAPITULO I;
2) printed page 49, the beginning of the long parallel-material range used as a layout
   stress test.

Embedded PDF text is preserved as a source extraction. A separate visual OCR reading is
produced from rendered page images with Tesseract. Neither layer is human-verified and
neither is silently promoted to linguistic/semantic equivalence.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

from PIL import Image
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/tellechea-1826-dgb.pdf")
OUT_DIR = ROOT / "data/pilot"
JSONL = OUT_DIR / "tellechea-1826.minimal-pilot.jsonl"
TEI = OUT_DIR / "tellechea-1826.minimal-pilot.tei.xml"
DIAG = OUT_DIR / "tellechea-1826.minimal-pilot.diagnostics.json"
EXPECTED_SHA256 = "c67b7942090613c494d8057be8aff59ea13a11519c29eae469afad8a85c30dfc"
WITNESS_ID = "RHD-WIT-TELLECHEA-1826-DGB"
SOURCE_ID = "RHD-SRC-TELLECHEA-1826"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def norm(text: str) -> str:
    text = text.lower()
    text = text.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    return re.sub(r"[^a-z0-9]+", " ", text)


def printed_number(text: str):
    # Historical body pages commonly begin with a parenthesized printed page number.
    head = (text or "")[:250]
    m = re.search(r"\(\s*([0-9]{1,3})\s*\)", head)
    return int(m.group(1)) if m else None


def render_page(pdf_page_1based: int, stem: str) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    prefix = OUT_DIR / stem
    subprocess.run(
        ["pdftoppm", "-f", str(pdf_page_1based), "-singlefile", "-r", "220", "-png", str(PDF), str(prefix)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    path = prefix.with_suffix(".png")
    if not path.exists():
        raise SystemExit(f"ERROR: rendered page missing: {path}")
    return path


def tesseract(image: Path, psm: int = 6) -> str:
    proc = subprocess.run(
        ["tesseract", str(image), "stdout", "-l", "spa", "--psm", str(psm)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return proc.stdout.strip()


def split_columns(image: Path, stem: str):
    with Image.open(image) as im:
        w, h = im.size
        top = int(h * 0.04)
        bottom = int(h * 0.97)
        margin = int(w * 0.035)
        gutter = int(w * 0.015)
        mid = w // 2
        left = im.crop((margin, top, mid - gutter, bottom))
        right = im.crop((mid + gutter, top, w - margin, bottom))
        left_path = OUT_DIR / f"{stem}-left.png"
        right_path = OUT_DIR / f"{stem}-right.png"
        left.save(left_path)
        right.save(right_path)
    return left_path, right_path


def spanish_score(text: str) -> int:
    words = re.findall(r"[a-záéíóúñ]+", text.lower())
    common = {"de", "la", "el", "que", "y", "en", "los", "las", "del", "para", "por", "con", "una", "un", "se", "su", "no", "es", "como", "al"}
    return sum(1 for w in words if w in common)


def similarity(a: str, b: str) -> float:
    # Token-set overlap is used only as a documentary agreement diagnostic.
    aa = set(re.findall(r"[a-záéíóúñ]+", a.lower()))
    bb = set(re.findall(r"[a-záéíóúñ]+", b.lower()))
    if not aa or not bb:
        return 0.0
    return round(len(aa & bb) / len(aa | bb), 4)


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


def provenance(record_id: str, embedded_activity: str, visual_activity: str):
    return [
        {
            "activity_id": embedded_activity,
            "activity_type": "embedded_text_extraction",
            "generated_entity": f"{record_id}#ocr_raw",
            "used_entities": [WITNESS_ID],
            "agent_id": "pypdf",
            "agent_type": "software",
            "method": "extract_text from checksum-fixed PDF",
            "timestamp": None,
            "software_version": None,
        },
        {
            "activity_id": visual_activity,
            "activity_type": "machine_visual_ocr",
            "generated_entity": f"{record_id}#diplomatic",
            "used_entities": [WITNESS_ID],
            "agent_id": "tesseract-spa",
            "agent_type": "software",
            "method": "220dpi facsimile render followed by Tesseract OCR; unadjudicated",
            "timestamp": None,
            "software_version": None,
        },
    ]


def main():
    if not PDF.exists():
        raise SystemExit(f"ERROR: checksum-fixed Tellechea PDF not found: {PDF}")
    digest = sha256(PDF)
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"ERROR: refusing non-pinned Tellechea binary: {digest}")

    reader = PdfReader(str(PDF), strict=False)
    texts = []
    for page in reader.pages:
        try:
            texts.append(page.extract_text() or "")
        except Exception:
            texts.append("")

    grammar_index = None
    for i, text in enumerate(texts):
        n = norm(text)
        if "libro primero" in n and "del nombre" in n and "cap" in n:
            grammar_index = i
            break
    if grammar_index is None:
        raise SystemExit("ERROR: could not deterministically locate LIBRO PRIMERO grammar anchor")
    grammar_printed = printed_number(texts[grammar_index])
    if grammar_printed is None:
        raise SystemExit("ERROR: grammar anchor lacks recoverable printed page number")

    parallel_index = None
    for i, text in enumerate(texts):
        if printed_number(text) == 49 and i > grammar_index:
            parallel_index = i
            break
    if parallel_index is None:
        raise SystemExit("ERROR: could not locate printed page 49 for parallel-layout pilot")

    units = []
    diagnostics = {
        "pilot_id": "RHD-TELLECHEA-1826-MINIMAL-PILOT-1",
        "witness_sha256": digest,
        "human_validation_claimed": False,
        "end_to_end_scope": "one grammar page plus one printed-page-49 parallel-layout page",
        "records": [],
    }

    # Unit 1: grammar page, full-page visual OCR.
    g_pdf_page = grammar_index + 1
    g_img = render_page(g_pdf_page, "tellechea-grammar-anchor")
    g_visual = tesseract(g_img, 6)
    g_embedded = texts[grammar_index].strip()
    g_id = "RHD-T1826-00001"
    units.append({
        "record_id": g_id,
        "source_id": SOURCE_ID,
        "witness_id": WITNESS_ID,
        "direction": None,
        "status": "active",
        "locators": {
            "printed_page": grammar_printed,
            "digital_page": g_pdf_page,
            "column": None,
            "region": None,
            "iiif_canvas": None,
            "iiif_target": None,
            "ocr_line_start": None,
            "ocr_line_end": None,
        },
        "layers": {
            "ocr_raw": layer(g_embedded, "source_embedded_text_preserved", "pypdf_embedded_text_extraction", "RHD-ACT-T1826-EMBED-00001", "unknown"),
            "segmentation": {
                "method": "deterministic_heading_anchor_libro_primero_capitulo_i",
                "score": None,
                "confidence": "high",
                "decision": "accepted",
                "decision_event_id": "RHD-ACT-T1826-SEG-00001",
            },
            "diplomatic": layer(g_visual, "machine_visual_ocr_unadjudicated", "tesseract_5_spa_from_220dpi_facsimile", "RHD-ACT-T1826-VIS-00001", "medium"),
            "critical": None,
            "normalized": None,
        },
        "lexical": None,
        "validation": [{
            "event_id": "RHD-VAL-T1826-00001",
            "scope": "philological",
            "decision": "machine_visual_ocr_generated_without_human_adjudication",
            "reviewer_type": "machine",
            "agent_id": "tesseract-spa",
            "date": None,
            "evidence": [WITNESS_ID, f"PDF:{g_pdf_page}", f"printed:{grammar_printed}"],
            "justification": "Independent visual OCR layer retained separately from embedded PDF text.",
            "confidence": "medium",
        }],
        "historical_relations": [],
        "provenance": provenance(g_id, "RHD-ACT-T1826-EMBED-00001", "RHD-ACT-T1826-VIS-00001"),
        "notes": [{
            "type": "document_genre",
            "text": "grammar_page: LIBRO PRIMERO / CAPITULO I anchor",
            "status": "machine_identified",
            "responsibility": "machine",
        }],
    })
    diagnostics["records"].append({
        "record_id": g_id,
        "pdf_page": g_pdf_page,
        "printed_page": grammar_printed,
        "embedded_chars": len(g_embedded),
        "visual_ocr_chars": len(g_visual),
        "token_jaccard": similarity(g_embedded, g_visual),
        "selection": "heading_anchor",
    })

    # Unit 2: printed page 49, column-aware visual OCR.
    p_pdf_page = parallel_index + 1
    p_img = render_page(p_pdf_page, "tellechea-parallel-p49")
    left_img, right_img = split_columns(p_img, "tellechea-parallel-p49")
    left_text = tesseract(left_img, 6)
    right_text = tesseract(right_img, 6)
    left_score = spanish_score(left_text)
    right_score = spanish_score(right_text)
    if left_score >= right_score * 1.35 and left_score >= 5:
        assignment = {"left": "es_candidate", "right": "und_candidate", "status": "machine_candidate"}
    elif right_score >= left_score * 1.35 and right_score >= 5:
        assignment = {"left": "und_candidate", "right": "es_candidate", "status": "machine_candidate"}
    else:
        assignment = {"left": "undetermined", "right": "undetermined", "status": "unresolved"}
    p_visual = "[COLUMN_LEFT]\n" + left_text + "\n\n[COLUMN_RIGHT]\n" + right_text
    p_embedded = texts[parallel_index].strip()
    p_id = "RHD-T1826-00002"
    units.append({
        "record_id": p_id,
        "source_id": SOURCE_ID,
        "witness_id": WITNESS_ID,
        "direction": None,
        "status": "active",
        "locators": {
            "printed_page": 49,
            "digital_page": p_pdf_page,
            "column": "two-column-layout-candidate",
            "region": None,
            "iiif_canvas": None,
            "iiif_target": None,
            "ocr_line_start": None,
            "ocr_line_end": None,
        },
        "layers": {
            "ocr_raw": layer(p_embedded, "source_embedded_text_preserved", "pypdf_embedded_text_extraction", "RHD-ACT-T1826-EMBED-00002", "unknown"),
            "segmentation": {
                "method": "printed_page_49_anchor_then_geometric_two_column_split",
                "score": None,
                "confidence": "medium",
                "decision": "accepted",
                "decision_event_id": "RHD-ACT-T1826-SEG-00002",
            },
            "diplomatic": layer(p_visual, "machine_visual_ocr_unadjudicated", "tesseract_5_spa_two_column_from_220dpi_facsimile", "RHD-ACT-T1826-VIS-00002", "medium"),
            "critical": None,
            "normalized": None,
        },
        "lexical": None,
        "validation": [{
            "event_id": "RHD-VAL-T1826-00002",
            "scope": "philological",
            "decision": "two_column_machine_visual_ocr_with_nonadjudicative_language_assignment",
            "reviewer_type": "machine",
            "agent_id": "tesseract-spa",
            "date": None,
            "evidence": [WITNESS_ID, f"PDF:{p_pdf_page}", "printed:49"],
            "justification": "Columns are geometrically separated. Language labels, when assigned, are machine candidates based only on conservative Spanish-function-word counts.",
            "confidence": "medium" if assignment["status"] == "machine_candidate" else "low",
        }],
        "historical_relations": [],
        "provenance": provenance(p_id, "RHD-ACT-T1826-EMBED-00002", "RHD-ACT-T1826-VIS-00002"),
        "notes": [
            {
                "type": "document_genre",
                "text": "parallel_layout_pilot_page",
                "status": "machine_candidate",
                "responsibility": "machine",
            },
            {
                "type": "column_language_assignment",
                "text": json.dumps(assignment, ensure_ascii=False, sort_keys=True),
                "status": assignment["status"],
                "responsibility": "machine",
            },
        ],
    })
    diagnostics["records"].append({
        "record_id": p_id,
        "pdf_page": p_pdf_page,
        "printed_page": 49,
        "embedded_chars": len(p_embedded),
        "visual_ocr_chars": len(p_visual),
        "token_jaccard": similarity(p_embedded, p_visual),
        "left_spanish_score": left_score,
        "right_spanish_score": right_score,
        "column_assignment": assignment,
        "selection": "printed_page_anchor",
    })

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    JSONL.write_text("\n".join(json.dumps(x, ensure_ascii=False, sort_keys=True) for x in units) + "\n", encoding="utf-8")
    DIAG.write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    ns = "http://www.tei-c.org/ns/1.0"
    ET.register_namespace("", ns)
    tei = ET.Element(f"{{{ns}}}TEI")
    header = ET.SubElement(tei, f"{{{ns}}}teiHeader")
    file_desc = ET.SubElement(header, f"{{{ns}}}fileDesc")
    title_stmt = ET.SubElement(file_desc, f"{{{ns}}}titleStmt")
    ET.SubElement(title_stmt, f"{{{ns}}}title").text = "RHD Tellechea 1826 minimal machine-only pilot"
    pub_stmt = ET.SubElement(file_desc, f"{{{ns}}}publicationStmt")
    ET.SubElement(pub_stmt, f"{{{ns}}}p").text = "Computational pilot; no human validation claimed."
    src_desc = ET.SubElement(file_desc, f"{{{ns}}}sourceDesc")
    ET.SubElement(src_desc, f"{{{ns}}}p").text = f"Checksum-fixed witness {WITNESS_ID}; SHA-256 {digest}."
    text_el = ET.SubElement(tei, f"{{{ns}}}text")
    body = ET.SubElement(text_el, f"{{{ns}}}body")
    for rec in units:
        div = ET.SubElement(body, f"{{{ns}}}div", {"type": "documentary-unit", "n": rec["record_id"]})
        ET.SubElement(div, f"{{{ns}}}pb", {"n": str(rec["locators"]["printed_page"]), "facs": f"pdf-page:{rec['locators']['digital_page']}"})
        ET.SubElement(div, f"{{{ns}}}note", {"type": "machine-status"}).text = rec["layers"]["diplomatic"]["status"]
        ET.SubElement(div, f"{{{ns}}}ab", {"type": "embedded-source-text"}).text = rec["layers"]["ocr_raw"]["text"]
        ET.SubElement(div, f"{{{ns}}}ab", {"type": "machine-visual-ocr"}).text = rec["layers"]["diplomatic"]["text"]
        if rec["record_id"] == p_id:
            ET.SubElement(div, f"{{{ns}}}note", {"type": "column-language-assignment"}).text = json.dumps(assignment, ensure_ascii=False, sort_keys=True)
    ET.ElementTree(tei).write(TEI, encoding="utf-8", xml_declaration=True)

    # Rendered PNG intermediates are evidence-generating scratch products, not committed pilot data.
    for png in OUT_DIR.glob("tellechea-*.png"):
        png.unlink()

    print(f"generated Tellechea minimal pilot: {len(units)} canonical documentary records -> {JSONL.relative_to(ROOT)}, {TEI.relative_to(ROOT)}")
    print("RHD_TELLECHEA_PILOT=" + json.dumps(diagnostics, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
