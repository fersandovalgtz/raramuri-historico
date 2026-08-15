# Procedencia — Rarámuri Histórico Digital

## Principio

La procedencia es una propiedad del dato, no una nota auxiliar. RHD conserva la cadena que conecta el testimonio histórico con cada capa computacional y editorial, y evita que una salida derivada pueda presentarse como si fuera texto original de Steffel.

## Fuente primaria y testimonio de trabajo

La obra histórica es:

> Steffel, Matthäus. 1809. “Tarahumarisches Wörterbuch, nebst einigen Nachrichten von den Sitten und Gebräuchen der Tarahumaren, in Neu-Biscaya, in der Audiencia Guadalaxara, im Vice-Königreiche Alt-Mexico, oder Neu-Spanien”. En Christoph Gottlieb von Murr (ed.), *Nachrichten von verschiedenen Ländern des Spanischen Amerika, aus eigenhändigen Aufsätzen einiger Missionare der Gesellschaft Jesu*, vol. I, pp. 293–374. Halle: Johann Christian Hendel.

El corpus se construyó inicialmente a partir de un **PDF facsimilar** y un **TXT OCR** suministrados al proyecto el 11 de agosto de 2026. El OCR fuente se conserva sin corrección retroactiva en `sources/steffel-1809-ocr-source.txt`; `sources/checksums.json` registra huellas criptográficas de los archivos fuente utilizados.

Para la release 1.0.0, el testimonio canónico de Steffel se documenta con SHA-256:

`4ccc94aaff1fcc948341a103255f2c3f52dd7b8ca488b6dc79a921b3c9d6244f`

La existencia de un hash fija **qué representación binaria fue usada por el pipeline**; no confiere derechos sobre el facsímil ni sustituye la referencia bibliográfica de la obra histórica.

## Horizonte 1791/1809

La convención `Steffel 1791/1809` distingue un hito de elaboración/correspondencia de la publicación impresa. En 1791 Steffel documenta en correspondencia su trabajo con materiales tarahumaras; la obra que constituye la fuente impresa de RHD fue publicada en 1809. Véase `docs/STEFFEL_SOURCE.md`.

## Cadena de transformación

La procedencia lógica del corpus puede resumirse así:

```text
obra histórica / testimonio facsimilar
        ↓
OCR fuente preservado
        ↓
segmentación de alta cobertura
        ↓
candidatos documentales con ID estable
        ↓
cotejo de límites, página y dirección
        ↓
reconstrucción por líneas/columnas
        ↓
transcripción diplomática IA-asistida
        ↓
auditoría de notas e incertidumbre
        ↓
recotejo PHIL IA-asistido
        ↓
capas derivadas de investigación
        ↓
CSV / JSON / XML / SQLite / TEI / TEI Lex-0 / IIIF
```

Cada flecha representa una transformación que debe ser reproducible o, cuando depende de una decisión editorial, quedar documentada en un manifiesto de revisión.

## Identificadores y no destrucción

Las unidades RHD utilizan identificadores estables. Un identificador no se recicla aunque un candidato resulte ser un falso límite. Esta decisión permite reconstruir la historia de la segmentación y evita que una unidad rechazada desaparezca silenciosamente del registro editorial.

Las correcciones se incorporan mediante overlays, manifiestos o capas derivadas. El principio general es **no sobrescribir la evidencia anterior cuando esa evidencia es necesaria para entender la decisión posterior**.

## Estado de la release 1.0.0

La versión `v1.0.0` conserva:

- 2,495 candidatos documentales con disposición;
- 1,965 artículos activos;
- 530 falsos límites preservados;
- 1,965 transcripciones diplomáticas IA-asistidas;
- 482 casos PHIL terminales (284 confirmados IA-asistidos, 152 correcciones propuestas IA-asistidas y 46 irresueltos);
- capas de investigación derivada, incluida una cola de 298 relaciones diacrónicas `candidate`;
- representaciones TEI/TEI Lex-0 e IIIF vinculadas al mismo snapshot.

El estado `v1.0.0` es **machine-only**. No se asigna retrospectivamente validación humana a ninguna capa que no la haya recibido.

## Fuente histórica frente a capas RHD

RHD distingue explícitamente:

- **texto/facsímil histórico:** objeto atribuido a Steffel y a su contexto de publicación;
- **OCR:** representación mecánica potencialmente errónea;
- **transcripción diplomática IA-asistida:** reconstrucción documental con estado propio;
- **corrección editorial propuesta:** decisión derivada, no texto fuente;
- **traducción o comentario editorial:** responsabilidad del proyecto;
- **relación computacional:** hipótesis generada por método, no afirmación histórica automática;
- **revisión humana:** sólo puede existir cuando una persona identificable la realiza y queda registrada.

## Materiales contemporáneos y terceros

La edición de Merrill y colaboradores publicada por la Universidad de Sonora en 2020 se utiliza como bibliografía y objeto de contraste académico independiente. Su traducción española **no se incorpora sistemáticamente como dato de RHD**. La licencia de RHD no se extiende a esa edición ni a otros materiales de terceros.

## Procedencia institucional y autoría

El responsable científico y mantenedor de RHD es Fernando Sandoval Gutierrez (ORCID `0000-0002-3168-6725`). Las afiliaciones y enlaces institucionales sirven para identificación académica; no deben interpretarse automáticamente como cesión de derechos, patrocinio o responsabilidad editorial institucional salvo que un documento específico así lo establezca.

## Archivo persistente

GitHub conserva el historial de desarrollo y la release `v1.0.0`, pero el gate de preservación externa se considera cerrado sólo cuando exista un depósito persistente y se verifique la correspondencia:

`DOI ↔ v1.0.0 ↔ commit canónico ↔ artefacto archivado ↔ manifiesto de integridad`.

Hasta entonces no se insertará un DOI de RHD no comprobado en `CITATION.cff` ni en los badges del repositorio.
