# Rarámuri Histórico Digital — Especificación RHD 1.0

**Estado:** borrador normativo para implementación de referencia en Steffel 1791/1809  
**Fecha:** 15 de agosto de 2026  
**Alcance:** núcleo reusable para futuras ediciones histórico-digitales del ecosistema RHD.

## 1. Propósito

RHD 1.0 define el modelo metodológico y técnico mediante el cual una fuente histórica puede incorporarse a Rarámuri Histórico Digital sin reconstruir el sistema desde cero. El Corpus Steffel 1791/1809 funciona como **implementación de referencia** y banco de pruebas, pero la especificación distingue estrictamente entre:

1. **núcleo RHD universal**, aplicable a cualquier fuente histórica;
2. **perfil de fuente**, que contiene las particularidades materiales, lingüísticas, tipográficas y editoriales de cada testimonio.

El objetivo operativo es que una fuente nueva requiera principalmente un perfil de fuente, reglas de segmentación y una calibración inicial, mientras reutiliza identificadores, capas, procedencia, revisión, exportaciones, validaciones y relaciones del núcleo RHD.

## 2. Principios normativos

Las palabras **DEBE**, **NO DEBE**, **DEBERÍA** y **PUEDE** se emplean en sentido normativo.

### 2.1 No sobrescritura

La evidencia primaria nunca se reemplaza por una interpretación posterior. El facsímil, OCR bruto, segmentación, transcripción diplomática, propuestas de corrección, decisiones humanas y normalizaciones DEBEN permanecer distinguibles y trazables.

### 2.2 Procedencia explícita

Toda transformación DEBE poder responder: qué entidad fue transformada, mediante qué actividad, por qué agente o sistema, con qué método, cuándo y con qué evidencia.

### 2.3 Incertidumbre preservada

La incertidumbre es un dato. El sistema NO DEBE forzar una lectura, segmentación, identidad léxica, interpretación semántica o correspondencia diacrónica para alcanzar completitud artificial.

### 2.4 Separación entre evidencia y análisis

Una coincidencia gráfica, una normalización de búsqueda o una relación computacional NO DEBEN convertirse automáticamente en cognación, identidad semántica, continuidad histórica, morfología o categoría gramatical.

### 2.5 Identificadores persistentes

Una unidad que haya recibido un identificador RHD NO DEBE reciclarlo, aun si después es rechazada, fusionada, dividida o reinterpretada.

### 2.6 Reproducibilidad

Toda capa derivada por software DEBERÍA poder regenerarse a partir de entradas versionadas, scripts versionados y parámetros declarados.

## 3. Arquitectura por capas

RHD 1.0 establece las siguientes capas lógicas:

`source_witness` → `facsimile` → `ocr_raw` → `segmentation_candidate` → `boundary_review` → `diplomatic_transcription` → `validation_event` → `critical_or_normalized_reading` → `lexical_structure` → `historical_relation`

Las implementaciones pueden añadir capas intermedias, pero NO DEBEN colapsar capas con diferente estatus epistemológico.

### 3.1 Source witness

Representa un testimonio documental concreto: edición, ejemplar, reproducción o facsímil utilizado. Debe registrar al menos identificador, título, autoría atribuida, fechas relevantes, procedencia, extensión, localización o URI cuando exista, derechos y checksum cuando el archivo se preserve localmente.

### 3.2 Facsimile

Representa páginas o vistas del testimonio. Debe permitir localización a nivel de página y, cuando sea técnicamente viable, región de página.

### 3.3 OCR raw

Preserva la salida OCR sin corrección editorial. Debe existir una relación explícita con página, línea o región de origen.

### 3.4 Segmentation candidate

Representa una propuesta de límite documental, no una entrada validada. Debe conservar método, puntaje o confianza técnica y evidencia de origen.

### 3.5 Boundary review

Registra aceptación, rechazo, fusión o división de una propuesta de segmentación sin borrar la propuesta original.

### 3.6 Diplomatic transcription

