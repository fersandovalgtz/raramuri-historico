# Ecosistema científico de Rarámuri Histórico Digital

## Principio de integración

Rarámuri Histórico Digital (RHD) se desarrolla como una **pieza interoperable dentro de un ecosistema de investigación**, no como un repositorio aislado. La integración se basa en enlaces explícitos, responsabilidades separadas, metadatos reutilizables e identificadores persistentes. Un vínculo entre proyectos no implica que sus datos, licencias, estados de validación o autoridades lingüísticas sean equivalentes.

## Núcleo rarámuri

### Rarámuri Histórico Digital

- Repositorio: https://github.com/fersandovalgtz/raramuri-historico
- Sitio: https://raramuri-historico.pages.dev
- Objeto: fuentes históricas, edición documental, procedencia y análisis computacional reproducible.
- Implementación de referencia: Corpus Steffel 1791/1809.
- Release canónica: `v1.0.0`.

### Rarámuri Digital

- Repositorio: https://github.com/fersandovalgtz/raramuri-digital
- Sitio: https://raramuri.ceees.mx
- DOI conceptual actualmente visible en el ecosistema: https://doi.org/10.5281/zenodo.21483353
- Objeto: infraestructura lexicográfica rarámuri–español contemporánea, datos, API y productos derivados.

**Relación con RHD:** los dos proyectos pueden producir relaciones diacrónicas investigables, pero permanecen separados. Una coincidencia gráfica o computacional entre Steffel y Rarámuri Digital no equivale por sí sola a continuidad histórica, identidad semántica, cognación o validación lingüística.

### Rarámuri · recursos educativos

- Repositorio: https://github.com/fersandovalgtz/raramuri-recursos-educativos
- Objeto: capa pedagógica para materiales, actividades y recursos educativos.

**Relación con RHD:** los productos educativos pueden reutilizar resultados publicados cuando su procedencia y nivel de validación lo permitan. El repositorio educativo no debe presentar una hipótesis computacional de RHD como conocimiento lingüístico confirmado.

## Humanidades digitales e historia

### Libro de Texto Mexicano Digital

- Repositorio: https://github.com/fersandovalgtz/libro-texto-mexicano-digital
- Objeto: infraestructura para tratamiento digital de libros de texto y patrimonio documental educativo.

Comparte con RHD principios de trazabilidad documental, preservación de fuente, datos estructurados, versionado y reproducibilidad.

### Historia de la educación en Chihuahua

- Repositorio: https://github.com/fersandovalgtz/historia-educacion-chihuahua
- Objeto: archivo digital de investigación histórica sobre instituciones, fuentes, hemerografía y memoria educativa.

Su relación con RHD es metodológica: ambos proyectos entienden el documento histórico como evidencia que debe conservar su procedencia y distinguirse de las capas interpretativas derivadas.

### Recursos educativos abiertos

- Repositorio: https://github.com/fersandovalgtz/recursos-educativos-abiertos
- Objeto: curación y documentación de materiales educativos reutilizables.

## Identidad académica y descubribilidad

RHD enlaza a identificadores y perfiles que permiten conectar el dataset con la producción científica de su responsable.

- ORCID: https://orcid.org/0000-0002-3168-6725
- GitHub: https://github.com/fersandovalgtz
- Google Scholar: https://scholar.google.com/citations?user=zNZsYYAAAAAJ&hl=es
- CATHI-UACJ: https://cathi.uacj.mx/handle/20.500.11961/3028/browse?authority=0000-0002-3168-6725&type=author
- ResearchGate: https://www.researchgate.net/profile/Fernando-Sandoval-Gutierrez
- ResearchID: https://researchid.co/fersandovalg
- Academia.edu: https://uacj.academia.edu/FernandoSandoval

La fuente de verdad para los metadatos de citación del repositorio es `CITATION.cff`; los perfiles externos sirven para descubrimiento y contexto, no para sustituir el registro versionado del proyecto.

## Entornos institucionales y públicos

- Universidad Autónoma de Ciudad Juárez: https://www.uacj.mx/
- CEEES Cuauhtémoc: https://ceees.mx/
- Rarámuri Digital, servicio público: https://raramuri.ceees.mx
- RHD, sitio público: https://raramuri-historico.pages.dev

Las afiliaciones institucionales describen la adscripción académica del responsable; no implican automáticamente que cada institución sea editora, depositaria, financiadora o avaladora de todas las afirmaciones del repositorio. Cuando una función institucional específica exista, deberá registrarse explícitamente en los metadatos o documentación correspondiente.

## Arquitectura de enlaces

```text
                        ORCID / perfiles académicos
                                  │
                                  ▼
                        Fernando Sandoval Gutierrez
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
     Rarámuri Digital     Rarámuri Histórico   otros repos científicos
     contemporáneo          Digital (RHD)        y educativos
              │                   │
              │          Corpus Steffel 1791/1809
              │                   │
              └──── relaciones diacrónicas ────┘
                    (candidate / revisables)
```

## Reglas para mantener coherente el ecosistema

1. **Un proyecto, una responsabilidad definida.** Evitar duplicar datasets canónicos entre repositorios.
2. **Enlazar, no fusionar sin evidencia.** Las relaciones entre recursos deben registrarse como relaciones tipadas.
3. **Versionar los objetos citables.** Una página web viva y una release científica cumplen funciones distintas.
4. **Propagar identificadores, no copiar metadatos a mano cuando pueda evitarse.** ORCID, DOI, repositorio y release deben mantenerse sincronizados.
5. **Separar difusión de evidencia.** Redes y sitios públicos pueden dirigir al objeto científico, pero el repositorio, la release y el depósito persistente conservan la autoridad documental.
6. **No crear autoridad lingüística por agregación tecnológica.** La conexión entre varios proyectos rarámuri no reemplaza revisión lingüística o comunitaria.

## Próxima capa de integración

Tras verificar el DOI de RHD `v1.0.0`, conviene propagarlo de manera controlada a:

- `CITATION.cff` y README de RHD;
- perfil científico `fersandovalgtz/fersandovalgtz`;
- Rarámuri Digital, en una sección de recursos históricos relacionados;
- sitio público de RHD;
- ORCID, como dataset/software de investigación según corresponda;
- materiales de difusión académica que remitan al corpus.

La propagación debe realizarse sólo después de comprobar la correspondencia exacta entre DOI, tag, commit y artefacto archivado.
