# Roadmap

## Estado de referencia — 15 de agosto de 2026

El Corpus Steffel 1791/1809 ya superó la fase de bootstrap documental. La versión 0.2.0 dispone de cobertura integral IA-asistida del cuerpo lexicográfico: 2,495 candidatos cotejados, 1,965 artículos activos, 1,965 transcripciones diplomáticas y 482 problemas explícitos recotejados mediante la serie RHD-PHIL. La fase automática general de recotejo está agotada; la validación humana independiente permanece abierta.

El siguiente objetivo estratégico es convertir Steffel en la **implementación de referencia de RHD 1.0**, de modo que la arquitectura pueda reutilizarse para nuevas fuentes históricas sin rediseño fundamental.

## 0.2 — Cobertura documental integral — alcanzada en fase IA-asistida

- Segmentación de alta cobertura del cuerpo lexicográfico.
- Cotejo de 2,495 candidatos.
- 1,965 artículos activos y 530 falsos límites rechazados.
- Transcripción diplomática IA-asistida completa de los artículos activos.
- 482 problemas abiertos identificados y recotejados.
- Manifiestos append-only y métricas reproducibles.

Este hito no equivale a edición crítica ni a validación humana/lingüística.

## 0.3 — Validación humana y anexos — en curso / pendiente

### Validación

- Comenzar por los 46 casos `unresolved_after_ai_recollation`.
- Continuar con 152 propuestas `corrected_ai_assisted`.
- Revisar después 284 `confirmed_ai_assisted` según alcance filológico, lingüístico, semántico/histórico o disciplinar.
- Adoptar futuras lecturas críticas en una capa derivada sin sobrescribir la diplomática.

### Anexos

- Estructurar el apéndice sobre numeración.
- Estructurar la muestra lingüística final latín–alemán–rarámuri.
- Mantener identificadores, página y procedencia compatibles con el núcleo RHD.

## 0.4 — RHD 1.0: arquitectura reusable — iniciada

- Congelar la especificación del núcleo reusable.
- Mantener un perfil de fuente independiente para Steffel.
- Mapear `data/entries.csv` al modelo canónico sin migración destructiva.
- Implementar JSON canónico validado mediante JSON Schema.
- Introducir objetos explícitos de procedencia y actividad mapeables a PROV-O.
- Preparar localización facsimilar compatible con IIIF Presentation 3.0.
- Mantener pruebas de invariantes y conteos durante la transición.

Documentos de trabajo:

- `docs/RHD_1_0_SPECIFICATION.md`
- `docs/RHD_1_0_EDITORIAL_PROTOCOL.md`
- `docs/STEFFEL_TO_RHD_1_0_MAPPING.md`
- `schemas/rhd-entry-1.0.schema.json`
- `source_profiles/steffel-1809.source.json`

## 0.5 — Interoperabilidad lexicográfica

- Reescribir el exportador TEI sobre la capa canónica RHD 1.0.
- Evitar el mapeo automático de `definition_raw` a `<def>` cuando la estructura documental no lo justifique.
- Distinguir glosa fuente, traducción editorial y comentario.
- Generar y validar TEI P5 conforme al perfil TEI Lex-0 adoptado.
- Evaluar CLDF Dictionary para proyecciones lingüísticas que cuenten con validación suficiente.
- Publicar OpenAPI y manifiestos de integridad.
- Implementar IIIF Manifest/Canvas y, donde sea posible, regiones de entrada.

## 0.6 — Capa diacrónica revisable

- Mantener candidatos Steffel ↔ Rarámuri Digital como relaciones, no fusiones.
- Conservar método, evidencia y controles negativos.
- Añadir eventos de revisión humana a relaciones prioritarias.
- Desarrollar visualizaciones de continuidad/cambio sin promover automáticamente cognación o ley fonológica.

## 0.7 — Segunda fuente piloto

La prueba real de RHD 1.0 será incorporar una segunda fuente sin alterar el núcleo. La nueva colección deberá:

1. crear su perfil de fuente;
2. calibrar segmentación sobre casos diversos;
3. reutilizar identificadores, capas, procedencia, incertidumbre, revisión y exportadores;
4. documentar cualquier cambio que revele una limitación genuina del núcleo RHD.

El éxito se medirá por la proporción de infraestructura reutilizada, no por velocidad de extracción aislada.

## 1.0 — Edición digital de investigación y plataforma reusable

Criterios propuestos:

- especificación RHD 1.0 estable;
- Steffel documentado como implementación de referencia;
- pipeline reusable probado al menos con una segunda fuente;
- TEI validado y generación reproducible;
- procedencia e integridad publicadas;
- mecanismo operativo de revisión/contribución humana;
- DOI y release versionado;
- depósito en Zenodo y archivado de software;
- documentación pública estable;
- declaración explícita de cobertura y límites epistemológicos.

RHD 1.0 no significará que toda afirmación lingüística esté validada, sino que la infraestructura editorial, la procedencia y los estados de revisión estén formalizados y sean reproducibles.
