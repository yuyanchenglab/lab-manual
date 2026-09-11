---
layout: default
title: Claude Code Usage
parent: Tutorials
grand_parent: Dry Lab
nav_order: 40
---

<!-- MOVED from docs/Intro to Computation/betty_claude.md, content unchanged (originally titled "Connecting the Betty (PARCC) Cluster to Claude"). Author appears to be someone going by "betty" or writing about the Betty cluster specifically — worth confirming attribution before publishing (see KeyContacts.md TODO). -->

# {{page.title}}

**Owner:** Ronnie

<!-- TODO (Ronnie): per Yuyan, this page's content should move to a Google Drive doc — replace the content below with a link to it once that's set up. -->
## What This Does

Connects Claude to the Betty HPC cluster over SSH, so the agent can read files, submit SLURM jobs, and pull results back. Covers both Claude Science (via the Compute panel) and Claude Code (the terminal agent, [Section 9](#sec-claude-code)). Nothing is installed on Betty — Claude reaches in through a connection you authenticate. Tested on Mac and Ubuntu, not WSL.

**Key idea:** Betty login needs two factors — an SSH key and a Kerberos ticket. An automated agent can't answer a Duo prompt, so you set up an SSH master connection you authenticate once by hand; Claude Science then rides that connection and never logs in itself.

## 1. Generate an SSH Key (if you don't have one)

```bash
ls ~/.ssh/id_ed25519.pub   # if it exists, skip to step 2
ssh-keygen -t ed25519      # otherwise, generate one
```

## 2. Install Your Key on Betty

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub <PennKey>@login.betty.parcc.upenn.edu
```

## 3. Edit Your SSH Config

Add to `~/.ssh/config`:

```
Host betty
    HostName login.betty.parcc.upenn.edu
    User <PennKey>
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
    GSSAPIAuthentication yes
    GSSAPIDelegateCredentials yes
    ControlMaster auto
    ControlPath ~/.ssh/control:%h:%p:%r
```

## 4. Get a Kerberos Ticket and Open the Master Connection

```bash
kinit <PennKey>@UPENN.EDU     # uppercase UPENN.EDU; complete Duo
klist                          # verify ticket
ssh -fNM betty                 # open persistent connection (returns silently on success)
ssh -O check betty             # should report "Master running"
```

macOS note: if you have stacked conda environments, `conda deactivate` until your prompt shows no `(env)` prefix — `kinit` may otherwise write the ticket to a cache SSH can't read.

## 5. Add Betty in the Claude Science Compute Panel

1. Open **Compute** in the Claude Science sidebar → **Add SSH host**.
2. Select `betty` if detected, or type the alias.
3. Paste the notes from Section 6 into "Anything Claude Science should know?"
4. Save — host should show **Connected**.

## 6. Cluster Notes to Paste In

```
Scheduler: SLURM. Submit jobs with sbatch/srun. Never run compute on a login node.
Account:   <your-account>          # e.g. from `sacctmgr show assoc user=$USER`
GPU:       partition <your-gpu-partition>, QOS <your-qos>, request --gres=gpu:1
CPU:       partition <your-cpu-partition>, QOS <your-qos>

GPU/CUDA WARNING: Betty's GPUs are NVIDIA B200 (compute capability sm_100). Any GPU
  framework must be built for CUDA 12.8+. A PyTorch cu121 (or earlier) wheel will NOT
  run on these GPUs -- it errors "sm_100 not compatible" and falls back to CPU. Build
  your env against a cu128 wheel, or use an NGC container with a recent CUDA.

Environment: module load miniconda3/<ver>, then
  source "$(conda info --base)/etc/profile.d/conda.sh", then conda activate <your env>.
Modules available: python/3.11.11, cuda/12.8.1, cuda/12.9.0 (check `module avail`).
Storage: keep data/checkpoints on your Ceph project dir; home (/vast/home) is only 50GB.
  Do not modify shared conda envs without asking.
```

## 7. Find Your Own Allocation

```bash
sacctmgr -n show assoc user=$USER format=Account,Partition,QOS
parcc_sqos.py
parcc_sfree.py
parcc_quota.py
```

## 8. Daily Use / Reconnecting

Kerberos tickets last **10 hours**; the master connection dies when closed or on a login-node reboot.

```bash
kinit <PennKey>@UPENN.EDU
```

If the master connection died:

```bash
kinit <PennKey>@UPENN.EDU
ssh -fNM betty
ssh -O check betty
```

## 9. Using Betty from Claude Code {#sec-claude-code}

Same idea — it rides the master connection from Step 4, never logs in itself.

**Run Claude Code on your laptop, reach into Betty:**

```bash
ssh betty 'sacct -X --format=JobID,State,Elapsed -S today'
ssh betty 'sbatch /ceph/projects/<you>/train.slurm'
```

Tell Claude Code (in its prompt or `CLAUDE.md`) that cluster commands must be prefixed `ssh betty '...'`, and real work goes through sbatch/srun, never the login node.

**Run Claude Code on Betty itself:**

```bash
curl -fsSL https://claude.ai/install.sh | bash -s stable
```

Then `cd` to your project on Ceph and run `claude`. VSCode Remote-SSH and plain `ssh` reuse your master connection, so login is instant, no Duo.

Two config files matter here, since Claude Code now sits on a login node where heavy compute is forbidden:

`~/.claude/settings.json` — blocks accidental training on the login node, pauses before submit/delete:

```json
{
  "permissions": {
    "deny": [
      "Bash(python train*)",
      "Bash(python *train*.py*)",
      "Bash(*--epochs*)"
    ],
    "ask": [
      "Bash(sbatch*)",
      "Bash(srun*)",
      "Bash(rm*)"
    ]
  }
}
```

`~/.claude/CLAUDE.md` — environment facts (adjust to your project; keep it short):

```markdown
# Betty (PARCC): environment notes for Claude Code

## Hard rules
- This is a LOGIN NODE. Never run training, data processing, or any heavy
  compute directly. All compute goes through SLURM (sbatch/srun).
- Confirm with me before submitting (sbatch) or cancelling (scancel) any job.

## SLURM
- Account: ycheng11-ycheng11lab-hippa
- GPU: partition b200-mig45 (45GB MIG slice), QOS mig, --gres=gpu:1
- Full GPU fallback: partition dgx-b200, QOS dgx
- CPU: partition genoa-std-mem / genoa-lrg-mem
- Check allocation: parcc_sqos.py, parcc_sfree.py, parcc_quota.py

## GPU / CUDA
- GPUs are NVIDIA B200 (sm_100) -> require CUDA 12.8+ builds.
- A torch cu121 wheel will NOT run on these GPUs (falls back to CPU).
  Use a cu128 build or an NGC container.

## Environments
- module load miniconda3/25.5.1
- source "$(conda info --base)/etc/profile.d/conda.sh"
- conda activate <env path>
- Do NOT modify shared conda envs.

## Storage
- Home /vast/home is only 50GB, code/config only.
- Data & checkpoints go on Ceph: /ceph/projects/ycheng11/ycheng11lab-hippa.
```

## Troubleshooting

* **"Permission denied (gssapi-with-mic,keyboard-interactive)":** key not accepted — check it's in `~/.ssh/authorized_keys` on Betty and that `~/.ssh` isn't group-writable (`chmod 700 ~/.ssh`).
* **"partial success":** key worked, second factor missing — run `kinit`, confirm with `klist`.
* **`kinit` seems to do nothing (macOS):** `conda deactivate` first, then `export KRB5CCNAME="API:"` (Sonoma 14+), retry.
* **Probe hangs / no output:** a master connection may already be open — check `ssh -O check betty`; close a stale one with `ssh -O exit betty` and reopen.
* **Interactive login works but the agent probe fails:** the agent needs the master connection (Step 4) — plain interactive login isn't enough since the agent can't answer Duo. Confirm the ticket hasn't expired (`klist`).

**Important:** you must be on campus or Penn GlobalProtect VPN for any of this to work. Never run training or heavy compute on a login node.
