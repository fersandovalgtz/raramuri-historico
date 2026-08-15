#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys

ROOT=Path(__file__).resolve().parents[1]
MD=ROOT/"data/research/diachronic_machine_report.md"
CSV=ROOT/"data/research/diachronic_machine_report.csv"
CAL=ROOT/"data/research/diachronic_machine_calibration.json"
errors=[]
for p in (MD,CSV,CAL):
    if not p.exists(): errors.append(f"missing report artifact: {p.relative_to(ROOT)}")
if errors:
    print("\n".join("ERROR: "+e for e in errors)); sys.exit(1)

cal=json.loads(CAL.read_text(encoding="utf-8"))
with CSV.open(encoding="utf-8",newline="") as fh:
    rows=list(csv.DictReader(fh))
if len(rows)!=298: errors.append(f"CSV must contain 298 candidates, got {len(rows)}")
if len({r.get('semantic_context_id') for r in rows})!=298: errors.append("duplicate/missing candidate IDs in report CSV")
for r in rows:
    if r.get("relation_status")!="candidate": errors.append(f"{r.get('semantic_context_id')}: promoted beyond candidate")
    if r.get("scope")!="documentary_and_graphemic_retrieval_evidence_only": errors.append(f"{r.get('semantic_context_id')}: scope changed")
    if r.get("semantic_probability") not in {"",None}: errors.append(f"{r.get('semantic_context_id')}: semantic probability fabricated")
    if r.get("cognacy_probability") not in {"",None}: errors.append(f"{r.get('semantic_context_id')}: cognacy probability fabricated")
    if r.get("etymological_probability") not in {"",None}: errors.append(f"{r.get('semantic_context_id')}: etymological probability fabricated")
    if r.get("historical_continuity_probability") not in {"",None}: errors.append(f"{r.get('semantic_context_id')}: continuity probability fabricated")
    if str(r.get("human_reviewed")).lower() not in {"false","0"}: errors.append(f"{r.get('semantic_context_id')}: human review fabricated")

text=MD.read_text(encoding="utf-8")
if "298 relaciones candidatas" not in text: errors.append("Markdown report does not declare 298-candidate universe")
if str(cal.get("null_pair_count")) not in text: errors.append("Markdown report does not disclose null-pair count")
for phrase in ("no constituye", "identidad semántica", "cognación", "etimología", "continuidad histórica"):
    if phrase not in text: errors.append(f"Markdown epistemic guardrail missing: {phrase}")
for forbidden in ("cognado confirmado", "etimología confirmada", "ley fonológica demostrada", "continuidad histórica confirmada"):
    if forbidden in text.lower(): errors.append(f"forbidden overclaim in report: {forbidden}")
if text.count("| ") < 30: errors.append("Markdown prioritized table appears incomplete")

if errors:
    print("\n".join("ERROR: "+e for e in errors)); sys.exit(1)
print(f"OK: publishable diachronic report covers 298 candidates and {cal.get('null_pair_count')} null controls without semantic, cognacy, etymological or human-validation promotion")
