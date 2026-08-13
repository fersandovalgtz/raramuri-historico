#!/usr/bin/env python3
import json,csv
from research_common import OUT,dump

def main():
    src=json.loads((OUT/'de_rar_inventory_guided_attestations.json').read_text(encoding='utf-8'))['records']
    recs=[]
    for a in src:
        recs.append({
          'concordance_id':'','graphic_key':a['graphic_key'],
          'rar_de':{'record_id':a['rar_de_record_id'],'form_diplomatic':a['rar_de_form_diplomatic'],'german_gloss_local':a['rar_de_german_gloss_local'],'printed_page':a['rar_de_printed_page']},
          'de_rar':{'record_id':a['de_rar_record_id'],'headword_diplomatic':a['de_rar_headword_diplomatic'],'printed_page':a['de_rar_printed_page']},
          'relation':{'type':'internal_parallel_attestation_candidate','exact_form_attestation':True,'reciprocal_german_support':a['reciprocal_german_support'],'reciprocal_support_type':a['reciprocal_support_type'],'status':'machine_candidate'},
          'human_reviewed':False,'decision':'not_assessed'
        })
    recs.sort(key=lambda x:(not x['relation']['reciprocal_german_support'],x['graphic_key'],x['rar_de']['record_id'],x['de_rar']['record_id']))
    for i,x in enumerate(recs,1): x['concordance_id']=f'RHD-ICONC-{i:06d}'
    dump(OUT/'internal_concordance.json',{'dataset':'raramuri-historico-steffel-1809','layer':'steffel_internal_bidirectional_concordance','generated':'2026-08-13','count':len(recs),'human_reviewed':False,'automatic_semantic_judgment':False,'records':recs})
    summary={'candidate_count':len(recs),'reciprocal_german_support_count':sum(x['relation']['reciprocal_german_support'] for x in recs),'unique_graphic_keys':len({x['graphic_key'] for x in recs}),'rar_de_records_represented':len({x['rar_de']['record_id'] for x in recs}),'de_rar_records_represented':len({x['de_rar']['record_id'] for x in recs}),'human_reviewed':False,'automatic_semantic_judgment':False}
    dump(OUT/'internal_concordance_summary.json',summary)
    fields=['concordance_id','graphic_key','rar_de_record_id','rar_de_form','rar_de_german_gloss','rar_de_page','de_rar_record_id','de_rar_headword','de_rar_page','reciprocal_german_support','reciprocal_support_type','human_reviewed','decision']
    with (OUT/'internal_concordance.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for x in recs:
            w.writerow({'concordance_id':x['concordance_id'],'graphic_key':x['graphic_key'],'rar_de_record_id':x['rar_de']['record_id'],'rar_de_form':x['rar_de']['form_diplomatic'],'rar_de_german_gloss':x['rar_de']['german_gloss_local'],'rar_de_page':x['rar_de']['printed_page'],'de_rar_record_id':x['de_rar']['record_id'],'de_rar_headword':x['de_rar']['headword_diplomatic'],'de_rar_page':x['de_rar']['printed_page'],'reciprocal_german_support':str(x['relation']['reciprocal_german_support']).lower(),'reciprocal_support_type':x['relation']['reciprocal_support_type'],'human_reviewed':'false','decision':'not_assessed'})
    print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__': main()
