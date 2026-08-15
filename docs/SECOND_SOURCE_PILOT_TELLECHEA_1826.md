# Segunda fuente piloto — Miguel Tellechea, 1826

**Estado:** witness público fijado por checksum; prueba mínima y prueba fuerte de 205 páginas completadas.  
**Avance de la dimensión de replicación:** **100%**.

## Por qué Tellechea

El *Compendio gramatical para la inteligencia del idioma tarahumar* de Miguel Joaquín Tellechea fue publicado en México por la Imprenta de la Federación en Palacio en 1826. Es suficientemente cercano a Steffel para mantener continuidad temática e histórica, pero estructuralmente muy distinto: no es un diccionario bidireccional, sino una obra gramatical con materiales religiosos y extensos pasajes español–tarahumara.

Esa diferencia lo convirtió en una prueba fuerte de reutilización. RHD debía demostrar que sus conceptos universales —witness, unidad documental, localizador, capas, procedencia, incertidumbre y exportación— podían sobrevivir fuera del formato lexicográfico sin convertir el núcleo en un modelo hecho a la medida de Tellechea.

## Witness canónico del piloto

La Dirección General de Bibliotecas de la Secretaría de Cultura mantiene una reproducción PDF pública de la obra. El 15 de agosto de 2026 GitHub Actions recuperó directamente ese binario y fijó su identidad de manera reproducible:

- witness: `RHD-WIT-TELLECHEA-1826-DGB`;
- URI de recuperación: `https://dgb.cultura.gob.mx/recursos/documentos/lenguasindigenas/Compendiogramaticalpara.pdf`;
- tamaño: **95,088,307 bytes**;
- páginas PDF: **205**;
- versión PDF observada: **1.6**;
- SHA-256: `c67b7942090613c494d8057be8aff59ea13a11519c29eae469afad8a85c30dfc`.

La identidad queda registrada en `sources/tellechea-1826-witness.json`. La CI vuelve a descargar el PDF y exige que checksum, tamaño y número de páginas permanezcan exactos. Un cambio del proveedor constituye un cambio de witness y no puede aceptarse silenciosamente.

## Capa textual y evidencia visual

El witness posee una capa textual sustancial: **193 páginas con texto extraíble**, **285,857 caracteres** y una mediana de **1,553 caracteres** en páginas no vacías. Esa capa se preserva como evidencia documental y no se denomina transcripción diplomática.

La prueba mínima agregó una segunda lectura independiente desde el facsímil mediante renderizado y OCR visual. La prueba fuerte conserva el mismo principio: las páginas con capa textual escasa reciben un fallback visual separado, de modo que el texto embebido no adquiera autoridad editorial por defecto.

## Prueba mínima — completada

La prueba mínima trabajó con dos unidades reales y estructuralmente diferentes. `RHD-T1826-00001` corresponde a **PDF 32 / impreso 6**, localizado por `LIBRO PRIMERO`, `CAPITULO I` y `Del Nombre`; `RHD-T1826-00002` corresponde a **PDF 75 / impreso 49**, una página de disposición paralela que incluye *Persignum Crucis*, *Pater Noster* y *Ave Maria*.

Ambas unidades atravesaron verificación de checksum, extracción de texto embebido, renderizado facsimilar, OCR visual independiente, canonicalización RHD, JSON Schema y TEI. En ninguno de los casos se fabricó una entrada Lex-0 ni una atribución de validación humana.

## Prueba fuerte — completada

La prueba fuerte extiende el mismo patrón al **witness completo de 205 páginas** mediante `scripts/generate_tellechea_full_pilot.py` y `tests/validate_tellechea_full_pilot.py`.

Cada página recibe un identificador documental determinista `RHD-T1826-10001` … `RHD-T1826-10205`, un localizador digital, una capa de texto fuente preservada, una disposición de segmentación y procedencia explícita. Las páginas con texto embebido escaso reciben OCR visual separado; las restantes conservan una proyección documental explícitamente marcada como no visual y no adjudicada.

El validator exige simultáneamente:

- **205 registros canónicos para 205 páginas**;
- validación de todos los registros contra el mismo `schemas/rhd-entry-1.0.schema.json` utilizado por RHD;
- secuencia determinista de IDs y páginas;
- conservación de las anclas PDF 32 / impreso 6 y PDF 75 / impreso 49;
- al menos 190 páginas con capa textual fuente y más de 250,000 caracteres recuperados;
- activación real del fallback OCR visual en las páginas donde hace falta;
- jerarquía documental machine-candidate conservadora;
- **cero cambios requeridos al núcleo universal RHD**;
- **cero entradas Lex-0 generadas** para este material no lexicográfico;
- **cero validaciones humanas fabricadas**;
- TEI documental completa con 205 unidades y sin elementos `<entry>`.

El 15 de agosto de 2026 esta prueba quedó verde en GitHub Actions. La salida completa se empaquetó como artefacto reproducible `tellechea-1826-full-witness-rhd-pilot`; la primera ejecución exitosa correspondió al run `31887068250`, artifact `9247575047`, con digest SHA-256 del ZIP `fb0fbf4b64c9978e97212951778e6843c21b3d64e7308e37b7dfbab34a6d13f8`.

Los tres productos derivados son:

- `data/pilot/tellechea-1826.full-witness.jsonl`;
- `data/pilot/tellechea-1826.full-witness.tei.xml`;
- `data/pilot/tellechea-1826.full-witness.diagnostics.json`.

Se generan dentro de CI y se incluyen en el manifiesto de integridad del release; no se presentan como fuentes originales ni como una edición humana de Tellechea.

## Qué demuestra el cierre

La segunda fuente ya no es sólo una prueba de concepto. La totalidad del witness declarado atraviesa el sistema con los mismos conceptos de identidad, capas, procedencia, validación de esquema y exportación utilizados por la implementación de referencia. Las peculiaridades de Tellechea permanecen en su perfil y adaptador; el núcleo RHD no necesitó adquirir reglas específicas de esta obra.

Por ello el gate de industrialización se considera **cerrado al 100%**. El significado del cierre es preciso: RHD ha demostrado reutilización computacional end-to-end sobre una segunda fuente histórica real, estructuralmente distinta y completa en el alcance declarado. No significa que Tellechea sea una edición crítica humana, ni que cada lectura histórica haya sido adjudicada lingüísticamente.

## Consecuencia para RHD 1.0

Con la prueba fuerte cerrada, la pregunta ya no es si RHD puede salir del diccionario de Steffel. Esa capacidad quedó demostrada empíricamente. El camino crítico del proyecto se concentra ahora en **IIIF canónico**, **release/archivo persistente**, **cierre de productos diacrónicos** y el pequeño residual de refinamiento de anexos.
