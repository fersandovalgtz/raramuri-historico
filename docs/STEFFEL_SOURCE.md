# Matthäus Steffel y el *Tarahumarisches Wörterbuch*: nota documental e histórica

## Propósito de esta nota

Este documento describe la **fuente histórica** de Rarámuri Histórico Digital (RHD) y separa con claridad cuatro objetos que no deben confundirse:

1. la experiencia lingüística y misionera de Matthäus Steffel en la Sierra Tarahumara durante el siglo XVIII;
2. los manuscritos y materiales que Steffel elaboró posteriormente en Europa;
3. la publicación impresa de 1809 editada por Christoph Gottlieb von Murr;
4. la representación computacional, editorial y reproducible creada por RHD en 2026.

RHD no moderniza retrospectivamente a Steffel ni convierte su vocabulario en autoridad sobre el rarámuri contemporáneo. El corpus documenta un testimonio histórico situado y conserva las diferencias entre fuente, transcripción, anotación e interpretación.

## 1. Matthäus Steffel (1734–1806)

Matthäus Steffel nació el **20 de septiembre de 1734 en Jihlava (Iglau), Moravia**, entonces parte de la Monarquía de los Habsburgo, y murió en **Brno en 1806**. Ingresó en la Compañía de Jesús en 1754 y partió hacia Nueva España al año siguiente. La investigación historiográfica reciente reconstruye su formación en el Colegio de San Francisco Javier de Tepotzotlán y su actividad en la Sierra Tarahumara a partir de 1761.

Entre 1761 y 1767 trabajó en distintos puntos de la región, con estancias documentadas en **Tónachi, Tomochic, Nonoava y San Francisco de Borja**. La expulsión de los jesuitas de los dominios españoles en 1767 interrumpió esa experiencia. Steffel regresó a Europa y continuó trabajando, años después, con los materiales lingüísticos adquiridos durante su estancia en Nueva España.

La literatura especializada insiste en que su obra no debe leerse sólo como herramienta misionera. Sus descripciones contienen observaciones lingüísticas, pragmáticas y etnográficas y participan del ambiente intelectual europeo de fines de la Ilustración. Aarón Grageda ha estudiado específicamente el papel del diccionario en las primeras empresas de comparación y tipología lingüística; Zarina Estrada Fernández ha situado la gramática de Steffel en la historia de la gramaticografía jesuita y en su desplazamiento hacia una perspectiva ilustrada más crítica y descriptiva.

## 2. ¿Por qué «1791/1809»?

La denominación **Corpus Steffel 1791/1809** distingue un hito documental de la fecha de publicación.

- **1791** remite a la fase de elaboración y circulación manuscrita documentada por la correspondencia de Steffel. En una carta fechada en Brno el **28 de marzo de 1791**, Steffel informa a Christoph Gottlieb von Murr sobre su trabajo con traducciones y materiales tarahumaras y sobre la revisión de esos materiales después de décadas sin practicar la lengua.
- **1809** es la fecha de la publicación impresa del *Tarahumarisches Wörterbuch* dentro de la compilación editada por von Murr.

Por tanto, `1791/1809` **no significa que existan dos ediciones impresas equivalentes** ni que el diccionario haya sido publicado en 1791. Es una convención de RHD para hacer visible la historia material e intelectual que precede a la edición impresa.

## 3. Publicación de 1809

La referencia bibliográfica adoptada por RHD es:

> Steffel, Matthäus. 1809. “Tarahumarisches Wörterbuch, nebst einigen Nachrichten von den Sitten und Gebräuchen der Tarahumaren, in Neu-Biscaya, in der Audiencia Guadalaxara, im Vice-Königreiche Alt-Mexico, oder Neu-Spanien”. En Christoph Gottlieb von Murr (ed.), *Nachrichten von verschiedenen Ländern des Spanischen Amerika, aus eigenhändigen Aufsätzen einiger Missionare der Gesellschaft Jesu*, vol. I, pp. 293–374. Halle: Johann Christian Hendel.

La *Cambridge World History of Lexicography* registra asimismo la contribución de Steffel en el volumen I, pp. 293–374, dentro de la compilación de von Murr.

### Estructura documental relevante para RHD

La contribución completa ocupa las **pp. 293–374** del volumen. Dentro de ese conjunto:

- los paratextos introductorios preceden al cuerpo lexicográfico;
- el **cuerpo del diccionario comienza en la p. 301**;
- la disposición cambia de **alemán→rarámuri a rarámuri→alemán dentro de la p. 353**;
- el cuerpo lexicográfico se cierra antes de los materiales anexos;
- el **apéndice comienza en la p. 369**;
- los materiales finales incluyen la numeración tarahumara y una muestra lingüística en la que aparecen **22 fórmulas** y el **Padrenuestro**, con versiones en latín, alemán y rarámuri según corresponda.

Esta estructura es importante computacionalmente: la inversión de dirección dentro de una misma página impide tratar la fuente como una tabla homogénea y obliga a que el modelo de datos registre dirección, página, procedencia y tipo documental.

## 4. Un diccionario y también un documento etnográfico

El título de la obra anuncia que el vocabulario se acompaña de noticias sobre los «usos y costumbres» de los tarahumaras. Numerosas entradas integran comentarios que exceden una equivalencia léxica estricta. La bibliografía moderna ha caracterizado por ello el texto como una fuente valiosa no sólo para la historia de la lengua sino también para la historia cultural y antropológica de la región.

RHD conserva ese carácter mediante una política de **no reducción**: una entrada histórica no se transforma automáticamente en un par `lema = traducción`. La microestructura, las glosas, los comentarios y la materialidad tipográfica forman parte de la evidencia.

