<p align="center">
  <strong>Rarámuri Histórico Digital</strong><br>
  Corpus Steffel 1791/1809
</p>

<p align="center">
  <img src="https://img.shields.io/badge/dataset-0.2.0-172033?style=flat-square" alt="Dataset 0.2.0">
  <img src="https://img.shields.io/badge/fuente-Steffel%201809-7a263a?style=flat-square" alt="Steffel 1809">
  <img src="https://img.shields.io/badge/candidatos%20segmentados-2%2C495-2d6a4f?style=flat-square" alt="2,495 candidate entries">
  <img src="https://img.shields.io/badge/cotejados%20con%20facsímil-100-0f766e?style=flat-square" alt="100 facsimile-reviewed candidates">
  <img src="https://img.shields.io/badge/falsos%20positivos%20detectados-14-9b2c2c?style=flat-square" alt="14 rejected false positives">
  <img src="https://img.shields.io/badge/código-MIT-172033?style=flat-square" alt="MIT">
</p>

## Propósito

**Rarámuri Histórico Digital** es la infraestructura histórica complementaria de [Rarámuri Digital](https://github.com/fersandovalgtz/raramuri-digital). Su objetivo es convertir fuentes lexicográficas y lingüísticas históricas en datos trazables, consultables y reutilizables sin borrar la forma documental original.

La primera colección es el **Corpus Steffel 1791/1809**, basado en el *Tarahumarisches Wörterbuch* de Matthäus Steffel. La obra contiene vocabulario alemán–tarahumara, vocabulario tarahumara–alemán, observaciones gramaticales y culturales, un apéndice sobre numeración y una muestra lingüística trilingüe.

**Sitio público:** https://fersandovalgtz.github.io/raramuri-historico/

## Estado 0.2.0: cobertura integral + cotejo facsimilar iniciado

La capa automática contiene **2,495 candidatos de artículo lexicográfico**: **1,607 alemán→rarámuri** y **888 rarámuri→alemán**. Las 60 entradas previamente curadas conservan sus identificadores persistentes originales.

El primer lote de cotejo facsimilar (`RHD-FR-001`) revisó visualmente **100 candidatos de confianza automática alta**. Se aceptaron **86 arranques de artículo**, se rechazaron **14 falsos límites** y se corrigieron **4 lemas** por errores inequívocos de OCR: `Allmächtig`, `Eingraben`, `Faſttag` y `Fledermaus`. Los candidatos rechazados conservan su `record_id` y pasan a `rejected_false_positive`; los aceptados quedan como `facsimile_checked_headword_ai_assisted`.

Este cotejo es explícitamente **asistido por IA y limitado al lema y al inicio del artículo**. No equivale a transcripción diplomática completa ni a validación lingüística.

El número 2,495 no se presenta como conteo filológico definitivo. El primer lote confirmó además un problema estructural importante: el OCR suministrado no siempre conserva el orden de lectura de las páginas a dos columnas, por lo que un lema auténtico puede arrastrar texto perteneciente a otro artículo. Las fases siguientes deben reconstruir los cuerpos de artículo desde la evidencia de página.

La regla editorial es: **facsímil → OCR bruto → segmentación de alta cobertura → cotejo de límites → transcripción diplomática → normalización → datos estructurados**.

## Datos principales

- `data/entries.csv`: capa maestra integral, incluidos candidatos rechazados con estado explícito.
- `data/review/facsimile_review_batch_001.json`: evidencia editorial del primer lote de 100 cotejos.
- `FACSIMILE_REVIEW_STATUS.md`: resultados y alcance metodológico del cotejo.
- `data/entries_curated.csv`: 60 anclas iniciales.
- `data/ocr_dictionary_lines.csv`: capa de auditoría de líneas OCR.
- `data/corpus_inventory.json`: inventario, conteos y progreso de revisión.
- `data/json/entries.json`, `data/xml/entries.xml`, `data/xml/steffel-1809-tei-machine.xml` y `data/raramuri_historico.sqlite`: serializaciones derivadas.
- `data/sections/`: apéndice de numeración y muestra lingüística separados.
- `sources/steffel-1809-ocr-source.txt`: OCR primario preservado sin corrección.

## Reproducibilidad

```bash
python3 scripts/extract_full_corpus.py
python3 scripts/apply_review_overrides.py
python3 scripts/generate_exports.py
python3 tests/validate.py
```

Las revisiones facsimilares son capas de sobreescritura editorial reproducibles: nunca modifican el OCR fuente. Los identificadores asignados no se reciclan aunque un candidato sea posteriormente rechazado.

## Relación con Rarámuri Digital

Este repositorio permanece separado de la base contemporánea. Las correspondencias futuras Steffel ↔ Rarámuri Digital se modelarán como relaciones explícitas con estado, confianza, método y revisión humana; nunca como fusiones automáticas.

- Recurso contemporáneo: https://raramuri.ceees.mx
- Repositorio contemporáneo: https://github.com/fersandovalgtz/raramuri-digital

## Responsable

**Dr. Fernando Sandoval Gutierrez**  
Universidad CEEES · Universidad Autónoma de Ciudad Juárez · Cuerpo Académico UACJ-113  
ORCID: 0000-0002-3168-6725

## Licencias

Código: MIT. Las capas editoriales y datos derivados del proyecto se proponen bajo CC BY 4.0. El facsímil histórico y las reproducciones de terceros deben citarse y reutilizarse conforme a su propia procedencia. Véanse `DATA_LICENSE.md`, `SOURCES.md` y `PROVENANCE.md`.
