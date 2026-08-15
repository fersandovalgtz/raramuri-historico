#!/usr/bin/env python3
"""Structure Steffel appendices from preserved OCR without claiming facsimile validation.

Outputs:
- numeration OCR section plus mechanically detected numbered expressions;
- 22 trilingual-language-sample OCR blocks using stable content anchors;
- the Lord's Prayer as a separate OCR documentary block.

All records remain `ocr_structured_candidate`, `human_verified=false` and
`facsimile_verified=false` until an independent image-based collation is performed.
"""

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OCR = ROOT / "sources" / "steffel-1809-ocr-source.txt"
OUT_DIR = ROOT / "data" / "appendices"
NUM_OUT = OUT_DIR / "numeration_ocr_candidates.json"
SAMPLE_OUT = OUT_DIR / "trilingual_sample_ocr_candidates.json"

NUM_START = "J. Von der tarahumariſchen Art zu zaͤhlen."
SAMPLE_START = "Ccrahumariſche Sprachbrobe."
PRAYER_START = "Das Gebet des Herrn."

FORMULA_ANCHORS = [
    "Deus non moritur",
    "liberos ſuos",
    "Hec ink erat",
    "Infans non vult",
    "Hæe. puella",
    "Hi quatuor",
    "Hie vir",
    "Frater tuus",
    "Neifus eft",
    "Habemus duos",
    "In capite",
    "Lingua et dentes",
    "Dextrum brachium",
    "Pilus elt longus",
    "Pifeis habet",
    "En avis tarde",
    "Folia arboris",
    "Ignis ardet",
    "Unda in fluvio",
    "Luna major",
    "Heri veſperi",
    "Nox obſcura",
]


def locate(lines, needle, start=0):
    for i in range(start, len(lines)):
        if needle in lines[i]:
            return i
    raise ValueError(f"anchor not found: {needle}")


def source_block(lines, start, end):
    return {
        "source_ocr_line_start": start + 1,
        "source_ocr_line_end": end,
        "ocr_text": "\n".join(lines[start:end]).strip(),
    }


def main():
    lines = OCR.read_text(encoding="utf-8").splitlines()
    num_start = locate(lines, NUM_START)
    sample_start = locate(lines, SAMPLE_START, num_start)
    prayer_start = locate(lines, PRAYER_START, sample_start)

    numeration_lines = lines[num_start:sample_start]
    numeric_candidates = []
    # Deliberately broad OCR-level retrieval. It finds surface number labels but
    # does not normalize or linguistically analyze the historical expressions.
    number_re = re.compile(r"^\s*(\d{1,4})[\.\s]+(.+?)\s*$")
    for offset, line in enumerate(numeration_lines):
        match = number_re.match(line)
        if not match:
            continue
        numeric_candidates.append(
            {
                "candidate_id": f"RHD-S1809-NUMOCR-{len(numeric_candidates)+1:04d}",
                "numeric_label_ocr": match.group(1),
                "expression_ocr": match.group(2),
                "source_ocr_line": num_start + offset + 1,
                "status": "ocr_structured_candidate",
                "facsimile_verified": False,
                "human_verified": False,
            }
        )

    numeration = {
        "collection_id": "RHD-S1809-APP-NUMERATION",
        "source": "Steffel 1809",
        "title_ocr": NUM_START,
        "expected_printed_section_start": 369,
        "status": "ocr_structured_candidate",
        "facsimile_verified": False,
        "human_verified": False,
        "normalization_performed": False,
        "linguistic_analysis_performed": False,
        "source_block": source_block(lines, num_start, sample_start),
        "numbered_expression_candidates": numeric_candidates,
        "editorial_note": "OCR-level structural inventory only. Historical number forms and counting systems require direct facsimile collation before diplomatic or analytical promotion.",
    }

    formula_positions = []
    cursor = sample_start
    for number, anchor in enumerate(FORMULA_ANCHORS, 1):
        pos = locate(lines, anchor, cursor)
        formula_positions.append((number, anchor, pos))
        cursor = pos + 1

    formulas = []
    for index, (number, anchor, start) in enumerate(formula_positions):
        end = formula_positions[index + 1][2] if index + 1 < len(formula_positions) else prayer_start
        block = source_block(lines, start, end)
        formulas.append(
            {
                "record_id": f"RHD-S1809-SAMPLE-{number:02d}",
                "formula_number_editorial": number,
                "retrieval_anchor": anchor,
                "status": "ocr_structured_candidate",
                "expected_languages": ["la", "de", "und"],
                "language_alignment_verified": False,
                "facsimile_verified": False,
                "human_verified": False,
                **block,
            }
        )

    prayer = {
        "record_id": "RHD-S1809-PRAYER-01",
        "title_ocr": PRAYER_START,
        "status": "ocr_structured_candidate",
        "language": "und",
        "facsimile_verified": False,
        "human_verified": False,
        **source_block(lines, prayer_start, len(lines)),
    }

    sample = {
        "collection_id": "RHD-S1809-APP-TRILINGUAL-SAMPLE",
        "source": "Steffel 1809",
        "title_ocr": SAMPLE_START,
        "expected_printed_page_start": 371,
        "expected_printed_page_end": 374,
        "status": "ocr_structured_candidate",
        "facsimile_verified": False,
        "human_verified": False,
        "formula_count": len(formulas),
        "formula_numbering_source": "editorial reconstruction from printed/OCR sequence; OCR visibly corrupts or omits several numeric labels",
        "formulas": formulas,
        "lord_prayer": prayer,
        "editorial_note": "The 22 formula blocks are segmented by stable Latin/OCR anchors but are not yet language-line parsed or diplomatically collated. The Lord's Prayer is preserved separately because it follows formula 22 outside the numbered series.",
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NUM_OUT.write_text(json.dumps(numeration, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    SAMPLE_OUT.write_text(json.dumps(sample, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"generated appendix OCR candidates: {len(numeric_candidates)} numbered-expression lines, "
        f"{len(formulas)} trilingual formula blocks, 1 separate Lord's Prayer block"
    )


if __name__ == "__main__":
    main()
