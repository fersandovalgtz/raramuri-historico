# Preparación de release científico RHD 1.0 — Steffel

**Corte:** 15 de agosto de 2026  
**Alcance:** edición histórico-digital computacional e IA-asistida, sin intervención humana de adjudicación.  
**Estado:** prerelease científico; no declarar 1.0 final todavía.  
**Avance ponderado vigente:** **93.0%**.

La política de alcance vigente es `docs/MACHINE_ONLY_SCIENTIFIC_POLICY.md`. La ausencia de revisión humana no es un defecto pendiente del release: es una decisión metodológica explícita. Ningún artefacto puede presentar resultados IA-asistidos como `human_verified`.

## Gates cerrados

### G1. Cobertura documental del cuerpo lexicográfico — cerrado

- 2,495 candidatos con disposición editorial IA-asistida.
- 1,965 artículos activos.
- 530 falsos límites conservados como historia de extracción.
- 1,965 transcripciones diplomáticas IA-asistidas.
- Ningún lote automático de frontera o recotejo PHIL pendiente.

### G2. Modelo reusable — cerrado

- especificación RHD 1.0;
- JSON Schema canónico;
- perfil Steffel separado del núcleo;
- plantilla machine-only para fuentes futuras;
- adaptador no destructivo `Steffel -> RHD canonical`;
- procedencia explícita para OCR, segmentación, diplomática y PHIL;
- pruebas que impiden que los perfiles reintroduzcan requisitos de adjudicación humana.

### G3. Interoperabilidad lexicográfica — cerrado salvo gate IIIF independiente

- TEI RHD rica separada de la proyección interoperable;
- TEI Lex-0 estricta;
- validación automatizada contra el RNG oficial TEI Lex-0 0.9.5;
- prohibición testada de fabricar `<def>` desde material no estructurado;
- suplemento TEI específico para anexos y texto paralelo;
- anexos fuera de la proyección Lex-0 estricta.

### G4. Recotejo y contabilidad de incertidumbre — cerrado

Los 482 problemas explícitos tienen estado computacional terminal y trazable:

- 284 `confirmed_ai_assisted`;
- 152 `corrected_ai_assisted`;
- 46 `unresolved_after_ai_recollation`.

`unresolved_after_ai_recollation` es un estado final legítimo dentro del alcance machine-only. La edición no fuerza una lectura única donde la evidencia visual no la sostenga.

### G5. Capa diacrónica — infraestructura cerrada; calibración final en CI

- 298 relaciones Steffel ↔ Rarámuri Digital representadas como `candidate`;
- 298 puntuaciones reproducibles de apoyo documental de recuperación;
- calibración añadida contra **5,066 controles nulos deterministas** obtenidos mediante 17 desplazamientos circulares del mismo inventario moderno;
- informe científico machine-only reproducible añadido al pipeline;
- semántica, cognación, etimología, ley fonética y continuidad histórica permanecen explícitamente no adjudicadas.

La calibración mide únicamente **especificidad grafémica de recuperación** frente a emparejamientos rotos. No convierte un candidato en cognado ni en relación histórica confirmada.

### G6. Apéndices y muestra paralela — científicamente cerrados en alcance machine-only

- mapeo reproducible `PDF 79–84 ↔ impreso 369–374`;
- 24 objetos canónicos: 1 numeración + 22 fórmulas + 1 Padre Nuestro;
- sistema numeral estructurado computacionalmente;
- 22 fórmulas alineadas por IA en latín, alemán y tarahumara;
- 66 campos paralelos con confianza explícita;
- Padre Nuestro separado y transcrito visualmente hasta `Amen.`;
- suplemento TEI específico;
- registro formal de **incertidumbre terminal machine-only** para todas las lecturas medias/bajas.

Las lecturas no seguras se conservan como evidencia incierta; no son reparadas por conjetura y no bloquean el cierre machine-only.

### G9. Replicabilidad externa / industrialización — cerrado

La segunda fuente es **Miguel Joaquín Tellechea, _Compendio gramatical para la inteligencia del idioma tarahumar_ (1826)**. Su witness público DGB está fijado como `RHD-WIT-TELLECHEA-1826-DGB`:

