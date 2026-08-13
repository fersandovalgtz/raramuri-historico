#!/usr/bin/env python3
import json, unicodedata
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data/research/diachronic_graphemic_seed_pairs.json'
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

def matches(r,h,m,pos,levels):
 if r['relation_level'] not in levels:return False
 a,b=r['historical_normalized'],r['modern_normalized']
 return (a.endswith(h) and b.endswith(m)) if pos=='suffix' else (h in a and m in b)

src=json.loads(SRC.read_text(encoding='utf-8'))
rows=[]
for x in src['records']:
 r=dict(x); a,b=norm(x['historical_surface']),norm(x['modern_surface'])
 r['historical_normalized']=a; r['modern_normalized']=b
 d=lev(a,b); r['edit_distance']=d; r['normalized_similarity']=round(1-d/max(len(a),len(b),1),4)
 rows.append(r)

patterns=[]
for pid,scope,h,m,pos,levels,minfam in MOTIFS:
 hit=[r for r in rows if matches(r,h,m,pos,levels)]
 positive=[r for r in hit if not r['negative_control']]
 negative=[r for r in hit if r['negative_control']]
 pf=sorted({r['family_id'] for r in positive}); nf=sorted({r['family_id'] for r in negative})
 if len(pf)>=minfam: status='recurrent_documentary_pattern_strong' if len(pf)>=3 else 'recurrent_documentary_pattern'
 elif len(pf)==1 and scope=='lexical' and nf: status='non_discriminative_or_under_supported'
 elif len(pf)==1: status='single_family_observation'
 else: status='not_observed_in_positive_seed_families'
 patterns.append({'pattern_id':pid,'scope':scope,'historical_string':h,'modern_string':m,'position':pos,
  'positive_independent_family_count':len(pf),'positive_family_ids':pf,'negative_control_match_count':len(negative),
  'negative_control_family_ids':nf,'matched_seed_ids':[r['seed_id'] for r in hit],'status':status})

summary={'dataset':src['dataset'],'layer':'priority_seed_diachronic_graphemic_pattern_summary_v1','generated':src['generated'],
 'seed_record_count':len(rows),'positive_seed_record_count':sum(not r['negative_control'] for r in rows),
 'positive_independent_family_count':len({r['family_id'] for r in rows if not r['negative_control']}),
 'negative_control_record_count':sum(r['negative_control'] for r in rows),'pair_alignments':rows,'patterns':patterns,
 'human_reviewed':False,'automatic_sound_correspondence_inference':False,'automatic_phonological_interpretation':False,
 'cognacy_judgment':'not_performed','historical_continuity_judgment':'not_performed'}
OUT.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

p={x['pattern_id']:x for x in patterns}
md=f'''# Perfil de correspondencias gráficas histórico → moderno

**Corte:** 2026-08-13. **Estatus:** exploratorio y reproducible; no constituye reconstrucción fonológica.

Se analizaron **{summary['positive_seed_record_count']} registros positivos** de **{summary['positive_independent_family_count']} familias léxicas independientes**, más **{summary['negative_control_record_count']} controles negativos**. El algoritmo sólo prueba motivos gráficos predefinidos sobre candidatos ya priorizados; no descubre cognados nuevos.

## Resultado principal

`-ameke → -ami` aparece en **{p['ameke_to_ami']['positive_independent_family_count']} familias positivas independientes**: {', '.join(p['ameke_to_ami']['positive_family_ids'])}. Se conserva como regularidad documental del dominio participial, no como identidad morfológica adjudicada.

`tsch → ch` aparece en **{p['tsch_to_ch']['positive_independent_family_count']} familias positivas independientes**: {', '.join(p['tsch_to_ch']['positive_family_ids'])}. Es la primera diferencia gráfica histórica concreta de esta matriz que supera el requisito de más de un lexema semánticamente convergente. Su estatus es **hipótesis de regularidad gráfica recurrente**, no correspondencia fonológica.

`ss → s` y `aa → a` siguen apoyados por una sola familia. `e → i` final aparece en un candidato positivo, pero también en el control negativo `Bajé ~ Bají`; por ello esa semejanza aislada no discrimina continuidad histórica.

## Patrones

| Patrón | Familias positivas | Control negativo | Estatus |
|---|---:|---:|---|
'''
for x in patterns:
 md+=f"| `{x['historical_string']} → {x['modern_string']}` | {x['positive_independent_family_count']} | {x['negative_control_match_count']} | `{x['status']}` |\n"
md+='''

Las formas diplomáticas permanecen intactas. Las distancias de edición son descriptivas; no representan fonemas ni morfemas. Ningún resultado modifica `human_reviewed=false`, `cognacy_judgment=not_performed` o `historical_continuity_judgment=not_performed`.
'''
REPORT.write_text(md,encoding='utf-8')
print(json.dumps({'patterns':patterns,'human_reviewed':False},ensure_ascii=False))
