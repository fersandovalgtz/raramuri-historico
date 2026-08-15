#!/usr/bin/env python3
"""Generate a non-destructive RHD 1.0 canonical projection from Steffel 0.2.0.

This adapter deliberately preserves data/entries.csv as the operational master.
It does not adjudicate semantics, morphology, cognacy, or human validation.
"""

from __future__ import annotations

from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "entries.csv"
PROFILE_PATH = ROOT / "source_profiles" / "steffel-1809.source.json"
OUT_DIR = ROOT / "data" / "canonical"
OUT_JSONL = OUT_DIR / "steffel-1809.entries.jsonl"
OUT_SUMMARY = OUT_DIR / "steffel-1809.summary.json"


def text(value) -> str:
    return (value or "").strip()


def integer_or_none(value):
    value = text(value)
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return value


def float_or_none(value):
    value = text(value)
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def boolish(value) -> bool:
    return text(value).lower() in {"1", "true", "yes", "y"}


def canonical_status(row: dict[str, str]) -> str:
    status = text(row.get("status"))
    if status == "rejected_false_positive":
        return "rejected_boundary"
    if status in {
        "facsimile_checked_headword_ai_assisted",
        "diplomatic_transcription_ai_assisted",
    }:
        return "active"
    return "candidate"


def source_pointer(row: dict[str, str]) -> str:
    start = integer_or_none(row.get("source_ocr_line_start"))
    end = integer_or_none(row.get("source_ocr_line_end"))
    if start is None or end is None:
        return "sources/steffel-1809-ocr-source.txt"
    return f"sources/steffel-1809-ocr-source.txt#L{start}-L{end}"


def witness_pointer(profile: dict, row: dict[str, str]) -> str:
    witness_id = profile["witness"]["witness_id"]
    page = integer_or_none(row.get("printed_page"))
    column = text(row.get("facsimile_column"))
    suffix = f"#printed_page={page}" if page is not None else ""
    if column:
        suffix += f"&column={column}"
    return witness_id + suffix


def make_forms(row: dict[str, str]) -> list[dict]:
    forms = []
    diplomatic = text(row.get("headword_diplomatic"))
    raw = text(row.get("headword_raw"))
    search = text(row.get("headword_search"))

    lemma = diplomatic or raw
    if lemma:
        forms.append(
            {
                "form_id": f"{row['record_id']}-FORM-LEMMA",
                "type": "lemma",
                "orth": lemma,
                "language": None,
                "script": "Latn",
                "source_layer": "diplomatic" if diplomatic else "operational_headword_raw",
                "cert": None,
            }
        )

    if search and search != lemma:
        forms.append(
            {
                "form_id": f"{row['record_id']}-FORM-SEARCH",
                "type": "normalized",
                "orth": search,
                "language": None,
                "script": "Latn",
                "source_layer": "headword_search_technical",
                "cert": None,
            }
        )
    return forms


def make_senses(row: dict[str, str]) -> list[dict]:
    """Only project explicitly editorial translations here.

    definition_raw is intentionally NOT promoted automatically to a semantic <sense>
    because its documentary role varies by lexicographic direction and article structure.
    """
    translation = text(row.get("translation_es_editorial"))
    if not translation:
        return []
    return [
        {
            "sense_id": f"{row['record_id']}-SENSE-EDITORIAL-1",
            "source_gloss": None,
            "editorial_translation": translation,
            "language": "es",
            "examples": [],
            "notes": [
                "Editorial Spanish translation; not attributed to Steffel and not a human-validated semantic segmentation."
            ],
            "cert": None,
        }
    ]


def make_notes(row: dict[str, str]) -> list[dict]:
    notes = []
    diplomatic_note = text(row.get("diplomatic_note"))
    if diplomatic_note:
        notes.append(
            {
                "type": "diplomatic_note",
                "text": diplomatic_note,
                "status": text(row.get("diplomatic_note_state")) or None,
                "responsibility": "ai_assisted_editorial_layer",
            }
        )
    editorial_note = text(row.get("editorial_note"))
    if editorial_note:
        notes.append(
            {
                "type": "editorial_note",
                "text": editorial_note,
                "status": None,
                "responsibility": "project_editorial_layer",
            }
        )
    return notes


def make_provenance(profile: dict, row: dict[str, str], status: str) -> list[dict]:
    rid = row["record_id"]
    ocr_pointer = source_pointer(row)
    witness = witness_pointer(profile, row)
    extraction_method = text(row.get("extraction_method")) or "source_specific_segmentation"

    events = [
        {
            "activity_id": f"RHD-ACT-OCRLINK-{rid}",
            "activity_type": "ocr_source_linkage",
            "generated_entity": f"{rid}#layers.ocr_raw",
            "used_entities": [ocr_pointer],
            "agent_id": None,
            "agent_type": "software",
            "method": "preserved_source_ocr_linkage",
            "timestamp": None,
            "software_version": None,
        },
        {
            "activity_id": f"RHD-ACT-SEG-{rid}",
            "activity_type": "segmentation_candidate_generation",
            "generated_entity": f"{rid}#layers.segmentation",
            "used_entities": [f"{rid}#layers.ocr_raw"],
            "agent_id": None,
            "agent_type": "software",
            "method": extraction_method,
            "timestamp": None,
            "software_version": None,
        },
    ]

    if status == "active" and text(row.get("article_diplomatic")):
        events.append(
            {
                "activity_id": text(row.get("diplomatic_batch")) or f"RHD-ACT-DIP-{rid}",
                "activity_type": "diplomatic_transcription",
                "generated_entity": f"{rid}#layers.diplomatic",
                "used_entities": [witness],
                "agent_id": None,
                "agent_type": "ai_system",
                "method": text(row.get("diplomatic_review_method"))
                or "ai_assisted_direct_facsimile_collation",
                "timestamp": None,
                "software_version": None,
            }
        )
    return events


