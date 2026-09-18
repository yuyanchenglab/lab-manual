---
layout: default
title: Xenium
parent: Tutorials
grand_parent: Wet Lab
nav_order: 60
---

<!-- NEEDS LAB INPUT: this is the wet-bench Xenium protocol (tissue prep, slide loading, instrument run) — distinct from the dry-lab analysis pipeline doc. No content exists yet. Per the Mouse Glaucoma project notes (Drive), Gaby and Kelly have run Xenium tissue prep together and coordinated with Chris (vendor) on instrument installation — they're the likely authors. -->

# {{page.title}}

**Owner:** Gaby

<!-- TODO (Gaby): per Yuyan, this page's content should move to a Google Drive doc — replace the content below with a link to it once that's set up. -->
## Overview

Our lab houses a Xenium Analyzer platform from 10x Genomics that performs imaging-based spatial transcriptomics. For lab members who will be involved in performing or assissting collaborators with Xenium experiments, please review the [Xenium SOP](https://drive.google.com/file/d/1aA3V9SrkZ3vc8SjTEyslsPVGT3W6hKwE/view?usp=sharing) document, which covers setting up new Xenium experiments, sample preparation, data generation and handling, and instrument handling.

## Materials

Kits for Xenium experiemnts can be purchased directly from [10x Genomics](https://www.10xgenomics.com/platforms/xenium). Custom probe panels can be designed through the [Xenium Panel Designer](https://www.10xgenomics.com/support/software/xenium-panel-designer/latest). This requires an account with 10x Genomics. See the [Cheng Lab Accounts Information spreadsheet](https://docs.google.com/spreadsheets/d/18-Hlodp0looHGu7hGMEuRxE0vloXJTvM7aFtwfmxMYc/edit?gid=0#gid=0) for login details. 

All reagents needed to run Xenium experiemnts are housed in lab. If performing an experiment for a collaborator, we ask that they purchase their own nuclease-free water, 200-proof  alcohol, xylene (if preparing FFPE tissues), methanol and either PFA or Formaldehyde (if preparing fresh frozen tissue), as well as any reagents needed for performig post-xenium staining. A list of reagents needed to run a Xenium experiemnt can be found in the [Xenium In Situ Gene Expression Protocol Planner](https://www.10xgenomics.com/support/in-situ-gene-expression/documentation/steps/experimental-design-and-planning/xenium-in-situ-gene-expression-%E2%80%93-protocol-planner). Review the items in the [Xenium Cost Breakdown and Reagent Usage](https://drive.google.com/drive/folders/1UoEudZqlgDtxW96rhnAeipmv92x-PzBa?usp=sharing) for further details on the materials needed.

## Tissue Prep Protocol

The Xenium Analyzer supports workflows for Fresh Frozen or FFPE tissues. Work with Wei (Cheng Lab memebrs) or a core if you are not planning to section yourself. See the guides below for further details.

[Xenium In Situ Fresh Frozen Tissue Preparation Handbook](https://www.10xgenomics.com/support/in-situ-gene-expression/documentation/steps/tissue-prep/xenium-in-situ-spatial-profiling-for-fresh-frozen-%E2%80%93-tissue-preparation-guide)
[Xenium In Situ for FFPE Tissue Preparation Handbook](https://www.10xgenomics.com/support/instruments/xenium-analyzer/xenium-in-situ-spatial-profiling-for-ffpe-%E2%80%93-tissue-preparation-guide)

10x Genomics does not officially support a Fixed Frozen protocol for fixed tissues embedded in OCT. However, there is an unofficial protocol that outlines how to perform such experiments. See ["Are fixed tissues embedded in OCT compatible with Xenium?"](https://kb.10xgenomics.com/s/article/17968908868877-Are-fixed-tissues-embedded-in-OCT-compatible-with-Xenium)

## Instrument Run

*In preparation for a new Xenium experiment, a readiness test should be performed at least one week prior to the planned start date of the experiment. Further details on performing a readiness test can be found in [Xenium Analyzer User Guide](https://www.10xgenomics.com/support/instruments/xenium-analyzer/xenium-analyzer-user-guide).
On the day that slides will be loaded, the Xenium Analyzer will perform a microfluidics check when a new experiment is inititaited. Once that has completed, buffers, slides, and other platform components can be loaded. **Work with Gaby, Yuyan, or your collaborator for region selection to ensure proper annotation of sections.

*Handling of the Xenium Analyzer, including reagent loading and cleanup, is performed by Gaby. DO NOT touch the intrument without supervision or explicit permission. 
** Xenium limits region selection to 8 unique regions. If a slide has more than 8 sections, multiple sections will need to be combined into a single region.

## Results / Output

Several folders and files are generated for each region selected during a Xenium run. All data should be transferred and uploaded to the appropriate PMACS directory. See [Xenium SOP](https://drive.google.com/file/d/1aA3V9SrkZ3vc8SjTEyslsPVGT3W6hKwE/view?usp=sharing) for further details on where data should be placed.

For those interested in reviewing Xenium data, 10x Genomics provides an interactive visualization tool called [Xenium Explorer](https://www.10xgenomics.com/support/software/xenium-explorer/latest), which can be downloaded locally onto your computer. *Collaborator's that wish to see their data must provide THEIR OWN hard drive for data transfer. Data visualization in Xenium Explorer requires the full data output for each region. This is a lot of data so collaborator's should be made aware they may not be able to house the data locally on their computer.

*Data transfer from the Xenium computer to the PMACS server is performed with a 1TB hard drive provided by 10x Genomics. DO NOT give this hard drive to collaborators. If they wish to transfer the data to their computer, they must come to the lab space to do so, OR provide you with their own hard drive for you to perform the data transfer yourself.

## Instrument Maintenance

For further details on maintenance of the Xenium Analyzer, please refer to the [Xenium Maintenance SOP](https://drive.google.com/file/d/14oa_jnDXeLxhHWfKO1veVv7jnViCQsGj/view?usp=sharing).

## Related

* Analysis pipeline: [Xenium Spatial Pipeline Usage](../../Dry-Lab/Tutorials/Pipelines/XeniumSpatialPipeline)
