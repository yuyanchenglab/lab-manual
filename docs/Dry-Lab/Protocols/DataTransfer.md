---
layout: default
title: Data Transfer
parent: Protocols
grand_parent: Dry Lab
nav_order: 10
---

<!-- Written Oct 2026. Checked on PMACS on 2026-10-08: rclone and lftp are installed on Mercury (rclone 1.55.1, lftp 4.4.8) and on rhel9 compute nodes (rclone 1.72.1, lftp 4.9.2); from both, Box (api.box.com:443, upload.box.com:443, ftp.box.com:990) and Betty (login.betty.parcc.upenn.edu:22) are reachable. Mercury has `screen` and `kinit` but not `tmux`.
Betty side, from prj2401: Box -> Betty (rclone 1.75 in ~/bin, login through an SSH port forward) set up 2026-09-23; shared-link downloads with box_pull.py (then scripts/00_box_pull.py in prj2401) 2026-09-24 and 09-30, SHA-1 verified; box_pull.py --list rerun 2026-10-09. PMACS -> Betty streamed through the laptop, md5 on both ends, Sept 2026, from the `pmacs` alias (Mercury not yet used this way). Laptop -> Betty code with rsync used daily.
Checked from a Betty login node on 2026-10-09: github.com (22, 443), ssh.github.com (443), mercury.pmacs.upenn.edu (22), api.box.com and upload.box.com (443) reachable; git 2.43, tmux 3.4 and screen installed; no system rclone, no gh, no Globus CLI; ~/bin is on PATH only in login shells. The public lab-manual repo clones with no login; a private repo asks for credentials.
NOT yet run by the lab: the direct Mercury <-> Betty rsync (section 3) and the GitHub SSH key on Betty (section 6, option B). Whoever does either first, update the notes there. -->

# {{page.title}}

**Owner:** Rushil

How to move data between **Box**, the **PMACS** cluster, the **PARCC** cluster (Betty) and **GitHub**, in either direction. If you haven't set up your accounts yet, start with [Server Access](../ServerAccess).

