# Roadmap — Rarámuri Histórico Digital

## Estado de referencia — RHD 1.0.1

RHD 1.0.1 es la versión pública archivada de referencia del Corpus Steffel 1791/1809. Conserva el corpus científico fijado en 1.0.0 y añade documentación, metadatos, citación, descubribilidad y articulación del ecosistema.

La fase documental machine-only está cerrada dentro de su alcance: cobertura, transcripción diplomática IA-asistida, incertidumbre terminal explícita, anexos, TEI/TEI Lex-0, IIIF, procedencia y replicación sobre Tellechea 1826. El trabajo futuro no consiste en «terminar Steffel» mediante más inferencia automática, sino en mejorar preservación, revisión humana independiente, reutilización de la infraestructura y producción científica derivada.

## Preservación persistente — completada

- Concept DOI del proyecto: **10.5281/zenodo.21957212**.
- DOI de la versión archivada v1.0.1: **10.5281/zenodo.21958018**.
- GitHub permanece como espacio vivo de desarrollo; Zenodo funciona como snapshot persistente citable.
- CFF, CodeMeta, README y sitio público deben mantener sincronizados release, DOI, licencias y límites epistemológicos.

No deben alterarse retrospectivamente tags/releases ya publicados para corregir documentación posterior.

## Prioridad A — revisión humana independiente

La release 1.0.1 permanece válida dentro de su alcance machine-only. Una capa humana futura será una **extensión versionada**, no una corrección silenciosa del pasado.

Orden recomendado:

1. 46 casos `unresolved_after_ai_recollation`;
2. 152 `corrected_ai_assisted`;
3. muestra o revisión completa de 284 `confirmed_ai_assisted` según disponibilidad de especialistas;
4. revisión de relaciones diacrónicas prioritarias con competencia lingüística/histórica pertinente.

Toda adjudicación humana debe registrar persona, fecha, alcance, evidencia, decisión y relación con el estado previo. No se permitirá promover registros por lote a `human_verified` sin evidencia individual o protocolo explícito.

## Prioridad B — RHD como infraestructura reusable

- Mantener estable el núcleo RHD 1.x y versionar contratos de datos semánticamente.
- Conservar perfiles de fuente separados del núcleo reusable.
- Publicar ejemplos mínimos y fixtures para que terceros puedan implementar nuevos adaptadores.
- Formalizar PROV-O cuando aporte interoperabilidad real.
- Mantener hashes, manifiestos y relaciones release→fuente→pipeline→outputs.
- Mantener TEI RHD rica y TEI Lex-0 estricta como productos distintos.
- Mantener IIIF Presentation 3 como capa de localización documental.
- Evaluar RO-Crate y Software Heritage cuando añadan preservación/interoperabilidad sin duplicación improductiva.

## Prioridad C — segunda y siguientes fuentes históricas

Tellechea 1826 ya demostró que el núcleo puede reutilizarse sin rediseño fundamental. El siguiente objetivo es convertir esa demostración en una colección histórica sostenible.

Cada nueva fuente debe tener perfil propio, referencia bibliográfica y testimonio identificable, calibración documental específica, reutilización del núcleo de IDs/capas/procedencia/incertidumbre/revisión/exportadores, y métricas que distingan infraestructura compartida de código específico de fuente.

## Prioridad D — integración controlada con Rarámuri Digital

RHD y Rarámuri Digital seguirán siendo repositorios independientes.

- Mantener relaciones Steffel ↔ Rarámuri Digital como objetos tipados y revisables.
- Publicar identificadores recíprocos cuando sean estables.
- Evitar la fusión automática de lemas históricos y contemporáneos.
- Distinguir coincidencia gráfica, apoyo documental, hipótesis diacrónica, revisión humana e interpretación lingüística.
- Desarrollar visualizaciones de continuidad/cambio que hagan visible la incertidumbre y la procedencia.

Véase `docs/ECOSYSTEM.md`.

## Prioridad E — publicación científica

RHD permite producir al menos dos objetos académicos diferenciados: un **data paper / scholarly dataset paper** sobre fuente, modelo, cobertura, procedencia, formatos, validaciones técnicas, límites y DOI; y un **artículo metodológico** sobre RHD como modelo generalizable de edición histórico-digital IA-asistida con preservación de incertidumbre, demostrando portabilidad con Steffel y Tellechea.

Ambos productos deben citar el software/dataset archivado y no reemplazar su citación.

## Prioridad F — preservación, descubribilidad y calidad

- Mantener Zenodo como archivo versionado y DOI persistente.
- Integrar el registro en ORCID y perfiles académicos pertinentes.
- Mantener CFF y CodeMeta sincronizados.
- Evaluar archivado del software en Software Heritage.
- Mantener enlaces recíprocos desde Rarámuri Digital, perfil científico, sitios institucionales y repositorios relacionados.
- Revisar periódicamente enlaces externos y documentación de fuente.
- Mantener CI de datos y una segunda capa CI para metadatos/documentación pública.

## Prioridad G — gobernanza y sostenibilidad

- Aplicar `GOVERNANCE.md` a decisiones editoriales y técnicas.
- Mantener `CONTRIBUTING.md` orientado a contribuciones con evidencia.
- Usar issues/PRs como registro público de cambios no sensibles.
- Separar seguridad de debate científico mediante `SECURITY.md`.
- Registrar cambios relevantes en `CHANGELOG.md`.
- Mantener roles CRediT y atribución explícita en `CONTRIBUTORS.md`.

## Criterios para una futura 1.1.0

Una 1.1.0 debe representar una **adición compatible y científicamente significativa**: revisión humana documentada, una nueva capa interoperable verificable, incorporación estable de una nueva fuente, o nuevas herramientas de consulta que no reescriban retrospectivamente las afirmaciones de 1.0.x.

Los cambios incompatibles del núcleo deben reservarse para una versión mayor.

## Lo que RHD no debe hacer

- reescribir retrospectivamente releases publicadas;
- confundir mejora de interfaz con nueva evidencia científica;
- declarar validación humana por inferencia o automatización;
- borrar incertidumbres para elevar una métrica de completitud;
- fusionar datos históricos y contemporáneos sin relación tipada;
- fabricar DOI, autorías, revisiones o procedencias;
- duplicar metadatos sin una fuente de verdad clara.

La prioridad posterior a 1.0 es hacer más durable, citable, reusable y científicamente inteligible lo ya construido, y después escalarlo con control de evidencia.
