---
layout: default
title: IIS PowerShell Script
parent: Certdog
nav_order: 13
---

# Certdog IIS PowerShell Script

This script can be used to generate certificates, bind them to IIS sites and then automatically renew  

You can obtain the script from github [here](https://github.com/krestfield/certdog-iis)



## Pre-requisites

An instance of certdog is required. A Docker image of certdog can be obtained from here:  

[https://hub.docker.com/r/krestfield/certdog](https://hub.docker.com/r/krestfield/certdog)

You may also install the application locally. Contact [Krestfield Support](mailto:support@krestfield.com) to obtain the installer



## Overview

The script can generate a local CSR (stored in the Local Machine certificate store), with additional SANs (subject alternative names), if required  

This can be processed by the certdog application, and the issued certificate installed  

IIS bindings can then be updated with the new certificate details  

The script can also create a scheduled task which will, by default, run every day and check the expiry of the certificates bound to the bindings selected. When nearing expiry, the certificate will be automatically renewed and the relevant IIS binding updated



## Get the Script

The free version is available [here](https://github.com/krestfield/certdog-iis)

You should have the following files:

* certdog-iis.ps1

* settings.json

Save these to a local folder on the machine hosting the IIS instance



## Settings (settings.json)

Settings are stored within the ``settings.json`` file. Sample contents:

```json
{
	"certdogUrl" : "https://127.0.0.1/certdog/api",
	"certIssuerName" : "Test CA",
	"renewalDays" : 30,
	"csrKeyLength" : 2048,
	"csrHash" : "sha256",
	"csrProvider" : "Microsoft RSA SChannel Cryptographic Provider",
	"csrProviderType" : 12,
	"exportable" : "FALSE",
	"eventLogId" : 5280,
	"errorLogId" : 5281
}
```

* certdogUrl

The URL of the certdog installation's api. If using the Docker image the default setting will operate OK

* certIssuer

The name of the certificate issuer as configured in certdog (e.g. Certdog TLS Issuer)

* renewalDays

When the script is run with the *-renew* option this value will be used when deciding whether to renew certificates or not

If a certificate is expiring in *renewalDays* (or fewer) the renewal process will initiate

* csrKeyLength

When a new CSR is generated (when creating a new or renewing a current certificate), this key length will be used

* csrHash

The hash used to generate the CSR

* csrProvider

This is the Microsoft provider that will be used to generate the CSR

* csrProviderType

This depends on the csrProvider selected and must match. See [here](https://docs.microsoft.com/en-us/dotnet/api/system.security.cryptography.cspparameters.providertype?view=net-5.0) for more information

* exportable

If TRUE then it will be permitted for the private key of the issued certificate to be exported (e.g. as a password protected PFX/PKCS#12 file)

* eventLogId

This is the Event Log ID that will be assigned to entries the script adds. If monitoring events, you may need to note this value. It can also be updated here

* errorLogId

This is the Event Log ID that will be assigned to entries the script adds when errors occur. If monitoring error events, you may need to note this value. It can also be updated here



## Running

Open a PowerShell window as Administrator



 Simple run options:

```powershell
.\certdog-iis.ps1 -new
```

This will prompt for all information including the certdog login as well as the binding and certificate details. See the sample output below for more details



To provide the certdog authentication details (and not be prompted for username/password), run:

```powershell
.\certdog-iis.ps1 -new -username [certdoguser] -password [certdogpassword]
```

  

 Once the above has been performed the script saves the required information. Running:

```powershell
.\certdog-iis.ps1 -renew
```

Will check and process any renewals required for the sites and bindings configured when the ``-new`` switch was used

  

As above, this can be run with the username and password options:

```powershell
.\certdog-iis.ps1 -renew -username [certdoguser] -password [certdogpassword]
```

 



 To list what bindings are being monitored:

```powershell
.\certdog-iis.ps1 -list
```

   

 To create a scheduled task that runs the ``.\certdog-iis.ps1 -renew`` script daily, run

```powershell
.\certdog-iis.ps1 -taskonly
```



To override the certdog URL as specified in the ``settings.json`` file, use ``-certdogUrl`` e.g.

```powershell
.\certdog-iis.ps1 -new -certdogUrl https://certdog.org.com/certdog/api
```

   

To ignore any SSL errors (if the certdog URL is not protected with a trusted cert), use ``-ignoreSslErrors`` e.g.

```powershell
.\certdog-iis.ps1 -new -ignoreSslErrors
```



   





## Logging

When configuring the script (i.e. running with the ``-new`` option), all output is to the console  



When checking for renewals (when running with the ``-renew`` option) output is to a log file and the Windows Event Log. This is because this option will usually be run from a Scheduled Task (or other scheduler)

The log files are contained in a directory called ``.\logs`` created at the same location as the script. Each log file is named:

``YYYYMMDDTHHMMSS_certdogrenew.log``

e.g.

``20210509T140645_certdogrenew.log``



Entries are added to the Windows event log. With the ID (``eventLogId``) as specified in ``settings.json``. If an error occurs an error log entry will be added with the ID ``errorLogId`` - again, this is specified in ``settings.json``



## Credentials

The script requires the certdog credentials. That is the username and password of a user who has access to the Certificate Issuer configured in certdog  

These credentials can be saved by the script as secure strings which are tied to the user account on the machine running the script. This means that the ``-renew`` option can be run without requiring the username or password to be specified. And this is how the script will be called from the Scheduled Task  

Note that for this to work, the account the scheduled task runs under must be the same as the account the scheduled task runs under. This could be your own account or a service account  

If you wish to run the scheduled task under the LOCAL SYSTEM account you may use [pstools](https://docs.microsoft.com/en-us/sysinternals/downloads/pstools) to start a powershell as LOCAL SYSTEM, then set the credentials by running the following:

```powershell
.\certdog-iis.ps1 -setcreds
```

These will then be accessible by the LOCAL SYSTEM account



## Tips

It is a good idea to test that the renewal actually works as expected. This is easy to confirm with certdog as we can create an internal CA with a short lifetime certificate profile  for testing. Then we can set the ``renewalDays`` period to be short and confirm everything works as expected  

1. Create a local certificate issuer, if not already done so. See the guide [here](https://krestfield.github.io/docs/certdog/create_local_certificate_issuer.html). Create a profile which has a lifetime of 1 day
2. Update the ``settings.json`` file and set ``renewalDays : 1`` and the ``certIssuerName`` to whatever you have called the certificate issuer
3. Run ``certdog-iis.ps1 -new`` and create a new certificate, store the credentials and create a scheduled task
4. The task, by default, should run that night (or early next morning). You can run the task on demand before this. Monitor the Event Log for events from source ``certdog`` and event ID's as configured in ``settings.json`` (these are 5280 and 5281 by default)
5. If everything gets renewed OK you know the accounts etc. are all good
6. Now update ``settings.json`` to point to the chosen Certificate Issuer and update the ``renewalDays`` to be a reasonable time before your certificates expire and you want them renewed

