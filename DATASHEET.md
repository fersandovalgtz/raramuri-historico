# Datasheet — Rarámuri Histórico Digital / Corpus Steffel 1791/1809

## Identificación

**Nombre:** Rarámuri Histórico Digital — Corpus Steffel 1791/1809  
**Versión canónica:** 1.0.0  
**Fecha de release:** 15 de agosto de 2026  
**Responsable:** Fernando Sandoval Gutierrez  
**ORCID:** 0000-0002-3168-6725  
**Repositorio:** https://github.com/fersandovalgtz/raramuri-historico  
**Sitio:** https://raramuri-historico.pages.dev  
**Tipo de recurso:** dataset de investigación + edición histórico-digital + software/pipeline de investigación.

## Fuente histórica

La colección de referencia deriva del *Tarahumarisches Wörterbuch* de Matthäus Steffel, publicado en 1809 dentro del volumen I de la compilación de Christoph Gottlieb von Murr. La contribución ocupa las pp. 293–374; el cuerpo lexicográfico comienza en la p. 301, invierte su dirección dentro de la p. 353 y es seguido por materiales anexos hasta la p. 374. Véase `docs/STEFFEL_SOURCE.md`.

**Lenguas de la fuente:** alemán y rarámuri/tarahumara; los materiales finales incluyen latín.  
**Páginas facsimilares del testimonio de trabajo:** 84.  
**Procedencia técnica:** `PROVENANCE.md` y `sources/checksums.json`.

## Composición de RHD 1.0.0

| Componente | Cantidad / estado |
|---|---:|
| Candidatos documentales cotejados | 2,495 / 2,495 |
| Artículos activos | 1,965 |
| Falsos límites preservados | 530 |
| Transcripciones diplomáticas IA-asistidas | 1,965 / 1,965 |
| Casos PHIL terminales | 482 |
| `confirmed_ai_assisted` | 284 |
| `corrected_ai_assisted` | 152 |
| `unresolved_after_ai_recollation` | 46 |
| Relaciones diacrónicas | 298 `candidate` |
| IIIF Canvases | 84 |
| Enlaces registro→Canvas | 1,965 |

Los conteos describen el snapshot `v1.0.0`; no deben extrapolarse automáticamente a futuras versiones.

## Cómo se construyó

El pipeline combina OCR de fuente, segmentación de alta cobertura, cotejo facsimilar IA-asistido, reconstrucción documental, transcripción diplomática, triage de incertidumbre, recotejo PHIL y generación de capas derivadas. Los manifiestos de revisión se conservan como evidencia append-only. Las transformaciones no deben sobrescribir silenciosamente la capa documental previa.

## Validación y estado epistemológico

La release 1.0.0 adopta un alcance **machine-only**. Todo el corpus activo tiene cobertura documental IA-asistida dentro de ese alcance, pero **no se afirma validación filológica o lingüística humana independiente**.

Los 46 casos `unresolved_after_ai_recollation` son incertidumbres terminales explícitas de la fase machine-only. Los 152 `corrected_ai_assisted` son propuestas documentales IA-asistidas y los 284 `confirmed_ai_assisted` sostienen una lectura previa dentro de la misma clase de autoridad. Ninguna de esas clases equivale a `human_verified`.

## Usos previstos

- historia de la lengua y de la lexicografía;
- historiografía lingüística;
- humanidades digitales y edición documental;
- análisis de la microestructura lexicográfica;
- estudios de circulación histórica del conocimiento;
- comparación diacrónica **como generación de hipótesis**;
- enseñanza de métodos de ciencia abierta, edición digital y reproducibilidad;
- desarrollo y evaluación de modelos de datos para fuentes históricas.

## Usos no previstos o de alto riesgo interpretativo

- usar el OCR o una salida IA-asistida como transcripción autorizada sin atender su estado;
- presentar las formas históricas de Steffel como norma del rarámuri contemporáneo;
- inferir por coincidencia gráfica identidad semántica, cognación o continuidad histórica;
- usar el corpus como sustituto de conocimiento lingüístico o cultural de comunidades rarámuri actuales;
- borrar las atribuciones históricas de expresiones etnográficas o juicios presentes en la fuente;
- atribuir a revisión humana resultados que no la han recibido.

## Formatos

CSV, JSON, XML, SQLite, TEI RHD, TEI Lex-0, JSON Schema e IIIF Presentation 3, además de documentación y manifiestos de procedencia/revisión.

## Licencias

- software/código original: MIT;
- datos, metadatos, anotaciones, traducciones y capas editoriales originales de RHD: CC BY 4.0;
- fuente histórica y materiales de terceros: conforme a su propio estatus jurídico y procedencia.

Véase `DATA_LICENSE.md`.

## Sesgos y limitaciones

La fuente es un documento histórico producido por un misionero europeo del siglo XVIII y refleja las categorías, intereses, ortografías y relaciones coloniales de su contexto. La digitalización añade otra capa de mediación: calidad facsimilar, OCR, segmentación y decisiones computacionales. RHD intenta hacer visibles esas mediaciones en vez de ocultarlas.

La cobertura completa de la fase machine-only no convierte el corpus en una edición crítica humana definitiva. La ausencia de revisión humana independiente debe conservarse como metadato relevante para cualquier reutilización.

## Mantenimiento y versionado

`v1.0.0` es la implementación de referencia estable. Las modificaciones futuras que cambien datos científicos deberán quedar documentadas en `CHANGELOG.md`, asociadas a una nueva versión y ser reproducibles. El DOI de la release 1.0.0 se incorporará sólo después de verificar el depósito persistente correspondiente.
