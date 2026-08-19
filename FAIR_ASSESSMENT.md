# Evaluación FAIR y FAIR4RS — RHD 1.0.1

## Alcance

Esta autoevaluación aplica dos marcos complementarios:

- los principios **FAIR** para datos y objetos de investigación: Findable, Accessible, Interoperable, Reusable;
- los principios **FAIR4RS** para software de investigación, que extienden esos criterios a identificadores de versiones, metadatos ricos, interoperabilidad, licencias, procedencia y reutilización del software.

La evaluación es deliberadamente conservadora: una capacidad sólo se considera cerrada cuando existe evidencia verificable. Para RHD 1.0.1, el gate de persistencia ya está cerrado mediante Zenodo.

## Findable / Localizable

**Estado: alto.**

- Repositorio público y release archivada `v1.0.1`.
- Concept DOI del proyecto: `10.5281/zenodo.21957212`.
- DOI específico de v1.0.1: `10.5281/zenodo.21958018`.
- Identificadores internos estables para registros y artefactos de revisión.
- `CITATION.cff` en la raíz con autor, ORCID, título, versión, fecha, licencia, resumen, palabras clave y DOI de versión.
- `codemeta.json` proporciona metadatos JSON-LD complementarios para software e infraestructura.
- README, `SOURCES.md`, `PROVENANCE.md`, `DATASHEET.md` y documentación específica describen el objeto y su procedencia.
- Release versionada y Git permiten identificar el snapshot científico y su historia de cambios.

### FAIR4RS relacionado

- F1/F1.2: DOI de versión y Concept DOI distinguen snapshot y familia de versiones.
- F2: metadatos ricos en CFF, CodeMeta y documentación humana.
- F3/F4: los identificadores persistentes aparecen explícitamente en metadatos y landing pública.

## Accessible / Accesible

**Estado: alto.**

- Código, datos derivados permitidos y documentación son accesibles por HTTPS/GitHub.
- Existe un sitio público asociado al proyecto.
- Zenodo conserva un snapshot citable fuera del ciclo de vida de la interfaz viva de GitHub Pages.
- Los objetos de datos se distribuyen en formatos abiertos o ampliamente implementados.
- El testimonio, sus reproducciones y materiales de terceros conservan su régimen jurídico y procedencia; accesibilidad técnica no equivale a licencia de reutilización.

### FAIR4RS relacionado

- A1/A1.1: Git/HTTPS, Zenodo y formatos abiertos permiten recuperación mediante protocolos estándar.
- A2: los metadatos de la versión archivada permanecen disponibles mediante el registro persistente.

## Interoperable / Interoperable

**Estado: alto.**

- Capa canónica estructurada y serializaciones CSV, JSON, XML y SQLite.
- Representación TEI RHD rica y proyección TEI Lex-0 estricta.
- Proyección estricta validada contra TEI Lex-0 0.9.5 en el alcance documentado por el corpus científico.
- IIIF Presentation 3 para localización del testimonio y enlaces registro→Canvas.
- JSON Schema y perfiles de fuente para separar el núcleo RHD de particularidades documentales.
- Objetos de procedencia y actividades de transformación diseñados para ser mapeables a modelos de procedencia estándar.
- Relaciones con Rarámuri Digital y otras fuentes se mantienen tipadas y no como fusiones implícitas.

### FAIR4RS relacionado

- I1: lectura/escritura en estándares comunitarios relevantes para humanidades digitales, lexicografía y datos estructurados.
- I2: referencias calificadas a fuente, releases, proyectos relacionados y objetos derivados.

## Reusable / Reutilizable

**Estado: alto, condicionado al respeto del alcance epistemológico.**

- Licencias diferenciadas y explícitas: MIT para software; CC BY 4.0 para datos, metadatos y capas editoriales originales de RHD.
- `PROVENANCE.md`, hashes, manifiestos append-only y estados de revisión permiten reconstruir el origen de decisiones.
- `EDITORIAL_POLICY.md` separa evidencia, transcripción, propuesta, incertidumbre y validación.
- Scripts de generación y pruebas permiten regenerar artefactos y verificar invariantes.
- La replicación sobre Tellechea 1826 demuestra portabilidad del núcleo sin rediseño fundamental.
- La documentación declara explícitamente lo que **no** puede inferirse: los candidatos computacionales no son automáticamente análisis lingüísticos, etimologías ni validaciones humanas.

### FAIR4RS relacionado

- R1/R1.1: atributos relevantes y licencias claras.
- R1.2: procedencia detallada.
- R2: referencias a dependencias conceptuales, estándares y objetos relacionados.
- R3: adopción de prácticas y estándares de la comunidad de investigación digital.

## Citación y persistencia

RHD trata datos y software como productos científicos citables. El repositorio utiliza `CITATION.cff`, CodeMeta, releases versionadas y metadatos legibles por máquina.

Correspondencia pública vigente:

`release v1.0.1 ↔ repositorio GitHub ↔ snapshot Zenodo ↔ DOI 10.5281/zenodo.21958018`

El Concept DOI `10.5281/zenodo.21957212` representa la familia de versiones y debe usarse para enlazar el proyecto vivo; el DOI `10.5281/zenodo.21958018` identifica específicamente v1.0.1 y debe usarse cuando la investigación dependa de ese snapshot.

## Evidencia de buenas prácticas

| Dimensión | Evidencia principal |
|---|---|
| Citación | `CITATION.cff`, `codemeta.json`, Zenodo v1.0.1 |
| Persistencia | Concept DOI `10.5281/zenodo.21957212`; v1.0.1 `10.5281/zenodo.21958018` |
| Procedencia | `PROVENANCE.md`, `sources/checksums.json`, manifiestos de revisión |
| Licencias | `LICENSE`, `DATA_LICENSE.md` |
| Calidad | `tests/`, workflows de GitHub Actions, manifiestos de integridad |
| Documentación de datos | `DATASHEET.md`, `COVERAGE.md`, `EDITORIAL_POLICY.md` |
| Interoperabilidad | TEI, TEI Lex-0, IIIF Presentation 3, JSON Schema, CSV/JSON/XML/SQLite |
| Reproducibilidad | `REPRODUCIBILITY.md`, `scripts/`, tests |
| Versionado | tags, releases, `CHANGELOG.md` |
| Gobernanza | `GOVERNANCE.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md` |
| Ecosistema | `docs/ECOSYSTEM.md` |

## Referencias normativas

- Wilkinson, M. D. et al. 2016. “The FAIR Guiding Principles for scientific data management and stewardship”. *Scientific Data* 3:160018. https://doi.org/10.1038/sdata.2016.18
- Barker, M. et al. 2022. “Introducing the FAIR Principles for research software”. *Scientific Data* 9:622. https://doi.org/10.1038/s41597-022-01710-x
- Data Citation Synthesis Group. 2014. *Joint Declaration of Data Citation Principles*. FORCE11. https://doi.org/10.25490/a97f-egyk
- Smith, A. M.; Katz, D. S.; Niemeyer, K. E.; FORCE11 Software Citation Working Group. 2016. “Software Citation Principles”. *PeerJ Computer Science* 2:e86. https://doi.org/10.7717/peerj-cs.86

## Resultado

**RHD 1.0.1 cumple de manera sustantiva con prácticas FAIR/FAIR4RS en identificadores persistentes, metadatos, acceso, interoperabilidad, licenciamiento, procedencia, reproducibilidad y versionado.** Las principales áreas futuras ya no son de persistencia básica, sino de preservación adicional —por ejemplo Software Heritage—, revisión humana independiente y ampliación controlada a nuevas fuentes.
