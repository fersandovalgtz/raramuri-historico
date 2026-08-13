#!/usr/bin/env python3
from collections import defaultdict
from research_common import OUT,rows,active,norm,split_components,dump
import json

def main():
    rar=[r for r in rows() if active(r) and r.get('direction')=='RAR-DE']
    explicit=[]; bykey=defaultdict(list)
    for r in rar:
        form=(r.get('headword_diplomatic') or '').strip(); comps=split_components(form)
        for i,c in enumerate(comps,1):
            bykey[norm(c)].append({'record_id':r.get('record_id',''),'component_index':i,'form_diplomatic':c,'printed_page':int(r.get('printed_page') or 0)})
        if len(comps)>1:
            explicit.append({'group_id':'','record_id':r.get('record_id',''),'printed_page':int(r.get('printed_page') or 0),'headword_diplomatic':form,'components':[{'form':c,'graphic_key':norm(c)} for c in comps],'relation_type':'explicit_source_variant_group','human_reviewed':False})
    explicit.sort(key=lambda x:x['record_id'])
    for i,x in enumerate(explicit,1): x['group_id']=f'RHD-VAREXP-{i:05d}'
    collisions=[]
    for k,vals in bykey.items():
        surfaces=sorted({v['form_diplomatic'] for v in vals})
        if len(surfaces)<2: continue
        collisions.append({'group_id':'','graphic_key':k,'surface_forms':surfaces,'attestations':vals,'relation_type':'normalized_graphic_collision_group','interpretive_scope':'Shared conservative graphic key only; this does not prove linguistic variant status.','human_reviewed':False})
    collisions.sort(key=lambda x:x['graphic_key'])
    for i,x in enumerate(collisions,1): x['group_id']=f'RHD-VARCOL-{i:05d}'
    payload={'dataset':'raramuri-historico-steffel-1809','layer':'historical_documentary_variant_index','generated':'2026-08-13','human_reviewed':False,'explicit_source_variant_group_count':len(explicit),'normalized_graphic_collision_group_count':len(collisions),'explicit_source_variant_groups':explicit,'normalized_graphic_collision_groups':collisions}
    dump(OUT/'historical_variant_index.json',payload)
    summary={'explicit_source_variant_group_count':len(explicit),'normalized_graphic_collision_group_count':len(collisions),'human_reviewed':False}
    dump(OUT/'historical_variant_index_summary.json',summary); print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__': main()
