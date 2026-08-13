# `-ugameke` — recollation directa contra facsímil

**Fecha:** 2026-08-13  
**Tipo de revisión:** auditoría asistida por IA contra el facsímil; **no** revisión humana independiente.

## Alcance

Se localizaron en el facsímil los **18/18** miembros `ugameke` que la capa computacional clasificaba como procedentes exclusivamente de recuperación DE–RAR. La auditoría revisó las ocurrencias impresas asociadas a esos miembros y, de manera separada, examinó los 15 contextos que el proxy formal había marcado por terminar gráficamente como un infinitivo alemán.

## Resultado documental

- **15/18** candidatos funcionan como unidades de una sola palabra bajo la recollation actual.
- **1** candidato contiene una concatenación de máquina: `gabassirugameke` corresponde en la fuente a la secuencia **`gā baſſirúgameke`**; por tanto, no debe contarse como un tipo independiente. El token final solapa con `bassirugameke`, ya documentado en RAR–DE.
- **2** candidatos son expresiones de varias palabras cuyo token final ya solapa con un miembro RAR–DE: **`Tá pagótugameke`** y **`Pouguaca jumarúgameke`**. Para análisis de terminación no deben tratarse como tipos `ugameke` independientes sin una política explícita de tokenización.
- Entre los **14** candidatos que cargaban la señal del proxy, quedan **12** tipos recuperados independientes de una palabra después de este control de unidad gráfica.

## Auditoría del proxy alemán

El proxy `infinitive_ending_proxy` era deliberadamente una señal de **forma gráfica**, no un etiquetado gramatical. La recollation lo confirma: de sus **15 contextos** dentro de los 14 miembros recuperados señalados, **11** corresponden plausiblemente a encabezados verbales de infinitivo en el contexto impreso, mientras **4** son falsos positivos funcionales de la terminación gráfica:

- `Scherben` — sustantivo;
- `Gebraten` — participio/adjetival;
- `Waizen` — sustantivo;
- `Ungewaſchen` — participio/adjetival.

Después de excluir además la unidad concatenada `gā baſſirúgameke` y la expresión no independiente `Tá pagótugameke`, quedan **10 contextos verbales plausibles distribuidos en 9 miembros recuperados de una sola palabra**. Esta cifra **no** es una nueva prueba inferencial porque el resto de los 174 contextos todavía no ha recibido una auditoría gramatical equivalente.

## Consecuencia metodológica

El resultado anterior no invalida la señal estadística original, pero sí delimita con mayor precisión qué estaba midiendo. La asociación `ugameke ↔ infinitive_ending_proxy` combinaba: a) verdaderos encabezados verbales; b) palabras alemanas no verbales terminadas gráficamente en `-en`; y c) algunos problemas de unidad/tokenización en la capa de recuperación. Por ello, cualquier nueva prueba deberá usar **unidades de token compatibles entre procedencias** y una **clasificación funcional del contexto alemán aplicada al universo completo**, no sólo a los casos `ugameke`.

## Lecturas verificadas especialmente relevantes

- p. 301: `Tepulirúgameke`, `Hulirúgameke`, `Pagorúgameke`;
- p. 308 y 312: `Polirúgameke`;
- p. 315: `tſchapirúgameke`;
- p. 320: `Guauguérúgameke`;
- p. 321: `Pagorúgameke`, `Ipagatúgameke`;
- p. 323 y 347: `Ta/Tá pagotúgameke` como expresión de varias palabras;
- p. 326–327: `gā baſſirúgameke`, con separación explícita en la fuente;
- p. 330 y 346: `Jolárugameke / jolarúgameke`;
- p. 338: `Gaſſirúgameke`, `Tſchutárugameke`;
- p. 344: `Tſchipúgameke`;
- p. 350: `holirúgameke`, `Pauguirugameke`, `Pouguaca jumarúgameke`;
- p. 352: `tanarúgameke`, `tutſchirúgameke`.

## Próximo control

Construir una capa **component-aware/token-aware** de la constelación `-ameke`, colapsando expresiones que contienen un token final ya documentado y conservando explícitamente las expresiones multipalabra. Después, auditar funcionalmente **todos** los contextos alemanes que alimentan los proxies antes de repetir las pruebas de asociación/permutación.

La revisión humana permanece en **0** y ninguna bandera de validación humana cambia como consecuencia de esta auditoría.
