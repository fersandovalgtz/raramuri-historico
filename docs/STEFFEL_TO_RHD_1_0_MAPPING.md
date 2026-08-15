# Mapeo Steffel 0.2.0 → núcleo RHD 1.0

Este documento evita una migración destructiva. `data/entries.csv` continúa como maestro operativo de Steffel mientras sus campos se mapean al modelo semántico reusable RHD 1.0.

## 1. Mapeo principal

| Steffel 0.2.0 | RHD 1.0 | Observación |
|---|---|---|
| `record_id` | `record_id` | Persistente y no reciclable. |
| `source_code` | `source_id` / perfil | El perfil resuelve `STEFFEL-1809` a `RHD-SRC-STEFFEL-1809`. |
| `direction` | `direction` | Vocabulario específico de la fuente. |
| `printed_page` | `locators.printed_page` | Conservado. |
| `pdf_page` | `locators.digital_page` | Conservado. |
| `facsimile_column` | `locators.column` | Conservado. |
| `source_ocr_line_start` | `locators.ocr_line_start` | Conservado. |
| `source_ocr_line_end` | `locators.ocr_line_end` | Conservado. |
| `headword_ocr_raw` | `layers.ocr_raw.headword` | Evidencia OCR. |
| `article_ocr_raw` | `layers.ocr_raw.text` | Evidencia OCR. |
| `delimiter` | `layers.segmentation.method/evidence` | Debe conservarse como señal de frontera. |
| `extraction_score` | `layers.segmentation.score` | Puntaje técnico, no certeza filológica. |
| `segmentation_confidence` | `layers.segmentation.confidence` | Vocabulario del perfil Steffel. |
| `status` | `status` + `layers.segmentation.decision` | Conviene separar estado del registro de decisión de frontera. |
| `headword_diplomatic` | `layers.diplomatic.headword` | No sobrescribible. |
| `article_diplomatic` | `layers.diplomatic.text` | No sobrescribible. |
| `diplomatic_status` | `layers.diplomatic.status` | Conservado. |
| `diplomatic_batch` | `layers.diplomatic.activity_id` | Resolver al manifiesto de actividad. |
| `diplomatic_note` | `notes[]` | Nota con estado y responsabilidad. |
| `diplomatic_note_state` | `notes[].status` / validación | Permite enrutar `open_validation`. |
| `human_verified` | `validation[]` derivado | En RHD 1.0 la prueba primaria es el evento humano; la bandera puede seguir como proyección. |
| `diplomatic_review_method` | `provenance[].method` | Método de la actividad. |
| `headword_search` | forma normalizada técnica | No debe confundirse con lectura crítica. |
| `translation_es_editorial` | `lexical.senses[].editorial_translation` | Debe conservar etiqueta editorial moderna. |
| `definition_raw` | `source_gloss` o evidencia OCR según dirección | Requiere mapeo direction-aware, no conversión ciega. |
| `editorial_note` | `notes[]` | Separar historia editorial de incertidumbre abierta. |

## 2. Campos que no deben reinterpretarse automáticamente

### `definition_raw`

El nombre es operacional y no siempre representa una definición lexicográfica en sentido TEI/Lex-0. En DE–RAR puede contener material de equivalencia, ejemplos o estructura interna; en RAR–DE puede funcionar como glosa alemana y material adicional. La transformación a `sense` requiere reglas específicas y, para casos complejos, revisión.

### `headword_raw`

Puede incorporar restauraciones editoriales documentadas. No debe utilizarse como sustituto de `headword_diplomatic`. Para interoperabilidad se debe conservar la cadena de derivación.

### `headword_search`

Es una clave de recuperación. No es una forma histórica, una forma fonológica ni una afirmación de identidad lingüística.

## 3. Decisiones de compatibilidad

1. No reemplazar `entries.csv` durante la fase RHD 1.0 inicial.
2. Añadir un transformador `SteffelOperationalEntry -> RHDCanonicalEntry`.
3. Validar la salida transformada con `schemas/rhd-entry-1.0.schema.json`.
4. Generar TEI desde la capa canónica, no directamente desde supuestos implícitos del CSV.
5. Mantener exports existentes durante una fase de doble generación para comprobar equivalencia y detectar regresiones.

## 4. Deuda técnica identificada

### TEI

El exportador actual declara correctamente que su salida es una capa de investigación y no una edición Lex-0 validada. La siguiente implementación debe:

- distinguir glosa fuente de traducción editorial;
- modelar `form` y `sense` con reglas direction-aware;
- incluir responsabilidad y certeza;
- enlazar facsímil;
- validar contra TEI P5 y el perfil Lex-0 adoptado;
- evitar presentar `definition_raw` como `<def>` de manera automática cuando la estructura documental no lo justifique.

### Procedencia

Los manifiestos existentes constituyen una base fuerte, pero RHD 1.0 debe exponerlos mediante objetos de actividad/agente/derivación para que puedan mapearse a PROV-O.

### Facsímil interoperable

La localización actual por página/columna debe prepararse para URI de Canvas y, cuando exista segmentación espacial suficiente, targets de región IIIF.

## 5. Pruebas de migración

El adaptador Steffel → RHD 1.0 debe probar como mínimo:

- 1,965 registros activos transformables sin pérdida de `record_id`;
- 530 límites rechazados preservables cuando formen parte del inventario de procedencia;
- preservación exacta de transcripción diplomática;
- preservación de los 482 problemas de validación;
- imposibilidad de convertir actividad IA en bandera humana;
- reversibilidad o trazabilidad de todas las normalizaciones;
- igualdad de conteos por página y dirección antes/después de la transformación.

## 6. Prioridad de implementación

1. Crear adaptador canónico sin modificar datos maestros.
2. Añadir tests de conteos e invariantes.
3. Generar JSON canónico para una muestra y después para las 1,965 entradas activas.
4. Reescribir exportador TEI sobre la capa canónica.
5. Añadir IIIF/procedencia interoperable.
6. Sólo después considerar si conviene sustituir el CSV como maestro operativo.

La regla es conservadora: **RHD 1.0 debe aumentar interoperabilidad sin sacrificar la trazabilidad lograda en Steffel 0.2.0.**
