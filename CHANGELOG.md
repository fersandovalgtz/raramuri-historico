# Changelog

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