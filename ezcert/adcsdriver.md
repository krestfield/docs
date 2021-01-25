---
layout: default
title: ADCS Driver
parent: EzCert
nav_order: 5
---
# EzCert ADCS Driver

This component is the interface to ADCS (Active Directory Certificate Services)  

You have the option of installing this together with the other components but it can also be installed separately and/or on other machines 

Multiple instances of the driver can be installed in the same domain



## Requirements

- Windows Server 2016
- Windows Server 2019
- .NET Framework 4.8 Runtime

The server hosting the driver must be in the same domain as the Microsoft CA you wish to obtain certificates from

Ensure that port 27017 is open to wherever the database is hosted i.e. the server hosting the database must allow incoming connections on port 27017 from the machine hosting the ADCS Driver. This is only required if the ADCS driver is being installed on a separate machine




## Installation

1. From the ``.\ezcert\install\install`` directory, run:
   ``install-adcs-service.ps1``
   
2. The installer will attempt to locate the database URL but if prompted, you must enter this

3. The full URL starts: ``mongodb://certmanuser...``

4. If you do not know what this value is, in the main installation, locate this file:

5. ``.\ezcert\config\application.properties`` the database URL is referenced by the ``spring.data.mongodb.url`` property e.g.

```properties
spring.data.mongodb.uri=mongodb://certmanuser:ARBaVNlOkeTsLPLs@127.0.0.1/certman?tls=true
```

In this case the URL that must be entered is:

```properties
mongodb://certmanuser:ARBaVNlOkeTsLPLs@127.0.0.1/certman?tls=true
```

This URL contains sensitive information. Do not store unprotected. Once entered the ADCS driver will store this value encrypted

---

Monitor the system's Event Log for entries in the Application log with Source: **EzCertAdcsDriver**  

If you see entries such as the following:

```
Unable to connect to database at 127.0.0.1/certman?tls=true Details: Connection  to database is down. Check URL and connectivity - including any whitelists Will  try again in 30 seconds
```

This indicates that either the database URL was not set correctly or the TLS certificate is not trusted  

If the UI is working OK then the most likely cause is that the TLS certificate is not trusted. If you are still using the default certificate bundled with the system, you can (temporarily) install this certificate:  

   ``.\ezcert\config\sslcerts\dbssl_root.cer``  

Into the **Local Machine** **Trusted Root Certification Authorities** store. Then restart the ADCS service

If this does not resolve the issue, check that the main server's 27017 port can be accessed from this location and the database URL entered is correct



## Configuration

Login to the UI and select **Administration > Agents** from the menu  

You should see an entry for the agent. It will be named the FQDN of the machine it resides on  

Click this entry and select **Approve**  

 The agent will now be able to process requests



Note that when configuring a Certificate Issuer for a Microsoft CA you must select the agent that you want to process requests for that CA

   

## File Logging

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

 

## Threading

By default, the driver creates a number of threads (typically 5) to process certificate requests. But this value can be tuned, if required

To change this value, set the following environment variable to the number of threads required:  

``ADCS_DRIVER_THREADS``

e.g.  
![image-20201222143722766](.\images\threadsenvvar.png) 

Restart the Krestfield Adcs Driver from the services snapin

