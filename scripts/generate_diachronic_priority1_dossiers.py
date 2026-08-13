#!/usr/bin/env python3
"""Generate reviewer-ready dossiers for tier-1 diachronic adjudication candidates.

The dossiers reorganize already-generated evidence for independent review. They do
not adjudicate meaning, etymology, historical continuity, dialect identity, or
normative equivalence, and they never alter either source corpus.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "data" / "diachronic"
QUEUE = D / "adjudication_queue.json"
SCHEMA = D / "correspondence_schema.json"
OUT = D / "priority1_adjudication_dossiers.json"
COMPACT = D / "priority1_adjudication_dossiers_compact.json"
INDEX = D / "PRIORITY1_ADJUDICATION_INDEX.md"
DOSSIERS = D / "dossiers" / "priority1"


def clean(value):
    return "" if value is None else str(value)


def main():
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    if queue.get("human_reviewed") is not False:
        raise SystemExit("adjudication queue must remain unreviewed before dossier generation")

    tier1 = [x for x in queue.get("records", []) if int(x.get("priority_tier", 0)) == 1]
    DOSSIERS.mkdir(parents=True, exist_ok=True)

    # Remove only deterministic files produced by this generator, so stale dossiers
    # cannot survive a changed queue while unrelated material remains untouched.
    for old in DOSSIERS.glob("RHD-DIA-P1-*_RHD-ADJ-*.md"):
        old.unlink()

    review_decisions = schema.get("review_decisions", [])
    adopted_types = schema.get("adopted_relation_types", [])
    confidence_values = schema.get("confidence_values", [])

    records = []
    compact = []
    for n, source in enumerate(tier1, 1):
        adj_id = source["adjudication_id"]
        dossier_id = f"RHD-DIA-P1-{n:03d}"
        h = source["historical"]
        m = source["modern"]
        rel = source["candidate_relation"]
        evidence = source["review_evidence"]

        dossier = {
            "dossier_id": dossier_id,
            "review_order": n,
            "adjudication_id": adj_id,
            "source_candidate_id": source["source_candidate_id"],
            "source_cohort": source["source_cohort"],
            "status": "awaiting_independent_adjudication",
            "priority": {
                "tier": source["priority_tier"],
                "score": source["priority_score"],
                "reasons": source.get("priority_reasons", []),
                "interpretation": "Review-order heuristic only; priority is not linguistic validation.",
            },
            "historical_evidence": {
                "record_id": h["record_id"],
                "form_diplomatic": h.get("form_diplomatic", ""),
                "matched_component": h.get("matched_component", ""),
                "matched_component_index": h.get("matched_component_index", 1),
                "article_diplomatic": h.get("article_diplomatic", ""),
                "printed_page": h.get("printed_page", ""),
                "preservation_note": "Diplomatic evidence is reproduced for comparison and must not be overwritten by this review.",
            },
            "modern_evidence": {
                "record_id": m["record_id"],
                "headword": m.get("headword", ""),
                "matched_component": m.get("matched_component", ""),
                "translation_raw": m.get("translation_raw", ""),
                "classification": m.get("classification", ""),
                "source_code": m.get("source_code", ""),
                "status": m.get("status", ""),
            },
            "machine_candidate": rel,
            "review_evidence": {
                "historical_component_candidate_count": evidence.get("historical_component_candidate_count", 0),
                "semantic_evidence_available": bool(evidence.get("semantic_evidence_available", False)),
                "automatic_semantic_judgment": "not_performed",
                "automatic_etymological_judgment": "not_performed",
                "automatic_historical_continuity_judgment": "not_performed",
            },
            "independent_adjudication": {
                "reviewer": {"name": "", "affiliation": "", "orcid": "", "expertise": []},
                "review_date": "",
                "decision": "not_assessed",
                "adopted_relation_type": "not_assessed",
                "semantic_relation_note": "",
                "historical_continuity_note": "",
                "dialect_or_variant_note": "",
                "evidence": "",
                "confidence": "not_assessed",
                "reviewer_note": "",
            },
            "allowed_values": {
                "decision": review_decisions,
                "adopted_relation_type": adopted_types,
                "confidence": confidence_values,
            },
            "verification": {
                "human_reviewed": False,
                "semantic_relation_human_assessed": False,
                "historical_continuity_human_assessed": False,
            },
        }
        records.append(dossier)
        compact.append([
            n,
            dossier_id,
            adj_id,
            source["source_candidate_id"],
            source["source_cohort"],
            h["record_id"],
            h.get("matched_component", ""),
            h.get("printed_page", ""),
            m["record_id"],
            m.get("matched_component", ""),
            m.get("translation_raw", ""),
            rel.get("type", ""),
            source["priority_score"],
        ])

        reasons = ", ".join(f"`{clean(x)}`" for x in source.get("priority_reasons", []))
        decision_opts = " | ".join(review_decisions)
        relation_opts = " | ".join(adopted_types)
        confidence_opts = " | ".join(confidence_values)
        filename = f"{dossier_id}_{adj_id}.md"
        lines = [
            f"# {dossier_id} — {adj_id}",
            "",
            "**Estado:** pendiente de adjudicación humana independiente.  ",
            f"**Orden:** {n} de {len(tier1)}.  ",
            f"**Candidato fuente:** `{source['source_candidate_id']}` · cohorte `{source['source_cohort']}`.  ",
            f"**Prioridad:** nivel **1**, puntuación **{source['priority_score']}**.",
            "",
            "> La prioridad sólo ordena la revisión. No constituye una conclusión semántica, etimológica o histórica.",
            "",
            "## Evidencia histórica preservada",
            "",
            f"**Registro:** `{h['record_id']}`  ",
            f"**Página impresa:** **{h.get('printed_page', '')}**  ",
            f"**Forma diplomática:** `{clean(h.get('form_diplomatic'))}`  ",
            f"**Componente comparado:** `{clean(h.get('matched_component'))}`  ",
            "",
            f"**Artículo diplomático:** {clean(h.get('article_diplomatic'))}",
            "",
            "## Evidencia contemporánea preservada",
            "",
            f"**Registro:** `{m['record_id']}`  ",
            f"**Lema:** `{clean(m.get('headword'))}`  ",
            f"**Componente comparado:** `{clean(m.get('matched_component'))}`  ",
            f"**Clasificación:** `{clean(m.get('classification'))}`  ",
            f"**Traducción de la fuente:** {clean(m.get('translation_raw'))}  ",
            f"**Fuente:** `{clean(m.get('source_code'))}` · estado `{clean(m.get('status'))}`.",
            "",
            "## Hipótesis automática que debe evaluarse",
            "",
            f"**Tipo:** `{clean(rel.get('type'))}`  ",
            f"**Alcance declarado:** {clean(rel.get('interpretive_scope'))}",
            "",
            f"**Razones de priorización:** {reasons}",
            "",
            f"**Alternativas para este componente histórico:** **{evidence.get('historical_component_candidate_count', 0)}**.",
            "",
            "No se ha realizado automáticamente ningún juicio de identidad semántica, cognación, continuidad histórica, identidad dialectal ni equivalencia normativa.",
            "",
            "## Adjudicación del revisor independiente",
            "",
            "**Revisor:**  ",
            "**Afiliación:**  ",
            "**ORCID:**  ",
            "**Competencia relevante:**  ",
            "**Fecha:**  ",
            "",
            f"**Decisión:** `{decision_opts}`",
            "",
            f"**Tipo de relación adoptada:** `{relation_opts}`",
            "",
            "**Relación semántica — análisis y evidencia:**  ",
            "",
            "**Continuidad histórica — análisis y evidencia:**  ",
            "",
            "**Variante/dialecto — análisis y evidencia:**  ",
            "",
            f"**Confianza:** `{confidence_opts}`",
            "",
            "**Nota del revisor:**  ",
            "",
            "## Regla de preservación",
            "",
            "La decisión se registra exclusivamente en la capa de correspondencias. No debe sobrescribir el facsímil, OCR, `headword_diplomatic`, `article_diplomatic` ni los registros `RD-######` de Rarámuri Digital. `human_reviewed` permanece en `false` hasta que exista una decisión humana explícita, identificada y trazable.",
            "",
        ]
        (DOSSIERS / filename).write_text("\n".join(lines), encoding="utf-8")

    payload = {
        "dataset": "raramuri-historico-steffel-1809",
        "stage": "diachronic_priority1_independent_adjudication_dossiers",
        "selection_rule": "priority_tier=1 from data/diachronic/adjudication_queue.json, preserving deterministic queue order",
        "count": len(records),
        "human_reviewed": False,
        "automatic_semantic_judgment": False,
        "automatic_etymological_judgment": False,
        "automatic_historical_continuity_judgment": False,
        "records": records,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    compact_payload = {
        "stage": payload["stage"],
        "count": len(compact),
        "human_reviewed": False,
        "fields": [
            "review_order", "dossier_id", "adjudication_id", "source_candidate_id", "source_cohort",
            "historical_record_id", "historical_component", "printed_page", "modern_record_id",
            "modern_component", "modern_translation_raw", "candidate_relation_type", "priority_score",
        ],
        "records": compact,
    }
    COMPACT.write_text(json.dumps(compact_payload, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")

    idx = [
        "# Expedientes de adjudicación diacrónica — prioridad 1",
        "",
        f"Total: **{len(records)}** expedientes. Revisión humana completada: **0**.",
        "",
        "Casos de mayor prioridad documental preparados para revisión independiente. La prioridad no constituye validación lingüística, semántica ni etimológica.",
        "",
        "| Orden | Expediente | ADJ | Fuente | Histórico | Forma histórica | p. | Moderno | Forma moderna | Traducción moderna |",
        "|---:|---|---|---|---|---|---:|---|---|---|",
    ]
    for r in records:
        h = r["historical_evidence"]
        m = r["modern_evidence"]
        fn = f"{r['dossier_id']}_{r['adjudication_id']}.md"
        hf = clean(h.get("matched_component")).replace("|", "/")
        mf = clean(m.get("matched_component")).replace("|", "/")
        tr = clean(m.get("translation_raw")).replace("|", "/")
        idx.append(
            f"| {r['review_order']} | [{r['dossier_id']}](dossiers/priority1/{fn}) | `{r['adjudication_id']}` | "
            f"`{r['source_candidate_id']}` | `{h['record_id']}` | {hf} | {h.get('printed_page', '')} | "
            f"`{m['record_id']}` | {mf} | {tr} |"
        )
    INDEX.write_text("\n".join(idx) + "\n", encoding="utf-8")

    print(f"Generated {len(records)} tier-1 diachronic independent-adjudication dossiers; human reviewed=0")


if __name__ == "__main__":
    main()
