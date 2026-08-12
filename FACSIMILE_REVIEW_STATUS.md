# Facsimile collation and diplomatic transcription status

Rarámuri Histórico Digital mantiene diecisiete lotes append-only de revisión de límites y una capa separada de transcripción diplomática. Todo el trabajo actual de cotejo visual es IA-asistido y se distingue explícitamente de una futura validación humana, filológica y lingüística independiente.

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
| **Cumulative reviewed corpus** | **1,609** | **1,365** | **244** | **573** | **301–368** |

La capa de cobertura conserva 2,495 candidatos. Los 609 `high_machine` ya fueron resueltos. Los primeros **1,000 de 1,110 `medium_machine`** también fueron cotejados: **812 arranques aceptados y 188 falsos límites**. Quedan **110 `medium_machine`** y posteriormente 716 `low_machine`. Los IDs rechazados permanecen persistentes y nunca se reciclan; la capa activa provisional contiene **2,251 candidatos**.

`RHD-FR-017` está enteramente en rarámuri→alemán. El facsímil corrige la extensión automática 360–365 a **360–364**, acepta 91 candidatos y rechaza nueve glosas alemanas mal segmentadas como supuestos lemas: `Brod`, `Mehr`, `Kriegen`, `Zange`, `Belohnen`, `Bekennen`, `Wahrheit`, `Weg` y `Nicht viel`. **90 de los 91 arranques aceptados requieren corrección clara de lema**, y 24 registros cambian de página tras cotejo directo.

Entre las lecturas recuperadas están `Lála`, `Moorápera`, `Nachtétuje`, `Nacuguíta`, `Nassípasic`, `Noitsámela`, `Ossanaguóameke`, `Pitschabúrameke`, `Rachtábatsáboa`, `Rauguelíki` y `Rhaná`. El facsímil es autoritativo; Merrill et al. (2020) se usa únicamente como ayuda secundaria de colación para grafías difíciles.

## Diplomatic transcription

`RHD-DIP-017A`–`RHD-DIP-017J` aportan **91 transcripciones completas** para todos los arranques aceptados de FR-017. La serie acumulada contiene **1,365 artículos diplomáticos IA-asistidos**, exactamente los mismos 1,365 arranques aceptados entre 1,609 límites cotejados. El inventario registra **512 notas explícitas de incertidumbre**. Todos los registros permanecen `human_verified=false`.

La lectura `Putschíla, Brust, uber.` se conserva diplomáticamente tal como aparece visualmente y la glosa final queda marcada para recotejo humano independiente.

## Next editorial stage

La siguiente etapa es **`RHD-FR-018`**. La cola determinista contiene 100 de los 110 `medium_machine` restantes, desde `RHD-S1809-02234` hasta `RHD-S1809-02478`. La asignación automática alcanza p. 369; como el vocabulario termina en p. 368 y el apéndice comienza en p. 369, el próximo lote deberá resolver explícitamente el límite diccionario/apéndice mediante el facsímil. Global `full_diplomatic_transcription_completed` continúa en `false`.