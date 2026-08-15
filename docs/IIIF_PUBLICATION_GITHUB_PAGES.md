# Runbook de publicación IIIF canónica — GitHub Pages

**Corte:** 15 de agosto de 2026  
**Estado:** paquete de publicación validado offline; endpoint público todavía no desplegado.  
**Gate RHD:** IIIF 90% → 100% sólo después de verificación HTTP(S) 84/84.

## Infraestructura pública elegida

El repositorio `fersandovalgtz/raramuri-historico` ya tiene GitHub Pages habilitado y publica el directorio `public/` desde `main` mediante `.github/workflows/pages.yml`.

Base pública reservada para el witness Steffel:

`https://fersandovalgtz.github.io/raramuri-historico/iiif/steffel-1809`

Esta ruta reutiliza la infraestructura pública ya existente del proyecto y no depende de Dropbox, Internet Archive, Getty ni otro proveedor externo mutable.

## Identidad canónica que debe preservarse

Toda publicación se deriva exclusivamente del PDF Steffel fijado como:

- 84 páginas;
- 6,251,443 bytes;
- SHA-256 `4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f`.

`scripts/build_steffel_iiif_images.py` debe rechazar cualquier PDF que no coincida con esas tres invariantes. Ningún witness externo puede sustituirlo por coincidencia de título, edición o apariencia.

## Perfil de distribución

Para publicación web se adopta un perfil ligero y explícitamente separado de la preparación interna JPEG120:

- inventario: `data/iiif/steffel-1809-published-png72-assets.json`;
- formato: PNG binarizado;
- resolución de presentación: 72 dpi;
- 84 archivos `001.png` … `084.png`;
- hash SHA-256, bytes, ancho y alto versionados por cada página.

El perfil PNG72 no cambia la identidad del witness: es una derivación de distribución del mismo PDF checksum-fixed.

## Generadores y pruebas

La publicación tiene cuatro controles separados:

1. `scripts/generate_steffel_static_iiif.py` + `tests/validate_steffel_static_iiif_preparation.py`: preparación estructural interna con `.invalid`, 84 Canvases y 1,965 enlaces página/Canvas.
2. `scripts/generate_steffel_public_iiif_candidate.py` + `tests/validate_steffel_public_iiif_candidate.py`: candidato GitHub Pages con URLs públicas PNG72, pero sin afirmar que la red ya las sirve.
3. `data/iiif/steffel-1809-published-png72-assets.json`: autoridad de integridad de los 84 recursos derivados de publicación.
4. `scripts/verify_published_steffel_iiif.py`: gate de red; recupera Manifest y las 84 imágenes, recalcula SHA-256, bytes y dimensiones, y rechaza regiones `xywh` o afirmaciones humanas no sustentadas.

## Evidencia CI vigente

El run de GitHub Actions `31895612447` validó correctamente:

- Tellechea 205/205;
- 24 anexos y 43 incertidumbres terminales;
- 298 candidatos diacrónicos contra 5,066 controles nulos;
- TEI RHD y Lex-0 0.9.5;
- preparación IIIF 84/84;
- candidato GitHub Pages PNG72 84/84;
- 1,965/1,965 enlaces registro activo → Canvas;
- manifiesto de prerelease íntegro.

El mismo run ejecutó el verificador de red contra la URL final y recibió **HTTP 404**. Ese resultado es correcto mientras los archivos todavía no se hayan desplegado: confirma que el sistema no confunde un candidato offline con una publicación existente.

## Procedimiento de despliegue

Cuando se autorice el paso de publicación:

1. partir del PDF canónico exacto y reconstruir las 84 imágenes de distribución;
2. comprobar cada archivo contra `steffel-1809-published-png72-assets.json`;
3. colocar los PNG en `public/iiif/steffel-1809/pages/001.png` … `084.png`;
4. generar el paquete público con base `https://fersandovalgtz.github.io/raramuri-historico/iiif/steffel-1809`;
5. colocar `manifest.json` y `canvas-map.json` en `public/iiif/steffel-1809/`;
6. desplegar `public/` mediante el workflow Pages ya existente;
7. ejecutar `python3 scripts/verify_published_steffel_iiif.py`;
8. cerrar el gate únicamente si el verificador confirma 84 Canvases, 84 imágenes recuperables, 84 hashes correctos, 0 regiones inventadas y 0 afirmaciones de validación humana.

## Qué no debe hacerse

No se debe publicar un Manifest que apunte a `.invalid`, declarar el gate cerrado sólo porque el JSON sea sintácticamente válido, sustituir el witness por un ítem de Internet Archive/Dropbox/Getty no idéntico, inventar coordenadas `xywh`, ni presentar el procesamiento IA-asistido como validación humana.

## Efecto en la métrica de terminación

La métrica oficial permanece en **98.0% / 2.0%** mientras el endpoint público continúe sin desplegar y no exista todavía el release/archivo persistente.

Una verificación pública 84/84 cerrará el punto residual de IIIF y elevará la terminación a **99.0%**. El último punto corresponderá entonces exclusivamente a publicar RHD 1.0 estable y depositarlo en un archivo persistente con identificador citable y correspondencia comprobada contra el manifiesto de integridad.
