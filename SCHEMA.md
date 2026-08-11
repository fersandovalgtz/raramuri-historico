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
| `headword_raw` | Lema de presentación de la capa actual; en anclas puede incorporar una restauración editorial documentada. |
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
| `status` | Estado técnico; los candidatos automáticos son `machine_segmented_unverified`. |
| `validation` | Estado de cotejo facsimilar y validación lingüística. |

## Capas

`facsimile` → `ocr_raw` → `machine_segmentation` → `diplomatic_transcription` → `normalized_transcription` → `lexical_entry` → `historical_correspondence`.

La segmentación automática no se confunde con la entidad lexicográfica validada. Una futura fusión o rechazo debe conservar trazabilidad e identificadores históricos.
