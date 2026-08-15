# Matriz de terminación — Steffel / RHD 1.0 machine-only

**Corte:** 15 de agosto de 2026  
**Avance ponderado:** **90.0%**  
**Restante ponderado:** **10.0%**

## Alcance

Esta matriz sustituye, para el alcance vigente, la métrica que consideraba obligatoria una futura revisión humana. El objetivo actual es terminar Steffel como **edición histórico-digital científica, computacional e IA-asistida**, con cero intervención humana requerida y con incertidumbre explícita donde la evidencia no permite una lectura única.

El 90.0% no es una tasa de exactitud lingüística ni una afirmación de validación humana. Es una medida ponderada de terminación del objeto científico-digital y de la infraestructura reusable RHD.

| Dimensión | Peso | Avance | Puntos |
|---|---:|---:|---:|
| Cobertura documental, segmentación y diplomática | 30 | 100% | 30.00 |
| Recotejo IA y contabilidad explícita de incertidumbre | 20 | 100% | 20.00 |
| Arquitectura reusable RHD 1.0 y procedencia | 15 | 100% | 15.00 |
| TEI / Lex-0 / IIIF | 10 | 80% | 8.00 |
| Investigación diacrónica computacional | 10 | 75% | 7.50 |
| Apéndice numérico + 22 fórmulas + Padre Nuestro | 5 | 90% | 4.50 |
| Release, integridad, archivo y citabilidad | 5 | 60% | 3.00 |
| Replicación end-to-end con una segunda fuente | 5 | 40% | 2.00 |
| **Total** | **100** |  | **90.00** |

## Qué está cerrado

El cuerpo lexicográfico está cerrado en el alcance machine-only: 2,495 candidatos tienen disposición, 1,965 artículos permanecen activos y 1,965 cuentan con transcripción diplomática IA-asistida. Los 482 problemas explícitos tienen estado terminal computacional: 284 confirmados por IA, 152 con corrección propuesta por IA y 46 conservados como irresueltos después del recotejo. La categoría `unresolved_after_ai_recollation` es un resultado científico legítimo, no una tarea humana pendiente.

La arquitectura RHD 1.0 está implementada mediante esquema canónico, perfil de fuente, plantilla reusable, procedencia y pruebas automáticas. La proyección TEI Lex-0 estricta valida contra el RNG oficial 0.9.5, mientras que la TEI RHD rica conserva capas que deliberadamente no pertenecen a Lex-0. La plantilla y los perfiles Steffel/Tellechea son probados en CI para impedir que reaparezcan por accidente requisitos de adjudicación humana.

Los anexos finales tienen mapeo facsimilar IA comprobado: PDF 79–84 corresponde a impreso 369–374. Existen 24 objetos canónicos: una sección de numeración, 22 fórmulas paralelas y un Padre Nuestro separado. El sistema numeral ya está estructurado computacionalmente; las 22 fórmulas tienen alineación visual IA latín–alemán–tarahumara con confianza por campo; el Padre Nuestro cuenta con transcripción visual IA y segmentos inciertos explícitos. Todo ello se serializa en un suplemento TEI específico y se mantiene fuera de la exportación Lex-0 estricta.

Las 298 relaciones diacrónicas cuentan con una puntuación reproducible de **apoyo documental de recuperación**, calculada a partir de similitud gráfica conservadora, atestiguaciones internas y apoyo documental recíproco. La puntuación no representa semántica, cognación, etimología ni continuidad histórica; todas las relaciones siguen siendo `candidate`.

El release cuenta con un generador determinista de manifiesto de integridad que calcula SHA-256, tamaños y conteos, y con una prueba independiente que recompone esos valores durante CI. El paquete incluye las capas visuales del apéndice, la TEI específica de anexos, el registro de witnesses, huellas perceptuales para control IIIF y la declaración de conformidad machine-only.

## Avances parciales que ya reciben crédito

Se localizó y verificó en CI un Manifest IIIF Presentation 3 del ítem de Internet Archive `tarahumarischesw00stef`, pero la comparación perceptual contra el facsímil checksum-fixed de RHD mostró una divergencia fuerte. Se conserva por ello como **witness paralelo no canónico** y como control negativo: no se le asignan localizadores de evidencia RHD. Esto fortalece la integridad del proyecto, pero no cierra IIIF porque todavía falta servir o identificar de manera estable el escaneo canónico exacto.

La segunda fuente piloto, **Miguel Joaquín Tellechea, 1826, _Compendio gramatical para la inteligencia del idioma tarahumar_**, ya tiene witness reproducible. El PDF público de la Dirección General de Bibliotecas está fijado como `RHD-WIT-TELLECHEA-1826-DGB`: 205 páginas, 95,088,307 bytes y SHA-256 `c67b7942090613c494d8057be8aff59ea13a11519c29eae469afad8a85c30dfc`. La CI exige que esa identidad permanezca exacta y caracteriza su capa textual sin confundirla con una transcripción diplomática.

Además, Tellechea ya superó la **prueba mínima end-to-end** definida para el piloto. Dos unidades reales y estructuralmente diferentes —una página gramatical identificada por el ancla `LIBRO PRIMERO / CAPITULO I` y la página impresa 49 usada como prueba de disposición paralela— atraviesan verificación del witness, extracción de texto embebido, renderizado del facsímil, OCR visual independiente, segmentación, representación canónica RHD y exportación TEI. El proceso conserva por separado las capas documentales, no fabrica equivalencias lingüísticas y no atribuye validación humana.

Por ello la dimensión de replicación pasa de 0% a **40%**. Es un crédito deliberadamente conservador: demuestra que el núcleo funciona fuera del diccionario y que el pipeline puede procesar una fuente histórica distinta sin rediseño fundamental, pero la prueba fuerte exige todavía extender el procedimiento al alcance completo declarado para las 205 páginas.

## El 10% que permanece abierto

El trabajo residual se concentra principalmente en tres frentes y un margen menor de refinamiento:

1. **IIIF canónico:** publicar el facsímil checksum-fixed del proyecto mediante un servicio estable o localizar una representación inequívocamente idéntica, y extender el mapeo página/Canvas al testimonio completo.
2. **Release científico:** fijar versión, `CITATION`, release estable, archivo/depósito e identificador persistente. `CHANGELOG` y el manifiesto de integridad ya están preparados.
3. **Prueba fuerte de industrialización:** extender el pipeline probado sobre Tellechea al witness completo de 205 páginas, documentando cualquier cambio inevitable y manteniendo las peculiaridades de la fuente fuera del núcleo universal.
4. **Refinamiento residual del apéndice:** pueden mejorarse lecturas gráficas de baja confianza, pero bajo el alcance machine-only no es obligatorio eliminar toda ambigüedad; puede conservarse como incertidumbre terminal documentada.

## Condición de 100%

Dentro del alcance machine-only, **100% no significa ausencia absoluta de ambigüedad**. Significa que toda ambigüedad detectada tiene representación explícita y trazable; que todos los productos científicos son reproducibles e íntegros; que los anexos están incorporados; que el facsímil canónico tiene enlace estable; que existe un release citable y archivado; y que el núcleo RHD ha demostrado su reutilización en el alcance completo declarado de una segunda fuente real sin rediseño fundamental.
