---
layout: default
title: Running a JKS Scan
parent: Certdog
nav_order: 128
---
# Running a JKS (Java Key Store) Scan

  <br>

Certificates can be discovered and imported into the certdog inventory from JKS files residing on Linux environments.

This can be done by running a local PowerShell script which will analyse JKS files residing on the remote servers.

<br>

## Overview of Operation

The PowerShell script uses the SSH protocol to run a remote script on each of the selected Linux servers. This script attempts to extract certificates from JKS files.  

It can target individual JKS files or scan a directory and all sub -directories.

The script running on the remote server will call the certdog API to import any discovered certificates.

<br>

## Pre-Requisites

* Permissions to execute PowerShell scripts. Normally the PowerShell script is run from the certdog server itself, but it can be run from any server.
  
* SSH is enabled on the remote servers.
  
* The remote servers can be accessed by the PowerShell script.
  
* The remote servers can access the certdog API over port 443.
  
* You have the account details with permissions to access the remote servers.

* You have the password to access the target JKS file(s).

* The remote servers require curl and keytool to be available.

<br>

The script will require the following information:

- Remote IP Addresses (of the Linux servers)

- The Username and Password that will be used to access these remote Linux server(s)

- The URL of the certdog server

- An API key for the script to be able to authenticate to certdog

- The IDs of the user and team we want the imported certificates to be associated with

- The location of the folder or JKS filename

- The password to access the target JKS files

  

We will see how to obtain these values in the next section.

<br>

<br>

## Quick Start

