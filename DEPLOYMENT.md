# Publicación web

El MVP web vive en `public/` y no requiere compilación. Está preparado para GitHub Pages mediante `.github/workflows/pages.yml`.

## Activación inicial

En GitHub, abra **Settings → Pages** y seleccione **GitHub Actions** como fuente de publicación. Esta activación es una configuración administrativa del repositorio y se realiza una sola vez.

Después de activarla, el workflow `pages` puede ejecutarse manualmente. Una vez verificado el primer despliegue, conviene habilitar despliegue automático en cada cambio de `main`.

## Dominio previsto

La URL temporal de GitHub Pages puede utilizarse para pruebas. Para producción, el proyecto está concebido para un subdominio del ecosistema CEEES, preferentemente `historico.raramuri.ceees.mx`, una vez que la edición alcance una fase pública estable.
