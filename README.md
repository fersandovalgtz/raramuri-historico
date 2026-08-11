<p align="center">
  <strong>Rarámuri Histórico Digital</strong><br>
  Corpus Steffel 1791/1809
</p>

<p align="center">
  <img src="https://img.shields.io/badge/dataset-0.1.0--mvp-172033?style=flat-square" alt="Dataset 0.1.0 MVP">
  <img src="https://img.shields.io/badge/fuente-Steffel%201809-7a263a?style=flat-square" alt="Steffel 1809">
  <img src="https://img.shields.io/badge/facsímil-84%20páginas-455B55?style=flat-square" alt="84 PDF pages">
  <img src="https://img.shields.io/badge/entradas%20iniciales-60-2d6a4f?style=flat-square" alt="60 starter entries">
  <img src="https://img.shields.io/badge/estado-cotejo%20pendiente-b7791f?style=flat-square" alt="Facsimile collation pending">
  <img src="https://img.shields.io/badge/código-MIT-172033?style=flat-square" alt="MIT">
</p>

## Propósito

**Rarámuri Histórico Digital** es la infraestructura histórica complementaria de [Rarámuri Digital](https://github.com/fersandovalgtz/raramuri-digital). Su objetivo es convertir fuentes lexicográficas y lingüísticas históricas en datos trazables, consultables y reutilizables sin borrar la forma documental original.

La primera colección es el **Corpus Steffel 1791/1809**, basado en el *Tarahumarisches Wörterbuch* de Matthäus Steffel. La obra incluye vocabulario alemán–tarahumara, vocabulario tarahumara–alemán, observaciones gramaticales y culturales, un apéndice sobre numeración y una muestra lingüística trilingüe.

## Estado del MVP

La versión `0.1.0-mvp` fija la arquitectura científica antes de escalar la transcripción. Incluye 60 entradas iniciales con procedencia, un CSV canónico, una proyección JSON para la interfaz, esquema de datos, políticas editoriales y de gobernanza, metadatos de citación, scripts reproducibles para generar JSON/XML/TEI/SQLite y un sitio estático de consulta.

El proyecto se construyó sobre un facsímil de 84 páginas y un OCR de trabajo. Los archivos de ingesta originales se preservan fuera de la capa editorial del repositorio y se registran mediante checksums; el repositorio enlaza además copias públicas de consulta. **Nada de lo extraído se presenta como validación lingüística definitiva.**

La regla editorial fundamental es: **facsímil → OCR bruto → transcripción diplomática → normalización → datos estructurados**. Ninguna normalización sustituye la evidencia de la fuente.

## Reproducibilidad

El CSV es la fuente canónica del MVP. Las serializaciones derivadas se regeneran con:

```bash
python3 scripts/build_exports.py
python3 tests/validate.py
```

El pipeline produce JSON completo, XML, borrador TEI, SQLite y la proyección JSON usada por la interfaz pública. GitHub Actions ejecuta la misma secuencia en cada cambio.

## Estructura

- `data/entries_curated.csv`: dataset canónico inicial.
- `data/correspondences_template.csv`: modelo de futuras relaciones Steffel ↔ Rarámuri Digital.
- `public/`: MVP web de consulta.
- `scripts/build_exports.py`: generación reproducible de serializaciones.
- `SCHEMA.md`: modelo de datos.
- `PROVENANCE.md`: procedencia documental.
- `EDITORIAL_POLICY.md`: criterios de transcripción y normalización.
- `GOVERNANCE.md`: separación entre evidencia, interpretación y validación.
- `ROADMAP.md`: ruta hacia la edición digital de investigación.

## Identificadores

Las entradas usan `RHD-S1809-#####`. El prefijo diferencia Rarámuri Histórico Digital (`RHD`) del conjunto contemporáneo Rarámuri Digital (`RD`).

## Relación con Rarámuri Digital

Este repositorio permanece separado de la base contemporánea. Las correspondencias futuras se modelarán como relaciones explícitas con estado (`exacta`, `probable`, `posible`, `rechazada`) y nivel de confianza, nunca como fusiones automáticas.

- Recurso contemporáneo: https://raramuri.ceees.mx
- Repositorio contemporáneo: https://github.com/fersandovalgtz/raramuri-digital

## Fuente primaria y consulta

- Open Library: https://openlibrary.org/works/OL16883366W/
- Internet Archive: https://archive.org/details/tarahumarischesw00stef

## Responsable

**Dr. Fernando Sandoval Gutierrez**  
Universidad CEEES · Universidad Autónoma de Ciudad Juárez · Cuerpo Académico UACJ-113  
ORCID: 0000-0002-3168-6725

## Licencias

Código: MIT. Las capas editoriales y datos derivados del proyecto se proponen bajo CC BY 4.0 en este MVP; la obra histórica debe citarse por su propia procedencia. Véase `DATA_LICENSE.md`.
