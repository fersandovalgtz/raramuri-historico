# Correcciones a la cola preliminar `rugameke` derivada del TXT

**Fecha:** 2026-08-13. El inventario `rugameke_txt_inventory_v1` es una cola de OCR y no debe tratarse como inventario validado. La recollación dirigida del facsímil produjo las siguientes correcciones:

- `Pagorügameke` del TXT es un falso positivo de OCR: la imagen dice `Pagotúgameke`. Se excluye de la cola `rugameke`.
- `Irkirügameke` es un fragmento OCR de la entrada `Sikirúgameke`; se fusiona con ese tipo.
- `Porichirügameke` se recolló como `Potſchirúgameke`; se fusiona con el tipo `potschirugameke` ya observado en DE–RAR.
- `Boicarügameke` se recolló como `Baicarúgameke`.
- Se recuperaron cuatro tipos omitidos por cortes de línea/segmentación OCR: `Hulirugameke`, `Polirügameke`, `Kiasrugameke` y `Tutschirügameke`.

Aplicadas estas correcciones, la cola facsimile-aware contiene provisionalmente **19 tipos candidatos `rugameke`** y **24 ocurrencias candidatas**. El número sigue siendo provisional hasta recollar todos los tipos contra el facsímil.

La corrección más importante es metodológica: la búsqueda de sufijos sobre OCR no puede basarse únicamente en tokens completos, porque Steffel y el OCR distribuyen numerosas formas entre líneas. La próxima versión del generador deberá reconstruir cortes de línea y conservar el facsímil como autoridad final.

`human_reviewed=false`; `facsimile_recollated_all_types=false`; `automatic_morphological_extension=false`; `historical_continuity_judgment=not_performed`.
