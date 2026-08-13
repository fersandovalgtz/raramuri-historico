#!/usr/bin/env python3
from __future__ import annotations
import csv,json
from research_common import OUT,dump

def main():
    src=json.loads((OUT/'ameke_constellation_members.json').read_text(encoding='utf-8'))
    records=[]
    for m in src['records']:
        if m.get('exclusive_suffix_class')!='ugameke':
            continue
        if set(m.get('source_layers') or [])!={'DE-RAR-residual-recovery'}:
            continue
        proxy_count=int((m.get('german_context_shape_proxy_counts') or {}).get('infinitive_ending_proxy',0))
        records.append({'audit_id':'','member_id':m['member_id'],'graphic_key':m['graphic_key'],'surface_forms':m.get('surface_forms',[]),'printed_pages':m.get('printed_pages',[]),'german_contexts':m.get('german_contexts',[]),'recovery_ids':m.get('recovery_ids',[]),'target_proxy_context_count':proxy_count,'priority':'P1_signal_bearing' if proxy_count>0 else 'P2_other_recovered_ugameke','facsimile_reviewed':False,'facsimile_decision':'not_assessed','facsimile_reading':'','review_notes':'','human_reviewed':False,'interpretive_scope':'Queue for direct facsimile recollation of DE-RAR-recovery-only ugameke members. Presence in this queue does not confirm a form, segmentation, morpheme, grammatical category or semantic function.'})
    records.sort(key=lambda x:(0 if x['priority'].startswith('P1') else 1,min(x['printed_pages'] or [9999]),x['graphic_key']))
    for i,x in enumerate(records,1):x['audit_id']=f'RHD-UG-FAC-{i:03d}'
    summary={'dataset':'raramuri-historico-steffel-1809','layer':'ugameke_facsimile_audit_queue_v1','generated':'2026-08-13','candidate_count':len(records),'signal_bearing_candidate_count':sum(x['target_proxy_context_count']>0 for x in records),'other_recovered_candidate_count':sum(x['target_proxy_context_count']==0 for x in records),'facsimile_reviewed_count':0,'human_reviewed':False,'automatic_morphological_analysis':False,'interpretive_scope':'Direct source-verification queue only; no automatic acceptance or linguistic interpretation.'}
    dump(OUT/'ugameke_facsimile_audit_queue.json',{'dataset':summary['dataset'],'layer':summary['layer'],'generated':summary['generated'],'count':len(records),'human_reviewed':False,'records':records})
    dump(OUT/'ugameke_facsimile_audit_queue_summary.json',summary)
    with (OUT/'ugameke_facsimile_audit_queue.csv').open('w',encoding='utf-8',newline='') as f:
        fields=['audit_id','member_id','graphic_key','surface_forms','printed_pages','german_contexts','recovery_ids','target_proxy_context_count','priority','facsimile_reviewed','facsimile_decision','facsimile_reading','review_notes','human_reviewed'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for x in records:
            r={k:x.get(k,'') for k in fields}
            for k in ('surface_forms','printed_pages','german_contexts','recovery_ids'):r[k]=' | '.join(map(str,r[k]))
            w.writerow(r)
    print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
