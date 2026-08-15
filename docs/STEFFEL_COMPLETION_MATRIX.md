# Matriz de terminación científica — Steffel / RHD 1.0

**Corte:** 15 de agosto de 2026  
**Objeto evaluado:** terminar científicamente el Corpus Steffel 1791/1809 y convertirlo en implementación de referencia suficientemente robusta para reutilizar el método en nuevas fuentes históricas.

## Regla de cálculo

El porcentaje no representa exactitud lingüística ni tasa de validación. Es una medida de **terminación ponderada del proyecto científico-editorial y de su infraestructura reusable**. Cada dimensión tiene un peso distinto según su importancia para poder declarar Steffel terminado y RHD replicable.

| Dimensión | Peso | Avance computado | Puntos | Evidencia / condición pendiente |
|---|---:|---:|---:|---|
| 1. Cobertura documental, segmentación y transcripción diplomática | 30 | 100% | 30.0 | 2,495 candidatos cotejados; 1,965 artículos activos; 1,965 transcripciones diplomáticas IA-asistidas; cola automática documental agotada. |
| 2. Validación humana independiente y capa crítica | 20 | 25% | 5.0 | Protocolo, cola, prioridades, recotejo PHIL y paquetes preparados; pero 0/482 casos tienen adjudicación humana independiente. |
| 3. Arquitectura reusable RHD 1.0 y procedencia | 15 | 100% | 15.0 | Especificación, JSON Schema, perfil Steffel, plantilla de nuevas fuentes, adaptador canónico, procedencia, PHIL y relaciones diacrónicas integradas, CI. |
| 4. Interoperabilidad TEI/TEI Lex-0/IIIF | 10 | 70% | 7.0 | TEI P5 se genera desde la capa canónica, con invariantes de cabecera alineadas a Lex-0; falta validación formal del perfil Lex-0 y capa IIIF facsimilar. |
| 5. Investigación diacrónica y comparativa | 10 | 60% | 6.0 | 298 candidatos, concordancia interna y controles; falta adjudicación humana semántica, etimológica y de continuidad para relaciones seleccionadas. |
| 6. Apéndices y muestra lingüística final | 5 | 0% | 0.0 | Numeración y muestra trilingüe aún no estructuradas dentro del modelo RHD. |
| 7. Release científico, archivo y citabilidad 1.0 | 5 | 40% | 2.0 | Repositorio, licencias, CITATION y documentación existen; falta release RHD 1.0 estable, DOI/depósito/archivo final y declaración de conformidad. |
| 8. Prueba de replicabilidad sobre una segunda fuente | 5 | 0% | 0.0 | Ya existe plantilla reusable, pero el núcleo todavía no ha sido probado de extremo a extremo con una segunda fuente histórica. |
| **TOTAL** | **100** |  | **65.0** |  |

## Resultado

**Avance global ponderado: 65%.**  
**Trabajo restante ponderado: 35%.**

Se recomienda interpretar el valor con una incertidumbre de aproximadamente ±3 puntos porque las dimensiones de validación humana y replicación pueden revelar problemas no observables antes de la revisión externa o de una segunda ingestión real.

## Distinciones indispensables

- **Cobertura documental IA-asistida:** prácticamente completa para el cuerpo lexicográfico.
- **Adjudicación humana independiente:** 0/482; no debe confundirse con el avance global del proyecto.
- **Infraestructura reusable:** ya alcanzó una primera implementación funcional y testeada.
- **Edición crítica científicamente cerrada:** todavía no alcanzada.

## Camino crítico para llegar a 100%

1. Ejecutar revisión humana independiente, empezando por 46 casos irresueltos, después 152 correcciones propuestas y finalmente 284 confirmaciones IA-asistidas según el alcance especializado requerido.
2. Crear la capa de lectura crítica que adopte decisiones humanas sin sobrescribir la diplomática.
3. Cerrar validación TEI/TEI Lex-0 y resolver interoperabilidad facsimilar IIIF.
4. Estructurar el apéndice de numeración y la muestra final latín–alemán–rarámuri.
5. Adjudicar una muestra científicamente prioritaria de las relaciones diacrónicas y publicar estados explícitos de certeza.
6. Preparar release 1.0, DOI/depósito/archivo y declaración de conformidad.
7. Ejecutar una segunda fuente piloto mediante `source_profiles/_template.source.json`; documentar únicamente las modificaciones del núcleo que esa prueba demuestre necesarias.

## Criterio de cierre

RHD Steffel podrá considerarse completamente terminado como modelo de referencia cuando las capas documentales sean reproducibles, el universo declarado de revisión humana esté adjudicado o explícitamente marcado como irresoluble, los productos interoperables validen, anexos y corpus paralelo estén estructurados, la edición tenga un release científico citable y el mismo pipeline haya procesado una segunda fuente sin rediseño fundamental.
