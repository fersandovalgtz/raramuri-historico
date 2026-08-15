# Plan de publicación persistente — RHD 1.0

**Corte:** 15 de agosto de 2026  
**Estado:** IIIF público cerrado; candidato estable 1.0.0 preparado; depósito/DOI persistente pendiente.  
**Efecto en la métrica:** este gate corresponde al último 1% del alcance machine-only.

## Objetivo

Cerrar RHD 1.0 como un objeto científico no sólo reproducible en GitHub, sino **estable, citable y archivado**. Este gate no añade trabajo lingüístico ni filológico: congela y deposita el objeto ya validado.

## Estado previo al depósito

- PR #2 fusionado a `main`.
- IIIF Presentation 3 desplegado y verificado por el pipeline canónico.
- Licencia definitiva: software MIT; datos, metadatos y capas editoriales originales de RHD bajo CC BY 4.0.
- `CITATION.cff` preparado para `1.0.0`.
- `docs/RELEASE_NOTES_V1.0.0.md` preparado.
- `RELEASE_READY_V1.0.0` registra la autorización explícita del responsable.
- `.github/workflows/release-v1.0.0.yml` crea el tag y GitHub Release únicamente después de que el pipeline canónico del commit de `main` termine con éxito.

## Archivo recomendado

El destino preferente para el snapshot científico es **Zenodo**, por su integración habitual con GitHub, versionado de depósitos y asignación de DOI. Esta preferencia no constituye por sí sola un depósito ni permite inventar un DOI.

Si se usa otro archivo con identificador persistente y preservación verificable, el gate puede cerrarse con equivalencia funcional, siempre que sea público, estable y citable.

## Secuencia de cierre

1. fusionar a `main` el candidato de release 1.0.0;
2. ejecutar CI canónica completa sobre ese commit;
3. si la CI termina verde, crear automáticamente tag/release `v1.0.0` exactamente sobre el SHA validado;
4. comprobar que el GitHub Release no es draft ni prerelease;
5. depositar el snapshot de `v1.0.0` en Zenodo u otro archivo persistente;
6. obtener el DOI/identificador real;
7. verificar correspondencia entre depósito, tag/commit y manifiesto de integridad;
8. incorporar el identificador real a `CITATION.cff` y a la evidencia de publicación;
9. sólo entonces actualizar la métrica global de 99% a 100%.

## Evidencia mínima para cerrar el gate

Deben existir simultáneamente:

- tag estable `v1.0.0`;
- GitHub Release estable;
- identificador persistente real emitido por un archivo;
- URL pública del registro archivado;
- versión archivada identificable como RHD 1.0.0;
- correspondencia verificable entre snapshot, commit/tag y manifiesto RHD;
- `CITATION.cff` con el identificador real;
- ausencia de afirmaciones `human_verified` no sustentadas.

## Qué no cuenta como cierre

No basta con crear un tag sin depósito, escribir manualmente un DOI hipotético, enlazar sólo la rama mutable `main`, conservar únicamente artefactos temporales de GitHub Actions o confundir el GitHub Release con un archivo científico persistente independiente.

## Condición de 100%

RHD se mantiene en **99%** hasta que exista y se verifique el depósito persistente con identificador citable real. La publicación IIIF y el objeto científico ya están cerrados; el único residual es archivístico.
