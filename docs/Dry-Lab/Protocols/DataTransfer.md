---
layout: default
title: Data Transfer
parent: Protocols
grand_parent: Dry Lab
nav_order: 10
---

<!-- Written Oct 2026. Checked on PMACS on 2026-10-08: rclone and lftp are installed on Mercury (rclone 1.55.1, lftp 4.4.8) and on rhel9 compute nodes (rclone 1.72.1, lftp 4.9.2); from both, Box (api.box.com:443, upload.box.com:443, ftp.box.com:990) and Betty (login.betty.parcc.upenn.edu:22) are reachable. Mercury has `screen` and `kinit` but not `tmux`. Nothing on the Betty side has been run by the lab yet; those steps follow PARCC's documentation. -->

# {{page.title}}

**Owner:** Rushil

How to move data between **Box**, the **PMACS** cluster and the **PARCC** cluster (Betty), in either direction. If you haven't set up your accounts yet, start with [Server Access](../ServerAccess).

## Which route to use

| From ↔ to | Run the transfer on | Tool | Section |
|---|---|---|---|
| Box ↔ PMACS | a PMACS compute node (or Mercury) | `rclone` (or `lftp`) | [2](#box-pmacs) |
| PMACS ↔ PARCC | Mercury, PMACS's file-transfer server | `rsync` over SSH | [3](#pmacs-parcc) |
| Box ↔ PARCC | via PMACS, or on Betty | `rclone` | [4](#box-parcc) |
| Your laptop ↔ a cluster | your laptop | `rsync` / `scp`, or Globus | [5](#laptop) |

Never run transfers on the head nodes (`consign` on PMACS, `login0x` on Betty) beyond small files. On PMACS, file transfers belong on Mercury (`mercury.pmacs.upenn.edu`); it has no `bsub`, so keep long transfers alive with `screen`.

## Before you move anything

{: .warning }
Check what the data is before it leaves the cluster. Patient-derived data lives in `/project/hipaa_ycheng11lab/` for a reason: ask Dr. Cheng before putting anything identifiable or HIPAA-covered on Box, and never make a Box shared link for it public. See Penn's [data risk classification](https://isc.upenn.edu/security/penn-data-risk-classification) and the [PennBox FAQ](https://isc.upenn.edu/resources/pennbox-faq).

* **Box has a per-file size limit** (15 GB, per the PMACS wiki). Split larger files first (`split -b 10G big.tar big.tar.part_`).
* **Many small files are slow** on Box (API rate limits) and burden PARCC's file systems. `tar` a directory into one file before you move it.
* **Use `copy`, not `sync`.** `rclone sync` and `rsync --delete` delete files at the destination that aren't in the source.
* **Verify after every large transfer.** Commands are given in each section.

## 1. One-time setup: connect `rclone` to your Box {#setup-rclone}

You do this once on PMACS. Your home directory is shared by Mercury and the compute nodes, so the connection works on both.

**a. On your laptop**, install rclone (Mac: `brew install rclone`; Windows: download from [rclone.org](https://rclone.org/downloads/)). Your laptop is only needed for one login step, because the cluster has no web browser.

**b. On PMACS**, start an interactive job and run the setup:

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

**c. On your laptop**, run that command exactly as printed:

```bash
rclone authorize "box"
```

A browser opens. Sign in to Box with your Penn account (choose single sign-on and use `<pennkey>@upenn.edu`). The laptop terminal then prints a token block.

**d. Back on PMACS**, paste the token at the `config_token>` prompt. Answer `y` to keep the remote, then `q` to quit.

**e. Test it:**

```bash
rclone lsd box:                 # your top-level Box folders
rclone ls "box:<folder>" | head
```

{: .important }
`~/.config/rclone/rclone.conf` now holds a token that opens **your whole Box account**. Keep it private (`chmod 600 ~/.config/rclone/rclone.conf`). Never copy it into a project folder or a git repo, and never paste it into a chat or a coding agent.

The token lapses if you don't use rclone for 60 days. It also breaks if the same config is used on two machines, because each refresh token works only once. If you see `Invalid refresh token`, run `rclone config reconnect box:` and repeat step c.

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

Run this on **Mercury**. It is PMACS's transfer server, and it can reach Betty. Betty asks for two of three factors: a Kerberos ticket, an SSH key, or Duo. Here you use a Kerberos ticket plus Duo.

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

**Through PMACS (tested pieces).** Box → PMACS with [section 2](#box-pmacs), then PMACS → PARCC with [section 3](#pmacs-parcc). This is the simplest route when the data belongs on PMACS anyway.

**Directly on Betty (not yet tested by the lab).**

1. Check for rclone on a Betty login node: `command -v rclone`. If it's missing, put the [single rclone binary](https://rclone.org/downloads/) in `~/bin`; no administrator is needed.
2. Run [section 1](#setup-rclone) again on Betty to make a **separate** Box remote. Don't copy your PMACS `rclone.conf`: each Box refresh token works only once, so two machines sharing one config break each other.
3. Copy small amounts on the login node, for example `rclone copy "box:<box/folder>" /ceph/projects/ycheng11/ycheng11lab-hippa/<project-id>/data -P`. For anything large, follow PARCC's advice to use Globus or a batch job.

<!-- TODO (Ronnie?): run section 4 on Betty once and replace "not yet tested" with what happened. Also check whether Penn's Globus subscription includes a Box connector; if so, Globus can move Box <-> "ceph parcc" directly. -->

## 5. Your laptop ↔ a cluster {#laptop}

* **PMACS**, through Mercury (on the PMACS VPN if you're off campus):

  ```bash
  rsync -av <local_path> <pennkey>@mercury.pmacs.upenn.edu:/project/hipaa_ycheng11lab/<project-id>/
  ```

* **PARCC**: `scp <local_file> <pennkey>@login.betty.parcc.upenn.edu:/ceph/projects/ycheng11/ycheng11lab-hippa/<project-id>/` for small files. Use [Globus](https://parcc.upenn.edu/training/storage/globus-data-transfer/) (collections "vast parcc" and "ceph parcc") for anything large.
* **Box**: the web interface is fine for a few small files.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Invalid refresh token` from rclone | `rclone config reconnect box:`, then repeat step 1c on your laptop |
| A Box upload fails on one big file | It's over Box's per-file limit: `split` or `tar` it into smaller pieces |
| A transfer stopped when your laptop slept | Use `screen` on Mercury, or a `bsub` batch job (section 2) |
| Box transfer of many small files crawls | `tar` the directory first; Box rate-limits API calls |
| `command not found: bsub` | You're on Mercury, which has no scheduler. Use `screen`, or run from `consign` with `bsub` |

## Sources

* PMACS HPC wiki: [Rclone](https://hpcwiki.pmacs.upenn.edu/wiki/index.php/HPC:Rclone), [lftp](https://hpcwiki.pmacs.upenn.edu/wiki/index.php/HPC:lftp), [Login and file transfer](https://hpcwiki.pmacs.upenn.edu/wiki/index.php/HPC:Login)
* PARCC: [Logging in](https://parcc.upenn.edu/training/getting-started/logging-in/), [Looking around (scp)](https://parcc.upenn.edu/training/getting-started/looking-around/), [Globus data transfer](https://parcc.upenn.edu/training/storage/globus-data-transfer/)
* rclone: [Box backend](https://rclone.org/box/)
