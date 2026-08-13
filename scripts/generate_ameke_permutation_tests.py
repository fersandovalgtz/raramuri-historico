#!/usr/bin/env python3
"""Deterministic permutation controls for the historical -ameke constellation.

The null model shuffles the five mutually exclusive graphic ending labels across
whole -ameke members, preserving: (1) class sizes, (2) every member's German
context bag, and (3) the corpus-wide proxy totals. Observed class-vs-rest proxy
rate differences are evaluated by empirical two-sided p-values, Benjamini-
Hochberg FDR, and a max-|rate difference| family-wise permutation control.
An omnibus chi-square statistic is also calibrated by the same permutations.

These tests ask whether documentary context distributions are difficult to
explain by random reassignment of the GRAPHIC classes. They do NOT establish
morphemes, grammatical categories, semantic functions, paradigms, lexical
identity, historical continuity, or human validation.
"""
from __future__ import annotations
from collections import Counter
import csv,json,math,random
from research_common import OUT,dump

SEED=1809
ITERATIONS=20000
CLASS_ORDER=('ameke_other','gameke','iameke','ugameke','jameke')


def chi_square(table):
    rows=len(table); cols=len(table[0]) if rows else 0
    rtot=[sum(r) for r in table]; ctot=[sum(table[i][j] for i in range(rows)) for j in range(cols)]; total=sum(rtot)
    if not total:return 0.0
    x=0.0
    for i in range(rows):
        for j in range(cols):
            exp=rtot[i]*ctot[j]/total
            if exp>0:x+=(table[i][j]-exp)**2/exp
    return x


def cramer_v(x2,total,r,c):
    den=total*max(1,min(r-1,c-1))
    return math.sqrt(x2/den) if den else 0.0


def bh_qvalues(pvals):
    m=len(pvals); order=sorted(range(m),key=lambda i:pvals[i]); q=[1.0]*m; running=1.0
    for rank0 in range(m-1,-1,-1):
        idx=order[rank0]; rank=rank0+1; running=min(running,pvals[idx]*m/rank); q[idx]=min(1.0,running)
    return q


def table_for(labels,vectors,p_index):
    ci={c:i for i,c in enumerate(CLASS_ORDER)}; table=[[0]*len(p_index) for _ in CLASS_ORDER]
    for lab,vec in zip(labels,vectors):
        row=table[ci[lab]]
        for p,n in vec.items(): row[p_index[p]]+=n
    return table


def rate_diffs(table):
    ctot=[sum(row) for row in table]; global_counts=[sum(table[i][j] for i in range(len(table))) for j in range(len(table[0]))]; total=sum(ctot)
    out=[]
    for i,row in enumerate(table):
        rest_total=total-ctot[i]
        for j,count in enumerate(row):
            rest_count=global_counts[j]-count
            local_rate=count/ctot[i] if ctot[i] else 0.0
            rest_rate=rest_count/rest_total if rest_total else 0.0
            out.append((local_rate-rest_rate,local_rate,rest_rate,count,ctot[i],rest_count,rest_total))
    return out


