# Esquema de datos

## Identidad

- Dataset: `0.1.0-mvp`.
- Entrada: `RHD-S1809-#####`.
- Fuente inicial: `STEFFEL-1809`.
- Codificación: UTF-8.

## Entrada maestra

| Campo | Regla |
|---|---|
| `record_id` | Identificador persistente de la transcripción estructurada. |
| `source_code` | Fuente documental controlada. |
| `direction` | `DE-RAR` o `RAR-DE`. |
| `headword_raw` | Forma conservada de la fuente/OCR cotejado. Nunca se sobrescribe. |
| `headword_search` | Clave técnica de búsqueda; reemplaza ſ por s y elimina diacríticos solo para recuperación. |
| `gloss_de_raw` | Glosa alemana tal como se conserva en la capa de trabajo. |
| `translation_es_editorial` | Traducción española añadida por el proyecto; no forma parte de Steffel. |
| `printed_page` | Página de la edición de 1809. |
| `pdf_page` | Página física del facsímil suministrado. |
| `source_ocr_line` | Línea de evidencia dentro del TXT suministrado. |
| `editorial_note` | Advertencias, variantes o decisiones editoriales. |
| `status` | Estado técnico de extracción. |
| `validation` | Estado de cotejo/validación. |

## Capas previstas

`facsimile` → `ocr_raw` → `diplomatic_transcription` → `normalized_transcription` → `lexical_entry` → `historical_correspondence`.

## Correspondencias diacrónicas futuras

Las relaciones con Rarámuri Digital se almacenarán aparte, con `historical_entry_id`, `rd_entry_id`, `relation_type`, `confidence`, `method`, `review_status` y `reviewer`.
