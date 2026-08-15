# Matriz de terminación — Steffel / RHD 1.0 machine-only

**Corte:** 15 de agosto de 2026  
**Avance ponderado:** **99.0%**  
**Restante ponderado:** **1.0%**

## Alcance

Esta matriz mide la terminación de Steffel como **edición histórico-digital científica, computacional e IA-asistida**, con cero intervención humana requerida y con incertidumbre explícita donde la evidencia no permite una lectura única. El porcentaje no es una tasa de exactitud lingüística ni una afirmación de validación humana.

| Dimensión | Peso | Avance | Puntos |
|---|---:|---:|---:|
| Cobertura documental, segmentación y diplomática | 30 | 100% | 30.00 |
| Recotejo IA y contabilidad explícita de incertidumbre | 20 | 100% | 20.00 |
| Arquitectura reusable RHD 1.0 y procedencia | 15 | 100% | 15.00 |
| TEI / Lex-0 / IIIF | 10 | 100% | 10.00 |
| Investigación diacrónica computacional | 10 | 100% | 10.00 |
| Apéndice numérico + 22 fórmulas + Padre Nuestro | 5 | 100% | 5.00 |
| Release, integridad, archivo y citabilidad | 5 | 80% | 4.00 |
| Replicación end-to-end con una segunda fuente | 5 | 100% | 5.00 |
| **Total** | **100** |  | **99.00** |

## Gates científicos cerrados

El cuerpo lexicográfico está cerrado en alcance machine-only: 2,495 candidatos tienen disposición, 1,965 artículos permanecen activos y 1,965 cuentan con transcripción diplomática IA-asistida. Los 482 problemas explícitos tienen estado terminal computacional: 284 `confirmed_ai_assisted`, 152 `corrected_ai_assisted` y 46 `unresolved_after_ai_recollation`.

La arquitectura RHD 1.0, el JSON Schema, los perfiles de fuente y la procedencia están implementados. La TEI RHD rica y la proyección TEI Lex-0 estricta permanecen separadas; Lex-0 valida contra el RNG oficial 0.9.5.

Los anexos están cerrados al 100%: `PDF 79–84 ↔ impreso 369–374`, 24 objetos canónicos y 43 incertidumbres terminales explícitas. La capa diacrónica también está cerrada: 298 relaciones `candidate`, calibradas contra 5,066 emparejamientos nulos deterministas, sin convertir similitud grafémica en cognación, semántica o continuidad histórica.

## Segunda fuente: industrialización cerrada

Miguel Joaquín Tellechea (1826) se procesa en 205/205 páginas con el mismo núcleo RHD: 0 rediseños del núcleo universal, 0 entradas Lex-0 fabricadas y 0 atribuciones humanas. El gate de replicación está al 100%.

## IIIF: gate público cerrado

El witness canónico de Steffel permanece fijado como 84 páginas, 6,251,443 bytes, SHA-256 `4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f`.

La publicación IIIF Presentation 3 está desplegada en GitHub Pages con 84 Canvases y 1,965 enlaces registro→Canvas, sin regiones `xywh` inventadas. El pipeline canónico de `main` ejecutó con éxito el gate **Verify published canonical Steffel IIIF endpoint if available** después de la fusión del PR #2. Por ello la dimensión TEI / Lex-0 / IIIF pasa a 100%.

## Release científico

La licencia definitiva queda fijada como **MIT para software/código** y **CC BY 4.0 para datos, metadatos y capas editoriales originales de RHD**, preservando aparte el estatus jurídico de fuentes históricas y materiales de terceros.

`CITATION.cff` se prepara como `1.0.0`. El GitHub Release `v1.0.0` se crea únicamente después de que el pipeline canónico del commit candidato en `main` termine verde. La creación del tag/release no equivale por sí sola al cierre del archivo persistente.

## El 1% que permanece abierto

Queda exclusivamente el gate de **archivo/citabilidad persistente**: depositar el snapshot estable `v1.0.0` en un archivo público con identificador persistente real (preferentemente Zenodo/DOI), comprobar su correspondencia con el tag/commit y el manifiesto de integridad, e incorporar ese identificador a los metadatos.

## Condición de 100%

Dentro del alcance machine-only, 100% no significa ausencia de ambigüedad. Significa que el objeto científico ya terminado, interoperable y publicado por IIIF esté además **archivado y citable mediante un identificador persistente real**.
