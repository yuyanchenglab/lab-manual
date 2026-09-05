---
layout: default
title: IDE Setup
parent: Computing Basics
grand_parent: Dry Lab
has_children: false
nav_order: 10
---

<!-- MOVED from docs/Intro to Computation/SetupIDE.md, content unchanged -->

# {{page.title}}

With access to the PMACS server (see [PMACS Usage](../Tutorials/Access/PMACS)), here are some IDE options:

* [VS Code](#VS-Code)
* [Jupyter Notebook](#Jupyter-Notebook)

The Posix server supports both, but caps you at 20GB memory — these approaches let you request more.

---
<a name="VS-Code"></a>

# Setting Up VS Code for PMACS HPC

Two approaches: **Interactive Session** (simple, capped at 8 hours) or **Alternate Method** (scripted, longer sessions).

## Step 1: Install VS Code Locally

Download from the [official page](https://code.visualstudio.com/download), sign in with GitHub or Microsoft (required for tunnel auth), and install the **Remote - Tunnels** extension.

## Step 2: Install the VS Code CLI on PMACS HPC

(Already done as of 4/15/25 — pinned to v1.85 because the server's GLIBC 2.17.0 isn't supported by v1.86+.)

```bash
wget -O /project/hipaa_ycheng11lab/software/vscode_1.85/vscode-server.tar.gz "https://update.code.visualstudio.com/1.85.2/cli-alpine-x64/stable"
tar -xzf /project/hipaa_ycheng11lab/software/vscode_1.85/vscode-server.tar.gz -C /project/hipaa_ycheng11lab/software/vscode_1.85
```

Add to `PATH` if needed:

```bash
echo $PATH | grep --color "/project/hipaa_ycheng11lab/software/vscode_1.85"
echo '# Include the VS Code Server executable from the shared installation in PATH' >> ~/.bashrc
echo 'export PATH="/project/hipaa_ycheng11lab/software/vscode_1.85:$PATH"' >> ~/.bashrc
source ~/.bashrc
which code   # should show .../vscode_1.85/bin/code
```

## Approach A: Interactive Session (up to 8 hours)

```bash
bsub -n 4 -R "rusage[mem=8000]" -Is bash
code tunnel
```

Authenticate if prompted. In local VS Code, open **Remote Explorer** → **Tunnels**, find your session by name and connect (or use Command Palette → **Remote-Tunnels: Connect to Remote Tunnel**).

## Approach B: Scripted (longer sessions)

Pre-authenticate:

```bash
code tunnel user login --provider github
code tunnel user show
```

Submission script (`vscode_server.sh`, example requests 48 hours):

```bash
#!/bin/bash
#BSUB -J  vscode_server
#BSUB -W 48:00
#BSUB -n 4
#BSUB -M 51200
#BSUB -o vscode.%J.log
#BSUB -e vscode.%J.error

code tunnel --accept-server-license-terms
```

```bash
bsub < vscode_server.sh
bpeek <JobID>   # view output; if not pre-authed, follow the device-login URL shown here
```

Then connect from local VS Code the same way as Approach A.

**Notes:** SSH into worker nodes is restricted and doesn't persist across node changes — tunnels follow you instead. Interactive queue caps at ~8 hours (`bqueues -l interactive`). Stuck tunnel → reload VS Code window or rerun the script.

---
<a name="Jupyter-Notebook"></a>

# Setting Up Jupyter Notebook for PMACS HPC

## Mac

Instructions borrow from the [HPC wiki](https://hpc.upenn.edu/wiki/index.php/HPC:Jupyter), updated as of 02/19/2025. Windows/MobaXTerm follows the same steps with a GUI for port forwarding at step 3.

1. Log into an interactive session, `cd` to your working directory.

    ```bash
    bsub -Is bash
    module load python/3.11 gcc/12.2.0   # gcc/10.2.0 also works
    pip install -U jupyter_nbextensions_configurator jupyter_server_proxy scikit-learn   # first time only
    ```

2. Start Jupyter:

    ```bash
    jupyter notebook --ip $(hostname)
    ```

    Note the node name and the `http://127.0.0.1:PORT/?token=...` URL in the output. Leave this running.

3. In a new terminal on your Mac/Linux machine, tunnel in (match the node name and port from step 2):

    ```bash
    ssh -L 8888:node157:8888 <your_username>@consign.pmacs.upenn.edu
    ```

4. Paste the `http://127.0.0.1:...` URL from step 2 into your browser. (Unique per session — not bookmarkable.)

## Windows MobaXTerm

Same result, replaces step 3 above:

1. `Tools → MobaSSHTunnel (port forwarding)` → new SSH tunnel (start it only after the Jupyter server is running).
2. Fill in: MyComputer port `8888`; SSH Server `PMACS_USERNAME@consign`, port `22`; Remote Server `nodeNODENUM.hpc.local`, port `8888` (unless the URL says otherwise). Save, name it, start it.
3. Paste the URL into a browser — you should see the Jupyter GUI, and the CLI should report a GET request.
