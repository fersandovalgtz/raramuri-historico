# Segunda fuente piloto — Miguel Tellechea, 1826

**Estado:** fuente seleccionada para prueba de replicabilidad; witness exacto aún no fijado.  
**No acredita todavía el gate end-to-end.**

## Por qué Tellechea

El *Compendio gramatical para la inteligencia del idioma tarahumar* de Miguel Joaquín Tellechea fue publicado en México por la Imprenta de la Federación en Palacio en 1826. Es suficientemente cercano a Steffel para mantener continuidad temática e histórica, pero estructuralmente muy distinto: no es un diccionario bidireccional, sino una obra gramatical con materiales religiosos y extensos pasajes español–tarahumara.

Esa diferencia lo vuelve una prueba más fuerte que escoger simplemente otro vocabulario con la misma forma documental de Steffel. Si RHD puede procesar Tellechea manteniendo intactos sus conceptos de witness, evidencia, capas, procedencia, identificadores, incertidumbre y exportación, tendremos una demostración mucho más convincente de que el núcleo es realmente reusable.

## Evidencia bibliográfica y acceso digital

Se han localizado al menos dos referencias digitales públicas útiles para adquisición/control bibliográfico:

- Google Play Books identifica una reproducción gratuita de 172 páginas con ID `b9BTAAAAcAAJ`.
- La Biblioteca Virtual de la Filología Española registra la edición de 1826 y distintos ejemplares institucionales.

Ninguna de esas referencias se convierte automáticamente en witness RHD. Primero debe seleccionarse un binario o servicio de imágenes reproducible y fijar su identidad con checksum/URI estable.

## Diferencias que deben vivir en el perfil y no en el núcleo

Steffel organiza principalmente artículos lexicográficos. Tellechea exigirá unidades como capítulos gramaticales, ejemplos, paradigmas y bloques paralelos español–tarahumara. El núcleo RHD no debe adquirir reglas con nombres como `tellechea_paragraph` o `tellechea_prayer`; esas particularidades deben residir en `source_profiles/tellechea-1826.pilot-candidate.json` y, si hace falta, en un adaptador específico.

Los conceptos universales deben seguir siendo los mismos: witness, unidad documental, localizador, capa OCR, transcripción visual IA, derivación estructurada, procedencia, incertidumbre, relación entre unidades y exportación interoperable.

## Pipeline piloto

1. **Adquisición machine-only del witness:** obtener un PDF/imágenes legalmente accesibles, calcular SHA-256, registrar metadatos y conservar el binario fuera de Git cuando corresponda.
2. **Cartografía documental:** detectar portada, prefación, gramática, materiales paralelos, paratextos y otras divisiones sin asumir desde el OCR que todo es equivalente.
3. **OCR preservado:** conservar OCR bruto y sus errores antes de cualquier limpieza.
4. **Segmentación jerárquica:** generar candidatos de sección, párrafo, paradigma/ejemplo y bloque paralelo.
5. **Cotejo visual IA:** adoptar/rechazar fronteras y producir lectura documental con incertidumbre explícita.
6. **Canonicalización:** representar las unidades con IDs `RHD-T1826-#####` y procedencia comparable a Steffel.
7. **Paralelismo:** alinear español–tarahumara donde la disposición impresa lo justifique; no fabricar equivalencia cuando la relación sea discursiva y no frase-a-frase.
8. **TEI:** generar una proyección documental adecuada; **no** forzar materiales gramaticales/paralelos dentro de Lex-0.
9. **Comparación con RHD core:** registrar cada modificación requerida al núcleo y clasificarla como bug general, capacidad universal faltante o peculiaridad que debe permanecer en el perfil.
10. **CI:** reproducir el pipeline desde evidencia hasta salidas derivadas y verificar que ninguna fase fabrique revisión humana.

## Prueba mínima y prueba fuerte

La **prueba mínima** consiste en hacer atravesar de extremo a extremo al menos una sección gramatical completa y una sección paralela español–tarahumara. Sirve para detectar temprano si el modelo falla fuera del diccionario.

La **prueba fuerte**, necesaria para cerrar el gate de industrialización, es procesar el witness completo declarado para el piloto y demostrar que los cambios al núcleo fueron nulos o conceptualmente generales. El objetivo no es que Tellechea se parezca a Steffel; es que ambos puedan expresarse mediante el mismo sistema científico-digital.

## Estado actual

La selección y el perfil de Tellechea están preparados, pero **el porcentaje de la dimensión “segunda fuente end-to-end” permanece en 0%** hasta que exista witness checksum-fixed y datos realmente procesados. Esta regla evita inflar el avance por trabajo puramente preparatorio.
