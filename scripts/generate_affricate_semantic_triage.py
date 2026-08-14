#!/usr/bin/env python3
"""Create an AI-assisted semantic triage layer for the 26 source-supported affricate candidates.

This layer is deliberately downstream from the documentary ranking. It compares the
historical German gloss/article with the pinned modern Spanish translation only after
candidate retrieval and documentary ranking have been frozen. It does not alter the
ranking, does not adjudicate cognacy or historical continuity, and is explicitly not
human review.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "data" / "research"
CANDIDATES = RESEARCH / "source_supported_affricate_candidates.json"
RANKING = RESEARCH / "affricate_candidate_evidence_ranking.json"
OUT_JSON = RESEARCH / "affricate_semantic_triage.json"
OUT_CSV = RESEARCH / "affricate_semantic_triage.csv"
SUMMARY = RESEARCH / "affricate_semantic_triage_summary.json"
REPORT = RESEARCH / "AFFRICATE_SEMANTIC_TRIAGE.md"

# Human-readable, explicit assessment table. The Spanish renderings of German glosses
# are working translations supplied for transparent AI triage; they are not source text.
ASSESSMENTS = {
    "RHD-AFFSRC-000001": ("strong_direct_overlap", "high", "Lachen = reír", "‘Lachen’ corresponde directamente a ‘Reír, sonreír’."),
    "RHD-AFFSRC-000002": ("compatible_related_domain", "medium", "Vorher, voraus = antes / por delante", "‘Vorher, voraus’ comparte el dominio temporal/espacial de ‘Primeramente, adelante, enfrente’, pero no es equivalencia estricta."),
    "RHD-AFFSRC-000003": ("contradictory", "high", "Vorher, voraus = antes / por delante", "La glosa histórica no corresponde a ‘Meter / poner adentro’."),
    "RHD-AFFSRC-000004": ("contradictory", "high", "Schwein = cerdo", "‘Schwein’ no corresponde a ‘Perro’."),
    "RHD-AFFSRC-000005": ("contradictory", "high", "Schwein = cerdo", "‘Schwein’ no corresponde a ‘Hermana mayor’."),
    "RHD-AFFSRC-000006": ("contradictory", "high", "Schwein = cerdo", "Este registro histórico significa ‘cerdo’; no corresponde a la entrada moderna ‘Dormir’. El histórico de dormir es otra entrada distinta."),
    "RHD-AFFSRC-000007": ("strong_direct_overlap", "high", "Schwein = cerdo", "‘Schwein’ y ‘Marrano’ corresponden directamente al mismo dominio léxico."),
    "RHD-AFFSRC-000008": ("compatible_related_domain", "low", "Kurz = corto", "‘Kurz’ y ‘Chiquitos’ comparten un dominio dimensional, pero corto y pequeño no son equivalentes."),
    "RHD-AFFSRC-000009": ("contradictory", "high", "Draußen = afuera", "‘Draußen’ no corresponde a ‘Saber, conocer / hay luz / verse bien’."),
    "RHD-AFFSRC-000010": ("strong_direct_overlap", "high", "Draußen = afuera", "‘Draußen’ corresponde directamente a ‘Afuera’."),
    "RHD-AFFSRC-000011": ("strong_direct_overlap", "high", "wissen, sehen, erfahren = saber, ver, conocer/enterarse", "El artículo histórico verbal comparte directamente ‘saber/ver/conocer’ con la entrada moderna ‘Saber, conocer’."),
    "RHD-AFFSRC-000012": ("contradictory", "high", "wissen, sehen, erfahren = saber, ver, conocer/enterarse", "El artículo histórico verbal no corresponde a la entrada moderna ‘Afuera’."),
    "RHD-AFFSRC-000013": ("contradictory", "high", "Anfüllen = llenar", "‘Anfüllen’ no corresponde a ‘Brincar’."),
    "RHD-AFFSRC-000014": ("contradictory", "high", "Anfüllen = llenar", "‘Anfüllen’ no corresponde a ‘Soplar’."),
    "RHD-AFFSRC-000015": ("contradictory", "high", "Noch = todavía / aún", "‘Noch’ no corresponde a ‘Robar’."),
    "RHD-AFFSRC-000016": ("contradictory", "medium", "Krätze = sarna", "‘Krätze’ es una afección cutánea; ‘Feo’ no constituye una correspondencia léxica suficiente."),
    "RHD-AFFSRC-000017": ("compatible_related_domain", "medium", "Krätze = sarna", "‘Tener granos o llagas’ comparte el dominio de afección cutánea con ‘Krätze’, pero no equivale necesariamente a ‘sarna’."),
    "RHD-AFFSRC-000018": ("contradictory", "high", "Wegwerfen = tirar / desechar", "‘Wegwerfen’ no corresponde a ‘Tener granos o llagas’."),
    "RHD-AFFSRC-000019": ("contradictory", "high", "Wunde = herida", "‘Wunde’ no corresponde a ‘Chanate / zanate’."),
    "RHD-AFFSRC-000020": ("strong_direct_overlap", "high", "Nehmen, Ergreifen = tomar, coger, agarrar", "La glosa histórica corresponde directamente a ‘Coger, agarrar / tomar’."),
    "RHD-AFFSRC-000021": ("strong_direct_overlap", "medium", "Gewebe = tejido / tela", "‘Gewebe’ es compatible de forma directa con ‘Manta, ropa’ en el dominio de tejido/textil."),
    "RHD-AFFSRC-000022": ("strong_direct_overlap", "high", "Fein, Dünn, Flach = fino, delgado, plano", "La glosa histórica incluye ‘Flach’, que corresponde directamente a ‘Plano’."),
    "RHD-AFFSRC-000023": ("contradictory", "high", "Stinken = apestar", "‘Stinken’ no corresponde a ‘Estar amargo’; este caso funciona además como decoy gráfico ya preservado en el holdout."),
    "RHD-AFFSRC-000024": ("compatible_related_domain", "low", "Der Ort, wo sich ein zahmes Thier befindet = lugar/posición donde se encuentra un animal doméstico", "Existe proximidad en el dominio de localización/estado de un animal con ‘Estar parado’, pero la equivalencia es incierta."),
    "RHD-AFFSRC-000025": ("strong_direct_overlap", "high", "Schleifen, Schärfen = afilar / aguzar", "La glosa histórica corresponde directamente a ‘Afilar’."),
    "RHD-AFFSRC-000026": ("strong_direct_overlap", "high", "Schwarz = negro", "‘Schwarz’ corresponde directamente a ‘Negro’; la forma histórica usada aquí pertenece sólo a la capa de sensibilidad facsimilar IA-asistida."),
}


def synthesis_label(semantic_label: str, documentary_tier: int) -> str:
    if semantic_label == "strong_direct_overlap" and documentary_tier <= 2:
        return "priority_positive"
    if semantic_label == "strong_direct_overlap":
        return "semantic_positive_documentary_ambiguity"
    if semantic_label == "compatible_related_domain" and documentary_tier <= 2:
        return "priority_related_but_uncertain"
    if semantic_label == "compatible_related_domain":
        return "related_domain_low_documentary_priority"
    if semantic_label == "contradictory":
        return "graphic_decoy_or_semantic_negative"
    return "unresolved"


def main() -> None:
    candidates = json.loads(CANDIDATES.read_text(encoding="utf-8"))
    ranking = json.loads(RANKING.read_text(encoding="utf-8"))
    records = candidates["records"]
    rank_by_id = {r["source_candidate_id"]: r for r in ranking["records"]}
    ids = {r["candidate_id"] for r in records}
    if ids != set(ASSESSMENTS):
        missing = sorted(ids - set(ASSESSMENTS))
        extra = sorted(set(ASSESSMENTS) - ids)
        raise SystemExit(f"assessment coverage mismatch missing={missing} extra={extra}")
    if ids != set(rank_by_id):
        raise SystemExit("documentary ranking does not cover the same candidate set")

    out = []
    for r in records:
        cid = r["candidate_id"]
        label, confidence, german_working_es, rationale = ASSESSMENTS[cid]
        dr = rank_by_id[cid]
        item = {
            "semantic_triage_id": f"RHD-AFFSEM-{len(out)+1:06d}",
            "source_candidate_id": cid,
            "historical": {
                "record_id": r["historical"]["record_id"],
                "form": r["historical"]["comparison_surface"],
                "article_diplomatic": r["historical"]["article_diplomatic"],
                "reading_layer": r["historical"]["reading_layer"],
                "printed_page": r["historical"]["printed_page"],
            },
            "modern": {
                "record_id": r["modern"]["record_id"],
                "headword": r["modern"]["headword"],
                "translation_raw": r["modern"]["translation_raw"],
                "classification": r["modern"]["classification"],
            },
            "documentary_ranking": {
                "rank": dr["rank"],
                "priority_tier": dr["priority_tier"],
                "positive_holdout_pair": dr["positive_holdout_pair"],
                "internal_support_label": dr["internal_support_label"],
                "unique_exact_projected_modern_record": dr["unique_exact_projected_modern_record"],
            },
            "ai_semantic_triage": {
                "label": label,
                "confidence": confidence,
                "german_working_translation_es": german_working_es,
                "rationale": rationale,
                "semantic_similarity_computed_numerically": False,
                "ai_assisted": True,
                "human_reviewed": False,
            },
            "synthesis_review_label": synthesis_label(label, int(dr["priority_tier"])),
            "cognacy_judgment": "not_performed",
            "historical_continuity_judgment": "not_performed",
            "sound_correspondence_judgment": "not_performed",
            "human_reviewed": False,
        }
        out.append(item)

    sem_counts = Counter(x["ai_semantic_triage"]["label"] for x in out)
    synth_counts = Counter(x["synthesis_review_label"] for x in out)
    high_positive = [x for x in out if x["synthesis_review_label"] == "priority_positive"]
    summary = {
        "dataset": candidates["dataset"],
        "layer": "affricate_ai_semantic_triage_v1",
        "generated": "2026-08-13",
        "candidate_count": len(out),
        "semantic_label_counts": dict(sorted(sem_counts.items())),
        "synthesis_label_counts": dict(sorted(synth_counts.items())),
        "priority_positive_count": len(high_positive),
        "priority_positive_candidate_ids": [x["source_candidate_id"] for x in high_positive],
        "assessment_method": "explicit_ai_assisted_bilingual_gloss_comparison_after_documentary_ranking_v1",
        "documentary_ranking_modified": False,
        "semantic_similarity_used_for_candidate_retrieval": False,
        "semantic_similarity_used_for_documentary_ranking": False,
        "working_german_translations_are_source_text": False,
        "ai_assisted": True,
        "human_reviewed": False,
        "cognacy_judgment": "not_performed",
        "historical_continuity_judgment": "not_performed",
        "automatic_sound_correspondence_inference": False,
        "interpretive_scope": "AI-assisted semantic triage for review prioritization only. Labels do not establish cognacy, historical continuity, phonological correspondence, or human validation.",
    }
    payload = {
        "dataset": candidates["dataset"],
        "layer": summary["layer"],
        "generated": "2026-08-13",
        "count": len(out),
        "records": out,
        "ai_assisted": True,
        "human_reviewed": False,
        "cognacy_judgment": "not_performed",
        "historical_continuity_judgment": "not_performed",
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    fields = ["semantic_triage_id", "source_candidate_id", "documentary_rank", "documentary_tier", "historical_form", "historical_article", "modern_headword", "modern_translation", "semantic_label", "confidence", "working_german_translation_es", "synthesis_review_label", "human_reviewed"]
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for x in out:
            w.writerow({
                "semantic_triage_id": x["semantic_triage_id"],
                "source_candidate_id": x["source_candidate_id"],
                "documentary_rank": x["documentary_ranking"]["rank"],
                "documentary_tier": x["documentary_ranking"]["priority_tier"],
                "historical_form": x["historical"]["form"],
                "historical_article": x["historical"]["article_diplomatic"],
                "modern_headword": x["modern"]["headword"],
                "modern_translation": x["modern"]["translation_raw"],
                "semantic_label": x["ai_semantic_triage"]["label"],
                "confidence": x["ai_semantic_triage"]["confidence"],
                "working_german_translation_es": x["ai_semantic_triage"]["german_working_translation_es"],
                "synthesis_review_label": x["synthesis_review_label"],
                "human_reviewed": False,
            })

    md = [
        "# Triage semántico independiente de candidatos de africadas",
        "",
        "**Corte:** 2026-08-13. **Estatus:** lectura semántica IA-asistida posterior al ranking documental; no es adjudicación humana.",
        "",
        f"Se revisan **{len(out)} candidatos**. La semántica no intervino en la recuperación ni en el ranking documental previo.",
        "",
        f"- alineación semántica directa fuerte: **{sem_counts.get('strong_direct_overlap', 0)}**;",
        f"- dominio relacionado pero no equivalente: **{sem_counts.get('compatible_related_domain', 0)}**;",
        f"- contradicción semántica: **{sem_counts.get('contradictory', 0)}**.",
        "",
        f"La síntesis produce **{len(high_positive)} candidatos `priority_positive`**, es decir, alineación semántica directa fuerte + Tier documental 1/2.",
        "",
        "| Doc. rank | Histórico | Moderno | Triage | Conf. | Síntesis |",
        "|---:|---|---|---|---|---|",
    ]
    for x in sorted(out, key=lambda z: z["documentary_ranking"]["rank"]):
        md.append(f"| {x['documentary_ranking']['rank']} | `{x['historical']['form']}` | `{x['modern']['headword']}` | {x['ai_semantic_triage']['label']} | {x['ai_semantic_triage']['confidence']} | {x['synthesis_review_label']} |")
    md += [
        "",
        "Las traducciones de trabajo del alemán son auxiliares analíticos generados para esta capa y **no son texto de la fuente**. Los artículos diplomáticos y las traducciones modernas originales se conservan por separado.",
        "",
        "`ai_assisted=true`; `human_reviewed=false`; `cognacy_judgment=not_performed`; `historical_continuity_judgment=not_performed`; `sound_correspondence_judgment=not_performed`.",
    ]
    REPORT.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
