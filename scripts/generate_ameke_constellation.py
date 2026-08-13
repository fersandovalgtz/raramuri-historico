#!/usr/bin/env python3
"""Analyze the historical -ameke graphic constellation without morphological claims.

This layer isolates forms whose conservative graphic key ends in -ameke and
compares the nested graphic endings -ameke, -gameke, -iameke, -ugameke and
-jameke. It strips those endings mechanically to create base-string contrast
candidates, combines source recurrence, German documentary context, page
coverage, and Steffel's internal DE-RAR↔RAR-DE concordance, and emits review
priorities.

It does NOT segment morphology, assign morphemes or grammatical categories,
identify lexemes, infer semantic functions, reconstruct forms, or mark human
validation.
"""
from __future__ import annotations
from collections import Counter, defaultdict
import csv, json, re
from research_common import OUT, rows, active, norm, alen, split_components, gloss, dump

STRONG_RECOVERY_GRADES={'A_machine_documentary_signal','B_machine_documentary_signal','C_machine_profile_signal'}
SUFFIXES=('ameke','gameke','iameke','ugameke','jameke')
EXCLUSIVE_ORDER=('ugameke','iameke','jameke','gameke','ameke')
STOP={'aber','alle','als','am','an','auch','auf','aus','bei','beim','bis','da','das','dem','den','der','des','die','ein','eine','einem','einen','einer','eines','er','es','für','hat','haben','im','in','ist','item','man','mit','nach','nicht','noch','oder','ohne','sein','sind','so','und','vom','von','vor','war','werden','wie','wird','zu','zum','zur'}
INF_END=('eln','ern','en'); PROP_END=('förmig','ig','lich','isch','haft','sam','bar','los'); NOM_END=('ung','heit','keit','nis','schaft','tum')

def tokens(text): return sorted({w for w in re.findall(r'[a-z]+',norm(text)) if len(w)>=3 and w not in STOP})
def shape_proxy(text):
    ws=[w for w in re.findall(r'[a-z]+',norm(text)) if len(w)>=3]
    if len(ws)!=1:return 'multiword_or_ambiguous_proxy'
    w=ws[0]
    if w.endswith(NOM_END):return 'nominalization_ending_proxy'
    if w.endswith(PROP_END):return 'property_ending_proxy'
    if w.endswith(INF_END):return 'infinitive_ending_proxy'
    return 'other_single_word_proxy'
def lev(a,b):
    prev=list(range(len(b)+1))
    for i,ca in enumerate(a,1):
        cur=[i]
        for j,cb in enumerate(b,1):cur.append(min(cur[-1]+1,prev[j]+1,prev[j-1]+(ca!=cb)))
        prev=cur
    return prev[-1]
def exclusive_class(key):
    for suffix in EXCLUSIVE_ORDER:
        if key.endswith(suffix) and len(key)>len(suffix):return 'ameke_other' if suffix=='ameke' else suffix
    return None
def stripped_suffix(cls): return 'ameke' if cls=='ameke_other' else cls

def build_universe():
    u=defaultdict(lambda:{'surface_forms':set(),'source_layers':set(),'rar_de_record_ids':set(),'recovery_ids':set(),'printed_pages':set(),'german_contexts':set()})
    for r in rows():
        if not active(r) or r.get('direction')!='RAR-DE':continue
        form=(r.get('headword_diplomatic') or '').strip(); g=gloss(r.get('article_diplomatic',''),form)
        for c in split_components(form):
            k=norm(c)
            if not k.endswith('ameke'):continue
            x=u[k];x['surface_forms'].add(c);x['source_layers'].add('RAR-DE');x['rar_de_record_ids'].add(r.get('record_id',''))
            if r.get('printed_page'):x['printed_pages'].add(int(r['printed_page']))
            if g:x['german_contexts'].add(g)
    rec=json.loads((OUT/'de_rar_residual_recovery_queue.json').read_text(encoding='utf-8'))['records']
    for r in rec:
        if r['evidence_grade'] not in STRONG_RECOVERY_GRADES:continue
        k=r['graphic_key']
        if not k.endswith('ameke'):continue
        x=u[k];x['surface_forms'].update(r['surface_forms']);x['source_layers'].add('DE-RAR-residual-recovery');x['recovery_ids'].add(r['recovery_id'])
        x['printed_pages'].update(int(p) for p in r.get('printed_pages',[]) if p);x['german_contexts'].update(h for h in r.get('de_rar_headwords',[]) if h)
    return u

