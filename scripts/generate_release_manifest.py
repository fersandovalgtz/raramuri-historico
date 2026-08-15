#!/usr/bin/env python3
"""Generate a deterministic integrity manifest for the Steffel machine-only scholarly release."""

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "dist"
OUT = OUT_DIR / "rhd-steffel-release-manifest.json"

FILES = [
    ("source_ocr", "sources/steffel-1809-ocr-source.txt"),
    ("source_checksums", "sources/checksums.json"),
    ("master_entries", "data/entries.csv"),
    ("corpus_inventory", "data/corpus_inventory.json"),
    ("canonical_jsonl", "data/canonical/steffel-1809.entries.jsonl"),
    ("canonical_appendices", "data/canonical/steffel-1809.appendices.json"),
    ("diachronic_machine_scores", "data/research/diachronic_machine_scores.json"),
    ("tei_rich", "data/tei/rhd-steffel-1809-tei.xml"),
    ("tei_lex0", "data/tei/rhd-steffel-1809-lex0.xml"),
    ("appendix_numeration", "data/appendices/numeration_ocr_candidates.json"),
    ("appendix_trilingual", "data/appendices/trilingual_sample_ocr_candidates.json"),
    ("appendix_facsimile_map", "data/appendices/facsimile_page_map.json"),
    ("canonical_schema", "schemas/rhd-entry-1.0.schema.json"),
    ("source_profile", "source_profiles/steffel-1809.source.json"),
    ("machine_only_policy", "docs/MACHINE_ONLY_SCIENTIFIC_POLICY.md"),
    ("completion_model", "project/completion-model-machine-only.json"),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    records = []
    missing = []
    for role, rel in FILES:
        path = ROOT / rel
        if not path.exists():
            missing.append(rel)
            continue
        records.append(
            {
                "role": role,
                "path": rel,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    if missing:
        raise SystemExit("release manifest cannot be generated; missing: " + ", ".join(missing))

    canonical = ROOT / "data/canonical/steffel-1809.entries.jsonl"
    canonical_rows = [line for line in canonical.read_text(encoding="utf-8").splitlines() if line.strip()]
    appendix_source = read_json(ROOT / "data/appendices/trilingual_sample_ocr_candidates.json")
    appendix_canonical = read_json(ROOT / "data/canonical/steffel-1809.appendices.json")
    diachronic = read_json(ROOT / "data/research/diachronic_machine_scores.json")
    completion = read_json(ROOT / "project/completion-model-machine-only.json")
    page_map = read_json(ROOT / "data/appendices/facsimile_page_map.json")

    manifest = {
        "manifest_id": "RHD-STEFFEL-MACHINE-ONLY-RELEASE-MANIFEST-1",
        "generated_from": "repository working tree",
        "release_scope": "machine-only historical-digital scholarly edition; zero required human adjudication",
        "human_validation_claimed": False,
        "counts": {
            "canonical_lexical_records": len(canonical_rows),
            "canonical_appendix_objects": len(appendix_canonical.get("objects", [])),
            "trilingual_formula_blocks": appendix_source.get("formula_count"),
            "appendix_facsimile_pages_mapped": len(page_map.get("mapping", [])),
            "diachronic_documentary_candidates_scored": diachronic.get("count"),
        },
        "completion": {
            "weighted_completion_percent": completion.get("weighted_completion_percent"),
            "weighted_remaining_percent": completion.get("weighted_remaining_percent"),
        },
        "files": records,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"generated release integrity manifest with {len(records)} hashed artifacts -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
