# PARCC / Betty - Login and Orientation

A simple repeatable guide to log in to Betty and get oriented. 

---

## Step 1 - Get a Kerberos ticket

Betty uses Kerberos for login. Grab a ticket, then follow the Duo (if prompted):

```
kinit wronnie@UPENN.EDU
```
Check your ticket anytime with `klist` (shows the principal and expiration). Renew with `kinit -R` or just run `kinit` again.

---

## Step 2 - SSH in

```
ssh wronnie@login.betty.parcc.upenn.edu
```

The Kerberos ticket authenticates you. You know you are in when you see the Betty banner ("Welcome to Betty! PARCC's first supercomputer") and a prompt like:

```
wronnie@login02:~$
```

**Two login hostnames exist:**

- `login.betty.parcc.upenn.edu` - general login (used above)
- `slurm_login.parcc.upenn.edu` - used in the job-submission tutorials

Either gets you onto Betty. If a job-submission example references `slurm_login`, use that.

---

## Optional Step (optional, one time) - Set up an SSH key to skip repeated auth

Generating an SSH key and registering it means smoother future logins. On your Mac:

```
ssh-keygen -t ed25519          # encrypt with a passphrase when prompted
kinit pennkey@UPENN.EDU
ssh-copy-id pennkey@login.betty.parcc.upenn.edu
```

You can also add SSH multiplexing to `~/.ssh/config` so one connection is reused (sign in once, open many sessions). Add to a `Host *.parcc.upenn.edu` block:

```
Host *.parcc.upenn.edu
  VerifyHostKeyDNS yes
  GSSAPIAuthentication yes
  ControlMaster auto
  ControlPath ~/.ssh/control:%h:%p:%r
```

The `GSSAPIAuthentication yes` line is what makes Kerberos work over SSH, so it is worth adding regardless.

---
# Generic info

 - You are on the LOGIN node - do not run heavy work here

`login0x` is a shared login node, like PMACS's `hpclogin1`. Rules:

- Do NOT run training, inference, or big data processing directly here.
- Light commands only: `ls`, `cd`, editing files, checking status, submitting jobs.
- For real compute, request a node (Step 6).

---
## First orientation commands

Run these once to see where you stand. (If any say "command not found," make sure your PATH contains `/vast/parcc/sw/bin`.)

```
parcc_quota.py            # your storage: home (small) vs project (big)
parcc_sfree.py            # free nodes, partitions, GPU availability
parcc_sqos.py             # which QOS you are allowed to request
```

These three answer: how much space you have, where jobs can run, and what you can request.

---

## Know your two storage locations

| Pool    | Path                                        | Size   | Use for                       |
| ------- | ------------------------------------------- | ------ | ----------------------------- |
| home    | `/vast/home/w/"pennkey"`                    | 50 GB  | scripts, configs, small files |
| project | `/ceph/projects/ycheng11/ycheng11lab-hippa` | 536 GB | data, models, scGPT work      |

**Do heavy work in the project (ceph) space, not home.** Home is small and fills fast. Your data and models belong in the ceph project directory.

```
cd /ceph/projects/ycheng11/ycheng11lab-hippa
ls
```


---

## Step 7 - Get a compute node (interactive)

Real Betty partitions:

- `dgx-b200` - GPU nodes (NVIDIA B200)
- `genoa-std-mem` - CPU nodes (AMD Genoa)

Check live availability first: `parcc_free.py` or `sinfo`.

CPU interactive session:

```
salloc -p genoa-std-mem --cpus-per-task=4 --mem=16G --time=02:00:00
```

GPU interactive session (a quick "hello GPU" test that runs nvidia-smi and exits):

```
srun -p dgx-b200 --gpus=1 -t 00:01:00 nvidia-smi
```

Or an interactive GPU shell:

```
srun --pty -p dgx-b200 --gpus=1 --cpus-per-task=8 --mem=64G --time=02:00:00 bash
```

On the compute node, load software and activate your env:

```
module load anaconda3
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate <your-env-path>
```

The `source ...conda.sh` line is required for `conda activate` to work in scripts and non-interactive shells. When done, `exit` to release the node.

---

## Step 8 - Submit a real job (batch)

For training or long runs, do NOT use interactive. Write a script and `sbatch` it. This is the real Betty GPU template (based on the PARCC MNIST tutorial). Save as `job.sbatch`:

```bash
#!/bin/bash
#SBATCH --job-name=scgpt
#SBATCH --output=slurm-%j.out
#SBATCH --time=04:00:00
#SBATCH --partition=dgx-b200        # GPU partition on Betty
#SBATCH --gpus=1
#SBATCH --cpus-per-task=14
#SBATCH --mem=256G

module load anaconda3
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate <your-env-path>

hostname
nvidia-smi || true                  # quick debug info
python your_script.py
```

Then:

```
sbatch job.sbatch          # submit
squeue -u $USER            # check status (PENDING / RUNNING)
tail -f slurm-<JOBID>.out  # watch output live
scancel <JOBID>            # cancel if needed
```

Batch jobs survive disconnection, so you can close your laptop and come back.

```

**IMPORTANT - ColdFront access:** to submit SLURM jobs at all, you must be on your PI's ColdFront project allocation.

---

