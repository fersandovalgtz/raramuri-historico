# Matriz de terminación — Steffel / RHD 1.0 machine-only

**Corte:** 15 de agosto de 2026  
**Avance ponderado:** **88.0%**  
**Restante ponderado:** **12.0%**

## Alcance

Esta matriz sustituye, para el alcance vigente, la métrica que consideraba obligatoria una futura revisión humana. El objetivo actual es terminar Steffel como **edición histórico-digital científica, computacional e IA-asistida**, con cero intervención humana requerida y con incertidumbre explícita donde la evidencia no permite una lectura única.

El 88.0% no es una tasa de exactitud lingüística ni una afirmación de validación humana. Es una medida ponderada de terminación del objeto científico-digital y de la infraestructura reusable RHD.

| Dimensión | Peso | Avance | Puntos |
|---|---:|---:|---:|
| Cobertura documental, segmentación y diplomática | 30 | 100% | 30.00 |
| Recotejo IA y contabilidad explícita de incertidumbre | 20 | 100% | 20.00 |
| Arquitectura reusable RHD 1.0 y procedencia | 15 | 100% | 15.00 |
| TEI / Lex-0 / IIIF | 10 | 80% | 8.00 |
| Investigación diacrónica computacional | 10 | 75% | 7.50 |
| Apéndice numérico + 22 fórmulas + Padre Nuestro | 5 | 90% | 4.50 |
| Release, integridad, archivo y citabilidad | 5 | 60% | 3.00 |
| Replicación end-to-end con una segunda fuente | 5 | 0% | 0.00 |
| **Total** | **100** |  | **88.00** |

## Qué está cerrado

El cuerpo lexicográfico está cerrado en el alcance machine-only: 2,495 candidatos tienen disposición, 1,965 artículos permanecen activos y 1,965 cuentan con transcripción diplomática IA-asistida. Los 482 problemas explícitos tienen estado terminal computacional: 284 confirmados por IA, 152 con corrección propuesta por IA y 46 conservados como irresueltos después del recotejo. La categoría `unresolved_after_ai_recollation` es un resultado científico legítimo, no una tarea humana pendiente.

La arquitectura RHD 1.0 está implementada mediante esquema canónico, perfil de fuente, plantilla reusable, procedencia y pruebas automáticas. La proyección TEI Lex-0 estricta valida contra el RNG oficial 0.9.5, mientras que la TEI RHD rica conserva capas que deliberadamente no pertenecen a Lex-0.

Los anexos finales tienen mapeo facsimilar IA comprobado: PDF 79–84 corresponde a impreso 369–374. Existen 24 objetos canónicos: una sección de numeración, 22 fórmulas paralelas y un Padre Nuestro separado. El sistema numeral ya está estructurado computacionalmente; las 22 fórmulas tienen alineación visual IA latín–alemán–tarahumara con confianza por campo; el Padre Nuestro cuenta con transcripción visual IA y segmentos inciertos explícitos. Todo ello se serializa en un suplemento TEI específico y se mantiene fuera de la exportación Lex-0 estricta.

Las 298 relaciones diacrónicas cuentan con una puntuación reproducible de **apoyo documental de recuperación**, calculada a partir de similitud gráfica conservadora, atestiguaciones internas y apoyo documental recíproco. La puntuación no representa semántica, cognación, etimología ni continuidad histórica; todas las relaciones siguen siendo `candidate`.

El release cuenta con un generador determinista de manifiesto de integridad que calcula SHA-256, tamaños y conteos, y con una prueba independiente que recompone esos valores durante CI. El paquete incluye ahora también las capas visuales del apéndice, la TEI específica de anexos y la declaración de conformidad machine-only.

## El 12% que permanece abierto

El trabajo residual se concentra principalmente en tres frentes y un margen menor de refinamiento:

1. **IIIF:** verificar un Manifest real y estable del witness externo o desplegar uno controlado, y extender el mapeo página/Canvas al testimonio completo.
2. **Release científico:** fijar versión, `CHANGELOG`, `CITATION`, release estable, archivo/depósito e identificador persistente.
3. **Prueba de industrialización:** procesar una segunda fuente histórica real end-to-end mediante el mismo núcleo RHD y documentar cualquier cambio inevitable.
4. **Refinamiento residual del apéndice:** pueden mejorarse lecturas gráficas de baja confianza, pero bajo el alcance machine-only no es obligatorio eliminar toda ambigüedad; puede conservarse como incertidumbre terminal documentada.

## Condición de 100%

Dentro del alcance machine-only, **100% no significa ausencia absoluta de ambigüedad**. Significa que toda ambigüedad detectada tiene representación explícita y trazable; que todos los productos científicos son reproducibles e íntegros; que los anexos están incorporados; que el facsímil tiene enlace estable; que existe un release citable y archivado; y que el núcleo RHD ha demostrado su reutilización con una segunda fuente real sin rediseño fundamental.
