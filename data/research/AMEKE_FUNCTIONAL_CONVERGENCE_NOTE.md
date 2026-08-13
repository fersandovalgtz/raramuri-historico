# Nota de convergencia funcional e histórica: `ameke` en Steffel

**Corte:** 2026-08-13  
**Estatus:** evidencia fuente-explícita + comparación diacrónica todavía no adjudicada.

## Hallazgo central en la fuente primaria

La función de `ameke` ya no debe presentarse sólo como hipótesis distribucional. En la p. impresa 353 (PDF 63), Steffel afirma que las terminaciones `ameke` designan el *Mittelwort* de tiempo presente y significado activo. En la terminología gramatical de la época, *Mittelwort* corresponde a participio. Steffel añade que en la pronunciación rarámuri se omite con frecuencia la última sílaba `ke`, aunque él decide escribirla en todas las formas de este tipo.

En el *Vorbericht* (p. 298 / PDF 8) distingue auxiliares de sentido activo (`mela`, `ruje`) y pasivo (`ruc`, `boa`, `poa`), y explica que `ruc` añadido a un verbo indica que lo expresado por éste ya ocurrió.

La p. 354 / PDF 64 proporciona una segmentación explícita de `Baſſirúgameke`: Steffel dice que allí se combinan `ruc`, de significado pasivo, y `ameke`, de significado activo, y que en la composición `baſſi + ruc + ameke` la `c` de `ruc` se convierte en `g`. Por tanto, al menos para este caso, `rugameke` procede explícitamente de `ruc + ameke` según el análisis del propio autor.

## Evidencia interna del diccionario

El inventario RAR–DE contiene diez parejas gráficas exactas `X` ↔ `X+ameke`. Una codificación AI de la relación entre las glosas alemanas —no de la semántica rarámuri— las distribuye en **7/10 expresiones de persona/participante** y **3/10 expresiones de estado/propiedad**. Entre ellas están `Bajé` «Rufen» ↔ `Bajéameke` «der Rufende», `Cotſchimé` «Schlafen» ↔ `Cotſchimeameke` «Ein Schlafender», `Cuguí` «Helfen» ↔ `Cuguíameke` «Helfer», `Neſſé` «Bewahren/Hüten» ↔ `Neſſéameke` «Hüter», `Lessí` «Ermatten, müde werden» ↔ `Lessíameke` «Müde, matt» y `Saaté` «Sand» ↔ `Saatéameke` «Sandig».

La microestructura aporta además series coherentes con la nota gramatical: `Bula, Binden` → `Buliruc, es ist gebunden` → `Bulirúgameke, Gebundenes`; `Meliruc, es ist geschlachtet/getödtet` → `Melirúgameke, Geschlachtet`; `Pagóta, Abwaschen/Taufen` → `Pagotúgameke, Ein Getaufter`; `Siká, Hauen/zerschneiden` → `Sikirúgameke, Zerhauenes`.

## Control cuantitativo y facsimilar de `rugameke`

La clase computacional `ugameke` contiene nueve formas RAR–DE directas. Un detector alemán sensible a flexión identifica **6/9** con glosa de superficie participial candidata, frente a **10/58** en el resto de las clases `-ameke` (66.7% vs. 17.2%; Δ≈.4943; permutación de 20,000 iteraciones p=.00425; Fisher p≈.004257; OR descriptiva=9.6).

Las nueve formas y sus nueve glosas fueron después recolladas por IA directamente contra el facsímil. **9/9 lecturas se confirmaron y las 6/9 glosas participiales sobreviven el control facsimilar.** Se conservaron también los tres contraejemplos (`dreyfach`, `Vollkommen`, `Schwanger`), de modo que el patrón no se formula como categórico.

Dado el análisis explícito de `Baſſirúgameke`, la etiqueta `ugameke` debe entenderse sólo como una clase gráfica heredada del pipeline. Al menos parte de sus miembros pertenece a una construcción que Steffel analiza como `ruc + ameke → rugameke`.

## Comparación moderna independiente

Caballero 2022 documenta en Choguita Rarámuri **`-ame` (PTCP)** en S12. Describe nominalizaciones agentivas, patientivas y de tema, además de usos con predicados estativos. La convergencia con Steffel es ahora doble: funcional, porque ambos materiales involucran participiales y expresiones de participante/estado; y formal, porque Steffel señala expresamente que el `ke` final de `ameke` suele omitirse en la pronunciación.

Esta convergencia es mucho más fuerte que una mera semejanza gráfica, pero **todavía no constituye una demostración comparativa de cognación o continuidad histórica** entre la variedad documentada por Steffel y el Choguita Rarámuri moderno.

## Formulación defendible para una futura publicación

**Steffel describe explícitamente `ameke` como terminación participial presente de valor activo, documenta la frecuente ausencia fonética de `ke` y analiza una formación `ruc + ameke → rugameke` con `c → g`. La distribución interna del vocabulario y los controles cuantitativos/facsimilares son coherentes con esa descripción. Una gramática moderna independiente documenta `-ame` como participial en Choguita Rarámuri. La continuidad histórica entre ambos sistemas es una hipótesis comparativa fuerte, pero aún requiere demostración filológica, dialectológica y revisión humana independiente.**

`source_explicit_historical_grammar=true`; `ai_facsimile_recollated=true`; `human_reviewed=false`; `historical_continuity_judgment=not_performed`; `cognacy_judgment=not_performed`.
