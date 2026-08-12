<p align="center">
  <strong>Rarámuri Histórico Digital</strong><br>
  Corpus Steffel 1791/1809
</p>

<p align="center">
  <img src="https://img.shields.io/badge/dataset-0.2.0-172033?style=flat-square" alt="Dataset 0.2.0">
  <img src="https://img.shields.io/badge/fuente-Steffel%201809-7a263a?style=flat-square" alt="Steffel 1809">
  <img src="https://img.shields.io/badge/candidatos%20segmentados-2%2C495-2d6a4f?style=flat-square" alt="2,495 candidate entries">
  <img src="https://img.shields.io/badge/l%C3%ADmites%20cotejados-1%2C609-b7791f?style=flat-square" alt="1,609 boundaries reviewed">
  <img src="https://img.shields.io/badge/art%C3%ADculos%20diplom%C3%A1ticos%20AI--asistidos-1%2C365-455B55?style=flat-square" alt="1,365 AI-assisted diplomatic articles">
  <img src="https://img.shields.io/badge/c%C3%B3digo-MIT-172033?style=flat-square" alt="MIT">
</p>

## Propósito

**Rarámuri Histórico Digital** es la infraestructura histórica complementaria de [Rarámuri Digital](https://github.com/fersandovalgtz/raramuri-digital). Su objetivo es convertir fuentes lexicográficas y lingüísticas históricas en datos trazables, consultables y reutilizables sin borrar la forma documental original.

La primera colección es el **Corpus Steffel 1791/1809**, basado en el *Tarahumarisches Wörterbuch* de Matthäus Steffel. La obra contiene vocabulario alemán–tarahumara, vocabulario tarahumara–alemán, observaciones gramaticales y culturales, un apéndice sobre numeración y una muestra lingüística trilingüe.

## Estado 0.2.0: cobertura integral y revisión editorial

La segmentación de alta cobertura contiene **2,495 candidatos de artículo lexicográfico**: **1,607 alemán→rarámuri** y **888 rarámuri→alemán**. El número 2,495 no se presenta como conteo filológico definitivo: la tipografía Fraktur, el OCR y la composición a dos columnas producen límites candidatos que deben resolverse contra el facsímil.

A través de `RHD-FR-001`–`RHD-FR-017` se han cotejado visualmente **1,609 límites candidatos**: **1,365 arranques de artículo aceptados**, **244 falsos límites rechazados** y **573 correcciones claras de lema**. Los identificadores rechazados se preservan y nunca se reciclan. La capa activa queda provisionalmente en **2,251 candidatos**.

La totalidad de los **609 candidatos `high_machine`** ya fue resuelta. También se han revisado **1,000 de los 1,110 candidatos `medium_machine`**: **812 arranques aceptados y 188 falsos límites**. Restan sólo **110 candidatos de confianza media** y posteriormente 716 candidatos `low_machine`.

## Capa diplomática

Los **1,365 arranques aceptados** cuentan con transcripción diplomática completa IA-asistida. La serie llega a `RHD-DIP-017J`; conserva página, columna, forma documental y notas explícitas de incertidumbre. El inventario registra **512 transcripciones con una nota de incertidumbre**.

`RHD-FR-017` revisa el décimo lote sistemático de 100 candidatos `medium_machine`, íntegramente en rarámuri→alemán. El cotejo directo corrige su extensión real a las páginas impresas **360–364**: **91 arranques aceptados, 9 falsos límites, 90 correcciones claras de lema y 24 correcciones de página**. Los nueve límites rechazados son glosas alemanas elevadas erróneamente a candidatos independientes por el OCR lineal, entre ellas `Brod`, `Mehr`, `Kriegen`, `Zange`, `Belohnen`, `Bekennen`, `Wahrheit`, `Weg` y `Nicht viel`.

Entre las recuperaciones facsimilares figuran `Lála`, `Lessíameke`, `Moorápera`, `Nachtétuje`, `Nacuguíta`, `Nassípasic`, `Noitsámela`, `Ossanaguóameke`, `Pitschabúrameke`, `Rachtábatsáboa`, `Rauguelíki` y `Rhaná`. `RHD-DIP-017A`–`RHD-DIP-017J` proporcionan transcripción completa para los 91 artículos aceptados. La última glosa de `Putschíla` se conserva literalmente como `uber.` y queda señalada para relectura humana independiente.

El facsímil de 1809 sigue siendo la autoridad. Para grafías rarámuri difíciles se utiliza únicamente como colación secundaria la transcripción publicada por Merrill et al. (2020), DOI `10.47807/UNISON.8`; esta consulta no sustituye al testimonio facsimilar. Todos los registros diplomáticos actuales mantienen **`human_verified=false`**.

La regla editorial es:

**facsímil → OCR bruto → segmentación de alta cobertura → cola editorial determinista → cotejo de límites y dirección → reconstrucción por columnas → transcripción diplomática → validación humana/lingüística → normalización → datos estructurados.**

## Datos principales

- `data/entries.csv`: capa maestra integral con overlays editoriales.
- `data/entries_curated.csv`: 60 anclas iniciales con identificadores persistentes.
- `data/review/`: manifiestos append-only de revisión (`RHD-FR-001`–`RHD-FR-017`).
- `data/review/next_review_queue.json`: siguiente cohorte editorial generada de forma determinista.
- `data/facsimile/`: modelo explícito de columnas para las páginas lexicográficas impresas 301–368.
- `data/diplomatic/`: **1,365 transcripciones diplomáticas IA-asistidas** hasta `RHD-DIP-017J`.
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

El pipeline reconstruye la capa automática, aplica los manifiestos editoriales, genera la siguiente cola en orden de fuente y excluye todos los IDs ya revisados. Las correcciones nunca sustituyen el OCR fuente. GitHub Actions valida los overlays y regenera las exportaciones derivadas.

La siguiente cohorte sistemática es **`RHD-FR-018`**. La cola determinista contiene los siguientes 100 `medium_machine`, desde `RHD-S1809-02234` (`Rheneke`) hasta `RHD-S1809-02478` (`Vaflürichi`). La estimación automática abarca pp. 365–369; como el diccionario propiamente dicho termina en p. 368 y el apéndice comienza en p. 369, el próximo cotejo tratará ese límite documental como un problema editorial explícito y no asumirá que los candidatos etiquetados como p. 369 pertenezcan al vocabulario.

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