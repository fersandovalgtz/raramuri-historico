#!/usr/bin/env python3
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
V=ROOT/'data'/'validation'; R=V/'review'; D=V/'dossiers'/'priority1'
priority=json.load((V/'human_review_priority.json').open(encoding='utf-8'))
unc=json.load((V/'uncertainty_queue.json').open(encoding='utf-8'))
unc_by={x['record_id']:x for x in unc.get('records',[])}
phil={}
for p in sorted(R.glob('philological_review_batch_*.json')):
    m=json.load(p.open(encoding='utf-8'))
    for x in m.get('records',[]):
        y=dict(x); y['_batch']=m.get('batch_id'); y['_manifest']=str(p.relative_to(ROOT)); phil[y['record_id']]=y
p1=[x for x in priority.get('records',[]) if x.get('priority_rank')==1 and x.get('ai_recollation_disposition')=='unresolved_after_ai_recollation']
records=[]; compact=[]; D.mkdir(parents=True,exist_ok=True)
for n,p in enumerate(p1,1):
    rid=p['record_id']; u=unc_by.get(rid); ph=phil.get(rid)
    if not u or not ph: raise SystemExit(f'missing dossier evidence: {rid}')
    did=f'RHD-HUM-P1-{n:03d}'
    ai={k:ph.get(k) for k in ('disposition','residual_route','note','previous_reading','proposed_reading','confirmed_reading','correction_scope') if ph.get(k) is not None}
    ai.update({'source_batch':ph.get('_batch'),'source_manifest':ph.get('_manifest')})
    rec={
      'dossier_id':did,'review_order':n,'record_id':rid,'status':'awaiting_independent_review','priority_rank':1,
      'source_locator':{'source_authority':'Steffel 1809 facsimile','printed_page':u.get('printed_page'),'pdf_page':u.get('pdf_page'),'facsimile_column':u.get('facsimile_column'),'direction':u.get('direction')},
      'documentary_record':{'headword_diplomatic':u.get('headword_diplomatic'),'article_diplomatic':u.get('article_diplomatic')},
      'open_validation':{'category':u.get('category'),'note':u.get('open_validation_note'),'recommended_action':u.get('recommended_action')},
      'ai_recollation':ai,
      'independent_review':{'reviewer':{'name':'','affiliation':'','orcid':'','expertise':[]},'review_date':'','phil_relationship':'not_applicable','philological_decision':{'status':'not_assessed','reading':'','evidence':'','confidence':'not_assessed'},'linguistic_decision':{'status':'not_assessed','analysis':'','evidence':''},'semantic_historical_decision':{'status':'not_assessed','analysis':'','evidence':''},'disciplinary_decision':{'domain':'','status':'not_assessed','analysis':'','evidence':''},'reviewer_note':''},
      'verification':{'human_verified':False,'philologically_verified_by_human':False,'linguistically_verified':False}
    }
    records.append(rec); compact.append([n,did,rid,u.get('printed_page'),u.get('pdf_page'),u.get('facsimile_column'),u.get('direction'),u.get('headword_diplomatic'),u.get('category'),ph.get('_batch'),ai.get('residual_route')])
    s=rec['source_locator']; d=rec['documentary_record']; o=rec['open_validation']
    lines=[f'# {did} — {rid}','', '**Estado:** pendiente de revisión humana independiente.  ',f'**Orden:** {n} de {len(p1)}.  ',f"**Fuente PHIL:** `{ph.get('_batch')}` · `{ph.get('_manifest')}`.",'','## Localización facsimilar','',f"- página impresa: **{s['printed_page']}**",f"- página PDF: **{s['pdf_page']}**",f"- columna: **{s['facsimile_column']}**",f"- dirección: **{s['direction']}**",'','## Evidencia diplomática preservada','',f"**Lema:** `{d['headword_diplomatic']}`",'',f"**Artículo:** {d['article_diplomatic']}",'','## Problema abierto','',f"**Categoría:** `{o['category']}`",'',f"**Nota:** {o['note']}",'',f"**Acción recomendada:** {o['recommended_action']}",'','## Recotejo IA-asistido','',f"**Disposición:** `{ai.get('disposition')}`",'',f"**Ruta residual:** `{ai.get('residual_route')}`",'',f"**Nota PHIL:** {ai.get('note','')}"]
    for label,key in [('Lectura previa','previous_reading'),('Lectura propuesta','proposed_reading'),('Lectura confirmada/provisional','confirmed_reading'),('Alcance de corrección','correction_scope')]:
        if ai.get(key): lines += ['',f'**{label}:** {ai[key]}']
    lines += ['','## Decisión del revisor independiente','','**Revisor:**  ','**Afiliación:**  ','**ORCID:**  ','**Competencia relevante:**  ','**Fecha:**  ','','**Relación con PHIL:** `confirm | accept_proposed_correction | modify_proposed_correction | reject_proposed_correction | not_applicable`','','**Decisión filológica:** `confirmed_diplomatic | accepted_ai_proposed_correction | human_corrected_reading | remain_unresolved | not_assessed`','','**Lectura adoptada/propuesta:**  ','','**Evidencia y justificación:**  ','','**Confianza:** `high | medium | low | not_assessed`','','**Decisión lingüística:** `confirmed | corrected | variant_identified | uncertain | not_assessed`','','**Análisis lingüístico / evidencia:**  ','','**Decisión semántica-histórica:** `confirmed_source_gloss | clarified_historical_sense | requires_contextual_annotation | uncertain | not_assessed`','','**Análisis semántico-histórico / evidencia:**  ','','**Anotación disciplinar especializada:**  ','','## Regla de preservación','','La revisión independiente puede alimentar una capa crítica o normalizada derivada, pero no debe sobrescribir el facsímil, OCR, `headword_diplomatic`, `article_diplomatic` ni el historial PHIL. Las banderas de verificación permanecen en `false` hasta una decisión humana explícita y trazable.','']
    (D/f'{did}_{rid}.md').write_text('\n'.join(lines),encoding='utf-8')
out={'stage':'priority1_independent_human_review_dossiers','selection_rule':'priority_rank=1 and unresolved_after_ai_recollation in deterministic priority order','count':len(records),'human_verified':False,'records':records}
(V/'priority1_review_dossiers.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
co={'stage':'priority1_independent_human_review_dossiers','count':len(compact),'human_verified':False,'fields':['review_order','dossier_id','record_id','printed_page','pdf_page','facsimile_column','direction','headword_diplomatic','category','source_batch','residual_route'],'records':compact}
(V/'priority1_review_dossiers_compact.json').write_text(json.dumps(co,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
idx=['# Expedientes de revisión humana — prioridad 1','','Casos `unresolved_after_ai_recollation` preparados para revisión independiente; no constituyen validación humana ni lingüística.','','| Orden | Expediente | Registro | p. impresa | p. PDF | columna | dirección | lema | ruta residual |','|---:|---|---|---:|---:|---|---|---|---|']
for r in records:
    s=r['source_locator']; a=r['ai_recollation']; d=r['documentary_record']; fn=f"{r['dossier_id']}_{r['record_id']}.md"
    idx.append(f"| {r['review_order']} | [{r['dossier_id']}](dossiers/priority1/{fn}) | `{r['record_id']}` | {s['printed_page']} | {s['pdf_page']} | {s['facsimile_column']} | {s['direction']} | {d['headword_diplomatic']} | `{a.get('residual_route','')}` |")
(V/'PRIORITY1_REVIEW_INDEX.md').write_text('\n'.join(idx)+'\n',encoding='utf-8')
print(f'Generated {len(records)} priority-1 independent-review dossiers')
