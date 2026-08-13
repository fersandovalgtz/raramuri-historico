#!/usr/bin/env python3
"""Exact descriptive tests for initial <tsch>/<ts> distribution.

Uses corpus counts only. Fisher exact p-values measure association inside this
finite diplomatic inventory; they are not population-level sampling claims and
do not establish phoneme identity or historical rule persistence.
"""
from __future__ import annotations
import json, math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'data/research'
IN=D/'historical_affricate_graphemic_inventory_summary.json'
OUT=D/'historical_affricate_distribution_tests.json'
REPORT=D/'HISTORICAL_AFFRICATE_DISTRIBUTION_TESTS.md'


def hypergeom_prob(a,b,c,d):
    r1=a+b; r2=c+d; c1=a+c; n=r1+r2
    return math.comb(c1,a)*math.comb(n-c1,r1-a)/math.comb(n,r1)

def fisher_two_sided(tab):
    a,b=tab[0]; c,d=tab[1]
    r1=a+b; r2=c+d; c1=a+c; n=r1+r2
    lo=max(0,r1-(n-c1)); hi=min(r1,c1)
    pobs=hypergeom_prob(a,b,c,d)
    p=0.0
    for x in range(lo,hi+1):
        y=r1-x; z=c1-x; w=r2-z
        q=hypergeom_prob(x,y,z,w)
        if q <= pobs + 1e-15: p += q
    return min(1.0,p)

def corrected_or(tab):
    a,b=tab[0]; c,d=tab[1]
    return ((a+.5)*(d+.5))/((b+.5)*(c+.5))

def get(c,key): return int(c.get(key,0))

s=json.loads(IN.read_text(encoding='utf-8'))
c=s['grapheme_position_following_counts']
ts_a=get(c,'ts:initial:a'); ts_e=get(c,'ts:initial:e'); ts_iou=sum(get(c,f'ts:initial:{v}') for v in 'iou')
tsch_a=get(c,'tsch:initial:a'); tsch_e=get(c,'tsch:initial:e'); tsch_iou=sum(get(c,f'tsch:initial:{v}') for v in 'iou')
base=[[ts_e,ts_iou],[tsch_e,tsch_iou]]
base_n=sum(map(sum,base)); base_initial=ts_a+tsch_a+base_n
base_compatible=base_initial-s['potential_initial_exception_count']

sens=s.get('facsimile_correction_sensitivity') or {}
# Sensitivity is deliberately narrow: the sole proposed Tſchécemeke→Tſchócameke
# recollation moves one initial tsch token from e to o.
if sens.get('sensitivity_potential_initial_exception_count')==0 and tsch_e>=1:
    sens_tab=[[ts_e,ts_iou],[tsch_e-1,tsch_iou+1]]
else:
    sens_tab=base
sens_n=sum(map(sum,sens_tab)); sens_initial=ts_a+tsch_a+sens_n
sens_exceptions=int(sens.get('sensitivity_potential_initial_exception_count',s['potential_initial_exception_count']))
sens_compatible=sens_initial-sens_exceptions

