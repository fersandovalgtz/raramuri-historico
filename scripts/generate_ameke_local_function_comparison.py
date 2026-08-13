#!/usr/bin/env python3
"""Compare -ameke graphic classes using locally aligned German labels.

This supersedes article-headword proxy comparisons for the current research front.
It combines direct RAR-DE German glosses with DE-RAR local-label proposals, maps
all contexts to token-aware documentary units, and applies conservative German
surface-shape proxies. No German POS tagger, semantic classifier, or Raramuri
morphological analysis is performed.

Two analyses are produced:
1) all_machine_local: all proposed local labels plus direct RAR-DE contexts;
2) conservative_alignment: direct RAR-DE contexts plus DE-RAR proposals marked
   low review risk.

Permutation unit: unique (exclusive graphic class, analysis token) unit.
"""
from __future__ import annotations
from collections import Counter, defaultdict
import csv, json, math, random, re, unicodedata
from pathlib import Path

OUT = Path('data/research')
SEED = 1809
ITERATIONS = 20000
CLASS_ORDER = ('ameke_other','gameke','iameke','ugameke','jameke')

SEPARABLE_GE_PREFIXES = (
    'abge','ange','aufge','ausge','einge','festge','fortge','herge','hinge','losge',
    'mitge','nachge','niederge','stattge','teilge','umge','unterge','vorge','wegge',
    'weiterge','wiederge','zuge','zuruckge','zurückge'
)
INSEPARABLE_PREFIXES = ('be','emp','ent','er','miss','ver','zer')
PROPERTY_ENDINGS = ('ig','lich','isch','haft','sam','bar','los','ern','förmig')
NOMINAL_ENDINGS = ('ung','heit','keit','nis','schaft','tum')
EXPLICIT_STRONG_PAST = {'gethan'}


def load(name):
    return json.loads((OUT/name).read_text(encoding='utf-8'))


def norm_de(s):
    s = unicodedata.normalize('NFKD', s or '')
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r'\s+', ' ', s.replace('ſ','s').replace('ß','ss').casefold()).strip(' ,;:.!?-')


def single_word(s):
    k = norm_de(s)
    ws = re.findall(r'[a-z]+', k)
    return ws[0] if len(ws)==1 else ''


def strip_inf(w):
    if w.endswith('en') and len(w)>4: return w[:-2]
    if w.endswith('n') and len(w)>4: return w[:-1]
    return w


def strip_participle(w):
    x=w
    for p in SEPARABLE_GE_PREFIXES:
        if x.startswith(p):
            x=x[len(p):]
            break
    else:
        if x.startswith('ge') and len(x)>5: x=x[2:]
        else:
            for p in INSEPARABLE_PREFIXES:
                if x.startswith(p) and len(x)>len(p)+3:
                    x=x[len(p):]
                    break
    if x.endswith('et') and len(x)>4: x=x[:-2]
    elif x.endswith('t') and len(x)>3: x=x[:-1]
    elif x.endswith('en') and len(x)>4: x=x[:-2]
    return x


def similarity(a,b):
    if not a or not b:return 0.0
    m,n=len(a),len(b)
    prev=list(range(n+1))
    for i,ca in enumerate(a,1):
        cur=[i]
        for j,cb in enumerate(b,1):
            cur.append(min(cur[-1]+1,prev[j]+1,prev[j-1]+(ca!=cb)))
        prev=cur
    d=prev[-1]
    return 1-d/max(m,n)


def classify(label, article_headword=''):
    k=norm_de(label); w=single_word(label); h=single_word(article_headword)
    if not w:
        return 'multiword_or_ambiguous_proxy'
    if w.endswith('end') and len(w)>=6:
        return 'present_participle_surface_proxy'
    if w in EXPLICIT_STRONG_PAST:
        return 'past_participle_surface_proxy'
    strong_ge = w.startswith('ge') or w.startswith('unge') or any(w.startswith(p) for p in SEPARABLE_GE_PREFIXES)
    if strong_ge and (w.endswith('t') or w.endswith('en') or w.endswith('et') or w in EXPLICIT_STRONG_PAST):
        return 'past_participle_surface_proxy'
    if h and w != h and w.startswith(INSEPARABLE_PREFIXES) and (w.endswith('t') or w.endswith('en') or w.endswith('et')):
        if similarity(strip_participle(w), strip_inf(h)) >= .55:
            return 'past_participle_surface_proxy'
    if w.endswith(PROPERTY_ENDINGS):
        return 'property_surface_proxy'
    if w.endswith(NOMINAL_ENDINGS):
        return 'nominal_surface_proxy'
    return 'other_single_word_proxy'


