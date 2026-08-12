#!/usr/bin/env python3
from pathlib import Path
import csv, json, sqlite3, xml.etree.ElementTree as ET
import hashlib

ROOT=Path(__file__).resolve().parents[1]
CSV=ROOT/'data/entries.csv'
rows=list(csv.DictReader(CSV.open(encoding='utf-8')))
pm=ROOT/'project-metadata.json'
project_metadata=json.loads(pm.read_text(encoding='utf-8')) if pm.exists() else {}

# JSON
jdir=ROOT/'data/json'; jdir.mkdir(parents=True,exist_ok=True)
(jdir/'entries.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Public projection keeps enough provenance for research use
pdir=ROOT/'public/data'; pdir.mkdir(parents=True,exist_ok=True)
(pdir/'entries.json').write_text(json.dumps(rows,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')

# Generic XML
xdir=ROOT/'data/xml'; xdir.mkdir(parents=True,exist_ok=True)
root=ET.Element('raramuriHistorico',{'source':'STEFFEL-1809','version':'0.2.0-editorial-progress'})
for r in rows:
    e=ET.SubElement(root,'entry',{'id':r['record_id'],'direction':r['direction'],'status':r['status']})
    for k,v in r.items():
        if k in {'record_id','direction','status'}: continue
        c=ET.SubElement(e,k); c.text=v
ET.indent(root)
ET.ElementTree(root).write(xdir/'entries.xml',encoding='utf-8',xml_declaration=True)

# TEI research layer (not claimed as validated Lex-0)
TEI='http://www.tei-c.org/ns/1.0'; ET.register_namespace('',TEI)
tei=ET.Element(f'{{{TEI}}}TEI')
header=ET.SubElement(tei,f'{{{TEI}}}teiHeader')
fd=ET.SubElement(header,f'{{{TEI}}}fileDesc')
ts=ET.SubElement(fd,f'{{{TEI}}}titleStmt')
ET.SubElement(ts,f'{{{TEI}}}title').text='Rarámuri Histórico Digital — Corpus Steffel 1791/1809'
ps=ET.SubElement(fd,f'{{{TEI}}}publicationStmt')
ET.SubElement(ps,f'{{{TEI}}}p').text=(
    'Machine-segmented research layer with partial AI-assisted facsimile and diplomatic overlays; '
    'not a validated TEI Lex-0 edition.'
)
sd=ET.SubElement(fd,f'{{{TEI}}}sourceDesc')
ET.SubElement(sd,f'{{{TEI}}}p').text='Matthäus Steffel, Tarahumarisches Wörterbuch, 1809; project facsimile and supplied OCR.'
text=ET.SubElement(tei,f'{{{TEI}}}text'); body=ET.SubElement(text,f'{{{TEI}}}body')
for d in ('DE-RAR','RAR-DE'):
    div=ET.SubElement(body,f'{{{TEI}}}div',{'type':'dictionary','n':d})
    for r in (x for x in rows if x['direction']==d):
        e=ET.SubElement(div,f'{{{TEI}}}entry',{'{http://www.w3.org/XML/1998/namespace}id':r['record_id']})
        form=ET.SubElement(e,f'{{{TEI}}}form',{'type':'lemma'})
        lemma=r.get('headword_diplomatic','').strip() or r['headword_raw']
        ET.SubElement(form,f'{{{TEI}}}orth').text=lemma
        sense=ET.SubElement(e,f'{{{TEI}}}sense')
        ET.SubElement(sense,f'{{{TEI}}}def').text=r['definition_raw']
        if r.get('article_diplomatic','').strip():
            cit=ET.SubElement(e,f'{{{TEI}}}cit',{'type':'diplomatic-transcription'})
            ET.SubElement(cit,f'{{{TEI}}}quote').text=r['article_diplomatic']
            ET.SubElement(cit,f'{{{TEI}}}note',{'type':'verification'}).text=(
                'AI-assisted visual transcription; independent human/philological verification pending.'
            )
        note=ET.SubElement(e,f'{{{TEI}}}note',{'type':'segmentation-status'})
        note.text=r['segmentation_confidence']
        if r.get('diplomatic_status','').strip():
            dn=ET.SubElement(e,f'{{{TEI}}}note',{'type':'diplomatic-status'})
            dn.text=r['diplomatic_status']
        bibl=ET.SubElement(e,f'{{{TEI}}}bibl')
        bibl.text=f"Steffel 1809, p. {r['printed_page']}; OCR lines {r['source_ocr_line_start']}–{r['source_ocr_line_end']}"
ET.indent(tei)
ET.ElementTree(tei).write(xdir/'steffel-1809-tei-machine.xml',encoding='utf-8',xml_declaration=True)

# SQLite
sq=ROOT/'data/raramuri_historico.sqlite'
if sq.exists(): sq.unlink()
con=sqlite3.connect(sq)
cols=list(rows[0].keys())
con.execute('CREATE TABLE entries ('+','.join(f'"{c}" TEXT' for c in cols)+', PRIMARY KEY(record_id))')
con.executemany(
    'INSERT INTO entries ('+','.join(f'"{c}"' for c in cols)+') VALUES ('+','.join('?' for _ in cols)+')',
    [[r[c] for c in cols] for r in rows]
)
con.execute('CREATE INDEX idx_entries_headword_search ON entries(headword_search)')
con.execute('CREATE INDEX idx_entries_direction ON entries(direction)')
con.execute('CREATE INDEX idx_entries_printed_page ON entries(printed_page)')
if 'diplomatic_status' in cols:
    con.execute('CREATE INDEX idx_entries_diplomatic_status ON entries(diplomatic_status)')
con.commit(); con.close()

# Public metadata mirrors project metadata
if pm.exists():
    (pdir/'metadata.json').write_text(pm.read_text(encoding='utf-8'),encoding='utf-8')

# Reproducible manifest for tracked research files (manifest does not hash itself)
manifest_files=[]
for path in sorted(ROOT.rglob('*')):
    if not path.is_file(): continue
    rel=path.relative_to(ROOT).as_posix()
    if rel in {'manifest.json'} or rel.startswith('.git/') or rel.startswith('.tmp'): continue
    b=path.read_bytes()
    manifest_files.append({'path':rel,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
(ROOT/'manifest.json').write_text(
    json.dumps({
        'dataset':project_metadata.get('dataset_id','raramuri-historico-steffel-1809'),
        'version':project_metadata.get('version','0.2.0'),
        'generated':project_metadata.get('generated',''),
        'files':manifest_files
    },ensure_ascii=False,indent=2)+'\n',
    encoding='utf-8'
)
print(f'generated exports for {len(rows)} candidate entries')
