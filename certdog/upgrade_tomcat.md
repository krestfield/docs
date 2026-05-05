---
layout: default
title: Upgrading Tomcat
parent: Certdog
nav_order: 111
---

# Upgrading Tomcat

You will only need to perform this step when instructed to by Krestfield support. If unsure, contact us here: [support@krestfield.com](mailto:support@krestfield.com) 

<br>

### Steps

<u>Step 1</u>

Download the upgrade script [from here](https://krestfield.s3.dualstack.eu-west-2.amazonaws.com/certdog/scripts/upgrade-tomcat.zip), unzip and copy the .ps1 file to the following folder: ``.\certdog\install`` 

E.g.

```powershell
c:\certdog\install\upgrade-tomcat.ps1
```

<br>

<u>Step 2</u>

Open a PowerShell window as Administrator, navigate to ``.\certdog\install`` and run:

```	powershell
.\upgrade-tomcat.ps1
```

<br>

The latest Tomcat version will be downloaded and installed:

```powershell
PS C:\WINDOWS\system32> cd C:\certdog\install\                                                                                                                                     PS C:\certdog\install> .\upgrade-tomcat.ps1                                                                                                                                         Stopping Certdog service...
Downloading tomcat...Please wait (this may take several minutes)
Checking hash...
Hash verified OK
tomcat downloaded OK
Unzipping...
tomcat unzipped OK

Backing up current Tomcat installation to C:\certdog\install\..\tomcat.bak.20260505-1552 ...
Moving new Tomcat installation into place...
Copying configuration...
Copying webapps...
Starting Certdog service...

Tomcat upgrade complete.
A backup of the previous Tomcat installation is located at: C:\certdog\install\..\tomcat.bak.20260421-1252
```

<br>

### Rollback

If any errors do occur then the upgrade may be rolled back. To do this, stop the certdog service. Delete the ``.\certdog\tomcat`` folder. Note the backup location (e.g. ``C:\certdog\install\..\tomcat.bak.20260421-1252``) and simply rename to ``.\certdog\tomcat``

Start the certdog service.

<br>

### Cleanup

When satisfied that the installation is all working correctly you may delete the backup of the old Tomcat files. These are copied to the location output by the script e.g. ``C:\certdog\install\..\tomcat.bak.20260421-1252``