Representa la lectura documental que intenta reproducir fielmente grafías, puntuación y estructura visible. Debe declarar método y estatus de revisión.

### 3.7 Validation event

Registra una decisión filológica, lingüística, semántica/histórica o disciplinar. Una validación en un plano NO implica validación automática en los demás.

### 3.8 Critical or normalized reading

Representa una lectura adoptada o una forma normalizada para fines explícitos. Debe enlazar la evidencia diplomática y la decisión que la justifica.

### 3.9 Lexical structure

Representa forma, lema, variantes, sentidos, glosas, traducciones, ejemplos, remisiones y otras unidades lexicográficas cuando la estructura de la fuente lo permita.

### 3.10 Historical relation

Representa una relación derivada entre unidades históricas o entre una unidad histórica y otra fuente/corpus. Debe declarar tipo, método, evidencia, confianza y estatus de revisión.

## 4. Entidades canónicas

RHD 1.0 define las siguientes entidades conceptuales:

- `Source`
- `Witness`
- `Page`
- `Region`
- `OCRSegment`
- `EntryCandidate`
- `LexicalEntry`
- `Form`
- `Sense`
- `Attestation`
- `EditorialDecision`
- `ValidationEvent`
- `HistoricalRelation`
- `Agent`
- `Activity`

Estas entidades constituyen el **modelo canónico semántico**. RHD 1.0 no exige todavía una única serialización canónica. El Corpus Steffel puede conservar `data/entries.csv` como maestro operativo mientras JSON, XML, TEI, SQLite u otros formatos se generan como proyecciones, siempre que exista un mapeo explícito al modelo RHD.

## 5. Identificadores

### 5.1 Fuente

Formato recomendado: `RHD-SRC-<codigo>`.

Ejemplo: `RHD-SRC-STEFFEL-1809`.

### 5.2 Registro documental / entrada

Formato ya adoptado: `RHD-S1809-#####`.

Los perfiles futuros DEBEN definir un prefijo estable y no ambiguo.

### 5.3 Decisiones y actividades

Se recomiendan prefijos específicos por actividad:

- `RHD-FR-###` — revisión de frontera/segmentación;
- `RHD-DIP-###` — transcripción diplomática;
- `RHD-PHIL-###` — recotejo filológico IA-asistido;
- `RHD-HR-###` — revisión humana;
- `RHD-REL-########` — relación histórica/diacrónica.

## 6. Estados epistemológicos

Toda afirmación relevante debe poder distinguir al menos:

- `machine_candidate`
- `ai_assisted`
- `human_reviewed`
- `human_verified`
- `unresolved`
- `rejected`

Para revisión especializada deben mantenerse ejes independientes:

- `philological_status`
- `linguistic_status`
- `semantic_historical_status`
- `disciplinary_status`

## 7. Confianza

La confianza DEBE describir el alcance de una afirmación concreta. No se permite una única puntuación global que mezcle lectura gráfica, segmentación, semántica y continuidad histórica.

Se recomienda una escala controlada:

- `high`
- `medium`
- `low`
- `unresolved`

Los modelos numéricos pueden coexistir, pero deben documentar su cálculo y no sustituir las categorías editoriales.

## 8. Perfil de fuente

Cada nueva fuente DEBE contar con un perfil versionado que declare como mínimo:

- identidad bibliográfica;
- testimonio utilizado;
- rangos de páginas relevantes;
- idiomas y direcciones lexicográficas;
- estructura material del texto;
- grafías históricas relevantes;
- abreviaturas y convenciones;
- reglas de segmentación candidatas;
- mapeo entre página impresa y página digital;
- reglas permitidas de normalización de búsqueda;
- reglas prohibidas de normalización;
- criterios de cobertura;
- problemas conocidos;
- política de validación humana;
- mapeo al núcleo RHD.

Las reglas específicas de una fuente NO DEBEN incorporarse silenciosamente al núcleo universal.

## 9. Interoperabilidad

### 9.1 TEI / TEI Lex-0

