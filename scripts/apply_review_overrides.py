#!/usr/bin/env python3
"""Apply facsimile-review overlays to the machine candidate layer.

Review manifests are append-only editorial evidence. Machine candidates keep
their persistent record_id even when rejected, so later identifiers never shift.
A facsimile headword review does not imply diplomatic or linguistic validation.
"""
from pathlib import Path
import csv, json, re, unicodedata

ROOT = Path(__file__).resolve().parents[1]
ENTRIES = ROOT / "data" / "entries.csv"
REVIEW_DIR = ROOT / "data" / "review"
INVENTORY = ROOT / "data" / "corpus_inventory.json"

def search_key(s: str) -> str:
    s = (s.replace('ſ','s').replace('ß','ss').replace('⸗','-')
           .replace('ä','ae').replace('Ä','Ae').replace('ö','oe').replace('Ö','Oe')
           .replace('ü','ue').replace('Ü','Ue'))
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = re.sub(r'[^0-9A-Za-z ]+', ' ', s.casefold())
    return re.sub(r'\s+', ' ', s).strip()

rows = list(csv.DictReader(ENTRIES.open(encoding="utf-8")))
if not rows:
    raise SystemExit("data/entries.csv is empty")
fieldnames = list(rows[0].keys())
by_id = {r["record_id"]: r for r in rows}

reviewed = accepted = rejected = corrections = 0
seen = set()

for path in sorted(REVIEW_DIR.glob("facsimile_review_batch_*.json")):
    manifest = json.load(path.open(encoding="utf-8"))
    batch = manifest["batch_id"]
    rejection_map = manifest.get("rejections", {})
    correction_map = manifest.get("corrections", {})
    note_map = manifest.get("notes", {})
    scope = manifest.get("review_scope", "")
    method = manifest.get("review_method", "")

    for item in manifest.get("records", []):
        rid, printed_page = item
        if rid in seen:
            raise SystemExit(f"duplicate review override for {rid}")
        seen.add(rid)
        reviewed += 1
        if rid not in by_id:
            raise SystemExit(f"review record_id not found in entries.csv: {rid}")
        r = by_id[rid]
        r["printed_page"] = str(printed_page)
        r["pdf_page"] = str(int(printed_page) - 290)

        note_parts = [r.get("editorial_note", "").strip()]
        if rid in rejection_map:
            rejected += 1
            info = rejection_map[rid]
            review_note = info.get("note", "").strip()
            if review_note:
                note_parts.append(review_note)
            r["status"] = "rejected_false_positive"
            r["validation"] = "rechazado_como_límite_lexicográfico_tras_cotejo_facsímil_ai_asistido"
        else:
            accepted += 1
            if rid in correction_map:
                corrections += 1
                info = correction_map[rid]
                corrected = info["corrected_headword"].strip()
                r["headword_raw"] = corrected
                r["headword_search"] = search_key(corrected)
                review_note = info.get("note", "").strip()
                if review_note:
                    note_parts.append(review_note)
            if rid in note_map and note_map[rid].strip():
                note_parts.append(note_map[rid].strip())
            r["status"] = "facsimile_checked_headword_ai_assisted"
            r["validation"] = (
                "cotejo_facsímil_de_lema_y_arranque_de_artículo_ai_asistido;"
                "transcripción_diplomática_y_validación_lingüística_pendientes"
            )

        note_parts.append(f"{batch}: {method}; scope={scope}; exact_page={printed_page}.")
        r["editorial_note"] = " ".join(x for x in note_parts if x)

with ENTRIES.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(rows)

inv = json.load(INVENTORY.open(encoding="utf-8"))
inv["facsimile_review"] = {
    "reviewed_candidate_boundaries": reviewed,
    "accepted_headword_starts": accepted,
    "rejected_false_positive_boundaries": rejected,
    "headword_corrections": corrections,
    "active_candidates_after_review": len(rows) - rejected,
    "scope": "headword_and_entry_start_boundary",
    "method": "visual_facsimile_collation_ai_assisted",
    "full_diplomatic_transcription_completed": False
}
INVENTORY.write_text(json.dumps(inv, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Applied {reviewed} reviews: {accepted} accepted, {rejected} rejected, {corrections} corrections")
