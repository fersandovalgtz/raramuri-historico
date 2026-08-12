# Facsimile review

Este directorio conserva manifiestos editoriales append-only sobre la segmentación OCR de alta cobertura. Los IDs son persistentes: un falso límite se rechaza, pero nunca se recicla. La revisión IA-asistida se mantiene explícitamente separada de la validación humana/filológica y lingüística.

## Estado de revisión

`RHD-FR-001`–`RHD-FR-007` agotaron los 609 candidatos `high_machine`: 553 arranques aceptados, 56 falsos límites y 298 correcciones de lema.

`RHD-FR-008`–`RHD-FR-018` cubren los primeros once lotes sistemáticos de 100 registros `medium_machine`. Tras FR-018 se han revisado **1,100 de 1,110 candidatos medios**: **899 aceptados y 201 rechazados**.

`RHD-FR-018` contiene **100 candidatos revisados, 87 arranques aceptados, 13 falsos límites y 82 correcciones claras de lema**. El cotejo directo sitúa la cohorte en pp. **364–368**, no 365–369, y corrige la página de **45 registros**.

Los falsos límites incluyen glosas alemanas como `Gott`, `Weiß`, `Nein`, `Spielen`, `Winkel`, `Maus` y `Eichhörnchen`; el catchword `Sulála`; el running header `Wörterbüch`; el ejemplo interno `Sulatschic`; y `Tuſchi`, que no tiene correlato de inicio de artículo en el facsímil. Entre las recuperaciones figuran `Rhenéke`, `R-guála`, `Schugiámeke`, `Sinépi putié`, `Tajenaságo`, `Telsiguála`, `Tótschi`, `Tschie`, `Tschulugéameke`, `Tulchilki` y `Vassúritschi`.

El manifiesto fija además la frontera **diccionario p. 368 / apéndice p. 369**. Ningún registro de FR-018 se trata como artículo lexicográfico de p. 369; los desplazamientos de OCR se corrigen a p. 368 sólo cuando el facsímil los sustenta.

`RHD-DIP-018A`–`RHD-DIP-018I` proporcionan overlay diplomático completo para los **87 arranques aceptados**. El OCR fuente permanece intacto; correcciones, página, columna y transcripción se aplican como capas editoriales reproducibles.

Estado acumulado: **1,709 candidatos cotejados, 1,452 aceptados, 257 falsos límites, 655 correcciones claras, 1,452 transcripciones diplomáticas completas y 2,238 candidatos activos provisionales** de la cobertura original de 2,495.

## Cola determinista

`scripts/generate_review_queue.py` genera `next_review_queue.json` y `next_review_queue_compact.json` a partir de la capa regenerada y todos los manifiestos append-only. Selecciona IDs no revisados en orden de fuente, agotando `medium_machine` antes de `low_machine`.

Quedan **10 `medium_machine`** y 716 `low_machine`. `RHD-FR-019` contiene esos diez candidatos finales, desde `RHD-S1809-02480` (`Uelemeke`) hasta `RHD-S1809-02494` (`Vuoſſaguaca`). Todos aparecen automáticamente en p. 369, que es ya el apéndice; por ello FR-019 debe decidir exclusivamente mediante facsímil si son entradas rezagadas de p. 368, artefactos de linealización o material no lexicográfico.