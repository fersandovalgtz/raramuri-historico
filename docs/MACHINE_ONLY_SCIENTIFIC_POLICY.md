# Política científica de intervención humana cero

**Proyecto:** Rarámuri Histórico Digital — Corpus Steffel 1791/1809  
**Decisión:** 15 de agosto de 2026

## 1. Alcance

El Corpus Steffel se cerrará como una **edición histórico-digital computacional e IA-asistida sin intervención humana de adjudicación**. No se exigirá revisión filológica, lingüística, semántica, comunitaria o histórica realizada por terceros para considerar completa la edición computacional.

Esta decisión modifica el objetivo de terminación: RHD no afirmará producir una edición crítica humanamente validada. Producirá una edición científica computacional reproducible, con evidencia, procedencia, estados epistemológicos e incertidumbre explícita.

## 2. Regla fundamental

La ausencia de revisión humana **no autoriza** a convertir resultados automáticos en `human_verified`, `expert_verified`, `community_validated` ni equivalentes.

Los estados permitidos deben describir honestamente el procedimiento realizado, por ejemplo:

- `confirmed_ai_assisted`;
- `corrected_ai_assisted`;
- `unresolved_after_ai_recollation`;
- `machine_candidate`;
- `ocr_structured_candidate`;
- `ai_visual_collation`.

## 3. Tratamiento de los 482 casos PHIL

Los 482 casos dejan de constituir una cola de trabajo humano obligatoria. Su cierre computacional se define por la existencia de un evento PHIL trazable para cada caso:

- 284 `confirmed_ai_assisted`;
- 152 `corrected_ai_assisted`;
- 46 `unresolved_after_ai_recollation`.

Los 46 irresueltos **no son fallos del cierre** siempre que permanezcan explícitamente marcados como inciertos y que la edición no seleccione arbitrariamente una lectura única. En una edición computacional científica, conservar una ambigüedad documentada es preferible a fabricar certeza.

Los paquetes de revisión humana ya generados se conservan como artefactos históricos/opcionales de interoperabilidad editorial, pero no forman parte del camino crítico ni del porcentaje de terminación.

## 4. Normalización y análisis lingüístico

La normalización automática puede utilizarse para búsqueda, agrupamiento, concordancia, recuperación y generación de candidatos. No debe presentarse como norma ortográfica contemporánea ni como validación lingüística.

Las relaciones diacrónicas pueden permanecer como candidatos probabilísticos o documentales. RHD no debe transformar automáticamente similitud gráfica, coincidencia de recuperación o apoyo contextual en cognación, etimología, equivalencia semántica o continuidad histórica.

## 5. Criterio de calidad sin personas revisoras

La calidad se sostendrá mediante:

1. preservación del facsímil y OCR como evidencia;
2. capas no destructivas;
3. identificadores persistentes;
4. procedencia de cada transformación;
5. controles automáticos e invariantes;
6. validación contra esquemas externos cuando existan;
7. checksums e integridad de release;
8. reproducción determinista del pipeline;
9. estados de incertidumbre explícitos;
10. prueba end-to-end con otra fuente histórica real.

## 6. Criterio de terminación

Steffel se considerará terminado dentro de este alcance cuando:

- el cuerpo lexicográfico esté cubierto y trazable;
- todos los problemas detectados tengan un estado computacional explícito, incluido `unresolved` cuando corresponda;
- anexos y textos paralelos estén incorporados con trazabilidad facsimilar/IA;
- TEI/Lex-0 y demás exportaciones pertinentes sean reproducibles y validadas;
- la relación facsimilar esté resuelta mediante mapeo estable y, cuando sea viable, IIIF;
- exista release científico citable con manifiesto de integridad;
- una segunda fuente histórica real demuestre que el núcleo RHD es reusable sin rediseño fundamental.

## 7. Fórmula de declaración pública

La documentación deberá utilizar expresiones como **“edición histórico-digital computacional”, “cotejo IA-asistido”, “transcripción diplomática IA-asistida”** o **“candidato computacional”**. No se utilizará “validado por especialistas”, “edición crítica humanamente revisada” ni formulaciones equivalentes salvo que en el futuro existiera efectivamente tal intervención, lo cual no forma parte del alcance actual.
