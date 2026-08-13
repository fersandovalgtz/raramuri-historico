# Scientific validation layer

Esta carpeta contiene la fase posterior a la primera pasada editorial integral contra el facsímil. Su propósito es separar con rigor recotejo filológico, evaluación lingüística, normalización auxiliar y correspondencias diacrónicas.

La capa diplomática permanece inmutable como evidencia documental. Ninguna normalización, interpretación semántica ni propuesta `RHD-PHIL` sobrescribe `headword_diplomatic` o `article_diplomatic`.

## Estado de entrada

El corpus tiene 2,495 candidatos facsimilarmente revisados. Tras rechazar 530 falsos límites quedan 1,965 artículos activos provisionales, todos con transcripción diplomática completa IA-asistida.

La auditoría de notas distinguió **676 registros con alguna nota diplomática**, de los cuales **194 documentan decisiones editoriales ya resueltas** y **482 permanecen `open_validation`**. El triage inicial distribuye estos 482 casos en 230 lecturas gráficas, 29 problemas de estructura de artículo, 201 formas históricas rarámuri, 2 cuestiones de semántica/glosa y 20 casos generales. Estas categorías son organizativas, no diagnósticos lingüísticos.

## RHD-PHIL-001–010

La serie `RHD-PHIL-001`–`RHD-PHIL-010` agotó la segunda recollación filológica IA-asistida de **los 482/482 casos abiertos**. `validation_progress.json` registra 482 revisados, 0 restantes y `next_ai_recollation_batch=null`.

Cada manifiesto es append-only y usa sólo tres disposiciones: `confirmed_ai_assisted`, `corrected_ai_assisted` y `unresolved_after_ai_recollation`. Ninguna sobrescribe automáticamente la transcripción diplomática.

La reinspección de alta resolución y, en los últimos casos, a **600 dpi**, produjo reparaciones documentales como `Caú. Cajútſchi.`, `Talahipoa`, `Talahúmali`, `Somúca!`, `Painaguéameke`, `Nachcatule`, `Tamatsiame`, `Tepágatigameke`, `Techtéke`, `Atác, oder hatúca` y `Tſeſtarácameke, oder Stácameke`. También corrigió falsos diacríticos y conservó abiertos sólo los casos donde la evidencia sigue sin permitir una decisión documental única.

Ninguno de los 482 casos ha sido convertido en validación humana: `human_verified=false`, `philologically_verified_by_human=false` y `linguistically_verified=false` siguen siendo la regla.

## Prioridad para revisión independiente

`human_review_priority.json` y su vista compacta se generan determinísticamente a partir de `human_review_queue.json`. Después de la recollación final a alta resolución, la cola queda así:

- **Prioridad 1 — 46 registros:** `unresolved_after_ai_recollation`; la segunda inspección IA no logró cerrar el problema documental.
- **Prioridad 2 — 152 registros:** `corrected_ai_assisted`; existe una reparación propuesta que debe ser aceptada, modificada o rechazada por una persona.
- **Prioridad 3 — 284 registros:** `confirmed_ai_assisted`; la lectura documental se sostiene, pero permanece juicio lingüístico, semántico, histórico o disciplinar independiente.

Dentro de cada prioridad, los registros se ordenan por página impresa y después por `record_id` persistente. La prioridad organiza trabajo y no modifica ninguna bandera de verificación.

## Artefactos

- `uncertainty_queue.json`: 482 problemas explícitamente abiertos, con artículo diplomático, nota y acción recomendada.
- `uncertainty_queue_compact.json`: vista compacta de la cola integral.
- `validation_inventory.json`: conteos del triage inicial y estados independientes de validación.
- `review/philological_review_batch_001.json`–`philological_review_batch_010.json`: segunda inspección IA-asistida de los 482 casos.
- `next_philological_batch.json`: sin cohorte pendiente una vez agotados los 482 registros.
- `human_review_queue.json`: 482 registros recotejados por IA y preparados para juicio humano independiente.
- `human_review_priority.json` / `human_review_priority_compact.json`: prioridad reproducible **46 / 152 / 284**.
- `HUMAN_REVIEW_PROTOCOL.md`: procedimiento y semántica de la revisión independiente.
- `human_review_template.json`: plantilla de decisión que separa filología, lingüística, semántica/historia y revisión disciplinar.
- `validation_progress.json`: 482/482 recotejados, 0 pendientes automáticos y 0 verificaciones humanas declaradas.

## Ruta humana

La siguiente fase no debe ser otra recollación automática general. La revisión independiente deberá registrar identidad del revisor, fecha, competencia relevante, decisión, evidencia y alcance de la decisión. Conviene distinguir cuatro planos: lectura filológica, análisis lingüístico rarámuri, interpretación semántica/histórica y anotación disciplinar especializada.

Los **46 casos de prioridad 1** deben revisarse primero. Después deben adjudicarse las **152 correcciones propuestas**. Las **284 confirmaciones IA-asistidas** pueden requerir todavía análisis lingüístico o disciplinar aunque su lectura gráfica sea estable.

Una nueva reinspección automática sólo se justifica de manera puntual si aparece una imagen fuente mejor o un indicio documental concreto; no debe usarse para convertir mecánicamente incertidumbre legítima en falsa certeza.

## Capas posteriores

Una vez documentada la revisión independiente podrán construirse `normalized_transcription`, relaciones de variantes, correspondencias históricas con Rarámuri Digital y anotación crítica. Esas capas deberán enlazar siempre al `record_id`, método y evidencia y nunca borrar el facsímil, OCR, transcripción diplomática o historial PHIL.
