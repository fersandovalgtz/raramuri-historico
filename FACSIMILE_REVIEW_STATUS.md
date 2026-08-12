# Facsimile collation and diplomatic transcription status

Rarámuri Histórico Digital mantiene dieciocho lotes append-only de revisión de límites y una capa separada de transcripción diplomática. Todo el trabajo actual de cotejo visual es IA-asistido y se distingue explícitamente de una futura validación humana, filológica y lingüística independiente.

## Boundary-review results

| Batch | Reviewed | Accepted | Rejected | Headword corrections | Printed-page span |
|---|---:|---:|---:|---:|---|
| `RHD-FR-001` | 100 | 86 | 14 | 4 | 301–317 |
| `RHD-FR-002` | 100 | 85 | 15 | 10 | 318–339 |
| `RHD-FR-003` | 100 | 89 | 11 | 33 | 339–357 |
| `RHD-FR-004` | 100 | 90 | 10 | 62 | 357–361 |
| `RHD-FR-005` | 100 | 96 | 4 | 90 | 361–365 |
| `RHD-FR-006` | 100 | 98 | 2 | 91 | 365–368 |
| `RHD-FR-007` | 9 | 9 | 0 | 8 | 368 |
| **High-confidence tier** | **609** | **553** | **56** | **298** | **301–368** |
| `RHD-FR-008` | 100 | 72 | 28 | 9 | 301–308 |
| `RHD-FR-009` | 100 | 70 | 30 | 7 | 308–315 |
| `RHD-FR-010` | 100 | 79 | 21 | 13 | 315–322 |
| `RHD-FR-011` | 100 | 81 | 19 | 5 | 322–327 |
| `RHD-FR-012` | 100 | 81 | 19 | 12 | 328–338 |
| `RHD-FR-013` | 100 | 83 | 17 | 9 | 338–344 |
| `RHD-FR-014` | 100 | 81 | 19 | 6 | 345–350 |
| `RHD-FR-015` | 100 | 84 | 16 | 37 | 350–356 |
| `RHD-FR-016` | 100 | 90 | 10 | 87 | 356–360 |
| `RHD-FR-017` | 100 | 91 | 9 | 90 | 360–364 |
| `RHD-FR-018` | 100 | 87 | 13 | 82 | 364–368 |
| **Cumulative reviewed corpus** | **1,709** | **1,452** | **257** | **655** | **301–368** |

La capa de cobertura conserva 2,495 candidatos. Los 609 `high_machine` ya fueron resueltos. Los primeros **1,100 de 1,110 `medium_machine`** también fueron cotejados: **899 arranques aceptados y 201 falsos límites**. Quedan **10 `medium_machine`** y posteriormente 716 `low_machine`. Los IDs rechazados permanecen persistentes y nunca se reciclan; la capa activa provisional contiene **2,238 candidatos**.

`RHD-FR-018` resuelve el extremo final de la sección rarámuri→alemán. El facsímil corrige la extensión automática a **pp. 364–368**, acepta 87 candidatos, rechaza 13 falsos límites, corrige 82 lemas y cambia de página 45 registros. Entre los rechazos hay glosas alemanas, un catchword, un running header, un ejemplo interno y un artefacto OCR sin correlato facsimilar.

El lote verifica directamente la frontera documental: **p. 368 es la última página del diccionario; p. 369 inicia el apéndice**. Ningún candidato de FR-018 se acepta como artículo de diccionario en p. 369. Los candidatos automáticamente desplazados a 369 sólo se recolocan en 368 cuando existe evidencia visual inequívoca.

## Diplomatic transcription

`RHD-DIP-018A`–`RHD-DIP-018I` aportan **87 transcripciones completas** para todos los arranques aceptados de FR-018. La serie acumulada contiene **1,452 artículos diplomáticos IA-asistidos**, exactamente los mismos 1,452 arranques aceptados entre 1,709 límites cotejados. El inventario registra **521 notas explícitas de incertidumbre**. Todos los registros permanecen `human_verified=false`.

Entre las lecturas señaladas para futura re-colación independiente están variantes o secuencias difíciles de `Sini, oder Schine`, `Tamateiáme`, `T-fliguá`, `Tótschi`, `Tschapíboli`, `Tschie`, `Tlestatáccameke, oder Stácameke`, `Tulchilki` y `Vassúritschi`.

## Next editorial stage

La siguiente etapa es **`RHD-FR-019`**, que contiene los **10 `medium_machine` restantes**: `RHD-S1809-02480`–`RHD-S1809-02494`. Todos están etiquetados automáticamente como p. 369, pero esa página pertenece al apéndice. FR-019 deberá establecer si alguno corresponde todavía a una entrada rezagada de p. 368 o si son artefactos/material no lexicográfico. Tras FR-019 comenzará el nivel `low_machine`. Global `full_diplomatic_transcription_completed` continúa en `false`.