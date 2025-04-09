---
layout: default
title: Basics
parent: Dry Lab SOPs
has_children: false
nav_order: 10
---
<!--Merge this page with intro to computation and Dry Lab SOP index-->
# {{page.title}}

## PMACS HPC Usage

Refer to the [HPC wiki](https://hpcwiki.pmacs.upenn.edu/index.php/HPC:User_Guide) and if that is not sufficient, email HPC support at [psom-pmacshpc@pennmedicine.upenn.edu](psom-pmacshpc@pennmedicine.upenn.edu). Bala is typically the one to answer questions to this account.

### Port Forwarding for Jupyter Notebooks

Occassionally, you'd want to program and use Jupyter Notebooks, but the 20GB limit on the Posix server is far too little memory. You can instead start an interactive job on the HPC with a higher memory cap and use that and port forwarding.

First, start an interactive job. Here's an example one, you can change the number of cores and amount of memory to fit your needs, the more resources, the longer it will take to get access to it, though.

`bsub -n 4 -M 100000 -R "rusage[mem=100000] span[hosts=1]" -Is bash`

Navigate to what will be your root directory for you notebook. For some reason, you can't fully explore the filesystem with jupyter, so make sure everything you need is in that directory or any subdirectories.

Start a jupyter notebook server like so:

`jupyter notebook --ip $(hostname)`

You should see a lot of logging text fill the screen. The important bit is on the bottom and looks like this:

    ...
    [C 11:01:27.037 NotebookApp]

        To access the notebook, open this file in a browser:
            file:///home/jfmaurer/.local/share/jupyter/runtime/nbserver-196944-open.html
        Or copy and paste one of these URLs:
            http://node198:8888/?token=43af8f011f60ad0c15d2faeee6ff34892efc8952dfa27e8e
        or http://127.0.0.1:8888/?token=43af8f011f60ad0c15d2faeee6ff34892efc8952dfa27e8e
    [I 11:01:27.302 NotebookApp] Skipped non-installed server(s): bash-language-server, dockerfile-language-server-nodejs, javascript-typescript-langserver, jedi-language-server, julia-language-server, pyright, python-language-server, python-lsp-server, sql-language-server, texlab, typescript-language-server, unified-language-server, vscode-css-languageserver-bin, vscode-html-languageserver-bin, vscode-json-languageserver-bin, yaml-language-server

If your output looks like this, copy the second URL with the localhost IP (127.0.0.1:8888). Don't do anything just yet.

#### Windows MobaXTerm

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

## The different types of analyses that we do

## Uploading Our Raw Data for Review