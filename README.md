<p align="center">
  <strong>Rarámuri Histórico Digital</strong><br>
  Corpus Steffel 1791/1809
</p>

<p align="center">
  <img src="https://img.shields.io/badge/dataset-0.2.0-172033?style=flat-square" alt="Dataset 0.2.0">
  <img src="https://img.shields.io/badge/fuente-Steffel%201809-7a263a?style=flat-square" alt="Steffel 1809">
  <img src="https://img.shields.io/badge/candidatos%20segmentados-2%2C495-2d6a4f?style=flat-square" alt="2,495 candidate entries">
  <img src="https://img.shields.io/badge/l%C3%ADmites%20cotejados-1%2C919-b7791f?style=flat-square" alt="1,919 boundaries reviewed">
  <img src="https://img.shields.io/badge/art%C3%ADculos%20diplom%C3%A1ticos%20AI--asistidos-1%2C542-455B55?style=flat-square" alt="1,542 AI-assisted diplomatic articles">
  <img src="https://img.shields.io/badge/c%C3%B3digo-MIT-172033?style=flat-square" alt="MIT">
</p>

## Propósito

**Rarámuri Histórico Digital** es la infraestructura histórica complementaria de [Rarámuri Digital](https://github.com/fersandovalgtz/raramuri-digital). Convierte fuentes lexicográficas históricas en datos trazables, consultables y reutilizables sin borrar la forma documental original.

La primera colección es el **Corpus Steffel 1791/1809**, basado en el *Tarahumarisches Wörterbuch* de Matthäus Steffel. El cuerpo lexicográfico impreso ocupa pp. 301–368; el cambio alemán→rarámuri / rarámuri→alemán ocurre dentro de p. 353 y el apéndice comienza en p. 369.

## Estado 0.2.0: cobertura integral y revisión editorial

La segmentación de alta cobertura contiene **2,495 candidatos**: 1,607 alemán→rarámuri y 888 rarámuri→alemán. Este número no se presenta como conteo filológico definitivo: Fraktur, OCR y composición a dos columnas producen falsos límites que se resuelven contra el facsímil.

A través de `RHD-FR-001`–`RHD-FR-021` se han cotejado **1,919 límites candidatos**: **1,542 arranques aceptados**, **377 falsos límites** y **677 correcciones claras de lema**. La capa activa queda provisionalmente en **2,118 candidatos**.

Los niveles `high_machine` y `medium_machine` están agotados. En `low_machine` se han revisado **200 de 716 candidatos**: **81 arranques aceptados y 119 falsos límites**. Quedan **516 candidatos de baja confianza**.

## RHD-FR-021: segundo lote de baja confianza

`RHD-FR-021` revisa 100 candidatos en orden determinista. El facsímil corrige la extensión automática pp. 316–326 a **pp. 314–326**. El resultado es **41 arranques reales, 59 falsos límites, 5 correcciones claras de lema y 37 correcciones de página**.

Las cinco reparaciones de lema son `Flachs`, `Forttragen`, `Hügel`, `Hurtig` y `Jenſeits des Fluſſes`. El lote confirma patrones característicos de baja confianza: prosa de artículos largos, ejemplos, equivalentes rarámuri, repeticiones internas y catchwords. `RHD-S1809-00671` (`Heil`) es un caso explícito: el candidato procede del catchword al pie de p. 323; el artículo real comienza en p. 324 bajo otro ID persistente.

## Capa diplomática

Los **1,542 arranques aceptados** tienen transcripción diplomática completa IA-asistida. `RHD-DIP-021A`–`RHD-DIP-021E` añaden los **41 artículos completos** aceptados en FR-021, incluidos `Flachs`, `Gegenwart`, `Großvater`, `Heurathen`, `Hülſenfrucht`, `Ich`, `Klein` y `Kienholz zum Brennen`.

El inventario registra **553 transcripciones con nota explícita de incertidumbre**. Las notas documentan dificultades reales de grafía, diacríticos o secuencias rarámuri; todos los registros mantienen `human_verified=false`.

El facsímil de 1809 es la autoridad. Merrill et al. (2020), DOI `10.47807/UNISON.8`, se utiliza únicamente como colación secundaria para lecturas difíciles; nunca sustituye ni normaliza silenciosamente el testimonio histórico.

La regla editorial es:

**facsímil → OCR bruto → segmentación de alta cobertura → cola editorial determinista → cotejo de límites y dirección → reconstrucción por columnas → transcripción diplomática → validación humana/lingüística → normalización → datos estructurados.**

## Datos principales

- `data/entries.csv`: capa maestra integral con overlays editoriales.
- `data/entries_curated.csv`: 60 anclas iniciales con identificadores persistentes.
- `data/review/`: manifiestos append-only de revisión (`RHD-FR-001`–`RHD-FR-021`).
- `data/review/next_review_queue.json`: siguiente cohorte generada determinísticamente.
- `data/facsimile/`: modelo de columnas para pp. 301–368.
- `data/diplomatic/`: 1,542 transcripciones diplomáticas IA-asistidas hasta `RHD-DIP-021E`.
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

La siguiente cohorte es **`RHD-FR-022`**, tercer lote `low_machine`: los primeros 100 de los **516** candidatos restantes, desde `RHD-S1809-00789` (`Kieſelſtein`) hasta `RHD-S1809-00964` (OCR `C | ſondere bedeutet eine ver`), estimados automáticamente alrededor de pp. **327–334**. Cada disposición seguirá resolviéndose contra el facsímil.

## Identificadores y relación diacrónica

Las unidades usan `RHD-S1809-#####`; un ID nunca se reutiliza aunque su límite sea rechazado. El corpus histórico permanece separado de Rarámuri Digital. Las futuras correspondencias Steffel ↔ Rarámuri Digital serán relaciones explícitas con confianza, método y revisión.

## Responsable

**Dr. Fernando Sandoval Gutierrez**  
Universidad CEEES · Universidad Autónoma de Ciudad Juárez · Cuerpo Académico UACJ-113  
ORCID: 0000-0002-3168-6725

## Licencias

Código: MIT. Las capas editoriales y datos derivados del proyecto se proponen bajo CC BY 4.0. Véanse `DATA_LICENSE.md`, `SOURCES.md` y `PROVENANCE.md`.
