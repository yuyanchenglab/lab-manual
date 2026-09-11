---
layout: default
title: PARCC Usage
parent: Access
nav_order: 10
---

<!-- MOVED from docs/Intro to Computation/parcc_guide.md, content unchanged -->

# {{page.title}}

**Owner:** Ronnie

<!-- TODO (Ronnie): per Yuyan, this page's content should move to a Google Drive doc — replace the content below with a link to it once that's set up. -->
A simple repeatable guide to log in to Betty (the PARCC cluster) and get oriented.

## Step 1 — Get a Kerberos Ticket

```
kinit <pennkey>@UPENN.EDU
```

Complete Duo if prompted. Check anytime with `klist`; renew with `kinit -R` or just re-run `kinit`.

## Step 2 — SSH In

```
ssh <pennkey>@login.betty.parcc.upenn.edu
```

You're in when you see the Betty banner and a `<pennkey>@login0x:~$` prompt.

Two login hostnames: `login.betty.parcc.upenn.edu` (general) and `slurm_login.parcc.upenn.edu` (used in job-submission tutorials) — either works.

## Optional — SSH Key Setup (skip repeated auth)

```
ssh-keygen -t ed25519
kinit <pennkey>@UPENN.EDU
ssh-copy-id <pennkey>@login.betty.parcc.upenn.edu
```

Add multiplexing to `~/.ssh/config`:

```
Host *.parcc.upenn.edu
  VerifyHostKeyDNS yes
  GSSAPIAuthentication yes
  ControlMaster auto
  ControlPath ~/.ssh/control:%h:%p:%r
```

## You're on a Login Node — No Heavy Work Here

`login0x` is shared, like PMACS's `hpclogin1`. Light commands only (`ls`, `cd`, editing, status checks, submitting jobs). Real compute goes through a requested node (Step 7) or a batch job (Step 8).

## First Orientation Commands

```
parcc_quota.py     # your storage: home (small) vs project (big)
parcc_sfree.py     # free nodes/partitions/GPU availability
parcc_sqos.py      # which QOS you're allowed to request
```

(Make sure `/vast/parcc/sw/bin` is on your `PATH` if these say "command not found.")

## Storage

| Pool | Path | Size | Use for |
|---|---|---|---|
| home | `/vast/home/<first-letter>/<pennkey>` | 50 GB | scripts, configs, small files |
| project | `/ceph/projects/ycheng11/ycheng11lab-hippa` | 536 GB | data, models, scGPT work |

Do heavy work in the ceph project space, not home.

## Step 7 — Get a Compute Node (Interactive)

Real partitions: `dgx-b200` (GPU, NVIDIA B200), `genoa-std-mem` (CPU, AMD Genoa). Check availability with `parcc_sfree.py` or `sinfo`.

```
salloc -p genoa-std-mem --cpus-per-task=4 --mem=16G --time=02:00:00
srun -p dgx-b200 --gpus=1 -t 00:01:00 nvidia-smi              # quick GPU test
srun --pty -p dgx-b200 --gpus=1 --cpus-per-task=8 --mem=64G --time=02:00:00 bash  # interactive GPU shell
```

On the node:

```
module load anaconda3
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate <your-env-path>
```

`exit` to release the node when done.

## Step 8 — Submit a Batch Job

For training/long runs, don't use interactive — write a script and `sbatch` it:

```bash
#!/bin/bash
#SBATCH --job-name=scgpt
#SBATCH --output=slurm-%j.out
#SBATCH --time=04:00:00
#SBATCH --partition=dgx-b200
#SBATCH --gpus=1
#SBATCH --cpus-per-task=14
#SBATCH --mem=256G

module load anaconda3
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate <your-env-path>

hostname
nvidia-smi || true
python your_script.py
```

```
sbatch job.sbatch          # submit
squeue -u $USER            # check status
tail -f slurm-<JOBID>.out  # watch output live
scancel <JOBID>            # cancel if needed
```

Batch jobs survive disconnection.

**Important:** you must be on your PI's ColdFront project allocation to submit SLURM jobs at all.
