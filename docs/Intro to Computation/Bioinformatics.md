---
layout: default
title: Intro to Bioinformatics
nav_order: 40
parent: Intro to Computation
has_children: false
---

# {{page.title}}

Here is where we can overlap with the biology team.

## Why?

We want to look both broadly and specifically, but that requires our data size to grow past the size of excel t-tests. In our lab, we are looking for signatures that cell expression reveals to us that can clue is into the mechanisms of sight degradation. We can use that to search for medicines that show the anti-signature as potential treatments.

## Central Dogma

DNA is transcribed into RNA and translated into proteins.

## Pairing Desired Information with Data Type

* Bulk RNA-seq: Cheap, broad characterization of expression
* Bulk ATAC-seq: Broad characterization of epigenome
* CutNRun:
* HiChIP-seq: Broad characterization of chromatin configuration
* Single Cell RNA-seq: Precise characterization of expression clustered by cell type
* Single Cell ATAC-seq: Precise characterization of epigenome clustered by cell type
* Spatial Transcriptomics: Precise characterization of genes of interest in situ; Cell-Cell Communication

## External Resources

* Journal articles. As a scientist, there is no way around it. You need to read published work and read through their methods to see what other labs are doing with their data. We have Journal Club instead of our usual lab meeting once a month in our lab.
* [Seurat](https://satijalab.org/seurat/) by the Satija lab is an R package that can do quite a few single cell sequencing analysis. Their website is full of helpful vignettes to show you default workflows for many projects.
* [Single Cell Best Practives](https://www.sc-best-practices.org/)[^1] is a full-length e-book available for free and is current as of 2023.

[^1]: Heumos, L., Schaar, A.C., Lance, C. et al. Best practices for single-cell analysis across modalities. Nat Rev Genet (2023). https://doi.org/10.1038/s41576-023-00586-w

* [Analyzing RNA-seq data with DESeq2](https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html) is an amazing vignette by DESeq2's authors Michael Love et al.
* [Biostarts](biostarts.org) is an amazing bioinformatics forum for specific questions you need answered. Additionally, Michael Love is an active member here!
* Here are a few YouTube channels that I, Jeffrey Maurer, personally approve for various reasons related to bioinformatics:
    * [Illumina](http://www.youtube.com/@IlluminaInc) ([website](illumina.com)) is the company that produces sequencing machines and it could be useful to view some of their presentations to understand how our data is produced and why it may look how it does.
    * [StatQuest](https://www.youtube.com/@statquest) ([website](https://statquest.org/)) features introductions to various statistical, data science and bioinformatics topics by Dr. Josh Starmer from UNC-Chapel Hill.
    * [Bioinformagician](https://www.youtube.com/@Bioinformagician) ([website](https://bioinformagician.org/)) provides highly specific tutorials on various topics, such as the single cell ATACseq pipeline or a bioinformatics-specific file format overview.
    * [Sanbomics](https://www.youtube.com/@sanbomics) ([website](https://www.sanbomics.com/)) is another channel with detailed walkthroughs of common bioinformatics tasks.