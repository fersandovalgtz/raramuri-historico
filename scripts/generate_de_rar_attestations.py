#!/usr/bin/env python3
from collections import defaultdict
from research_common import ROOT,OUT,rows,active,norm,alen,split_components,gloss,dump
import csv,re,json

GERMAN_STOPWORDS={'aber','alle','als','am','an','auch','auf','aus','bei','beim','bis','da','das','dem','den','der','des','die','ein','eine','einem','einen','einer','eines','er','es','für','hat','haben','im','in','ist','item','man','mit','nach','nicht','noch','oder','ohne','sein','sind','so','und','vom','von','vor','war','werden','wie','wird','zu','zum','zur'}

def reciprocal(de_head,rar_gloss):
    a,b=norm(de_head),norm(rar_gloss)
    if not a or not b: return False,'none'
    if a==b: return True,'exact_normalized_german_headword_gloss_match'
    if alen(a)>=4 and (f' {a} ' in f' {b} ' or f' {b} ' in f' {a} '): return True,'german_headword_gloss_containment'
    return False,'none'

def residual_segments(article,headword):
    t=re.sub(r'\s+',' ',article or '').strip()
    if headword and t.startswith(headword): t=t[len(headword):].lstrip(' ,.;:-')
    out=[]; seen=set()
    for seg in re.split(r'[.,;:!?]',t):
        seg=re.sub(r'\s+',' ',seg).strip().strip(' .,:;!?()[]{}\"')
        k=norm(seg)
        if not k or alen(seg)<3 or alen(seg)>30: continue
        words=k.split()
        if not 1<=len(words)<=3: continue
        if sum(w in GERMAN_STOPWORDS for w in words)/len(words)>=.5: continue
        if k==norm(headword) or (seg,k) in seen: continue
        seen.add((seg,k)); out.append(seg)
    return out

def main():
    rr=[r for r in rows() if active(r)]
    de=[r for r in rr if r.get('direction')=='DE-RAR']; rar=[r for r in rr if r.get('direction')=='RAR-DE']
    inv=defaultdict(list)
    for r in rar:
        form=(r.get('headword_diplomatic') or '').strip(); g=gloss(r.get('article_diplomatic',''),form)
        for i,c in enumerate(split_components(form),1):
            inv[norm(c)].append({'record_id':r.get('record_id',''),'component_index':i,'component':c,'printed_page':int(r.get('printed_page') or 0),'german_gloss_local':g})
    keys=sorted(inv,key=lambda k:(-len(k),k)); attest=[]; seen=set(); residual=[]; rseen=set()
    for r in de:
        did=r.get('record_id',''); head=(r.get('headword_diplomatic') or '').strip(); article=(r.get('article_diplomatic') or '').strip(); an=f" {norm(article)} "; hk=norm(head)
        for k in keys:
            if len(re.sub(r'[^a-z0-9]','',k))<3 or k==hk or f' {k} ' not in an: continue
            for src in inv[k]:
                marker=(did,src['record_id'],src['component_index'],k)
                if marker in seen: continue
                seen.add(marker); rec,rt=reciprocal(head,src['german_gloss_local'])
                attest.append({'attestation_id':'','de_rar_record_id':did,'de_rar_headword_diplomatic':head,'de_rar_article_diplomatic':article,'de_rar_printed_page':int(r.get('printed_page') or 0),'rar_de_record_id':src['record_id'],'rar_de_component_index':src['component_index'],'rar_de_form_diplomatic':src['component'],'rar_de_german_gloss_local':src['german_gloss_local'],'rar_de_printed_page':src['printed_page'],'graphic_key':k,'short_form_warning':len(re.sub(r'[^a-z0-9]','',k))<4,'reciprocal_german_support':rec,'reciprocal_support_type':rt,'status':'machine_documentary_candidate','human_reviewed':False,'method':'rar_de_inventory_guided_exact_attestation_v1','interpretive_scope':'Exact normalized form attestation inside a DE-RAR article; no lexical, semantic, etymological, dialectal or historical identity is asserted.'})
        for seg in residual_segments(article,head):
            k=norm(seg)
            if k in inv or (did,k) in rseen: continue
            rseen.add((did,k)); residual.append({'candidate_id':'','de_rar_record_id':did,'de_rar_headword_diplomatic':head,'candidate_span_diplomatic':seg,'graphic_key':k,'printed_page':int(r.get('printed_page') or 0),'confidence':'low_machine','status':'unclassified_residual_span','human_reviewed':False,'method':'punctuation_segment_residual_queue_v1','interpretive_scope':'Residual punctuation-derived span for inspection only; it is not asserted to be a Rarámuri form.'})
    attest.sort(key=lambda x:(x['de_rar_record_id'],x['rar_de_record_id'],x['rar_de_component_index']))
    residual.sort(key=lambda x:(x['de_rar_record_id'],x['graphic_key']))
    for i,x in enumerate(attest,1): x['attestation_id']=f'RHD-IATT-{i:06d}'
    for i,x in enumerate(residual,1): x['candidate_id']=f'RHD-RSPAN-{i:06d}'
    dump(OUT/'de_rar_inventory_guided_attestations.json',{'dataset':'raramuri-historico-steffel-1809','layer':'de_rar_inventory_guided_raramuri_attestations','generated':'2026-08-13','count':len(attest),'human_reviewed':False,'exhaustive_extraction':False,'method_note':'High-precision inventory-guided attestation layer; not exhaustive parsing of all DE-RAR Rarámuri strings.','records':attest})
    dump(OUT/'de_rar_residual_span_candidates.json',{'dataset':'raramuri-historico-steffel-1809','layer':'de_rar_residual_span_candidates','generated':'2026-08-13','count':len(residual),'human_reviewed':False,'records':residual})
    summary={'candidate_count':len(attest),'de_rar_records_represented':len({x['de_rar_record_id'] for x in attest}),'rar_de_records_represented':len({x['rar_de_record_id'] for x in attest}),'unique_graphic_keys':len({x['graphic_key'] for x in attest}),'reciprocal_german_support_count':sum(x['reciprocal_german_support'] for x in attest),'short_form_warning_count':sum(x['short_form_warning'] for x in attest),'residual_span_candidates_low_machine':len(residual),'human_reviewed':False}
    dump(OUT/'de_rar_inventory_guided_attestations_summary.json',summary)
    with (OUT/'de_rar_inventory_guided_attestations.csv').open('w',encoding='utf-8',newline='') as f:
        fields=['attestation_id','de_rar_record_id','de_rar_headword_diplomatic','de_rar_printed_page','rar_de_record_id','rar_de_component_index','rar_de_form_diplomatic','rar_de_german_gloss_local','rar_de_printed_page','graphic_key','short_form_warning','reciprocal_german_support','reciprocal_support_type','human_reviewed']; w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); [w.writerow({k:x.get(k,'') for k in fields}) for x in attest]
    print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__': main()
