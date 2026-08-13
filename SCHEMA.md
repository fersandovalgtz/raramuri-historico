# Esquema de datos / Data Schema

## Identidad y versiones

- Dataset: `0.2.0`.
- Identificador: `RHD-S1809-#####`, persistente y no reciclable.
- Fuente: `STEFFEL-1809`.
- Direcciones: `DE-RAR` y `RAR-DE`.
- Codificación: UTF-8.

## Capa maestra `data/entries.csv`

| Campo | Función |
|---|---|
| `record_id` | Identificador persistente. Los 60 IDs iniciales se preservan. |
| `source_code` | Fuente documental controlada. |
| `direction` | Dirección lexicográfica. |
| `headword_raw` | Lema de presentación de la capa actual; puede incorporar una restauración editorial documentada. |
| `headword_ocr_raw` | Prefijo exactamente segmentado desde la línea OCR, antes de correcciones editoriales. |
| `headword_search` | Clave técnica normalizada para recuperación. |
| `definition_raw` | Contenido OCR asociado al candidato después del lema. |
| `translation_es_editorial` | Traducción española propia solo cuando existe en la capa curada; nunca atribuida a Steffel. |
| `editorial_note` | Decisión o advertencia editorial. |
| `article_ocr_raw` | Bloque OCR completo asignado al candidato. |
| `printed_page` / `pdf_page` | Localización documental. |
| `source_ocr_line_start` / `source_ocr_line_end` | Rango exacto de evidencia dentro del TXT primario. |
| `delimiter` | Señal tipográfica usada para proponer el límite. |
| `extraction_score` | Puntaje técnico del segmentador. |
| `segmentation_confidence` | `curated_anchor`, `high_machine`, `medium_machine` o `low_machine`. |
| `curated_anchor` | Indica pertenencia a las 60 anclas iniciales. |
| `extraction_method` | Método reproducible empleado. |
| `status` | Estado técnico/editorial del candidato. |
| `validation` | Estado de cotejo facsimilar y validación lingüística. |
| `facsimile_column` | Columna documental cotejada. |
| `headword_diplomatic` | Lema transcrito diplomáticamente desde el facsímil. |
| `article_diplomatic` | Artículo completo en transcripción diplomática IA-asistida. |
| `diplomatic_status` / `diplomatic_batch` | Estado y lote de procedencia de la capa diplomática. |
| `diplomatic_note` | Nota editorial asociada a la lectura diplomática. |
| `diplomatic_note_state` | `none`, `resolved_editorial_note` u `open_validation`; distingue notas históricas ya resueltas de problemas científicos todavía abiertos. |
| `human_verified` | Sólo puede ser verdadero cuando exista revisión humana independiente explícitamente documentada. |
| `diplomatic_review_method` | Método de cotejo de la transcripción diplomática. |

## Capa de validación científica `data/validation/`

La capa diplomática no se sobrescribe. Los problemas abiertos se seleccionan únicamente cuando `diplomatic_note_state=open_validation`.

`uncertainty_queue.json` conserva la cola integral de casos abiertos. Su clasificación (`graphic_reading`, `article_structure`, `historical_raramuri_form`, `semantic_or_gloss`, `general_open_validation`) es un **triage determinista**, no una validación lingüística.

Los manifiestos `data/validation/review/philological_review_batch_###.json` registran un segundo recotejo IA-asistido contra el facsímil. Cada registro usa una de tres disposiciones:

- `confirmed_ai_assisted`: la lectura documental previa queda sostenida por el nuevo recotejo;
- `corrected_ai_assisted`: se propone una lectura corregida, preservando siempre la diplomática anterior;
- `unresolved_after_ai_recollation`: la imagen no permite cerrar el problema sin revisión independiente.

`next_philological_batch.json` contiene los siguientes 50 IDs abiertos aún no recotejados. `human_review_queue.json` contiene únicamente registros ya recotejados por IA que conservan una ruta humana, filológica, lingüística, semántica o disciplinar. `validation_progress.json` resume el avance sin transformar ninguna de esas revisiones en una credencial humana.

Una corrección propuesta en `RHD-PHIL` no modifica `headword_diplomatic` ni `article_diplomatic`. Si en una edición crítica posterior se adopta una lectura revisada, deberá vivir en una capa derivada con vínculo al `record_id`, método, responsable, fecha y evidencia.

## Capas

`facsimile` → `ocr_raw` → `machine_segmentation` → `diplomatic_transcription` → `ai_philological_recollation` → `independent_human_validation` → `normalized_transcription` → `lexical_entry` → `historical_correspondence`.

La segmentación automática no se confunde con la entidad lexicográfica validada. La transcripción diplomática integral tampoco equivale a validación humana. Toda futura fusión, rechazo, normalización o correspondencia debe conservar trazabilidad e identificadores históricos.
