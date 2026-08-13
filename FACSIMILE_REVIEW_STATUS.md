# Facsimile collation and diplomatic transcription status

Rarámuri Histórico Digital mantiene veinticinco lotes append-only de revisión de límites. Todo `RHD-FR-001`–`RHD-FR-025` cuenta actualmente con inspección directa del facsímil IA-asistida; esto permanece separado de la futura validación humana, filológica y lingüística independiente.

## Boundary-review results

| Batch / tier | Reviewed | Accepted | Rejected | Headword corrections | Printed-page span |
|---|---:|---:|---:|---:|---|
| `RHD-FR-001`–`RHD-FR-007` · high | 609 | 553 | 56 | 298 | 301–368 |
| `RHD-FR-008`–`RHD-FR-019` · medium | 1,110 | 908 | 202 | 366 | 301–368 |
| `RHD-FR-020` · low | 100 | 40 | 60 | 8 | 301–314 |
| `RHD-FR-021` · low | 100 | 41 | 59 | 5 | 314–326 |
| `RHD-FR-022` · low | 100 | 69 | 31 | 4 | 326–333 |
| `RHD-FR-023` · low | 100 | 58 | 42 | 4 | 333–343 |
| `RHD-FR-024` · low | 100 | 86 | 14 | 10 | 343–347 |
| `RHD-FR-025` · low | 100 | 86 | 14 | 10 | 347–352 |
| **Low-confidence reviewed** | **600** | **380** | **220** | **41** | **301–352** |
| **Cumulative reviewed corpus** | **2,319** | **1,841** | **478** | **705** | **301–368** |

Los niveles `high_machine` y `medium_machine` están agotados. De los 716 candidatos `low_machine`, se han resuelto **600** y quedan **116**. La capa activa provisional contiene **2,017 candidatos** de los 2,495 originales.

`RHD-FR-025` corrige la extensión automática a pp. **347–352** y produce 86 aceptados / 14 rechazados, diez correcciones de lema y 27 reajustes de página. Las correcciones son `Verfault`, `Verleihen`, `Verlobt`, `Vier`, `Vor`, `Vorlängst`, `Wie immer`, `Wiederholen`, `Wo` y `Ziegelerde`.

Los falsos límites de FR-025 se concentran en material interno de `Verheyrathet`, `Verhexen`, `Verſtorben`, `Vogel`, `Weib`, `Waizen`, `Wissen`, `Wolf`, `Wie`, `Würfel` y `Wurzel`.

## Diplomatic transcription

La capa acumulada contiene **1,841 artículos diplomáticos IA-asistidos** y **620 notas explícitas de incertidumbre**. `RHD-DIP-025A`–`I` aportan los 86 artículos completos del lote. Ningún lote permanece pendiente de imagen directa; todos los registros continúan `human_verified=false`.

La frontera documental sigue fijada en p. 368 / p. 369 y `full_diplomatic_transcription_completed` continúa en `false`.

## Next editorial stage

La siguiente etapa es **`RHD-FR-026`**, penúltima cohorte `low_machine`: 100 de los 116 candidatos restantes, desde `RHD-S1809-01609` (`Zinnen`) hasta `RHD-S1809-02404` (OCR `Tofacameke Weiß`). Comienza en p. 352, cruza el cambio alemán→rarámuri / rarámuri→alemán dentro de p. 353 y se extiende automáticamente hasta aproximadamente p. 367. La revisión deberá ser explícitamente **direction-aware**. Tras FR-026 quedarían 16 candidatos de baja confianza.
