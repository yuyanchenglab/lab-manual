---
layout: default
title: Bioconda
parent: Computing Basics
grand_parent: Dry Lab
has_children: false
nav_order: 40
---

<!-- MOVED from docs/Intro to Computation/Bioconda.md. NOTE: my fetch returned a summary, not the raw file — diff against the source before publishing. -->

# {{page.title}}

How to test and publish a conda package to Bioconda, using `x-spear` as the reference example.

## Local Testing

Create a conda environment and install `conda-build`/`conda-verify`. Place data files in `src/<package>/data`, and update version numbers in both `setup.py` and `meta.yaml` before building locally.

## Repository Release

After pushing to `main`, create a GitHub release tagged `vX.Y.Z` (lowercase `v` required).

## Bioconda Publication

Fork `bioconda-recipes`, update `meta.yaml` with the new release's SHA256 hash:

```
wget -O- https://github.com/<user>/<repo>/archive/refs/tags/v<version>.tar.gz | shasum -a 256
```

Open a pull request against `bioconda-recipes`.

## Final Step

Comment `@BiocondaBot please add label` on the PR. The Bioconda team reviews; once approved, the package appears on the bioconda channel within 30–60 minutes.
