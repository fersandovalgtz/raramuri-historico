#!/usr/bin/env python3
from pathlib import Path
import csv, json, sqlite3, xml.etree.ElementTree as ET, re, hashlib, sys
root=Path(__file__).resolve().parents[1]
errors=[]
rows=list(csv.DictReader((root/'data/entries_curated.csv').open(encoding='utf-8')))
ids=[r['record_id'] for r in rows]
if len(rows) != 60: errors.append(f'expected 60 starter entries, got {len(rows)}')
if len(ids)!=len(set(ids)): errors.append('duplicate record_id')
for r in rows:
    if not re.fullmatch(r'RHD-S1809-\d{5}',r['record_id']): errors.append('bad id '+r['record_id'])
    if r['direction'] not in {'DE-RAR','RAR-DE'}: errors.append('bad direction '+r['record_id'])
    if not r['headword_raw'].strip(): errors.append('empty headword '+r['record_id'])
    if not (301 <= int(r['printed_page']) <= 374): errors.append('bad printed page '+r['record_id'])

j=json.load((root/'data/json/entries_curated.json').open(encoding='utf-8'))
if len(j)!=len(rows): errors.append('JSON count differs from CSV')
ET.parse(root/'data/xml/entries_curated.xml')
ET.parse(root/'data/xml/steffel-1809-tei-draft.xml')
con=sqlite3.connect(root/'data/raramuri_historico.sqlite')
n=con.execute('select count(*) from entries').fetchone()[0]; con.close()
if n != len(rows): errors.append(f'sqlite count {n} != csv {len(rows)}')
public=json.load((root/'public/data/entries.json').open(encoding='utf-8'))
if len(public)!=len(rows): errors.append('public projection count differs from CSV')

checks_path=root/'sources/checksums.json'
if checks_path.exists():
    for item in json.load(checks_path.open()):
        p=root/item['file']
        if p.exists():
            got=hashlib.sha256(p.read_bytes()).hexdigest()
            if got != item['sha256']: errors.append('checksum mismatch '+item['file'])

if errors:
    print('\n'.join('ERROR: '+e for e in errors)); sys.exit(1)
print(f'OK: {len(rows)} canonical entries; derived exports parse and counts agree')
