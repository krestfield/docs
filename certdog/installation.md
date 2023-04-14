---
layout: default
title: Windows Installation
parent: Certdog
nav_order: 5
---

# Certdog Windows Installation

> From version: 1.8.0

<br>

The following steps outline the steps required to install the Certdog on a single system

If the pre-requisites are in place, the entire installation should not take more than 10 minutes  

<br>

If you don't want to read any details  right now and just want to quickly download to try things out - see the [Quick Installation Guide](quick_installation_guide.html) or the [Demo Quickstart](demo_quickstart.html) (which will install with default login details, for testing purposes)

<br>

### Pre-requisites

The system may be installed on the following operating systems:  


* Windows Server 2016

* Windows Server 2019

* Windows Server 2022

* Windows 10/11 [^1]

<br>

The following components are required:

* .NET 4.8 Runtime

* Visual C++ Runtime (this will be installed by the installer if not present)

<br>

You must have local Administrator privileges on the system

<br>

It is recommended to install on a clean system. But if this is not possible the system must not already have an instance of MongoDB running as this will conflict with the standard installer. If you wish to use an existing MongoDB instance, contact support@krestfield.com for details




### 1.  Download the Installer

See [here](download-locations.html) for download locations

<br>

### 1.1 Unzip

Unzip this to a location on the target machine. E.g.

`````powershell
c:\certdog
`````

But you can unzip to a location of your choice e.g.

```powershell
f:\apps\certdog
```

```powershell
c:\program files\krestfield\certdog
```

<br>

Open a PowerShell prompt as **Administrator** and navigate to this folder e.g.

```powershell
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\WINDOWS\system32> cd "C:\certdog"
PS C:\certdog>
```

<br>

Run ``dir`` and check the file structure looks something like the following:

```powershell
    Directory: C:\Program Files\Krestfield\certdog


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        06/01/2021     17:46                bin
d-----        05/01/2021     16:01                config
d-----        08/01/2021     11:27                install
d-----        07/01/2021     15:22                java
d-----        07/01/2021     15:22                logs
d-----        06/01/2021     15:48                tomcat
```

If you don't see the ``install`` directory, the unzipping process may have failed. Check that you have the correct permissions, then delete the *certdog* folder and attempt the unzip process again

<br>

### 2. Run the Installer

The installer may be run interactively, where you specify items as required. Or you may simply provide all of the required information as parameters to the script

Whichever is chosen, the following information will be required:  

* The Database User Admin Account Password
  * This account is the main database administrator and is used by the installer to create the other initial database accounts required by the system
  * You will not normally need to use this account on a day-to-day basis but you must retain the details  
  * If you wish to manually configure the database later (for example if all user accounts were lost), these credentials will be required
  * This can be entered when prompted or provided to the install script with the ``-dbAdminPassword`` parameter
* First Admin User Details
  * The account details for the first user that will log into the system,. They will be configured as an administrator
  * As well as a username and password, you will be required to enter an email address. All certdog user accounts require an associated email address to which notifications from the system may be sent
  * You may provide these details interactively or supply them as the following parameters to the script:``-firstAdminUsername``, ``-firstAdminPassword``, ``-firstAdminEmail``
* Network Details
  * The listening IP address and port number that the service will listen on
  * These can be provided to the script using the ``listeningIpAddress`` and ``listeningPort`` parameters
* Whether to install the ADCS Agent or not
  * This can be provided as the following switch ``-installAdcsAgent``
* Acceptance of the End User License Agreement
  * This can be accepted by providing the following switch ``-acceptEula`` to the script

<br>

From the PowerShell prompt, navigate into the ``install`` directory and either just run the ``.\install.ps1`` script and follow the prompts:

```powershell
PS C:\certdog> cd install
PS C:\certdog\install> .\install.ps1
```

Or run with the required parameters:  

```powershell
.\install.ps1 -acceptEula -dbAdminPassword $dbPassword -firstAdminUsername $adminUsername -firstAdminEmail $adminEmail -firstAdminPassword $adminPassword -listeningIpAddress 0.0.0.0 -listeningPort 443 -installAdcsAgent
```

You can set the required parameters mentioned above as follows:

```powershell
$dbPassword='password'
$adminUsername='admin'
$adminEmail='admin@nowhere.com'
$adminPassword='password'
```

