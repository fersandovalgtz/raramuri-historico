# Matriz de terminación — Steffel / RHD 1.0 machine-only

**Corte:** 15 de agosto de 2026  
**Avance ponderado:** **93.0%**  
**Restante ponderado:** **7.0%**

## Alcance

Esta matriz mide la terminación de Steffel como **edición histórico-digital científica, computacional e IA-asistida**, con cero intervención humana requerida y con incertidumbre explícita donde la evidencia no permite una lectura única. El 93.0% no es una tasa de exactitud lingüística ni una afirmación de validación humana.

| Dimensión | Peso | Avance | Puntos |
|---|---:|---:|---:|
| Cobertura documental, segmentación y diplomática | 30 | 100% | 30.00 |
| Recotejo IA y contabilidad explícita de incertidumbre | 20 | 100% | 20.00 |
| Arquitectura reusable RHD 1.0 y procedencia | 15 | 100% | 15.00 |
| TEI / Lex-0 / IIIF | 10 | 80% | 8.00 |
| Investigación diacrónica computacional | 10 | 75% | 7.50 |
| Apéndice numérico + 22 fórmulas + Padre Nuestro | 5 | 90% | 4.50 |
| Release, integridad, archivo y citabilidad | 5 | 60% | 3.00 |
| Replicación end-to-end con una segunda fuente | 5 | 100% | 5.00 |
| **Total** | **100** |  | **93.00** |

## Gates cerrados

El cuerpo lexicográfico está cerrado en el alcance machine-only: 2,495 candidatos tienen disposición, 1,965 artículos permanecen activos y 1,965 cuentan con transcripción diplomática IA-asistida. Los 482 problemas explícitos tienen estado terminal computacional: 284 `confirmed_ai_assisted`, 152 `corrected_ai_assisted` y 46 `unresolved_after_ai_recollation`. La incertidumbre irresuelta es un estado científico trazable, no una tarea humana pendiente.

La arquitectura RHD 1.0 está implementada mediante esquema canónico, perfiles de fuente, plantilla reusable, procedencia y pruebas automáticas. La proyección TEI Lex-0 estricta valida contra el RNG oficial 0.9.5, mientras la TEI RHD rica conserva las capas documentales y epistemológicas que no pertenecen a Lex-0.

Los anexos finales tienen mapeo facsimilar reproducible: PDF 79–84 corresponde a impreso 369–374. Existen 24 objetos canónicos: una sección de numeración, 22 fórmulas paralelas y un Padre Nuestro separado. La numeración está estructurada computacionalmente; las 22 fórmulas tienen alineación visual IA latín–alemán–tarahumara con confianza por campo; y el Padre Nuestro conserva incertidumbre gráfica explícita. Todo se serializa en un suplemento TEI específico y permanece fuera de Lex-0.

Las 298 relaciones diacrónicas cuentan con puntuaciones reproducibles de **apoyo documental de recuperación**. Ninguna puntuación se interpreta como equivalencia semántica, cognación, etimología o continuidad histórica; todas las relaciones permanecen `candidate`.

## Segunda fuente: gate de industrialización cerrado

La segunda fuente piloto es **Miguel Joaquín Tellechea, 1826, _Compendio gramatical para la inteligencia del idioma tarahumar_**. Su PDF público de la Dirección General de Bibliotecas está fijado como `RHD-WIT-TELLECHEA-1826-DGB`: **205 páginas, 95,088,307 bytes, SHA-256 `c67b7942090613c494d8057be8aff59ea13a11519c29eae469afad8a85c30dfc`**.

La prueba mínima ya había demostrado que una unidad gramatical y una unidad de disposición paralela podían atravesar el pipeline. La prueba fuerte está igualmente cerrada: GitHub Actions procesa **205/205 páginas** como unidades documentales persistentes, conserva la capa textual embebida, aplica OCR visual separado en páginas escasas, valida los 205 objetos contra el mismo JSON Schema RHD y genera una TEI documental completa. El proceso registra **cero rediseños del núcleo universal**, **cero entradas Lex-0 fabricadas** y **cero atribuciones de validación humana**. El producto completo se publica como artefacto reproducible `tellechea-1826-full-witness-rhd-pilot` en CI.

Esto demuestra a escala completa que RHD puede industrializar una fuente histórica estructuralmente distinta del diccionario de Steffel sin convertir reglas particulares de Tellechea en reglas universales. La dimensión de replicación es **100%**. Esto no equivale a declarar una edición crítica humana de Tellechea; es el cierre del gate de reutilización computacional definido por RHD.

## IIIF: identidad canónica preservada; proveedor externo mutable

El witness de trabajo de 84 páginas permanece fijado internamente por SHA-256 `4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f`, tamaño **6,251,443 bytes** y **84 páginas**. Es la autoridad de identidad del proyecto.

El ítem Internet Archive `tarahumarischesw00stef` sigue registrado como witness paralelo no canónico porque su comparación perceptual con el facsímil de trabajo mostró una divergencia fuerte. El ejemplar Getty/Internet Archive se mantiene también como candidato externo sujeto a comprobación y nunca sustituye automáticamente al witness canónico.

El enlace de Dropbox publicado por el Repositorio de Lenguas es **mutable**. Una ejecución anterior llegó a recuperar un binario de 84 páginas que coincidía con el witness fijado, pero una ejecución posterior del 15 de agosto de 2026 recuperó desde la misma URL un PDF distinto: **438 páginas, 26,702,093 bytes, SHA-256 `3c2169d818770fecff7eca822c7dcc52f35d66356c5279913d85fb5364c652ce`**. La búsqueda automática de una ventana contigua de 84 páginas tampoco estableció identidad visual con el witness canónico. Por tanto, el enlace externo se conserva solamente como **fuente mutable diagnóstica**, no como dependencia de construcción ni evidencia de identidad.

La CI científica queda desacoplada de esa mutabilidad: el probe puede registrar cambios del proveedor, pero un cambio externo no bloquea las capas checksum-fixed, Tellechea, TEI, Lex-0, anexos, diacronía ni manifiesto de integridad. La publicación IIIF canónica se cerrará únicamente cuando los recursos de imagen deriven del witness exacto o de una copia cuya identidad haya sido demostrada de nuevo.

## El 7% que permanece abierto

El residual ponderado está concentrado en cuatro frentes:

1. **IIIF canónico — 2.0 puntos:** publicar recursos de imagen estables derivados del witness exacto y un Manifest Presentation 3 canónico con 84 Canvases, más localizadores página/Canvas y, donde corresponda, regiones. Ninguna URL mutable puede cerrar este gate por sí sola.
2. **Release científico — 2.0 puntos:** fijar versión, completar `CITATION`, publicar release estable y depositarlo en un archivo con identificador persistente. El manifiesto de integridad ya existe.
3. **Investigación diacrónica — 2.5 puntos:** completar la calibración y productos de investigación documental sobre las 298 relaciones sin promoverlas artificialmente a afirmaciones semánticas o etimológicas.
4. **Refinamiento residual del apéndice — 0.5 puntos:** consolidar las lecturas gráficas de baja confianza o mantenerlas explícitamente como incertidumbre terminal documentada.

## Condición de 100%

Dentro del alcance machine-only, **100% no significa ausencia absoluta de ambigüedad**. Significa que toda ambigüedad detectada tiene representación explícita y trazable; que todos los productos son reproducibles e íntegros; que los anexos están incorporados; que el facsímil canónico tiene representación IIIF estable; que existe un release citable y archivado; y que el núcleo RHD demostró su reutilización a escala completa en una segunda fuente real. Este último requisito ya está cerrado con Tellechea 1826.
