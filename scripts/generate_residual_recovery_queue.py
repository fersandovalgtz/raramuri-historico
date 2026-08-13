#!/usr/bin/env python3
"""Cluster residual profile signals into a documentary recovery queue.

The queue deduplicates machine signals and ranks cross-entry recurrence. It does
not identify language, accept lexemes, normalize the diplomatic text, or mark
human review.
"""
from collections import defaultdict,Counter
import csv,json
from research_common import OUT,dump

RANK={'strong_raramuri_profile_signal':2,'possible_raramuri_profile_signal':1}

def grade(best_class,occurrences,similarity):
    if best_class=='strong_raramuri_profile_signal' and occurrences>=2 and similarity>=.70:return 'A_machine_documentary_signal'
    if best_class=='strong_raramuri_profile_signal' and (occurrences>=2 or similarity>=.70):return 'B_machine_documentary_signal'
    if best_class=='strong_raramuri_profile_signal':return 'C_machine_profile_signal'
    return 'D_machine_possible_profile_signal'

def main():
    tri=json.loads((OUT/'de_rar_residual_span_triage.json').read_text(encoding='utf-8'))['records']
    selected=[x for x in tri if x['profile_class'] in RANK]
    groups=defaultdict(list)
    for x in selected:groups[x['graphic_key']].append(x)
    out=[]
    for key,items in groups.items():
        items=sorted(items,key=lambda x:(-RANK[x['profile_class']],-x['profile_log_likelihood_ratio'],-x['nearest_rar_de_similarity'],x['triage_id']))
        best=items[0]; records=sorted({x['de_rar_record_id'] for x in items}); pages=sorted({x['printed_page'] for x in items}); heads=sorted({x['de_rar_headword_diplomatic'] for x in items}); surfaces=sorted({x['candidate_span_diplomatic'] for x in items})
        maxsim=max(x['nearest_rar_de_similarity'] for x in items); nearest=next((x['nearest_rar_de_graphic_key'] for x in items if x['nearest_rar_de_similarity']==maxsim),'')
        g=grade(best['profile_class'],len(records),maxsim)
        out.append({'recovery_id':'','graphic_key':key,'surface_forms':surfaces,'occurrence_count':len(items),'distinct_de_rar_record_count':len(records),'de_rar_record_ids':records,'de_rar_headwords':heads,'printed_pages':pages,'best_profile_class':best['profile_class'],'best_profile_log_likelihood_ratio':best['profile_log_likelihood_ratio'],'nearest_rar_de_graphic_key':nearest,'nearest_rar_de_similarity':maxsim,'evidence_grade':g,'status':'machine_recovery_candidate','human_reviewed':False,'decision':'not_assessed','interpretive_scope':'Deduplicated documentary recovery candidate only; not a confirmed Rarámuri form, lexeme, semantic unit, cognate or validated historical relation.'})
    order={'A_machine_documentary_signal':1,'B_machine_documentary_signal':2,'C_machine_profile_signal':3,'D_machine_possible_profile_signal':4}
    out.sort(key=lambda x:(order[x['evidence_grade']],-x['distinct_de_rar_record_count'],-x['best_profile_log_likelihood_ratio'],x['graphic_key']))
    for i,x in enumerate(out,1):x['recovery_id']=f'RHD-RREC-{i:06d}'
    grades=Counter(x['evidence_grade'] for x in out); recurrent=sum(x['distinct_de_rar_record_count']>=2 for x in out)
    summary={'dataset':'raramuri-historico-steffel-1809','generated':'2026-08-13','unique_recovery_candidate_groups':len(out),'source_profile_signal_spans':len(selected),'evidence_grade_counts':dict(sorted(grades.items())),'cross_entry_recurrent_groups':recurrent,'human_reviewed':False,'automatic_language_identification':False,'automatic_lexeme_creation':False,'method':'deduplicated_residual_profile_recovery_queue_v1'}
    dump(OUT/'de_rar_residual_recovery_queue.json',{'dataset':summary['dataset'],'layer':'de_rar_residual_recovery_candidates','generated':summary['generated'],'count':len(out),'human_reviewed':False,'automatic_language_identification':False,'automatic_lexeme_creation':False,'records':out});dump(OUT/'de_rar_residual_recovery_queue_summary.json',summary)
    with (OUT/'de_rar_residual_recovery_queue.csv').open('w',encoding='utf-8',newline='') as f:
        fields=['recovery_id','graphic_key','surface_forms','occurrence_count','distinct_de_rar_record_count','de_rar_headwords','printed_pages','best_profile_class','best_profile_log_likelihood_ratio','nearest_rar_de_graphic_key','nearest_rar_de_similarity','evidence_grade','human_reviewed','decision'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader();
        for x in out:
            row={k:x.get(k,'') for k in fields}
            for k in ('surface_forms','de_rar_headwords','printed_pages'):row[k]=' | '.join(map(str,row[k]))
            w.writerow(row)
    print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
