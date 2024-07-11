---
layout: default
title: Intro to Programming
nav_order: 2
parent: Intro to Computation
has_children: false
---

# {{page.title}}

In your .bashrc file in your home directory on the HPC server, I suggest you place these lines: 

```
if [ $HOSTNAME != "consign.hpc.local" ] &&
   [ $HOSTNAME != "mercury.pmacs.upenn.edu" ] &&
   [ $HOSTNAME != "hpclogin.pmacs.upenn.edu" ] &&
   [ $HOSTNAME != "hpclogin1" ]; then
    module load R4.3
    module load python/3.11
    module load sratoolkit/3.1.0
    module load curl
    module load fastqc/0.11.7
fi 
```

This way, we are all working on the same version of R and python and so that you can use some commonly used tools without thinking about it in the future. 

## Intro to the Command Line

## Intro to Python

## Intro to R

Quite a lot of biostat packages are run in R for a few reasons: 

* CRAN
* Statistics oriented syntax
* Rstudio

CRAN stands for the “Comprehensive R Archive Network” and is where you are likely to find additional R code for your use. By simply performing `installPackages(“magittr”)` in the R interpretter, R will go to CRAN through your internet connection and install that package for you. All you have to do is `library(magittr)` all of the magittr package is available to you! 

R is statistically oriented in quite a few different ways. The base package that is loaded for you when you open R contains native operators for linear algebra and set operations, such as %in% for testing set intersection and %o% for outer products. It has a base system of plotting and quickly creating test data, such as the built-in datasets and the r* distribution functions. 

Rstudio is the IDE that has everything you would want to run, troubleshoot and profile code. It allows you to run your code right from the source editor. Feel free to customize the look of your Rstudio to fit your needs. 

If you are using a large dataset, remember that the Rstudio server that you should have access has a limit of 20GB of memory. If you need to use more than that, you must use an interactive session with enough memory and use the command line. If you figure out how to run your own Rstudio server on the HPC to tunnel into, reach out to Jeff at Jeffrey.Maurer@pennmedicine.upenn.edu or reach out less formally in Slack. 