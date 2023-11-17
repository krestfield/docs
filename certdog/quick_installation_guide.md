---
layout: default
title: Quick Windows Installation
parent: Certdog
nav_order: 4
---

# Certdog Quick Windows Installation

> From version: 1.8.0

 <br>

See [here](download-locations.html) for download locations and instructions

See [here](demo-quickstart.html) for the demo installation (which will install with a single command using default values for the admin user)

<br>

Open a PowerShell window as Administrator and navigate to the installation directory, e.g.:

```powershell
cd c:\certdog\install\
```

Set up your initial usernames and passwords:

```powershell
$dbPassword='password'
$adminUsername='admin'
$adminEmail='admin@nowhere.com'
$adminPassword='password'
```

Note, to enter the passwords in a secure way, you may obtain the admin credentials as follows:

```
$adminUser=GetCredential
```

Enter the admin username and password. Then run the following to set the ``$adminUsername`` and ``$adminPassword`` variables

```
$adminUsername = $adminUser.UserName
$adminPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($adminUser.Password))
```

<br>

Run the installation as follows:

```powershell
.\install.ps1 `
	-acceptEula ` 
	-dbAdminPassword $dbPassword `
	-firstAdminUsername $adminUsername `
	-firstAdminEmail $adminEmail `
	-firstAdminPassword $adminPassword `
	-listeningIpAddress 0.0.0.0 `
	-listeningPort 443 `
	-installAdcsAgent
```

