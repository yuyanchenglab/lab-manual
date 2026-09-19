---
layout: default
title: Claude to Git
parent: Coding Agents
nav_order: 45
---

<!-- Written Sep 2026 from the working setup used on prj2601 (X-SPEAR). Sister page to Claude to PMACS: that page is about reaching the cluster, this one is about how the agent's edits get into the lab's GitHub without leaking credentials or clobbering anyone's work. -->

# {{page.title}}

**Owner:** Rushil

## What is happening, in one minute

Claude Code runs on your laptop inside a checkout of a lab repo. It edits files there, and — when you tell it to — commits and pushes them using **your** git identity and **your** GitHub login. Two things make this safe:

1. **Claude never holds a GitHub credential.** `gh auth login` stores your token in the macOS Keychain (Windows Credential Manager on WSL) and installs a git *credential helper*, so `git push` fetches the token itself at the moment of the push. Claude runs `git push`; it never sees, reads, or types the token. That is enforced by a deny-list (Section 3), the same way the cluster password is on the [Claude to PMACS](ClaudeToPMACS) page.
2. **Claude works on a branch and stops before the irreversible steps.** Committing is cheap to undo; pushing to `main`, force-pushing, and deleting branches are not, so those ask you first.

**Where things live** — the same picture as the PMACS page:

| Where | What | Who commits from here |
|---|---|---|
| Laptop checkout `~/Desktop/<project-id>/` | code, configs, notes, small result tables, figures | you + Claude |
| Cluster clone `/project/hipaa_ycheng11lab/<project-id>/<pennkey>/<repo>/` | the same repo, plus data and job outputs | Claude, via `ssh pmacs`, **results only** |
| GitHub `yuyanchenglab/<repo>` | the shared history; `main` is what the lab sees | — |

Code goes laptop → GitHub → cluster (`git pull`). Result files can go cluster → GitHub → laptop. Because both ends commit, `git pull --rebase` before every push is a rule, not a suggestion: the one time this project skipped it, a push was rejected, the cluster's `git pull` said "already up to date", and five 12-hour jobs ran against a script that did not have the flag they were given.

Data, anything HIPAA-tagged, and anything over a few MB stay out of git. `.gitignore` covers it, and Claude is told to check before `git add`.

## 1. One-time setup (you, ~5 minutes)

**a. GitHub access** — send your GitHub username to Jeff for the repo(s) you need ([GitHub Usage](../Access/GitHubUsage)).

**b. `gh` and the credential helper** — this stores the token in the OS credential store and teaches git to use it; you authorize once in the browser:

macOS:

```bash
brew install gh
gh auth login -h github.com --web --git-protocol https
gh auth setup-git
gh auth status          # → Logged in to github.com account <you> (keyring)
```

Windows (inside the WSL2 Ubuntu terminal from the PMACS page):

```bash
sudo apt-get install -y gh
gh auth login -h github.com --web --git-protocol https
gh auth setup-git
gh auth status
```

Never paste a token into a Claude prompt, a `.env`, or a `CLAUDE.md`. If you ever see one in a transcript, revoke it at github.com → Settings → Developer settings.

**c. Identity** — what your commits are signed as:

```bash
git config --global user.name  "<Your Name>"
git config --global user.email "<your@pennmedicine.upenn.edu>"
```

**d. Clone** (or `cd` into an existing checkout):

```bash
gh repo clone yuyanchenglab/<repo> ~/Desktop/<project-id>
cd ~/Desktop/<project-id> && git remote -v      # https://github.com/yuyanchenglab/<repo>.git
```

On the cluster, `git pull` needs no credentials for a public repo; for a private one, run `gh auth login` there **once, interactively, in your own terminal** — not through Claude.

## 2. Guard rails for Claude Code (do this)

Add to `~/.claude/settings.json` (merge with the PMACS block if you have it):

