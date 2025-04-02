---
layout: default
title: Source Control
nav_order: 30
parent: Intro to Computation
has_children: false
---

# {{page.title}}

## Intro to Git

Git is a version control tool. It is used to keep track of how text gradually changes in code. Here are the commands to get started:

```bash
$ git clone https://github.com/[OWNER]/[REPO].git # Download a repo from Github
$ git status # View changed files
$ git diff [FILE] # View what the changes are in the repo, differences in just a set of files in the repo
$ git add NEW_FILE # Tell git that you want it to start track changes in this file from now on
$ git stage TRACKED_FILE # Specify what files you want to save
$ git commit –m “DESCRIBE WHAT YOU CHANGED” # Locally save changes in staged files and start tracking changes in newly added files
$ git push # Sync github server’s version of the repo's files with local repo. Allows everyone to see your changes.
```

## Github Usage

Make a [github.com](github.com) account and give the username to Jeff ([jeffrey.maurer@pennmedicine.upenn.edu](jeffrey.maurer@pennmedicine.upenn.edu)). We can add you as a contributor if you are here long-term in the dry lab. We prefer that as few hands touch the main branches as possible.

In .gitignore, add "\*_small\*" and "\*_toy\*" for projects where new ground will be broken, requiring small test data.

## Intro to Virtual Environments

WIP

The hippa directory has a software directory that has a virtual environment directory. Usage has not been fully described.