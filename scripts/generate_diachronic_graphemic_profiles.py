#!/usr/bin/env python3
"""Generate conservative diachronic graphemic profiles.

Seed evidence and out-of-seed semantic holdouts are kept separate. Positive,
negative, and unresolved holdout cases are counted separately. No cognacy,
sound change, phoneme identity, or historical continuity is adjudicated.
"""
import json, unicodedata
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SEED=ROOT/'data/research/diachronic_graphemic_seed_pairs.json'
HOLD=ROOT/'data/research/diachronic_graphemic_holdout_pairs.json'
OUT=ROOT/'data/research/diachronic_graphemic_pattern_summary.json'
REPORT=ROOT/'data/research/DIACHRONIC_GRAPHEMIC_PATTERN_REPORT.md'

MOTIFS=[
 ('ameke_to_ami','derivational','ameke','ami','suffix',['participial_surface'],3),
 ('ame_to_ami','derivational','ame','ami','suffix',['historical_short_surface_to_modern'],2),
 ('tsch_to_ch','lexical','tsch','ch','any',['base','participial_surface'],2),
 ('ss_to_s','lexical','ss','s','any',['base','participial_surface'],2),
 ('aa_to_a','lexical','aa','a','any',['base','participial_surface'],2),
 ('final_e_to_i','lexical','e','i','suffix',['base'],2),
]

def norm(s):
 s=s.replace('ſ','s').replace('’',"'").replace('‘',"'")
 s=unicodedata.normalize('NFKD',s)
 s=''.join(c for c in s if not unicodedata.combining(c)).casefold()
 return ''.join(c for c in s if c.isalpha() or c=="'")

def lev(a,b):
 prev=list(range(len(b)+1))
 for i,x in enumerate(a,1):
  cur=[i]
  for j,y in enumerate(b,1):
   cur.append(min(cur[-1]+1,prev[j]+1,prev[j-1]+(x!=y)))
  prev=cur
 return prev[-1]

def enrich_seed(x):
 r=dict(x); a,b=norm(x['historical_surface']),norm(x['modern_surface'])
 r['historical_normalized']=a; r['modern_normalized']=b
 d=lev(a,b); r['edit_distance']=d; r['normalized_similarity']=round(1-d/max(len(a),len(b),1),4)
 return r

def enrich_holdout(x):
 r=dict(x); r['historical_normalized']=norm(x['historical_surface'])
 if x.get('modern_surface'):
  b=norm(x['modern_surface']); r['modern_normalized']=b
  d=lev(r['historical_normalized'],b); r['edit_distance']=d
  r['normalized_similarity']=round(1-d/max(len(r['historical_normalized']),len(b),1),4)
 else:
  r['modern_normalized_candidates']=[norm(v) for v in x.get('modern_surface_candidates',[])]
  r['edit_distance']=None; r['normalized_similarity']=None
 return r

def seed_matches(r,h,m,pos,levels):
 if r['relation_level'] not in levels:return False
 a,b=r['historical_normalized'],r['modern_normalized']
 return (a.endswith(h) and b.endswith(m)) if pos=='suffix' else (h in a and m in b)

def holdout_matches(r,pid,h,m,pos):
 flag={'tsch_to_ch':'tests_tsch_to_ch','ameke_to_ami':'tests_ameke_to_ami'}.get(pid)
 if not flag or not r.get(flag,False) or not r.get('modern_normalized'): return False
 a,b=r['historical_normalized'],r['modern_normalized']
 return (a.endswith(h) and b.endswith(m)) if pos=='suffix' else (h in a and m in b)

