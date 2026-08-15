# Changelog

## 0.9.0-machine-only-prerelease — 2026-08-15

### Alcance científico

- Se adopta formalmente la política **machine-only**: no se requiere adjudicación humana para el cierre del Corpus Steffel.
- Ningún resultado IA-asistido puede presentarse como `human_verified`, `expert_verified` o equivalente.
- `unresolved_after_ai_recollation` se reconoce como estado terminal legítimo cuando la evidencia no permite seleccionar una lectura única.
- Los 482 problemas PHIL quedan cerrados computacionalmente: 284 `confirmed_ai_assisted`, 152 `corrected_ai_assisted` y 46 `unresolved_after_ai_recollation`.
- La métrica ponderada machine-only queda en **98.0% terminado / 2.0% pendiente**; el residual corresponde exclusivamente a publicación IIIF persistente y release/archivo persistente.

### RHD 1.0 reusable

- Especificación del núcleo RHD, JSON Schema canónico, perfil Steffel y plantilla reusable de perfiles de fuente.
- Adaptador Steffel → RHD canónico con separación de OCR, diplomática, PHIL, traducción editorial, relaciones históricas y procedencia.
- 482 eventos PHIL incorporados sin fabricar validación humana.
- 298 relaciones Steffel ↔ Rarámuri Digital incorporadas como `candidate`.

### Interoperabilidad

- Separación entre TEI RHD rica y proyección TEI Lex-0 estricta.
- Validación CI de la proyección estricta contra el RNG oficial **TEI Lex-0 0.9.5**.
- Suplemento TEI específico para anexos, separado de Lex-0.
- Política y pruebas que impiden crear automáticamente `<def>` desde material fuente no estructurado.
- El PDF Steffel canónico fue re-verificado como **84 páginas, 6,251,443 bytes, SHA-256 `4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f`**.
- Desde ese witness exacto se incorporan huellas de las 84 páginas, inventario de dimensiones, constructor exact-binary, generador IIIF Presentation 3, **84 Canvases**, Canvas-map y **1,965/1,965 enlaces registro activo → Canvas**.
- La preparación IIIF no inventa regiones `xywh`; mientras las imágenes no estén alojadas por HTTPS estable, el Manifest de CI usa deliberadamente un dominio reservado `.invalid` y no simula una publicación inexistente.
- Los proveedores externos mutables o no idénticos permanecen sólo como diagnósticos/witnesses paralelos no canónicos.

### Anexos Steffel 369–374 — cerrado en alcance machine-only

- Cotejo visual IA y mapeo facsimilar exacto `PDF 79–84 ↔ impreso 369–374`.
- Capa canónica de 24 objetos: 1 sección de numeración, 22 fórmulas y 1 Padre Nuestro.
- Estructuración computacional del sistema numeral con cardinales/ejemplos, sistemas de conteo, multiplicativos, otras expresiones numéricas y ordinales.
- Alineación visual IA de las 22 fórmulas en latín–alemán–tarahumara: 66 campos paralelos con nivel de confianza y segmentos inciertos explícitos.
- Transcripción visual IA del Padre Nuestro como bloque independiente hasta `Amen.`.
- Registro terminal de incertidumbre: toda lectura media/baja o segmento dudoso queda inventariado como `explicit_machine_uncertainty`, sin reparación especulativa y sin requisito humano.
- La incertidumbre residual es un estado científico terminal y ya no constituye trabajo pendiente.

### Investigación diacrónica computacional — cerrada en alcance machine-only

- Las 298 relaciones candidatas reciben puntuación reproducible de **apoyo documental de recuperación** mediante similitud gráfica conservadora, atestiguación interna y apoyo documental recíproco.
- Se añade calibración contra **5,066 emparejamientos nulos deterministas** obtenidos mediante 17 desplazamientos circulares del mismo inventario de formas modernas.
- Cada relación conserva `candidate`; la calibración mide únicamente especificidad grafémica de recuperación.
- Se genera un informe científico y tabla reproducibles sobre las 298 relaciones.
- Las pruebas prohíben convertir puntuaciones o percentiles en probabilidad semántica, cognación, etimología, ley fonológica o continuidad histórica.
- La dimensión diacrónica queda cerrada al **100% dentro del alcance machine-only** sin adjudicación semántica automática ni humana.

### Segunda fuente e industrialización

