# `-ugameke`: estado de la evidencia documental y estadística

**Corte:** 2026-08-13  
**Revisión humana independiente:** 0  
**Estatus:** hipótesis documental/estadística asistida por IA; no análisis morfológico validado.

## Corrección de partida

La recollación del facsímil mostró que varias formas `ugameke` recuperadas en DE–RAR corresponden a subentradas alemanas locales y no al encabezado general del artículo. Entre los casos comprobados están `Tepulirúgameke` junto a **Abgehauen**, `Hulirúgameke` junto a **Abgeſchickt**, `Polirúgameke` junto a **Bedeckt/Gedeckt**, `tſchapirúgameke` junto a **Ergriffen**, `Jolárugameke` junto a **Gemacht**, `jolarúgameke` junto a **Gethan**, `tanarúgameke` junto a **Gezeugt** y `tulchirúgameke` junto a **Zerrieben**. Por ello, los análisis actuales usan etiquetas alemanas locales y unidades token-aware.

## Comparación local corregida

La capa actual contiene 174 contextos: 67 RAR–DE directos y 107 propuestas locales DE–RAR. Con 20,000 permutaciones y semilla 1809, `ugameke` presenta 13/31 contextos con proxy superficial de participio pasado frente a 6/143 en las otras clases: **Δ = 0.377397, p = 0.00005, q = 0.00075, FWER = 0.00045**. Para cualquier forma participial, la relación es 14/31 frente a 21/143: **Δ = 0.304760, p = 0.00085, q = 0.00425, FWER = 0.00585**.

En el subconjunto conservador (RAR–DE directos + DE–RAR de bajo riesgo), `ugameke` conserva 10/25 contextos de participio pasado frente a 4/106: **Δ = 0.362264, p = 0.0001, q = 0.0015, FWER = 0.00225**.

## Microestructura DE–RAR

Al modelar explícitamente la relación `encabezado alemán → subentrada local → clase gráfica rarámuri`, 63 celdas únicas artículo×clase contienen 9 candidatos conservadores de subentrada de participio pasado perteneciente a la misma familia gráfica alemana del encabezado. Siete de esos nueve corresponden a `ugameke`: **7/16 frente a 2/47**, Δ = 0.394947, p empírica = 0.00075.

En los 59 artículos que contienen una sola clase gráfica, la relación es **7/14 frente a 2/45**, Δ = 0.455556, p = 0.0003. Restringiendo a encabezados de apariencia infinitiva, `ugameke` conserva **7/12 frente a 2/14**; en artículos monoclase con encabezado infinitivo, **7/11 frente a 2/13**. Esta capa describe una convención microestructural plausible de Steffel, no una categoría gramatical rarámuri.

## Control por artículo y sensibilidad leave-one-out

Al colapsar repeticiones a 63 celdas únicas artículo × clase, el proxy de participio pasado local conserva 9/16 para `ugameke` frente a 4/47: **Δ = 0.477394, p = 0.0004, q = 0.004, FWER = 0.012199**. Al restringir a 59 artículos que contienen una sola clase gráfica, conserva 8/14 frente a 4/45: **Δ = 0.482540, p = 0.0005, q = 0.005, FWER = 0.026299**.

En el jackknife por artículo monoclase, la diferencia basal es **Δ = 0.482540** y, después de retirar cada artículo por separado, siempre permanece positiva: mínimo **0.449573**, máximo **0.526496**, mediana **0.480519**. En el jackknife por token, el efecto basal es **Δ = 0.424176** y todas las eliminaciones dejan la diferencia entre **0.385714 y 0.469048**. La asociación no depende de un artículo ni de una forma aislada.

## Revisión de la aparente asimetría RAR–DE / DE–RAR

El proxy inicial era demasiado estrecho para la dirección RAR–DE: reconocía principalmente participios no flexionados y dejaba fuera glosas participiales nominalizadas o flexionadas. Una auditoría superficial ampliada detectó, entre las nueve formas RAR–DE directas de clase `ugameke`, seis glosas con forma participial candidata: **Gekochtes, Gebundenes, Geschlachtet, Ein Getaufter, Fortgetragenes y Zerhauenes**. La comparación es **6/9 para `ugameke` frente a 10/58 para las demás clases**, tasa 0.666667 frente a 0.172414, **Δ = 0.494253, p empírica = 0.00425** con 20,000 permutaciones.

Por tanto, la afirmación anterior de que la señal no se reproducía en RAR–DE debe matizarse: **no se reproducía con el proxy superficial estrecho; sí aparece con una auditoría que contempla flexión/nominalización participial alemana**. Este segundo resultado sigue siendo una heurística de forma, no etiquetado POS validado, y requiere revisión filológica humana antes de usarse como evidencia lingüística fuerte.

## Qué está sustentado

Bajo alineación local corregida, filtros de riesgo, control por artículo, sensibilidad leave-one-out y una auditoría específica de formas alemanas flexionadas, la clase gráfica mecánica `ugameke` está sobrerrepresentada junto a expresiones alemanas de apariencia participial en ambas direcciones documentales del diccionario, aunque los mecanismos de observación difieren entre DE–RAR y RAR–DE.

## Qué no está sustentado todavía

Estos resultados no demuestran que `-ugameke` sea un morfema ni que marque participio, resultado, voz, aspecto u otra categoría gramatical. Tampoco demuestran equivalencia estructural exacta entre la expresión alemana y la forma rarámuri. Los clasificadores alemanes son heurísticas de superficie y no sustituyen una revisión filológica o gramatical independiente. No existe todavía validación humana independiente.

## Formulación de trabajo recomendada

**“Asociación documental reproducible entre la clase gráfica `ugameke` y contextos alemanes de apariencia participial en las dos direcciones del diccionario de Steffel, con evidencia especialmente clara en la microestructura DE–RAR y en glosas RAR–DE flexionadas/nominalizadas.”**

La siguiente fase debe revisar manualmente las glosas alemanas candidatas, caracterizar la convención lexicográfica de Steffel y contrastar después el patrón con gramáticas y diccionarios independientes.
