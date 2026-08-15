# Preparación de release científico RHD 1.0 — Steffel

**Corte:** 15 de agosto de 2026  
**Estado:** prerelease científico; no declarar 1.0 final todavía.

## Gates que ya están satisfechos

### G1. Cobertura documental del cuerpo lexicográfico

- 2,495 candidatos con disposición editorial IA-asistida.
- 1,965 artículos activos.
- 530 falsos límites conservados como historia de extracción.
- 1,965 transcripciones diplomáticas IA-asistidas.
- Ningún lote automático de frontera o recotejo PHIL pendiente.

### G2. Modelo reusable

- Especificación RHD 1.0.
- JSON Schema canónico.
- Perfil Steffel separado del núcleo.
- Plantilla para fuentes futuras.
- Adaptador no destructivo `Steffel -> RHD canonical`.
- Procedencia explícita para OCR, segmentación, diplomática y PHIL.

### G3. Interoperabilidad lexicográfica mínima

- Edición TEI RHD rica separada de la proyección interoperable.
- Proyección TEI Lex-0 estricta.
- Validación automatizada contra el RNG oficial TEI Lex-0 0.9.5 en CI.
- Prohibición testada de fabricar `<def>` desde material no estructurado.

### G4. Preparación de revisión humana

- 482 problemas abiertos recotejados IA-asistidamente.
- Priorización 46 / 152 / 284.
- Paquetes independientes preparados con decisiones en blanco.
- Protocolo que separa evaluación filológica, lingüística, semántico-histórica y disciplinar.

### G5. Capa diacrónica no adjudicativa

- 298 candidatos representados como relaciones derivadas.
- Los estados permanecen `candidate`.
- No existe promoción automática a cognación, equivalencia semántica o continuidad histórica.

## Gates todavía abiertos

### G6. Revisión humana crítica — bloqueante

**Estado:** 0/482 revisados independientemente.

Requisito de cierre: definir el universo humano mínimo del release y completar la revisión de ese universo o mantener explícitamente los casos como irresolubles. Las decisiones adoptadas deben vivir en una capa crítica derivada y no sobrescribir la diplomática.

### G7. Apéndices — bloqueante para edición Steffel integral

Existe segmentación OCR candidata para numeración, 22 fórmulas trilingües y Padre Nuestro. Falta:

- cotejo facsimilar;
- transcripción diplomática;
- alineación de las tres lenguas;
- integración canónica y TEI.

### G8. IIIF — abierto

Existe modelo lógico y campos reservados. El repositorio Git no contiene la imagen/facsímil. Existe un ejemplar digital externo identificado como Internet Archive `tarahumarischesw00stef`; antes de fijarlo como dependencia de release deben verificarse el Manifest IIIF real, la correspondencia de páginas con el witness de trabajo y la estabilidad de las URIs.

### G9. Release/archivo — abierto

Antes de 1.0 final:

- actualizar `CHANGELOG.md`;
- fijar versión y commit;
- regenerar exportaciones/manifest de integridad;
- generar release GitHub;
- depositar dataset/software y obtener identificador persistente apropiado;
- registrar DOI/URI en `CITATION.cff` y documentación;
- comprobar archivo de software;
- publicar declaración de conformidad y limitaciones.

### G10. Replicabilidad externa — bloqueante para declarar el método industrializado

La plantilla reusable existe, pero se requiere una segunda fuente histórica real procesada de extremo a extremo. La prueba debe documentar:

- qué componentes se reutilizaron sin cambios;
- qué parámetros residieron sólo en el perfil de fuente;
- qué modificaciones al núcleo fueron realmente inevitables;
- si los IDs, procedencia, revisión, canonicalización y exportaciones funcionaron sin rediseño conceptual.

## Política de nomenclatura de releases

Hasta cerrar G6, G7, G8/G9 y G10, no se recomienda llamar al conjunto **RHD 1.0 final**. Pueden publicarse prereleases o versiones 0.x claramente etiquetadas, siempre declarando la cobertura documental alcanzada y las validaciones todavía pendientes.

## Criterio de decisión

El release 1.0 final no depende de alcanzar una apariencia de “100% de certeza lingüística”. Depende de que todas las afirmaciones publicadas tengan estado epistemológico, procedencia y alcance verificables, y de que la infraestructura haya demostrado ser reusable con otra fuente real.
