#!/usr/bin/env python3
"""Rank existing affricate candidates by documentary evidence, never semantics."""
from __future__ import annotations
from collections import Counter, defaultdict
from pathlib import Path
import csv, json, re, unicodedata

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'data/research'
SRC=D/'source_supported_affricate_candidates.json'
HOLD=D/'diachronic_graphemic_holdout_pairs.json'
OLD=D/'affricate_diachronic_overlap.json'
ICONC=D/'internal_concordance.json'
OUT=D/'affricate_candidate_evidence_ranking.json'
CSV=D/'affricate_candidate_evidence_ranking.csv'
SUM=D/'affricate_candidate_evidence_ranking_summary.json'
REPORT=D/'AFFRICATE_CANDIDATE_EVIDENCE_RANKING.md'
APOS=str.maketrans({'’':"'",'‘':"'",'ʼ':"'",'ʻ':"'",'`':"'",'´':"'"})

def norm(s:str)->str:
    s=(s or '').strip().translate(APOS).replace('ſ','s').replace('ß','ss')
    s=unicodedata.normalize('NFKD',s)
    s=''.join(c for c in s if unicodedata.category(c)!='Mn').casefold()
    s=re.sub(r"[^0-9a-z' -]+",' ',s)
    return re.sub(r'\s+',' ',s).strip(" .,:;!?()[]{}\"'-")

def load(p:Path)->dict:
    if not p.exists(): raise SystemExit(f'missing {p.relative_to(ROOT)}')
    return json.loads(p.read_text(encoding='utf-8'))

