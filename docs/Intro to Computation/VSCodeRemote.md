---
layout: default
title: Setting VS Code for PMACS HPC
has_children: false
nav_order: 10
---

# Setting Up VS Code for PMACS HPC

This guide will walk you through installing VS Code locally, setting up a remote VS Code server on a PMACS HPC worker node, and tunneling into it. This approach lets you leverage VS Code’s interactive features, such as native notebook support, for your remote workflows on the HPC.

### Overview
1. Install VS Code and the Remote - Tunnels extension.
2. Install the VS Code CLI on the remote server.
3. Start an interactive session on the PMACS HPC worker node and run a VS Code server.
4. Connect to the remote server instance from your local VS Code.

---

### Step 1: Install VS Code Locally

1. Download and install VS Code from the [official download page](https://code.visualstudio.com/download).
2. Launch VS Code and log in with either your GitHub or Microsoft account. **This login is required to verify and authenticate your remote tunnels**.
3. In VS Code, install the **Remote - Tunnels** extension by Microsoft from the Extensions Marketplace. This extension is essential for establishing and managing remote tunnels.

---

### Step 2: Install the VS Code CLI on the PMACS HPC Server

1. **Determine Your Architecture**:
   - Connect to the PMACS HPC via SSH (to the main cluster, not a worker node).
   - Run:
     ```bash
     uname -m
     ```
   - Confirm that the output shows `x86_64`, which indicates 64-bit architecture.

2. **Download the VS Code CLI**:
   - Download the **VS Code CLI for Alpine Linux (x64)** to `~/.local/bin`:
     ```bash
     wget -P ~/.local/bin https://code.visualstudio.com/sha/download?build=stable&os=cli-alpine-x64
     ```
   - Unzip the downloaded file:
     ```bash
     tar -xvf ~/.local/bin/code-server.tar.gz -C ~/.local/bin
     ```
   
3. **Add `~/.local/bin` to Your PATH** (if not already done):
   - Append this to your `.bashrc` file:
     ```bash
     echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
     source ~/.bashrc
     ```
   - Verify the installation:
     ```bash
     which code
     ```
   - You should see `~/.local/bin/code` in the output, confirming the CLI is correctly installed.

---

### Step 3: Start a Remote VS Code Server on a PMACS Worker Node

1. **Request an Interactive Node on the PMACS HPC**:
   - Use the following command to request an interactive session:
     ```bash
     bsub -n 4 -R "rusage[mem=8000]" -Is bash
     ```
   - Adjust the memory and CPU cores (`-n` and `mem` parameters) as needed for your work.

2. **Start the VS Code Tunnel**:
   - Once on the interactive node, start a VS Code tunnel by typing:
     ```bash
     code tunnel
     ```
   - You will be prompted to log in with your GitHub or Microsoft account to authenticate the tunnel. Follow the instructions to complete this verification.

3. **Confirm Tunnel Startup**:
   - After successful authentication, the terminal will display a link, showing that the VS Code server is active and accessible through the tunnel.

---

### Step 4: Connect to the Remote Instance in Local VS Code

1. **Open the Remote Explorer in VS Code**:
   - On your local machine, open VS Code and navigate to the **Remote Explorer** tab on the sidebar.
   - Under **Tunnels**, you should see the active tunnel corresponding to your remote PMACS session.

2. **Connect Using the Command Palette (Optional)**:
   - Alternatively, open the Command Palette (`Cmd + Shift + P` on macOS or `Ctrl + Shift + P` on Windows/Linux).
   - Select **Remote-Tunnels: Connect to Remote Tunnel**, and choose your remote PMACS server from the list.

3. **Verify Functionality**:
   - Open a test file or Jupyter notebook to ensure that you can edit, save, and run code in the remote environment.
   - Confirm access to files and notebooks, as well as the interactive features you intend to use.

---

### Notes and Troubleshooting

- **Why Not SSH?** While you can SSH into PMACS, SSH sessions do not persist across worker nodes due to security configurations, and the ability to SSH directly into a worker has been restricted. Using the VS Code tunnel ensures that your session follows you to the worker node for interactive use.

- **Connection Issues**: If your remote tunnel does not appear in the Remote Explorer, try reloading the VS Code window (`Cmd + R` or `Ctrl + R`) or restarting the tunnel with `code tunnel` in the remote terminal.

- **Additional Configurations**: If you encounter any limitations on memory, CPU cores, or Jupyter notebook access, you may need to adjust the parameters for your interactive session or consult PMACS documentation for further resource options.

---

With these steps, you should have a fully functional VS Code setup on the PMACS HPC for Penn Medicine, enabling efficient coding, notebook execution, and resource management on the remote server. Enjoy using VS Code to simplify your remote workflows!