#!/usr/bin/env python3
from collections import Counter,defaultdict
import json,random,re,unicodedata
from pathlib import Path
OUT=Path('data/research');SEED=1809;N=20000
CLASSES=('ameke_other','gameke','iameke','ugameke','jameke')
SEP=('abge','ange','aufge','ausge','einge','festge','fortge','herge','hinge','losge','mitge','nachge','niederge','umge','unterge','vorge','wegge','weiterge','wiederge','zuge','zuruckge','zurückge')
INSEP=('be','emp','ent','er','miss','ver','zer')
def load(n):return json.loads((OUT/n).read_text(encoding='utf-8'))
def norm(s):
 s=unicodedata.normalize('NFKD',s or '');s=''.join(c for c in s if not unicodedata.combining(c));return re.sub(r'\s+',' ',s.replace('ſ','s').replace('ß','ss').casefold()).strip(' ,;:.!?-')
def word(s):
 w=re.findall(r'[a-z]+',norm(s));return w[0] if len(w)==1 else ''
def infstem(w):
 if w.endswith('en') and len(w)>=5:return w[:-2]
 if w.endswith('n') and len(w)>=5:return w[:-1]
 return ''
def pstem(w,present=False):
 x=w
 if present and x.endswith('end') and len(x)>=6:return x[:-3]
 for p in SEP:
  if x.startswith(p):x=x[len(p):];break
 else:
  if x.startswith('unge') and len(x)>7:x=x[4:]
  elif x.startswith('ge') and len(x)>5:x=x[2:]
  else:
   for p in INSEP:
    if x.startswith(p) and len(x)>len(p)+3:x=x[len(p):];break
 if x.endswith('et') and len(x)>4:x=x[:-2]
 elif x.endswith('t') and len(x)>3:x=x[:-1]
 elif x.endswith('en') and len(x)>4:x=x[:-2]
 return x
def lev(a,b):
 prev=list(range(len(b)+1))
 for i,ca in enumerate(a,1):
  cur=[i]
  for j,cb in enumerate(b,1):cur.append(min(cur[-1]+1,prev[j]+1,prev[j-1]+(ca!=cb)))
  prev=cur
 return prev[-1]
def sim(a,b):return 0 if not a or not b else 1-lev(a,b)/max(len(a),len(b))
def relation(x):
 h=word(x.get('article_headword',''));l=word(x.get('local_german_label',''));p=x.get('functional_proxy','')
 if not h or not l:return 'multiword_or_ambiguous',0
 if h==l:return 'same_as_article_headword',1
 hs=infstem(h)
 if p=='past_participle_surface_proxy' and hs:
  z=sim(hs,pstem(l));return ('past_participle_subentry_family_candidate' if z>=.60 else 'past_participle_subentry_unmatched'),z
 if p=='present_participle_surface_proxy' and hs:
  z=sim(hs,pstem(l,True));return ('present_participle_subentry_family_candidate' if z>=.60 else 'present_participle_subentry_unmatched'),z
 if p=='property_surface_proxy':return 'property_local_subentry',0
 return 'other_local_subentry',0
def collapse(rows):
 g=defaultdict(list)
 for r in rows:g[(r['record_id'],r['exclusive_suffix_class'])].append(r)
 pr=['past_participle_subentry_family_candidate','present_participle_subentry_family_candidate','past_participle_subentry_unmatched','present_participle_subentry_unmatched','property_local_subentry','same_as_article_headword','other_local_subentry','multiword_or_ambiguous'];rank={x:i for i,x in enumerate(pr)}
 return [dict(min(v,key=lambda x:rank.get(x['microstructure_relation'],99)),record_class_context_count=len(v)) for k,v in sorted(g.items())]
def test(rows,outcome):
 labels=[r['exclusive_suffix_class'] for r in rows];ys=[r['microstructure_relation']==outcome for r in rows];target='ugameke'
 def d(labs):
  tn=sum(c==target and y for c,y in zip(labs,ys));td=sum(c==target for c in labs);rn=sum(c!=target and y for c,y in zip(labs,ys));rd=len(labs)-td;tr=tn/td if td else 0;rr=rn/rd if rd else 0;return tn,td,rn,rd,tr,rr,tr-rr
 obs=d(labels);rng=random.Random(SEED);p=list(labels);ext=0
 for _ in range(N):
  rng.shuffle(p)
  if abs(d(p)[-1])+1e-12>=abs(obs[-1]):ext+=1
 tn,td,rn,rd,tr,rr,delta=obs
 return {'outcome':outcome,'target_numerator':tn,'target_denominator':td,'rest_numerator':rn,'rest_denominator':rd,'target_rate':round(tr,6),'rest_rate':round(rr,6),'rate_difference':round(delta,6),'empirical_two_sided_p':round((ext+1)/(N+1),6),'human_reviewed':False}
def main():
 src=load('ameke_local_function_contexts.json')['records'];rows=[]
 for x in src:
  if x.get('source_layer')!='DE-RAR-local-proposal' or x.get('alignment_risk')!='low':continue
  rel,s=relation(x);y=dict(x);y['article_headword_shape']='infinitive_surface_proxy' if infstem(word(x.get('article_headword',''))) else 'other_or_ambiguous';y['microstructure_relation']=rel;y['headword_local_family_similarity']=round(s,6);y['human_reviewed']=False;rows.append(y)
 cells=collapse(rows);cnt=Counter(r['record_id'] for r in cells);single=[r for r in cells if cnt[r['record_id']]==1];inf=[r for r in cells if r['article_headword_shape']=='infinitive_surface_proxy'];inf_single=[r for r in single if r['article_headword_shape']=='infinitive_surface_proxy']
 analyses={}
 for name,sub in [('record_class_cells',cells),('single_class_articles',single),('infinitive_headword_record_class_cells',inf),('infinitive_headword_single_class_articles',inf_single)]:
  analyses[name]={'observation_count':len(sub),'counts_by_class':dict(Counter(r['exclusive_suffix_class'] for r in sub)),'microstructure_relation_counts':dict(Counter(r['microstructure_relation'] for r in sub)),'relation_counts_by_class':{c:dict(Counter(r['microstructure_relation'] for r in sub if r['exclusive_suffix_class']==c)) for c in CLASSES},'tests':[test(sub,o) for o in ('past_participle_subentry_family_candidate','present_participle_subentry_family_candidate')] if sub else []}
 summary={'dataset':'raramuri-historico-steffel-1809','layer':'ameke_de_rar_microstructure_v1','generated':'2026-08-13','low_risk_context_count':len(rows),'unique_record_class_cell_count':len(cells),'single_class_article_count':len(single),'infinitive_headword_cell_count':len(inf),'random_seed':SEED,'permutation_iterations':N,'analyses':analyses,'human_reviewed':False,'automatic_part_of_speech_tagging':False,'automatic_morphological_analysis':False,'interpretive_scope':'Documentary DE-RAR article-headword to local-label surface microstructure; family candidates are conservative string relationships, not grammatical analysis.'}
 (OUT/'ameke_de_rar_microstructure.json').write_text(json.dumps({'dataset':summary['dataset'],'count':len(rows),'human_reviewed':False,'records':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(OUT/'ameke_de_rar_microstructure_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