def concordance_map():
    out=defaultdict(list)
    for x in json.loads((OUT/'internal_concordance.json').read_text(encoding='utf-8'))['records']:out[x['graphic_key']].append(x)
    return out

def member_record(i,key,data,cmap):
    cls=exclusive_class(key)
    if not cls:return None
    suffix=stripped_suffix(cls);base=key[:-len(suffix)]
    if alen(base)<1:return None
    conc=cmap.get(key,[]);reciprocal=sum(1 for x in conc if x.get('relation',{}).get('reciprocal_german_support') is True);proxy=Counter(shape_proxy(g) for g in data['german_contexts'])
    return {'member_id':f'RHD-AMEKE-{i:05d}','graphic_key':key,'surface_forms':sorted(data['surface_forms']),'exclusive_suffix_class':cls,'mechanically_stripped_suffix':suffix,'mechanically_stripped_base':base,'base_alphanumeric_length':alen(base),'inclusive_suffix_matches':[s for s in SUFFIXES if key.endswith(s)],'source_layers':sorted(data['source_layers']),'rar_de_record_ids':sorted(x for x in data['rar_de_record_ids'] if x),'recovery_ids':sorted(data['recovery_ids']),'printed_pages':sorted(data['printed_pages']),'german_contexts':sorted(data['german_contexts']),'german_context_shape_proxy_counts':dict(sorted(proxy.items())),'internal_concordance_count':len(conc),'internal_reciprocal_german_support_count':reciprocal,'internally_reattested':bool(conc),'internal_reciprocal_support':bool(reciprocal),'status':'machine_ameke_graphic_member','human_reviewed':False,'automatic_morphological_analysis':False,'automatic_morpheme_assignment':False,'automatic_semantic_classification':False,'interpretive_scope':'Mechanical string decomposition inside the -ameke constellation; the stripped base and suffix class are not asserted to be linguistic morphemes or lexemes.'}
def context_tokens(m):
    out=set()
    for g in m['german_contexts']:out.update(tokens(g))
    return out
def contrast_priority(kind,a,b,shared):
    internal=int(a['internally_reattested'])+int(b['internally_reattested']);reciprocal=int(a['internal_reciprocal_support'])+int(b['internal_reciprocal_support'])
    if kind=='exact_shared_stripped_base' and internal==2 and reciprocal>=1:return 1
    if kind=='exact_shared_stripped_base' and internal>=1:return 2
    if kind=='exact_shared_stripped_base':return 3
    if internal==2 and shared:return 3
    return 4

def build_contrasts(members):
    out=[]
    for i,a in enumerate(members):
        for b in members[i+1:]:
            if a['exclusive_suffix_class']==b['exclusive_suffix_class']:continue
            ba=a['mechanically_stripped_base'];bb=b['mechanically_stripped_base']
            if ba==bb:kind='exact_shared_stripped_base';dist=0
            else:
                if min(alen(ba),alen(bb))<3:continue
                dist=lev(ba,bb)
                if dist!=1:continue
                kind='edit_distance_one_stripped_base_neighbor'
            shared=sorted(context_tokens(a)&context_tokens(b));pri=contrast_priority(kind,a,b,shared)
            out.append({'contrast_id':'','contrast_type':kind,'review_priority_tier':pri,'member_a_id':a['member_id'],'member_a_key':a['graphic_key'],'member_a_suffix_class':a['exclusive_suffix_class'],'member_a_base':ba,'member_b_id':b['member_id'],'member_b_key':b['graphic_key'],'member_b_suffix_class':b['exclusive_suffix_class'],'member_b_base':bb,'base_edit_distance':dist,'shared_german_context_tokens':shared,'shared_german_context_token_count':len(shared),'both_internally_reattested':a['internally_reattested'] and b['internally_reattested'],'either_internal_reciprocal_support':a['internal_reciprocal_support'] or b['internal_reciprocal_support'],'status':'machine_ameke_base_contrast_candidate','human_reviewed':False,'automatic_morphological_analysis':False,'automatic_semantic_judgment':False,'interpretive_scope':'Contrast between mechanically stripped base strings in different nested -ameke classes. Exact/shared or edit-distance-one bases do not establish a paradigm, derivation, morphology, lexical identity or semantic relation.'})
    out.sort(key=lambda x:(x['review_priority_tier'],0 if x['contrast_type']=='exact_shared_stripped_base' else 1,-x['shared_german_context_token_count'],x['member_a_key'],x['member_b_key']))
    for i,x in enumerate(out,1):x['contrast_id']=f'RHD-AMEKE-C-{i:05d}'
    return out

