<p align="center">
  <strong>Rarámuri Histórico Digital</strong><br>
  Corpus Steffel 1791/1809
</p>

<p align="center">
  <img src="https://img.shields.io/badge/dataset-0.1.0--mvp-172033?style=flat-square" alt="Dataset 0.1.0 MVP">
  <img src="https://img.shields.io/badge/fuente-Steffel%201809-7a263a?style=flat-square" alt="Steffel 1809">
  <img src="https://img.shields.io/badge/páginas%20facsimilares-84-455B55?style=flat-square" alt="84 PDF pages">
  <img src="https://img.shields.io/badge/entradas%20curadas-60-2d6a4f?style=flat-square" alt="60 curated starter entries">
  <img src="https://img.shields.io/badge/estado-cotejo%20pendiente-b7791f?style=flat-square" alt="Facsimile collation pending">
  <img src="https://img.shields.io/badge/código-MIT-172033?style=flat-square" alt="MIT">
</p>

## Propósito

**Rarámuri Histórico Digital** es la infraestructura histórica complementaria de [Rarámuri Digital](https://github.com/fersandovalgtz/raramuri-digital). Su objetivo es convertir fuentes lexicográficas y lingüísticas históricas en datos trazables, consultables y reutilizables sin borrar la forma documental original.

La primera colección es el **Corpus Steffel 1791/1809**, basado en el *Tarahumarisches Wörterbuch* de Matthäus Steffel. La obra incluye vocabulario alemán–tarahumara, vocabulario tarahumara–alemán, observaciones gramaticales y culturales, un apéndice sobre numeración y una muestra lingüística trilingüe.

## Estado del MVP

Esta versión contiene el facsímil suministrado de 84 páginas, el OCR de trabajo, 60 entradas iniciales curadas a partir de pasajes legibles, un esquema de procedencia, CSV, JSON, XML, SQLite, un borrador TEI y un sitio estático de consulta. **Nada de lo extraído se presenta como validación lingüística definitiva.**

La regla editorial fundamental es: **facsímil → transcripción diplomática → transcripción normalizada → datos estructurados**. Ninguna normalización sustituye la evidencia de la fuente.

## Inicio rápido

Abra `public/index.html` directamente o sirva el directorio:

```bash
python3 -m http.server 8000 -d public
```

Después visite `http://localhost:8000`.

Para validar el dataset:

```bash
python3 tests/validate.py
```

## Estructura

- `sources/`: facsímil, OCR original y checksums.
- `data/entries_curated.csv`: primeras entradas estructuradas y trazables.
- `data/pages.csv`: extracción OCR página por página desde el PDF.
- `data/json/`, `data/xml/`, `data/raramuri_historico.sqlite`: serializaciones.
- `public/`: MVP web de consulta.
- `SCHEMA.md`: modelo de datos.
- `PROVENANCE.md`: política de procedencia.
- `EDITORIAL_POLICY.md`: criterios de transcripción y normalización.
- `ROADMAP.md`: siguiente fase científica y técnica.

## Identificadores

Las entradas usan `RHD-S1809-#####`. El prefijo diferencia Rarámuri Histórico Digital (`RHD`) del dataset contemporáneo Rarámuri Digital (`RD`).

## Relación con Rarámuri Digital

Este repositorio permanece separado de la base contemporánea. Las correspondencias futuras se modelarán como relaciones explícitas con estado (`exacta`, `probable`, `posible`, `rechazada`) y nivel de confianza, nunca como fusiones automáticas.

- Recurso contemporáneo: https://raramuri.ceees.mx
- Repositorio contemporáneo: https://github.com/fersandovalgtz/raramuri-digital

## Responsable

**Dr. Fernando Sandoval Gutierrez**  
Universidad CEEES · Universidad Autónoma de Ciudad Juárez · Cuerpo Académico UACJ-113  
ORCID: 0000-0002-3168-6725

## Licencias

Código: MIT. Las capas editoriales y datos derivados del proyecto se proponen bajo CC BY 4.0 en este MVP; el facsímil histórico debe citarse por su propia procedencia. Véase `DATA_LICENSE.md`.
