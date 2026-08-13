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
  <img src="https://img.shields.io/badge/c%C3%B3digo-MIT-172033?style=flat-square" alt="MIT">
</p>

## Propósito

**Rarámuri Histórico Digital** es la infraestructura histórica complementaria de [Rarámuri Digital](https://github.com/fersandovalgtz/raramuri-digital). Convierte fuentes lexicográficas históricas en datos trazables, consultables y reutilizables sin borrar la forma documental original.

La primera colección es el **Corpus Steffel 1791/1809**, basado en el *Tarahumarisches Wörterbuch* de Matthäus Steffel. El cuerpo lexicográfico impreso ocupa pp. 301–368; el cambio alemán→rarámuri / rarámuri→alemán ocurre dentro de p. 353 y el apéndice comienza en p. 369.

## Estado 0.2.0: primera pasada facsimilar integral

La segmentación de alta cobertura produjo **2,495 candidatos**: 60 anclas curatoriales, 609 `high_machine`, 1,110 `medium_machine` y 716 `low_machine`. **Los 2,495 han sido cotejados contra el facsímil** mediante revisión editorial IA-asistida. El resultado provisional es **1,965 arranques lexicográficos aceptados**, **530 falsos límites rechazados** y **781 correcciones de lema**.

Los **1,965 artículos activos** tienen transcripción diplomática completa IA-asistida. El inventario registra **676 transcripciones con nota explícita de incertidumbre** y ningún lote pendiente de recotejo directo de imagen. `data/review/next_review_queue.json` y su versión compacta están agotados.

Este hito significa **cobertura editorial/facsimilar y diplomática completa de la fase IA-asistida**, no una edición crítica definitiva. Todos los registros conservan `human_verified=false`: la validación humana, filológica y lingüística independiente sigue pendiente. Asimismo, 2,495 es el universo de candidatos de la segmentación de alta cobertura, no un conteo filológico definitivo de entradas; **1,965** es el conteo activo provisional después de depurar falsos límites.

## Cierre de la frontera documental

`RHD-FR-026` fue revisado con criterio explícitamente **direction-aware**: comienza en p. 352, cruza la inversión dentro de p. 353 y continúa en rarámuri→alemán hasta p. 367. Produjo 54 aceptados y 46 falsos límites; después de la inversión, glosas alemanas como `Kind`, `Natter`, `Pfeffer`, `Speise` o `Bart` dejaron de ser tratadas como posibles headwords.

`RHD-FR-027` resolvió los últimos 16 candidatos `low_machine`: 10 aceptados y 6 rechazados. El cotejo mostró que los candidatos asignados automáticamente a p. 369 pertenecían todavía a la columna derecha de p. 368. De este modo queda verificado que **p. 368 es la última página del diccionario y p. 369 inicia el apéndice**, sin candidatos lexicográficos residuales en el apéndice.

`RHD-FR-028` auditó las 60 anclas curatoriales iniciales directamente contra el facsímil: las 60 son arranques reales, 31 lemas requirieron reparación documental y cuatro registros fueron reajustados de p. 358 a p. 359. `RHD-DIP-028A`–`F` completaron su capa diplomática.

## Capa diplomática

`data/diplomatic/` contiene una transcripción diplomática completa para cada uno de los **1,965 arranques activos aceptados**. La capa preserva grafía histórica, ſ larga, diacríticos, variantes, ejemplos y notas extensas cuando el facsímil los sustenta. Las lecturas que aún requieren juicio filológico o lingüístico conservan una nota de incertidumbre en vez de ser normalizadas silenciosamente.

La regla editorial es:

**facsímil → OCR bruto → segmentación de alta cobertura → cotejo de límites y dirección → reconstrucción por columnas → transcripción diplomática → validación humana/lingüística → normalización → datos estructurados.**

## Datos principales

- `data/entries.csv`: capa maestra integral con overlays editoriales.
- `data/entries_curated.csv`: 60 anclas iniciales, ahora sincronizadas con el cotejo facsimilar y la capa diplomática.
- `data/review/`: manifiestos append-only `RHD-FR-001`–`RHD-FR-028`.
- `data/review/next_review_queue.json`: cola determinista actualmente vacía.
- `data/facsimile/`: modelo de columnas para pp. 301–368.
- `data/diplomatic/`: **1,965** transcripciones completas hasta `RHD-DIP-028F`.
- `data/corpus_inventory.json`: inventario regenerado y comprobación calculada de cobertura.
- JSON, XML, TEI y SQLite: serializaciones derivadas.

## Reproducibilidad

```bash
python3 scripts/extract_full_corpus.py
python3 scripts/apply_review_overrides.py
python3 scripts/generate_review_queue.py
python3 scripts/generate_exports.py
python3 tests/validate.py
```

`apply_review_overrides.py` calcula `all_candidate_boundaries_facsimile_reviewed`, `full_diplomatic_transcription_completed` y `full_active_corpus_coverage`; estas banderas sólo son verdaderas cuando los conteos y la proveniencia satisfacen las condiciones del pipeline.

## Siguiente etapa editorial

Ya no existe una siguiente cohorte automática. La prioridad pasa a **validación humana/filológica y lingüística independiente**, comenzando por los **676 registros con nota de incertidumbre**. Después corresponde establecer normalizaciones explícitas, relaciones de variantes, correspondencias históricas con Rarámuri Digital y, cuando proceda, anotación crítica de los contenidos culturales e históricos de la fuente.

## Identificadores y relación diacrónica

Las unidades usan `RHD-S1809-#####`; un ID nunca se reutiliza aunque su límite haya sido rechazado. El corpus histórico permanece separado de Rarámuri Digital. Las futuras correspondencias Steffel ↔ Rarámuri Digital serán relaciones explícitas con confianza, método y revisión.

## Responsable

**Dr. Fernando Sandoval Gutierrez**  
Universidad CEEES · Universidad Autónoma de Ciudad Juárez · Cuerpo Académico UACJ-113  
ORCID: 0000-0002-3168-6725

## Licencias

Código: MIT. Las capas editoriales y datos derivados del proyecto se proponen bajo CC BY 4.0. Véanse `DATA_LICENSE.md`, `SOURCES.md` y `PROVENANCE.md`.
