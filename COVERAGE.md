# Cobertura del corpus — RHD 1.0.0

## Estado canónico

La release `v1.0.0` sustituye las métricas provisionales de las fases 0.1/0.2 por un **snapshot científico cerrado dentro del alcance machine-only**. La cobertura documental no significa validación lingüística humana: describe qué partes de la fuente fueron procesadas, cotejadas y representadas por el pipeline reproducible.

| Capa | Cantidad | Interpretación |
|---|---:|---|
| Candidatos documentales totales | **2,495** | Unidades candidatas sometidas a cotejo de límites. |
| Artículos activos | **1,965** | Arranques lexicográficos aceptados en la capa maestra. |
| Falsos límites | **530** | Candidatos rechazados pero preservados en la historia editorial. |
| Transcripciones diplomáticas IA-asistidas | **1,965 / 1,965** | Cobertura de todos los artículos activos. |
| Casos con problema explícito recotejados por PHIL | **482 / 482** | Cola machine-only agotada. |
| `confirmed_ai_assisted` | **284** | Lectura previa sostenida tras recotejo IA-asistido. |
| `corrected_ai_assisted` | **152** | Reparación documental propuesta por recotejo IA-asistido. |
| `unresolved_after_ai_recollation` | **46** | Incertidumbre explícita preservada; no se fuerza resolución. |
| Anclas curatoriales históricas | **60** | Registros semilla conservados para trazabilidad del desarrollo. |

## Extensión material

El testimonio digital de trabajo comprende **84 páginas facsimilares** vinculadas a la contribución de Steffel. La contribución impresa ocupa las pp. 293–374; el cuerpo lexicográfico comienza en la p. 301, cambia de alemán→rarámuri a rarámuri→alemán dentro de la p. 353 y da paso a los materiales anexos al final del volumen. El modelo RHD representa la dirección y el tipo documental porque esos cambios son estructuralmente relevantes.

## Qué significa «cobertura integral»

En RHD 1.0.0 significa que:

- los 2,495 candidatos documentales tienen una disposición editorial registrada;
- los 1,965 artículos activos tienen transcripción diplomática IA-asistida;
- la cola explícita de 482 problemas fue recotejada en la serie PHIL;
- los casos que no pueden resolverse de manera responsable permanecen marcados como incertidumbre;
- la fuente y las líneas OCR necesarias para reconstruir el proceso se conservan con procedencia;
- los anexos incluidos en el alcance de la release se modelaron sin fabricar contenido ausente.

No significa que cada lectura haya sido confirmada por una persona especialista ni que el corpus represente una norma lingüística contemporánea.

## Garantía contra omisiones silenciosas

RHD mantiene una capa de líneas OCR, identificadores no reutilizables, manifiestos de revisión append-only, checksums de fuente y pruebas de conteos/invariantes. Esta combinación permite distinguir tres situaciones que un simple «dataset final» ocultaría: una unidad aceptada, un candidato rechazado y una incertidumbre conservada.

Las revisiones futuras deben **añadir evidencia y estado**, no borrar la historia de cómo una lectura llegó a su forma actual.

## Cobertura interoperable

La capa canónica se proyecta a formatos derivados, incluidos CSV, JSON, XML, SQLite, TEI RHD y TEI Lex-0. La publicación IIIF Presentation 3 expone **84 Canvases** y mantiene **1,965 enlaces registro→Canvas** sin inventar regiones `xywh` cuando no existe evidencia suficiente para fijarlas.

## Capa diacrónica

Las **298 relaciones diacrónicas** de la release permanecen como `candidate`. Su existencia indica que el pipeline produjo hipótesis reproducibles y documentadas; no incrementa el número de entradas «validadas» ni demuestra continuidad histórica, identidad semántica o cognación.

## Próximas ampliaciones

Una revisión humana independiente podrá aceptar, modificar, rechazar o dejar inciertas lecturas de `v1.0.0`. Esa revisión deberá incorporarse como una capa posterior, con nueva versión y procedencia, sin reescribir retrospectivamente la naturaleza machine-only del snapshot 1.0.0.
