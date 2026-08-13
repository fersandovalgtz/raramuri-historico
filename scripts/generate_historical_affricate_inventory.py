#!/usr/bin/env python3
"""Inventory <tsch>/<ts> occurrences in active historical RAR-DE headwords.

This is a graphemic inventory. It tests Merrill's published distributional
description against the project's diplomatic headword inventory without
changing any source reading or inferring a historical sound law.
"""
from __future__ import annotations

from collections import Counter
import csv
import re
from pathlib import Path

from research_common import OUT, rows, active, norm, split_components, dump

CSV_OUT = OUT / 'historical_affricate_graphemic_inventory.csv'
JSON_OUT = OUT / 'historical_affricate_graphemic_inventory.json'
SUMMARY_OUT = OUT / 'historical_affricate_graphemic_inventory_summary.json'
REPORT_OUT = OUT / 'HISTORICAL_AFFRICATE_INVENTORY_REPORT.md'

AFFRICATE_RE = re.compile(r'tsch|ts')
VOWELS = set('aeiou')


def following_class(key: str, end: int) -> tuple[str, str]:
    if end >= len(key):
        return '', 'end'
    ch = key[end]
    if ch in VOWELS:
        return ch, f'vowel_{ch}'
    return ch, 'nonvowel'


def merrill_expectation(grapheme: str, position: str, following: str) -> str:
    """Encode only the distribution Merrill 2020 §7.5.2 explicitly reports."""
    if position == 'medial':
        return 'compatible_with_reported_medial_free_variation'
    if position != 'initial' or following not in VOWELS:
        return 'outside_simple_reported_initial_vowel_rule'
    if following == 'a':
        return 'compatible_with_reported_initial_free_variation'
    if following == 'e':
        return ('compatible_with_reported_initial_distribution'
                if grapheme == 'ts' else 'potential_exception_to_reported_initial_distribution')
    if following in {'i','o','u'}:
        return ('compatible_with_reported_initial_distribution'
                if grapheme == 'tsch' else 'potential_exception_to_reported_initial_distribution')
    return 'not_assessed'