payload={
 'dataset':s['dataset'],'layer':'historical_affricate_initial_distribution_exact_tests_v1','generated':'2026-08-13',
 'scope':'Initial occurrences with following vowel; <a> is analyzed separately because Merrill reports free variation there.',
 'initial_a':{
   'ts_count':ts_a,'tsch_count':tsch_a,'total':ts_a+tsch_a,
   'interpretation':'Both spellings are attested before a; equal 6/6 counts are compatible with, but do not prove, free variation.'},
 'non_a_baseline':{
   'table_rows':['ts','tsch'],'table_columns':['e','i_o_u'],'table':base,'n':base_n,
   'fisher_two_sided_p':fisher_two_sided(base),'haldane_anscombe_odds_ratio':corrected_or(base),
   'interpretation':'Very strong within-corpus association between grapheme choice and following vowel category; one diplomatic tsch+e exception remains.'},
 'non_a_facsimile_sensitivity':{
   'table_rows':['ts','tsch'],'table_columns':['e','i_o_u'],'table':sens_tab,'n':sens_n,
   'fisher_two_sided_p':fisher_two_sided(sens_tab),'haldane_anscombe_odds_ratio':corrected_or(sens_tab),
   'interpretation':'Under the facsimile-based proposed reading, e is exclusively ts and i/o/u exclusively tsch in the current initial inventory.'},
 'merrill_simple_initial_model':{
   'baseline_initial_vowel_occurrences':base_initial,'baseline_compatible':base_compatible,
   'baseline_compatibility_rate':round(base_compatible/base_initial,6) if base_initial else None,
   'facsimile_sensitivity_initial_vowel_occurrences':sens_initial,'facsimile_sensitivity_compatible':sens_compatible,
   'facsimile_sensitivity_compatibility_rate':round(sens_compatible/sens_initial,6) if sens_initial else None},
 'sampling_inference_caution':'The corpus is not a random sample. Fisher p-values are descriptive exact association measures conditional on observed margins, not estimates of population-level historical probabilities.',
 'automatic_phonological_interpretation':False,'automatic_rule_equation':False,'historical_rule_continuity_judgment':'not_performed','human_reviewed':False}
OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

md=f'''# Pruebas exactas de distribución inicial `<ts>` / `<tsch>`

**Corte:** 2026-08-13. **Estatus:** estadística descriptiva exacta del inventario; no es inferencia de una ley fonológica.

## Antes de `a`

El inventario contiene **{ts_a} `<ts>` y {tsch_a} `<tsch>`** en posición inicial antes de `a`. La presencia de ambas grafías, con 6/6 ocurrencias, es compatible con la descripción de Merrill de variación libre en ese entorno. La igualdad de conteos no demuestra por sí sola variación libre fonológica.

## Fuera de `a`: `e` frente a `i/o/u`

En la capa diplomática actual la tabla es `[[{ts_e}, {ts_iou}], [{tsch_e}, {tsch_iou}]]` para filas `<ts>, <tsch>` y columnas `e, i/o/u`. La asociación exacta es muy fuerte: **Fisher bilateral p={payload['non_a_baseline']['fisher_two_sided_p']:.3g}**. La única celda discordante es el registro `Tſchécemeke` ya enviado a revisión facsimilar.

En la sensibilidad que usa la lectura propuesta `Tſchócameke` sin modificar el diplomático, la tabla pasa a `[[{sens_tab[0][0]}, {sens_tab[0][1]}], [{sens_tab[1][0]}, {sens_tab[1][1]}]]`: `e` queda exclusivamente con `<ts>` e `i/o/u` exclusivamente con `<tsch>`. Fisher bilateral: **p={payload['non_a_facsimile_sensitivity']['fisher_two_sided_p']:.3g}**.

## Ajuste al modelo inicial simple de Merrill

- capa diplomática: **{base_compatible}/{base_initial} = {100*payload['merrill_simple_initial_model']['baseline_compatibility_rate']:.1f}%** de las ocurrencias iniciales ante vocal compatibles;
- sensibilidad facsimilar: **{sens_compatible}/{sens_initial} = {100*payload['merrill_simple_initial_model']['facsimile_sensitivity_compatibility_rate']:.1f}%**.

Estos porcentajes describen este inventario concreto; no son tasas de una población histórica aleatoria. El resultado refuerza la correspondencia entre la distribución observada en RHD y el análisis publicado de Merrill, pero no demuestra identidad de reglas a través del tiempo.

`automatic_phonological_interpretation=false`; `automatic_rule_equation=false`; `historical_rule_continuity_judgment=not_performed`; `human_reviewed=false`.
'''
REPORT.write_text(md,encoding='utf-8')
print(json.dumps(payload,ensure_ascii=False))
