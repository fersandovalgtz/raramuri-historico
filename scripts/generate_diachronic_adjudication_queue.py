#!/usr/bin/env python3
"""Prioritize diachronic machine candidates for independent human adjudication.

Priority is a review-order heuristic only. No semantic, etymological or historical
continuity judgment is automated, and all human-review fields remain false/blank.
"""
from pathlib import Path
from collections import Counter
import csv, json

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'data/diachronic'
EXACT=D/'exact_graphic_candidates.json'
PROB=D/'probable_graphic_candidates.json'
OUT=D/'adjudication_queue.json'
CSV=D/'adjudication_queue.csv'
SUMMARY=D/'adjudication_queue_summary.json'
INDEX=D/'ADJUDICATION_REVIEW_INDEX.md'


def load(path, cohort):
    p=json.loads(path.read_text(encoding='utf-8'))
    assert p['human_reviewed'] is False
    return [(cohort,x) for x in p['records']]


def comp_key(x):
    h=x['historical']
    return h['record_id'], int(h.get('matched_component_index') or 1)


def rank_candidate(cohort,x,multiplicity):
    h=x['historical']; m=x['modern']; r=x['candidate_relation']
    semantic_ready=bool((h.get('article_diplomatic') or '').strip()) and bool((m.get('translation_raw') or '').strip())
    reasons=[]; score=0
    if cohort=='exact':
        score+=45; reasons.append('exact_normalized_graphic_match')
        if r.get('short_form_warning',False):
            score-=8; reasons.append('short_form_warning')
        else:
            score+=8; reasons.append('not_short_form')
        if int(r.get('modern_candidates_for_key') or 1)==1:
            score+=5; reasons.append('unique_modern_key_match')
        else:
            reasons.append('ambiguous_modern_key_match')
    else:
        dist=int(r.get('edit_distance') or 99); sim=float(r.get('similarity') or 0)
        score+=28 if dist==1 else 16
        reasons.append(f'edit_distance_{dist}')
        score+=max(0,int(round((sim-.75)*40)))
        reasons.append(f'graphic_similarity_{sim:.2f}')
    if multiplicity==1:
        score+=10; reasons.append('single_candidate_for_historical_component')
    elif multiplicity==2:
        score+=4; reasons.append('two_candidates_for_historical_component')
    else:
        reasons.append(f'{multiplicity}_candidates_for_historical_component')
    if semantic_ready:
        score+=5; reasons.append('semantic_context_available_for_human_review')
    else:
        reasons.append('semantic_context_incomplete')
    if (m.get('status') or '').strip().lower()=='transcrito':
        score+=1; reasons.append('modern_record_transcribed')
    # Tier 1 is reserved for the strongest documentary exact matches: not short
    # and unique at the exact-key level. Nearby probable alternatives are still
    # retained and lower the score through multiplicity, but do not erase the
    # stronger evidentiary status of an exact normalized match.
    if cohort=='exact' and not r.get('short_form_warning',False) and int(r.get('modern_candidates_for_key') or 1)==1 and score>=55:
        tier=1
    elif cohort=='exact':
        tier=2
    elif int(r.get('edit_distance') or 99)==1 and multiplicity==1 and float(r.get('similarity') or 0)>=.85 and score>=43:
        tier=2
    elif int(r.get('edit_distance') or 99)==1:
        tier=3
    else:
        tier=4
    return tier,score,reasons,semantic_ready


