---
layout: default
title: GitHub Usage
parent: Access
nav_order: 30
---

<!-- MOVED + expanded from docs/Intro to Computation/SourceControl.md. IMPORTANT: my fetch of the live SourceControl.md returned a summary rather than the raw file (the fetch tool condensed it), so the "Getting Access" and ".gitignore" sections below are faithful to that summary, but the command examples under "Everyday Workflow" are standard practice I've added, not sourced from the original file. Please diff this against the real file before publishing. -->

# {{page.title}}

**Owner:** Jeff

<!-- TODO (Jeff): per Yuyan, this page's content should move to a Google Drive doc — replace the content below with a link to it once that's set up. -->
## Getting Access

Create a GitHub account, then send your username to Jeff ([jeffrey.maurer@pennmedicine.upenn.edu](mailto:jeffrey.maurer@pennmedicine.upenn.edu)) for contributor access to the relevant repo(s).

We prefer that as few hands as possible touch the main branch directly — use a branch + pull request for anything beyond a trivial fix.

## Everyday Workflow

```
git clone <repo-url>
git status
git diff
git add <file>
git commit -m "short description of the change"
git push
```

For a new piece of work, branch first:

```
git checkout -b <your-name>/<short-description>
# make changes, commit, push
git push -u origin <your-name>/<short-description>
```

Then open a pull request on GitHub for review before merging to `main`.

## Project Repos vs. This Manual

Project code/scripts belong in their own project repo (see [Project Management → Dry Lab](../../ProjectSetup)), not in `lab-manual`. `lab-manual` is only for onboarding/SOP content like this page.

## .gitignore Conventions

For projects with test data, exclude files matching `*_small*` and `*_toy*` patterns in `.gitignore`.

## Virtual Environments

The lab maintains a shared software directory for reproducible environments across projects. Check that directory's README for the specific setup instructions for your project.

<!-- TODO: this section needs the actual path and more specifics — flagged since the source summary was thin here too -->
