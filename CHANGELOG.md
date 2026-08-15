# Changelog

## Unreleased — repository scientific standards

### Documentación científica y descubribilidad

- README reconstruido como landing científica: fuente histórica, estado de la release, arquitectura de evidencia, datos, interoperabilidad, reproducibilidad, citación, licencias, límites epistemológicos y ecosistema.
- Nueva nota documental `docs/STEFFEL_SOURCE.md` para distinguir la experiencia de Steffel, el horizonte manuscrito de 1791, la publicación de 1809 y la representación computacional de RHD.
- Bibliografía y `SOURCES.md` ampliados con la referencia primaria de 1809 y estudios especializados contemporáneos.
- `DATASHEET.md`, `COVERAGE.md`, `PROVENANCE.md`, `FAIR_ASSESSMENT.md` y `REPRODUCIBILITY.md` alineados con el snapshot canónico 1.0.0.
- `CITATION.cff` reforzado con commit canónico, ORCID, afiliación, landing page y palabras clave; `codemeta.json` actualizado como metadatos complementarios del software de investigación.

### Gobernanza y sostenibilidad

- `CONTRIBUTING.md` ampliado con requisitos de evidencia, revisión humana identificada, impacto de cambios de datos y reglas de atribución.
- `GOVERNANCE.md` ampliado con fuentes de autoridad, política de versionado, reglas de releases y manejo explícito del desacuerdo científico.
- Nuevos `CODE_OF_CONDUCT.md` y `SECURITY.md`.
- `ROADMAP.md` reemplazado por una hoja de ruta posterior a 1.0: DOI/archivo, revisión humana opcional, infraestructura reusable, nuevas fuentes, publicación científica y preservación.

### Ecosistema

- Nuevo `docs/ECOSYSTEM.md` con vínculos explícitos hacia Rarámuri Digital, repositorios educativos e histórico-digitales, perfiles académicos, sitios públicos y reglas para mantener separadas las responsabilidades de cada proyecto.
- No se modificaron datos científicos, el tag `v1.0.0` ni su release histórica como parte de esta actualización documental.

## 1.0.0 — 2026-08-15

### Estado

- RHD 1.0 machine-only queda fijado como implementación de referencia reusable para fuentes histórico-digitales.
- Métrica oficial: **99.0% terminado / 1.0% pendiente**. El único residual es archivo/DOI persistente; no queda trabajo científico del corpus dentro del alcance vigente.
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

### Release y archivo

- `CITATION.cff` pasa a `1.0.0`.
- `docs/RELEASE_NOTES_V1.0.0.md` documenta el snapshot estable.
- `RELEASE_READY_V1.0.0` registra autorización explícita.
- `.github/workflows/release-v1.0.0.yml` crea `v1.0.0` y el GitHub Release únicamente después de una CI canónica verde del commit candidato en `main`.
- El proyecto **no se declarará 100%** hasta obtener un depósito persistente real con identificador citable —preferentemente DOI de Zenodo— y verificar su correspondencia con tag/commit/manifiesto.

## 0.9.0-machine-only-prerelease — 2026-08-15

- Se adoptó formalmente la política machine-only.
- Se cerraron computacionalmente los 482 problemas PHIL preservando incertidumbre terminal.
- Se implementaron especificación RHD 1.0, JSON Schema, perfiles de fuente y adaptadores no destructivos.
- Se separaron TEI RHD rica y TEI Lex-0 estricta.
- Se cerraron anexos y calibración diacrónica machine-only.
- Se demostró la industrialización completa sobre Tellechea 1826.
- Se preparó la publicación IIIF y el manifiesto determinista de integridad.
- La métrica prerelease quedó en 98% mientras seguían abiertos IIIF público y archivo/release persistente.

## Trabajo previo relevante

El historial Git conserva las etapas documentales, recotejos PHIL, investigación interna Steffel, análisis de la constelación `-ameke`, pruebas de permutación, desarrollo de anexos, Tellechea y construcción de la arquitectura RHD 1.0. Los manifiestos de revisión y validación permanecen append-only y trazables en `data/`.