def main()->None:
    src,hold,old,iconc=map(load,[SRC,HOLD,OLD,ICONC])
    recs=src['records']
    if src.get('human_reviewed') is not False: raise SystemExit('source layer must remain non-adjudicative')

    positive=defaultdict(list); hold_all=defaultdict(list)
    for h in hold.get('records',[]):
        mids=[]
        if h.get('modern_record_id'): mids.append(h['modern_record_id'])
        mids.extend(h.get('modern_record_ids') or [])
        for mid in mids:
            k=(norm(h.get('historical_surface','')),mid); hold_all[k].append(h)
            if h.get('count_toward_positive') is True: positive[k].append(h.get('holdout_id',''))

    oldpairs=defaultdict(list)
    for x in old.get('records',[]):
        hid=(x.get('historical') or {}).get('record_id',''); mid=(x.get('modern') or {}).get('record_id','')
        if hid and mid: oldpairs[(hid,mid)].append(x.get('overlap_id',''))

    internal=defaultdict(lambda:{'attestation_count':0,'reciprocal_support_count':0,'ids':[],'reciprocal_ids':[]})
    for x in iconc.get('records',[]):
        rid=(x.get('rar_de') or {}).get('record_id','')
        if not rid: continue
        a=internal[rid]; a['attestation_count']+=1; cid=x.get('concordance_id','')
        if cid: a['ids'].append(cid)
        if (x.get('relation') or {}).get('reciprocal_german_support') is True:
            a['reciprocal_support_count']+=1
            if cid: a['reciprocal_ids'].append(cid)

    groups=defaultdict(set)
    for x in recs:
        h=x['historical']; groups[(h['record_id'],x['projected_comparison_key'],h.get('reading_layer','diplomatic'))].add(x['modern']['record_id'])

    ranked=[]
    for x in recs:
        h,m=x['historical'],x['modern']; hid,mid=h['record_id'],m['record_id']
        layer=h.get('reading_layer','diplomatic'); surface=h.get('comparison_surface') or h.get('form_diplomatic','')
        hp=sorted(set(positive.get((norm(surface),mid),[]))); op=sorted(set(oldpairs.get((hid,mid),[])))
        ins=internal[hid]
        ilevel=2 if ins['reciprocal_support_count'] else (1 if ins['attestation_count'] else 0)
        ilabel='reciprocal_documentary_support' if ilevel==2 else ('internal_form_attestation_only' if ilevel==1 else 'none')
        mids=sorted(groups[(hid,x['projected_comparison_key'],layer)]); unique=len(mids)==1
        signals=[]
        if hp: signals.append('prespecified_positive_holdout_pair')
        if op: signals.append('preexisting_diachronic_pair_corroboration')
        if ilevel: signals.append('steffel_internal_documentary_attestation')
        if unique: signals.append('unique_exact_projected_modern_record')
        nh=int(bool(op))+int(bool(ilevel))+int(unique)
        tier=1 if hp else (2 if nh>=2 else (3 if nh==1 else 4))
        reason='prespecified positive holdout pair' if tier==1 else ('at least two non-semantic signals' if tier==2 else ('one non-semantic signal' if tier==3 else 'projection only'))
        matched=[]
        for z in hold_all.get((norm(surface),mid),[]):
            matched.append({'holdout_id':z.get('holdout_id'),'evidence_class':z.get('evidence_class'),'count_toward_positive':z.get('count_toward_positive'),'negative_control':z.get('negative_control',False),'used_for_ranking':z.get('count_toward_positive') is True})
        ranked.append({
            'ranking_id':'','rank':0,'source_candidate_id':x['candidate_id'],'priority_tier':tier,'priority_tier_reason':reason,
            'documentary_signal_count':len(signals),'documentary_signal_classes':signals,
            'historical':{'record_id':hid,'printed_page':h.get('printed_page'),'form_diplomatic':h.get('form_diplomatic'),'comparison_surface':surface,'reading_layer':layer,'article_diplomatic':h.get('article_diplomatic','')},
            'modern':{'record_id':mid,'headword':m.get('headword',''),'component':m.get('component',''),'translation_raw':m.get('translation_raw',''),'classification':m.get('classification',''),'translation_or_classification_used_for_ranking':False},
            'projection':{'historical_comparison_key':x.get('historical_comparison_key'),'projected_comparison_key':x.get('projected_comparison_key'),'operations':x.get('projection_operations',[]),'modern_record_count_for_exact_projected_key':len(mids),'modern_record_ids_for_exact_projected_key':mids,'unique_exact_projected_modern_record':unique},
            'holdout_evidence':{'prespecified_positive_pair':bool(hp),'positive_holdout_ids':hp,'matched_holdout_records':matched},
            'preexisting_diachronic_evidence':{'exact_pair_corroborated':bool(op),'overlap_ids':op},
            'steffel_internal_evidence':{'support_level':ilevel,'support_label':ilabel,'attestation_count':ins['attestation_count'],'reciprocal_support_count':ins['reciprocal_support_count'],'concordance_ids':sorted(set(ins['ids'])),'reciprocal_concordance_ids':sorted(set(ins['reciprocal_ids']))},
            'facsimile_sensitivity':layer!='diplomatic','semantic_similarity_used_for_ranking':False,'automatic_semantic_judgment':False,'automatic_sound_correspondence_inference':False,'cognacy_judgment':'not_performed','historical_continuity_judgment':'not_performed','human_reviewed':False})

    ranked.sort(key=lambda x:(x['priority_tier'],x['facsimile_sensitivity'],-int(x['preexisting_diachronic_evidence']['exact_pair_corroborated']),-x['steffel_internal_evidence']['support_level'],-int(x['projection']['unique_exact_projected_modern_record']),-x['steffel_internal_evidence']['reciprocal_support_count'],x['historical']['record_id'],x['modern']['record_id']))
    for i,x in enumerate(ranked,1): x['rank']=i; x['ranking_id']=f'RHD-AFFRANK-{i:06d}'
    tiers=Counter(str(x['priority_tier']) for x in ranked); sigs=Counter(s for x in ranked for s in x['documentary_signal_classes'])
    summary={'dataset':src['dataset'],'layer':'affricate_candidate_documentary_evidence_ranking_v1','generated':'2026-08-13','candidate_count':len(ranked),'priority_tier_counts':dict(sorted(tiers.items())),'documentary_signal_counts':dict(sorted(sigs.items())),'positive_holdout_pair_count':sum(x['holdout_evidence']['prespecified_positive_pair'] for x in ranked),'preexisting_exact_pair_corroboration_count':sum(x['preexisting_diachronic_evidence']['exact_pair_corroborated'] for x in ranked),'internal_reciprocal_support_candidate_count':sum(x['steffel_internal_evidence']['reciprocal_support_count']>0 for x in ranked),'internal_form_attestation_candidate_count':sum(x['steffel_internal_evidence']['attestation_count']>0 for x in ranked),'unique_exact_projected_modern_record_count':sum(x['projection']['unique_exact_projected_modern_record'] for x in ranked),'ambiguous_exact_projected_modern_record_count':sum(not x['projection']['unique_exact_projected_modern_record'] for x in ranked),'diplomatic_candidate_count':sum(not x['facsimile_sensitivity'] for x in ranked),'facsimile_sensitivity_candidate_count':sum(x['facsimile_sensitivity'] for x in ranked),'top_ranked_candidate_ids':[x['source_candidate_id'] for x in ranked[:10]],'ranking_method':'deterministic_lexicographic_documentary_priority_v1','tier_policy':{'1':'prespecified positive holdout pair','2':'no positive holdout; at least two of exact prior pair corroboration, internal Steffel attestation, unique projected modern record','3':'no positive holdout; exactly one of those three signals','4':'projection only'},'translation_or_classification_used_for_ranking':False,'semantic_similarity_used_for_ranking':False,'automatic_semantic_judgment':False,'automatic_sound_correspondence_inference':False,'cognacy_judgment':'not_performed','historical_continuity_judgment':'not_performed','human_reviewed':False,'interpretive_scope':'Priority ordering by documentary provenance and ambiguity controls only; not a probability or linguistic score.'}
    OUT.write_text(json.dumps({'dataset':src['dataset'],'layer':summary['layer'],'generated':'2026-08-13','count':len(ranked),'records':ranked,'semantic_similarity_used_for_ranking':False,'automatic_semantic_judgment':False,'automatic_sound_correspondence_inference':False,'human_reviewed':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    SUM.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    fields=['rank','ranking_id','priority_tier','source_candidate_id','historical_record_id','historical_form','reading_layer','printed_page','modern_record_id','modern_headword','projected_key','positive_holdout_pair','prior_exact_pair_corroboration','internal_support_label','internal_attestation_count','internal_reciprocal_support_count','modern_record_count_for_exact_projected_key','unique_exact_projected_modern_record','facsimile_sensitivity','semantic_similarity_used_for_ranking','human_reviewed']
    with CSV.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for x in ranked:
            w.writerow({'rank':x['rank'],'ranking_id':x['ranking_id'],'priority_tier':x['priority_tier'],'source_candidate_id':x['source_candidate_id'],'historical_record_id':x['historical']['record_id'],'historical_form':x['historical']['comparison_surface'],'reading_layer':x['historical']['reading_layer'],'printed_page':x['historical']['printed_page'],'modern_record_id':x['modern']['record_id'],'modern_headword':x['modern']['headword'],'projected_key':x['projection']['projected_comparison_key'],'positive_holdout_pair':x['holdout_evidence']['prespecified_positive_pair'],'prior_exact_pair_corroboration':x['preexisting_diachronic_evidence']['exact_pair_corroborated'],'internal_support_label':x['steffel_internal_evidence']['support_label'],'internal_attestation_count':x['steffel_internal_evidence']['attestation_count'],'internal_reciprocal_support_count':x['steffel_internal_evidence']['reciprocal_support_count'],'modern_record_count_for_exact_projected_key':x['projection']['modern_record_count_for_exact_projected_key'],'unique_exact_projected_modern_record':x['projection']['unique_exact_projected_modern_record'],'facsimile_sensitivity':x['facsimile_sensitivity'],'semantic_similarity_used_for_ranking':False,'human_reviewed':False})

    lines=['# Priorización documental de candidatos de africadas','', '**Corte:** 2026-08-13. **Estatus:** priorización de revisión; no adjudica cognación, significado ni cambio fonológico.','',f"Se ordenan **{len(ranked)} candidatos** sin comparar la glosa alemana histórica con la traducción española moderna ni utilizar la clase gramatical moderna.",'',f"Tier 1 = **{tiers.get('1',0)}**; Tier 2 = **{tiers.get('2',0)}**; Tier 3 = **{tiers.get('3',0)}**; Tier 4 = **{tiers.get('4',0)}**.",'','| Rango | Tier | Histórico | Moderno | Holdout | Cola previa | Apoyo interno | Único | Lectura |','|---:|---:|---|---|---|---|---|---|---|']
    for x in ranked[:15]: lines.append(f"| {x['rank']} | {x['priority_tier']} | `{x['historical']['comparison_surface']}` | `{x['modern']['headword']}` | {'sí' if x['holdout_evidence']['prespecified_positive_pair'] else 'no'} | {'sí' if x['preexisting_diachronic_evidence']['exact_pair_corroborated'] else 'no'} | {x['steffel_internal_evidence']['support_label']} | {'sí' if x['projection']['unique_exact_projected_modern_record'] else 'no'} | {x['historical']['reading_layer']} |")
    lines += ['','El apoyo interno sólo describe la evidencia bidireccional dentro de Steffel; no valida la relación con el registro moderno.','', '`semantic_similarity_used_for_ranking=false`; `translation_or_classification_used_for_ranking=false`; `automatic_semantic_judgment=false`; `automatic_sound_correspondence_inference=false`; `cognacy_judgment=not_performed`; `historical_continuity_judgment=not_performed`; `human_reviewed=false`.']
    REPORT.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__': main()
