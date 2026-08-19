# Changelog

## Unreleased — repository experience and metadata alignment

### Added

- New repository header artwork and stronger visual hierarchy inspired by the mature Rarámuri Digital repository, while retaining a distinct historical-documentary identity for RHD.
- English-language repository overview for international discovery.
- Clearer quality signals for CI, CFF, CodeMeta, FAIR/FAIR4RS, provenance, reproducibility and persistent identifiers.

### Changed

- Public-facing metadata now consistently identifies `v1.0.1` as the current archived release.
- `CITATION.cff` now points to the version DOI `10.5281/zenodo.21958018`, uses MIT for the software record, and states the machine-only validation boundary for v1.0.1.
- `codemeta.json` now identifies version 1.0.1 and links both the version DOI and the Concept DOI `10.5281/zenodo.21957212`.
- Repository navigation and landing content are being aligned with the strongest design and discoverability patterns already proven in Rarámuri Digital.

### Scientific data

- No corpus records, transcriptions, review states, uncertainty states, diachronic candidates or historical-source evidence are modified by this intervention.

## 1.0.1 — 2026-08-15

### Documentation, metadata and preservation

- Patch release focused on scientific documentation, metadata, discoverability, governance and ecosystem integration.
- Scientific corpus unchanged from 1.0.0.
- Archived in Zenodo as **Software**.
- Version DOI: **10.5281/zenodo.21958018**.
- Concept DOI for all RHD versions: **10.5281/zenodo.21957212**.

## 1.0.0 — 2026-08-15

### Estado

- RHD 1.0 machine-only queda fijado como implementación de referencia reusable para fuentes histórico-digitales.
- Métrica oficial en el momento del release: **99.0% terminado / 1.0% pendiente**, correspondiente entonces al archivo/DOI persistente.
- PR #2 fusionado a `main`.
- Licencia definitiva: **MIT** para software/código y **CC BY 4.0** para datos, metadatos y capas editoriales originales de RHD.

### Corpus Steffel

- 2,495 candidatos documentales con disposición; 1,965 artículos activos; 530 falsos límites preservados.
- 1,965/1,965 transcripciones diplomáticas IA-asistidas.
- 482 casos PHIL terminales: 284 `confirmed_ai_assisted`, 152 `corrected_ai_assisted`, 46 `unresolved_after_ai_recollation`.
- Cero afirmaciones de validación humana.

### Interoperabilidad y anexos

- TEI RHD rica y TEI Lex-0 estricta separadas; proyección estricta validada contra TEI Lex-0 0.9.5.
- Anexos `PDF 79–84 ↔ impreso 369–374`: numeración, 22 fórmulas, Padre Nuestro y 43 incertidumbres terminales explícitas.
- IIIF Presentation 3 público: 84 Canvases, 1,965 enlaces registro→Canvas, 0 regiones `xywh` inventadas.
- El pipeline canónico de `main` verifica con éxito el endpoint IIIF público; la dimensión TEI / Lex-0 / IIIF queda al 100%.

### Investigación y replicación

- 298 relaciones diacrónicas permanecen `candidate`, calibradas contra 5,066 emparejamientos nulos deterministas; no se interpretan automáticamente como semántica, cognación, etimología o continuidad histórica.
- Tellechea 1826 procesa 205/205 páginas con el mismo núcleo RHD, 0 rediseños del núcleo universal, 0 entradas Lex-0 fabricadas y 0 atribuciones humanas.

### Release

- `docs/RELEASE_NOTES_V1.0.0.md` documenta el snapshot estable.
- `RELEASE_READY_V1.0.0` registra autorización explícita.
- `.github/workflows/release-v1.0.0.yml` crea `v1.0.0` y el GitHub Release únicamente después de una CI canónica verde del commit candidato en `main`.

## 0.9.0-machine-only-prerelease — 2026-08-15

- Se adoptó formalmente la política machine-only.
- Se cerraron computacionalmente los 482 problemas PHIL preservando incertidumbre terminal.
- Se implementaron especificación RHD 1.0, JSON Schema, perfiles de fuente y adaptadores no destructivos.
- Se separaron TEI RHD rica y TEI Lex-0 estricta.
- Se cerraron anexos y calibración diacrónica machine-only.
- Se demostró la industrialización completa sobre Tellechea 1826.
- Se preparó la publicación IIIF y el manifiesto determinista de integridad.

## Trabajo previo relevante

El historial Git conserva las etapas documentales, recotejos PHIL, investigación interna Steffel, análisis de la constelación `-ameke`, pruebas de permutación, desarrollo de anexos, Tellechea y construcción de la arquitectura RHD 1.0. Los manifiestos de revisión y validación permanecen append-only y trazables en `data/`.
