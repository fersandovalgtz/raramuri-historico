# Preparación de release científico RHD 1.0 — Steffel

**Corte:** 15 de agosto de 2026  
**Alcance:** edición histórico-digital computacional e IA-asistida, sin intervención humana de adjudicación.  
**Estado:** prerelease científico; no declarar 1.0 final todavía.

La política de alcance vigente es `docs/MACHINE_ONLY_SCIENTIFIC_POLICY.md`. La ausencia de revisión humana no es un defecto pendiente del release: es una decisión metodológica explícita. Ningún artefacto puede presentar resultados IA-asistidos como `human_verified`.

## Gates ya satisfechos

### G1. Cobertura documental del cuerpo lexicográfico — cerrado

- 2,495 candidatos con disposición editorial IA-asistida.
- 1,965 artículos activos.
- 530 falsos límites conservados como historia de extracción.
- 1,965 transcripciones diplomáticas IA-asistidas.
- Ningún lote automático de frontera o recotejo PHIL pendiente.

### G2. Modelo reusable — cerrado

- Especificación RHD 1.0.
- JSON Schema canónico.
- Perfil Steffel separado del núcleo.
- Plantilla machine-only para fuentes futuras.
- Adaptador no destructivo `Steffel -> RHD canonical`.
- Procedencia explícita para OCR, segmentación, diplomática y PHIL.
- Pruebas que impiden que los perfiles reintroduzcan requisitos de adjudicación humana.

### G3. Interoperabilidad lexicográfica mínima — cerrado

- Edición TEI RHD rica separada de la proyección interoperable.
- Proyección TEI Lex-0 estricta.
- Validación automatizada contra el RNG oficial TEI Lex-0 0.9.5 en CI.
- Prohibición testada de fabricar `<def>` desde material no estructurado.
- Los anexos RHD permanecen fuera de la proyección Lex-0 estricta.
- Existe un suplemento TEI específico para anexos y texto paralelo.

### G4. Recotejo y contabilidad de incertidumbre sin intervención humana — cerrado

Los 482 problemas explícitos tienen estado computacional terminal y trazable:

- 284 `confirmed_ai_assisted`;
- 152 `corrected_ai_assisted`;
- 46 `unresolved_after_ai_recollation`.

`unresolved_after_ai_recollation` es un estado final legítimo dentro del alcance machine-only. La edición no debe forzar una lectura única donde la evidencia visual no la sostenga.

Los paquetes de revisión humana ya creados se conservan únicamente como artefactos históricos/opcionales; no pertenecen al camino crítico ni a la CI de release.

### G5. Capa diacrónica no adjudicativa — cerrada como infraestructura

- 298 candidatos representados como relaciones derivadas.
- Los estados permanecen `candidate`.
- Los 298 reciben una puntuación reproducible de apoyo documental de recuperación.
- Las pruebas impiden convertir esa puntuación en probabilidad de cognación, equivalencia semántica, etimología o continuidad histórica.

### G6. Apéndices y muestra paralela — cerrado para alcance machine-only

- detección estructural OCR del apéndice de numeración;
- cotejo visual IA de la frontera completa del apéndice;
- mapeo exacto `PDF 79–84 ↔ impreso 369–374`;
- sistema numeral estructurado computacionalmente, con confianza e incertidumbre por forma;
- 22 fórmulas identificadas, ordenadas y alineadas por IA en latín, alemán y tarahumara;
- 66 campos paralelos con nivel de confianza explícito;
- dos fórmulas conservan baja confianza en el campo tarahumara sin corrección conjetural;
- Padre Nuestro identificado como objeto independiente y transcrito visualmente por IA hasta `Amen.`;
- capa canónica de 24 objetos: 1 numeración + 22 fórmulas + 1 oración;
- suplemento TEI de anexos con responsabilidad no humana explícita;
- integración de los objetos en la infraestructura RHD sin contaminación de Lex-0.

