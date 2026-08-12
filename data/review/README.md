# Facsimile review

Este directorio conserva manifiestos editoriales append-only sobre la segmentación OCR de alta cobertura. Los IDs son persistentes: un falso límite se rechaza, pero nunca se recicla. La revisión IA-asistida permanece separada de la validación humana/filológica y lingüística.

## Estado de revisión

`RHD-FR-001`–`RHD-FR-007` agotaron los 609 `high_machine`: 553 aceptados, 56 rechazados y 298 correcciones de lema. `RHD-FR-008`–`RHD-FR-019` agotaron los 1,110 `medium_machine`: 908 aceptados, 202 rechazados y 366 correcciones.

`RHD-FR-020` abre el nivel `low_machine`. De 100 candidatos, **40 son arranques reales y 60 falsos límites**. El facsímil coloca la cohorte en pp. **301–314**, no 301–316, y corrige la página de **52 registros**. Los falsos límites son principalmente fragmentos de prosa o ejemplos de artículos extensos; también aparecen equivalentes rarámuri confundidos con lemas y subentradas internas.

Ocho lemas aceptados requieren corrección clara respecto del OCR: `Berauſchen`, `Beſehen`, `Beſen`, `Betrübt ſeyn`, `Donnerſchlag`, `Ehemann`, `Eben ſo` y `Einſam`. `RHD-S1809-00343` (`Drauſſen`) queda en p. 313: el texto homónimo al pie de p. 312 es únicamente el catchword.

`RHD-DIP-020A`–`RHD-DIP-020E` proporcionan overlay diplomático completo para los 40 arranques aceptados. El OCR fuente permanece intacto.

Estado acumulado: **1,819 candidatos cotejados, 1,501 aceptados, 318 falsos límites, 672 correcciones, 1,501 transcripciones diplomáticas completas y 2,177 candidatos activos provisionales**. El inventario registra 529 transcripciones con nota explícita de incertidumbre; todos los registros permanecen `human_verified=false`.

## Cola determinista

`scripts/generate_review_queue.py` genera `next_review_queue.json` y `next_review_queue_compact.json` en orden de fuente y excluye todos los IDs ya revisados. Los niveles alto y medio están agotados. Quedan **616 `low_machine`**.

`RHD-FR-021` contiene los siguientes 100 candidatos bajos, desde `RHD-S1809-00422` (`Haaſe`) hasta `RHD-S1809-00787` (`Kienholz zum Brennen`), estimados automáticamente alrededor de pp. 316–326. La alta tasa de falsos límites observada en FR-020 refuerza que ninguna disposición debe inferirse por apariencia OCR: tipografía, sangría, continuidad de artículo y facsímil siguen siendo determinantes.
