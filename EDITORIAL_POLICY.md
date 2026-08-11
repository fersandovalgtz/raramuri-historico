# Política editorial

## Principio de no sobrescritura

La forma documental es evidencia histórica. Toda corrección, restauración, modernización o traducción vive en un campo separado y deja rastro de procedencia.

## Capas

1. **Facsímil:** imagen de la edición histórica.
2. **OCR bruto:** salida automática preservada sin corrección.
3. **Segmentación automática:** propuesta de límites de artículo orientada a máxima cobertura.
4. **Transcripción diplomática:** caracteres y límites cotejados con la página.
5. **Normalización:** forma auxiliar para búsqueda o comparación.
6. **Anotación:** traducción, gramática, etiquetas culturales y correspondencias diacrónicas.

## Estado 0.2.0

El corpus integral se marca `machine_segmented_unverified`. `segmentation_confidence` expresa confianza técnica en el límite propuesto, no exactitud lingüística. Las 60 anclas iniciales se distinguen como `curated_anchor`, pero también conservan pendiente el cotejo facsimilar completo y la validación lingüística.

La revisión puede fusionar, dividir, rechazar o restaurar candidatos. Los identificadores ya asignados no se reciclan; las transformaciones deben quedar registradas en el historial editorial.

## Discurso histórico

Los juicios coloniales, etnocéntricos o misioneros se conservan como parte de la fuente y se atribuyen al autor. Las notas modernas distinguen descripción documental, traducción y comentario editorial.
