---
layout: default
title: Server Access
nav_order: 10
parent: Dry Lab
has_children: false
---

<!-- NEW — assembled from docs/Onboarding/LabAccess.md (PMACS HPC Account section), docs/Intro to Computation/parcc_guide.md, and docs/Intro to Computation/ComputationResources.md (VPN section). Needs a read-through since it's newly assembled rather than moved verbatim. -->

# {{page.title}}

**Owner:** Ronnie

<!-- TODO (Ronnie): per Yuyan, this page's content should move to a Google Drive doc — replace the content below with a link to it once that's set up. -->
This page is for anyone doing computational work — getting your accounts and access set up before you start. For the day-to-day how-to once you're set up, see [Lab Tutorials → Dry Lab](Tutorials/).

## 1. PMACS HPC Account

Email Dr. Cheng with:

    User's Full Name:
    User's Email:
    User's PennKey:
    User's PennID:
    Lab rotation end date / account expiration date (if applicable):

You'll get an email with next steps. If you're in the dry lab, also request access to the GPU nodes and the RStudio/Posix server ([rstudio-pro3.pmacs.upenn.edu](https://rstudio-pro3.pmacs.upenn.edu/)) by emailing [psom-pmacshpc@pennmedicine.upenn.edu](mailto:psom-pmacshpc@pennmedicine.upenn.edu).

Reference: [HPC Wiki – First Login](https://hpcwiki.pmacs.upenn.edu/index.php/HPC:Login#First_Login), [HPC User Guide](https://hpcwiki.pmacs.upenn.edu/index.php/HPC:User_Guide).

## 2. PARCC / Betty Account

The PARCC cluster ("Betty") is used for high-GPU/demanding jobs. See [Lab Tutorials → PARCC](Tutorials/Access/PARCC) for the full login/orientation walkthrough once your account exists.

<!-- TODO: confirm the actual PARCC account-request process — parcc_guide.md assumes you already have an account. Who requests it, and is a ColdFront allocation under Yuyan's PI account required for every new dry-lab member? -->

## 3. VPN (for off-campus access)

Required for the RStudio/Posix server or PMACS cluster off-campus:

* PC: [install guide](https://www.med.upenn.edu/pmacs/assets/user-content/documents/pmacs-vpn-windows-automated-install-and-configuration-(preferred).pdf)
* Mac: [install guide](https://www.med.upenn.edu/pmacs/assets/user-content/documents/pmacs-vpn-mac-os-automated-install-and-configuration-(preferred).pdf)

These PDFs are slightly outdated — we now use the **Ivanti Secure Access** client, not Pulse Secure. Every connection requires two-factor auth (Duo push, phone call, or SMS).

If you have connection issues, in order: restart the client → add a new connection with `remote.pmacs.upenn.edu` as the server URL → [deep-clean and reinstall](https://forums.ivanti.com/s/article/Deep-Clean-Procedure-for-Windows-and-MAC?language=en_US).

## 4. Set Up Your Environment

Once you're in, continue to [Computing Basics](Computing-Basics/) for IDE setup, command-line orientation, and Python/R environments.

## 5. Get Added to the Lab Software Group

Ask Jeff to add you to the `hipaa_ycheng11lab` group so files you create are shared with the lab (see [Computing Basics → Command Line](Computing-Basics/CommandLine)).
