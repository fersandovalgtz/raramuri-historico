# Facsimile collation and diplomatic transcription status

Rarámuri Histórico Digital mantiene veintidós lotes append-only de revisión de límites. La revisión actual es IA-asistida y permanece explícitamente separada de la futura validación humana, filológica y lingüística independiente. Los métodos de evidencia se conservan por lote: FR-001–FR-021 incluyen cotejo visual directo; FR-022 queda señalado para recotejo directo de imagen.

## Boundary-review results

| Batch / tier | Reviewed | Accepted | Rejected | Headword corrections | Printed-page span |
|---|---:|---:|---:|---:|---|
| `RHD-FR-001`–`RHD-FR-007` · high | 609 | 553 | 56 | 298 | 301–368 |
| `RHD-FR-008`–`RHD-FR-019` · medium | 1,110 | 908 | 202 | 366 | 301–368 |
| `RHD-FR-020` · low | 100 | 40 | 60 | 8 | 301–314 |
| `RHD-FR-021` · low | 100 | 41 | 59 | 5 | 314–326 |
| `RHD-FR-022` · low | 100 | 69 | 31 | 4 | 326–333 |
| **Low-confidence reviewed** | **300** | **150** | **150** | **17** | **301–333** |
| **Cumulative reviewed corpus** | **2,019** | **1,611** | **408** | **681** | **301–368** |

Los niveles `high_machine` y `medium_machine` están agotados. De los 716 candidatos `low_machine`, se han resuelto **300** y quedan **416**. La capa activa provisional contiene **2,087 candidatos** de los 2,495 originales.

`RHD-FR-022` presenta un perfil menos ruidoso que FR-020/021: **69 %** de los candidatos se retienen como arranques y **31 %** se rechazan. La alineación corrige pp. 327–334 a **pp. 326–333**, con **61 reajustes de página**. Las cuatro correcciones de lema son `Knüttel`, `Koſt`, `Kriegen` y `Lehrling`.

### Provenance exception: RHD-FR-022

Las imágenes directas del facsímil no estuvieron disponibles en el runtime que produjo FR-022. Este lote se apoya en el OCR primario preservado, en la arquitectura de página/columnas que ya había sido verificada visualmente y en una transcripción académica de la versión publicada sólo como colación secundaria. Por esa razón el manifiesto contiene `direct_facsimile_image_reinspection=false` y el inventario lo enumera en `direct_facsimile_image_recheck_pending_batches`. No debe describirse como cotejo visual directo ni como validación humana.

El pipeline conserva ahora esta heterogeneidad bajo `mixed_ai_assisted_editorial_collation` y registra las metodologías efectivamente usadas.

## Diplomatic transcription

`RHD-DIP-022A`–`RHD-DIP-022G` aportan **69 transcripciones completas** para todos los arranques aceptados de FR-022. La capa acumulada contiene **1,611 artículos diplomáticos IA-asistidos** y **622 notas explícitas de incertidumbre**. Los 69 registros nuevos incluyen una nota de recotejo directo de imagen, de modo que no se confunda reconstrucción documental con inspección visual del testimonio.

Todos los registros permanecen `human_verified=false`. La frontera documental sigue fijada en p. 368 / p. 369.

## Next editorial stage

La siguiente etapa es **`RHD-FR-023`**, cuarto lote `low_machine`: 100 candidatos de los 416 restantes, desde `RHD-S1809-00965` (`Nachſehen`) hasta `RHD-S1809-01238` (`Spielplatz`), estimados alrededor de pp. **334–343**. Global `full_diplomatic_transcription_completed` continúa en `false`.
