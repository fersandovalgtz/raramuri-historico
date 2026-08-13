#!/usr/bin/env python3
import csv,json
from collections import Counter
from research_common import OUT,dump
from generate_graphic_context_associations import shape_proxy

def main():
    members=json.load((OUT/'ameke_constellation_members.json').open(encoding='utf-8'))['records']
    tokens=json.load((OUT/'ameke_token_aware_members.json').open(encoding='utf-8'))['records']
    token_by={x['member_id']:x for x in tokens}; out=[]
    for m in members:
        t=token_by[m['member_id']]; contexts=m.get('german_contexts') or []; pages=m.get('printed_pages') or []
        for i,context in enumerate(contexts):
            p=shape_proxy(context); page_list=[pages[i]] if len(pages)==len(contexts) else pages
            out.append({'audit_id':'','member_id':m['member_id'],'exclusive_suffix_class':m['exclusive_suffix_class'],'analysis_token_key':t['analysis_token_key'],'provenance':t['member_level_provenance'],'german_context':context,'printed_pages':page_list,'surface_shape_proxy':p,'priority':1 if p=='infinitive_ending_proxy' else 2 if p in {'property_ending_proxy','nominalization_ending_proxy'} else 3,'ai_function_reviewed':False,'ai_function_class':'not_assessed','human_reviewed':False,'human_function_decision':'not_assessed'})
    out.sort(key=lambda x:(x['priority'],x['exclusive_suffix_class'],x['analysis_token_key'],x['german_context']))
    for i,x in enumerate(out,1):x['audit_id']=f'RHD-GER-FUNC-{i:04d}'
    counts=Counter(x['surface_shape_proxy'] for x in out)
    summary={'dataset':'raramuri-historico-steffel-1809','generated':'2026-08-13','context_count':len(out),'shape_proxy_counts':dict(sorted(counts.items())),'priority1_count':counts.get('infinitive_ending_proxy',0),'ai_function_reviewed_count':0,'human_reviewed_count':0,'automatic_part_of_speech_tagging':False}
    dump(OUT/'ameke_german_context_audit_queue.json',{'dataset':summary['dataset'],'count':len(out),'human_reviewed':False,'records':out});dump(OUT/'ameke_german_context_audit_queue_summary.json',summary)
    with (OUT/'ameke_german_context_audit_queue.csv').open('w',encoding='utf-8',newline='') as f:
        fields=['audit_id','member_id','exclusive_suffix_class','analysis_token_key','provenance','german_context','printed_pages','surface_shape_proxy','priority','ai_function_reviewed','ai_function_class','human_reviewed','human_function_decision'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for x in out:
            r={k:x.get(k,'') for k in fields};r['printed_pages']=' | '.join(map(str,r['printed_pages']));w.writerow(r)
    print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