def main() -> None:
    occurrences = []
    component_keys = set()
    source_records = set()

    for r in rows():
        if not active(r) or r.get('direction') != 'RAR-DE':
            continue
        for component in split_components(r.get('headword_diplomatic', '')):
            key = norm(component).replace(' ', '')
            if not key:
                continue
            matches = list(AFFRICATE_RE.finditer(key))
            if not matches:
                continue
            component_keys.add((r.get('record_id',''), component, key))
            source_records.add(r.get('record_id',''))
            for n, m in enumerate(matches, 1):
                g = m.group(0)
                follow, fclass = following_class(key, m.end())
                pos = 'initial' if m.start() == 0 else 'medial'
                occurrences.append({
                    'occurrence_id': f"RHD-AFF-OCC-{len(occurrences)+1:05d}",
                    'record_id': r.get('record_id',''),
                    'printed_page': int(r.get('printed_page') or 0),
                    'headword_component_diplomatic': component,
                    'graphic_key': key,
                    'occurrence_within_component': n,
                    'grapheme': g,
                    'start_index': m.start(),
                    'position': pos,
                    'preceding_character': key[m.start()-1] if m.start() else '',
                    'following_character': follow,
                    'following_class': fclass,
                    'merrill_distribution_check': merrill_expectation(g, pos, follow),
                    'status': 'machine_graphemic_inventory_only',
                    'automatic_phonological_interpretation': False,
                    'automatic_sound_correspondence_inference': False,
                    'human_reviewed': False,
                })

    by_graph = Counter(x['grapheme'] for x in occurrences)
    by_pos = Counter((x['grapheme'], x['position']) for x in occurrences)
    by_env = Counter((x['grapheme'], x['position'], x['following_character'] or 'END') for x in occurrences)
    checks = Counter(x['merrill_distribution_check'] for x in occurrences)
    exceptions = [x for x in occurrences if x['merrill_distribution_check'] == 'potential_exception_to_reported_initial_distribution']

    payload = {
        'dataset': 'raramuri-historico-steffel-1809',
        'layer': 'historical_affricate_graphemic_inventory_v1',
        'generated': '2026-08-13',
        'source_scope': 'active RAR-DE headword_diplomatic components only',
        'occurrence_count': len(occurrences),
        'source_record_count': len(source_records),
        'component_count': len(component_keys),
        'records': occurrences,
        'human_reviewed': False,
        'automatic_phonological_interpretation': False,
        'automatic_sound_correspondence_inference': False,
        'interpretive_scope': 'Diplomatic <tsch>/<ts> occurrence inventory only. Distributional checks compare strings to Merrill 2020 §7.5.2 and do not adjudicate phoneme identity or rule persistence.'
    }
    summary = {
        'dataset': payload['dataset'],
        'layer': 'historical_affricate_graphemic_inventory_summary_v1',
        'generated': payload['generated'],
        'occurrence_count': len(occurrences),
        'source_record_count': len(source_records),
        'component_count': len(component_keys),
        'grapheme_counts': dict(sorted(by_graph.items())),
        'grapheme_position_counts': {
            f'{g}:{p}': n for (g,p), n in sorted(by_pos.items())
        },
        'grapheme_position_following_counts': {
            f'{g}:{p}:{v}': n for (g,p,v), n in sorted(by_env.items())
        },
        'merrill_distribution_check_counts': dict(sorted(checks.items())),
        'potential_initial_exception_count': len(exceptions),
        'potential_initial_exceptions': [
            {
                'occurrence_id': x['occurrence_id'],
                'record_id': x['record_id'],
                'form': x['headword_component_diplomatic'],
                'graphic_key': x['graphic_key'],
                'grapheme': x['grapheme'],
                'following_character': x['following_character'],
                'printed_page': x['printed_page'],
            } for x in exceptions
        ],
        'published_reference_model': {
            'initial_before_a': 'tsch and ts reported in free variation',
            'initial_before_e': 'ts reported',
            'initial_before_i_o_u': 'tsch reported',
            'medial_before_vowels': 'tsch and ts reported in free variation',
            'reference': 'Merrill et al. 2020 §7.5.2'
        },
        'human_reviewed': False,
        'automatic_phonological_interpretation': False,
        'automatic_sound_correspondence_inference': False,
    }

    dump(JSON_OUT, payload)
    dump(SUMMARY_OUT, summary)
    with CSV_OUT.open('w', encoding='utf-8', newline='') as f:
        fields = list(occurrences[0].keys()) if occurrences else [
            'occurrence_id','record_id','printed_page','headword_component_diplomatic','graphic_key','occurrence_within_component','grapheme','start_index','position','preceding_character','following_character','following_class','merrill_distribution_check','status','automatic_phonological_interpretation','automatic_sound_correspondence_inference','human_reviewed'
        ]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(occurrences)

    lines = [
        '# Inventario histórico completo de `<tsch>` / `<ts>` en RAR–DE',
        '',
        '**Corte:** 2026-08-13. **Estatus:** inventario grafemático reproducible; no es reconstrucción fonológica.',
        '',
        f"Se localizaron **{len(occurrences)} ocurrencias** de `<tsch>`/`<ts>` en **{len(component_keys)} componentes** pertenecientes a **{len(source_records)} registros RAR–DE activos**.",
        '',
        '## Distribución por grafema y posición',
        '',
        '| Grafema / posición | Ocurrencias |',
        '|---|---:|',
    ]
    for (g,p), n in sorted(by_pos.items()):
        lines.append(f'| `{g}` / {p} | {n} |')
    lines += [
        '',
        '## Contraste con la descripción de Merrill 2020 §7.5.2',
        '',
        'El script codifica literalmente el modelo publicado: variación inicial `<tsch> ~ <ts>` ante `a`, `<ts>` ante `e`, `<tsch>` ante `i/o/u`, y variación de ambos en posición medial. Los casos que no encajan se marcan como **excepciones potenciales para revisión**, no como errores de Steffel ni del corpus.',
        '',
        f"Excepciones iniciales potenciales detectadas: **{len(exceptions)}**.",
        '',
    ]
    if exceptions:
        lines += ['| Forma | Grafema | Vocal siguiente | Página |', '|---|---|---|---:|']
        for x in exceptions:
            lines.append(f"| `{x['headword_component_diplomatic']}` | `{x['grapheme']}` | `{x['following_character']}` | {x['printed_page']} |")
    else:
        lines.append('No se detectaron excepciones iniciales potenciales bajo esta codificación.')
    lines += [
        '',
        'Los resultados deben compararse posteriormente con las transcripciones fonéticas de Merrill y con descripciones modernas por variedad. Las formas diplomáticas no se modifican.',
        '',
        '`automatic_phonological_interpretation=false`; `automatic_sound_correspondence_inference=false`; `human_reviewed=false`.',
    ]
    REPORT_OUT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(summary)


if __name__ == '__main__':
    main()