def convert(profile: dict, row: dict[str, str]) -> dict:
    rid = row["record_id"]
    status = canonical_status(row)
    rejected = status == "rejected_boundary"
    diplomatic_text = text(row.get("article_diplomatic")) if not rejected else ""
    diplomatic_head = text(row.get("headword_diplomatic")) if not rejected else ""

    notes = make_notes(row)
    lexical = {
        "forms": make_forms(row),
        "senses": make_senses(row),
        "cross_references": [],
    }

    canonical = {
        "record_id": rid,
        "source_id": profile["source_id"],
        "witness_id": profile["witness"]["witness_id"],
        "direction": text(row.get("direction")) or None,
        "status": status,
        "locators": {
            "printed_page": integer_or_none(row.get("printed_page")),
            "digital_page": integer_or_none(row.get("pdf_page")),
            "column": text(row.get("facsimile_column")) or None,
            "region": None,
            "iiif_canvas": None,
            "iiif_target": None,
            "ocr_line_start": integer_or_none(row.get("source_ocr_line_start")),
            "ocr_line_end": integer_or_none(row.get("source_ocr_line_end")),
        },
        "layers": {
            "ocr_raw": {
                "text": text(row.get("article_ocr_raw")) or text(row.get("definition_raw")),
                "headword": text(row.get("headword_ocr_raw")) or None,
                "status": "preserved_source_ocr",
                "method": "preserved_source_ocr_linkage",
                "activity_id": f"RHD-ACT-OCRLINK-{rid}",
                "responsibility": None,
                "confidence": None,
                "derived_from": [source_pointer(row)],
            },
            "segmentation": {
                "method": text(row.get("extraction_method")) or "source_specific_segmentation",
                "score": float_or_none(row.get("extraction_score")),
                "confidence": text(row.get("segmentation_confidence")) or "unknown",
                "decision": "rejected" if rejected else ("accepted" if status == "active" else "pending"),
                "decision_event_id": None,
            },
            "diplomatic": {
                "text": diplomatic_text,
                "headword": diplomatic_head or None,
                "status": (
                    "not_applicable_rejected_boundary"
                    if rejected
                    else (text(row.get("diplomatic_status")) or "pending")
                ),
                "method": (
                    "none"
                    if rejected
                    else (
                        text(row.get("diplomatic_review_method"))
                        or "ai_assisted_direct_facsimile_collation"
                    )
                ),
                "activity_id": None if rejected else (text(row.get("diplomatic_batch")) or None),
                "responsibility": None if rejected else "ai_assisted",
                "confidence": None,
                "derived_from": [] if rejected else [witness_pointer(profile, row)],
            },
            "critical": None,
            "normalized": None,
        },
        "lexical": lexical,
        "validation": [],
        "historical_relations": [],
        "provenance": make_provenance(profile, row, status),
        "notes": notes,
    }

    # Preserve the epistemic boundary explicitly. A flat source flag cannot create
    # a synthetic human validation event; that must be joined from an actual review manifest.
    if boolish(row.get("human_verified")):
        canonical["notes"].append(
            {
                "type": "legacy_human_verified_flag",
                "text": "Operational source row carries human_verified=true; canonical human event must be joined from its review manifest before promotion.",
                "status": "requires_event_join",
                "responsibility": "adapter_safeguard",
            }
        )
    return canonical


def main() -> None:
    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    rows = list(csv.DictReader(INPUT.open(encoding="utf-8")))
    canonical = [convert(profile, row) for row in rows]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with OUT_JSONL.open("w", encoding="utf-8") as fh:
        for item in canonical:
            fh.write(json.dumps(item, ensure_ascii=False, separators=(",", ":")) + "\n")

    summary = {
        "dataset": "raramuri-historico-steffel-1809",
        "rhd_core_version": profile["rhd_core_version"],
        "source_profile_version": profile["profile_version"],
        "records_total": len(canonical),
        "active": sum(x["status"] == "active" for x in canonical),
        "rejected_boundary": sum(x["status"] == "rejected_boundary" for x in canonical),
        "candidate": sum(x["status"] == "candidate" for x in canonical),
        "open_validation_notes": sum(
            any(n.get("status") == "open_validation" for n in x["notes"]) for x in canonical
        ),
        "human_validation_events": sum(
            any(v.get("reviewer_type") == "human" for v in x["validation"]) for x in canonical
        ),
        "scope": "non-destructive documentary projection; PHIL/human validation manifests are not yet joined",
    }
    OUT_SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"generated {len(canonical)} RHD canonical records: "
        f"{summary['active']} active, {summary['rejected_boundary']} rejected boundaries"
    )


if __name__ == "__main__":
    main()
