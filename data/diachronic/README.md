# Capa de correspondencias diacrónicas

Esta carpeta modela relaciones explícitas entre **Rarámuri Histórico Digital — Corpus Steffel 1791/1809** y **Rarámuri Digital**. La separación entre ambos corpus es deliberada: ninguna correspondencia fusiona ni reemplaza formas documentales.

## Fuente contemporánea de referencia

La primera fuente de comparación es `fersandovalgtz/raramuri-digital`, conjunto de datos 1.0.0. La entidad canónica contemporánea usa identificadores persistentes `RD-######` y conserva por separado `headword`, `headword_raw` y `headword_normalized`. Para reproducibilidad, el registro inicial queda fijado al commit `156921f4edfe27d784edc1e6444867eaa368f2e5` y al archivo `data/lexicon-master.csv`.

## Unidad de relación

Una correspondencia es una **hipótesis trazable entre dos entidades**, no una equivalencia lingüística automática. Debe conservar:

- `historical_record_id` (`RHD-S1809-#####`);
- forma histórica diplomática y página;
- `modern_record_id` (`RD-######`);
- forma contemporánea fuente y normalizada;
- tipo de relación propuesto;
- método de generación;
- evidencia y puntuación cuando exista;
- estado de revisión independiente.

## Tipos de relación candidatos

- `exact_normalized_graphic_match`: coincidencia de claves normalizadas mediante una regla documental explícita; no implica identidad semántica.
- `probable_graphic_correspondence`: semejanza gráfica suficiente para revisión, pero sin identidad exacta.
- `semantic_correspondence_candidate`: la evidencia de glosa sugiere relación y requiere juicio lingüístico.
- `historical_variant_candidate`: posible relación histórica/ortográfica que requiere análisis especializado.
- `no_supported_match`: revisión explícita sin correspondencia aceptable.
- `uncertain`: evidencia insuficiente o contradictoria.

Los tipos anteriores describen **candidatos**. Una relación sólo puede adquirir `human_reviewed=true` mediante una decisión independiente documentada.

## Política de normalización para candidatos

La normalización automática puede usarse únicamente como clave de búsqueda. La primera estrategia conservadora permite: Unicode NFC/NFKD según la operación, minúsculas, eliminación de diacríticos para una clave secundaria y conversión de `ſ` a `s`. No se deben introducir equivalencias fonológicas, morfológicas o dialectales automáticas.

Toda clave normalizada debe coexistir con la forma histórica diplomática y la forma contemporánea fuente.

## Flujo recomendado

1. Generar candidatos de coincidencia gráfica exacta entre formas rarámuri históricas y `headword_normalized` contemporáneo.
2. Mantener separadas las coincidencias múltiples por homonimia.
3. Revisar manualmente forma, sentido, contexto y fuente.
4. Registrar aceptación, modificación, rechazo o incertidumbre.
5. Sólo después construir análisis de continuidad/cambio léxico, ortográfico o semántico.

## Artefactos

- `source_registry.json`: versiones y commits fijados de los corpus comparados.
- `correspondence_schema.json`: contrato de datos de la relación diacrónica.
- `correspondence_template.json`: plantilla de adjudicación de una correspondencia.

Esta capa nunca sobrescribe `headword_diplomatic`, `article_diplomatic`, el facsímil, el historial PHIL ni los registros `RD-######` de Rarámuri Digital.
