---
layout: default
title: Demo QuickStart Setup Guide
parent: Certdog
nav_order: 400
---

# Demo QuickStart Setup Guide

> From version: 1.8.0

 <br>

## Pre-Requisites

* An internet connection (as additional components may be downloaded)
* .NET v4.8 runtime
* Administrator privileges  
* Windows Server 2016/2019/2022
* Windows 10/11

<br>

## Download

1. Locate the file to download from [here](download-locations.html)

2. Right click the zip file (e.g. ``certdogfree_v180.zip``), choose **Properties** and tick the **Unblock** check box (if present). Depending on your security settings, this will prevent several prompts when running the scripts  

3. Unzip to a location on your drive e.g. if you unzip to ``C:\`` you will end up with a directory **C:\certdogfree** (but you can place this anywhere on your system)

<br>

## Installation

Open a PowerShell as **Administrator**, navigate to the **certdogfree\install** directory and run:

```powershell
.\install-demo.ps1
```

<br>

Login with the *username* and *password* that will be displayed at the end of the installation

<br>

Note that a default TLS certificate is configured for 127.0.0.1. You can issue a new TLS certificate to replace this or temporarily install the root from here: ``.\certdogfree\config\sslcerts\dbssl_root.cer`` 

<br>

If you hit any issues, see the troubleshooting guide [here](install_troubleshooting.html)

<br>

Full Documentation: [https://krestfield.github.io/docs/certdog/certdog.html](https://krestfield.github.io/docs/certdog/certdog.html)

