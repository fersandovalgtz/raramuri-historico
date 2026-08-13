# Facsimile collation and diplomatic transcription status

Rarámuri Histórico Digital mantiene veinticuatro lotes append-only de revisión de límites. Todo el cotejo de `RHD-FR-001`–`RHD-FR-024` cuenta actualmente con inspección directa del facsímil IA-asistida; esto permanece explícitamente separado de la futura validación humana, filológica y lingüística independiente.

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
| **Low-confidence reviewed** | **500** | **294** | **206** | **31** | **301–347** |
| **Cumulative reviewed corpus** | **2,219** | **1,755** | **464** | **695** | **301–368** |

Los niveles `high_machine` y `medium_machine` están agotados. De los 716 candidatos `low_machine`, se han resuelto **500** y quedan **216**. La capa activa provisional contiene **2,031 candidatos** de los 2,495 originales.

## Direct-image re-collation completed

`RHD-FR-022` y `RHD-DIP-022A`–`G` fueron recotejados directamente contra el facsímil original después de que las imágenes volvieran a estar disponibles. El balance 69/31 y las cuatro correcciones de lema se confirmaron. La inspección directa sí produjo ajustes diplomáticos —por ejemplo `Sepála`, `Natſíla` y `Nalſinaja / Nalſinäe`—. El inventario ya no enumera ningún lote en `direct_facsimile_image_recheck_pending_batches`.

## Recent low-confidence batches

`RHD-FR-023` corrige su span automático a pp. **333–343** y produce 58/42, con cuatro correcciones de lema (`Ob?`, `Recht`, `Schließen`, `Schrauben`) y 29 reajustes de página. Sus artículos extensos incluyen `Packſattel`, `Schlangen`, `Sohle`, `Speiſe` y `Spielplatz`.

`RHD-FR-024` se sitúa en pp. **343–347** y produce 86/14, con diez reparaciones de lema y 19 reajustes de página. La auditoría de solapamiento rechaza `RHD-S1809-01296` como catchword `Stute` de p. 344, evitando duplicar el artículo auténtico ya representado por `RHD-S1809-01297`; además recupera `RHD-S1809-01293` como `Stroh`.

## Diplomatic transcription

La capa acumulada contiene **1,755 artículos diplomáticos IA-asistidos** y **598 notas explícitas de incertidumbre**. `RHD-DIP-023A`–`F` aportan 58 artículos y `RHD-DIP-024A`–`I` otros 86. Todos los registros permanecen `human_verified=false`.

La frontera documental sigue fijada en p. 368 / p. 369. Global `full_diplomatic_transcription_completed` continúa en `false`.

## Next editorial stage

La siguiente etapa es **`RHD-FR-025`**, sexto lote `low_machine`: 100 candidatos de los 216 restantes, desde `RHD-S1809-01419` (`Verbrechen`) hasta `RHD-S1809-01608` (`Zinn`), estimados alrededor de pp. **348–352**. Tras ese lote quedarán 116 candidatos bajos, próximos a la transición de dirección de p. 353.
