#!/usr/bin/env python3
"""Permutation controls for the token-aware -ameke analysis layer.

Randomization unit: unique (exclusive graphic class, analysis token) unit.
Documentary contexts from member rows that collapse to the same token unit are
pooled. This answers whether the original formal German-context association
survives correction of documentary counting units. It does not perform German
part-of-speech analysis and does not establish morphology or grammar.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import csv,json,math,random
from research_common import OUT,dump

SEED=1811
ITERATIONS=20000
CLASS_ORDER=('ameke_other','gameke','iameke','ugameke','jameke')

def bh_qvalues(pvals):
    m=len(pvals); order=sorted(range(m),key=lambda i:pvals[i]); q=[1.0]*m; running=1.0
    for rank0 in range(m-1,-1,-1):
        idx=order[rank0]; rank=rank0+1
        running=min(running,pvals[idx]*m/rank); q[idx]=min(1.0,running)
    return q

def rate_diff(labels,vectors,target_class,proxy):
    tn=td=rn=rd=0
    for lab,vec in zip(labels,vectors):
        total=sum(vec.values()); count=int(vec.get(proxy,0))
        if lab==target_class: tn+=count;td+=total
        else: rn+=count;rd+=total
    tr=tn/td if td else 0.0; rr=rn/rd if rd else 0.0
    return {'target_numerator':tn,'target_denominator':td,'rest_numerator':rn,'rest_denominator':rd,'target_rate':tr,'rest_rate':rr,'rate_difference':tr-rr}

def main():
    original=json.loads((OUT/'ameke_constellation_members.json').read_text(encoding='utf-8'))['records']
    token=json.loads((OUT/'ameke_token_aware_members.json').read_text(encoding='utf-8'))['records']
    orig_by={x['member_id']:x for x in original}
    groups=defaultdict(list)
    for x in token: groups[(x['exclusive_suffix_class'],x['analysis_token_key'])].append(x)
    units=[]
    for (cls,key),items in groups.items():
        proxy=Counter()
        contexts=[]
        for item in items:
            o=orig_by[item['member_id']]
            proxy.update(o.get('german_context_shape_proxy_counts') or {})
            contexts.extend(o.get('german_contexts') or [])
        units.append({'exclusive_suffix_class':cls,'analysis_token_key':key,'member_ids':sorted(x['member_id'] for x in items),'proxy_counts':dict(proxy),'german_contexts':contexts})
    units.sort(key=lambda x:(CLASS_ORDER.index(x['exclusive_suffix_class']),x['analysis_token_key']))
    labels=[x['exclusive_suffix_class'] for x in units]
    vectors=[x['proxy_counts'] for x in units]
    proxies=sorted({p for v in vectors for p,n in v.items() if n})
    observed=[]
    for cls in CLASS_ORDER:
        for proxy in proxies:
            eff=rate_diff(labels,vectors,cls,proxy)
            observed.append((cls,proxy,eff))
    raw=[0]*len(observed); maxx=[0]*len(observed); rng=random.Random(SEED); perm=list(labels); eps=1e-12
    for _ in range(ITERATIONS):
        rng.shuffle(perm)
        vals=[]
        for cls,proxy,_obs in observed:
            vals.append(rate_diff(perm,vectors,cls,proxy)['rate_difference'])
        mx=max(abs(x) for x in vals) if vals else 0
        for i,val in enumerate(vals):
            if abs(val)+eps>=abs(observed[i][2]['rate_difference']):raw[i]+=1
            if mx+eps>=abs(observed[i][2]['rate_difference']):maxx[i]+=1
    p=[(x+1)/(ITERATIONS+1) for x in raw]; fwer=[(x+1)/(ITERATIONS+1) for x in maxx]; q=bh_qvalues(p)
    tests=[]
    for i,(cls,proxy,eff) in enumerate(observed):
        sig=(q[i]<=.05 and fwer[i]<=.05 and abs(eff['rate_difference'])>=.10 and eff['target_denominator']>=10 and eff['target_numerator']>=3)
        tests.append({'test_id':f'RHD-AMEKE-TOKPERM-{i+1:03d}','exclusive_suffix_class':cls,'german_context_proxy':proxy,'unit_count':sum(x==cls for x in labels),'observed_target_count':eff['target_numerator'],'observed_target_context_count':eff['target_denominator'],'observed_target_rate':round(eff['target_rate'],6),'observed_rest_rate':round(eff['rest_rate'],6),'observed_rate_difference':round(eff['rate_difference'],6),'empirical_two_sided_p':round(p[i],6),'bh_fdr_q':round(q[i],6),'max_abs_rate_difference_fwer_p':round(fwer[i],6),'conservative_token_aware_signal':sig,'human_reviewed':False,'automatic_morphological_analysis':False,'automatic_semantic_classification':False})
    tests.sort(key=lambda x:(not x['conservative_token_aware_signal'],x['max_abs_rate_difference_fwer_p'],x['bh_fdr_q'],-abs(x['observed_rate_difference'])))
    for rank,x in enumerate(tests,1):x['review_rank']=rank
    sig=[x for x in tests if x['conservative_token_aware_signal']]
    summary={'dataset':'raramuri-historico-steffel-1809','layer':'ameke_token_aware_permutation_controls_v1','generated':'2026-08-13','random_seed':SEED,'permutation_iterations':ITERATIONS,'randomization_unit':'unique_exclusive_class_plus_analysis_token_unit','token_unit_count':len(units),'token_unit_counts_by_class':dict((c,Counter(labels)[c]) for c in CLASS_ORDER),'context_count':sum(sum(v.values()) for v in vectors),'tested_proxy_count':len(proxies),'cell_test_count':len(tests),'raw_empirical_p_le_0_05_count':sum(x['empirical_two_sided_p']<=.05 for x in tests),'bh_fdr_q_le_0_05_count':sum(x['bh_fdr_q']<=.05 for x in tests),'maxT_fwer_p_le_0_05_count':sum(x['max_abs_rate_difference_fwer_p']<=.05 for x in tests),'conservative_token_aware_signal_count':len(sig),'conservative_token_aware_signals':sig,'human_reviewed':False,'automatic_morphological_analysis':False,'automatic_semantic_classification':False,'interpretive_scope':'Permutation-calibrated formal context dependence after correcting documentary token units. The German proxy remains surface-form based and is not part-of-speech annotation.'}
    dump(OUT/'ameke_token_aware_permutation_tests.json',{'dataset':summary['dataset'],'layer':summary['layer'],'generated':summary['generated'],'count':len(tests),'human_reviewed':False,'records':tests})
    dump(OUT/'ameke_token_aware_permutation_summary.json',summary)
    with (OUT/'ameke_token_aware_permutation_tests.csv').open('w',encoding='utf-8',newline='') as f:
        fields=['review_rank','test_id','exclusive_suffix_class','german_context_proxy','unit_count','observed_target_count','observed_target_context_count','observed_target_rate','observed_rest_rate','observed_rate_difference','empirical_two_sided_p','bh_fdr_q','max_abs_rate_difference_fwer_p','conservative_token_aware_signal','human_reviewed'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for x in tests:w.writerow({k:x.get(k,'') for k in fields})
    print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
