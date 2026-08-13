<p align="center">
  <strong>Rarámuri Histórico Digital</strong><br>
  Corpus Steffel 1791/1809
</p>

<p align="center">
  <img src="https://img.shields.io/badge/dataset-0.2.0-172033?style=flat-square" alt="Dataset 0.2.0">
  <img src="https://img.shields.io/badge/fuente-Steffel%201809-7a263a?style=flat-square" alt="Steffel 1809">
  <img src="https://img.shields.io/badge/candidatos%20segmentados-2%2C495-2d6a4f?style=flat-square" alt="2,495 candidate entries">
  <img src="https://img.shields.io/badge/l%C3%ADmites%20revisados-2%2C219-b7791f?style=flat-square" alt="2,219 boundaries reviewed">
  <img src="https://img.shields.io/badge/art%C3%ADculos%20diplom%C3%A1ticos%20AI--asistidos-1%2C755-455B55?style=flat-square" alt="1,755 AI-assisted diplomatic articles">
  <img src="https://img.shields.io/badge/c%C3%B3digo-MIT-172033?style=flat-square" alt="MIT">
</p>

## Propósito

**Rarámuri Histórico Digital** es la infraestructura histórica complementaria de [Rarámuri Digital](https://github.com/fersandovalgtz/raramuri-digital). Convierte fuentes lexicográficas históricas en datos trazables, consultables y reutilizables sin borrar la forma documental original.

La primera colección es el **Corpus Steffel 1791/1809**, basado en el *Tarahumarisches Wörterbuch* de Matthäus Steffel. El cuerpo lexicográfico impreso ocupa pp. 301–368; el cambio alemán→rarámuri / rarámuri→alemán ocurre dentro de p. 353 y el apéndice comienza en p. 369.

## Estado 0.2.0

La segmentación de alta cobertura contiene **2,495 candidatos**: 1,607 alemán→rarámuri y 888 rarámuri→alemán. Este número no se presenta como conteo filológico definitivo: Fraktur, OCR y composición a dos columnas producen falsos límites que se depuran contra el facsímil.

A través de `RHD-FR-001`–`RHD-FR-024` se han revisado **2,219 límites candidatos**: **1,755 arranques aceptados**, **464 falsos límites** y **695 correcciones claras de lema**. La capa activa queda provisionalmente en **2,031 candidatos**.

Los niveles `high_machine` y `medium_machine` están agotados. En `low_machine` se han revisado **500 de 716 candidatos**: **294 aceptados y 206 rechazados**. Quedan **216**.

## Recotejo directo de RHD-FR-022

El facsímil original volvió a estar disponible y `RHD-FR-022` fue recotejado directamente contra las imágenes de pp. 326–333. El balance de límites se confirmó —69 aceptados / 31 rechazados— y sus cuatro reparaciones de lema permanecieron válidas. Las 69 transcripciones de `RHD-DIP-022A`–`G` también fueron revisadas contra imagen directa; entre las correcciones documentales resultantes figuran `Körper, Sepála`, `Lichtputze, Natſíla` y `Müßig, Nalſinaja / Nalſinäe`.

Ya no existe ningún lote pendiente de recotejo de imagen. Todos los registros continúan `human_verified=false`: cotejo directo por IA no equivale a validación humana, filológica o lingüística.

## RHD-FR-023 y RHD-FR-024

`RHD-FR-023`, pp. **333–343**, revisó 100 candidatos: **58 aceptados, 42 rechazados, 4 correcciones de lema y 29 correcciones de página**. Sus 58 artículos están completos en `RHD-DIP-023A`–`F`, incluidos `Packſattel`, `Schlangen`, `Sohle`, `Speiſe` y `Spielplatz`.

`RHD-FR-024`, pp. **343–347**, revisó otros 100: **86 aceptados, 14 rechazados, 10 correcciones de lema y 19 correcciones de página**. La auditoría de solapamiento detectó que `RHD-S1809-01296` (`Stute`) era el catchword de p. 344 y evitó duplicar el artículo auténtico ya representado por `RHD-S1809-01297`. Al mismo tiempo recuperó `RHD-S1809-01293` como el lema genuino `Stroh`. Las 86 transcripciones completas están en `RHD-DIP-024A`–`I`, incluidos `Strick`, `Tanz` y la serie `Un-` / `Ver-` de p. 347.

## Capa diplomática

Los **1,755 arranques aceptados** tienen transcripción diplomática completa IA-asistida. El inventario registra **598 transcripciones con nota explícita de incertidumbre**. El facsímil de 1809 es la autoridad; las lecturas difíciles se conservan como provisionales cuando corresponde y no se normalizan silenciosamente.

La regla editorial es:

**facsímil → OCR bruto → segmentación de alta cobertura → cola editorial determinista → cotejo de límites y dirección → reconstrucción por columnas → transcripción diplomática → validación humana/lingüística → normalización → datos estructurados.**

## Datos principales

- `data/entries.csv`: capa maestra integral con overlays editoriales.
- `data/entries_curated.csv`: 60 anclas iniciales con identificadores persistentes.
- `data/review/`: manifiestos append-only de revisión (`RHD-FR-001`–`RHD-FR-024`).
- `data/review/next_review_queue.json`: siguiente cohorte generada determinísticamente.
- `data/facsimile/`: modelo de columnas para pp. 301–368.
- `data/diplomatic/`: 1,755 transcripciones diplomáticas IA-asistidas hasta `RHD-DIP-024I`.
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

El pipeline reconstruye la capa automática, aplica manifiestos editoriales, excluye IDs ya revisados y regenera exportaciones. GitHub Actions valida el corpus y protege los auto-push concurrentes.

La siguiente cohorte es **`RHD-FR-025`**, sexto lote `low_machine`: 100 de los **216** candidatos restantes, desde `RHD-S1809-01419` (`Verbrechen`) hasta `RHD-S1809-01608` (`Zinn`), estimados alrededor de pp. **348–352**. Después quedarán 116 candidatos bajos, ya muy próximos a la transición de dirección de p. 353.

## Identificadores y relación diacrónica

Las unidades usan `RHD-S1809-#####`; un ID nunca se reutiliza aunque su límite sea rechazado. El corpus histórico permanece separado de Rarámuri Digital. Las futuras correspondencias Steffel ↔ Rarámuri Digital serán relaciones explícitas con confianza, método y revisión.

## Responsable

**Dr. Fernando Sandoval Gutierrez**  
Universidad CEEES · Universidad Autónoma de Ciudad Juárez · Cuerpo Académico UACJ-113  
ORCID: 0000-0002-3168-6725

## Licencias

Código: MIT. Las capas editoriales y datos derivados del proyecto se proponen bajo CC BY 4.0. Véanse `DATA_LICENSE.md`, `SOURCES.md` y `PROVENANCE.md`.
