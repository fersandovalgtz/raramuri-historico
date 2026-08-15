# Preparación de release científico RHD 1.0 — Steffel

**Corte:** 15 de agosto de 2026  
**Alcance:** edición histórico-digital computacional e IA-asistida, sin intervención humana de adjudicación.  
**Estado:** prerelease científico prácticamente cerrado; todavía no declarar RHD 1.0 final.  
**Avance ponderado vigente:** **98.0%**.  
**Restante ponderado:** **2.0%**.

La política vigente es `docs/MACHINE_ONLY_SCIENTIFIC_POLICY.md`. La ausencia de revisión humana no constituye un pendiente: es una decisión metodológica explícita. Ningún artefacto puede presentar resultados IA-asistidos como `human_verified`.

## Gates científicos cerrados

### G1. Cobertura documental del cuerpo lexicográfico — cerrado

- 2,495 candidatos con disposición editorial IA-asistida;
- 1,965 artículos activos;
- 530 falsos límites preservados como historia de extracción;
- 1,965 transcripciones diplomáticas IA-asistidas;
- ningún lote automático de frontera o recotejo PHIL pendiente.

### G2. Modelo reusable RHD 1.0 — cerrado

- especificación RHD 1.0;
- JSON Schema canónico;
- perfil Steffel separado del núcleo universal;
- plantilla machine-only para fuentes futuras;
- adaptador no destructivo Steffel → RHD canonical;
- procedencia explícita para OCR, segmentación, diplomática y validación IA;
- pruebas que impiden reintroducir requisitos humanos.

### G3. TEI / TEI Lex-0 — cerrado

- TEI RHD rica separada de la proyección interoperable;
- TEI Lex-0 estricta;
- validación automatizada contra el RNG oficial TEI Lex-0 0.9.5;
- prohibición testada de fabricar `<def>` desde material no estructurado;
- suplemento TEI específico para anexos y texto paralelo;
- anexos deliberadamente fuera de Lex-0.

### G4. Recotejo e incertidumbre — cerrado

Los 482 problemas explícitos tienen estado computacional terminal:

- 284 `confirmed_ai_assisted`;
- 152 `corrected_ai_assisted`;
- 46 `unresolved_after_ai_recollation`.

`unresolved_after_ai_recollation` es un estado final legítimo. La edición no fuerza una lectura única donde la evidencia no la sostenga.

### G5. Investigación diacrónica computacional — cerrado

Las 298 relaciones Steffel ↔ Rarámuri Digital permanecen `candidate`, pero el producto de investigación machine-only está completo:

- 298 puntuaciones reproducibles de apoyo documental;
- calibración contra **5,066 emparejamientos nulos deterministas** mediante 17 desplazamientos circulares;
- informe científico machine-only reproducible;
- tabla completa de candidatos y especificidad grafémica;
- pruebas que impiden convertir el puntaje en equivalencia semántica, cognación, etimología, ley fonética o continuidad histórica.

La CI completa validó este gate repetidamente, incluido el run `31895612447` que incorpora además la ruta de publicación IIIF GitHub Pages.

### G6. Apéndices y muestra paralela — cerrado

- mapeo `PDF 79–84 ↔ impreso 369–374`;
- 24 objetos canónicos: 1 numeración + 22 fórmulas + 1 Padre Nuestro;
- numeración estructurada computacionalmente;
- 22 fórmulas alineadas por IA en latín, alemán y tarahumara;
- 66 campos paralelos con confianza explícita;
- Padre Nuestro separado y transcrito visualmente hasta `Amen.`;
- suplemento TEI específico;
- **43 lecturas residuales** registradas como incertidumbre terminal machine-only.

No queda revisión humana ni reparación conjetural pendiente.

### G9. Replicabilidad / industrialización — cerrado

La segunda fuente es **Miguel Joaquín Tellechea, _Compendio gramatical para la inteligencia del idioma tarahumar_ (1826)**. Su witness DGB está fijado como `RHD-WIT-TELLECHEA-1826-DGB`:

- 205 páginas;
- 95,088,307 bytes;
- SHA-256 `c67b7942090613c494d8057be8aff59ea13a11519c29eae469afad8a85c30dfc`.

El pipeline procesa **205/205 páginas**, valida 205 unidades documentales contra el mismo esquema RHD y genera TEI documental completa. Resultado:

- **0 rediseños del núcleo universal**;
- **0 entradas Lex-0 fabricadas**;
- **0 atribuciones humanas**.

La industrialización queda demostrada a escala completa sobre una fuente estructuralmente distinta de Steffel.

## G7. IIIF canónico — 90%, estructura y candidato público cerrados; hosting pendiente

El witness Steffel canónico fue re-verificado directamente:

- **84 páginas**;
- **6,251,443 bytes**;
- SHA-256 `4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f`.

