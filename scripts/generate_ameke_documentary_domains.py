#!/usr/bin/env python3
"""German documentary-gloss domain proxies for the historical -ameke constellation.

Only German documentary context is classified. No Rarámuri semantic class,
morpheme, POS, or historical function is assigned. Direct RAR-DE glosses are
re-parsed from data/entries.csv; DE-RAR contexts retain local-alignment risk.
"""
from collections import Counter,defaultdict
import csv,json,random,re
from research_common import OUT,rows,active,norm,gloss,dump
SEED=1809;ITERATIONS=20000
CLASSES=('ameke_other','gameke','iameke','ugameke','jameke')
TEST_DOMAINS=('color_property_proxy','physical_property_proxy','human_person_agent_proxy','state_condition_proxy','process_result_surface_proxy')
COLOR={'rot','roth','schwarz','weiss','weis','gelb','grun','blau','grau','braun','purpur','violett','grunlich','rotlich','schwarzlich','weisslich'}
PHYSICAL={'gross','gros','klein','dick','dunn','kalt','heiss','heis','hart','weich','rund','krumm','lang','kurz','scharf','stumpf','breit','schmal','hoch','niedrig','tief','schwer','leicht','trocken','nass','wasserig','glatt','rauh','rauhig','fleischig','holzern','frostig','fest','locker','hell','dunkel'}
STATE={'krank','blind','schwanger','faul','tot','todt','lebendig','hungrig','durstig','mude','ermudet','bewusst','unbewusst','gelehrt','klug','zornig','furchtsam','heilend','allwissend','verstorben','verungluckt','kraftlos','arm','bose'}
PERSON={'getaufter','getaufte','getauften','rufende','rufender','erschaffer','ehemann','eheweib','gemahl','mann','weib','person','mensch','kind','vater','mutter','tochter','sohn','widder'}
PART={'past_participle_surface_proxy','present_participle_surface_proxy'}
def load(n):return json.loads((OUT/n).read_text(encoding='utf-8'))
def toks(s):return re.findall(r'[a-z]+',norm(s))
def hasstem(ts,lex):
 for t in ts:
  if t in lex:return True
  for suf in ('e','en','er','es','em'):
   if t.endswith(suf) and len(t)-len(suf)>=3 and t[:-len(suf)] in lex:return True
 return False
def domains(label,fp=''):
 ts=toks(label);text=' '.join(ts);z=[]
 if hasstem(ts,COLOR):z.append('color_property_proxy')
 if hasstem(ts,PHYSICAL):z.append('physical_property_proxy')
 if hasstem(ts,STATE):z.append('state_condition_proxy')
 if hasstem(ts,PERSON) or bool(re.match(r'^(ein|eine|einen|einem|einer)\s+[a-z]+(?:er|e|en)?$',text)):z.append('human_person_agent_proxy')
 if fp in PART:z.append('process_result_surface_proxy')
 return z or ['other_or_unclassified']
def bh(ps):
 m=len(ps);order=sorted(range(m),key=lambda i:ps[i]);q=[1.]*m;run=1.
 for r0 in range(m-1,-1,-1):
  i=order[r0];run=min(run,ps[i]*m/(r0+1));q[i]=min(1.,run)
 return q