def suffix_profiles(members):
    profiles=[]
    for cls in ['ameke_other','gameke','iameke','ugameke','jameke']:
        ms=[m for m in members if m['exclusive_suffix_class']==cls];contexts=[g for m in ms for g in m['german_contexts']];pc=Counter(shape_proxy(g) for g in contexts)
        profiles.append({'exclusive_suffix_class':cls,'member_count':len(ms),'german_context_count':len(contexts),'internally_reattested_member_count':sum(m['internally_reattested'] for m in ms),'internal_reciprocal_support_member_count':sum(m['internal_reciprocal_support'] for m in ms),'distinct_printed_page_count':len({p for m in ms for p in m['printed_pages']}),'german_context_shape_proxy_counts':dict(sorted(pc.items())),'german_context_shape_proxy_rates':{k:round(v/len(contexts),3) for k,v in sorted(pc.items())} if contexts else {}})
    return profiles
def proxy_contrasts(profiles):
    out=[];proxies=sorted({k for p in profiles for k in p['german_context_shape_proxy_counts']})
    for i,a in enumerate(profiles):
        for b in profiles[i+1:]:
            if a['german_context_count']<10 or b['german_context_count']<10:continue
            for pr in proxies:
                ra=a['german_context_shape_proxy_rates'].get(pr,0.0);rb=b['german_context_shape_proxy_rates'].get(pr,0.0)
                out.append({'class_a':a['exclusive_suffix_class'],'class_b':b['exclusive_suffix_class'],'proxy':pr,'rate_a':ra,'rate_b':rb,'absolute_rate_difference':round(abs(ra-rb),3),'status':'machine_descriptive_rate_contrast','human_reviewed':False})
    out.sort(key=lambda x:(-x['absolute_rate_difference'],x['class_a'],x['class_b'],x['proxy']));return out[:30]

