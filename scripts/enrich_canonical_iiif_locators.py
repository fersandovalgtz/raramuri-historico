#!/usr/bin/env python3
"""Add deterministic page-level IIIF Canvas locators to generated Steffel canonical records."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
CANON=ROOT/"data/canonical/steffel-1809.entries.jsonl"
SUMMARY=ROOT/"data/canonical/steffel-1809.iiif-linkage-summary.json"
BASE="https://fersandovalgtz.github.io/raramuri-historico/iiif/steffel-1809"
MANIFEST=f"{BASE}/manifest.json"

def canvas(page): return f"{BASE}/canvas/p{page:03d}"

def main():
    rows=[json.loads(line) for line in CANON.read_text(encoding="utf-8").splitlines() if line.strip()]
    mapped=0; active=0; active_mapped=0; active_missing=[]; invalid_pages=[]
    for r in rows:
        loc=r.setdefault("locators",{})
        page=loc.get("digital_page")
        if r.get("status")=="active": active+=1
        if isinstance(page,int) and 1<=page<=84:
            loc["iiif_canvas"]=canvas(page)
            loc["iiif_target"]=canvas(page)
            mapped+=1
            if r.get("status")=="active": active_mapped+=1
        elif page is None:
            loc["iiif_canvas"]=None; loc["iiif_target"]=None
            if r.get("status")=="active": active_missing.append(r.get("record_id"))
        else:
            invalid_pages.append({"record_id":r.get("record_id"),"digital_page":page})
    CANON.write_text("".join(json.dumps(r,ensure_ascii=False,sort_keys=True)+"\n" for r in rows),encoding="utf-8")
    summary={"linkage_id":"RHD-STEFFEL-1809-IIIF-LINKAGE-1","manifest_id":MANIFEST,"records_total":len(rows),"records_canvas_mapped":mapped,"active_records":active,"active_records_canvas_mapped":active_mapped,"active_records_without_digital_page":active_missing,"invalid_digital_pages":invalid_pages,"linkage_level":"page_canvas","region_targets_generated":0,"human_validation_claimed":False}
    SUMMARY.write_text(json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("RHD_IIIF_LINKAGE="+json.dumps({"records":len(rows),"mapped":mapped,"active":active,"active_mapped":active_mapped,"active_missing":len(active_missing),"invalid_pages":len(invalid_pages)},sort_keys=True))
if __name__=="__main__": main()
