#!/usr/bin/env python3
"""Documentary string test for possible final -ke segmentation in historical -ameke forms.
No morpheme boundary, function, cognacy, or continuity is inferred.
"""
import json
from research_common import OUT,rows,active,norm,split_components,dump

def main():
 forms=[]
 for r in rows():
  if active(r) and r.get('direction')=='RAR-DE':
   for s in split_components(r.get('headword_diplomatic','')):
    k=norm(s)
    if k:forms.append({'record_id':r.get('record_id',''),'surface':s,'key':k,'page':r.get('printed_page','')})
 by={}
 for x in forms:by.setdefault(x['key'],[]).append(x)
 keys=set(by);ameke=sorted(k for k in keys if k.endswith('ameke') and len(k)>5);records=[]
 for k in ameke:
  base=k[:-5];xame=base+'ame'
  records.append({'ameke_key':k,'mechanical_base':base,'xame_key':xame,'xame_attested':xame in keys,'xame_attestations':by.get(xame,[]),'bare_base_attested':base in keys,'bare_base_attestations':by.get(base,[]),'ameke_attestations':by[k],'status':'documentary_string_test_only','human_reviewed':False,'automatic_morpheme_segmentation':False,'historical_continuity_judgment':'not_performed'})
 final_ke=sorted(k for k in keys if k.endswith('ke'));other_ke=[k for k in final_ke if not k.endswith('ameke')];final_ame=sorted(k for k in keys if k.endswith('ame'))
 s={'dataset':'raramuri-historico-steffel-1809','layer':'ameke_final_ke_documentary_test_v1','generated':'2026-08-13','unique_rar_de_graphic_keys':len(keys),'ameke_key_count':len(ameke),'final_ke_key_count':len(final_ke),'final_ke_outside_ameke_key_count':len(other_ke),'final_ame_key_count':len(final_ame),'ameke_with_exact_xame_counterpart_count':sum(x['xame_attested'] for x in records),'ameke_with_exact_bare_base_counterpart_count':sum(x['bare_base_attested'] for x in records),'xame_counterpart_examples':[x for x in records if x['xame_attested']][:25],'bare_base_counterpart_examples':[x for x in records if x['bare_base_attested']][:25],'final_ke_outside_ameke_examples':other_ke[:50],'final_ame_examples':final_ame[:50],'human_reviewed':False,'automatic_morpheme_segmentation':False,'automatic_morphological_analysis':False,'interpretive_scope':'Exact historical string-distribution evidence only. Matches may motivate review but do not establish segmentation as -ame+-ke.'}
 dump(OUT/'ameke_ke_segmentation_evidence.json',{'dataset':s['dataset'],'count':len(records),'human_reviewed':False,'records':records});dump(OUT/'ameke_ke_segmentation_evidence_summary.json',s);print(json.dumps(s,ensure_ascii=False))
if __name__=='__main__':main()
