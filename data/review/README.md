# Facsimile review

Este directorio conserva manifiestos editoriales append-only sobre la segmentación OCR de alta cobertura. Los IDs son persistentes: un falso límite se rechaza, pero nunca se recicla. La revisión IA-asistida permanece separada de la validación humana/filológica y lingüística.

## Estado de revisión

`RHD-FR-001`–`RHD-FR-007` agotaron los 609 `high_machine`: 553 aceptados, 56 rechazados y 298 correcciones. `RHD-FR-008`–`RHD-FR-019` agotaron los 1,110 `medium_machine`: 908 aceptados, 202 rechazados y 366 correcciones.

El nivel `low_machine` lleva seis lotes completos: FR-020 = 40/60; FR-021 = 41/59; FR-022 = 69/31; FR-023 = 58/42; FR-024 = 86/14; FR-025 = 86/14. En conjunto se han revisado **600 de 716 candidatos bajos: 380 aceptados y 220 falsos límites**. Quedan **116**.

`RHD-FR-025` se sitúa en pp. **347–352**, con 86 aceptados, 14 rechazados, diez correcciones de lema y 27 correcciones de página. Las reparaciones son `Verfault`, `Verleihen`, `Verlobt`, `Vier`, `Vor`, `Vorlängst`, `Wie immer`, `Wiederholen`, `Wo` y `Ziegelerde`.

Los rechazos muestran otra vez por qué el nivel bajo requiere imagen directa: frases internas de artículos extensos, equivalentes rarámuri, cross-references y repeticiones del propio lema fueron segmentados como candidatos independientes por el OCR.

Estado acumulado: **2,319 candidatos revisados, 1,841 aceptados, 478 falsos límites, 705 correcciones, 1,841 transcripciones diplomáticas completas y 2,017 candidatos activos provisionales**. El inventario registra **620** notas explícitas de incertidumbre. Todos permanecen `human_verified=false`.

## Cola determinista y transición de p. 353

`scripts/generate_review_queue.py` genera `next_review_queue.json` y `next_review_queue_compact.json` en orden de fuente y excluye todos los IDs ya revisados. Quedan **116 `low_machine`**.

`RHD-FR-026` toma los siguientes 100, desde `RHD-S1809-01609` (`Zinnen`) hasta `RHD-S1809-02404` (OCR `Tofacameke Weiß`). Esta cohorte es especial: comienza todavía en la sección alemán→rarámuri de p. 352, cruza el cambio de dirección dentro de p. 353 y continúa por la sección rarámuri→alemán hasta aproximadamente p. 367. Por tanto, la validez de un límite y la naturaleza del headword deben evaluarse con la dirección documental correspondiente a cada registro. Tras FR-026 quedarán 16 candidatos bajos.
