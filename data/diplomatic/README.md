# Diplomatic transcription layer

Este directorio contiene overlays editoriales append-only producidos mediante cotejo IA-asistido contra el facsímil Steffel 1809. El facsímil es autoritativo; el OCR se conserva como evidencia secundaria. Todos los registros actuales tienen `human_verified=false`.

La cobertura diplomática está completa para todos los arranques aceptados hasta `RHD-FR-025`. La capa acumulada contiene **1,841 transcripciones diplomáticas IA-asistidas**, exactamente los 1,841 arranques aceptados entre 2,319 candidatos revisados.

`RHD-DIP-025A`–`I` añaden **86 artículos completos** en pp. 347–352. El lote incluye la serie `Ver-`, `Vier`, `Vor`, `Wahrheit`, `Waſſer`, el bloque `W-` y la serie `Z-` hasta `Zinn`. Las formas OCR dañadas se reparan sólo cuando la imagen lo permite; las lecturas lingüísticamente inciertas mantienen nota explícita.

La serie histórica reciente conserva como unidades completas artículos extensos y evita promover prosa interna, ejemplos o glosas a headwords independientes. El inventario registra **620 transcripciones con nota de incertidumbre** y ningún lote pendiente de recotejo de imagen directa.

Las particularidades históricas del impreso, incluidas formulaciones culturales hoy problemáticas, se preservan como evidencia documental. Su conservación no implica adhesión editorial y puede complementarse con anotación crítica posterior.

Los campos diplomáticos se aplican mediante `scripts/apply_review_overrides.py` y se propagan a CSV, JSON, XML, TEI, SQLite y la proyección pública.

## Siguiente tramo

Quedan **116 `low_machine`**. `RHD-FR-026` revisará 100 candidatos desde `Zinnen` hasta el OCR `Tofacameke Weiß`, cruzando dentro de p. 353 la transición alemán→rarámuri / rarámuri→alemán. Las futuras transcripciones de este lote deberán preservar explícitamente la dirección de cada artículo: tras la frontera, el headword documental es rarámuri y el alemán pasa a ocupar la glosa.
