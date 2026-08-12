# Diplomatic transcription layer

Este directorio contiene overlays editoriales append-only producidos mediante comparación visual directa con el facsímil Steffel 1809. El facsímil es autoritativo; el OCR se conserva como ayuda secundaria y nunca como fuente de verdad para límites, página, columna o lectura del artículo.

Las transcripciones preservan la formulación y puntuación documentales sin codificar los saltos tipográficos de línea. El método es `visual_facsimile_transcription_ai_assisted`; todos los registros actuales tienen `human_verified=false`.

`RHD-DIP-001A`–`RHD-DIP-007A` cubren los 553 arranques aceptados del nivel `high_machine`. Las series posteriores proporcionan cobertura completa para cada arranque aceptado en los lotes `medium_machine` revisados.

`RHD-DIP-017A`–`RHD-DIP-017J` añaden **91 artículos completos** de `RHD-FR-017`, todos dentro de rarámuri→alemán y con arranques en pp. **360–364**. La serie incluye formas recuperadas como `Lála`, `Lessíameke`, `Moorápera`, `Nachtétuje`, `Nacuguíta`, `Nassípasic`, `Noitsámela`, `Ossanaguóameke`, `Pitschabúrameke`, `Rachtábatsáboa`, `Rauguelíki` y `Rhaná`.

La transcripción de `Putschíla` conserva `Putschíla, Brust, uber.` porque ésa es la lectura visual del facsímil; la última glosa alemana se marca como incierta para recotejo humano/filológico. La transcripción de Merrill et al. (2020, DOI `10.47807/UNISON.8`) funciona sólo como colación secundaria para grafías difíciles y nunca sustituye la evidencia facsimilar.

La capa acumulada contiene **1,365 transcripciones diplomáticas IA-asistidas**, exactamente los **1,365 arranques aceptados entre 1,609 candidatos cotejados**. El inventario registra **512 transcripciones con nota explícita de incertidumbre**. Todos los registros permanecen `human_verified=false`.

Los campos diplomáticos son aplicados por `scripts/apply_review_overrides.py` y propagados a JSON, XML, TEI, SQLite y la proyección pública. El OCR fuente no se modifica.

La revisión de alta confianza y los primeros diez lotes `medium_machine` están completos a nivel de límites y transcripción diplomática IA-asistida. No es una conclusión global del corpus: quedan **110 `medium_machine`**, 716 `low_machine` y toda la validación humana/lingüística independiente.

El siguiente lote es `RHD-FR-018`. Su cola alcanza automáticamente p. 369; dado que el diccionario termina en p. 368 y el apéndice comienza en p. 369, la próxima revisión deberá distinguir cuidadosamente entradas lexicográficas, catchwords y materiales del apéndice.