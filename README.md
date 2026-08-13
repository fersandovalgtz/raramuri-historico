<p align="center">
  <strong>Rarámuri Histórico Digital</strong><br>
  Corpus Steffel 1791/1809
</p>

<p align="center">
  <img src="https://img.shields.io/badge/dataset-0.2.0-172033?style=flat-square" alt="Dataset 0.2.0">
  <img src="https://img.shields.io/badge/fuente-Steffel%201809-7a263a?style=flat-square" alt="Steffel 1809">
  <img src="https://img.shields.io/badge/candidatos%20segmentados-2%2C495-2d6a4f?style=flat-square" alt="2,495 candidate entries">
  <img src="https://img.shields.io/badge/l%C3%ADmites%20revisados-2%2C319-b7791f?style=flat-square" alt="2,319 boundaries reviewed">
  <img src="https://img.shields.io/badge/art%C3%ADculos%20diplom%C3%A1ticos%20AI--asistidos-1%2C841-455B55?style=flat-square" alt="1,841 AI-assisted diplomatic articles">
  <img src="https://img.shields.io/badge/c%C3%B3digo-MIT-172033?style=flat-square" alt="MIT">
</p>

## Propósito

**Rarámuri Histórico Digital** es la infraestructura histórica complementaria de [Rarámuri Digital](https://github.com/fersandovalgtz/raramuri-digital). Convierte fuentes lexicográficas históricas en datos trazables, consultables y reutilizables sin borrar la forma documental original.

La primera colección es el **Corpus Steffel 1791/1809**, basado en el *Tarahumarisches Wörterbuch* de Matthäus Steffel. El cuerpo lexicográfico impreso ocupa pp. 301–368; el cambio alemán→rarámuri / rarámuri→alemán ocurre dentro de p. 353 y el apéndice comienza en p. 369.

## Estado 0.2.0

La segmentación de alta cobertura contiene **2,495 candidatos**: 1,607 alemán→rarámuri y 888 rarámuri→alemán. A través de `RHD-FR-001`–`RHD-FR-025` se han revisado **2,319 límites candidatos**: **1,841 arranques aceptados**, **478 falsos límites** y **705 correcciones claras de lema**. La capa activa queda provisionalmente en **2,017 candidatos**.

Los niveles `high_machine` y `medium_machine` están agotados. En `low_machine` se han revisado **600 de 716 candidatos**: **380 aceptados y 220 rechazados**. Quedan **116**.

## Recotejo y lotes recientes

`RHD-FR-022` y `RHD-DIP-022A`–`G` fueron recotejados directamente contra las imágenes originales; ya no existe ningún lote pendiente de recotejo de imagen. `RHD-FR-023`, pp. 333–343, produjo 58 aceptados / 42 rechazados. `RHD-FR-024`, pp. 343–347, produjo 86 / 14 y resolvió el catchword `Stute` de p. 344 junto con la recuperación del lema `Stroh`.

`RHD-FR-025`, pp. **347–352**, revisó 100 candidatos: **86 aceptados, 14 rechazados, 10 correcciones de lema y 27 correcciones de página**. Entre las reparaciones figuran `Verfault`, `Verleihen`, `Verlobt`, `Vier`, `Vor`, `Vorlängst`, `Wie immer`, `Wiederholen`, `Wo` y `Ziegelerde`. Sus 86 artículos están completos en `RHD-DIP-025A`–`I`.

## Capa diplomática

Los **1,841 arranques aceptados** tienen transcripción diplomática completa IA-asistida. El inventario registra **620 transcripciones con nota explícita de incertidumbre**. El facsímil de 1809 es la autoridad; las lecturas difíciles se mantienen como provisionales cuando corresponde. Todos los registros permanecen `human_verified=false`.

La regla editorial es:

**facsímil → OCR bruto → segmentación de alta cobertura → cola editorial determinista → cotejo de límites y dirección → reconstrucción por columnas → transcripción diplomática → validación humana/lingüística → normalización → datos estructurados.**

## Datos principales

- `data/entries.csv`: capa maestra integral con overlays editoriales.
- `data/entries_curated.csv`: 60 anclas iniciales con identificadores persistentes.
- `data/review/`: manifiestos append-only (`RHD-FR-001`–`RHD-FR-025`).
- `data/review/next_review_queue.json`: siguiente cohorte determinista.
- `data/facsimile/`: modelo de columnas para pp. 301–368.
- `data/diplomatic/`: 1,841 transcripciones completas hasta `RHD-DIP-025I`.
- `data/corpus_inventory.json`: inventario regenerado.
- JSON, XML, TEI y SQLite: serializaciones derivadas.

## Reproducibilidad

```bash
python3 scripts/extract_full_corpus.py
python3 scripts/apply_review_overrides.py
python3 scripts/generate_review_queue.py
python3 scripts/generate_exports.py
python3 tests/validate.py
```

## Siguiente etapa: RHD-FR-026

`RHD-FR-026` contiene 100 de los **116** candidatos `low_machine` restantes, desde `RHD-S1809-01609` (`Zinnen`) hasta `RHD-S1809-02404` (OCR `Tofacameke Weiß`). La cohorte comienza en p. 352 y **cruza el cambio de dirección dentro de p. 353**, extendiéndose automáticamente hasta aproximadamente p. 367. Por tanto deberá revisarse con gramática de lema sensible a la dirección: antes de la frontera el headword es alemán; después, el headword es rarámuri y el alemán funciona como glosa. Tras FR-026 quedarían sólo 16 candidatos bajos.

## Identificadores y relación diacrónica

Las unidades usan `RHD-S1809-#####`; un ID nunca se reutiliza aunque su límite sea rechazado. El corpus histórico permanece separado de Rarámuri Digital. Las futuras correspondencias Steffel ↔ Rarámuri Digital serán relaciones explícitas con confianza, método y revisión.

## Responsable

**Dr. Fernando Sandoval Gutierrez**  
Universidad CEEES · Universidad Autónoma de Ciudad Juárez · Cuerpo Académico UACJ-113  
ORCID: 0000-0002-3168-6725

## Licencias

Código: MIT. Las capas editoriales y datos derivados del proyecto se proponen bajo CC BY 4.0. Véanse `DATA_LICENSE.md`, `SOURCES.md` y `PROVENANCE.md`.
