# Reproducibilidad — Rarámuri Histórico Digital

## Objetivo

RHD busca que una persona investigadora pueda reconstruir la relación entre **fuente, código, decisiones editoriales y artefactos derivados** sin depender de una explicación oral del autor. Reproducibilidad no significa que una revisión humana deba llegar a la misma interpretación; significa que el proceso computacional, sus insumos y sus transformaciones estén suficientemente especificados para ser auditados.

## Snapshot canónico

La referencia científica estable es la release `v1.0.0`, asociada al commit:

`441cbac036d82e83451e32378a030c3bb0923bf6`

Las métricas o resultados citados de esa versión deben compararse contra el snapshot versionado, no contra el estado futuro de `main`.

## Insumos y fijación

- Fuente bibliográfica: Steffel 1809, documentada en `docs/STEFFEL_SOURCE.md`.
- OCR fuente preservado: `sources/steffel-1809-ocr-source.txt`.
- Hashes de insumos: `sources/checksums.json`.
- SHA-256 del testimonio canónico documentado para v1.0.0: `4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f`.
- Procedencia: `PROVENANCE.md`.

## Pipeline principal

Los scripts individuales tienen funciones específicas y deben ejecutarse desde un checkout limpio de la versión que se quiere reproducir. La secuencia de alto nivel utilizada por RHD incluye:

```bash
python3 scripts/extract_full_corpus.py
python3 scripts/apply_review_overrides.py
python3 scripts/generate_review_queue.py
python3 scripts/generate_validation_queue.py
python3 scripts/generate_next_philological_batch.py
python3 scripts/generate_human_review_priority.py
python3 scripts/generate_exports.py
python3 scripts/generate_de_rar_attestations.py
python3 scripts/generate_internal_concordance.py
python3 scripts/generate_historical_variants.py
python3 scripts/generate_semantic_context_queue.py
python3 scripts/generate_graphemic_statistics.py
python3 scripts/generate_research_statistics.py
python3 scripts/generate_research_snapshot.py
python3 scripts/sync_research_metadata.py
python3 tests/validate.py
python3 tests/validate_validation_phase.py
```

No todos los artefactos científicos dependen necesariamente de cada script de esta lista. La lógica de dependencias debe consultarse en el código y documentación específicos del artefacto que se quiera reconstruir.

## Clases de reproducibilidad

### Determinista

Procesos que, con los mismos archivos de entrada, versión de código y parámetros, deben producir el mismo resultado estructural. Los tests y hashes son apropiados para estas capas.

### IA-asistida con evidencia congelada

Las fases históricas que utilizaron asistencia de IA no deben simularse como si la reproducción exacta de una llamada externa fuera requisito de validez. RHD conserva **el resultado, su estado, la evidencia documental y los manifiestos de decisión**. La reproducibilidad relevante consiste en poder auditar cómo ese resultado se incorporó al snapshot y qué autoridad se le asignó.

### Revisión humana

Una revisión humana es replicable como procedimiento —mismo testimonio, protocolo, registro y criterios— pero puede producir desacuerdo experto legítimo. RHD debe conservar ese desacuerdo en vez de forzar identidad de decisiones.

## Invariantes críticos

Una reconstrucción compatible con `v1.0.0` debe preservar, en el alcance de esa release, entre otros:

- 2,495 candidatos documentales con disposición;
- 1,965 artículos activos;
- 530 falsos límites;
- 1,965 transcripciones diplomáticas IA-asistidas;
- 482 casos PHIL terminales distribuidos en 284 / 152 / 46;
- 84 IIIF Canvases;
- 1,965 enlaces registro→Canvas;
- 298 relaciones diacrónicas con estado `candidate`.

Una divergencia no es automáticamente un error: puede indicar que se está ejecutando otra versión. Por eso todo reporte debe incluir tag o commit.

## Entorno

El repositorio utiliza principalmente Python y contiene además componentes JavaScript, HTML, CSS y SQL. Para resultados destinados a publicación, registre como mínimo:

- sistema operativo;
- versión de Python;
- commit/tag;
- dependencias relevantes;
- comandos ejecutados;
- parámetros o semillas cuando existan;
- hashes de insumos críticos.

Si una dependencia externa modifica su comportamiento, el resultado debe compararse con el snapshot versionado y documentarse la desviación.

## CI y releases

GitHub Actions funciona como control automatizado de invariantes y como gate para procesos de release. Una ejecución verde confirma los tests codificados en ese workflow; **no equivale a revisión filológica o lingüística humana**.

La evidencia de creación de `v1.0.0` está registrada en `docs/GITHUB_RELEASE_EVIDENCE_V1.0.0.json`.

## Archivo persistente

La reproducibilidad a largo plazo requiere más que un repositorio vivo. Cuando el depósito de `v1.0.0` en Zenodo quede verificado, este documento deberá registrar el DOI y la correspondencia entre:

`DOI ↔ release ↔ commit ↔ hashes ↔ artefactos`.

## Reporte de discrepancias

Si una persona no puede reproducir un conteo o artefacto:

1. confirme tag/commit;
2. confirme hashes de insumos;
3. ejecute los tests de validación;
4. registre entorno y comandos;
5. abra un issue con la diferencia observada y el resultado esperado.

Las discrepancias bien documentadas son información científica útil y no deben ocultarse.
