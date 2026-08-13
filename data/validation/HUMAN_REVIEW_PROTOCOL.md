# Protocolo de revisión humana independiente

Este protocolo define la fase posterior a `RHD-PHIL-001`–`RHD-PHIL-010`. Su propósito es impedir que una segunda lectura IA-asistida sea presentada como validación humana o lingüística.

## Principios

1. **No sobrescritura.** La revisión humana no modifica el facsímil, OCR bruto, transcripción diplomática ni manifiestos PHIL. Toda decisión vive en una capa derivada enlazada al `record_id`.
2. **Alcance explícito.** Una persona puede confirmar una lectura filológica sin validar una interpretación lingüística, semántica, histórica o disciplinar.
3. **Evidencia trazable.** Toda decisión debe citar página impresa, facsímil utilizado y, cuando corresponda, fuentes comparativas externas.
4. **Competencia declarada.** El registro debe indicar nombre, afiliación, ORCID cuando exista y área de competencia relevante del revisor.
5. **Incertidumbre permitida.** `remain_unresolved` es una decisión válida. No se fuerza una solución para alcanzar una tasa artificial de completitud.

## Orden de prioridad

`human_review_priority.json` ordena los 482 casos de la siguiente manera:

- **Prioridad 1:** `unresolved_after_ai_recollation`. La segunda inspección IA no logró cerrar la lectura o estructura documental.
- **Prioridad 2:** `corrected_ai_assisted`. Existe una reparación propuesta que una persona debe aceptar, modificar o rechazar.
- **Prioridad 3:** `confirmed_ai_assisted`. La lectura documental es estable, pero permanece una ruta lingüística, semántica, histórica o disciplinar independiente.

Dentro de cada prioridad se ordena por página impresa y después por `record_id` persistente.

## Unidad de decisión

Cada revisión humana debe registrar como mínimo:

- `record_id`;
- revisor, afiliación y competencia;
- fecha de revisión;
- decisión filológica;
- lectura adoptada si cambia la diplomática o la propuesta PHIL;
- evidencia y justificación;
- nivel de confianza;
- decisión lingüística separada (`not_assessed` es admisible);
- decisión semántica/histórica separada cuando proceda;
- decisión disciplinar especializada cuando proceda;
- relación con la propuesta PHIL: `confirm`, `accept_proposed_correction`, `modify_proposed_correction`, `reject_proposed_correction` o `not_applicable`.

## Estados recomendados

### Decisión filológica

- `confirmed_diplomatic`
- `accepted_ai_proposed_correction`
- `human_corrected_reading`
- `remain_unresolved`
- `not_assessed`

### Decisión lingüística

- `confirmed`
- `corrected`
- `variant_identified`
- `uncertain`
- `not_assessed`

### Decisión semántica / histórica

- `confirmed_source_gloss`
- `clarified_historical_sense`
- `requires_contextual_annotation`
- `uncertain`
- `not_assessed`

### Decisión disciplinar

- `confirmed`
- `corrected`
- `requires_specialist`
- `not_assessed`

## Condiciones para marcar verificación

`human_verified=true` sólo puede establecerse cuando existe una decisión humana explícita y trazable sobre el alcance declarado. `philologically_verified_by_human=true` requiere una decisión filológica cerrada distinta de `remain_unresolved` y `not_assessed`. `linguistically_verified=true` requiere revisión lingüística independiente; nunca se deriva automáticamente de una confirmación filológica.

## Adopción en una edición crítica

Una lectura humana adoptada no debe reemplazar físicamente `article_diplomatic`. Debe alimentar una futura capa `critical_reading` o `normalized_transcription`, vinculada al `record_id` y a la decisión humana correspondiente. La transcripción diplomática continúa siendo el testimonio documental reproducible.

## Casos históricos sensibles

Los pasajes coloniales, etnocéntricos, misioneros o peyorativos se transcriben como evidencia de la fuente. Una revisión humana puede añadir contexto crítico, pero no debe suavizar retrospectivamente el texto histórico ni presentar sus afirmaciones como hechos contemporáneamente validados.
