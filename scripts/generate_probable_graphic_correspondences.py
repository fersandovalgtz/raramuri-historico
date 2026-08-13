#!/usr/bin/env python3
"""Generate conservative probable Steffel ↔ Rarámuri Digital graphic candidates.

This second cohort is deliberately distinct from exact normalized matches. It uses
only bounded character-edit distance on documentary comparison keys. The output is
a review queue, not a claim of semantic identity, cognacy, lexical continuity,
dialect identity or normative equivalence.
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
EXACT = ROOT / "data" / "diachronic" / "exact_graphic_candidates.json"
OUT_JSON = ROOT / "data" / "diachronic" / "probable_graphic_candidates.json"
OUT_CSV = ROOT / "data" / "diachronic" / "probable_graphic_candidates.csv"
SUMMARY = ROOT / "data" / "diachronic" / "probable_graphic_candidates_summary.json"

APOSTROPHES = str.maketrans({
    "’": "'", "‘": "'", "ʼ": "'", "ʻ": "'", "ʹ": "'", "`": "'", "´": "'"
})
DASHES = str.maketrans({"–": "-", "—": "-", "‑": "-", "‐": "-"})
EDGE_PUNCT = " .,:;!?()[]{}"
MAX_PER_HISTORICAL_COMPONENT = 3


def normalized_graphic_key(value: str) -> str:
    """Conservative comparison key; never treated as a linguistic normalization."""
    value = (value or "").strip().translate(APOSTROPHES).translate(DASHES)
    value = value.replace("ſ", "s").replace("ß", "ss")
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    value = value.casefold()
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
        if len(re.sub(r"[^a-z0-9]", "", key)) < 4:
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
        ["git", "-C", str(MODERN_ROOT), "rev-parse", "HEAD"], text=True
    ).strip()
    if actual != expected_commit:
        raise SystemExit(
            f"pinned contemporary checkout mismatch: expected {expected_commit}, got {actual}"
        )


def levenshtein(a: str, b: str, max_distance: int = 2) -> int:
    """Bounded Levenshtein distance; returns max_distance+1 when the bound is exceeded."""
    if a == b:
        return 0
    if abs(len(a) - len(b)) > max_distance:
        return max_distance + 1
    if len(a) > len(b):
        a, b = b, a
    previous = list(range(len(a) + 1))
    for j, cb in enumerate(b, start=1):
        current = [j]
        row_min = current[0]
        for i, ca in enumerate(a, start=1):
            current.append(min(
                current[-1] + 1,
                previous[i] + 1,
                previous[i - 1] + (ca != cb),
            ))
            row_min = min(row_min, current[-1])
        if row_min > max_distance:
            return max_distance + 1
        previous = current
    return previous[-1]


def allowed_distance(key: str) -> int:
    n = len(re.sub(r"[^a-z0-9]", "", key))
    if n < 4:
        return 0
    if n <= 8:
        return 1
    return 2


def main() -> None:
    if not HISTORICAL.exists() or not MODERN.exists():
        raise SystemExit("historical corpus or pinned contemporary checkout is missing")

    historical_source = registry_source("historical")
    modern_source = registry_source("contemporary")
    modern_commit = modern_source.get("commit", "")
    if not re.fullmatch(r"[0-9a-f]{40}", modern_commit):
        raise SystemExit("contemporary source registry must pin a 40-character commit SHA")
    verify_pinned_checkout(modern_commit)

    exact_pairs: set[tuple[str, int, str, int]] = set()
    if EXACT.exists():
        exact_payload = json.loads(EXACT.read_text(encoding="utf-8"))
        for item in exact_payload.get("records", []):
            h = item["historical"]
            m = item["modern"]
            exact_pairs.add((
                h["record_id"], int(h["matched_component_index"]),
                m["record_id"], int(m["matched_component_index"]),
            ))

    historical_rows = list(csv.DictReader(HISTORICAL.open(encoding="utf-8")))
    modern_rows = list(csv.DictReader(MODERN.open(encoding="utf-8-sig")))

    modern_buckets: dict[tuple[str, int], list[dict]] = defaultdict(list)
    eligible_modern = 0
    for row in modern_rows:
        rid = (row.get("record_id") or "").strip()
        headword = (row.get("headword") or "").strip()
        if not re.fullmatch(r"RD-[0-9]{6}", rid) or not headword:
            continue
        eligible_modern += 1
        for component_index, component in enumerate(split_components(headword), start=1):
            key = normalized_graphic_key(component)
            if not key:
                continue
            modern_buckets[(key[0], len(key))].append({
                "row": row,
                "component": component,
                "component_index": component_index,
                "key": key,
            })

    candidates: list[dict] = []
    eligible_historical = 0
    hist_records_with_candidates: set[str] = set()
    modern_records_matched: set[str] = set()
    distinct_hist_components = 0
    distance_counts: dict[str, int] = defaultdict(int)

    for row in historical_rows:
        if row.get("direction") != "RAR-DE" or row.get("status") == "rejected_false_positive":
            continue
        rid = (row.get("record_id") or "").strip()
        diplomatic = (row.get("headword_diplomatic") or "").strip()
        if not re.fullmatch(r"RHD-S1809-[0-9]{5}", rid) or not diplomatic:
            continue
        eligible_historical += 1
        for h_index, h_component in enumerate(split_components(diplomatic, historical=True), start=1):
            h_key = normalized_graphic_key(h_component)
            max_d = allowed_distance(h_key)
            if max_d == 0 or not h_key:
                continue
            pool: list[dict] = []
            for length in range(max(4, len(h_key) - max_d), len(h_key) + max_d + 1):
                pool.extend(modern_buckets.get((h_key[0], length), []))

            component_hits: list[tuple[int, float, dict]] = []
            for m_item in pool:
                m = m_item["row"]
                m_key = m_item["key"]
                if h_key == m_key:
                    continue
                pair = (rid, h_index, m.get("record_id", ""), m_item["component_index"])
                if pair in exact_pairs:
                    continue
                d = levenshtein(h_key, m_key, max_distance=max_d)
                if d == 0 or d > max_d:
                    continue
                similarity = 1.0 - (d / max(len(h_key), len(m_key)))
                # A distance of two is admitted only for long forms and high proportional similarity.
                if d == 2 and (max(len(h_key), len(m_key)) < 9 or similarity < 0.80):
                    continue
                component_hits.append((d, similarity, m_item))

            component_hits.sort(key=lambda x: (
                x[0], -x[1], x[2]["key"], x[2]["row"].get("record_id", ""),
                x[2]["component_index"],
            ))
            if component_hits:
                distinct_hist_components += 1

            seen_modern: set[tuple[str, int]] = set()
            kept = 0
            for d, similarity, m_item in component_hits:
                m = m_item["row"]
                marker = (m.get("record_id", ""), m_item["component_index"])
                if marker in seen_modern:
                    continue
                seen_modern.add(marker)
                candidates.append({
                    "correspondence_id": "",
                    "historical": {
                        "record_id": rid,
                        "form_diplomatic": diplomatic,
                        "matched_component": h_component,
                        "matched_component_index": h_index,
                        "match_key": h_key,
                        "article_diplomatic": row.get("article_diplomatic", ""),
                        "printed_page": int(row.get("printed_page") or 0),
                        "direction": row.get("direction", ""),
                    },
                    "modern": {
                        "record_id": m.get("record_id", ""),
                        "headword": m.get("headword", ""),
                        "headword_raw": m.get("headword_raw", ""),
                        "headword_normalized": m.get("headword_normalized", ""),
                        "matched_component": m_item["component"],
                        "matched_component_index": m_item["component_index"],
                        "match_key": m_item["key"],
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
                        "type": "probable_graphic_correspondence",
                        "status": "machine_candidate",
                        "historical_graphic_key": h_key,
                        "modern_graphic_key": m_item["key"],
                        "edit_distance": d,
                        "similarity": round(similarity, 4),
                        "same_initial_required": True,
                        "max_candidates_per_historical_component": MAX_PER_HISTORICAL_COMPONENT,
                        "interpretive_scope": (
                            "Bounded graphic similarity only. This candidate does not assert semantic identity, "
                            "cognacy, lexical continuity, dialect identity, phonological correspondence or normative equivalence."
                        ),
                    },
                    "derivation": {
                        "method": "conservative_bounded_edit_distance_v1",
                        "historical_source": historical_source.get("canonical_file", "data/entries.csv"),
                        "modern_repository": modern_source.get("repository", ""),
                        "modern_commit": modern_commit,
                        "modern_source": modern_source.get("canonical_file", ""),
                        "normalization": (
                            "Unicode NFKD; remove combining diacritics; ſ→s; ß→ss; casefold; "
                            "unify apostrophe/dash glyphs; collapse whitespace; preserve spaces, apostrophes and hyphens."
                        ),
                        "candidate_rule": (
                            "Minimum component length 4; same initial character; length-bounded Levenshtein distance; "
                            "distance ≤1 for keys of length 4–8; distance ≤2 only for keys length ≥9 with similarity ≥0.80; "
                            "exact-normalized matches excluded; at most three modern candidates retained per historical component."
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
                distance_counts[str(d)] += 1
                hist_records_with_candidates.add(rid)
                modern_records_matched.add(m.get("record_id", ""))
                kept += 1
                if kept >= MAX_PER_HISTORICAL_COMPONENT:
                    break

    candidates.sort(key=lambda x: (
        x["historical"]["record_id"],
        x["historical"]["matched_component_index"],
        x["candidate_relation"]["edit_distance"],
        -x["candidate_relation"]["similarity"],
        x["modern"]["record_id"],
        x["modern"]["matched_component_index"],
    ))
    for i, item in enumerate(candidates, start=1):
        item["correspondence_id"] = f"RHD-PCORR-{i:06d}"

    payload = {
        "dataset": "raramuri-historico-steffel-1809",
        "layer": "diachronic_correspondence_candidates",
        "cohort": "probable_graphic_correspondence_v1",
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
        "historical_records_with_candidates": len(hist_records_with_candidates),
        "historical_components_with_candidates": distinct_hist_components,
        "modern_records_matched": len(modern_records_matched),
        "edit_distance_counts": dict(sorted(distance_counts.items())),
        "relation_type": "probable_graphic_correspondence",
        "candidate_status": "machine_candidate",
        "human_reviewed": False,
        "modern_repository": modern_source.get("repository", ""),
        "modern_commit": modern_commit,
        "modern_source": modern_source.get("canonical_file", ""),
        "method": "conservative_bounded_edit_distance_v1",
        "max_candidates_per_historical_component": MAX_PER_HISTORICAL_COMPONENT,
        "scope_note": (
            "Counts describe bounded graphic-similarity candidates only. No candidate is a validated semantic, "
            "etymological, phonological, dialectal or historical-continuity relation."
        ),
    }

    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    fields = [
        "correspondence_id", "historical_record_id", "historical_form_diplomatic",
        "historical_matched_component", "historical_printed_page", "historical_graphic_key",
        "modern_record_id", "modern_headword", "modern_matched_component", "modern_graphic_key",
        "modern_classification", "modern_translation_raw", "modern_source_code", "edit_distance",
        "similarity", "relation_type", "candidate_status", "modern_commit", "human_reviewed", "review_decision"
    ]
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for x in candidates:
            w.writerow({
                "correspondence_id": x["correspondence_id"],
                "historical_record_id": x["historical"]["record_id"],
                "historical_form_diplomatic": x["historical"]["form_diplomatic"],
                "historical_matched_component": x["historical"]["matched_component"],
                "historical_printed_page": x["historical"]["printed_page"],
                "historical_graphic_key": x["candidate_relation"]["historical_graphic_key"],
                "modern_record_id": x["modern"]["record_id"],
                "modern_headword": x["modern"]["headword"],
                "modern_matched_component": x["modern"]["matched_component"],
                "modern_graphic_key": x["candidate_relation"]["modern_graphic_key"],
                "modern_classification": x["modern"]["classification"],
                "modern_translation_raw": x["modern"]["translation_raw"],
                "modern_source_code": x["modern"]["source_code"],
                "edit_distance": x["candidate_relation"]["edit_distance"],
                "similarity": x["candidate_relation"]["similarity"],
                "relation_type": x["candidate_relation"]["type"],
                "candidate_status": x["candidate_relation"]["status"],
                "modern_commit": x["derivation"]["modern_commit"],
                "human_reviewed": "false",
                "review_decision": "not_assessed",
            })

    print(
        "Generated probable graphic candidates: "
        f"{len(candidates)} relations; {len(hist_records_with_candidates)} historical records; "
        f"{distinct_hist_components} historical components; distances={dict(sorted(distance_counts.items()))}."
    )


if __name__ == "__main__":
    main()