Desde ese binario exacto RHD ya dispone de:

- huellas de las 84 páginas;
- inventario versionado de dimensiones de Canvas;
- constructor exact-binary que rechaza cualquier PDF no idéntico;
- generador determinista IIIF Presentation 3 de preparación;
- **84 Canvases** y Annotation Pages de `painting` preparados;
- `canvas-map.json` reproducible;
- **1,965/1,965 enlaces registro activo → Canvas** a nivel página;
- **0 regiones `xywh` inventadas**;
- prueba automatizada de todos esos invariantes.

Además, el proyecto ya tiene habilitado GitHub Pages en `https://fersandovalgtz.github.io/raramuri-historico/` y se preparó un perfil específico de publicación:

- `data/iiif/steffel-1809-published-png72-assets.json`: inventario de 84 PNG exact-witness con hash, bytes y dimensiones;
- `scripts/generate_steffel_public_iiif_candidate.py`: candidato Presentation 3 con la base pública definitiva;
- `tests/validate_steffel_public_iiif_candidate.py`: valida 84/84 Canvases y 1,965/1,965 enlaces públicos;
- `scripts/verify_published_steffel_iiif.py`: gate de red que sólo cierra IIIF si Manifest + 84 PNG son recuperables y coinciden con el inventario exacto.

El run **`31895612447`** pasó todos los gates deterministas: Tellechea 205/205, corpus canónico, anexos, diacronía, TEI/Lex-0, preparación IIIF interna, candidato PNG72 GitHub Pages y manifiesto de release.

La prueba de red del mismo run obtuvo **HTTP 404** en la URL final `https://fersandovalgtz.github.io/raramuri-historico/iiif/steffel-1809/manifest.json`. Esto es el comportamiento esperado mientras los archivos no estén desplegados: el gate permanece abierto sin fingir una publicación inexistente.

Por tanto, G7 no se declara todavía 100%: **lo único pendiente es colocar los 84 PNG y el Manifest/Canvas-map en Pages y obtener una verificación HTTP(S) 84/84**. Las regiones `xywh` no son requisito para cerrar el nivel página y sólo se agregarán si existen coordenadas espaciales reales.

El procedimiento de despliegue está fijado en `docs/IIIF_PUBLICATION_GITHUB_PAGES.md`. Los witnesses de Internet Archive y el enlace mutable de Dropbox siguen siendo controles externos, nunca sustitutos automáticos del witness canónico.

## G8. Release, integridad y archivo — 80%

Ya están cerrados:

- `CITATION.cff` como `0.9.0-machine-only-prerelease`;
- `CHANGELOG.md` sincronizado con el estado 98/2;
- política machine-only;
- declaración de conformidad;
- generador determinista del manifiesto de integridad;
- recomputación de SHA-256, tamaños y conteos;
- incorporación de corpus lexical, TEI/Lex-0, anexos, incertidumbre terminal, calibración diacrónica y Tellechea 205/205;
- validación integral del prerelease en CI.

Falta exclusivamente para el cierre editorial de RHD 1.0:

- fijar commit/tag definitivo;
- publicar el release estable;
- depositar datos/software en un archivo persistente;
- obtener/fijar un identificador citable apropiado;
- comprobar que la copia archivada coincide con el manifiesto de integridad.

## Métrica vigente

| Dimensión | Peso | Avance | Puntos |
|---|---:|---:|---:|
| Cobertura documental | 30 | 100% | 30.0 |
| Incertidumbre y recotejo machine-only | 20 | 100% | 20.0 |
| Arquitectura reusable | 15 | 100% | 15.0 |
| TEI / Lex-0 / IIIF | 10 | 90% | 9.0 |
| Investigación diacrónica | 10 | 100% | 10.0 |
| Apéndices | 5 | 100% | 5.0 |
| Release / archivo / citabilidad | 5 | 80% | 4.0 |
| Segunda fuente | 5 | 100% | 5.0 |
| **Total** | **100** |  | **98.0** |

## El 2% restante

Ya no corresponde a ciencia pendiente del corpus. Se concentra exclusivamente en:

1. **1 punto — publicación IIIF persistente:** desplegar y verificar Manifest + 84 PNG exact-witness en GitHub Pages. Un resultado verde de `verify_published_steffel_iiif.py` elevará la terminación a **99.0%**.
2. **1 punto — publicación final persistente:** tag/release estable + depósito/archivo con identificador citable y comprobación de integridad. Este último gate llevará la edición a **100%**.

## Condición de 100%

RHD 1.0 machine-only llegará al 100% cuando el objeto científico ya terminado sea también **públicamente persistente y citable**. No se exige ausencia de ambigüedad ni revisión humana: las incertidumbres ya están representadas explícitamente. El residual actual es de infraestructura de publicación y archivo, no de análisis científico.