def bh_qvalues(pvals):
    m=len(pvals); order=sorted(range(m), key=lambda i:pvals[i]); q=[1.0]*m; running=1.0
    for rank0 in range(m-1,-1,-1):
        i=order[rank0]; rank=rank0+1
        running=min(running,pvals[i]*m/rank); q[i]=min(1.0,running)
    return q


def rate_diff(labels, vectors, target_class, outcome):
    tn=td=rn=rd=0
    for lab,v in zip(labels,vectors):
        total=sum(v.values()); count=int(v.get(outcome,0))
        if lab==target_class: tn+=count; td+=total
        else: rn+=count; rd+=total
    tr=tn/td if td else 0.; rr=rn/rd if rd else 0.
    return tn,td,rn,rd,tr,rr,tr-rr


def permutation_tests(units, analysis_name):
    labels=[u['exclusive_suffix_class'] for u in units]
    vectors=[Counter(u['functional_proxy_counts']) for u in units]
    outcomes=('participle_surface_proxy','past_participle_surface_proxy','present_participle_surface_proxy')
    obs=[]
    for cls in CLASS_ORDER:
        for outcome in outcomes:
            obs.append((cls,outcome,rate_diff(labels,vectors,cls,outcome)))
    raw=[0]*len(obs); maxx=[0]*len(obs); rng=random.Random(SEED); perm=list(labels); eps=1e-12
    for _ in range(ITERATIONS):
        rng.shuffle(perm)
        vals=[]
        for cls,outcome,_ in obs:
            vals.append(rate_diff(perm,vectors,cls,outcome)[-1])
        mx=max(abs(v) for v in vals) if vals else 0
        for i,v in enumerate(vals):
            if abs(v)+eps >= abs(obs[i][2][-1]): raw[i]+=1
            if mx+eps >= abs(obs[i][2][-1]): maxx[i]+=1
    ps=[(x+1)/(ITERATIONS+1) for x in raw]
    fw=[(x+1)/(ITERATIONS+1) for x in maxx]
    qs=bh_qvalues(ps)
    tests=[]
    for i,(cls,outcome,e) in enumerate(obs):
        tn,td,rn,rd,tr,rr,diff=e
        sig=qs[i]<=.05 and fw[i]<=.05 and abs(diff)>=.10 and td>=10 and tn>=3
        tests.append({
            'analysis':analysis_name,'exclusive_suffix_class':cls,'outcome':outcome,
            'target_numerator':tn,'target_denominator':td,'rest_numerator':rn,'rest_denominator':rd,
            'target_rate':round(tr,6),'rest_rate':round(rr,6),'rate_difference':round(diff,6),
            'empirical_two_sided_p':round(ps[i],6),'bh_fdr_q':round(qs[i],6),
            'max_abs_rate_difference_fwer_p':round(fw[i],6),'conservative_signal':sig,
            'human_reviewed':False,'automatic_part_of_speech_tagging':False,
            'automatic_morphological_analysis':False
        })
    tests.sort(key=lambda x:(not x['conservative_signal'],x['max_abs_rate_difference_fwer_p'],x['bh_fdr_q'],-abs(x['rate_difference'])))
    for i,x in enumerate(tests,1):x['review_rank']=i
    return tests


