# Declaración de conformidad científica — RHD 1.0 machine-only / Steffel

**Fecha de corte:** 15 de agosto de 2026  
**Objeto:** Corpus Steffel 1791/1809 como implementación de referencia de Rarámuri Histórico Digital.

## Declaración

La implementación satisface actualmente los requisitos internos de **RHD 1.0 machine-only** para preservación no destructiva de evidencia, identificación persistente, separación de capas, procedencia, incertidumbre explícita, canonicalización reproducible e interoperabilidad lexicográfica básica.

Esta declaración **no certifica revisión humana**, validación comunitaria, norma ortográfica contemporánea, equivalencia semántica histórica, cognación, etimología ni continuidad lingüística.

## Conformidades comprobables

### Evidencia y capas

- El OCR fuente se conserva como evidencia y no es sustituido por la diplomática.
- La transcripción diplomática es una capa derivada IA-asistida.
- Las decisiones PHIL son eventos append-only y no reescriben silenciosamente la evidencia anterior.
- `unresolved_after_ai_recollation` se conserva como estado terminal legítimo cuando no hay base suficiente para escoger una lectura.
- Normalización y formas de búsqueda se mantienen separadas de la grafía documental.

### Identidad y procedencia

- Cada registro lexical activo tiene `record_id` persistente.
- El modelo canónico conserva localizadores y eventos de procedencia.
- Los perfiles específicos de fuente están separados del núcleo RHD.
- Existe una plantilla de perfil para nuevas fuentes.

### Interoperabilidad

- Existe TEI RHD rica para representar capas documentales y epistemológicas propias del proyecto.
- Existe una proyección TEI Lex-0 deliberadamente estrecha y separada.
- La proyección Lex-0 se valida automáticamente en GitHub Actions contra el RNG oficial TEI Lex-0 0.9.5.
- Los anexos documentales no se fuerzan dentro de Lex-0.

### Anexos

- El tramo facsimilar final está mapeado como `PDF 79–84 ↔ impreso 369–374` mediante cotejo visual IA.
- Existen 24 objetos canónicos de anexo: 1 sección numérica, 22 fórmulas y 1 Padre Nuestro.
- La secuencia de las 22 fórmulas y la separación del Padre Nuestro se preservan.
- Ningún objeto de anexo afirma validación humana.

### Investigación diacrónica

- Las 298 relaciones Steffel ↔ Rarámuri Digital permanecen `candidate`.
- Existe puntuación reproducible de apoyo documental de recuperación.
- Las pruebas prohíben convertir esa puntuación en probabilidad semántica, cognación, etimología o continuidad histórica.

### Integridad

- Existe un generador determinista de manifiesto de release.
- El manifiesto incluye SHA-256 y tamaño de artefactos nucleares.
- La CI recomputa los hashes, tamaños y conteos y falla ante divergencias.

## No conformidades / requisitos aún abiertos

La presente declaración es de **conformidad de implementación**, no de release 1.0 final. Permanecen abiertos:

- cierre de la transcripción/alineación IA de los anexos paralelos;
- publicación/verificación IIIF del witness completo;
- release estable, archivo e identificador persistente;
- prueba de replicación completa con una segunda fuente histórica real.

## Regla de citación metodológica

Al describir el corpus deben preferirse expresiones como:

> edición histórico-digital computacional e IA-asistida; transcripción diplomática IA-asistida; cotejo visual IA; relaciones diacrónicas candidatas; incertidumbre explícita.

No deben utilizarse expresiones como “edición crítica revisada por especialistas”, “validada por hablantes” o equivalentes mientras tales procedimientos no formen parte del alcance y de la evidencia del proyecto.
