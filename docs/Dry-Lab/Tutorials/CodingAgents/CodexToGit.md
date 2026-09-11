---
layout: default
title: Codex to Git
parent: Coding Agents
nav_order: 55
---

<!-- CONTENT PROVIDED by Yuyan (uploaded connectcodextogithub.md), lightly adapted to this page's title/front matter. Owner unchanged: Yuyan. -->

# {{page.title}}

**Owner:** Yuyan

This guide uses [`yuyanchenglab/lab-manual`](https://github.com/yuyanchenglab/lab-manual) as the example. The goal is to complete the entire workflow in the Codex desktop app:

1. Open the local repository.
2. Create or select a branch.
3. Ask Codex to review and edit files.
4. Inspect and refine the diff.
5. Validate the site.
6. Commit and push the branch.
7. Create a pull request.
8. Wait for CI and merge the pull request into `main`.
9. Monitor GitHub Pages and verify the published site.

## One-time setup

### 1. Install and connect the GitHub plugin

The GitHub plugin gives Codex authenticated access to GitHub repositories, branches, pull requests, issues, CI, and supported publishing operations.

1. Open **Plugins** in the ChatGPT desktop app.
2. Search for the official **GitHub** plugin.
3. Install it and select **Connect**.
4. Complete GitHub authorization in the browser.
5. Give the connection access to `yuyanchenglab/lab-manual`.
6. If GitHub requests organization approval, have an organization owner approve it.
7. Start a new Codex task after connecting the plugin.

Plugin connections have their own authentication. They do not automatically reuse credentials from Terminal or the GitHub CLI.

### 2. Authenticate local GitHub operations

The Codex desktop app can stage, commit, push, and create a pull request without leaving the app. Local Git authentication is also useful for loading pull-request context and for Git operations performed through the integrated shell.

On macOS:

```bash
brew install gh
gh auth login -h github.com --web --git-protocol https
gh auth setup-git
gh auth status
```

Complete the browser authorization. `gh auth status` should report the intended account as logged in and active.

Never paste a GitHub token into a Codex prompt.

### 3. Clone the lab manual

If it is not already on the computer:

```bash
cd ~/Downloads
gh repo clone yuyanchenglab/lab-manual
cd lab-manual
```

Confirm that the remote is correct:

```bash
git remote -v
```

Expected remote:

```text
https://github.com/yuyanchenglab/lab-manual.git
```

### 4. Open the repository in Codex

1. Open Codex in the ChatGPT desktop app.
2. Add or open `~/Downloads/lab-manual` as a local project.
3. Start a new task in that project.
4. Choose **Local** to edit the current checkout directly. Choose **Worktree** when you want Codex to isolate the work from other changes in your checkout.

For a simple documentation update, **Local** is the most direct workflow. Before starting, make sure unrelated uncommitted changes are not mixed into the checkout.

## Workflow for making a change

The following example creates a documentation branch, updates the lab manual, reviews the result, and pushes it.

### Step 1: Inspect the repository and create a branch

Send Codex this prompt:

```text
In this lab-manual repository, inspect the current Git status, branch, and remotes.
Preserve any existing user changes. Fetch origin, update from origin/main, and
create a new branch named docs/update-onboarding. Do not edit files yet.
```

Codex should report:

- the current branch;
- whether the working tree is clean;
- the configured `origin` URL; and
- the newly created branch.

If the working tree contains unrelated changes, decide whether to commit, stash, move, or keep them before continuing. Do not let Codex discard them automatically.

### Step 2: Ask Codex to review the relevant content

Example prompt:

```text
Review the onboarding documentation in docs/Onboarding and the related links
from docs/Joining-the-Lab. Identify outdated, duplicated, or broken content.
Report your findings first. Do not edit anything yet.
```

This read-only pass lets you agree on the scope before files change.

For a formal Git diff review, type `/review` in the prompt box. Codex can review uncommitted changes, a commit, or the current branch against a base branch.

### Step 3: Request the edits

After reviewing the findings, send a focused implementation prompt:

```text
Apply the agreed onboarding documentation changes. Keep the Just the Docs
front matter and navigation structure valid, preserve unrelated content, and
update any affected internal links. Show me a concise summary when finished.
Do not commit or push yet.
```

Codex edits the files in the open project. Because the task is paused before committing, you can inspect everything first.

### Step 4: Inspect and refine the diff

Open the review/diff pane in Codex. It reflects the repository's actual Git state, including changes made by Codex and any changes made elsewhere.

Review the diff by file or hunk. You can:

- stage or revert individual hunks;
- stage or revert complete files;
- add inline comments to specific lines; and
- ask Codex to address those comments.

Example follow-up:

```text
Address my inline comments. Keep the scope minimal and do not commit or push.
```

Then run `/review` and select **Review uncommitted changes**. Resolve important findings before committing.

### Step 5: Validate the lab manual

`lab-manual` is a Jekyll site using the Just the Docs theme. On first setup, install its Ruby dependencies:

```bash
bundle install
```

Build the site:

```bash
bundle exec jekyll build
```

For a local browser preview:

```bash
bundle exec jekyll serve
```

Then open `http://localhost:4000`.

You can ask Codex to do the non-interactive validation directly:

```text
Run the appropriate validation for this Jekyll documentation site. Build it
with bundle exec jekyll build, inspect any errors or warnings relevant to my
changes, and fix only problems caused by this branch. Do not commit or push.
```

Review the final diff again after any fixes.

### Step 6: Commit and push from Codex

You can use the app's **Commit or push** controls, or ask Codex to perform the exact operation.

Example prompt:

```text
Review the final Git diff and confirm the Jekyll build passed. Commit only the
changes from this task with the message "Update onboarding documentation".
Push the current branch to origin with upstream tracking. Verify that the
remote branch points to the same commit as the local branch, and give me the
GitHub branch URL. Do not merge anything.
```

Codex should perform the equivalent of:

```bash
git add <intended-files>
git commit -m "Update onboarding documentation"
git push -u origin docs/update-onboarding
```

The instruction to commit only the task's files prevents unrelated local changes from being included accidentally.

### Step 7: Create a pull request

If the branch should be reviewed before merging, ask:

```text
Using the GitHub connection, create a pull request from
docs/update-onboarding into main. Summarize the documentation changes and
include the successful Jekyll build in the test section. Do not merge it.
```

Review the proposed title and description before Codex creates the pull request if you want tighter control.

### Step 8: Wait for CI and merge into `main`

The lab manual's CI workflow builds the Jekyll site for every pull request. Do not merge until that check succeeds. Ask Codex to confirm that the pull request is mergeable and still current with `main`, then merge it using a method permitted by the repository.

Example prompt:

```text
Check the pull request for docs/update-onboarding. Wait for all required CI
checks, including the Jekyll build, to finish. If every required check passes
and the branch is mergeable, merge the pull request into main using a merge
method allowed by the repository. Do not force-push or bypass protections.
Give me the pull-request URL and the resulting main commit SHA.
```

If a check fails, have Codex inspect the relevant Actions log, explain the failure, and fix only problems caused by the branch. Push the fix to the same branch and wait for CI again before merging.

### Step 9: Publish and verify the lab manual

No separate release command is normally needed for this repository. Merging into `main` triggers `.github/workflows/pages.yml`, which builds the Jekyll site and deploys it with GitHub Pages.

Ask Codex to monitor both the main-branch CI run and the Pages deployment:

```text
After the pull request is merged, monitor the GitHub Actions runs triggered by
the new main commit. Wait for both CI and "Deploy Jekyll site to Pages" to
finish. If they succeed, open https://yuyanchenglab.github.io/lab-manual/ and
verify that the expected documentation and navigation are live. Give me the
main commit SHA, Actions run URLs, and live-site URL. If a run fails, report
the relevant error and do not make unrelated changes.
```

Useful pages:

- [Lab manual Actions](https://github.com/yuyanchenglab/lab-manual/actions)
- [Published lab manual](https://yuyanchenglab.github.io/lab-manual/)

A successful merge and a successful Pages workflow are separate milestones. Do not call the change published until the Pages deployment succeeds and the live site shows the expected result.

## A reusable prompt for the whole workflow

Use this when the requested change is already clear:

```text
Work in the yuyanchenglab/lab-manual repository.

1. Inspect Git status, branch, and remotes; preserve unrelated user changes.
2. Fetch origin and create branch docs/SHORT-DESCRIPTION from origin/main.
3. Review the relevant documentation and explain the proposed scope.
4. Make the requested edits while preserving Just the Docs front matter,
   navigation, and unrelated content.
5. Run bundle exec jekyll build and fix only regressions caused by the edits.
6. Show me the final diff and stop for my approval before committing.

Do not commit, push, create a pull request, or merge until I explicitly approve.
```

After approving the diff, send:

```text
Commit only the approved changes with a clear commit message, push the current
branch to origin with upstream tracking, verify that local and remote commit
SHAs match, create a pull request into main, and give me the branch and
pull-request URLs. Stop before merging.
```

After reviewing the pull request and deciding to publish, send:

```text
Wait for every required pull-request check to pass. If the pull request is
mergeable, merge it into main without bypassing repository protections. Then
monitor the CI and "Deploy Jekyll site to Pages" workflows for the resulting
main commit. When both succeed, verify the expected change at
https://yuyanchenglab.github.io/lab-manual/ and give me the pull-request,
workflow-run, and live-site URLs.
```

## If pushing fails inside Codex

First ask Codex to verify both available authentication paths:

```text
Check whether the GitHub plugin can access yuyanchenglab/lab-manual with push
permission, and check local gh auth status. Do not expose any token values.
Use the connected GitHub plugin to publish the branch if the local Keychain
credential is unavailable, then verify the remote commit SHA.
```

Common causes include:

- the GitHub plugin was not granted access to `yuyanchenglab/lab-manual`;
- organization approval is pending;
- `gh auth status` is invalid in the Codex execution context;
- Terminal and Codex have different macOS Keychain access;
- the account lacks repository write permission; or
- branch protection or repository rules reject the update.

The plugin connection and local `gh` authentication are separate. One may work even when the other does not.

## Recommended safety habits

- Start each change on a dedicated branch.
- Ask for a read-only review before editing when the scope is uncertain.
- Tell Codex not to commit or push until you approve the diff.
- Run `/review` before committing.
- Validate the Jekyll build before pushing.
- Commit only files related to the task.
- Push a branch and use a pull request instead of updating `main` directly.
- Merge only after required pull-request checks pass.
- Confirm the Pages workflow succeeded and inspect the live site before calling the change published.
- Never paste GitHub credentials or tokens into a prompt.

## Official OpenAI documentation

- [Local environments and built-in Git tools](https://learn.chatgpt.com/docs/environments/local-environment)
- [Code review in Codex](https://learn.chatgpt.com/docs/code-review)
- [Plugins: installation, connections, and permissions](https://learn.chatgpt.com/docs/plugins)

Last reviewed: September 11, 2026.
