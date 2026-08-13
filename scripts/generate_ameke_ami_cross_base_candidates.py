#!/usr/bin/env python3
"""Cross historical exact X~X+ameke pairs with modern exact X~X+ami pairs.

Ranking is graphic only. German/Spanish glosses are carried for later human or
philological assessment but do not affect the score. No cognacy, continuity or
semantic equivalence is assigned automatically.
"""
from pathlib import Path
import json,csv,re,unicodedata

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'research'
MODERN=ROOT/'.tmp-raramuri-digital'/'data'/'lexicon-master.csv'
PIN='156921f4edfe27d784edc1e6444867eaa368f2e5'

def norm(s):
 s=(s or '').replace('ſ','s').replace('ß','ss').replace('’',"'").replace('‘',"'")
 s=unicodedata.normalize('NFKD',s);s=''.join(c for c in s if unicodedata.category(c)!='Mn').casefold()
 return re.sub(r'[^a-z0-9]+','',s)

def lev(a,b):
 if len(a)<len(b):a,b=b,a
 prev=list(range(len(b)+1))
 for i,x in enumerate(a,1):
  cur=[i]
  for j,y in enumerate(b,1):cur.append(min(cur[-1]+1,prev[j]+1,prev[j-1]+(x!=y)))
  prev=cur
 return prev[-1]

def sim(a,b):return 1-lev(a,b)/max(len(a),len(b),1)
def dump(n,o):(OUT/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
 hist=json.loads((OUT/'ameke_exact_base_pair_contexts.json').read_text(encoding='utf-8'))['records']
 mpairs=json.loads((OUT/'modern_exact_base_ami_pairs.json').read_text(encoding='utf-8'))['records']
 modern=list(csv.DictReader(MODERN.open(encoding='utf-8-sig'))); byid={r['record_id']:r for r in modern}
 cand=[]
 for h in hist:
  hb=norm(h['mechanical_base_key'])
  ranked=[]
  for m in mpairs:
   mb=norm(m['mechanical_base_key'])
   if not hb or not mb or hb[0]!=mb[0]:continue
   s=sim(hb,mb)
   if s<0.5:continue
   bases=[byid[x] for x in m.get('exact_base_record_ids',[]) if x in byid]
   ranked.append((s,mb,m,bases))
  ranked.sort(key=lambda z:(-z[0],z[1],z[2]['record_id']))
  for rank,(s,mb,m,bases) in enumerate(ranked[:5],1):
   cand.append({
    'historical_pair_id':h['pair_id'],'historical_base_key':h['mechanical_base_key'],'historical_ameke_key':h['ameke_key'],
    'historical_base_glosses':[x['german_gloss'] for x in h['base_attestations']],
    'historical_ameke_glosses':[x['german_gloss'] for x in h['ameke_attestations']],
    'modern_target_record_id':m['record_id'],'modern_base_key':m['mechanical_base_key'],'modern_ami_headword':m['headword'],
    'modern_ami_classification_family':m['classification_family'],'modern_ami_translation':m['translation_raw'],
    'modern_base_records':[{'record_id':b['record_id'],'headword':b['headword'],'classification_family':b['classification_family'],'translation_raw':b['translation_raw']} for b in bases],
    'base_graphic_similarity':round(s,6),'rank_within_historical_base':rank,
    'relation_status':'graphic_cross_corpus_candidate','semantic_equivalence_judgment':'not_performed',
    'cognacy_judgment':'not_performed','historical_continuity_judgment':'not_performed','human_reviewed':False
   })
 high=[x for x in cand if x['base_graphic_similarity']>=0.75]
 summary={'dataset':'raramuri-historico-steffel-1809','layer':'historical_ameke_modern_ami_exact_base_crosswalk_v1','generated':'2026-08-13','modern_commit':PIN,'historical_exact_pair_count':len(hist),'modern_exact_base_ami_pair_count':len(mpairs),'candidate_count':len(cand),'high_graphic_similarity_candidate_count':len(high),'high_graphic_similarity_candidates':high,'ranking_method':'normalized Levenshtein similarity on base strings only; same initial character; similarity >=0.50; top five per historical base','semantic_equivalence_judgment':'not_performed','cognacy_judgment':'not_performed','historical_continuity_judgment':'not_performed','human_reviewed':False}
 dump('ameke_ami_cross_base_candidates.json',{'dataset':summary['dataset'],'count':len(cand),'records':cand,'human_reviewed':False});dump('ameke_ami_cross_base_candidates_summary.json',summary);print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