seed=json.loads(SEED.read_text(encoding='utf-8'))
hold=json.loads(HOLD.read_text(encoding='utf-8'))
seed_rows=[enrich_seed(x) for x in seed['records']]
hold_rows=[enrich_holdout(x) for x in hold['records']]
patterns=[]
for pid,scope,h,m,pos,levels,minfam in MOTIFS:
 sh=[r for r in seed_rows if seed_matches(r,h,m,pos,levels)]
 hh=[r for r in hold_rows if holdout_matches(r,pid,h,m,pos)]
 sp=[r for r in sh if not r['negative_control']]; sn=[r for r in sh if r['negative_control']]
 hp=[r for r in hh if r.get('count_toward_positive',False) and not r['negative_control']]
 hn=[r for r in hh if r['negative_control']]
 sf={r['family_id'] for r in sp}; hf={r['family_id'] for r in hp}; total=sf|hf
 if len(total)>=3: status='recurrent_documentary_pattern_strong'
 elif len(total)>=2: status='recurrent_documentary_pattern'
 elif len(total)==1 and (sn or hn) and scope=='lexical': status='non_discriminative_or_under_supported'
 elif len(total)==1: status='single_family_observation'
 else: status='not_observed_in_positive_evidence'
 if pid=='tsch_to_ch' and len(hf)>=3:
  status='source_supported_recurrent_phonetic_compatibility_hypothesis'
 patterns.append({
  'pattern_id':pid,'scope':scope,'historical_string':h,'modern_string':m,'position':pos,
  'seed_positive_family_count':len(sf),'seed_positive_family_ids':sorted(sf),
  'seed_negative_control_count':len(sn),'seed_negative_control_family_ids':sorted({r['family_id'] for r in sn}),
  'holdout_positive_family_count':len(hf),'holdout_positive_family_ids':sorted(hf),
  'holdout_negative_control_count':len(hn),'holdout_negative_control_family_ids':sorted({r['family_id'] for r in hn}),
  'total_positive_independent_family_count':len(total),'total_positive_family_ids':sorted(total),
  'matched_seed_ids':[r['seed_id'] for r in sh],'matched_holdout_ids':[r['holdout_id'] for r in hh],
  'status':status,'automatic_phonological_interpretation':False,'automatic_sound_correspondence_inference':False,
  'human_reviewed':False})

by={x['pattern_id']:x for x in patterns}
hold_pos=[r for r in hold_rows if r.get('count_toward_positive',False) and not r['negative_control']]
hold_neg=[r for r in hold_rows if r['negative_control']]
hold_unresolved=[r for r in hold_rows if not r.get('count_toward_positive',False) and not r['negative_control']]
summary={
 'dataset':seed['dataset'],'layer':'seed_plus_holdout_diachronic_graphemic_pattern_summary_v3','generated':seed['generated'],
 'seed_record_count':len(seed_rows),'seed_positive_record_count':sum(not r['negative_control'] for r in seed_rows),
 'seed_positive_independent_family_count':len({r['family_id'] for r in seed_rows if not r['negative_control']}),
 'holdout_record_count':len(hold_rows),'holdout_positive_record_count':len(hold_pos),
 'holdout_positive_independent_family_count':len({r['family_id'] for r in hold_pos}),
 'holdout_unresolved_record_count':len(hold_unresolved),'holdout_negative_control_record_count':len(hold_neg),
 'selection_independence':'holdouts selected by semantic/domain retrieval from published Steffel examples, not by requiring the tested modern graphic pattern; unresolved and negative cases are retained',
 'seed_pair_alignments':seed_rows,'holdout_pair_alignments':hold_rows,'patterns':patterns,
 'source_supported_interpretation':{
  'steffel_tsch':'Merrill et al. 2020 §7.5.2 associates <tsch> with voiceless palatoalveolar affricate [č] and analyzes <tsch>/<ts> as allophones of /č/.',
  'steffel_ss':'Merrill et al. 2020 §7.5.5 interprets intervocalic <ss> as voiceless [s], not phonological gemination.',
  'modern_choguita':'Caballero 2022 gives phonemic /tʃ/ and /s/, optional /tʃ/→[ts] depalatalization before low central vowels, and independently documents tʃaˈpí “grab”.',
  'shared_environment':'Historical initial <tsch>/<ts> free variation before a and modern optional /tʃ/→[ts] before low central vowels form a source-supported structural parallel; rule identity is not adjudicated.',
  'variety_caution':'Choguita and the pinned SRC-02 lexicon are independent modern sources/varieties and are not collapsed into one variety.'},
 'human_reviewed':False,'automatic_sound_correspondence_inference':False,'automatic_phonological_interpretation':False,
 'cognacy_judgment':'not_performed','historical_continuity_judgment':'not_performed'}
OUT.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

