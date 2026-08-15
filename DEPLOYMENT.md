# Publicación web — Rarámuri Histórico Digital

## Arquitectura

El sitio público es estático y vive en `public/`. No requiere un framework de compilación: `index.html`, `research.html`, `styles.css`, `app.js`, datos publicados e infraestructura IIIF se sirven como artefactos versionados del repositorio.

El workflow `.github/workflows/pages.yml` despliega `public/` mediante GitHub Pages y se activa para cambios pertinentes en `main`. El sitio no debe introducir resultados científicos que no existan en el repositorio: la interfaz es una capa de acceso al snapshot documentado, no una fuente independiente de verdad.

## URL pública verificada

GitHub Pages está habilitado públicamente mediante workflow y declara como `html_url`:

`https://fersandovalgtz.github.io/raramuri-historico/`

Ésta debe utilizarse como **homepage canónica** del repositorio mientras no se adopte y verifique un dominio institucional propio.

Si posteriormente se adopta un dominio estable —por ejemplo un subdominio del ecosistema `raramuri.ceees.mx`— el cambio debe propagarse de forma coordinada a:

- metadata `homepage` del repositorio;
- `CITATION.cff`;
- `codemeta.json`;
- README;
- DOI/Zenodo cuando el registro permita actualizar la landing relacionada;
- enlaces desde Rarámuri Digital y el perfil científico.

No se recomienda mantener simultáneamente varias URLs como «canónicas». Pueden existir espejos, pero una sola landing debe actuar como dirección pública preferente.

## Contenido que debe permanecer sincronizado

La landing pública debe reflejar como mínimo:

- versión científica vigente;
- métricas canónicas de cobertura;
- estado de validación y límites epistemológicos;
- referencia completa de Steffel 1809;
- enlace al repositorio y a `CITATION.cff`;
- licencias diferenciadas;
- DOI únicamente después de verificación del depósito persistente;
- enlaces al ecosistema relacionado.

## Despliegue

Un cambio en `public/**` fusionado a `main` activa el workflow de Pages según sus filtros. Antes de publicar un cambio científico, verifique los tests canónicos y que las métricas mostradas en la web correspondan a la versión citada.

Para cambios exclusivamente de interfaz, no incremente la versión científica si no cambia el objeto de investigación. Para cambios de datos o interpretación, aplique `GOVERNANCE.md` y `CHANGELOG.md`.

## IIIF

La publicación IIIF forma parte del contrato de acceso documental de RHD 1.0.0. El workflow contiene comprobaciones específicas para materializar y verificar el paquete de imágenes del testimonio en los contextos previstos por el repositorio. No deben inventarse regiones de imagen o coordenadas que no estén respaldadas por evidencia publicada.

## Preservación

El sitio web puede evolucionar y por ello **no sustituye al archivo persistente de una release**. GitHub conserva desarrollo y versionado; el depósito con DOI conserva el snapshot citable. Una publicación web correcta debe facilitar el acceso a ambos sin confundir sus funciones.