Las lecturas visuales de baja confianza pueden permanecer como incertidumbre terminal; no se exige eliminarlas para cerrar este gate.

## Gates todavía abiertos

### G7. IIIF canónico — abierto, con control negativo ya resuelto

El witness canónico del proyecto es el facsímil de trabajo fijado por SHA-256 y registrado en `sources/external-references.json`. Su tramo final ya tiene mapeo interno reproducible `PDF 79–84 ↔ impreso 369–374`.

Se localizó y verificó automáticamente el Manifest IIIF Presentation 3 de Internet Archive `tarahumarischesw00stef`. Sin embargo, una comparación perceptual contra huellas calculadas de las seis páginas locales mostró una divergencia fuerte. Por tanto, ese ítem queda registrado como **witness externo paralelo no canónico**, no como sustituto del facsímil checksum-fixed.

La CI conserva este resultado como control negativo: verifica que el Manifest externo siga siendo usable y que no se promueva accidentalmente a evidencia canónica.

Para cerrar G7 todavía hace falta una de estas dos soluciones:

1. publicar el facsímil checksum-fixed mediante un servicio IIIF estable controlado por el proyecto; o
2. localizar un servicio externo cuya identidad con el escaneo de trabajo pueda demostrarse reproduciblemente.

Después habrá que mapear el witness completo a Canvases y, cuando exista evidencia espacial, a regiones de entrada.

### G8. Release, integridad y archivo — parcialmente abierto

Ya están resueltos:

- `CHANGELOG` preparado para RHD 1.0 machine-only;
- generador determinista de manifiesto de integridad;
- recomputación automática de SHA-256, tamaños y conteos;
- incorporación al manifiesto de capas lexicales, canónicas, diacrónicas, TEI/Lex-0, anexos visuales, identidad de witnesses y perfiles de fuente;
- declaración de política machine-only;
- declaración explícita de conformidad de implementación.

Falta:

- actualizar `CITATION.cff` cuando se fije el identificador/versionado candidato definitivo;
- fijar versión y commit de release;
- generar release GitHub estable;
- depositar dataset/software y obtener identificador persistente apropiado;
- comprobar archivo de software/datos.

### G9. Replicabilidad externa — Tellechea 1826 seleccionado, pero 0% end-to-end

La segunda fuente piloto seleccionada es **Miguel Joaquín Tellechea, _Compendio gramatical para la inteligencia del idioma tarahumar_ (1826)**. Es deliberadamente más exigente que otro diccionario: combina gramática, ejemplos y materiales paralelos español–tarahumara.

Ya existen:

- `source_profiles/tellechea-1826.pilot-candidate.json`;
- `docs/SECOND_SOURCE_PILOT_TELLECHEA_1826.md`;
- criterios machine-only de ingestión y éxito;
- pruebas que mantienen la dimensión en 0% mientras no exista ingestión real.

No se concede avance end-to-end por haber elegido o modelado la fuente. Para cerrar G9 debe fijarse por checksum un witness concreto y procesarse realmente mediante el mismo núcleo RHD, documentando:

- qué componentes se reutilizaron sin cambios;
- qué parámetros residieron sólo en el perfil;
- qué modificaciones al núcleo fueron realmente inevitables;
- si IDs, procedencia, canonicalización, texto paralelo y exportaciones funcionaron sin rediseño conceptual.

## Política de nomenclatura de releases

No se debe llamar al conjunto **“edición crítica humanamente validada”**. La designación correcta es **edición histórico-digital computacional / IA-asistida**.

El release RHD 1.0 final podrá cerrarse sin revisión humana cuando G7–G9 queden resueltos y todos los estados de incertidumbre sigan siendo explícitos, trazables y no destructivos.

## Criterio de decisión

El release 1.0 no exige una ficción de certeza total. Exige que cada afirmación tenga procedencia, método y estado epistemológico verificables; que los artefactos sean reproducibles e íntegros; y que el pipeline haya demostrado reutilización real sobre una segunda fuente histórica.
