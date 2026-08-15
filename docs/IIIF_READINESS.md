# Preparación IIIF — Corpus Steffel 1791/1809

**Estado:** estructura canónica IIIF preparada y validada; publicación HTTP(S) estable todavía abierta.  
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
- `scripts/generate_steffel_static_iiif.py`: generador determinista de Presentation 3;
- `tests/validate_steffel_static_iiif_preparation.py`: prueba de estructura, identidad y no-afirmaciones.

La CI genera y valida:

- **1 Manifest Presentation 3 preparado**;
- **84 Canvases**;
- 84 Annotation Pages de `painting` y sus cuerpos de imagen declarados;
- `canvas-map.json` con orden y dimensiones de las 84 páginas;
- **1,965 enlaces registro activo → Canvas**;
- **0 targets `xywh` inventados**;
- **0 atribuciones de validación humana**.

El run `31894274565` pasó todos esos gates junto con TEI/Lex-0, anexos, diacronía, Tellechea y manifiesto de release.

## 4. Por qué el Manifest preparado usa `.invalid`

Mientras las 84 imágenes no estén publicadas en un endpoint estable, el generador usa por defecto `https://rhd.invalid/iiif/steffel-1809`. `.invalid` es deliberado: permite probar IDs absolutos, estructura, Canvas-map y vinculación RHD sin presentar como pública una URL inexistente.

Cuando exista alojamiento estable, el mismo generador se ejecutará con `--base-url https://<host-estable>/...`. Sólo entonces podrá promoverse la preparación a IIIF canónico publicado.

## 5. Mapeo RHD → IIIF ya resuelto

| RHD | IIIF Presentation 3.0 | Estado |
|---|---|---|
| Witness Steffel canónico | `Manifest` | estructura preparada; hosting pendiente |
| Página digital | `Canvas` | **84/84 preparado** |
| Imagen de página | Annotation `painting` | estructura preparada; recurso HTTP pendiente |
| Registro lexical activo | `iiif_canvas` a nivel página | **1,965/1,965 preparado** |
| Región de entrada | `Canvas#xywh=...` | **no generada**; no existen coordenadas suficientes |
| Transcripción diplomática | capa RHD separada | resuelta fuera de `painting` |
| Reproducción externa no idéntica | witness paralelo | permanece no canónica |

El cierre RHD 1.0 **no requiere regiones `xywh`** para el nivel de página. Las regiones se incorporarán sólo si posteriormente existe segmentación espacial real y verificable.

## 6. Witnesses externos

Internet Archive `tarahumarischesw00stef` continúa como witness paralelo no canónico: su comparación perceptual con el witness de trabajo mostró fuerte divergencia. El ejemplar Getty/Internet Archive sigue siendo únicamente un control/candidato externo.

El URL de Dropbox asociado al Repositorio de Lenguas es mutable y ya devolvió binarios distintos. Ninguno de esos proveedores puede sustituir silenciosamente el witness checksum-fixed.

## 7. Lo único que falta para cerrar IIIF

La parte estructural y de vinculación ya está terminada. El gate residual es exclusivamente de publicación:

1. alojar las 84 imágenes derivadas del witness exacto en un endpoint HTTP(S) persistente;
2. regenerar el Manifest con la base pública real;
3. probar automáticamente que Manifest + 84 imágenes son recuperables y coherentes con las dimensiones/inventario canónicos;
4. congelar esos identificadores para el release final.

## 8. Criterio de cierre

IIIF pasará de 90% a 100% cuando el paquete ya preparado sea **públicamente recuperable y persistente**. No se requiere una nueva fase científica ni revisión humana: el trabajo pendiente es hosting/identificación persistente del facsímil derivado exacto.