def main():
    members=load('ameke_constellation_members.json')['records']
    tok=load('ameke_token_aware_members.json')['records']
    props=load('ameke_local_context_ai_proposals.json')['records']
    m_by={x['member_id']:x for x in members}; t_by={x['member_id']:x for x in tok}
    contexts=[]
    seen=set()
    # Direct RAR-DE contexts are already locally aligned by dictionary direction.
    for m in members:
        if 'RAR-DE' not in (m.get('source_layers') or []): continue
        t=t_by[m['member_id']]
        for g in m.get('german_contexts') or []:
            key=(m['member_id'],'RAR-DE',g)
            if key in seen:continue
            seen.add(key)
            proxy=classify(g,'')
            contexts.append({'member_id':m['member_id'],'exclusive_suffix_class':t['exclusive_suffix_class'],
                'analysis_token_key':t['analysis_token_key'],'source_layer':'RAR-DE','record_id':' | '.join(m.get('rar_de_record_ids') or []),
                'article_headword':'','local_german_label':g,'alignment_risk':'direct','functional_proxy':proxy,
                'human_reviewed':False})
    # DE-RAR recovered contexts use the local-label proposal layer, not article headwords.
    for p in props:
        if p['member_id'] not in t_by: continue
        t=t_by[p['member_id']]
        key=(p['member_id'],p['record_id'],p['proposed_local_german_label'])
        if key in seen:continue
        seen.add(key)
        proxy=classify(p['proposed_local_german_label'],p.get('article_headword',''))
        contexts.append({'member_id':p['member_id'],'exclusive_suffix_class':t['exclusive_suffix_class'],
            'analysis_token_key':t['analysis_token_key'],'source_layer':'DE-RAR-local-proposal','record_id':p['record_id'],
            'article_headword':p.get('article_headword',''),'local_german_label':p['proposed_local_german_label'],
            'alignment_risk':p.get('proposal_review_risk','high'),'functional_proxy':proxy,'human_reviewed':False})

    for x in contexts:
        x['participle_surface_proxy']=x['functional_proxy'] in {'past_participle_surface_proxy','present_participle_surface_proxy'}

    analyses={}
    for name,ctxs in {
        'all_machine_local':contexts,
        'conservative_alignment':[x for x in contexts if x['source_layer']=='RAR-DE' or x['alignment_risk']=='low']
    }.items():
        groups=defaultdict(list)
        for x in ctxs: groups[(x['exclusive_suffix_class'],x['analysis_token_key'])].append(x)
        units=[]
        for (cls,key),items in sorted(groups.items()):
            c=Counter(x['functional_proxy'] for x in items)
            c['participle_surface_proxy']=sum(x['participle_surface_proxy'] for x in items)
            units.append({'exclusive_suffix_class':cls,'analysis_token_key':key,'context_count':len(items),
                'functional_proxy_counts':dict(c),'member_ids':sorted(set(x['member_id'] for x in items))})
        tests=permutation_tests(units,name)
        analyses[name]={'context_count':len(ctxs),'token_unit_count':len(units),
            'token_unit_counts_by_class':dict(Counter(u['exclusive_suffix_class'] for u in units)),
            'functional_proxy_counts':dict(Counter(x['functional_proxy'] for x in ctxs)),
            'participle_surface_proxy_count':sum(x['participle_surface_proxy'] for x in ctxs),
            'class_context_counts':{c:sum(x['exclusive_suffix_class']==c for x in ctxs) for c in CLASS_ORDER},
            'class_participle_counts':{c:sum(x['exclusive_suffix_class']==c and x['participle_surface_proxy'] for x in ctxs) for c in CLASS_ORDER},
            'conservative_signal_count':sum(x['conservative_signal'] for x in tests),
            'conservative_signals':[x for x in tests if x['conservative_signal']],
            'tests':tests}

    summary={'dataset':'raramuri-historico-steffel-1809','layer':'ameke_local_german_function_comparison_v1',
        'generated':'2026-08-13','random_seed':SEED,'permutation_iterations':ITERATIONS,
        'context_count_total':len(contexts),'direct_rar_de_context_count':sum(x['source_layer']=='RAR-DE' for x in contexts),
        'de_rar_local_proposal_context_count':sum(x['source_layer']!='RAR-DE' for x in contexts),
        'de_rar_low_risk_context_count':sum(x['source_layer']!='RAR-DE' and x['alignment_risk']=='low' for x in contexts),
        'analyses':{k:{kk:vv for kk,vv in v.items() if kk!='tests'} for k,v in analyses.items()},
        'human_reviewed':False,'automatic_part_of_speech_tagging':False,'automatic_morphological_analysis':False,
        'interpretive_scope':'German local-label surface comparison across token-aware documentary classes. Participle proxies are conservative orthographic/morphographic heuristics, not POS tags; signals do not establish a Raramuri morpheme or grammatical function.'}
    (OUT/'ameke_local_function_contexts.json').write_text(json.dumps({'dataset':summary['dataset'],'count':len(contexts),'human_reviewed':False,'records':contexts},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    all_tests=[]
    for v in analyses.values(): all_tests.extend(v['tests'])
    (OUT/'ameke_local_function_permutation_tests.json').write_text(json.dumps({'dataset':summary['dataset'],'count':len(all_tests),'human_reviewed':False,'records':all_tests},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUT/'ameke_local_function_comparison_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (OUT/'ameke_local_function_contexts.csv').open('w',encoding='utf-8',newline='') as f:
        fields=['member_id','exclusive_suffix_class','analysis_token_key','source_layer','record_id','article_headword','local_german_label','alignment_risk','functional_proxy','participle_surface_proxy','human_reviewed'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader();
        for x in contexts:w.writerow({k:x.get(k,'') for k in fields})
    with (OUT/'ameke_local_function_permutation_tests.csv').open('w',encoding='utf-8',newline='') as f:
        fields=['review_rank','analysis','exclusive_suffix_class','outcome','target_numerator','target_denominator','rest_numerator','rest_denominator','target_rate','rest_rate','rate_difference','empirical_two_sided_p','bh_fdr_q','max_abs_rate_difference_fwer_p','conservative_signal','human_reviewed'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader();
        for x in all_tests:w.writerow({k:x.get(k,'') for k in fields})
    print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__': main()
