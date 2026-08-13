#!/usr/bin/env python3
import json,re,unicodedata
from collections import Counter
from pathlib import Path
P=Path('data/research')
def norm(s):
 s=unicodedata.normalize('NFKD',s or '')
 s=''.join(c for c in s if not unicodedata.combining(c))
 return s.replace('ſ','s').replace('ß','ss').casefold()
def words(s): return re.findall(r'[a-z]+',norm(s))
def candidates(s):
 out=[]
 for w in words(s):
  forms=[w]
  for suf in ('em','er','es','e'):
   if w.endswith(suf) and len(w)-len(suf)>=5: forms.append(w[:-len(suf)])
  for b in forms:
   if b.endswith('end') and len(b)>=6: out.append((w,'present-shaped'))
   if (b.startswith('ge') or b.startswith('unge')) and len(b)>=6 and (b.endswith('t') or b.endswith('en')): out.append((w,'past-shaped'))
   if b.startswith(('be','er','ver','zer')) and len(b)>=7 and b.endswith('t'): out.append((w,'past-shaped'))
 return out
def main():
 rows=json.loads((P/'ameke_local_function_contexts.json').read_text(encoding='utf-8'))['records']
 rows=[r for r in rows if r['source_layer']=='RAR-DE']
 audit=[]
 for r in rows:
  hits=candidates(r['local_german_label'])
  audit.append({'member_id':r['member_id'],'class':r['exclusive_suffix_class'],'token':r['analysis_token_key'],'gloss':r['local_german_label'],'v1':r.get('participle_surface_proxy',False),'inflected_surface_candidate':bool(hits),'hits':hits,'human_reviewed':False})
 summary={'dataset':'raramuri-historico-steffel-1809','count':len(audit),'by_class':dict(Counter(x['class'] for x in audit)),'v1_by_class':{c:sum(x['v1'] for x in audit if x['class']==c) for c in sorted(set(x['class'] for x in audit))},'inflected_candidate_by_class':{c:sum(x['inflected_surface_candidate'] for x in audit if x['class']==c) for c in sorted(set(x['class'] for x in audit))},'ugameke_records':[x for x in audit if x['class']=='ugameke'],'human_reviewed':False,'automatic_part_of_speech_tagging':False,'interpretive_scope':'Surface sensitivity audit only; candidate endings are not validated German POS tags.'}
 (P/'rar_de_participial_inflection_audit.json').write_text(json.dumps({'records':audit},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (P/'rar_de_participial_inflection_audit_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__': main()
