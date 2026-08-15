<p align="center">
  <strong>Rarámuri Histórico Digital</strong><br>
  <em>Corpus Steffel 1791/1809 · edición histórico-digital · datos de investigación · infraestructura reproducible</em>
</p>

<p align="center">
  <a href="https://github.com/fersandovalgtz/raramuri-historico/releases/tag/v1.0.1"><img src="https://img.shields.io/badge/release-v1.0.1-172033?style=flat-square" alt="Release v1.0.1"></a>
  <a href="https://doi.org/10.5281/zenodo.21957212"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.21957212.svg" alt="DOI"></a>
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
  <a href="#estado-científico-de-rhd-101"><strong>Estado científico</strong></a> ·
  <a href="#datos-e-interoperabilidad"><strong>Datos</strong></a> ·
  <a href="#reproducibilidad-y-ciencia-abierta"><strong>Reproducibilidad</strong></a> ·
  <a href="#citación"><strong>Citación</strong></a> ·
  <a href="docs/ECOSYSTEM.md"><strong>Ecosistema</strong></a> ·
  <a href="https://fersandovalgtz.github.io/raramuri-historico/"><strong>Sitio público</strong></a>
</p>

---

## Qué es Rarámuri Histórico Digital

**Rarámuri Histórico Digital (RHD)** es una infraestructura de investigación para transformar fuentes históricas sobre la lengua rarámuri en objetos digitales **trazables, versionados, citables, interoperables y reproducibles**, sin borrar la forma documental de la fuente ni convertir inferencias computacionales en hechos lingüísticos.

La implementación de referencia es el **Corpus Steffel 1791/1809**, construido a partir del *Tarahumarisches Wörterbuch* de Matthäus Steffel. El repositorio conserva separadamente el testimonio histórico, OCR, segmentación, transcripciones diplomáticas IA-asistidas, decisiones editoriales, incertidumbres, relaciones derivadas y representaciones interoperables. Cuando la evidencia no permite una lectura única, la incertidumbre se conserva como resultado legítimo.

RHD es una edición histórico-digital **machine-only**. La release pública vigente es **v1.0.1**, una actualización de documentación, metadatos, descubribilidad y ecosistema que conserva sin cambios el contenido científico fijado en v1.0.0. No sustituye una edición filológica humana ni habla en nombre de las comunidades rarámuri contemporáneas. Su objeto es documental e histórico y cada afirmación queda limitada por la autoridad de la capa que la sustenta.

## Matthäus Steffel y el *Tarahumarisches Wörterbuch*

Matthäus Steffel (1734–1806), jesuita originario de Jihlava, Moravia, trabajó en la Sierra Tarahumara entre 1761 y 1767, con estancias documentadas en Tónachi, Tomochic, Nonoava y San Francisco de Borja. Tras la expulsión de la Compañía de Jesús de los dominios españoles regresó a Europa y continuó elaborando materiales lingüísticos.

El diccionario fue publicado póstumamente en **1809** por Christoph Gottlieb von Murr dentro del volumen I de *Nachrichten von verschiedenen Ländern des Spanischen Amerika, aus eigenhändigen Aufsätzen einiger Missionare der Gesellschaft Jesu* (Halle: Johann Christian Hendel). La contribución de Steffel ocupa las pp. **293–374**; el cuerpo lexicográfico comienza en la p. **301**, cambia de alemán→rarámuri a rarámuri→alemán dentro de la p. **353** y es seguido por materiales anexos hasta la p. 374.

La fórmula **1791/1809** no designa dos ediciones impresas. `1791` remite al horizonte manuscrito y epistolar documentado durante la elaboración de los materiales; `1809` es la fecha de la edición impresa utilizada por RHD. La historia documental, bibliografía y criterios de esta denominación se explican en [docs/STEFFEL_SOURCE.md](docs/STEFFEL_SOURCE.md).

El texto no es sólo una lista bilingüe: integra observaciones de uso, gramática, prácticas comunicativas y descripciones culturales propias de su contexto histórico. RHD preserva esa microestructura y atribuye los juicios históricos a la fuente, en vez de convertirlos en afirmaciones contemporáneas del proyecto.

### Referencia primaria

