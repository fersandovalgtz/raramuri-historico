<p align="center">
  <strong>Rarámuri Histórico Digital</strong><br>
  Corpus Steffel 1791/1809
</p>

<p align="center">
  <img src="https://img.shields.io/badge/dataset-0.2.0-172033?style=flat-square" alt="Dataset 0.2.0">
  <img src="https://img.shields.io/badge/fuente-Steffel%201809-7a263a?style=flat-square" alt="Steffel 1809">
  <img src="https://img.shields.io/badge/candidatos%20cotejados-2%2C495%2F2%2C495-2d6a4f?style=flat-square" alt="2,495 of 2,495 candidates collated">
  <img src="https://img.shields.io/badge/art%C3%ADculos%20activos-1%2C965-b7791f?style=flat-square" alt="1,965 active articles">
  <img src="https://img.shields.io/badge/transcripci%C3%B3n%20diplom%C3%A1tica-1%2C965%2F1%2C965-455B55?style=flat-square" alt="1,965 of 1,965 active articles diplomatically transcribed">
  <img src="https://img.shields.io/badge/validaci%C3%B3n%20abierta-482-7a263a?style=flat-square" alt="482 explicit open validation records">
  <img src="https://img.shields.io/badge/recotejo%20PHIL-50%2F482-455B55?style=flat-square" alt="50 of 482 open records AI-recollated">
  <img src="https://img.shields.io/badge/c%C3%B3digo-MIT-172033?style=flat-square" alt="MIT">
</p>

## Propósito

