# Metadatos administrativos recomendados para GitHub

GitHub mantiene algunos metadatos de descubribilidad fuera del árbol Git. Para evitar que esos campos administrativos diverjan de la documentación versionada, este archivo registra los valores canónicos recomendados para la sección **About** del repositorio.

## Description

```text
Edición histórico-digital reproducible del Tarahumarisches Wörterbuch de Matthäus Steffel (1791/1809): corpus rarámuri histórico, procedencia explícita, TEI/TEI Lex-0, IIIF y datos FAIR.
```

## Website

```text
https://fersandovalgtz.github.io/raramuri-historico/
```

GitHub Pages confirma este endpoint público y HTTPS mediante despliegue por workflow.

## Topics

```text
raramuri
tarahumara
matthaus-steffel
historical-lexicography
digital-humanities
indigenous-languages
research-data
research-software
open-science
fair-data
fair4rs
provenance
reproducibility
digital-edition
lexicography
tei
tei-lex-0
iiif
historical-linguistics
chihuahua
```

## Criterio de mantenimiento

- `Description` debe describir el objeto científico, no una campaña o estado temporal.
- `Website` debe apuntar a una única landing pública canónica y verificada.
- `Topics` deben favorecer descubribilidad disciplinar, técnica, geográfica y lingüística sin convertir hipótesis en etiquetas de hecho.
- El DOI no debe introducirse como topic; debe registrarse en metadatos de citación una vez verificado.
- Si cambia la URL canónica o el nombre científico del proyecto, actualice este archivo junto con README, `CITATION.cff`, `codemeta.json` y `DEPLOYMENT.md`.

## Estado observado antes de esta actualización

Al auditar el repositorio el 15 de agosto de 2026, la API de GitHub devolvía `description: null`, `homepage: null` y `topics: []`. Estos tres campos son configuración administrativa de GitHub y no se modifican mediante los archivos del repositorio.
