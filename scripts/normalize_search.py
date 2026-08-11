#!/usr/bin/env python3
import sys, re, unicodedata
def key(s):
    s=s.replace('ſ','s'); s=unicodedata.normalize('NFD',s)
    s=''.join(c for c in s if unicodedata.category(c)!='Mn')
    s=re.sub(r'[^0-9a-zA-Z ]+',' ',s.casefold())
    return re.sub(r'\s+',' ',s).strip()
for arg in sys.argv[1:]: print(key(arg))
