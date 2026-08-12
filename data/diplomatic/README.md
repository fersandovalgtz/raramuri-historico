# Diplomatic transcription layer

Este directorio contiene overlays editoriales append-only producidos mediante comparación visual directa con el facsímil Steffel 1809. El facsímil es autoritativo; el OCR se conserva como ayuda secundaria y nunca como fuente de verdad para límites, página, columna o lectura del artículo.

Las transcripciones preservan la formulación y puntuación documentales sin codificar los saltos tipográficos de línea. El método es `visual_facsimile_transcription_ai_assisted`; todos los registros actuales tienen `human_verified=false`.

`RHD-DIP-001A`–`RHD-DIP-007A` cubren los 553 arranques aceptados del nivel `high_machine`. Las series `RHD-DIP-008A`–`RHD-DIP-019A` proporcionan cobertura completa para cada arranque aceptado del nivel `medium_machine` ya agotado.

`RHD-DIP-019A` añade **9 artículos completos** de `RHD-FR-019`, todos localizados por cotejo en la columna derecha de **p. 368** pese a haber sido asignados automáticamente a p. 369. Las entradas son `Uélameke`, `Uilí`, `Uipáca`, `Veréndo`, `Vissigó`, `Ulé`, `Ululú`, `Upéameke` y `Vuossaguáca`.

La capa diplomática conserva la fuente incluso cuando existe comentario editorial posterior. Así, `Uélameke` mantiene el acento impreso y `Ulé, Spielblatt.` conserva la glosa alemana del testimonio de 1809. Merrill et al. (2020, DOI `10.47807/UNISON.8`) identifica ambas como formas potencialmente problemáticas, pero esta colación secundaria no sustituye ni corrige silenciosamente el facsímil.

La capa acumulada contiene **1,461 transcripciones diplomáticas IA-asistidas**, exactamente los **1,461 arranques aceptados entre 1,719 candidatos cotejados**. El inventario registra **521 transcripciones con nota explícita de incertidumbre**. Todos los registros permanecen `human_verified=false`.

La revisión de límites y la transcripción diplomática IA-asistida están completas para los **609 `high_machine`** y los **1,110 `medium_machine`**. Esto no constituye cierre global: quedan **716 `low_machine`** y toda la validación humana/lingüística independiente.

La frontera **diccionario p. 368 / apéndice p. 369** está verificada directamente. Ninguna transcripción diplomática del diccionario se asigna a p. 369.

Los campos diplomáticos son aplicados por `scripts/apply_review_overrides.py` y propagados a JSON, XML, TEI, SQLite y la proyección pública. El OCR fuente no se modifica.

La siguiente etapa es `RHD-FR-020`, primer lote `low_machine`, con los primeros 100 de 716 candidatos de baja confianza. Dada la abundancia de fragmentos internos y prosa OCR en esa cohorte, la proporción de transcripciones diplomáticas resultante dependerá del cotejo de límites y no debe anticiparse desde la cola automática.