```json
{
  "permissions": {
    "deny": [
      "Bash(gh auth token*)",
      "Bash(gh auth login*)",
      "Bash(gh auth refresh*)",
      "Bash(git credential*)",
      "Bash(security find-internet-password*)",
      "Bash(git push --force*)",
      "Bash(git push -f*)",
      "Bash(git push * --force*)",
      "Read(~/.config/gh/**)",
      "Read(~/.git-credentials)"
    ],
    "ask": [
      "Bash(git push*)",
      "Bash(git reset --hard*)",
      "Bash(git checkout -- *)",
      "Bash(git clean*)",
      "Bash(git branch -D*)",
      "Bash(git push * --delete*)",
      "Bash(gh pr merge*)",
      "Bash(gh repo delete*)"
    ]
  }
}
```

Deny = Claude physically cannot run it. Ask = you get a prompt each time. `git push` is in *ask* rather than deny because pushing is the whole point — you just want to see it happen.

## 3. The prompt to paste into Claude Code

Save as `CLAUDE.md` in the repo root (commit it — everyone on the project gets the same rules), or paste it as the first message. Replace the `<...>` placeholders.

````markdown
# Git and GitHub — how changes from this checkout reach the lab

## Where this repo lives
- GitHub:   https://github.com/yuyanchenglab/<repo>   (org: yuyanchenglab; main is protected)
- Laptop:   ./  (this directory) — edit and commit CODE here
- Cluster:  /project/hipaa_ycheng11lab/<project-id>/<pennkey>/<repo>/ — `git pull` here,
            commit RESULT FILES here only when I ask

## Identity and credentials
- Commits are signed as me: `git config user.name` / `user.email` are already set. Never
  change them, never add a Co-Authored-By or "Generated by" trailer unless I ask.
- Pushing uses a credential helper backed by the OS keychain. You do not need, will never
  be given, and must never look for a token: never run `gh auth token`, `gh auth login`,
  `git credential fill`, or read ~/.config/gh, ~/.git-credentials, or any .env.
- If a token, password, or key ever appears in command output, do not repeat it, do not
  save it, and tell me so I can revoke it.

## Branching
- Never commit directly to main. Before the first edit of a task, create or switch to a
  branch named <pennkey>/<short-task-name> from an up-to-date main:
      git fetch origin && git switch -c <pennkey>/<task> origin/main
- One task per branch. If I ask for something unrelated, ask whether it belongs on a
  new branch.

## Committing
- Before `git add`, run `git status` and read it. Stage files by name, never `git add -A`
  or `git add .`. Do not stage: data files, anything > 5 MB, logs, *.h5ad, *.zarr,
  *.parquet, *.rds, *.csv over a few hundred KB, .env, credentials, or anything under a
  path .gitignore already excludes. If in doubt, ask.
- Commit message: a short imperative first line (<= 70 chars) saying WHAT changed, then
  a blank line, then WHY if it is not obvious. No emoji, no "WIP".
- Commit when a coherent step is done — not after every edit, not once at the end.
- Never amend or rebase a commit that has already been pushed.

## Pushing and pulling — the rules that prevent lost work
- Before ANY push: `git pull --rebase origin <branch>` (and for main, `origin/main`).
  Both the laptop and the cluster commit to this repo; a push that is rejected as
  non-fast-forward means the other side is ahead. Rebase, then push. Never force-push.
- After `git pull` on the cluster, verify the file you changed actually has the change
  there (`grep` for the new flag or function) BEFORE submitting a job that depends on it.
  "Already up to date" after a rejected push means the cluster is running old code.
- Push the branch with `git push -u origin <branch>`; tell me the branch URL.
- Never push to main directly. Never delete a remote branch unless I ask.

## Pull requests
- Open PRs with `gh pr create --base main --head <branch>`; title = the commit's first
  line; body = what changed, why, and how it was checked (tests run, job IDs, figures).
