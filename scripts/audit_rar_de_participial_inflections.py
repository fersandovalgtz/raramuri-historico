#!/usr/bin/env python3
import json,re,unicodedata,random
from collections import Counter
from pathlib import Path
P=Path('data/research');SEED=1809;N=20000
SEP=('abge','ange','aufge','ausge','einge','festge','fortge','herge','hinge','losge','mitge','nachge','niederge','umge','unterge','vorge','wegge','weiterge','wiederge','zuge','zuruckge','zurückge')
INSEP=('be','er','ver','zer')
def norm(s):
 s=unicodedata.normalize('NFKD',s or '')
 s=''.join(c for c in s if not unicodedata.combining(c))
 return s.replace('ſ','s').replace('ß','ss').casefold()
def words(s): return re.findall(r'[a-z]+',norm(s))
def candidates(s):
 out=[]
 for w in words(s):
  forms=[(w,'bare')]
  for suf in ('em','er','es','e'):
   if w.endswith(suf) and len(w)-len(suf)>=5: forms.append((w[:-len(suf)],'inflected'))
  for b,route in forms:
   if b.endswith('end') and len(b)>=6: out.append((w,'present-shaped',b,route))
   strong=(b.startswith('ge') or b.startswith('unge') or any(b.startswith(p) for p in SEP))
   if strong and len(b)>=6 and (b.endswith('t') or b.endswith('en')): out.append((w,'past-shaped',b,route))
   if any(b.startswith(p) for p in INSEP) and len(b)>=7 and (b.endswith('t') or (route=='inflected' and b.endswith('en'))): out.append((w,'past-shaped',b,route))
 return out
def perm(audit):
 labels=[x['class'] for x in audit];ys=[x['inflected_surface_candidate'] for x in audit];target='ugameke'
 def calc(ls):
  tn=sum(c==target and y for c,y in zip(ls,ys));td=sum(c==target for c in ls);rn=sum(c!=target and y for c,y in zip(ls,ys));rd=len(ls)-td;tr=tn/td if td else 0;rr=rn/rd if rd else 0;return tn,td,rn,rd,tr,rr,tr-rr
 obs=calc(labels);rng=random.Random(SEED);p=list(labels);ext=0
 for _ in range(N):
  rng.shuffle(p)
  if abs(calc(p)[-1])+1e-12>=abs(obs[-1]):ext+=1
 tn,td,rn,rd,tr,rr,d=obs
 return {'target_numerator':tn,'target_denominator':td,'rest_numerator':rn,'rest_denominator':rd,'target_rate':round(tr,6),'rest_rate':round(rr,6),'rate_difference':round(d,6),'empirical_two_sided_p':round((ext+1)/(N+1),6)}
def main():
 rows=json.loads((P/'ameke_local_function_contexts.json').read_text(encoding='utf-8'))['records']
 rows=[r for r in rows if r['source_layer']=='RAR-DE']
 audit=[]
 for r in rows:
  hits=candidates(r['local_german_label'])
  audit.append({'member_id':r['member_id'],'class':r['exclusive_suffix_class'],'token':r['analysis_token_key'],'gloss':r['local_german_label'],'v1':r.get('participle_surface_proxy',False),'inflected_surface_candidate':bool(hits),'hits':hits,'human_reviewed':False})
 cs=sorted(set(x['class'] for x in audit))
 summary={'dataset':'raramuri-historico-steffel-1809','count':len(audit),'by_class':dict(Counter(x['class'] for x in audit)),'v1_by_class':{c:sum(x['v1'] for x in audit if x['class']==c) for c in cs},'inflected_candidate_by_class':{c:sum(x['inflected_surface_candidate'] for x in audit if x['class']==c) for c in cs},'ugameke_vs_rest_permutation':perm(audit),'random_seed':SEED,'permutation_iterations':N,'ugameke_records':[x for x in audit if x['class']=='ugameke'],'human_reviewed':False,'automatic_part_of_speech_tagging':False,'interpretive_scope':'Surface sensitivity audit only; candidate endings are not validated German POS tags.'}
 (P/'rar_de_participial_inflection_audit.json').write_text(json.dumps({'records':audit},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (P/'rar_de_participial_inflection_audit_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__': main()