- Se fija el witness público de **Miguel Joaquín Tellechea, 1826, _Compendio gramatical para la inteligencia del idioma tarahumar_**: 205 páginas, 95,088,307 bytes, SHA-256 `c67b7942090613c494d8057be8aff59ea13a11519c29eae469afad8a85c30dfc`.
- Prueba mínima end-to-end: una unidad gramatical y una unidad de disposición paralela atraviesan extracción, OCR visual independiente, canonicalización y TEI.
- Prueba fuerte end-to-end: **205/205 páginas** se convierten en unidades documentales RHD deterministas y TEI completa.
- El procesamiento completo de Tellechea registra **0 rediseños del núcleo universal**, **0 entradas Lex-0 fabricadas** y **0 atribuciones humanas**.
- Queda demostrado que el núcleo RHD puede industrializar una segunda fuente histórica estructuralmente distinta del diccionario de Steffel.

### Integridad y release

- Generador determinista de manifiesto de prerelease con SHA-256, tamaños y conteos.
- El manifiesto incluye capas lexicales, canónicas, diacrónicas, calibración nula, anexos, incertidumbre terminal, TEI/Lex-0 y productos mínimo/completo de Tellechea.
- IIIF se modela como gate independiente: su falta de hosting público no invalida las demás capas checksum-fixed ni puede convertirse en falsa afirmación de completitud.
- `CITATION.cff` preparado para `0.9.0-machine-only-prerelease`.
- Declaración de conformidad de implementación RHD 1.0 machine-only.
- Métrica de terminación machine-only versionada y auditable.
- La CI integral valida Tellechea 205/205, anexos, incertidumbre terminal, calibración 298×5,066, informe diacrónico, TEI/Lex-0, preparación IIIF de 84 Canvases/1,965 enlaces y manifiesto de integridad.

### Pendientes para release final RHD 1.0

- **IIIF público persistente:** alojar por HTTPS las 84 imágenes derivadas del witness exacto, regenerar el Manifest con identificadores reales y verificar Manifest + 84 recursos contra sus hashes/dimensiones.
- **Release/archivo persistente:** fijar commit/tag final, publicar RHD 1.0 estable y depositar datos/software en un archivo persistente con identificador citable, verificando correspondencia con el manifiesto de integridad.

<!-- AMEKE_PERM_CHANGELOG_START -->
## Control por permutaciones `-ameke` — 2026-08-13

- 20,000 permutaciones deterministas por miembro, semilla 1809; prueba ómnibus p=0.0001.
- 3 contrastes con FDR q≤.05 y 1 con control familiar max-|Δ|≤.05.
- La única señal que sobrevive simultáneamente FDR y el control familiar max-|Δ| es **`ugameke` ↔ `infinitive_ending_proxy`**: 0.516 dentro de la clase frente a 0.126 en el resto (Δ=0.390; p=5e-05; q=0.001; FWER=0.0012).
- Revisión humana y análisis morfológico/semántico automáticos permanecen desactivados.
<!-- AMEKE_PERM_CHANGELOG_END -->

## Investigación interna — 2026-08-13

- Nueva extracción conservadora DE–RAR guiada por el inventario RAR–DE: 989 atestiguaciones candidatas; 1458 segmentos residuales quedan separados como baja confianza.
- Concordancia interna Steffel DE–RAR ↔ RAR–DE: 989 relaciones candidatas, 337 con apoyo alemán recíproco.
- Índice documental de variantes: 24 grupos explícitos y 7 colisiones gráficas conservadoras.
- Contexto diacrónico enriquecido para los 298 candidatos: 153 con apoyo interno recíproco, 77 con atestiguación interna no recíproca y 68 sólo con contexto entre corpus.
- Estadística grafémica y corte reproducible en `data/research/`; exportaciones CSV para concordancia y contexto semántico.
- La revisión humana de relaciones permanece en 0; ninguna señal computacional se interpreta como validación lingüística.

## 0.2.0 — 2026-08-11

- Cobertura integral de ambos rangos lexicográficos del OCR.
- 2,495 candidatos de artículo; 60 anclas con identificadores preservados.
- OCR fuente incorporado, tabla de líneas completa y exportaciones regenerables.
- Validación automatizada actualizada para la capa integral.

## 0.1.0-mvp — 2026-08-11

- Creación de Rarámuri Histórico Digital como infraestructura separada de Rarámuri Digital.
- Incorporación preservada del facsímil y OCR de Steffel 1809.
- Esquema inicial `RHD-S1809-#####`.
- 60 registros iniciales estructurados y marcados como OCR sin cotejo final.
- Exportaciones CSV, JSON, XML y SQLite.
- Borrador TEI.
- MVP web de consulta.
- Checksums, procedencia, política editorial, gobernanza y roadmap.