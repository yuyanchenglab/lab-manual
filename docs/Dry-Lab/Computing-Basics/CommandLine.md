---
layout: default
title: Command Line
parent: Computing Basics
grand_parent: Dry Lab
has_children: false
nav_order: 20
---

<!-- MOVED + edited from docs/Intro to Computation/Programming.md — this page keeps the command-line/job-submission content; the Python/R content moved to PythonR.md. -->

# {{page.title}}

## Client Access

Setup options are on the [HPC wiki](https://hpcwiki.pmacs.upenn.edu/wiki/index.php/HPC:Login#SSH_Clients). Mac's Terminal app works but is missing some commands (see Personalization below). Install a free FTP client (WinSCP, CyberDuck, Filezilla) for a GUI file transfer — use the **SFTP** connection type.

## Logging In

First time: follow the [HPC wiki's First Login steps](https://hpcwiki.pmacs.upenn.edu/index.php/HPC:Login#First_Login). Otherwise:

```
$ ssh <PMACS_ID>@consign.pmacs.upenn.edu
```

If the password prompt never comes and the connection times out, check you're on the VPN.

## Command Line Personalization

Your `.bashrc` runs on every new terminal/job submission. To use lab-installed software, add to it:

```bash
if [ $HOSTNAME != "consign.hpc.local" ] &&
   [ $HOSTNAME != "mercury.pmacs.upenn.edu" ] &&
   [ $HOSTNAME != "hpclogin.pmacs.upenn.edu" ] &&
   [ $HOSTNAME != "hpclogin1" ]; then
    LAB_SOFTWARE="/project/hipaa_ycheng11lab/software/"
    SOFTBIN="${LAB_SOFTWARE}/bin/"
    PATH=$SOFTBIN:$PATH
    export PATH
fi
```

On your own machine, Mac users should install [Homebrew](https://brew.sh/) (`apt-get`/`yum`/`pip`'s equivalent):

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

then e.g. `brew install wget`.

Windows/MobaXTerm: Settings → Configurations → Terminal Features → set logging to printable output with timestamps (very useful for later debugging). You can also create SSH sessions for Mercury/Consign — right-click the session → Edit Session → Advanced SSH Settings → Execute Command `newgrp hipaa_ycheng11lab`, so files you create are shared with the lab.

## Interactive Nodes

Mirrors the [HPC User Guide](https://hpcwiki.pmacs.upenn.edu/wiki/index.php/HPC:User_Guide) — worth a read for more detail.

Use an interactive node for compute-intensive jobs rather than running directly on the head node (`consign.pmacs.upenn.edu`):

```
$ bsub -Is bash
$ bsub -n 4 -R "rusage[mem=75000] span[hosts=1]" -M 75000 -Is bash   # with more memory/cores
```

For a Jupyter notebook within the node (Mac steps — see [Tutorials → IDE Setup](../Tutorials/Access/SetupIDE) for the full walkthrough; other OSes: [HPC wiki](https://hpcwiki.pmacs.upenn.edu/wiki/index.php/HPC:Jupyter)):

* `cd` to your working directory first (Jupyter's GUI navigation between subdirectories is limited).
* On the interactive node: `jupyter notebook --ip $(hostname)`
* In another local terminal, tunnel in: `ssh -L 8888:node###:8888 <your_username>@consign.pmacs.upenn.edu` (match node name/port to the output)
* Open the `http://127.0.0.1...` link from the notebook output — unique per session.

## Submitting Jobs

Basic:

```
$ bsub <script_name>
```

With parameters:

```
$ bsub -J IHRA_markers -e IHRA_markers.%J.error -n 8 -R -M 1024 'rusage[mem=1024] span[hosts=1]' bash IHRA_gene_marker_predicates.bash
```

| Flag | Meaning |
|---|---|
| `-J IHRA_markers` | LSF job name |
| `-o IHRA_markers.%J.out` | output file (needed to receive one) |
| `-e IHRA_markers.%J.error` | error file (needed to receive one) |
| `-n 8` | cores requested |
| `-M 1024` | MB of memory |
| `-R 'rusage[mem=1024] span[hosts=1]'` | ensure enough memory + all cores on one node |
| `bash` | job type |
| `IHRA_gene_marker_predicates.bash` | script name |

Or run an LSF job script directly (parameters live in the file's header):

```
$ bsub < <script_name>
```

```bash
#!/bin/bash
#BSUB -J JNAME
#BSUB -o JNAME.%J.out
#BSUB -e JNAME.%J.error
#BSUB -n 1
#BSUB -M 10
#BSUB -R "rusage[mem=10] span[hosts=1]"
#BSUB -notify done         # email when the job finishes
#BSUB -u <username>@pennmedicine.upenn.edu   # required alongside -notify

echo "hello"
```