> Steffel, Matthäus. 1809. “Tarahumarisches Wörterbuch, nebst einigen Nachrichten von den Sitten und Gebräuchen der Tarahumaren, in Neu-Biscaya, in der Audiencia Guadalaxara, im Vice-Königreiche Alt-Mexico, oder Neu-Spanien”. En Christoph Gottlieb von Murr (ed.), *Nachrichten von verschiedenen Ländern des Spanischen Amerika, aus eigenhändigen Aufsätzen einiger Missionare der Gesellschaft Jesu*, vol. I, 293–374. Halle: Johann Christian Hendel.

Véanse [SOURCES.md](SOURCES.md), [PROVENANCE.md](PROVENANCE.md) y la edición contemporánea de William L. Merrill y colaboradores, publicada por la Universidad de Sonora en 2020 (DOI `10.47807/UNISON.8`).

## Estado científico de RHD 1.0.1

La release **`v1.0.1`** es la versión pública vigente y archivada en Zenodo. Conserva sin cambios el corpus científico fijado por **`v1.0.0`** y añade mejoras de documentación científica, metadatos, citación, descubribilidad y articulación del ecosistema.

| Dimensión | Estado v1.0.1 |
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

**No se afirma validación humana independiente.** Ningún resultado IA-asistido se presenta como `human_verified`, `philologically_verified_by_human` o `linguistically_verified`. Las 298 relaciones diacrónicas permanecen como candidatos; no se promueven automáticamente a cognación, etimología, equivalencia semántica ni continuidad histórica.