Note: If you see the message ``Do you want to run software from this untrusted publisher?`` type **A** to always run. The scripts are signed with a publicly trusted CA, but depending on your security settings, there may still be a requirement to recognise the signer

<br>

If  your system does not have the Visual C++ Redistributable packages installed, this installer will begin. Complete this installation and when complete, return and re-start the ``.\install.ps1`` script

<br>

If  you do not have the .NET 4.8 Runtime installed, the installer will recognise this and end. Install the .NET 4.8 Runtime then restart the ``.\install.ps1`` script

<br>

The installer will start and display some initial information. e.g.

```powershell
Krestfield Certdog Setup Version 1.8
====================================

End User Agreement (EULA)
The EULA for this software can be obtained from the following location:
https://krestfield.s3.eu-west-2.amazonaws.com/certdog/KrestfieldCertdogEULA.pdf
By continuing and installing the software you accept the terms of this license agreement

...
```

Download and read the EULA and if happy to accept the agreement, type ``y`` to proceed with the install

<br>

If the script has been run without any parameters then follow the prompts when prompted  

If the script has been run with parameters the installer will run through the process without any prompting

<br>

At the end of installation you should see a message as follows:

<img src=".\images\installer_end.png" alt="End of Installation" style="zoom:80%;" />

Record the database administrator account details, including the username displayed and the password you provided (either interactively or as the ``-dbAdminPassword`` parameter)

The Master Secret is a top level secret that is used to protect keys held within the system. It is initially saved to a file (as specified in the output). This file is encrypted under the current user's account to initially protect others from accessing it. However, it is **strongly recommended** that it is saved somewhere secure and the file removed

You may need this secret if you re-install the main Certdog service, change the account the service runs under or attempt to start individual services manually. Normally, after install it is not required, but if lost any credentials stored within the system will be unrecoverable

<br>

### 3. Verify the Installation

Sometimes the Certdog service takes a while to initialise. In the first instance check the Services snapin and search for the following services and check they are running

* Krestfield Certdog Service 

* Krestfield Certdog Database

If not, attempt to start manually

<br>

If the services are not starting, check the installation log files for any errors

* installlog.out
* installlog.txt

If no errors were shown during the installation these files should just contain audit information

<br>

From the PowerShell prompt, navigate to the ``..\bin`` folder and type ``.\is-db-running.ps1``:

```powershell
PS C:\certdog\install> cd ..\bin
PS C:\certdog\bin> .\is-db-running.ps1
Database is running
```

The message ``Database is running`` should be seen  

Then type, ``is-api-running.ps1``  

```powershell
PS C:\certdog\bin> .\is-api-running.ps1
Testing https://127.0.0.1/certdog/api...
API is running
```

The message ``API is running`` should be seen  

If either the database or API are not running, see the Troubleshooting guide [here](install_troubleshooting.html)

<br>

Next, open a browser and navigate to ``https://[Your IP Address]/certdog``. Note: Internet Explorer is not supported

Where ``[Your IP Address]`` is the address chosen during the installation e.g.

``https://127.0.0.1/certdog``

You should see a warning such as:

<img src=".\images\sslconnectionerror.png" alt="image-20210108155429427" style="zoom:67%;" />

This is because we have not yet configured a valid SSL certificate.  For now, click **Advanced** then click **Continue to 127.0.0.1 (unsafe)** 

You should see the login screen:

<img src=".\images\login.png" alt="image-20210325144153311" style="zoom:67%;" />

Enter the **username** and **password** for the First Admin User that you provided during the installation and click **Login**  

You should be logged in OK.  The initial view will be ***Certificates***, but at this stage there are none to show    

A successful login indicates that the installation was completed OK  

<br>

### 4. SSL Configuration

By default an a test SSL certificate protects the system using the default 127.0.0.1 IP address  

This certificate will not be trusted by your system. You will see warnings when accessing the application via browser and REST API calls may fail  

For test purposes you may continue to use the provided SSL certificate. To enable trust double click the following certificate:  

``[Install Dir]\config\sslcerts\dbssl_root.cer``  

<img src=".\images\def_ssl_root.png" alt="image-20210108162250620" style="zoom:67%;" />

Click Install **Certificate**... and select **Local Machine**

<img src=".\images\root_cert_store.png" alt="image-20210108162426401" style="zoom:67%;" />

Select **Place all certificates in the following store** and browse to **Trusted Root Certification Authorities**, click **Next** and then **Finish**

