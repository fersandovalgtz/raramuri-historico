#!/usr/bin/env python3
import json,re,unicodedata
from pathlib import Path
OUT=Path('data/research')
def norm(s):
 s=unicodedata.normalize('NFKD',s or '');s=''.join(c for c in s if not unicodedata.combining(c));return re.sub(r'[^a-z0-9]+','',s.replace('ſ','s').replace('ß','ss').casefold())
def lev(a,b):
 prev=list(range(len(b)+1))
 for i,ca in enumerate(a,1):
  cur=[i]
  for j,cb in enumerate(b,1):cur.append(min(cur[-1]+1,prev[j]+1,prev[j-1]+(ca!=cb)))
  prev=cur
 return prev[-1]
def sim(a,b):return 0 if not a or not b else 1-lev(a,b)/max(len(a),len(b))
TARGETS=[
 {'id':'RHD-EXT-0001','queries':['pagotugameke'],'modern':['pakótami','pagótami'],'gloss':'good person (baptized); good people/people','analysis':'Caballero 2008 identifies pakótami as a participle','source':'Caballero 2008','priority':'A'},
 {'id':'RHD-EXT-0002','queries':['stacameke','tsestaracameke'],'modern':['sitákame'],'gloss':'red thing(s)','analysis':'Caballero 2008 documents sitákame within the participial -ame system','source':'Caballero 2008','priority':'A'},
 {'id':'RHD-EXT-0003','queries':['tsehecemeke','tsehocameke'],'modern':['chókami'],'gloss':'black-PTCP','analysis':'Islas Flores describes -(k)ame/-ame as participial in adjectival derivation','source':'Islas Flores 2017/2018','priority':'B'}]
def main():
 ms=json.loads((OUT/'ameke_constellation_members.json').read_text(encoding='utf-8'))['records'];rows=[]
 for t in TARGETS:
  scored=[]
  for m in ms:
   k=norm(m.get('graphic_key',''));q=max(sim(k,norm(x)) for x in t['queries']);scored.append((q,m))
  score,m=max(scored,key=lambda x:x[0]);modern_sim=max(sim(norm(m.get('graphic_key','')),norm(x)) for x in t['modern'])
  rows.append({'external_id':t['id'],'priority':t['priority'],'historical_query_forms':t['queries'],'matched_member_id':m['member_id'],'historical_graphic_key':m.get('graphic_key'),'historical_surface_forms':m.get('surface_forms',[]),'historical_german_contexts':m.get('german_contexts',[]),'historical_query_similarity':round(score,6),'modern_published_forms':t['modern'],'modern_published_gloss':t['gloss'],'modern_published_analysis':t['analysis'],'external_source':t['source'],'full_string_similarity_to_best_modern_form':round(modern_sim,6),'relation_status':'external_form_semantic_parallel_candidate','historical_continuity_judgment':'not_performed','cognacy_judgment':'not_performed','automatic_morphological_analysis':False,'human_reviewed':False})
 s={'dataset':'raramuri-historico-steffel-1809','layer':'external_literature_comparison_candidates_v1','generated':'2026-08-13','count':len(rows),'human_reviewed':False,'automatic_morphological_analysis':False,'historical_continuity_judgment':'not_performed','cognacy_judgment':'not_performed'}
 (OUT/'external_literature_comparison_candidates.json').write_text(json.dumps({'dataset':s['dataset'],'count':len(rows),'records':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(OUT/'external_literature_comparison_candidates_summary.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'summary':s,'records':rows},ensure_ascii=False))
if __name__=='__main__':main()
