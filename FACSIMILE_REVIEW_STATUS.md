# Facsimile collation and diplomatic transcription status

Rarámuri Histórico Digital mantiene veinte lotes append-only de revisión de límites. Todo el cotejo visual actual es IA-asistido y permanece explícitamente separado de la futura validación humana, filológica y lingüística independiente.

## Boundary-review results

| Batch / tier | Reviewed | Accepted | Rejected | Headword corrections | Printed-page span |
|---|---:|---:|---:|---:|---|
| `RHD-FR-001`–`RHD-FR-007` · high | 609 | 553 | 56 | 298 | 301–368 |
| `RHD-FR-008`–`RHD-FR-019` · medium | 1,110 | 908 | 202 | 366 | 301–368 |
| `RHD-FR-020` · low | 100 | 40 | 60 | 8 | 301–314 |
| **Cumulative reviewed corpus** | **1,819** | **1,501** | **318** | **672** | **301–368** |

Los niveles `high_machine` y `medium_machine` están agotados. De los 716 candidatos `low_machine`, se han resuelto los primeros 100 y quedan **616**. La capa activa provisional contiene **2,177 candidatos** de los 2,495 originales.

`RHD-FR-020` confirma un cambio marcado de perfil: sólo **40 %** de los candidatos de este primer lote bajo son arranques reales y **60 %** son falsos límites. Los rechazos son principalmente prosa descriptiva, ejemplos, equivalentes rarámuri o subentradas internas capturadas por el OCR como supuestos lemas. El cotejo corrige además la extensión automática pp. 301–316 a **pp. 301–314** y reajusta la página de **52 registros**.

Entre los arranques recuperados figuran `Abſchneiden`, `Armbruſt`, `Bauen`, `Baum`, `Berauſchen`, `Dörren`, `Drauſſen`, `Ehemann` y `Eichhorn`. Ocho lemas requieren corrección clara. `Drauſſen` se distingue del catchword homónimo de p. 312: el artículo real comienza en p. 313.

## Diplomatic transcription

`RHD-DIP-020A`–`RHD-DIP-020E` aportan **40 transcripciones completas** para todos los arranques aceptados de FR-020. La capa acumulada contiene **1,501 artículos diplomáticos IA-asistidos** y **529 notas explícitas de incertidumbre**. Todos los registros permanecen `human_verified=false`.

La frontera documental sigue fijada en p. 368 / p. 369. El facsímil es autoritativo y Merrill et al. (2020) se usa sólo como ayuda secundaria de colación.

## Next editorial stage

La siguiente etapa es **`RHD-FR-021`**, segundo lote `low_machine`: 100 candidatos desde `RHD-S1809-00422` (`Haaſe`) hasta `RHD-S1809-00787` (`Kienholz zum Brennen`), estimados alrededor de pp. 316–326. Quedan 616 candidatos bajos antes de ese lote. Global `full_diplomatic_transcription_completed` continúa en `false`.
