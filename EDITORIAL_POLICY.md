# Política editorial

## Principio de no sobrescritura

La forma documental es evidencia histórica. Toda corrección, restauración, modernización, traducción o interpretación vive en una capa separada y deja rastro de procedencia. Una lectura propuesta durante una fase posterior nunca borra la transcripción diplomática que motivó la revisión.

## Capas

1. **Facsímil:** imagen de la edición histórica y autoridad documental primaria.
2. **OCR bruto:** salida automática preservada sin corrección.
3. **Segmentación automática:** propuesta de límites de artículo orientada a máxima cobertura.
4. **Cotejo de límites:** decisión editorial IA-asistida sobre arranques, páginas, columnas y falsos positivos.
5. **Transcripción diplomática:** caracteres y artículos completos cotejados con la página; puede ser IA-asistida sin implicar validación humana.
6. **Recotejo filológico IA-asistido:** segunda inspección de lecturas marcadas como abiertas, registrada en `RHD-PHIL-###` sin sobrescribir la capa diplomática.
7. **Validación humana independiente:** revisión filológica, lingüística, semántica o disciplinar con revisor, fecha, competencia, decisión y evidencia explícitas.
8. **Normalización:** forma auxiliar para búsqueda o comparación; siempre enlazada a la diplomática.
9. **Anotación:** traducción, gramática, etiquetas culturales y correspondencias diacrónicas.

## Estado editorial actual

Los 2,495 candidatos segmentados han sido cotejados directamente contra el facsímil mediante revisión IA-asistida. Se rechazaron 530 falsos límites y permanecen 1,965 artículos activos provisionales; todos cuentan con transcripción diplomática completa IA-asistida. Este logro expresa **cobertura editorial documental**, no validación humana ni exactitud lingüística definitiva.

Las notas diplomáticas se clasifican ahora en `none`, `resolved_editorial_note` y `open_validation`. Una nota no vacía no equivale automáticamente a una incertidumbre: las correcciones ya resueltas permanecen documentadas como historia editorial, mientras sólo `open_validation` ingresa a la cola científica.

La primera cola científica contiene 482 casos abiertos. El triage automático sirve para ordenar el trabajo y no debe citarse como diagnóstico lingüístico. Los manifiestos `RHD-PHIL` pueden confirmar una lectura, proponer una corrección o declarar que el problema sigue irresoluble tras recotejo IA-asistido. En los tres casos `human_verified=false`.

Una propuesta `corrected_ai_assisted` se conserva como lectura candidata en la capa de validación; no reemplaza automáticamente `headword_diplomatic` ni `article_diplomatic`. Sólo una política editorial posterior, documentada y revisable, podrá decidir qué lectura derivada se adopta en una edición crítica o normalizada.

## Identificadores y trazabilidad

Los identificadores ya asignados no se reciclan. Las transformaciones deben quedar registradas en el historial editorial. Una futura fusión, división o correspondencia con Rarámuri Digital debe enlazar IDs y declarar método, confianza y responsable.

## Discurso histórico

Los juicios coloniales, etnocéntricos o misioneros se conservan como parte de la fuente y se atribuyen al autor. Las notas modernas distinguen descripción documental, traducción y comentario editorial. La conservación documental no constituye adhesión editorial.
