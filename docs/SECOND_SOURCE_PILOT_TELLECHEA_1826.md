# Segunda fuente piloto — Miguel Tellechea, 1826

**Estado:** witness público fijado por checksum; procesamiento end-to-end aún no iniciado.  
**No acredita todavía el gate end-to-end.**

## Por qué Tellechea

El *Compendio gramatical para la inteligencia del idioma tarahumar* de Miguel Joaquín Tellechea fue publicado en México por la Imprenta de la Federación en Palacio en 1826. Es suficientemente cercano a Steffel para mantener continuidad temática e histórica, pero estructuralmente muy distinto: no es un diccionario bidireccional, sino una obra gramatical con materiales religiosos y extensos pasajes español–tarahumara.

Esa diferencia lo vuelve una prueba más fuerte que escoger simplemente otro vocabulario con la misma forma documental de Steffel. Si RHD puede procesar Tellechea manteniendo intactos sus conceptos de witness, evidencia, capas, procedencia, identificadores, incertidumbre y exportación, tendremos una demostración mucho más convincente de que el núcleo es realmente reusable.

## Witness canónico del piloto

La Dirección General de Bibliotecas de la Secretaría de Cultura mantiene una reproducción PDF pública de la obra. El 15 de agosto de 2026 GitHub Actions recuperó directamente ese binario y fijó su identidad de manera reproducible:

- witness: `RHD-WIT-TELLECHEA-1826-DGB`;
- URI de recuperación: `https://dgb.cultura.gob.mx/recursos/documentos/lenguasindigenas/Compendiogramaticalpara.pdf`;
- tamaño: **95,088,307 bytes**;
- páginas PDF: **205**;
- versión PDF observada: **1.6**;
- SHA-256: `c67b7942090613c494d8057be8aff59ea13a11519c29eae469afad8a85c30dfc`.

La identidad queda registrada en `sources/tellechea-1826-witness.json`. La CI vuelve a descargar el PDF y exige que checksum, tamaño y número de páginas sigan siendo exactamente los mismos. Un cambio del proveedor debe aparecer como cambio de witness, no aceptarse silenciosamente.

Google Play Books y la Biblioteca Virtual de la Filología Española se conservan como referencias bibliográficas/digitales independientes. No sustituyen el witness DGB checksum-fixed.

## Diferencias que deben vivir en el perfil y no en el núcleo

Steffel organiza principalmente artículos lexicográficos. Tellechea exigirá unidades como capítulos gramaticales, ejemplos, paradigmas y bloques paralelos español–tarahumara. El núcleo RHD no debe adquirir reglas con nombres como `tellechea_paragraph` o `tellechea_prayer`; esas particularidades deben residir en `source_profiles/tellechea-1826.pilot-candidate.json` y, si hace falta, en un adaptador específico.

Los conceptos universales deben seguir siendo los mismos: witness, unidad documental, localizador, capa OCR, transcripción visual IA, derivación estructurada, procedencia, incertidumbre, relación entre unidades y exportación interoperable.

## Pipeline piloto

1. **Adquisición machine-only del witness — cerrada:** PDF público recuperado, SHA-256 fijado y verificado en CI.
2. **Cartografía documental:** detectar portada, prefación, gramática, materiales paralelos, paratextos y otras divisiones sin asumir desde el OCR que todo es equivalente.
3. **OCR/texto fuente preservado:** conservar cualquier capa textual recuperable tal como existe antes de limpieza; si el PDF carece de texto útil, producir una capa OCR machine-only separada.
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

La selección, el perfil y **la adquisición reproducible del witness ya están cerrados**. Sin embargo, el porcentaje de la dimensión “segunda fuente end-to-end” permanece en **0%** hasta que material del PDF recorra realmente extracción/OCR, segmentación, canonicalización y exportación TEI. Fijar el binario es un prerrequisito importante, pero todavía no demuestra replicabilidad del pipeline.
