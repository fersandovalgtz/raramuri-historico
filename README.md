<p align="center">
  <strong>Rarámuri Histórico Digital</strong><br>
  Corpus Steffel 1791/1809
</p>

<p align="center">
  <img src="https://img.shields.io/badge/dataset-0.2.0-172033?style=flat-square" alt="Dataset 0.2.0">
  <img src="https://img.shields.io/badge/fuente-Steffel%201809-7a263a?style=flat-square" alt="Steffel 1809">
  <img src="https://img.shields.io/badge/candidatos%20segmentados-2%2C495-2d6a4f?style=flat-square" alt="2,495 candidate entries">
  <img src="https://img.shields.io/badge/l%C3%ADmites%20cotejados-1%2C709-b7791f?style=flat-square" alt="1,709 boundaries reviewed">
  <img src="https://img.shields.io/badge/art%C3%ADculos%20diplom%C3%A1ticos%20AI--asistidos-1%2C452-455B55?style=flat-square" alt="1,452 AI-assisted diplomatic articles">
  <img src="https://img.shields.io/badge/c%C3%B3digo-MIT-172033?style=flat-square" alt="MIT">
</p>

## Propósito

**Rarámuri Histórico Digital** es la infraestructura histórica complementaria de [Rarámuri Digital](https://github.com/fersandovalgtz/raramuri-digital). Su objetivo es convertir fuentes lexicográficas y lingüísticas históricas en datos trazables, consultables y reutilizables sin borrar la forma documental original.

La primera colección es el **Corpus Steffel 1791/1809**, basado en el *Tarahumarisches Wörterbuch* de Matthäus Steffel. La obra contiene vocabulario alemán–tarahumara, vocabulario tarahumara–alemán, observaciones gramaticales y culturales, un apéndice sobre numeración y una muestra lingüística trilingüe.

## Estado 0.2.0: cobertura integral y revisión editorial

La segmentación de alta cobertura contiene **2,495 candidatos de artículo lexicográfico**: **1,607 alemán→rarámuri** y **888 rarámuri→alemán**. Este número no se presenta como conteo filológico definitivo: la tipografía Fraktur, el OCR y la composición a dos columnas producen límites candidatos que deben resolverse contra el facsímil.

A través de `RHD-FR-001`–`RHD-FR-018` se han cotejado visualmente **1,709 límites candidatos**: **1,452 arranques de artículo aceptados**, **257 falsos límites rechazados** y **655 correcciones claras de lema**. Los identificadores rechazados se preservan y nunca se reciclan. La capa activa queda provisionalmente en **2,238 candidatos**.

La totalidad de los **609 candidatos `high_machine`** ya fue resuelta. También se han revisado **1,100 de los 1,110 candidatos `medium_machine`**: **899 arranques aceptados y 201 falsos límites**. Restan sólo **10 candidatos de confianza media** y posteriormente 716 candidatos `low_machine`.

## Capa diplomática

Los **1,452 arranques aceptados** cuentan con transcripción diplomática completa IA-asistida. La serie llega a `RHD-DIP-018I`; conserva página, columna, forma documental y notas explícitas de incertidumbre. El inventario registra **521 transcripciones con una nota de incertidumbre**.

`RHD-FR-018` revisa el undécimo lote sistemático de 100 candidatos `medium_machine`, en el extremo final del vocabulario rarámuri→alemán. El cotejo directo corrige su extensión automática a las páginas impresas **364–368**: **87 arranques aceptados, 13 falsos límites, 82 correcciones claras de lema y 45 correcciones de página**. Entre los falsos límites aparecen glosas alemanas (`Gott`, `Weiß`, `Nein`, `Spielen`, `Winkel`, `Maus`, `Eichhörnchen`), un running header, un catchword, un ejemplo gramatical y un artefacto OCR sin correlato facsimilar.

Este lote fija además una frontera documental importante: **el diccionario propiamente dicho termina en p. 368 y el apéndice comienza en p. 369**. Los candidatos que el OCR había desplazado a p. 369 fueron recolocados en p. 368 sólo cuando el facsímil mostró un artículo lexicográfico real; ningún registro de FR-018 fue aceptado como entrada de diccionario en p. 369.

Entre las lecturas recuperadas figuran `Rhenéke`, `R-guála`, `Schugiámeke`, `Sinépi putié`, `Tajenaságo`, `Telsiguála`, `Tótschi`, `Tschie`, `Tschulugéameke`, `Tlestatáccameke, oder Stácameke`, `Tulchilki`, `Vakítsi` y `Vassúritschi`. `RHD-DIP-018A`–`RHD-DIP-018I` proporcionan transcripción completa para los 87 artículos aceptados.

El facsímil de 1809 sigue siendo la autoridad. Para grafías rarámuri difíciles se utiliza únicamente como colación secundaria la transcripción publicada por Merrill et al. (2020), DOI `10.47807/UNISON.8`; esta consulta no sustituye al testimonio facsimilar. Todos los registros diplomáticos actuales mantienen **`human_verified=false`**.

La regla editorial es:

**facsímil → OCR bruto → segmentación de alta cobertura → cola editorial determinista → cotejo de límites y dirección → reconstrucción por columnas → transcripción diplomática → validación humana/lingüística → normalización → datos estructurados.**

## Datos principales

- `data/entries.csv`: capa maestra integral con overlays editoriales.
- `data/entries_curated.csv`: 60 anclas iniciales con identificadores persistentes.
- `data/review/`: manifiestos append-only de revisión (`RHD-FR-001`–`RHD-FR-018`).
- `data/review/next_review_queue.json`: siguiente cohorte editorial generada de forma determinista.
- `data/facsimile/`: modelo explícito de columnas para las páginas lexicográficas impresas 301–368.
- `data/diplomatic/`: **1,452 transcripciones diplomáticas IA-asistidas** hasta `RHD-DIP-018I`.
- `data/corpus_inventory.json`: inventario regenerado de cobertura y progreso editorial.
- `data/json/entries.json`, `data/xml/entries.xml`, `data/xml/steffel-1809-tei-machine.xml` y `data/raramuri_historico.sqlite`: serializaciones derivadas.
- `sources/steffel-1809-ocr-source.txt`: OCR primario preservado sin corrección.

## Reproducibilidad

```bash
python3 scripts/extract_full_corpus.py
python3 scripts/apply_review_overrides.py
python3 scripts/generate_review_queue.py
python3 scripts/generate_exports.py
python3 tests/validate.py
```

El pipeline reconstruye la capa automática, aplica los manifiestos editoriales, genera la siguiente cola en orden de fuente y excluye todos los IDs ya revisados. Las correcciones nunca sustituyen el OCR fuente. GitHub Actions valida los overlays y regenera las exportaciones derivadas. El workflow usa concurrencia por rama y evita auto-commits obsoletos cuando `main` ya avanzó, reduciendo fallos espurios por carreras de `git push`.

La siguiente cohorte sistemática es **`RHD-FR-019`**. La cola determinista contiene los **10 `medium_machine` restantes**, desde `RHD-S1809-02480` (`Uelemeke`) hasta `RHD-S1809-02494` (`Vuoſſaguaca`), todos etiquetados automáticamente como p. 369. Dado que el apéndice comienza en esa página, FR-019 deberá determinar contra el facsímil si cada candidato es una entrada rezagada de p. 368, un artefacto de linealización o material no lexicográfico del apéndice. Después de FR-019 comenzará la revisión sistemática de `low_machine`.

## Identificadores

Las unidades usan `RHD-S1809-#####`. Los identificadores `RHD-S1809-00001` a `RHD-S1809-00060` continúan vinculados a sus 60 anclas originales. Un identificador asignado no se reutiliza aunque un límite sea posteriormente rechazado o fusionado.

## Relación con Rarámuri Digital

El corpus histórico permanece separado de la base contemporánea. Las futuras correspondencias Steffel ↔ Rarámuri Digital se modelarán como relaciones explícitas con estado, confianza, método y revisión; nunca como fusiones automáticas.

- Recurso contemporáneo: https://raramuri.ceees.mx
- Repositorio contemporáneo: https://github.com/fersandovalgtz/raramuri-digital

## Responsable

**Dr. Fernando Sandoval Gutierrez**  
Universidad CEEES · Universidad Autónoma de Ciudad Juárez · Cuerpo Académico UACJ-113  
ORCID: 0000-0002-3168-6725

## Licencias

Código: MIT. Las capas editoriales y datos derivados del proyecto se proponen bajo CC BY 4.0. El facsímil histórico y las reproducciones de terceros deben citarse y reutilizarse conforme a su propia procedencia. Véanse `DATA_LICENSE.md`, `SOURCES.md` y `PROVENANCE.md`.