Download the script from [here](https://krestfield.s3.eu-west-2.amazonaws.com/certdog/scripts/certdog-jks-scan.zip)

Save the script and unzip the contents into a folder. 

Edit ``run-jks-scan.ps1`` editing the values for:

* $remoteIps
  * The single or list of remote IP addresses for the Linux servers to be scanned
  * E.g. ``$remoteIps = @("192.168.50.1","192.168.50.1","192.168.50.3")``

* $jksFileOrFolder
  * The name of a JKS file or a folder. If a folder is specified it (and sub-directories) will be scanned for all *.jks files
  * E.g. ``$jksFileOrFolder="/home/user/apps/keys.jks"``

* $jksPassword
  * The password to access the JKS file(s)
  * E.g. ``changeit``

* $certdogAuthToken
  * See [Obtain an API Token](#obtain-an-api-token) on how to obtain this
  * E.g. ``$certdogAuthToken="eyJhbGciO...BLKIl-A"``

* $certdogApiUrl
  * The URL of the certdog server
  * E.g. https://certdog.server.com

* $certdogOwnerUserId
  * The ID of the user who will own the imported certificates. See [Obtain the User and Team ID](#obtain-the-user-and-team-id) on how to obtain this
  * E.g. `668f96118afa1d3f24016e59`

* $certdogOwnerTeamId
  * The ID of the team that will own the imported certificates. See [Obtain the User and Team ID](#obtain-the-user-and-team-id) on how to obtain this
  * E.g. ``668f95d78afa1d3f24016e56``

* $certdogExtraInfo
  * Text that will be added to the imported certificates to help locate them from searches. 
  * E.g. ``"Import of JKS files from dev servers"``

* $remoteMachineUsername
  * The username of an account on the remote Linux server with permissions to access the JKS files
  * E.g. ``linuxuser``

* $remoteMachinePassword
  * The password of the account above
  * E.g. ``password``

<br>

NOTE: It is not recommended to hardcode any sensitive values except for testing purposes. The ``run-jks-scan.ps1`` script has some recommendations for protecting these values.

<br>

Execute the ``./run-jks-scan.ps1`` script

The script will run and for each file a log file will be produced e.g. ``output-192.168.50.223.log`` which can be viewed to observe any errors.

<br>

### The jks-scan.ps1 Script

This is the main PowerShell script that is called from the ``run-jks-scan.ps1`` script mentioned above. It does not need to be called in that way and can be called from any other script/tool as long as it is provided with the required parameters.  

The script essentially performs three operations for each of the specified Linux servers:

1. Copy the ``jks-scan.sh`` script to the remote server's ``/tmp`` directory
2. Execute the script with the parameters provided (JKS file, password, certdog URL etc.)
3. Copy the produced log file back to the calling server

<br>

### The jks-scan.sh Script

This is a bash script. It performs the local interrogation of the JKS files. 

This script makes use of *keytool* and *curl*. These must be available on the remote Linux server.

If a single JKS file is provided, it processes that and ends. Otherwise, it will search for all JKS files at the folder specified (and sub-folders) and attempt to process all discovered JKS files.  

For each JKS file it extracts the aliases, and then for each alias the actual certificate data.  Keytool is used for this process.

This data is then imported to certdog via the REST API. Curl is used during this process.

A log file is produced, which the calling script will collect at the end of the processing.

<br>

## Certdog Setup

Decide what user and team you wish the certificates to be associated with. 

Either choose an existing user or create a new user for this specific purpose. For example. you may create a Team that has no permissions on any Certificate Issuers and a new user that is a member of this team. This will give this *certificate import* user very limited privileges - only permitted to import certificates and then view these certificates.  

To setup a dedicated user and team, follow Appendix A below.   

<br>

#### Obtain the User and Team ID

From certdog, as an Administrator, navigate to **Users** under the *ADMINISTRATION* section. Select the chosen user and click **View/Edit**. 

The user ID is displayed. You can click to copy this value.

<img src="./images/copy_user_id.png" alt="image-20250314115834215" style="zoom: 67%;" />



For older versions (1.11 and earlier) the URL in the browser will contain the ID. This is the number at the end of the URL. 

E.g. When viewing a user's details, the URL may display something like this:

```
https://certdog.net/certdog/ui/#/administration/edituser/673de9bcfac0d02ac6ced94d
```

In this case the user ID is: ``673de9bcfac0d02ac6ced94d``

Note this ID.

Do the same for the Team you wish the certificates to be associated with. Note: The user must be a member of the team selected.

You can also use the PowerShell module to obtain the user and team IDs. See [Appendix C]()

<br>

<br>

#### Obtain an API Token

As an Administrator navigate to **Users** under the *ADMINISTRATION* section. Select the chosen user and click **View/Edit**. 

In the *API Token* section, select the time you wish this API key to remain valid for. If you are running a one-time scan, you can keep this value short (e.g. 1 Hour). If running multiple (as part of a scheduled task) select a longer value.

Click **Generate Token** and click on the *Token* to copy it.

Retain the value as it will be required by the PowerShell script.

<img src="./images/image-20250314163205098.png" alt="image-20250314163205098" style="zoom:67%;" />

<br>

<br>

#### Certdog API URL

This is simply the hostname or IP Address where the certdog server resides. E.g. ``https://certdog.krestfield.local`` or ``https://192.168.55.42`` 

<br>

<br>

### Appendix A: Creating a dedicated User and Team

See here: [https://krestfield.github.io/docs/certdog/teams.html](https://krestfield.github.io/docs/certdog/teams.html) for details on how to add a new team.  

Do not set the team to be an Administrator and there is no need to specify any Certificate Issuers. The Team will not need any specific permissions.

See here: [https://krestfield.github.io/docs/certdog/users.html](https://krestfield.github.io/docs/certdog/users.html) for details on how to add a new user. Add this user to the team created above. 

<br>

### Appendix C: User and Team IDs

The user and team IDs can be obtained via the PowerShell module.

Open a PowerShell window as Administrator and navigate to where the certdog-module.psm1 file is located. If on the certdog server this will be ``[certdog install location]\bin`` e.g. ``c:\certdog\bin``  

Run the following commands to locate the user and team IDs:

```powershell
PS C:\certdog\bin> Import-Module .\certdog-module.psm1
PS C:\certdog\bin> login
Username: admin
Password: ********
Attempting login at: https://127.0.0.1/certdog/api
Authenticated OK
PS C:\certdog\bin> get-user -username cert-import

id                     : 673de9bcfac0d02ac6ced94d
email                  : cert-import@krestfield.com
username               : cert-import
group                  : USER
enabled                : True
teamsIds               : {673de985fac0d02ac6ced94b}
numFailedLoginAttempts : 0
userMessage            :
nextAllowedLogonTime   : 0
accountType            : 0
accountTypeStr         : Local
lastLoginTime          : 2024-11-21T11:22:57.888+00:00
lastLoginIpAddress     : 127.0.0.1
mustChangePassword     : False

PS C:\certdog\bin> get-team -name Cert-Import-Team

id                     : 673de985fac0d02ac6ced94b
name                   : Cert-Import-Team
description            :
internalGroup          : USER
adGroups               : {}
authorisedCas          : {}
adminUsernames         : {}
dontSendEmailsOnIssue  : True
dontSendReminderEmails : False
ipWhiteList            :
```

The IDs are displayed.

