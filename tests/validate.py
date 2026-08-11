#!/usr/bin/env python3
from pathlib import Path
import csv, json, sqlite3, xml.etree.ElementTree as ET, re, hashlib, sys
root=Path(__file__).resolve().parents[1]
errors=[]
rows=list(csv.DictReader((root/'data/entries.csv').open(encoding='utf-8')))
ids=[r['record_id'] for r in rows]
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
# derived formats
j=json.load((root/'data/json/entries.json').open(encoding='utf-8'))
if len(j)!=len(rows): errors.append('JSON count differs from CSV')
ET.parse(root/'data/xml/entries.xml')
ET.parse(root/'data/xml/steffel-1809-tei-machine.xml')
con=sqlite3.connect(root/'data/raramuri_historico.sqlite')
n=con.execute('select count(*) from entries').fetchone()[0]; con.close()
if n != len(rows): errors.append(f'sqlite count {n} != csv {len(rows)}')
public=json.load((root/'public/data/entries.json').open(encoding='utf-8'))
if len(public)!=len(rows): errors.append('public projection count differs from CSV')
# dictionary line audit layer must cover both directions
line_rows=list(csv.DictReader((root/'data/ocr_dictionary_lines.csv').open(encoding='utf-8')))
if not line_rows or {r['direction'] for r in line_rows}!={'DE-RAR','RAR-DE'}: errors.append('dictionary OCR line audit layer missing direction')
# source checksum if source file is present in repository
checks_path=root/'sources/checksums.json'
if checks_path.exists():
    for item in json.load(checks_path.open()):
        p=root/item['file']
        if p.exists():
            got=hashlib.sha256(p.read_bytes()).hexdigest()
            if got != item['sha256']: errors.append('checksum mismatch '+item['file'])
if errors:
    print('\n'.join('ERROR: '+e for e in errors)); sys.exit(1)
print(f"OK: {len(rows)} candidate entries; {len(cur)} persistent curated anchors; exports and audit layer agree")
