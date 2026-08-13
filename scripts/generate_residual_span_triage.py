#!/usr/bin/env python3
# Machine prioritization only; no automatic language identification or lexeme creation.
from __future__ import annotations
from collections import Counter
import csv,json,math,re
from research_common import OUT,rows,active,norm,alen,split_components,gloss,dump
ALPHA=0.5

def chargrams(value):
    k=norm(value).replace(' ','_')
    if not k:return []
    p='^'+k+'$'; out=[]
    for n in (2,3,4):
        out += [p[i:i+n] for i in range(len(p)-n+1)] if len(p)>=n else []
    return out

def words(value): return [w for w in re.findall(r'[a-z]+',norm(value)) if len(w)>=3]
def percentile(vals,q):
    if not vals:return 0.0
    s=sorted(vals); p=(len(s)-1)*q; lo=int(math.floor(p)); hi=int(math.ceil(p))
    return s[lo] if lo==hi else s[lo]+(s[hi]-s[lo])*(p-lo)
def lev(a,b,limit=4):
    if abs(len(a)-len(b))>limit:return limit+1
    prev=list(range(len(b)+1))
    for i,ca in enumerate(a,1):
        cur=[i]; row=i
        for j,cb in enumerate(b,1):
            v=min(cur[-1]+1,prev[j]+1,prev[j-1]+(ca!=cb));cur.append(v);row=min(row,v)
        if row>limit:return limit+1
        prev=cur
    return prev[-1]

def main():
    rr=[r for r in rows() if active(r)]; rar=[r for r in rr if r.get('direction')=='RAR-DE']; de=[r for r in rr if r.get('direction')=='DE-RAR']
    positive=[c for r in rar for c in split_components(r.get('headword_diplomatic','')) if alen(c)>=3]
    german=[(r.get('headword_diplomatic') or '') for r in de]
    for r in rar:german.extend(words(gloss(r.get('article_diplomatic',''),r.get('headword_diplomatic',''))))
    german=[x for x in german if alen(x)>=3]
    pc=Counter(g for x in positive for g in chargrams(x)); gc=Counter(g for x in german for g in chargrams(x)); vocab=set(pc)|set(gc); pt=sum(pc.values()); gt=sum(gc.values()); v=max(1,len(vocab))
    def score(x):
        gs=chargrams(x)
        if not gs:return 0.0
        return sum(math.log(((pc[g]+ALPHA)/(pt+ALPHA*v))/((gc[g]+ALPHA)/(gt+ALPHA*v))) for g in gs)/len(gs)
    ps=[score(x) for x in positive]; gs=[score(x) for x in german]
    strong=max(percentile(gs,.90),percentile(ps,.25)); possible=max(percentile(gs,.75),percentile(ps,.10)); german_thr=min(percentile(gs,.75),percentile(ps,.10))
    gv={w for x in german for w in words(x)}; rkeys=sorted({norm(x) for x in positive if alen(x)>=3})
    src=json.loads((OUT/'de_rar_residual_span_candidates.json').read_text(encoding='utf-8'))['records']; out=[]
    for rec in src:
        span=rec['candidate_span_diplomatic']; k=rec['graphic_key']; sc=score(span); toks=words(span); gh=sum(t in gv for t in toks); gratio=gh/len(toks) if toks else 0.0
        nearest=''; nd=None
        for rk in rkeys:
            if not rk or not k or rk[0]!=k[0] or abs(len(rk)-len(k))>3:continue
            d=lev(k,rk,4)
            if nd is None or d<nd or (d==nd and rk<nearest):nearest,nd=rk,d
        nsim=round(1-nd/max(len(k),len(nearest)),3) if nd is not None and nearest else 0.0
        if sc>=strong and gratio==0: cls='strong_raramuri_profile_signal'; conf='high_machine_signal'
        elif sc>=possible and gratio<.5: cls='possible_raramuri_profile_signal'; conf='medium_machine_signal'
        elif gratio>=.67 or sc<=german_thr: cls='german_context_profile_signal'; conf='high_machine_context_signal'
        else: cls='mixed_or_uncertain_profile'; conf='low_machine_signal'
        tier=1 if cls=='strong_raramuri_profile_signal' and nsim>=.70 else 2 if cls=='strong_raramuri_profile_signal' or (cls=='possible_raramuri_profile_signal' and nsim>=.70) else 3 if cls=='possible_raramuri_profile_signal' else 4
        out.append({'triage_id':'','source_candidate_id':rec['candidate_id'],'de_rar_record_id':rec['de_rar_record_id'],'de_rar_headword_diplomatic':rec['de_rar_headword_diplomatic'],'candidate_span_diplomatic':span,'graphic_key':k,'printed_page':rec['printed_page'],'profile_class':cls,'machine_signal_confidence':conf,'review_priority_tier':tier,'profile_log_likelihood_ratio':round(sc,4),'german_anchor_token_ratio':round(gratio,3),'nearest_rar_de_graphic_key':nearest,'nearest_rar_de_edit_distance':nd,'nearest_rar_de_similarity':nsim,'status':'machine_triage_only','human_reviewed':False,'decision':'not_assessed','method':'character_ngram_documentary_profile_triage_v1','interpretive_scope':'Profile-based prioritization only. The class is not a language identification, lexical entry, semantic judgment, cognacy claim or validation.'})
    out.sort(key=lambda x:(x['review_priority_tier'],-x['profile_log_likelihood_ratio'],-x['nearest_rar_de_similarity'],x['source_candidate_id']))
    for i,x in enumerate(out,1):x['triage_id']=f'RHD-RTRI-{i:06d}'
    counts=Counter(x['profile_class'] for x in out); tiers=Counter(str(x['review_priority_tier']) for x in out)
    summary={'dataset':'raramuri-historico-steffel-1809','generated':'2026-08-13','candidate_count':len(out),'profile_class_counts':dict(sorted(counts.items())),'review_priority_tier_counts':dict(sorted(tiers.items())),'thresholds':{'strong_raramuri_profile_signal':round(strong,4),'possible_raramuri_profile_signal':round(possible,4),'german_context_profile_signal_upper':round(german_thr,4)},'training_reference_counts':{'rar_de_components':len(positive),'german_reference_strings':len(german)},'human_reviewed':False,'automatic_language_identification':False,'automatic_lexeme_creation':False,'method':'character_ngram_documentary_profile_triage_v1'}
    dump(OUT/'de_rar_residual_span_triage.json',{'dataset':summary['dataset'],'layer':'de_rar_residual_span_profile_triage','generated':summary['generated'],'count':len(out),'human_reviewed':False,'automatic_language_identification':False,'automatic_lexeme_creation':False,'records':out}); dump(OUT/'de_rar_residual_span_triage_summary.json',summary)
    with (OUT/'de_rar_residual_span_triage.csv').open('w',encoding='utf-8',newline='') as f:
        fields=['triage_id','source_candidate_id','de_rar_record_id','de_rar_headword_diplomatic','candidate_span_diplomatic','graphic_key','printed_page','profile_class','machine_signal_confidence','review_priority_tier','profile_log_likelihood_ratio','german_anchor_token_ratio','nearest_rar_de_graphic_key','nearest_rar_de_edit_distance','nearest_rar_de_similarity','human_reviewed','decision'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader();[w.writerow({k:x.get(k,'') for k in fields}) for x in out]
    print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
