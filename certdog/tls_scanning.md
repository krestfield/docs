---
layout: default
title: Running a TLS Scan
parent: Certdog
nav_order: 16
---
# Running a TLS Scan

  <br>

TLS certificates can be discovered from end points and imported into the certdog inventory. This enables searching and expiry monitoring of those certificates. This can also assist with locating unknown or unexpected certificates (including self-signed instances).

The scan operates via a PowerShell script that can be run within your own infrastructure. The script requires no special privileges, is signed and only requires network access. The script will perform the scan and upload discovered certificates to certdog. 

<br>

<br>

## Pre-Requisites

* A server in your environment that has  access to the end points (and ports) you wish to scan

* The server must have access to the certdog server over port 443

* The ability to download and run the PowerShell script



The script will require the following information:

- The **certdog server name or IP address**

  e.g. certdog.internalserver.local or 192.168.55.142 etc.

- An **API key** for the script to be able to authenticate to certdog

- The **IDs of the user and team** we want the imported certificates to be associated with

- The **server names or IP addresses** to scan

  - This can be a set of individual IP addresses or server names or a range, subnet or CIDR block of IP addresses


 We will see how to obtain these values in the next section.

<br>

<br>

## Certdog Setup

First, decide what user and team you wish the certificates to be associated with. 

Either choose an existing user or create a new user for this specific purpose. For example. you may create a Team that has no permissions on any Certificate Issuers and a new user that is a member of this team. This will give this *certificate import* user very limited privileges - only permitted to import certificates and then view these certificates.  

To setup a dedicated user and team, follow Appendix A below.   

<br>

#### Obtain the User and Team ID

From certdog, as an Administrator, navigate to **Users** under the *ADMINISTRATION* section. Select the chosen user and click **View/Edit**. 

The URL in the browser will contain the ID. This is the number at the end of the URL. 

E.g. When viewing a user's details, the URL may display something like this:

```
https://certdog.net/certdog/ui/#/administration/edituser/673de9bcfac0d02ac6ced94d
```

In this case the user ID is: ``673de9bcfac0d02ac6ced94d``

Do the same for Team you wish the certificates to be associated with. Note: The user must be a member of the team selected.

You can also use the PowerShell module to obtain the user ID. See [Appendix C]()

<br>

#### Obtain an API Token

As an Administrator navigate to **Users** under the *ADMINISTRATION* section. Select the chosen user and click **View/Edit**. 

In the *API Token* section, select the time you wish this API key to remain valid for. If you are running a one-time scan, you can keep this value short (e.g. 1 Hour). If running multiple (as part of a scheduled task) select a longer value.

Click **Generate Token** and click on the **produced token** to copy.

Retain the value as it will be required by the PowerShell script.

<br>

#### Certdog Server Name

This is simply the hostname or IP Address where the certdog server resides. E.g. ``certdog.krestfield.local`` or ``192.168.55.42`` 

<br>

#### Scan End Points (Server Names or IP Addresses)

Decide what end points you wish to scan. Noting that the end points must be reachable by the script over the ports required.  

End points may be provided as hostnames, IP addresses or a range of IP addresses. Ranges can be provided as a start and end IP address or a range specified in CIDR notation.

<br>

<br>

## Running the Script

Download the PowerShell script from here and place in a suitable location on your chosen server.

Ensure you have the following information ready:

* The certdog server name

* The user and team IDs

* The server list or IP addresses to scan

* The API token



The parameters to the script are:

- certdogServer
  - Mandatory. The certdog server name e.g. ``certdog.krestfield.local``
- userId
  - Mandatory. The user ID e.g. ``673de9bcfac0d02ac6ced94d``
- teamId
  - Mandatory. The team ID e.g. ``473df9bce6c0d02ac6cedd49``
- ports
  - If omitted defaults to 443. Otherwise a single or multiple ports (comma separated) can be specified e.g. ``80,8080,443,444``
- apiToken
  - If omitted you will be prompted to enter the API token. It will not be displayed on the screen if entered in this way.
- ignoreSslErrors
  - Switch. If the server running the script does not trust the TLS certificate protecting the certdog API, include this switch e.g. ``-ignoreSslErrors``
- additionalText
  - Additional text that you wish to be stored along side the certificate e.g. ``From SCAN of the 10.54.24.0/24 subnet``



To specify a start and end IP address. Use the ``ipStart`` and ``ipEnd`` parameters:

- ipStart
  - The starting IP address e.g. ``192.168.55.0``
- ipEnd
  - The ending IP address e.g.  ``192.168.55.128``



To specify a single or list of server  names or IP addresses use the ``serverList`` parameter:

- serverList
  - The servers to be scanned. Specified as IP addresses or hostnames e.g. ``google.com,microsoft.com,amazon.co.uk`` or ``192.168.55.10`` or ``krestfield.com``



If you wish to specify a subnet, use the ``ipAddress`` and ``subnetMask`` parameters:

- ipAddress
  - The IP address e.g. ``192.168.55.0``
- subnetMask
  - The subnet mask. Do not include the ``/``, just specify the number e.g. to specify the ``/24`` range just provide``24``



Open a PowerShell window and navigate to where the script is located.

Enter ``.\tls-scan.ps1`` and provide the required parameters then click Enter. E.g.:

```
tls-scan.ps1 -certdogserver 127.0.0.1 -userid 673de9bcfac0d02ac6ced94d -teamid 473df9bce6c0d02ac6cedd49 -ipstart 192.168.100.1 -ipend 192.168.100.255 -ports (443,80)
Enter API Token: *******
```

If you haven't specified the ``apiToken`` parameter you will be asked to enter this now.

The script will scan through the range of servers or IP addresses, report when it locates a certificate and send to certdog:

```
Trying IP Address 142.250.187.94
Trying IP Address 142.250.187.95
Trying IP Address 142.250.187.96
Found CN=*.google.com at 142.250.187.96
Trying IP Address 142.250.187.97
Found CN=*.googleusercontent.com at 142.250.187.97
Trying IP Address 142.250.187.98
Found CN=*.g.doubleclick.net at 142.250.187.98
Trying IP Address 142.250.187.99
Found CN=google.com at 142.250.187.99
Trying IP Address 142.250.187.100
```

When complete, go back to certdog to view the imported certificates.  

You will be able to search for the certificates by Team name, User name or even by the text provided via the ``additionalText`` parameter - which will be stored in the certificate's ``Extra Information`` field.

<br>

<br>

### Appendix A: Creating a dedicated User and Team

See here: [https://krestfield.github.io/docs/certdog/teams.html](https://krestfield.github.io/docs/certdog/teams.html) for details on how to add a new team.  

Do not set the team to be an Administrator and there is no need to specify any Certificate Issuers. The Team will not need any specific permissions.

See here: [https://krestfield.github.io/docs/certdog/users.html](https://krestfield.github.io/docs/certdog/users.html) for details on how to add a new user. Add this user to the team created above. 

<br>

<br>

### Appendix B: Installing PowerShell on Non-Microsoft Operating Systems

Instructions on how to install PowerShell on other operating systems can be found here:

https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell?view=powershell-7.4

<br>

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

