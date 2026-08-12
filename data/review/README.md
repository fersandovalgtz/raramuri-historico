# Facsimile review

Este directorio conserva manifiestos editoriales append-only sobre la segmentación OCR de alta cobertura. Los IDs son persistentes: un falso límite se rechaza, pero nunca se recicla. La revisión IA-asistida permanece separada de la validación humana/filológica y lingüística.

## Estado de revisión

`RHD-FR-001`–`RHD-FR-007` agotaron los 609 `high_machine`: 553 aceptados, 56 rechazados y 298 correcciones de lema. `RHD-FR-008`–`RHD-FR-019` agotaron los 1,110 `medium_machine`: 908 aceptados, 202 rechazados y 366 correcciones.

El nivel `low_machine` lleva dos lotes completos. `RHD-FR-020` resolvió 100 candidatos con 40 aceptados / 60 rechazados; `RHD-FR-021` resuelve otros 100 con **41 aceptados / 59 rechazados**. En conjunto se han cotejado **200 de 716 candidatos bajos: 81 aceptados y 119 falsos límites**.

`RHD-FR-021` se sitúa facsimilarmente en pp. **314–326**, no 316–326, y corrige la página de **37 registros**. Cinco lemas requieren reparación clara: `Flachs`, `Forttragen`, `Hügel`, `Hurtig` y `Jenſeits des Fluſſes`.

Los falsos límites proceden sobre todo de prosa, ejemplos y equivalentes internos de artículos extensos. Casos metodológicos destacados: `RHD-S1809-00577` es una repetición interna de `Gegenwart`; `RHD-S1809-00671` (`Heil`) es el catchword de p. 323, no el artículo de p. 324; `RHD-S1809-00739`, segmentado por OCR como `Hüte`, se recupera facsimilarmente como `Hügel`.

`RHD-DIP-021A`–`RHD-DIP-021E` proporcionan overlay diplomático completo para los **41 arranques aceptados**. El OCR fuente permanece intacto.

Estado acumulado: **1,919 candidatos cotejados, 1,542 aceptados, 377 falsos límites, 677 correcciones, 1,542 transcripciones diplomáticas completas y 2,118 candidatos activos provisionales**. El inventario registra **553** transcripciones con nota explícita de incertidumbre; todos los registros permanecen `human_verified=false`.

## Cola determinista

`scripts/generate_review_queue.py` genera `next_review_queue.json` y `next_review_queue_compact.json` en orden de fuente y excluye todos los IDs ya revisados. Los niveles alto y medio están agotados. Quedan **516 `low_machine`**.

`RHD-FR-022` contiene los siguientes 100 candidatos bajos, desde `RHD-S1809-00789` (`Kieſelſtein`) hasta `RHD-S1809-00964` (OCR `C | ſondere bedeutet eine ver`), estimados automáticamente alrededor de pp. **327–334**. Dado el perfil de FR-020/021, ninguna disposición debe inferirse por apariencia OCR: tipografía, sangría, continuidad de artículo y facsímil siguen siendo determinantes.
