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
allowed_accepted_statuses={'facsimile_checked_headword_ai_assisted','diplomatic_transcription_ai_assisted'}
for rid in reviewed_ids:
    if rid in by_id:
        if rid in rejected_ids and by_id[rid]['status']!='rejected_false_positive': errors.append(f'rejected review not applied: {rid}')
        if rid not in rejected_ids and by_id[rid]['status'] not in allowed_accepted_statuses: errors.append(f'accepted facsimile review not applied: {rid}')
fr=inv.get('facsimile_review',{})
if reviewed_ids:
    if fr.get('reviewed_candidate_boundaries') != len(reviewed_ids): errors.append('inventory reviewed count mismatch')
    if fr.get('rejected_false_positive_boundaries') != len(rejected_ids): errors.append('inventory rejection count mismatch')
    if fr.get('active_candidates_after_review') != len(rows)-len(rejected_ids): errors.append('inventory active count mismatch')
    expected_corrections={'RHD-S1809-00072':'Allmächtig','RHD-S1809-00396':'Eingraben','RHD-S1809-00472':'Faſttag','RHD-S1809-00509':'Fledermaus'}
    for rid,head in expected_corrections.items():
        if by_id.get(rid,{}).get('headword_raw') != head: errors.append(f'facsimile headword correction missing: {rid}')

layout_path=root/'data/facsimile/page_layout_301_317.csv'
layout_rows=list(csv.DictReader(layout_path.open(encoding='utf-8'))) if layout_path.exists() else []
if len(layout_rows)!=34:
    errors.append(f'expected 34 page-column layout records, got {len(layout_rows)}')
else:
    pairs={(int(r['printed_page']),r['column']) for r in layout_rows}
    expected_pairs={(p,c) for p in range(301,318) for c in ('left','right')}
    if pairs != expected_pairs: errors.append('page-layout coverage is not exactly pages 301–317 x left/right')
    if any(r.get('human_verified','').lower()!='false' for r in layout_rows): errors.append('AI-assisted page-layout rows must not claim human verification')

dip_paths=sorted((root/'data/diplomatic').glob('diplomatic_batch_*.json'))
dip_ids=[]
for p in dip_paths:
    m=json.load(p.open(encoding='utf-8'))
    if m.get('human_verified') is not False: errors.append(f'{p.name} must explicitly be human_verified=false')
    recs=m.get('records',[])
    if m.get('summary',{}).get('complete_article_transcriptions') != len(recs): errors.append(f'diplomatic summary mismatch in {p.name}')
    for item in recs:
        rid=item['record_id']; dip_ids.append(rid)
        if rid not in by_id:
            errors.append(f'diplomatic id missing from entries: {rid}'); continue
        r=by_id[rid]
        if rid in rejected_ids: errors.append(f'diplomatic overlay targets rejected id: {rid}')
        if r.get('status')!='diplomatic_transcription_ai_assisted': errors.append(f'diplomatic status not applied: {rid}')
        if r.get('headword_diplomatic','') != item.get('headword_diplomatic',''): errors.append(f'diplomatic headword mismatch: {rid}')
        if r.get('article_diplomatic','') != item.get('article_diplomatic',''): errors.append(f'diplomatic article mismatch: {rid}')
        if r.get('facsimile_column','') not in {'left','right'}: errors.append(f'missing facsimile column: {rid}')
        if r.get('human_verified','').lower()!='false': errors.append(f'diplomatic record incorrectly claims human verification: {rid}')
        if int(r['printed_page']) != int(item['printed_page']): errors.append(f'diplomatic page mismatch: {rid}')
        note=(r.get('diplomatic_note') or '').strip()
        state=r.get('diplomatic_note_state','')
        if not note and state!='none': errors.append(f'empty diplomatic note must have state none: {rid}')
        if note and state not in {'resolved_editorial_note','open_validation'}: errors.append(f'non-empty diplomatic note has invalid state: {rid}')
