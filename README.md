<p align="center">
  <strong>Rarámuri Histórico Digital</strong><br>
  Corpus Steffel 1791/1809
</p>

<p align="center">
  <img src="https://img.shields.io/badge/dataset-0.2.0-172033?style=flat-square" alt="Dataset 0.2.0">
  <img src="https://img.shields.io/badge/fuente-Steffel%201809-7a263a?style=flat-square" alt="Steffel 1809">
  <img src="https://img.shields.io/badge/candidatos%20segmentados-2%2C495-2d6a4f?style=flat-square" alt="2,495 candidate entries">
  <img src="https://img.shields.io/badge/anclas%20curadas-60-455B55?style=flat-square" alt="60 curated anchors">
  <img src="https://img.shields.io/badge/cobertura-rango%20lexicográfico%20completo-6A1B9A?style=flat-square" alt="Complete lexicographic span">
  <img src="https://img.shields.io/badge/cotejo%20facsimilar-en%20progreso-b7791f?style=flat-square" alt="Facsimile collation in progress">
  <img src="https://img.shields.io/badge/código-MIT-172033?style=flat-square" alt="MIT">
</p>

## Propósito

**Rarámuri Histórico Digital** es la infraestructura histórica complementaria de [Rarámuri Digital](https://github.com/fersandovalgtz/raramuri-digital). Su objetivo es convertir fuentes lexicográficas y lingüísticas históricas en datos trazables, consultables y reutilizables sin borrar la forma documental original.

La primera colección es el **Corpus Steffel 1791/1809**, basado en el *Tarahumarisches Wörterbuch* de Matthäus Steffel. La obra contiene vocabulario alemán–tarahumara, vocabulario tarahumara–alemán, observaciones gramaticales y culturales, un apéndice sobre numeración y una muestra lingüística trilingüe.

## Estado 0.2.0: cobertura integral

El repositorio **ya no está limitado a las 60 entradas semilla**. La versión 0.2.0 incorpora el rango lexicográfico completo del OCR suministrado y ejecuta una segmentación automática orientada a máxima cobertura. El resultado actual contiene **2,495 candidatos de artículo lexicográfico**: **1,607 alemán→rarámuri** y **888 rarámuri→alemán**. Las 60 entradas previamente curadas conservan sus identificadores persistentes originales y funcionan como anclas editoriales.

El número 2,495 **no se presenta como conteo filológico definitivo de entradas**. La tipografía Fraktur, errores del OCR, columnas y continuaciones de artículo producen límites candidatos que pueden dividir o unir artículos incorrectamente. Por ello cada registro mantiene `segmentation_confidence`, líneas de procedencia, página estimada y estado editorial. La política de esta etapa favorece cobertura antes que falsa precisión: es preferible conservar un candidato dudoso y revisarlo contra el facsímil que omitir silenciosamente una posible entrada.

La regla editorial continúa siendo: **facsímil → OCR bruto → segmentación de alta cobertura → transcripción diplomática → normalización → datos estructurados**. Ninguna normalización sustituye la evidencia de la fuente.

## Datos principales

- `data/entries.csv`: capa maestra integral de candidatos lexicográficos.
- `data/entries_curated.csv`: 60 anclas iniciales, conservadas para control editorial y compatibilidad de identificadores.
- `data/ocr_dictionary_lines.csv`: todas las líneas no vacías de los dos rangos lexicográficos, con dirección y página, para auditar omisiones.
- `data/corpus_inventory.json`: conteos, rangos y metodología de cobertura.
- `data/json/entries.json`, `data/xml/entries.xml`, `data/xml/steffel-1809-tei-machine.xml` y `data/raramuri_historico.sqlite`: serializaciones derivadas de la capa maestra.
- `data/sections/`: OCR separado del apéndice de numeración y de la muestra lingüística.
- `sources/steffel-1809-ocr-source.txt`: OCR primario suministrado, preservado sin corrección.

## Estados editoriales

`curated_anchor` identifica las 60 anclas ya trabajadas. Los demás límites se clasifican como `high_machine`, `medium_machine` o `low_machine` según señales tipográficas y de estructura. Todos los candidatos automáticos permanecen `machine_segmented_unverified` hasta su cotejo visual. El estado de segmentación no equivale a validación lingüística.

## Reproducibilidad

Regenerar la capa integral y sus exportaciones:

```bash
python3 scripts/extract_full_corpus.py
python3 scripts/generate_exports.py
python3 tests/validate.py
```

La extracción trabaja únicamente sobre el OCR histórico suministrado y las 60 anclas editoriales del proyecto; no incorpora como datos la traducción española de la edición crítica de 2020.

## Identificadores

Las entradas usan `RHD-S1809-#####`. Los identificadores `RHD-S1809-00001` a `RHD-S1809-00060` permanecen vinculados a las mismas 60 anclas ya publicadas. Los nuevos candidatos reciben identificadores a partir de `00061`; un identificador asignado no debe reutilizarse para otra entidad aunque un límite sea posteriormente rechazado o fusionado.

## Relación con Rarámuri Digital

Este repositorio permanece separado de la base contemporánea. Las correspondencias futuras se modelarán como relaciones explícitas con estado, confianza, método y revisión humana; nunca como fusiones automáticas.

- Recurso contemporáneo: https://raramuri.ceees.mx
- Repositorio contemporáneo: https://github.com/fersandovalgtz/raramuri-digital

## Responsable

**Dr. Fernando Sandoval Gutierrez**  
Universidad CEEES · Universidad Autónoma de Ciudad Juárez · Cuerpo Académico UACJ-113  
ORCID: 0000-0002-3168-6725

## Licencias

Código: MIT. Las capas editoriales y datos derivados del proyecto se proponen bajo CC BY 4.0. El facsímil histórico y las reproducciones de terceros deben citarse y reutilizarse conforme a su propia procedencia. Véanse `DATA_LICENSE.md`, `SOURCES.md` y `PROVENANCE.md`.