md=f'''# Perfil de correspondencias gráficas histórico → moderno

**Corte:** 2026-08-13. **Estatus:** exploratorio y reproducible; no constituye reconstrucción fonológica.

La fase de descubrimiento usa la matriz prioritaria como **semilla** y la evaluación posterior usa un conjunto **holdout seleccionado por significado/dominio independiente**. Se conservan explícitamente resultados positivos, negativos y no resueltos.

## `tsch → ch`: regularidad con holdout independiente

En la semilla, `tsch → ch` estaba apoyado por **{by['tsch_to_ch']['seed_positive_family_count']} familias**. El holdout aporta **{by['tsch_to_ch']['holdout_positive_family_count']} familias positivas**, para **{by['tsch_to_ch']['total_positive_independent_family_count']} familias positivas totales**. Los positivos incluyen `tschapí ~ Chapí` «agarrar», `tschicúli ~ Chicuri` «ratón», `tschócameke ~ Chócami` «negro», `tschutá ~ Chutá` «afilar», `echtschá ~ Ichá` «sembrar» y `tschouguá ~ Cho’huá` «extinguir/apagar». Se conserva el control `tschipú` «apestar» ~ `Chipú` «estar amargo» y el caso no resuelto `tschumíla` «boca, hocico», cuyo dominio moderno tiene más de un candidato (`Riní`, `Cho’ó`) y no se fuerza a una única correspondencia.

Este resultado cuenta además con apoyo fonético independiente: Merrill et al. (2020, §7.5.2 y Apéndice 5) atribuyen a `<tsch>` el valor [č], mientras Caballero (2022) documenta /tʃ/ y su realización opcional [ts] antes de vocal baja central. La coincidencia de entorno `a` entre la variación histórica `<tsch> ~ <ts>` y la despalatalización moderna constituye un **paralelo alofónico estructural**, no una demostración de persistencia de la misma regla.

## `-ameke → -ami`

La semilla aporta **{by['ameke_to_ami']['seed_positive_family_count']} familias positivas** y el holdout añade `tschócameke ~ Chócami` «negro», para **{by['ameke_to_ami']['total_positive_independent_family_count']} familias positivas totales**. El control `Bajéameke ~ Bajíami` recuerda que compartir el patrón terminal no demuestra identidad léxica.

## Otros motivos

`ss → s` continúa limitado a una familia de la matriz, aunque Merrill interpreta `<ss>` intervocálica como [s] sorda y no geminación. `aa → a` sigue siendo una observación de una sola familia. El final `e → i` permanece no discriminativo porque aparece tanto en `Cotſchimé ~ Cochí` como en el control semánticamente negativo `Bajé ~ Bají`.

## Resumen cuantitativo

| Patrón | Semilla + | Holdout + | Familias + totales | Controles negativos | Estatus |
|---|---:|---:|---:|---:|---|
'''
for x in patterns:
 md+=f"| `{x['historical_string']} → {x['modern_string']}` | {x['seed_positive_family_count']} | {x['holdout_positive_family_count']} | {x['total_positive_independent_family_count']} | {x['seed_negative_control_count']+x['holdout_negative_control_count']} | `{x['status']}` |\n"
md+=f'''

El holdout completo contiene **{len(hold_pos)} positivos, {len(hold_unresolved)} no resuelto y {len(hold_neg)} control negativo**. Retener los casos adversos es parte del diseño contra circularidad.

Las formas diplomáticas permanecen intactas. Las semejanzas gráficas y la compatibilidad fonética no adjudican cognación. Para promover una regularidad a correspondencia histórica se requiere todavía control dialectal explícito, ampliación a más vocabulario no seleccionado, análisis de contexto segmental y revisión humana/comparativa independiente.

`automatic_sound_correspondence_inference=false`; `automatic_phonological_interpretation=false`; `human_reviewed=false`; `cognacy_judgment=not_performed`; `historical_continuity_judgment=not_performed`.
'''
REPORT.write_text(md,encoding='utf-8')
print(json.dumps({'tsch_total_families':by['tsch_to_ch']['total_positive_independent_family_count'],'ameke_total_families':by['ameke_to_ami']['total_positive_independent_family_count'],'holdout_positive':len(hold_pos),'holdout_unresolved':len(hold_unresolved),'holdout_negative':len(hold_neg),'human_reviewed':False},ensure_ascii=False))
