#!/usr/bin/env python3
import csv,json,re
from research_common import OUT,rows,active,dump

def clean(s): return re.sub(r'\s+',' ',s or '').strip(' ,;:.!?-')
def local(article,surface):
    p=article.find(surface)
    if p<0:p=article.casefold().find(surface.casefold())
    if p<0:return None
    left=article[:p]; major=re.split(r'[.!?:]',left); same=clean(major[-1]); prev=clean(major[-2] if len(major)>1 else '')
    minor=[clean(x) for x in re.split(r'[,;]',major[-1]) if clean(x)]
    return {'same_major_left':same,'same_minor_left':minor[-1] if minor else same,'previous_major_clause':prev,'left_window':clean(article[max(0,p-160):p]),'right_window':clean(article[p:p+100])}
def main():
    entries={r.get('record_id'):r for r in rows() if active(r) and r.get('direction')=='DE-RAR'}
    recs={x['recovery_id']:x for x in json.load((OUT/'de_rar_residual_recovery_queue.json').open(encoding='utf-8'))['records']}
    members=json.load((OUT/'ameke_constellation_members.json').open(encoding='utf-8'))['records'];out=[]
    for m in members:
        if 'DE-RAR-residual-recovery' not in set(m.get('source_layers') or []):continue
        for rid in m.get('recovery_ids') or []:
            for eid in recs.get(rid,{}).get('de_rar_record_ids',[]):
                e=entries.get(eid,{}); article=e.get('article_diplomatic','')
                for surface in m.get('surface_forms') or []:
                    x=local(article,surface)
                    if not x:continue
                    out.append({'alignment_id':'','member_id':m['member_id'],'recovery_id':rid,'record_id':eid,'article_headword':e.get('headword_diplomatic',''),'surface_form':surface,'printed_page':int(e.get('printed_page') or 0),**x,'ai_reviewed':False,'ai_local_label':'','human_reviewed':False})
    out.sort(key=lambda x:(x['printed_page'],x['article_headword'],x['member_id']))
    for i,x in enumerate(out,1):x['alignment_id']=f'RHD-AMEKE-LCTX-{i:04d}'
    s={'dataset':'raramuri-historico-steffel-1809','generated':'2026-08-13','count':len(out),'member_count':len({x['member_id'] for x in out}),'record_count':len({x['record_id'] for x in out}),'article_headword_is_not_assumed_local_gloss':True,'human_reviewed_count':0}
    dump(OUT/'ameke_local_context_candidates.json',{'dataset':s['dataset'],'count':len(out),'human_reviewed':False,'records':out});dump(OUT/'ameke_local_context_candidates_summary.json',s)
    with (OUT/'ameke_local_context_candidates.csv').open('w',encoding='utf-8',newline='') as f:
        fields=list(out[0].keys()) if out else [];w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(out)
    print(json.dumps(s,ensure_ascii=False))
if __name__=='__main__':main()
