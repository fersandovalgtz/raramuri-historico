#!/usr/bin/env python3
"""Intersect the full historical <tsch>/<ts> inventory with the existing
298-item diachronic semantic-context queue.

The script creates no new lexical or semantic matches. It only joins two
pre-existing derived layers by stable historical record_id and preserves their
machine-only epistemic status.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / 'data/research'
AFF = D / 'historical_affricate_graphemic_inventory.json'
SEM = D / 'diachronic_semantic_context_queue.json'
OUT_JSON = D / 'affricate_diachronic_overlap.json'
OUT_CSV = D / 'affricate_diachronic_overlap.csv'
OUT_SUM = D / 'affricate_diachronic_overlap_summary.json'
OUT_MD = D / 'AFFRICATE_DIACHRONIC_OVERLAP_REPORT.md'


def env_bucket(o: dict) -> str:
    pos = o.get('position')
    v = o.get('following_character', '')
    if pos == 'initial':
        if v == 'a': return 'initial_a'
        if v == 'e': return 'initial_e'
        if v in {'i','o','u'}: return 'initial_i_o_u'
        return 'initial_nonvowel_or_other'
    if v in {'a','e','i','o','u'}: return 'medial_vowel'
    return 'medial_nonvowel_or_other'


def candidate_method(source_id: str) -> str:
    if source_id.startswith('RHD-PCORR-'):
        return 'probable_graphic_correspondence'
    if source_id.startswith('RHD-CORR-'):
        return 'exact_normalized_graphic_match'
    return 'other_existing_candidate_method'


def main() -> None:
    aff = json.loads(AFF.read_text(encoding='utf-8'))
    sem = json.loads(SEM.read_text(encoding='utf-8'))

    by_record: dict[str, list[dict]] = defaultdict(list)
    for o in aff['records']:
        x = dict(o)
        x['environment_bucket'] = env_bucket(o)
        by_record[o['record_id']].append(x)

    joined = []
    for r in sem['records']:
        hrid = r['historical']['record_id']
        occs = by_record.get(hrid)
        if not occs:
            continue
        sig = r.get('machine_context_signal', {})
        joined.append({
            'overlap_id': f"RHD-AFF-DIA-{len(joined)+1:05d}",
            'semantic_context_id': r.get('semantic_context_id'),
            'adjudication_id': r.get('adjudication_id'),
            'source_candidate_id': r.get('source_candidate_id'),
            'candidate_method': candidate_method(r.get('source_candidate_id','')),
            'priority_tier': r.get('priority_tier'),
            'historical': r.get('historical'),
            'modern': r.get('modern'),
            'affricate_occurrences': occs,
            'affricate_graphemes': sorted({o['grapheme'] for o in occs}),
            'affricate_environment_buckets': sorted({o['environment_bucket'] for o in occs}),
            'machine_context_signal_type': sig.get('type'),
            'internal_attestation_count': sig.get('internal_attestation_count', 0),
            'internal_reciprocal_support_count': sig.get('internal_reciprocal_support_count', 0),
            'cross_language_semantic_similarity_computed': False,
            'semantic_judgment': 'not_performed',
            'etymological_judgment': 'not_performed',
            'historical_continuity_judgment': 'not_performed',
            'automatic_sound_correspondence_inference': False,
            'human_reviewed': False,
        })

    hist_records = {r['historical']['record_id'] for r in joined}
    modern_records = {r['modern']['record_id'] for r in joined}
    aff_occ_ids = {o['occurrence_id'] for r in joined for o in r['affricate_occurrences']}
    method_counts = Counter(r['candidate_method'] for r in joined)
    signal_counts = Counter(r['machine_context_signal_type'] for r in joined)
    tier_counts = Counter(str(r['priority_tier']) for r in joined)
    env_candidate_counts = Counter(e for r in joined for e in r['affricate_environment_buckets'])
    env_hist_records = defaultdict(set)
    for r in joined:
        for e in r['affricate_environment_buckets']:
            env_hist_records[e].add(r['historical']['record_id'])

    reciprocal = [r for r in joined if r['internal_reciprocal_support_count'] > 0]
    exact = [r for r in joined if r['candidate_method'] == 'exact_normalized_graphic_match']
    probable = [r for r in joined if r['candidate_method'] == 'probable_graphic_correspondence']

    summary = {
        'dataset': aff['dataset'],
        'layer': 'historical_affricate_existing_diachronic_candidate_overlap_v1',
        'generated': '2026-08-13',
        'affricate_inventory_occurrence_count': aff['occurrence_count'],
        'affricate_inventory_historical_record_count': aff['source_record_count'],
        'diachronic_semantic_queue_candidate_count': sem['count'],
        'diachronic_semantic_queue_signal_counts': sem.get('signal_counts', {}),
        'overlap_candidate_count': len(joined),
        'overlap_historical_record_count': len(hist_records),
        'overlap_modern_record_count': len(modern_records),
        'overlap_affricate_occurrence_count': len(aff_occ_ids),
        'affricate_historical_record_coverage_rate': round(len(hist_records) / aff['source_record_count'], 6) if aff['source_record_count'] else None,
        'candidate_method_counts': dict(sorted(method_counts.items())),
        'machine_context_signal_counts': dict(sorted(signal_counts.items())),
        'priority_tier_counts': dict(sorted(tier_counts.items())),
        'environment_candidate_counts': dict(sorted(env_candidate_counts.items())),
        'environment_historical_record_counts': {k: len(v) for k,v in sorted(env_hist_records.items())},
        'candidates_with_internal_reciprocal_documentary_support': len(reciprocal),
        'exact_graphic_candidate_count': len(exact),
        'probable_graphic_candidate_count': len(probable),
        'human_reviewed': False,
        'automatic_semantic_judgment': False,
        'automatic_sound_correspondence_inference': False,
        'cognacy_judgment': 'not_performed',
        'historical_continuity_judgment': 'not_performed',
        'interpretive_scope': 'Join of pre-existing affricate inventory and pre-existing diachronic candidate queue by historical record_id only. No new correspondence is generated.'
    }

    payload = {
        'dataset': aff['dataset'],
        'layer': 'historical_affricate_existing_diachronic_candidate_overlap_v1',
        'generated': '2026-08-13',
        'count': len(joined),
        'records': joined,
        'human_reviewed': False,
        'automatic_semantic_judgment': False,
        'automatic_sound_correspondence_inference': False,
        'cognacy_judgment': 'not_performed',
        'historical_continuity_judgment': 'not_performed'
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    OUT_SUM.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    fields = [
        'overlap_id','semantic_context_id','adjudication_id','source_candidate_id','candidate_method','priority_tier',
        'historical_record_id','historical_form','historical_gloss','historical_page','modern_record_id','modern_headword',
        'modern_translation','modern_classification','affricate_graphemes','affricate_environment_buckets',
        'machine_context_signal_type','internal_attestation_count','internal_reciprocal_support_count','human_reviewed'
    ]
    with OUT_CSV.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for r in joined:
            h, m = r['historical'], r['modern']
            w.writerow({
                'overlap_id': r['overlap_id'], 'semantic_context_id': r['semantic_context_id'],
                'adjudication_id': r['adjudication_id'], 'source_candidate_id': r['source_candidate_id'],
                'candidate_method': r['candidate_method'], 'priority_tier': r['priority_tier'],
                'historical_record_id': h.get('record_id'), 'historical_form': h.get('form_diplomatic'),
                'historical_gloss': h.get('german_gloss_local'), 'historical_page': h.get('printed_page'),
                'modern_record_id': m.get('record_id'), 'modern_headword': m.get('headword'),
                'modern_translation': m.get('translation_raw'), 'modern_classification': m.get('classification'),
                'affricate_graphemes': '|'.join(r['affricate_graphemes']),
                'affricate_environment_buckets': '|'.join(r['affricate_environment_buckets']),
                'machine_context_signal_type': r['machine_context_signal_type'],
                'internal_attestation_count': r['internal_attestation_count'],
                'internal_reciprocal_support_count': r['internal_reciprocal_support_count'],
                'human_reviewed': False,
            })

    md = [
        '# Solapamiento entre africadas históricas y candidatos diacrónicos existentes', '',
        '**Corte:** 2026-08-13. **Estatus:** unión determinista de capas preexistentes; no crea cognados nuevos.', '',
        f"El inventario contiene **{aff['source_record_count']} registros históricos** con `<tsch>/<ts>`. La cola diacrónica existente contiene **{sem['count']} candidatos**. Su intersección por `historical.record_id` produce **{len(joined)} candidatos**, correspondientes a **{len(hist_records)} registros históricos** y **{len(modern_records)} registros modernos**.", '',
        f"Esto cubre **{100*summary['affricate_historical_record_coverage_rate']:.1f}%** de los registros históricos con africadas mediante al menos un candidato moderno ya existente. No significa que ese porcentaje tenga una correspondencia histórica válida; sólo mide disponibilidad de candidatos para revisión.", '',
        '## Calidad documental disponible', '',
        f"- candidatos exactos normalizados ya existentes: **{len(exact)}**;",
        f"- candidatos gráficos probables ya existentes: **{len(probable)}**;",
        f"- candidatos con apoyo documental recíproco interno de Steffel: **{len(reciprocal)}**.", '',
        '## Distribución por entorno histórico', '',
        '| Entorno | Registros históricos con candidato | Candidatos |', '|---|---:|---:|'
    ]
    for e in sorted(set(env_candidate_counts) | set(env_hist_records)):
        md.append(f"| `{e}` | {len(env_hist_records[e])} | {env_candidate_counts[e]} |")
    md += ['',
        'Esta capa es útil para priorizar la siguiente revisión: permite trabajar primero con formas de `<ts>/<tsch>` que ya cuentan con candidato moderno y, cuando existe, apoyo recíproco interno, sin introducir una búsqueda semántica nueva.', '',
        '`automatic_semantic_judgment=false`; `automatic_sound_correspondence_inference=false`; `cognacy_judgment=not_performed`; `historical_continuity_judgment=not_performed`; `human_reviewed=false`.'
    ]
    OUT_MD.write_text('\n'.join(md) + '\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False))

if __name__ == '__main__':
    main()
