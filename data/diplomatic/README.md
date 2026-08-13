# Diplomatic transcription layer

Este directorio contiene overlays editoriales append-only producidos mediante cotejo IA-asistido contra el facsímil Steffel 1809. El facsímil es autoritativo; el OCR se conserva como evidencia secundaria. Todos los registros actuales tienen `human_verified=false`.

## Cobertura

La capa diplomática cubre **los 1,965 artículos activos aceptados** después de revisar los 2,495 candidatos originales. Esto equivale a `full_active_corpus_coverage=true` y `full_diplomatic_transcription_completed=true` en la fase editorial IA-asistida. Las banderas se calculan en `scripts/apply_review_overrides.py`: requieren que todos los candidatos estén revisados, que el número de transcripciones coincida con los arranques aceptados y que no existan lotes pendientes de recotejo directo de imagen.

El inventario registra **676 transcripciones con nota explícita de incertidumbre**. Estas notas no significan ausencia de facsímil: señalan lecturas que, aun directamente cotejadas, merecen validación filológica o lingüística independiente.

## Lotes de cierre

`RHD-DIP-026A`–`F` aportan las 54 transcripciones aceptadas del lote direction-aware que cruza la inversión de p. 353. En la sección rarámuri→alemán se preserva explícitamente la forma rarámuri como headword y el alemán como glosa.

`RHD-DIP-027A` contiene las diez últimas transcripciones de la cola `low_machine` y cierra documentalmente el diccionario en p. 368, antes del apéndice de p. 369.

`RHD-DIP-028A`–`F` incorporan las 60 anclas curatoriales que antes permanecían `unverified_ocr`. Con esta serie, las 60 anclas quedan sincronizadas con `data/entries.csv` y poseen transcripción diplomática completa.

## Alcance editorial

Las particularidades históricas del impreso —grafía, ſ larga, diacríticos, variantes, ejemplos, notas etnográficas y formulaciones culturales históricas— se preservan como evidencia documental cuando el facsímil las sustenta. Su conservación no implica adhesión editorial. Las normalizaciones futuras deberán mantenerse separadas de la capa diplomática.

La cobertura completa de esta capa **no equivale a validación humana o lingüística completa**. El siguiente trabajo pertinente es revisar independientemente los 676 registros con incertidumbre, confirmar lecturas difíciles y documentar las decisiones de validación sin sobrescribir la evidencia diplomática.

Los campos diplomáticos se aplican mediante `scripts/apply_review_overrides.py` y se propagan a CSV, JSON, XML, TEI, SQLite y la proyección pública.
