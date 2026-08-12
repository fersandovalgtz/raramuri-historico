<p align="center">
  <strong>Rarámuri Histórico Digital</strong><br>
  Corpus Steffel 1791/1809
</p>

<p align="center">
  <img src="https://img.shields.io/badge/dataset-0.2.0-172033?style=flat-square" alt="Dataset 0.2.0">
  <img src="https://img.shields.io/badge/fuente-Steffel%201809-7a263a?style=flat-square" alt="Steffel 1809">
  <img src="https://img.shields.io/badge/candidatos%20segmentados-2%2C495-2d6a4f?style=flat-square" alt="2,495 candidate entries">
  <img src="https://img.shields.io/badge/l%C3%ADmites%20cotejados-1%2C719-b7791f?style=flat-square" alt="1,719 boundaries reviewed">
  <img src="https://img.shields.io/badge/art%C3%ADculos%20diplom%C3%A1ticos%20AI--asistidos-1%2C461-455B55?style=flat-square" alt="1,461 AI-assisted diplomatic articles">
  <img src="https://img.shields.io/badge/c%C3%B3digo-MIT-172033?style=flat-square" alt="MIT">
</p>

## Propósito

**Rarámuri Histórico Digital** es la infraestructura histórica complementaria de [Rarámuri Digital](https://github.com/fersandovalgtz/raramuri-digital). Su objetivo es convertir fuentes lexicográficas y lingüísticas históricas en datos trazables, consultables y reutilizables sin borrar la forma documental original.

La primera colección es el **Corpus Steffel 1791/1809**, basado en el *Tarahumarisches Wörterbuch* de Matthäus Steffel. La obra contiene vocabulario alemán–tarahumara, vocabulario tarahumara–alemán, observaciones gramaticales y culturales, un apéndice sobre numeración y una muestra lingüística trilingüe.

## Estado 0.2.0: cobertura integral y revisión editorial

La segmentación de alta cobertura contiene **2,495 candidatos de artículo lexicográfico**: **1,607 alemán→rarámuri** y **888 rarámuri→alemán**. Este número no se presenta como conteo filológico definitivo: la tipografía Fraktur, el OCR y la composición a dos columnas producen límites candidatos que deben resolverse contra el facsímil.

A través de `RHD-FR-001`–`RHD-FR-019` se han cotejado visualmente **1,719 límites candidatos**: **1,461 arranques de artículo aceptados**, **258 falsos límites rechazados** y **664 correcciones claras de lema**. Los identificadores rechazados se preservan y nunca se reciclan. La capa activa queda provisionalmente en **2,237 candidatos**.

Los dos niveles superiores de la segmentación automática están ya agotados. Los **609 candidatos `high_machine`** produjeron 553 arranques aceptados y 56 falsos límites. Los **1,110 candidatos `medium_machine`** produjeron **908 arranques aceptados y 202 falsos límites**. Quedan únicamente **716 candidatos `low_machine`** para la revisión sistemática de límites.

## Capa diplomática

Los **1,461 arranques aceptados** cuentan con transcripción diplomática completa IA-asistida. La serie llega a `RHD-DIP-019A`; conserva página, columna, forma documental y notas explícitas de incertidumbre. El inventario registra **521 transcripciones con una nota de incertidumbre**.

`RHD-FR-019` cierra el nivel `medium_machine` con sus diez candidatos finales. Todos habían sido asignados automáticamente a p. 369, pero el cotejo demuestra que **los diez proceden de la columna derecha de p. 368**, inmediatamente antes del apéndice. Nueve son artículos reales y uno —`Bär`— es una glosa/remisión interna de `Vohí, Bär, s. Bär.`. El lote queda en **9 arranques aceptados, 1 falso límite, 9 correcciones de lema y 10 correcciones de página**.

Las nueve entradas recuperadas son `Uélameke`, `Uilí`, `Uipáca`, `Veréndo`, `Vissigó`, `Ulé`, `Ululú`, `Upéameke` y `Vuossaguáca`. `RHD-DIP-019A` proporciona la transcripción diplomática completa de las nueve. La forma impresa `Uélameke` y la glosa `Ulé, Spielblatt.` se conservan literalmente en la capa diplomática aunque la edición académica moderna discuta ambas como posibles errores históricos; la evidencia documental no se normaliza silenciosamente.

El cotejo confirma de nuevo la frontera documental: **el diccionario propiamente dicho termina en p. 368 y el apéndice comienza en p. 369**. Ningún artículo de diccionario se proyecta a p. 369.

El facsímil de 1809 sigue siendo la autoridad. Para grafías rarámuri difíciles se utiliza únicamente como colación secundaria la transcripción publicada por Merrill et al. (2020), DOI `10.47807/UNISON.8`; esta consulta no sustituye al testimonio facsimilar. Todos los registros diplomáticos actuales mantienen **`human_verified=false`**.

La regla editorial es:

**facsímil → OCR bruto → segmentación de alta cobertura → cola editorial determinista → cotejo de límites y dirección → reconstrucción por columnas → transcripción diplomática → validación humana/lingüística → normalización → datos estructurados.**

## Datos principales

- `data/entries.csv`: capa maestra integral con overlays editoriales.
- `data/entries_curated.csv`: 60 anclas iniciales con identificadores persistentes.
- `data/review/`: manifiestos append-only de revisión (`RHD-FR-001`–`RHD-FR-019`).
- `data/review/next_review_queue.json`: siguiente cohorte editorial generada de forma determinista.
- `data/facsimile/`: modelo explícito de columnas para las páginas lexicográficas impresas 301–368.
- `data/diplomatic/`: **1,461 transcripciones diplomáticas IA-asistidas** hasta `RHD-DIP-019A`.
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

La siguiente cohorte sistemática es **`RHD-FR-020`**, el primer lote `low_machine`. La cola determinista contiene los primeros 100 de los 716 candidatos de baja confianza, desde `RHD-S1809-00061` (`Vorrede erinnert habe`) hasta `RHD-S1809-00421` (`Vogel`), automáticamente distribuidos alrededor de pp. 301–316. A diferencia de los niveles superiores, esta cohorte contiene numerosos fragmentos de prosa, glosas y segmentos internos, por lo que se espera una tasa de falsos límites sustancialmente mayor y el facsímil será decisivo para cada aceptación.

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