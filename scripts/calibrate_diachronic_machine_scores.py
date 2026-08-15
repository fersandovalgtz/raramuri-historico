#!/usr/bin/env python3
"""Calibrate RHD diachronic retrieval evidence against deterministic null pairings.

This script measures only graphemic retrieval specificity. It does NOT estimate
semantic identity, cognacy, etymology or historical continuity. The 298 observed
historical-modern pairings are compared with circularly shifted modern-form pairings
from the same candidate universe. Thus the null controls preserve the same marginal
form inventory while breaking the observed pairing structure.
"""

from pathlib import Path
from statistics import mean, median
import json

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/research/diachronic_machine_scores.json"
OUT = ROOT / "data/research/diachronic_machine_calibration.json"

SHIFTS = [1, 7, 13, 23, 37, 53, 71, 97, 127, 149, 173, 191, 211, 229, 251, 269, 281]


def ratio(a, b):
    # Reuse the exact conservative normalization and SequenceMatcher semantics from the
    # scoring layer without importing it (keeps this artifact self-describing).
    from difflib import SequenceMatcher
    import unicodedata

    def norm(value):
        value = (value or "").replace("ſ", "s").replace("ß", "ss")
        value = unicodedata.normalize("NFKD", value.casefold())
        return "".join(ch for ch in value if ch.isalpha() and not unicodedata.combining(ch))

    a2, b2 = norm(a), norm(b)
    return SequenceMatcher(None, a2, b2).ratio() if a2 and b2 else 0.0


def quantile(values, p):
    if not values:
        return None
    vals = sorted(values)
    idx = round((len(vals) - 1) * p)
    return round(vals[max(0, min(len(vals) - 1, idx))], 6)


def main():
    payload = json.loads(INPUT.read_text(encoding="utf-8"))
    records = payload.get("records", [])
    if len(records) != 298:
        raise SystemExit(f"ERROR: expected 298 diachronic candidates, got {len(records)}")

    observed = [float(r.get("graphemic", {}).get("sequence_ratio") or 0.0) for r in records]
    modern_forms = [r.get("modern_form") for r in records]
    historical_forms = [r.get("historical_form") for r in records]

    null_by_shift = []
    null_all = []
    n = len(records)
    for shift in SHIFTS:
        shifted = [ratio(historical_forms[i], modern_forms[(i + shift) % n]) for i in range(n)]
        null_all.extend(shifted)
        null_by_shift.append({
            "shift": shift,
            "pair_count": n,
            "mean_sequence_ratio": round(mean(shifted), 6),
            "median_sequence_ratio": round(median(shifted), 6),
            "p90_sequence_ratio": quantile(shifted, 0.90),
        })

    null_sorted = sorted(null_all)
    calibrated = []
    for record, obs in zip(records, observed):
        ge = sum(v >= obs for v in null_all)
        tail = (ge + 1) / (len(null_all) + 1)
        percentile = sum(v <= obs for v in null_all) / len(null_all)
        if percentile >= 0.95:
            specificity = "very_high_graphemic_specificity"
        elif percentile >= 0.80:
            specificity = "high_graphemic_specificity"
        elif percentile >= 0.50:
            specificity = "moderate_graphemic_specificity"
        else:
            specificity = "low_graphemic_specificity"
        calibrated.append({
            "semantic_context_id": record.get("semantic_context_id"),
            "source_candidate_id": record.get("source_candidate_id"),
            "historical_record_id": record.get("historical_record_id"),
            "modern_record_id": record.get("modern_record_id"),
            "historical_form": record.get("historical_form"),
            "modern_form": record.get("modern_form"),
            "observed_sequence_ratio": round(obs, 6),
            "null_empirical_percentile": round(percentile, 6),
            "null_empirical_upper_tail": round(tail, 6),
            "graphemic_specificity_bucket": specificity,
            "relation_status": "candidate",
            "calibration_scope": "graphemic_retrieval_specificity_only",
            "semantic_probability": None,
            "cognacy_probability": None,
            "etymological_probability": None,
            "historical_continuity_probability": None,
            "human_reviewed": False,
        })

    observed_mean = mean(observed)
    null_mean = mean(null_all)
    summary_buckets = {}
    for r in calibrated:
        summary_buckets[r["graphemic_specificity_bucket"]] = summary_buckets.get(r["graphemic_specificity_bucket"], 0) + 1

    out = {
        "dataset": "raramuri-historico-steffel-1809",
        "layer": "diachronic_machine_graphemic_calibration",
        "candidate_count": len(records),
        "null_pair_count": len(null_all),
        "null_control_design": "17 deterministic circular shifts of the same modern-form inventory",
        "shifts": SHIFTS,
        "scope": "graphemic_retrieval_specificity_only",
        "automatic_semantic_judgment": False,
        "automatic_cognacy_judgment": False,
        "automatic_etymological_judgment": False,
        "automatic_historical_continuity_judgment": False,
        "human_reviewed": False,
        "summary": {
            "observed_mean_sequence_ratio": round(observed_mean, 6),
            "observed_median_sequence_ratio": round(median(observed), 6),
            "observed_p90_sequence_ratio": quantile(observed, 0.90),
            "null_mean_sequence_ratio": round(null_mean, 6),
            "null_median_sequence_ratio": round(median(null_all), 6),
            "null_p90_sequence_ratio": quantile(null_all, 0.90),
            "mean_ratio_lift_over_null": round(observed_mean - null_mean, 6),
            "candidate_specificity_buckets": dict(sorted(summary_buckets.items())),
        },
        "null_by_shift": null_by_shift,
        "records": calibrated,
        "interpretation_guardrail": "A high empirical graphemic specificity score means only that the observed spelling/form pairing is unusually similar relative to deterministic broken-pair controls from this candidate set. It is not evidence by itself of semantic identity, cognacy, etymology, sound law or historical continuity."
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"calibrated {len(records)} candidates against {len(null_all)} deterministic null pairings; "
        f"observed mean={observed_mean:.4f}, null mean={null_mean:.4f}, lift={observed_mean-null_mean:.4f}"
    )


if __name__ == "__main__":
    main()
