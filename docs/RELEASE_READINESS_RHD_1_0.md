# Preparación de release científico RHD 1.0 — Steffel

**Corte:** 15 de agosto de 2026  
**Alcance:** edición histórico-digital computacional e IA-asistida, sin intervención humana de adjudicación.  
**Estado:** candidato estable 1.0.0; IIIF público cerrado; archivo/DOI persistente pendiente.  
**Avance ponderado vigente:** **99.0%**.  
**Restante ponderado:** **1.0%**.

La política vigente es `docs/MACHINE_ONLY_SCIENTIFIC_POLICY.md`. La ausencia de revisión humana no constituye un pendiente: es una decisión metodológica explícita. Ningún artefacto puede presentar resultados IA-asistidos como `human_verified`.

## Gates cerrados

### G1. Cobertura documental — cerrado

- 2,495 candidatos con disposición editorial IA-asistida;
- 1,965 artículos activos;
- 530 falsos límites preservados como historia de extracción;
- 1,965 transcripciones diplomáticas IA-asistidas;
- ningún lote automático pendiente.

### G2. Modelo reusable RHD 1.0 — cerrado

Especificación RHD 1.0, JSON Schema, perfil Steffel, plantilla reusable, adaptador no destructivo y procedencia explícita están implementados y probados.

### G3. TEI / TEI Lex-0 — cerrado

La TEI RHD rica permanece separada de la proyección TEI Lex-0 estricta; la proyección valida contra el RNG oficial TEI Lex-0 0.9.5 y las pruebas impiden fabricar `<def>` donde la fuente no lo justifica.

### G4. Recotejo e incertidumbre — cerrado

Los 482 problemas explícitos tienen estado computacional terminal: 284 `confirmed_ai_assisted`, 152 `corrected_ai_assisted` y 46 `unresolved_after_ai_recollation`. La incertidumbre es una salida científica legítima.

### G5. Investigación diacrónica computacional — cerrado

Las 298 relaciones Steffel ↔ Rarámuri Digital permanecen `candidate`, con puntuación documental reproducible, calibración contra 5,066 emparejamientos nulos deterministas e informe/tablas machine-only. No se convierten automáticamente en afirmaciones semánticas, cognadas, etimológicas o de continuidad histórica.

### G6. Apéndices — cerrado

Mapeo `PDF 79–84 ↔ impreso 369–374`, 24 objetos canónicos —numeración, 22 fórmulas y Padre Nuestro— y 43 incertidumbres terminales explícitas.

### G7. IIIF canónico — cerrado al 100%

El witness Steffel canónico permanece fijado como 84 páginas, 6,251,443 bytes y SHA-256 `4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f`.

GitHub Pages publica el paquete IIIF Presentation 3 con 84 Canvases y 1,965 enlaces registro→Canvas, sin `xywh` inventado. Después de la fusión del PR #2, el pipeline canónico de `main` completó con éxito el paso **Verify published canonical Steffel IIIF endpoint if available**. Por tanto el gate de publicación IIIF queda cerrado.

### G9. Replicabilidad / industrialización — cerrado

Tellechea 1826 está fijado como `RHD-WIT-TELLECHEA-1826-DGB`: 205 páginas, 95,088,307 bytes, SHA-256 `c67b7942090613c494d8057be8aff59ea13a11519c29eae469afad8a85c30dfc`. El pipeline procesa 205/205 páginas con 0 rediseños del núcleo universal, 0 entradas Lex-0 fabricadas y 0 atribuciones humanas.

## G8. Release, integridad y archivo — parcialmente cerrado

Ya están cerrados:

- política machine-only y declaración de conformidad;
- licencia definitiva: software MIT; datos/metadatos/capas editoriales originales RHD CC BY 4.0;
- manifiesto determinista de integridad;
- CI integral sobre corpus, Tellechea, anexos, diacronía, TEI/Lex-0 e IIIF;
- PR #2 fusionado a `main`;
- `CITATION.cff` preparado como `1.0.0`;
- notas estables `docs/RELEASE_NOTES_V1.0.0.md`;
- workflow que crea `v1.0.0` únicamente después de una CI canónica verde del commit candidato en `main`.

Queda exclusivamente:

- depositar el snapshot estable `v1.0.0` en un archivo persistente público;
- obtener un identificador persistente real, preferentemente DOI de Zenodo;
- comprobar que el depósito corresponde al tag/commit y al manifiesto de integridad;
- incorporar el identificador real a `CITATION.cff` y a la evidencia de release.

## Métrica vigente

| Dimensión | Peso | Avance | Puntos |
|---|---:|---:|---:|
| Cobertura documental | 30 | 100% | 30.0 |
| Incertidumbre y recotejo machine-only | 20 | 100% | 20.0 |
| Arquitectura reusable | 15 | 100% | 15.0 |
| TEI / Lex-0 / IIIF | 10 | 100% | 10.0 |
| Investigación diacrónica | 10 | 100% | 10.0 |
| Apéndices | 5 | 100% | 5.0 |
| Release / archivo / citabilidad | 5 | 80% | 4.0 |
| Segunda fuente | 5 | 100% | 5.0 |
| **Total** | **100** |  | **99.0** |

## Condición de 100%

RHD 1.0 machine-only llegará al 100% únicamente cuando el snapshot estable tenga **archivo persistente + identificador citable real + evidencia de correspondencia con el tag/commit/manifiesto**. No queda trabajo científico del corpus ni revisión humana requerida dentro del alcance vigente.
