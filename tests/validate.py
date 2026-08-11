#!/usr/bin/env python3
from pathlib import Path
import csv, json, sqlite3, xml.etree.ElementTree as ET, re, hashlib, sys
root=Path(__file__).resolve().parents[1]
errors=[]
rows=list(csv.DictReader((root/'data/entries.csv').open(encoding='utf-8')))
ids=[r['record_id'] for r in rows]
by_id={r['record_id']:r for r in rows}
inv=json.load((root/'data/corpus_inventory.json').open(encoding='utf-8'))
if len(rows) != inv['candidate_entries_total']: errors.append(f"entries {len(rows)} != inventory {inv['candidate_entries_total']}")
if len(rows) < 1000: errors.append(f'implausibly small integral candidate layer: {len(rows)}')
if len(ids)!=len(set(ids)): errors.append('duplicate record_id')
for r in rows:
    if not re.fullmatch(r'RHD-S1809-\d{5}',r['record_id']): errors.append('bad id '+r['record_id'])
    if r['direction'] not in {'DE-RAR','RAR-DE'}: errors.append('bad direction '+r['record_id'])
    if not r['headword_raw'].strip(): errors.append('empty headword '+r['record_id'])
    if r['segmentation_confidence'] not in {'curated_anchor','high_machine','medium_machine','low_machine'}: errors.append('bad confidence '+r['record_id'])
    if not (301 <= int(r['printed_page']) <= 369): errors.append('bad dictionary printed page '+r['record_id'])
    if int(r['source_ocr_line_end']) < int(r['source_ocr_line_start']): errors.append('bad line range '+r['record_id'])

cur=[r for r in rows if r['curated_anchor']=='yes']
if len(cur)!=60: errors.append(f'expected 60 curated anchors, got {len(cur)}')
expected={f'RHD-S1809-{i:05d}' for i in range(1,61)}
if {r['record_id'] for r in cur} != expected: errors.append('curated persistent IDs 00001–00060 were not preserved exactly')

review_paths=sorted((root/'data/review').glob('facsimile_review_batch_*.json'))
reviewed_ids=[]
rejected_ids=set()
for p in review_paths:
    m=json.load(p.open(encoding='utf-8'))
    recs=m.get('records',[])
    if m.get('summary',{}).get('reviewed') != len(recs): errors.append(f'review summary mismatch in {p.name}')
    for rid,page in recs:
        reviewed_ids.append(rid)
        if rid not in by_id: errors.append(f'review id missing from entries: {rid}')
        elif int(by_id[rid]['printed_page']) != int(page): errors.append(f'exact page override missing for {rid}')
    rejected_ids.update(m.get('rejections',{}).keys())
if len(reviewed_ids)!=len(set(reviewed_ids)): errors.append('duplicate reviewed record_id across review batches')
for rid in reviewed_ids:
    if rid in by_id:
        if rid in rejected_ids and by_id[rid]['status']!='rejected_false_positive': errors.append(f'rejected review not applied: {rid}')
        if rid not in rejected_ids and by_id[rid]['status']!='facsimile_checked_headword_ai_assisted': errors.append(f'accepted facsimile review not applied: {rid}')
fr=inv.get('facsimile_review',{})
if reviewed_ids:
    if fr.get('reviewed_candidate_boundaries') != len(reviewed_ids): errors.append('inventory reviewed count mismatch')
    if fr.get('rejected_false_positive_boundaries') != len(rejected_ids): errors.append('inventory rejection count mismatch')
    if fr.get('active_candidates_after_review') != len(rows)-len(rejected_ids): errors.append('inventory active count mismatch')
    expected_corrections={'RHD-S1809-00072':'Allmächtig','RHD-S1809-00396':'Eingraben','RHD-S1809-00472':'Faſttag','RHD-S1809-00509':'Fledermaus'}
    for rid,head in expected_corrections.items():
        if by_id.get(rid,{}).get('headword_raw') != head: errors.append(f'facsimile headword correction missing: {rid}')

j=json.load((root/'data/json/entries.json').open(encoding='utf-8'))
if len(j)!=len(rows): errors.append('JSON count differs from CSV')
ET.parse(root/'data/xml/entries.xml')
ET.parse(root/'data/xml/steffel-1809-tei-machine.xml')
con=sqlite3.connect(root/'data/raramuri_historico.sqlite')
n=con.execute('select count(*) from entries').fetchone()[0]; con.close()
if n != len(rows): errors.append(f'sqlite count {n} != csv {len(rows)}')
public=json.load((root/'public/data/entries.json').open(encoding='utf-8'))
if len(public)!=len(rows): errors.append('public projection count differs from CSV')
line_rows=list(csv.DictReader((root/'data/ocr_dictionary_lines.csv').open(encoding='utf-8')))
if not line_rows or {r['direction'] for r in line_rows}!={'DE-RAR','RAR-DE'}: errors.append('dictionary OCR line audit layer missing direction')
checks_path=root/'sources/checksums.json'
if checks_path.exists():
    for item in json.load(checks_path.open()):
        p=root/item['file']
        if p.exists():
            got=hashlib.sha256(p.read_bytes()).hexdigest()
            if got != item['sha256']: errors.append('checksum mismatch '+item['file'])
if errors:
    print('\n'.join('ERROR: '+e for e in errors)); sys.exit(1)
print(f"OK: {len(rows)} candidates; {len(reviewed_ids)} facsimile-reviewed boundaries; {len(rejected_ids)} rejected; exports agree")
