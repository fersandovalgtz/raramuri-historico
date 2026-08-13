#!/usr/bin/env python3
"""Hostile robustness controls for the historical -ugameke documentary signal.

This layer stress-tests the already pre-specified association between the
exclusive graphic class `ugameke` and the transparent German
`infinitive_ending_proxy`. It uses multiple permutation nulls, member-binary
outcomes, provenance/page stratification, subgroup checks, and leave-one-out
influence diagnostics.

The controls deliberately preserve the documentary member as the unit of
randomization. Page stratification assigns each member to the 10-page block of
its median printed page; provenance stratification uses the member's source
layer signature. These are sensitivity analyses of DOCUMENTARY dependence.
They do not establish morphology, morphemes, grammatical categories, semantic
functions, paradigms, lexical identity, historical continuity, or human
validation.
"""
from __future__ import annotations
from collections import Counter, defaultdict
import csv, json, random, statistics
from research_common import OUT, dump

SEED = 1810
ITERATIONS = 20000
TARGET_CLASS = 'ugameke'
TARGET_PROXY = 'infinitive_ending_proxy'


def provenance(m):
    s=set(m.get('source_layers',[]))
    rar='RAR-DE' in s
    rec='DE-RAR-residual-recovery' in s
    if rar and rec:return 'mixed_RAR-DE_and_DE-RAR-recovery'
    if rar:return 'RAR-DE_only'
    if rec:return 'DE-RAR-recovery_only'
    return 'other_or_unknown'


def median_page(m):
    pages=[int(x) for x in m.get('printed_pages',[]) if x not in (None,'')]
    if not pages:return None
    return int(statistics.median(sorted(pages)))


