# Diplomatic transcription layer

Este directorio contiene overlays editoriales append-only producidos mediante comparación visual directa con el facsímil Steffel 1809. El facsímil es autoritativo; el OCR se conserva como evidencia secundaria y nunca como fuente de verdad para límites, página, columna o lectura del artículo. Todos los registros actuales tienen `human_verified=false`.

La cobertura diplomática está completa para los niveles `high_machine` y `medium_machine`. La serie `RHD-DIP-020A`–`RHD-DIP-021E` cubre además todos los arranques aceptados en los primeros **200 candidatos `low_machine`**.

`RHD-DIP-021A`–`RHD-DIP-021E` añaden **41 artículos completos** de `RHD-FR-021`, localizados por cotejo en pp. **315–326** dentro de una cohorte de límites que abarca pp. 314–326. Entre ellos figuran `Erſchrecken`, `Flachs`, `Friſch`, `Früh`, `Gegenwart`, `Großvater`, `Hernach`, `Heurathen`, `Hügel`, `Hülſenfrucht`, `Ich`, `Jenſeits des Fluſſes`, `Klein` y `Kienholz zum Brennen`.

La capa acumulada contiene **1,542 transcripciones diplomáticas IA-asistidas**, exactamente los 1,542 arranques aceptados entre 1,919 candidatos cotejados. El inventario registra **553 transcripciones con nota explícita de incertidumbre**. Las notas se reservan para dificultades documentales reales —diacríticos, secuencias rarámuri o reconstrucción de formas partidas por salto de línea— y no se añaden automáticamente por pertenecer al nivel bajo.

`Hülſenfrucht` e `Ich` ejemplifican artículos densos preservados como unidades completas; las formas difíciles se mantienen como lectura diplomática provisional, no como normalización lingüística. `Hügel` documenta además una reparación de lema contra el OCR (`Hüte`).

Merrill et al. (2020, DOI `10.47807/UNISON.8`) se usa únicamente como colación secundaria. Las particularidades del impreso no se normalizan silenciosamente. Los campos diplomáticos se aplican mediante `scripts/apply_review_overrides.py` y se propagan a JSON, XML, TEI, SQLite y la proyección pública.

El corpus no está globalmente terminado: quedan **516 `low_machine`** y toda la validación humana/lingüística independiente. El siguiente lote es `RHD-FR-022`, desde `RHD-S1809-00789` hasta `RHD-S1809-00964`.
