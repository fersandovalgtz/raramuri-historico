# Segunda fuente piloto — Miguel Tellechea, 1826

**Estado:** witness público fijado por checksum; prueba mínima end-to-end completada; procesamiento fuerte del witness completo pendiente.  
**Avance de la dimensión de replicación:** **40%**.

## Por qué Tellechea

El *Compendio gramatical para la inteligencia del idioma tarahumar* de Miguel Joaquín Tellechea fue publicado en México por la Imprenta de la Federación en Palacio en 1826. Es suficientemente cercano a Steffel para mantener continuidad temática e histórica, pero estructuralmente muy distinto: no es un diccionario bidireccional, sino una obra gramatical con materiales religiosos y extensos pasajes español–tarahumara.

Esa diferencia lo vuelve una prueba más fuerte que escoger simplemente otro vocabulario con la misma forma documental de Steffel. La prueba mínima ya demuestra que RHD puede representar material gramatical y disposición paralela sin convertirlos artificialmente en artículos lexicográficos ni rediseñar sus conceptos de witness, evidencia, capas, procedencia, identificadores e incertidumbre.

## Witness canónico del piloto

La Dirección General de Bibliotecas de la Secretaría de Cultura mantiene una reproducción PDF pública de la obra. El 15 de agosto de 2026 GitHub Actions recuperó directamente ese binario y fijó su identidad de manera reproducible:

- witness: `RHD-WIT-TELLECHEA-1826-DGB`;
- URI de recuperación: `https://dgb.cultura.gob.mx/recursos/documentos/lenguasindigenas/Compendiogramaticalpara.pdf`;
- tamaño: **95,088,307 bytes**;
- páginas PDF: **205**;
- versión PDF observada: **1.6**;
- SHA-256: `c67b7942090613c494d8057be8aff59ea13a11519c29eae469afad8a85c30dfc`.

La identidad queda registrada en `sources/tellechea-1826-witness.json`. La CI vuelve a descargar el PDF y exige que checksum, tamaño y número de páginas sigan siendo exactamente los mismos. Un cambio del proveedor debe aparecer como cambio de witness, no aceptarse silenciosamente.

Google Play Books y la Biblioteca Virtual de la Filología Española se conservan como referencias bibliográficas/digitales independientes. No sustituyen el witness DGB checksum-fixed.

## Capa textual del PDF

El witness resultó especialmente favorable para una ingestión machine-only porque posee una capa textual sustancial. La inspección automatizada de las 205 páginas encontró:

- **193 páginas con texto extraíble**;
- **285,857 caracteres** extraídos;
- mediana de **1,553 caracteres** en las páginas no vacías;
- clasificación automática `substantial_embedded_text_layer`.

Esta capa no se considera transcripción diplomática. Se preserva como `source_embedded_text_preserved` y se contrasta con una segunda lectura producida directamente desde el facsímil. De este modo, un error del texto embebido no se convierte automáticamente en lectura editorial.

## Diferencias que deben vivir en el perfil y no en el núcleo

Steffel organiza principalmente artículos lexicográficos. Tellechea exige unidades como capítulos gramaticales, ejemplos, paradigmas y bloques paralelos español–tarahumara. El núcleo RHD no debe adquirir reglas con nombres como `tellechea_paragraph` o `tellechea_prayer`; esas particularidades permanecen en `source_profiles/tellechea-1826.pilot-candidate.json` y en el generador/adaptador específico.

Los conceptos universales siguen siendo los mismos: witness, unidad documental, localizador, capa fuente, lectura visual machine-only, derivación estructurada, procedencia, incertidumbre, relaciones entre unidades y exportación interoperable.

## Prueba mínima end-to-end — completada

El 15 de agosto de 2026 se ejecutó en GitHub Actions una prueba real sobre dos unidades documentalmente distintas. El pipeline hizo, de forma reproducible y sin intervención humana, la siguiente secuencia: verificación del checksum del PDF, extracción de la capa textual embebida, localización estructural, renderizado de la página facsimilar, OCR visual independiente con Tesseract, representación canónica RHD, validación contra el JSON Schema y exportación TEI.

### Unidad 1 — gramática

