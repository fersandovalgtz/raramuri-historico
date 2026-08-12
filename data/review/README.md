# Facsimile review

Este directorio conserva manifiestos editoriales append-only sobre la segmentación OCR de alta cobertura. Los IDs son persistentes: un falso límite se rechaza, pero nunca se recicla. La revisión IA-asistida permanece separada de la validación humana/filológica y lingüística, y cada manifiesto conserva el método de evidencia realmente utilizado.

## Estado de revisión

`RHD-FR-001`–`RHD-FR-007` agotaron los 609 `high_machine`: 553 aceptados, 56 rechazados y 298 correcciones de lema. `RHD-FR-008`–`RHD-FR-019` agotaron los 1,110 `medium_machine`: 908 aceptados, 202 rechazados y 366 correcciones.

El nivel `low_machine` lleva tres lotes completos. FR-020 produjo 40 aceptados / 60 rechazados; FR-021, 41 / 59; FR-022, **69 / 31**. En conjunto se han revisado **300 de 716 candidatos bajos: 150 aceptados y 150 falsos límites**. Quedan **416**.

`RHD-FR-022` alinea la cohorte en pp. **326–333**, no 327–334, y corrige la página de **61 registros**. Cuatro lemas se reparan: `Knüttel`, `Koſt`, `Kriegen` y `Lehrling`. Entre los falsos límites aparecen prosa de `Kranich`, `Kraut`, `Kukuck`, `Leopard`, `Mädchen`, `Mästen` y `Mutter`, equivalentes rarámuri internos y frases subordinadas.

## Excepción documental de FR-022

FR-022 no tuvo relectura directa de las imágenes del facsímil en el runtime de producción. Su manifiesto declara `direct_facsimile_image_reinspection=false`. La revisión usa el OCR primario preservado como evidencia textual, la arquitectura de página/columnas previamente verificada visualmente y una transcripción académica de la versión publicada únicamente como colación secundaria.

El lote debe ser recotejado más adelante contra imagen directa. El script `apply_review_overrides.py` conserva esta diferencia metodológica en el inventario mediante `mixed_ai_assisted_editorial_collation`, una lista de métodos y `direct_facsimile_image_recheck_pending_batches`. No se presenta FR-022 como revisión visual ni humana.

`RHD-DIP-022A`–`RHD-DIP-022G` proporcionan overlay diplomático para los **69 arranques aceptados**. El OCR fuente permanece intacto.

Estado acumulado: **2,019 candidatos revisados, 1,611 aceptados, 408 falsos límites, 681 correcciones, 1,611 transcripciones diplomáticas completas y 2,087 candidatos activos provisionales**. El inventario registra **622** transcripciones con nota explícita de incertidumbre; todos los registros permanecen `human_verified=false`.

## Cola determinista

`scripts/generate_review_queue.py` genera `next_review_queue.json` y `next_review_queue_compact.json` en orden de fuente y excluye todos los IDs ya revisados. Los niveles alto y medio están agotados. Quedan **416 `low_machine`**.

`RHD-FR-023` contiene los siguientes 100 candidatos bajos, desde `RHD-S1809-00965` (`Nachſehen`) hasta `RHD-S1809-01238` (`Spielplatz`), estimados automáticamente alrededor de pp. **334–343**. Ninguna disposición se considera validación humana; cuando no haya inspección directa de imagen, la excepción deberá declararse en el manifiesto correspondiente.
