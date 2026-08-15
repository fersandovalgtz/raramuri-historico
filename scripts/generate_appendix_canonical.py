#!/usr/bin/env python3
"""Generate canonical RHD appendix objects for Steffel under the machine-only policy.

The canonical appendix layer joins:
- OCR-structured numeration material;
- 22 OCR-structured trilingual formula blocks;
- AI visual formula-level Latin/German/Tarahumara alignment;
- the separate Lord's Prayer block;
- AI-visual facsimile page mapping (PDF 79–84 ↔ printed 369–374).

It never claims human verification. Formula alignment is explicitly AI-assisted and may
carry field-level uncertainty while the facsimile remains the documentary authority.
"""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "data" / "appendices"
NUM = APP / "numeration_ocr_candidates.json"
SAMPLE = APP / "trilingual_sample_ocr_candidates.json"
ALIGN = APP / "trilingual_visual_alignment_ai.json"
PAGE_MAP = APP / "facsimile_page_map.json"
OUT_DIR = ROOT / "data" / "canonical"
OUT = OUT_DIR / "steffel-1809.appendices.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def page_index(page_map):
    return {x["printed_page"]: x for x in page_map["mapping"]}


def main():
    num = load(NUM)
    sample = load(SAMPLE)
    alignment = load(ALIGN)
    facs = load(PAGE_MAP)
    pmap = page_index(facs)
    aligned = {x["formula"]: x for x in alignment.get("formulas", [])}

    numeration = {
        "object_id": "RHD-S1809-APP-NUMERATION",
        "object_type": "appendix_numeration",
        "source": "Steffel 1809",
        "printed_pages": [369, 370],
        "pdf_pages": [pmap[369]["pdf_page"], pmap[370]["pdf_page"]],
        "title_source_ocr": num.get("title_ocr"),
        "layers": {
            "ocr": {
                "status": "source_ocr",
                "text": num.get("source_block", {}).get("ocr_text", ""),
                "source_ocr_line_start": num.get("source_block", {}).get("source_ocr_line_start"),
                "source_ocr_line_end": num.get("source_block", {}).get("source_ocr_line_end"),
            },
            "visual_collation": {
                "status": "confirmed_ai_assisted",
                "method": "ai_visual_collation",
                "human_verified": False,
                "evidence": [
                    {"printed_page": 369, "pdf_page": pmap[369]["pdf_page"]},
                    {"printed_page": 370, "pdf_page": pmap[370]["pdf_page"]},
                ],
                "claim": "Appendix heading and two-page counting-system section boundaries confirmed visually; individual readings remain OCR/AI candidates unless separately transcribed.",
            },
        },
        "numbered_expression_candidates": num.get("numbered_expression_candidates", []),
        "normalization_performed": False,
        "linguistic_analysis_performed": False,
        "human_verified": False,
    }

    formula_page = {}
    for i in range(1, 23):
        formula_page[i] = 371 if i <= 4 else 372 if i <= 11 else 373 if i <= 18 else 374

    formulas = []
    for src in sample.get("formulas", []):
        n = src["formula_number_editorial"]
        printed = formula_page[n]
        visual = aligned[n]
        formulas.append(
            {
                "object_id": src["record_id"],
                "object_type": "parallel_formula",
                "sequence": n,
                "source": "Steffel 1809",
                "printed_page": printed,
                "pdf_page": pmap[printed]["pdf_page"],
                "expected_languages": ["la", "de", "und"],
                "machine_alignment_complete": True,
                "human_alignment_verified": False,
                "layers": {
                    "ocr": {
                        "status": "ocr_structured_candidate",
                        "text": src.get("ocr_text", ""),
                        "retrieval_anchor": src.get("retrieval_anchor"),
                        "source_ocr_line_start": src.get("source_ocr_line_start"),
                        "source_ocr_line_end": src.get("source_ocr_line_end"),
                    },
                    "visual_collation": {
                        "status": "confirmed_ai_assisted",
                        "method": "ai_visual_collation",
                        "human_verified": False,
                        "claim": f"Printed formula number {n} is present in the facsimile sequence on p. {printed}.",
                    },
                    "parallel_alignment": {
                        "status": "aligned_ai_assisted",
                        "method": "ai_visual_transcription_and_formula_alignment",
                        "line_breaks_normalized": True,
                        "human_verified": False,
                        "texts": {
                            "la": visual["latin"],
                            "de": visual["german"],
                            "und": visual["tarahumara"],
                        },
                        "confidence": visual.get("confidence", {}),
                        "uncertain_segments": visual.get("uncertain_segments", []),
                    },
                },
                "human_verified": False,
            }
        )

    prayer_src = sample.get("lord_prayer", {})
    prayer = {
        "object_id": "RHD-S1809-PRAYER-01",
        "object_type": "prayer_text",
        "source": "Steffel 1809",
        "title_source_ocr": prayer_src.get("title_ocr"),
        "printed_page": 374,
        "pdf_page": pmap[374]["pdf_page"],
        "language": "und",
        "layers": {
            "ocr": {
                "status": "ocr_structured_candidate",
                "text": prayer_src.get("ocr_text", ""),
                "source_ocr_line_start": prayer_src.get("source_ocr_line_start"),
                "source_ocr_line_end": prayer_src.get("source_ocr_line_end"),
            },
            "visual_collation": {
                "status": "confirmed_ai_assisted",
                "method": "ai_visual_collation",
                "human_verified": False,
                "claim": "Separate heading 'Das Gebet des Herrn' and following Tarahumara prayer block confirmed visually after formula 22 on printed p. 374.",
            },
        },
        "human_verified": False,
    }

    payload = {
        "schema_id": "RHD-APPENDIX-CANONICAL-1.0",
        "source_profile": "steffel-1809",
        "edition_scope": "machine-only scholarly edition",
        "human_validation_claimed": False,
        "facsimile_mapping": {
            "method": facs.get("verification_method"),
            "mapping": facs.get("mapping"),
        },
        "objects": [numeration, *formulas, prayer],
        "counts": {
            "objects": 24,
            "numeration_sections": 1,
            "parallel_formulas": 22,
            "machine_aligned_parallel_formulas": 22,
            "prayer_texts": 1,
        },
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"generated canonical appendix layer with {len(payload['objects'])} objects and 22 AI-aligned formula triples -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