def page_block(m,width=10):
    p=median_page(m)
    if p is None:return 'page_unknown'
    start=(p//width)*width
    return f'p{start:03d}-{start+width-1:03d}'


def enrich(m):
    d=dict(m)
    counts=m.get('german_context_shape_proxy_counts',{})
    d['_context_total']=sum(int(v) for v in counts.values())
    d['_target_proxy_count']=int(counts.get(TARGET_PROXY,0))
    d['_target_proxy_binary']=1 if d['_target_proxy_count']>0 else 0
    d['_provenance']=provenance(m)
    d['_page10']=page_block(m,10)
    d['_page5']=page_block(m,5)
    return d


def effect(ms, binary=False):
    target=[m for m in ms if m['exclusive_suffix_class']==TARGET_CLASS]
    rest=[m for m in ms if m['exclusive_suffix_class']!=TARGET_CLASS]
    if not target or not rest:return None
    if binary:
        ta=sum(m['_target_proxy_binary'] for m in target); tb=len(target)
        ra=sum(m['_target_proxy_binary'] for m in rest); rb=len(rest)
    else:
        ta=sum(m['_target_proxy_count'] for m in target); tb=sum(m['_context_total'] for m in target)
        ra=sum(m['_target_proxy_count'] for m in rest); rb=sum(m['_context_total'] for m in rest)
    if tb==0 or rb==0:return None
    tr=ta/tb; rr=ra/rb
    return {'target_numerator':ta,'target_denominator':tb,'rest_numerator':ra,'rest_denominator':rb,
            'target_rate':tr,'rest_rate':rr,'rate_difference':tr-rr}


def effect_from_labels(ms, labels, binary=False):
    ta=tb=ra=rb=0
    for m,lab in zip(ms,labels):
        if binary:
            num=m['_target_proxy_binary']; den=1
        else:
            num=m['_target_proxy_count']; den=m['_context_total']
        if lab==TARGET_CLASS:ta+=num;tb+=den
        else:ra+=num;rb+=den
    if tb==0 or rb==0:return None
    return ta/tb-ra/rb


def stratified_permutation(ms, stratum_key, binary=False, seed_offset=0):
    obs=effect(ms,binary=binary)
    if obs is None:return None
    strata=defaultdict(list)
    for i,m in enumerate(ms):strata[stratum_key(m)].append(i)
    base=[m['exclusive_suffix_class'] for m in ms]
    rng=random.Random(SEED+seed_offset)
    exceed=0; null_sum=0.0; null_sumsq=0.0
    exchangeable=0; informative_strata=0
    for idxs in strata.values():
        labs={base[i] for i in idxs}
        if len(idxs)>1 and len(labs)>1:
            exchangeable+=len(idxs);informative_strata+=1
    eps=1e-12
    for _ in range(ITERATIONS):
        labs=list(base)
        for idxs in strata.values():
            if len(idxs)<2:continue
            vals=[labs[i] for i in idxs]
            rng.shuffle(vals)
            for i,v in zip(idxs,vals):labs[i]=v
        d=effect_from_labels(ms,labs,binary=binary)
        if d is None:continue
        null_sum+=d;null_sumsq+=d*d
        if abs(d)+eps>=abs(obs['rate_difference']):exceed+=1
    p=(exceed+1)/(ITERATIONS+1)
    mean=null_sum/ITERATIONS
    var=max(0.0,null_sumsq/ITERATIONS-mean*mean)
    return {'observed':obs,'empirical_two_sided_p':p,'null_mean_rate_difference':mean,
            'null_sd_rate_difference':var**0.5,'stratum_count':len(strata),
            'informative_strata_count':informative_strata,'exchangeable_member_count':exchangeable,
            'permutation_iterations':ITERATIONS}


def subgroup_permutation(ms, label, seed_offset):
    sub=[m for m in ms if m['_provenance']==label]
    counts=Counter(m['exclusive_suffix_class'] for m in sub)
    out={'provenance':label,'member_count':len(sub),'target_member_count':counts.get(TARGET_CLASS,0),
         'other_member_count':len(sub)-counts.get(TARGET_CLASS,0)}
    if out['target_member_count']<2 or out['other_member_count']<2:
        out.update({'status':'insufficient_exchangeable_members','context_effect':None,'member_binary_effect':None})
        return out
    out['status']='estimable'
    out['context_effect']=stratified_permutation(sub,lambda m:'all',False,seed_offset)
    out['member_binary_effect']=stratified_permutation(sub,lambda m:'all',True,seed_offset+100)
    return out


def loo(ms, selector=None):
    rows=[]
    for i,m in enumerate(ms):
        if selector and not selector(m):continue
        sub=ms[:i]+ms[i+1:]
        ce=effect(sub,False);be=effect(sub,True)
        if ce is None or be is None:continue
        rows.append({'removed_member_id':m['member_id'],'removed_graphic_key':m['graphic_key'],
                     'removed_class':m['exclusive_suffix_class'],'removed_provenance':m['_provenance'],
                     'removed_page10':m['_page10'],'removed_target_proxy_count':m['_target_proxy_count'],
                     'context_rate_difference':ce['rate_difference'],'member_binary_rate_difference':be['rate_difference']})
    return rows


def summarize_loo(rows):
    if not rows:return {'case_count':0}
    c=[x['context_rate_difference'] for x in rows];b=[x['member_binary_rate_difference'] for x in rows]
    worst=min(rows,key=lambda x:x['context_rate_difference'])
    return {'case_count':len(rows),'context_rate_difference_min':min(c),'context_rate_difference_max':max(c),
            'context_nonpositive_count':sum(x<=0 for x in c),'member_binary_rate_difference_min':min(b),
            'member_binary_rate_difference_max':max(b),'member_binary_nonpositive_count':sum(x<=0 for x in b),
            'worst_context_case':worst}


def leave_group_out(ms,keyfunc,name):
    groups=sorted({keyfunc(m) for m in ms})
    out=[]
    for g in groups:
        sub=[m for m in ms if keyfunc(m)!=g]
        ce=effect(sub,False);be=effect(sub,True)
        if ce is None or be is None:continue
        out.append({'grouping':name,'removed_group':g,'remaining_member_count':len(sub),
                    'context_rate_difference':ce['rate_difference'],'member_binary_rate_difference':be['rate_difference']})
    return out


def main():
    src=json.loads((OUT/'ameke_constellation_members.json').read_text(encoding='utf-8'))
    ms=[enrich(m) for m in src['records']]
    assert len(ms)==147
    assert sum(m['exclusive_suffix_class']==TARGET_CLASS for m in ms)==27
    baseline_context=effect(ms,False);baseline_binary=effect(ms,True)
    target=[m for m in ms if m['exclusive_suffix_class']==TARGET_CLASS]
    target_proxy_members=[m for m in target if m['_target_proxy_binary']]
    target_context_total=sum(m['_target_proxy_count'] for m in target)
    concentration={'target_member_count':len(target),'target_members_with_proxy':len(target_proxy_members),
                   'target_proxy_context_count':target_context_total,
                   'max_proxy_contexts_in_one_target_member':max((m['_target_proxy_count'] for m in target),default=0),
                   'share_of_target_proxy_contexts_in_largest_member':(max((m['_target_proxy_count'] for m in target),default=0)/target_context_total if target_context_total else 0),
                   'target_members_with_proxy_ids':[m['member_id'] for m in target_proxy_members]}
    schemes=[
      ('unstratified',lambda m:'all'),
      ('source_provenance_signature',lambda m:m['_provenance']),
      ('printed_page_10_block',lambda m:m['_page10']),
      ('printed_page_5_block',lambda m:m['_page5']),
      ('source_x_page10',lambda m:(m['_provenance'],m['_page10'])),
    ]
    perm=[]
    for si,(name,key) in enumerate(schemes):
        for binary in (False,True):
            r=stratified_permutation(ms,key,binary,1000*si+(100 if binary else 0))
            perm.append({'scheme':name,'outcome':'member_binary_any_infinitive_proxy' if binary else 'context_rate_infinitive_proxy',**r})
    provenance_labels=sorted({m['_provenance'] for m in ms})
    subgroup=[subgroup_permutation(ms,p,5000+i*300) for i,p in enumerate(provenance_labels)]
    loo_all=loo(ms)
    loo_target=loo(ms,lambda m:m['exclusive_suffix_class']==TARGET_CLASS)
    page10_loo=leave_group_out(ms,lambda m:m['_page10'],'printed_page_10_block')
    prov_loo=leave_group_out(ms,lambda m:m['_provenance'],'source_provenance_signature')
    robust_perm=[x for x in perm if x['empirical_two_sided_p']<=0.05 and x['observed']['rate_difference']>0]
    summary={'dataset':'raramuri-historico-steffel-1809','layer':'ameke_ugameke_hostile_robustness_controls_v1','generated':'2026-08-13',
      'target_graphic_class':TARGET_CLASS,'target_german_context_proxy':TARGET_PROXY,'random_seed_base':SEED,
      'permutation_iterations_per_test':ITERATIONS,'member_count':len(ms),'baseline_context_effect':baseline_context,
      'baseline_member_binary_effect':baseline_binary,'target_signal_concentration':concentration,
      'permutation_scheme_count':len(schemes),'permutation_test_count':len(perm),
      'positive_p_le_0_05_permutation_test_count':len(robust_perm),
      'all_primary_context_permutation_schemes_p_le_0_05':all(x['empirical_two_sided_p']<=0.05 and x['observed']['rate_difference']>0 for x in perm if x['outcome']=='context_rate_infinitive_proxy'),
      'all_member_binary_permutation_schemes_p_le_0_05':all(x['empirical_two_sided_p']<=0.05 and x['observed']['rate_difference']>0 for x in perm if x['outcome']=='member_binary_any_infinitive_proxy'),
      'leave_one_member_out':summarize_loo(loo_all),'leave_one_target_member_out':summarize_loo(loo_target),
      'leave_one_page10_block_out':{'case_count':len(page10_loo),'context_rate_difference_min':min((x['context_rate_difference'] for x in page10_loo),default=None),'context_nonpositive_count':sum(x['context_rate_difference']<=0 for x in page10_loo)},
      'leave_one_provenance_out':{'case_count':len(prov_loo),'context_rate_difference_min':min((x['context_rate_difference'] for x in prov_loo),default=None),'context_nonpositive_count':sum(x['context_rate_difference']<=0 for x in prov_loo)},
      'human_reviewed':False,'automatic_morphological_analysis':False,'automatic_morpheme_assignment':False,
      'automatic_semantic_classification':False,'automatic_part_of_speech_tagging':False,'automatic_paradigm_inference':False,
      'interpretive_scope':'Stress tests of one pre-specified documentary association. Robustness to provenance/page stratification or leave-one-out influence does not identify a linguistic function.'}
    dump(OUT/'ameke_ugameke_robustness_controls.json',{'dataset':summary['dataset'],'layer':summary['layer'],'generated':summary['generated'],'count':len(perm),'permutation_tests':perm,'provenance_subgroups':subgroup,'leave_one_member_out':loo_all,'leave_one_target_member_out':loo_target,'leave_one_page10_block_out':page10_loo,'leave_one_provenance_out':prov_loo,'human_reviewed':False,'automatic_morphological_analysis':False,'automatic_semantic_classification':False})
    dump(OUT/'ameke_ugameke_robustness_controls_summary.json',summary)
    with (OUT/'ameke_ugameke_robustness_permutations.csv').open('w',encoding='utf-8',newline='') as f:
        fields=['scheme','outcome','empirical_two_sided_p','observed_rate_difference','observed_target_rate','observed_rest_rate','stratum_count','informative_strata_count','exchangeable_member_count','permutation_iterations']
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for x in perm:w.writerow({'scheme':x['scheme'],'outcome':x['outcome'],'empirical_two_sided_p':round(x['empirical_two_sided_p'],6),'observed_rate_difference':round(x['observed']['rate_difference'],6),'observed_target_rate':round(x['observed']['target_rate'],6),'observed_rest_rate':round(x['observed']['rest_rate'],6),'stratum_count':x['stratum_count'],'informative_strata_count':x['informative_strata_count'],'exchangeable_member_count':x['exchangeable_member_count'],'permutation_iterations':x['permutation_iterations']})
    print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__':main()
