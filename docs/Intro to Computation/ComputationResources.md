---
layout: default
title: Intro to Computational Resources
nav_order: 10
parent: Intro to Computation
has_children: false
---

# {{page.title}}

## PMACS Access

Email Dr. Cheng with the following information for access to folders in the PMACS server:

    User's Full Name: 
    User's Email: 
    User's PennKey: 
    User's PennID: 
    Lab rotation end date/Account expiration date (if applicable):

You should receive an email with the next steps. If you are in the dry lab, you should also request access to the GPU nodes and the rstudio/posix server ([https://rstudio-pro3.pmacs.upenn.edu/](https://rstudio-pro3.pmacs.upenn.edu/)). Send a friendly email requesting access to [psom-pmacshpc@pennmedicine.upenn.edu](psom-pmacshpc@pennmedicine.upenn.edu).

Additional resources:
* First login steps: [https://hpcwiki.pmacs.upenn.edu/index.php/HPC:Login#First_Login](https://hpcwiki.pmacs.upenn.edu/index.php/HPC:Login#First_Login)
* General cluster usage information: [https://hpcwiki.pmacs.upenn.edu/index.php/HPC:User_Guide](https://hpcwiki.pmacs.upenn.edu/index.php/HPC:User_Guide)
* Weekly office hours information: [https://hpcwiki.pmacs.upenn.edu/index.php/HPC:Main_Page#Weekly_Office_Hours](https://hpcwiki.pmacs.upenn.edu/index.php/HPC:Main_Page#Weekly_Office_Hours)
* Email for questions/issues: [psom-pmacshpc@pennmedicine.upenn.edu](psom-pmacshpc@pennmedicine.upenn.edu)

## PMACS Etiquette

When on PMACS, please do not use the consign headnode for work. If you ask too much of it, your command will be reaped. Don't rely on that safeguard, we want to be both user and good stewards of the server since access is a privilege.

## Computing through VPN

To access the PMACS cluster, you must have the VPN installed. Use the following PDFs to install the VPN:

* PC: [link](https://www.med.upenn.edu/pmacs/assets/user-content/documents/pmacs-vpn-windows-automated-install-and-configuration-(preferred).pdf)
* Mac: [link](https://www.med.upenn.edu/pmacs/assets/user-content/documents/pmacs-vpn-mac-os-automated-install-and-configuration-(preferred).pdf)

The instructions are slightly outdated as we no longer use the Pulse Secure client and instead use the Ivanti Secure Access client with the following icon:

<img src="/assets/images/IvantiSecureAccessIcon.webp" alt="drawing" width="50"/>

Everytime you connect to the VPN, it will ask for two factor authentication. There are three options:

* Duo Push to phone_push (iOS)
* Phone call to XXX-XXX-XXXX
* SMS passcodes to XXX-XXX-XXXX

Enter the number of your desired authentication method and complete the authentication. You should be connected afterwards. 

If there are any issues with your VPN connection, try the following. If one of these is unsuccessful, continue to the next one.

* Restart the client
* Add a new connection with remote.pmacs.upenn.edu as the server URL
* Follow the steps at this [link](https://forums.ivanti.com/s/article/Deep-Clean-Procedure-for-Windows-and-MAC?language=en_US) to uninstall and then reinstall the VPN.

