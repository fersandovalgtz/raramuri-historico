# Política editorial — Rarámuri Histórico Digital

## Principio de no sobrescritura

La forma documental es evidencia histórica. Toda corrección, restauración, modernización, traducción o interpretación vive en una capa separada y deja rastro de procedencia. Una lectura propuesta durante una fase posterior nunca borra la transcripción diplomática ni la evidencia que motivó la revisión.

## Capas de autoridad

1. **Facsímil/testimonio:** imagen de la edición histórica y autoridad documental primaria para la lectura del impreso utilizado.
2. **OCR bruto:** salida automática preservada sin corrección retroactiva.
3. **Segmentación automática:** propuesta de límites de artículo orientada a máxima cobertura.
4. **Cotejo de límites:** decisión editorial IA-asistida sobre arranques, páginas, columnas, dirección y falsos positivos.
5. **Transcripción diplomática:** representación de caracteres y artículos cotejada con la página; puede ser IA-asistida sin implicar validación humana.
6. **Recotejo filológico IA-asistido:** segunda inspección de lecturas problemáticas, registrada en `RHD-PHIL-###` sin sobrescribir la capa diplomática.
7. **Validación humana independiente:** revisión filológica, lingüística, semántica, histórica o disciplinar con revisor, fecha, alcance, decisión y evidencia explícitas.
8. **Normalización:** forma auxiliar para búsqueda o comparación; siempre enlazada a la diplomática y a la decisión que la sustenta.
9. **Anotación/relación derivada:** traducción, comentario, etiquetas, concordancias y candidatos diacrónicos; nunca heredan automáticamente la autoridad de la fuente.

## Snapshot canónico 1.0.0

RHD `v1.0.0` congela un estado **machine-only** reproducible del Corpus Steffel 1791/1809. Los 2,495 candidatos documentales tienen disposición registrada: 1,965 artículos activos y 530 falsos límites preservados. Los 1,965 artículos activos disponen de transcripción diplomática IA-asistida dentro del alcance de esa release.

La auditoría de incertidumbre identificó 482 registros que requirieron recotejo PHIL. La serie `RHD-PHIL-001`–`RHD-PHIL-010` cubre los 482/482 casos y cierra la cola automática de esa fase con tres estados terminales:

- `confirmed_ai_assisted`: **284**;
- `corrected_ai_assisted`: **152**;
- `unresolved_after_ai_recollation`: **46**.

Estos estados son terminales **sólo para el alcance machine-only de v1.0.0**. Ninguno se transforma por ello en `human_verified`.

## Incorporación de propuestas

Una propuesta `corrected_ai_assisted` no reemplaza retrospectivamente el texto diplomático congelado en una release. Si una revisión posterior adopta, modifica o rechaza esa propuesta, la decisión debe entrar en una nueva capa o versión con procedencia explícita.

Del mismo modo, `confirmed_ai_assisted` significa que un recotejo automático/IA-asistido sostuvo una lectura previa; no significa «correcto por consenso experto». `unresolved_after_ai_recollation` es un resultado legítimo y no una falla que deba ocultarse.

## Revisión humana futura

`data/validation/human_review_queue.json` y los artefactos de prioridad permiten organizar una revisión independiente posterior. En `v1.0.0` no se afirma revisión humana filológica o lingüística de los 482 casos PHIL.

La revisión debe declarar su **alcance**. Confirmar una lectura gráfica no confirma automáticamente una etimología, análisis morfológico, identificación botánica/zoológica, equivalencia semántica o descripción cultural. Cada clase de afirmación requiere la evidencia y competencia pertinentes.

Una futura revisión humana puede aceptar, modificar, rechazar o mantener incierta una lectura. Su resultado pertenecerá a una versión posterior; no cambiará retrospectivamente la naturaleza de `v1.0.0`.

## Relaciones diacrónicas

Las 298 relaciones diacrónicas de `v1.0.0` permanecen en estado `candidate`. Pueden incorporar coincidencia gráfica, concordancia interna u otras señales computacionales, pero no se promueven automáticamente a cognación, etimología, identidad semántica o continuidad histórica.

Cualquier promoción futura debe registrar método, evidencia, responsable y clase de revisión.

## Identificadores y trazabilidad

Los identificadores ya asignados no se reciclan. Una fusión, división, rechazo de límite o correspondencia con Rarámuri Digital debe enlazar IDs y declarar método, confianza, versión y responsabilidad de la decisión.

Los manifiestos de revisión son evidencia del proceso y se preservan de forma append-only cuando esa propiedad forme parte de su contrato.

## Discurso histórico y contexto colonial

Los juicios coloniales, etnocéntricos o misioneros presentes en Steffel se conservan como parte de la fuente y se atribuyen al autor y a su contexto histórico. Las notas modernas distinguen descripción documental, traducción y comentario editorial. La conservación del discurso histórico no constituye adhesión del proyecto ni validación contemporánea de esas afirmaciones.

RHD tampoco presenta la obra de Steffel como representación normativa de las comunidades rarámuri actuales. La relación entre documentación histórica y lengua/cultura contemporáneas exige análisis específico y, cuando corresponda, participación o conocimiento competente que debe quedar documentado.

## Versionado editorial

Una release científica publicada es un objeto histórico del propio proyecto. No se modifica para hacerla coincidir con conocimiento posterior. Las correcciones y nuevas validaciones se publican en versiones nuevas conforme a `GOVERNANCE.md`, se registran en `CHANGELOG.md` y mantienen vínculos de procedencia hacia el estado anterior.
