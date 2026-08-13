#!/usr/bin/env python3
"""Build German documentary-gloss domain proxies for the historical -ameke constellation.

This layer classifies only the *German documentary context* into transparent,
rule-based surface domains. It does not assign Rarámuri semantic classes,
morphemes, POS, or historical functions. Direct RAR-DE glosses are re-parsed
from data/entries.csv; DE-RAR contexts come from the existing local-alignment
proposal layer and retain their review-risk tier.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import csv,json,random,re
from pathlib import Path
from research_common import OUT,rows,active,norm,gloss,dump

SEED=1809
ITERATIONS=20000
CLASSES=('ameke_other','gameke','iameke','ugameke','jameke')
DOMAINS=(
 'color_property_proxy','physical_property_proxy','human_person_agent_proxy',
 'state_condition_proxy','process_result_surface_proxy','other_or_unclassified'
)

COLOR={
 'rot','roth','schwarz','weiss','weis','gelb','grun','blau','grau','braun',
 'purpur','violett','grunlich','rotlich','schwarzlich','weisslich'
}
PHYSICAL={
 'gross','gros','klein','dick','dunn','kalt','heiss','heis','hart','weich','rund',
 'krumm','lang','kurz','scharf','stumpf','breit','schmal','hoch','niedrig','tief',
 'schwer','leicht','trocken','nass','wasserig','glatt','rauh','rauhig','dunne',
 'fleischig','holzern','frostig','fest','locker','hell','dunkel'
}
STATE={
 'krank','blind','schwanger','faul','tot','todt','lebendig','hungrig','durstig',
 'mude','ermudet','bewusst','unbewusst','gelehrt','klug','zornig','furchtsam',
 'heilend','allwissend','verstorben','verungluckt','kraftlos','arm','bose'
}
PERSON_WORDS={
 'getaufter','getaufte','getauften','rufende','rufender','erschaffer','ehemann',
 'eheweib','gemahl','mann','weib','person','mensch','kind','vater','mutter',
 'tochter','sohn','widder'
}
PARTICIPLE_PROXIES={'past_participle_surface_proxy','present_participle_surface_proxy'}

def load(name): return json.loads((OUT/name).read_text(encoding='utf-8'))

def german_tokens(s): return re.findall(r'[a-z]+',norm(s))

def has_stem(tokens,lexicon):
    for t in tokens:
        if t in lexicon:return True
        # modest inflection tolerance, documentary only
        for suf in ('e','en','er','es','em'):
            if t.endswith(suf) and len(t)-len(suf)>=3 and t[:-len(suf)] in lexicon:return True
    return False

def domain_proxies(label,functional_proxy=''):
    toks=german_tokens(label); text=' '.join(toks); tags=[]
    if has_stem(toks,COLOR): tags.append('color_property_proxy')
    if has_stem(toks,PHYSICAL): tags.append('physical_property_proxy')
    if has_stem(toks,STATE): tags.append('state_condition_proxy')
    person=(has_stem(toks,PERSON_WORDS) or bool(re.match(r'^(ein|eine|einen|einem|einer)\s+[a-z]+(?:er|e|en)?$',text)))
    if person: tags.append('human_person_agent_proxy')
    if functional_proxy in PARTICIPLE_PROXIES: tags.append('process_result_surface_proxy')
    if not tags: tags=['other_or_unclassified']
    return tags

def bh(pvals):
    m=len(pvals);order=sorted(range(m),key=lambda i:pvals[i]);q=[1.0]*m;run=1.0
    for r0 in range(m-1,-1,-1):
        i=order[r0];rank=r0+1;run=min(run,pvals[i]*m/rank);q[i]=min(1.0,run)
    return q

def calc(labels,vectors,cls,domain):
    tn=td=rn=rd=0
    for c,v in zip(labels,vectors):
        y=domain in v
        if c==cls:td+=1;tn+=int(y)
        else:rd+=1;rn+=int(y)
    tr=tn/td if td else 0.;rr=rn/rd if rd else 0.
    return tn,td,rn,rd,tr,rr,tr-rr

def permutation_tests(records,name):
    # collapse to unique class + analysis token to limit repeated documentary attestations
    g=defaultdict(list)
    for r in records:g[(r['exclusive_suffix_class'],r['analysis_token_key'])].append(r)
    units=[]
    for (c,k),items in sorted(g.items()):
        tags=set()
        for x in items:tags.update(x['german_documentary_domain_proxies'])
        units.append({'class':c,'token':k,'domains':tags})
    labels=[u['class'] for u in units];vectors=[u['domains'] for u in units]
    obs=[]
    for c in CLASSES:
        for d in DOMAINS[:-1]:obs.append((c,d,calc(labels,vectors,c,d)))
    rng=random.Random(SEED);perm=list(labels);raw=[0]*len(obs);mx=[0]*len(obs)
    for _ in range(ITERATIONS):
        rng.shuffle(perm);vals=[calc(perm,vectors,c,d)[-1] for c,d,_ in obs];m=max(abs(x) for x in vals) if vals else 0
        for i,v in enumerate(vals):
            if abs(v)+1e-12>=abs(obs[i][2][-1]):raw[i]+=1
            if m+1e-12>=abs(obs[i][2][-1]):mx[i]+=1
    ps=[(x+1)/(ITERATIONS+1) for x in raw];qs=bh(ps);fw=[(x+1)/(ITERATIONS+1) for x in mx]
    tests=[]
    for i,(c,d,x) in enumerate(obs):
        tn,td,rn,rd,tr,rr,delta=x
        tests.append({'analysis':name,'exclusive_suffix_class':c,'german_documentary_domain_proxy':d,'target_numerator':tn,'target_denominator':td,'rest_numerator':rn,'rest_denominator':rd,'target_rate':round(tr,6),'rest_rate':round(rr,6),'rate_difference':round(delta,6),'empirical_two_sided_p':round(ps[i],6),'bh_fdr_q':round(qs[i],6),'max_abs_rate_difference_fwer_p':round(fw[i],6),'conservative_signal':bool(qs[i]<=.05 and fw[i]<=.05 and abs(delta)>=.10 and td>=8 and tn>=3),'human_reviewed':False,'automatic_semantic_classification':False,'automatic_morphological_analysis':False})
    tests.sort(key=lambda x:(not x['conservative_signal'],x['max_abs_rate_difference_fwer_p'],x['bh_fdr_q'],-abs(x['rate_difference'])))
    return units,tests

def main():
    members=load('ameke_constellation_members.json')['records'];mby={m['member_id']:m for m in members}
    token=load('ameke_token_aware_members.json')['records'];tby={x['member_id']:x for x in token}
    entry_by={r.get('record_id'):r for r in rows() if active(r)}
    contexts=load('ameke_local_function_contexts.json')['records']
    direct_proxy={(x['member_id'],x.get('record_id','')):x.get('functional_proxy','') for x in contexts if x.get('source_layer')=='RAR-DE'}
    records=[];seen=set()

    # RAR-DE: derive German gloss again from source article, not the prior parsed context layer.
    for m in members:
        if 'RAR-DE' not in (m.get('source_layers') or []):continue
        t=tby.get(m['member_id']);
        if not t:continue
        for rid in m.get('rar_de_record_ids') or []:
            r=entry_by.get(rid)
            if not r:continue
            g=gloss(r.get('article_diplomatic',''),r.get('headword_diplomatic',''))
            tier='source_verified_rar_de_article_gloss' if g else 'source_article_unparsed'
            fp=''
            # Recompute minimal participial shape from source gloss by borrowing any exact matching direct context when available.
            for x in contexts:
                if x.get('source_layer')=='RAR-DE' and x.get('member_id')==m['member_id'] and norm(x.get('local_german_label',''))==norm(g):fp=x.get('functional_proxy','');break
            key=(m['member_id'],rid,norm(g),'RAR-DE')
            if key in seen:continue
            seen.add(key)
            tags=domain_proxies(g,fp)
            records.append({'member_id':m['member_id'],'record_id':rid,'exclusive_suffix_class':t['exclusive_suffix_class'],'analysis_token_key':t['analysis_token_key'],'source_direction':'RAR-DE','source_provenance':'direct_historical_entry','gloss_evidence_tier':tier,'source_verified_german_gloss':g,'machine_parsed_german_context':'','german_context_for_analysis':g,'functional_surface_proxy':fp,'german_documentary_domain_proxies':tags,'human_reviewed':False,'automatic_semantic_classification':False,'automatic_morphological_analysis':False})

    # DE-RAR: preserve machine local-alignment proposal and risk status.
    for x in contexts:
        if x.get('source_layer')!='DE-RAR-local-proposal':continue
        label=x.get('local_german_label','');risk=x.get('alignment_risk','high');tier='machine_local_de_rar_low_risk' if risk=='low' else 'machine_local_de_rar_high_risk'
        key=(x['member_id'],x.get('record_id',''),norm(label),'DE-RAR')
        if key in seen:continue
        seen.add(key)
        tags=domain_proxies(label,x.get('functional_proxy',''))
        records.append({'member_id':x['member_id'],'record_id':x.get('record_id',''),'exclusive_suffix_class':x['exclusive_suffix_class'],'analysis_token_key':x['analysis_token_key'],'source_direction':'DE-RAR','source_provenance':'local_alignment_proposal','gloss_evidence_tier':tier,'source_verified_german_gloss':'','machine_parsed_german_context':label,'german_context_for_analysis':label,'functional_surface_proxy':x.get('functional_proxy',''),'german_documentary_domain_proxies':tags,'human_reviewed':False,'automatic_semantic_classification':False,'automatic_morphological_analysis':False})

    analyses={}
    for name,subset in {
        'all_documentary':records,
        'conservative_documentary':[r for r in records if r['gloss_evidence_tier'] in {'source_verified_rar_de_article_gloss','machine_local_de_rar_low_risk'}],
        'direct_rar_de_only':[r for r in records if r['source_direction']=='RAR-DE'],
        'de_rar_low_risk_only':[r for r in records if r['gloss_evidence_tier']=='machine_local_de_rar_low_risk']
    }.items():
        units,tests=permutation_tests(subset,name)
        analyses[name]={'context_count':len(subset),'token_unit_count':len(units),'contexts_by_class':dict(Counter(r['exclusive_suffix_class'] for r in subset)),'domain_proxy_counts':dict(Counter(d for r in subset for d in r['german_documentary_domain_proxies'])),'domain_proxy_counts_by_class':{c:dict(Counter(d for r in subset if r['exclusive_suffix_class']==c for d in r['german_documentary_domain_proxies'])) for c in CLASSES},'conservative_signal_count':sum(t['conservative_signal'] for t in tests),'conservative_signals':[t for t in tests if t['conservative_signal']]}
    all_tests=[]
    for name,subset in {'all_documentary':records,'conservative_documentary':[r for r in records if r['gloss_evidence_tier'] in {'source_verified_rar_de_article_gloss','machine_local_de_rar_low_risk'}],'direct_rar_de_only':[r for r in records if r['source_direction']=='RAR-DE'],'de_rar_low_risk_only':[r for r in records if r['gloss_evidence_tier']=='machine_local_de_rar_low_risk']}.items():all_tests.extend(permutation_tests(subset,name)[1])
    summary={'dataset':'raramuri-historico-steffel-1809','layer':'ameke_german_documentary_domain_proxies_v1','generated':'2026-08-13','context_count':len(records),'source_verified_rar_de_count':sum(r['gloss_evidence_tier']=='source_verified_rar_de_article_gloss' for r in records),'de_rar_low_risk_count':sum(r['gloss_evidence_tier']=='machine_local_de_rar_low_risk' for r in records),'de_rar_high_risk_count':sum(r['gloss_evidence_tier']=='machine_local_de_rar_high_risk' for r in records),'random_seed':SEED,'permutation_iterations':ITERATIONS,'analyses':analyses,'human_reviewed':False,'automatic_semantic_classification':False,'automatic_morphological_analysis':False,'interpretive_scope':'Transparent rule-based domains assigned only to German documentary gloss/context strings. They are not Rarámuri semantic classes and do not establish historical morphology or grammatical function.'}
    dump(OUT/'ameke_documentary_domain_proxies.json',{'dataset':summary['dataset'],'count':len(records),'human_reviewed':False,'automatic_semantic_classification':False,'records':records})
    dump(OUT/'ameke_documentary_domain_proxies_summary.json',summary)
    dump(OUT/'ameke_documentary_domain_permutation_tests.json',{'dataset':summary['dataset'],'count':len(all_tests),'human_reviewed':False,'records':all_tests})
    with (OUT/'ameke_documentary_domain_proxies.csv').open('w',encoding='utf-8',newline='') as f:
        fields=['member_id','record_id','exclusive_suffix_class','analysis_token_key','source_direction','gloss_evidence_tier','source_verified_german_gloss','machine_parsed_german_context','german_context_for_analysis','functional_surface_proxy','german_documentary_domain_proxies','human_reviewed'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for r in records:w.writerow({**{k:r.get(k,'') for k in fields},'german_documentary_domain_proxies':' | '.join(r['german_documentary_domain_proxies'])})
    print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
