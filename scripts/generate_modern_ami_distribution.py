#!/usr/bin/env python3
"""Describe final -ami strings in the pinned contemporary Rarámuri Digital lexicon.

This is a documentary distribution layer. It does not assign a morpheme to
records merely because their normalized headword ends in `ami`. Modern
morphological interpretation remains grounded separately in published grammar.
"""
from pathlib import Path
from collections import Counter, defaultdict
import csv, json, re, unicodedata

ROOT=Path(__file__).resolve().parents[1]
MODERN=ROOT/'.tmp-raramuri-digital'/'data'/'lexicon-master.csv'
OUT=ROOT/'data'/'research'
PIN='156921f4edfe27d784edc1e6444867eaa368f2e5'

def norm(s):
    s=(s or '').replace('’',"'").replace('‘',"'").replace('ʼ',"'")
    s=unicodedata.normalize('NFKD',s)
    s=''.join(c for c in s if unicodedata.category(c)!='Mn').casefold()
    s=re.sub(r"[^a-z0-9' -]+",' ',s)
    return re.sub(r'\s+',' ',s).strip()

def dump(name,obj):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    rows=list(csv.DictReader(MODERN.open(encoding='utf-8-sig')))
    active=[r for r in rows if (r.get('status') or '').lower()!='rejected']
    for r in active:
        r['_key']=norm(r.get('headword_normalized') or r.get('headword'))
    all_keys=defaultdict(list)
    for r in active:
        if r['_key']: all_keys[r['_key']].append(r)

    ami=[]
    for r in active:
        key=r['_key']
        if not key.endswith('ami'): continue
        simple=bool(re.fullmatch(r"[a-z0-9']+",key))
        bare=(key=='ami')
        base=key[:-3] if len(key)>3 else ''
        exact_base=all_keys.get(base,[]) if base else []
        ami.append({
            'record_id':r['record_id'],'headword':r['headword'],'normalized_key':key,
            'classification':r.get('classification',''),'classification_family':r.get('classification_family',''),
            'translation_raw':r.get('translation_raw',''),'source_code':r.get('source_code',''),
            'source_document':r.get('source_document',''),'page_start':r.get('page_start',''),
            'simple_single_token':simple,'bare_ami_lexeme':bare,
            'mechanical_base_key':base,
            'exact_base_key_attested':bool(exact_base),
            'exact_base_record_ids':[x['record_id'] for x in exact_base],
            'exact_base_headwords':[x['headword'] for x in exact_base],
            'status':'documentary_final_ami_string',
            'automatic_morpheme_assignment':False,'human_reviewed':False
        })

    suffix_candidates=[x for x in ami if x['simple_single_token'] and not x['bare_ami_lexeme']]
    base_pairs=[x for x in suffix_candidates if x['exact_base_key_attested']]
    by_family=Counter(x['classification_family'] or '(blank)' for x in suffix_candidates)
    by_class=Counter(x['classification'] or '(blank)' for x in suffix_candidates)
    by_source=Counter(x['source_code'] or '(blank)' for x in suffix_candidates)

    # Preserve a few transparent, reproducible examples from each major family.
    examples={}
    for fam in ('Adj','Pp','S'):
        z=[x for x in suffix_candidates if x['classification_family']==fam]
        examples[fam]=z[:15]

    ros=[x for x in ami if x['record_id']=='RD-002179']
    summary={
        'dataset':'raramuri-historico-steffel-1809',
        'layer':'pinned_modern_raramuri_digital_final_ami_distribution_v1',
        'generated':'2026-08-13',
        'modern_repository':'fersandovalgtz/raramuri-digital','modern_commit':PIN,
        'modern_active_record_count':len(active),
        'final_ami_record_count':len(ami),
        'simple_nonbare_final_ami_candidate_count':len(suffix_candidates),
        'bare_ami_lexeme_count':sum(x['bare_ami_lexeme'] for x in ami),
        'exact_base_plus_ami_pair_count':len(base_pairs),
        'classification_family_counts':dict(by_family),
        'classification_counts':dict(by_class),
        'source_code_counts':dict(by_source),
        'rosacami_record':ros[0] if ros else None,
        'major_family_examples':examples,
        'human_reviewed':False,'automatic_morpheme_assignment':False,
        'automatic_historical_continuity_judgment':False,'cognacy_judgment':'not_performed',
        'interpretive_scope':'String-final -ami distribution in the pinned contemporary lexicon. Exact X~X+ami pairs are documentary graphic pairs only. Morphological interpretation must be established independently and source/variety heterogeneity must be retained.'
    }
    dump('modern_final_ami_distribution.json',{'dataset':summary['dataset'],'count':len(ami),'records':ami,'human_reviewed':False})
    dump('modern_final_ami_distribution_summary.json',summary)
    dump('modern_exact_base_ami_pairs.json',{'dataset':summary['dataset'],'count':len(base_pairs),'records':base_pairs,'human_reviewed':False,'automatic_morpheme_assignment':False})
    print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__': main()
