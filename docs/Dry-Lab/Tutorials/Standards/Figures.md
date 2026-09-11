---
layout: default
title: Figures
parent: Standards
nav_order: 100
---

<!-- MOVED from docs/Dry Lab SOPs/Figures.md. NOTE: my fetch of the live file returned a summary, not the raw markdown, so treat this as faithful-but-paraphrased and diff against the source before publishing. -->

# {{page.title}}

## Size and Format

Figures are often no bigger than 3" x 3", with text typically below 10pt Arial. Both R and Python support manual size adjustments for overall figures and plotting panels.

## File Type

Save as PDF — it permits post-production editing (e.g., in Illustrator) without compromising the underlying data. R-generated PDFs are particularly amenable to this.

## Workflow Philosophy

Done is better than perfect. Expect that a first pass will need refinement after consultation with Yuyan to meet publication standards.

## Retina Cell Ordering

When visualizing retinal cells, use this order: RGC, AC, HC, BC, MG, Cone, Rod, Endothelial, Astrocytes, Microglia.

## ChengLabThemes Package

A locally-installed R package provides styling functions for lab-standard figures ([repo](https://github.com/yuyanchenglab/ChengLabThemes)). It remains unreleased pending v1.0.0, timed to the lab's first manuscript, once the team finalizes aesthetic preferences.
