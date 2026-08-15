<p align="center">
  <strong>Rarámuri Histórico Digital</strong><br>
  <em>Corpus Steffel 1791/1809 · edición histórico-digital, datos de investigación e infraestructura reproducible</em>
</p>

<p align="center">
  <a href="https://github.com/fersandovalgtz/raramuri-historico/releases/tag/v1.0.0"><img src="https://img.shields.io/badge/release-v1.0.0-172033?style=flat-square" alt="Release v1.0.0"></a>
  <img src="https://img.shields.io/badge/artículos-1%2C965-2d6a4f?style=flat-square" alt="1,965 artículos activos">
  <img src="https://img.shields.io/badge/fuente-Steffel%201809-7a263a?style=flat-square" alt="Steffel 1809">
  <img src="https://img.shields.io/badge/TEI%20Lex--0-validado-455B55?style=flat-square" alt="TEI Lex-0 validado">
  <img src="https://img.shields.io/badge/IIIF-Presentation%203-b7791f?style=flat-square" alt="IIIF Presentation 3">
  <a href="DATA_LICENSE.md"><img src="https://img.shields.io/badge/datos-CC%20BY%204.0-9a6b1f?style=flat-square" alt="Datos CC BY 4.0"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/código-MIT-172033?style=flat-square" alt="Código MIT"></a>
  <a href="https://orcid.org/0000-0002-3168-6725"><img src="https://img.shields.io/badge/ORCID-0000--0002--3168--6725-A6CE39?style=flat-square&logo=orcid&logoColor=white" alt="ORCID"></a>
</p>

<p align="center">
  <a href="docs/STEFFEL_SOURCE.md"><strong>Fuente histórica</strong></a> ·
  <a href="#estado-científico-de-la-versión-100"><strong>Estado científico</strong></a> ·
  <a href="#datos-y-representaciones"><strong>Datos</strong></a> ·
  <a href="#reproducibilidad"><strong>Reproducibilidad</strong></a> ·
  <a href="#citación"><strong>Citación</strong></a> ·
  <a href="docs/ECOSYSTEM.md"><strong>Ecosistema</strong></a> ·
  <a href="https://raramuri-historico.pages.dev"><strong>Sitio</strong></a>
</p>

---

## Qué es Rarámuri Histórico Digital

**Rarámuri Histórico Digital (RHD)** es una infraestructura de investigación para transformar fuentes históricas sobre la lengua rarámuri en objetos digitales **trazables, versionados, citables, interoperables y reproducibles**, sin borrar la forma documental de la fuente ni convertir inferencias computacionales en hechos lingüísticos.

La implementación de referencia es el **Corpus Steffel 1791/1809**, construido a partir del *Tarahumarisches Wörterbuch* de Matthäus Steffel. El repositorio conserva por separado el testimonio histórico, el OCR, la segmentación, las transcripciones diplomáticas IA-asistidas, las decisiones editoriales, los estados de incertidumbre, las relaciones derivadas y las representaciones interoperables. La incertidumbre explícita es un resultado legítimo: cuando la evidencia no permite una lectura única, el sistema no la fabrica.

RHD no pretende sustituir una edición filológica humana ni hablar en nombre de las comunidades rarámuri contemporáneas. Su objeto es **documental e histórico** y sus afirmaciones se limitan al alcance que cada capa de evidencia permite.

## La fuente: Matthäus Steffel y el *Tarahumarisches Wörterbuch*

Matthäus Steffel (1734–1806) fue un jesuita originario de Jihlava, en Moravia. Se formó en Nueva España y trabajó en la Sierra Tarahumara entre 1761 y 1767, con estancias documentadas en Tónachi, Tomochic, Nonoava y San Francisco de Borja. Tras la expulsión de la Compañía de Jesús de los dominios españoles, regresó a Europa y continuó trabajando sus materiales lingüísticos. La bibliografía especializada sitúa el diccionario en el horizonte intelectual de la Ilustración europea, la historiografía lingüística y las primeras empresas comparativas y tipológicas sobre lenguas americanas.

