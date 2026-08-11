<p align="center">
  <strong>Rarámuri Histórico Digital</strong><br>
  Corpus Steffel 1791/1809
</p>

<p align="center">
  <img src="https://img.shields.io/badge/dataset-0.2.0-172033?style=flat-square" alt="Dataset 0.2.0">
  <img src="https://img.shields.io/badge/fuente-Steffel%201809-7a263a?style=flat-square" alt="Steffel 1809">
  <img src="https://img.shields.io/badge/candidatos%20segmentados-2%2C495-2d6a4f?style=flat-square" alt="2,495 candidate entries">
  <img src="https://img.shields.io/badge/l%C3%ADmites%20cotejados-100-b7791f?style=flat-square" alt="100 boundaries reviewed">
  <img src="https://img.shields.io/badge/art%C3%ADculos%20diplom%C3%A1ticos%20AI--asistidos-10-455B55?style=flat-square" alt="10 AI-assisted diplomatic articles">
  <img src="https://img.shields.io/badge/c%C3%B3digo-MIT-172033?style=flat-square" alt="MIT">
</p>

## Propósito

**Rarámuri Histórico Digital** es la infraestructura histórica complementaria de [Rarámuri Digital](https://github.com/fersandovalgtz/raramuri-digital). Su objetivo es convertir fuentes lexicográficas y lingüísticas históricas en datos trazables, consultables y reutilizables sin borrar la forma documental original.

La primera colección es el **Corpus Steffel 1791/1809**, basado en el *Tarahumarisches Wörterbuch* de Matthäus Steffel. La obra contiene vocabulario alemán–tarahumara, vocabulario tarahumara–alemán, observaciones gramaticales y culturales, un apéndice sobre numeración y una muestra lingüística trilingüe.

## Estado 0.2.0: cobertura integral y revisión editorial

La segmentación de alta cobertura contiene **2,495 candidatos de artículo lexicográfico**: **1,607 alemán→rarámuri** y **888 rarámuri→alemán**. Las 60 entradas previamente curadas conservan sus identificadores persistentes originales.

El número 2,495 no se presenta como conteo filológico definitivo. La tipografía Fraktur, errores del OCR y el diseño a dos columnas producen límites candidatos que pueden dividir o unir artículos incorrectamente. Por ello el proyecto separa explícitamente cobertura automática, cotejo facsimilar, transcripción diplomática y futura validación lingüística.

El primer lote de cotejo facsimilar (`RHD-FR-001`) revisó 100 límites candidatos: 86 arranques fueron aceptados, 14 falsos límites fueron rechazados y cuatro lemas recibieron correcciones claras de OCR. La capa activa pública queda provisionalmente en 2,481 candidatos.

## Primera capa diplomática

Las páginas impresas 301–317 (PDF 11–27) ya cuentan con un modelo explícito de sus dos columnas. Sobre esa evidencia se creó `RHD-DIP-001A`, con **10 artículos cortos transcritos completamente** desde el facsímil.

Estos registros usan el estado `diplomatic_transcription_ai_assisted`. La transcripción conserva grafía y puntuación de la fuente, pero no codifica los saltos tipográficos de línea. **No se presenta como verificación humana**: `human_verified=false` y la revisión filológica independiente continúa pendiente.

La regla editorial es:

**facsímil → OCR bruto → segmentación de alta cobertura → cotejo de límites → reconstrucción por columnas → transcripción diplomática → validación humana/lingüística → normalización → datos estructurados.**

## Datos principales

- `data/entries.csv`: capa maestra integral con overlays editoriales.
- `data/entries_curated.csv`: 60 anclas iniciales con identificadores persistentes.
- `data/review/`: manifiestos de revisión de límites y lemas.
- `data/facsimile/page_layout_301_317.csv`: modelo de columnas para las primeras 17 páginas lexicográficas.
- `data/diplomatic/diplomatic_batch_001.json`: primera colección de transcripciones completas de artículo.
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

El pipeline reconstruye primero la capa automática y después aplica, de manera reproducible, los manifiestos editoriales. Las correcciones no sustituyen ni alteran el OCR fuente.

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
