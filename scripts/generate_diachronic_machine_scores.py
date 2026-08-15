#!/usr/bin/env python3
"""Generate non-semantic machine evidence scores for the 298 diachronic candidates.

The score is explicitly NOT a probability of cognacy, semantic identity, etymology or
historical continuity. It ranks documentary/retrieval support using only:
- conservative graphemic similarity of historical and modern forms;
- internal Steffel attestation count;
- reciprocal documentary support count;
- previously assigned machine context signal type.

All relations remain `candidate`.
"""

from pathlib import Path
from collections import Counter
from difflib import SequenceMatcher
import json
import math
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/research/diachronic_semantic_context_queue.json"
OUT = ROOT / "data/research/diachronic_machine_scores.json"

SIGNAL_BASE = {
    "cross_corpus_context_only": 0.10,
    "internal_form_attestation_only": 0.25,
    "internal_reciprocal_documentary_support": 0.35,
}


def normalized_form(value):
    value = (value or "").replace("ſ", "s").replace("ß", "ss")
    value = unicodedata.normalize("NFKD", value.casefold())
    return "".join(ch for ch in value if ch.isalpha() and not unicodedata.combining(ch))


def graphemic_features(historical, modern):
    h = normalized_form(historical)
    m = normalized_form(modern)
    if not h or not m:
        return {
            "historical_normalized": h,
            "modern_normalized": m,
            "exact_normalized_match": False,
            "sequence_ratio": 0.0,
        }
    return {
        "historical_normalized": h,
        "modern_normalized": m,
        "exact_normalized_match": h == m,
        "sequence_ratio": round(SequenceMatcher(None, h, m).ratio(), 6),
    }


def score_record(item):
    historical = item.get("historical", {})
    modern = item.get("modern", {})
    signal = item.get("machine_context_signal", {})
    signal_type = signal.get("type") or "cross_corpus_context_only"
    g = graphemic_features(
        historical.get("matched_component") or historical.get("form_diplomatic"),
        modern.get("headword"),
    )

    score = SIGNAL_BASE.get(signal_type, 0.05)
    # Graphemic component: exact conservative normalized equality is strong retrieval
    # evidence; otherwise use a bounded sequence-similarity contribution.
    if g["exact_normalized_match"]:
        graphemic_component = 0.35
    else:
        graphemic_component = 0.25 * g["sequence_ratio"]
    score += graphemic_component

    att = int(signal.get("internal_attestation_count") or 0)
    rec = int(signal.get("internal_reciprocal_support_count") or 0)
    attestation_component = min(0.15, math.log1p(att) / math.log(11) * 0.15) if att else 0.0
    reciprocal_component = min(0.20, rec * 0.10)
    score += attestation_component + reciprocal_component
    score = round(min(0.99, max(0.0, score)), 6)

    if score >= 0.75:
        bucket = "high_documentary_support"
    elif score >= 0.50:
        bucket = "medium_documentary_support"
    else:
        bucket = "low_documentary_support"

    return {
        "semantic_context_id": item.get("semantic_context_id"),
        "source_candidate_id": item.get("source_candidate_id"),
        "historical_record_id": historical.get("record_id"),
        "modern_record_id": modern.get("record_id"),
        "historical_form": historical.get("form_diplomatic"),
        "modern_form": modern.get("headword"),
        "signal_type": signal_type,
        "internal_attestation_count": att,
        "internal_reciprocal_support_count": rec,
        "graphemic": g,
        "components": {
            "signal_base": SIGNAL_BASE.get(signal_type, 0.05),
            "graphemic": round(graphemic_component, 6),
            "internal_attestation": round(attestation_component, 6),
            "reciprocal_support": round(reciprocal_component, 6),
        },
        "documentary_support_score": score,
        "support_bucket": bucket,
        "relation_status": "candidate",
        "score_scope": "documentary_retrieval_support_only",
        "semantic_probability": None,
        "cognacy_probability": None,
        "etymological_probability": None,
        "historical_continuity_probability": None,
        "human_reviewed": False,
    }


def main():
    data = json.loads(INPUT.read_text(encoding="utf-8"))
    records = [score_record(item) for item in data.get("records", [])]
    buckets = Counter(r["support_bucket"] for r in records)
    exact = sum(1 for r in records if r["graphemic"]["exact_normalized_match"])
    payload = {
        "dataset": "raramuri-historico-steffel-1809",
        "layer": "diachronic_machine_documentary_support",
        "count": len(records),
        "score_scope": "documentary_retrieval_support_only",
        "automatic_semantic_judgment": False,
        "automatic_cognacy_judgment": False,
        "automatic_etymological_judgment": False,
        "automatic_historical_continuity_judgment": False,
        "human_reviewed": False,
        "method": {
            "signal_base": SIGNAL_BASE,
            "graphemic_exact_component": 0.35,
            "graphemic_nonexact_component": "0.25 * SequenceMatcher ratio on conservative normalized forms",
            "internal_attestation_component": "min(0.15, log1p(count)/log(11)*0.15)",
            "reciprocal_support_component": "min(0.20, count*0.10)",
            "cap": 0.99,
            "buckets": {"high": ">=0.75", "medium": ">=0.50 and <0.75", "low": "<0.50"},
        },
        "summary": {
            "support_buckets": dict(sorted(buckets.items())),
            "exact_conservative_normalized_form_matches": exact,
        },
        "records": records,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"generated documentary-only machine scores for {len(records)} diachronic candidates -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
