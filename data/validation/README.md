# Scientific validation layer

Esta carpeta inaugura la fase posterior a la primera pasada editorial integral contra el facsímil. Su propósito es separar con rigor cuatro operaciones que no deben confundirse: recotejo filológico de lecturas inciertas, evaluación lingüística de formas históricas rarámuri, normalización auxiliar y correspondencias diacrónicas.

La capa diplomática permanece inmutable como evidencia documental. Ninguna normalización, interpretación semántica o decisión lingüística debe sobrescribir `headword_diplomatic` ni `article_diplomatic`.

## Estado de entrada

El corpus tiene 2,495 candidatos facsimilarmente revisados. Tras rechazar 530 falsos límites quedan 1,965 artículos activos provisionales, todos con transcripción diplomática completa IA-asistida. Los registros con `diplomatic_note` no vacío forman la primera cola científica de incertidumbres. Su clasificación es heurística y reproducible; no equivale a validación humana, filológica ni lingüística.

## Artefactos generados

- `uncertainty_queue.json`: cola integral, ordenada por prioridad, con artículo diplomático, nota y acción recomendada.
- `uncertainty_queue_compact.json`: vista compacta para selección de lotes de revisión.
- `validation_inventory.json`: conteos por tipo de incertidumbre y estados de validación.

La prioridad automática distingue, en este orden, problemas de lectura gráfica, estructura del artículo, forma histórica rarámuri, semántica/glosa y otras incertidumbres editoriales. La clasificación se deriva de las notas editoriales existentes y debe entenderse como triage, no como análisis lingüístico definitivo.

## Próximos manifiestos

Los recotejos filológicos IA-asistidos se documentarán como `RHD-PHIL-###` y siempre mantendrán `human_verified=false`. Una validación humana futura deberá registrar revisor, fecha, competencia, decisión y evidencia, sin borrar la lectura previa.

Las normalizaciones se alojarán en una capa separada y deberán incluir método, confianza y vínculo al `record_id`. Las correspondencias con Rarámuri Digital se modelarán del mismo modo: relación explícita, no fusión silenciosa.
