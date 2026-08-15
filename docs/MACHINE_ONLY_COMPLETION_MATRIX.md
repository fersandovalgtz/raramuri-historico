# Matriz de terminación — Steffel / RHD 1.0 machine-only

**Corte:** 15 de agosto de 2026  
**Avance ponderado:** **98.0%**  
**Restante ponderado:** **2.0%**

## Alcance

Esta matriz mide la terminación de Steffel como **edición histórico-digital científica, computacional e IA-asistida**, con cero intervención humana requerida y con incertidumbre explícita donde la evidencia no permite una lectura única. El 98.0% no es una tasa de exactitud lingüística ni una afirmación de validación humana.

| Dimensión | Peso | Avance | Puntos |
|---|---:|---:|---:|
| Cobertura documental, segmentación y diplomática | 30 | 100% | 30.00 |
| Recotejo IA y contabilidad explícita de incertidumbre | 20 | 100% | 20.00 |
| Arquitectura reusable RHD 1.0 y procedencia | 15 | 100% | 15.00 |
| TEI / Lex-0 / IIIF | 10 | 90% | 9.00 |
| Investigación diacrónica computacional | 10 | 100% | 10.00 |
| Apéndice numérico + 22 fórmulas + Padre Nuestro | 5 | 100% | 5.00 |
| Release, integridad, archivo y citabilidad | 5 | 80% | 4.00 |
| Replicación end-to-end con una segunda fuente | 5 | 100% | 5.00 |
| **Total** | **100** |  | **98.00** |

## Gates científicos cerrados

El cuerpo lexicográfico está cerrado en el alcance machine-only: 2,495 candidatos tienen disposición, 1,965 artículos permanecen activos y 1,965 cuentan con transcripción diplomática IA-asistida. Los 482 problemas explícitos tienen estado terminal computacional: 284 `confirmed_ai_assisted`, 152 `corrected_ai_assisted` y 46 `unresolved_after_ai_recollation`. La incertidumbre irresuelta es un estado científico trazable, no una tarea humana pendiente.

La arquitectura RHD 1.0 está implementada mediante esquema canónico, perfiles de fuente, plantilla reusable, procedencia y pruebas automáticas. La proyección TEI Lex-0 estricta valida contra el RNG oficial 0.9.5, mientras la TEI RHD rica conserva las capas documentales y epistemológicas que no pertenecen a Lex-0.

Los anexos quedan **cerrados al 100% en alcance machine-only**. El mapeo facsimilar PDF 79–84 ↔ impreso 369–374 está fijado; existen 24 objetos canónicos —numeración, 22 fórmulas paralelas y Padre Nuestro— y todos se serializan en un suplemento TEI específico. Las lecturas medias/bajas remanentes fueron trasladadas a un registro formal de incertidumbre terminal: ninguna se corrige por conjetura y ninguna exige intervención humana para cerrar el corpus.

La capa diacrónica queda igualmente **cerrada al 100% dentro del alcance declarado**. Las 298 relaciones Steffel ↔ Rarámuri Digital mantienen estado `candidate`, pero ahora cuentan con puntuación documental reproducible, calibración contra **5,066 emparejamientos nulos deterministas** y un informe/tablas publicables machine-only. Las pruebas prohíben que estas puntuaciones se interpreten automáticamente como equivalencia semántica, cognación, etimología, ley fonética o continuidad histórica.

## Segunda fuente: gate de industrialización cerrado

La segunda fuente piloto es **Miguel Joaquín Tellechea, 1826, _Compendio gramatical para la inteligencia del idioma tarahumar_**. Su PDF público DGB está fijado como `RHD-WIT-TELLECHEA-1826-DGB`: **205 páginas, 95,088,307 bytes, SHA-256 `c67b7942090613c494d8057be8aff59ea13a11519c29eae469afad8a85c30dfc`**.

La prueba fuerte procesa **205/205 páginas** como unidades documentales persistentes, preserva la capa textual embebida, aplica OCR visual separado en páginas escasas, valida los 205 objetos contra el mismo JSON Schema RHD y genera TEI documental completa. Resultado: **0 rediseños del núcleo universal**, **0 entradas Lex-0 fabricadas** y **0 atribuciones humanas**. La dimensión de replicación permanece cerrada al **100%**.

## IIIF: estructura canónica preparada; publicación pendiente

El PDF canónico de Steffel fue re-verificado directamente contra el binario de trabajo: **84 páginas, 6,251,443 bytes, SHA-256 `4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f`**.

Desde ese binario exacto se generaron localmente las 84 imágenes de página y se registraron dimensiones canónicas de Canvas para las 84 páginas. El repositorio contiene ahora:

- inventario de dimensiones `data/iiif/steffel-1809-canonical-canvas-dimensions.json`;
- constructor reproducible `scripts/build_steffel_iiif_images.py`, que rechaza cualquier PDF con checksum/tamaño/páginas distintos;
- generador `scripts/generate_steffel_static_iiif.py`;
- Manifest IIIF Presentation 3 preparado con **84 Canvases**;
- Canvas-map reproducible;
- mapa página/Canvas para los **1,965 registros activos**;
- prueba `tests/validate_steffel_static_iiif_preparation.py` que exige 84 Canvases, 1,965 enlaces, **0 regiones xywh inventadas** y ausencia de afirmaciones humanas.

Toda esta cadena pasó CI en el run `31894274565`. La preparación usa deliberadamente el dominio reservado `.invalid` mientras las imágenes no estén publicadas en un host estable. Por eso IIIF recibe 90%, no 100%: la estructura, las dimensiones y la vinculación están terminadas; falta sólo la **publicación pública y recuperación estable de los recursos exact-binary-derived**, con identificadores persistentes.

Los witnesses de Internet Archive y el enlace mutable de Dropbox siguen siendo controles externos, no sustitutos del witness canónico.

## Release científico: prerelease cerrado; publicación estable pendiente

`CITATION.cff`, `CHANGELOG`, política machine-only, declaración de conformidad y manifiesto determinista de integridad están preparados. La CI completa verificó el manifiesto junto con corpus lexical, anexos, calibración diacrónica y Tellechea 205/205. Esto eleva la dimensión de release a **80%**.

Lo que falta ya no es trabajo científico del corpus: es la acción editorial de publicación final —release estable y depósito/archivo con identificador persistente—.

## El 2% que permanece abierto

El residual ponderado queda concentrado exclusivamente en dos acciones de publicación:

1. **IIIF público estable — 1.0 punto:** alojar las 84 imágenes derivadas del witness exacto en un endpoint HTTP(S) persistente, regenerar el Manifest con esa base real y probar la recuperación de las 84 imágenes/Canvases. No se requieren regiones `xywh` para cerrar el nivel página; sólo se añadirán si en el futuro existen coordenadas reales.
2. **Release/archivo persistente — 1.0 punto:** publicar la versión estable, fijar el commit/tag definitivo y depositar el conjunto en un archivo persistente con identificador citable apropiado.

## Condición de 100%

Dentro del alcance machine-only, **100% no significa ausencia absoluta de ambigüedad**. Esa condición científica ya se resolvió preservando incertidumbre explícita. El 100% significa ahora que la edición ya terminada esté también **publicada de forma persistente**: facsímil canónico accesible mediante IIIF estable y release final archivado/citable. La ciencia computacional, los anexos, la calibración diacrónica y la prueba de industrialización ya no forman parte del residual.