El texto fue publicado en 1809 por Christoph Gottlieb von Murr dentro del volumen I de *Nachrichten von verschiedenen Ländern des Spanischen Amerika, aus eigenhändigen Aufsätzen einiger Missionare der Gesellschaft Jesu* (Halle: Johann Christian Hendel). La contribución de Steffel ocupa las pp. **293–374**; el cuerpo lexicográfico comienza en la p. **301**, cambia de alemán→rarámuri a rarámuri→alemán dentro de la p. **353**, y los materiales finales incluyen el apéndice sobre numeración y una muestra lingüística con fórmulas en latín, alemán y rarámuri.

El diccionario es más que una lista bilingüe: contiene observaciones sobre usos, costumbres y prácticas comunicativas. Precisamente por ello RHD conserva la **microestructura documental y el contexto** en vez de reducir cada entrada a una equivalencia léxica moderna.

→ [Nota documental, historia de la fuente y bibliografía especializada](docs/STEFFEL_SOURCE.md)

### Referencia primaria

> Steffel, Matthäus. 1809. “Tarahumarisches Wörterbuch, nebst einigen Nachrichten von den Sitten und Gebräuchen der Tarahumaren, in Neu-Biscaya, in der Audiencia Guadalaxara, im Vice-Königreiche Alt-Mexico, oder Neu-Spanien”. En Christoph Gottlieb von Murr (ed.), *Nachrichten von verschiedenen Ländern des Spanischen Amerika, aus eigenhändigen Aufsätzen einiger Missionare der Gesellschaft Jesu*, vol. I, 293–374. Halle: Johann Christian Hendel.

Véanse también [SOURCES.md](SOURCES.md), [PROVENANCE.md](PROVENANCE.md) y la edición contemporánea de William L. Merrill y colaboradores (Universidad de Sonora, 2020; DOI `10.47807/UNISON.8`).

## Estado científico de la versión 1.0.0

La versión canónica **RHD 1.0.0** fija a Steffel 1791/1809 como implementación de referencia de una edición histórico-digital **machine-only**, con trazabilidad y límites epistemológicos explícitos.

| Dimensión | Estado v1.0.0 |
|---|---:|
| Candidatos documentales cotejados | **2,495 / 2,495** |
| Artículos lexicográficos activos | **1,965** |
| Falsos límites preservados | **530** |
| Transcripciones diplomáticas IA-asistidas | **1,965 / 1,965** |
| Casos PHIL recotejados | **482 / 482** |
| `confirmed_ai_assisted` | **284** |
| `corrected_ai_assisted` | **152** |
| `unresolved_after_ai_recollation` | **46** |
| Relaciones diacrónicas computacionales | **298 `candidate`** |
| IIIF Presentation 3 | **84 Canvases** |
| Enlaces registro→Canvas | **1,965** |
| Replicación piloto Tellechea 1826 | **205 / 205 páginas** |

**No se afirma validación humana independiente.** Ningún resultado IA-asistido se presenta como `human_verified`, `philologically_verified_by_human` o `linguistically_verified`. Los 46 casos irresueltos permanecen abiertos deliberadamente y las 298 relaciones diacrónicas permanecen como candidatos; no se promueven automáticamente a cognación, etimología, equivalencia semántica ni continuidad histórica.

