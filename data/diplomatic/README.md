# Diplomatic transcription layer

Este directorio contiene overlays editoriales append-only producidos mediante cotejo IA-asistido contra el facsímil Steffel 1809. El facsímil es autoritativo; el OCR se conserva como evidencia secundaria. Todos los registros actuales tienen `human_verified=false`.

La cobertura diplomática está completa para todos los arranques aceptados hasta `RHD-FR-024`. La capa acumulada contiene **1,755 transcripciones diplomáticas IA-asistidas**, exactamente los 1,755 arranques aceptados entre 2,219 candidatos revisados.

## Recotejo de RHD-DIP-022A–G

Las 69 transcripciones de FR-022 fueron reabiertas contra las imágenes directas del facsímil y ahora llevan `direct_facsimile_image_reinspection=true` y método `visual_facsimile_transcription_ai_assisted`. El recotejo confirmó la segmentación y produjo ajustes diplomáticos concretos, entre ellos `Körper, Sepála`, `Lichtputze, Natſíla` y `Müßig, Nalſinaja / Nalſinäe`. Ya no queda ningún lote diplomático pendiente de imagen directa.

## RHD-DIP-023 y RHD-DIP-024

`RHD-DIP-023A`–`F` añaden **58 artículos completos** en pp. 333–343. Se preservan como unidades artículos extensos como `Packſattel`, `Schlangen`, `Sohle`, `Speiſe` y `Spielplatz`, evitando convertir prosa interna en nuevos lemas.

`RHD-DIP-024A`–`I` añaden **86 artículos completos** en pp. 343–347. Incluyen `Strick`, el largo artículo `Tanz`, la recuperación `Stroh` y las series `Un-` / `Ver-` de p. 347. Las formas tipográficamente inciertas conservan notas explícitas en lugar de normalizarse silenciosamente.

El inventario registra **598 transcripciones con nota de incertidumbre**. Estas notas representan dificultades documentales o lingüísticas reales; ya no se usan para marcar una carencia de acceso al facsímil.

Las particularidades históricas del impreso, incluidas formulaciones culturales hoy problemáticas, se preservan en la capa diplomática como evidencia documental. Su conservación no implica adhesión editorial y puede complementarse después con anotación crítica.

Los campos diplomáticos se aplican mediante `scripts/apply_review_overrides.py` y se propagan a CSV, JSON, XML, TEI, SQLite y la proyección pública.

El corpus no está globalmente terminado: quedan **216 `low_machine`** y toda la validación humana/lingüística independiente. El siguiente lote es `RHD-FR-025`, desde `RHD-S1809-01419` (`Verbrechen`) hasta `RHD-S1809-01608` (`Zinn`), aproximadamente pp. 348–352.
