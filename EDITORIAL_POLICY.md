# Política editorial

## Principio de no sobrescritura

La forma documental es evidencia histórica. Toda corrección, restauración, modernización, traducción o interpretación vive en una capa separada y deja rastro de procedencia. Una lectura propuesta durante una fase posterior nunca borra la transcripción diplomática que motivó la revisión.

## Capas

1. **Facsímil:** imagen de la edición histórica y autoridad documental primaria.
2. **OCR bruto:** salida automática preservada sin corrección.
3. **Segmentación automática:** propuesta de límites de artículo orientada a máxima cobertura.
4. **Cotejo de límites:** decisión editorial IA-asistida sobre arranques, páginas, columnas y falsos positivos.
5. **Transcripción diplomática:** caracteres y artículos completos cotejados con la página; puede ser IA-asistida sin implicar validación humana.
6. **Recotejo filológico IA-asistido:** segunda inspección de lecturas abiertas, registrada en `RHD-PHIL-###` sin sobrescribir la capa diplomática.
7. **Validación humana independiente:** revisión filológica, lingüística, semántica o disciplinar con revisor, fecha, competencia, decisión y evidencia explícitas.
8. **Normalización:** forma auxiliar para búsqueda o comparación; siempre enlazada a la diplomática y a la decisión que la sustenta.
9. **Anotación:** traducción, gramática, etiquetas culturales y correspondencias diacrónicas.

## Estado editorial actual

Los 2,495 candidatos segmentados han sido cotejados contra el facsímil mediante revisión IA-asistida. Se rechazaron 530 falsos límites y permanecen 1,965 artículos activos provisionales; todos cuentan con transcripción diplomática completa IA-asistida. Este logro expresa **cobertura editorial documental**, no validación humana ni exactitud lingüística definitiva.

Las notas diplomáticas se clasifican en `none`, `resolved_editorial_note` y `open_validation`. De 676 registros con alguna nota, 194 son historia editorial ya resuelta y 482 constituyen la cola científica abierta.

La serie **`RHD-PHIL-001`–`RHD-PHIL-010` ha recotejado los 482/482 casos abiertos** contra el facsímil de alta resolución. La cola automática está agotada. Una disposición `confirmed_ai_assisted` sostiene una lectura; `corrected_ai_assisted` propone una reparación documental; `unresolved_after_ai_recollation` conserva expresamente la incertidumbre. En los tres casos las banderas humanas siguen en falso.

Una propuesta `corrected_ai_assisted` no reemplaza automáticamente `headword_diplomatic` ni `article_diplomatic`. Sólo una decisión independiente, documentada y revisable, podrá adoptarla, modificarla o rechazarla en una futura capa crítica o normalizada.

## Siguiente fase: juicio independiente

`data/validation/human_review_queue.json` contiene 482 registros preparados para revisión humana. En el estado actual hay **0 registros `human_verified`, 0 `philologically_verified_by_human` y 0 `linguistically_verified`**.

La revisión debe declarar su alcance. Confirmar una lectura gráfica no implica confirmar una etimología, un análisis morfológico, una identificación botánica/zoológica o una descripción cultural. Cada una de esas decisiones debe registrar competencia, responsable y evidencia propias.

Los casos `unresolved_after_ai_recollation` deben tener prioridad. A continuación deben adjudicarse las propuestas `corrected_ai_assisted`. Las confirmaciones IA-asistidas también pueden requerir evaluación lingüística, semántica o disciplinar aunque su lectura documental sea estable.

## Identificadores y trazabilidad

Los identificadores ya asignados no se reciclan. Las transformaciones deben quedar registradas en el historial editorial. Una futura fusión, división o correspondencia con Rarámuri Digital debe enlazar IDs y declarar método, confianza y responsable.

## Discurso histórico

Los juicios coloniales, etnocéntricos o misioneros se conservan como parte de la fuente y se atribuyen al autor. Las notas modernas distinguen descripción documental, traducción y comentario editorial. La conservación documental no constituye adhesión editorial ni validación de las afirmaciones históricas de la fuente.