def main():
    universe=build_universe();cmap=concordance_map();members=[]
    for key in sorted(universe):
        m=member_record(len(members)+1,key,universe[key],cmap)
        if m:members.append(m)
    contrasts=build_contrasts(members);profiles=suffix_profiles(members);inclusive={s:sum(1 for m in members if s in m['inclusive_suffix_matches']) for s in SUFFIXES};exclusive=Counter(m['exclusive_suffix_class'] for m in members)
    groups=defaultdict(list)
    for m in members:groups[m['mechanically_stripped_base']].append(m)
    exact=[]
    for base,ms in sorted(groups.items()):
        if len({m['exclusive_suffix_class'] for m in ms})<2:continue
        exact.append({'mechanically_stripped_base':base,'member_ids':[m['member_id'] for m in ms],'graphic_keys':[m['graphic_key'] for m in ms],'suffix_classes':sorted({m['exclusive_suffix_class'] for m in ms}),'member_count':len(ms),'all_internally_reattested':all(m['internally_reattested'] for m in ms),'any_internal_reciprocal_support':any(m['internal_reciprocal_support'] for m in ms)})
    summary={'dataset':'raramuri-historico-steffel-1809','generated':'2026-08-13','layer':'ameke_graphic_constellation_v1','member_count':len(members),'inclusive_suffix_member_counts':inclusive,'exclusive_suffix_member_counts':dict(sorted(exclusive.items())),'members_internally_reattested':sum(m['internally_reattested'] for m in members),'members_with_internal_reciprocal_support':sum(m['internal_reciprocal_support'] for m in members),'exact_shared_stripped_base_group_count':len(exact),'exact_shared_stripped_base_groups':exact,'base_contrast_candidate_count':len(contrasts),'exact_base_contrast_pair_count':sum(x['contrast_type']=='exact_shared_stripped_base' for x in contrasts),'edit_distance_one_base_contrast_pair_count':sum(x['contrast_type']=='edit_distance_one_stripped_base_neighbor' for x in contrasts),'contrast_review_priority_tier_counts':dict(sorted(Counter(x['review_priority_tier'] for x in contrasts).items())),'exclusive_suffix_profiles':profiles,'top_descriptive_proxy_rate_contrasts':proxy_contrasts(profiles),'human_reviewed':False,'automatic_morphological_analysis':False,'automatic_morpheme_assignment':False,'automatic_semantic_classification':False,'automatic_paradigm_inference':False,'method':'nested_suffix_string_decomposition_and_documentary_base_contrast_v1','interpretive_scope':'Descriptive machine analysis of nested -ameke strings, mechanically stripped bases, German source contexts, page recurrence and internal Steffel reattestation. No morphological, grammatical, lexical or semantic function is asserted.'}
    dump(OUT/'ameke_constellation_members.json',{'dataset':summary['dataset'],'layer':'ameke_constellation_members','generated':summary['generated'],'count':len(members),'human_reviewed':False,'automatic_morphological_analysis':False,'automatic_morpheme_assignment':False,'records':members});dump(OUT/'ameke_base_contrast_candidates.json',{'dataset':summary['dataset'],'layer':'ameke_base_contrast_candidates','generated':summary['generated'],'count':len(contrasts),'human_reviewed':False,'automatic_morphological_analysis':False,'automatic_semantic_judgment':False,'records':contrasts});dump(OUT/'ameke_constellation_summary.json',summary)
    with (OUT/'ameke_constellation_members.csv').open('w',encoding='utf-8',newline='') as f:
        fields=['member_id','graphic_key','surface_forms','exclusive_suffix_class','mechanically_stripped_suffix','mechanically_stripped_base','source_layers','printed_pages','german_contexts','internal_concordance_count','internal_reciprocal_german_support_count','human_reviewed'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for m in members:w.writerow({'member_id':m['member_id'],'graphic_key':m['graphic_key'],'surface_forms':' | '.join(m['surface_forms']),'exclusive_suffix_class':m['exclusive_suffix_class'],'mechanically_stripped_suffix':m['mechanically_stripped_suffix'],'mechanically_stripped_base':m['mechanically_stripped_base'],'source_layers':' | '.join(m['source_layers']),'printed_pages':' | '.join(map(str,m['printed_pages'])),'german_contexts':' | '.join(m['german_contexts']),'internal_concordance_count':m['internal_concordance_count'],'internal_reciprocal_german_support_count':m['internal_reciprocal_german_support_count'],'human_reviewed':False})
    with (OUT/'ameke_base_contrast_candidates.csv').open('w',encoding='utf-8',newline='') as f:
        fields=['contrast_id','contrast_type','review_priority_tier','member_a_key','member_a_suffix_class','member_a_base','member_b_key','member_b_suffix_class','member_b_base','base_edit_distance','shared_german_context_tokens','both_internally_reattested','either_internal_reciprocal_support','human_reviewed'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for x in contrasts:w.writerow({'contrast_id':x['contrast_id'],'contrast_type':x['contrast_type'],'review_priority_tier':x['review_priority_tier'],'member_a_key':x['member_a_key'],'member_a_suffix_class':x['member_a_suffix_class'],'member_a_base':x['member_a_base'],'member_b_key':x['member_b_key'],'member_b_suffix_class':x['member_b_suffix_class'],'member_b_base':x['member_b_base'],'base_edit_distance':x['base_edit_distance'],'shared_german_context_tokens':' | '.join(x['shared_german_context_tokens']),'both_internally_reattested':x['both_internally_reattested'],'either_internal_reciprocal_support':x['either_internal_reciprocal_support'],'human_reviewed':False})
    print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
