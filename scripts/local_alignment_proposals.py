#!/usr/bin/env python3
import json,re
from collections import Counter
from research_common import OUT,rows,active,norm,split_components,dump

def clean(s): return re.sub(r'\s+',' ',s or '').strip(' ,;:.!?-')
def main():
    src=json.load((OUT/'ameke_local_context_candidates.json').open(encoding='utf-8'))['records']
    corr={x['alignment_id']:x for x in json.load((OUT/'ameke_facsimile_occurrence_corrections.json').open(encoding='utf-8'))['records']}
    rar=set()
    for r in rows():
        if active(r) and r.get('direction')=='RAR-DE':rar.update(norm(x) for x in split_components(r.get('headword_diplomatic','')))
    out=[]
    for x in src:
        c=corr.get(x['alignment_id'])
        if c:label=c['local_german_label'];method='facsimile_correction';surface=c['facsimile_reading'];risk='low'
        else:
            label='';method=''
            for key in ('same_minor_left','same_major_left','previous_major_clause'):
                q=clean(x.get(key,''));q=q.split(',')[0].strip()
                if q and len(q)<=50 and norm(q) not in rar:label=q;method=key;break
            if not label:label=x['article_headword'];method='article_headword_fallback'
            surface=x['surface_form'];risk='low' if method in {'same_minor_left','same_major_left'} else 'high'
        out.append({'alignment_id':x['alignment_id'],'member_id':x['member_id'],'record_id':x['record_id'],'printed_page':x['printed_page'],'article_headword':x['article_headword'],'analysis_surface':surface,'proposed_local_german_label':label,'proposal_method':method,'proposal_review_risk':risk,'human_reviewed':False})
    mc=Counter(x['proposal_method'] for x in out);rc=Counter(x['proposal_review_risk'] for x in out)
    s={'dataset':'raramuri-historico-steffel-1809','generated':'2026-08-13','count':len(out),'method_counts':dict(sorted(mc.items())),'review_risk_counts':dict(sorted(rc.items())),'facsimile_correction_count':mc.get('facsimile_correction',0),'human_reviewed_count':0}
    dump(OUT/'ameke_local_context_ai_proposals.json',{'dataset':s['dataset'],'count':len(out),'human_reviewed':False,'records':out});dump(OUT/'ameke_local_context_ai_proposals_summary.json',s)
    print(json.dumps(s,ensure_ascii=False))
if __name__=='__main__':main()
