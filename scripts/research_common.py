#!/usr/bin/env python3
from pathlib import Path
import csv,re,unicodedata,json
ROOT=Path(__file__).resolve().parents[1]
ENTRIES=ROOT/'data/entries.csv'; OUT=ROOT/'data/research'
APOS=str.maketrans({'’':"'",'‘':"'",'ʼ':"'",'ʻ':"'",'`':"'",'´':"'"})
DASH=str.maketrans({'–':'-','—':'-','‑':'-','‐':'-','⸗':'-'})

def norm(v):
    v=(v or '').strip().translate(APOS).translate(DASH).replace('ſ','s').replace('ß','ss')
    v=unicodedata.normalize('NFKD',v)
    v=''.join(c for c in v if unicodedata.category(c)!='Mn').casefold()
    v=re.sub(r"[^0-9a-z' -]+",' ',v)
    v=re.sub(r'\s+',' ',v).strip(" .,:;!?()[]{}\"'-")
    return v

def alen(v): return len(re.sub(r'[^a-z0-9]','',norm(v)))
def split_components(v):
    parts=re.split(r'\s+(?:oder|item)\s+|[,;/]',(v or '').strip(),flags=re.I); out=[]; seen=set()
    for p in parts:
        p=re.sub(r'\s+',' ',p).strip().strip(' .,:;!?()[]{}\"')
        k=norm(p)
        if alen(p)>=2 and k and (p,k) not in seen: out.append(p); seen.add((p,k))
    return out

def rows(): return list(csv.DictReader(ENTRIES.open(encoding='utf-8')))
def active(r): return r.get('status')!='rejected_false_positive' and bool((r.get('article_diplomatic') or '').strip())
def gloss(article,form=''):
    t=re.sub(r'\s+',' ',(article or '').strip())
    if ',' in t: t=t.split(',',1)[1].strip()
    elif form and t.startswith(form): t=t[len(form):].lstrip(' ,.;:-')
    return re.split(r'[.;]',t,maxsplit=1)[0].strip()
def dump(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
