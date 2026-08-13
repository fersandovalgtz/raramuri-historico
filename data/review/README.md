# Facsimile review

Este directorio conserva manifiestos editoriales append-only sobre la segmentación OCR de alta cobertura. Los IDs son persistentes: un falso límite se rechaza, pero nunca se recicla. La revisión IA-asistida permanece separada de la validación humana/filológica y lingüística.

## Estado de revisión

La primera pasada contra facsímil está completa para los **2,495 candidatos** del Corpus Steffel 1791/1809.

- `RHD-FR-001`–`RHD-FR-007`: 609 `high_machine`; 553 aceptados, 56 rechazados, 298 correcciones.
- `RHD-FR-008`–`RHD-FR-019`: 1,110 `medium_machine`; 908 aceptados, 202 rechazados, 366 correcciones.
- `RHD-FR-020`–`RHD-FR-027`: 716 `low_machine`; 444 aceptados, 272 rechazados, 86 correcciones.
- `RHD-FR-028`: auditoría de las 60 `curated_anchor`; 60 aceptadas, 0 rechazadas, 31 correcciones.

Estado acumulado: **2,495 revisados, 1,965 aceptados, 530 falsos límites y 781 correcciones de lema**. Los 1,965 aceptados son artículos activos provisionales, no un conteo filológico definitivo.

## Cierre direction-aware y frontera del diccionario

`RHD-FR-026` fue el lote de transición: empezó en p. 352, cruzó la inversión alemán→rarámuri / rarámuri→alemán dentro de p. 353 y continuó hasta p. 367. Después de la inversión, el criterio de arranque cambió correctamente: la forma rarámuri es el headword y el alemán funciona como glosa. El lote produjo 54 aceptados, 46 falsos límites, 36 correcciones de lema y 36 reajustes de página.

`RHD-FR-027` resolvió los últimos 16 candidatos `low_machine`. El resultado fue 10 aceptados / 6 rechazados, con 9 reparaciones de lema y 15 correcciones de página. La inspección directa mostró que los candidatos estimados en p. 369 pertenecían aún a la columna derecha de p. 368; p. 369 inicia el apéndice y no contiene ningún candidato lexicográfico residual.

`RHD-FR-028` incorporó finalmente las 60 anclas iniciales al mismo estándar de cotejo directo. Todas eran arranques reales; entre las reparaciones más claras figuran `Abzählen`, `Babalí`, `Iguá` y `Pahí`.

## Cola determinista

`scripts/generate_review_queue.py` continúa siendo reproducible, pero la cola está actualmente **agotada**:

```json
{"tier": null, "remaining_before_batch": 0, "records": []}
```

No debe generarse un nuevo `RHD-FR` a partir de la segmentación actual. La siguiente fase es validación humana/filológica y lingüística de los artículos activos, especialmente de los 676 que conservan nota de incertidumbre.

Todos los manifiestos siguen siendo `human_verified=false` salvo que una futura fase de validación registre explícitamente lo contrario.
