#!/usr/bin/env python3
"""Generate a human-adjudication packet from the affricate semantic triage layer.

This script does not validate any linguistic relation. It only converts the existing
AI-assisted semantic triage and documentary ranking into a reproducible review queue
and individual dossiers. All adjudication fields are initialized as not_assessed and
human_reviewed remains false.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import csv
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "data" / "research"
SOURCE = RESEARCH / "affricate_semantic_triage.json"
OUT_JSON = RESEARCH / "affricate_human_review_queue.json"
OUT_CSV = RESEARCH / "affricate_human_review_queue.csv"
SUMMARY = RESEARCH / "affricate_human_review_queue_summary.json"
INDEX = RESEARCH / "AFFRICATE_HUMAN_REVIEW_QUEUE.md"
DOSSIERS = RESEARCH / "affricate_human_review_dossiers"

PRIORITY = {
    "priority_positive": (1, "semantic_direct_plus_documentary_tier_1_or_2"),
    "semantic_positive_documentary_ambiguity": (2, "semantic_direct_but_documentary_ambiguity"),
    "priority_related_but_uncertain": (3, "related_domain_plus_documentary_tier_1_or_2"),
    "related_domain_low_documentary_priority": (4, "related_domain_low_documentary_priority"),
    "graphic_decoy_or_semantic_negative": (5, "semantic_negative_control_or_graphic_decoy"),
}


def safe_text(value: object) -> str:
    return str(value or "").replace("|", "/").replace("\n", " ").strip()


def reviewer_template() -> dict:
    return {
        "human_reviewed": False,
        "reviewer": "",
        "affiliation": "",
        "orcid": "",
        "review_date": "",
        "facsimile_verified": "not_assessed",
        "historical_reading": "not_assessed",
        "semantic_relation": "not_assessed",
        "form_relation": "not_assessed",
        "cognacy": "not_assessed",
        "historical_continuity": "not_assessed",
        "sound_correspondence": "not_assessed",
        "decision": "not_assessed",
        "confidence": "not_assessed",
        "evidence": "",
        "note": "",
    }


def dossier_text(item: dict) -> str:
    h = item["historical"]
    m = item["modern"]
    d = item["documentary_ranking"]
    s = item["machine_semantic_triage"]
    r = item["independent_adjudication"]
    return "\n".join(
        [
            f"# Dossier de revisión {item['review_id']}",
            "",
            "**Estatus:** pendiente de revisión humana independiente. Este dossier organiza evidencia; no adjudica cognación, continuidad histórica ni correspondencia fonológica.",
            "",
            "## Identificación",
            "",
            f"- candidato fuente: `{item['source_candidate_id']}`",
            f"- prioridad de revisión: **{item['review_priority']}** ({item['review_priority_reason']})",
            f"- rango documental previo: **{d['rank']}**; tier documental: **{d['priority_tier']}**",
            "",
            "## Evidencia histórica",
            "",
            f"- registro: `{h['record_id']}`; página impresa: **{h['printed_page']}**",
            f"- forma de comparación: `{safe_text(h['form'])}`",
            f"- capa de lectura: `{safe_text(h['reading_layer'])}`",
            f"- artículo diplomático: {safe_text(h['article_diplomatic'])}",
            "",
            "## Candidato moderno",
            "",
            f"- registro: `{m['record_id']}`",
            f"- lema: `{safe_text(m['headword'])}`",
            f"- traducción de la fuente moderna: {safe_text(m['translation_raw'])}",
            f"- clasificación: `{safe_text(m['classification'])}`",
            "",
            "## Evidencia de máquina disponible para el revisor",
            "",
            f"- triage semántico IA-asistido: `{s['label']}`; confianza: `{s['confidence']}`",
            f"- traducción de trabajo del alemán: {safe_text(s['german_working_translation_es'])}",
            f"- razonamiento de triage: {safe_text(s['rationale'])}",
            f"- síntesis previa: `{item['source_synthesis_label']}`",
            "",
            "La traducción de trabajo y el triage son auxiliares analíticos posteriores al ranking documental; no sustituyen el texto de la fuente ni una revisión humana.",
            "",
            "## Adjudicación independiente",
            "",
            f"- facsímil verificado: `{r['facsimile_verified']}`",
            f"- lectura histórica: `{r['historical_reading']}`",
            f"- relación semántica: `{r['semantic_relation']}`",
            f"- relación formal: `{r['form_relation']}`",
            f"- cognación: `{r['cognacy']}`",
            f"- continuidad histórica: `{r['historical_continuity']}`",
            f"- correspondencia fonológica: `{r['sound_correspondence']}`",
            f"- decisión: `{r['decision']}`",
            f"- confianza: `{r['confidence']}`",
            "- evidencia: ",
            "- nota: ",
            "- revisor / afiliación / ORCID / fecha: ",
            "",
            "`human_reviewed=false` hasta que una persona complete y firme la adjudicación.",
            "",
        ]
    )


def main() -> None:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    if payload.get("human_reviewed") is not False:
        raise SystemExit("semantic triage source must remain human_reviewed=false")

    records = payload["records"]
    queue = []
    for source in records:
        label = source["synthesis_review_label"]
        if label not in PRIORITY:
            raise SystemExit(f"unknown synthesis label: {label}")
        priority, reason = PRIORITY[label]
        queue.append(
            {
                "review_id": "",
                "source_candidate_id": source["source_candidate_id"],
                "review_priority": priority,
                "review_priority_reason": reason,
                "historical": source["historical"],
                "modern": source["modern"],
                "documentary_ranking": source["documentary_ranking"],
                "machine_semantic_triage": source["ai_semantic_triage"],
                "source_synthesis_label": label,
                "machine_evidence_scope": {
                    "ai_assisted": True,
                    "human_reviewed": False,
                    "cognacy_judgment": "not_performed",
                    "historical_continuity_judgment": "not_performed",
                    "sound_correspondence_judgment": "not_performed",
                },
                "independent_adjudication": reviewer_template(),
            }
        )

    queue.sort(
        key=lambda x: (
            x["review_priority"],
            int(x["documentary_ranking"]["rank"]),
            x["source_candidate_id"],
        )
    )
    for i, item in enumerate(queue, 1):
        item["review_id"] = f"RHD-AFFHUM-{i:06d}"

    priority_counts = Counter(str(x["review_priority"]) for x in queue)
    synthesis_counts = Counter(x["source_synthesis_label"] for x in queue)
    summary = {
        "dataset": payload["dataset"],
        "layer": "affricate_independent_human_review_queue_v1",
        "generated": payload.get("generated", "2026-08-13"),
        "candidate_count": len(queue),
        "priority_counts": dict(sorted(priority_counts.items())),
        "synthesis_label_counts": dict(sorted(synthesis_counts.items())),
        "priority_1_count": priority_counts.get("1", 0),
        "human_reviewed_count": 0,
        "source_layer": payload.get("layer", "affricate_ai_semantic_triage_v1"),
        "review_order_method": "deterministic_mapping_from_documentary_plus_ai_semantic_triage_v1",
        "interpretive_scope": "Queue and dossiers organize review only. They do not establish semantic identity, cognacy, historical continuity, dialect identity, grapheme-phoneme equivalence, or sound correspondence.",
        "human_reviewed": False,
    }
    out = {
        "dataset": payload["dataset"],
        "layer": summary["layer"],
        "generated": summary["generated"],
        "count": len(queue),
        "source_layer": summary["source_layer"],
        "human_reviewed": False,
        "automatic_cognacy_judgment": False,
        "automatic_historical_continuity_judgment": False,
        "automatic_sound_correspondence_inference": False,
        "records": queue,
    }

    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    fields = [
        "review_id",
        "review_priority",
        "source_candidate_id",
        "documentary_rank",
        "documentary_tier",
        "historical_record_id",
        "historical_page",
        "historical_form",
        "historical_article",
        "modern_record_id",
        "modern_headword",
        "modern_translation",
        "semantic_label",
        "semantic_confidence",
        "source_synthesis_label",
        "human_reviewed",
        "decision",
    ]
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for item in queue:
            writer.writerow(
                {
                    "review_id": item["review_id"],
                    "review_priority": item["review_priority"],
                    "source_candidate_id": item["source_candidate_id"],
                    "documentary_rank": item["documentary_ranking"]["rank"],
                    "documentary_tier": item["documentary_ranking"]["priority_tier"],
                    "historical_record_id": item["historical"]["record_id"],
                    "historical_page": item["historical"]["printed_page"],
                    "historical_form": item["historical"]["form"],
                    "historical_article": item["historical"]["article_diplomatic"],
                    "modern_record_id": item["modern"]["record_id"],
                    "modern_headword": item["modern"]["headword"],
                    "modern_translation": item["modern"]["translation_raw"],
                    "semantic_label": item["machine_semantic_triage"]["label"],
                    "semantic_confidence": item["machine_semantic_triage"]["confidence"],
                    "source_synthesis_label": item["source_synthesis_label"],
                    "human_reviewed": "false",
                    "decision": "not_assessed",
                }
            )

    if DOSSIERS.exists():
        shutil.rmtree(DOSSIERS)
    DOSSIERS.mkdir(parents=True, exist_ok=True)
    for item in queue:
        (DOSSIERS / f"{item['review_id']}.md").write_text(dossier_text(item), encoding="utf-8")

    lines = [
        "# Cola de revisión humana de candidatos de africadas",
        "",
        f"**Corte:** {summary['generated']}. **Candidatos:** {len(queue)}. **Revisión humana completada:** 0.",
        "",
        "Esta capa convierte el ranking documental y el triage semántico IA-asistido en un orden reproducible de inspección. La prioridad es logística y epistemológica: no constituye validación lingüística.",
        "",
        "Prioridad 1 = alineación semántica directa fuerte + tier documental 1/2; prioridad 2 = alineación directa con ambigüedad documental; prioridad 3 = dominio relacionado con buen soporte documental; prioridad 4 = dominio relacionado con menor prioridad documental; prioridad 5 = negativos semánticos y señuelos gráficos, conservados como controles.",
        "",
        "| P | Dossier | Fuente | Histórico | Moderno | Rango doc. | Triage semántico | Síntesis |",
        "|---:|---|---|---|---|---:|---|---|",
    ]
    for item in queue:
        lines.append(
            f"| {item['review_priority']} | `{item['review_id']}` | `{item['source_candidate_id']}` | "
            f"`{safe_text(item['historical']['form'])}` | `{safe_text(item['modern']['headword'])}` | "
            f"{item['documentary_ranking']['rank']} | `{item['machine_semantic_triage']['label']}` | `{item['source_synthesis_label']}` |"
        )
    lines += [
        "",
        "Cada dossier conserva por separado el artículo diplomático histórico, el candidato moderno, la evidencia documental, el triage de máquina y una plantilla vacía de adjudicación independiente.",
        "",
        "`human_reviewed=false`; `cognacy_judgment=not_performed`; `historical_continuity_judgment=not_performed`; `sound_correspondence_judgment=not_performed`.",
        "",
    ]
    INDEX.write_text("\n".join(lines), encoding="utf-8")

    print(
        f"Generated affricate human review packet: {len(queue)} candidates; "
        f"priorities={dict(sorted(priority_counts.items()))}; human reviewed=0"
    )


if __name__ == "__main__":
    main()
