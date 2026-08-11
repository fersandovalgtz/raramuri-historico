#!/usr/bin/env python3
"""Machine-segment the complete lexicographic portions of Steffel 1791/1809.

This is a coverage-first extraction. It deliberately prefers false-positive article
boundaries over silently omitting a possible entry. Every candidate is explicitly
marked as unverified until collated against the facsimile.
"""
from __future__ import annotations
from pathlib import Path
import csv, json, re, unicodedata
from bisect import bisect_right

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'sources' / 'steffel-1809-ocr-source.txt'
CURATED = ROOT / 'data' / 'entries_curated.csv'
OUT = ROOT / 'data' / 'entries.csv'
LINES_OUT = ROOT / 'data' / 'ocr_dictionary_lines.csv'
PUBLIC = ROOT / 'public' / 'data' / 'entries.json'
INVENTORY = ROOT / 'data' / 'corpus_inventory.json'
SECTIONS = ROOT / 'data' / 'sections'

PROSE_STARTERS = set('''
der die das den dem des ein eine einer eines einem einen er es sie wir ihr man
wenn wann wie weil wo was welche welcher welches welchen welchem deren dessen
diese dieser dieses jene jener jenes hier dort so denn aber auch und oder mit
von vor nach bei bey auf aus in im am an zum zur zu gemeiniglich endlich sobald
nachdem darein darauf daraus dadurch damit ihre seine mein meine dein deine euer
eure noch nun dann daher davon dazu woraus wovon worauf obgleich indem über uber
unter zwischen
'''.split())
HEADERS = ('wörterbuch','woͤrterbuch','deutſch','deutsch','tarahumariſch',
           'tarahumarisch','anhang','sprachprobe','sprachbrobe')

FIELDS = [
    'record_id','source_code','direction','headword_raw','headword_ocr_raw','headword_search',
    'definition_raw','translation_es_editorial','editorial_note','article_ocr_raw','printed_page','pdf_page',
    'source_ocr_line_start','source_ocr_line_end','delimiter','extraction_score',
    'segmentation_confidence','curated_anchor','extraction_method','status','validation'
]


def search_key(s: str) -> str:
    s = (s.replace('ſ','s').replace('ß','ss').replace('⸗','-')
           .replace('ä','ae').replace('Ä','Ae').replace('ö','oe').replace('Ö','Oe')
           .replace('ü','ue').replace('Ü','Ue'))
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = re.sub(r'[^0-9A-Za-z ]+', ' ', s.casefold())
    return re.sub(r'\s+', ' ', s).strip()


def clean_lead(s: str) -> str:
    return re.sub(r'^[\s\d\*#%\\/|_=+~^<>\[\]{}“”„‚‘’\'\"`´;:,.!?()\-]+','',s.strip()).strip()


def find_sections(lines: list[str]) -> dict[str, tuple[int,int]]:
    # 1-based inclusive line ranges. Boundaries are detected from headings in the supplied OCR.
    inv_heading = next(i for i,l in enumerate(lines,1) if i > 7000 and 'Tarahumariſch' in l and 'Deutſches' in l)
    appendix = next(i for i,l in enumerate(lines,1) if i > inv_heading and l.strip() == 'Anhang')
    # The first German headword block begins immediately after the introductory matter and the A heading.
    de_start = 438
    rar_start = inv_heading + 8  # skips heading/noise; first article Äbe
    # If OCR layout shifts, search for the known first inverse article near the heading.
    for i in range(inv_heading, min(inv_heading+30, len(lines))):
        if clean_lead(lines[i-1]).startswith('Äbe'):
            rar_start = i; break
    return {
        'DE-RAR': (de_start, inv_heading-1),
        'RAR-DE': (rar_start, appendix-1),
        'APPENDIX': (appendix, len(lines)),
    }


def load_curated() -> dict[int,dict[str,str]]:
    if not CURATED.exists(): return {}
    return {int(r['source_ocr_line']): r for r in csv.DictReader(CURATED.open(encoding='utf-8'))}


