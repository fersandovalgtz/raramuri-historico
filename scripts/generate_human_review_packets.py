#!/usr/bin/env python3
"""Prepare non-adjudicative human-review packets from the canonical RHD layer.

The script never fills reviewer decisions. It packages the source evidence, PHIL history,
priority route and a blank decision form so independent specialists can review efficiently.
"""

from pathlib import Path
from collections import defaultdict
import json

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data" / "canonical" / "steffel-1809.entries.jsonl"
PRIORITY = ROOT / "data" / "validation" / "human_review_priority_compact.json"
OUT = ROOT / "data" / "validation" / "human_review_packets"
BATCH_SIZE = 10


def load_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def blank_decision():
    return {
        "reviewer": {
            "name": None,
            "affiliation": None,
            "orcid": None,
            "competence": [],
        },
        "review_date": None,
        "philological_decision": "not_assessed",
        "adopted_reading": None,
        "linguistic_decision": "not_assessed",
        "semantic_historical_decision": "not_assessed",
        "disciplinary_decision": "not_assessed",
        "relation_to_ai_proposal": "not_applicable",
        "confidence": None,
        "evidence": [],
        "justification": None,
        "human_verified": False,
    }


def main():
    canonical = {x["record_id"]: x for x in load_jsonl(CANONICAL)}
    priority = json.loads(PRIORITY.read_text(encoding="utf-8"))
    grouped = defaultdict(list)

    for raw in priority["records"]:
        priority_number, rid, printed_page, disposition, review_route = raw
        item = canonical[rid]
        grouped[priority_number].append(
            {
                "record_id": rid,
                "printed_page": printed_page,
                "priority": priority_number,
                "ai_disposition": disposition,
                "recommended_review_route": review_route,
                "documentary_evidence": {
                    "direction": item.get("direction"),
                    "locators": item.get("locators"),
                    "ocr": item.get("layers", {}).get("ocr_raw"),
                    "diplomatic": item.get("layers", {}).get("diplomatic"),
                    "editorial_notes": item.get("notes", []),
                },
                "ai_philological_history": [
                    event
                    for event in item.get("validation", [])
                    if event.get("scope") == "philological" and event.get("reviewer_type") == "ai_assisted"
                ],
                "diachronic_candidates_for_context_only": item.get("historical_relations", []),
                "independent_review": blank_decision(),
            }
        )

    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {
        "stage": "independent_human_review_packets",
        "source": "Rarámuri Histórico Digital — Steffel 1791/1809",
        "policy": "Packets contain evidence and blank decision structures only; no human decision is inferred or prefilled.",
        "batch_size": BATCH_SIZE,
        "priority_counts": {},
        "packets": [],
    }

    for priority_number in sorted(grouped):
        records = grouped[priority_number]
        manifest["priority_counts"][str(priority_number)] = len(records)
        for index in range(0, len(records), BATCH_SIZE):
            chunk = records[index:index + BATCH_SIZE]
            packet_no = index // BATCH_SIZE + 1
            filename = f"priority_{priority_number}_packet_{packet_no:02d}.json"
            payload = {
                "priority": priority_number,
                "packet": packet_no,
                "count": len(chunk),
                "human_reviewed": False,
                "instructions": [
                    "Review against the facsimile evidence independently of the AI disposition.",
                    "Declare only the scopes actually assessed.",
                    "remain_unresolved / not_assessed are valid outcomes.",
                    "Do not infer cognacy, morphology or historical continuity from graphic similarity alone.",
                ],
                "records": chunk,
            }
            (OUT / filename).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            manifest["packets"].append({"file": filename, "priority": priority_number, "count": len(chunk)})

    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"generated {len(manifest['packets'])} human-review packets for {sum(manifest['priority_counts'].values())} records")


if __name__ == "__main__":
    main()
