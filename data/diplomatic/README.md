# Diplomatic transcription layer

Este directorio contiene overlays editoriales append-only producidos mediante comparación visual directa con el facsímil Steffel 1809. El facsímil es autoritativo; el OCR se conserva como evidencia secundaria y nunca como fuente de verdad para límites, página, columna o lectura del artículo. Todos los registros actuales tienen `human_verified=false`.

La cobertura diplomática está completa para los niveles `high_machine` y `medium_machine`. `RHD-DIP-020A`–`RHD-DIP-020E` inauguran la transcripción del nivel `low_machine` con **40 artículos completos** aceptados en `RHD-FR-020`.

La serie incluye artículos breves y remisiones, pero también reconstrucciones completas de piezas extensas como `Armbruſt`, `Bauen`, `Baum` y `Eichhorn`. El lote se distribuye en pp. **301–314**; `Drauſſen` se transcribe en p. 313, distinguiendo su artículo del catchword de p. 312.

La capa acumulada contiene **1,501 transcripciones diplomáticas IA-asistidas**, exactamente los 1,501 arranques aceptados entre 1,819 candidatos cotejados. El inventario registra **529 transcripciones con nota explícita de incertidumbre**. Las notas se reservan para dificultades documentales reales —diacríticos, secuencias rarámuri o detalles de artículos largos— y no se añaden automáticamente por pertenecer al nivel de baja confianza.

Merrill et al. (2020, DOI `10.47807/UNISON.8`) se usa únicamente como colación secundaria. Las particularidades del impreso no se normalizan silenciosamente. Los campos diplomáticos se aplican mediante `scripts/apply_review_overrides.py` y se propagan a JSON, XML, TEI, SQLite y la proyección pública.

El corpus no está globalmente terminado: quedan **616 `low_machine`** y toda la validación humana/lingüística independiente. El siguiente lote es `RHD-FR-021`, segundo lote bajo, desde `RHD-S1809-00422` hasta `RHD-S1809-00787`.
