---
layout: default
title: Python & R
parent: Computing Basics
grand_parent: Dry Lab
has_children: false
nav_order: 30
---

<!-- MOVED + edited from docs/Intro to Computation/Programming.md — Python & R sections only. The original "Intro to Python" heading had no content in the live repo; kept as a flagged gap rather than invented. -->

# {{page.title}}

## Intro to Python

<!-- existing page had this heading with no content underneath — kept as a flagged gap -->

[NEEDS CONTENT]

## Intro to R

Quite a lot of biostat work runs in R, for a few reasons:

* **CRAN** — the "Comprehensive R Archive Network," where most additional R packages live. `install.packages("magrittr")` fetches and installs from CRAN automatically; `library(magrittr)` then loads it.
* **Statistics-oriented syntax** — the base package (loaded automatically) includes native linear algebra/set operators, like `%in%` for set intersection and `%o%` for outer products, plus built-in plotting and test datasets/`r*` distribution functions.
* **RStudio** — the IDE for running, troubleshooting, and profiling code directly from the source editor. Customize its look as you like.

If working with a large dataset: the RStudio server has a **20GB memory limit**. Beyond that, use an interactive session with more memory via the command line (see [Command Line](CommandLine)). If you figure out running your own RStudio server on the HPC to tunnel into, reach out to Jeff.
