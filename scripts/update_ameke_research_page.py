#!/usr/bin/env python3
"""Publish an idempotent non-adjudicative -ameke permutation note to docs."""
from pathlib import Path
import json,re,html
from research_common import ROOT,OUT

START='<!-- AMEKE_PERM_START -->'; END='<!-- AMEKE_PERM_END -->'
RSTART='<!-- AMEKE_PERM_README_START -->'; REND='<!-- AMEKE_PERM_README_END -->'
CSTART='<!-- AMEKE_PERM_CHANGELOG_START -->'; CEND='<!-- AMEKE_PERM_CHANGELOG_END -->'

def replace_or_insert(text,start,end,block,anchor):
    pat=re.compile(re.escape(start)+r'.*?'+re.escape(end),re.S)
    wrapped=start+'\n'+block.strip()+'\n'+end
    if pat.search(text):return pat.sub(wrapped,text)
    if anchor in text:return text.replace(anchor,wrapped+'\n'+anchor,1)
    return text+'\n'+wrapped+'\n'

def fmt(x):
    if isinstance(x,float):return f'{x:.6g}'
    return str(x)

def main():
    p=json.loads((OUT/'ameke_permutation_tests_summary.json').read_text(encoding='utf-8'))
    sig=p.get('conservative_permutation_signals',[])
    if sig:
        s=sig[0]
        signal_html=f'''<div class="callout"><strong>Señal que sobrevive el control conservador:</strong> <code>{html.escape(s['exclusive_suffix_class'])}</code> ↔ <code>{html.escape(s['german_context_proxy'])}</code>. Tasa local {s['observed_class_rate']:.3f} frente a {s['observed_rest_rate']:.3f} en el resto (Δ={s['observed_rate_difference']:.3f}); p empírica={fmt(s['empirical_two_sided_p'])}, q BH={fmt(s['bh_fdr_q'])}, FWER max-|Δ|={fmt(s['max_abs_rate_difference_fwer_p'])}. Esta dependencia estadística no identifica una función lingüística.</div>'''
        signal_md=f"La única señal que sobrevive simultáneamente FDR y el control familiar max-|Δ| es **`{s['exclusive_suffix_class']}` ↔ `{s['german_context_proxy']}`**: {s['observed_class_rate']:.3f} dentro de la clase frente a {s['observed_rest_rate']:.3f} en el resto (Δ={s['observed_rate_difference']:.3f}; p={fmt(s['empirical_two_sided_p'])}; q={fmt(s['bh_fdr_q'])}; FWER={fmt(s['max_abs_rate_difference_fwer_p'])})."
    else:
        signal_html='<div class="callout">Ninguna celda sobrevive actualmente el control conservador max-|Δ|.</div>'
        signal_md='Ninguna celda sobrevive actualmente el control conservador max-|Δ|.'
    hblock=f'''<section class="panel" id="ameke-permutation"><h2>Control aleatorio de la constelación <code>-ameke</code></h2><p>Se ejecutaron <strong>{p['permutation_iterations']:,} permutaciones deterministas</strong> (semilla {p['random_seed']}) reasignando las cinco etiquetas gráficas exclusivas entre los {p['member_count']} miembros completos, sin romper sus bolsas de contexto alemán. El modelo nulo conserva tamaños de clase y evidencia documental por miembro.</p><div class="pagegrid"><article class="pagecard"><span>{p['omnibus_empirical_permutation_p']}</span><strong>p empírica ómnibus</strong><p>χ² observado {p['omnibus_chi_square_observed']:.3f}; V de Cramér descriptivo {p['omnibus_cramers_v_descriptive']:.3f}.</p></article><article class="pagecard"><span>{p['bh_fdr_q_le_0_05_count']}</span><strong>celdas con FDR q≤.05</strong><p>De {p['cell_test_count']} contrastes clase↔proxy.</p></article><article class="pagecard"><span>{p['maxT_fwer_p_le_0_05_count']}</span><strong>celdas con FWER≤.05</strong><p>Control familiar max-|diferencia de tasas|.</p></article></div>{signal_html}<p class="small">La unidad de aleatorización es el miembro histórico completo. La significación estadística documenta dependencia entre una terminación gráfica y un proxy formal del alemán; no constituye segmentación morfológica, categoría gramatical, significado ni paradigma.</p></section>'''
    page=ROOT/'public/research.html'
    text=page.read_text(encoding='utf-8')
    text=replace_or_insert(text,START,END,hblock,'</main>')
    page.write_text(text,encoding='utf-8')

    md=f'''## Control por permutaciones de la constelación `-ameke`\n\nSe ejecutan **{p['permutation_iterations']:,} permutaciones reproducibles** con semilla `{p['random_seed']}`, reasignando las clases gráficas exclusivas entre miembros completos. La prueba ómnibus produce χ²={p['omnibus_chi_square_observed']:.3f}, V de Cramér descriptivo={p['omnibus_cramers_v_descriptive']:.3f} y p empírica={fmt(p['omnibus_empirical_permutation_p'])}. De {p['cell_test_count']} contrastes, {p['raw_empirical_p_le_0_05_count']} tienen p≤.05 sin corrección, {p['bh_fdr_q_le_0_05_count']} mantienen q BH≤.05 y {p['maxT_fwer_p_le_0_05_count']} sobreviven el control familiar max-|Δ|.\n\n{signal_md}\n\nEl resultado se interpreta como **dependencia documental entre clases gráficas y proxies formales del contexto alemán**, no como prueba de morfemas, categorías gramaticales, semántica, paradigmas o continuidad histórica. Artefactos: `data/research/ameke_permutation_tests.json`, `.csv` y `_summary.json`.\n\n'''
    rp=ROOT/'README.md'; rt=rp.read_text(encoding='utf-8'); rt=replace_or_insert(rt,RSTART,REND,md,'## Frontera documental'); rp.write_text(rt,encoding='utf-8')

    cb=f'''## Control por permutaciones `-ameke` — 2026-08-13\n\n- {p['permutation_iterations']:,} permutaciones deterministas por miembro, semilla {p['random_seed']}; prueba ómnibus p={fmt(p['omnibus_empirical_permutation_p'])}.\n- {p['bh_fdr_q_le_0_05_count']} contrastes con FDR q≤.05 y {p['maxT_fwer_p_le_0_05_count']} con control familiar max-|Δ|≤.05.\n- {signal_md}\n- Revisión humana y análisis morfológico/semántico automáticos permanecen desactivados.\n\n'''
    cp=ROOT/'CHANGELOG.md'; ct=cp.read_text(encoding='utf-8'); ct=replace_or_insert(ct,CSTART,CEND,cb,'## Investigación interna — 2026-08-13'); cp.write_text(ct,encoding='utf-8')

if __name__=='__main__':main()
