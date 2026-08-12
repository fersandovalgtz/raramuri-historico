#!/usr/bin/env python3
"""Apply facsimile-review and diplomatic-transcription overlays.

Editorial manifests are append-only evidence. Machine candidates keep persistent
record IDs even when a boundary is rejected. AI-assisted editorial review is kept
explicitly distinct from human/philological verification, and heterogeneous
review methods are preserved rather than collapsed into a single visual claim.
"""
from pathlib import Path
import csv, json, re, unicodedata

ROOT = Path(__file__).resolve().parents[1]
ENTRIES = ROOT / "data" / "entries.csv"
REVIEW_DIR = ROOT / "data" / "review"
DIPLOMATIC_DIR = ROOT / "data" / "diplomatic"
INVENTORY = ROOT / "data" / "corpus_inventory.json"

DIP_FIELDS = [
    "facsimile_column","headword_diplomatic","article_diplomatic",
    "diplomatic_status","diplomatic_batch","diplomatic_note",
    "human_verified","diplomatic_review_method"
]

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
for f in DIP_FIELDS:
    if f not in fieldnames:
        fieldnames.append(f)
for r in rows:
    for f in DIP_FIELDS:
        r.setdefault(f, "")
by_id = {r["record_id"]: r for r in rows}

reviewed = accepted = rejected = corrections = 0
seen = set()
review_methods = set()
review_direct_image_pending_batches = []

for path in sorted(REVIEW_DIR.glob("facsimile_review_batch_*.json")):
    manifest = json.load(path.open(encoding="utf-8"))
    batch = manifest["batch_id"]
    rejection_map = manifest.get("rejections", {})
    correction_map = manifest.get("corrections", {})
    note_map = manifest.get("notes", {})
    scope = manifest.get("review_scope", "")
    method = manifest.get("review_method", "")
    if method:
        review_methods.add(method)
    if manifest.get("direct_facsimile_image_reinspection") is False:
        review_direct_image_pending_batches.append(batch)

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
            r["validation"] = "rechazado_como_límite_lexicográfico_tras_revisión_editorial_ai_asistida"
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
            if rid in note_map and isinstance(note_map[rid], str) and note_map[rid].strip():
                note_parts.append(note_map[rid].strip())
            r["status"] = "facsimile_checked_headword_ai_assisted"
            r["validation"] = (
                "revisión_editorial_de_lema_y_arranque_de_artículo_ai_asistida;"
                "transcripción_diplomática_y_validación_lingüística_pendientes"
            )

        note_parts.append(f"{batch}: {method}; scope={scope}; exact_page={printed_page}.")
        if manifest.get("direct_facsimile_image_reinspection") is False:
            note_parts.append("Direct facsimile image re-collation pending for this batch.")
        r["editorial_note"] = " ".join(x for x in note_parts if x)

dip_count = 0
dip_batches = []
dip_pages = set()
dip_uncertain = 0
dip_seen = set()
dip_methods = set()
dip_direct_image_pending_batches = []
for path in sorted(DIPLOMATIC_DIR.glob("diplomatic_batch_*.json")):
    manifest = json.load(path.open(encoding="utf-8"))
    batch = manifest["batch_id"]
    method = manifest.get("review_method", "")
    human_verified = bool(manifest.get("human_verified", False))
    dip_batches.append(batch)
    if method:
        dip_methods.add(method)
    if manifest.get("direct_facsimile_image_reinspection") is False:
        dip_direct_image_pending_batches.append(batch)
    for item in manifest.get("records", []):
        rid = item["record_id"]
        if rid in dip_seen:
            raise SystemExit(f"duplicate diplomatic override for {rid}")
        dip_seen.add(rid)
        if rid not in by_id:
            raise SystemExit(f"diplomatic record_id not found in entries.csv: {rid}")
        r = by_id[rid]
        if r.get("status") == "rejected_false_positive":
            raise SystemExit(f"diplomatic overlay targets rejected boundary: {rid}")
        page = int(item["printed_page"])
        r["printed_page"] = str(page)
        r["pdf_page"] = str(int(item.get("pdf_page", page - 290)))
        r["facsimile_column"] = item.get("column", "")
        r["headword_diplomatic"] = item.get("headword_diplomatic", "").strip()
        r["article_diplomatic"] = item.get("article_diplomatic", "").strip()
        r["diplomatic_status"] = item.get("transcription_status", "complete_ai_assisted")
        r["diplomatic_batch"] = batch
        r["diplomatic_note"] = item.get("uncertainty_note", "").strip()
        r["human_verified"] = "true" if human_verified else "false"
        r["diplomatic_review_method"] = method
        r["status"] = "diplomatic_transcription_ai_assisted"
        r["validation"] = (
            "transcripción_diplomática_ai_asistida;"
            "pendiente_de_validación_humana_y_lingüística"
        )
        if manifest.get("direct_facsimile_image_reinspection") is False:
            extra = "Direct facsimile image re-collation pending for this diplomatic batch."
            r["diplomatic_note"] = " ".join(x for x in (r["diplomatic_note"], extra) if x)
        dip_count += 1
        dip_pages.add(page)
        if r["diplomatic_note"]:
            dip_uncertain += 1

with ENTRIES.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(rows)

inv = json.load(INVENTORY.open(encoding="utf-8"))
review_methods_sorted = sorted(review_methods)
dip_methods_sorted = sorted(dip_methods)
inv["facsimile_review"] = {
    "reviewed_candidate_boundaries": reviewed,
    "accepted_headword_starts": accepted,
    "rejected_false_positive_boundaries": rejected,
    "headword_corrections": corrections,
    "active_candidates_after_review": len(rows) - rejected,
    "scope": "headword_and_entry_start_boundary",
    "method": review_methods_sorted[0] if len(review_methods_sorted) == 1 else "mixed_ai_assisted_editorial_collation",
    "methods": review_methods_sorted,
    "direct_facsimile_image_recheck_pending_batches": review_direct_image_pending_batches,
    "full_diplomatic_transcription_completed": False
}
inv["diplomatic_transcription"] = {
    "batches": dip_batches,
    "complete_article_transcriptions_ai_assisted": dip_count,
    "pages_represented": sorted(dip_pages),
    "records_with_uncertainty_note": dip_uncertain,
    "method": dip_methods_sorted[0] if len(dip_methods_sorted) == 1 else "mixed_ai_assisted_diplomatic_transcription",
    "methods": dip_methods_sorted,
    "direct_facsimile_image_recheck_pending_batches": dip_direct_image_pending_batches,
    "human_verified": False,
    "scope_note": "Complete article text for accepted records; source spelling/punctuation retained where supported; typographic line wrapping not encoded. Batches without direct facsimile image reinspection are explicitly flagged for later re-collation."
}
INVENTORY.write_text(json.dumps(inv, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(
    f"Applied {reviewed} boundary reviews: {accepted} accepted, {rejected} rejected, "
    f"{corrections} corrections; {dip_count} complete AI-assisted diplomatic articles; "
    f"direct-image recheck pending review batches={review_direct_image_pending_batches}"
)
