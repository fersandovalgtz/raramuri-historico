#!/usr/bin/env python3
"""Generate conservative diachronic graphemic profiles.

Seed evidence and out-of-seed semantic holdouts are kept separate. The output
is documentary/comparative only: no cognacy, sound change, phoneme identity,
or historical continuity is automatically adjudicated.
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

def enrich(x,id_field):
 r=dict(x); a,b=norm(x['historical_surface']),norm(x['modern_surface'])
 r['historical_normalized']=a; r['modern_normalized']=b
 d=lev(a,b); r['edit_distance']=d; r['normalized_similarity']=round(1-d/max(len(a),len(b),1),4)
 r['record_key']=r[id_field]
 return r

def seed_matches(r,h,m,pos,levels):
 if r['relation_level'] not in levels:return False
 a,b=r['historical_normalized'],r['modern_normalized']
 return (a.endswith(h) and b.endswith(m)) if pos=='suffix' else (h in a and m in b)

def holdout_matches(r,pid,h,m,pos):
 flag={'tsch_to_ch':'tests_tsch_to_ch','ameke_to_ami':'tests_ameke_to_ami'}.get(pid)
 if not flag or not r.get(flag,False): return False
 a,b=r['historical_normalized'],r['modern_normalized']
 return (a.endswith(h) and b.endswith(m)) if pos=='suffix' else (h in a and m in b)

seed=json.loads(SEED.read_text(encoding='utf-8'))
hold=json.loads(HOLD.read_text(encoding='utf-8'))
seed_rows=[enrich(x,'seed_id') for x in seed['records']]
hold_rows=[enrich(x,'holdout_id') for x in hold['records']]
patterns=[]
for pid,scope,h,m,pos,levels,minfam in MOTIFS:
 sh=[r for r in seed_rows if seed_matches(r,h,m,pos,levels)]
 hp=[r for r in hold_rows if holdout_matches(r,pid,h,m,pos)]
 sp=[r for r in sh if not r['negative_control']]; sn=[r for r in sh if r['negative_control']]
 pp=[r for r in hp if not r['negative_control']]; pn=[r for r in hp if r['negative_control']]
 sf={r['family_id'] for r in sp}; hf={r['family_id'] for r in pp}; total=sf|hf
 if len(total)>=3: status='recurrent_documentary_pattern_strong'
 elif len(total)>=2: status='recurrent_documentary_pattern'
 elif len(total)==1 and (sn or pn) and scope=='lexical': status='non_discriminative_or_under_supported'
 elif len(total)==1: status='single_family_observation'
 else: status='not_observed_in_positive_evidence'
 patterns.append({
  'pattern_id':pid,'scope':scope,'historical_string':h,'modern_string':m,'position':pos,
  'seed_positive_family_count':len(sf),'seed_positive_family_ids':sorted(sf),
  'seed_negative_control_count':len(sn),'seed_negative_control_family_ids':sorted({r['family_id'] for r in sn}),
  'holdout_positive_family_count':len(hf),'holdout_positive_family_ids':sorted(hf),
  'holdout_negative_control_count':len(pn),'holdout_negative_control_family_ids':sorted({r['family_id'] for r in pn}),
  'total_positive_independent_family_count':len(total),'total_positive_family_ids':sorted(total),
  'matched_seed_ids':[r['seed_id'] for r in sh],'matched_holdout_ids':[r['holdout_id'] for r in hp],
  'status':status,'automatic_phonological_interpretation':False,'automatic_sound_correspondence_inference':False,
  'human_reviewed':False})

by={x['pattern_id']:x for x in patterns}
summary={
 'dataset':seed['dataset'],'layer':'seed_plus_holdout_diachronic_graphemic_pattern_summary_v2','generated':seed['generated'],
 'seed_record_count':len(seed_rows),'seed_positive_record_count':sum(not r['negative_control'] for r in seed_rows),
 'seed_positive_independent_family_count':len({r['family_id'] for r in seed_rows if not r['negative_control']}),
 'holdout_record_count':len(hold_rows),'holdout_positive_record_count':sum(not r['negative_control'] for r in hold_rows),
 'holdout_positive_independent_family_count':len({r['family_id'] for r in hold_rows if not r['negative_control']}),
 'selection_independence':'holdouts selected by semantic equivalence from published Steffel examples, not by requiring the tested modern graphic pattern',
 'seed_pair_alignments':seed_rows,'holdout_pair_alignments':hold_rows,'patterns':patterns,
 'source_supported_interpretation':{
  'steffel_tsch':'Merrill et al. 2020 §7.5.2 associates <tsch> with voiceless palatoalveolar affricate [č] and analyzes <tsch>/<ts> as allophones of /č/.',
  'steffel_ss':'Merrill et al. 2020 §7.5.5 interprets intervocalic <ss> as voiceless [s], not phonological gemination.',
  'modern_choguita':'Caballero 2022 gives phonemic /tʃ/ and /s/ and independently documents tʃaˈpí “grab”.',
  'variety_caution':'Choguita and the pinned SRC-02 lexicon are independent modern sources/varieties and are not collapsed into one variety.'},
 'human_reviewed':False,'automatic_sound_correspondence_inference':False,'automatic_phonological_interpretation':False,
 'cognacy_judgment':'not_performed','historical_continuity_judgment':'not_performed'}
OUT.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

md=f'''# Perfil de correspondencias gráficas histórico → moderno

**Corte:** 2026-08-13. **Estatus:** exploratorio y reproducible; no constituye reconstrucción fonológica.

La fase de descubrimiento usa la matriz prioritaria como **semilla** y la evaluación posterior usa un conjunto **holdout seleccionado por equivalencia semántica independiente**. Se conservan ambos estratos separados para evitar contar como validación los mismos pares que originaron la hipótesis.

## `tsch → ch`: primera regularidad con holdout independiente

En la semilla, `tsch → ch` estaba apoyado por **{by['tsch_to_ch']['seed_positive_family_count']} familias**. El holdout añade **{by['tsch_to_ch']['holdout_positive_family_count']} familias semánticamente independientes**, para **{by['tsch_to_ch']['total_positive_independent_family_count']} familias positivas totales**. El holdout incluye `tschapí ~ Chapí` «agarrar», `tschicúli ~ Chicuri` «ratón», `tschócameke ~ Chócami` «negro», `tschutá ~ Chutá` «afilar» y `echtschá ~ Ichá` «sembrar». También se conserva el control `tschipú` «apestar» ~ `Chipú` «estar amargo», formalmente atractivo pero semánticamente fallido.

Este resultado ya no es sólo gráfico: Merrill et al. (2020, §7.5.2) atribuyen a `<tsch>` de Steffel el valor de africada palatoalveolar sorda [č] y Caballero (2022) documenta /tʃ/ en Choguita, incluyendo explícitamente `tʃaˈpí` «grab». Por ello `tsch ~ ch` puede describirse como **compatibilidad fonética respaldada por fuentes y recurrente en múltiples familias**, pero todavía no como ley de cambio histórico.

## `-ameke → -ami`

La semilla aporta **{by['ameke_to_ami']['seed_positive_family_count']} familias positivas** y el holdout añade `tschócameke ~ Chócami` «negro», para **{by['ameke_to_ami']['total_positive_independent_family_count']} familias positivas totales**. El control `Bajéameke ~ Bajíami` recuerda que compartir el patrón derivacional no demuestra identidad léxica.

## Otros motivos

`ss → s` continúa limitado a una familia de la matriz, aunque Merrill ofrece una interpretación fonética independiente decisiva: `<ss>` intervocálica representa [s] sorda y no geminación. `aa → a` sigue siendo una observación de una sola familia. El final `e → i` permanece no discriminativo porque aparece tanto en `Cotſchimé ~ Cochí` como en el control semánticamente negativo `Bajé ~ Bají`.

## Resumen cuantitativo

| Patrón | Semilla + | Holdout + | Familias + totales | Controles negativos | Estatus |
|---|---:|---:|---:|---:|---|
'''
for x in patterns:
 md+=f"| `{x['historical_string']} → {x['modern_string']}` | {x['seed_positive_family_count']} | {x['holdout_positive_family_count']} | {x['total_positive_independent_family_count']} | {x['seed_negative_control_count']+x['holdout_negative_control_count']} | `{x['status']}` |\n"
md+='''

Las formas diplomáticas permanecen intactas. Las semejanzas gráficas y la compatibilidad fonética no adjudican cognación. Para promover una regularidad a correspondencia histórica se requiere todavía control dialectal explícito, ampliación a más vocabulario no seleccionado, análisis de contexto segmental y revisión humana/comparativa independiente.

`automatic_sound_correspondence_inference=false`; `automatic_phonological_interpretation=false`; `human_reviewed=false`; `cognacy_judgment=not_performed`; `historical_continuity_judgment=not_performed`.
'''
REPORT.write_text(md,encoding='utf-8')
print(json.dumps({'tsch_total_families':by['tsch_to_ch']['total_positive_independent_family_count'],'ameke_total_families':by['ameke_to_ami']['total_positive_independent_family_count'],'human_reviewed':False},ensure_ascii=False))
