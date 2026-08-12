# Facsimile review

Este directorio conserva manifiestos editoriales append-only sobre la segmentación OCR de alta cobertura. Los IDs son persistentes: un falso límite se rechaza, pero nunca se recicla. La revisión IA-asistida se mantiene explícitamente separada de la validación humana/filológica y lingüística.

## Estado de revisión

`RHD-FR-001`–`RHD-FR-007` agotaron los 609 candidatos `high_machine`: 553 arranques aceptados, 56 falsos límites y 298 correcciones de lema.

`RHD-FR-008`–`RHD-FR-019` agotaron los **1,110 candidatos `medium_machine`**: **908 arranques aceptados, 202 falsos límites y 366 correcciones claras de lema**.

`RHD-FR-019` contiene los diez candidatos medios finales. Todos aparecían automáticamente en p. 369, pero el cotejo directo los sitúa en la columna derecha de **p. 368** y corrige las diez asignaciones de página. Nueve son artículos reales y `RHD-S1809-02488` (`Bär`) se rechaza porque es la glosa/remisión de `Vohí, Bär, s. Bär.`.

Los nueve lemas recuperados son `Uélameke`, `Uilí`, `Uipáca`, `Veréndo`, `Vissigó`, `Ulé`, `Ululú`, `Upéameke` y `Vuossaguáca`. Todos requieren corrección respecto del OCR candidato. El manifiesto conserva además una nota editorial: `Uélameke` y `Ulé, Spielblatt.` se mantienen tal como están impresos, aunque Merrill et al. (2020) señale problemas históricos en la acentuación del primero y en la glosa alemana del segundo.

`RHD-DIP-019A` proporciona overlay diplomático completo para los **9 arranques aceptados**. El OCR fuente permanece intacto; correcciones, página, columna y transcripción se aplican como capas editoriales reproducibles.

Estado acumulado: **1,719 candidatos cotejados, 1,461 aceptados, 258 falsos límites, 664 correcciones claras, 1,461 transcripciones diplomáticas completas y 2,237 candidatos activos provisionales** de la cobertura original de 2,495. El inventario registra 521 transcripciones con nota explícita de incertidumbre; todos los registros permanecen `human_verified=false`.

La frontera documental está verificada: **p. 368 es la última página del diccionario; p. 369 inicia el apéndice**.

## Cola determinista

`scripts/generate_review_queue.py` genera `next_review_queue.json` y `next_review_queue_compact.json` a partir de la capa regenerada y todos los manifiestos append-only. Selecciona IDs no revisados en orden de fuente, agotando `medium_machine` antes de `low_machine`.

Los niveles `high_machine` y `medium_machine` están agotados. Quedan **716 `low_machine`**. La siguiente cohorte, `RHD-FR-020`, contiene los primeros 100 candidatos de baja confianza, desde `RHD-S1809-00061` (`Vorrede erinnert habe`) hasta `RHD-S1809-00421` (`Vogel`), automáticamente asignados alrededor de pp. 301–316. La cola incluye numerosos fragmentos claramente sospechosos de prosa o glosa; ninguno debe rechazarse sólo por apariencia OCR, pero se espera una tasa de falsos límites sensiblemente mayor y el facsímil seguirá siendo la autoridad.