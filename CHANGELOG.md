# Changelog

## Unreleased — RHD 1.0 machine-only reference implementation

### Alcance científico

- Se adopta formalmente la política **machine-only**: no se requiere adjudicación humana para el cierre del Corpus Steffel.
- Ningún resultado IA-asistido puede presentarse como `human_verified`, `expert_verified` o equivalente.
- `unresolved_after_ai_recollation` se reconoce como estado terminal legítimo cuando la evidencia no permite seleccionar una lectura única.
- Los 482 problemas PHIL quedan cerrados computacionalmente: 284 `confirmed_ai_assisted`, 152 `corrected_ai_assisted` y 46 `unresolved_after_ai_recollation`.

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

### Anexos Steffel 369–374

- Cotejo visual IA y mapeo facsimilar exacto `PDF 79–84 ↔ impreso 369–374`.
- Capa canónica de 24 objetos: 1 sección de numeración, 22 fórmulas y 1 Padre Nuestro.
- Estructuración computacional del sistema numeral con cardinales/ejemplos, sistemas de conteo, multiplicativos, otras expresiones numéricas y ordinales.
- Alineación visual IA de las 22 fórmulas en latín–alemán–tarahumara: 66 campos paralelos con nivel de confianza y segmentos inciertos explícitos.
- Transcripción visual IA del Padre Nuestro como bloque independiente hasta `Amen.`.
- Las lecturas gráficas de baja confianza se conservan como incertidumbre y no se corrigen por conjetura.

### Investigación diacrónica computacional

- Las 298 relaciones candidatas reciben puntuación reproducible de **apoyo documental de recuperación** mediante similitud gráfica conservadora, atestiguación interna y apoyo documental recíproco.
- Las pruebas prohíben convertir esa puntuación en probabilidad semántica, cognación, etimología o continuidad histórica.

### Integridad y release

- Generador determinista de manifiesto de release con SHA-256, tamaños y conteos.
- La CI recompone hashes y conteos de capas lexicales, canónicas, diacrónicas, TEI/Lex-0, anexos visuales y documentación de política/conformidad.
- Declaración de conformidad de implementación RHD 1.0 machine-only.
- Métrica de terminación machine-only versionada y auditable.

### Pendientes para release final

- Cerrar/verificar IIIF sobre el witness completo.
- Fijar versión, actualizar metadatos de citación, publicar release estable y depósito/identificador persistente.
- Ejecutar una segunda fuente histórica end-to-end para demostrar industrialización del núcleo RHD.

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
