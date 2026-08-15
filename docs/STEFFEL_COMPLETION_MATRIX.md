# Matriz de terminación científica — Steffel / RHD 1.0

**Corte:** 15 de agosto de 2026  
**Objeto evaluado:** terminar científicamente el Corpus Steffel 1791/1809 y convertirlo en implementación de referencia suficientemente robusta para reutilizar el método en nuevas fuentes históricas.

## Regla de cálculo

El porcentaje no representa exactitud lingüística ni tasa de validación. Es una medida de **terminación ponderada del proyecto científico-editorial y de su infraestructura reusable**. Cada dimensión tiene un peso distinto según su importancia para poder declarar Steffel terminado y RHD replicable.

| Dimensión | Peso | Avance computado | Puntos | Evidencia / condición pendiente |
|---|---:|---:|---:|---|
| 1. Cobertura documental, segmentación y transcripción diplomática | 30 | 100% | 30.0 | 2,495 candidatos cotejados; 1,965 artículos activos; 1,965 transcripciones diplomáticas IA-asistidas; cola automática documental agotada. |
| 2. Validación humana independiente y capa crítica | 20 | 25% | 5.0 | Protocolo, cola, prioridades, recotejo PHIL y 482 casos empaquetados para revisión; **0/482** tienen adjudicación humana independiente. El 25% mide infraestructura/preparación, no tasa de revisión humana. |
| 3. Arquitectura reusable RHD 1.0 y procedencia | 15 | 100% | 15.0 | Especificación, JSON Schema, perfil Steffel, plantilla de nuevas fuentes, adaptador canónico, procedencia, 482 eventos PHIL y 298 relaciones diacrónicas integradas con pruebas. |
| 4. Interoperabilidad TEI/TEI Lex-0/IIIF | 10 | 80% | 8.0 | TEI RHD rico separado de proyección Lex-0 estricta; la proyección estricta valida en CI contra el RNG oficial TEI Lex-0 0.9.5. Falta IIIF sobre facsímil real y enlaces espaciales. |
| 5. Investigación diacrónica y comparativa | 10 | 60% | 6.0 | 298 candidatos, concordancia interna y controles incorporados sin promoción semántica automática; falta adjudicación humana semántica, etimológica y de continuidad para relaciones seleccionadas. |
| 6. Apéndices y muestra lingüística final | 5 | 30% | 1.5 | Ya existe inventario OCR estructurado del apéndice de numeración, 22 bloques de la muestra trilingüe y el Padre Nuestro separado; falta cotejo facsimilar diplomático e integración canónica/TEI. |
| 7. Release científico, archivo y citabilidad 1.0 | 5 | 40% | 2.0 | Repositorio, licencias, CITATION y documentación existen; falta release RHD 1.0 estable, DOI/depósito/archivo final y declaración de conformidad. |
| 8. Prueba de replicabilidad sobre una segunda fuente | 5 | 0% | 0.0 | Existe plantilla reusable, pero el núcleo todavía no ha sido probado de extremo a extremo con una segunda fuente histórica real. |
| **TOTAL** | **100** |  | **67.5** |  |

## Resultado actualizado

**Avance global ponderado exacto: 67.5%.**  
**Trabajo restante ponderado exacto: 32.5%.**

Para comunicación ordinaria puede expresarse como **68% realizado / 32% pendiente**. Se recomienda mantener una incertidumbre de aproximadamente ±3 puntos porque la revisión humana y la primera segunda-fuente real pueden revelar problemas no observables desde la automatización.

## Distinciones indispensables

- **Cobertura documental IA-asistida del cuerpo lexicográfico:** prácticamente completa.
- **Adjudicación humana independiente:** 0/482; no debe confundirse con el 67.5% global.
- **Infraestructura reusable:** ya cuenta con implementación canónica, perfiles de fuente, pruebas y una proyección Lex-0 validada.
- **Edición crítica científicamente cerrada:** todavía no alcanzada.

## Avances realizados en este ciclo RHD 1.0

1. Los diez manifiestos `RHD-PHIL-001–010` se proyectan como 482 eventos filológicos `ai_assisted`, sin fabricar validación humana.
2. Las 298 hipótesis Steffel ↔ Rarámuri Digital se integran como relaciones `candidate`; se preserva que no existe juicio semántico, etimológico ni de continuidad automática.
3. Se generan 482 paquetes de revisión humana, ordenados 46 / 152 / 284, con decisiones humanas en blanco.
4. Se separa la edición TEI RHD rica de una proyección Lex-0 estricta para no forzar categorías propias del proyecto dentro del estándar lexicográfico.
5. La proyección Lex-0 estricta pasa el RNG oficial TEI Lex-0 0.9.5 en GitHub Actions.
6. Se estructura a nivel OCR el apéndice de numeración, la muestra de 22 fórmulas latín–alemán–tarahumara y el Padre Nuestro como bloque independiente, sin atribuirles cotejo facsimilar todavía.
7. Se crea una plantilla reusable de perfil de fuente y se documenta el bloqueo legítimo de IIIF: falta una fuente estable de imágenes/facsímil direccionable.

## Camino crítico para llegar a 100%

1. Ejecutar revisión humana independiente, empezando por 46 casos irresueltos, después 152 correcciones propuestas y finalmente 284 confirmaciones IA-asistidas según el alcance especializado requerido.
2. Crear la capa de lectura crítica que adopte decisiones humanas sin sobrescribir la diplomática.
3. Publicar el facsímil mediante URIs/servicio estable y cerrar IIIF con Canvases y, cuando existan coordenadas reales, regiones de entrada.
4. Cotejar contra facsímil el apéndice de numeración y los 22 bloques trilingües; después integrarlos al modelo canónico y TEI.
5. Adjudicar una muestra científicamente prioritaria de las relaciones diacrónicas y publicar estados explícitos de certeza.
6. Preparar release 1.0, DOI/depósito/archivo y declaración de conformidad.
7. Ejecutar una segunda fuente piloto mediante `source_profiles/_template.source.json`; documentar únicamente las modificaciones del núcleo que esa prueba demuestre necesarias.

## Criterio de cierre

RHD Steffel podrá considerarse completamente terminado como modelo de referencia cuando las capas documentales sean reproducibles, el universo declarado de revisión humana esté adjudicado o explícitamente marcado como irresoluble, los productos interoperables validen, anexos y corpus paralelo estén estructurados, la edición tenga un release científico citable y el mismo pipeline haya procesado una segunda fuente sin rediseño fundamental.
