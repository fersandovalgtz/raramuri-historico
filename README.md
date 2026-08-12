<p align="center">
  <strong>Rarámuri Histórico Digital</strong><br>
  Corpus Steffel 1791/1809
</p>

<p align="center">
  <img src="https://img.shields.io/badge/dataset-0.2.0-172033?style=flat-square" alt="Dataset 0.2.0">
  <img src="https://img.shields.io/badge/fuente-Steffel%201809-7a263a?style=flat-square" alt="Steffel 1809">
  <img src="https://img.shields.io/badge/candidatos%20segmentados-2%2C495-2d6a4f?style=flat-square" alt="2,495 candidate entries">
  <img src="https://img.shields.io/badge/l%C3%ADmites%20cotejados-1%2C819-b7791f?style=flat-square" alt="1,819 boundaries reviewed">
  <img src="https://img.shields.io/badge/art%C3%ADculos%20diplom%C3%A1ticos%20AI--asistidos-1%2C501-455B55?style=flat-square" alt="1,501 AI-assisted diplomatic articles">
  <img src="https://img.shields.io/badge/c%C3%B3digo-MIT-172033?style=flat-square" alt="MIT">
</p>

## Propósito

**Rarámuri Histórico Digital** es la infraestructura histórica complementaria de [Rarámuri Digital](https://github.com/fersandovalgtz/raramuri-digital). Convierte fuentes lexicográficas históricas en datos trazables, consultables y reutilizables sin borrar la forma documental original.

La primera colección es el **Corpus Steffel 1791/1809**, basado en el *Tarahumarisches Wörterbuch* de Matthäus Steffel. El cuerpo lexicográfico impreso ocupa pp. 301–368; el cambio alemán→rarámuri / rarámuri→alemán ocurre dentro de p. 353 y el apéndice comienza en p. 369.

## Estado 0.2.0: cobertura integral y revisión editorial

La segmentación de alta cobertura contiene **2,495 candidatos**: 1,607 alemán→rarámuri y 888 rarámuri→alemán. Este número no se presenta como conteo filológico definitivo: Fraktur, OCR y composición a dos columnas producen falsos límites que se resuelven contra el facsímil.

A través de `RHD-FR-001`–`RHD-FR-020` se han cotejado **1,819 límites candidatos**: **1,501 arranques aceptados**, **318 falsos límites** y **672 correcciones claras de lema**. La capa activa queda provisionalmente en **2,177 candidatos**.

Los niveles `high_machine` y `medium_machine` están agotados: 609 candidatos altos produjeron 553 aceptados / 56 rechazados; 1,110 candidatos medios produjeron 908 / 202. `RHD-FR-020` inaugura `low_machine`: de sus primeros 100 candidatos sólo **40 son arranques reales y 60 son falsos límites**. Quedan **616 `low_machine`**.

## RHD-FR-020: primer lote de baja confianza

El cotejo facsimilar corrige la extensión automática pp. 301–316 a **pp. 301–314** y registra **52 correcciones de página**. Los falsos límites son sobre todo prosa, ejemplos, equivalentes rarámuri o subentradas internas de artículos extensos; esto confirma el cambio de perfil de error esperado para el nivel bajo.

Los 40 arranques aceptados incluyen, entre otros, `Abſchneiden`, `Als`, `Arm`, `Armbruſt`, `Bauen`, `Baum`, `Begreifen`, `Behend`, `Berauſchen`, `Betrübt ſeyn`, `Dörren`, `Drauſſen`, `Ehemann`, `Eichhorn`, `Eben ſo` y `Einſam`. Ocho lemas requieren corrección clara respecto del OCR. `Drauſſen` ejemplifica la necesidad de cotejo visual: aparece como catchword al pie de p. 312, pero su artículo comienza en p. 313.

## Capa diplomática

Los **1,501 arranques aceptados** tienen transcripción diplomática completa IA-asistida. `RHD-DIP-020A`–`RHD-DIP-020E` añaden las 40 transcripciones de FR-020, incluidos artículos extensos como `Armbruſt`, `Bauen`, `Baum` y `Eichhorn`. El inventario registra **529 transcripciones con nota explícita de incertidumbre**. Todos los registros mantienen `human_verified=false`.

El facsímil de 1809 es la autoridad. Merrill et al. (2020), DOI `10.47807/UNISON.8`, se utiliza únicamente como colación secundaria para lecturas difíciles; nunca sustituye ni normaliza silenciosamente el testimonio histórico.

La regla editorial es:

**facsímil → OCR bruto → segmentación de alta cobertura → cola editorial determinista → cotejo de límites y dirección → reconstrucción por columnas → transcripción diplomática → validación humana/lingüística → normalización → datos estructurados.**

## Datos principales

- `data/entries.csv`: capa maestra integral con overlays editoriales.
- `data/entries_curated.csv`: 60 anclas iniciales con identificadores persistentes.
- `data/review/`: manifiestos append-only de revisión (`RHD-FR-001`–`RHD-FR-020`).
- `data/review/next_review_queue.json`: siguiente cohorte generada determinísticamente.
- `data/facsimile/`: modelo de columnas para pp. 301–368.
- `data/diplomatic/`: 1,501 transcripciones diplomáticas IA-asistidas hasta `RHD-DIP-020E`.
- `data/corpus_inventory.json`: inventario regenerado.
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

El pipeline reconstruye la capa automática, aplica manifiestos editoriales, excluye IDs ya revisados y regenera exportaciones. GitHub Actions valida el corpus y usa una protección de concurrencia para evitar fallos espurios de auto-push cuando `main` avanza durante una ejecución.

La siguiente cohorte es **`RHD-FR-021`**, segundo lote `low_machine`: 100 de los 616 candidatos restantes, desde `RHD-S1809-00422` (`Haaſe`) hasta `RHD-S1809-00787` (`Kienholz zum Brennen`), estimados automáticamente alrededor de pp. 316–326. La pertenencia y paginación de cada candidato seguirán resolviéndose contra el facsímil.

## Identificadores y relación diacrónica

Las unidades usan `RHD-S1809-#####`; un ID nunca se reutiliza aunque su límite sea rechazado. El corpus histórico permanece separado de Rarámuri Digital. Las futuras correspondencias Steffel ↔ Rarámuri Digital serán relaciones explícitas con confianza, método y revisión.

## Responsable

**Dr. Fernando Sandoval Gutierrez**  
Universidad CEEES · Universidad Autónoma de Ciudad Juárez · Cuerpo Académico UACJ-113  
ORCID: 0000-0002-3168-6725

## Licencias

Código: MIT. Las capas editoriales y datos derivados del proyecto se proponen bajo CC BY 4.0. Véanse `DATA_LICENSE.md`, `SOURCES.md` y `PROVENANCE.md`.
