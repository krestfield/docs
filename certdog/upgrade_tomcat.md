---
layout: default
title: Upgrading Tomcat
parent: Certdog
nav_order: 111
---

# Upgrading Tomcat

You will only need to perform this step when instructed to by Krestfield support. If unsure contact [Krestfield Support](mailto:support@krestfield.com) 

<br>

### Steps

1. Download the upgrade script from here and copy to your installations ``.\certdog\install`` folder

2. Open a PowerShell window as Administrator, navigate to ``.\certdog\install`` and run:

```	
.\upgrade-tomcat.ps1
```

<br>

The latest Tomcat version will be downloaded and installed:

```
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
A backup of the previous Tomcat installation is located at: C:\certdog\install\..\tomcat.bak.20260505-1552
```

<br>

### Rollback

If any errors do occur then the upgrade may be rolled back. To do this, stop the certdog service. Delete the ``.\certdog\tomcat`` folder. Note the backup location (e.g. ``C:\certdog\install\..\tomcat.bak.20260505-1552``) and rename to ``.\certdog\tomcat``

Start the certdog service.



