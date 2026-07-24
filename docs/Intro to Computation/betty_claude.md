---
layout: default
title: Connecting the Betty (PARCC) Cluster to Claude
has_children: false
parent: Intro to Computation
nav_order: 20
---

# {{page.title}}

## What this does

This guide connects Claude to the Betty HPC cluster over SSH, so the agent can
read files, submit SLURM jobs, and pull results back. It covers both Claude
Science (through the Compute panel, Sections 1-8) and Claude Code (the terminal
agent, [Section 9](#sec-claude-code)). Nothing is installed on Betty. Claude
reaches in through a connection you authenticate. (This guide has been tested
on Mac and Ubuntu but not WSL. )

**Key idea:** Betty login requires two factors: an SSH key and a Kerberos
ticket. An
automated agent cannot answer a Duo prompt, so we set up an SSH master
connection that you authenticate once by hand. Claude Science then rides that
already-open connection and never has to log in itself.

## 1. Generate an SSH key if you don't already have one {#sec-key}

On your **local machine** (laptop/desktop), check first:

```bash
ls ~/.ssh/id_ed25519.pub
```

If that file exists, skip to [Section 2](#sec-install). Otherwise generate one:

```bash
ssh-keygen -t ed25519
```

## 2. Install your key on Betty {#sec-install}

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub <PennKey>@login.betty.parcc.upenn.edu
```

Enter your PennKey password when prompted, and complete Duo if asked. Replace
`<PennKey>` with your own.

## 3. Edit your SSH config {#sec-config}

Open `~/.ssh/config` in a text editor (like nano or vim) and add this block.

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

## 4. Get a Kerberos ticket and open the master connection {#sec-master}

Two factors are needed: your SSH key ([Section 2](#sec-install)) plus a Kerberos
ticket. Get the ticket, then open one persistent authenticated connection.

**macOS note:** If you have stacked environments, run `conda deactivate`
until your prompt shows no `(env)` prefix. If you do have stacked environments `kinit` may write the ticket to a
cache SSH cannot read. 

```bash
kinit <PennKey>@UPENN.EDU
```

Use **uppercase** `UPENN.EDU`. Complete the Duo prompt. You can check the ticket
exists with

```bash
klist
```

You should see a valid ticket for `<PennKey>@UPENN.EDU`. Now open the master
connection:

```bash
ssh -fNM betty
```

Returns silently on success. You can check: `ssh -O check betty` should
report "Master running", and `ssh betty` should drop you into a Betty shell
instantly with no prompt. If so, the connection is ready for Claude Science.

## 5. Add Betty in the Claude Science Compute panel {#sec-panel}

1. Open the **Compute** panel in the Claude Science sidebar.
2. Click **Add SSH host**.
3. If `betty` already appears in the detected-hosts list, select it. Otherwise
   type the alias `betty` under "Or type a host alias."
4. In the "Anything Claude Science should know?" box, paste the notes in
   [Section 6](#sec-notes).
5. Save. The host should show **Connected**. If the probe fails, see
   Troubleshooting.

## 6. Cluster notes to paste into the Compute panel {#sec-notes}

The lines below are Betty-wide and safe to paste as-is. The account, partition,
and QOS depend on your project, so fill in your own (see
[Section 7](#sec-findalloc)).

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

## 7. Find your own allocation {#sec-findalloc}

Account, partitions, and QOS are per-project. These PARCC helper scripts (on
`PATH` once `/vast/parcc/sw/bin` is included) report yours:

```bash
sacctmgr -n show assoc user=$USER format=Account,Partition,QOS   # your account + QOS
parcc_sqos.py        # QOS limits (CPU / memory / GPU caps)
parcc_sfree.py       # free nodes / GPUs per partition
parcc_quota.py       # your storage quotas
```

Use the values these print to fill in the placeholders in [Section 6](#sec-notes).

## 8. Daily use / reconnecting {#sec-daily}

The Kerberos ticket lasts **10 hours** and the master connection dies when
closed or when a login node reboots. When Kerberos ticket expires (which will happen with day to day use)
and claude or claude science is reporting that it can't connect to Betty just:
```bash
kinit <PennKey>@UPENN.EDU
```

If master connection dies, repeat steps from [Section 4](#sec-master):

```bash
kinit <PennKey>@UPENN.EDU
ssh -fNM betty
ssh -O check betty     # should report "Master running"
```

## 9. Using Betty from Claude Code {#sec-claude-code}

The idea is the same as Claude
Science: it never logs in itself, it rides the master connection you opened in
[Section 4](#sec-master). Pick one of two ways to wire it up.

**Run Claude Code on your laptop, reach into Betty.**
Keep working locally and let Claude Code run cluster commands over the master
connection. Because that connection is already authenticated, `ssh betty ...`
returns with no Duo prompt:

```bash
ssh betty 'sacct -X --format=JobID,State,Elapsed -S today'   # check your jobs
ssh betty 'sbatch /ceph/projects/<you>/train.slurm'          # submit a job
```

Tell Claude Code, in its prompt or in a `CLAUDE.md`, that any cluster command
must be prefixed with `ssh betty '...'` and that real work goes through
sbatch/srun, never on the login node. Best when your code lives on your laptop
and only the compute runs on Betty.

**Run Claude Code on Betty itself.**
Connect to Betty (VSCode Remote-SSH, or just `ssh betty`) and install Claude
Code into your home directory:

```bash
curl -fsSL https://claude.ai/install.sh | bash -s stable
```

Then `cd` to your project on Ceph and run `claude`. Because it runs on Betty, it
reads and writes cluster files directly, with no `ssh betty` prefix. VSCode
Remote-SSH and plain `ssh` both reuse your master connection, so logging in is
instant with no Duo.

Two config files matter here, because Claude Code is now sitting on a login node
where heavy compute is forbidden. Here is my settings.json and claude.md.

`~/.claude/settings.json` blocks accidental training on the login node and
pauses before submitting or deleting:

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

`~/.claude/CLAUDE.md` gives it the environment facts (SLURM account, GPU/CUDA
constraints, storage layout). Adjust to your liking, a nice short and concise CLAUDE.md 
is important to avoid inefficient token usage. 

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
- GPUs are NVIDIA B200 (sm_100) → require CUDA 12.8+ builds.
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

- **"Permission denied (gssapi-with-mic,keyboard-interactive)":** your key was
  not accepted. Check that your key is really in `~/.ssh/authorized_keys` on
  Betty, and that home/`.ssh` permissions are not group-writable
  (`chmod 700 ~/.ssh`).
- **"partial success":** the key worked but the second factor is missing. Run
  `kinit` and confirm with `klist`.
- **`kinit` seems to do nothing (macOS):** run `conda deactivate` first, then
  `export KRB5CCNAME="API:"` (Sonoma 14+) and retry.
- **Probe hangs / no output:** a master connection may already be open. Check
  with `ssh -O check betty`; close a stale one with `ssh -O exit betty` and
  re-open it.
- **Interactive login works but the agent probe fails:** the agent needs the
  master connection ([Section 4](#sec-master)); a plain interactive login is not
  enough, because the agent cannot answer Duo itself. Also confirm the ticket
  has not expired (`klist`) and re-run [Section 8](#sec-daily) if it has.

## Important reminders

- You must be on campus or Penn GlobalProtect VPN for any of this to work.
- Never run training or heavy compute on a login node.
