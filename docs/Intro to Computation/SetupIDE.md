---
layout: default
title: IDE Setup
has_children: false
parent: Intro to Computation
nav_order: 15
--- 

# {{page.title}}

With access to the PMACS server from [Intro to Computational Resources](ComputationResources.html), here are some IDE options. 

 * [VS Code](#VS-Code)
 * [Jupyter Notebook](#Jupyter-Notebook)

While the Posix server does support these IDEs, it does pose a 20GB memory limit on your work. These options allow you to request more resources.

---
<a name="VS-Code"></a>

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

1. **Download the VS Code CLI (Already Done!!!)**
   
   4/15/25: Changed to version 1.85 due to server having GLIBC 2.17.0 which is not supported
   by vs code versions 1.86 and newer

   ```bash
   # Download the VS Code Server v1.85 archive into the target directory and name it vscode-server.tar.gz
   wget -O /project/hipaa_ycheng11lab/software/vscode_1.85/vscode-server.tar.gz "https://update.code.visualstudio.com/1.85.2/cli-alpine-x64/stable"

   # Extract the downloaded archive in the same directory, stripping the top-level folder (adjust --strip-components as needed)
   tar -xzf /project/hipaa_ycheng11lab/software/vscode_1.85/vscode-server.tar.gz -C /project/hipaa_ycheng11lab/software/vscode_1.85
   ```

2. **Add `/project/hipaa_ycheng11lab/software/vscode_1.85` to PATH** (if needed)

   ```bash
   # Check if the VS Code Server bin directory is already in PATH
   echo $PATH | grep --color "/project/hipaa_ycheng11lab/software/vscode_1.85"

   # Add the VS Code Server executable to the PATH for all users via the shared installation
   echo '# Include the VS Code Server executable from the shared installation in PATH' >> ~/.bashrc
   echo 'export PATH="/project/hipaa_ycheng11lab/software/vscode_1.85:$PATH"' >> ~/.bashrc

   # Reload your bash configuration
   source ~/.bashrc

   # Verify the 'code' executable is now being used
   which code
   ```

You should see `/project/hipaa_ycheng11lab/software/vscode_1.85/bin/code` in the output.

---

## Approach A: Using an Interactive Session (Up to 8 Hours)

1. **Request an Interactive Node**

   ```bash
   bsub -n 4 -R "rusage[mem=8000]" -Is bash
   ```

   Adjust CPU and memory as needed. By default, the interactive queue limits sessions to 8 hours.

2. **Start the VS Code Tunnel**

   ```bash
   code tunnel
   ```

   Authenticate if prompted. The account you use to authenticate will connect VS Code to the tunnel you just opened. You’ll see a link in the terminal once the server is ready.

3. **Connect Locally**

   - In your local VS Code, open the **Remote Explorer** from the side bar. The logo is a monitor with a `><` badge in front.
   - Under **Tunnels**, you should see your PMACS session. It will use your name. Click to connect.  
   - Alternatively, use the Command Palette, search for **Remote-Tunnels: Connect to Remote Tunnel**, and pick the PMACS session.

---

## Approach B: Submitting a Script for Longer Sessions

1. Pre-Authenticate (Optional, but Recommended)

Before you submit your script, make sure you’re logged in to VS Code Tunnels on the HPC. This avoids having to grab a device code while the job runs.

```bash
code tunnel user login --provider github
code tunnel user show
```

If you see an active account, you’re ready.

2. Create a Submission Script

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

3. Submit the Script

From the HPC login node, run:

```bash
bsub < vscode_server.sh
```

Take note of the job ID printed to the screen (e.g., `<86979279>`).

4. Check Job Output and Tunnel Status

Use `bpeek` to view output while the job runs:

```bash
bpeek <JobID>
```

If you’re not pre-authenticated, the output might show something like:

```
To grant access to the server, please log into https://github.com/login/device and use code 87B9-A3B8
```

Go to that URL on your local machine, enter the code, and complete authentication.

5. Connect From Your Local VS Code

- Once the server is up, open VS Code on your local machine.  
- Go to the **Remote Explorer**. Under **Tunnels**, look for your HPC job.  
- Or use the Command Palette: **Remote-Tunnels: Connect to Remote Tunnel** and select the PMACS HPC session.

At this point, you should be able to open files, notebooks, and terminals through your local VS Code, with the job potentially running for up to the time limit you requested (eg `-W 48:00` in the script).

---

## Notes and Troubleshooting

- **Why Tunnels Instead of SSH?** SSH access into worker nodes is restricted and sessions don’t persist across HPC worker node changes. The VS Code tunnel follows you to the worker node.
- **Queue Limits**: The interactive queue has shorter limits (often 8 hours). To see details, run `bqueues -l interactive`.
- **Stuck Tunnel?** If the remote tunnel doesn’t appear, reload your local VS Code window (`Ctrl+R` or `Cmd+R`) or rerun the script.  
- **Resource Adjustments**: If you need more memory or CPU, update `-n` and `-M` in your job script.  


<a name="Jupyter-Notebook"></a>

# Setting Up Jupyter Notebook for PMACS HPC

## Mac

This guide will walk you through setting up a remote Jupyer server on a PMACS HPC worker node and tunneling into it. This guide only walks through the process for setting it up from an interactive session. This guide borrows from the HPC wiki guide [here](https://hpc.upenn.edu/wiki/index.php/HPC:Jupyter) but is more updated as of 02/19/2025.

**NOTE**: The following instructions are for Mac clients. For Windows clients, the process is essentially the same. MobaXTerm does have a GUI for port forwarding in place of step 3.

1. Log into an interactive session on the HPC. Navigate to your working directory since it is difficult to navigate to anything by subdirectories from the Jupyter GUI. 

If this is your first walkthrough, install the missing packages from the python/3.11 module.

```[obki@consign ~]$ bsub -Is bash
<< Waiting for dispatch...>>
<<Starting on node157.hpc.local>>
[obki@node157 ~]$ module load python/3.11 gcc/12.2.0 # gcc/10.2.0 also works.
[obki@node157 ~]$ pip install -U jupyter_nbextensions_configurator jupyter_server_proxy scikit-learn # If first time
```

**NOTE**: If another version of python or gcc is loaded in, you can remove it by running `module remove gcc/VERSION`, where VERSION is the one you don't want to use.

2. Run `jupyter notebook --ip $(hostname)`

You should see output like the following:

```[I 16:13:48.696 NotebookApp] Serving notebooks from local directory: /home/obki
[I 16:13:48.696 NotebookApp] The Jupyter Notebook is running at:
[I 16:13:48.696 NotebookApp] http://node157.hpc.local:8888/?token=fbf40f23ca994ac5046337e6427ffea8d2be346fa54653ff
[I 16:13:48.696 NotebookApp]  or http://127.0.0.1:8888/?token=fbf40f23ca994ac5046337e6427ffea8d2be346fa54653ff
[I 16:13:48.697 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[W 16:13:48.707 NotebookApp] No web browser found: could not locate runnable browser.
[C 16:13:48.707 NotebookApp]


    To access the notebook, open this file in a browser:
        file:///home/obki/.local/share/jupyter/runtime/nbserver-19940-open.html
    Or copy and paste one of these URLs:

        http://node157.hpc.local:8888/?token=fbf40f23ca994ac5046337e6427ffea8d2be346fa54653ff
     or http://127.0.0.1:8888/?token=fbf40f23ca994ac5046337e6427ffea8d2be346fa54653ff
```

If you see something similar to the above, you have set up the Jupyter Server. Leave this running.

3. If you are on Windows MobaXTerm, this is where you can choose to continue here or use the GUI. Keep the previous terminal open and create a new terminal on your Mac or Linux machine. Create the tunnel using the following command:

```ssh -L 8888:node157:8888 <your_user_name>@consign.pmacs.upenn.edu```

Since the interactive session with the Jupyter Server is running on "node157", use that hostname in the above SSH forwarding command. Similarly, if the Jupyter Server is on different port number than `8888`, change the two `8888`'s in the forwarding command to match the port number in the URL generated by the "jupyter notebook --ip $(hostname)" command.

4. Copy the link generated in the output of the "jupyter notebook --ip $(hostname)" command (the link that starts with "http://127.0.0.1:").

In the above example, that would be:

```http://127.0.0.1:8888/?token=fbf40f23ca994ac5046337e6427ffea8d2be346fa54653ff```

**NOTE**: This link is unique and you will not be able to bookmark it.

Paste the link into a web browser and you should have the Jupyter IDE in the browser.

## Windows MobaXTerm

The following procedure gets the same results as the Mac instructions. You would start this procedure instead of step 3 in the Mac section.

1) Use the `Tools -> MobaSSHTunnel (port forwarding)` option to pull up a window.

2) Start a new SSH tunnel.
If you have a tunnel already setup, you need to make sure you activate it only after you started the jupyter server in the first place.

3) Fill in the information from local client to remote server.

    MyComputer port: 8888
    Firewall
    SSH Server: PMACS_USERNAME@consign, port 22
    Remote Server: nodeNODENUM.hpc.local, port 8888 unless the URL says otherwise.

Save.

4) Give the tunnel a name by clicking on the name in the list of tunnels.

5) Start the tunnel by pressing the play button.

6) Go to a browser and paste the URL you copied before. You should see a jupyter notebook GUI in your webpage and you have successfully done it! Additionally, the CLI where you started the server should report a GET request.