#!/usr/bin/env python3
"""Document German context for exact historical X ~ X+ameke graphic pairs.
No morphological or semantic relation is inferred automatically.
"""
import json,re,unicodedata
from research_common import OUT,rows,active,norm,gloss,dump

def de_tokens(s):
 s=unicodedata.normalize('NFKD',s or '');s=''.join(c for c in s if not unicodedata.combining(c));s=s.replace('ſ','s').replace('ß','ss').casefold()
 return set(re.findall(r'[a-z]+',s))

def main():
 src=json.loads((OUT/'ameke_ke_segmentation_evidence_summary.json').read_text(encoding='utf-8'))['bare_base_counterpart_examples']
 rr={r.get('record_id',''):r for r in rows() if active(r)};out=[]
 for i,x in enumerate(src,1):
  base_articles=[];ameke_articles=[]
  for a in x['bare_base_attestations']:
   r=rr.get(a['record_id'],{});base_articles.append({'record_id':a['record_id'],'surface':a['surface'],'page':a['page'],'article':r.get('article_diplomatic',''),'german_gloss':gloss(r.get('article_diplomatic',''),r.get('headword_diplomatic',''))})
  for a in x['ameke_attestations']:
   r=rr.get(a['record_id'],{});ameke_articles.append({'record_id':a['record_id'],'surface':a['surface'],'page':a['page'],'article':r.get('article_diplomatic',''),'german_gloss':gloss(r.get('article_diplomatic',''),r.get('headword_diplomatic',''))})
  bt=set().union(*(de_tokens(a['german_gloss']) for a in base_articles));at=set().union(*(de_tokens(a['german_gloss']) for a in ameke_articles));inter=sorted(bt&at);union=bt|at
  out.append({'pair_id':f'RHD-AMEKE-BASE-{i:03d}','mechanical_base_key':x['mechanical_base'],'ameke_key':x['ameke_key'],'base_attestations':base_articles,'ameke_attestations':ameke_articles,'exact_german_token_overlap':inter,'german_token_jaccard':round(len(inter)/len(union),6) if union else 0.0,'status':'documentary_pair_only','semantic_judgment':'not_performed','morphological_judgment':'not_performed','human_reviewed':False})
 s={'dataset':'raramuri-historico-steffel-1809','layer':'ameke_exact_base_pair_contexts_v1','generated':'2026-08-13','pair_count':len(out),'pairs_with_any_exact_german_token_overlap':sum(bool(x['exact_german_token_overlap']) for x in out),'pairs_with_zero_exact_german_token_overlap':sum(not x['exact_german_token_overlap'] for x in out),'records':out,'human_reviewed':False,'semantic_judgment':'not_performed','morphological_judgment':'not_performed','interpretive_scope':'German gloss/context juxtaposition for exact X ~ X+ameke graphic pairs. Token overlap is descriptive only and is not semantic equivalence.'}
 dump(OUT/'ameke_exact_base_pair_contexts.json',s);dump(OUT/'ameke_exact_base_pair_contexts_summary.json',{k:v for k,v in s.items() if k!='records'});print(json.dumps({k:v for k,v in s.items() if k!='records'},ensure_ascii=False))
if __name__=='__main__':main()
