---
layout: default
title: Quick Windows Installation
parent: Certdog
nav_order: 2
---

# Certdog Quick Windows Installation

 <br>

Ensure you have the .NET v4.8 runtime installed and have the required Administrator privileges  

You can install this on Windows Server 2016 or 2019. If installing on Windows 10 and you require access to a Microsoft ADCS Certificate Authority the RSAT (Remote Server Administration Tools) for Windows 10 are also required

More detailed information can be found [here](.\installation.html) - including how to verify the download and account details etc. It is recommended that you read through this (when you have more time) and before you install certdog on any production systems 

But for now...

<br> 

1. Obtain the download link from your FTP account or contact support@krestfield.com, download and unzip on to the local drive  
2. Open a PowerShell as **Administrator**, navigate to the **.\install** directory of the unzipped folder and run ``.\install.ps1`` (e.g. ``c:\certdog\install\install.ps1``)
4. Enter a *password* for the **Database User Admin Account**
5. Enter a *username*, *email* and *password* for the **First Admin User Account**
6. For interfaces choose **0.0.0.0 (Listen on all)** and accept the default port (443)
7. Enter a *password* for the **master password**
8. Say yes (**y**) to install the ADCS agent
9. To temporarily remove any browser TLS warnings, install this file ``.\certdog\config\sslcerts\dbssl_root.cer`` into the **Local Machine's**  **Trusted Root Certification Authorities** store  
10. Open a browser and navigate to: [https://127.0.0.1/certdog/ui](https://127.0.0.1/certdog/ui)
11. Enter the username and password as configured in step 4 above to login

<br>

If you hit any issues, see the troubleshooting guide [here](install_troubleshooting.html)