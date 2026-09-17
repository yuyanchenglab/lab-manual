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

[NEEDS INPUT]

## 2. Acquire the Metadata Sheet

<!-- NEEDS LAB INPUT: is this the "Cheng Lab Collaborator Metadata Submission" form referenced in Drive, or a separate per-project template? -->

[NEEDS INPUT]

## 3. Create the Project Folder

On the PMACS server, create a folder named for the project ID under the appropriate lab project space:

    /project/hipaa_ycheng11lab/<project-id>/

<!-- TODO: confirm this is the right root path — Programming.md references /project/hipaa_ycheng11lab/software/ for shared lab software specifically, and the old Drive doc separately mentions "ycheng11_lab" (non-HIPAA) vs "ycheng11lab_hippa" (HIPAA) project spaces. Which one is the default for a new project, and when do you use the other? -->

## 4. Create Your Own Subfolder

Inside the project folder, create a subfolder under your PennKey/username:

    /project/hipaa_ycheng11lab/<project-id>/<your-username>/

Do your compute here — keep intermediate/working files scoped to your own subfolder so the shared project folder stays organized (see [Lab Duties](../Lab-Management/LabDuties) — Jeff's server-cleanup responsibilities depend on this).

## 5. Push Scripts to the Lab GitHub

Code/scripts (not data) go to the [lab-manual](https://github.com/yuyanchenglab) org's project repos, not the server. See [Lab Tutorials → GitHub Usage](Tutorials/Access/GitHubUsage) for the actual git workflow.

Keep large or sensitive data out of git — see the `.gitignore` conventions in GitHub Usage.

## 6. Using a Coding Agent

If you're using a coding agent (Claude Code, Codex, etc.) to help with the project, see:

* [Claude to PARCC](Tutorials/CodingAgents/ClaudeToPARCC)
* [Claude to PMACS](Tutorials/CodingAgents/ClaudeToPMACS)
* [Claude to Git](Tutorials/CodingAgents/ClaudeToGit)
* [Codex to PMACS](Tutorials/CodingAgents/CodexToPMACS)
* [Codex to Git](Tutorials/CodingAgents/CodexToGit)

<!-- NEEDS LAB INPUT: any project-management-specific rules for agent use — e.g. should a CLAUDE.md live in every project folder by convention? Should agent-authored commits be flagged somehow? -->
