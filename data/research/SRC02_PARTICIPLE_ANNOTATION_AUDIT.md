# SRC-02 — auditoría de evidencia participial explícita

**Fecha:** 2026-08-13. **Estatus:** análisis documental IA-asistido; revisión humana pendiente.

## Hallazgo principal

La distribución gráfica moderna en `-ami` no debe confundirse con una categoría gramatical única. En el corte fijado de SRC-02 hay **214 registros finales en `-ami`**, pero sólo **20** están clasificados explícitamente como `Pp`. El léxico completo contiene **40 registros clasificados `Pp`**. Por consiguiente, la mitad de los registros que la fuente clasifica como `Pp` cae en la clase gráfica final `-ami`, mientras que la gran mayoría de las formas finales en `-ami` está clasificada de otra manera.

Esto no reduce la importancia de `-ami`; al contrario, permite separar tres niveles que antes podían confundirse: **forma superficial**, **clasificación explícita de la fuente** y **relación derivacional inferida por comparación semántica**.

## La clasificación `Pp` también subestima la evidencia participial explícita

Hay formas cuyo registro derivado no está clasificado `Pp`, pero cuya entrada verbal base las identifica expresamente como participios. Un caso especialmente claro es `Bicá` ‘pudrir’, cuya nota da `pp.: bicáami`; el registro independiente `Bicáami` significa ‘podrido’, aunque aparece sin clasificación `Pp`. Por tanto, contar únicamente las filas etiquetadas `Pp` subestima las relaciones participiales que la propia fuente documenta.

`Comíami` proporciona el caso contrario y más fuerte: la entrada está clasificada `Pp` y otra entrada de la misma familia vuelve a identificarla explícitamente como `pp: comíami`. Aquí convergen dos mecanismos independientes de anotación de SRC-02.

También aparecen participios simples y transparentes como `Cochí` ‘dormir’ → `cochíami` (`pp.`) y `Cusé` ‘tocar la flauta’ → `cuséami` (`pp.`). Estos ejemplos demuestran directamente que una formación superficial en `-ami` puede recibir análisis participial explícito en la fuente moderna.

## Contraejemplo decisivo: `-ami` no equivale mecánicamente a `Pp`

La entrada `Hua` ‘madurarse’ contiene una distinción interna extraordinariamente útil: **`ad.: huáami; pp.: huacami`**. El registro `Huácami` aparece además como ‘maduro’ y se remite a ese participio. La propia fuente, dentro de una sola familia léxica, distingue una forma en `-ami` etiquetada como adjetiva de otra forma en `-cami` identificada como participio.

Este contraste impide sostener una regla del tipo “toda forma final en `-ami` es un participio”. A la vez, confirma que `-ami` forma parte de un espacio morfológico donde sí hay participios, junto con otras realizaciones como `-cami`, `-rami`, `-tami`, `-huami` y estructuras más complejas.

## Efecto sobre los candidatos diacrónicos prioritarios

### `Tſchiperameke ~ Chipérami`

`Chipérami` ‘plano’ está clasificado directamente como `Pp` en SRC-02. Este dato refuerza de forma sustancial el componente morfológico del candidato histórico-moderno: ya no depende solamente de semejanza gráfica y coincidencia semántica.

### `Tſchócameke ~ Chócami`

`Chócami` ‘negro’ está clasificado como adjetivo, no como `Pp`. Cerca existe una familia distinta `Chocó` ‘estar agrio’ → `chocóami` identificada explícitamente como participial. En consecuencia, `Tſchócameke ~ Chócami` puede mantenerse como candidato léxico/grafemático, pero **no debe utilizarse como evidencia moderna explícita de participio** mientras no aparezca una fuente adicional que lo justifique.

### `Seliameke ~ Siríami`

`Siríami` ‘gobernador tradicional’ está clasificado como sustantivo, no como `Pp`. Su fuerza comparativa procede de la coincidencia institucional con Steffel y de la documentación independiente de Choguita `siˈríame` ‘governor(s)’. La etiqueta sustantiva de SRC-02 es compatible con una forma lexicalizada, pero la lexicalización no se declara aquí como hecho histórico demostrado.

### `Neſſéameke ~ Niséami`

`Niséami` ‘pastor’ también está clasificado como sustantivo. La fuerza del par continúa radicando en la relación moderna `Nisé` ‘cuidar, pastorear’ → `Niséami` ‘pastor’ y en la evidencia histórica `Neſſé` ‘guardar/cuidar’ → `Neſſéameke` ‘guardián’, incluida la atestación especializada ‘pastor de ovejas’. No se presenta la etiqueta `Pp` como argumento porque SRC-02 no la proporciona para `Niséami`.

## Consecuencia para el modelo diacrónico

El modelo de trabajo debe ser **estratificado**. El nivel 1 es gráfico: formas finales en `-ami`. El nivel 2 es fuente-explícito: formas que SRC-02 clasifica o identifica como `Pp`. El nivel 3 es derivacional-semántico: pares cuya relación base→derivado es transparente aunque la fuente no los marque `Pp`. El nivel 4 es comparativo-diacrónico: candidatos históricos-modernosh que requieren correspondencias fonológicas, semánticas y dialectales independientes.

Esta arquitectura reduce falsos positivos y, al mismo tiempo, hace más fuerte cualquier candidato que sobreviva a los cuatro niveles.

## Nota metodológica sobre búsquedas textuales

Las búsquedas literales de marcadores como `pp.:` dentro del CSV bruto no deben contarse directamente como “entradas participiales”, porque una misma nota puede aparecer serializada en más de una columna. Por esa razón, esta auditoría utiliza el campo de clasificación para conteos de registros únicos y emplea las notas `pp.` como evidencia cualitativa/familiar, no como un conteo bruto equivalente a entradas únicas.

`ai_assisted=true`; `human_reviewed=false`; `automatic_morpheme_assignment=false`; `automatic_lexicalization_judgment=false`; `cognacy_judgment=not_performed`; `historical_continuity_judgment=not_performed`.
