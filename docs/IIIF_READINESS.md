# Preparación IIIF — Corpus Steffel 1791/1809

**Estado:** arquitectura preparada; publicación IIIF no cerrada.  
**Corte:** 15 de agosto de 2026.

## 1. Decisión

RHD 1.0 adopta IIIF Presentation API 3.0 como objetivo para representar la relación entre el testimonio facsimilar, sus páginas y las capas de transcripción/anotación. La implementación no debe inventar Canvases ni regiones sin una fuente de imagen estable y direccionable.

## 2. Estado actual del repositorio

El directorio `sources/` conserva el OCR, checksums y documentación de procedencia, pero el facsímil binario/servicio de imágenes no forma parte del repositorio Git. Por tanto, el proyecto puede definir el **modelo lógico IIIF**, pero no publicar honestamente un Manifest plenamente funcional con imágenes y dimensiones verificables hasta fijar el servicio de imagen o URI estable del facsímil.

## 3. Mapeo RHD → IIIF previsto

| RHD | IIIF Presentation 3.0 | Regla |
|---|---|---|
| Witness Steffel | `Manifest` | Un manifiesto describe el testimonio de trabajo. |
| Página digital | `Canvas` | Un Canvas por vista/página digital, con URI HTTP(S) persistente. |
| Imagen de página | `Annotation` con `motivation=painting` | Sólo cuando exista recurso de imagen HTTP(S) estable. |
| Región de entrada | target `Canvas#xywh=...` o selector equivalente | Sólo cuando haya coordenadas reales de segmentación. |
| Transcripción diplomática | Annotation no-painting / capa RHD enlazada | Debe quedar separada de la imagen y conservar responsabilidad/estatus. |
| Traducción/comentario | Annotation diferenciada | No se confunde con la fuente histórica. |

## 4. Campos ya reservados en el modelo canónico

`schemas/rhd-entry-1.0.schema.json` ya contempla:

- `locators.iiif_canvas`;
- `locators.iiif_target`;
- `locators.region` con `x`, `y`, `width`, `height` y unidad.

Estos campos deben permanecer `null` mientras no exista evidencia espacial verificable.

## 5. Requisitos para desbloquear IIIF completo

1. Fijar una URI estable del facsímil o un servicio de imágenes controlado por el proyecto/institución.
2. Determinar dimensiones de cada página digital.
3. Crear mapeo reproducible `pdf_page ↔ Canvas`.
4. Generar Annotation Pages de `painting` para las imágenes.
5. Incorporar coordenadas de región sólo cuando provengan de segmentación real y verificable.
6. Validar el Manifest contra Presentation API 3.0 y probarlo en al menos un visor IIIF.
7. Persistir los identificadores de Canvas; no regenerarlos de manera incompatible entre releases.

## 6. Lo que sí puede automatizarse antes del hosting

- generador de identificadores deterministas de Canvas;
- tabla de correspondencia entre página impresa y página digital;
- esquema de Annotation Page;
- pruebas que prohíban publicar `iiif_canvas`/`iiif_target` sin URI HTTP(S) real;
- documentación de cómo una segunda fuente debe declarar su estrategia facsimilar.

## 7. Criterio de cierre

La dimensión IIIF no se marcará como completa por tener un JSON sintácticamente correcto. Se cerrará cuando exista una representación navegable del facsímil real, con Canvases persistentes, imágenes recuperables y vínculos reproducibles desde las entradas RHD hacia las páginas o regiones que constituyen su evidencia documental.
