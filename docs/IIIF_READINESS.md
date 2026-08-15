# Preparación IIIF — Corpus Steffel 1791/1809

**Estado:** arquitectura preparada; publicación IIIF canónica todavía no cerrada.  
**Corte:** 15 de agosto de 2026.

## 1. Decisión

RHD 1.0 adopta IIIF Presentation API 3.0 como objetivo para representar la relación entre el testimonio facsimilar, sus páginas y las capas de transcripción/anotación. La implementación no debe inventar Canvases ni regiones sin una fuente de imagen estable y direccionable.

La validación del witness y de sus correspondencias puede realizarse íntegramente mediante procedimientos computacionales/IA dentro del alcance machine-only. No se requiere intervención humana, pero sí evidencia recuperable, mapeos reproducibles y estados de identidad/incertidumbre explícitos.

## 2. Witness canónico de trabajo

El directorio `sources/` conserva OCR, checksums y documentación de procedencia, pero el facsímil binario no forma parte del repositorio Git. El witness canónico del proyecto queda fijado por SHA-256 en `sources/checksums.json` y registrado en `sources/external-references.json`.

El PDF de trabajo tiene 84 páginas. Su tramo final fue cotejado visualmente por IA: **PDF 79–84 corresponde a las páginas impresas 369–374**. Este mapeo cubre el apéndice numérico, las 22 fórmulas de la *Tarahumarische Sprachprobe* y el Padre Nuestro, y se conserva en `data/appendices/facsimile_page_map.json`.

La inspección de las primeras páginas del PDF identifica la obra y a Matthäus Steffel, pero no expone en esas páginas una marca institucional suficientemente clara para resolver el repositorio de origen del binario. Ese dato permanece abierto en vez de inferirse.

## 3. Internet Archive: referencia paralela, no witness canónico

Se registró el ítem de Internet Archive **`tarahumarischesw00stef`** como reproducción externa paralela. Su Manifest es recuperable como IIIF Presentation 3 y contiene 90 Canvases. Sin embargo, los Canvases están etiquetados por número de escaneo y no por paginación impresa.

RHD probó de manera automatizada si ese ítem podía sustituir al facsímil canónico. Para ello se calcularon huellas perceptuales dHash de las seis páginas locales ya identificadas como 369–374 y se compararon contra ventanas consecutivas de las páginas finales del Manifest externo. El mejor resultado observado produjo distancias de Hamming **117, 100, 119, 130, 113 y 104**, con media **113.83/256**. Es una divergencia demasiado grande para declarar identidad de escaneo mediante este método.

Por tanto, el ítem se clasifica como **`parallel_external_witness_candidate` / `canonical_for_rhd=false`**. No se afirma necesariamente que sea otra edición; se afirma únicamente lo que la prueba permite: **no está verificado como el mismo escaneo que el facsímil de trabajo y no puede sustituirlo silenciosamente**.

La CI conserva esta diferencia como un control negativo: verifica que el Manifest externo siga siendo IIIF 3 y que la evidencia de imagen continúe apoyando su condición no canónica. Si en el futuro la reproducción cambia o aparece evidencia fuerte de identidad, la prueba fallará y obligará a reconsiderar explícitamente el registro de witnesses.

## 4. Mapeo RHD → IIIF previsto

| RHD | IIIF Presentation 3.0 | Regla |
|---|---|---|
| Witness Steffel canónico | `Manifest` | Debe representar el facsímil checksum-fixed, no sólo una reproducción compatible por título. |
| Página digital | `Canvas` | Un Canvas por vista/página digital, con URI HTTP(S) persistente. |
| Imagen de página | `Annotation` con `motivation=painting` | Sólo cuando exista recurso de imagen HTTP(S) estable. |
| Región de entrada | target `Canvas#xywh=...` o selector equivalente | Sólo cuando haya coordenadas reales de segmentación. |
| Transcripción diplomática | Annotation no-painting / capa RHD enlazada | Debe quedar separada de la imagen y conservar responsabilidad/estatus. |
| Traducción/comentario | Annotation diferenciada | No se confunde con la fuente histórica. |
| Reproducción externa no idéntica | witness paralelo | Puede documentarse/compararse, pero no recibe los localizadores canónicos de las entradas RHD. |

## 5. Campos ya reservados en el modelo canónico

`schemas/rhd-entry-1.0.schema.json` ya contempla:

- `locators.iiif_canvas`;
- `locators.iiif_target`;
- `locators.region` con `x`, `y`, `width`, `height` y unidad.

Estos campos deben permanecer `null` mientras no exista evidencia espacial verificable sobre el witness canónico.

## 6. Requisitos para cerrar IIIF canónico

1. Localizar un servicio/Manifest que represente reproduciblemente el mismo escaneo checksum-fixed del PDF de trabajo, o publicar ese facsímil mediante un servicio IIIF controlado por el proyecto.
2. Determinar dimensiones y orden de las 84 páginas digitales.
3. Crear mapeo reproducible `pdf_page ↔ Canvas` y `printed_page ↔ Canvas` para el witness completo.
4. Generar/usar Annotation Pages de `painting` para las imágenes.
5. Incorporar coordenadas de región sólo cuando provengan de segmentación real y verificable.
6. Validar el Manifest contra Presentation API 3.0 y probar sus recursos de imagen.
7. Persistir los identificadores de Canvas entre releases.

## 7. Automatización ya disponible

- registro machine-readable de witnesses canónicos y paralelos;
- verificación automática de existencia y estructura del Manifest externo;
- huellas perceptuales del witness local para pruebas de identidad entre reproducciones;
- control negativo que impide sustituir por error el ítem de Internet Archive;
- mapeo local PDF 79–84 ↔ impreso 369–374;
- campos IIIF reservados en el modelo RHD;
- política que prohíbe publicar `iiif_canvas`/`iiif_target` sin evidencia real.

## 8. Criterio de cierre

La dimensión IIIF no se marcará como completa por tener un JSON sintácticamente correcto ni por localizar otra copia digital de la misma obra. Se cerrará cuando exista una representación navegable del **witness canónico de trabajo**, con Canvases persistentes, imágenes recuperables y vínculos reproducibles desde las entradas RHD hacia las páginas o regiones que constituyen su evidencia documental. No se exige validación humana; sí identidad de witness, consistencia automatizada y trazabilidad completa.
