#!/usr/bin/env python3
"""Generate a deterministic queue for post-diplomatic scientific validation.

This stage does not claim human, philological, or linguistic verification. It
prioritizes active diplomatic records explicitly marked `open_validation`, while
preserving the diplomatic layer as immutable evidence.
"""
from pathlib import Path
import csv, json, re

ROOT = Path(__file__).resolve().parents[1]
ENTRIES = ROOT / "data" / "entries.csv"
OUTDIR = ROOT / "data" / "validation"
OUTDIR.mkdir(parents=True, exist_ok=True)

rows = list(csv.DictReader(ENTRIES.open(encoding="utf-8")))

RULES = [
    (
        1,
        "graphic_reading",
        re.compile(r"uncertain|unclear|ambiguous|illegible|difficult|provisional|glyph|letter|blur|damage|obscur|faint|could (?:be|read)|may (?:be|read)|not certain|exact [^.]{0,80}remain", re.I),
        "Reinspect the printed form at high resolution; resolve characters only when the image supports a unique reading."
    ),
    (
        2,
        "article_structure",
        re.compile(r"boundary|continuation|catchword|column|page drift|page assignment|article structure|punctuation|line break|cross-reference", re.I),
        "Recheck article extent, column continuity, punctuation, and cross-reference status against the facsimile."
    ),
    (
        3,
        "historical_raramuri_form",
        re.compile(r"rarámuri|rar[aá]muri|linguistic|morpholog|historical form|variant|accent|orthograph|suffix|particle|root|verbal|phonolog", re.I),
        "Preserve the diplomatic reading; request independent linguistic assessment of the historical Rarámuri form."
    ),
    (
        4,
        "semantic_or_gloss",
        re.compile(r"gloss|meaning|semantic|translation|german gloss|spanish|sense|botanical|zoological|cultural identification", re.I),
        "Keep source wording separate from editorial interpretation; verify gloss, sense, or domain identification independently."
    ),
]

def classify(note: str):
    for priority, category, rx, action in RULES:
        if rx.search(note):
            return priority, category, action
    return 5, "general_open_validation", "Independent philological and/or linguistic review required; do not normalize over the diplomatic layer."

records = []
resolved_note_count = 0
nonempty_note_count = 0
for r in rows:
    if r.get("status") == "rejected_false_positive":
        continue
    if r.get("diplomatic_status") != "complete_ai_assisted":
        continue
    note = (r.get("diplomatic_note") or "").strip()
    if note:
        nonempty_note_count += 1
    state = (r.get("diplomatic_note_state") or "").strip()
    if state == "resolved_editorial_note":
        resolved_note_count += 1
        continue
    if state != "open_validation":
        continue
    priority, category, action = classify(note)
    records.append({
        "record_id": r["record_id"],
        "priority": priority,
        "category": category,
        "direction": r.get("direction", ""),
        "printed_page": int(r["printed_page"]),
        "pdf_page": int(r["pdf_page"]),
        "facsimile_column": r.get("facsimile_column", ""),
        "headword_diplomatic": r.get("headword_diplomatic", ""),
        "article_diplomatic": r.get("article_diplomatic", ""),
        "open_validation_note": note,
        "recommended_action": action,
        "human_verified": False,
        "philologically_verified": False,
        "linguistically_verified": False,
        "validation_state": "pending_independent_review"
    })

records.sort(key=lambda x: (x["priority"], x["printed_page"], x["record_id"]))

counts = {}
for x in records:
    counts[x["category"]] = counts.get(x["category"], 0) + 1

full = {
    "dataset": "raramuri-historico-steffel-1809",
    "stage": "post_diplomatic_scientific_validation",
    "selection_rule": "active complete_ai_assisted diplomatic records with diplomatic_note_state=open_validation",
    "classification_method": "deterministic regex triage over explicit open-validation notes",
    "classification_is_linguistic_validation": False,
    "human_verified": False,
    "nonempty_diplomatic_notes_total": nonempty_note_count,
    "resolved_editorial_notes_excluded": resolved_note_count,
    "count": len(records),
    "category_counts": counts,
    "records": records,
}
(OUTDIR / "uncertainty_queue.json").write_text(json.dumps(full, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

compact_records = [
    [x["record_id"], x["priority"], x["category"], x["printed_page"], x["facsimile_column"], x["headword_diplomatic"]]
    for x in records
]
compact = {
    "nonempty_diplomatic_notes_total": nonempty_note_count,
    "resolved_editorial_notes_excluded": resolved_note_count,
    "count": len(records),
    "category_counts": counts,
    "first_batch_size": min(50, len(records)),
    "records": compact_records,
}
(OUTDIR / "uncertainty_queue_compact.json").write_text(json.dumps(compact, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")

inventory = {
    "stage": "scientific_validation_preparation",
    "diplomatic_records_with_any_editorial_note": nonempty_note_count,
    "resolved_editorial_notes_excluded_from_open_queue": resolved_note_count,
    "active_diplomatic_records_with_explicit_open_validation": len(records),
    "category_counts": counts,
    "priority_order": [
        "graphic_reading",
        "article_structure",
        "historical_raramuri_form",
        "semantic_or_gloss",
        "general_open_validation"
    ],
    "human_verified_records": 0,
    "philologically_verified_records": 0,
    "linguistically_verified_records": 0,
    "normalization_overwrites_diplomatic_layer": False,
}
(OUTDIR / "validation_inventory.json").write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(
    f"Generated scientific-validation queue: {len(records)} open records from "
    f"{nonempty_note_count} non-empty diplomatic notes; resolved notes excluded={resolved_note_count}; categories={counts}"
)