if len(dip_ids)!=len(set(dip_ids)): errors.append('duplicate diplomatic record_id across batches')
di=inv.get('diplomatic_transcription',{})
if dip_ids:
    if di.get('complete_article_transcriptions_ai_assisted') != len(dip_ids): errors.append('inventory diplomatic count mismatch')
    if di.get('human_verified') is not False: errors.append('inventory diplomatic layer must state human_verified=false')
    note_rows=[r for r in rows if r.get('status')!='rejected_false_positive' and r.get('diplomatic_status')=='complete_ai_assisted' and (r.get('diplomatic_note') or '').strip()]
    open_rows=[r for r in note_rows if r.get('diplomatic_note_state')=='open_validation']
    resolved_rows=[r for r in note_rows if r.get('diplomatic_note_state')=='resolved_editorial_note']
    if di.get('records_with_editorial_note') != len(note_rows): errors.append('inventory editorial-note count mismatch')
    if di.get('records_with_explicit_open_validation_note') != len(open_rows): errors.append('inventory open-validation count mismatch')
    if di.get('records_with_resolved_editorial_note') != len(resolved_rows): errors.append('inventory resolved-note count mismatch')

validation_queue_path=root/'data/validation/uncertainty_queue.json'
validation_inventory_path=root/'data/validation/validation_inventory.json'
if not validation_queue_path.exists():
    errors.append('scientific uncertainty queue missing')
else:
    vq=json.load(validation_queue_path.open(encoding='utf-8'))
    vrecs=vq.get('records',[])
    expected_open=[r for r in rows if r.get('status')!='rejected_false_positive' and r.get('diplomatic_status')=='complete_ai_assisted' and r.get('diplomatic_note_state')=='open_validation']
    if vq.get('count') != len(vrecs): errors.append('validation queue count mismatch')
    if len(vrecs) != len(expected_open): errors.append(f'validation queue coverage mismatch: {len(vrecs)} != {len(expected_open)}')
    vids=[x.get('record_id') for x in vrecs]
    if len(vids)!=len(set(vids)): errors.append('duplicate record_id in validation queue')
    allowed_categories={'graphic_reading','article_structure','historical_raramuri_form','semantic_or_gloss','general_open_validation'}
    for x in vrecs:
        rid=x.get('record_id')
        if rid not in by_id: errors.append(f'validation queue id missing from entries: {rid}'); continue
        if x.get('category') not in allowed_categories: errors.append(f'bad validation category: {rid}')
        if x.get('priority') not in {1,2,3,4,5}: errors.append(f'bad validation priority: {rid}')
        if x.get('human_verified') is not False: errors.append(f'validation queue must not claim human verification: {rid}')
        if x.get('philologically_verified') is not False: errors.append(f'validation queue must not claim philological verification: {rid}')
        if x.get('linguistically_verified') is not False: errors.append(f'validation queue must not claim linguistic verification: {rid}')
        if x.get('validation_state')!='pending_independent_review': errors.append(f'bad validation state: {rid}')
        if by_id[rid].get('diplomatic_note_state')!='open_validation': errors.append(f'validation queue record is not open_validation: {rid}')
    if validation_inventory_path.exists():
        vi=json.load(validation_inventory_path.open(encoding='utf-8'))
        if vi.get('active_diplomatic_records_with_explicit_open_validation') != len(vrecs): errors.append('validation inventory count mismatch')
        if any(vi.get(k)!=0 for k in ('human_verified_records','philologically_verified_records','linguistically_verified_records')):
            errors.append('scientific validation inventory must begin with zero independent verified records')
    else:
        errors.append('validation inventory missing')

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
print(f"OK: {len(rows)} candidates; {len(reviewed_ids)} facsimile-reviewed boundaries; {len(rejected_ids)} rejected; {len(dip_ids)} complete AI-assisted diplomatic articles; explicit open-validation queue validated; exports agree")
