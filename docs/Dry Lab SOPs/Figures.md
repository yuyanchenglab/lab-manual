---
layout: default
title: Figures
parent: Dry Lab SOPs
has_children: false
nav_order: 20
---

# {{page.title}}

## Principles for Figure Design

We want our results to meet publishing guidelines, be presented their intended meaning clearly and be aesthetically pleasing. For that, there are a couple of things to keep in mind.

* Figures are often no bigger than 3 x 3. Both R and python allow you to manually adjust the size of your figures overall and the size of the plotting panel within the image. Text is often kept below 10 pt font Arial.
* Save as PDF. The PDF format allows manipulated without affecting the underlying data. Alterations such as rescaling and moving the legend are done in Illustrator by Yuyan. The PDF's from R are typically easier to adjust, so prefer plotting in R.
* Done is better than perfect, and what is perfect to you will likely not match guidelines and require additional adjustment after consulting Yuyan.
* When plotting retina cells, keep them in anatomical order: RGC, AC, HC, BC, MG, Cone, Rod, Endothelial, Astrocytes, Microglia

## ChengLabThemes

This is an R package installed locally on the HPC server and contains many helper functions for creating figures for the lab that match previous work.