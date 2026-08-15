# Roadmap — Rarámuri Histórico Digital

## Estado de referencia — RHD 1.0.0

RHD 1.0.0 fija el Corpus Steffel 1791/1809 como **implementación de referencia reusable** de una edición histórico-digital machine-only. La fase de construcción científica incluida en ese alcance está cerrada: cobertura documental, transcripción diplomática IA-asistida, estados terminales de incertidumbre, anexos, TEI/TEI Lex-0, IIIF, procedencia y prueba de replicación sobre Tellechea 1826.

El roadmap posterior a 1.0 ya no consiste en «terminar Steffel» mediante más inferencia automática. Se divide en preservación, revisión humana opcional, consolidación de la infraestructura reusable, nuevas fuentes y productos científicos derivados.

## Gate inmediato — archivo persistente de v1.0.0

**Prioridad máxima.**

- Depositar o verificar en Zenodo el snapshot exacto de `v1.0.0`.
- Comprobar correspondencia entre DOI, tag, commit `441cbac036d82e83451e32378a030c3bb0923bf6`, artefacto archivado y manifiesto de integridad.
- Registrar DOI de versión y, cuando corresponda, DOI conceptual.
- Propagar el identificador verificado a `CITATION.cff`, README, metadatos, perfil científico y sitio público.
- Conservar GitHub como espacio vivo de desarrollo y Zenodo como snapshot persistente citable.

Este gate no debe resolverse fabricando un DOI, reutilizando el de otro proyecto ni alterando retrospectivamente la release canónica.

## Línea A — revisión humana independiente

La release 1.0.0 permanece válida dentro de su alcance machine-only. Una capa humana futura será una **extensión versionada**, no una corrección silenciosa del pasado.

Orden sugerido:

1. 46 casos `unresolved_after_ai_recollation`;
2. 152 `corrected_ai_assisted`;
3. muestra o revisión completa de 284 `confirmed_ai_assisted` según disponibilidad de especialistas;
4. revisión de relaciones diacrónicas prioritarias con competencia lingüística/histórica pertinente.

Toda adjudicación humana debe registrar persona, fecha, alcance, evidencia, decisión y relación con el estado previo. No se permitirá promover registros por lote a `human_verified` sin evidencia individual o protocolo explícito.

## Línea B — RHD como infraestructura reusable

### Especificación y contratos

- Mantener estable el núcleo RHD 1.x.
- Versionar cambios de JSON Schema de manera semántica.
- Conservar perfiles de fuente separados del núcleo.
- Publicar ejemplos mínimos y fixtures que permitan a terceros implementar un nuevo adaptador.
- Documentar compatibilidad hacia atrás y política de deprecación.

### Procedencia

- Formalizar el mapeo de entidades, actividades y agentes a PROV-O donde aporte interoperabilidad real.
- Mantener hashes de fuentes y artefactos críticos.
- Exponer manifiestos legibles por máquina que conecten release, fuente, pipeline y outputs.

### Interfaces

- Mantener TEI RHD rica y TEI Lex-0 estricta como productos distintos.
- Mantener IIIF Presentation 3 como capa de localización documental.
- Publicar/estabilizar OpenAPI cuando exista un servicio de consulta que lo justifique.
- Evaluar RO-Crate para empaquetado de objetos de investigación cuando no duplique metadatos sin valor añadido.

## Línea C — segunda y siguientes fuentes históricas

Tellechea 1826 ya demostró que el núcleo puede reutilizarse sin rediseño fundamental. El siguiente objetivo es convertir esa demostración en una **colección histórica sostenible**.

Cada nueva fuente debe:

- tener perfil de fuente propio;
- conservar referencia bibliográfica y testimonio identificable;
- calibrar segmentación según su materialidad;
- reutilizar IDs, capas, procedencia, incertidumbre, revisión y exportadores del núcleo;
- documentar cualquier modificación requerida al estándar RHD;
- producir métricas que distingan infraestructura reutilizada de código específico de la fuente.

El éxito no se mide por volumen de OCR procesado, sino por la capacidad de incorporar fuentes heterogéneas sin degradar procedencia, evidencia ni reproducibilidad.

## Línea D — integración con Rarámuri Digital

RHD y Rarámuri Digital seguirán siendo repositorios independientes.

- Mantener relaciones Steffel ↔ Rarámuri Digital como objetos tipados y revisables.
- Publicar identificadores recíprocos cuando sean estables.
- Evitar la fusión automática de lemas históricos y contemporáneos.
- Distinguir coincidencia gráfica, apoyo documental, hipótesis diacrónica, revisión humana y eventual interpretación lingüística.
- Desarrollar visualizaciones de continuidad/cambio que muestren incertidumbre y procedencia.

Véase `docs/ECOSYSTEM.md`.

## Línea E — publicación científica

RHD 1.0 permite producir al menos dos objetos académicos diferenciados:

### Data paper / scholarly dataset paper

Debe describir:

- fuente histórica y relevancia;
- modelo de datos;
- metodología de extracción y revisión;
- métricas de cobertura;
- procedencia y control de incertidumbre;
- formatos y estándares;
- validaciones técnicas;
- límites epistemológicos y usos recomendados;
- DOI de la release archivada.

### Artículo metodológico

Debe argumentar RHD como modelo generalizable de edición histórico-digital IA-asistida con preservación de incertidumbre y demostrar su replicabilidad mediante Steffel y Tellechea.

Los dos productos deben citar el dataset/software, no reemplazar su citación.

## Línea F — preservación y descubribilidad

- Zenodo para DOI y snapshot versionado.
- ORCID para identidad y descubrimiento académico.
- CodeMeta y CFF como metadatos legibles por máquina.
- Evaluar archivado en Software Heritage para el componente de software.
- Mantener enlaces desde el perfil científico, CEEES, Rarámuri Digital y otros repositorios relacionados.
- Revisar periódicamente enlaces externos y documentación de la fuente.

## Línea G — gobernanza y sostenibilidad

- Aplicar `GOVERNANCE.md` para decisiones editoriales y técnicas.
- Mantener `CONTRIBUTING.md` orientado a contribuciones con evidencia.
- Usar issues/PRs como registro público de cambios no sensibles.
- Separar problemas de seguridad de debates científicos mediante `SECURITY.md`.
- Registrar cambios relevantes en `CHANGELOG.md`.

## Criterios para una futura 1.1.0

Una versión 1.1.0 deberá representar una **adición compatible y científicamente significativa**, por ejemplo:

- DOI y metadatos persistentes plenamente integrados;
- nuevas capas documentales/revisión humana sin romper el esquema 1.0;
- mejoras interoperables verificables;
- incorporación estable de una nueva fuente con cambios compatibles;
- nuevas herramientas de consulta que no alteren las afirmaciones científicas de v1.0.0.

Los cambios incompatibles del núcleo deberán reservarse para una versión mayor.

## Lo que RHD no debe hacer

- reescribir retrospectivamente `v1.0.0`;
- confundir mejora de interfaz con nueva evidencia científica;
- declarar validación humana por inferencia o automatización;
- borrar incertidumbres para elevar una métrica de «completitud»;
- fusionar datos históricos y contemporáneos sin relación tipada;
- duplicar información de metadatos en múltiples archivos sin una fuente de verdad clara.

La prioridad posterior a 1.0 es **hacer más durable, citable, reusable y científicamente inteligible lo que ya se construyó**, y después escalarlo a nuevas fuentes.
