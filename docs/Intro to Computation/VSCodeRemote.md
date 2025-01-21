---
layout: default
title: Setting VS Code for PMACS HPC
has_children: false
nav_order: 10
--- 

# Setting Up VS Code for PMACS HPC

This guide will walk you through installing VS Code locally, setting up a remote VS Code server on a PMACS HPC worker node, and tunneling into it. This approach lets you leverage VS Code’s interactive features, such as native notebook support, for your remote workflows on the HPC. It includes two approaches:

1. **Interactive Session** (simple, but limited to 8 hours).  
2. **Alternate Method** (preferred if you want longer sessions).

## Quick Overview

1. Install VS Code and the Remote - Tunnels extension on your local computer.  
2. Install the VS Code CLI on the PMACS HPC server.  
3. **Approach A (Interactive):** Start an interactive HPC session, run `code tunnel`, and connect.  
4. **Approach B (Scripted):** Submit a job script that runs the VS Code server in a non-interactive queue for a longer duration.  

---

## Step 1: Install VS Code Locally

1. Download and install VS Code from the [official download page](https://code.visualstudio.com/download).  
2. Launch VS Code and sign in using GitHub or Microsoft. **This login is required to verify and authenticate your remote tunnels**.
3. In VS Code, install the **Remote - Tunnels** extension by Microsoft from the Extensions Marketplace.

---

## Step 2: Install the VS Code CLI on PMACS HPC

1. **Check Architecture**  
   ```bash
   uname -m
   ```  
   Confirm output is `x86_64`.

2. **Download the VS Code CLI**  
   ```bash
   wget -P ~/.local/bin https://code.visualstudio.com/sha/download?build=stable&os=cli-alpine-x64
   tar -xvf ~/.local/bin/code-server.tar.gz -C ~/.local/bin
   ```

3. **Add `~/.local/bin` to PATH** (if needed)  
   ```bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   which code
   ```  
   You should see `~/.local/bin/code` in the output.

---

## Approach A: Using an Interactive Session (Up to 8 Hours)

1. **Request an Interactive Node**  
   ```bash
   bsub -n 4 -R "rusage[mem=8000]" -Is bash
   ```  
   Adjust CPU and memory as needed. By default, interactive queue limits sessions to around 8 hours. You can check queue limits using:
   ```bash
   bqueues -l interactive
   ```

2. **Start the VS Code Tunnel**  
   ```bash
   code tunnel
   ```  
   Authenticate if prompted. You’ll see a link in the terminal once the server is ready.

3. **Connect Locally**  
   - In your local VS Code, open the **Remote Explorer** side panel.  
   - Under **Tunnels**, you should see your PMACS session. Click to connect.  
   - Alternatively, use the Command Palette, search for **Remote-Tunnels: Connect to Remote Tunnel**, and pick the PMACS session.

---

## Approach B: Submitting a Script for Longer Sessions

Use this method if you need more than 8 hours. You’ll submit a job to a queue that has a longer time limit (e.g., normal queue).  

### 1. Pre-Authenticate (Optional but Recommended)

Before you submit your script, make sure you’re logged in to VS Code Tunnels on the HPC. This avoids having to grab a device code while the job runs.

```bash
code tunnel user login --provider github
code tunnel user show
```

If you see an active account, you’re ready.

### 2. Create a Submission Script

Below is an example script (call it `vscode_server.sh`) that requests 48 hours:

```bash
#!/bin/bash
#BSUB -J  vscode_server       # Job name
#BSUB -W 48:00                # Wall time
#BSUB -n 4                    # Number of cores
#BSUB -M 51200                # 50GB of memory total
#BSUB -o vscode.%J.log        # Standard output log
#BSUB -e vscode.%J.error      # Standard error log

# Load any needed modules here
# Example: module load python

# Run the VS Code tunnel
code tunnel --accept-server-license-terms
```

Adjust resources (`-W`, `-n`, `-M`) based on your needs.

### 3. Submit the Script

From the HPC login node, run:

```bash
bsub < vscode_server.sh
```

Take note of the job ID printed to the screen (e.g., `<86979279>`).

### 4. Check Job Output and Tunnel Status

Use `bpeek` to view output while the job runs:

```bash
bpeek <JobID>
```

If you’re not pre-authenticated, the output might show something like:

```
To grant access to the server, please log into https://github.com/login/device and use code 87B9-A3B8
```

Go to that URL on your local machine, enter the code, and complete authentication.

### 5. Connect From Your Local VS Code

- Once the server is up, open VS Code on your local machine.  
- Go to the **Remote Explorer**. Under **Tunnels**, look for your HPC job.  
- Or use the Command Palette: **Remote-Tunnels: Connect to Remote Tunnel** and select the PMACS HPC session.

At this point, you should be able to open files, notebooks, and terminals through your local VS Code, with the job potentially running for up to the time limit you requested (`-W 48:00` in the script).

---

## Notes and Troubleshooting

- **Why Tunnels Instead of SSH?** SSH access into worker nodes is restricted and sessions don’t persist across HPC worker node changes. The VS Code tunnel follows you to the worker node.  
- **Queue Limits**: The interactive queue has shorter limits (often 8 hours). To see details, run `bqueues -l interactive`. If you need more time, submit to a different queue with higher limits.  
- **Stuck Tunnel?** If the remote tunnel doesn’t appear, reload your local VS Code window (`Ctrl+R` or `Cmd+R`) or rerun the script.  
- **Resource Adjustments**: If you need more memory or CPU, update `-n` and `-M` in your job script.  

By following these steps, you can keep a long-running VS Code server session active on PMACS HPC, allowing you to work interactively on your remote code and data without worry of hitting the 8-hour limit.