# Capa de correspondencias diacrónicas

Esta carpeta modela relaciones explícitas entre **Rarámuri Histórico Digital — Corpus Steffel 1791/1809** y **Rarámuri Digital**. La separación entre ambos corpus es deliberada: ninguna correspondencia fusiona ni reemplaza formas documentales.

## Fuente contemporánea de referencia

La fuente de comparación es `fersandovalgtz/raramuri-digital`, conjunto de datos 1.0.0. La entidad canónica contemporánea usa identificadores persistentes `RD-######` y conserva por separado `headword`, `headword_raw` y `headword_normalized`. Para reproducibilidad, el registro queda fijado al commit `156921f4edfe27d784edc1e6444867eaa368f2e5` y al archivo `data/lexicon-master.csv`.

## Unidad de relación

Una correspondencia es una **hipótesis trazable entre dos entidades**, no una equivalencia lingüística automática. Conserva el identificador histórico `RHD-S1809-#####`, forma diplomática y página, el identificador contemporáneo `RD-######`, forma contemporánea fuente y normalizada, tipo de relación propuesto, método de generación, evidencia documental disponible y estado de revisión independiente.

## Cohorte 1: coincidencia gráfica exacta

`exact_graphic_candidates.json` contiene la primera cohorte automática. Compara componentes rarámuri de la sección RAR–DE de Steffel con componentes de `headword` del corpus contemporáneo mediante una clave gráfica conservadora. El corte reproducible actual contiene **50 relaciones candidatas**, correspondientes a **36 registros históricos**, **48 registros contemporáneos** y **35 claves gráficas distintas**.

El tipo de relación es `exact_normalized_graphic_match`. La normalización se usa sólo como clave documental: Unicode NFKD, eliminación de marcas combinantes, `ſ→s`, `ß→ss`, minúsculas, unificación de variantes gráficas de apóstrofos y guiones y colapso de espacios. No se aplican equivalencias fonológicas, morfológicas o dialectales.

Una coincidencia exacta de forma no demuestra continuidad semántica. El corpus conserva por ello la glosa histórica y la traducción contemporánea junto con el candidato y mantiene `human_reviewed=false` hasta una adjudicación independiente.

## Cohorte 2: correspondencia gráfica probable

`probable_graphic_candidates.json` contiene una segunda cohorte, separada de las coincidencias exactas. El corte actual produce **248 relaciones candidatas**, distribuidas en **124 registros históricos**, **126 componentes históricos** y **185 registros contemporáneos**. De las 248 relaciones, **247 tienen distancia de edición 1** y **1 tiene distancia 2**.

El tipo de relación es `probable_graphic_correspondence`. El método `conservative_bounded_edit_distance_v1` exige componente de al menos cuatro caracteres, misma inicial gráfica, exclusión de coincidencias exactas ya presentes en la cohorte 1, distancia de Levenshtein máxima 1 para claves de longitud 4–8, distancia máxima 2 únicamente para claves de longitud 9 o mayor y similitud proporcional mínima de 0.80, y máximo de tres candidatos contemporáneos por componente histórico.

Estas restricciones reducen el espacio de búsqueda sin introducir una teoría fonológica o histórica. Un candidato puede ser gráficamente cercano y, sin embargo, carecer de relación semántica o etimológica. Por ello esta cohorte es una **cola de revisión**, no una lista de cognados o continuidades léxicas.

## Cola de adjudicación independiente

`adjudication_queue.json` integra las dos cohortes sin fusionarlas y ordena las **298 hipótesis documentales** para revisión humana. El corte actual representa **137 registros históricos** y **221 registros contemporáneos**. Las 298 relaciones conservan contexto semántico histórico y contemporáneo disponible para lectura humana, pero el sistema no realiza comparación semántica automática.

La prioridad actual se distribuye en cuatro niveles: **21 candidatos de nivel 1**, **32 de nivel 2**, **244 de nivel 3** y **1 de nivel 4**. El nivel 1 reserva las coincidencias exactas más fuertes: forma no corta y correspondencia única en la clave gráfica exacta. El resto de las coincidencias exactas pasa al nivel 2, junto con los casos probables excepcionalmente fuertes; la mayor parte de las correspondencias por distancia de edición queda en nivel 3 y el único caso de distancia 2 queda en nivel 4.

