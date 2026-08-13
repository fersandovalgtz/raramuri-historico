# `-ugameke`: estado de la evidencia documental y estadística

**Corte:** 2026-08-13  
**Revisión humana independiente:** 0  
**Estatus:** hipótesis documental/estadística asistida por IA; no análisis morfológico validado.

## Corrección de partida

La recollación del facsímil mostró que varias formas `ugameke` recuperadas en DE–RAR corresponden a subentradas alemanas locales y no al encabezado general del artículo. Entre los casos comprobados están `Tepulirúgameke` junto a **Abgehauen**, `Hulirúgameke` junto a **Abgeſchickt**, `Polirúgameke` junto a **Bedeckt/Gedeckt**, `tſchapirúgameke` junto a **Ergriffen**, `Jolárugameke` junto a **Gemacht**, `jolarúgameke` junto a **Gethan**, `tanarúgameke` junto a **Gezeugt** y `tulchirúgameke` junto a **Zerrieben**. Por ello, los análisis actuales usan etiquetas alemanas locales y unidades token-aware.

## Comparación local corregida

La capa actual contiene 174 contextos: 67 RAR–DE directos y 107 propuestas locales DE–RAR. Con 20,000 permutaciones y semilla 1809, `ugameke` presenta 13/31 contextos con proxy superficial de participio pasado frente a 6/143 en las otras clases: **Δ = 0.377397, p = 0.00005, q = 0.00075, FWER = 0.00045**. Para cualquier forma participial, la relación es 14/31 frente a 21/143: **Δ = 0.304760, p = 0.00085, q = 0.00425, FWER = 0.00585**.

En el subconjunto conservador (RAR–DE directos + DE–RAR de bajo riesgo), `ugameke` conserva 10/25 contextos de participio pasado frente a 4/106: **Δ = 0.362264, p = 0.0001, q = 0.0015, FWER = 0.00225**.

## Asimetría documental

La señal no se reproduce de forma independiente en los 67 contextos RAR–DE directos: `ugameke` tiene 1/9 contextos participiales y no hay señal conservadora. En los 64 contextos DE–RAR de bajo riesgo, `ugameke` tiene 9/16 contextos de participio pasado frente a 4/48: **Δ = 0.479167, p = 0.0006, q = 0.009, FWER = 0.037998**.

La formulación correcta es, por tanto, una **asociación documental dentro de la microestructura DE–RAR**, no una replicación gramatical en ambas direcciones del diccionario.

## Control por artículo

Al colapsar repeticiones a 63 celdas únicas artículo × clase, `ugameke` conserva 9/16 frente a 4/47 para participio pasado: **Δ = 0.477394, p = 0.0004, q = 0.004, FWER = 0.012199**. Al restringir a 59 artículos que contienen una sola clase gráfica, conserva 8/14 frente a 4/45: **Δ = 0.482540, p = 0.0005, q = 0.005, FWER = 0.026299**.

## Sensibilidad leave-one-out

En el jackknife por artículo monoclase, la diferencia basal es **Δ = 0.482540** y, después de retirar cada artículo por separado, siempre permanece positiva: mínimo **0.449573**, máximo **0.526496**, mediana **0.480519**. En el jackknife por token, el efecto basal es **Δ = 0.424176** y todas las eliminaciones dejan la diferencia entre **0.385714 y 0.469048**.

La asociación no depende de un artículo ni de una forma aislada.

## Qué está sustentado

Bajo alineación local corregida, filtros de riesgo, control por artículo y sensibilidad leave-one-out, la clase gráfica mecánica `ugameke` está sobrerrepresentada junto a etiquetas alemanas de forma participial —especialmente de participio pasado— en la dirección DE–RAR de Steffel.

## Qué no está sustentado todavía

Estos resultados no demuestran que `-ugameke` sea un morfema ni que marque participio, resultado, voz, aspecto u otra categoría gramatical. Tampoco demuestran equivalencia estructural exacta entre la etiqueta alemana y la forma rarámuri. La distribución podría reflejar en parte una convención lexicográfica de Steffel. No existe todavía validación humana independiente.

## Formulación de trabajo recomendada

**“Asociación documental entre la clase gráfica `ugameke` y subentradas alemanas de forma participial en Steffel 1809.”**

La siguiente fase debe tratar la microestructura DE–RAR como objeto filológico: relación entre encabezado, subentrada local, forma rarámuri y recurrencia por familias léxicas antes de contrastar con gramáticas y diccionarios independientes.