Finally, click **Yes**

If you now close the browser, re-open and navigate to https://127.0.0.1/excert/ui the warnings should be gone

Note: This is a test certificate and should not be trusted in a production environment. You should still continue to create a valid SSL certificate as described [here](configure_server_ssl.html)

<br>
### Windows Services

**Database Service**  

This service will be installed by the install script

This service is the database and appears in the services snapin as **Krestfield Certdog Database**

<br>

**Application Service**  

This service will be installed by the install script but can also be installed manually by running the .msi installer separately. This .msi installer is located here:   

`` [Install Folder]\install\bin\InstallCertdogService.msi``  

This service starts and stops the system  

In the services snapin, this service is called **Krestfield Certdog Service**

<br>
**AD Certificate Services Agent**  

This service interfaces with your Microsoft ADCS instance.  More details on this service can be found [here](adcsdriver.html)  

In the services snapin, this service is called **Krestfield Adcs Driver**



[^1]: If installing on Windows 10 and you require access to a Microsoft ADCS Certificate Authority the RSAT (Remote Server Administration Tools) for Windows 10 are also required  

<br>

<br>

<hr>

#### Sample Installation Output

```powershell
Krestfield Certdog Setup Version 1.8
====================================

End User Agreement (EULA)

The EULA for this software can be obtained from the following location:

https://krestfield.s3.eu-west-2.amazonaws.com/certdog/KrestfieldCertdogEULA.pdf

By continuing and installing the software you accept the terms of this license agreement

Type 'y' to accept and continue, any other key to reject: y


Installing...

This script will now install the Certdog system on this machine

Downloading java...Please wait (this may take several minutes)
Checking hash...
Hash verified OK
java downloaded OK
Unzipping...
java unzipped OK
Registering location..
Java installation complete..


Downloading database...Please wait (this may take several minutes)
Checking hash...
Hash verified OK
database downloaded OK
Unzipping...
database unzipped OK

Database User Admin Account Setup
---------------------------------

This is the database administrator account
It will be used to create other database users and configure their access
Record this account's details as you may need it to manage user accounts in the future

The username for this account is: certmanadmin

You must provide a password
Note that the password for this account cannot contain '@' or ':' characters

Please enter the password for this account: ********
Please confirm the password for this account: ********


Configuring database...

The Krestfield Certdog Database service is starting.
The Krestfield Certdog Database service was started successfully.

Configuring authorisation and restarting...

The Krestfield Certdog Database service is stopping.
The Krestfield Certdog Database service was stopped successfully.

The Krestfield Certdog Database service is starting.
The Krestfield Certdog Database service was started successfully.



First Admin User Account Setup
------------------------------

This is the account for the first administrator

This user will be able to login to the UI (or API) as an administrator and create other users

Enter the username: krestfield
Enter the email address: support@krestfield.com
Please enter the password: ********
Please confirm the password: ********

Database and accounts have been configured

If there are any issues, check the log files installlog.out and installlog.txt for errors

You can re-run this script but should first reset the database by running reset-db.ps1


The interface that the application will listen on must now be set
For local testing the loopback (127.0.0.1) interface can be used
If you want to access the UI and API from other machines, choose another interface/IP Address
Or select all (0.0.0.0) to listen on all available interfaces

Available interfaces
--------------------
  1. 10.0.2.4
  2. 127.0.0.1
  3. 0.0.0.0 (Listen on all)

What interface do you wish the application to be available on (Enter 1 to 3): 2

What port do you wish the application to listen on (443):

Selected interface:  127.0.0.1:443

Updating configuration...
Configuration complete...


Installing Application Service
------------------------------

Installing the Certdog Service from C:\certdog\install\bin\InstallCertdogService.msi
Service installed OK

Starting Certdog Service

A Master Password is required to start this service the first time
Store this password securely as it may be needed if changes are made to the configuration

Please enter the master password: ********
Please confirm the master password: ********

Starting the service...

Service started OK


AD Certificate Services Agent
-----------------------------

Do you wish to install the ADCS agent on this machine (y/n)?: y

Installing Adcs agent from C:\certdog\install\bin\AdcsDriverInstaller.msi
Services installed OK

Configure Adcs Service

Starting the service...

Service started OK
If the database URL changes, re-run this script

Checking Installation...
Database is running
Testing https://127.0.0.1/certdog/api...
API is running

Installation is complete
```



