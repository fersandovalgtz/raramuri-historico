#!/usr/bin/env python3
"""Build a component-aware/token-aware view of the historical -ameke constellation.

The original constellation intentionally treated each recovered graphic string as
one documentary member. This derivative layer keeps those expressions intact but
adds a final-token analysis unit so multiword expressions or a verified machine
concatenation do not masquerade as independent suffix-bearing types.

No source text is overwritten. No morpheme, grammatical category, semantic
function or human validation is asserted.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import csv,json,re
from research_common import OUT,dump,norm

AUDIT_TOKEN_OVERRIDES={
    'RHD-AMEKE-00023':'bassirugameke'
}

def final_token(key:str)->str:
    parts=[x for x in re.split(r'\s+',norm(key).strip()) if x]
    return parts[-1] if parts else norm(key)

def main():
    members=json.loads((OUT/'ameke_constellation_members.json').read_text(encoding='utf-8'))['records']
    audit=json.loads((OUT/'ugameke_facsimile_ai_audit.json').read_text(encoding='utf-8'))
    audit_by={x['member_id']:x for x in audit['records']}
    direct_tokens=set()
    for m in members:
        if 'RAR-DE' in set(m.get('source_layers') or []):
            k=AUDIT_TOKEN_OVERRIDES.get(m['member_id'],final_token(m['graphic_key']))
            direct_tokens.add(k)
    rows=[]
    for m in members:
        source_layers=sorted(set(m.get('source_layers') or []))
        member_key=norm(m['graphic_key'])
        token=AUDIT_TOKEN_OVERRIDES.get(m['member_id'],final_token(member_key))
        a=audit_by.get(m['member_id'])
        audited_unit_decision=a.get('source_unit_decision') if a else 'not_in_ugameke_facsimile_audit'
        member_is_multiword=' ' in member_key
        token_differs=(token!=member_key)
        direct_overlap=(token in direct_tokens and 'RAR-DE' not in source_layers)
        token_provenance='RAR-DE_supported' if token in direct_tokens else 'recovery_only_or_other_machine_layer'
        rows.append({
            'member_id':m['member_id'],
            'graphic_key':m['graphic_key'],
            'exclusive_suffix_class':m['exclusive_suffix_class'],
            'source_layers':source_layers,
            'member_level_provenance':'RAR-DE' if 'RAR-DE' in source_layers else 'DE-RAR-recovery',
            'analysis_token_key':token,
            'analysis_token_differs_from_member_key':token_differs,
            'member_is_multiword_expression':member_is_multiword,
            'direct_rar_de_support_for_analysis_token':token in direct_tokens,
            'recovered_member_overlaps_direct_rar_de_token':direct_overlap,
            'facsimile_unit_decision':audited_unit_decision,
            'printed_pages':m.get('printed_pages',[]),
            'german_contexts':m.get('german_contexts',[]),
            'target_infinitive_shape_proxy_count':int((m.get('german_context_shape_proxy_counts') or {}).get('infinitive_ending_proxy',0)),
            'human_reviewed':False,
            'automatic_morphological_analysis':False,
            'interpretive_scope':'Token-aware documentary analysis unit only. Multiword expressions remain preserved as expressions; the final-token key is used only to avoid double-counting suffix-bearing strings across provenance.'
        })
    groups=defaultdict(list)
    for r in rows:groups[(r['exclusive_suffix_class'],r['analysis_token_key'])].append(r)
    units=[]
    for (cls,key),items in groups.items():
        units.append({
            'exclusive_suffix_class':cls,'analysis_token_key':key,
            'member_ids':sorted(x['member_id'] for x in items),
            'member_count':len(items),
            'has_rar_de_member':any(x['member_level_provenance']=='RAR-DE' for x in items),
            'has_de_rar_recovery_member':any(x['member_level_provenance']=='DE-RAR-recovery' for x in items),
            'recovered_member_overlap_count':sum(x['recovered_member_overlaps_direct_rar_de_token'] for x in items),
            'target_infinitive_shape_proxy_context_count':sum(x['target_infinitive_shape_proxy_count'] for x in items),
            'human_reviewed':False
        })
    units.sort(key=lambda x:(x['exclusive_suffix_class'],x['analysis_token_key']))
    ug_members=[r for r in rows if r['exclusive_suffix_class']=='ugameke']
    ug_units=[u for u in units if u['exclusive_suffix_class']=='ugameke']
    recovered=[r for r in ug_members if r['member_level_provenance']=='DE-RAR-recovery']
    signal=[r for r in recovered if r['target_infinitive_shape_proxy_count']>0]
    summary={
        'dataset':'raramuri-historico-steffel-1809','layer':'ameke_token_aware_analysis_v1','generated':'2026-08-13',
        'member_count':len(rows),'unique_token_unit_count':len(units),
        'member_counts_by_exclusive_suffix_class':dict(sorted(Counter(r['exclusive_suffix_class'] for r in rows).items())),
        'token_unit_counts_by_exclusive_suffix_class':dict(sorted(Counter(u['exclusive_suffix_class'] for u in units).items())),
        'multiword_member_count':sum(r['member_is_multiword_expression'] for r in rows),
        'token_differs_from_member_key_count':sum(r['analysis_token_differs_from_member_key'] for r in rows),
        'recovered_members_overlapping_direct_rar_de_token_count':sum(r['recovered_member_overlaps_direct_rar_de_token'] for r in rows),
        'ugameke_member_count':len(ug_members),'ugameke_unique_token_unit_count':len(ug_units),
        'ugameke_recovered_only_member_count':len(recovered),
        'ugameke_recovered_members_overlapping_direct_rar_de_token_count':sum(r['recovered_member_overlaps_direct_rar_de_token'] for r in recovered),
        'ugameke_recovered_independent_token_member_count':sum(not r['recovered_member_overlaps_direct_rar_de_token'] for r in recovered),
        'ugameke_signal_bearing_recovered_member_count':len(signal),
        'ugameke_signal_bearing_independent_token_member_count':sum(not r['recovered_member_overlaps_direct_rar_de_token'] for r in signal),
        'human_reviewed':False,'automatic_morphological_analysis':False,'automatic_morpheme_assignment':False,
        'interpretive_scope':'Component-aware counting correction for documentary units only; not a linguistic segmentation or morphological analysis.'
    }
    dump(OUT/'ameke_token_aware_members.json',{'dataset':summary['dataset'],'layer':summary['layer'],'generated':summary['generated'],'count':len(rows),'human_reviewed':False,'records':rows})
    dump(OUT/'ameke_token_aware_units.json',{'dataset':summary['dataset'],'layer':'ameke_token_aware_units_v1','generated':summary['generated'],'count':len(units),'human_reviewed':False,'records':units})
    dump(OUT/'ameke_token_aware_summary.json',summary)
    with (OUT/'ameke_token_aware_members.csv').open('w',encoding='utf-8',newline='') as f:
        fields=['member_id','graphic_key','exclusive_suffix_class','member_level_provenance','analysis_token_key','analysis_token_differs_from_member_key','member_is_multiword_expression','direct_rar_de_support_for_analysis_token','recovered_member_overlaps_direct_rar_de_token','facsimile_unit_decision','target_infinitive_shape_proxy_count','human_reviewed'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for x in rows:w.writerow({k:x.get(k,'') for k in fields})
    print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