La descripción completa del snapshot está en [docs/RELEASE_NOTES_V1.0.0.md](docs/RELEASE_NOTES_V1.0.0.md). El tag canónico es [`v1.0.0`](https://github.com/fersandovalgtz/raramuri-historico/releases/tag/v1.0.0).

## Arquitectura de evidencia

RHD adopta una cadena editorial explícita y no destructiva:

**facsímil → OCR bruto → segmentación → cotejo de límites y dirección → reconstrucción documental → transcripción diplomática → triage de incertidumbre → recotejo filológico IA-asistido → capas derivadas → revisión humana independiente cuando exista**.

Tres reglas gobiernan el corpus:

1. **La fuente no se sobrescribe.** Las correcciones y propuestas viven en overlays o manifiestos append-only.
2. **La procedencia acompaña al dato.** Cada transformación debe poder remontarse a una fuente, página, registro y actividad de procesamiento.
3. **La autoridad de una capa está tipada.** OCR, cotejo IA-asistido, propuesta editorial, revisión humana y análisis lingüístico no son estados intercambiables.

Documentos normativos: [EDITORIAL_POLICY.md](EDITORIAL_POLICY.md) · [PROVENANCE.md](PROVENANCE.md) · [DATASHEET.md](DATASHEET.md) · [COVERAGE.md](COVERAGE.md) · [FAIR_ASSESSMENT.md](FAIR_ASSESSMENT.md).

## Datos y representaciones

El repositorio mantiene una capa maestra y exportaciones derivadas para diferentes necesidades de investigación.

| Recurso | Función |
|---|---|
| `data/entries.csv` | capa maestra con evidencia y overlays editoriales |
| `data/entries_curated.csv` | anclas curatoriales históricas del proceso |
| `data/diplomatic/` | transcripciones diplomáticas IA-asistidas |
| `data/review/` | manifiestos de cotejo documental append-only |
| `data/validation/` | incertidumbre, recotejo PHIL y colas de revisión |
| `data/research/` | concordancias, variantes, pruebas y relaciones derivadas |
| JSON / XML / SQLite | serializaciones reproducibles |
| TEI RHD | representación rica del modelo documental |
| TEI Lex-0 | proyección lexicográfica estricta e interoperable |
| IIIF Presentation 3 | localización del testimonio y enlaces registro→Canvas |
| `schemas/` | contratos de datos y validación estructural |
| `source_profiles/` | configuración específica de cada fuente histórica |

La separación entre **núcleo reusable** y **perfil de fuente** permite aplicar RHD a otros testimonios sin rediseñar la arquitectura universal. La replicación sobre Tellechea 1826 funciona como prueba de esa portabilidad.

## Reproducibilidad

La generación de artefactos científicos está automatizada mediante scripts versionados y pruebas de invariantes. Para reconstruir las principales capas desde un entorno compatible:

```bash
python3 scripts/extract_full_corpus.py
python3 scripts/apply_review_overrides.py
python3 scripts/generate_review_queue.py
python3 scripts/generate_validation_queue.py
python3 scripts/generate_human_review_priority.py
python3 scripts/generate_exports.py
python3 scripts/generate_de_rar_attestations.py
python3 scripts/generate_internal_concordance.py
python3 scripts/generate_historical_variants.py
python3 scripts/generate_graphemic_statistics.py
python3 scripts/generate_research_statistics.py
python3 tests/validate.py
python3 tests/validate_validation_phase.py
```

Los checksums del testimonio de trabajo, las reglas de procedencia y los manifiestos de integridad permiten verificar que un resultado corresponda al estado documental que declara. Consulte [REPRODUCIBILITY.md](REPRODUCIBILITY.md), [PROVENANCE.md](PROVENANCE.md) y `sources/checksums.json`.

## Ciencia abierta, FAIR y preservación

RHD trata **datos y software como productos científicos citables**. La infraestructura incorpora identificadores internos estables, control de versiones, metadatos legibles por máquina, licencias diferenciadas, procedencia, formatos interoperables, validación automatizada y una release científica congelada. La evaluación se documenta en [FAIR_ASSESSMENT.md](FAIR_ASSESSMENT.md), con referencia a FAIR para datos y FAIR4RS para software de investigación.

El archivo persistente con DOI se gestiona como una capa separada de GitHub. **No se declara un DOI hasta verificar que el depósito corresponda exactamente a la release canónica.** Una vez depositado `v1.0.0`, el DOI de versión y, cuando proceda, el DOI conceptual se incorporarán a `CITATION.cff`, README y metadatos del proyecto.

## Citación

Los metadatos canónicos se mantienen en [`CITATION.cff`](CITATION.cff). GitHub puede convertir este archivo directamente a formatos bibliográficos desde **Cite this repository**.

Mientras se completa el depósito persistente de `v1.0.0`, la referencia recomendada es:

> Sandoval Gutierrez, Fernando. 2026. *Rarámuri Histórico Digital — Corpus Steffel 1791/1809*, versión 1.0.0. GitHub. https://github.com/fersandovalgtz/raramuri-historico

Para trabajos que dependan de una versión concreta, cite además el tag/release utilizado. Cuando el DOI esté verificado, éste sustituirá la URL de GitHub como identificador persistente principal de la versión archivada.

## Licencias y derechos

RHD utiliza un esquema deliberadamente separado:

- **software y código original:** [MIT](LICENSE);
- **datos, metadatos, anotaciones, traducciones y capas editoriales originales de RHD:** [CC BY 4.0](DATA_LICENSE.md);
- **fuentes históricas y materiales de terceros:** conservan su propio estatus jurídico y deben citarse según su procedencia.

La licencia CC BY 4.0 de las capas originales **no crea derechos sobre la obra de Steffel ni sobre reproducciones o ediciones de terceros**. La edición crítica contemporánea de 2020 se usa como bibliografía y no se redistribuye sistemáticamente como dataset.

## Ecosistema científico

RHD forma parte de un conjunto de repositorios, servicios y perfiles conectados, no de un proyecto aislado.

| Recurso | Relación con RHD |
|---|---|
| [Rarámuri Digital](https://github.com/fersandovalgtz/raramuri-digital) · [web](https://raramuri.ceees.mx) | infraestructura lexicográfica contemporánea hermana; las relaciones históricas se mantienen como candidatos trazables, no como fusiones automáticas |
| [Rarámuri · recursos educativos](https://github.com/fersandovalgtz/raramuri-recursos-educativos) | capa pedagógica separada del corpus científico |
| [Libro de Texto Mexicano Digital](https://github.com/fersandovalgtz/libro-texto-mexicano-digital) | proyecto hermano de patrimonio documental y humanidades digitales |
| [Historia de la educación en Chihuahua](https://github.com/fersandovalgtz/historia-educacion-chihuahua) | archivo de investigación histórica dentro del mismo ecosistema de ciencia abierta |
| [Recursos educativos abiertos](https://github.com/fersandovalgtz/recursos-educativos-abiertos) | infraestructura de curación y reutilización educativa |
| [Perfil científico en GitHub](https://github.com/fersandovalgtz) | puerta de entrada al conjunto de proyectos y producción abierta |
| [CEEES Cuauhtémoc](https://ceees.mx) | entorno institucional y de divulgación académica vinculado al ecosistema |

→ [Mapa ampliado del ecosistema, perfiles académicos y estrategia de interoperabilidad](docs/ECOSYSTEM.md)

## Autor, responsabilidad y perfiles académicos

**Dr. Fernando Sandoval Gutierrez**  
ORCID: [0000-0002-3168-6725](https://orcid.org/0000-0002-3168-6725)  
Universidad Autónoma de Ciudad Juárez · Universidad CEEES / CEEES Cuauhtémoc · Cuerpo Académico UACJ-113

Perfiles: [GitHub](https://github.com/fersandovalgtz) · [Google Scholar](https://scholar.google.com/citations?user=zNZsYYAAAAAJ&hl=es) · [CATHI-UACJ](https://cathi.uacj.mx/handle/20.500.11961/3028/browse?authority=0000-0002-3168-6725&type=author) · [ResearchGate](https://www.researchgate.net/profile/Fernando-Sandoval-Gutierrez) · [ResearchID](https://researchid.co/fersandovalg) · [Academia.edu](https://uacj.academia.edu/FernandoSandoval)

## Contribución y gobernanza

Las contribuciones documentales, filológicas, lingüísticas, técnicas o históricas son bienvenidas cuando preservan la trazabilidad de la evidencia. Antes de proponer una corrección, revise [CONTRIBUTING.md](CONTRIBUTING.md), [GOVERNANCE.md](GOVERNANCE.md) y [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Los problemas de seguridad se reportan según [SECURITY.md](SECURITY.md).

---

**RHD 1.0.0 preserva el documento histórico, la incertidumbre y el proceso de transformación como partes inseparables del objeto científico.**
