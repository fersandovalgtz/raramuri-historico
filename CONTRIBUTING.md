# Contribuir a Rarámuri Histórico Digital

RHD acepta contribuciones documentales, filológicas, lingüísticas, históricas, técnicas y de metadatos cuando **aumentan la evidencia o la reproducibilidad sin borrar la procedencia**. El objetivo no es maximizar el número de correcciones, sino mejorar el corpus de manera auditable.

## Antes de contribuir

Lea primero:

- `EDITORIAL_POLICY.md` — autoridad y separación de capas;
- `PROVENANCE.md` — procedencia y no destrucción de evidencia;
- `DATASHEET.md` — alcance, limitaciones y usos no previstos;
- `docs/STEFFEL_SOURCE.md` — contexto documental de la fuente;
- `GOVERNANCE.md` — toma de decisiones y versionado;
- `CODE_OF_CONDUCT.md` — reglas de interacción.

## Tipos de contribución

### Corrección documental

Debe indicar como mínimo:

- `record_id`;
- página impresa y/o Canvas/página facsimilar;
- lectura actual;
- lectura propuesta;
- evidencia que permite decidir;
- si la propuesta afecta transcripción, segmentación, dirección, glosa, estructura u otro campo;
- nombre o identidad académica de quien revisa cuando se solicite atribución como revisión humana.

Cuando el facsímil sea ambiguo, **no se fuerza una solución**. Una contribución válida puede concluir que el caso debe permanecer irresuelto.

### Revisión humana independiente

La etiqueta humana no se concede por haber ejecutado un script, revisado una tabla agregada o aceptado una sugerencia automática sin inspección. Una adjudicación humana debe documentar:

- la persona responsable;
- fecha y alcance;
- evidencia examinada;
- decisión;
- relación con el estado previo (`confirmed_ai_assisted`, `corrected_ai_assisted`, `unresolved_after_ai_recollation`, etc.).

Las revisiones humanas futuras se añaden como una capa posterior a `v1.0.0`; no cambian retrospectivamente la naturaleza machine-only de esa release.

### Contribución lingüística o histórica

Debe distinguir entre:

- evidencia de la fuente;
- bibliografía secundaria;
- juicio filológico;
- análisis lingüístico;
- hipótesis diacrónica;
- conocimiento de uso contemporáneo.

Una coincidencia gráfica no basta para afirmar equivalencia semántica, cognación, etimología o continuidad histórica.

### Código y reproducibilidad

Los cambios de software deben:

- conservar o ampliar los tests relevantes;
- no alterar silenciosamente conteos canónicos;
- documentar cualquier cambio de esquema;
- mantener determinismo cuando el proceso se declara reproducible;
- evitar introducir credenciales, datos sensibles o dependencias innecesarias;
- actualizar documentación y `CHANGELOG.md` cuando corresponda.

## Flujo recomendado

1. Abra un issue describiendo el problema o propuesta, salvo correcciones triviales de documentación.
2. Cite el registro, archivo o componente afectado.
3. Cree una rama con un cambio acotado.
4. Añada pruebas o evidencia reproducible cuando aplique.
5. Abra un pull request explicando **qué cambia, por qué cambia y qué evidencia lo justifica**.
6. Mantenga separados cambios editoriales, cambios de datos y refactors técnicos cuando mezclarlos dificulte la revisión.

## Pull requests sobre datos

Un PR que cambie `data/entries.csv` o una capa científica debe incluir una nota de impacto con:

- conteos antes/después;
- IDs afectados;
- archivos derivados que deben regenerarse;
- tests ejecutados;
- compatibilidad con esquema;
- impacto en release/versionado.

Los archivos derivados deben regenerarse con el pipeline; no se recomienda editarlos manualmente si existe una fuente canónica que los produce.

## Política de identificadores

Los IDs históricos de RHD no se reciclan. Rechazar un candidato no autoriza a reutilizar su identificador para otra unidad. Esta regla protege la trazabilidad longitudinal del corpus.

## Traducciones y materiales de terceros

Las traducciones españolas, anotaciones o imágenes procedentes de ediciones contemporáneas no se copiarán sistemáticamente sin base jurídica clara. Una cita académica no equivale a permiso para redistribuir una obra protegida como dataset.

## Estilo documental

- Use Markdown claro y enlaces persistentes cuando sea posible.
- Prefiera referencias bibliográficas completas a afirmaciones sin fuente.
- Para Steffel, conserve grafías históricas cuando la discusión sea documental.
- Diferencie `rarámuri` como autodenominación contemporánea de las formas históricas o bibliográficas cuando el contexto lo requiera.
- No atribuya a una comunidad, institución o persona una validación que no esté documentada.

## Seguridad

No reporte vulnerabilidades sensibles en un issue público. Siga `SECURITY.md`.

## Licencias de contribuciones

Al enviar una contribución usted acepta que:

- el código original aportado se distribuya bajo MIT;
- los datos, metadatos y capas editoriales originales aportadas al proyecto se distribuyan bajo CC BY 4.0, salvo que se documente otra condición compatible;
- conserva la responsabilidad de no aportar material de terceros que no pueda redistribuirse legítimamente.

## Reconocimiento

Las contribuciones sustantivas podrán registrarse en `CONTRIBUTORS.md` y, cuando la naturaleza del aporte lo justifique, en metadatos de una release o producto científico. La atribución académica se decide por contribución real y documentada, no por automatismo.
