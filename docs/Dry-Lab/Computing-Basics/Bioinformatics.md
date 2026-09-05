---
layout: default
title: Intro to Bioinformatics
parent: Computing Basics
grand_parent: Dry Lab
has_children: false
nav_order: 50
---

<!-- MOVED from docs/Intro to Computation/Bioinformatics.md, content unchanged -->

# {{page.title}}

Where we overlap with the biology team.

## Why?

We want to look both broadly and specifically, which means data past the size of Excel t-tests. We're looking for expression signatures that clue us into mechanisms of sight degradation — then searching for medicines showing the anti-signature as potential treatments.

## Central Dogma

DNA is transcribed into RNA and translated into proteins.

## Pairing Desired Information with Data Type

* Bulk RNA-seq: cheap, broad characterization of expression
* Bulk ATAC-seq: broad characterization of the epigenome
* CutNRun: *(description TODO)*
* HiChIP-seq: broad characterization of chromatin configuration
* Single Cell RNA-seq: precise characterization of expression, clustered by cell type
* Single Cell ATAC-seq: precise characterization of the epigenome, clustered by cell type
* Spatial Transcriptomics: precise, in-situ characterization of genes of interest; cell-cell communication

## External Resources

* Journal articles — read published methods to see what other labs are doing. The lab runs Journal Club instead of the usual lab meeting once a month.
* [Seurat](https://satijalab.org/seurat/) (Satija lab) — R package for single-cell analysis, with vignettes for default workflows.
* [Single Cell Best Practices](https://www.sc-best-practices.org/) — free e-book, current as of 2023.[^1]
* [Analyzing RNA-seq data with DESeq2](https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html) — vignette by DESeq2's authors.
* [Biostars](https://www.biostars.org/) — bioinformatics Q&A forum (Michael Love, DESeq2's author, is an active member).
* YouTube channels (Jeffrey Maurer's picks): [Illumina](http://www.youtube.com/@IlluminaInc) (sequencing-machine presentations), [StatQuest](https://www.youtube.com/@statquest) (stats/bioinformatics intros), [Bioinformagician](https://www.youtube.com/@Bioinformagician) (specific pipeline walkthroughs), [Sanbomics](https://www.youtube.com/@sanbomics) (detailed task walkthroughs).

[^1]: Heumos, L., Schaar, A.C., Lance, C. et al. Best practices for single-cell analysis across modalities. *Nat Rev Genet* (2023). https://doi.org/10.1038/s41576-023-00586-w
