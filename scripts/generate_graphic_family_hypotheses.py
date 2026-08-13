#!/usr/bin/env python3
"""Generate non-adjudicative graphic-family hypotheses from Steffel.

The 47 grade-A residual recovery groups are used only as documentary seeds.
This script discovers recurrent prefixes/suffixes and bounded graphic
neighborhoods across the historical RAR-DE inventory and residual recovery
queue. It does NOT perform morphological segmentation, assign morphemes,
identify language, create lexemes, infer cognacy, or mark human validation.
"""
from __future__ import annotations
from collections import defaultdict
import csv,json,re
from research_common import OUT,rows,active,norm,alen,split_components,dump

STRONG_GRADES={'A_machine_documentary_signal','B_machine_documentary_signal','C_machine_profile_signal'}

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

def lcp(a,b):
    n=0
    for x,y in zip(a,b):
        if x!=y:break
        n+=1
    return n

def lcs(a,b): return lcp(a[::-1],b[::-1])
def sim(a,b,d=None):
    if not a or not b:return 0.0
    if d is None:d=lev(a,b,4)
    return round(1-d/max(len(a),len(b)),3)
def median(vals):
    s=sorted(vals); n=len(s)
    if not n:return 0
    return s[n//2] if n%2 else round((s[n//2-1]+s[n//2])/2,1)

def pattern_candidates(keys,seed_keys,kind):
    bucket=defaultdict(set); seed_bucket=defaultdict(set)
    for k in keys:
        maxn=min(7,len(k)-1)
        for n in range(3,maxn+1):
            p=k[:n] if kind=='prefix' else k[-n:]
            bucket[p].add(k)
            if k in seed_keys:seed_bucket[p].add(k)
    raw=[]
    for p,members in bucket.items():
        seeds=seed_bucket.get(p,set())
        if len(members)<3 or len(seeds)<2:continue
        raw.append({'pattern':p,'pattern_type':f'recurrent_{kind}_candidate','length':len(p),'member_count':len(members),'grade_a_seed_count':len(seeds),'members':sorted(members),'grade_a_seed_members':sorted(seeds)})
    keep=[]
    for x in sorted(raw,key=lambda z:(-z['length'],-z['member_count'],z['pattern'])):
        if any(set(x['members'])==set(y['members']) and x['pattern_type']==y['pattern_type'] for y in keep):continue
        keep.append(x)
    keep.sort(key=lambda z:(-z['grade_a_seed_count'],-z['member_count'],-z['length'],z['pattern']))
    return keep

def main():
    rec=json.loads((OUT/'de_rar_residual_recovery_queue.json').read_text(encoding='utf-8'))['records']
    seeds=[x for x in rec if x['evidence_grade']=='A_machine_documentary_signal']
    recovery=[x for x in rec if x['evidence_grade'] in STRONG_GRADES]
    rar=[]
    for r in rows():
        if not active(r) or r.get('direction')!='RAR-DE':continue
        for c in split_components(r.get('headword_diplomatic','')):
            k=norm(c)
            if alen(k)>=3:rar.append({'record_id':r.get('record_id',''),'form_diplomatic':c,'graphic_key':k,'printed_page':int(r.get('printed_page') or 0)})
    rar_by_key=defaultdict(list)
    for x in rar:rar_by_key[x['graphic_key']].append(x)
    recovery_by_key={x['graphic_key']:x for x in recovery}; seed_keys={x['graphic_key'] for x in seeds}; universe=sorted(set(rar_by_key)|set(recovery_by_key))
    prefixes=pattern_candidates(universe,seed_keys,'prefix'); suffixes=pattern_candidates(universe,seed_keys,'suffix'); patterns=prefixes+suffixes
    for i,x in enumerate(patterns,1):
        x['pattern_id']=f'RHD-GPAT-{i:05d}';x['status']='machine_graphic_pattern_hypothesis';x['human_reviewed']=False;x['interpretive_scope']='Recurrent string pattern only; not a morpheme, morphological rule, phonological correspondence or validated linguistic unit.'
    neighborhoods=[]
    for seed in sorted(seeds,key=lambda x:x['graphic_key']):
        sk=seed['graphic_key']; candidates=[]
        for k in universe:
            if k==sk:continue
            mn=min(len(sk),len(k)); mx=max(len(sk),len(k))
            if mn<3:continue
            d=lev(sk,k,4); s=sim(sk,k,d) if d<=4 else 0.0; cp=lcp(sk,k); cs=lcs(sk,k)
            long_shared=max(cp,cs)>=max(4,int(round(mn*.55))); bounded_edit=(d<=2 and mx<=10) or (d<=3 and mx>10 and s>=.75)
            if not (long_shared or bounded_edit):continue
            reasons=[]
            if bounded_edit:reasons.append('bounded_graphic_edit_neighbor')
            if cp>=max(4,int(round(mn*.55))):reasons.append('shared_long_prefix')
            if cs>=max(4,int(round(mn*.55))):reasons.append('shared_long_suffix')
            source='rar_de_inventory' if k in rar_by_key else 'residual_recovery'; payload={'graphic_key':k,'source_layer':source,'edit_distance':d if d<=4 else None,'similarity':s,'shared_prefix_length':cp,'shared_suffix_length':cs,'evidence_reasons':reasons}
            if source=='rar_de_inventory':payload['rar_de_attestations']=rar_by_key[k]
            else:
                rr=recovery_by_key[k];payload['recovery_id']=rr['recovery_id'];payload['surface_forms']=rr['surface_forms'];payload['evidence_grade']=rr['evidence_grade'];payload['de_rar_headwords']=rr['de_rar_headwords']
            candidates.append(payload)
        candidates.sort(key=lambda x:(-len(x['evidence_reasons']),-x['similarity'],-max(x['shared_prefix_length'],x['shared_suffix_length']),x['graphic_key']))
        neighborhoods.append({'family_hypothesis_id':'','seed_recovery_id':seed['recovery_id'],'seed_graphic_key':sk,'seed_surface_forms':seed['surface_forms'],'seed_de_rar_headwords':seed['de_rar_headwords'],'seed_occurrence_count':seed['occurrence_count'],'neighbors':candidates,'neighbor_count':len(candidates),'status':'machine_graphic_family_hypothesis','human_reviewed':False,'automatic_morphological_analysis':False,'interpretive_scope':'Exhaustive bounded graphic neighborhood around a grade-A documentary seed under this method. Shared strings and edit proximity are not morphemes, paradigms, cognates or validated lexical relations.'})
    neighborhoods.sort(key=lambda x:(-x['neighbor_count'],x['seed_graphic_key']))
    for i,x in enumerate(neighborhoods,1):x['family_hypothesis_id']=f'RHD-GFAM-{i:05d}'
    counts=[x['neighbor_count'] for x in neighborhoods]; suffix_focus=[x for x in patterns if x['pattern_type']=='recurrent_suffix_candidate'][:30]; prefix_focus=[x for x in patterns if x['pattern_type']=='recurrent_prefix_candidate'][:30]
    summary={'dataset':'raramuri-historico-steffel-1809','generated':'2026-08-13','grade_a_seed_count':len(seeds),'strong_profile_recovery_universe_count':len(recovery),'rar_de_graphic_key_count':len(rar_by_key),'graphic_universe_key_count':len(universe),'family_hypothesis_count':len(neighborhoods),'families_with_neighbors':sum(x['neighbor_count']>0 for x in neighborhoods),'total_neighbor_links':sum(counts),'median_neighbor_count':median(counts),'max_neighbor_count':max(counts) if counts else 0,'neighborhoods_exhaustive_under_method':True,'recurrent_prefix_pattern_count':len(prefixes),'recurrent_suffix_pattern_count':len(suffixes),'top_prefix_patterns':[{'pattern':x['pattern'],'member_count':x['member_count'],'grade_a_seed_count':x['grade_a_seed_count']} for x in prefix_focus],'top_suffix_patterns':[{'pattern':x['pattern'],'member_count':x['member_count'],'grade_a_seed_count':x['grade_a_seed_count']} for x in suffix_focus],'human_reviewed':False,'automatic_morphological_analysis':False,'automatic_morpheme_assignment':False,'automatic_lexeme_creation':False,'method':'grade_a_seeded_graphic_family_hypotheses_v1'}
    dump(OUT/'graphic_family_hypotheses.json',{'dataset':summary['dataset'],'layer':'steffel_graphic_family_hypotheses','generated':summary['generated'],'count':len(neighborhoods),'human_reviewed':False,'automatic_morphological_analysis':False,'automatic_morpheme_assignment':False,'neighborhoods_exhaustive_under_method':True,'records':neighborhoods})
    dump(OUT/'graphic_pattern_hypotheses.json',{'dataset':summary['dataset'],'layer':'steffel_recurrent_graphic_pattern_hypotheses','generated':summary['generated'],'count':len(patterns),'human_reviewed':False,'automatic_morphological_analysis':False,'automatic_morpheme_assignment':False,'records':patterns})
    dump(OUT/'graphic_family_hypotheses_summary.json',summary)
    with (OUT/'graphic_family_hypotheses.csv').open('w',encoding='utf-8',newline='') as f:
        fields=['family_hypothesis_id','seed_recovery_id','seed_graphic_key','seed_surface_forms','seed_de_rar_headwords','seed_occurrence_count','neighbor_count','neighbor_graphic_keys','human_reviewed'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for x in neighborhoods:w.writerow({'family_hypothesis_id':x['family_hypothesis_id'],'seed_recovery_id':x['seed_recovery_id'],'seed_graphic_key':x['seed_graphic_key'],'seed_surface_forms':' | '.join(x['seed_surface_forms']),'seed_de_rar_headwords':' | '.join(x['seed_de_rar_headwords']),'seed_occurrence_count':x['seed_occurrence_count'],'neighbor_count':x['neighbor_count'],'neighbor_graphic_keys':' | '.join(n['graphic_key'] for n in x['neighbors']),'human_reviewed':False})
    print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
