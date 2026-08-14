# Auditoría de procedencia de SRC-02 (`DICCIONARIO raramuri.pdf`)

**Fecha:** 2026-08-13.  
**Estatus:** procedencia bibliográfica no resuelta; hipótesis de filiación documentada y separada de la identidad del archivo.

## Problema

Rarámuri Digital declara dos fuentes distintas. `SRC-01` es K. Simón Hilton, *Diccionario tarahumara de Samachique* (1993), utilizado como facsímil de cotejo. `SRC-02` es un archivo identificado sólo como `DICCIONARIO raramuri.pdf`, del cual se estructuraron 2,581 entradas de las páginas 3–87. El propio `DATASHEET.md` señala que el cotejo sistemático contra `SRC-01` continúa pendiente.

Los metadatos internos revisados (`project-metadata.json`, `fair-dataset.jsonld`, `extraction-report.json`, `README.md` y el commit inicial del léxico maestro) no proporcionan autor, edición, URL archivística, hash del PDF fuente, portada ni colofón para `SRC-02`. Por ello **no puede identificarse bibliográficamente el archivo a partir del repositorio actual**.

## Puntos de referencia oficiales de SIL

SIL México cataloga el *Diccionario tarahumara de Samachique, Chihuahua, México* de Hilton en 1993 como una “edición especial corregida y actualizada”, con viii + 146 páginas y aproximadamente 2,500 entradas.

SIL cataloga además *Diccionario tarahumara actualizado* de Wes Shoemaker, creado en 2016, con 95 páginas y aproximadamente 2,500 entradas. La descripción institucional es especialmente relevante: se trata de una **versión actualizada del Diccionario tarahumara (VIMSA 101, 1993) con cambios ortográficos recientes** y se publica como borrador.

Esto establece documentalmente una relación editorial entre 1993 y 2016, pero no identifica automáticamente `SRC-02` con ninguna de las dos versiones.

## Comparación con el borrador de 2016 indexado en línea

Una copia indexada del borrador de 2016, identificada como `Dicccionario raramuri.pdf`, conserva el aviso de materiales inéditos de SIL y la marca “Borrador (lunes, 1 de agosto de 2016...)”. Su estructura lexicográfica coincide de manera estrecha con numerosos contenidos de SRC-02, pero la grafía presenta cambios sistemáticos.

El ejemplo inicial es diagnóstico. SRC-02 conserva una entrada `A` ‘Buscar’ con el ejemplo `Nijeni ama cahué`, además de formas como `Ábia simíbari` y pretérito `ari`. El borrador de 2016 tiene el mismo ejemplo y la misma arquitectura paradigmática, pero escribe `Nijeni ama kawé`, `ábia simíbali` y pretérito `ali`. No es sólo una coincidencia léxica: es la misma microestructura con diferencias fonográficas compatibles con una actualización ortográfica.

Otros contrastes apuntan en la misma dirección:

| concepto | SRC-02 | borrador 2016 indexado |
|---|---|---|
| arco | `Catá` | `katá` (y también `atá`) |
| aguja | `Huichá` | `wichá` |
| agua | `Ba'huí` | `baꞌwí` |
| caballo en el ejemplo inicial | `cahué` | `kawé` |

La inferencia razonable es que SRC-02 pertenece probablemente a **una capa anterior a la actualización ortográfica de 2016 dentro de la misma tradición lexicográfica**, muy posiblemente relacionada con Hilton 1993 o con un derivado pre-2016 de esa obra. Esta es una hipótesis de filiación, no una identificación de archivo.

## Estado de procedencia

Se conservan dos campos conceptualmente separados:

- **identidad del archivo:** no resuelta;
- **filiación lexicográfica:** probable tradición Hilton 1993 / pre-actualización de 2016, con confianza moderada-alta.

No debe citarse `SRC-02 = Hilton 1993` ni `SRC-02 = Shoemaker 2016` como hecho hasta localizar evidencia de nivel archivo: portada, colofón, metadatos PDF, identificador archivístico, hash o cotejo página por página.

## Consecuencia para la investigación diacrónica

La cautela afecta sobre todo a la **independencia documental**. Si una forma moderna de SRC-02 coincide exactamente con una forma que una publicación secundaria atribuye a Hilton, esa coincidencia no puede contarse automáticamente como una corroboración moderna independiente mientras la genealogía documental esté abierta.

Esto no invalida los datos internos de SRC-02. Una nota como `pp.: cochíami` sigue siendo evidencia documental real de lo que dice SRC-02. Lo que debe separarse es otra cuestión: si esa anotación constituye una fuente independiente de Hilton o una transmisión/reelaboración de la misma tradición lexicográfica.

La misma regla se aplicará al dominio de colores: las correspondencias publicadas Steffel–Hilton–Brambila continúan siendo importantes, pero los matches exactos de SRC-02 con Hilton se etiquetarán como **posiblemente dependientes** hasta resolver la procedencia.

## Próximas pruebas

La resolución fuerte requiere localizar el PDF original utilizado como SRC-02. Si aparece, deben registrarse título interno, autores, fecha, extensión, propiedades PDF y SHA-256. Después conviene cotejar una muestra diagnóstica de entradas contra Hilton 1993 y Shoemaker 2016, incluyendo ortografía, paginación, ejemplos, orden de entradas y variantes.

Mientras eso no ocurra, el estado recomendado es:

`file_identity=unresolved`; `bibliographic_identity=unresolved`; `lineage_hypothesis=likely_pre2016_Hilton_1993_tradition`; `lineage_confidence=moderate_to_high`; `documentary_independence_from_Hilton=not_established`.

`ai_assisted=true`; `official_sil_metadata_verified=true`; `repository_metadata_audited=true`; `indexed_2016_text_consulted=true`; `source_file_bytes_verified=false`; `human_reviewed_by_project=false`.
