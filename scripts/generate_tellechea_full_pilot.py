#!/usr/bin/env python3
"""Traverse all 205 pages of the checksum-fixed Tellechea witness through RHD.

The strong pilot is a documentary industrialization test, not a human-adjudicated
critical edition. Embedded PDF text is preserved as source evidence. Sparse pages get
an independent visual OCR fallback. All pages become stable RHD documentary units,
major section headings remain machine candidates, and the witness is exported to TEI
without creating Lex-0 entries or human-validation claims.
"""
from __future__ import annotations
from pathlib import Path
import hashlib, json, re, subprocess, sys, tempfile
import xml.etree.ElementTree as ET
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/tellechea-1826-dgb.pdf")
OUT = ROOT / "data/pilot"
JSONL = OUT / "tellechea-1826.full-witness.jsonl"
TEI = OUT / "tellechea-1826.full-witness.tei.xml"
DIAG = OUT / "tellechea-1826.full-witness.diagnostics.json"
SHA = "c67b7942090613c494d8057be8aff59ea13a11519c29eae469afad8a85c30dfc"
PAGES = 205
WIT = "RHD-WIT-TELLECHEA-1826-DGB"
SRC = "RHD-SRC-TELLECHEA-1826"
NS = "http://www.tei-c.org/ns/1.0"; XMLNS = "http://www.w3.org/XML/1998/namespace"
ET.register_namespace("", NS)
HEADINGS = [
    ("preface", ("prefacion", "prefacio")), ("book_1", ("libro primero",)),
    ("book_2", ("libro segundo",)), ("book_3", ("libro tercero",)),
    ("book_4", ("libro cuarto",)),
    ("doctrinal_material", ("doctrina christiana", "doctrina cristiana")),
    ("prayers_or_sacramental_material", ("oraciones", "sacramentos")),
]

def q(tag): return f"{{{NS}}}{tag}"
def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""): h.update(chunk)
    return h.hexdigest()
def norm(text):
    text = (text or "").lower().translate(str.maketrans("áéíóúü", "aeiouu"))
    return re.sub(r"[^a-z0-9]+", " ", text)
def printed(text):
    m = re.search(r"\(\s*([0-9]{1,3})\s*\)", (text or "")[:300])
    return int(m.group(1)) if m else None
def major_heading(text):
    head = norm((text or "")[:900])
    for typ, variants in HEADINGS:
        for variant in variants:
            if variant in head: return typ, variant
    return None, None
def chapter_heading(text):
    m = re.search(r"\bcap(?:itulo|itvlo|\.)?\s+([ivxlcdm0-9]+)\b", norm((text or "")[:700]))
    return m.group(0) if m else None

