#!/usr/bin/env python3
from pathlib import Path
import subprocess, csv, argparse
p=argparse.ArgumentParser(); p.add_argument('pdf'); p.add_argument('--out',default='data/pages.csv'); a=p.parse_args()
tmp=Path('.tmp-steffel.txt')
subprocess.run(['pdftotext','-layout',a.pdf,str(tmp)],check=True)
pages=tmp.read_text(errors='replace').split('\f');
if pages and pages[-1]=='': pages.pop()
Path(a.out).parent.mkdir(parents=True,exist_ok=True)
with Path(a.out).open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['pdf_page','printed_page','text_ocr_pdf']); w.writeheader()
    for i,t in enumerate(pages,1): w.writerow({'pdf_page':i,'printed_page':i+290 if i>=11 else '', 'text_ocr_pdf':t.strip()})
tmp.unlink(missing_ok=True)
print(f'wrote {len(pages)} pages to {a.out}')