def main():
    src=json.loads((OUT/'ameke_constellation_members.json').read_text(encoding='utf-8'))
    members=src['records']
    labels=[m['exclusive_suffix_class'] for m in members]
    assert Counter(labels)==Counter({'ameke_other':53,'gameke':17,'iameke':28,'ugameke':27,'jameke':22})
    proxies=sorted({p for m in members for p,n in m['german_context_shape_proxy_counts'].items() if n>0})
    p_index={p:i for i,p in enumerate(proxies)}
    vectors=[m['german_context_shape_proxy_counts'] for m in members]
    obs_table=table_for(labels,vectors,p_index)
    obs=rate_diffs(obs_table)
    obs_x2=chi_square(obs_table); total_contexts=sum(sum(r) for r in obs_table)
    test_count=len(obs)
    raw_exceed=[0]*test_count; max_exceed=[0]*test_count; null_sum=[0.0]*test_count; null_sumsq=[0.0]*test_count; omnibus_exceed=0
    rng=random.Random(SEED); perm_labels=list(labels)
    eps=1e-12
    for _ in range(ITERATIONS):
        rng.shuffle(perm_labels)
        table=table_for(perm_labels,vectors,p_index)
        diffs=rate_diffs(table)
        absvals=[abs(x[0]) for x in diffs]; max_abs=max(absvals) if absvals else 0.0
        for k,(d,*_) in enumerate(diffs):
            ad=abs(d); null_sum[k]+=d; null_sumsq[k]+=d*d
            if ad+eps>=abs(obs[k][0]): raw_exceed[k]+=1
        for k,o in enumerate(obs):
            if max_abs+eps>=abs(o[0]):max_exceed[k]+=1
        if chi_square(table)+eps>=obs_x2:omnibus_exceed+=1
    raw_p=[(x+1)/(ITERATIONS+1) for x in raw_exceed]; fwer_p=[(x+1)/(ITERATIONS+1) for x in max_exceed]; q=bh_qvalues(raw_p)
    tests=[]; k=0
    class_context_totals={CLASS_ORDER[i]:sum(obs_table[i]) for i in range(len(CLASS_ORDER))}
    class_member_counts=Counter(labels)
    global_proxy_counts={proxies[j]:sum(obs_table[i][j] for i in range(len(CLASS_ORDER)) ) for j in range(len(proxies))}
    for i,cls in enumerate(CLASS_ORDER):
        for j,proxy in enumerate(proxies):
            d,lr,rr,count,local_total,rest_count,rest_total=obs[k]
            mean=null_sum[k]/ITERATIONS; var=max(0.0,null_sumsq[k]/ITERATIONS-mean*mean); sd=math.sqrt(var); z=(d-mean)/sd if sd else 0.0
            signal=(fwer_p[k]<=0.05 and q[k]<=0.05 and abs(d)>=0.10 and local_total>=10 and count>=3)
            tests.append({'test_id':f'RHD-AMEKE-PERM-{k+1:03d}','exclusive_suffix_class':cls,'german_context_proxy':proxy,'class_member_count':class_member_counts[cls],'class_context_count':local_total,'observed_proxy_count':count,'observed_class_rate':round(lr,6),'observed_rest_rate':round(rr,6),'observed_rate_difference':round(d,6),'absolute_rate_difference':round(abs(d),6),'permutation_null_mean_rate_difference':round(mean,6),'permutation_null_sd':round(sd,6),'permutation_z_score_descriptive':round(z,4),'empirical_two_sided_p':round(raw_p[k],6),'bh_fdr_q':round(q[k],6),'max_abs_rate_difference_fwer_p':round(fwer_p[k],6),'effect_direction':'enriched_in_class' if d>0 else ('depleted_in_class' if d<0 else 'no_difference'),'conservative_permutation_signal':signal,'status':'machine_permutation_context_test','human_reviewed':False,'automatic_morphological_analysis':False,'automatic_morpheme_assignment':False,'automatic_semantic_classification':False,'automatic_part_of_speech_tagging':False,'automatic_paradigm_inference':False})
            k+=1
    tests.sort(key=lambda x:(not x['conservative_permutation_signal'],x['max_abs_rate_difference_fwer_p'],x['bh_fdr_q'],-x['absolute_rate_difference'],x['exclusive_suffix_class'],x['german_context_proxy']))
    for rank,x in enumerate(tests,1):x['review_rank']=rank
    omnibus_p=(omnibus_exceed+1)/(ITERATIONS+1)
    signals=[x for x in tests if x['conservative_permutation_signal']]
    summary={'dataset':'raramuri-historico-steffel-1809','layer':'ameke_context_permutation_controls_v1','generated':'2026-08-13','random_seed':SEED,'permutation_iterations':ITERATIONS,'randomization_unit':'whole_ameke_member','null_model':'shuffle_exclusive_graphic_suffix_class_labels_across_members_preserving_class_sizes_and_member_context_bags','member_count':len(members),'context_count':total_contexts,'exclusive_suffix_member_counts':dict((c,class_member_counts[c]) for c in CLASS_ORDER),'exclusive_suffix_context_counts':class_context_totals,'german_context_proxy_counts':global_proxy_counts,'tested_proxy_count':len(proxies),'cell_test_count':test_count,'omnibus_chi_square_observed':round(obs_x2,6),'omnibus_cramers_v_descriptive':round(cramer_v(obs_x2,total_contexts,len(CLASS_ORDER),len(proxies)),6),'omnibus_empirical_permutation_p':round(omnibus_p,6),'raw_empirical_p_le_0_05_count':sum(x['empirical_two_sided_p']<=0.05 for x in tests),'bh_fdr_q_le_0_05_count':sum(x['bh_fdr_q']<=0.05 for x in tests),'maxT_fwer_p_le_0_05_count':sum(x['max_abs_rate_difference_fwer_p']<=0.05 for x in tests),'conservative_permutation_signal_count':len(signals),'conservative_permutation_signals':signals,'human_reviewed':False,'automatic_morphological_analysis':False,'automatic_morpheme_assignment':False,'automatic_semantic_classification':False,'automatic_part_of_speech_tagging':False,'automatic_paradigm_inference':False,'interpretive_scope':'Permutation-calibrated association between mutually exclusive historical graphic endings and transparent German context-shape proxies. Statistical dependence is not a grammatical, morphological or semantic analysis.'}
    dump(OUT/'ameke_permutation_tests.json',{'dataset':summary['dataset'],'layer':summary['layer'],'generated':summary['generated'],'count':len(tests),'random_seed':SEED,'permutation_iterations':ITERATIONS,'human_reviewed':False,'automatic_morphological_analysis':False,'automatic_semantic_classification':False,'records':tests})
    dump(OUT/'ameke_permutation_tests_summary.json',summary)
    with (OUT/'ameke_permutation_tests.csv').open('w',encoding='utf-8',newline='') as f:
        fields=['review_rank','test_id','exclusive_suffix_class','german_context_proxy','class_member_count','class_context_count','observed_proxy_count','observed_class_rate','observed_rest_rate','observed_rate_difference','empirical_two_sided_p','bh_fdr_q','max_abs_rate_difference_fwer_p','conservative_permutation_signal','human_reviewed'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for x in tests:w.writerow({k:x[k] for k in fields})
    print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__':main()
