#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "dist/rhd-steffel-release-manifest.json"
errors = []

if not MANIFEST.exists():
    print("ERROR: release manifest missing")
    sys.exit(1)

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
if manifest.get("human_validation_claimed") is not False:
    errors.append("manifest must explicitly deny human-validation claim")
if "machine-only" not in (manifest.get("release_scope") or ""):
    errors.append("release scope does not declare machine-only edition")
files = manifest.get("files", [])
if len(files) < 15:
    errors.append(f"too few release artifacts: {len(files)}")
paths = [x.get("path") for x in files]
if len(paths) != len(set(paths)):
    errors.append("duplicate path in release manifest")

for item in files:
    rel = item.get("path")
    path = ROOT / str(rel)
    if not path.exists():
        errors.append(f"manifest path missing: {rel}")
        continue
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != item.get("sha256"):
        errors.append(f"sha256 mismatch: {rel}")
    if not re.fullmatch(r"[0-9a-f]{64}", item.get("sha256") or ""):
        errors.append(f"invalid sha256 format: {rel}")
    if path.stat().st_size != item.get("bytes"):
        errors.append(f"byte count mismatch: {rel}")

counts = manifest.get("counts", {})
canonical = ROOT / "data/canonical/steffel-1809.entries.jsonl"
canonical_count = sum(1 for line in canonical.read_text(encoding="utf-8").splitlines() if line.strip())
appendix = json.loads((ROOT / "data/canonical/steffel-1809.appendices.json").read_text(encoding="utf-8"))
appendix_count = len(appendix.get("objects", []))
if counts.get("canonical_lexical_records") != canonical_count:
    errors.append("canonical lexical record count mismatch")
if counts.get("canonical_appendix_objects") != appendix_count or appendix_count != 24:
    errors.append(f"canonical appendix object count mismatch: manifest={counts.get('canonical_appendix_objects')} actual={appendix_count}")
if counts.get("trilingual_formula_blocks") != 22:
    errors.append("release manifest must report 22 trilingual formula blocks")
if counts.get("appendix_facsimile_pages_mapped") != 6:
    errors.append("release manifest must report six mapped appendix facsimile pages")

completion = json.loads((ROOT / "project/completion-model-machine-only.json").read_text(encoding="utf-8"))
if manifest.get("completion", {}).get("weighted_completion_percent") != completion.get("weighted_completion_percent"):
    errors.append("completion percentage differs from machine-only completion model")

if errors:
    print("\n".join("ERROR: " + e for e in errors))
    sys.exit(1)
print(
    f"OK: release manifest verifies {len(files)} artifacts, {canonical_count} lexical records, "
    f"{appendix_count} canonical appendix objects, 22 formula blocks and six facsimile page mappings"
)
