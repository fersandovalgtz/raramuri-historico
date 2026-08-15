# RHD 1.0 — Protocolo editorial reusable

**Estado:** borrador normativo  
**Implementación de referencia:** Corpus Steffel 1791/1809

## 1. Objeto

Este protocolo convierte la experiencia acumulada en Steffel en un procedimiento reusable para incorporar futuras fuentes históricas a Rarámuri Histórico Digital. No sustituye protocolos especializados de revisión humana; los organiza dentro de un flujo general común.

## 2. Regla de oro

**La evidencia anterior no se borra.** Toda intervención posterior debe añadirse como una capa, decisión o relación trazable.

## 3. Flujo editorial estándar

### Fase A — Registro y preservación

1. Crear `source_id` y `witness_id`.
2. Registrar descripción bibliográfica y material del testimonio.
3. Preservar el archivo fuente cuando jurídicamente sea posible.
4. Calcular SHA-256 para archivos preservados.
5. Crear mapeo entre paginación impresa y paginación digital.
6. Registrar derechos, procedencia y URI externa cuando corresponda.

**Salida mínima:** fuente identificable y reproducible.

### Fase B — Perfil de fuente

Antes de extracción masiva se debe crear un perfil que declare:

- direcciones lexicográficas;
- estructura por columnas;
- signos de frontera;
- abreviaturas;
- grafías históricas relevantes;
- zonas que no pertenecen al diccionario;
- reglas de normalización permitidas y prohibidas;
- cambios de sección dentro de una misma página;
- anomalías materiales conocidas.

Una regla encontrada en una fuente no se transfiere automáticamente a otra.

### Fase C — Calibración

Seleccionar una muestra deliberadamente heterogénea. Debe incluir casos sencillos y difíciles, cambios de sección, remisiones, variantes, artículos extensos, formas dudosas y ejemplos de cada convención material importante.

El objetivo no es producir una muestra estadísticamente representativa, sino **estresar el modelo** antes de ejecutar extracción total.

### Fase D — Segmentación de alta cobertura

El segmentador debe favorecer recuperación amplia. Cada candidato registra:

- localización;
- texto OCR asociado;
- señal usada para proponer frontera;
- método;
- puntaje/confianza;
- versión del sistema.

Un candidato no es una entrada.

### Fase E — Cotejo de frontera

Cada candidato recibe una disposición explícita:

- `accepted`;
- `rejected`;
- `merged`;
- `split`;
- `unresolved`.

Los candidatos rechazados conservan su identificador y evidencia.

### Fase F — Transcripción diplomática

La transcripción diplomática se realiza contra la imagen, no contra el OCR como autoridad final. Debe preservar, en la medida definida por el perfil:

- grafías históricas;
- diacríticos;
- puntuación;
- abreviaturas;
- orden visible;
- variantes impresas.

La transcripción puede ser IA-asistida, pero debe declararlo. `AI-assisted` nunca equivale a `human_verified`.

### Fase G — Auditoría de incertidumbre

Toda nota o duda debe clasificarse. Como mínimo:

- lectura gráfica;
- estructura de artículo;
- forma lingüística histórica;
- glosa/semántica;
- identificación disciplinar;
- problema general.

La clasificación sirve para enrutar revisión; no resuelve el problema.

### Fase H — Recotejo especializado IA-asistido

Puede existir una segunda inspección con imágenes de mayor resolución o criterios especializados. Sus decisiones deben ser append-only y adoptar estados como:

- `confirmed_ai_assisted`;
- `corrected_ai_assisted`;
- `unresolved_after_ai_recollation`.

Una corrección propuesta no modifica físicamente la transcripción diplomática.

### Fase I — Revisión humana independiente

La revisión humana debe declarar:

- persona;
- afiliación;
- ORCID cuando exista;
- competencia relevante;
- fecha;
- alcance;
- decisión;
- evidencia;
- justificación;
- confianza.

Los ejes filológico, lingüístico, semántico/histórico y disciplinar son independientes.

`remain_unresolved` es una salida válida.

### Fase J — Lectura crítica y normalización

Sólo después de una decisión explícita puede crearse una capa crítica o normalizada que adopte una corrección. Debe conservar vínculo a:

- registro original;
- lectura diplomática;
- evento de revisión;
- responsable;
- método.

La normalización para búsqueda puede existir antes, pero debe estar marcada como técnica y no como lectura crítica.

### Fase K — Estructuración lexicográfica

Cuando la evidencia lo permita, separar:

