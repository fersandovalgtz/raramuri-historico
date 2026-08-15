#!/usr/bin/env python3
"""Create a terminal uncertainty register for Steffel appendices.

Machine-only completion does not require forcing every historical glyph into a single
reading. This register inventories every medium/low-confidence appendix reading and
every explicit uncertain segment, then freezes it as a traceable terminal uncertainty.
No item is silently corrected, normalized or promoted to human verification.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
TRI = ROOT / "data/appendices/trilingual_visual_alignment_ai.json"
NUM = ROOT / "data/appendices/numeration_visual_structure_ai.json"
PRAYER = ROOT / "data/appendices/prayer_visual_transcription_ai.json"
OUT = ROOT / "data/appendices/terminal_uncertainty_register.json"


def add(items, source_layer, locator, reading, confidence, note=None):
    items.append({
        "uncertainty_id": f"RHD-S1809-APP-UNC-{len(items)+1:04d}",
        "source_layer": source_layer,
        "locator": locator,
        "reading": reading,
        "confidence": confidence,
        "uncertainty_note": note,
        "terminal_status": "explicit_machine_uncertainty",
        "resolution_required_for_machine_only_completion": False,
        "human_review_required": False,
        "normalization_or_repair_performed": False,
    })


def main():
    tri = json.loads(TRI.read_text(encoding="utf-8"))
    num = json.loads(NUM.read_text(encoding="utf-8"))
    prayer = json.loads(PRAYER.read_text(encoding="utf-8"))
    items = []

    for formula in tri.get("formulas", []):
        confidence = formula.get("confidence", {})
        for lang in ("la", "de", "und"):
            level = confidence.get(lang)
            if level in {"medium", "low"}:
                add(
                    items,
                    "trilingual_visual_alignment_ai",
                    {"formula": formula.get("formula"), "printed_page": formula.get("printed_page"), "pdf_page": formula.get("pdf_page"), "language": lang},
                    formula.get({"la":"latin", "de":"german", "und":"tarahumara"}[lang]),
                    level,
                    "; ".join(formula.get("uncertain_segments", [])) or None,
                )
        # Preserve explicit uncertainty notes even when a field-level confidence is high.
        if formula.get("uncertain_segments") and all(v == "high" for v in confidence.values()):
            add(items, "trilingual_visual_alignment_ai", {"formula": formula.get("formula"), "printed_page": formula.get("printed_page"), "pdf_page": formula.get("pdf_page"), "language": "mixed"}, None, "medium", "; ".join(formula.get("uncertain_segments", [])))

    collections = [
        "primary_cardinals", "secondary_counting_system_examples", "third_counting_system_examples",
        "fourth_counting_system_examples", "multiplicatives", "other_number_words", "ordinals"
    ]
    for collection in collections:
        for idx, obj in enumerate(num.get(collection, []), 1):
            level = obj.get("confidence")
            if level in {"medium", "low"}:
                locator = {"collection": collection, "index": idx}
                for key in ("value", "times", "ordinal"):
                    if key in obj: locator[key] = obj[key]
                add(items, "numeration_visual_structure_ai", locator, obj.get("form"), level, obj.get("uncertainty"))

    prayer_conf = prayer.get("confidence")
    if prayer_conf in {"medium", "low"}:
        add(
            items,
            "prayer_visual_transcription_ai",
            {"record_id": prayer.get("record_id"), "source": prayer.get("source")},
            prayer.get("text"),
            prayer_conf,
            "; ".join(prayer.get("uncertain_segments", [])) or prayer.get("epistemic_note"),
        )

    summary = {"high": 0, "medium": 0, "low": 0}
    for item in items:
        summary[item["confidence"]] = summary.get(item["confidence"], 0) + 1

    payload = {
        "register_id": "RHD-S1809-APPENDIX-TERMINAL-UNCERTAINTY-01",
        "scope": "machine_only_appendix_terminal_uncertainty",
        "policy": "Residual graphic ambiguity is preserved as evidence. Machine-only completion does not require speculative repair or a fabricated unique reading.",
        "human_review_required": False,
        "human_validation_claimed": False,
        "all_items_terminal": True,
        "summary": {"count": len(items), "by_confidence": summary},
        "items": items,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"registered {len(items)} appendix uncertainties as explicit terminal machine states -> {OUT.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
