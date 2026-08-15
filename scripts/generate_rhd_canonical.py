#!/usr/bin/env python3
"""Generate a non-destructive RHD 1.0 canonical projection from Steffel 0.2.0.

This adapter deliberately preserves data/entries.csv as the operational master.
It joins append-only RHD-PHIL manifests as explicit AI-assisted validation events,
without adjudicating semantics, morphology, cognacy, or human verification.
"""

from __future__ import annotations

from pathlib import Path
from collections import Counter, defaultdict
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "entries.csv"
PROFILE_PATH = ROOT / "source_profiles" / "steffel-1809.source.json"
PHIL_DIR = ROOT / "data" / "validation" / "review"
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
    """Project only explicit editorial translations.

    definition_raw is intentionally NOT promoted automatically to a semantic sense
    because its documentary role varies by direction and article microstructure.
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


def load_phil_events() -> tuple[dict[str, list[dict]], dict[str, dict], Counter]:
    """Read append-only PHIL manifests and index them by persistent record_id."""
    by_record: dict[str, list[dict]] = defaultdict(list)
    batch_meta: dict[str, dict] = {}
    disposition_counts: Counter = Counter()

    for path in sorted(PHIL_DIR.glob("philological_review_batch_*.json")):
        manifest = json.loads(path.read_text(encoding="utf-8"))
        batch_id = text(manifest.get("batch_id")) or path.stem
        batch_meta[batch_id] = {
            "review_date": text(manifest.get("review_date")) or None,
            "review_method": text(manifest.get("review_method")) or "ai_assisted_philological_recollation",
            "source_authority": text(manifest.get("source_authority")) or None,
            "human_verified": manifest.get("human_verified") is True,
            "philologically_verified_by_human": manifest.get("philologically_verified_by_human") is True,
            "linguistically_verified": manifest.get("linguistically_verified") is True,
            "manifest_path": path.relative_to(ROOT).as_posix(),
        }
        for record in manifest.get("records", []):
            rid = text(record.get("record_id"))
            if not rid:
                continue
            disposition = text(record.get("disposition")) or "unresolved"
            disposition_counts[disposition] += 1
            by_record[rid].append(
                {
                    "batch_id": batch_id,
                    "manifest_path": path.relative_to(ROOT).as_posix(),
                    "review_date": batch_meta[batch_id]["review_date"],
                    "review_method": batch_meta[batch_id]["review_method"],
                    "source_authority": batch_meta[batch_id]["source_authority"],
                    "disposition": disposition,
                    "confirmed_reading": text(record.get("confirmed_reading")) or None,
                    "previous_reading": text(record.get("previous_reading")) or None,
                    "proposed_reading": text(record.get("proposed_reading")) or None,
                    "correction_scope": text(record.get("correction_scope")) or None,
                    "residual_route": text(record.get("residual_route")) or None,
                    "note": text(record.get("note")) or None,
                    "printed_page": integer_or_none(record.get("printed_page")),
                }
            )
    return by_record, batch_meta, disposition_counts


def make_phil_validation_event(profile: dict, row: dict[str, str], event: dict) -> dict:
    evidence = [witness_pointer(profile, row), event["manifest_path"]]
    if event.get("source_authority"):
        evidence.append(f"source_authority: {event['source_authority']}")
    if event.get("confirmed_reading"):
        evidence.append(f"confirmed_reading: {event['confirmed_reading']}")
    if event.get("previous_reading"):
        evidence.append(f"previous_reading: {event['previous_reading']}")
    if event.get("proposed_reading"):
        evidence.append(f"proposed_reading: {event['proposed_reading']}")
    if event.get("correction_scope"):
        evidence.append(f"correction_scope: {event['correction_scope']}")
    if event.get("residual_route"):
        evidence.append(f"residual_route: {event['residual_route']}")

    return {
        "event_id": f"{event['batch_id']}:{row['record_id']}",
        "scope": "philological",
        "decision": event["disposition"],
        "reviewer_type": "ai_assisted",
        "agent_id": None,
        "date": event.get("review_date"),
        "evidence": evidence,
        "justification": event.get("note"),
        "confidence": None,
    }


def make_provenance(profile: dict, row: dict[str, str], status: str, phil_events: list[dict]) -> list[dict]:
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

    for event in phil_events:
        events.append(
            {
                "activity_id": event["batch_id"],
                "activity_type": "ai_assisted_philological_recollation",
                "generated_entity": f"{rid}#validation/{event['batch_id']}",
                "used_entities": [witness, f"{rid}#layers.diplomatic", event["manifest_path"]],
                "agent_id": None,
                "agent_type": "ai_system",
                "method": event.get("review_method") or "ai_assisted_philological_recollation",
                "timestamp": None,
                "software_version": None,
            }
        )
    return events


def convert(profile: dict, row: dict[str, str], phil_events: list[dict]) -> dict:
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
    validation = [make_phil_validation_event(profile, row, event) for event in phil_events]

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
        "validation": validation,
        "historical_relations": [],
        "provenance": make_provenance(profile, row, status, phil_events),
        "notes": notes,
    }

    # A flat source flag cannot create a synthetic human validation event; a real
    # human review manifest must be joined before any reviewer_type=human event exists.
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
    phil_by_record, batch_meta, disposition_counts = load_phil_events()
    canonical = [convert(profile, row, phil_by_record.get(row["record_id"], [])) for row in rows]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with OUT_JSONL.open("w", encoding="utf-8") as fh:
        for item in canonical:
            fh.write(json.dumps(item, ensure_ascii=False, separators=(",", ":")) + "\n")

    all_validation = [event for item in canonical for event in item["validation"]]
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
        "philological_ai_validation_events": sum(
            v.get("scope") == "philological" and v.get("reviewer_type") == "ai_assisted"
            for v in all_validation
        ),
        "philological_ai_batches": sorted(batch_meta),
        "philological_ai_dispositions": dict(sorted(disposition_counts.items())),
        "human_validation_events": sum(v.get("reviewer_type") == "human" for v in all_validation),
        "scope": "non-destructive documentary projection with RHD-PHIL AI-assisted events joined; independent human review remains separate and absent until real review manifests exist",
    }
    OUT_SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"generated {len(canonical)} RHD canonical records: "
        f"{summary['active']} active, {summary['rejected_boundary']} rejected boundaries, "
        f"{summary['philological_ai_validation_events']} PHIL events"
    )


if __name__ == "__main__":
    main()
