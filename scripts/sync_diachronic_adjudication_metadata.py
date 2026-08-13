#!/usr/bin/env python3
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
pm_path=ROOT/'project-metadata.json'
summary_path=ROOT/'data/diachronic/adjudication_queue_summary.json'
pm=json.loads(pm_path.read_text(encoding='utf-8'))
a=json.loads(summary_path.read_text(encoding='utf-8'))
scope=pm.setdefault('scope',{})
pipeline=pm.setdefault('editorial_pipeline',{})
scope['diachronic_adjudication_candidates']=int(a.get('candidate_count',0))
scope['diachronic_adjudication_priority_tiers']=a.get('priority_tier_counts',{})
scope['diachronic_adjudication_historical_records']=int(a.get('historical_records_represented',0))
scope['diachronic_adjudication_modern_records']=int(a.get('modern_records_represented',0))
scope['diachronic_semantic_context_available_candidates']=int(a.get('semantic_evidence_available_count',0))
pipeline['diachronic_adjudication_queue']='data/diachronic/adjudication_queue.json'
pipeline['diachronic_adjudication_csv']='data/diachronic/adjudication_queue.csv'
pipeline['diachronic_adjudication_summary']='data/diachronic/adjudication_queue_summary.json'
pipeline['diachronic_adjudication_index']='data/diachronic/ADJUDICATION_REVIEW_INDEX.md'
pipeline['diachronic_adjudication_generator']='scripts/generate_diachronic_adjudication_queue.py'
pipeline['diachronic_adjudication_candidate_count']=int(a.get('candidate_count',0))
pipeline['diachronic_adjudication_priority_tiers']=a.get('priority_tier_counts',{})
pipeline['diachronic_adjudication_human_reviewed_count']=int(a.get('human_reviewed_count',0))
pipeline['diachronic_adjudication_policy']='The adjudication score orders human review only. No automatic semantic, etymological or historical-continuity judgment is performed; acceptance or rejection requires explicit independent review.'
p1=int(a.get('priority_tier_counts',{}).get('1',0))
pipeline['diachronic_next_review_priority']=f'Review the {p1} tier-1 diachronic candidates first, then tier 2, while keeping all correspondence decisions independent from the documentary transcription layer.'
pm_path.write_text(json.dumps(pm,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Synchronized diachronic adjudication metadata: {a.get("candidate_count",0)} candidates; tier1={p1}; human reviewed={a.get("human_reviewed_count",0)}')
