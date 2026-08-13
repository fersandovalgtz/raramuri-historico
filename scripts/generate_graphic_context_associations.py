#!/usr/bin/env python3
"""Cross Steffel graphic-family hypotheses with German documentary context.

This layer measures associations between recurrent historical strings / graphic
neighborhoods and the German headwords or local glosses already present in the
source. It uses document-frequency log-odds and transparent German word-shape
proxies. It does NOT assign meanings, parts of speech, morphemes, paradigms,
lexemes, cognates, or human validation.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import csv,json,math,re
from research_common import OUT,rows,active,norm,split_components,gloss,dump

STOP={
    'aber','alle','als','am','an','auch','auf','aus','bei','beim','bis','da','das','dem','den','der','des','die',
    'ein','eine','einem','einen','einer','eines','er','es','für','hat','haben','im','in','ist','item','man','mit',
    'nach','nicht','noch','oder','ohne','sein','sind','so','und','vom','von','vor','war','werden','wie','wird','zu','zum','zur'
}

INF_END=('eln','ern','en')
PROP_END=('förmig','ig','lich','isch','haft','sam','bar','los')
NOM_END=('ung','heit','keit','nis','schaft','tum')


def tokens(text):
    return sorted({w for w in re.findall(r'[a-z]+',norm(text)) if len(w)>=3 and w not in STOP})


def shape_proxy(text):
    k=norm(text)
    ws=[w for w in re.findall(r'[a-z]+',k) if len(w)>=3]
    if len(ws)!=1:return 'multiword_or_ambiguous_proxy'
    w=ws[0]
    if w.endswith(NOM_END):return 'nominalization_ending_proxy'
    if w.endswith(PROP_END):return 'property_ending_proxy'
    if w.endswith(INF_END):return 'infinitive_ending_proxy'
    return 'other_single_word_proxy'


def build_context_map():
    ctx=defaultdict(set)
    provenance=defaultdict(list)
    for r in rows():
        if not active(r):continue
        if r.get('direction')=='RAR-DE':
            form=(r.get('headword_diplomatic') or '').strip()
            g=gloss(r.get('article_diplomatic',''),form)
            if not g:continue
            for c in split_components(form):
                k=norm(c)
                if not k:continue
                ctx[k].add(g)
                provenance[k].append({'source_layer':'RAR-DE','record_id':r.get('record_id',''),'german_context':g,'printed_page':int(r.get('printed_page') or 0)})
    rec=json.loads((OUT/'de_rar_residual_recovery_queue.json').read_text(encoding='utf-8'))['records']
    for x in rec:
        if x['evidence_grade'] not in {'A_machine_documentary_signal','B_machine_documentary_signal','C_machine_profile_signal'}:continue
        k=x['graphic_key']
        for h in x['de_rar_headwords']:
            if h:
                ctx[k].add(h)
                provenance[k].append({'source_layer':'DE-RAR-residual-recovery','recovery_id':x['recovery_id'],'german_context':h})
    return ctx,provenance


def token_df(ctx):
    out=Counter()
    for vals in ctx.values():
        seen=set()
        for v in vals:seen.update(tokens(v))
        out.update(seen)
    return out


def enrichment(member_keys,ctx,global_df,N):
    covered=[k for k in member_keys if k in ctx and ctx[k]]
    n=len(covered)
    if not n:return [],0
    local=Counter()
    for k in covered:
        seen=set()
        for v in ctx[k]:seen.update(tokens(v))
        local.update(seen)
    scored=[]
    for tok,a in local.items():
        if a<2:continue
        g=global_df[tok]; b=max(0,g-a); c=max(0,n-a); d=max(0,(N-n)-b)
        score=math.log((a+.5)/(c+.5))-math.log((b+.5)/(d+.5))
        coverage=a/n
        robust=a>=3 and coverage>=.10 and score>=1.5
        scored.append({'token':tok,'member_key_document_frequency':a,'global_key_document_frequency':g,'member_coverage':round(coverage,3),'log_odds_enrichment':round(score,4),'robust_under_method':robust})
    scored.sort(key=lambda x:(-x['log_odds_enrichment'],-x['member_key_document_frequency'],x['token']))
    return scored[:15],n


def proxies(member_keys,ctx):
    cnt=Counter(); total=0
    for k in member_keys:
        for v in sorted(ctx.get(k,set())):
            cnt[shape_proxy(v)]+=1; total+=1
    rates={k:round(v/total,3) for k,v in sorted(cnt.items())} if total else {}
    return dict(sorted(cnt.items())),rates,total


def proxy_enrichment(local_counts,local_total,global_counts,global_total):
    if not local_total or not global_total:return []
    out=[]
    for label,g in sorted(global_counts.items()):
        a=local_counts.get(label,0); b=max(0,g-a); c=max(0,local_total-a); d=max(0,(global_total-local_total)-b)
        score=math.log((a+.5)/(c+.5))-math.log((b+.5)/(d+.5))
        lr=a/local_total; gr=g/global_total
        robust=local_total>=10 and a>=5 and lr>=max(gr*1.5,gr+.05) and score>=.75
        out.append({'proxy':label,'local_count':a,'local_rate':round(lr,3),'global_count':g,'global_rate':round(gr,3),'rate_ratio':round(lr/gr,3) if gr else None,'log_odds_enrichment':round(score,4),'robust_under_method':robust})
    out.sort(key=lambda x:(-x['log_odds_enrichment'],-x['local_count'],x['proxy']))
    return out


def main():
    ctx,prov=build_context_map(); N=len(ctx); global_df=token_df(ctx)
    global_proxy=Counter()
    for vals in ctx.values():
        for v in vals:global_proxy[shape_proxy(v)]+=1
    global_proxy_total=sum(global_proxy.values())
    gp=json.loads((OUT/'graphic_pattern_hypotheses.json').read_text(encoding='utf-8'))['records']
    gf=json.loads((OUT/'graphic_family_hypotheses.json').read_text(encoding='utf-8'))['records']

    patterns=[]
    for p in gp:
        members=p['members']; top,cov=enrichment(members,ctx,global_df,N); pc,pr,ct=proxies(members,ctx); pe=proxy_enrichment(pc,ct,global_proxy,global_proxy_total)
        patterns.append({'association_id':'','pattern_id':p['pattern_id'],'pattern':p['pattern'],'pattern_type':p['pattern_type'],'pattern_member_count':len(members),'context_covered_member_count':cov,'context_coverage_ratio':round(cov/len(members),3) if members else 0.0,'german_context_string_count':ct,'german_word_shape_proxy_counts':pc,'german_word_shape_proxy_rates':pr,'german_word_shape_proxy_enrichment':pe,'top_german_context_token_associations':top,'robust_token_association_count':sum(t['robust_under_method'] for t in top),'robust_proxy_association_count':sum(x['robust_under_method'] for x in pe),'status':'machine_documentary_context_association','human_reviewed':False,'automatic_semantic_classification':False,'automatic_part_of_speech_tagging':False,'automatic_morphological_analysis':False,'interpretive_scope':'German documentary-context association for a recurrent string pattern. Enrichment and word-shape proxies are not semantic categories, parts of speech, morphemes or validated linguistic functions.'})
    patterns.sort(key=lambda x:(-x['context_covered_member_count'],-len(x['top_german_context_token_associations']),x['pattern_type'],x['pattern']))
    for i,x in enumerate(patterns,1):x['association_id']=f'RHD-GCTX-P-{i:05d}'

    families=[]
    for f in gf:
        keys=[f['seed_graphic_key']]+[n['graphic_key'] for n in f['neighbors']]
        keys=sorted(set(keys)); top,cov=enrichment(keys,ctx,global_df,N); pc,pr,ct=proxies(keys,ctx); pe=proxy_enrichment(pc,ct,global_proxy,global_proxy_total)
        families.append({'association_id':'','family_hypothesis_id':f['family_hypothesis_id'],'seed_recovery_id':f['seed_recovery_id'],'seed_graphic_key':f['seed_graphic_key'],'family_key_count':len(keys),'context_covered_key_count':cov,'context_coverage_ratio':round(cov/len(keys),3) if keys else 0.0,'german_context_string_count':ct,'german_word_shape_proxy_counts':pc,'german_word_shape_proxy_rates':pr,'german_word_shape_proxy_enrichment':pe,'top_german_context_token_associations':top,'robust_token_association_count':sum(t['robust_under_method'] for t in top),'robust_proxy_association_count':sum(x['robust_under_method'] for x in pe),'status':'machine_documentary_context_association','human_reviewed':False,'automatic_semantic_classification':False,'automatic_part_of_speech_tagging':False,'automatic_morphological_analysis':False,'interpretive_scope':'German documentary-context association for a graphic neighborhood. Token enrichment and word-shape proxies do not establish meaning, grammatical category, morphology, lexical identity or historical continuity.'})
    families.sort(key=lambda x:(-x['context_covered_key_count'],-len(x['top_german_context_token_associations']),x['seed_graphic_key']))
    for i,x in enumerate(families,1):x['association_id']=f'RHD-GCTX-F-{i:05d}'

    top_patterns=[]; robust_tokens=[]; robust_proxies=[]
    for x in patterns:
        if x['top_german_context_token_associations']:
            y=x['top_german_context_token_associations'][0]
            top_patterns.append({'pattern_id':x['pattern_id'],'pattern':x['pattern'],'pattern_type':x['pattern_type'],'covered_members':x['context_covered_member_count'],'top_token':y['token'],'top_token_member_df':y['member_key_document_frequency'],'top_token_member_coverage':y['member_coverage'],'top_token_log_odds':y['log_odds_enrichment'],'robust_under_method':y['robust_under_method']})
        for y in x['top_german_context_token_associations']:
            if y['robust_under_method']:
                robust_tokens.append({'pattern_id':x['pattern_id'],'pattern':x['pattern'],'pattern_type':x['pattern_type'],**y})
        for y in x['german_word_shape_proxy_enrichment']:
            if y['robust_under_method']:
                robust_proxies.append({'pattern_id':x['pattern_id'],'pattern':x['pattern'],'pattern_type':x['pattern_type'],'context_count':x['german_context_string_count'],**y})
    top_patterns.sort(key=lambda x:(-x['top_token_log_odds'],-x['top_token_member_df'],x['pattern']))
    robust_tokens.sort(key=lambda x:(-x['log_odds_enrichment'],-x['member_key_document_frequency'],x['pattern'],x['token']))
    robust_proxies.sort(key=lambda x:(-x['log_odds_enrichment'],-x['local_count'],x['pattern'],x['proxy']))
    summary={'dataset':'raramuri-historico-steffel-1809','generated':'2026-08-13','context_key_universe_count':N,'pattern_association_count':len(patterns),'family_association_count':len(families),'patterns_with_context':sum(x['context_covered_member_count']>0 for x in patterns),'families_with_context':sum(x['context_covered_key_count']>0 for x in families),'patterns_with_enriched_tokens':sum(bool(x['top_german_context_token_associations']) for x in patterns),'families_with_enriched_tokens':sum(bool(x['top_german_context_token_associations']) for x in families),'global_german_word_shape_proxy_counts':dict(sorted(global_proxy.items())),'top_pattern_token_associations':top_patterns[:20],'robust_pattern_token_association_count':len(robust_tokens),'robust_pattern_token_associations':robust_tokens[:30],'robust_pattern_proxy_association_count':len(robust_proxies),'robust_pattern_proxy_associations':robust_proxies[:30],'robustness_note':'Token robustness requires member_df>=3, member coverage>=0.10 and log-odds>=1.5. Proxy robustness requires >=10 context strings, local count>=5, local rate >=1.5x global and +0.05 absolute, and log-odds>=0.75. These remain machine signals, not semantic or grammatical classifications.','human_reviewed':False,'automatic_semantic_classification':False,'automatic_part_of_speech_tagging':False,'automatic_morphological_analysis':False,'automatic_morpheme_assignment':False,'method':'document_frequency_log_odds_context_association_v2'}
    dump(OUT/'graphic_context_pattern_associations.json',{'dataset':summary['dataset'],'layer':'steffel_graphic_pattern_german_context_associations','generated':summary['generated'],'count':len(patterns),'human_reviewed':False,'automatic_semantic_classification':False,'automatic_part_of_speech_tagging':False,'records':patterns})
    dump(OUT/'graphic_context_family_associations.json',{'dataset':summary['dataset'],'layer':'steffel_graphic_family_german_context_associations','generated':summary['generated'],'count':len(families),'human_reviewed':False,'automatic_semantic_classification':False,'automatic_part_of_speech_tagging':False,'records':families})
    dump(OUT/'graphic_context_associations_summary.json',summary)
    with (OUT/'graphic_context_pattern_associations.csv').open('w',encoding='utf-8',newline='') as f:
        fields=['association_id','pattern_id','pattern','pattern_type','pattern_member_count','context_covered_member_count','context_coverage_ratio','german_context_string_count','robust_token_association_count','robust_proxy_association_count','top_tokens','robust_proxies','human_reviewed'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for x in patterns:w.writerow({'association_id':x['association_id'],'pattern_id':x['pattern_id'],'pattern':x['pattern'],'pattern_type':x['pattern_type'],'pattern_member_count':x['pattern_member_count'],'context_covered_member_count':x['context_covered_member_count'],'context_coverage_ratio':x['context_coverage_ratio'],'german_context_string_count':x['german_context_string_count'],'robust_token_association_count':x['robust_token_association_count'],'robust_proxy_association_count':x['robust_proxy_association_count'],'top_tokens':' | '.join(t['token'] for t in x['top_german_context_token_associations']),'robust_proxies':' | '.join(p['proxy'] for p in x['german_word_shape_proxy_enrichment'] if p['robust_under_method']),'human_reviewed':False})
    with (OUT/'graphic_context_family_associations.csv').open('w',encoding='utf-8',newline='') as f:
        fields=['association_id','family_hypothesis_id','seed_recovery_id','seed_graphic_key','family_key_count','context_covered_key_count','context_coverage_ratio','german_context_string_count','robust_token_association_count','robust_proxy_association_count','top_tokens','robust_proxies','human_reviewed'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for x in families:w.writerow({'association_id':x['association_id'],'family_hypothesis_id':x['family_hypothesis_id'],'seed_recovery_id':x['seed_recovery_id'],'seed_graphic_key':x['seed_graphic_key'],'family_key_count':x['family_key_count'],'context_covered_key_count':x['context_covered_key_count'],'context_coverage_ratio':x['context_coverage_ratio'],'german_context_string_count':x['german_context_string_count'],'robust_token_association_count':x['robust_token_association_count'],'robust_proxy_association_count':x['robust_proxy_association_count'],'top_tokens':' | '.join(t['token'] for t in x['top_german_context_token_associations']),'robust_proxies':' | '.join(p['proxy'] for p in x['german_word_shape_proxy_enrichment'] if p['robust_under_method']),'human_reviewed':False})
    print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__':main()
