---
layout: default
title: PMACS Usage
parent: Tutorials
grand_parent: Dry Lab
nav_order: 20
---

<!-- MOVED + edited from docs/Intro to Computation/ComputationResources.md — the PARCC section that used to be on this page moved to PARCC.md. Everything else unchanged. -->

# {{page.title}}

Account setup: see [Onboarding → Dry Lab Setup](../../ServerAccess).

## PMACS Etiquette

Don't use the Consign headnode for work — use it to log into an interactive session or use Mercury for file transfers. If you ask too much of Consign, your command may be reaped. Don't rely on that safeguard; be a responsible user, since access is a privilege.

## Computing Through VPN

Required to access the RStudio/Posix server or PMACS cluster off-campus:

* PC: [install guide](https://www.med.upenn.edu/pmacs/assets/user-content/documents/pmacs-vpn-windows-automated-install-and-configuration-(preferred).pdf)
* Mac: [install guide](https://www.med.upenn.edu/pmacs/assets/user-content/documents/pmacs-vpn-mac-os-automated-install-and-configuration-(preferred).pdf)

These are slightly outdated — we now use the **Ivanti Secure Access** client (not Pulse Secure):

<img src="/lab-manual/assets/images/IvantiSecureAccessIcon.webp" alt="drawing" width="50"/>

Every connection requires two-factor auth: Duo push, phone call, or SMS passcode.

If you have issues, try in order:
* Restart the client
* Add a new connection with `remote.pmacs.upenn.edu` as the server URL
* [Deep-clean and reinstall](https://forums.ivanti.com/s/article/Deep-Clean-Procedure-for-Windows-and-MAC?language=en_US)