La puntuación usa únicamente propiedades documentales y de organización de la revisión: fuerza de la cohorte gráfica, distancia/similitud cuando corresponde, multiplicidad de candidatos para un componente histórico, advertencia de forma corta, disponibilidad de glosas/contextos para revisión y estado de transcripción de la entrada moderna. **No calcula similitud semántica, cognación ni continuidad histórica.**

Cada registro recibe un identificador `RHD-ADJ-######` y conserva campos independientes para revisor, afiliación, ORCID, fecha, decisión, tipo de relación adoptado, relación semántica, continuidad histórica, confianza, evidencia y nota. Todos permanecen inicialmente como `human_reviewed=false` y `not_assessed`.

## Tipos de relación candidatos

- `exact_normalized_graphic_match`: coincidencia de claves normalizadas mediante una regla documental explícita; no implica identidad semántica.
- `probable_graphic_correspondence`: semejanza gráfica acotada suficiente para revisión; no implica correspondencia fonológica ni histórica.
- `semantic_correspondence_candidate`: la evidencia de glosa sugiere relación y requiere juicio lingüístico.
- `historical_variant_candidate`: posible relación histórica/ortográfica que requiere análisis especializado.
- `no_supported_match`: revisión explícita sin correspondencia aceptable.
- `uncertain`: evidencia insuficiente o contradictoria.

Los tipos anteriores describen **candidatos**. Una relación sólo puede adquirir `human_reviewed=true` mediante una decisión independiente documentada.

## Política de normalización y no sobrescritura

Toda clave de comparación coexiste con la forma histórica diplomática y la forma contemporánea fuente. Esta capa nunca sobrescribe `headword_diplomatic`, `article_diplomatic`, el facsímil, el historial PHIL ni los registros `RD-######` de Rarámuri Digital.

Las capas diacrónicas tampoco autorizan automáticamente etiquetas de cognación, continuidad, cambio semántico, identidad dialectal o equivalencia normativa. Esas interpretaciones requieren revisión especializada y evidencia explícita.

## Flujo científico

La secuencia es: generar candidatos documentales; conservar homónimos y alternativas por separado; priorizar la revisión sin adjudicar el contenido; revisar forma, sentido, contexto y fuente; registrar aceptación, modificación, rechazo o incertidumbre; y sólo después construir análisis de continuidad/cambio léxico, ortográfico o semántico.

## Artefactos reproducibles

- `source_registry.json`: versiones y commits fijados de los corpus comparados.
- `correspondence_schema.json`: contrato de datos de la relación diacrónica.
- `correspondence_template.json`: plantilla de adjudicación de una correspondencia.
- `exact_graphic_candidates.json` / `.csv`: cohorte 1 completa.
- `exact_graphic_candidates_summary.json`: resumen cuantitativo de cohorte 1.
- `probable_graphic_candidates.json` / `.csv`: cohorte 2 completa.
- `probable_graphic_candidates_summary.json`: resumen cuantitativo de cohorte 2.
- `adjudication_queue.json` / `.csv`: cola integrada y priorizada de las 298 hipótesis.
- `adjudication_queue_summary.json`: conteos de la cola y niveles de prioridad.
- `ADJUDICATION_REVIEW_INDEX.md`: índice legible para revisión sistemática.
- `scripts/generate_diachronic_correspondences.py`: generador determinista de coincidencias exactas.
- `scripts/generate_probable_graphic_correspondences.py`: generador determinista de correspondencias gráficas probables.
- `scripts/generate_diachronic_adjudication_queue.py`: generador determinista de la cola de adjudicación.

GitHub Actions reconstruye las dos cohortes y la cola de adjudicación contra el snapshot contemporáneo fijado y valida identificadores, duplicados, separación entre cohortes, límites de candidatos, orden de prioridad y estados de revisión. Todas las relaciones permanecen con revisión humana igual a cero hasta que exista adjudicación independiente documentada.
