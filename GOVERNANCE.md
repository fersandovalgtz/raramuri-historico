# Gobernanza de Rarámuri Histórico Digital

## 1. Objeto de la gobernanza

Rarámuri Histórico Digital (RHD) combina una fuente histórica, datos derivados, software de investigación, decisiones editoriales y análisis computacionales. La gobernanza existe para que esos componentes evolucionen sin perder trazabilidad, atribución ni límites epistemológicos.

## 2. Mantenimiento

El mantenedor responsable de la versión 1.x es **Fernando Sandoval Gutierrez** (ORCID `0000-0002-3168-6725`). El mantenimiento comprende la integración de cambios, versionado, releases, documentación de procedencia y custodia del alcance científico del repositorio.

La función de mantenedor **no equivale a autoridad lingüística sobre el rarámuri contemporáneo**. Las decisiones que requieran competencia filológica, lingüística, comunitaria o disciplinar deben registrar la clase de revisión y la identidad de quien la realiza.

## 3. Fuentes de autoridad

Ante discrepancias, se sigue este orden:

1. **testimonio histórico/facsímil** para cuestiones documentales;
2. **manifiestos y procedencia versionados** para reconstruir decisiones del proyecto;
3. **especificación y esquemas vigentes** para contratos de datos;
4. **revisión humana identificada** para adjudicaciones que exijan juicio experto;
5. **literatura especializada** para interpretación historiográfica o lingüística, sin sobrescribir automáticamente la fuente.

Una salida de IA, OCR o modelo estadístico nunca adquiere mayor autoridad por repetición.

## 4. Decisiones editoriales

Toda decisión que altere una lectura, frontera, dirección, glosa o relación científica debe ser atribuible, justificable por evidencia, reconstruible a partir del historial, compatible con la política de no destrucción y representada con un estado que refleje su autoridad real.

Los estados de incertidumbre pueden ser terminales. No existe obligación de resolver un caso ambiguo.

## 5. Cambios al modelo de datos

Los cambios se clasifican como:

- **patch:** correcciones compatibles sin cambio de contrato;
- **minor:** campos, exportaciones o capacidades compatibles añadidas;
- **major:** cambios incompatibles del núcleo, semántica de campos o identificadores.

Los IDs estables no se reciclan. Un cambio mayor debe proporcionar estrategia de migración o una justificación explícita de por qué no es posible.

## 6. Versiones científicas

Una release científica debe fijar como mínimo tag semántico, commit exacto, fecha, notas de release, estado de licencias, métricas relevantes, límites epistemológicos y resultados de validación/CI que formen parte del criterio de release.

Una release publicada no se reescribe retrospectivamente para incorporar conocimiento posterior. Las mejoras posteriores pertenecen a una nueva versión.

## 7. Archivo y citación

El repositorio vivo y el archivo persistente cumplen funciones distintas. Cuando una release tenga DOI:

- el DOI debe resolver al snapshot archivado correcto;
- `CITATION.cff`, README y otros metadatos deben señalar el identificador verificado;
- el DOI de una versión no se reutiliza para otra;
- cuando exista DOI conceptual, debe distinguirse del DOI de versión.

## 8. Contribuciones externas

Los pull requests pueden ser aceptados, modificados o rechazados con base en calidad de evidencia, compatibilidad con el modelo RHD, reproducibilidad, claridad de procedencia, estatus jurídico de los materiales y protección contra afirmaciones de autoridad no sustentadas.

Las contribuciones sustantivas deben recibir atribución adecuada. La coautoría de productos académicos se determina por contribución intelectual real y las normas aplicables a cada publicación, no por el número de commits.

## 9. Conflictos de interpretación

Cuando dos interpretaciones plausibles no puedan resolverse con la evidencia disponible, RHD debe conservar la pluralidad o incertidumbre de manera explícita. El mantenedor no debe seleccionar una lectura sólo para producir un dataset aparentemente más completo.

## 10. Relación con comunidades e instituciones

RHD estudia documentación histórica sobre el rarámuri. La publicación técnica de un corpus no confiere representación sobre las comunidades rarámuri actuales. Si en el futuro se incorpora validación o colaboración comunitaria, su alcance, consentimiento, atribución y decisiones deberán documentarse específicamente.

Las afiliaciones institucionales del responsable no implican automáticamente patrocinio, aprobación o propiedad institucional del repositorio.

## 11. Seguridad, conducta y ética

- Interacción comunitaria: `CODE_OF_CONDUCT.md`.
- Vulnerabilidades o incidentes: `SECURITY.md`.
- Contribuciones científicas: `CONTRIBUTING.md`.
- Licencias: `LICENSE` y `DATA_LICENSE.md`.
- Alcance y riesgos de reutilización: `DATASHEET.md`.

## 12. Modificación de esta gobernanza

Los cambios sustantivos a este documento deben realizarse mediante pull request, explicar su motivación y quedar registrados en el historial. Una modificación de gobernanza no puede alterar por sí sola la evidencia o el estado científico de releases ya publicadas.
