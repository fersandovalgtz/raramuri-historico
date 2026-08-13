# Scientific validation layer

Esta carpeta contiene la fase posterior a la primera pasada editorial integral contra el facsímil. Su propósito es separar con rigor recotejo filológico, evaluación lingüística, normalización auxiliar y correspondencias diacrónicas.

La capa diplomática permanece inmutable como evidencia documental. Ninguna normalización, interpretación semántica ni propuesta `RHD-PHIL` sobrescribe `headword_diplomatic` o `article_diplomatic`.

## Estado de entrada

El corpus tiene 2,495 candidatos facsimilarmente revisados. Tras rechazar 530 falsos límites quedan 1,965 artículos activos provisionales, todos con transcripción diplomática completa IA-asistida.

La auditoría de notas distinguió **676 registros con alguna nota diplomática**, de los cuales **194 documentan decisiones editoriales ya resueltas** y **482 permanecen `open_validation`**. El triage inicial distribuye estos 482 casos en 230 lecturas gráficas, 29 problemas de estructura de artículo, 201 formas históricas rarámuri, 2 cuestiones de semántica/glosa y 20 casos generales. Estas categorías son organizativas, no diagnósticos lingüísticos.

## RHD-PHIL-001–010

La serie `RHD-PHIL-001`–`RHD-PHIL-010` agotó la segunda recollación filológica IA-asistida de **los 482/482 casos abiertos**. `validation_progress.json` registra 482 revisados, 0 restantes y `next_ai_recollation_batch=null`.

Cada manifiesto es append-only y usa sólo tres disposiciones:

- `confirmed_ai_assisted`: el nuevo recotejo sostiene la lectura documental previa;
- `corrected_ai_assisted`: se propone una reparación gráfica o textual sustentada por el facsímil, sin sobrescribir la diplomática;
- `unresolved_after_ai_recollation`: la imagen o la estructura documental no permiten cerrar el caso con suficiente seguridad.

Las propuestas PHIL produjeron reparaciones documentales útiles —por ejemplo `Caú. Cajuſchi.`, `Talahipoa`, `Talahúmali`, `Sonúca!`, `Techtéke`, `Atác, oder hatúca`, la restitución de `Mir, netſchi` y `jujega` en `Ich`, así como numerosas correcciones de diacríticos— y conservaron abiertos los casos donde la evidencia no permite una decisión única.

Ninguno de los 482 casos ha sido convertido en validación humana: `human_verified=false`, `philologically_verified_by_human=false` y `linguistically_verified=false` siguen siendo la regla.

## Artefactos

- `uncertainty_queue.json`: 482 problemas explícitamente abiertos, con artículo diplomático, nota y acción recomendada.
- `uncertainty_queue_compact.json`: vista compacta de la cola integral.
- `validation_inventory.json`: conteos del triage inicial y estados independientes de validación.
- `review/philological_review_batch_001.json`–`philological_review_batch_010.json`: segunda inspección IA-asistida de los 482 casos.
- `next_philological_batch.json`: sin cohorte pendiente una vez agotados los 482 registros.
- `human_review_queue.json`: **482 registros** recotejados por IA y preparados para juicio humano independiente.
- `validation_progress.json`: 482/482 recotejados, 0 pendientes automáticos y 0 verificaciones humanas declaradas.

## Ruta humana

La siguiente fase no debe ser otra recollación automática. La revisión independiente deberá registrar, como mínimo, identidad del revisor, fecha, competencia relevante, decisión, evidencia y alcance de la decisión. Conviene distinguir cuatro planos: lectura filológica, análisis lingüístico rarámuri, interpretación semántica/histórica y anotación disciplinar especializada.

Las correcciones `corrected_ai_assisted` deben aceptarse, rechazarse o modificarse explícitamente por esa capa humana antes de alimentar una edición crítica. Los casos `unresolved_after_ai_recollation` deben priorizarse porque contienen la incertidumbre documental residual más fuerte.

## Capas posteriores

Una vez documentada la revisión independiente podrán construirse `normalized_transcription`, relaciones de variantes, correspondencias históricas con Rarámuri Digital y anotación crítica. Esas capas deberán enlazar siempre al `record_id`, método y evidencia y nunca borrar el facsímil, OCR, transcripción diplomática o historial PHIL.
