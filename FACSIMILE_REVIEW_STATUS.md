# Facsimile collation and diplomatic transcription status

Rarámuri Histórico Digital mantiene veintiún lotes append-only de revisión de límites. Todo el cotejo visual actual es IA-asistido y permanece explícitamente separado de la futura validación humana, filológica y lingüística independiente.

## Boundary-review results

| Batch / tier | Reviewed | Accepted | Rejected | Headword corrections | Printed-page span |
|---|---:|---:|---:|---:|---|
| `RHD-FR-001`–`RHD-FR-007` · high | 609 | 553 | 56 | 298 | 301–368 |
| `RHD-FR-008`–`RHD-FR-019` · medium | 1,110 | 908 | 202 | 366 | 301–368 |
| `RHD-FR-020` · low | 100 | 40 | 60 | 8 | 301–314 |
| `RHD-FR-021` · low | 100 | 41 | 59 | 5 | 314–326 |
| **Low-confidence reviewed** | **200** | **81** | **119** | **13** | **301–326** |
| **Cumulative reviewed corpus** | **1,919** | **1,542** | **377** | **677** | **301–368** |

Los niveles `high_machine` y `medium_machine` están agotados. De los 716 candidatos `low_machine`, se han resuelto **200** y quedan **516**. La capa activa provisional contiene **2,118 candidatos** de los 2,495 originales.

`RHD-FR-021` mantiene el perfil de depuración intensiva: **41 %** de los candidatos son arranques reales y **59 %** falsos límites. El facsímil corrige la extensión automática pp. 316–326 a **pp. 314–326** y reajusta la página de **37 registros**.

Las cinco correcciones de lema son `Flachs`, `Forttragen`, `Hügel`, `Hurtig` y `Jenſeits des Fluſſes`. Los rechazos comprenden prosa de `Ente`, `Feige indianiſche`, `Fiſchen`, `Fliege`, `Fragen`, `Gebirg`, `Getränk` y `Gries`, además de ejemplos, equivalentes rarámuri y repeticiones internas. `Heil` (`RHD-S1809-00671`) se rechaza como catchword de p. 323; el artículo auténtico inicia en p. 324 bajo otro ID.

## Diplomatic transcription

`RHD-DIP-021A`–`RHD-DIP-021E` aportan **41 transcripciones completas** para todos los arranques aceptados de FR-021. La capa acumulada contiene **1,542 artículos diplomáticos IA-asistidos** y **553 notas explícitas de incertidumbre**. Todos los registros permanecen `human_verified=false`.

La frontera documental sigue fijada en p. 368 / p. 369. El facsímil es autoritativo y Merrill et al. (2020) se usa sólo como ayuda secundaria de colación.

## Next editorial stage

La siguiente etapa es **`RHD-FR-022`**, tercer lote `low_machine`: 100 candidatos de los 516 restantes, desde `RHD-S1809-00789` (`Kieſelſtein`) hasta `RHD-S1809-00964` (OCR `C | ſondere bedeutet eine ver`), estimados alrededor de pp. **327–334**. Global `full_diplomatic_transcription_completed` continúa en `false`.
