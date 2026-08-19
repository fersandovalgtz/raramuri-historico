# Rarámuri Histórico Digital

**Corpus Steffel 1791/1809 · historical-digital scholarly edition · research data · reproducible infrastructure**

[Project site](https://fersandovalgtz.github.io/raramuri-historico/) · [Zenodo Concept DOI](https://doi.org/10.5281/zenodo.21957212) · [Version 1.0.1 DOI](https://doi.org/10.5281/zenodo.21958018) · [Spanish README](README.md)

Rarámuri Histórico Digital (RHD) is a research infrastructure for transforming historical sources on the Rarámuri language into traceable, versioned, citable, interoperable and reproducible digital objects without erasing documentary form or promoting computational inference to linguistic fact.

The reference implementation is the **Steffel 1791/1809 Corpus**, built from Matthäus Steffel's *Tarahumarisches Wörterbuch*, published posthumously in 1809. The `1791/1809` formula distinguishes the documented manuscript/epistolary horizon from the printed edition used by RHD; it does not indicate two printed editions.

## Current archived release

| Dimension | Status |
|---|---:|
| Release | **v1.0.1** |
| Documentary candidates reviewed | **2,495 / 2,495** |
| Active lexicographic articles | **1,965** |
| Preserved false boundaries | **530** |
| AI-assisted diplomatic transcriptions | **1,965 / 1,965** |
| PHIL cases re-collated | **482 / 482** |
| Terminal unresolved cases | **46** |
| Diachronic computational relations | **298 candidates** |
| IIIF Presentation 3 | **84 Canvases** |
| Record-to-Canvas links | **1,965** |

RHD v1.0.1 is a **machine-only** scholarly edition. It does **not** claim independent human philological or linguistic validation. AI-assisted confirmations, corrections and unresolved readings remain explicitly typed and are never presented as human verification.

## Evidence architecture

RHD uses a non-destructive chain of evidence:

**historical witness → raw OCR → segmentation → boundary/direction collation → documentary reconstruction → AI-assisted diplomatic transcription → uncertainty triage → PHIL re-collation → derived layers → independent human review when available**.

Source evidence is never overwritten. Provenance accompanies each transformation, and authority levels remain distinct across OCR, machine-assisted collation, editorial proposals, human review and linguistic analysis.

## Interoperability and reproducibility

The repository provides structured and derived representations in CSV, JSON, XML and SQLite, a rich RHD TEI representation, a strict TEI Lex-0 projection, IIIF Presentation 3 resources, schemas, source profiles, checksums and reproducible generation/validation scripts.

Key documents: [Reproducibility](REPRODUCIBILITY.md) · [FAIR/FAIR4RS self-assessment](FAIR_ASSESSMENT.md) · [Provenance](PROVENANCE.md) · [Datasheet](DATASHEET.md) · [Governance](GOVERNANCE.md) · [Editorial policy](EDITORIAL_POLICY.md).

## Citation and persistent identifiers

Project / all versions: **https://doi.org/10.5281/zenodo.21957212**

Current archived version: **https://doi.org/10.5281/zenodo.21958018**

Recommended citation:

> Sandoval Gutierrez, Fernando. 2026. *Rarámuri Histórico Digital — Corpus Steffel 1791/1809*, version 1.0.1. Zenodo. https://doi.org/10.5281/zenodo.21958018

When an argument depends on a historical reading, cite Steffel 1809 and the relevant printed page in addition to RHD.

## Licenses

Software and original code are released under the [MIT License](LICENSE). Original RHD data, metadata, annotations, translations and editorial layers are released under [CC BY 4.0](DATA_LICENSE.md). Historical sources and third-party materials retain their own legal status and provenance.

## Research ecosystem

RHD is the historical-documentary node of a broader open research ecosystem. Its closest sister project is [Rarámuri Digital](https://github.com/fersandovalgtz/raramuri-digital), a contemporary lexicographic research infrastructure. Historical and contemporary resources remain separate; cross-project relations are typed and reviewable rather than automatically merged.

## Responsible researcher

**Fernando Sandoval Gutierrez**  
Universidad Autónoma de Ciudad Juárez · Universidad CEEES / CEEES Cuauhtémoc  
ORCID: [0000-0002-3168-6725](https://orcid.org/0000-0002-3168-6725)  
Email: [fernando.sandoval@uacj.mx](mailto:fernando.sandoval@uacj.mx)