`RHD-T1826-00001` corresponde a **PDF 32 / página impresa 6**. Fue localizada por la combinación estructural `LIBRO PRIMERO`, `CAPITULO I` y `Del Nombre`.

- texto embebido preservado: **1,083 caracteres**;
- OCR visual independiente: **991 caracteres**;
- solapamiento documental Jaccard de tokens: **0.4201**;
- `lexical = null`;
- estado visual: `machine_visual_ocr_unadjudicated`.

La unidad demuestra que el núcleo RHD puede representar una página gramatical sin forzarla al modelo de diccionario.

### Unidad 2 — disposición paralela español–tarahumara

`RHD-T1826-00002` corresponde a **PDF 75 / página impresa 49**, encabezada por material del *Persignum Crucis*, *Pater Noster* y *Ave Maria*. La página se dividió geométricamente en dos columnas antes del OCR visual.

- texto embebido preservado: **1,404 caracteres**;
- OCR visual independiente: **1,218 caracteres**;
- solapamiento documental Jaccard de tokens: **0.4155**;
- puntuación conservadora de palabras funcionales españolas: **4** en la columna izquierda y **32** en la derecha;
- asignación machine-only: izquierda `und_candidate`, derecha `es_candidate`;
- estado de la asignación: `machine_candidate`, no certeza lingüística;
- `lexical = null`.

La disposición y el contenido permiten tratar la página como prueba de paralelismo documental sin inferir que cada línea forme una traducción uno-a-uno. La asignación lingüística puede revisarse computacionalmente en futuras capas, pero no se transforma en una afirmación humana ni semántica.

## Artefactos reproducibles de la prueba mínima

La ejecución genera y valida:

- `data/pilot/tellechea-1826.minimal-pilot.jsonl`;
- `data/pilot/tellechea-1826.minimal-pilot.tei.xml`;
- `data/pilot/tellechea-1826.minimal-pilot.diagnostics.json`;
- `scripts/generate_tellechea_pilot.py`;
- `tests/validate_tellechea_pilot.py`.

Los registros canónicos validan contra el mismo JSON Schema utilizado por RHD, pero la TEI documental de Tellechea no genera `<entry>` de diccionario ni contamina la proyección Lex-0.

## Qué demostró la prueba mínima

La prueba mínima ya satisface cinco afirmaciones útiles sobre la industrialización:

1. un witness externo distinto puede fijarse y vigilarse por identidad binaria;
2. RHD admite unidades no lexicográficas manteniendo el mismo modelo de procedencia;
3. texto embebido y lectura visual independiente pueden coexistir como capas no destructivas;
4. una página bilingüe en columnas puede representarse sin inventar equivalencia semántica frase a frase;
5. el núcleo universal no necesitó convertirse en un modelo específico de Tellechea.

Por esta razón la dimensión de replicación recibe **40%**, no 100%. Se ha demostrado la viabilidad end-to-end mínima, pero aún no la industrialización del witness completo.

## Prueba fuerte — pendiente

Para cerrar la dimensión debe procesarse el alcance completo declarado del witness de **205 páginas**. La prueba fuerte deberá:

- construir la cartografía documental completa;
- crear unidades persistentes para gramática, paradigmas, ejemplos, textos paralelos y paratextos;
- conservar la capa textual embebida y producir cotejo visual machine-only donde corresponda;
- modelar el paralelismo sólo donde la evidencia de disposición lo justifique;
- producir una TEI documental completa;
- registrar cualquier modificación necesaria al núcleo RHD y clasificarla como capacidad universal, corrección general o peculiaridad que debe permanecer en el perfil;
- demostrar en CI que el pipeline completo sigue siendo reproducible y que ninguna fase fabrica adjudicación humana.

## Criterio de cierre

El gate de industrialización no se cerrará porque dos páginas funcionaron. Se cerrará cuando el witness completo de Tellechea atraviese el pipeline declarado sin rediseño fundamental del núcleo RHD. La prueba mínima cambia, sin embargo, el estado metodológico del proyecto: la reutilización fuera del formato diccionario **ya fue demostrada empíricamente**, aunque todavía no a escala completa.
