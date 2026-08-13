#!/usr/bin/env python3
"""Article-cluster controls for low-risk DE-RAR -ameke local alignments.

Two conservative documentary collapses are tested:
1) unique_record_class_cells: at most one observation per DE-RAR record × graphic class;
2) single_class_articles_only: only DE-RAR records whose retained low-risk contexts
   all belong to one graphic class, with one binary observation per article.

The outcome is whether an article/cell contains a participle-shaped local German
label (and separately a past-participle-shaped label). This reduces inflation from
multiple recovered forms inside the same German article. No POS or Raramuri
morphological claims are made.
"""
from collections import Counter, defaultdict
import csv, json, random
from pathlib import Path

OUT=Path('data/research');SEED=1809;ITERATIONS=20000
CLASSES=('ameke_other','gameke','iameke','ugameke','jameke')
OUTCOMES=('participle_surface_proxy','past_participle_surface_proxy')


def bh(p):
    m=len(p);order=sorted(range(m),key=lambda i:p[i]);q=[1.0]*m;run=1.0
    for r0 in range(m-1,-1,-1):
        i=order[r0];run=min(run,p[i]*m/(r0+1));q[i]=min(1.0,run)
    return q


def test_rows(name,rows):
    labels=[x['exclusive_suffix_class'] for x in rows]
    obs=[]
    for cls in CLASSES:
        for o in OUTCOMES:
            tn=sum(x[o] for x in rows if x['exclusive_suffix_class']==cls);td=sum(x['exclusive_suffix_class']==cls for x in rows)
            rn=sum(x[o] for x in rows if x['exclusive_suffix_class']!=cls);rd=len(rows)-td
            tr=tn/td if td else 0.;rr=rn/rd if rd else 0.;obs.append((cls,o,tn,td,rn,rd,tr,rr,tr-rr))
    raw=[0]*len(obs);mxp=[0]*len(obs);rng=random.Random(SEED);perm=list(labels);eps=1e-12
    for _ in range(ITERATIONS):
        rng.shuffle(perm);vals=[]
        for cls,o,*_ in obs:
            tn=sum(x[o] for lab,x in zip(perm,rows) if lab==cls);td=sum(lab==cls for lab in perm)
            rn=sum(x[o] for lab,x in zip(perm,rows) if lab!=cls);rd=len(rows)-td
            vals.append((tn/td if td else 0.)-(rn/rd if rd else 0.))
        mx=max(abs(v) for v in vals) if vals else 0
        for i,v in enumerate(vals):
            if abs(v)+eps>=abs(obs[i][-1]):raw[i]+=1
            if mx+eps>=abs(obs[i][-1]):mxp[i]+=1
    ps=[(x+1)/(ITERATIONS+1) for x in raw];fw=[(x+1)/(ITERATIONS+1) for x in mxp];qs=bh(ps)
    tests=[]
    for i,z in enumerate(obs):
        cls,o,tn,td,rn,rd,tr,rr,d=z;sig=qs[i]<=.05 and fw[i]<=.05 and abs(d)>=.10 and td>=8 and tn>=3
        tests.append({'analysis':name,'exclusive_suffix_class':cls,'outcome':o,'target_numerator':tn,'target_denominator':td,'rest_numerator':rn,'rest_denominator':rd,'target_rate':round(tr,6),'rest_rate':round(rr,6),'rate_difference':round(d,6),'empirical_two_sided_p':round(ps[i],6),'bh_fdr_q':round(qs[i],6),'max_abs_rate_difference_fwer_p':round(fw[i],6),'conservative_signal':sig,'human_reviewed':False})
    tests.sort(key=lambda x:(not x['conservative_signal'],x['max_abs_rate_difference_fwer_p'],x['bh_fdr_q'],-abs(x['rate_difference'])))
    return {'observation_count':len(rows),'counts_by_class':dict(Counter(x['exclusive_suffix_class'] for x in rows)),'participle_counts_by_class':{c:sum(x['exclusive_suffix_class']==c and x['participle_surface_proxy'] for x in rows) for c in CLASSES},'past_participle_counts_by_class':{c:sum(x['exclusive_suffix_class']==c and x['past_participle_surface_proxy'] for x in rows) for c in CLASSES},'conservative_signal_count':sum(x['conservative_signal'] for x in tests),'conservative_signals':[x for x in tests if x['conservative_signal']]},tests


def main():
    ctx=json.loads((OUT/'ameke_local_function_contexts.json').read_text(encoding='utf-8'))['records']
    ctx=[x for x in ctx if x['source_layer']=='DE-RAR-local-proposal' and x['alignment_risk']=='low']
    byrec=defaultdict(list)
    for x in ctx:byrec[x['record_id']].append(x)
    cells=[]
    for rid,items in sorted(byrec.items()):
        bycls=defaultdict(list)
        for x in items:bycls[x['exclusive_suffix_class']].append(x)
        for cls,ys in sorted(bycls.items()):
            cells.append({'record_id':rid,'exclusive_suffix_class':cls,'participle_surface_proxy':any(y['participle_surface_proxy'] for y in ys),'past_participle_surface_proxy':any(y['functional_proxy']=='past_participle_surface_proxy' for y in ys),'source_context_count':len(ys)})
    single=[]
    mixed=0
    for rid,items in sorted(byrec.items()):
        classes=sorted(set(x['exclusive_suffix_class'] for x in items))
        if len(classes)!=1:mixed+=1;continue
        single.append({'record_id':rid,'exclusive_suffix_class':classes[0],'participle_surface_proxy':any(x['participle_surface_proxy'] for x in items),'past_participle_surface_proxy':any(x['functional_proxy']=='past_participle_surface_proxy' for x in items),'source_context_count':len(items)})
    a,ta=test_rows('unique_record_class_cells',cells);b,tb=test_rows('single_class_articles_only',single)
    summary={'dataset':'raramuri-historico-steffel-1809','layer':'ameke_de_rar_article_cluster_robustness_v1','generated':'2026-08-13','low_risk_context_count':len(ctx),'unique_de_rar_record_count':len(byrec),'mixed_class_record_count':mixed,'analyses':{'unique_record_class_cells':a,'single_class_articles_only':b},'random_seed':SEED,'permutation_iterations':ITERATIONS,'human_reviewed':False,'automatic_part_of_speech_tagging':False,'automatic_morphological_analysis':False,'interpretive_scope':'Article-collapsed control for low-risk DE-RAR local-label surface proxies. Collapsing prevents repeated recovered forms within one German article from inflating evidence; no grammatical category is assigned to Raramuri forms.'}
    tests=ta+tb
    (OUT/'ameke_article_cluster_robustness_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUT/'ameke_article_cluster_robustness_tests.json').write_text(json.dumps({'dataset':summary['dataset'],'count':len(tests),'human_reviewed':False,'records':tests},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (OUT/'ameke_article_cluster_robustness_tests.csv').open('w',encoding='utf-8',newline='') as f:
        fields=['analysis','exclusive_suffix_class','outcome','target_numerator','target_denominator','rest_numerator','rest_denominator','target_rate','rest_rate','rate_difference','empirical_two_sided_p','bh_fdr_q','max_abs_rate_difference_fwer_p','conservative_signal','human_reviewed'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader();[w.writerow({k:x.get(k,'') for k in fields}) for x in tests]
    print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__':main()
