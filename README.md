<p align="center">
  <strong>Rarámuri Histórico Digital</strong><br>
  Corpus Steffel 1791/1809
</p>

<p align="center">
  <img src="https://img.shields.io/badge/dataset-0.2.0-172033?style=flat-square" alt="Dataset 0.2.0">
  <img src="https://img.shields.io/badge/fuente-Steffel%201809-7a263a?style=flat-square" alt="Steffel 1809">
  <img src="https://img.shields.io/badge/candidatos%20segmentados-2%2C495-2d6a4f?style=flat-square" alt="2,495 candidate entries">
  <img src="https://img.shields.io/badge/l%C3%ADmites%20revisados-2%2C019-b7791f?style=flat-square" alt="2,019 boundaries reviewed">
  <img src="https://img.shields.io/badge/art%C3%ADculos%20diplom%C3%A1ticos%20AI--asistidos-1%2C611-455B55?style=flat-square" alt="1,611 AI-assisted diplomatic articles">
  <img src="https://img.shields.io/badge/c%C3%B3digo-MIT-172033?style=flat-square" alt="MIT">
</p>

## Propósito

**Rarámuri Histórico Digital** es la infraestructura histórica complementaria de [Rarámuri Digital](https://github.com/fersandovalgtz/raramuri-digital). Convierte fuentes lexicográficas históricas en datos trazables, consultables y reutilizables sin borrar la forma documental original.

La primera colección es el **Corpus Steffel 1791/1809**, basado en el *Tarahumarisches Wörterbuch* de Matthäus Steffel. El cuerpo lexicográfico impreso ocupa pp. 301–368; el cambio alemán→rarámuri / rarámuri→alemán ocurre dentro de p. 353 y el apéndice comienza en p. 369.

## Estado 0.2.0: cobertura integral y revisión editorial

La segmentación de alta cobertura contiene **2,495 candidatos**: 1,607 alemán→rarámuri y 888 rarámuri→alemán. Este número no se presenta como conteo filológico definitivo: Fraktur, OCR y composición a dos columnas producen falsos límites que se depuran mediante evidencia documental explícita.

A través de `RHD-FR-001`–`RHD-FR-022` se han revisado **2,019 límites candidatos**: **1,611 arranques aceptados**, **408 falsos límites** y **681 correcciones claras de lema**. La capa activa queda provisionalmente en **2,087 candidatos**.

Los niveles `high_machine` y `medium_machine` están agotados. En `low_machine` se han revisado **300 de 716 candidatos**: **150 arranques aceptados y 150 falsos límites**. Quedan **416 candidatos de baja confianza**.

## RHD-FR-022: tercer lote de baja confianza

`RHD-FR-022` revisa 100 candidatos en orden determinista. La alineación documental corrige la extensión automática pp. 327–334 a **pp. 326–333**. El resultado es **69 arranques aceptados, 31 falsos límites, 4 correcciones claras de lema y 61 correcciones de página**. Las reparaciones son `Knüttel`, `Koſt`, `Kriegen` y `Lehrling`.

Este lote tiene una **excepción de proveniencia** que se conserva expresamente. En el runtime de FR-022 no estuvieron disponibles las imágenes directas del facsímil. Las decisiones se apoyan en el OCR primario preservado, la arquitectura de página/columnas previamente verificada visualmente en el repositorio y la transcripción académica de la versión publicada sólo como colación secundaria. Por ello `RHD-FR-022` está marcado `direct_facsimile_image_reinspection=false` y debe ser recotejado contra imagen antes de cualquier validación humana o filológica.

El pipeline admite ahora proveniencia heterogénea y el inventario registra `mixed_ai_assisted_editorial_collation`, las metodologías efectivamente utilizadas y el lote pendiente de recotejo directo de imagen. No se transforma esta excepción en una falsa afirmación de cotejo visual.

## Capa diplomática

Los **1,611 arranques aceptados** tienen transcripción diplomática completa IA-asistida. `RHD-DIP-022A`–`RHD-DIP-022G` añaden los **69 artículos** de FR-022, incluidos `Kraut`, `Leopard`, `Mädchen`, `Lernen`, `Maulſchelle`, `Mutter`, `Nachfolgen` y `Nachgehen`.

El inventario registra **622 transcripciones con nota explícita de incertidumbre**. El aumento incluye los 69 registros de FR-022 porque todos conservan explícitamente la obligación de recotejo directo de imagen. Las siete unidades `RHD-DIP-022A`–`G` están marcadas como pendientes de esa comprobación y todos los registros mantienen `human_verified=false`.

El facsímil de 1809 continúa siendo la autoridad editorial. Las fuentes secundarias pueden ayudar a localizar y colacionar una lectura, pero no sustituyen el testimonio primario ni autorizan normalizaciones silenciosas.

La regla editorial es:

**facsímil → OCR bruto → segmentación de alta cobertura → cola editorial determinista → revisión de límites con proveniencia explícita → reconstrucción por columnas → transcripción diplomática → recotejo de imagen cuando corresponda → validación humana/lingüística → normalización → datos estructurados.**

## Datos principales

- `data/entries.csv`: capa maestra integral con overlays editoriales.
- `data/entries_curated.csv`: 60 anclas iniciales con identificadores persistentes.
- `data/review/`: manifiestos append-only de revisión (`RHD-FR-001`–`RHD-FR-022`).
- `data/review/next_review_queue.json`: siguiente cohorte generada determinísticamente.
- `data/facsimile/`: modelo de columnas para pp. 301–368.
- `data/diplomatic/`: 1,611 transcripciones diplomáticas IA-asistidas hasta `RHD-DIP-022G`.
- `data/corpus_inventory.json`: inventario regenerado con métodos y lotes pendientes de recotejo directo.
- JSON, XML, TEI y SQLite: serializaciones derivadas.
- `sources/steffel-1809-ocr-source.txt`: OCR primario preservado sin corrección.

## Reproducibilidad

```bash
python3 scripts/extract_full_corpus.py
python3 scripts/apply_review_overrides.py
python3 scripts/generate_review_queue.py
python3 scripts/generate_exports.py
python3 tests/validate.py
```

El pipeline reconstruye la capa automática, aplica manifiestos editoriales, preserva métodos heterogéneos, excluye IDs ya revisados y regenera exportaciones. GitHub Actions valida el corpus y usa protección de concurrencia para evitar fallos espurios de auto-push cuando `main` avanza durante una ejecución.

La siguiente cohorte es **`RHD-FR-023`**, cuarto lote `low_machine`: 100 de los **416** candidatos restantes, desde `RHD-S1809-00965` (`Nachſehen`) hasta `RHD-S1809-01238` (`Spielplatz`), estimados automáticamente alrededor de pp. **334–343**.

## Identificadores y relación diacrónica

Las unidades usan `RHD-S1809-#####`; un ID nunca se reutiliza aunque su límite sea rechazado. El corpus histórico permanece separado de Rarámuri Digital. Las futuras correspondencias Steffel ↔ Rarámuri Digital serán relaciones explícitas con confianza, método y revisión.

## Responsable

**Dr. Fernando Sandoval Gutierrez**  
Universidad CEEES · Universidad Autónoma de Ciudad Juárez · Cuerpo Académico UACJ-113  
ORCID: 0000-0002-3168-6725

## Licencias

Código: MIT. Las capas editoriales y datos derivados del proyecto se proponen bajo CC BY 4.0. Véanse `DATA_LICENSE.md`, `SOURCES.md` y `PROVENANCE.md`.
