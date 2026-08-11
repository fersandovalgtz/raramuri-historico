# Cobertura del corpus

## Versión 0.2.0

La versión 0.2.0 sustituye el modelo de muestra limitada por una **capa de cobertura integral del rango lexicográfico** del OCR de Steffel suministrado al proyecto.

| Capa | Cantidad | Interpretación |
|---|---:|---|
| Candidatos lexicográficos totales | 2,495 | Límites de artículo detectados por segmentación de alta cobertura. |
| Alemán → rarámuri | 1,607 | Candidatos dentro del primer diccionario. |
| Rarámuri → alemán | 888 | Candidatos dentro del diccionario inverso. |
| Anclas curadas | 60 | Registros semilla con identificador histórico preservado. |
| `high_machine` | 609 | Señales de inicio relativamente fuertes; aún sin cotejo. |
| `medium_machine` | 1,110 | Señales intermedias; requiere revisión. |
| `low_machine` | 716 | Candidato conservado por política de máxima cobertura. |

## Qué significa “completo” en esta etapa

“Completo” significa que el pipeline procesa **todo el tramo lexicográfico de ambas direcciones** y conserva también todas sus líneas OCR en `data/ocr_dictionary_lines.csv`; ya no selecciona únicamente 60 ejemplos. No significa que 2,495 sea el número crítico definitivo de artículos ni que cada frontera automática sea correcta.

La unidad documental puede quedar fragmentada por OCR, columnas, guiones de final de línea o encabezados. Durante el cotejo facsimilar algunos candidatos se fusionarán, otros se rechazarán y pueden aparecer fronteras que la extracción automática no individualizó. Esas decisiones se registrarán sin borrar la evidencia previa y sin reciclar identificadores.

## Garantía contra omisiones silenciosas

Además de `data/entries.csv`, el repositorio conserva una tabla de las líneas no vacías de ambos rangos lexicográficos con página y dirección. Esto permite auditar cualquier candidato faltante directamente contra el OCR fuente y reconstruir el proceso de segmentación.
