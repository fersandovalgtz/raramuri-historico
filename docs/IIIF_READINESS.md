# Preparación IIIF — Corpus Steffel 1791/1809

**Estado:** estructura canónica y candidato de publicación GitHub Pages preparados y validados; publicación HTTP(S) estable todavía abierta.  
**Corte:** 15 de agosto de 2026.

## 1. Decisión

RHD 1.0 adopta IIIF Presentation API 3.0 para representar la relación entre el testimonio facsimilar, sus páginas y las capas de transcripción/anotación. La implementación machine-only no requiere intervención humana, pero exige identidad de witness, procedencia reproducible y prohibición explícita de inventar regiones espaciales.

## 2. Witness canónico exacto

El PDF canónico fue re-verificado directamente antes de preparar IIIF:

- **84 páginas**;
- **6,251,443 bytes**;
- SHA-256 **`4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f`**.

El binario continúa fuera de Git; `sources/checksums.json` y `sources/external-references.json` fijan su identidad. El tramo final conserva el mapeo reproducible **PDF 79–84 ↔ impreso 369–374**.

## 3. Preparación IIIF exact-binary-derived

Desde el PDF exacto se generaron localmente 84 imágenes derivadas a 120 dpi y se comprobaron sus dimensiones. El repositorio conserva lo necesario para reproducir y auditar esa derivación sin almacenar el facsímil binario:

- `data/iiif/steffel-1809-all84-page-fingerprints.json`: huellas de las 84 páginas;
- `data/iiif/steffel-1809-canonical-canvas-dimensions.json`: dimensiones de los 84 Canvases medidas desde el witness exacto;
- `scripts/build_steffel_iiif_images.py`: constructor que **rechaza** cualquier PDF cuyo checksum, tamaño o número de páginas no coincida con el witness canónico;
- `scripts/generate_steffel_static_iiif.py`: generador determinista de Presentation 3 de preparación;
- `tests/validate_steffel_static_iiif_preparation.py`: prueba de estructura, identidad y no-afirmaciones.

La CI genera y valida:

- **1 Manifest Presentation 3 preparado**;
- **84 Canvases**;
- 84 Annotation Pages de `painting` y sus cuerpos de imagen declarados;
- `canvas-map.json` con orden y dimensiones de las 84 páginas;
- **1,965 enlaces registro activo → Canvas**;
- **0 targets `xywh` inventados**;
- **0 atribuciones de validación humana**.

## 4. Perfil de publicación GitHub Pages

El repositorio ya dispone de GitHub Pages en `https://fersandovalgtz.github.io/raramuri-historico/`, desplegado desde `public/` en `main`.

Para la publicación del facsímil se preparó un perfil web ligero separado del perfil JPEG120 interno:

- `data/iiif/steffel-1809-published-png72-assets.json`: inventario de **84 PNG** derivados del witness exacto, con SHA-256, bytes, ancho y alto por página;
- `scripts/generate_steffel_public_iiif_candidate.py`: genera el candidato Presentation 3 con base pública real y 84 cuerpos `image/png`;
- `tests/validate_steffel_public_iiif_candidate.py`: valida **84/84 Canvases**, integridad del inventario y **1,965/1,965 enlaces registro → Canvas**;
- `scripts/verify_published_steffel_iiif.py`: gate de red que recupera Manifest + las 84 imágenes y recalcula sus hashes, tamaños y dimensiones.

La base pública final reservada es:

`https://fersandovalgtz.github.io/raramuri-historico/iiif/steffel-1809`

El run **`31895612447`** pasó todos los gates deterministas, incluidos candidato PNG72, 84 Canvases, 1,965 enlaces, Lex-0, anexos, diacronía, Tellechea 205/205 y manifiesto de release.

El verificador de red del mismo run recibió **HTTP 404** en la URL final. Ese resultado mantiene correctamente abierto el gate: el candidato offline existe, pero los 84 recursos todavía no están desplegados en Pages.

## 5. Por qué la preparación interna usa `.invalid`

Mientras las imágenes no estén publicadas, el generador estructural interno usa por defecto `https://rhd.invalid/iiif/steffel-1809`. `.invalid` es deliberado: permite probar IDs absolutos, estructura, Canvas-map y vinculación RHD sin presentar como pública una URL inexistente.

El candidato GitHub Pages usa la URL pública final, pero mantiene `public_image_host_verified=false` hasta que `verify_published_steffel_iiif.py` confirme recuperación e integridad 84/84.

## 6. Mapeo RHD → IIIF ya resuelto

| RHD | IIIF Presentation 3.0 | Estado |
|---|---|---|
| Witness Steffel canónico | `Manifest` | candidato público preparado; hosting pendiente |
| Página digital | `Canvas` | **84/84 preparado** |
| Imagen de página | Annotation `painting` | **84/84 inventariada por hash**; endpoint aún 404 |
| Registro lexical activo | `iiif_canvas` a nivel página | **1,965/1,965 preparado** |
| Región de entrada | `Canvas#xywh=...` | **no generada**; no existen coordenadas suficientes |
| Transcripción diplomática | capa RHD separada | resuelta fuera de `painting` |
| Reproducción externa no idéntica | witness paralelo | permanece no canónica |

El cierre RHD 1.0 **no requiere regiones `xywh`** para el nivel de página. Las regiones se incorporarán sólo si posteriormente existe segmentación espacial real y verificable.

## 7. Witnesses externos

Internet Archive `tarahumarischesw00stef` continúa como witness paralelo no canónico: la comparación live del run `31895612447` encontró nuevamente divergencia perceptual fuerte (mejor ventana externa 70–75; media dHash 121.50/256). El ejemplar Getty/Internet Archive sigue siendo únicamente un control/candidato externo y su probe tiene timeout no bloqueante.

El URL de Dropbox asociado al Repositorio de Lenguas es mutable y en el mismo run volvió a entregar el PDF divergente de 438 páginas, 26,702,093 bytes y SHA-256 `3c2169d818770fecff7eca822c7dcc52f35d66356c5279913d85fb5364c652ce`. Ninguno de esos proveedores puede sustituir silenciosamente el witness checksum-fixed.

## 8. Lo único que falta para cerrar IIIF

La parte estructural, de identidad, inventario y vinculación está terminada. El gate residual es exclusivamente de publicación:

1. reconstruir o materializar las 84 imágenes PNG72 desde el witness exacto y comprobarlas contra `steffel-1809-published-png72-assets.json`;
2. alojarlas en `public/iiif/steffel-1809/pages/` mediante GitHub Pages;
3. publicar `manifest.json` y `canvas-map.json` con la base final;
4. ejecutar `scripts/verify_published_steffel_iiif.py` y obtener 84/84 hashes, tamaños y dimensiones correctos;
5. congelar esos identificadores para el release final.

El procedimiento operativo completo está documentado en `docs/IIIF_PUBLICATION_GITHUB_PAGES.md`.

## 9. Criterio de cierre

IIIF pasará de 90% a 100% cuando el paquete ya preparado sea **públicamente recuperable y persistente** y el verificador de red confirme 84/84 recursos exactos. No se requiere una nueva fase científica ni revisión humana: el trabajo pendiente es hosting/identificación persistente del facsímil derivado exacto.
