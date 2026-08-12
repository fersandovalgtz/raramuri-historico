# Facsimile collation and diplomatic transcription status

Rarámuri Histórico Digital mantiene diecinueve lotes append-only de revisión de límites y una capa separada de transcripción diplomática. Todo el trabajo actual de cotejo visual es IA-asistido y se distingue explícitamente de una futura validación humana, filológica y lingüística independiente.

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
| `RHD-FR-019` | 10 | 9 | 1 | 9 | 368 |
| **Medium-confidence tier** | **1,110** | **908** | **202** | **366** | **301–368** |
| **Cumulative reviewed corpus** | **1,719** | **1,461** | **258** | **664** | **301–368** |

La capa de cobertura conserva 2,495 candidatos. Los dos niveles superiores están ahora **completamente agotados**: 609 `high_machine` y 1,110 `medium_machine`. El nivel medio produjo **908 arranques aceptados y 202 falsos límites**. Quedan **716 `low_machine`** sin revisión sistemática. Los IDs rechazados permanecen persistentes y nunca se reciclan; la capa activa provisional contiene **2,237 candidatos**.

`RHD-FR-019` resuelve los diez candidatos medios finales. Aunque la cola automática ubicaba todos en p. 369, el facsímil demuestra que su evidencia pertenece a la columna derecha de **p. 368**, antes de la indicación `Anhang`. Nueve son entradas reales y `Bär` es una glosa/remisión dentro de `Vohí, Bär, s. Bär.`. El lote corrige los nueve lemas aceptados y las diez asignaciones de página.

Las formas recuperadas son `Uélameke`, `Uilí`, `Uipáca`, `Veréndo`, `Vissigó`, `Ulé`, `Ululú`, `Upéameke` y `Vuossaguáca`. El facsímil sigue siendo autoritativo; Merrill et al. (2020) se usa únicamente como ayuda secundaria de colación. La capa diplomática conserva literalmente la forma impresa `Uélameke` y la glosa `Spielblatt` de `Ulé`, aunque el estudio moderno discuta ambas como posibles errores del testimonio histórico.

La frontera documental queda establecida de manera inequívoca: **p. 368 cierra el diccionario y p. 369 inicia el apéndice**.

## Diplomatic transcription

`RHD-DIP-019A` aporta **9 transcripciones completas** para todos los arranques aceptados de FR-019. La serie acumulada contiene **1,461 artículos diplomáticos IA-asistidos**, exactamente los mismos 1,461 arranques aceptados entre 1,719 límites cotejados. El inventario registra **521 notas explícitas de incertidumbre**. Todos los registros permanecen `human_verified=false`.

## Next editorial stage

La siguiente etapa es **`RHD-FR-020`**, el primer lote `low_machine`. Su cola contiene los primeros 100 de 716 candidatos de baja confianza, desde `RHD-S1809-00061` (`Vorrede erinnert habe`) hasta `RHD-S1809-00421` (`Vogel`), aproximadamente en pp. **301–316** según la asignación automática. La cohorte está poblada por numerosos fragmentos de prosa, glosas y secuencias internas, por lo que el cotejo facsimilar deberá privilegiar tipografía, sangría y continuidad documental sobre la apariencia textual del OCR. Global `full_diplomatic_transcription_completed` continúa en `false`.