def candidate(lines: list[str], i: int, direction: str, curated: dict[int,dict[str,str]]):
    raw = lines[i-1].strip()
    if i in curated:
        r = curated[i]
        return dict(head=r['headword_raw'], delimiter='curated', score=100, curated='yes')
    if not raw or len(raw) < 3 or re.fullmatch(r'[\d\W_]+', raw): return None
    low = raw.casefold()
    if any(h in low for h in HEADERS): return None
    s = clean_lead(raw)
    if not s: return None
    positions=[]
    for d in (',','.','!',':',';'):
        p=s.find(d)
        if 1 <= p <= 50: positions.append((p,d))
    if not positions: return None
    p, delim = min(positions)
    head = s[:p].strip(' -–—')
    if not head or len(head)>45 or re.search(r'\d',head): return None
    words=head.split()
    key=search_key(head)
    if not key or len(key)<2 or len(words)>6: return None
    first=key.split()[0]
    first_alpha=next((c for c in head if c.isalpha()),'')
    if not first_alpha.isupper(): return None
    if first in PROSE_STARTERS: return None
    # Exclude highly sentence-like prefixes while retaining genuine multiword lemmas.
    if len(words)>=4 and any(x in f' {key} ' for x in (' ist ',' sind ',' hat ',' haben ',' wird ',' werden ',' kann ',' soll ',' muss ',' muß ',' welcher ',' welche ',' welches ')):
        return None
    score=5
    if direction=='DE-RAR': score += 5 if delim in '.!' else 3
    else: score += 6 if delim==',' else 2
    if len(words)<=2: score+=3
    elif len(words)==3: score+=1
    if len(head)<=24: score+=2
    if i>1 and not lines[i-2].strip(): score+=2
    # Penalize German-looking prose fragments in the inverse section.
    if direction=='RAR-DE' and first in {'kind','bogen','natter','sünder','wasser','mörtel','salz','wollen','eheweib','grube','ich'}:
        score-=5
    return dict(head=head, delimiter=delim, score=score, curated='no')


def confidence(score: int, curated: str) -> str:
    if curated=='yes': return 'curated_anchor'
    if score >= 17: return 'high_machine'
    if score >= 14: return 'medium_machine'
    return 'low_machine'


def page_anchors(lines: list[str], sections: dict[str,tuple[int,int]]):
    # Anchor line numbers to printed pages using explicit headers from the OCR; interpolate gaps.
    anchors=[(438,301),(551,302),(720,303),(901,304),(1048,305),(1231,306),
             (1612,309),(1749,310),(1927,311),(1972,312),(2173,313),(2266,314),
             (2570,318),(3205,319),(3286,320),(3557,321),(3849,324),(4073,325),
             (4136,326),(4359,327),(4641,330),(4912,332),(5097,334),(5305,336),
             (5433,337),(5544,338),(5880,340),(6084,341),(6151,342),(6376,343),
             (6452,344),(6586,345),(6839,346),(7026,348),(7222,349),(7297,350),
             (7454,351),(7615,352),(7749,353),(7873,354),(8098,355),(8180,356),
             (8399,357),(8486,358),(8822,360),(8978,361),(9078,362),(9335,363),
             (9440,364),(9784,366),(10128,368),(10286,369),(10613,371),(10669,372),
             (10738,373),(10815,374)]
    anchors=sorted(set(anchors))
    return anchors


def page_for_line(i:int, anchors:list[tuple[int,int]]) -> int:
    xs=[x for x,_ in anchors]
    j=bisect_right(xs,i)-1
    if j<0:return 301
    if j==len(anchors)-1:return anchors[j][1]
    x0,p0=anchors[j]; x1,p1=anchors[j+1]
    if p1<=p0:return p0
    # Interpolate when several printed pages are missing from OCR headers.
    frac=(i-x0)/(x1-x0)
    return max(p0,min(p1,round(p0+frac*(p1-p0))))