RHD 1.0 adopta TEI P5 como marco principal para una futura edición académica interoperable y TEI Lex-0 como referencia de modelado lexicográfico. La exportación TEI debe representar de manera diferenciada formas, sentidos, glosas, citas, procedencia, responsabilidad y enlaces al facsímil.

Mientras el exportador no haya superado validación estructural y pruebas de round-trip, la representación TEI debe declararse **derivada** y no fuente única de verdad.

### 9.2 IIIF

RHD 1.0 debe ser compatible con un futuro manifiesto IIIF Presentation 3.0. Cada página debe poder representarse como Canvas y cada entrada o región como anotación o selector espacial cuando exista resolución suficiente.

### 9.3 Procedencia PROV

El modelo de procedencia debe ser mapeable a PROV-O mediante las nociones de `Entity`, `Activity`, `Agent`, `wasDerivedFrom`, `wasGeneratedBy` y asociaciones equivalentes. No se exige RDF para la implementación 1.0.

## 10. Conformidad de una fuente RHD

Se establecen cuatro niveles.

### RHD-L1 — Preservación

Fuente identificada, facsímil/OCR preservado, checksums y paginación trazable.

### RHD-L2 — Edición documental

Segmentación, cotejo de límites y transcripción diplomática con procedencia explícita.

### RHD-L3 — Edición revisada

Protocolo de revisión independiente operativo y decisiones humanas registradas sin sobrescritura.

### RHD-L4 — Interoperabilidad y comparación

Exportación TEI validada, enlaces facsimilares interoperables, relaciones históricas explícitas y publicación versionada reproducible.

Una fuente puede estar completa en L2 y parcialmente en L3/L4; el estado debe publicarse por nivel, no como una etiqueta global de “terminada”.

## 11. Criterio de implementación de referencia: Steffel

El Corpus Steffel es la implementación de referencia RHD 1.0 porque ya dispone de:

- cobertura integral de segmentación del cuerpo lexicográfico;
- transcripción diplomática IA-asistida de los artículos activos;
- manifiestos append-only de revisión;
- cola explícita de problemas abiertos;
- protocolo de revisión humana;
- relaciones internas y diacrónicas separadas de la validación;
- exportaciones reproducibles.

La tarea RHD 1.0 no es reiniciar Steffel, sino **mapear su arquitectura madura al núcleo reusable** y extraer de ese caso una plantilla transferible.

## 12. Política para nuevas fuentes

La incorporación de una nueva fuente debe seguir esta secuencia:

1. registrar fuente y testimonio;
2. preservar archivos y checksums;
3. crear perfil de fuente;
4. calibrar segmentación sobre una muestra deliberadamente diversa;
5. ejecutar segmentación de alta cobertura;
6. cotejar límites;
7. producir transcripción diplomática;
8. clasificar incertidumbre;
9. habilitar revisión independiente;
10. producir capas normalizadas/lexicográficas;
11. generar interoperabilidad y relaciones históricas;
12. publicar release versionado con métricas de cobertura y validación.

## 13. Gestión de cambios

Cambios que alteren identificadores, significado de estados, reglas de no sobrescritura o semántica de entidades requieren incremento mayor de versión de la especificación.

Cambios compatibles que añadan campos opcionales, vocabularios o mapeos pueden incorporarse en versiones menores.

Los perfiles de fuente tienen versionado independiente del núcleo RHD.

## 14. Referencias normativas y técnicas

- TEI Consortium, *TEI P5 Guidelines for Electronic Text Encoding and Interchange*.
- TEI Lex-0, *A baseline encoding for lexicographic data*.
- IIIF Consortium, *Presentation API 3.0*.
- W3C, *PROV-O: The PROV Ontology*.

## 15. Decisión arquitectónica central

RHD 1.0 declara como canónico el **modelo semántico y de procedencia**, no un archivo concreto. Esta decisión permite que el corpus Steffel conserve temporalmente sus estructuras operativas maduras y, al mismo tiempo, que nuevas fuentes nazcan directamente bajo el modelo reusable sin obligar a migraciones destructivas.