#!/usr/bin/env python3
"""Jackknife sensitivity analysis for the DE-RAR ugameke signal.

Uses only low-risk DE-RAR local alignments. Two independent documentary units:
1) single-class German articles, one binary past-participle observation/article;
2) token-aware graphic units, one binary past-participle observation/token.

For each unit, remove it once and recompute ugameke-vs-rest rate difference.
This is an influence/sensitivity diagnostic, not a significance test and not a
morphological analysis.
"""
from collections import defaultdict
import csv,json,statistics
from pathlib import Path

OUT=Path('data/research')
TARGET='ugameke'

def effect(rows):
    t=[x for x in rows if x['exclusive_suffix_class']==TARGET]
    r=[x for x in rows if x['exclusive_suffix_class']!=TARGET]
    tn=sum(x['past_participle_surface_proxy'] for x in t);rn=sum(x['past_participle_surface_proxy'] for x in r)
    tr=tn/len(t) if t else 0.;rr=rn/len(r) if r else 0.
    return {'target_numerator':tn,'target_denominator':len(t),'rest_numerator':rn,'rest_denominator':len(r),'target_rate':tr,'rest_rate':rr,'rate_difference':tr-rr}

def jackknife(rows,id_field,analysis):
    base=effect(rows);recs=[]
    for x in rows:
        kept=[y for y in rows if y is not x]
        e=effect(kept)
        recs.append({'analysis':analysis,'removed_id':x[id_field],'removed_class':x['exclusive_suffix_class'],'removed_past_participle':bool(x['past_participle_surface_proxy']),'rate_difference':round(e['rate_difference'],6),'target_rate':round(e['target_rate'],6),'rest_rate':round(e['rest_rate'],6),'human_reviewed':False})
    diffs=[x['rate_difference'] for x in recs]
    target_recs=[x for x in recs if x['removed_class']==TARGET]
    return {'observation_count':len(rows),'baseline':{k:(round(v,6) if isinstance(v,float) else v) for k,v in base.items()},'leave_one_out_count':len(recs),'minimum_rate_difference':round(min(diffs),6),'maximum_rate_difference':round(max(diffs),6),'median_rate_difference':round(statistics.median(diffs),6),'all_leave_one_out_effects_positive':all(d>0 for d in diffs),'all_leave_one_out_effects_ge_0_20':all(d>=.20 for d in diffs),'target_unit_leave_one_out_minimum':round(min(x['rate_difference'] for x in target_recs),6) if target_recs else None,'target_unit_leave_one_out_maximum':round(max(x['rate_difference'] for x in target_recs),6) if target_recs else None,'most_influential_deletions':sorted(recs,key=lambda x:x['rate_difference'])[:10]},recs

def main():
    ctx=json.loads((OUT/'ameke_local_function_contexts.json').read_text(encoding='utf-8'))['records']
    ctx=[x for x in ctx if x['source_layer']=='DE-RAR-local-proposal' and x['alignment_risk']=='low']
    byrec=defaultdict(list)
    for x in ctx:byrec[x['record_id']].append(x)
    articles=[]
    for rid,items in sorted(byrec.items()):
        classes=set(x['exclusive_suffix_class'] for x in items)
        if len(classes)!=1:continue
        articles.append({'record_id':rid,'exclusive_suffix_class':next(iter(classes)),'past_participle_surface_proxy':any(x['functional_proxy']=='past_participle_surface_proxy' for x in items)})
    bytok=defaultdict(list)
    for x in ctx:bytok[(x['exclusive_suffix_class'],x['analysis_token_key'])].append(x)
    tokens=[]
    for (cls,key),items in sorted(bytok.items()):
        tokens.append({'token_key':key,'exclusive_suffix_class':cls,'past_participle_surface_proxy':any(x['functional_proxy']=='past_participle_surface_proxy' for x in items)})
    a,ar=jackknife(articles,'record_id','single_class_article_jackknife')
    t,tr=jackknife(tokens,'token_key','token_unit_jackknife')
    out={'dataset':'raramuri-historico-steffel-1809','layer':'ugameke_jackknife_robustness_v1','generated':'2026-08-13','analyses':{'single_class_article_jackknife':a,'token_unit_jackknife':t},'human_reviewed':False,'automatic_part_of_speech_tagging':False,'automatic_morphological_analysis':False,'interpretive_scope':'Leave-one-out sensitivity of the low-risk DE-RAR past-participle surface association. Stability indicates the documentary effect is not driven by one retained article or token; it does not establish a Raramuri morpheme or grammatical category.'}
    (OUT/'ugameke_jackknife_robustness_summary.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    rows=ar+tr
    with (OUT/'ugameke_jackknife_robustness.csv').open('w',encoding='utf-8',newline='') as f:
        fields=['analysis','removed_id','removed_class','removed_past_participle','rate_difference','target_rate','rest_rate','human_reviewed'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
    print(json.dumps(out,ensure_ascii=False))
if __name__=='__main__':main()