**Rarámuri Histórico Digital** es la infraestructura histórica complementaria de [Rarámuri Digital](https://github.com/fersandovalgtz/raramuri-digital). Convierte fuentes lexicográficas históricas en datos trazables, consultables y reutilizables sin borrar la forma documental original.

La primera colección es el **Corpus Steffel 1791/1809**, basado en el *Tarahumarisches Wörterbuch* de Matthäus Steffel. El cuerpo lexicográfico impreso ocupa pp. 301–368; el cambio alemán→rarámuri / rarámuri→alemán ocurre dentro de p. 353 y el apéndice comienza en p. 369.

## Estado 0.2.0: primera pasada facsimilar integral

La segmentación de alta cobertura produjo **2,495 candidatos**: 60 anclas curatoriales, 609 `high_machine`, 1,110 `medium_machine` y 716 `low_machine`. **Los 2,495 han sido cotejados contra el facsímil** mediante revisión editorial IA-asistida. El resultado provisional es **1,965 arranques lexicográficos aceptados**, **530 falsos límites rechazados** y **781 correcciones de lema**.

Los **1,965 artículos activos** tienen transcripción diplomática completa IA-asistida y ningún lote permanece pendiente de recotejo directo de imagen. `data/review/next_review_queue.json` está agotado.

Este hito significa **cobertura editorial/facsimilar y diplomática completa de la fase IA-asistida**, no una edición crítica definitiva. Todos los registros conservan `human_verified=false`. Asimismo, 2,495 es el universo de candidatos de la segmentación de alta cobertura, no un conteo filológico definitivo de entradas; **1,965** es el conteo activo provisional después de depurar falsos límites.

## De notas editoriales a problemas realmente abiertos

Una auditoría posterior mostró que una nota diplomática no equivale automáticamente a una incertidumbre. De los **676 registros con alguna nota diplomática**, **194 documentan decisiones editoriales ya resueltas** y **482 conservan un problema explícitamente abierto**. El campo `diplomatic_note_state` distingue `none`, `resolved_editorial_note` y `open_validation`.

La cola científica de 482 casos se organiza mediante triage determinista: 230 lecturas gráficas, 29 problemas de estructura de artículo, 201 formas históricas rarámuri, 2 cuestiones semánticas/glosa y 20 casos generales. Esta clasificación organiza el trabajo; no es validación lingüística.

## RHD-PHIL: segunda inspección filológica IA-asistida

La nueva serie `RHD-PHIL-###` recoteja contra el facsímil de alta resolución únicamente los casos `open_validation`. Es una capa append-only: **nunca sobrescribe** `headword_diplomatic` ni `article_diplomatic`.

`RHD-PHIL-001` revisó los primeros **50 casos** de pp. 301–320: **25 lecturas fueron confirmadas**, **11 recibieron una corrección gráfica propuesta** y **14 permanecen irresolubles después del segundo recotejo IA-asistido**. Entre las reparaciones propuestas figuran `Mapúieri`, `Napavitſchi`, `Temaſeáli`, `Nachteuje`, `Teé`, `Pultſché`, `Tſchapiboli`, `Tſchutſchá` y `Raveli`. Todas siguen `human_verified=false`.

Quedan **432 casos abiertos por recotejar mediante esta fase IA-asistida**. `data/validation/next_philological_batch.json` apunta ya a `RHD-PHIL-002` con los siguientes 50. En paralelo, `human_review_queue.json` conserva los casos ya recotejados que todavía requieren juicio humano filológico, lingüístico, semántico o disciplinar.

## Frontera documental

`RHD-FR-026` fue revisado con criterio explícitamente **direction-aware**: comienza en p. 352, cruza la inversión dentro de p. 353 y continúa en rarámuri→alemán hasta p. 367. Produjo 54 aceptados y 46 falsos límites.

`RHD-FR-027` resolvió los últimos 16 candidatos `low_machine`: 10 aceptados y 6 rechazados. El cotejo mostró que los candidatos asignados automáticamente a p. 369 pertenecían todavía a p. 368. De este modo queda verificado que **p. 368 es la última página del diccionario y p. 369 inicia el apéndice**.

`RHD-FR-028` auditó las 60 anclas curatoriales iniciales directamente contra el facsímil: las 60 son arranques reales, 31 lemas requirieron reparación documental y cuatro registros fueron reajustados de p. 358 a p. 359. `RHD-DIP-028A`–`F` completaron su capa diplomática.

## Regla editorial

**facsímil → OCR bruto → segmentación de alta cobertura → cotejo de límites y dirección → reconstrucción por columnas → transcripción diplomática → triage de problemas abiertos → recotejo filológico IA-asistido → validación humana/lingüística independiente → normalización → datos estructurados y correspondencias diacrónicas.**

## Datos principales

- `data/entries.csv`: capa maestra integral con overlays editoriales y `diplomatic_note_state`.
- `data/entries_curated.csv`: 60 anclas iniciales sincronizadas con la capa maestra.
- `data/review/`: manifiestos append-only `RHD-FR-001`–`RHD-FR-028`.
- `data/diplomatic/`: **1,965** transcripciones completas hasta `RHD-DIP-028F`.
- `data/validation/uncertainty_queue.json`: **482** casos explícitamente abiertos.
- `data/validation/review/`: manifiestos append-only `RHD-PHIL-###`.
- `data/validation/next_philological_batch.json`: siguiente cohorte determinista aún no recotejada.
- `data/validation/human_review_queue.json`: ruta separada para revisión humana independiente.
- `data/validation/validation_progress.json`: avance cuantitativo de la fase científica.
- `data/corpus_inventory.json`: inventario regenerado y comprobación calculada de cobertura.
- JSON, XML, TEI y SQLite: serializaciones derivadas.

## Reproducibilidad

```bash
python3 scripts/extract_full_corpus.py
python3 scripts/apply_review_overrides.py
python3 scripts/generate_review_queue.py
python3 scripts/generate_validation_queue.py
python3 scripts/generate_next_philological_batch.py
python3 scripts/generate_exports.py
python3 tests/validate.py
python3 tests/validate_validation_phase.py
```

## Siguiente etapa operativa

La siguiente cohorte es **`RHD-PHIL-002`**. La revisión humana independiente sigue en cero y deberá documentar revisor, fecha, competencia, decisión y evidencia. Después corresponde construir normalizaciones explícitas, relaciones de variantes, correspondencias históricas con Rarámuri Digital y anotación crítica sin borrar la capa diplomática.

## Identificadores y relación diacrónica

Las unidades usan `RHD-S1809-#####`; un ID nunca se reutiliza aunque su límite haya sido rechazado. El corpus histórico permanece separado de Rarámuri Digital. Las futuras correspondencias Steffel ↔ Rarámuri Digital serán relaciones explícitas con confianza, método y revisión.

## Responsable

**Dr. Fernando Sandoval Gutierrez**  
Universidad CEEES · Universidad Autónoma de Ciudad Juárez · Cuerpo Académico UACJ-113  
ORCID: 0000-0002-3168-6725

## Licencias

Código: MIT. Las capas editoriales y datos derivados del proyecto se proponen bajo CC BY 4.0. Véanse `DATA_LICENSE.md`, `SOURCES.md` y `PROVENANCE.md`.