→ [Release v1.0.1](https://github.com/fersandovalgtz/raramuri-historico/releases/tag/v1.0.1) · [Notas científicas de v1.0.0](docs/RELEASE_NOTES_V1.0.0.md) · [Política editorial](EDITORIAL_POLICY.md) · [Cobertura](COVERAGE.md)

## Arquitectura de evidencia

RHD adopta una cadena editorial explícita y no destructiva:

**testimonio → OCR bruto → segmentación → cotejo de límites y dirección → reconstrucción documental → transcripción diplomática IA-asistida → triage de incertidumbre → recotejo PHIL → capas derivadas → revisión humana independiente cuando exista**.

Tres reglas gobiernan el corpus:

1. **La fuente no se sobrescribe.** Correcciones y propuestas viven en capas o manifiestos que preservan la evidencia previa.
2. **La procedencia acompaña al dato.** Toda transformación debe poder remontarse a una fuente, página, registro y actividad de procesamiento.
3. **La autoridad de una capa está tipada.** OCR, cotejo IA-asistido, propuesta editorial, revisión humana y análisis lingüístico no son estados intercambiables.

Documentos normativos: [EDITORIAL_POLICY.md](EDITORIAL_POLICY.md) · [PROVENANCE.md](PROVENANCE.md) · [DATASHEET.md](DATASHEET.md) · [GOVERNANCE.md](GOVERNANCE.md).

## Datos e interoperabilidad

| Recurso | Función |
|---|---|
| `data/entries.csv` | capa maestra con evidencia y overlays editoriales |
| `data/diplomatic/` | transcripciones diplomáticas IA-asistidas |
| `data/review/` | manifiestos de cotejo documental |
| `data/validation/` | incertidumbre, recotejo PHIL y colas de revisión |
| `data/research/` | concordancias, variantes, pruebas y relaciones derivadas |
| CSV / JSON / XML / SQLite | serializaciones reproducibles |
| TEI RHD | representación rica del modelo documental |
| TEI Lex-0 | proyección lexicográfica estricta e interoperable |
| IIIF Presentation 3 | localización del testimonio y enlaces registro→Canvas |
| `schemas/` | contratos de datos y validación estructural |
| `source_profiles/` | configuración específica de cada fuente histórica |

La separación entre **núcleo reusable** y **perfil de fuente** permite aplicar RHD a otros testimonios sin rediseñar la arquitectura universal. La replicación sobre Tellechea 1826 constituye la primera prueba de esa portabilidad.

## Reproducibilidad y ciencia abierta

La generación de artefactos está automatizada mediante scripts versionados y pruebas de invariantes. Los checksums del testimonio, manifiestos de integridad y documentación de procedencia permiten verificar que un resultado corresponda al estado que declara.

Consulte [REPRODUCIBILITY.md](REPRODUCIBILITY.md), [FAIR_ASSESSMENT.md](FAIR_ASSESSMENT.md) y `sources/checksums.json`. RHD aplica principios FAIR para datos y FAIR4RS para software de investigación, con metadatos en [`CITATION.cff`](CITATION.cff) y [`codemeta.json`](codemeta.json).

El snapshot público vigente está preservado en Zenodo. El **Concept DOI** del proyecto es [`10.5281/zenodo.21957212`](https://doi.org/10.5281/zenodo.21957212) y el DOI específico de **v1.0.1** es [`10.5281/zenodo.21958018`](https://doi.org/10.5281/zenodo.21958018).

## Citación

GitHub puede generar una cita desde [`CITATION.cff`](CITATION.cff). Para citar exactamente la versión pública vigente:

> Sandoval Gutierrez, Fernando. 2026. *Rarámuri Histórico Digital — Corpus Steffel 1791/1809*, versión 1.0.1. Zenodo. https://doi.org/10.5281/zenodo.21958018

Para enlazar el proyecto y todas sus versiones, utilice el Concept DOI: [`10.5281/zenodo.21957212`](https://doi.org/10.5281/zenodo.21957212).

Cuando un argumento dependa de una lectura del documento histórico, cite además **Steffel 1809** y la página correspondiente. Esta doble citación mantiene separadas la autoría histórica y la responsabilidad editorial/computacional de RHD.

## Licencias y derechos

- **Software y código original:** [MIT](LICENSE).
- **Datos, metadatos, anotaciones, traducciones y capas editoriales originales de RHD:** [CC BY 4.0](DATA_LICENSE.md).
- **Fuente histórica y materiales de terceros:** conservan su propio estatus jurídico y deben citarse según su procedencia.

La licencia de RHD no crea derechos sobre la obra de Steffel ni sobre ediciones contemporáneas de terceros.

## Ecosistema científico

RHD forma parte de un conjunto de proyectos conectados y mantiene las responsabilidades de cada uno separadas:

| Recurso | Relación con RHD |
|---|---|
| [Rarámuri Digital](https://github.com/fersandovalgtz/raramuri-digital) · [sitio](https://raramuri.ceees.mx) | infraestructura lexicográfica contemporánea hermana; las relaciones históricas permanecen tipadas y revisables |
| [Rarámuri · recursos educativos](https://github.com/fersandovalgtz/raramuri-recursos-educativos) | capa pedagógica independiente del corpus científico |
| [Libro de Texto Mexicano Digital](https://github.com/fersandovalgtz/libro-texto-mexicano-digital) | proyecto hermano de patrimonio documental y humanidades digitales |
| [Historia de la educación en Chihuahua](https://github.com/fersandovalgtz/historia-educacion-chihuahua) | investigación histórica y archivo digital dentro del mismo ecosistema de ciencia abierta |
| [Recursos educativos abiertos](https://github.com/fersandovalgtz/recursos-educativos-abiertos) | curación y reutilización educativa |
| [Perfil científico en GitHub](https://github.com/fersandovalgtz) | puerta de entrada al conjunto de proyectos abiertos |
| [Sitio público de RHD](https://fersandovalgtz.github.io/raramuri-historico/) | interfaz de consulta y divulgación del corpus |

→ [Mapa ampliado del ecosistema](docs/ECOSYSTEM.md)

## Autor y perfiles académicos

**Dr. Fernando Sandoval Gutierrez**  
ORCID: [0000-0002-3168-6725](https://orcid.org/0000-0002-3168-6725)  
Correo institucional: [fernando.sandoval@uacj.mx](mailto:fernando.sandoval@uacj.mx)  
Universidad Autónoma de Ciudad Juárez · Universidad CEEES / CEEES Cuauhtémoc · Cuerpo Académico UACJ-113

Perfiles: [GitHub](https://github.com/fersandovalgtz) · [Google Scholar](https://scholar.google.com/citations?user=zNZsYYAAAAAJ&hl=es) · [CATHI-UACJ](https://cathi.uacj.mx/handle/20.500.11961/3028/browse?authority=0000-0002-3168-6725&type=author) · [ResearchGate](https://www.researchgate.net/profile/Fernando-Sandoval-Gutierrez) · [ResearchID](https://researchid.co/fersandovalg) · [Academia.edu](https://uacj.academia.edu/FernandoSandoval)

## Contribuir

Las contribuciones documentales, filológicas, lingüísticas, históricas y técnicas son bienvenidas cuando aumentan la evidencia sin borrar la procedencia. Consulte [CONTRIBUTING.md](CONTRIBUTING.md), [GOVERNANCE.md](GOVERNANCE.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) y [SECURITY.md](SECURITY.md).

---

**RHD 1.0.1 preserva el documento histórico, la incertidumbre y el proceso de transformación como partes inseparables del objeto científico.**