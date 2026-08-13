#!/usr/bin/env python3
"""Generate conservative Steffel ↔ Rarámuri Digital graphic candidates.

The output is a documentary comparison layer. A machine candidate never asserts
semantic identity, cognacy, lexical continuity, dialect identity or normative
equivalence, and it never overwrites either source corpus.
"""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import csv
import json
import re
import subprocess
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
HISTORICAL = ROOT / "data" / "entries.csv"
REGISTRY = ROOT / "data" / "diachronic" / "source_registry.json"
MODERN_ROOT = ROOT / ".tmp-raramuri-digital"
MODERN = MODERN_ROOT / "data" / "lexicon-master.csv"
OUT_JSON = ROOT / "data" / "diachronic" / "exact_graphic_candidates.json"
OUT_CSV = ROOT / "data" / "diachronic" / "exact_graphic_candidates.csv"
SUMMARY = ROOT / "data" / "diachronic" / "exact_graphic_candidates_summary.json"

APOSTROPHES = str.maketrans({
    "’": "'", "‘": "'", "ʼ": "'", "ʻ": "'", "ʹ": "'", "`": "'", "´": "'"
})
DASHES = str.maketrans({"–": "-", "—": "-", "‑": "-", "‐": "-"})
EDGE_PUNCT = " .,:;!?()[]{}"


def normalized_graphic_key(value: str) -> str:
    """Conservative comparison key, not a phonological normalization."""
    value = (value or "").strip().translate(APOSTROPHES).translate(DASHES)
    value = value.replace("ſ", "s").replace("ß", "ss")
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    value = value.casefold()
    # Preserve spaces, apostrophes and hyphens; deleting them would create a
    # stronger equivalence claim than this first documentary pass warrants.
    value = re.sub(r"[^0-9a-z' -]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip(EDGE_PUNCT + "\"'-")
    return value


def split_components(value: str, historical: bool = False) -> list[str]:
    """Split only explicit variant separators; never infer morphology."""
    value = (value or "").strip()
    if not value:
        return []
    pattern = r"\s+(?:oder|item)\s+|[,;/]" if historical else r"[,;/]"
    raw_parts = re.split(pattern, value, flags=re.IGNORECASE)
    out: list[str] = []
    seen: set[tuple[str, str]] = set()
    for part in raw_parts:
        part = re.sub(r"\s+", " ", part).strip().strip(EDGE_PUNCT)
        key = normalized_graphic_key(part)
        if len(re.sub(r"[^a-z0-9]", "", key)) < 2:
            continue
        marker = (part, key)
        if marker not in seen:
            out.append(part)
            seen.add(marker)
    return out


def registry_source(role: str) -> dict:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    for source in registry.get("sources", []):
        if source.get("role") == role:
            return source
    raise SystemExit(f"source_registry.json lacks role={role}")


def verify_pinned_checkout(expected_commit: str) -> None:
    actual = subprocess.check_output(
        ["git", "-C", str(MODERN_ROOT), "rev-parse", "HEAD"],
        text=True,
    ).strip()
    if actual != expected_commit:
        raise SystemExit(
            f"pinned contemporary checkout mismatch: expected {expected_commit}, got {actual}"
        )


