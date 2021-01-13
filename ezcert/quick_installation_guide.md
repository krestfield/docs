---
layout: default
title: Quick Windows Installation
parent: EzCert
nav_order: 2
---

# Quick Windows Installation

 

If you want to get up and running quickly - just go through the following 10 steps

More detailed information can be found [here](.\installation.html) - including how to verify the download and troubleshooting. It is recommended that you read through this (when you have more time) and before you install EzCert on any production systems 

But for now...

 

1. [Click here to download](https://krestfield.s3.eu-west-2.amazonaws.com/ezcert/v1.0.1/ezcert.zip) and unzip on to the local drive

2. Open a PowerShell as **Administrator** and navigate to the **.\install** directory of the unzipped folder

   Run ``.\install.ps1``

3. Say yes (**y**) to download java and the database binaries

4. Enter a *password* for the **Database User Admin Account**

5. Enter a *username*, *email* and *password* for the **First Admin User Account**

6. For interfaces choose **0.0.0.0 (Listen on all)**

7. Enter a *password* for the **master password**

8. If you are on a server based machine (Server 2016/2019) say yes (**y**) to install the ADCS agent, otherwise choose no (**n**)

9. Open a browser and navigate to: [https://127.0.0.1/ezcert/ui](https://127.0.0.1/ezcert/ui)

10. Enter the username and password as configured in step 5 above



To temporarily remove any browser TLS warnings, install this file ``.\ezcert\config\sslcerts\dbssl_root.cer`` into your local certificate trust store