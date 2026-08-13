# Scientific validation layer

Esta carpeta contiene la fase posterior a la primera pasada editorial integral contra el facsímil. Su propósito es separar con rigor recotejo filológico, evaluación lingüística, normalización auxiliar y correspondencias diacrónicas.

La capa diplomática permanece inmutable como evidencia documental. Ninguna normalización, interpretación semántica o decisión lingüística sobrescribe `headword_diplomatic` ni `article_diplomatic`.

## Estado de entrada y depuración de notas

El corpus tiene 2,495 candidatos facsimilarmente revisados. Tras rechazar 530 falsos límites quedan 1,965 artículos activos provisionales, todos con transcripción diplomática completa IA-asistida.

La primera auditoría de notas mostró que **676 registros tenían alguna nota diplomática**, pero no todas representaban problemas pendientes. Se introdujo `diplomatic_note_state` para distinguirlas: **194 notas editoriales ya resueltas** quedan fuera de la cola científica y **482 registros** permanecen `open_validation`.

La cola abierta se distribuye por triage reproducible en 230 casos de lectura gráfica, 29 de estructura de artículo, 201 de forma histórica rarámuri, 2 de semántica/glosa y 20 casos generales. Estas categorías organizan trabajo; no son diagnósticos lingüísticos.

## RHD-PHIL-001

`RHD-PHIL-001` recotejó directamente contra el facsímil de alta resolución los primeros 50 casos abiertos, correspondientes a pp. 301–320. El resultado fue **25 lecturas confirmadas IA-asistidas, 11 correcciones propuestas y 14 casos todavía irresueltos**.

Las correcciones propuestas viven exclusivamente en `review/philological_review_batch_001.json`. Entre ellas figuran `Mapúieri`, `Napavitſchi`, `Temaſeáli`, `Nachteuje`, `Teé`, `Pultſché`, `Tſchapiboli`, la eliminación de acentos no visibles en formas de `Ehemann`, `Tſchutſchá` y `Raveli`. Ninguna de ellas sobrescribe automáticamente la transcripción diplomática.

Después de este lote hay **50 de 482 casos recotejados** y **432 pendientes**. `next_philological_batch.json` avanza determinísticamente a `RHD-PHIL-002` con los siguientes 50 registros.

## Artefactos

- `uncertainty_queue.json`: 482 problemas explícitamente abiertos, con artículo diplomático, nota y acción recomendada.
- `uncertainty_queue_compact.json`: vista compacta de la cola integral.
- `validation_inventory.json`: conteos del triage inicial y estados independientes de validación.
- `review/philological_review_batch_###.json`: manifiestos append-only de recotejo IA-asistido.
- `next_philological_batch.json`: siguiente cohorte determinista de hasta 50 IDs aún no recotejados.
- `human_review_queue.json`: registros ya recotejados que conservan una ruta explícita de revisión humana/lingüística/disciplinar.
- `validation_progress.json`: avance cuantitativo de la fase sin convertir recotejo IA en verificación humana.

## Semántica de las disposiciones RHD-PHIL

`confirmed_ai_assisted` indica que la nueva inspección sostiene la lectura documental previa. `corrected_ai_assisted` introduce una lectura propuesta porque el facsímil permite una reparación gráfica clara. `unresolved_after_ai_recollation` conserva el problema abierto porque la imagen no permite una decisión suficientemente segura.

Todas estas disposiciones mantienen `human_verified=false`. La cola humana prioriza los casos irresueltos y después las lecturas corregidas o confirmadas que requieren juicio lingüístico, semántico, zoológico, etnomusicológico u otra competencia independiente.

## Siguiente etapa operativa

El siguiente lote automático es `RHD-PHIL-002`. La validación humana futura deberá registrar revisor, fecha, competencia, decisión y evidencia. Las normalizaciones y las correspondencias con Rarámuri Digital se alojarán en capas separadas, con método y confianza explícitos.
