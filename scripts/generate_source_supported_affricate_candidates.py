#!/usr/bin/env python3
"""Generate source-supported historical-affricate → modern graphic candidates.

Unlike the generic probable matcher, this layer may project historical <tsch>
and <ts> to a modern comparison string <ch> because Merrill et al. 2020 gives
an explicit historical phonetic analysis of both spellings as allophones of
/č/, while modern Choguita independently has /tʃ/. The projection is used only
for candidate retrieval. It is NOT an automatic sound law, cognacy decision,
or dialect-normalization rule.

The layer also tests the already independently supported terminal documentary
projection -ameke → -ami, but stores that operation separately in the evidence.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import csv, json, re, subprocess, unicodedata

ROOT=Path(__file__).resolve().parents[1]
HIST=ROOT/'data/research/historical_affricate_graphemic_inventory.json'
MODERN_ROOT=ROOT/'.tmp-raramuri-digital'
MODERN=MODERN_ROOT/'data/lexicon-master.csv'
REGISTRY=ROOT/'data/diachronic/source_registry.json'
OUT=ROOT/'data/research/source_supported_affricate_candidates.json'
CSV_OUT=ROOT/'data/research/source_supported_affricate_candidates.csv'
SUMMARY=ROOT/'data/research/source_supported_affricate_candidates_summary.json'
REPORT=ROOT/'data/research/SOURCE_SUPPORTED_AFFRICATE_CANDIDATES.md'
HOLDOUT=ROOT/'data/research/diachronic_graphemic_holdout_pairs.json'

APOS=str.maketrans({'’':"'",'‘':"'",'ʼ':"'",'ʻ':"'",'`':"'",'´':"'"})

def norm(s:str)->str:
    s=(s or '').strip().translate(APOS).replace('ſ','s').replace('ß','ss')
    s=unicodedata.normalize('NFKD',s)
    s=''.join(c for c in s if unicodedata.category(c)!='Mn').casefold()
    s=re.sub(r"[^0-9a-z' -]+",' ',s)
    return re.sub(r'\s+',' ',s).strip(" .,:;!?()[]{}\"'-")

def split_modern(s:str)->list[str]:
    out=[]
    for p in re.split(r'[,;/]',s or ''):
        p=re.sub(r'\s+',' ',p).strip().strip(' .,:;!?()[]{}')
        if p and norm(p): out.append(p)
    return out

def modern_commit()->str:
    reg=json.loads(REGISTRY.read_text(encoding='utf-8'))
    for x in reg.get('sources',[]):
        if x.get('role')=='contemporary': return x.get('commit','')
    raise SystemExit('missing contemporary source')

def verify_pin(expected:str)->None:
    actual=subprocess.check_output(['git','-C',str(MODERN_ROOT),'rev-parse','HEAD'],text=True).strip()
    if actual!=expected: raise SystemExit(f'comparison source pin mismatch: {actual} != {expected}')

def projections(key:str)->list[dict]:
    """Return explicit documentary comparison projections, de-duplicated."""
    items=[]
    # One operation name covers both historical spellings because the historical
    # source analysis treats them as allophonic spellings of /č/.
    aff=re.sub(r'tsch|ts','ch',key)
    if aff!=key:
        items.append({'projected_key':aff,'operations':['historical_affricate_spelling_to_modern_ch_candidate_key']})
        if aff.endswith('ameke'):
            items.append({'projected_key':aff[:-5]+'ami','operations':['historical_affricate_spelling_to_modern_ch_candidate_key','terminal_ameke_to_ami_candidate_key']})
        if aff.endswith('ame'):
            items.append({'projected_key':aff[:-3]+'ami','operations':['historical_affricate_spelling_to_modern_ch_candidate_key','terminal_ame_to_ami_candidate_key']})
    seen=set(); out=[]
    for x in items:
        marker=(x['projected_key'],tuple(x['operations']))
        if marker not in seen:
            seen.add(marker); out.append(x)
    return out

def main()->None:
    if not HIST.exists() or not MODERN.exists(): raise SystemExit('required historical inventory or modern checkout missing')
    pin=modern_commit(); verify_pin(pin)
    hist=json.loads(HIST.read_text(encoding='utf-8'))
    modern_rows=list(csv.DictReader(MODERN.open(encoding='utf-8-sig')))
    modern_index=defaultdict(list)
    for r in modern_rows:
        rid=(r.get('record_id') or '').strip(); hw=(r.get('headword') or '').strip()
        if not re.fullmatch(r'RD-[0-9]{6}',rid) or not hw: continue
        for i,c in enumerate(split_modern(hw),1):
            k=norm(c)
            modern_index[k].append({'record_id':rid,'headword':hw,'component':c,'component_index':i,
                'translation_raw':r.get('translation_raw',''),'classification':r.get('classification',''),
                'classification_family':r.get('classification_family',''),'source_code':r.get('source_code','')})

    # Collapse inventory occurrences to unique historical components, preserving
    # all affricate environments associated with the component.
    components={}
    for o in hist['records']:
        marker=(o['record_id'],o['headword_component_diplomatic'])
        x=components.setdefault(marker,{'record_id':o['record_id'],'printed_page':o['printed_page'],
            'form_diplomatic':o['headword_component_diplomatic'],'graphic_key':o['graphic_key'],
            'affricate_occurrences':[]})
        x['affricate_occurrences'].append({'occurrence_id':o['occurrence_id'],'grapheme':o['grapheme'],
            'position':o['position'],'following_character':o['following_character'],
            'merrill_distribution_check':o['merrill_distribution_check']})

    candidates=[]; projected_components=0
    for h in components.values():
        key=norm(h['graphic_key']).replace(' ','')
        ps=projections(key)
        if ps: projected_components+=1
        for p in ps:
            for m in modern_index.get(p['projected_key'],[]):
                candidates.append({
                    'candidate_id':f"RHD-AFFSRC-{len(candidates)+1:06d}",
                    'historical':h,
                    'modern':m,
                    'historical_comparison_key':key,
                    'projected_comparison_key':p['projected_key'],
                    'projection_operations':p['operations'],
                    'match_type':'exact_match_after_source_supported_candidate_projection',
                    'semantic_equivalence_judgment':'not_performed',
                    'cognacy_judgment':'not_performed','historical_continuity_judgment':'not_performed',
                    'automatic_sound_correspondence_inference':False,'automatic_morpheme_assignment':False,
                    'human_reviewed':False})

    hist_records={x['historical']['record_id'] for x in candidates}; modern_records={x['modern']['record_id'] for x in candidates}
    op_counts=Counter('|'.join(x['projection_operations']) for x in candidates)
    holdout_recovery=[]
    if HOLDOUT.exists():
        h=json.loads(HOLDOUT.read_text(encoding='utf-8'))
        by_pair={(x['historical']['record_id'],x['modern']['record_id']):x for x in candidates}
        # Holdout lacks historical RHD IDs, so validation is based only on the
        # explicitly named surface + modern record pair and is reported separately.
        by_surface={(norm(x['historical']['form_diplomatic']),x['modern']['record_id']):x for x in candidates}
        for r in h.get('records',[]):
            if not r.get('count_toward_positive') or not r.get('modern_record_id'): continue
            hit=by_surface.get((norm(r['historical_surface']),r['modern_record_id']))
            holdout_recovery.append({'holdout_id':r['holdout_id'],'historical_surface':r['historical_surface'],
                'modern_record_id':r['modern_record_id'],'recovered_by_exact_projection':bool(hit),
                'candidate_id':hit['candidate_id'] if hit else None})

    summary={
        'dataset':hist['dataset'],'layer':'source_supported_affricate_candidate_retrieval_v1','generated':'2026-08-13',
        'modern_repository':'fersandovalgtz/raramuri-digital','modern_commit':pin,
        'historical_affricate_component_count':hist['component_count'],'historical_components_with_projection':projected_components,
        'candidate_count':len(candidates),'historical_record_count':len(hist_records),'modern_record_count':len(modern_records),
        'projection_operation_counts':dict(sorted(op_counts.items())),
        'positive_holdout_projection_recovery':holdout_recovery,
        'positive_holdout_exact_projection_recovered_count':sum(x['recovered_by_exact_projection'] for x in holdout_recovery),
        'positive_holdout_tested_count':len(holdout_recovery),
        'semantic_equivalence_judgment':'not_performed','cognacy_judgment':'not_performed','historical_continuity_judgment':'not_performed',
        'automatic_sound_correspondence_inference':False,'automatic_morpheme_assignment':False,'human_reviewed':False,
        'interpretive_scope':'Exact modern-key retrieval after source-supported documentary comparison projections. Projection is a search operation only, not a sound law, phonological normalization, or cognacy claim.'}
    payload={'dataset':hist['dataset'],'layer':summary['layer'],'generated':'2026-08-13','count':len(candidates),'records':candidates,
        'human_reviewed':False,'automatic_sound_correspondence_inference':False,'cognacy_judgment':'not_performed','historical_continuity_judgment':'not_performed'}
    OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    SUMMARY.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    fields=['candidate_id','historical_record_id','historical_form','printed_page','historical_key','projected_key','projection_operations',
        'modern_record_id','modern_headword','modern_translation','modern_classification','human_reviewed']
    with CSV_OUT.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for x in candidates:
            w.writerow({'candidate_id':x['candidate_id'],'historical_record_id':x['historical']['record_id'],
                'historical_form':x['historical']['form_diplomatic'],'printed_page':x['historical']['printed_page'],
                'historical_key':x['historical_comparison_key'],'projected_key':x['projected_comparison_key'],
                'projection_operations':'|'.join(x['projection_operations']),'modern_record_id':x['modern']['record_id'],
                'modern_headword':x['modern']['headword'],'modern_translation':x['modern']['translation_raw'],
                'modern_classification':x['modern']['classification'],'human_reviewed':False})
    md=['# Candidatos modernos recuperados mediante proyección grafemática respaldada por fuentes','',
        '**Corte:** 2026-08-13. **Estatus:** recuperación de candidatos; no adjudica cognación ni cambio fonológico.','',
        f"Se proyectaron **{projected_components} componentes históricos** con `<tsch>/<ts>` hacia una clave moderna candidata `ch`. Los empates exactos contra el lexicón moderno fijado producen **{len(candidates)} candidatos**, correspondientes a **{len(hist_records)} registros históricos** y **{len(modern_records)} registros modernos**.",'',
        'La transformación es deliberadamente distinta de una normalización lingüística: sólo habilita búsqueda a partir del análisis publicado de Merrill y mantiene visibles tanto la forma diplomática como cada operación aplicada.','',
        f"En el pequeño holdout semántico previamente construido se recuperan por coincidencia exacta proyectada **{summary['positive_holdout_exact_projection_recovered_count']}/{summary['positive_holdout_tested_count']}** positivos; los restantes requieren otras diferencias gráficas y no se fuerzan.",'',
        '`semantic_equivalence_judgment=not_performed`; `automatic_sound_correspondence_inference=false`; `cognacy_judgment=not_performed`; `historical_continuity_judgment=not_performed`; `human_reviewed=false`.']
    REPORT.write_text('\n'.join(md)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__': main()