def main() -> None:
    if not HISTORICAL.exists():
        raise SystemExit("missing data/entries.csv")
    if not MODERN.exists():
        raise SystemExit(
            "missing pinned contemporary checkout at .tmp-raramuri-digital; "
            "the validation workflow must checkout source_registry.json's contemporary commit"
        )

    historical_source = registry_source("historical")
    modern_source = registry_source("contemporary")
    modern_commit = modern_source.get("commit", "")
    if not re.fullmatch(r"[0-9a-f]{40}", modern_commit):
        raise SystemExit("contemporary source registry must pin a 40-character commit SHA")
    verify_pinned_checkout(modern_commit)

    historical_rows = list(csv.DictReader(HISTORICAL.open(encoding="utf-8")))
    modern_rows = list(csv.DictReader(MODERN.open(encoding="utf-8-sig")))

    modern_index: dict[str, list[dict]] = defaultdict(list)
    eligible_modern = 0
    for row in modern_rows:
        rid = (row.get("record_id") or "").strip()
        headword = (row.get("headword") or "").strip()
        if not re.fullmatch(r"RD-[0-9]{6}", rid) or not headword:
            continue
        eligible_modern += 1
        for component_index, component in enumerate(split_components(headword), start=1):
            key = normalized_graphic_key(component)
            modern_index[key].append({
                "row": row,
                "component": component,
                "component_index": component_index,
            })

    candidates: list[dict] = []
    eligible_historical = 0
    historical_records_matched: set[str] = set()
    modern_records_matched: set[str] = set()
    matched_keys: set[str] = set()

    for row in historical_rows:
        if row.get("direction") != "RAR-DE" or row.get("status") == "rejected_false_positive":
            continue
        rid = (row.get("record_id") or "").strip()
        diplomatic = (row.get("headword_diplomatic") or "").strip()
        if not re.fullmatch(r"RHD-S1809-[0-9]{5}", rid) or not diplomatic:
            continue
        eligible_historical += 1
        for historical_component_index, historical_component in enumerate(
            split_components(diplomatic, historical=True), start=1
        ):
            key = normalized_graphic_key(historical_component)
            matches = modern_index.get(key, [])
            if not matches:
                continue
            matched_keys.add(key)
            for modern_match in matches:
                m = modern_match["row"]
                candidates.append({
                    "correspondence_id": "",
                    "historical": {
                        "record_id": rid,
                        "form_diplomatic": diplomatic,
                        "matched_component": historical_component,
                        "matched_component_index": historical_component_index,
                        "match_key": key,
                        "article_diplomatic": row.get("article_diplomatic", ""),
                        "printed_page": int(row.get("printed_page") or 0),
                        "direction": row.get("direction", ""),
                    },
                    "modern": {
                        "record_id": m.get("record_id", ""),
                        "headword": m.get("headword", ""),
                        "headword_raw": m.get("headword_raw", ""),
                        "headword_normalized": m.get("headword_normalized", ""),
                        "matched_component": modern_match["component"],
                        "matched_component_index": modern_match["component_index"],
                        "match_key": key,
                        "homonym_number": m.get("homonym_number", ""),
                        "classification": m.get("classification", ""),
                        "classification_family": m.get("classification_family", ""),
                        "translation_raw": m.get("translation_raw", ""),
                        "source_code": m.get("source_code", ""),
                        "source_document": m.get("source_document", ""),
                        "page_start": m.get("page_start", ""),
                        "page_end": m.get("page_end", ""),
                        "status": m.get("status", ""),
                    },
                    "candidate_relation": {
                        "type": "exact_normalized_graphic_match",
                        "status": "machine_candidate",
                        "graphic_key": key,
                        "modern_candidates_for_key": len(matches),
                        "short_form_warning": len(re.sub(r"[^a-z0-9]", "", key)) < 4,
                        "interpretive_scope": (
                            "Exact match under conservative graphic normalization only; "
                            "does not assert semantic identity, cognacy, lexical continuity, "
                            "dialect identity or normative equivalence."
                        ),
                    },
                    "derivation": {
                        "method": "conservative_exact_graphic_match_v1",
                        "historical_source": historical_source.get(
                            "canonical_file", "data/entries.csv"
                        ),
                        "modern_repository": modern_source.get("repository", ""),
                        "modern_commit": modern_commit,
                        "modern_source": modern_source.get("canonical_file", ""),
                        "normalization": (
                            "Unicode NFKD; remove combining diacritics; ſ→s; ß→ss; "
                            "casefold; unify apostrophe/dash glyphs; collapse whitespace; "
                            "preserve spaces, apostrophes and hyphens."
                        ),
                        "component_split": (
                            "Historical: explicit 'oder'/'item', comma, semicolon or slash; "
                            "modern: comma, semicolon or slash. No morphological segmentation."
                        ),
                    },
                    "independent_review": {
                        "human_reviewed": False,
                        "reviewer": "",
                        "review_date": "",
                        "decision": "not_assessed",
                        "adopted_relation_type": "not_assessed",
                        "confidence": "not_assessed",
                        "evidence": "",
                        "note": "",
                    },
                })
                historical_records_matched.add(rid)
                modern_records_matched.add(m.get("record_id", ""))

    candidates.sort(key=lambda x: (
        x["historical"]["record_id"],
        x["historical"]["matched_component_index"],
        x["modern"]["record_id"],
        x["modern"]["matched_component_index"],
    ))
    for i, item in enumerate(candidates, start=1):
        item["correspondence_id"] = f"RHD-CORR-{i:06d}"

    ambiguous_keys = {
        key for key in matched_keys
        if len({x["row"].get("record_id", "") for x in modern_index.get(key, [])}) > 1
    }
    short_candidates = sum(
        1 for x in candidates if x["candidate_relation"]["short_form_warning"]
    )

    payload = {
        "dataset": "raramuri-historico-steffel-1809",
        "layer": "diachronic_correspondence_candidates",
        "cohort": "exact_normalized_graphic_match_v1",
        "generated": "2026-08-13",
        "human_reviewed": False,
        "source_registry": "data/diachronic/source_registry.json",
        "modern_commit": modern_commit,
        "count": len(candidates),
        "records": candidates,
    }
    summary = {
        "dataset": payload["dataset"],
        "cohort": payload["cohort"],
        "generated": payload["generated"],
        "historical_direction": "RAR-DE",
        "historical_eligible_records": eligible_historical,
        "modern_eligible_records": eligible_modern,
        "candidate_count": len(candidates),
        "historical_records_with_candidates": len(historical_records_matched),
        "modern_records_matched": len(modern_records_matched),
        "unique_graphic_keys": len(matched_keys),
        "ambiguous_graphic_keys": len(ambiguous_keys),
        "short_form_candidates": short_candidates,
        "relation_type": "exact_normalized_graphic_match",
        "candidate_status": "machine_candidate",
        "human_reviewed": False,
        "modern_repository": modern_source.get("repository", ""),
        "modern_commit": modern_commit,
        "modern_source": modern_source.get("canonical_file", ""),
        "method": "conservative_exact_graphic_match_v1",
        "scope_note": (
            "Counts describe documentary comparison candidates only. No candidate is "
            "a validated semantic, etymological, dialectal or historical-continuity relation."
        ),
    }

    OUT_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    SUMMARY.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    fields = [
        "correspondence_id", "historical_record_id", "historical_form_diplomatic",
        "historical_matched_component", "historical_printed_page", "graphic_key",
        "modern_record_id", "modern_headword", "modern_headword_raw",
        "modern_headword_normalized", "modern_matched_component", "modern_homonym_number",
        "modern_classification", "modern_translation_raw", "modern_source_code",
        "relation_type", "candidate_status", "modern_candidates_for_key",
        "short_form_warning", "modern_commit", "human_reviewed", "review_decision",
    ]
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for x in candidates:
            writer.writerow({
                "correspondence_id": x["correspondence_id"],
                "historical_record_id": x["historical"]["record_id"],
                "historical_form_diplomatic": x["historical"]["form_diplomatic"],
                "historical_matched_component": x["historical"]["matched_component"],
                "historical_printed_page": x["historical"]["printed_page"],
                "graphic_key": x["candidate_relation"]["graphic_key"],
                "modern_record_id": x["modern"]["record_id"],
                "modern_headword": x["modern"]["headword"],
                "modern_headword_raw": x["modern"]["headword_raw"],
                "modern_headword_normalized": x["modern"]["headword_normalized"],
                "modern_matched_component": x["modern"]["matched_component"],
                "modern_homonym_number": x["modern"]["homonym_number"],
                "modern_classification": x["modern"]["classification"],
                "modern_translation_raw": x["modern"]["translation_raw"],
                "modern_source_code": x["modern"]["source_code"],
                "relation_type": x["candidate_relation"]["type"],
                "candidate_status": x["candidate_relation"]["status"],
                "modern_candidates_for_key": x["candidate_relation"]["modern_candidates_for_key"],
                "short_form_warning": str(
                    x["candidate_relation"]["short_form_warning"]
                ).lower(),
                "modern_commit": x["derivation"]["modern_commit"],
                "human_reviewed": "false",
                "review_decision": "not_assessed",
            })

    print(
        "Generated diachronic exact graphic candidates: "
        f"{len(candidates)} relations; {len(historical_records_matched)} historical "
        f"records; {len(modern_records_matched)} modern records; "
        f"{len(matched_keys)} keys."
    )


if __name__ == "__main__":
    main()