- Do not merge a PR yourself unless I say "merge it". Then: wait for CI, `gh pr merge
  --squash` (or the repo's allowed method), and report the resulting main commit SHA.

## On the cluster (via `ssh pmacs`)
- `git pull --rebase origin main` is the deploy step; nothing to reinstall.
- Commit result files from the cluster only when I ask, as me:
      git -c user.name="<Your Name>" -c user.email="<your email>" commit -m "..."
  then `git pull --rebase origin main && git push origin main`, then pull on the laptop.
- Never `git add` a results directory wholesale; name the files and check their sizes.

## Stop and ask before
- git push to main, git reset --hard, git checkout -- <file>, git clean, deleting any
  branch, force-pushing (which you cannot do anyway), merging a PR, changing .gitignore
  in a way that would newly track data, or anything that rewrites shared history.
````

## 4. What a good session looks like

```
you:     Add a --dry-run flag to scripts/run_pipeline.py.
claude:  git status                       → clean, on main
         git fetch origin && git switch -c rpatel/dry-run-flag origin/main
         [edits scripts/run_pipeline.py, runs the test]
         git add scripts/run_pipeline.py tests/test_run_pipeline.py
         git commit -m "run_pipeline: add --dry-run (prints the plan, submits nothing)"
         git pull --rebase origin rpatel/dry-run-flag   (nothing to do)
         → asks: push rpatel/dry-run-flag to origin?        you: yes
         git push -u origin rpatel/dry-run-flag
         "Pushed: https://github.com/yuyanchenglab/<repo>/tree/rpatel/dry-run-flag
          Open a PR?"
```

Good recovery when the cluster has moved ahead:

```
claude:  git push origin main → ! [rejected] non-fast-forward
         git pull --rebase origin main   → Successfully rebased
         git push origin main            → ok
         ssh pmacs 'cd …/<repo> && git pull --rebase origin main && grep -c dry_run scripts/run_pipeline.py'
         → 3   "Cluster has the flag; submitting the job now."
```

If Claude instead runs `git add -A`, commits to `main`, tries `gh auth token`, or proposes `--force` — stop it and re-paste the block.

## 5. Two habits that matter more than any tool

* **Read the diff before you say "push".** `git diff --stat` and a skim of `git diff` take 30 seconds. Claude is good at making edits and bad at knowing which of its edits you did not want.
* **Results committed from the cluster are still your commits.** Keep them small (tables, not matrices), name what they are in the message, and pull them down to the laptop straight after so the two checkouts do not drift.

## Troubleshooting

* **`fatal: could not read Username` / `Authentication failed` on push:** the credential helper is not installed for this git. `gh auth setup-git`, then `gh auth status`. On WSL, make sure you ran both inside Ubuntu, not PowerShell.
* **`! [rejected] … non-fast-forward`:** someone (probably the cluster clone, or you last week) pushed first. `git pull --rebase origin <branch>` then push. Never `--force`.
* **Rebase stops with conflicts:** Claude can resolve them — ask it to show you each conflicted hunk and its choice before `git rebase --continue`. If it gets messy, `git rebase --abort` returns you to where you were.
* **Claude committed a data file:** if not pushed yet, `git reset --soft HEAD~1`, unstage the file, recommit. If pushed, tell Jeff before doing anything — rewriting shared history needs coordination.
* **A secret got committed:** revoke it *first* (GitHub token → Settings → Developer settings; PMACS password → change it), then worry about the history. A rotated secret in git history is an embarrassment; a live one is an incident.
* **`gh: command not found` inside Claude but works in your terminal:** PATH difference. Put the Homebrew line (`eval "$(/opt/homebrew/bin/brew shellenv)"`) in `~/.zprofile`, not only `~/.zshrc`.
* **Cluster `git pull` says "Already up to date" but the change is missing:** your local push was rejected and you did not notice. Check `git log origin/main -1` on the laptop against `git log -1` on the cluster.

See also: [GitHub Usage](../Access/GitHubUsage) (branch + PR conventions), [Claude to PMACS](ClaudeToPMACS), [Codex to Git](CodexToGit) (the same workflow in the Codex desktop app).