def permutation_tests(records,name):
 g=defaultdict(list)
 for r in records:g[(r['exclusive_suffix_class'],r['analysis_token_key'])].append(r)
 units=[]
 for (c,k),items in sorted(g.items()):
  ds=set()
  for x in items:ds.update(x['german_documentary_domain_proxies'])
  units.append((c,k,ds))
 labels=[u[0] for u in units];vectors=[u[2] for u in units];n=len(units)
 class_n=Counter(labels);domain_n=Counter(d for v in vectors for d in v if d in TEST_DOMAINS)
 obs=[]
 for c in CLASSES:
  for d in TEST_DOMAINS:
   tn=sum(1 for lab,v in zip(labels,vectors) if lab==c and d in v);td=class_n[c];rn=domain_n[d]-tn;rd=n-td;tr=tn/td if td else 0.;rr=rn/rd if rd else 0.;obs.append((c,d,tn,td,rn,rd,tr,rr,tr-rr))
 rng=random.Random(SEED);perm=list(labels);raw=[0]*len(obs);mx=[0]*len(obs);eps=1e-12
 for _ in range(ITERATIONS):
  rng.shuffle(perm);hit={c:Counter() for c in CLASSES}
  for c,v in zip(perm,vectors):
   for d in v:
    if d in TEST_DOMAINS:hit[c][d]+=1
  vals=[]
  for c,d,tn,td,rn,rd,tr,rr,od in obs:
   ptn=hit[c][d];prn=domain_n[d]-ptn;vals.append((ptn/td if td else 0.)-(prn/rd if rd else 0.))
  maxabs=max((abs(v) for v in vals),default=0.)
  for i,v in enumerate(vals):
   if abs(v)+eps>=abs(obs[i][-1]):raw[i]+=1
   if maxabs+eps>=abs(obs[i][-1]):mx[i]+=1
 ps=[(x+1)/(ITERATIONS+1) for x in raw];qs=bh(ps);fw=[(x+1)/(ITERATIONS+1) for x in mx];tests=[]
 for i,(c,d,tn,td,rn,rd,tr,rr,delta) in enumerate(obs):
  tests.append({'analysis':name,'exclusive_suffix_class':c,'german_documentary_domain_proxy':d,'target_numerator':tn,'target_denominator':td,'rest_numerator':rn,'rest_denominator':rd,'target_rate':round(tr,6),'rest_rate':round(rr,6),'rate_difference':round(delta,6),'empirical_two_sided_p':round(ps[i],6),'bh_fdr_q':round(qs[i],6),'max_abs_rate_difference_fwer_p':round(fw[i],6),'conservative_signal':bool(qs[i]<=.05 and fw[i]<=.05 and abs(delta)>=.10 and td>=8 and tn>=3),'human_reviewed':False,'automatic_semantic_classification':False,'automatic_morphological_analysis':False})
 tests.sort(key=lambda x:(not x['conservative_signal'],x['max_abs_rate_difference_fwer_p'],x['bh_fdr_q'],-abs(x['rate_difference'])))
 return units,tests
