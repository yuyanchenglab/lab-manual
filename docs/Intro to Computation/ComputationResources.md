---
layout: default
title: Computation Resources
nav_order: 10
parent: Intro to Computation
has_children: false
---

# {{page.title}}

Refer to our [PMACS account setup](/lab-manual/docs/Onboarding/LabAccess.html#pmacs-hpc-account) section.

## PMACS Etiquette

Please do not use the Consign headnode for work. Use it to log into an interactive session or use Mercury when transferring files. If you ask too much of Consign, your command will be reaped. Don't rely on that safeguard, we want to be responsible users and good stewards of the server since access is a privilege.

## Computing through VPN

To access the rstudio/posix server or the PMACS cluster off-campus, you must have this VPN installed. Use the following PDFs to install the VPN:

* PC: [link](https://www.med.upenn.edu/pmacs/assets/user-content/documents/pmacs-vpn-windows-automated-install-and-configuration-(preferred).pdf)
* Mac: [link](https://www.med.upenn.edu/pmacs/assets/user-content/documents/pmacs-vpn-mac-os-automated-install-and-configuration-(preferred).pdf)

The instructions are slightly outdated as we no longer use the Pulse Secure client and instead use the Ivanti Secure Access client with the following icon:

<img src="/lab-manual/assets/images/IvantiSecureAccessIcon.webp" alt="drawing" width="50"/>

Everytime you connect to the VPN, it will ask for two factor authentication. There are three options:

1. Duo Push
2. Phone call to XXX-XXX-XXXX
3. SMS passcodes to XXX-XXX-XXXX

Enter the number of your desired authentication method and complete the authentication. You should be connected afterwards. 

If there are any issues with your VPN connection, try the following. If one of these is unsuccessful, continue to the next one.

* Restart the client
* Add a new connection with remote.pmacs.upenn.edu as the server URL
* Follow the steps at this [link](https://forums.ivanti.com/s/article/Deep-Clean-Procedure-for-Windows-and-MAC?language=en_US) to uninstall and then reinstall the VPN.

