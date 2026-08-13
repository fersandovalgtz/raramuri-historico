#!/usr/bin/env python3
from collections import defaultdict,Counter
from research_common import ROOT,OUT,norm,gloss,dump
import json,csv

def main():
    adj=json.loads((ROOT/'data/diachronic/adjudication_queue.json').read_text(encoding='utf-8'))
    conc=json.loads((OUT/'internal_concordance.json').read_text(encoding='utf-8'))['records']
    idx=defaultdict(list)
    for c in conc: idx[(c['rar_de']['record_id'],norm(c['rar_de']['form_diplomatic']))].append(c)
    records=[]; counts=Counter()
    for x in adj['records']:
        h=x['historical']; m=x['modern']; comp=h.get('matched_component',''); supports=idx.get((h.get('record_id',''),norm(comp)),[]); reciprocal=[c for c in supports if c['relation']['reciprocal_german_support']]
        signal='internal_reciprocal_documentary_support' if reciprocal else ('internal_form_attestation_only' if supports else 'cross_corpus_context_only'); counts[signal]+=1
        records.append({'semantic_context_id':'','adjudication_id':x['adjudication_id'],'source_candidate_id':x['source_candidate_id'],'priority_tier':x['priority_tier'],'historical':{'record_id':h.get('record_id',''),'form_diplomatic':h.get('form_diplomatic',''),'matched_component':comp,'german_gloss_local':gloss(h.get('article_diplomatic',''),h.get('form_diplomatic','')),'article_diplomatic':h.get('article_diplomatic',''),'printed_page':h.get('printed_page',0)},'modern':{'record_id':m.get('record_id',''),'headword':m.get('headword',''),'translation_raw':m.get('translation_raw',''),'classification':m.get('classification',''),'source_code':m.get('source_code','')},'machine_context_signal':{'type':signal,'internal_attestation_count':len(supports),'internal_reciprocal_support_count':len(reciprocal),'internal_concordance_ids':[c['concordance_id'] for c in supports],'cross_language_semantic_similarity_computed':False,'semantic_judgment':'not_performed','etymological_judgment':'not_performed','historical_continuity_judgment':'not_performed'},'independent_review':{'human_reviewed':False,'semantic_decision':'not_assessed','historical_continuity':'not_assessed','confidence':'not_assessed','evidence':'','note':''}})
    records.sort(key=lambda x:(x['priority_tier'] or 99,-x['machine_context_signal']['internal_reciprocal_support_count'],-x['machine_context_signal']['internal_attestation_count'],x['adjudication_id']))
    for i,x in enumerate(records,1): x['semantic_context_id']=f'RHD-SEMC-{i:06d}'
    dump(OUT/'diachronic_semantic_context_queue.json',{'dataset':'raramuri-historico-steffel-1809','layer':'diachronic_semantic_context_triage','generated':'2026-08-13','count':len(records),'human_reviewed':False,'cross_language_semantic_similarity_computed':False,'automatic_semantic_judgment':False,'signal_counts':dict(sorted(counts.items())),'records':records})
    summary={'candidate_count':len(records),'signal_counts':dict(sorted(counts.items())),'internal_reciprocal_documentary_support_count':counts.get('internal_reciprocal_documentary_support',0),'internal_form_attestation_only_count':counts.get('internal_form_attestation_only',0),'cross_corpus_context_only_count':counts.get('cross_corpus_context_only',0),'human_reviewed':False,'automatic_semantic_judgment':False,'cross_language_semantic_similarity_computed':False}
    dump(OUT/'diachronic_semantic_context_queue_summary.json',summary)
    fields=['semantic_context_id','adjudication_id','source_candidate_id','priority_tier','signal_type','historical_record_id','historical_form','historical_component','historical_german_gloss','historical_page','modern_record_id','modern_headword','modern_translation','modern_classification','internal_attestation_count','internal_reciprocal_support_count','human_reviewed','semantic_decision']
    with (OUT/'diachronic_semantic_context_queue.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for x in records:
            h=x['historical']; m=x['modern']; s=x['machine_context_signal']
            w.writerow({'semantic_context_id':x['semantic_context_id'],'adjudication_id':x['adjudication_id'],'source_candidate_id':x['source_candidate_id'],'priority_tier':x['priority_tier'],'signal_type':s['type'],'historical_record_id':h['record_id'],'historical_form':h['form_diplomatic'],'historical_component':h['matched_component'],'historical_german_gloss':h['german_gloss_local'],'historical_page':h['printed_page'],'modern_record_id':m['record_id'],'modern_headword':m['headword'],'modern_translation':m['translation_raw'],'modern_classification':m['classification'],'internal_attestation_count':s['internal_attestation_count'],'internal_reciprocal_support_count':s['internal_reciprocal_support_count'],'human_reviewed':'false','semantic_decision':'not_assessed'})
    print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__': main()