def visual_ocr(page, work):
    prefix = work / f"p{page:03d}"
    subprocess.run(["pdftoppm", "-f", str(page), "-singlefile", "-r", "150", "-gray", "-png", str(PDF), str(prefix)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    image = prefix.with_suffix(".png")
    proc = subprocess.run(["tesseract", str(image), "stdout", "-l", "spa", "--psm", "6"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    image.unlink(missing_ok=True)
    return proc.stdout.strip()

def text_layer(text, status, method, activity, confidence):
    return {"text": text, "headword": None, "status": status, "method": method, "activity_id": activity, "responsibility": "machine", "confidence": confidence, "derived_from": [WIT]}

def provenance(rid, page, fallback):
    items = [{"activity_id": f"RHD-ACT-T1826-FULL-EMBED-{page:03d}", "activity_type": "embedded_text_extraction", "generated_entity": f"{rid}#ocr_raw", "used_entities": [WIT], "agent_id": "pypdf", "agent_type": "software", "method": "extract_text from checksum-fixed PDF", "timestamp": None, "software_version": None}]
    if fallback:
        items.append({"activity_id": fallback, "activity_type": "machine_visual_ocr", "generated_entity": f"{rid}#diplomatic", "used_entities": [WIT], "agent_id": "tesseract-spa", "agent_type": "software", "method": "150dpi grayscale facsimile render plus Tesseract OCR fallback; unadjudicated", "timestamp": None, "software_version": None})
    else:
        items.append({"activity_id": f"RHD-ACT-T1826-FULL-PROJ-{page:03d}", "activity_type": "documentary_source_projection", "generated_entity": f"{rid}#diplomatic", "used_entities": [f"{rid}#ocr_raw", WIT], "agent_id": "rhd-tellechea-full-pilot", "agent_type": "software", "method": "non-visual documentary projection of embedded source extraction; explicitly not visual/human collation", "timestamp": None, "software_version": None})
    return items

def main():
    if not PDF.exists(): raise SystemExit(f"ERROR: missing checksum-fixed witness: {PDF}")
    sha = digest(PDF)
    if sha != SHA: raise SystemExit(f"ERROR: refusing non-pinned Tellechea binary: {sha}")
    reader = PdfReader(str(PDF), strict=False)
    if len(reader.pages) != PAGES: raise SystemExit(f"ERROR: expected {PAGES} pages, got {len(reader.pages)}")
    embedded = []
    for p in reader.pages:
        try: embedded.append((p.extract_text() or "").strip())
        except Exception: embedded.append("")

    OUT.mkdir(parents=True, exist_ok=True)
    records, transitions, chapters, fallbacks, blanks = [], [], [], [], []
    section_type, section_id, section_no = "front_matter", "T1826-SEC-001", 1
    with tempfile.TemporaryDirectory(prefix="rhd-t1826-full-") as td:
        work = Path(td)
        for i, source_text in enumerate(embedded):
            page = i + 1; head_type, head_match = major_heading(source_text)
            if head_type and head_type != section_type:
                section_no += 1; section_type = head_type; section_id = f"T1826-SEC-{section_no:03d}"
                transitions.append({"section_id": section_id, "section_type": head_type, "pdf_page": page, "printed_page": printed(source_text), "heading_match_normalized": head_match, "status": "machine_candidate"})
            chapter = chapter_heading(source_text)
            if chapter: chapters.append({"pdf_page": page, "heading_normalized": chapter})
            visual, fallback = "", None
            if len(source_text) < 80:
                fallback = f"RHD-ACT-T1826-FULL-VIS-{page:03d}"; fallbacks.append(page)
                try: visual = visual_ocr(page, work)
                except subprocess.CalledProcessError: visual = ""
            if not source_text and not visual: blanks.append(page)
            rid = f"RHD-T1826-{10000 + page:05d}"
            if fallback:
                diplomatic = text_layer(visual, "machine_visual_ocr_unadjudicated" if visual else "machine_visual_blank_or_nontextual_observation", "tesseract_5_spa_from_150dpi_facsimile_fallback", fallback, "medium" if visual else "low")
            else:
                diplomatic = text_layer(source_text, "machine_documentary_projection_unadjudicated", "source_embedded_text_documentary_projection_not_visual_transcription", f"RHD-ACT-T1826-FULL-PROJ-{page:03d}", "unknown")
            pp = printed(source_text)
            records.append({
                "record_id": rid, "source_id": SRC, "witness_id": WIT, "direction": None, "status": "active",
                "locators": {"printed_page": pp if pp is not None else "unpaginated", "digital_page": page, "column": None, "region": None, "iiif_canvas": None, "iiif_target": None, "ocr_line_start": None, "ocr_line_end": None},
                "layers": {
                    "ocr_raw": text_layer(source_text, "source_embedded_text_preserved" if source_text else "source_embedded_text_empty", "pypdf_embedded_text_extraction", f"RHD-ACT-T1826-FULL-EMBED-{page:03d}", "unknown"),
                    "segmentation": {"method": "pdf_page_boundary_plus_conservative_major_heading_state", "score": None, "confidence": "high", "decision": "accepted", "decision_event_id": f"RHD-ACT-T1826-FULL-SEG-{page:03d}"},
                    "diplomatic": diplomatic, "critical": None, "normalized": None,
                },
                "lexical": None,
                "validation": [{"event_id": f"RHD-VAL-T1826-FULL-{page:03d}", "scope": "philological", "decision": "machine_documentary_page_traversal_without_human_adjudication", "reviewer_type": "machine", "agent_id": "rhd-tellechea-full-pilot", "date": None, "evidence": [WIT, f"PDF:{page}"], "justification": "Complete-witness documentary traversal; embedded source evidence is preserved, with separate visual OCR only where sparse.", "confidence": "high" if source_text else "medium" if visual else "low"}],
                "historical_relations": [], "provenance": provenance(rid, page, fallback),
                "notes": [{"type": "document_section", "text": json.dumps({"section_id": section_id, "section_type": section_type, "major_heading_detected_here": head_type, "chapter_heading_candidate": chapter}, ensure_ascii=False, sort_keys=True), "status": "machine_candidate", "responsibility": "machine"}],
            })
    JSONL.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in records), encoding="utf-8")

    tei = ET.Element(q("TEI")); header = ET.SubElement(tei, q("teiHeader")); fd = ET.SubElement(header, q("fileDesc"))
    ts = ET.SubElement(fd, q("titleStmt")); ET.SubElement(ts, q("title")).text = "Tellechea 1826 — RHD full-witness machine-only industrialization pilot"
    ps = ET.SubElement(fd, q("publicationStmt")); ET.SubElement(ps, q("p")).text = "Machine-only derived pilot; no human validation claimed."
    sd = ET.SubElement(fd, q("sourceDesc")); ET.SubElement(sd, q("p")).text = f"Checksum-fixed witness {WIT}; SHA-256 {SHA}; {PAGES} PDF pages."
    body = ET.SubElement(ET.SubElement(tei, q("text")), q("body")); section_div = None; last_section = None
    for r in records:
        note = json.loads(r["notes"][0]["text"]); sid = note["section_id"]
        if sid != last_section:
            section_div = ET.SubElement(body, q("div"), {"type": "source-section", "subtype": note["section_type"], "n": sid}); last_section = sid
        unit = ET.SubElement(section_div, q("div"), {"type": "documentary-unit", f"{{{XMLNS}}}id": r["record_id"]})
        loc = r["locators"]; attrs = {"n": str(loc["digital_page"])}
        if loc["printed_page"] != "unpaginated": attrs["facs"] = f"printed:{loc['printed_page']}"
        ET.SubElement(unit, q("pb"), attrs)
        ET.SubElement(unit, q("ab"), {"type": "source-embedded-text"}).text = r["layers"]["ocr_raw"]["text"]
        dip = r["layers"]["diplomatic"]
        ET.SubElement(unit, q("ab"), {"type": "machine-visual-ocr-fallback" if "tesseract" in dip["method"] else "documentary-source-projection"}).text = dip["text"]
        if not r["layers"]["ocr_raw"]["text"] and not dip["text"]: ET.SubElement(unit, q("gap"), {"reason": "blank-or-nontextual-machine-observation", "unit": "page"})
    ET.indent(tei, space="  "); ET.ElementTree(tei).write(TEI, encoding="utf-8", xml_declaration=True)

    diagnostics = {"pilot_id": "RHD-TELLECHEA-1826-FULL-WITNESS-PILOT-1", "source_id": SRC, "witness_id": WIT, "witness_sha256": sha, "pdf_pages": PAGES, "canonical_records": len(records), "embedded_text_pages": sum(bool(t) for t in embedded), "embedded_text_characters": sum(map(len, embedded)), "visual_ocr_fallback_pages": fallbacks, "visual_ocr_fallback_count": len(fallbacks), "blank_or_nontextual_pages_after_fallback": blanks, "major_section_transitions": transitions, "chapter_heading_candidates": chapters, "minimal_visual_anchor_pages": [32, 75], "grammar_anchor": {"pdf_page": 32, "printed_page": 6}, "parallel_layout_anchor": {"pdf_page": 75, "printed_page": 49}, "rhd_core_changes_required": [], "source_specific_rules_location": "source_profile_or_adapter_only", "lex0_entries_generated": 0, "human_validation_claimed": False, "scope": "complete 205-page documentary traversal for RHD industrialization; not a human-adjudicated critical edition"}
    DIAG.write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("RHD_TELLECHEA_FULL_PILOT=" + json.dumps({"records": len(records), "embedded_text_pages": diagnostics["embedded_text_pages"], "visual_fallback_pages": len(fallbacks), "blank_pages": len(blanks), "major_sections": len(transitions), "rhd_core_changes_required": 0, "human_validation_claimed": False}, sort_keys=True))

if __name__ == "__main__": main()
