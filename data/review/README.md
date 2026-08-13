# Facsimile review

Este directorio conserva manifiestos editoriales append-only sobre la segmentación OCR de alta cobertura. Los IDs son persistentes: un falso límite se rechaza, pero nunca se recicla. La revisión IA-asistida permanece separada de la validación humana/filológica y lingüística.

## Estado de revisión

`RHD-FR-001`–`RHD-FR-007` agotaron los 609 `high_machine`: 553 aceptados, 56 rechazados y 298 correcciones de lema. `RHD-FR-008`–`RHD-FR-019` agotaron los 1,110 `medium_machine`: 908 aceptados, 202 rechazados y 366 correcciones.

El nivel `low_machine` lleva cinco lotes completos: FR-020 = 40/60; FR-021 = 41/59; FR-022 = 69/31; FR-023 = 58/42; FR-024 = 86/14. En conjunto se han revisado **500 de 716 candidatos bajos: 294 aceptados y 206 falsos límites**. Quedan **216**.

FR-022 fue posteriormente recotejado de manera directa contra las imágenes del facsímil. Sus disposiciones y cuatro correcciones de lema se confirmaron; ya no existe ninguna excepción pendiente de imagen.

`RHD-FR-023` se sitúa en pp. **333–343**, con 58 aceptados, 42 rechazados, cuatro correcciones de lema y 29 correcciones de página. Las reparaciones son `Ob?`, `Recht`, `Schließen` y `Schrauben`.

`RHD-FR-024` se sitúa en pp. **343–347**, con 86 aceptados, 14 rechazados, diez correcciones de lema y 19 correcciones de página. La revisión incluye una auditoría explícita de solapamiento con FR-014: `RHD-S1809-01296` es el catchword `Stute` al pie de p. 344 y se rechaza para no duplicar el artículo de p. 345 ya representado por `RHD-S1809-01297`. En sentido contrario, `RHD-S1809-01293`, OCR `Seh`, se recupera como el artículo genuino `Stroh`.

Las diez correcciones FR-024 son `Stroh`, `Trinker`, `Trinkgeſchirr`, `Uebelthäter`, `Umbringen`, `Ungern`, `Unverdorrt`, `Unverehelicht`, `Unverletzt` y `Verabſcheuen`.

Estado acumulado: **2,219 candidatos revisados, 1,755 aceptados, 464 falsos límites, 695 correcciones, 1,755 transcripciones diplomáticas completas y 2,031 candidatos activos provisionales**. Todos permanecen `human_verified=false`.

## Cola determinista

`scripts/generate_review_queue.py` genera `next_review_queue.json` y `next_review_queue_compact.json` en orden de fuente y excluye todos los IDs ya revisados. Los niveles alto y medio están agotados. Quedan **216 `low_machine`**.

`RHD-FR-025` contiene los siguientes 100 candidatos bajos, desde `RHD-S1809-01419` (`Verbrechen`) hasta `RHD-S1809-01608` (`Zinn`), estimados alrededor de pp. **348–352**. La cohorte sigue íntegramente antes del cambio de dirección de p. 353; los 116 candidatos bajos restantes se aproximarán o cruzarán esa transición.
