---
layout: default
title: Project Setup
nav_order: 20
parent: Dry Lab
has_children: false
---

<!-- NEW — drafted directly from your outline (project id -> meta sheet -> project-id folder -> username subfolder -> compute -> push to GitHub -> coding agent notes). I don't have a source for the actual project-ID registry or meta-sheet template, so those steps are flagged. Folder-path conventions below are inferred from Programming.md's LAB_SOFTWARE path and the old Drive onboarding doc's mention of "ycheng11_lab or ycheng11lab_hippa folders" — please confirm these are the right paths. -->

# {{page.title}}

**Owner:** Gaby

<!-- TODO (Gaby): per Yuyan, this page's content should move to a Google Drive doc — replace the content below with a link to it once that's set up. -->
Standard setup for a new dry-lab project, start to finish.

## 1. Assign a Project ID
<!-- NEEDS LAB INPUT: who assigns this, and where's the registry? A Drive sheet? Ask Yuyan/Jeff. -->
When initiating a new analysis project (ex. single-cell, spatial, etc.,), refer to the [Project Management Sheet](https://upenn.box.com/s/7n3fo09ud9lb2uyb7le6xf6fkn382d6m) on box. Follow the instructions below for adding a new project ID to the management sheet.

Format: prj#### — first 2 digits = last 2 digits of year; last 2 digits = next sequential number.
Example: if last ID is prj2604, next is prj2605.

## 2. Acquire the Metadata Sheet
<!-- NEEDS LAB INPUT: is this the "Cheng Lab Collaborator Metadata Submission" form referenced in Drive, or a separate per-project template? -->
For tracking sample metadata, use the [Cheng Lab sample metadata template](https://upenn.box.com/s/7wa2eajjmsf1ah3vnka4wf45fpxcdtna), which can be found on Box.

## 3. Create the Project Folder

On the PMACS server, create a folder named for the project ID under the appropriate lab project space (all analyses containing patient data should be performed in the hipaa_ycheng11lab directory):
    
    /project/ycheng11lab/<project-id>/
    /project/hipaa_ycheng11lab/<project-id>/


<!-- TODO: confirm this is the right root path — Programming.md references /project/hipaa_ycheng11lab/software/ for shared lab software specifically, and the old Drive doc separately mentions "ycheng11_lab" (non-HIPAA) vs "ycheng11lab_hippa" (HIPAA) project spaces. Which one is the default for a new project, and when do you use the other? -->

## 4. Create Your Own Subfolder

Inside the project folder, create a subfolder under your PennKey/username:

    /project/ycheng11lab/<project-id>/<your-username>
    /project/hipaa_ycheng11lab/<project-id>/<your-username>/

Do your compute here — keep intermediate/working files scoped to your own subfolder so the shared project folder stays organized (see [Lab Duties](../Lab-Management/LabDuties) — Jeff's server-cleanup responsibilities depend on this).

## 4. Data Copying

DO NOT COPY RAW DATA

Raw data files are very large and take up a lot of space on the server. Create soft links to raw data when necessary (data pre-processing is likely the only time you will need to soft link to large data files).

## 5. Data Preprocessing ("Master Analysis")

All snRNAseq, scRNAseq, and spatial data go through a pre-processing pipeline. These pre-processing pipelines have multiple steps that are specific to the type of data being analyzed. *Any pre-processing steps, and their respective output folders, should remain within the shared project directory. Any further downstream analysis (post-processing) should be performed in your user-specific directory.

*Only the lab member responsible for completing the pre-processing should edit data files within the shared project directory.

## 6. Virtual Project Environments

A virtual environment is an isolated, self-contained space that holds a specific version of a programming language and its own dedicated set of software libraries or packages. Our lab uses virtual environments (venvs) for several reasons:

* Avoid Conflicts: Different software projects often need different versions of the same library. Keeping them separate stops one project or type of anlysis from breaking another.

* Reproducible Workflows: Using venvs standardizes data analysis across multiple projects, ensuring consistent setups and fully replicable results.

Venvs for our lab can be found under

    /project/hipaa_ycheng11lab/software/virtual_environments


These venvs are not to be edited or changed for specific projects. If a project-specific venv is needed, one should be created under your user folder for that project
    
    /project/ycheng11lab/<project-id>/<your-username>/virtual_environments/<name-of-venv>/

## 7. Push Scripts to the Lab GitHub

Code/scripts (not data) go to the [lab-manual](https://github.com/yuyanchenglab) org's project repos, not the server. See [Lab Tutorials → GitHub Usage](Tutorials/Access/GitHubUsage) for the actual git workflow.

Keep large or sensitive data out of git — see the `.gitignore` conventions in GitHub Usage.

## 8. Using a Coding Agent

If you're using a coding agent (Claude Code, Codex, etc.) to help with the project, see:

* [Claude to PARCC](Tutorials/CodingAgents/ClaudeToPARCC)
* [Claude to PMACS](Tutorials/CodingAgents/ClaudeToPMACS)
* [Claude to Git](Tutorials/CodingAgents/ClaudeToGit)
* [Codex to PMACS](Tutorials/CodingAgents/CodexToPMACS)
* [Codex to Git](Tutorials/CodingAgents/CodexToGit)

<!-- NEEDS LAB INPUT: any project-management-specific rules for agent use — e.g. should a CLAUDE.md live in every project folder by convention? Should agent-authored commits be flagged somehow? -->
