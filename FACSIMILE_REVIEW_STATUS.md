# Facsimile collation and diplomatic transcription status

The first boundary-review batch (`RHD-FR-001`) covers 100 high-confidence machine candidates from the German→Rarámuri section, spanning printed pages 301–317.

## Boundary-review results

| Metric | Count |
|---|---:|
| Machine candidates reviewed | 100 |
| Accepted article starts | 86 |
| Rejected false-positive boundaries | 14 |
| Clear headword OCR corrections | 4 |

This first review validates the presence of a headword and the beginning of an article. It does not by itself validate the complete article body or linguistic interpretation.

## Page-layout reconstruction

Printed pages 301–317 have now been modeled explicitly as 17 two-column pages (`data/facsimile/page_layout_301_317.csv`), with left/right column order separated from OCR line order.

This responds to a central methodological finding: the supplied OCR does not always preserve the reading order of Steffel's two-column pages. A genuine headword can therefore be followed in the OCR by text that visually belongs to another article or column. `RHD-S1809-00065` (`Abweg`) is the first clear example: the headword is present on printed page 301, while the machine OCR block absorbs material from the neighboring `Adern` article.

## First complete article-text batch

`RHD-DIP-001A` adds ten complete short article transcriptions selected only where article boundaries and text are visually clear:

- `Abweg`, `Allmächtig`, `Allwiſſend` (p. 301);
- `Anderer`, `Anderſt`, `Anfaſſen`, `Anfechten`, `Anfechter`, `Anzünden` (p. 302);
- `Aufmerken` (p. 304).

These are marked `diplomatic_transcription_ai_assisted`. Source spelling and punctuation are retained; typographic line wrapping is not encoded. `human_verified=false`: independent human/philological verification remains pending.

The next editorial work is to extend page-layout-based article reconstruction through the remaining accepted starts on pages 301–317, then continue with a second facsimile batch.
