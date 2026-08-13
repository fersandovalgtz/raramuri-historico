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
  <img src="https://img.shields.io/badge/recotejo%20PHIL-482%2F482-455B55?style=flat-square" alt="482 of 482 open records AI-recollated">
  <img src="https://img.shields.io/badge/revisi%C3%B3n%20humana-0%2F482-6b7280?style=flat-square" alt="0 of 482 independently human reviewed">
  <img src="https://img.shields.io/badge/c%C3%B3digo-MIT-172033?style=flat-square" alt="MIT">
</p>

## Propósito

**Rarámuri Histórico Digital** es la infraestructura histórica complementaria de [Rarámuri Digital](https://github.com/fersandovalgtz/raramuri-digital). Convierte fuentes lexicográficas históricas en datos trazables, consultables y reutilizables sin borrar la forma documental original.

La primera colección es el **Corpus Steffel 1791/1809**, basado en el *Tarahumarisches Wörterbuch* de Matthäus Steffel. El cuerpo lexicográfico impreso ocupa pp. 301–368; el cambio alemán→rarámuri / rarámuri→alemán ocurre dentro de p. 353 y el apéndice comienza en p. 369.

## Estado 0.2.0: cobertura documental integral

La segmentación de alta cobertura produjo **2,495 candidatos**: 60 anclas curatoriales, 609 `high_machine`, 1,110 `medium_machine` y 716 `low_machine`. **Los 2,495 han sido cotejados contra el facsímil** mediante revisión editorial IA-asistida. El resultado provisional es **1,965 arranques lexicográficos aceptados**, **530 falsos límites rechazados** y **781 correcciones de lema**.

Los **1,965 artículos activos** tienen transcripción diplomática completa IA-asistida y ningún lote permanece pendiente de recotejo directo de imagen. La cola de límites está agotada. Esto significa cobertura documental/facsimilar y diplomática completa de la fase IA-asistida; **no equivale a una edición crítica definitiva ni a validación humana o lingüística**.

## Auditoría científica de problemas abiertos

De los **676 registros con alguna nota diplomática**, una auditoría separó **194 notas editoriales ya resueltas** de **482 registros que conservaban un problema explícitamente abierto**. El campo `diplomatic_note_state` distingue `none`, `resolved_editorial_note` y `open_validation`.

La cola científica de 482 casos fue clasificada por triage reproducible en 230 lecturas gráficas, 29 problemas de estructura de artículo, 201 formas históricas rarámuri, 2 cuestiones semánticas/glosa y 20 casos generales. Esta clasificación organiza el trabajo; no constituye juicio lingüístico.

## RHD-PHIL-001–010: recotejo filológico IA-asistido completo

La serie **`RHD-PHIL-001`–`RHD-PHIL-010` ha recotejado los 482/482 casos abiertos contra el facsímil de alta resolución**. `data/validation/next_philological_batch.json` queda sin una cohorte automática pendiente y `validation_progress.json` registra `ai_philological_recollation_remaining=0`.

Los manifiestos PHIL son append-only y **nunca sobrescriben** `headword_diplomatic` ni `article_diplomatic`. `confirmed_ai_assisted` sostiene una lectura previa; `corrected_ai_assisted` propone una reparación documental; `unresolved_after_ai_recollation` conserva expresamente un problema que no debe cerrarse sin juicio independiente.

Los últimos lotes fueron reinspeccionados hasta **600 dpi** y permitieron, entre otras reparaciones documentales, proponer `Mir, netſchi` y `jujega` en el artículo `Ich`, `Talahipoa` / `Talahúmali` en `Spiel`, `Caú. Cajútſchi.` en `Roß`, `Painaguéameke`, `Nachcatule`, `Tamatsiame`, `Somúca!`, `Tepágatigameke`, `Techtéke`, `Atác, oder hatúca` y `Tſeſtarácameke, oder Stácameke`. También quedaron deliberadamente abiertos problemas donde la evidencia sigue sin permitir una decisión única, como la estructura lexicográfica de `Lang`, la lectura compacta de `Verlobt`, ciertas secuencias gráficas de `Blind` y `Tſelixugi`.

**Ninguno de esos resultados es `human_verified`.** La fase automática general termina aquí; la siguiente fase legítima es revisión independiente por personas con competencia filológica, lingüística, histórica o disciplinar.

## Prioridad de revisión independiente

Los 482 registros recotejados se ordenan ahora de manera reproducible en `human_review_priority.json`:

- **46** `unresolved_after_ai_recollation` — prioridad 1;
- **152** `corrected_ai_assisted` — prioridad 2;
- **284** `confirmed_ai_assisted` — prioridad 3.

La prioridad no transforma ninguna lectura en validación humana; sólo organiza el trabajo pendiente por página y `record_id`.

## Frontera documental

`RHD-FR-026` fue revisado con criterio **direction-aware** al cruzar la inversión dentro de p. 353. `RHD-FR-027` resolvió los últimos candidatos `low_machine` y verificó que p. 368 cierra el diccionario y p. 369 inicia el apéndice sin candidatos lexicográficos residuales. `RHD-FR-028` auditó directamente las 60 anclas curatoriales y completó su capa diplomática.

## Regla editorial

**facsímil → OCR bruto → segmentación de alta cobertura → cotejo de límites y dirección → reconstrucción por columnas → transcripción diplomática → triage de problemas abiertos → recotejo filológico IA-asistido → validación humana/lingüística independiente → normalización → datos estructurados y correspondencias diacrónicas.**

## Datos principales

- `data/entries.csv`: capa maestra integral con overlays editoriales y `diplomatic_note_state`.
- `data/entries_curated.csv`: 60 anclas iniciales sincronizadas con la capa maestra.
- `data/review/`: manifiestos append-only `RHD-FR-001`–`RHD-FR-028`.
- `data/diplomatic/`: **1,965** transcripciones completas hasta `RHD-DIP-028F`.
- `data/validation/uncertainty_queue.json`: **482** casos explícitamente abiertos en la auditoría científica.
- `data/validation/review/`: manifiestos `RHD-PHIL-001`–`RHD-PHIL-010`, que cubren **482/482** casos.
- `data/validation/next_philological_batch.json`: sin lote pendiente tras agotar la recollación IA-asistida.
- `data/validation/human_review_queue.json`: **482** registros preparados para revisión humana independiente.
- `data/validation/human_review_priority.json` y `human_review_priority_compact.json`: cola ordenada **46 / 152 / 284**.
- `data/validation/HUMAN_REVIEW_PROTOCOL.md`: protocolo de adjudicación humana independiente.
- `data/validation/human_review_template.json`: plantilla estructurada de decisión.
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
python3 scripts/generate_human_review_priority.py
python3 scripts/generate_exports.py
python3 tests/validate.py
python3 tests/validate_validation_phase.py
```

## Siguiente etapa operativa

La siguiente etapa es **revisión humana independiente** de `data/validation/human_review_priority.json`, comenzando por los **46 casos aún irresueltos** y siguiendo con las **152 correcciones propuestas**. Cada decisión debe registrar revisor, fecha, competencia, evidencia y alcance, y distinguir confirmación filológica, decisión lingüística, interpretación semántica y anotación disciplinar. En el estado actual hay **482 casos preparados y 0 registros humanamente verificados**.

Sólo después corresponde adoptar lecturas críticas derivadas, construir normalizaciones explícitas, relaciones de variantes, correspondencias históricas con Rarámuri Digital y anotación crítica. Ninguna de esas capas deberá borrar la evidencia diplomática ni las propuestas PHIL anteriores.

## Identificadores y relación diacrónica

Las unidades usan `RHD-S1809-#####`; un ID nunca se reutiliza aunque su límite haya sido rechazado. El corpus histórico permanece separado de Rarámuri Digital. Las futuras correspondencias Steffel ↔ Rarámuri Digital serán relaciones explícitas con confianza, método y revisión.

## Responsable

**Dr. Fernando Sandoval Gutierrez**  
Universidad CEEES · Universidad Autónoma de Ciudad Juárez · Cuerpo Académico UACJ-113  
ORCID: 0000-0002-3168-6725

## Licencias

Código: MIT. Las capas editoriales y datos derivados del proyecto se proponen bajo CC BY 4.0. Véanse `DATA_LICENSE.md`, `SOURCES.md` y `PROVENANCE.md`.
