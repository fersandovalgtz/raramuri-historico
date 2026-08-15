#!/usr/bin/env python3
"""Generate a reproducible Markdown/CSV report from machine-only diachronic evidence.

The report summarizes retrieval evidence and null-calibrated graphemic specificity for
all 298 candidates. It deliberately does not infer semantics, cognacy, etymology,
sound laws or historical continuity.
"""
from pathlib import Path
import csv, json

ROOT=Path(__file__).resolve().parents[1]
SCORES=ROOT/"data/research/diachronic_machine_scores.json"
CAL=ROOT/"data/research/diachronic_machine_calibration.json"
MD=ROOT/"data/research/diachronic_machine_report.md"
CSV=ROOT/"data/research/diachronic_machine_report.csv"


def main():
    scores=json.loads(SCORES.read_text(encoding="utf-8"))
    cal=json.loads(CAL.read_text(encoding="utf-8"))
    if scores.get("count")!=298 or cal.get("candidate_count")!=298:
        raise SystemExit("ERROR: diachronic candidate universe is not 298/298")
    score_by_id={x.get("semantic_context_id"):x for x in scores.get("records",[])}
    rows=[]
    for c in cal.get("records",[]):
        sid=c.get("semantic_context_id"); s=score_by_id.get(sid,{})
        rows.append({
            "semantic_context_id":sid,
            "historical_record_id":c.get("historical_record_id"),
            "modern_record_id":c.get("modern_record_id"),
            "historical_form":c.get("historical_form"),
            "modern_form":c.get("modern_form"),
            "documentary_support_score":s.get("documentary_support_score"),
            "support_bucket":s.get("support_bucket"),
            "graphemic_sequence_ratio":c.get("observed_sequence_ratio"),
            "null_empirical_percentile":c.get("null_empirical_percentile"),
            "null_empirical_upper_tail":c.get("null_empirical_upper_tail"),
            "graphemic_specificity_bucket":c.get("graphemic_specificity_bucket"),
            "relation_status":"candidate",
            "scope":"documentary_and_graphemic_retrieval_evidence_only",
            "semantic_probability":None,
            "cognacy_probability":None,
            "etymological_probability":None,
            "historical_continuity_probability":None,
            "human_reviewed":False,
        })
    rows.sort(key=lambda r:(-(r["null_empirical_percentile"] or 0),-(r["documentary_support_score"] or 0),str(r["semantic_context_id"])))

    CSV.parent.mkdir(parents=True,exist_ok=True)
    fields=list(rows[0].keys())
    with CSV.open("w",encoding="utf-8",newline="") as fh:
        w=csv.DictWriter(fh,fieldnames=fields); w.writeheader(); w.writerows(rows)

    sm=cal.get("summary",{}); sb=scores.get("summary",{}).get("support_buckets",{}); cb=sm.get("candidate_specificity_buckets",{})
    top=rows[:30]
    lines=[
        "# RHD — Informe diacrónico computacional Steffel ↔ Rarámuri Digital",
        "",
        "**Alcance:** evidencia documental de recuperación y especificidad grafémica machine-only.  ",
        "**Universo:** 298 relaciones candidatas.  ",
        f"**Controles nulos:** {cal.get('null_pair_count')} emparejamientos rotos deterministas ({len(cal.get('shifts',[]))} desplazamientos circulares).",
        "",
        "## Regla epistemológica",
        "",
        "Todas las relaciones permanecen `candidate`. Un puntaje alto o un percentil grafémico alto **no constituye** por sí mismo evidencia suficiente de identidad semántica, cognación, etimología, ley fonológica ni continuidad histórica. Este informe sirve para priorizar e inspeccionar evidencia documental computacional, no para reemplazar una afirmación lingüística por una puntuación.",
        "",
        "## Resumen cuantitativo",
        "",
        f"- Media de similitud grafémica observada: **{sm.get('observed_mean_sequence_ratio')}**.",
        f"- Media en controles nulos: **{sm.get('null_mean_sequence_ratio')}**.",
        f"- Elevación observada sobre el nulo: **{sm.get('mean_ratio_lift_over_null')}**.",
        f"- Mediana observada: **{sm.get('observed_median_sequence_ratio')}**; mediana nula: **{sm.get('null_median_sequence_ratio')}**.",
        f"- P90 observado: **{sm.get('observed_p90_sequence_ratio')}**; P90 nulo: **{sm.get('null_p90_sequence_ratio')}**.",
        f"- Buckets de apoyo documental: `{json.dumps(sb,ensure_ascii=False,sort_keys=True)}`.",
        f"- Buckets de especificidad grafémica: `{json.dumps(cb,ensure_ascii=False,sort_keys=True)}`.",
        "",
        "## Treinta candidatos con mayor especificidad grafémica relativa",
        "",
        "| # | Steffel | Forma moderna | Apoyo doc. | Percentil nulo | Especificidad |",
        "|---:|---|---|---:|---:|---|",
    ]
    for i,r in enumerate(top,1):
        lines.append(f"| {i} | {str(r['historical_form']).replace('|','/')} | {str(r['modern_form']).replace('|','/')} | {r['documentary_support_score']} | {r['null_empirical_percentile']} | {r['graphemic_specificity_bucket']} |")
    lines += [
        "",
        "## Productos reproducibles",
        "",
        "- `diachronic_machine_scores.json`: apoyo documental de recuperación.",
        "- `diachronic_machine_calibration.json`: contraste grafémico contra controles nulos.",
        "- `diachronic_machine_report.csv`: las 298 relaciones con ambos conjuntos de métricas.",
        "- Este archivo Markdown: síntesis humana-legible generada automáticamente.",
        "",
        "## No-afirmaciones",
        "",
        "El pipeline mantiene en `null` las probabilidades semántica, de cognación, etimológica y de continuidad histórica. Tampoco declara leyes de sonido. Cualquier uso posterior debe conservar esta separación entre señal de recuperación y conclusión lingüística.",
        "",
    ]
    MD.write_text("\n".join(lines),encoding="utf-8")
    print(f"generated diachronic machine report for {len(rows)} candidates -> {MD.relative_to(ROOT)}, {CSV.relative_to(ROOT)}")

if __name__=="__main__": main()
