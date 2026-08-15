# Evaluación FAIR y FAIR4RS — RHD 1.0

## Alcance

Esta autoevaluación aplica dos marcos complementarios:

- los principios **FAIR** para datos y objetos de investigación: Findable, Accessible, Interoperable, Reusable;
- los principios **FAIR4RS** para software de investigación, que extienden esos criterios a identificadores de versiones, metadatos ricos, interoperabilidad, licencias, procedencia y reutilización del software.

La evaluación es deliberadamente conservadora. Un requisito dependiente de un servicio externo no se considera cerrado hasta que exista evidencia verificable. En particular, el DOI de RHD `v1.0.0` permanece **pendiente de verificación** aunque la release científica ya esté congelada en GitHub.

## Findable / Localizable

**Estado: alto, con un gate persistente pendiente.**

- Repositorio público y versión canónica etiquetada como `v1.0.0`.
- Identificadores internos estables para registros y artefactos de revisión.
- `CITATION.cff` en la raíz con autor, ORCID, título, versión, fecha, licencia, resumen y palabras clave.
- `codemeta.json` proporciona metadatos JSON-LD complementarios para software e infraestructura.
- README, `SOURCES.md`, `PROVENANCE.md`, `DATASHEET.md` y documentación específica describen el objeto y su procedencia.
- Release versionada y commit asociado permiten identificar el snapshot científico exacto.
- **Pendiente:** verificar un depósito persistente externo con DOI para `v1.0.0` y propagar ese identificador a todos los metadatos.

### FAIR4RS relacionado

- F1/F1.2: la release y el tag distinguen versiones; el DOI aportará el identificador global persistente de archivo.
- F2: metadatos ricos en CFF, CodeMeta y documentación humana.
- F3/F4: el identificador persistente se incorporará explícitamente cuando el depósito sea verificado.

## Accessible / Accesible

**Estado: alto.**

- Código, datos derivados permitidos y documentación son accesibles por HTTPS/GitHub.
- Existe un sitio público asociado al proyecto.
- Los objetos de datos se distribuyen en formatos abiertos o ampliamente implementados.
- El testimonio, sus reproducciones y materiales de terceros conservan su régimen jurídico y procedencia; la accesibilidad técnica no se confunde con licencia de reutilización.
- La documentación de una versión debe permanecer útil incluso si una interfaz web cambia; por eso el proyecto prioriza release, metadatos y archivo persistente sobre la URL de una aplicación viva.

### FAIR4RS relacionado

- A1/A1.1: Git/HTTPS y formatos abiertos permiten recuperación mediante protocolos estándar.
- A2: el objetivo del depósito persistente es asegurar que los metadatos de la versión permanezcan disponibles fuera del ciclo de vida de GitHub.

## Interoperable / Interoperable

**Estado: alto.**

- Capa canónica estructurada y serializaciones CSV, JSON, XML y SQLite.
- Representación TEI RHD rica y proyección TEI Lex-0 estricta.
- Proyección estricta validada contra TEI Lex-0 0.9.5 en el alcance documentado por la release 1.0.0.
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

RHD sigue el principio de que **datos y software son productos científicos citables**. El repositorio utiliza `CITATION.cff`, releases versionadas y metadatos legibles por máquina. Para la versión 1.0.0 se considera necesario un archivo externo persistente porque una URL de GitHub y un hash de commit, aunque importantes para la trazabilidad, no sustituyen por sí solos un identificador persistente de archivo reconocido en el sistema académico.

El cierre del gate será:

`release v1.0.0 ↔ commit canónico ↔ manifiesto de integridad ↔ depósito persistente ↔ DOI verificado`.

Hasta completar esa correspondencia, el proyecto no mostrará un badge DOI de RHD ni insertará un DOI no comprobado.

## Evidencia de buenas prácticas

| Dimensión | Evidencia principal |
|---|---|
| Citación | `CITATION.cff`, `codemeta.json`, release `v1.0.0` |
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

**RHD 1.0 cumple de manera sustantiva con prácticas FAIR/FAIR4RS en metadatos, acceso, interoperabilidad, licenciamiento, procedencia, reproducibilidad y versionado. El punto deliberadamente no cerrado es el identificador persistente externo de la release canónica.** Ese punto deberá actualizarse únicamente después de verificar el depósito real.