def main():
    lines=SRC.read_text(encoding='utf-8',errors='replace').splitlines()
    curated=load_curated(); sections=find_sections(lines); anchors=page_anchors(lines,sections)
    rows=[]; line_rows=[]; next_new_id=61
    counts={}
    for direction in ('DE-RAR','RAR-DE'):
        lo,hi=sections[direction]
        starts=[]
        for i in range(lo,hi+1):
            c=candidate(lines,i,direction,curated)
            if c: starts.append((i,c))
            if lines[i-1].strip():
                pg=page_for_line(i,anchors)
                line_rows.append({'source_ocr_line':i,'direction':direction,'printed_page':pg,'pdf_page':pg-290,'text':lines[i-1]})
        counts[direction]=len(starts)
        for idx,(start,c) in enumerate(starts):
            end=(starts[idx+1][0]-1) if idx+1<len(starts) else hi
            block='\n'.join(lines[start-1:end]).strip()
            # Definition starts after the detected delimiter on the first line, then continues through the block.
            first=clean_lead(lines[start-1])
            if c['delimiter']=='curated':
                # locate the curated headword's first punctuation; OCR may have damaged the initial character
                positions=[p for d in ('.',',','!',':',';') if (p:=first.find(d))>=1]
                cut=min(positions)+1 if positions else len(first)
            else:
                pos=first.find(c['delimiter']); cut=pos+1 if pos>=0 else len(first)
            rest=first[cut:].strip() + ('\n' + '\n'.join(lines[start:end]).strip() if end>=start+1 else '')
            pg=page_for_line(start,anchors)
            first_prefix = first[:cut-1].strip(' -–—') if cut else c['head']
            curated_row = curated.get(start)
            if curated_row:
                record_id = curated_row['record_id']
                translation_es = curated_row.get('translation_es_editorial','')
                editorial_note = curated_row.get('editorial_note','')
            else:
                record_id = f'RHD-S1809-{next_new_id:05d}'
                next_new_id += 1
                translation_es = ''
                editorial_note = 'Segmentación automática de alta cobertura; límite de artículo y lectura OCR pendientes de cotejo facsimilar.'
            rows.append({
                'record_id':record_id,'source_code':'STEFFEL-1809','direction':direction,
                'headword_raw':c['head'],'headword_ocr_raw':first_prefix,'headword_search':search_key(c['head']),
                'definition_raw':re.sub(r'\s+',' ',rest).strip(),
                'translation_es_editorial':translation_es,'editorial_note':editorial_note,
                'article_ocr_raw':block,'printed_page':pg,'pdf_page':pg-290,
                'source_ocr_line_start':start,'source_ocr_line_end':end,'delimiter':c['delimiter'],
                'extraction_score':c['score'],'segmentation_confidence':confidence(c['score'],c['curated']),
                'curated_anchor':c['curated'],'extraction_method':'coverage-first OCR line segmentation v1',
                'status':'machine_segmented_unverified' if c['curated']=='no' else 'seed_curated_ocr_unverified',
                'validation':'pendiente_de_cotejo_facsímil_y_validación_lingüística'
            })
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    with LINES_OUT.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['source_ocr_line','direction','printed_page','pdf_page','text']); w.writeheader(); w.writerows(line_rows)
    PUBLIC.parent.mkdir(parents=True,exist_ok=True)
    PUBLIC.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    SECTIONS.mkdir(parents=True,exist_ok=True)
    a0,a1=sections['APPENDIX']
    appendix='\n'.join(lines[a0-1:]).strip()
    # split language sample from appendix at its heading
    m=re.search(r'(?im)^.*(?:Sprachbrobe|Sprachprobe).*$' , appendix)
    if m:
        numerals=appendix[:m.start()].strip(); language=appendix[m.start():].strip()
    else:
        numerals=appendix; language=''
    (SECTIONS/'appendix-and-numerals-ocr.txt').write_text(numerals+'\n',encoding='utf-8')
    (SECTIONS/'language-sample-ocr.txt').write_text(language+'\n',encoding='utf-8')
    inventory={
        'dataset':'raramuri-historico-steffel-1809','extraction_version':'0.2.0-machine-complete',
        'source_lines':len(lines),'dictionary_ranges':{k:list(v) for k,v in sections.items() if k in ('DE-RAR','RAR-DE')},
        'candidate_entries_total':len(rows),'candidate_entries_by_direction':counts,
        'curated_seed_anchors':sum(r['curated_anchor']=='yes' for r in rows),
        'segmentation_confidence_counts':{x:sum(r['segmentation_confidence']==x for r in rows) for x in ('curated_anchor','high_machine','medium_machine','low_machine')},
        'methodological_note':'Candidate count is not asserted as the definitive lexicographic entry count. Coverage-first machine segmentation intentionally favors recall; every machine candidate remains unverified until facsimile collation.'
    }
    INVENTORY.write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(inventory,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