Steps marked **(you)** need your own login (Duo, a browser sign-in, your GitHub settings), so do them in your own terminal. A coding agent such as Claude Code can do everything else. [Section 7](#agent) has the guard rails and instructions to give it.

## Which route to use

| From ↔ to | Run the transfer on | Tool | Section |
|---|---|---|---|
| Box ↔ PMACS | a PMACS compute node (or Mercury) | `rclone` (or `lftp`) | [2](#box-pmacs) |
| PMACS ↔ PARCC | your laptop, streaming between its two SSH connections (tested); or Mercury, PMACS's file-transfer server | `ssh` piped into `ssh`, or `rsync` over SSH | [3](#pmacs-parcc) |
| Box ↔ PARCC | a Betty login node (tested), or via PMACS | `rclone`, and `box_pull.py` for shared links | [4](#box-parcc) |
| Your laptop ↔ a cluster | your laptop | `rsync` / `scp`, or Globus | [5](#laptop) |
| GitHub ↔ a cluster | your laptop (`rsync` of code), or the cluster's own clone | `rsync`, `git` | [6](#github) |

Keep transfers on the head nodes (`consign` on PMACS, `login0x` on Betty) to a few GB at most. On PMACS, file transfers belong on Mercury (`mercury.pmacs.upenn.edu`); it has no `bsub`, so keep long transfers alive with `screen`. On Betty, use `tmux` or `screen`.

## Before you move anything

{: .warning }
Check what the data is before it leaves the cluster. Patient-derived data lives in `/project/hipaa_ycheng11lab/` for a reason: ask Dr. Cheng before putting anything identifiable or HIPAA-covered on Box, and never make a Box shared link for it public. Patient-derived data never goes onto a laptop either. See Penn's [data risk classification](https://isc.upenn.edu/security/penn-data-risk-classification) and the [PennBox FAQ](https://isc.upenn.edu/resources/pennbox-faq).

* **Box has a per-file size limit** (15 GB, per the PMACS wiki). Split larger files first (`split -b 10G big.tar big.tar.part_`).
* **Many small files are slow** on Box (API rate limits) and burden PARCC's file systems. `tar` a directory into one file before you move it.
* **Use `copy`, not `sync`.** `rclone sync` and `rsync --delete` delete files at the destination that aren't in the source.
* **Verify after every large transfer.** Commands are given in each section.
* **Where data goes on Betty.** The lab has two project areas there. Ask Dr. Cheng which one your data belongs in, and to be added to its group:

  | Area | Path | Group | Notes |
  |---|---|---|---|
  | Ceph (HIPAA) | `/ceph/projects/ycheng11/ycheng11lab-hippa/` | `ycheng11Ycheng11LabHippaCeph` | The lab's HIPAA allocation. Ceph was unreadable for six days in Sept 2026. |
  | VAST | `/vast/projects/ycheng11/ycheng11lab/` | `ycheng11Ycheng11LabVast` | Faster, disaster-recovery backed; prj2401 works here with de-identified data. **About 86% used on 2026-10-09 (267 GB free).** |

## 1. One-time setup: connect `rclone` to your Box {#setup-rclone}

Do this once on each cluster you'll use. Make a separate Box login on each, and never copy `rclone.conf` from one to the other: each Box refresh token works only once, so two copies break each other.

### On PMACS

Your home directory is shared by Mercury and the compute nodes, so the connection works on both.

**a. On your laptop**, install rclone (Mac: `brew install rclone`; Windows: download from [rclone.org](https://rclone.org/downloads/)). Your laptop is only needed for one login step, because the cluster has no web browser.

**b. On PMACS (you)**, start an interactive job and run the setup:

```bash
ssh <pennkey>@consign.pmacs.upenn.edu
bsub -Is bash
rclone config
```

Answer the prompts:

* `n` for a new remote, and name it `box`
* Storage type: `box`
* Client id, client secret, config file and access token: press **Enter** to leave each blank
* Account type (`box_sub_type`): `user`
* Edit advanced config: `n`
* Use a web browser to authenticate automatically: **`n`**. rclone then prints a command beginning `rclone authorize "box"`.

**c. On your laptop (you)**, run that command exactly as printed:

```bash
rclone authorize "box"
```

A browser opens. Sign in to Box with your Penn account (choose single sign-on and use `<pennkey>@upenn.edu`). The laptop terminal then prints a token block.

**d. Back on PMACS (you)**, paste the token at the `config_token>` prompt. Answer `y` to keep the remote, then `q` to quit.

**e. Test it:**

```bash
rclone lsd box:                 # your top-level Box folders
rclone ls "box:<folder>" | head
```

### On Betty {#setup-rclone-betty}

Betty commands are written as `ssh betty '…'`. The `betty` alias and its shared connection come from [Claude to PARCC](../Tutorials/CodingAgents/ClaudeToPARCC), steps 1–4.

**a. Install rclone in your home directory.** Betty has no system-wide rclone, and no administrator is needed:

```bash
ssh betty 'mkdir -p ~/bin && d=$(mktemp -d) && cd "$d" \
  && curl -fsSL -o rclone.zip https://downloads.rclone.org/rclone-current-linux-amd64.zip \
  && unzip -qo rclone.zip && cp rclone-*-linux-amd64/rclone ~/bin/ && chmod 755 ~/bin/rclone \
  && cd ~ && rm -rf "$d" && ~/bin/rclone version | head -1'
```

Always call it as `~/bin/rclone`: `~/bin` is on your PATH only in a login shell, so a plain `ssh betty 'rclone …'` won't find it.

**b. Log in to Box (you)**, in your own terminal, about two minutes:

1. On your laptop, open a **separate** SSH connection with a port forward. The port forward carries Box's login page back to rclone on Betty. The two `-o` options keep it off your shared connection, so a stale shared connection can't block the forward.

   ```bash
   ssh -o ControlMaster=no -o ControlPath=none -L 53682:127.0.0.1:53682 <pennkey>@login.betty.parcc.upenn.edu
   ```

2. In that Betty session:

   ```bash
   ~/bin/rclone config create box box
   ```

   It prints `Failed to open browser automatically … please go to the following link: http://127.0.0.1:53682/auth?state=…`. That is expected on a server.
3. Open that link in your **laptop's** browser, sign in with PennKey (single sign-on), and click **Grant access to Box**. The terminal finishes. If it then prints the new configuration, that text includes your token: don't copy it anywhere.
4. Still on Betty:

   ```bash
   chmod 600 ~/.config/rclone/rclone.conf
   exit
   ```

**c. Test it:**

```bash
ssh betty '~/bin/rclone lsd box: --max-depth 1 | head'
```

**d. Install `box_pull.py`**, for Box shared links ([section 4](#box-parcc)):

```bash
ssh betty 'curl -fsSL -o ~/bin/box_pull.py https://raw.githubusercontent.com/yuyanchenglab/lab-manual/main/docs/Dry-Lab/Protocols/box_pull.py && chmod 755 ~/bin/box_pull.py'
```

### On either cluster

{: .important }
`~/.config/rclone/rclone.conf` now holds a token that opens **your whole Box account**. Keep it private (`chmod 600 ~/.config/rclone/rclone.conf`). Never copy it into a project folder or a git repo, and never paste it into a chat or a coding agent.

The token lapses if you don't use rclone for 60 days. If you see `Invalid refresh token`, reconnect with `rclone config reconnect box:` (you). On PMACS, then repeat step c. On Betty, run it in the port-forwarded session from step b, in place of `config create`.

## 2. Box ↔ PMACS {#box-pmacs}

Folder names with spaces need quotes. `-P` shows progress.

**Small transfers**, in an interactive job (`bsub -Is bash`):

```bash
# Box -> PMACS
rclone copy "box:<box/folder>" /project/hipaa_ycheng11lab/<project-id>/data/raw -P

# PMACS -> Box
rclone copy /project/hipaa_ycheng11lab/<project-id>/results "box:<box/folder>/results" -P
```

**Large transfers** go in a batch job, which keeps running after you log out:

```bash
bsub -q rhel9 -n 2 -J box_pull -o box_pull.%J.out \
  rclone copy "box:<box/folder>" /project/hipaa_ycheng11lab/<project-id>/data/raw -v --transfers 4
```

**Verify.** This compares sizes and checksums and lists anything missing or different:

```bash
rclone check "box:<box/folder>" /project/hipaa_ycheng11lab/<project-id>/data/raw --one-way
```

**Alternative: `lftp` over FTPS.** This is the PMACS wiki's other route. It needs a separate Box password, not your PennKey password: set one in Box under Account Settings → Authentication.

```bash
# PMACS -> Box (mirror -R uploads)
lftp -p 990 -e "open <pennkey>@upenn.edu@ftp.box.com; mirror -R /project/hipaa_ycheng11lab/<project-id>/results <box_folder>; exit"

# Box -> PMACS
lftp -p 990 -e "open <pennkey>@upenn.edu@ftp.box.com; mirror <box_folder> /project/hipaa_ycheng11lab/<project-id>/data/raw; exit"
```

## 3. PMACS ↔ PARCC {#pmacs-parcc}

**Through your laptop (tested).** PMACS logins use a password, so a Betty job can't log in to PMACS by itself. Instead your laptop holds one SSH connection to each cluster and pipes the data from one to the other. It streams through the laptop's network connection and is **never written to its disk**. This is the route an agent can run unattended.

First **(you)** open both connections. For Betty, run `kinit` and approve Duo ([Claude to PARCC](../Tutorials/CodingAgents/ClaudeToPARCC), step 4). For Mercury, run `PMACS_HOST=mercury ~/bin/pmacs-connect` ([Claude to PMACS](../Tutorials/CodingAgents/ClaudeToPMACS)); it should print `GOT_IT` or `MASTER_OK`. Then:

```bash
# one file
ssh mercury "cat /project/hipaa_ycheng11lab/<project-id>/<path>/<file>" \
  | ssh betty "cat > <betty dir>/<file>"

# verify: the two checksums must match
ssh mercury "md5sum /project/hipaa_ycheng11lab/<project-id>/<path>/<file>"
ssh betty   "md5sum <betty dir>/<file>"
```

```bash
# a folder, as a tar stream unpacked on Betty as it arrives
ssh mercury "tar -C /project/hipaa_ycheng11lab/<project-id>/<dir> -cf - ." \
  | ssh betty "mkdir -p <betty dir> && tar -C <betty dir> -xf -"

# verify: prints "identical" or the files that differ; saves nothing on the laptop
diff <(ssh mercury "cd /project/hipaa_ycheng11lab/<project-id>/<dir> && find . -type f -exec md5sum {} + | sort -k2") \
     <(ssh betty   "cd <betty dir> && find . -type f -exec md5sum {} + | sort -k2") && echo identical
```

To go **PARCC → PMACS**, swap the two sides. prj2401 ran these through the `pmacs` alias (a PMACS login node). They are written here for Mercury because PMACS asks that transfers run there; nothing else changes. Speed is set by your laptop's connection, so this suits files and folders of a few GB. For anything larger, use the direct route below.

{: .warning }
Never redirect the stream into a file on your laptop (`> file`, `scp` down, `rsync` to a local path). Checksums, file names and sizes are fine; file contents are not.

**Direct: Mercury ↔ Betty.** Your laptop isn't involved, but you type the passwords yourself, so an agent can't run it unattended. Run this on **Mercury**: it is PMACS's transfer server, and it can reach Betty. Betty asks for two of three factors: a Kerberos ticket, an SSH key, or Duo. Here you use a Kerberos ticket plus Duo.

```bash
ssh <pennkey>@mercury.pmacs.upenn.edu
screen -S xfer                        # keeps the transfer alive if you disconnect
kinit <pennkey>@UPENN.EDU             # Kerberos ticket for Betty

# PMACS -> PARCC
rsync -av --partial -e "ssh -o GSSAPIAuthentication=yes" \
  /project/hipaa_ycheng11lab/<project-id>/data/ \
  <pennkey>@login.betty.parcc.upenn.edu:/ceph/projects/ycheng11/ycheng11lab-hippa/<project-id>/data/
```

Approve the Duo prompt. To go **PARCC → PMACS**, swap the two paths. Detach from `screen` with `Ctrl-a d`, and reattach later with `screen -r xfer`.

**Verify** by rerunning the same `rsync` with `--checksum --dry-run` added. If nothing is listed, the copy is complete.

{: .note }
The network path from Mercury to Betty is open, but the lab hasn't yet run this end to end. If `kinit` fails on Mercury, pull from the Betty side instead. On a Betty login node, run `rsync -av --partial <pennkey>@mercury.pmacs.upenn.edu:/project/hipaa_ycheng11lab/<project-id>/data/ /ceph/projects/ycheng11/ycheng11lab-hippa/<project-id>/data/` (Mercury asks for your PMACS password). Whoever runs either version first, please update this note.

<!-- TODO: PMACS has a `globus` LSF queue, but we found no documented PMACS Globus collection. If one exists, Globus is the better route for very large PMACS <-> PARCC transfers (PARCC's collections are "vast parcc" and "ceph parcc"). Ask PMACS (psom-pmacshpc@pennmedicine.upenn.edu). -->

## 4. Box ↔ PARCC {#box-parcc}

**Directly on Betty (tested).** This is the usual route when the data belongs on Betty. It needs the one-time setup in [section 1, On Betty](#setup-rclone-betty).

```bash
# your own Box folders
ssh betty '~/bin/rclone copy "box:<box/folder>" <betty project dir>/data -P'

# Betty -> Box, into your own Box tree (read "Before you move anything" first)
ssh betty '~/bin/rclone copy <betty path> "box:<box/folder>" -P'
```

**Box shared links** (`https://upenn.box.com/s/…`) are how data usually reaches the lab, and rclone can't open them: it only sees your own Box folders. [`box_pull.py`](box_pull.py) uses your rclone login to download a shared link's contents. It keeps the folder structure and checks every file against Box's SHA-1. It reads the token inside its own process and never prints it.

```bash
# list a link's contents first; downloads nothing
ssh betty '/usr/bin/python3 ~/bin/box_pull.py <betty project dir>/data <label>=<shared link> --list'

# download, in tmux so it keeps going if your laptop sleeps; then check the log
ssh betty 'tmux new -d -s boxpull "/usr/bin/python3 ~/bin/box_pull.py <betty project dir>/data <label>=<shared link> > ~/box_pull.log 2>&1"'
ssh betty 'tail -5 ~/box_pull.log'
```

Each file is reported as `OK … sha1 match` or `FAIL`. Rerunning skips files already complete. Use `--exclude .tif` or `--only <text>` to choose files. A `404` means the link is open only to named collaborators: ask its owner to set **People with the link** to **People in University of Pennsylvania**.

A few GB is fine on the login node (prj2401 pulled 4.5 GB files this way). For more than that, PARCC recommends Globus. Whether Betty's compute nodes can reach Box hasn't been checked, so a batch job may not work.

**Through PMACS (tested pieces).** Box → PMACS with [section 2](#box-pmacs), then PMACS → PARCC with [section 3](#pmacs-parcc). This is the simplest route when the data belongs on PMACS anyway.

<!-- TODO: check whether Penn's Globus subscription includes a Box connector; if so, Globus can move Box <-> "ceph parcc" / "vast parcc" directly. -->

## 5. Your laptop ↔ a cluster {#laptop}

* **PMACS**, through Mercury (on the PMACS VPN if you're off campus):

  ```bash
  rsync -av <local_path> <pennkey>@mercury.pmacs.upenn.edu:/project/hipaa_ycheng11lab/<project-id>/
  ```

* **PARCC**: `scp <local_file> <pennkey>@login.betty.parcc.upenn.edu:/ceph/projects/ycheng11/ycheng11lab-hippa/<project-id>/` for small files. Use [Globus](https://parcc.upenn.edu/training/storage/globus-data-transfer/) (collections "vast parcc" and "ceph parcc") for anything large.
* **Box**: the web interface is fine for a few small files.

Only code, figures and aggregate tables come back to the laptop, never patient-derived data.

## 6. GitHub ↔ a cluster {#github}

**Public repos** need nothing on either cluster: `git clone https://github.com/yuyanchenglab/<repo>.git`.

**Private repos** (most project repos) on **PMACS**: see [Claude to Git](../Tutorials/CodingAgents/ClaudeToGit). On **Betty**, choose one of these two options:

**Option A: no GitHub login on Betty.** This is what prj2401 does. The git checkout lives on your laptop: you commit and push from there, and copy the code to Betty before running it.

```bash
# from the repo root on your laptop
rsync -a --exclude __pycache__ scripts/ betty:<betty project dir>/scripts/
```

This is simple and leaves no GitHub credential on the cluster. The cost is that Betty's copy isn't a git checkout, so copy before every job submission. A job will otherwise run the old script.

**Option B: a GitHub SSH key on Betty.** Betty then has its own clone and can `git pull` (and push results, under the rules in [Claude to Git](../Tutorials/CodingAgents/ClaudeToGit)). Betty has `git` 2.43 but not the `gh` tool, so this uses SSH.

{: .note }
Betty reaches GitHub on ports 22 and 443 (checked 2026-10-09), but no one in the lab has run these steps yet. Whoever does it first, please fix anything that differs and delete this note.

1. **(you)** On Betty, make a key used only for GitHub:

   ```bash
   ssh-keygen -t ed25519 -C "<pennkey>@betty" -f ~/.ssh/id_ed25519_github
   ```

   An empty passphrase lets jobs and agents use the key without a prompt. The key is limited to Betty, and you can revoke it on its own.
2. **(you)** Run `cat ~/.ssh/id_ed25519_github.pub` and add that **public** key on GitHub under **Settings → SSH and GPG keys → New SSH key**, titled `Betty (PARCC)`. Never copy the file without `.pub`.
3. **(you)** On Betty, point git at the key:

   ```bash
   cat >> ~/.ssh/config <<'EOF'

   Host github.com
       User git
       IdentityFile ~/.ssh/id_ed25519_github
       IdentitiesOnly yes
   EOF
   chmod 600 ~/.ssh/config
   ```

4. **(you)** Run `ssh -T git@github.com`. The first time, it asks you to confirm GitHub's host key: compare the fingerprint with [GitHub's published fingerprints](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints) before typing `yes`. Success looks like `Hi <username>! You've successfully authenticated…`.
5. **(you)** Set your identity on Betty: `git config --global user.name "<Your Name>"` and `git config --global user.email "<your email>"`.
6. Clone with the SSH address, not the `https://` one:

   ```bash
   ssh betty 'git clone git@github.com:yuyanchenglab/<repo>.git <betty project dir>/<repo>'
   ```

Data, anything HIPAA-tagged, and anything over a few MB stay out of git, on every machine.

## 7. Handing transfers to a coding agent {#agent}

Once you've done the **(you)** steps, an agent can run every transfer on this page except the direct Mercury ↔ Betty `rsync`. It reuses your open SSH connections and never logs in itself. Set it up in two parts.

**a. Guard rails.** Add these to `~/.claude/settings.json` on the machine where Claude Code runs, merged with the blocks from [Claude to PARCC](../Tutorials/CodingAgents/ClaudeToPARCC), [Claude to PMACS](../Tutorials/CodingAgents/ClaudeToPMACS) and [Claude to Git](../Tutorials/CodingAgents/ClaudeToGit). Deny means the agent cannot run the command; ask means you approve each one.

```json
{
  "permissions": {
    "deny": [
      "Bash(*rclone.conf*)",
      "Bash(*rclone config show*)",
      "Bash(*rclone config dump*)",
      "Bash(*rclone config create*)",
      "Bash(*rclone config reconnect*)",
      "Bash(*rclone sync*)",
      "Bash(*id_ed25519*)",
      "Bash(*rsync*--delete*)"
    ],
    "ask": [
      "Bash(*rclone copy*box:*)",
      "Bash(*rclone delete*)",
      "Bash(*rclone purge*)"
    ]
  }
}
```

**b. Instructions.** Paste this into your project's `CLAUDE.md`, or as your first message, and replace the `<…>` placeholders.

````markdown
# Data transfers: Box, PMACS, Betty, GitHub

## Hosts (set up by me; reuse the open connections, never log in yourself)
- Betty:   `ssh -o BatchMode=yes -o ConnectTimeout=20 betty '<cmd>'`
           SLURM, module and ~/bin need a login shell: `ssh betty 'bash -lc "<cmd>"'`
- PMACS:   `ssh mercury '<cmd>'` for transfers, `ssh pmacs '<cmd>'` for jobs.
           If a PMACS command fails to connect, run `PMACS_HOST=mercury ~/bin/pmacs-connect`
           (or plain `~/bin/pmacs-connect` for pmacs) and act on the ONE word it prints:
           MASTER_OK/GOT_IT -> continue; VPN_DOWN/TIMED_OUT -> stop, ask me about the VPN;
           AUTH_FAILED or anything else -> stop and tell me. Never retry a failed login.
- If Betty refuses (gssapi / "Permission denied"): my Kerberos ticket expired. Stop and ask
  me to run `kinit` and `ssh -fNM betty`. Never try to fix authentication yourself.

## Where data goes
- My project dir on Betty: <betty project dir>
- PMACS project dir: /project/hipaa_ycheng11lab/<project-id>/

## Box
- On Betty rclone is ~/bin/rclone, remote `box:`. Shared links: ~/bin/box_pull.py
  (`/usr/bin/python3 ~/bin/box_pull.py <dest> <label>=<link> [--list] [--only X] [--exclude X]`).
  Always --list first and show me the list before downloading anything over 1 GB.
  Long downloads run in tmux (`tmux new -d -s <name> "... > ~/<name>.log 2>&1"`); report OK/FAIL counts.
- Uploading to Box: ask me first, every time.

## PMACS <-> Betty
- Stream through this laptop, never via a file on it:
  `ssh mercury "cat SRC" | ssh betty "cat > DEST"` (folders: tar -cf - | tar -xf -).
- Verify every transfer with md5sum on both ends and report the result.

## GitHub on Betty
- <Option A: no git on Betty. Copy code with
   `rsync -a --exclude __pycache__ scripts/ betty:<betty project dir>/scripts/`
   before every sbatch, and say that you did.>
  <Option B: Betty has its own clone at <betty project dir>/<repo> (SSH key set up by me).
   `git pull --rebase` before running or pushing; push only when I say "push".>

## Never
- Read, print, copy or `cat` any credential: ~/.config/rclone/rclone.conf, anything in ~/.ssh,
  tokens, .env files, keychain output.
- Run `rclone config` subcommands, `rclone sync`, or `rsync --delete`. Use copy, never sync.
- Write patient-derived data to this laptop, or paste data rows into the chat.
  Checksums, file names, sizes and aggregate tables are fine.
- Run compute on a login node (Betty login0x, PMACS consign/hpclogin): use sbatch / bsub.
- Overwrite or delete anything at a destination without asking me.
````

{: .important }
> Three things in [PARCC Usage](../Tutorials/Access/PARCC) are out of date (checked Sept–Oct 2026), and agents trip on each:
>
> 1. `slurm_login.parcc.upenn.edu` doesn't resolve, on or off campus. Use `login.betty.parcc.upenn.edu` for everything, job submission included.
> 2. `sbatch`, `squeue` and `module` are only on the PATH in a login shell. Over SSH, wrap them: `ssh betty 'bash -lc "squeue -u $USER"'`. The same applies to `~/bin`.
> 3. Betty's job filter rejects `--mem` unless it exactly matches the partition's memory per CPU, and every `--mem` in that page's examples is refused. Leave it out and ask for CPUs only; memory follows. On `dgx-b200`, each GPU comes with 28 CPUs and 224 GB of memory.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Invalid refresh token` from rclone | `rclone config reconnect box:` (you); see [section 1](#setup-rclone), "On either cluster" |
| A Box upload fails on one big file | It's over Box's per-file limit: `split` or `tar` it into smaller pieces |
| A transfer stopped when your laptop slept | Use `screen` on Mercury, `tmux` on Betty, or a `bsub` batch job (section 2) |
| Box transfer of many small files crawls | `tar` the directory first; Box rate-limits API calls |
| `command not found: bsub` | You're on Mercury, which has no scheduler. Use `screen`, or run from `consign` with `bsub` |
| `rclone: command not found` on Betty | It's in `~/bin`, which is on the PATH only in a login shell. Use `~/bin/rclone`. |
| Browser can't connect to `127.0.0.1:53682` | The port forward isn't active. Run `rclone config create` in the session you opened with `-L 53682:…`, and leave it open until it finishes. |
| `box_pull.py` exits with a 404 | The shared link is limited to named collaborators. Ask its owner to open it to "People in University of Pennsylvania". |
| `could not read Username for 'https://github.com'` | The repo is private and you used its `https://` address. Use [section 6](#github), option A, or option B with the `git@github.com:` address. |
| `Permission denied (publickey)` from GitHub | The key isn't on your GitHub account, or the `Host github.com` block is missing. Debug with `ssh -vT git@github.com`. |
| SSH to both Betty and PMACS times out on port 22 | You're off campus without the VPN. |
| `Permission denied (gssapi-with-mic,keyboard-interactive)` from Betty | Your Kerberos ticket expired: `kinit`, then `ssh -fNM betty`. |
| `Permission denied` writing to a lab project area on Betty | You're not in that area's group (see "Before you move anything"). Ask Dr. Cheng. |

## Sources

* PMACS HPC wiki: [Rclone](https://hpcwiki.pmacs.upenn.edu/wiki/index.php/HPC:Rclone), [lftp](https://hpcwiki.pmacs.upenn.edu/wiki/index.php/HPC:lftp), [Login and file transfer](https://hpcwiki.pmacs.upenn.edu/wiki/index.php/HPC:Login)
* PARCC: [Logging in](https://parcc.upenn.edu/training/getting-started/logging-in/), [Looking around (scp)](https://parcc.upenn.edu/training/getting-started/looking-around/), [Globus data transfer](https://parcc.upenn.edu/training/storage/globus-data-transfer/)
* rclone: [Box backend](https://rclone.org/box/), [remote setup](https://rclone.org/remote_setup/), [downloads](https://rclone.org/downloads/)
* Box API: [shared items](https://developer.box.com/reference/get-shared-items/) (the `BoxApi: shared_link=` header)
* GitHub: [adding an SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account), [SSH key fingerprints](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints)