Esto es especialmente importante porque algunas formulaciones de Steffel expresan categorías, juicios y percepciones propias de un observador europeo del siglo XVIII. RHD las preserva como **evidencia histórica atribuida a la fuente**, no como descripciones neutrales ni como posiciones del proyecto.

## 5. La obra de Steffel en la historia de los estudios lingüísticos

La investigación de Aarón Grageda muestra que el diccionario debe entenderse dentro de las redes ilustradas de recolección y comparación de lenguas. Los materiales de Steffel se relacionaron con intereses de Christoph Gottlieb von Murr y con el proyecto de Hartwig Ludwig Christian Bacmeister de reunir muestras lingüísticas para comparación. La recepción posterior alcanzó discusiones vinculadas con la clasificación de lenguas americanas en el ámbito germano.

Este contexto justifica que RHD trate el objeto no únicamente como «diccionario antiguo», sino como una pieza de la **historia global de la producción, circulación y clasificación del conocimiento lingüístico**.

## 6. Testimonio de trabajo y procedencia digital

El pipeline de RHD parte de un facsímil digital y un OCR de trabajo. La procedencia técnica se documenta en [`PROVENANCE.md`](../PROVENANCE.md) y los hashes del material fuente en `sources/checksums.json`.

RHD distingue al menos estas capas:

`testimonio/facsímil → OCR fuente → candidatos de segmentación → cotejo documental → transcripción diplomática IA-asistida → estados de incertidumbre → capas derivadas → representaciones interoperables`.

La edición digital **no sustituye al testimonio**. Cada capa debe conservar suficiente información para regresar a la página y a la evidencia que la originó.

## 7. Relación con ediciones e investigaciones contemporáneas

La referencia contemporánea central es:

> Merrill, William L.; Maria Brumm; Greta de León; Zarina Estrada Fernández; Aarón Aurelio Grageda Bustamante. 2020. *El diccionario tarahumara–alemán de Matthäus Steffel: lengua y cultura rarámuri en el siglo XVIII*. Hermosillo: Universidad de Sonora. DOI: https://doi.org/10.47807/UNISON.8

El Repositorio Institucional de la Universidad de Sonora describe esta obra como la primera traducción al español del diccionario y un análisis detallado de su contenido. RHD la trata como **edición e investigación independiente**: se consulta bibliográficamente, pero sus traducciones protegidas no se copian sistemáticamente al dataset.

## 8. Bibliografía seleccionada y recursos de verificación

### Fuente primaria

- Steffel, Matthäus. 1809. “Tarahumarisches Wörterbuch, nebst einigen Nachrichten von den Sitten und Gebräuchen der Tarahumaren…”. En Christoph Gottlieb von Murr (ed.), *Nachrichten von verschiedenen Ländern des Spanischen Amerika, aus eigenhändigen Aufsätzen einiger Missionare der Gesellschaft Jesu*, vol. I, 293–374. Halle: Johann Christian Hendel.

### Estudios especializados

- Grageda, Aarón. 2019. “El diccionario alemán-tarahumara de Matthäus Steffel y la tipología lingüística del siglo XVIII”. *Nóesis. Revista de Ciencias Sociales y Humanidades* 28(56): 57–75. https://doi.org/10.20983/noesis.2019.2.7
- Estrada Fernández, Zarina. 2021. “Aportaciones de Matthäus Steffel al conocimiento de la escuela jesuita sobre el tarahumara”. *Cuadernos de Lingüística de El Colegio de México* 8. https://doi.org/10.24201/clecm.v8i0.212
- Merrill, William L.; Maria Brumm; Greta de León; Zarina Estrada Fernández; Aarón Aurelio Grageda Bustamante. 2020. *El diccionario tarahumara–alemán de Matthäus Steffel: lengua y cultura rarámuri en el siglo XVIII*. Universidad de Sonora. https://doi.org/10.47807/UNISON.8
- Brumm Roessler, María M. 2007. “El diccionario tarahumara-alemán de Matthäus Steffel como fuente de conocimiento de la lengua y la cultura tarahumaras”. En *Desde los confines de los imperios ibéricos: los jesuitas de habla alemana en las misiones americanas*, 395–408. Iberoamericana/Vervuert.
- Merrill, William L. 2007. “La obra lingüística del padre Matthäus Steffel S.J.” En *Desde los confines de los imperios ibéricos: los jesuitas de habla alemana en las misiones americanas*, 409–441. Iberoamericana/Vervuert.

### Registros y acceso

- Repositorio Institucional de la Universidad de Sonora, edición 2020: https://repositorioinstitucional.uson.mx/handle/20.500.12984/6339
- Open Library / Internet Archive, registro de la edición de 1809: https://openlibrary.org/works/OL16883366W/Tarahumarisches_W%C3%B6rterbuch_nebst_einigen_Nachrichten_von_den_Sitten_und_Gebr%C3%A4uchen_der_Tarahumaren
- Jesuit Online Bibliography, autoridad temática para Steffel y bibliografía jesuita: https://jesuitonlinebibliography.bc.edu/

## 9. Criterio de citación

Cuando un argumento dependa de la **fuente histórica**, debe citarse a Steffel 1809 y, cuando sea relevante, la página impresa. Cuando dependa de una **transformación o dataset de RHD**, debe citarse además la versión específica de RHD utilizada. Una vez completado el depósito persistente, el DOI de la versión archivada será el identificador preferente para esa segunda cita.

Esta doble citación mantiene separadas la autoría histórica de Steffel y la responsabilidad editorial/computacional de RHD.
