---
layout: default
title: ADCS Driver
parent: Certdog
nav_order: 5
---
# Certdog ADCS (Microsoft CA) Driver

This component is the interface to ADCS (Active Directory Certificate Services)  

You have the option of installing this together with the other components but it can also be installed separately and/or on other machines  

Multiple instances of the driver can be installed in the same and different domains  

<br>

## Requirements

- Windows Server 2016, 2019
- .NET Framework 4.8 Runtime
- A service account  

The server hosting the driver must be in the same domain as the Microsoft CA you wish to obtain certificates from  

You will normally require a service account with the required permissions to access your Microsoft CA. See the [Service Account](#service-account) section below  

If you are running multiple drivers or the driver is not installed on the same machine, ensure that port 27017 is open to wherever the database is hosted i.e. the server hosting the database must allow incoming connections on port 27017 from the machine hosting the ADCS Driver  

<br>


## Installation

1. From the ``.\certdog\install`` directory, run:
   ``install-adcs-service.ps1``
   
2. The installer will attempt to locate the database URL but if prompted, you must enter this

3. The full URL starts: ``mongodb://certmanuser...``

4. If you do not know what this value is, in the main installation, locate this file:

5. ``.\certdog\config\application.properties`` the database URL is referenced by the ``spring.data.mongodb.url`` property e.g.

```properties
spring.data.mongodb.uri=mongodb://certmanuser:ARBaVNlOkeTsLPLs@127.0.0.1/certman?tls=true
```

In this case the URL that must be entered is:

```properties
mongodb://certmanuser:ARBaVNlOkeTsLPLs@127.0.0.1/certman?tls=true
```

This URL contains sensitive information. Do not store unprotected. Once entered the ADCS driver will store this value encrypted

---

Monitor the system's Event Log for entries in the Application log with Source: **CertdogAdcsDriver**  

If you see entries such as the following:

```
Unable to connect to database at 127.0.0.1/certman?tls=true Details: Connection  to database is down. Check URL and connectivity - including any whitelists Will  try again in 30 seconds
```

This indicates that either the database URL was not set correctly or the TLS certificate is not trusted  

If the UI is working OK then the most likely cause is that the TLS certificate is not trusted. If you are still using the default certificate bundled with the system, you can (temporarily) install this certificate:  

   ``.\certdog\config\sslcerts\dbssl_root.cer``  

Into the **Local Machine** **Trusted Root Certification Authorities** store. Then restart the ADCS service

If this does not resolve the issue, check that the main server's 27017 port can be accessed from this location and the database URL entered is correct

<br>

### Upgrading

* Start **Apps and Features**. Locate the **Certdog ADCS Driver** and select **Uninstall**

* As an Administrator, run the ``AdcsDriverInstaller.msi``file from the ``\install\bin`` directory of the new version (e.g. ``c:\certdog\install\bin\AdcsDriverInstaller.msi``)

  This will install the new version of the driver  

If after the upgrade, the driver shows as *unregistered* in the Certdog UI (under the *Agents* menu), re-register following the steps in [Registering the service](#registering-the-service) below

<br>

## Service Account

The Microsoft CA requires that the certificate requestor has the required permissions on the CA and certificate template in order to be issued with a certificate  

See [here](https://krestfield.github.io/docs/pki/setting_adcs_template_permissions.html) for details around configuring permissions on the CA and templates  

To configure these permissions on the ADCS Driver, you have the following options:

<br>

**<u>1. Configure a Credential from within Certdog</u>**

By default, the ADCS Driver runs as service (called *Krestfield Adcs Driver*) under the LOCAL SYSTEM account. As part of a certificate request, Certdog instructs the driver what account to use to request the certificate from the CA  

This account to be used to request the certificates is specified in Certdog as a Credential and when creating the [Certificate Issuer](https://krestfield.github.io/docs/certdog/create_adcs_certificate_issuer.html) you select this Credential from the drop down  

The account must be a service account (configured with the *logon as a service* and *deny local logon* rights) and must have the correct permissions on the CA and template in order to be able to obtain a certificate    

<br>

**<u>2. Configure the ADCS Driver to run under a service account</u>**

Alternatively you may configure the ADCS Driver to run under a specific account and configure your [Certificate Issuer](https://krestfield.github.io/docs/certdog/create_adcs_certificate_issuer.html) within Certdog to not specify a credential - but to use the account the local agent (i.e. the ADCS Service) is running under  

To configure the driver to run under another account, from the services snapin, locate the *Krestfield Adcs Driver* service and enter the details for the account on the *Log On* tab. You will need to enter the account's username and password at this point 

This account must still be a service account (configured with the *logon as a service* and *deny local logon* rights) and must have the correct permissions on the CA and template in order to be able to obtain a certificate    

<br>

**<u>1. Run under the LOCAL SYSTEM (Computer) account</u>**

The final option does not require a specific service account but this will only work correctly if your CA and template are configured to allow the Computer Account (where this ADCS Driver is running) to obtain certificates

In this case the Krestfield Adcs Driver service remains running under LOCAL SYSTEM and your [Certificate Issuer](https://krestfield.github.io/docs/certdog/create_adcs_certificate_issuer.html) in Certdog is configured to use *No Credential (use local agent account)* 

This means the ADCS Driver will make requests to the CA based on the account it is running under, which is the LOCAL SYSTEM (Computer) account

<br>

If you switch between these options (e.g. you decide to specify a credential within Certdog rather than run the service under a service account) the agent must be re-registered (see below)

<br>

### Registering the Service

On initial install the ADCS Driver will be configured with the required settings (database URL) so there is nothing more to do 

But, if the account the driver is running under changes, the agent will lose these details (as they are protected under the account the service runs under)  

To reset, perform the following:

* Open a PowerShell window as Administrator and navigate to the ``.\install `` directory e.g. ``c:\certdog\install`` and run the following command:  ``.\configure-adcs-service.ps1``

* Next, from Certdog, select the **Agents** menu. The Agent entry may disappear then (when the page is refreshed after a minute or so) re-appear as un-approved. This is due to the agent going through the initialisation and key-exchange process with Certdog. Select the entry and click **Approve**  

* If you have existing Microsoft CA Certificate Issuers configured, for each one, click **Edit** and re-select the *Permitted Agents* (which in most cases will just be the one agent that was just approved)

<br>

## Configuration in Certdog

Once the service has been successfully installed to enable it for use within Certdog it must be approved as follows:  

Login to the UI and select **Administration > Agents** from the menu  

You should see an entry for the agent. It will be named the FQDN of the machine it resides on  

Click this entry and select **Approve**  

The agent will now be able to process requests  

<br>

Note that when configuring a Certificate Issuer for a Microsoft CA you must select the agent that you want to process requests for that CA

<br>

## Additional File Logging

To enable more logging, set the following environment variable to true:

``ADCS_DRIVER_FILE_LOGGING``

e.g.  
![image-20201222143624266](.\images\loggingenvvar.png)

And restart the Krestfield Adcs Driver from the services snapin

The log file will be written to:

``Environment.SpecialFolder.CommonApplicationData \Krestfield\AdcsAgent``

Which is here in Windows Server 2019

``C:\ProgramData\Krestfield\AdcsAgent\log.txt``



Note: This log provides debug level, verbose output and may be useful for tracing issues but the log file will continue to grow.  You should therefore, switch this level of logging off when not required

 <br>

## Threading

By default, the driver creates a number of threads (typically 5) to process certificate requests and this value should not be changed  

In some high volume/performance scenarios you may want to change or experiment with this value  

To change this value, set the following environment variable to the number of threads required:  

``ADCS_DRIVER_THREADS``

e.g.  
![image-20201222143722766](.\images\threadsenvvar.png) 

Restart the Krestfield Adcs Driver from the services snapin  

 <br>