def main():
    items=load(EXACT,'exact')+load(PROB,'probable')
    multiplicity=Counter(comp_key(x) for _,x in items)
    queue=[]
    for cohort,x in items:
        h=x['historical']; m=x['modern']; r=x['candidate_relation']
        mult=multiplicity[comp_key(x)]
        tier,score,reasons,semantic_ready=rank_candidate(cohort,x,mult)
        queue.append({
            'adjudication_id':'',
            'source_candidate_id':x['correspondence_id'],
            'source_cohort':cohort,
            'priority_tier':tier,
            'priority_score':score,
            'priority_reasons':reasons,
            'historical':{
                'record_id':h['record_id'],'form_diplomatic':h.get('form_diplomatic',''),
                'matched_component':h.get('matched_component',''),'matched_component_index':h.get('matched_component_index',1),
                'article_diplomatic':h.get('article_diplomatic',''),'printed_page':h.get('printed_page',0)
            },
            'modern':{
                'record_id':m['record_id'],'headword':m.get('headword',''),'matched_component':m.get('matched_component',''),
                'translation_raw':m.get('translation_raw',''),'classification':m.get('classification',''),
                'source_code':m.get('source_code',''),'status':m.get('status','')
            },
            'candidate_relation':r,
            'review_evidence':{
                'historical_component_candidate_count':mult,
                'semantic_evidence_available':semantic_ready,
                'automatic_semantic_judgment':'not_performed',
                'automatic_etymological_judgment':'not_performed',
                'automatic_historical_continuity_judgment':'not_performed'
            },
            'independent_adjudication':{
                'human_reviewed':False,'reviewer':'','affiliation':'','orcid':'','review_date':'',
                'decision':'not_assessed','adopted_relation_type':'not_assessed',
                'semantic_relation':'not_assessed','historical_continuity':'not_assessed',
                'confidence':'not_assessed','evidence':'','note':''
            }
        })
    queue.sort(key=lambda q:(q['priority_tier'],-q['priority_score'],q['historical']['record_id'],q['modern']['record_id'],q['source_candidate_id']))
    for i,q in enumerate(queue,1): q['adjudication_id']=f'RHD-ADJ-{i:06d}'
    tiers=Counter(str(q['priority_tier']) for q in queue)
    cohorts=Counter(q['source_cohort'] for q in queue)
    sem=sum(q['review_evidence']['semantic_evidence_available'] for q in queue)
    payload={
        'dataset':'raramuri-historico-steffel-1809','layer':'diachronic_independent_adjudication_queue',
        'generated':'2026-08-13','count':len(queue),'human_reviewed':False,
        'automatic_semantic_judgment':False,'automatic_etymological_judgment':False,
        'automatic_historical_continuity_judgment':False,'records':queue
    }
    summary={
        'dataset':payload['dataset'],'layer':payload['layer'],'generated':payload['generated'],
        'candidate_count':len(queue),'cohort_counts':dict(sorted(cohorts.items())),
        'priority_tier_counts':dict(sorted(tiers.items())),
        'historical_records_represented':len({q['historical']['record_id'] for q in queue}),
        'modern_records_represented':len({q['modern']['record_id'] for q in queue}),
        'semantic_evidence_available_count':sem,'human_reviewed_count':0,
        'method':'deterministic_review_priority_v1',
        'scope_note':'Priority orders independent review only; it does not validate semantic identity, cognacy, historical continuity, dialect identity or normative equivalence.'
    }
    OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    SUMMARY.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    fields=['adjudication_id','priority_tier','priority_score','source_candidate_id','source_cohort','historical_record_id','historical_form','historical_component','historical_page','modern_record_id','modern_headword','modern_translation','relation_type','component_candidate_count','semantic_evidence_available','human_reviewed','decision']
    with CSV.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for q in queue:
            w.writerow({
                'adjudication_id':q['adjudication_id'],'priority_tier':q['priority_tier'],'priority_score':q['priority_score'],
                'source_candidate_id':q['source_candidate_id'],'source_cohort':q['source_cohort'],
                'historical_record_id':q['historical']['record_id'],'historical_form':q['historical']['form_diplomatic'],
                'historical_component':q['historical']['matched_component'],'historical_page':q['historical']['printed_page'],
                'modern_record_id':q['modern']['record_id'],'modern_headword':q['modern']['headword'],
                'modern_translation':q['modern']['translation_raw'],'relation_type':q['candidate_relation']['type'],
                'component_candidate_count':q['review_evidence']['historical_component_candidate_count'],
                'semantic_evidence_available':str(q['review_evidence']['semantic_evidence_available']).lower(),
                'human_reviewed':'false','decision':'not_assessed'
            })
    lines=['# Índice de adjudicación diacrónica independiente','',f'Total: **{len(queue)}** candidatos. Revisión humana completada: **0**.','',
           'La prioridad ordena revisión; no constituye una conclusión lingüística. La evidencia semántica sólo se presenta para evaluación humana.','',
           '| P | ID | Fuente | Histórico | Forma histórica | Moderno | Forma moderna | Tipo | Semántica disponible |',
           '|---:|---|---|---|---|---|---|---|---|']
    for q in queue:
        semtxt='sí' if q['review_evidence']['semantic_evidence_available'] else 'no'
        hf=str(q['historical']['matched_component']).replace('|','/'); mf=str(q['modern']['matched_component']).replace('|','/')
        lines.append(f"| {q['priority_tier']} | {q['adjudication_id']} | {q['source_candidate_id']} | {q['historical']['record_id']} | {hf} | {q['modern']['record_id']} | {mf} | {q['candidate_relation']['type']} | {semtxt} |")
    INDEX.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(f"Generated diachronic adjudication queue: {len(queue)}; tiers={dict(sorted(tiers.items()))}; semantic-ready={sem}; human reviewed=0")

if __name__=='__main__': main()
