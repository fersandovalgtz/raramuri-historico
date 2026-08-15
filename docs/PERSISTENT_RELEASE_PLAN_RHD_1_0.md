# Plan de publicación persistente — RHD 1.0

**Corte:** 15 de agosto de 2026  
**Estado:** preparación de prerelease; no existe todavía un depósito/DOI RHD 1.0 confirmado.  
**Efecto en la métrica:** este gate corresponde al último 1% del alcance machine-only.

## Objetivo

Cerrar RHD 1.0 como un objeto científico no sólo reproducible en GitHub, sino **estable, citable y archivado**. Este gate no añade trabajo lingüístico ni filológico: congela y deposita el objeto ya validado.

## Metadatos ya disponibles

`CITATION.cff` contiene los metadatos base del depósito:

- título: **Rarámuri Histórico Digital — Corpus Steffel 1791/1809**;
- tipo: dataset;
- autor: Fernando Sandoval Gutierrez;
- ORCID: `0000-0002-3168-6725`;
- repositorio: `fersandovalgtz/raramuri-historico`;
- versión actual: `0.9.0-machine-only-prerelease`;
- alcance declarado: edición histórico-digital machine-only con incertidumbre explícita y sin afirmación de validación humana.

`DATA_LICENSE.md` propone **CC BY 4.0** para anotaciones originales, traducciones editoriales y estructuras de datos de RHD, preservando por separado las condiciones jurídicas/procedencia del facsímil histórico. La licencia definitiva del depósito debe respetar esa separación y no atribuir al proyecto derechos exclusivos sobre Steffel 1809.

## Archivo recomendado

El destino preferente para el snapshot científico es **Zenodo**, por su integración habitual con GitHub, versionado de depósitos y asignación de DOI. Esta recomendación no implica que el repositorio ya esté conectado ni que exista un DOI: no se encontró configuración de depósito en el árbol actual y no se inventará un identificador.

Si por razones institucionales se usa otro archivo que asigne identificador persistente y preserve el snapshot, el gate puede cerrarse con equivalencia funcional, siempre que sea público, estable, citable y verificable.

## Secuencia de cierre

1. cerrar primero el gate IIIF público o decidir explícitamente que el release final congela el estado IIIF publicado correspondiente;
2. ejecutar CI completa sobre el commit candidato final;
3. exigir resultado verde de corpus, Tellechea 205/205, anexos, diacronía, TEI/Lex-0, IIIF y manifiesto de integridad;
4. actualizar `CITATION.cff` de `0.9.0-machine-only-prerelease` a `1.0.0` y fijar la fecha efectiva de publicación;
5. actualizar `CHANGELOG.md` con una sección `1.0.0` que describa únicamente productos/gates realmente cerrados;
6. generar nuevamente `dist/rhd-steffel-release-manifest.json` sobre el commit final;
7. crear tag anotado `v1.0.0` apuntando exactamente a ese commit;
8. publicar GitHub Release `RHD 1.0` desde el mismo tag;
9. depositar el snapshot del tag/release y sus metadatos en el archivo persistente;
10. obtener el DOI/identificador emitido por el archivo;
11. incorporar ese identificador a `CITATION.cff` y a la documentación de release sin alterar los datos científicos del snapshot;
12. verificar que la copia archivada corresponda al tag y al manifiesto de integridad; registrar la evidencia de esa comprobación.

## Evidencia mínima para cerrar el gate

El gate de archivo/citabilidad sólo se considera cerrado cuando existan simultáneamente:

- tag final estable;
- GitHub Release estable;
- identificador persistente real emitido por un archivo;
- URL pública del registro archivado;
- versión archivada identificable como RHD 1.0;
- correspondencia verificable entre el snapshot archivado y el commit/tag/manifiesto RHD;
- `CITATION.cff` final que contenga el identificador real;
- ausencia de afirmaciones `human_verified` no sustentadas.

## Qué no cuenta como cierre

No basta con crear un tag sin depósito, escribir manualmente un DOI hipotético, enlazar la rama mutable `main`, conservar sólo artefactos temporales de GitHub Actions, o declarar un release estable antes de que la CI del commit final esté verde.

## Condición de 100%

Cuando IIIF público esté verificado, RHD quedará en **99%**. El proyecto llegará a **100%** únicamente después de completar el procedimiento anterior y registrar un identificador persistente real para el snapshot RHD 1.0. Hasta entonces la versión correcta sigue siendo prerelease y el PR #2 debe permanecer sin fusionar salvo decisión explícita del responsable del proyecto.
