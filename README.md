<p align="center">
  <strong>Rarámuri Histórico Digital</strong><br>
  Corpus Steffel 1791/1809
</p>

<p align="center">
  <img src="https://img.shields.io/badge/dataset-0.2.0-172033?style=flat-square" alt="Dataset 0.2.0">
  <img src="https://img.shields.io/badge/fuente-Steffel%201809-7a263a?style=flat-square" alt="Steffel 1809">
  <img src="https://img.shields.io/badge/candidatos%20segmentados-2%2C495-2d6a4f?style=flat-square" alt="2,495 candidate entries">
  <img src="https://img.shields.io/badge/l%C3%ADmites%20cotejados-1%2C109-b7791f?style=flat-square" alt="1,109 boundaries reviewed">
  <img src="https://img.shields.io/badge/art%C3%ADculos%20diplom%C3%A1ticos%20AI--asistidos-936-455B55?style=flat-square" alt="936 AI-assisted diplomatic articles">
  <img src="https://img.shields.io/badge/c%C3%B3digo-MIT-172033?style=flat-square" alt="MIT">
</p>

## Propósito

**Rarámuri Histórico Digital** es la infraestructura histórica complementaria de [Rarámuri Digital](https://github.com/fersandovalgtz/raramuri-digital). Su objetivo es convertir fuentes lexicográficas y lingüísticas históricas en datos trazables, consultables y reutilizables sin borrar la forma documental original.

La primera colección es el **Corpus Steffel 1791/1809**, basado en el *Tarahumarisches Wörterbuch* de Matthäus Steffel. La obra contiene vocabulario alemán–tarahumara, vocabulario tarahumara–alemán, observaciones gramaticales y culturales, un apéndice sobre numeración y una muestra lingüística trilingüe.

## Estado 0.2.0: cobertura integral y revisión editorial

La segmentación de alta cobertura contiene **2,495 candidatos de artículo lexicográfico**: **1,607 alemán→rarámuri** y **888 rarámuri→alemán**. Las 60 entradas previamente curadas conservan sus identificadores persistentes originales.

El número 2,495 no se presenta como conteo filológico definitivo. La tipografía Fraktur, errores del OCR y el diseño a dos columnas producen límites candidatos que pueden dividir o unir artículos incorrectamente. Por ello el proyecto separa explícitamente cobertura automática, cotejo facsimilar, transcripción diplomática y futura validación lingüística.

A través de `RHD-FR-001`–`RHD-FR-012` se han cotejado visualmente **1,109 límites candidatos**: **936 arranques de artículo fueron aceptados**, **173 falsos límites rechazados** y **344 lemas recibieron correcciones claras**. Los identificadores de los límites rechazados se preservan y nunca se reciclan. La capa activa queda provisionalmente en **2,322 candidatos**.

La totalidad de los **609 candidatos `high_machine`** ya fue resuelta. También se revisaron los primeros **500 de 1,110 candidatos `medium_machine`**: 383 arranques aceptados y 117 falsos límites. Restan **610 candidatos de confianza media** y posteriormente 716 candidatos `low_machine`.

## Capa diplomática

Los **936 arranques aceptados entre los 1,109 candidatos cotejados** cuentan con transcripción diplomática completa IA-asistida. La serie `RHD-DIP-001A`–`RHD-DIP-012D` conserva grafía y puntuación históricas y documenta de forma explícita las lecturas inciertas. El inventario registra actualmente **424 transcripciones con una nota de incertidumbre**.

En los artículos extensos o especialmente difíciles, la lectura del facsímil puede cotejarse adicionalmente con la edición crítica contemporánea de Merrill et al. (2020), ya documentada en `SOURCES.md`; ese cotejo funciona como evidencia secundaria y nunca sustituye al facsímil de 1809 como fuente autoritativa del proyecto.

Estos registros usan el estado `diplomatic_transcription_ai_assisted`. **No se presentan como verificación humana**: todos mantienen `human_verified=false` y la revisión filológica y lingüística independiente continúa pendiente.

La regla editorial es:

**facsímil → OCR bruto → segmentación de alta cobertura → cotejo de límites → reconstrucción por columnas → transcripción diplomática → validación humana/lingüística → normalización → datos estructurados.**

## Datos principales

- `data/entries.csv`: capa maestra integral con overlays editoriales.
- `data/entries_curated.csv`: 60 anclas iniciales con identificadores persistentes.
- `data/review/`: manifiestos append-only de revisión de límites y lemas (`RHD-FR-001`–`RHD-FR-012`).
- `data/facsimile/`: modelo explícito de columnas para las 68 páginas lexicográficas impresas 301–368.
- `data/diplomatic/`: transcripciones diplomáticas IA-asistidas de los 936 artículos aceptados hasta `RHD-FR-012`.
- `data/ocr_dictionary_lines.csv`: capa de auditoría de líneas OCR.
- `data/corpus_inventory.json`: conteos, rangos y progreso editorial.
- `data/json/entries.json`, `data/xml/entries.xml`, `data/xml/steffel-1809-tei-machine.xml` y `data/raramuri_historico.sqlite`: serializaciones derivadas.
- `data/sections/`: apéndice de numeración y muestra lingüística separados del cuerpo lexicográfico.
- `sources/steffel-1809-ocr-source.txt`: OCR primario preservado sin corrección.

## Reproducibilidad

```bash
python3 scripts/extract_full_corpus.py
python3 scripts/apply_review_overrides.py
python3 scripts/generate_exports.py
python3 tests/validate.py
```

El pipeline reconstruye primero la capa automática y después aplica, de manera reproducible, los manifiestos editoriales. Las correcciones no sustituyen ni alteran el OCR fuente. GitHub Actions ejecuta el pipeline y las pruebas de validación tras cambios en las capas editoriales y regenera las exportaciones derivadas.

## Identificadores

Las unidades usan `RHD-S1809-#####`. Los identificadores `RHD-S1809-00001` a `RHD-S1809-00060` continúan vinculados a sus 60 anclas originales. Un identificador asignado no se reutiliza aunque un límite sea posteriormente rechazado o fusionado.

## Relación con Rarámuri Digital

El corpus histórico permanece separado de la base contemporánea. Las correspondencias Steffel ↔ Rarámuri Digital se modelarán posteriormente como relaciones explícitas con estado, confianza, método y revisión; nunca como fusiones automáticas.

- Recurso contemporáneo: https://raramuri.ceees.mx
- Repositorio contemporáneo: https://github.com/fersandovalgtz/raramuri-digital

## Responsable

**Dr. Fernando Sandoval Gutierrez**  
Universidad CEEES · Universidad Autónoma de Ciudad Juárez · Cuerpo Académico UACJ-113  
ORCID: 0000-0002-3168-6725

## Licencias

Código: MIT. Las capas editoriales y datos derivados del proyecto se proponen bajo CC BY 4.0. El facsímil histórico y las reproducciones de terceros deben citarse y reutilizarse conforme a su propia procedencia. Véanse `DATA_LICENSE.md`, `SOURCES.md` y `PROVENANCE.md`.
