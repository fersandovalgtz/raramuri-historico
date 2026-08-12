# Diplomatic transcription layer

Este directorio contiene overlays editoriales append-only. El facsímil Steffel 1809 continúa siendo la autoridad editorial, pero el método efectivo de cada lote se conserva explícitamente: la mayor parte de la serie fue producida por comparación visual directa; `RHD-DIP-022A`–`RHD-DIP-022G` constituyen una excepción documental pendiente de recotejo directo de imagen. Todos los registros actuales tienen `human_verified=false`.

La cobertura diplomática está completa para todos los arranques aceptados hasta `RHD-FR-022`. La capa acumulada contiene **1,611 transcripciones diplomáticas IA-asistidas**, exactamente los 1,611 arranques aceptados entre 2,019 candidatos revisados.

`RHD-DIP-022A`–`RHD-DIP-022G` añaden **69 artículos completos** localizados en pp. **326–333**, entre ellos `Kraut`, `Leopard`, `Mädchen`, `Lernen`, `Löffel`, `Machen`, `Maulſchelle`, `Mutter`, `Nachfolgen` y `Nachgehen`. Artículos extensos como `Leopard`, `Mädchen` y `Mutter` se conservan como unidades completas, sin convertir sus frases internas en nuevos lemas.

## Proveniencia de RHD-DIP-022A–G

Las imágenes directas del facsímil no estuvieron disponibles en el runtime de estos siete sublotes. Las transcripciones se reconstruyeron mediante el OCR primario preservado, la arquitectura de página/columnas que ya había sido verificada visualmente y la transcripción académica de la versión publicada sólo como colación secundaria. Cada manifiesto lleva `direct_facsimile_image_reinspection=false` y el método `primary_ocr_preverified_facsimile_layout_secondary_transcription_ai_assisted`.

El pipeline registra ahora la capa global como `mixed_ai_assisted_diplomatic_transcription`, conserva la lista de métodos y enumera `RHD-DIP-022A`–`G` entre los lotes pendientes de recotejo directo. Los **622 registros con nota de incertidumbre** incluyen por diseño los 69 de FR-022, para que esta obligación metodológica viaje con cada registro hacia CSV, JSON, XML, TEI, SQLite y la proyección pública.

Las particularidades del impreso no se normalizan silenciosamente. Las lecturas difíciles se mantienen como provisionales hasta cotejo directo de imagen y validación filológica/lingüística independiente.

El corpus no está globalmente terminado: quedan **416 `low_machine`** y toda la validación humana/lingüística independiente. El siguiente lote es `RHD-FR-023`, desde `RHD-S1809-00965` hasta `RHD-S1809-01238`.
