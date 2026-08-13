#!/usr/bin/env python3
from collections import Counter
from research_common import OUT,rows,active,norm,split_components,dump
import statistics,unicodedata,json

def main():
    forms=[c for r in rows() if active(r) and r.get('direction')=='RAR-DE' for c in split_components(r.get('headword_diplomatic',''))]
    lengths=[len(''.join(ch for ch in norm(f) if ch.isalnum())) for f in forms if norm(f)]; chars=Counter(); diacritics=Counter()
    for f in forms:
        for ch in f:
            if ch.isalpha():
                chars[ch.casefold()]+=1
                if any(unicodedata.category(x)=='Mn' for x in unicodedata.normalize('NFD',ch)) or ord(ch)>127: diacritics[ch]+=1
    out={'dataset':'raramuri-historico-steffel-1809','generated':'2026-08-13','rar_de_component_count':len(forms),'length':{'min':min(lengths) if lengths else 0,'median':statistics.median(lengths) if lengths else 0,'mean':round(statistics.mean(lengths),3) if lengths else 0,'max':max(lengths) if lengths else 0},'character_frequency_diplomatic':dict(chars.most_common()),'diacritic_character_frequency':dict(diacritics.most_common()),'interpretive_scope':'Descriptive counts of diplomatic component strings only; no phonological analysis is implied.'}
    dump(OUT/'graphemic_statistics.json',out); print(json.dumps({'components':len(forms),'characters':len(chars),'diacritics':len(diacritics)},ensure_ascii=False))
if __name__=='__main__': main()
