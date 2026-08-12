# Diplomatic transcription layer

Este directorio contiene overlays editoriales append-only producidos mediante comparación visual directa con el facsímil Steffel 1809. El facsímil es autoritativo; el OCR se conserva como ayuda secundaria y nunca como fuente de verdad para límites, página, columna o lectura del artículo.

Las transcripciones preservan la formulación y puntuación documentales sin codificar los saltos tipográficos de línea. El método es `visual_facsimile_transcription_ai_assisted`; todos los registros actuales tienen `human_verified=false`.

`RHD-DIP-001A`–`RHD-DIP-007A` cubren los 553 arranques aceptados del nivel `high_machine`. Las series posteriores proporcionan cobertura completa para cada arranque aceptado en los lotes `medium_machine` revisados.

`RHD-DIP-018A`–`RHD-DIP-018I` añaden **87 artículos completos** de `RHD-FR-018`, localizados por cotejo en pp. **364–368**. La serie cubre el final documental del diccionario rarámuri→alemán y no incorpora material del apéndice de p. 369.

Entre las formas recuperadas están `Rhenéke`, `R-guála`, `Schugiámeke`, `Sinépi putié`, `Tajenaságo`, `Telsiguála`, `Tótschi`, `Tschie`, `Tschulugéameke`, `Tlestatáccameke, oder Stácameke`, `Tulchilki`, `Vakítsi` y `Vassúritschi`. Nueve nuevos registros llevan notas explícitas para secuencias o diacríticos que requieren re-colación humana/filológica independiente.

La capa acumulada contiene **1,452 transcripciones diplomáticas IA-asistidas**, exactamente los **1,452 arranques aceptados entre 1,709 candidatos cotejados**. El inventario registra **521 transcripciones con nota explícita de incertidumbre**. Todos los registros permanecen `human_verified=false`.

El cotejo FR-018 confirma que la última página lexicográfica es **p. 368** y que **p. 369 inicia el apéndice**. Esta frontera se conserva como dato editorial explícito; una asignación OCR a p. 369 no basta para tratar un candidato como artículo de diccionario.

Los campos diplomáticos son aplicados por `scripts/apply_review_overrides.py` y propagados a JSON, XML, TEI, SQLite y la proyección pública. El OCR fuente no se modifica.

La revisión de alta confianza y los primeros once lotes `medium_machine` están completos a nivel de límites y transcripción diplomática IA-asistida. No es una conclusión global del corpus: quedan **10 `medium_machine`**, 716 `low_machine` y toda la validación humana/lingüística independiente.

El siguiente lote es `RHD-FR-019`, compuesto por los diez candidatos medios finales. Todos están etiquetados automáticamente como p. 369 y deberán cotejarse contra la frontera 368/369 antes de aceptar cualquier lectura como entrada lexicográfica.