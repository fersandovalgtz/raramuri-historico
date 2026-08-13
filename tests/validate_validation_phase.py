#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
V = ROOT / "data" / "validation"
R = V / "review"
errors=[]

queue=json.load((V/'uncertainty_queue.json').open(encoding='utf-8'))
open_ids=[x['record_id'] for x in queue.get('records',[])]
open_set=set(open_ids)
if len(open_ids)!=len(open_set): errors.append('duplicate ID in open-validation queue')

reviewed=[]
dispositions={}
for path in sorted(R.glob('philological_review_batch_*.json')):
    m=json.load(path.open(encoding='utf-8'))
    if m.get('human_verified') is not False: errors.append(f'{path.name} claims human verification')
    if m.get('philologically_verified_by_human') is not False: errors.append(f'{path.name} claims human philological verification')
    if m.get('linguistically_verified') is not False: errors.append(f'{path.name} claims linguistic verification')
    recs=m.get('records',[])
    if m.get('summary',{}).get('reviewed') != len(recs): errors.append(f'{path.name} summary reviewed mismatch')
    counts={'confirmed_ai_assisted':0,'corrected_ai_assisted':0,'unresolved_after_ai_recollation':0}
    for x in recs:
        rid=x['record_id']; reviewed.append(rid); dispositions[rid]=x.get('disposition')
        if rid not in open_set: errors.append(f'{path.name} reviews ID outside open-validation queue: {rid}')
        if x.get('disposition') not in counts: errors.append(f'{path.name} bad disposition: {rid}')
        else: counts[x['disposition']]+=1
        if x.get('human_verified') is True: errors.append(f'{path.name} record claims human verification: {rid}')
    s=m.get('summary',{})
    for k,v in counts.items():
        if s.get(k) != v: errors.append(f'{path.name} summary mismatch for {k}')
if len(reviewed)!=len(set(reviewed)): errors.append('duplicate ID across philological review batches')
reviewed_set=set(reviewed)

next_batch=json.load((V/'next_philological_batch.json').open(encoding='utf-8'))
next_ids=[x['record_id'] for x in next_batch.get('records',[])]
if any(rid in reviewed_set for rid in next_ids): errors.append('next philological batch repeats an already reviewed ID')
remaining=[rid for rid in open_ids if rid not in reviewed_set]
if next_ids != remaining[:50]: errors.append('next philological batch is not the deterministic first 50 remaining IDs')
if next_batch.get('remaining_before_batch') != len(remaining): errors.append('remaining_before_batch mismatch')
if next_batch.get('human_verified') is not False: errors.append('next philological batch must state human_verified=false')

human=json.load((V/'human_review_queue.json').open(encoding='utf-8'))
human_ids=[x['record_id'] for x in human.get('records',[])]
if any(rid not in reviewed_set for rid in human_ids): errors.append('human review queue contains ID not yet AI-recollated')
if len(human_ids)!=len(set(human_ids)): errors.append('duplicate ID in human review queue')
if human.get('human_verified') is not False: errors.append('human queue must begin human_verified=false')
for x in human.get('records',[]):
    if x.get('human_verified') is not False or x.get('philologically_verified_by_human') is not False or x.get('linguistically_verified') is not False:
        errors.append('human queue record incorrectly claims independent verification: '+x['record_id'])

progress=json.load((V/'validation_progress.json').open(encoding='utf-8'))
if progress.get('open_validation_records_total') != len(open_ids): errors.append('progress total mismatch')
if progress.get('ai_philological_recollation_reviewed') != len(reviewed_set): errors.append('progress reviewed mismatch')
if progress.get('ai_philological_recollation_remaining') != len(remaining): errors.append('progress remaining mismatch')
if progress.get('human_review_queue_count') != len(human_ids): errors.append('progress human queue mismatch')
if any(progress.get(k)!=0 for k in ('human_verified_records','philologically_verified_by_human_records','linguistically_verified_records')):
    errors.append('independent verification counters must remain zero')

if errors:
    print('\n'.join('ERROR: '+e for e in errors)); sys.exit(1)
print(f"OK validation phase: {len(open_ids)} open; {len(reviewed_set)} AI-recollated; {len(remaining)} remaining; next={len(next_ids)}; human queue={len(human_ids)}")