- 205 páginas;
- 95,088,307 bytes;
- SHA-256 `c67b7942090613c494d8057be8aff59ea13a11519c29eae469afad8a85c30dfc`.

Después de la prueba mínima de dos unidades estructuralmente distintas, el pipeline procesa ahora **205/205 páginas** del witness completo. Cada página recibe una unidad documental RHD determinista; se preserva la capa textual fuente; las páginas escasas reciben OCR visual separado; los 205 objetos validan contra el mismo JSON Schema; y se genera TEI documental completa.

El resultado de la prueba fuerte es:

- **0 rediseños del núcleo universal**;
- **0 entradas Lex-0 fabricadas**;
- **0 atribuciones de validación humana**;
- artefacto CI reproducible del witness completo.

Por ello G9 queda **cerrado al 100%**. Esta prueba demuestra industrialización computacional del núcleo RHD sobre una fuente histórica completa y estructuralmente distinta; no declara una edición crítica humana de Tellechea.

## Gates todavía abiertos o condicionados

### G7. IIIF canónico — abierto

El witness Steffel canónico permanece fijado internamente como un PDF de **84 páginas, 6,251,443 bytes y SHA-256 `4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f`**.

Los proveedores externos se tratan como witnesses o diagnósticos, nunca como autoridades automáticas. El ítem Internet Archive `tarahumarischesw00stef` mostró divergencia perceptual fuerte y permanece como witness paralelo no canónico. El candidato Getty/Internet Archive continúa sujeto a probe independiente.

El enlace Dropbox del Repositorio de Lenguas demostró ser **mutable**: una ejecución posterior recuperó desde la misma URL un PDF de 438 páginas, 26,702,093 bytes y SHA-256 `3c2169d818770fecff7eca822c7dcc52f35d66356c5279913d85fb5364c652ce`. Por ello no puede considerarse dependencia canónica. La CI conserva el diagnóstico checksum-first pero ya no permite que la deriva de un proveedor externo bloquee los productos científicos checksum-fixed.

Para cerrar G7 hace falta publicar una representación IIIF Presentation 3 estable derivada del witness exacto checksum-fixed, con 84 Canvases y enlace página/Canvas para los registros RHD. Las regiones espaciales sólo se incorporarán donde exista evidencia; no se fabricarán coordenadas.

### G8. Release, integridad y archivo — parcialmente abierto

Ya están resueltos:

- `CHANGELOG.md` preparado;
- `CITATION.cff` preparado como `0.9.0-machine-only-prerelease`;
- generador determinista de manifiesto de integridad;
- recomputación automática de SHA-256, tamaños y conteos;
- incorporación de capas lexicales, canónicas, TEI/Lex-0, anexos, Tellechea completo, calibración diacrónica y registro de incertidumbre terminal;
- IIIF desacoplado como gate opcional hasta que exista realmente;
- política y declaración de conformidad machine-only.

Falta para **1.0 final**:

- cerrar G7 IIIF canónico;
- fijar commit/tag final;
- publicar GitHub Release estable;
- depositar datos/software en archivo persistente y fijar identificador citable;
- verificar que la copia archivada corresponde al manifiesto de integridad.

## Recalibración de terminación

La métrica oficial permanece **93.0% / 7.0%** mientras la nueva CI no haya validado conjuntamente:

1. registro terminal de incertidumbre del apéndice;
2. calibración de las 298 relaciones contra 5,066 controles nulos;
3. informe científico diacrónico reproducible;
4. manifiesto de prerelease con IIIF tratado correctamente como gate independiente.

Una vez verdes esos cuatro controles, se recalcularán las dimensiones de investigación diacrónica, apéndices y release. No se acreditará avance por documentación sola: el incremento requiere pruebas automáticas exitosas.

## Política de nomenclatura

No se debe llamar al conjunto **“edición crítica humanamente validada”**. La designación correcta es **edición histórico-digital computacional / IA-asistida, machine-only**.

El release RHD 1.0 final puede cerrarse sin revisión humana. El requisito es que toda incertidumbre permanezca explícita y trazable; que los artefactos sean reproducibles e íntegros; que exista IIIF estable para el witness canónico; que el release sea citable y archivado; y que el pipeline haya demostrado reutilización sobre una segunda fuente completa. Este último requisito ya quedó satisfecho con Tellechea 1826.