def main():
 members=load('ameke_constellation_members.json')['records'];token=load('ameke_token_aware_members.json')['records'];tby={x['member_id']:x for x in token};entry={r.get('record_id'):r for r in rows() if active(r)};contexts=load('ameke_local_function_contexts.json')['records'];records=[];seen=set()
 for m in members:
  if 'RAR-DE' not in (m.get('source_layers') or []) or m['member_id'] not in tby:continue
  t=tby[m['member_id']]
  for rid in m.get('rar_de_record_ids') or []:
   r=entry.get(rid)
   if not r:continue
   gg=gloss(r.get('article_diplomatic',''),r.get('headword_diplomatic',''));tier='source_verified_rar_de_article_gloss' if gg else 'source_article_unparsed';fp=''
   for x in contexts:
    if x.get('source_layer')=='RAR-DE' and x.get('member_id')==m['member_id'] and norm(x.get('local_german_label',''))==norm(gg):fp=x.get('functional_proxy','');break
   key=(m['member_id'],rid,norm(gg),'RAR-DE')
   if key in seen:continue
   seen.add(key);records.append({'member_id':m['member_id'],'record_id':rid,'exclusive_suffix_class':t['exclusive_suffix_class'],'analysis_token_key':t['analysis_token_key'],'source_direction':'RAR-DE','source_provenance':'direct_historical_entry','gloss_evidence_tier':tier,'source_verified_german_gloss':gg,'machine_parsed_german_context':'','german_context_for_analysis':gg,'functional_surface_proxy':fp,'german_documentary_domain_proxies':domains(gg,fp),'human_reviewed':False,'automatic_semantic_classification':False,'automatic_morphological_analysis':False})
 for x in contexts:
  if x.get('source_layer')!='DE-RAR-local-proposal':continue
  label=x.get('local_german_label','');tier='machine_local_de_rar_low_risk' if x.get('alignment_risk')=='low' else 'machine_local_de_rar_high_risk';key=(x['member_id'],x.get('record_id',''),norm(label),'DE-RAR')
  if key in seen:continue
  seen.add(key);records.append({'member_id':x['member_id'],'record_id':x.get('record_id',''),'exclusive_suffix_class':x['exclusive_suffix_class'],'analysis_token_key':x['analysis_token_key'],'source_direction':'DE-RAR','source_provenance':'local_alignment_proposal','gloss_evidence_tier':tier,'source_verified_german_gloss':'','machine_parsed_german_context':label,'german_context_for_analysis':label,'functional_surface_proxy':x.get('functional_proxy',''),'german_documentary_domain_proxies':domains(label,x.get('functional_proxy','')),'human_reviewed':False,'automatic_semantic_classification':False,'automatic_morphological_analysis':False})
 subsets={'all_documentary':records,'conservative_documentary':[r for r in records if r['gloss_evidence_tier'] in {'source_verified_rar_de_article_gloss','machine_local_de_rar_low_risk'}],'direct_rar_de_only':[r for r in records if r['source_direction']=='RAR-DE'],'de_rar_low_risk_only':[r for r in records if r['gloss_evidence_tier']=='machine_local_de_rar_low_risk']};analyses={};all_tests=[]
 for name,sub in subsets.items():
  units,tests=permutation_tests(sub,name);all_tests.extend(tests);analyses[name]={'context_count':len(sub),'token_unit_count':len(units),'contexts_by_class':dict(Counter(r['exclusive_suffix_class'] for r in sub)),'domain_proxy_counts':dict(Counter(d for r in sub for d in r['german_documentary_domain_proxies'])),'domain_proxy_counts_by_class':{c:dict(Counter(d for r in sub if r['exclusive_suffix_class']==c for d in r['german_documentary_domain_proxies'])) for c in CLASSES},'conservative_signal_count':sum(t['conservative_signal'] for t in tests),'conservative_signals':[t for t in tests if t['conservative_signal']]}
 summary={'dataset':'raramuri-historico-steffel-1809','layer':'ameke_german_documentary_domain_proxies_v1','generated':'2026-08-13','context_count':len(records),'source_verified_rar_de_count':sum(r['gloss_evidence_tier']=='source_verified_rar_de_article_gloss' for r in records),'de_rar_low_risk_count':sum(r['gloss_evidence_tier']=='machine_local_de_rar_low_risk' for r in records),'de_rar_high_risk_count':sum(r['gloss_evidence_tier']=='machine_local_de_rar_high_risk' for r in records),'random_seed':SEED,'permutation_iterations':ITERATIONS,'analyses':analyses,'human_reviewed':False,'automatic_semantic_classification':False,'automatic_morphological_analysis':False,'interpretive_scope':'Transparent rule-based domains assigned only to German documentary gloss/context strings. They are not Rarámuri semantic classes and do not establish historical morphology or grammatical function.'}
 dump(OUT/'ameke_documentary_domain_proxies.json',{'dataset':summary['dataset'],'count':len(records),'human_reviewed':False,'automatic_semantic_classification':False,'records':records});dump(OUT/'ameke_documentary_domain_proxies_summary.json',summary);dump(OUT/'ameke_documentary_domain_permutation_tests.json',{'dataset':summary['dataset'],'count':len(all_tests),'human_reviewed':False,'records':all_tests})
 with (OUT/'ameke_documentary_domain_proxies.csv').open('w',encoding='utf-8',newline='') as f:
  fields=['member_id','record_id','exclusive_suffix_class','analysis_token_key','source_direction','gloss_evidence_tier','source_verified_german_gloss','machine_parsed_german_context','german_context_for_analysis','functional_surface_proxy','german_documentary_domain_proxies','human_reviewed'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for r in records:w.writerow({**{k:r.get(k,'') for k in fields},'german_documentary_domain_proxies':' | '.join(r['german_documentary_domain_proxies'])})
 print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
