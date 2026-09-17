---
layout: default
title: Sequencing
parent: Tutorials
grand_parent: Wet Lab
nav_order: 55
---

<!-- NEW — added per lab request. Covers sequencing submission after library prep; referenced from Chromium 3' ("where libraries go for sequencing submission") but not previously documented as its own page. -->

# {{page.title}}

**Owner:** Gaby

<!-- TODO (Gaby): per Yuyan, this page's content should move to a Google Drive doc — replace the content below with a link to it once that's set up. --> 
## Submission Protocol
All sequencing for scRNAseq or snRNAseq experiemnts are performed by Novogene. Details for how to initiate a new sequencing projecg with Novogene is covered in the [Sequencing_SOP](https://drive.google.com/file/d/1nniogp2uDKybHIAeP5rGpAf5MbAotInm/view?usp=sharing)

## Materials for Shipping
Before submitting a request for pickup, ensure the necessary materials for sample shipment are in the lab. This includes packing tape, an insulated styrofoam box, 2 copies of the shipping label, dry ice, 50ml conical tubes, parafilm, and a small- or medium-sized ziploc baggy. Instrucitons on how to prepare tubes to be shipped are provided when sample submission is initiatied for the project in the Novogenen account.

## Results / Output
*Turnaround time for sequencing results on a full lane of a (10B or 25B) flow cell is typicall 7-10 days after samples have been received. Novogene will notify via email when data is ready to be released. For downloading data to the PMACS server, Novogene will provide an lftp command-line file transfer link. Details on how to use this link can be found within the Sequencing_SOP. Unless otherwise communicated, Novogene will provide raw sequencing data as compressed FASTQ files (.fq.gz or .fastq.gz).

*If partial sequencing on a lane of a 25B flow cell has been requested, turnaround time is typically longer, but usually no longer than 1 month.

[NEEDS INPUT — expected turnaround, file delivery format, naming/tracking conventions]

## Related
* Library prep: [Chromium 3'](Chromium3prime)
* Analysis pipeline: [scRNAseq Pipeline Usage](../../Dry-Lab/Tutorials/Pipelines/scRNAseqPipeline)
