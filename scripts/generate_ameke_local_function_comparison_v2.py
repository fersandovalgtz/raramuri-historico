#!/usr/bin/env python3
"""Corrected v2 runner for local -ameke German-function comparison.

The v1 generator counted an aggregate participle outcome in the same Counter as
its past/present subtypes and then used sum(counter.values()) as denominator,
which double-counted participial contexts. V2 keeps the same documentary inputs,
classification heuristics, seed and permutations, but uses each token unit's
actual context_count as denominator. No source or human-validation fields change.
"""
from collections import Counter
import json, random
from pathlib import Path
import generate_ameke_local_function_comparison as m


def rate_diff(labels, vectors, totals, target_class, outcome):
    tn=td=rn=rd=0
    for lab,v,total in zip(labels,vectors,totals):
        count=int(v.get(outcome,0))
        if lab==target_class: tn+=count; td+=total
        else: rn+=count; rd+=total
    tr=tn/td if td else 0.0; rr=rn/rd if rd else 0.0
    return tn,td,rn,rd,tr,rr,tr-rr


def corrected_permutation_tests(units, analysis_name):
    labels=[u['exclusive_suffix_class'] for u in units]
    vectors=[Counter(u['functional_proxy_counts']) for u in units]
    totals=[int(u['context_count']) for u in units]
    outcomes=('participle_surface_proxy','past_participle_surface_proxy','present_participle_surface_proxy')
    obs=[]
    for cls in m.CLASS_ORDER:
        for outcome in outcomes:
            obs.append((cls,outcome,rate_diff(labels,vectors,totals,cls,outcome)))
    raw=[0]*len(obs); maxx=[0]*len(obs); rng=random.Random(m.SEED); perm=list(labels); eps=1e-12
    for _ in range(m.ITERATIONS):
        rng.shuffle(perm)
        vals=[rate_diff(perm,vectors,totals,cls,outcome)[-1] for cls,outcome,_ in obs]
        mx=max(abs(v) for v in vals) if vals else 0.0
        for i,v in enumerate(vals):
            if abs(v)+eps >= abs(obs[i][2][-1]): raw[i]+=1
            if mx+eps >= abs(obs[i][2][-1]): maxx[i]+=1
    ps=[(x+1)/(m.ITERATIONS+1) for x in raw]
    fw=[(x+1)/(m.ITERATIONS+1) for x in maxx]
    qs=m.bh_qvalues(ps)
    tests=[]
    for i,(cls,outcome,e) in enumerate(obs):
        tn,td,rn,rd,tr,rr,diff=e
        sig=qs[i]<=.05 and fw[i]<=.05 and abs(diff)>=.10 and td>=10 and tn>=3
        tests.append({'analysis':analysis_name,'exclusive_suffix_class':cls,'outcome':outcome,
            'target_numerator':tn,'target_denominator':td,'rest_numerator':rn,'rest_denominator':rd,
            'target_rate':round(tr,6),'rest_rate':round(rr,6),'rate_difference':round(diff,6),
            'empirical_two_sided_p':round(ps[i],6),'bh_fdr_q':round(qs[i],6),
            'max_abs_rate_difference_fwer_p':round(fw[i],6),'conservative_signal':sig,
            'human_reviewed':False,'automatic_part_of_speech_tagging':False,'automatic_morphological_analysis':False})
    tests.sort(key=lambda x:(not x['conservative_signal'],x['max_abs_rate_difference_fwer_p'],x['bh_fdr_q'],-abs(x['rate_difference'])))
    for i,x in enumerate(tests,1): x['review_rank']=i
    return tests


def main():
    m.permutation_tests=corrected_permutation_tests
    m.main()
    p=Path('data/research/ameke_local_function_comparison_summary.json')
    s=json.loads(p.read_text(encoding='utf-8'))
    s['layer']='ameke_local_german_function_comparison_v2'
    s['denominator_policy']='actual_documentary_context_count_nonoverlapping'
    s['supersedes']='ameke_local_german_function_comparison_v1_denominator_bug'
    p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(s,ensure_ascii=False))

if __name__=='__main__': main()
