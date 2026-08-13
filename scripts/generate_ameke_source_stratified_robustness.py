#!/usr/bin/env python3
"""Source-stratified robustness tests for the local -ameke comparison.

Uses the already generated local-function context layer and repeats the same
20,000-permutation class-vs-rest test separately for:
- direct RAR-DE contexts only;
- low-risk DE-RAR local proposals only.

This separates evidence intrinsic to Steffel's RAR-DE direction from evidence
recovered through DE-RAR local alignment. It does not add POS tags, semantics,
or Raramuri morphological interpretation.
"""
from collections import Counter, defaultdict
import csv, json, random
from pathlib import Path

OUT=Path('data/research')
SEED=1809
ITERATIONS=20000
CLASSES=('ameke_other','gameke','iameke','ugameke','jameke')
OUTCOMES=('participle_surface_proxy','past_participle_surface_proxy','present_participle_surface_proxy')


def bh(p):
    m=len(p); order=sorted(range(m),key=lambda i:p[i]); q=[1.0]*m; run=1.0
    for r0 in range(m-1,-1,-1):
        i=order[r0]; run=min(run,p[i]*m/(r0+1)); q[i]=min(1.0,run)
    return q


def rate(labels,counts,totals,target,outcome):
    tn=td=rn=rd=0
    for lab,c,total in zip(labels,counts,totals):
        n=c.get(outcome,0)
        if lab==target:tn+=n;td+=total
        else:rn+=n;rd+=total
    tr=tn/td if td else 0.;rr=rn/rd if rd else 0.
    return tn,td,rn,rd,tr,rr,tr-rr


def run(name,ctx):
    groups=defaultdict(list)
    for x in ctx:groups[(x['exclusive_suffix_class'],x['analysis_token_key'])].append(x)
    units=[]
    for (cls,key),items in sorted(groups.items()):
        c=Counter(x['functional_proxy'] for x in items)
        c['participle_surface_proxy']=sum(bool(x['participle_surface_proxy']) for x in items)
        units.append((cls,key,c,len(items)))
    labels=[u[0] for u in units];counts=[u[2] for u in units];totals=[u[3] for u in units]
    obs=[]
    for cls in CLASSES:
        for o in OUTCOMES:obs.append((cls,o,rate(labels,counts,totals,cls,o)))
    raw=[0]*len(obs);mxp=[0]*len(obs);rng=random.Random(SEED);perm=list(labels);eps=1e-12
    for _ in range(ITERATIONS):
        rng.shuffle(perm)
        vals=[rate(perm,counts,totals,cls,o)[-1] for cls,o,_ in obs]
        mx=max(abs(v) for v in vals) if vals else 0
        for i,v in enumerate(vals):
            if abs(v)+eps>=abs(obs[i][2][-1]):raw[i]+=1
            if mx+eps>=abs(obs[i][2][-1]):mxp[i]+=1
    ps=[(x+1)/(ITERATIONS+1) for x in raw];fw=[(x+1)/(ITERATIONS+1) for x in mxp];qs=bh(ps)
    tests=[]
    for i,(cls,o,e) in enumerate(obs):
        tn,td,rn,rd,tr,rr,d=e
        sig=qs[i]<=.05 and fw[i]<=.05 and abs(d)>=.10 and td>=8 and tn>=3
        tests.append({'stratum':name,'exclusive_suffix_class':cls,'outcome':o,'target_numerator':tn,'target_denominator':td,'rest_numerator':rn,'rest_denominator':rd,'target_rate':round(tr,6),'rest_rate':round(rr,6),'rate_difference':round(d,6),'empirical_two_sided_p':round(ps[i],6),'bh_fdr_q':round(qs[i],6),'max_abs_rate_difference_fwer_p':round(fw[i],6),'conservative_signal':sig,'human_reviewed':False})
    tests.sort(key=lambda x:(not x['conservative_signal'],x['max_abs_rate_difference_fwer_p'],x['bh_fdr_q'],-abs(x['rate_difference'])))
    return {'context_count':len(ctx),'token_unit_count':len(units),'context_counts_by_class':{c:sum(x['exclusive_suffix_class']==c for x in ctx) for c in CLASSES},'participle_counts_by_class':{c:sum(x['exclusive_suffix_class']==c and x['participle_surface_proxy'] for x in ctx) for c in CLASSES},'conservative_signal_count':sum(x['conservative_signal'] for x in tests),'conservative_signals':[x for x in tests if x['conservative_signal']]},tests


def main():
    ctx=json.loads((OUT/'ameke_local_function_contexts.json').read_text(encoding='utf-8'))['records']
    strata={
      'direct_rar_de_only':[x for x in ctx if x['source_layer']=='RAR-DE'],
      'de_rar_low_risk_only':[x for x in ctx if x['source_layer']=='DE-RAR-local-proposal' and x['alignment_risk']=='low']
    }
    summaries={};alltests=[]
    for name,items in strata.items():
        s,t=run(name,items);summaries[name]=s;alltests.extend(t)
    out={'dataset':'raramuri-historico-steffel-1809','layer':'ameke_source_stratified_robustness_v1','generated':'2026-08-13','random_seed':SEED,'permutation_iterations':ITERATIONS,'strata':summaries,'human_reviewed':False,'automatic_part_of_speech_tagging':False,'automatic_morphological_analysis':False,'interpretive_scope':'Source-stratified robustness of German local-label surface proxies. Separate strata test whether a signal is present in direct RAR-DE documentation and/or low-risk DE-RAR local alignments; no grammatical interpretation is assigned.'}
    (OUT/'ameke_source_stratified_robustness_summary.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUT/'ameke_source_stratified_robustness_tests.json').write_text(json.dumps({'dataset':out['dataset'],'count':len(alltests),'human_reviewed':False,'records':alltests},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (OUT/'ameke_source_stratified_robustness_tests.csv').open('w',encoding='utf-8',newline='') as f:
        fields=['stratum','exclusive_suffix_class','outcome','target_numerator','target_denominator','rest_numerator','rest_denominator','target_rate','rest_rate','rate_difference','empirical_two_sided_p','bh_fdr_q','max_abs_rate_difference_fwer_p','conservative_signal','human_reviewed'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader();[w.writerow({k:x.get(k,'') for k in fields}) for x in alltests]
    print(json.dumps(out,ensure_ascii=False))

if __name__=='__main__':main()
