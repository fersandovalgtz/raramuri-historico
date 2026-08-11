# Procedencia

La fuente primaria de trabajo es el PDF facsimilar y el TXT OCR suministrados al proyecto el 11 de agosto de 2026. El OCR textual se conserva sin modificación en `sources/steffel-1809-ocr-source.txt`; `sources/checksums.json` registra las huellas SHA-256 del PDF y del TXT de origen. El repositorio puede enlazar el facsímil externo en lugar de duplicar necesariamente el binario.

La obra corresponde al *Tarahumarisches Wörterbuch* de Matthäus Steffel, compilado/fechado en 1791 y publicado en 1809 dentro de la compilación de Christoph Gottlieb von Murr. El facsímil de trabajo tiene 84 páginas; la paginación impresa relevante para el diccionario corre de 301 a 374.

La versión 0.2.0 procesa todo el rango de ambos diccionarios del OCR y conserva las líneas de evidencia. `data/entries.csv` es una segmentación automática de alta cobertura; `data/entries_curated.csv` conserva 60 anclas previamente trabajadas. Ningún candidato automático se presenta como transcripción diplomática ni como validación lingüística.

La traducción española de la edición crítica de la Universidad de Sonora no se reutiliza como dato del corpus. Se consulta como bibliografía y edición crítica independiente, respetando su licencia.
