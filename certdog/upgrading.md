---
layout: default
title: Windows Installation
parent: Certdog
nav_order: 20
---

# Upgrading Certdog

When upgrading to version 1.6 or above the following steps should be performed

<br>

### Step 1: Stop the services

Open the services snapin and stop the following services:

* Krestfield Cerdog Database

* Krestfield Cerdog Service

![Certdog Services](.\images\upgrade_services.png)

(To open the services snapin - click **Start**, type **services** and select the **Services App**)

<br>

### Step 2: Backup current installation

Rename or move your existing installation as we will be placing the new version at this location (if a rollback is required we will simply move the original folder back)

For example, rename the following folder:

```powershell
c:\certdog
```

to

```powershell
c:\certdog.bak
```

(If Windows complains that the folder cannot be renamed as it is in use, check that the services have stopped and there are no powershell, command prompts or file explorer windows open that are accessing the folder)

Make a note of this new location e.g. ``c:\certdog.bak`` as it is required in step 4 below

<br>

### Step 3: Extract the new version

Download and extract the new version to the original location. For example:

```powershell
c:\certdog
```

<br>

### Step 4: Run the upgrade

Open a PowerShell window as Administrator and navigate to your installations ``.\install`` folder e.g.

```powershell
c:\certdog\install
```

From the prompt, type ``.\upgrade.ps1`` and press **Enter**. E.g.

```powershell
PS C:\certdog\install> .\upgrade.ps1

Krestfield Certdog Upgrade to Version 1.6 from 1.5
==================================================

End User Agreement (EULA)
The EULA for this software can be obtained from the following location:
https://krestfield.s3.eu-west-2.amazonaws.com/certdog/KrestfieldCertdogEULA.pdf

By continuing and installing the software you accept the terms of this license agreement

Type 'y' to accept and continue, any other key to reject: 
```

Download and examine the EULA referenced. If happy to accept, type ``y`` to proceed with the upgrade

```powershell
Before proceeding ensure you have performed the following:

  1. The following services have been stopped:
     * Krestfield Certdog Database
     * Krestfield CertDog Service
  2. You have moved your current installation to a backup location
     E.g. Rename C:\certdog to C:\certdog.bak
  3. You have unzipped the new installer to the previous installed location E.g. C:\certdog
  4. You are running this script from the new installation C:\certdog\install\upgrade.ps1

For more information see: https://krestfield.github.io/docs/certdog/upgrading.html

Enter the location of your backup (previous certdog installation) location (e.g. c:\certdog.bak): c:\certdog.bak

Copying files from previous installation...
482 File(s) copied
83 File(s) copied
1 File(s) copied
8 File(s) copied
Starting services...
Starting database...
Starting certdog...
Upgrade Complete!
```

<br>

### Step 5: Upgrade the ADCS Driver

If you are using the ADCS Driver to interface with the Microsoft CA. You should also perform the following steps:

* Start **Apps and Features**. Locate the **Certdog ADCS Driver** and select **Uninstall**
* As an Administrator, run the ``AdcsDriverInstaller.msi``file from the ``\install\bin`` directory

This will install the new version of the driver. No further action should be required

<br>

<br>

## Rollback

If anything fails or you wish to revert back to your previous version, perform the following:

**Step 1**: Open the services snapin and stop the following services:

* Krestfield Cerdog Database

* Krestfield Cerdog Service

**Step 2**: Either move of delete the current certdog installation folder (this will currently contain the upgraded installation) e.g. delete the following folder

```powershell
c:\certdog
```

If you are just switching between versions - move the folder rather than delete - so it can be moved back to the installation location later

**Step 3**: Move (or copy) your backed up installation folder to this location. For example, copy

```powershell
c:\certdog.bak
```

to

```powershell
c:\certdog
```

**Step 4**: Start the services

