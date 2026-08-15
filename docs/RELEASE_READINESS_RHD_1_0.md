# Preparación de release científico RHD 1.0 — Steffel

**Corte:** 15 de agosto de 2026  
**Alcance:** edición histórico-digital computacional e IA-asistida, sin intervención humana de adjudicación.  
**Estado:** prerelease científico; no declarar 1.0 final todavía.  
**Avance ponderado vigente:** **90.0%**.

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

## Gates todavía abiertos o parcialmente abiertos

### G7. IIIF canónico — abierto, con controles externos activos

El witness canónico del proyecto es el facsímil de trabajo fijado por SHA-256 y registrado en `sources/external-references.json`. Su tramo final ya tiene mapeo interno reproducible `PDF 79–84 ↔ impreso 369–374`.

El Manifest IIIF Presentation 3 de Internet Archive `tarahumarischesw00stef` fue verificado automáticamente. La comparación perceptual contra huellas calculadas de las seis páginas locales mostró una divergencia fuerte, por lo que ese ítem permanece como **witness externo paralelo no canónico**.

Además se incorporó un segundo probe independiente para el ejemplar Getty/Internet Archive `gri_000133125012248650`. Su resultado se considera únicamente diagnóstico hasta que exista evidencia perceptual suficiente; ningún candidato externo puede ser promovido silenciosamente a witness canónico.

Para cerrar G7 hace falta publicar el facsímil checksum-fixed mediante un servicio IIIF estable controlado por el proyecto o localizar una representación externa cuya identidad con el escaneo de trabajo pueda demostrarse reproduciblemente. Después habrá que mapear el witness completo a Canvases y, cuando exista evidencia espacial, a regiones de entrada.

### G8. Release, integridad y archivo — parcialmente abierto

Ya están resueltos:

- `CHANGELOG` preparado para RHD 1.0 machine-only;
- generador determinista de manifiesto de integridad;
- recomputación automática de SHA-256, tamaños y conteos;
- incorporación al manifiesto de capas lexicales, canónicas, diacrónicas, TEI/Lex-0, anexos visuales, identidad de witnesses y perfiles de fuente;
- incorporación de los artefactos del piloto Tellechea al manifiesto de release;
- declaración de política machine-only;
- declaración explícita de conformidad de implementación.

Falta:

- actualizar `CITATION.cff` cuando se fije el identificador/versionado candidato definitivo;
- fijar versión y commit de release;
- generar release GitHub estable;
- depositar dataset/software y obtener identificador persistente apropiado;
- comprobar archivo de software/datos.

### G9. Replicabilidad externa — 40%, prueba mínima satisfecha; prueba fuerte pendiente

La segunda fuente piloto es **Miguel Joaquín Tellechea, _Compendio gramatical para la inteligencia del idioma tarahumar_ (1826)**. Es deliberadamente más exigente que otro diccionario porque combina gramática, ejemplos y materiales paralelos español–tarahumara.

El witness público DGB ya está fijado por checksum como `RHD-WIT-TELLECHEA-1826-DGB`: 205 páginas, 95,088,307 bytes y SHA-256 `c67b7942090613c494d8057be8aff59ea13a11519c29eae469afad8a85c30dfc`. La CI vuelve a descargarlo y falla si cambia su identidad.

La **prueba mínima end-to-end ya fue ejecutada realmente**. Dos unidades estructuralmente distintas recorren el mismo núcleo RHD:

- `RHD-T1826-00001`: página gramatical, PDF 32 / impreso 6, anclada por `LIBRO PRIMERO / CAPITULO I`;
- `RHD-T1826-00002`: página de disposición paralela, PDF 75 / impreso 49, con dos columnas separadas geométricamente y asignación lingüística conservadora como candidata, no como certeza.

Para ambas se preserva la capa textual embebida del PDF y se genera una lectura visual independiente mediante renderizado del facsímil + Tesseract. Las dos capas permanecen separadas; no se presenta OCR como validación humana ni se fabrican equivalencias semánticas. Los dos registros validan contra el JSON Schema RHD, `lexical` permanece `null`, y la exportación TEI representa unidades documentales sin coercionarlas a entradas Lex-0.

Los artefactos persistidos son:

- `data/pilot/tellechea-1826.minimal-pilot.jsonl`;
- `data/pilot/tellechea-1826.minimal-pilot.tei.xml`;
- `data/pilot/tellechea-1826.minimal-pilot.diagnostics.json`.

Esto justifica **40%** en la dimensión de replicación: la adquisición y la prueba mínima están resueltas, pero G9 no se cierra hasta extender el procedimiento al alcance completo declarado del witness de 205 páginas y producir un informe de impacto sobre el núcleo.

## Política de nomenclatura de releases

No se debe llamar al conjunto **“edición crítica humanamente validada”**. La designación correcta es **edición histórico-digital computacional / IA-asistida**.

El release RHD 1.0 final podrá cerrarse sin revisión humana cuando G7–G9 queden resueltos y todos los estados de incertidumbre sigan siendo explícitos, trazables y no destructivos.

## Criterio de decisión

El release 1.0 no exige una ficción de certeza total. Exige que cada afirmación tenga procedencia, método y estado epistemológico verificables; que los artefactos sean reproducibles e íntegros; y que el pipeline haya demostrado reutilización real sobre una segunda fuente histórica en el alcance completo declarado.
