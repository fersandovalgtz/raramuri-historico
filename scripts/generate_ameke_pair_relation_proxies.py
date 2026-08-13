#!/usr/bin/env python3
"""Classify only the *German documentary relation* in exact X ~ X+ameke pairs.

The labels below describe the relation between Steffel's German gloss strings.
They are AI-assisted analytical proxies for later human review; they are not
Rarámuri semantic classes, morpheme functions, cognacy judgments, or historical
continuity claims.
"""
import json
from collections import Counter
from research_common import OUT,dump

# Explicit, reviewable coding of the ten exact pairs. Keeping this mapping
# literal makes every analytical decision inspectable and reproducible.
PROXIES={
 'baje':('event_process_to_person_participant_expression','person_participant','high','Rufen -> der Rufende'),
 'cotschime':('event_process_to_person_participant_expression','person_participant','high','Schlafen -> Ein Schlafender'),
 'cugui':('event_process_to_person_participant_expression','person_participant','high','Helfen -> Helfer'),
 'igue':('degree_property_to_person_property_expression','person_participant','medium','Sehr -> Ein Starker, der Kräfte hat'),
 'lessi':('event_change_state_to_state_property_expression','state_property','high','Ermatten, müde werden -> Müde, matt'),
 'mukiiati':('property_to_property_expression','state_property','high','Sterblich -> Sterblich'),
 'nesse':('event_process_to_person_participant_expression','person_participant','high','Bewahren/Hüten -> Hüter'),
 'saate':('entity_to_property_expression','state_property','high','Sand -> Sandig'),
 'seli':('event_authority_to_institutional_person_expression','person_participant','medium','Befehlen -> Dorfrichter'),
 'tschitschi':('event_process_to_person_participant_expression','person_participant','medium','Saugen -> Säugling'),
}

def main():
 src=json.loads((OUT/'ameke_exact_base_pair_contexts.json').read_text(encoding='utf-8'))['records']
 out=[]
 for r in src:
  key=r['mechanical_base_key']
  relation,target,confidence,rationale=PROXIES[key]
  out.append({
   'pair_id':r['pair_id'],'mechanical_base_key':key,'ameke_key':r['ameke_key'],
   'base_german_glosses':[x['german_gloss'] for x in r['base_attestations']],
   'ameke_german_glosses':[x['german_gloss'] for x in r['ameke_attestations']],
   'german_documentary_relation_proxy':relation,
   'ameke_target_expression_family':target,
   'ai_coding_confidence':confidence,
   'coding_rationale':rationale,
   'coding_status':'ai_documentary_proxy_for_human_review',
   'human_reviewed':False,
   'automatic_raramuri_semantic_classification':False,
   'automatic_morphological_analysis':False,
   'historical_continuity_judgment':'not_performed',
   'cognacy_judgment':'not_performed'
  })
 summary={
  'dataset':'raramuri-historico-steffel-1809',
  'layer':'ameke_exact_base_pair_german_relation_proxies_v1',
  'generated':'2026-08-13','pair_count':len(out),
  'relation_proxy_counts':dict(Counter(x['german_documentary_relation_proxy'] for x in out)),
  'target_expression_family_counts':dict(Counter(x['ameke_target_expression_family'] for x in out)),
  'confidence_counts':dict(Counter(x['ai_coding_confidence'] for x in out)),
  'human_reviewed':False,'automatic_raramuri_semantic_classification':False,
  'automatic_morphological_analysis':False,
  'interpretive_scope':'AI-assisted coding of relations between German gloss expressions in ten exact historical graphic pairs. It does not assign Rarámuri morphology or semantics and requires independent human review.'
 }
 dump(OUT/'ameke_exact_base_pair_relation_proxies.json',{'dataset':summary['dataset'],'count':len(out),'records':out,'human_reviewed':False})
 dump(OUT/'ameke_exact_base_pair_relation_proxies_summary.json',summary)
 print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