- lema/formas;
- variantes;
- sentidos;
- glosas fuente;
- traducciones editoriales;
- ejemplos;
- remisiones;
- notas gramaticales;
- notas culturales.

La fuente histórica y el comentario moderno deben permanecer distinguibles.

### Fase L — Relaciones históricas

Las correspondencias con otras fuentes o con Rarámuri Digital se almacenan como relaciones, nunca como fusiones.

Cada relación debe contener:

- origen;
- destino;
- tipo de relación;
- método de recuperación;
- evidencia formal;
- evidencia semántica;
- evidencia externa, si existe;
- confianza;
- estatus de revisión humana.

Una semejanza gráfica no basta para promover una relación.

### Fase M — Exportación e interoperabilidad

Las exportaciones deben generarse desde capas versionadas y no editarse manualmente como fuentes paralelas.

Objetivos RHD 1.0:

- JSON canónico;
- CSV operacional cuando sea útil;
- SQLite;
- TEI P5 / TEI Lex-0 validado;
- manifiesto IIIF cuando el facsímil pueda servirse interoperablemente;
- manifiesto de integridad con checksums.

### Fase N — Release

Un release debe declarar por separado:

- cobertura documental;
- cobertura diplomática;
- problemas abiertos;
- revisión humana;
- interoperabilidad;
- relaciones diacrónicas;
- limitaciones.

No se permite resumir todo lo anterior mediante una única cifra de “exactitud”.

## 4. Gestión de conflictos editoriales

Cuando dos revisores o capas discrepen:

1. conservar ambas decisiones;
2. registrar alcance y evidencia de cada una;
3. no sobrescribir la capa anterior;
4. abrir un evento de adjudicación;
5. permitir que el resultado final sea `unresolved`.

## 5. Regla de traducción

Una traducción moderna nunca debe presentarse como parte de la fuente si no lo es. Deben distinguirse como mínimo:

- `source_gloss`;
- `editorial_translation`;
- `editorial_commentary`.

## 6. Regla sobre discurso histórico sensible

Expresiones coloniales, etnocéntricas, misioneras o peyorativas se preservan como evidencia documental y se atribuyen a su fuente. La capa editorial moderna puede contextualizar, pero no suavizar silenciosamente ni transformar afirmaciones históricas en hechos actuales.

## 7. Regla sobre inteligencia artificial

Toda intervención IA-asistida debe ser visible mediante procedencia. El sistema debe impedir semánticamente que estados IA activen banderas reservadas a revisión humana.

Como mínimo, una actividad IA registra:

- identificador de actividad;
- tarea;
- insumos;
- salida;
- modelo/sistema cuando esté disponible;
- fecha o commit;
- método;
- estatus no humano.

## 8. Criterios de cierre por fase

### Cierre documental

- todos los candidatos tienen disposición;
- todas las entradas activas tienen localización;
- todas las entradas activas tienen transcripción diplomática;
- no existe lote documental automático pendiente.

### Cierre de incertidumbre IA-asistida

- todas las dudas seleccionadas han sido recotejadas o se declaran no revisables automáticamente;
- las propuestas y dudas permanecen separadas de la diplomática.

### Cierre de revisión humana

Debe declararse el universo de revisión. No se puede afirmar “revisión humana completa” sin especificar qué conjunto y qué ejes fueron revisados.

### Cierre interoperable

- JSON Schema válido;
- TEI validado contra perfil declarado;
- exportaciones reproducibles;
- checksums regenerados;
- tests aprobados;
- release versionado.

## 9. Aplicación a Steffel

Steffel ya satisface de manera sustancial el cierre documental IA-asistido: la cobertura de segmentación, cotejo de fronteras y transcripción diplomática del cuerpo lexicográfico está completa según el repositorio 0.2.0. La siguiente transición no consiste en repetir extracción, sino en:

1. mapear las estructuras Steffel al núcleo RHD 1.0;
2. comenzar adjudicación humana prioritaria por los casos no resueltos;
3. validar el exportador TEI con un perfil formal;
4. incorporar localización facsimilar interoperable;
5. convertir las decisiones de Steffel que funcionaron en componentes configurables para la siguiente fuente.

## 10. Resultado esperado

Cuando este protocolo se aplique a una segunda fuente, el trabajo específico deberá concentrarse en el perfil y la calibración. El resto del pipeline —identidad, capas, procedencia, incertidumbre, revisión, exportación y publicación— debe reutilizarse sin rediseño fundamental.