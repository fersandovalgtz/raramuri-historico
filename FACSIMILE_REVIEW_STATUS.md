# Facsimile collation and diplomatic transcription status

Rarámuri Histórico Digital ha completado la **primera pasada editorial IA-asistida contra facsímil** de todo el universo de 2,495 candidatos del Corpus Steffel 1791/1809. Este estado permanece explícitamente separado de la futura validación humana, filológica y lingüística independiente.

## Boundary-review results

| Tier / audit | Reviewed | Accepted | Rejected | Headword corrections | Scope |
|---|---:|---:|---:|---:|---|
| `curated_anchor` · `RHD-FR-028` | 60 | 60 | 0 | 31 | pp. 301–363, muestra distribuida |
| `high_machine` · `RHD-FR-001`–`007` | 609 | 553 | 56 | 298 | pp. 301–368 |
| `medium_machine` · `RHD-FR-008`–`019` | 1,110 | 908 | 202 | 366 | pp. 301–368 |
| `low_machine` · `RHD-FR-020`–`027` | 716 | 444 | 272 | 86 | pp. 301–368 |
| **Total** | **2,495** | **1,965** | **530** | **781** | **diccionario completo** |

Los tres niveles automáticos y las 60 anclas curatoriales están agotados. `next_review_queue.json` y `next_review_queue_compact.json` están vacíos. Los **1,965 arranques aceptados** constituyen la capa activa provisional después de depurar 530 falsos límites; este número no debe confundirse con un conteo filológico definitivo de entradas.

## Hitos de cierre

`RHD-FR-026` cruzó de forma explícitamente **direction-aware** la inversión de p. 353: 54 aceptados, 46 rechazados, 36 correcciones de lema y 36 reajustes de página. Esto permitió distinguir sistemáticamente el headword rarámuri de sus glosas alemanas en la segunda mitad del diccionario.

`RHD-FR-027` resolvió los 16 últimos candidatos `low_machine`: 10 aceptados, 6 rechazados, 9 correcciones de lema y 15 correcciones de página. El facsímil demuestra que los registros que la máquina situaba en p. 369 pertenecían todavía a p. 368. Queda por tanto cerrada la frontera documental: **p. 368 es la última página lexicográfica y p. 369 comienza el apéndice**.

`RHD-FR-028` auditó las 60 anclas curatoriales: 60/60 son arranques reales, 31 lemas fueron corregidos y cuatro páginas reajustadas. Con ello todos los 2,495 candidatos están bajo el mismo estándar de inspección directa del facsímil IA-asistida.

## Diplomatic transcription

Los **1,965 artículos activos** tienen transcripción diplomática completa IA-asistida. El inventario registra **676 registros con nota explícita de incertidumbre**, ningún lote pendiente de imagen directa y `full_active_corpus_coverage=true`. La bandera `full_diplomatic_transcription_completed=true` se calcula automáticamente sólo cuando revisión, aceptación, transcripción y proveniencia cierran de forma consistente.

Todos los registros permanecen `human_verified=false`. Por tanto, la cobertura diplomática está completa en esta fase editorial, pero la edición no puede considerarse todavía validada humana o lingüísticamente.

## Next editorial stage

No queda una cola automática. La etapa siguiente es la **validación humana/filológica y lingüística independiente**, con prioridad para los 676 registros que conservan una nota de incertidumbre. Posteriormente podrán abordarse normalización explícita, variantes, correspondencias históricas y anotación crítica.
