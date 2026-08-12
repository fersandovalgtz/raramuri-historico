# Facsimile review

Este directorio conserva manifiestos editoriales append-only sobre la segmentación OCR de alta cobertura. Los IDs son persistentes: un falso límite se rechaza, pero nunca se recicla. La revisión IA-asistida se mantiene explícitamente separada de la validación humana/filológica y lingüística.

## Estado de revisión

`RHD-FR-001`–`RHD-FR-007` agotaron los 609 candidatos `high_machine`: 553 arranques aceptados, 56 falsos límites y 298 correcciones de lema.

`RHD-FR-008`–`RHD-FR-017` cubren los primeros diez lotes sistemáticos de 100 registros `medium_machine`. Tras FR-017 se han revisado **1,000 de 1,110 candidatos medios**: **812 aceptados y 188 rechazados**.

`RHD-FR-017` contiene **100 candidatos revisados, 91 arranques aceptados, 9 falsos límites y 90 correcciones claras de lema**. El cotejo directo sitúa la cohorte en pp. **360–364**, no 360–365, y corrige la página de **24 registros**.

Los nueve límites rechazados son glosas alemanas capturadas como supuestos lemas inversos: `Brod`, `Mehr`, `Kriegen`, `Zange`, `Belohnen`, `Bekennen`, `Wahrheit`, `Weg` y `Nicht viel`. Entre las recuperaciones figuran `Lessíameke`, `Moorápera`, `Nachtétuje`, `Nacuguíta`, `Nassípasic`, `Noitsámela`, `Ossanaguóameke`, `Pitschabúrameke`, `Rachtábatsáboa` y `Rhaná`.

`RHD-DIP-017A`–`RHD-DIP-017J` proporcionan overlay diplomático completo para los **91 arranques aceptados**. El OCR fuente permanece intacto; correcciones, página, columna y transcripción se aplican como capas editoriales reproducibles.

Estado acumulado: **1,609 candidatos cotejados, 1,365 aceptados, 244 falsos límites, 573 correcciones claras, 1,365 transcripciones diplomáticas completas y 2,251 candidatos activos provisionales** de la cobertura original de 2,495.

## Cola determinista

`scripts/generate_review_queue.py` genera `next_review_queue.json` y `next_review_queue_compact.json` a partir de la capa regenerada y todos los manifiestos append-only. Selecciona los primeros 100 IDs no revisados en orden de fuente, agotando `medium_machine` antes de `low_machine`.

Quedan **110 `medium_machine`** y 716 `low_machine`. `RHD-FR-018` tomará los siguientes 100, desde `RHD-S1809-02234` (`Rheneke`) hasta `RHD-S1809-02478` (`Vaflürichi`). La cola automática alcanza p. 369, pero el vocabulario propiamente dicho termina en p. 368 y el apéndice empieza en p. 369; por ello, la pertenencia de los candidatos finales al cuerpo lexicográfico deberá decidirse exclusivamente mediante cotejo documental.